#!/bin/bash

# Nicole Development Startup Script
# Makes it easy to start the development server

echo "🪵 Starting Nicole for Wood Thumb..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Copy .env.example to .env and add your API key:"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if knowledge base exists
if [ ! -f "knowledge/woodthumb.md" ]; then
    echo "⚠️  Warning: knowledge/woodthumb.md not found"
fi

echo ""
echo "✅ Nicole is ready!"
echo ""
echo "🌐 Starting FastAPI server..."
echo "   API: http://localhost:8000"
echo "   Health: http://localhost:8000/api/health"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "💬 Test the widget: Open widget/test.html in your browser"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the server
python -m uvicorn api.main:app --reload --port 8000
