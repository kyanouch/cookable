#!/bin/bash
# Quick Start Script for Cookable App
# This script automates the setup and running of the application

echo "╔════════════════════════════════════════╗"
echo "║  🍳 COOKABLE - Quick Start Script     ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if UV is installed
echo "🔍 Checking if UV is installed..."
if ! command -v uv &> /dev/null; then
    echo ""
    echo "❌ UV is not installed on your system."
    echo ""
    echo "Installing UV now..."
    echo ""

    # Detect OS and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # macOS or Linux
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "⚠️  Automatic installation not supported for your OS."
        echo "Please install UV manually from: https://github.com/astral-sh/uv"
        exit 1
    fi

    echo ""
    echo "✅ UV installed successfully!"
    echo ""
    echo "⚠️  Please restart your terminal and run this script again."
    exit 0
else
    echo "✅ UV is already installed ($(uv --version))"
fi

echo ""
echo "📦 Installing project dependencies..."
echo "   - streamlit"
echo "   - scikit-learn"
echo "   - pandas"
echo "   - numpy"
echo ""

# Install dependencies
uv add streamlit scikit-learn pandas numpy > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies."
    echo "Please run manually: uv add streamlit scikit-learn pandas numpy"
    exit 1
fi

echo ""
echo "🚀 Starting Cookable app..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  The app will open automatically in your browser"
echo "  URL: http://localhost:8501"
echo ""
echo "  Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the Streamlit app
uv run streamlit run 1_🏠_Home.py
