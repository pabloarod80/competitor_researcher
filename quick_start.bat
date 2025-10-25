@echo off
REM Quick start script for AI-Powered Competitor Tracker (Windows)

echo ==========================================
echo   Competitor Tracker Quick Start
echo ==========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Virtual environment not found.
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Streamlit not installed
    echo Please run install.bat first
    pause
    exit /b 1
)

echo Environment ready
echo.
echo Launching Competitor Tracker Web UI...
echo.
echo    The browser will open automatically
echo    Or go to: http://localhost:8501
echo.
echo    Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

REM Launch streamlit
streamlit run app.py
