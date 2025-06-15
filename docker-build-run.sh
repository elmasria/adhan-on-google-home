#!/bin/bash
set -e

echo "Stopping containers..."
docker-compose down

echo "cleaning up..."
rm -rf ./node_modules/ package-lock.json

echo "Building Docker image..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up --remove-orphans -d

echo "Removing old images..."
docker image prune -f

echo "Done."
