#!/bin/bash
# Script to run the AgentCyber server

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your GOOGLE_API_KEY before running the server."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo "Starting AgentCyber server..."
echo "API documentation will be available at: http://localhost:8000/docs"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
