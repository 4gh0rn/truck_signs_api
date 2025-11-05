#!/bin/bash

# Truck Signs API Deployment Script
# Run this script on your Cloud VM

set -e

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /path/to/your/truck_signs_api

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start new containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "✅ Checking service status..."
docker-compose ps

# Clean up old images
echo "🧹 Cleaning up old images..."
docker system prune -f

echo "🎉 Deployment completed successfully!"
echo "🌐 Your app should be available at: http://your-vm-ip:8020"
