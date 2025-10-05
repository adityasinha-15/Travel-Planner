#!/bin/bash

# Smart Travel Planner Startup Script

echo "🌟 Starting Smart Travel Planner..."
echo "=================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed"
    exit 1
fi

echo "✅ All prerequisites found"

# Start backend
echo ""
echo "🚀 Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy env.example to .env and add your API keys:"
    echo "   cp env.example .env"
    echo ""
fi

# Start backend in background
echo "🌐 Starting FastAPI server on http://localhost:8000"
python start.py &
BACKEND_PID=$!

# Go back to root and start frontend
cd ../frontend

echo ""
echo "🎨 Starting frontend server..."

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Start frontend
echo "🌐 Starting React app on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Smart Travel Planner is starting up!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '👋 Goodbye!'; exit 0" INT

# Wait for processes
wait
