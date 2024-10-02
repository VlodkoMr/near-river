#!/bin/bash

# Load environment variables from the specified file
set -a; source ".env"; set +a

# Remove carriage returns from environment variables (for Windows line endings)
for var in DB_CONNECTION SUBSTREAMS_API_KEY START_BLOCK END_BLOCK MAX_ARGS_LENGTH FILTERED_RECEIVER_IDS FILTERED_METHOD_NAMES; do
  eval "$var=\"\${$var//$'\r'/}\""
done

# Function to fetch the latest block number from the NEAR blockchain
get_latest_block() {
  curl -s https://rpc.mainnet.near.org \
    -d '{"jsonrpc":"2.0","id":"dontcare","method":"block","params":{"finality":"final"}}' \
    -H "Content-Type: application/json" | jq -r '.result.header.height'
}

# Set START_BLOCK to the latest block if required
if [[ "$START_BLOCK" == "latest" ]]; then
  START_BLOCK=$(get_latest_block)
  [[ -z "$START_BLOCK" ]] && { echo "Failed to fetch the latest block."; exit 1; }
  echo "Fetched latest block number: $START_BLOCK"
fi

# Generate Rust environment constants
cat > ./src/env.rs <<EOL
pub const MAX_ARGS_LENGTH: usize = ${MAX_ARGS_LENGTH};
pub const FILTERED_RECEIVER_IDS: &[&str] = &[$(echo "\"${FILTERED_RECEIVER_IDS//,/\", \"}\"")];
pub const FILTERED_METHOD_NAMES: &[&str] = &[$(echo "\"${FILTERED_METHOD_NAMES//,/\", \"}\"")];
EOL

# Build Rust project targeting WASM
echo "Building Rust project targeting WASM..."
cargo build --release --target wasm32-unknown-unknown || { echo "Rust build failed"; exit 1; }

# Initialization lock file
INIT_LOCK_FILE="./substreams_init.lock"

# Perform initialization if not already done
if [[ ! -f "$INIT_LOCK_FILE" ]]; then
  echo "Starting substreams-sink-sql setup..."
  for yaml_file in ./substreams.clickhouse.yaml ./substreams.postgresql.yaml; do
    sed -i "s/initialBlock: .*/initialBlock: $START_BLOCK/" "$yaml_file"
  done
  echo "Updated initialBlock to $START_BLOCK in YAML files."

  substreams-sink-sql setup "$DB_CONNECTION" ./substreams.clickhouse.yaml || { echo "substreams-sink-sql setup failed"; exit 1; }
  sleep 1

  touch "$INIT_LOCK_FILE"
  echo "Initialization completed. Lock file created at $INIT_LOCK_FILE."
else
  echo "Initialization already completed. Skipping setup."
fi

# Define block range and finals-only flag
BLOCK_RANGE="${END_BLOCK:+$START_BLOCK:$END_BLOCK}"
FINALS_ONLY="${START_BLOCK:+--final-blocks-only}"

# Run substreams-sink-sql with the provided options
substreams-sink-sql run "$DB_CONNECTION" ./substreams.clickhouse.yaml "$BLOCK_RANGE" \
  --header "x-api-key:$SUBSTREAMS_API_KEY" \
  --undo-buffer-size 50000 \
  --on-module-hash-mistmatch warn \
  $FINALS_ONLY
