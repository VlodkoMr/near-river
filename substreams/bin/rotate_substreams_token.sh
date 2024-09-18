#!/bin/bash

# Check if the environment file path is passed as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 path_to_env_file"
  exit 1
fi

ENV_FILE="$1"

# Load environment variables from the specified file
set -a
source "$ENV_FILE"
set +a

SUBSTREAMS_API_KEY="${SUBSTREAMS_API_KEY//$'\r'/}"

NEW_SUBSTREAMS_API_TOKEN=$(curl https://auth.streamingfast.io/v1/auth/issue -s --data-binary '{"api_key":"'$SUBSTREAMS_API_KEY'", "lifetime": 1300000}' | jq -r .token)

# Check if the token was successfully retrieved
if [ -z "$NEW_SUBSTREAMS_API_TOKEN" ]; then
  echo "Failed to retrieve the new token."
  exit 2
fi

echo "New token retrieved successfully."

# Update SUBSTREAMS_API_TOKEN in the .env file
sed -i "s/^SUBSTREAMS_API_TOKEN=.*/SUBSTREAMS_API_TOKEN=$NEW_SUBSTREAMS_API_TOKEN/" "$ENV_FILE"

echo "JWT Token updated."