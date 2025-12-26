#!/bin/bash
# Script to run the API server

cd "$(dirname "$0")"
uvicorn api.main:app --host 0.0.0.0 --port 5002 --reload

