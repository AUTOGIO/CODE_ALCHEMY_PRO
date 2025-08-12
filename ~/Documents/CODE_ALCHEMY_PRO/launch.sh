#!/bin/bash

# CODE_ALCHEMY Professional Launch Script
# Optimized for M3 iMac with LM Studio integration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_DIR="$HOME/Documents/CODE_ALCHEMY_PRO"
VENV_NAME="venv"
WEB_PORT="8501"
LM_STUDIO_URL="http://localhost:1234"

echo -e "${BLUE}🚀 CODE_ALCHEMY Professional Launch${NC}"
echo "========================================"
echo ""

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Project directory not found: $PROJECT_DIR${NC}"
    echo "Please run the installation script first:"
    echo "  ./scripts/install.sh"
    exit 1
fi

cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "Please run the installation script first:"
    echo "  ./scripts/install.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source "$VENV_NAME/bin/activate"

# Check LM Studio connection
echo -e "${BLUE}🔍 Checking LM Studio connection...${NC}"
if curl -s "$LM_STUDIO_URL/v1/models" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ LM Studio is running${NC}"
else
    echo -e "${YELLOW}⚠️ LM Studio not detected on $LM_STUDIO_URL${NC}"
    echo "Please start LM Studio first:"
    echo "1. Open LM Studio"
    echo "2. Load a model"
    echo "3. Start the server"
    echo ""
    echo "Continuing without LM Studio..."
fi

# Check if required packages are installed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
if python -c "import streamlit, plotly, pandas" 2>/dev/null; then
    echo -e "${GREEN}✅ Dependencies are installed${NC}"
else
    echo -e "${YELLOW}⚠️ Some dependencies are missing${NC}"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Launch the web interface
echo -e "${BLUE}🌐 Starting CODE_ALCHEMY Professional...${NC}"
echo "Web interface will be available at: http://localhost:$WEB_PORT"
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
streamlit run src/web/app.py \
    --server.port "$WEB_PORT" \
    --server.address localhost \
    --server.headless false \
    --browser.gatherUsageStats false 