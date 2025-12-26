#!/bin/bash
# Script to stop the web server running on the specified port

PORT=${1:-8081}

echo "Stopping web server on port $PORT..."

# Find and kill processes using the port
PIDS=$(lsof -ti :$PORT 2>/dev/null)

if [ -z "$PIDS" ]; then
    # Try alternative methods
    if command -v fuser &> /dev/null; then
        fuser -k $PORT/tcp 2>/dev/null
        PIDS=$(fuser $PORT/tcp 2>/dev/null | tr -d ' ')
    fi
    
    # Try with pgrep
    if [ -z "$PIDS" ]; then
        PIDS=$(pgrep -f "http.server.*$PORT" 2>/dev/null)
    fi
fi

if [ -z "$PIDS" ]; then
    echo "⚠️  No process found running on port $PORT"
    echo "The server may already be stopped."
    exit 0
fi

# Kill the processes
for PID in $PIDS; do
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping process $PID..."
        kill $PID 2>/dev/null
        
        # Wait a moment, then force kill if still running
        sleep 1
        if ps -p $PID > /dev/null 2>&1; then
            echo "Force killing process $PID..."
            kill -9 $PID 2>/dev/null
        fi
    fi
done

# Verify the port is free
sleep 1
if ss -tulpn 2>/dev/null | grep -q ":$PORT " || lsof -ti :$PORT > /dev/null 2>&1; then
    echo "⚠️  Port $PORT may still be in use. You may need to run:"
    echo "   sudo lsof -ti :$PORT | xargs sudo kill -9"
else
    echo "✅ Server stopped successfully. Port $PORT is now free."
fi
