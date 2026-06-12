@echo off
REM Quick Start Script for Azure Sentinel DevOps Orchestrator (Windows)
REM This script sets up the environment and runs the orchestrator

echo.
echo ========================================
echo Azure Sentinel DevOps Orchestrator
echo Quick Start for Windows
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11 or higher.
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Please edit .env with your Azure credentials
    echo.
    pause
) else (
    echo .env file already exists
)
echo.

REM Create logs directory
echo Creating logs directory...
if not exist "logs" mkdir logs
echo Logs directory created
echo.

REM Run tests
echo Running tests...
pytest test_orchestrator.py -v --tb=short
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed
    echo.
)
echo.

REM Run orchestrator
echo ========================================
echo Starting orchestrator...
echo ========================================
echo.
python run_orchestrator.py

echo.
echo ========================================
echo Quick start completed!
echo ========================================
echo.
echo Next steps:
echo   1. Check logs in logs\orchestrator.log
echo   2. View telemetry in Azure Portal
echo   3. Check Sentinel incidents
echo.
echo For full setup guide, see RUN_GUIDE.md
echo.
pause

@REM Made with Bob
