#!/bin/bash
# Quick deployment script for Docker

set -e

echo "🐳 Document Verifier - Docker Deployment Script"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "⚠️  Please edit .env and add your GITHUB_TOKEN before continuing!"
        read -p "Press Enter to continue after editing .env, or Ctrl+C to cancel..."
    else
        echo "❌ .env.example not found. Please create .env manually with required variables."
        echo "Required: GITHUB_TOKEN"
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

# Function to run docker-compose (handles both versions)
run_compose() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

# Parse command line arguments
ACTION=${1:-up}

case $ACTION in
    build)
        echo "🔨 Building Docker image..."
        run_compose build
        echo "✅ Build complete!"
        ;;
    up|start)
        echo "🚀 Starting containers..."
        run_compose up -d
        echo ""
        echo "✅ Containers started!"
        echo ""
        echo "📊 Container status:"
        run_compose ps
        echo ""
        echo "📝 View logs with: ./docker-deploy.sh logs"
        echo "🌐 Access the application at:"
        echo "   - API: http://localhost:5002"
        echo "   - UI: http://localhost:5002/ui"
        echo "   - Docs: http://localhost:5002/docs"
        ;;
    down|stop)
        echo "🛑 Stopping containers..."
        run_compose down
        echo "✅ Containers stopped!"
        ;;
    restart)
        echo "🔄 Restarting containers..."
        run_compose restart
        echo "✅ Containers restarted!"
        ;;
    logs)
        echo "📋 Showing logs (Ctrl+C to exit)..."
        run_compose logs -f
        ;;
    status)
        echo "📊 Container status:"
        run_compose ps
        echo ""
        echo "🏥 Health check:"
        if curl -s http://localhost:5002/api/v1/health > /dev/null 2>&1; then
            echo "✅ API is healthy"
            curl -s http://localhost:5002/api/v1/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:5002/api/v1/health
        else
            echo "❌ API is not responding"
        fi
        ;;
    rebuild)
        echo "🔨 Rebuilding containers..."
        run_compose down
        run_compose build --no-cache
        run_compose up -d
        echo "✅ Rebuild complete!"
        ;;
    shell)
        echo "🐚 Opening shell in container..."
        run_compose exec api bash
        ;;
    clean)
        echo "🧹 Cleaning up Docker resources..."
        read -p "This will remove containers, images, and volumes. Continue? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_compose down -v --rmi all
            docker system prune -f
            echo "✅ Cleanup complete!"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    *)
        echo "Usage: $0 {build|up|down|restart|logs|status|rebuild|shell|clean}"
        echo ""
        echo "Commands:"
        echo "  build    - Build Docker image"
        echo "  up       - Start containers (default)"
        echo "  down     - Stop containers"
        echo "  restart  - Restart containers"
        echo "  logs     - Show container logs"
        echo "  status   - Show container status and health"
        echo "  rebuild  - Rebuild and restart containers"
        echo "  shell    - Open shell in container"
        echo "  clean    - Remove containers, images, and volumes"
        exit 1
        ;;
esac

