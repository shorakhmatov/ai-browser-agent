#!/bin/bash

echo "AI Browser Agent"
echo "================"
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "Installing Playwright browsers..."
playwright install > /dev/null 2>&1

echo ""
echo "Starting AI Browser Agent..."
echo ""
python cli.py

read -p "Press enter to exit..."
