#!/bin/bash

# Production start script for Render
# This properly handles the PORT environment variable

# Default to 10000 if PORT not set
PORT=${PORT:-10000}

echo "Starting Nicole on port $PORT..."

# Start uvicorn with the PORT variable
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
