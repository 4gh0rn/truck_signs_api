#!/usr/bin/bash


read -p "Do you want a fresh build (no cache)? [y/N]: " fresh_build
if [[ "$fresh_build" =~ ^[Yy]$ ]]; then
    docker-compose build --no-cache
else
    docker-compose build
fi


docker-compose -f compose.yml up -d