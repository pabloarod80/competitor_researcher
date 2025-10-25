#!/bin/bash
# Installation script for AI-Powered Competitor Tracker

echo "=========================================="
echo "  AI-Powered Competitor Tracker"
echo "  Installation Script"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ ERROR: Python not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
echo "   This may take 1-2 minutes..."
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully!"
else
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Verify installation
echo "🧪 Verifying installation..."
python -c "import streamlit; import pandas; import requests; import yaml" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Installation verified!"
else
    echo "⚠️  Warning: Some modules may not be properly installed"
fi
echo ""

echo "=========================================="
echo "  ✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Launch the web interface:"
echo "   streamlit run app.py"
echo ""
echo "3. Or use the quick start script:"
echo "   ./quick_start.sh"
echo ""
echo "📖 For detailed instructions, see:"
echo "   - QUICKSTART.md (5-minute guide)"
echo "   - INSTALLATION_GUIDE.md (complete guide)"
echo ""
echo "Happy competitor tracking! 🎯"
