#!/bin/bash

# MCP GitHub Repository Analyzer - Virtual Environment Activator
# This script activates the virtual environment and provides helpful commands

echo "🚀 MCP GitHub Repository Analyzer"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
if ! python -c "import mcp" 2>/dev/null; then
    echo "📦 Installing packages..."
    pip install -r requirements.txt
    echo "✅ Packages installed!"
else
    echo "✅ Packages already installed!"
fi

echo ""
echo "🎯 Available commands:"
echo "  python test_mcp_server.py     - Test the setup"
echo "  python mcp_server.py          - Run the MCP server"
echo "  python example_client.py      - Run the example client"
echo ""
echo "🔧 To deactivate the virtual environment:"
echo "  deactivate"
echo ""
echo "✨ Your virtual environment is ready!"
echo "   You can now run the MCP server and tools." 