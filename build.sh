#!/usr/bin/bash

# Check if running in non-interactive mode (CI/CD)
if [ -t 0 ]; then
    # Interactive mode
    read -p "Do you want a fresh build (no cache)? [y/N]: " fresh_build
    if [[ "$fresh_build" =~ ^[Yy]$ ]]; then
        docker-compose build --no-cache
    else
        docker-compose build
    fi
else
    # Non-interactive mode (CI/CD)
    docker-compose build
fi

# Stop and remove only the app container (keep db running)
docker-compose stop app
docker-compose rm -f app

# Start containers with force recreate to ensure fresh start
docker-compose up -d --force-recreate