#!/bin/bash

# CODE_ALCHEMY Professional MCP Setup Script
# Configure MCP servers for Cursor integration

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_DIR="$HOME/Documents/CODE_ALCHEMY_PRO"
MCP_CONFIG_DIR="$HOME/.cursor"
MCP_CONFIG_FILE="$MCP_CONFIG_DIR/mcp.json"

echo -e "${BLUE}🔧 CODE_ALCHEMY Professional MCP Setup${NC}"
echo "============================================="
echo ""

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Project directory not found: $PROJECT_DIR${NC}"
    echo "Please run the installation script first:"
    echo "  ./scripts/install.sh"
    exit 1
fi

# Create MCP config directory
echo -e "${BLUE}📁 Creating MCP configuration directory...${NC}"
mkdir -p "$MCP_CONFIG_DIR"

# Create MCP configuration
echo -e "${BLUE}⚙️ Creating MCP configuration...${NC}"
cat > "$MCP_CONFIG_FILE" << 'MCP_EOF'
{
  "mcpServers": {
    "lm-studio-bridge": {
      "command": "python",
      "args": ["$HOME/Documents/CODE_ALCHEMY_PRO/src/mcp/lm_studio_bridge.py"],
      "env": {
        "LM_STUDIO_URL": "http://localhost:1234"
      }
    },
    "model-manager": {
      "command": "python",
      "args": ["$HOME/Documents/CODE_ALCHEMY_PRO/src/mcp/model_manager.py"],
      "env": {
        "MODELS_PATH": "/Volumes/MICRO/models"
      }
    },
    "code-assistant": {
      "command": "python",
      "args": ["$HOME/Documents/CODE_ALCHEMY_PRO/src/mcp/code_assistant.py"],
      "env": {
        "CODE_MODELS": "Phi-4-mini-reasoning-GGUF,DeepSeek-R1-Distill-Llama-8B-GGUF"
      }
    }
  }
}
MCP_EOF

echo -e "${GREEN}✅ MCP configuration created at $MCP_CONFIG_FILE${NC}"
echo -e "${YELLOW}🔄 Restart Cursor to apply MCP configuration${NC}"
echo ""
echo "Available MCP servers:"
echo "  - lm-studio-bridge: Direct access to LM Studio models"
echo "  - model-manager: Intelligent model selection"
echo "  - code-assistant: Context-aware code suggestions"
echo ""
echo "Usage in Cursor:"
echo "  @lm-studio-bridge list_models"
echo "  @model-manager recommend_model task=\"code analysis\""
echo "  @code-assistant analyze_code file=\"main.py\"" 