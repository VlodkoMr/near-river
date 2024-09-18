#!/bin/bash

# Check if the environment file path is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 path_to_env_file"
  exit 1
fi

# Load environment variables from the specified file
set -a
source "$1"
set +a

DB_CONNECTION="${DB_CONNECTION//$'\r'/}"

substreams-sink-sql run "$DB_CONNECTION" ./substreams.clickhouse.yaml \
--header "x-api-key:$SUBSTREAMS_API_KEY" --undo-buffer-size 50000 --on-module-hash-mistmatch warn