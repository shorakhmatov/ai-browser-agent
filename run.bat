@echo off
echo AI Browser Agent
echo ================
echo.

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1

echo Installing Playwright browsers...
playwright install > nul 2>&1

echo.
echo Starting AI Browser Agent...
echo.
python cli.py

pause
