#!/bin/bash
# Script to run the Celery worker for background task processing

cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file with required variables:"
    echo "   - GITHUB_TOKEN"
    echo "   - BEARER_TOKEN"
    echo "   - CELERY_BROKER_URL"
    echo "   - CELERY_RESULT_BACKEND"
    echo ""
fi

# Check if Redis is running
if command -v redis-cli &> /dev/null; then
    if ! redis-cli ping &> /dev/null; then
        echo "⚠️  Warning: Redis is not running"
        echo "   Please start Redis first:"
        echo "   docker run -d -p 6379:6379 --name redis redis:7-alpine"
        echo "   or: sudo systemctl start redis"
        echo ""
    fi
fi

echo "🚀 Starting Celery worker..."
echo "   Press Ctrl+C to stop"
echo ""

# Run Celery worker
celery -A core.celery worker --loglevel=info --concurrency=2
