#!/bin/bash
# Quick Start Script for Azure Sentinel DevOps Orchestrator
# This script sets up the environment and runs the orchestrator

set -e

echo "🚀 Azure Sentinel DevOps Orchestrator - Quick Start"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python -m venv .venv
    echo "   ✅ Virtual environment created"
else
    echo "   ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo "   ✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "   ✅ Pip upgraded"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "   ✅ Dependencies installed"

# Check if .env exists
echo ""
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "   ✅ .env file created"
    echo "   ⚠️  Please edit .env with your Azure credentials"
    echo ""
    read -p "Press Enter to continue after editing .env..."
else
    echo "ℹ️  .env file already exists"
fi

# Create logs directory
echo ""
echo "📁 Creating logs directory..."
mkdir -p logs
echo "   ✅ Logs directory created"

# Run tests
echo ""
echo "🧪 Running tests..."
pytest test_orchestrator.py -v --tb=short
echo "   ✅ Tests passed"

# Run orchestrator
echo ""
echo "🚀 Starting orchestrator..."
echo "=================================================="
echo ""
python run_orchestrator.py

echo ""
echo "=================================================="
echo "✅ Quick start completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Check logs in logs/orchestrator.log"
echo "  2. View telemetry in Azure Portal"
echo "  3. Check Sentinel incidents"
echo ""
echo "For full setup guide, see RUN_GUIDE.md"

# Made with Bob
