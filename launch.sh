#!/bin/bash

# SMART WORKSPACE Professional Launcher
# Launch the complete AI-powered workspace intelligence system

echo "🧪 SMART WORKSPACE Professional"
echo "=================================================="
echo "AI-Powered Workspace Intelligence System"
echo "Optimized for Apple Silicon M3"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "src/web/app.py" ]; then
    echo "❌ Error: Please run this script from the SMART_WORKSPACE_PRO directory"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $python_version detected. Required: Python $required_version or higher"
    exit 1
fi

echo "✅ Python $python_version - Compatible"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check LM Studio connection
echo "🤖 Checking LM Studio connection..."
if curl -s http://localhost:1234/v1/models > /dev/null; then
    echo "✅ LM Studio connected"
else
    echo "⚠️  LM Studio not available - some features may be limited"
fi

# Launch the workspace
echo "🚀 Launching SMART WORKSPACE Professional..."
echo "📊 Workspace will open in your browser at http://localhost:8501"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

python launch_workspace.py 