#!/bin/bash

# Ensure the .env file is in place
if [ ! -f .env ]; then
  echo ".env file not found!"
  exit 1
fi

echo "Initializing database..."
echo "User: $DB_USER"
echo "Password: $DB_PASSWORD"
echo "Database: $DB_NAME"

# Run the Docker container with the environment variables from the .env file
docker run --env-file .env -d --name postgres-container -p 5432:5432 postgres:latest
# You can add any further commands here that need to be executed after the container starts
echo "Docker container started successfully!"
