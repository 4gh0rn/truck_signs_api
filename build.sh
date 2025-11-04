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

# Stop and remove both containers explicitly to avoid docker-compose v1 'ContainerConfig' bug
docker-compose stop
docker-compose rm -f

# Start both containers fresh
docker-compose up -d