# 🧪 SMART WORKSPACE Professional

> **AI-Powered Workspace Intelligence System for Apple Silicon M3**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/AUTOGIO/CODE_ALCHEMY)
[![Platform](https://img.shields.io/badge/platform-macOS%20M3-green.svg)](https://www.apple.com/mac/)
[![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

## 🚀 Overview

SMART WORKSPACE Professional is a streamlined Multi-Agent System focused on three core areas: **File Organization & Analysis**, **Productivity Enhancement**, and **Workflow Automation**. The system leverages local AI processing with LM Studio integration and N8N workflow automation to provide intelligent file management and productivity optimization while maintaining user privacy through local-first processing.

## ✨ Key Features

- **🤖 Multi-Agent System**: 3 specialized AI agents focused on core workflows
- **🧠 LM Studio Integration**: Support for 16+ local models
- **📊 Professional Dashboard**: Static monitoring and analytics (no real-time updates)
- **🔗 MCP Integration**: Seamless Cursor integration via Model Control Protocol
- **🔒 Privacy-First**: Local processing with no data transmission
- **📁 Smart Organization**: AI-powered file categorization and management
- **🔄 Workflow Automation**: N8N integration for automated file processing

## 🏗️ Architecture

```
CODE_ALCHEMY_PRO/
├── src/
│   ├── agents/           # 6 specialized AI agents
│   ├── core/            # Configuration and monitoring
│   ├── web/             # Streamlit dashboard
│   ├── mcp/             # Model Control Protocol
│   └── integrations/    # External service connections
├── data/
│   ├── documents/       # Organized user files
│   ├── reports/         # Analysis reports
│   ├── cache/           # System cache
│   └── logs/            # Activity logs
├── config/              # Configuration files
├── docs/                # Documentation
└── examples/            # Usage examples
```

## 🚀 Quick Start

### Prerequisites

- **macOS**: Apple Silicon M3 Mac (recommended)
- **Python**: 3.9 or higher
- **LM Studio**: Running on localhost:1234
- **Models**: GGUF models in `/Volumes/MICRO/models`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AUTOGIO/CODE_ALCHEMY_PRO.git
   cd CODE_ALCHEMY_PRO
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start LM Studio**
   - Launch LM Studio
   - Load your models
   - Ensure server is running on localhost:1234

4. **Launch the system**
   ```bash
   python launch_dashboard.py
   ```

5. **Access dashboard**
   - Open browser to `http://localhost:8501`
   - Start organizing files and analyzing content

## 📊 System Components

### 🤖 AI Agents

#### **File Organization Agent**
- **Purpose**: Intelligent file categorization and organization
- **Features**: 
  - Automatic file type detection
  - Duplicate detection using SHA256
  - Smart folder structure creation
  - Real-time processing statistics

#### **Content Analysis Agent**
- **Purpose**: Document analysis and content understanding
- **Features**:
  - Text sentiment analysis
  - Document summarization
  - Key information extraction
  - Multimodal content processing

#### **Productivity Agent**
- **Purpose**: Workflow optimization and task management
- **Features**:
  - Task prioritization and analysis
  - Time tracking and efficiency metrics
  - Workflow automation suggestions
  - N8N integration and automation
  - Performance optimization recommendations

### 🧠 Model Management

#### **Supported Models**
- **DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf**: General purpose
- **Meta-Llama-3.1-8B-Instruct-Q6_K.gguf**: Instruction following
- **Phi-4-mini-reasoning-Q8_0.gguf**: Reasoning tasks
- **TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf**: Fast responses
- **Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf**: Vision tasks

#### **Model Selection**
- **File Organization**: DeepSeek-R1 for categorization
- **Content Analysis**: Llama-3.1 for document understanding
- **Productivity**: Llama-3.1 for workflow analysis and N8N automation

### 📊 Dashboard Features

#### **Static Monitoring**
- **System Resources**: Basic system information (no live updates)
- **Apple Silicon Metrics**: Static hardware information
- **Agent Activity**: Task completion through reports
- **Model Performance**: Performance analysis through static data

#### **File Management**
- **Upload Interface**: Drag-and-drop file upload
- **Organization View**: File categorization through reports
- **Duplicate Detection**: Visual duplicate identification
- **Processing Reports**: Detailed analysis reports

#### **Agent Control**
- **Enable/Disable**: Control individual agents
- **Performance Metrics**: Agent efficiency through reports
- **Task Queue**: Task status through reports
- **Error Handling**: Error reporting through logs

## 🔧 Configuration

### Environment Variables

```bash
# GitHub Integration (optional)
export GITHUB_TOKEN="your_github_token"
export GITHUB_USERNAME="your_username"

# LM Studio Configuration
export LM_STUDIO_URL="http://localhost:1234"

# Model Path
export MODELS_PATH="/Volumes/MICRO/models"
```

### Configuration Files

#### **System Settings** (`config/settings.json`)
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

## 📈 Usage Examples

### Basic File Organization

1. **Add files to process**
   ```bash
   cp ~/Documents/*.pdf data/documents/
   cp ~/Downloads/*.txt data/documents/
   ```

2. **Launch system**
   ```bash
   python launch_dashboard.py
   ```

3. **Monitor organization**
   - Check dashboard for progress updates
   - View organized files in `data/documents/`
   - Review reports in `data/reports/`

### Content Analysis

1. **Upload documents**
   - Use dashboard upload interface
   - Or copy files to `data/documents/`

2. **Run analysis**
   - Enable Content Analysis agent
   - Monitor analysis progress
   - View insights in dashboard

3. **Review results**
   - Check analysis reports
   - Export insights as JSON
   - Share results via dashboard

### Code Intelligence

1. **Add code files**
   ```bash
   cp ~/Projects/*.py data/documents/
   cp ~/Projects/*.js data/documents/
   ```

2. **Enable code analysis**
   - Activate Code Intelligence agent
   - Select language-specific models
   - Monitor analysis progress

3. **Review suggestions**
   - Check code quality scores
   - Review optimization suggestions
   - Apply security recommendations

## 🔒 Security & Privacy

### Privacy-First Design
- **Local Processing**: All data processed locally
- **No External Uploads**: Files stay on your system
- **Secure Storage**: Local file system only
- **Privacy Compliance**: GDPR and local privacy laws

### Security Features
- **File Integrity**: SHA256 hash verification
- **Access Control**: Local system access only
- **Audit Logging**: Comprehensive activity logs
- **Secure Configuration**: Environment-based settings

## 🍎 Apple Silicon Optimization

### M3-Specific Features
- **Neural Engine**: 16-core Neural Engine utilization
- **Unified Memory**: 16GB unified memory optimization
- **Parallel Processing**: Multi-core task distribution
- **Dynamic Caching**: Intelligent cache management

### Performance Benefits
- **Faster Processing**: Hardware-accelerated AI inference
- **Lower Latency**: Optimized for M3 architecture
- **Better Efficiency**: Reduced power consumption
- **Enhanced Security**: Hardware-based security features

## 🔧 Troubleshooting

### Common Issues

#### **Dashboard Won't Start**
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+

# Check port availability
lsof -i :8501
```

#### **LM Studio Connection Issues**
```bash
# Check LM Studio is running
curl http://localhost:1234/v1/models

# Verify model path
ls /Volumes/MICRO/models
```

#### **Performance Issues**
- **High CPU Usage**: Reduce concurrent agents
- **Memory Issues**: Lower batch sizes
- **Slow Response**: Check model loading

### Debug Mode
Enable debug mode in dashboard settings for detailed logging.

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION_GUIDE.md)**: Detailed setup instructions
- **[User Guide](docs/USER_GUIDE.md)**: Complete usage documentation
- **[API Reference](docs/API_REFERENCE.md)**: Technical documentation
- **[Examples](examples/)**: Usage examples and tutorials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 🆘 Support

- **Documentation**: Check the docs folder
- **Issues**: Report bugs on GitHub
- **Discussions**: Join community discussions
- **Email**: Contact for enterprise support

## 🎯 Roadmap

### Planned Features
- **Mobile Support**: Responsive design for mobile devices
- **API Access**: REST API for external integrations
- **Plugin System**: Extensible plugin architecture
- **Advanced Analytics**: Machine learning-based insights
- **Cloud Sync**: Cloud-based settings synchronization

### Performance Improvements
- **GPU Acceleration**: Enhanced GPU utilization
- **Distributed Processing**: Multi-machine support
- **Advanced Caching**: Intelligent cache optimization
- **Real-time Collaboration**: Multi-user support

---

**Made with ❤️ for Apple Silicon users**
