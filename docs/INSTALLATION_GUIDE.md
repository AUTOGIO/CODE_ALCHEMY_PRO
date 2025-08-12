# 📦 CODE_ALCHEMY Professional - Installation Guide

## 🎯 Overview

This guide will walk you through installing and setting up CODE_ALCHEMY Professional on your Apple Silicon Mac. The system is optimized for M3 chips but works on any Apple Silicon Mac.

## 📋 Prerequisites

### System Requirements

- **macOS**: 12.0 (Monterey) or higher
- **Hardware**: Apple Silicon Mac (M1/M2/M3 recommended)
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 10GB free space
- **Python**: 3.9 or higher

### Required Software

1. **Python 3.9+**
   ```bash
   # Check Python version
   python3 --version
   
   # Install if needed (using Homebrew)
   brew install python@3.9
   ```

2. **LM Studio**
   - Download from [LM Studio](https://lmstudio.ai/)
   - Install and configure for local model serving
   - Ensure server runs on `localhost:1234`

3. **GGUF Models**
   - Download models to `/Volumes/MICRO/models/`
   - Recommended models:
     - `DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf`
     - `Meta-Llama-3.1-8B-Instruct-Q6_K.gguf`
     - `Phi-4-mini-reasoning-Q8_0.gguf`
     - `TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf`

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/AUTOGIO/CODE_ALCHEMY_PRO.git

# Navigate to project directory
cd CODE_ALCHEMY_PRO
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv code_alchemy_env

# Activate virtual environment
source code_alchemy_env/bin/activate

# Verify activation
which python
# Should show: /path/to/CODE_ALCHEMY_PRO/code_alchemy_env/bin/python
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, plotly, pandas, psutil; print('✅ Dependencies installed successfully')"
```

### Step 4: Configure LM Studio

1. **Launch LM Studio**
   - Open LM Studio application
   - Go to Settings → Server
   - Enable "Start server at startup"
   - Set port to `1234`

2. **Load Models**
   - Go to Models tab
   - Add your GGUF models
   - Ensure models are loaded and ready

3. **Test Connection**
   ```bash
   # Test LM Studio connection
   curl http://localhost:1234/v1/models
   ```

### Step 5: Configure Model Path

```bash
# Create models directory (if using local storage)
mkdir -p /Volumes/MICRO/models

# Or set environment variable for different path
export MODELS_PATH="/path/to/your/models"
```

### Step 6: Initialize System

```bash
# Create necessary directories
mkdir -p data/{documents,reports,cache,logs}

# Set permissions
chmod 755 data/

# Test system initialization
python -c "from src.core.config import config; print('✅ Configuration loaded successfully')"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# LM Studio Configuration
LM_STUDIO_URL=http://localhost:1234

# Model Configuration
MODELS_PATH=/Volumes/MICRO/models

# GitHub Integration (optional)
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_github_username

# System Configuration
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### System Settings

Edit `config/settings.json` for custom configuration:

```json
{
  "system": {
    "environment": "production",
    "debug_mode": false,
    "log_level": "INFO"
  },
  "models": {
    "server_url": "http://localhost:1234",
    "default_model": "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
  },
  "agents": {
    "file_organization": {"enabled": true},
    "content_analysis": {"enabled": true},
    "code_intelligence": {"enabled": true},
    "productivity": {"enabled": true},
    "security": {"enabled": true}
  }
}
```

## 🧪 Testing Installation

### Quick Test

```bash
# Test basic functionality
python launch_dashboard.py

# Check if dashboard opens at http://localhost:8501
```

### Comprehensive Test

```bash
# Run system tests
python -m pytest tests/ -v

# Test file organization
python examples/01_code_analysis_project.py

# Test content analysis
python examples/02_document_processing.py
```

## 🚀 First Launch

### 1. Start LM Studio
- Launch LM Studio
- Ensure server is running on localhost:1234
- Load your preferred models

### 2. Launch Dashboard
```bash
# From project directory
python launch_dashboard.py
```

### 3. Access Dashboard
- Open browser to `http://localhost:8501`
- You should see the CODE_ALCHEMY Professional dashboard

### 4. Test File Organization
```bash
# Add some test files
cp ~/Documents/*.pdf data/documents/ 2>/dev/null || echo "No PDFs found"
cp ~/Downloads/*.txt data/documents/ 2>/dev/null || echo "No TXTs found"

# Check dashboard for file processing
```

## 🔧 Troubleshooting

### Common Issues

#### **Python Version Issues**
```bash
# Check Python version
python3 --version

# If version is < 3.9, upgrade
brew install python@3.9
```

#### **Dependency Installation Issues**
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install streamlit plotly pandas psutil
```

#### **LM Studio Connection Issues**
```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# If connection fails:
# 1. Ensure LM Studio is running
# 2. Check port 1234 is not blocked
# 3. Restart LM Studio server
```

#### **Permission Issues**
```bash
# Fix directory permissions
chmod -R 755 data/
chmod -R 755 config/

# Fix file permissions
chmod 644 *.py
chmod 644 *.md
```

#### **Port Conflicts**
```bash
# Check if port 8501 is in use
lsof -i :8501

# Kill process if needed
kill -9 $(lsof -t -i:8501)

# Or use different port
streamlit run src/web/app.py --server.port 8502
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug environment variable
export DEBUG_MODE=true

# Or edit config/settings.json
{
  "system": {
    "debug_mode": true,
    "log_level": "DEBUG"
  }
}
```

## 📊 Performance Optimization

### Apple Silicon Optimization

1. **Enable Neural Engine**
   ```json
   {
     "m3_optimization": {
       "neural_engine_enabled": true,
       "parallel_processing": true
     }
   }
   ```

2. **Memory Management**
   ```json
   {
     "m3_optimization": {
       "unified_memory_limit": "8GB",
       "dynamic_caching": true
     }
   }
   ```

### System Tuning

1. **Reduce Concurrent Agents**
   - Start with 2-3 agents enabled
   - Gradually increase based on performance

2. **Model Selection**
   - Use smaller models for faster processing
   - Load only necessary models

3. **Batch Processing**
   - Process files in smaller batches
   - Monitor memory usage

## 🔒 Security Considerations

### Local Processing
- All data is processed locally
- No files are uploaded to external servers
- Privacy is maintained through local-first approach

### Access Control
- Dashboard runs on localhost only
- No external network access by default
- Secure configuration management

### Data Protection
- Files are stored locally in `data/` directory
- SHA256 hashing for file integrity
- Comprehensive audit logging

## 📚 Next Steps

After successful installation:

1. **Read the User Guide**: `docs/USER_GUIDE.md`
2. **Explore Examples**: `examples/` directory
3. **Configure Integrations**: Set up GitHub/Google Drive if needed
4. **Customize Settings**: Adjust configuration for your workflow
5. **Join Community**: Report issues and share feedback

## 🆘 Getting Help

### Documentation
- **User Guide**: `docs/USER_GUIDE.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **Examples**: `examples/` directory

### Support Channels
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Community support and questions
- **Email**: Enterprise support inquiries

### Common Resources
- **LM Studio Documentation**: https://lmstudio.ai/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **Apple Silicon Optimization**: https://developer.apple.com/metal/

---

**Installation complete! 🎉**

Your CODE_ALCHEMY Professional system is now ready for use. Start by launching the dashboard and exploring the features.
