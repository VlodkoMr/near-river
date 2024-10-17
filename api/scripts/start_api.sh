#!/bin/bash

PORT=3000

echo "App running on http://localhost:${PORT} 🚀"

# Run Uvicorn with the passed arguments
uvicorn main:app --host 0.0.0.0 --port "${PORT}" --reload --timeout-keep-alive 90 # --log-level warning