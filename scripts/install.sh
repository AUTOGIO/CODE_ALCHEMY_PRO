#!/bin/bash

# CODE_ALCHEMY Professional Installation Script
# Optimized for M3 iMac with LM Studio integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Configuration
PROJECT_NAME="CODE_ALCHEMY_PRO"
PROJECT_DIR="$HOME/Documents/$PROJECT_NAME"
PYTHON_VERSION="3.11"
VENV_NAME="venv"

# Check system requirements
check_system_requirements() {
    log_step "Checking system requirements..."
    
    # Check macOS version
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "This script is designed for macOS"
        exit 1
    fi
    
    # Check if running on Apple Silicon
    if [[ $(uname -m) != "arm64" ]]; then
        log_warning "This script is optimized for Apple Silicon (M1/M2/M3)"
    fi
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log_success "Python $PYTHON_VER detected"
    
    # Check available disk space
    DISK_SPACE=$(df -h "$HOME" | awk 'NR==2 {print $4}' | sed 's/Gi//')
    if (( $(echo "$DISK_SPACE < 5" | bc -l) )); then
        log_warning "Low disk space: $DISK_SPACE GB available (5 GB recommended)"
    fi
    
    log_success "System requirements check completed"
}

# Create project structure
create_project_structure() {
    log_step "Creating project structure..."
    
    # Create main project directory
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Create directory structure
    mkdir -p {src/{core,agents/{base,file_organization,content_analysis,code_intelligence,productivity,security},mcp,web/{components,static/{css,js,images}},integrations},config,scripts,tests/{unit,integration,performance},data/{logs,cache,models},docs}
    
    # Create __init__.py files for Python packages
    find src -type d -exec touch {}/__init__.py \;
    
    log_success "Project structure created"
}

# Create virtual environment
create_virtual_environment() {
    log_step "Creating virtual environment..."
    
    cd "$PROJECT_DIR"
    
    # Create virtual environment
    python3 -m venv "$VENV_NAME"
    
    # Activate virtual environment
    source "$VENV_NAME/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    log_success "Virtual environment created and activated"
}

# Install dependencies
install_dependencies() {
    log_step "Installing Python dependencies..."
    
    cd "$PROJECT_DIR"
    source "$VENV_NAME/bin/activate"
    
    # Install core dependencies
    pip install streamlit plotly pandas numpy chardet python-dotenv rich pyyaml aiohttp
    
    # Install MCP dependencies
    pip install mcp
    
    # Install development dependencies
    pip install pytest black flake8 mypy
    
    log_success "Dependencies installed successfully"
}

# Create configuration files
create_configuration_files() {
    log_step "Creating configuration files..."
    
    cd "$PROJECT_DIR"
    
    # Create system configuration
    cat > config/system_config.yaml << 'EOF'
environment: development
m3_optimization:
  neural_engine_enabled: true
  unified_memory_limit: "12GB"
  parallel_processing: true
  dynamic_caching: true
  core_utilization: 8

model_config:
  models_path: "/Volumes/MICRO/models"
  server_url: "http://localhost:1234"
  default_model: "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
  fallback_model: "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"
  reasoning_model: "Phi-4-mini-reasoning-Q8_0.gguf"
  fast_model: "TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf"
  vision_model: "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
EOF

    # Create MCP configuration
    cat > config/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "lm-studio-bridge": {
      "command": "python",
      "args": ["src/mcp/lm_studio_bridge.py"],
      "env": {
        "LM_STUDIO_URL": "http://localhost:1234"
      }
    },
    "model-manager": {
      "command": "python",
      "args": ["src/mcp/model_manager.py"],
      "env": {
        "MODELS_PATH": "/Volumes/MICRO/models"
      }
    },
    "code-assistant": {
      "command": "python",
      "args": ["src/mcp/code_assistant.py"],
      "env": {
        "CODE_MODELS": "Phi-4-mini-reasoning-GGUF,DeepSeek-R1-Distill-Llama-8B-GGUF"
      }
    }
  }
}
EOF

    # Create requirements.txt
    cat > requirements.txt << 'EOF'
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
chardet>=5.2.0
python-dotenv>=1.0.0
rich>=13.0.0
pyyaml>=6.0
aiohttp>=3.8.0
mcp>=0.1.0
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
EOF

    # Create setup.py
    cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="code-alchemy-pro",
    version="2.0.0",
    description="CODE_ALCHEMY Professional - AI-Powered Desktop Intelligence System",
    author="AUTOGIO",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "aiohttp>=3.8.0",
        "mcp>=0.1.0",
    ],
    python_requires=">=3.9",
)
EOF

    log_success "Configuration files created"
}

# Create launch scripts
create_launch_scripts() {
    log_step "Creating launch scripts..."
    
    cd "$PROJECT_DIR"
    
    # Create main launch script
    cat > launch.sh << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional Launch Script

set -e

PROJECT_DIR="$HOME/Documents/CODE_ALCHEMY_PRO"
VENV_NAME="venv"

echo "🚀 Launching CODE_ALCHEMY Professional..."

# Check if virtual environment exists
if [ ! -d "$PROJECT_DIR/$VENV_NAME" ]; then
    echo "❌ Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source "$PROJECT_DIR/$VENV_NAME/bin/activate"

# Check if LM Studio is running
if ! curl -s http://localhost:1234/v1/models > /dev/null; then
    echo "⚠️ LM Studio not detected on localhost:1234"
    echo "Please start LM Studio first:"
    echo "1. Open LM Studio"
    echo "2. Load a model"
    echo "3. Start the server"
fi

# Launch the web interface
echo "🌐 Starting web interface..."
cd "$PROJECT_DIR"
streamlit run src/web/app.py --server.port 8501 --server.address localhost

EOF

    # Create MCP configuration script
    cat > setup_mcp.sh << 'EOF'
#!/bin/bash

# Setup MCP configuration for Cursor

MCP_CONFIG_DIR="$HOME/.cursor"
MCP_CONFIG_FILE="$MCP_CONFIG_DIR/mcp.json"

echo "🔧 Setting up MCP configuration for Cursor..."

# Create MCP config directory
mkdir -p "$MCP_CONFIG_DIR"

# Create MCP configuration
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

echo "✅ MCP configuration created at $MCP_CONFIG_FILE"
echo "🔄 Restart Cursor to apply MCP configuration"
EOF

    # Make scripts executable
    chmod +x launch.sh setup_mcp.sh
    
    log_success "Launch scripts created"
}

# Create documentation
create_documentation() {
    log_step "Creating documentation..."
    
    cd "$PROJECT_DIR/docs"
    
    # Create README
    cat > README.md << 'EOF'
# CODE_ALCHEMY Professional

## Overview
CODE_ALCHEMY Professional is an AI-powered desktop intelligence system optimized for Apple Silicon M3 iMacs. It provides intelligent file organization, content analysis, and productivity optimization through a sophisticated Multi-Agent System.

## Features
- �� Multi-Agent System with 5 specialized agents
- 🧠 LM Studio integration with 46+ models
- 📊 Professional web dashboard
- 🔗 MCP integration for Cursor
- 🚀 M3 Neural Engine optimization
- 🔒 Privacy-first local processing

## Quick Start
1. Run `./scripts/install.sh` to install
2. Run `./launch.sh` to start the system
3. Open http://localhost:8501 in your browser

## MCP Integration
Run `./setup_mcp.sh` to configure MCP servers for Cursor integration.

## System Requirements
- macOS 11.0+ (Big Sur or later)
- Apple Silicon M1/M2/M3
- Python 3.9+
- 8GB RAM minimum (16GB recommended)
- LM Studio with local models

## Architecture
- **Core**: Configuration management and system coordination
- **Agents**: Specialized AI agents for different tasks
- **Web**: Professional Streamlit dashboard
- **MCP**: Model Control Protocol integration
- **Integrations**: GitHub, Google Drive, LM Studio

## License
Proprietary - Alchemist AI Labs
EOF

    log_success "Documentation created"
}

# Main installation function
main() {
    echo "🧪 CODE_ALCHEMY Professional Installation"
    echo "========================================"
    echo ""
    
    check_system_requirements
    create_project_structure
    create_virtual_environment
    install_dependencies
    create_configuration_files
    create_launch_scripts
    create_documentation
    
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Start LM Studio and load a model"
    echo "2. Run: cd $PROJECT_DIR && ./launch.sh"
    echo "3. Open http://localhost:8501 in your browser"
    echo "4. Run ./setup_mcp.sh to configure MCP for Cursor" 