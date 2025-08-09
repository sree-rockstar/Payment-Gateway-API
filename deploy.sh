#!/bin/bash

# Payment Gateway API Docker Deployment Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! docker-compose --version > /dev/null 2>&1; then
        print_error "Docker Compose is not available. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to create SSL certificates for development
create_ssl_certs() {
    if [ ! -d "ssl" ]; then
        print_status "Creating SSL directory..."
        mkdir -p ssl
    fi
    
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        print_status "Generating self-signed SSL certificates for development..."
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        print_success "SSL certificates generated"
    else
        print_success "SSL certificates already exist"
    fi
}

# Function to create logs directory
create_logs_dir() {
    if [ ! -d "logs" ]; then
        print_status "Creating logs directory..."
        mkdir -p logs
        print_success "Logs directory created"
    fi
}

# Function to stop and remove existing containers
cleanup_existing() {
    print_status "Stopping and removing existing containers..."
    docker-compose down --remove-orphans 2>/dev/null || true
    print_success "Existing containers cleaned up"
}

# Function to build and start services
deploy_services() {
    local compose_file=${1:-"docker-compose.yml"}
    
    print_status "Building and starting services with $compose_file..."
    docker-compose -f $compose_file up --build -d
    
    print_success "Services started successfully"
}

# Function to wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    # Wait for MongoDB
    print_status "Waiting for MongoDB..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if docker-compose ps mongodb | grep -q "healthy"; then
            print_success "MongoDB is healthy"
            break
        fi
        sleep 5
        timeout=$((timeout - 5))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "MongoDB failed to become healthy within 2 minutes"
        exit 1
    fi
    
    # Wait for API
    print_status "Waiting for API..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            print_success "API is healthy"
            break
        fi
        sleep 5
        timeout=$((timeout - 5))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "API failed to become healthy within 2 minutes"
        exit 1
    fi
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
    
    print_status "Container Logs:"
    docker-compose logs --tail=10
}

# Function to show API information
show_api_info() {
    print_status "API Information:"
    echo "  🌐 API Base URL: http://localhost:8000"
    echo "  📚 Swagger UI: http://localhost:8000/docs"
    echo "  📖 ReDoc: http://localhost:8000/redoc"
    echo "  🔍 Health Check: http://localhost:8000/health"
    echo "  🗄️  MongoDB: localhost:27017"
    echo ""
    print_status "Test Credentials:"
    echo "  👤 Email: test@example.com"
    echo "  🔑 Password: testpass123"
    echo ""
    print_status "Environment Variables:"
    echo "  🔑 RAZORPAY_KEY_ID: ${RAZORPAY_KEY_ID:-rzp_test_EnZ3V3m6bWKwsb}"
    echo "  🔐 RAZORPAY_KEY_SECRET: ${RAZORPAY_KEY_SECRET:-your-razorpay-test-key-secret}"
}

# Function to run tests
run_tests() {
    print_status "Running API tests..."
    
    if command -v python3 > /dev/null 2>&1; then
        if [ -f "test_razorpay.py" ]; then
            python3 test_razorpay.py
        else
            print_warning "test_razorpay.py not found, skipping tests"
        fi
        
        if [ -f "test_swagger.py" ]; then
            python3 test_swagger.py
        else
            print_warning "test_swagger.py not found, skipping Swagger tests"
        fi
    else
        print_warning "Python3 not found, skipping tests"
    fi
}

# Main deployment function
main() {
    local environment=${1:-"production"}
    local compose_file="docker-compose.yml"
    
    if [ "$environment" = "dev" ]; then
        compose_file="docker-compose.dev.yml"
        print_status "Deploying in development mode"
    else
        print_status "Deploying in production mode"
    fi
    
    echo "🚀 Payment Gateway API Docker Deployment"
    echo "========================================"
    
    # Pre-deployment checks
    check_docker
    check_docker_compose
    create_ssl_certs
    create_logs_dir
    
    # Deployment
    cleanup_existing
    deploy_services $compose_file
    wait_for_services
    
    # Post-deployment
    show_status
    show_api_info
    
    print_success "Deployment completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. Visit http://localhost:8000/docs to test the API"
    echo "  2. Use the test credentials to authenticate"
    echo "  3. Try creating a payment with Razorpay"
    echo "  4. Check logs with: docker-compose logs -f"
    echo "  5. Stop services with: docker-compose down"
}

# Function to show help
show_help() {
    echo "Usage: $0 [dev|production]"
    echo ""
    echo "Options:"
    echo "  dev         Deploy in development mode (with volume mounts)"
    echo "  production  Deploy in production mode (default)"
    echo "  help        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  RAZORPAY_KEY_ID      Your Razorpay key ID"
    echo "  RAZORPAY_KEY_SECRET  Your Razorpay key secret"
    echo ""
    echo "Examples:"
    echo "  $0                    # Deploy in production mode"
    echo "  $0 dev               # Deploy in development mode"
    echo "  RAZORPAY_KEY_ID=xxx $0  # Deploy with custom Razorpay key"
}

# Parse command line arguments
case "${1:-production}" in
    "dev"|"development")
        main "dev"
        ;;
    "production"|"prod")
        main "production"
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Invalid option: $1"
        show_help
        exit 1
        ;;
esac
