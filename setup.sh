#!/bin/bash

# Astra Quick Setup Script
# This script automates the local setup process

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 Astra Quick Setup Script 🚀                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "📋 Step 1: Checking prerequisites..."
echo ""

# Check Docker
if command_exists docker; then
    DOCKER_VERSION=$(docker --version)
    print_success "Docker is installed: $DOCKER_VERSION"
else
    print_error "Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check Docker Compose
if command_exists docker-compose; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_success "Docker Compose is installed: $COMPOSE_VERSION"
else
    print_error "Docker Compose is not installed!"
    echo "Please install Docker Compose"
    exit 1
fi

# Check if Docker is running
if docker ps >/dev/null 2>&1; then
    print_success "Docker daemon is running"
else
    print_error "Docker daemon is not running!"
    echo "Please start Docker Desktop"
    exit 1
fi

echo ""
echo "⚙️  Step 2: Setting up environment..."
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    print_info ".env file already exists"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        print_success "Created new .env file from .env.example"
    else
        print_info "Keeping existing .env file"
    fi
else
    cp .env.example .env
    print_success "Created .env file from .env.example"
fi

echo ""
print_info "Generating secure SECRET_KEY..."
if command_exists python3; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    # Update SECRET_KEY in .env (works on both macOS and Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    else
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi
    print_success "Generated and set secure SECRET_KEY"
else
    print_info "Python3 not found. Please manually set SECRET_KEY in .env"
fi

echo ""
echo "🐳 Step 3: Building Docker containers..."
echo ""

print_info "This may take a few minutes on first run..."
if docker-compose up --build -d; then
    print_success "Docker containers built and started"
else
    print_error "Failed to build containers"
    exit 1
fi

echo ""
echo "⏳ Step 4: Waiting for services to be ready..."
echo ""

# Wait for services to be healthy
MAX_WAIT=60
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is ready!"
        break
    fi
    echo -n "."
    sleep 2
    WAITED=$((WAITED + 2))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    print_error "Services failed to start within $MAX_WAIT seconds"
    echo "Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "🧪 Step 5: Testing the installation..."
echo ""

# Test health endpoint
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    print_success "Health check passed"
else
    print_error "Health check failed"
    echo "Response: $HEALTH_RESPONSE"
fi

# Check all services
print_info "Running services:"
docker-compose ps

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         ✅ Setup Complete! ✅                                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
print_success "Astra is now running!"
echo ""
echo "📖 Quick Links:"
echo "   • API: http://localhost:8000"
echo "   • API Docs (Swagger): http://localhost:8000/docs"
echo "   • Health Check: http://localhost:8000/health"
echo ""
echo "🌐 To use the Web Client:"
echo "   1. Open: client/index.html in your browser"
echo "   2. Register a new account"
echo "   3. Login and start chatting!"
echo ""
echo "📊 Useful Commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart"
echo ""
print_info "See LOCAL_SETUP.md for detailed documentation"
echo ""
