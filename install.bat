@echo off
REM Installation script for AI-Powered Competitor Tracker (Windows)

echo ==========================================
echo   AI-Powered Competitor Tracker
echo   Installation Script (Windows)
echo ==========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take 1-2 minutes...
pip install -r requirements.txt -q

if %errorlevel% equ 0 (
    echo All dependencies installed successfully!
) else (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Verify installation
echo Verifying installation...
python -c "import streamlit; import pandas; import requests; import yaml" 2>nul

if %errorlevel% equ 0 (
    echo Installation verified!
) else (
    echo Warning: Some modules may not be properly installed
)
echo.

echo ==========================================
echo   Installation Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Launch the web interface:
echo    streamlit run app.py
echo.
echo 3. Or double-click:
echo    quick_start.bat
echo.
echo For detailed instructions, see:
echo    - QUICKSTART.md (5-minute guide)
echo    - INSTALLATION_GUIDE.md (complete guide)
echo.
echo Happy competitor tracking!
echo.
pause
