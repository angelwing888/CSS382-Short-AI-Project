@echo off
REM Colors for Windows (using title)
title Marvel Rivals Balance Tracker - Setup

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

REM Scrape data
echo.
echo Scraping balance data from Marvel Rivals (this may take a few minutes)...
python scraper.py

REM Start the app
echo.
echo ✓ Setup complete!
echo.
echo Starting the application...
echo.
python app.py

pause
