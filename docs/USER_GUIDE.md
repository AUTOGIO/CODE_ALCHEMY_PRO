# 📖 CODE_ALCHEMY Professional - User Guide

## 🎯 Introduction

Welcome to CODE_ALCHEMY Professional! This guide will help you master the system's features and optimize your workflow. The system is designed to be intuitive and powerful, providing AI-assisted productivity for Apple Silicon users.

## 🚀 Getting Started

### First Launch

1. **Start LM Studio**
   - Launch LM Studio application
   - Ensure server is running on localhost:1234
   - Load your preferred models

2. **Launch Dashboard**
   ```bash
   python launch_dashboard.py
   ```

3. **Access Dashboard**
   - Open browser to `http://localhost:8501`
   - You'll see the main dashboard interface

### Dashboard Overview

The dashboard is organized into several key sections:

- **📊 Overview**: System status and key metrics
- **🤖 Agents**: Control and monitor AI agents
- **📁 Files**: File organization and management
- **🧠 Models**: AI model management and testing
- **🔗 Integrations**: External service connections
- **⚙️ Settings**: System configuration

## 🤖 Working with AI Agents

### File Organization Agent

The File Organization Agent automatically categorizes and organizes your files.

#### **How to Use**

1. **Add Files**
   ```bash
   # Copy files to process
   cp ~/Documents/*.pdf data/documents/
   cp ~/Downloads/*.txt data/documents/
   ```

2. **Enable Agent**
   - Go to Agents tab in dashboard
   - Enable "File Organization Agent"
   - Monitor processing progress

3. **View Results**
   - Check organized files in `data/documents/`
   - Review processing reports in `data/reports/`
   - View duplicates detected

#### **Features**

- **Automatic Categorization**: Files sorted by type (documents, images, videos, etc.)
- **Duplicate Detection**: SHA256-based duplicate identification
- **Smart Organization**: Intelligent folder structure creation
- **Real-time Processing**: Live progress tracking

#### **Supported File Types**

- **Documents**: PDF, DOC, DOCX, TXT, MD, CSV
- **Images**: JPG, PNG, GIF, SVG, HEIC
- **Videos**: MP4, MOV, AVI, MKV
- **Audio**: MP3, WAV, M4A, FLAC
- **Code**: PY, JS, TS, JAVA, CPP, GO
- **Archives**: ZIP, RAR, TAR, GZ

### Content Analysis Agent

The Content Analysis Agent provides deep insights into your documents.

#### **How to Use**

1. **Upload Documents**
   - Use dashboard upload interface
   - Or copy files to `data/documents/`

2. **Run Analysis**
   - Enable "Content Analysis Agent"
   - Select analysis type (sentiment, summary, key points)
   - Monitor analysis progress

3. **Review Insights**
   - View analysis results in dashboard
   - Export insights as JSON
   - Share results with team

#### **Analysis Types**

- **Sentiment Analysis**: Document emotional tone
- **Key Information Extraction**: Important facts and data
- **Document Summarization**: Concise summaries
- **Topic Classification**: Content categorization
- **Entity Recognition**: People, places, organizations

### Code Intelligence Agent

The Code Intelligence Agent analyzes and optimizes your code.

#### **How to Use**

1. **Add Code Files**
   ```bash
   cp ~/Projects/*.py data/documents/
   cp ~/Projects/*.js data/documents/
   ```

2. **Enable Code Analysis**
   - Activate "Code Intelligence Agent"
   - Select programming language
   - Choose analysis type

3. **Review Suggestions**
   - Check code quality scores
   - Review optimization suggestions
   - Apply security recommendations

#### **Analysis Features**

- **Code Quality Assessment**: Complexity, maintainability, style
- **Performance Optimization**: Speed and efficiency suggestions
- **Security Analysis**: Vulnerability detection
- **Best Practices**: Coding standards compliance
- **Documentation**: Auto-generated code comments

### Productivity Agent

The Productivity Agent optimizes your workflow and task management.

#### **How to Use**

1. **Enable Agent**
   - Activate "Productivity Agent" in dashboard
   - Configure workflow preferences
   - Set productivity goals

2. **Monitor Performance**
   - Track task completion rates
   - Analyze time usage patterns
   - Review efficiency metrics

3. **Get Recommendations**
   - Workflow optimization suggestions
   - Time management tips
   - Task prioritization advice

#### **Features**

- **Task Analysis**: Workflow pattern recognition
- **Time Tracking**: Activity monitoring
- **Efficiency Metrics**: Performance measurement
- **Automation Suggestions**: Workflow improvements

### Security Agent

The Security Agent monitors system security and file integrity.

#### **How to Use**

1. **Enable Monitoring**
   - Activate "Security Agent"
   - Configure security preferences
   - Set monitoring parameters

2. **Monitor Alerts**
   - Check security dashboard
   - Review threat detection
   - Analyze access patterns

3. **Review Reports**
   - Security assessment reports
   - Vulnerability scans
   - Integrity checks

#### **Security Features**

- **File Integrity**: SHA256 hash verification
- **Access Monitoring**: File access patterns
- **Threat Detection**: Suspicious activity identification
- **Vulnerability Scanning**: Security issue detection

### Apple Silicon Detector

The Apple Silicon Detector optimizes performance for your M3 Mac.

#### **Automatic Optimization**

- **Neural Engine**: Leverages 16-core Neural Engine
- **Unified Memory**: Optimizes 16GB unified memory usage
- **Performance Monitoring**: Real-time hardware metrics
- **Dynamic Tuning**: Automatic performance optimization

## 🧠 Model Management

### Available Models

The system supports various AI models for different tasks:

#### **General Purpose Models**
- **DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf**: Best for general tasks
- **Meta-Llama-3.1-8B-Instruct-Q6_K.gguf**: Excellent for instructions
- **Phi-4-mini-reasoning-Q8_0.gguf**: Specialized for reasoning

#### **Specialized Models**
- **TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf**: Fast responses
- **Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf**: Vision tasks

### Model Selection

#### **For File Organization**
- **Primary**: DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf
- **Fallback**: Meta-Llama-3.1-8B-Instruct-Q6_K.gguf

#### **For Content Analysis**
- **Primary**: Meta-Llama-3.1-8B-Instruct-Q6_K.gguf
- **Reasoning**: Phi-4-mini-reasoning-Q8_0.gguf

#### **For Code Intelligence**
- **Python**: Mistral-7B-Instruct-v0.1-Q4_K_M.gguf
- **JavaScript**: Phi-4-mini-reasoning-Q8_0.gguf
- **General**: DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf

### Testing Models

1. **Access Model Testing**
   - Go to Models tab in dashboard
   - Select model to test
   - Run inference test

2. **Performance Metrics**
   - Response time measurement
   - Token generation speed
   - Quality assessment

3. **Model Switching**
   - Change models per task
   - Compare performance
   - Optimize for your workflow

## 📁 File Management

### Uploading Files

#### **Via Dashboard**
1. Go to Files tab
2. Click "Upload Files"
3. Select files to upload
4. Monitor processing progress

#### **Via Command Line**
```bash
# Copy files to documents directory
cp ~/Documents/*.pdf data/documents/
cp ~/Downloads/*.txt data/documents/

# Check processing status
ls data/documents/
```

### File Organization

#### **Automatic Organization**
- Files are automatically categorized by type
- Duplicates are detected and flagged
- Smart folder structure is created

#### **Manual Organization**
- Use dashboard to move files
- Create custom categories
- Organize by project or topic

#### **Search and Filter**
- Search files by name or content
- Filter by file type or date
- Sort by size or modification time

### File Types and Categories

#### **Documents** (`data/documents/document/`)
- PDF, DOC, DOCX, TXT, MD, CSV
- Spreadsheets, presentations
- Reports and articles

#### **Images** (`data/documents/image/`)
- JPG, PNG, GIF, SVG, HEIC
- Photos, graphics, screenshots
- Icons and logos

#### **Videos** (`data/documents/video/`)
- MP4, MOV, AVI, MKV
- Recordings, presentations
- Tutorial videos

#### **Audio** (`data/documents/audio/`)
- MP3, WAV, M4A, FLAC
- Music, podcasts, recordings
- Voice memos

#### **Code** (`data/documents/code/`)
- PY, JS, TS, JAVA, CPP, GO
- Scripts, applications
- Libraries and frameworks

#### **Other** (`data/documents/other/`)
- Archives (ZIP, RAR, TAR)
- Unknown file types
- Miscellaneous files

## 📊 Monitoring and Analytics

### System Monitoring

#### **Real-time Metrics**
- **CPU Usage**: Current processor utilization
- **Memory Usage**: RAM consumption
- **Disk Usage**: Storage space
- **Network Activity**: Data transfer

#### **Apple Silicon Metrics**
- **Neural Engine**: Utilization percentage
- **Unified Memory**: Usage and efficiency
- **GPU Cores**: Graphics processing
- **Performance**: Overall system health

### Agent Performance

#### **Task Completion**
- Files processed per agent
- Processing time and efficiency
- Error rates and success rates
- Queue status and backlog

#### **Quality Metrics**
- Analysis accuracy
- Processing speed
- Resource utilization
- User satisfaction scores

### Performance Optimization

#### **Memory Management**
- Monitor unified memory usage
- Optimize model loading
- Manage cache size
- Balance performance vs. memory

#### **Processing Speed**
- Batch size optimization
- Parallel processing settings
- Model selection for speed
- Hardware utilization

## 🔗 Integrations

### GitHub Integration

#### **Setup**
1. Create GitHub personal access token
2. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your_token"
   export GITHUB_USERNAME="your_username"
   ```
3. Enable in dashboard settings

#### **Features**
- **Repository Monitoring**: Track project changes
- **Auto-commit**: Automatic code commits
- **Issue Tracking**: Bug and feature tracking
- **Collaboration**: Team workflow integration

### Google Drive Integration

#### **Setup**
1. Configure Google Drive API
2. Set up sync folders
3. Enable in dashboard settings

#### **Features**
- **File Sync**: Automatic file synchronization
- **Backup**: Cloud backup of important files
- **Collaboration**: Shared folder access
- **Version Control**: File version management

### MCP Integration

#### **Model Control Protocol**
- **Cursor Integration**: Seamless IDE integration
- **Model Management**: Direct model control
- **Code Assistance**: Real-time code help
- **Workflow Automation**: Streamlined development

## ⚙️ Configuration

### System Settings

#### **Environment Configuration**
```json
{
  "system": {
    "environment": "production",
    "debug_mode": false,
    "log_level": "INFO"
  }
}
```

#### **Performance Settings**
```json
{
  "m3_optimization": {
    "neural_engine_enabled": true,
    "parallel_processing": true,
    "unified_memory_limit": "8GB"
  }
}
```

### Agent Configuration

#### **Enable/Disable Agents**
```json
{
  "agents": {
    "file_organization": {"enabled": true},
    "content_analysis": {"enabled": true},
    "code_intelligence": {"enabled": true},
    "productivity": {"enabled": true},
    "security": {"enabled": true}
  }
}
```

#### **Model Assignment**
```json
{
  "agents": {
    "file_organization": {
      "model": "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
    },
    "content_analysis": {
      "model": "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"
    }
  }
}
```

### Customization

#### **File Organization Rules**
- Custom file type mappings
- Folder structure preferences
- Naming conventions
- Processing priorities

#### **Analysis Preferences**
- Content analysis depth
- Code review criteria
- Security scanning levels
- Performance thresholds

## 🔧 Troubleshooting

### Common Issues

#### **Dashboard Not Loading**
```bash
# Check if Streamlit is running
lsof -i :8501

# Restart dashboard
python launch_dashboard.py
```

#### **Agent Not Responding**
1. Check agent status in dashboard
2. Restart specific agent
3. Check system resources
4. Review error logs

#### **Model Connection Issues**
```bash
# Test LM Studio connection
curl http://localhost:1234/v1/models

# Check model availability
ls /Volumes/MICRO/models
```

#### **Performance Issues**
1. Reduce concurrent agents
2. Lower batch sizes
3. Use smaller models
4. Monitor memory usage

### Debug Mode

#### **Enable Debug Logging**
```json
{
  "system": {
    "debug_mode": true,
    "log_level": "DEBUG"
  }
}
```

#### **Check Logs**
```bash
# View system logs
tail -f data/logs/system.log

# View agent logs
tail -f data/logs/agents.log
```

## 📈 Best Practices

### File Organization

1. **Regular Processing**
   - Process files weekly
   - Review duplicates regularly
   - Clean up old files

2. **Naming Conventions**
   - Use descriptive file names
   - Include dates in names
   - Avoid special characters

3. **Folder Structure**
   - Organize by project
   - Use consistent naming
   - Keep structure simple

### Content Analysis

1. **Document Preparation**
   - Use clear, readable formats
   - Include relevant metadata
   - Organize by topic

2. **Analysis Strategy**
   - Start with summaries
   - Deep dive into key documents
   - Track insights over time

3. **Result Management**
   - Export important insights
   - Share with team members
   - Archive old reports

### Code Intelligence

1. **Code Quality**
   - Follow best practices
   - Use consistent formatting
   - Include documentation

2. **Security**
   - Regular security scans
   - Update dependencies
   - Review access patterns

3. **Performance**
   - Monitor execution times
   - Optimize bottlenecks
   - Profile resource usage

### System Maintenance

1. **Regular Updates**
   - Update dependencies
   - Check for new models
   - Review configuration

2. **Backup Strategy**
   - Backup important files
   - Export configurations
   - Archive reports

3. **Performance Monitoring**
   - Track system metrics
   - Optimize settings
   - Plan for growth

## 🎯 Advanced Usage

### Workflow Automation

#### **Batch Processing**
```bash
# Process multiple files
for file in ~/Documents/*.pdf; do
  cp "$file" data/documents/
done

# Monitor processing
tail -f data/logs/processing.log
```

#### **Scheduled Tasks**
```bash
# Create cron job for regular processing
0 9 * * * cd /path/to/CODE_ALCHEMY_PRO && python launch_dashboard.py
```

### Custom Integrations

#### **API Development**
- Extend system with custom APIs
- Integrate with external services
- Build custom workflows

#### **Plugin System**
- Create custom agents
- Add new file types
- Extend analysis capabilities

### Performance Tuning

#### **Apple Silicon Optimization**
- Monitor Neural Engine usage
- Optimize unified memory
- Balance performance vs. battery

#### **Model Optimization**
- Test different model combinations
- Optimize for specific tasks
- Balance speed vs. quality

## 📚 Resources

### Documentation
- **Installation Guide**: `docs/INSTALLATION_GUIDE.md`
- **API Reference**: `docs/API_REFERENCE.md`
- **Examples**: `examples/` directory

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Share tips and ask questions
- **Contributing**: Help improve the system

### Support
- **Email**: Enterprise support
- **Documentation**: Comprehensive guides
- **Examples**: Real-world usage examples

---

**Happy coding with CODE_ALCHEMY Professional! 🚀**

The system is designed to grow with your needs. Start with basic file organization and gradually explore advanced features as you become comfortable with the interface.
