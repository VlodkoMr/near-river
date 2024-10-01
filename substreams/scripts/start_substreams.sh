#!/bin/bash

# Load environment variables from the specified file
set -a
source ".env"
set +a

make protogen

echo "Building Rust project targeting WASM..."
cargo build --release --target wasm32-unknown-unknown || { echo "Rust build failed"; exit 1; }

INIT_LOCK_FILE="./substreams_init.lock"

if [[ ! -f "$INIT_LOCK_FILE" ]]; then
  echo "Starting substreams-sink-sql setup..."

  # Function to fetch the latest block number from the NEAR blockchain
  get_latest_block() {
    # Fetch latest block using NEAR RPC API
    near_latest_block=$(curl -s https://rpc.mainnet.near.org -d '{"jsonrpc":"2.0","id":"dontcare","method":"block","params":{"finality":"final"}}' -H "Content-Type: application/json" | jq -r '.result.header.height')
    echo "$near_latest_block"
  }

  # If START_BLOCK is set to "latest", fetch the latest block from NEAR blockchain
  if [[ "$START_BLOCK" == "latest" ]]; then
    latest_block=$(get_latest_block)

    if [[ -n "$latest_block" ]]; then
      echo "Fetched latest block number: $latest_block"
      START_BLOCK=$latest_block
    else
      echo "Failed to fetch the latest block number."
      exit 1
    fi
  fi

  # Update the initialBlock value in the ClickHouse YAML file
  sed -i "s/initialBlock: .*/initialBlock: $START_BLOCK/" ./substreams.clickhouse.yaml
  echo "Update initialBlock in substreams.clickhouse.yaml to $START_BLOCK"

  # Update the initialBlock value in the PostgreSQL YAML file
  sed -i "s/initialBlock: .*/initialBlock: $START_BLOCK/" ./substreams.postgresql.yaml
  echo "Update initialBlock in substreams.postgresql.yaml to $START_BLOCK"

  # Strip carriage returns from DB_CONNECTION (useful in case the .env file has Windows-style line endings)
  DB_CONNECTION="${DB_CONNECTION//$'\r'/}"

  # Set up the substreams-sink-sql
  substreams-sink-sql setup "$DB_CONNECTION" ./substreams.clickhouse.yaml || { echo "substreams-sink-sql setup failed"; exit 1; }
  sleep 1

  # Create the lock file to indicate initialization is complete
  touch "$INIT_LOCK_FILE"
  echo "Initialization completed. Lock file created at $INIT_LOCK_FILE"
else
  echo "Initialization has already been completed. Skipping setup."
fi

DB_CONNECTION="${DB_CONNECTION//$'\r'/}"

substreams-sink-sql run "$DB_CONNECTION" ./substreams.clickhouse.yaml \
--header "x-api-key:$SUBSTREAMS_API_KEY" --undo-buffer-size 50000 --on-module-hash-mistmatch warn