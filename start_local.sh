#!/bin/bash
# Script to start API server and Celery worker locally
# This script starts both services in the background

cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Starting Document Verification System..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo "   Please create .env file with required variables:"
    echo "   - GITHUB_TOKEN"
    echo "   - BEARER_TOKEN"
    echo "   - CELERY_BROKER_URL=redis://localhost:6379/0"
    echo "   - CELERY_RESULT_BACKEND=redis://localhost:6379/1"
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"

# Check if Redis is running
REDIS_RUNNING=false
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        REDIS_RUNNING=true
        echo -e "${GREEN}✅ Redis is running${NC}"
    fi
fi

if [ "$REDIS_RUNNING" = false ]; then
    echo -e "${YELLOW}⚠️  Warning: Redis is not running${NC}"
    echo "   Attempting to start Redis with Docker..."
    
    # Check if Docker is available
    if command -v docker &> /dev/null; then
        # Check if Redis container already exists
        if docker ps -a --format '{{.Names}}' | grep -q "^redis$"; then
            echo "   Starting existing Redis container..."
            docker start redis &> /dev/null
        else
            echo "   Creating new Redis container..."
            docker run -d -p 6379:6379 --name redis redis:7-alpine &> /dev/null
        fi
        
        # Wait a moment for Redis to start
        sleep 2
        
        # Verify Redis is now running
        if redis-cli ping &> /dev/null; then
            echo -e "${GREEN}✅ Redis started successfully${NC}"
            REDIS_RUNNING=true
        else
            echo -e "${RED}❌ Failed to start Redis${NC}"
            echo "   Please start Redis manually:"
            echo "   docker run -d -p 6379:6379 --name redis redis:7-alpine"
            echo "   or: sudo systemctl start redis"
            exit 1
        fi
    else
        echo -e "${RED}❌ Docker not found. Please start Redis manually:${NC}"
        echo "   docker run -d -p 6379:6379 --name redis redis:7-alpine"
        echo "   or: sudo systemctl start redis"
        exit 1
    fi
fi

# Check if port 5002 is already in use
if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Warning: Port 5002 is already in use${NC}"
    echo "   Another process may be using the API port"
    echo "   Continuing anyway..."
fi

echo ""
echo "📦 Starting services..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $API_PID $CELERY_PID 2>/dev/null
    wait $API_PID $CELERY_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Start API server in background
echo "   Starting API server (port 5002)..."
uvicorn api.main:app --host 0.0.0.0 --port 5002 --reload > /tmp/api.log 2>&1 &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Check if API started successfully
if ! kill -0 $API_PID 2>/dev/null; then
    echo -e "${RED}❌ Failed to start API server${NC}"
    echo "   Check /tmp/api.log for errors"
    exit 1
fi

echo -e "${GREEN}   ✅ API server started (PID: $API_PID)${NC}"

# Start Celery worker in background
echo "   Starting Celery worker..."
celery -A core.celery worker --loglevel=info --concurrency=2 > /tmp/celery.log 2>&1 &
CELERY_PID=$!

# Wait a moment for Celery to start
sleep 2

# Check if Celery started successfully
if ! kill -0 $CELERY_PID 2>/dev/null; then
    echo -e "${RED}❌ Failed to start Celery worker${NC}"
    echo "   Check /tmp/celery.log for errors"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}   ✅ Celery worker started (PID: $CELERY_PID)${NC}"

echo ""
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo ""
echo "📍 Services:"
echo "   - API Server: http://localhost:5002"
echo "   - API Docs: http://localhost:5002/docs"
echo "   - Health Check: http://localhost:5002/api/v1/health"
echo ""
echo "📋 Logs:"
echo "   - API logs: tail -f /tmp/api.log"
echo "   - Celery logs: tail -f /tmp/celery.log"
echo ""
echo "🛑 Press Ctrl+C to stop all services"
echo ""

# Wait for processes
wait $API_PID $CELERY_PID
