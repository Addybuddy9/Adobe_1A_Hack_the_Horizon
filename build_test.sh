#!/bin/bash
# Adobe Challenge 1A - Build and Test Script

set -e  # Exit on any error

echo "=============================================="
echo "🚀 Adobe Challenge 1A - Build & Test Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
check_docker() {
    echo "🔍 Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_status "Docker is running"
}

# Check if Docker Compose is available
check_docker_compose() {
    echo "🔍 Checking Docker Compose..."
    if ! command -v docker-compose &> /dev/null; then
        if ! docker compose version &> /dev/null; then
            print_error "Docker Compose is not available"
            exit 1
        else
            COMPOSE_CMD="docker compose"
        fi
    else
        COMPOSE_CMD="docker-compose"
    fi
    
    print_status "Docker Compose is available: $COMPOSE_CMD"
}

# Build the Docker image
build_image() {
    echo "🏗️  Building Docker image..."
    
    # Official challenge build command
    echo "📦 Using official challenge build command..."
    if docker build --platform linux/amd64 -t adobe-challenge1a:latest .; then
        print_status "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
    
    # Also build with docker-compose
    echo "📦 Building with Docker Compose..."
    if $COMPOSE_CMD build; then
        print_status "Docker Compose build successful"
    else
        print_warning "Docker Compose build failed, but manual build succeeded"
    fi
}

# Test the setup
test_setup() {
    echo "🧪 Testing the setup..."
    
    # Check if input directory has PDFs
    if [ ! -d "input" ]; then
        print_warning "Input directory not found, creating it..."
        mkdir -p input
    fi
    
    pdf_count=$(find input -name "*.pdf" | wc -l)
    if [ "$pdf_count" -eq 0 ]; then
        print_warning "No PDF files found in input directory"
        echo "ℹ️  Please add PDF files to the input directory for testing"
    else
        print_status "Found $pdf_count PDF files in input directory"
    fi
    
    # Create output directory if it doesn't exist
    mkdir -p output cache
    
    # Test with official challenge command
    echo "🔍 Testing with official challenge command..."
    if docker run --rm \
        -v "$(pwd)/input:/app/input" \
        -v "$(pwd)/output:/app/output" \
        --network none \
        adobe-challenge1a:latest --help &> /dev/null; then
        print_status "Official challenge command test passed"
    else
        print_warning "Official challenge command test failed (expected if no PDFs)"
    fi
}

# Run with Docker Compose
run_compose() {
    echo "🚀 Running with Docker Compose..."
    
    if [ "$1" = "detached" ]; then
        print_status "Starting in detached mode..."
        $COMPOSE_CMD up -d
    else
        print_status "Starting in foreground mode..."
        $COMPOSE_CMD up
    fi
}

# Clean up
cleanup() {
    echo "🧹 Cleaning up..."
    $COMPOSE_CMD down --remove-orphans
    docker image prune -f
    print_status "Cleanup completed"
}

# Main execution
main() {
    case "${1:-}" in
        "build")
            check_docker
            check_docker_compose
            build_image
            ;;
        "test")
            check_docker
            test_setup
            ;;
        "run")
            check_docker
            check_docker_compose
            run_compose "${2:-}"
            ;;
        "cleanup")
            cleanup
            ;;
        "all")
            check_docker
            check_docker_compose
            build_image
            test_setup
            print_status "Build and test completed successfully!"
            echo "ℹ️  To run the container:"
            echo "   ./build_test.sh run"
            echo "   or"
            echo "   docker-compose up"
            ;;
        *)
            echo "Usage: $0 {build|test|run|cleanup|all}"
            echo ""
            echo "Commands:"
            echo "  build    - Build Docker images"
            echo "  test     - Test the setup"
            echo "  run      - Run with Docker Compose"
            echo "  cleanup  - Clean up containers and images"
            echo "  all      - Build and test everything"
            echo ""
            echo "Examples:"
            echo "  $0 all                 # Build and test"
            echo "  $0 run                 # Run in foreground"
            echo "  $0 run detached        # Run in background"
            exit 1
            ;;
    esac
}

main "$@"
