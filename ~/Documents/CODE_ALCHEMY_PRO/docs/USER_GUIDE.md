# 📚 CODE_ALCHEMY Professional User Guide

## 🎯 Overview

Welcome to CODE_ALCHEMY Professional! This guide will help you master the AI-powered desktop intelligence system designed for Apple Silicon M3. Learn how to use all features, optimize performance, and maximize productivity.

## 🚀 Quick Start

### First Launch
```bash
# Start the system
cd ~/Documents/CODE_ALCHEMY_PRO
./scripts/launch.sh

# Access the dashboard
open http://localhost:8501
```

### System Dashboard
The main dashboard provides:
- **📊 Real-time metrics**: System performance and agent status
- **🤖 Agent controls**: Start/stop individual agents
- **📁 File organization**: Monitor file categorization
- **🧠 AI insights**: Confidence scores and recommendations

## 🎛️ Dashboard Navigation

### Main Interface
```
┌─────────────────────────────────────┐
│ 🧪 CODE_ALCHEMY Professional       │
├─────────────────────────────────────┤
│ 📊 Dashboard │ 🤖 Agents │ 📁 Files │
│ 📈 Analytics │ ⚙️ Settings │ 🔗 Integrations │
└─────────────────────────────────────┘
```

### Sidebar Controls
- **System Status**: CPU, Memory, Neural Engine usage
- **Quick Actions**: Refresh, Analyze, Organize
- **Agent Controls**: Individual agent toggles
- **Performance Metrics**: Real-time monitoring

## 🤖 Multi-Agent System

### File Organization Agent
**Purpose**: Intelligent file categorization and organization

**Features**:
- Automatic file type detection
- Smart folder creation
- Security-aware handling
- Pattern-based organization

**Usage**:
```bash
# Organize desktop files
Click "📁 Organize Files" in dashboard

# Monitor organization
View "File Organization" section in analytics
```

**Configuration**:
```yaml
# config/agent_config.yaml
file_organization:
  enabled: true
  model: "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
  batch_size: 8
  memory_limit: "2GB"
```

### Content Analysis Agent
**Purpose**: Deep content understanding and analysis

**Features**:
- Semantic content analysis
- Technology stack detection
- Document classification
- Multimodal analysis (images, documents)

**Usage**:
```bash
# Analyze content
Click "🧠 Analyze Content" in dashboard

# View insights
Check "Content Analysis" section in analytics
```

### Code Intelligence Agent
**Purpose**: Advanced code analysis and suggestions

**Features**:
- Code review and analysis
- Programming language detection
- Best practice suggestions
- Security vulnerability scanning

**Usage**:
```bash
# Analyze code project
Click "💻 Analyze Code" in dashboard

# Get suggestions
View "Code Intelligence" section in analytics
```

### Productivity Agent
**Purpose**: Workflow optimization and time management

**Features**:
- Workflow pattern analysis
- Time tracking and optimization
- Performance recommendations
- Task automation suggestions

**Usage**:
```bash
# Optimize workflow
Click "⚡ Optimize Productivity" in dashboard

# View recommendations
Check "Productivity" section in analytics
```

### Security Monitor Agent
**Purpose**: Continuous security and privacy protection

**Features**:
- Real-time security scanning
- Privacy protection
- Threat detection
- Compliance monitoring

**Usage**:
```bash
# Security scan
Click "🔒 Security Scan" in dashboard

# View security status
Check "Security" section in analytics
```

## 🔗 MCP Integration

### Cursor Integration
**Setup**:
```bash
# Configure MCP for Cursor
./scripts/setup_mcp.sh

# Restart Cursor
# MCP servers will be available in Cursor
```

**Available MCP Servers**:
- **lm-studio-bridge**: Direct access to LM Studio models
- **model-manager**: Intelligent model selection
- **code-assistant**: Context-aware code suggestions

**Usage in Cursor**:
```
@lm-studio-bridge list_models
@model-manager recommend_model task="code analysis"
@code-assistant analyze_code file="main.py"
```

### LM Studio Integration
**Model Management**:
```bash
# List available models
curl http://localhost:1234/v1/models

# Switch models in LM Studio
# Models are automatically detected by CODE_ALCHEMY
```

**Model Selection**:
- **Default**: DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf
- **Fast**: TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf
- **Reasoning**: Phi-4-mini-reasoning-Q8_0.gguf
- **Vision**: Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf

## 📊 Analytics & Monitoring

### Performance Metrics
- **File Organization Rate**: Percentage of files successfully organized
- **AI Confidence Score**: Average confidence of AI decisions
- **System Performance**: Overall system efficiency
- **Memory Usage**: Current memory consumption
- **Response Time**: Average response time for operations

### Real-time Monitoring
```bash
# View system logs
tail -f data/logs/system.log

# Monitor performance
Check "Performance" tab in dashboard

# View agent status
Check "Agents" tab in dashboard
```

### Custom Analytics
```python
# Access analytics data
from src.web.analytics import Analytics

analytics = Analytics()
performance_data = analytics.get_performance_metrics()
```

## ⚙️ Configuration

### System Configuration
```yaml
# config/system_config.yaml
environment: development
m3_optimization:
  neural_engine_enabled: true
  unified_memory_limit: "12GB"
  parallel_processing: true
  core_utilization: 8
```

### Agent Configuration
```yaml
# config/agent_config.yaml
file_organization:
  enabled: true
  model: "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
  batch_size: 8

content_analysis:
  enabled: true
  model: "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"
  multimodal: true
```

### Model Configuration
```yaml
# config/model_config.yaml
models_path: "/Volumes/MICRO/models"
server_url: "http://localhost:1234"
default_model: "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
```

## 🔧 Advanced Usage

### Custom Workflows
```python
# Create custom workflow
from src.agents.file_organization import FileOrganizationAgent
from src.agents.content_analysis import ContentAnalysisAgent

# Initialize agents
file_agent = FileOrganizationAgent()
content_agent = ContentAnalysisAgent()

# Run custom workflow
file_agent.organize_files("/path/to/files")
content_agent.analyze_content("/path/to/content")
```

### API Integration
```python
# Use CODE_ALCHEMY as a library
from src.core.config import config
from src.web.app import CodeAlchemyApp

# Initialize system
app = CodeAlchemyApp()
app.run()
```

### Custom Models
```yaml
# Add custom model configuration
model_config:
  custom_models:
    my_model: "/path/to/custom/model.gguf"
    specialized_model: "/path/to/specialized/model.gguf"
```

## 🎯 Best Practices

### Performance Optimization
1. **Use appropriate models**: Match model size to task complexity
2. **Monitor memory usage**: Keep memory usage under 12GB
3. **Batch operations**: Group similar operations together
4. **Regular maintenance**: Clean cache and logs periodically

### Security Guidelines
1. **Keep models local**: Never upload sensitive data
2. **Regular scans**: Run security scans weekly
3. **Monitor logs**: Check for unusual activity
4. **Update regularly**: Keep system and models updated

### Productivity Tips
1. **Start with organization**: Let the system organize files first
2. **Use MCP integration**: Leverage Cursor integration for development
3. **Monitor analytics**: Track performance improvements
4. **Customize workflows**: Adapt to your specific needs

## 🔍 Troubleshooting

### Common Issues

#### Issue: Dashboard Not Loading
```bash
# Check if Streamlit is running
lsof -i :8501

# Restart the system
pkill -f streamlit
./scripts/launch.sh
```

#### Issue: Agents Not Responding
```bash
# Check agent status
Check "Agents" tab in dashboard

# Restart specific agent
Toggle agent off/on in dashboard

# Check logs
tail -f data/logs/agents.log
```

#### Issue: LM Studio Connection Failed
```bash
# Check LM Studio status
curl -s http://localhost:1234/v1/models

# Restart LM Studio
# Load model and start server
```

#### Issue: High Memory Usage
```bash
# Check memory usage
top -l 1 | grep "PhysMem"

# Adjust memory limits
# Edit config/system_config.yaml
# Reduce unified_memory_limit
```

### Performance Issues
```bash
# Monitor system performance
Check "Performance" tab in dashboard

# Optimize settings
# Adjust batch_size and memory_limit in config
```

## 📈 Advanced Features

### Custom Integrations
```python
# Add custom integration
from src.integrations.base import BaseIntegration

class CustomIntegration(BaseIntegration):
    def __init__(self):
        super().__init__("custom_integration")
    
    def process_data(self, data):
        # Custom processing logic
        return processed_data
```

### Custom Analytics
```python
# Create custom analytics
from src.web.analytics import Analytics

class CustomAnalytics(Analytics):
    def custom_metric(self):
        # Custom metric calculation
        return metric_value
```

### Workflow Automation
```bash
# Create automated workflow
# Edit scripts/automation.sh
#!/bin/bash
cd ~/Documents/CODE_ALCHEMY_PRO
source venv/bin/activate
python3 -c "from src.workflows.automation import run_workflow; run_workflow()"
```

## 📞 Support & Resources

### Getting Help
- **Documentation**: [docs/](docs/)
- **API Reference**: [docs/API_REFERENCE.md](API_REFERENCE.md)
- **Installation Guide**: [docs/INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Deployment Guide**: [docs/DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Community & Support
- **GitHub Issues**: [GitHub Issues](https://github.com/AUTOGIO/CODE_ALCHEMY/issues)
- **Email Support**: support@alchemist-ai-labs.com
- **Discord Community**: [Join our Discord](https://discord.gg/codealchemy)

### Training Resources
- **Video Tutorials**: [YouTube Channel](https://youtube.com/@codealchemy)
- **Blog Posts**: [Technical Blog](https://blog.alchemist-ai-labs.com)
- **Webinars**: [Monthly Webinars](https://alchemist-ai-labs.com/webinars)

---

**Master CODE_ALCHEMY Professional and unlock your productivity potential! 🚀** 