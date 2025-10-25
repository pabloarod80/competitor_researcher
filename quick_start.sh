#!/bin/bash
# Quick start script for AI-Powered Competitor Tracker

echo "=========================================="
echo "  🚀 Competitor Tracker Quick Start"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found."
    echo "   Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ ERROR: Streamlit not installed"
    echo "   Please run ./install.sh first"
    exit 1
fi

echo "✅ Environment ready"
echo ""
echo "🌐 Launching Competitor Tracker Web UI..."
echo ""
echo "   ➡️  The browser will open automatically"
echo "   ➡️  Or go to: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Launch streamlit
streamlit run app.py
