#!/bin/bash
# Launcher script for Competitor Tracker Web UI

echo "Starting Competitor Tracker Web UI..."
echo ""
echo "Installing/checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Launching web interface..."
echo "Open your browser to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
