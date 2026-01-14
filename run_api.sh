#!/bin/bash
# Script to run the API server

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment (venv)..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "✅ Activating virtual environment (.venv)..."
    source .venv/bin/activate
fi

uvicorn api.main:app --host 0.0.0.0 --port 5002 --reload

