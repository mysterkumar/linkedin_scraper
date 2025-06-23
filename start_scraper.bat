@echo off
title LinkedIn Scraper Launcher
echo.
echo ================================================
echo         LINKEDIN SCRAPER LAUNCHER
echo ================================================
echo.
echo Starting the enhanced LinkedIn scraper...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Run the launcher
python launcher.py

echo.
echo Scraper finished.
pause
