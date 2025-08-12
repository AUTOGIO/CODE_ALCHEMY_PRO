# 📦 CODE_ALCHEMY Professional Installation Guide

## 🎯 Overview

This guide provides step-by-step instructions for installing CODE_ALCHEMY Professional on your Apple Silicon M3 iMac. The system is optimized for macOS and requires specific hardware and software prerequisites.

## 📋 Prerequisites

### Hardware Requirements
- **Mac**: Apple Silicon M1/M2/M3 Mac
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB free space minimum
- **Network**: Internet connection for initial setup

### Software Requirements
- **macOS**: 11.0+ (Big Sur or later)
- **Python**: 3.9 or higher
- **LM Studio**: Latest version with local models
- **Git**: For version control (optional)

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

#### Step 1: Download the Project
```bash
# Clone the repository
git clone https://github.com/AUTOGIO/CODE_ALCHEMY_PRO.git
cd CODE_ALCHEMY_PRO

# Or download and extract if no Git
curl -L https://github.com/AUTOGIO/CODE_ALCHEMY_PRO/archive/main.zip -o CODE_ALCHEMY_PRO.zip
unzip CODE_ALCHEMY_PRO.zip
cd CODE_ALCHEMY_PRO-main
```

#### Step 2: Run Installation Script
```bash
# Make script executable
chmod +x scripts/install.sh

# Run installation
./scripts/install.sh
```

The installation script will:
- ✅ Check system requirements
- ✅ Create project structure
- ✅ Set up virtual environment
- ✅ Install Python dependencies
- ✅ Create configuration files
- ✅ Set up launch scripts

#### Step 3: Verify Installation
```bash
# Check if everything is installed
python3 -c "import streamlit, plotly, pandas; print('✅ Dependencies installed')"

# Check project structure
ls -la ~/Documents/CODE_ALCHEMY_PRO/
```

### Method 2: Manual Installation

#### Step 1: Create Project Directory
```bash
# Create project directory
mkdir -p ~/Documents/CODE_ALCHEMY_PRO
cd ~/Documents/CODE_ALCHEMY_PRO
```

#### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### Step 3: Install Dependencies
```bash
# Install core dependencies
pip install streamlit plotly pandas numpy chardet python-dotenv rich pyyaml aiohttp

# Install MCP dependencies
pip install mcp

# Install development dependencies
pip install pytest black flake8 mypy
```

#### Step 4: Create Configuration Files
```bash
# Create config directory
mkdir -p config

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
```

## 🔧 Configuration

### LM Studio Setup

1. **Download LM Studio**
   - Visit [LM Studio](https://lmstudio.ai/)
   - Download the latest version for macOS

2. **Load Your Models**
   - Open LM Studio
   - Navigate to your models directory: `/Volumes/MICRO/models`
   - Load a model (recommended: DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf)

3. **Start the Server**
   - In LM Studio, go to "Local Server"
   - Click "Start Server"
   - Verify it's running on `http://localhost:1234`

### MCP Configuration for Cursor

```bash
# Set up MCP configuration
./scripts/setup_mcp.sh

# Restart Cursor to apply changes
```

## 🧪 Testing the Installation

### Test 1: Basic System Check
```bash
cd ~/Documents/CODE_ALCHEMY_PRO
source venv/bin/activate

# Test imports
python3 -c "
import streamlit
import plotly
import pandas
import numpy
print('✅ All core dependencies working')
"
```

### Test 2: LM Studio Connection
```bash
# Test LM Studio connection
curl -s http://localhost:1234/v1/models | head -20
```

### Test 3: Launch Web Interface
```bash
# Launch the system
./scripts/launch.sh

# Open http://localhost:8501 in your browser
```

## 🔍 Troubleshooting

### Common Issues

#### Issue: Python Version Error
```bash
# Check Python version
python3 --version

# If version < 3.9, install newer Python
brew install python@3.11
```

#### Issue: Virtual Environment Not Found
```bash
# Recreate virtual environment
cd ~/Documents/CODE_ALCHEMY_PRO
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: LM Studio Not Running
```bash
# Check if LM Studio is running
curl -s http://localhost:1234/v1/models

# If not running, start LM Studio and load a model
```

#### Issue: Port Already in Use
```bash
# Check what's using port 8501
lsof -i :8501

# Kill the process or change port
pkill -f streamlit
```

### Performance Optimization

#### M3-Specific Optimizations
```bash
# Check M3 optimization settings
cat config/system_config.yaml | grep -A 5 "m3_optimization"
```

#### Memory Management
```bash
# Monitor memory usage
top -l 1 | grep "PhysMem"

# If memory usage is high, adjust settings
# Edit config/system_config.yaml
# Reduce unified_memory_limit to "8GB"
```

## 📊 System Verification

### Check Installation Status
```bash
# Run system verification
python3 -c "
import sys
import os
print(f'Python version: {sys.version}')
print(f'Working directory: {os.getcwd()}')
print(f'Virtual environment: {os.environ.get(\"VIRTUAL_ENV\", \"Not activated\")}')
"
```

### Verify All Components
```bash
# Check all components are working
cd ~/Documents/CODE_ALCHEMY_PRO
source venv/bin/activate

# Test core modules
python3 -c "
from src.core.config import config
print('✅ Configuration system working')
"

# Test web interface
python3 -c "
import streamlit
print('✅ Streamlit working')
"

# Test MCP
python3 -c "
import mcp
print('✅ MCP working')
"
```

## 🎉 Installation Complete

Once all tests pass, your CODE_ALCHEMY Professional system is ready to use!

### Next Steps
1. **Launch the system**: `./scripts/launch.sh`
2. **Access the dashboard**: http://localhost:8501
3. **Configure MCP**: `./scripts/setup_mcp.sh`
4. **Read the User Guide**: [docs/USER_GUIDE.md](USER_GUIDE.md)

## 📞 Support

If you encounter issues during installation:

1. **Check the logs**: `tail -f data/logs/system.log`
2. **Verify prerequisites**: Ensure all requirements are met
3. **Contact support**: support@alchemist-ai-labs.com
4. **Check GitHub issues**: [GitHub Issues](https://github.com/AUTOGIO/CODE_ALCHEMY/issues)

---

**Installation completed successfully! 🚀** 