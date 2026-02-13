#!/bin/bash

# Production start script
# Handles PORT environment variable for Railway/Render

PORT=${PORT:-8000}

echo "Starting Nicole on port $PORT..."

exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
