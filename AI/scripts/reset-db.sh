#!/bin/bash

echo "🗑️  Resetting MongoDB database..."

# Stop and remove containers
echo "Stopping containers..."
docker-compose down

# Remove MongoDB volume to start fresh
echo "Removing MongoDB volume..."
docker volume rm ai_mongodb_data 2>/dev/null || echo "Volume not found, continuing..."

# Start containers again
echo "Starting containers..."
docker-compose up --build -d

echo "✅ Database reset completed!"
echo "📊 MongoDB will initialize with the new user and database structure."
