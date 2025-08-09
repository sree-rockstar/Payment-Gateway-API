#!/bin/bash

# Payment Gateway API Startup Script

echo "🚀 Starting Payment Gateway API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo "⚠️ Please edit .env file with your configuration before running the application!"
    echo "   - Set your SECRET_KEY"
    echo "   - Add your Razorpay credentials"
    exit 1
fi

# Check if MongoDB is running
echo "🔍 Checking MongoDB connection..."
if ! nc -z localhost 27017 2>/dev/null; then
    echo "⚠️ MongoDB is not running on localhost:27017"
    echo "   Please start MongoDB before running the application:"
    echo "   mongod"
    exit 1
fi

echo "✅ MongoDB is running"

# Start the application
echo "🌟 Starting FastAPI application..."
python run.py
