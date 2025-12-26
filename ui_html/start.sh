#!/bin/bash
# Simple script to start a local web server for the UI

PORT=${1:-8081}

# Function to check if port is in use
check_port() {
    local port=$1
    # Try Python socket check first (most reliable)
    python3 -c "import socket; s = socket.socket(); s.settimeout(0.1); result = s.connect_ex(('localhost', $port)); s.close(); exit(0 if result == 0 else 1)" 2>/dev/null
    if [ $? -eq 0 ]; then
        return 0  # Port is in use
    fi
    
    # Fallback to system tools
    if command -v ss &> /dev/null; then
        ss -tuln 2>/dev/null | grep -q ":$port " && return 0
    fi
    if command -v netstat &> /dev/null; then
        netstat -tuln 2>/dev/null | grep -q ":$port.*LISTEN" && return 0
    fi
    if command -v lsof &> /dev/null; then
        lsof -i :$port > /dev/null 2>&1 && return 0
    fi
    
    return 1  # Port appears to be free
}

# Function to find an available port
find_available_port() {
    local start_port=$1
    local port=$start_port
    local max_attempts=10
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if ! check_port $port; then
            echo $port
            return 0
        fi
        port=$((port + 1))
        attempt=$((attempt + 1))
    done
    
    return 1
}

# Check if requested port is available
if check_port $PORT; then
    echo "⚠️  Port $PORT is already in use."
    echo "Attempting to find an available port..."
    AVAILABLE_PORT=$(find_available_port $PORT)
    
    if [ -z "$AVAILABLE_PORT" ]; then
        echo "❌ Could not find an available port. Please free up a port or specify a different one."
        echo ""
        echo "Usage: $0 [PORT]"
        echo "Example: $0 3000"
        exit 1
    fi
    
    echo "✅ Using port $AVAILABLE_PORT instead"
    PORT=$AVAILABLE_PORT
fi

echo "Starting web server on port $PORT..."
echo "Open http://localhost:$PORT in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try Python 3 first, then Python 2, then suggest alternatives
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer $PORT
else
    echo "Python not found. Please install Python or use another HTTP server."
    echo "Alternatively, you can open index.html directly in your browser."
    exit 1
fi
