#!/bin/bash

echo "AI Career Coach - Setup Script"
echo "=============================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "Building and starting AI Career Coach..."
echo ""

# Build and start containers
docker-compose up --build -d

echo ""
echo "Waiting for services to start..."
sleep 30

# Check if services are running
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "Backend is running!"
else
    echo "Backend failed to start. Check logs with: docker-compose logs backend"
fi

if curl -f http://localhost:3000 &> /dev/null; then
    echo "Frontend is running!"
else
    echo "Frontend failed to start. Check logs with: docker-compose logs frontend"
fi

echo ""
echo "=============================="
echo "AI Career Coach is ready!"
echo "=============================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
echo ""
