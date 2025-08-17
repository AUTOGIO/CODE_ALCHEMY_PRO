# 🧪 SMART WORKSPACE Professional Interactive Dashboard

A comprehensive, real-time system management dashboard for SMART WORKSPACE Professional, providing complete control over AI agents, models, integrations, and system performance.

## 🚀 Features

### 🎛️ Control Panel
- **System Controls**: Neural engine, parallel processing, dynamic caching
- **Agent Management**: Start/stop agents, priority control, batch operations
- **Model Controls**: Model switching, performance optimization, parameter tuning
- **Performance Monitoring**: Real-time metrics, resource management
- **Advanced Settings**: Debug options, experimental features

### 📊 System Monitor
- **Static Metrics**: Basic system information (no real-time updates)
- **Historical Reports**: Available through file organization reports
- **Manual Analysis**: Performance analysis through static data
- **Hardware Information**: Basic system specs (no live monitoring)

### 🤖 Agent Manager
- **Agent Overview**: Status, performance, task completion
- **Individual Controls**: Per-agent configuration and monitoring
- **Batch Operations**: Start/stop all agents, priority management
- **Performance Analytics**: Agent performance trends

### 🔗 Integration Controller
- **N8N Workflows**: File organization and content analysis automation
- **Webhook Management**: External trigger handling
- **Workflow Status**: Monitor automation execution
- **Integration Health**: Connection status and performance
- **Service Status**: GitHub, Google Drive, LM Studio, MCP
- **Connection Management**: Connect/disconnect, sync controls

### 📈 Performance Analyzer
- **Component Removed**: Real-time performance monitoring disabled
- **Static Analysis**: Available through file organization reports
- **Manual Review**: Performance data through static reports
- **No Live Updates**: System operates without continuous monitoring

### ⚙️ Settings Panel
- **System Settings**: Core system configuration
- **AI Configuration**: Model parameters, performance settings
- **Security Settings**: Encryption, access control, audit logging
- **Integration Settings**: Service configurations
- **Import/Export**: Settings backup and restore

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- macOS (optimized for M3 iMac)
- 8GB+ RAM recommended

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CODE_ALCHEMY_PRO
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the dashboard**
   ```bash
   python launch_dashboard.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - The dashboard will automatically open

## 📋 System Requirements

### Hardware
- **CPU**: Apple Silicon M1/M2/M3 (optimized)
- **Memory**: 8GB minimum, 12GB+ recommended
- **Storage**: 2GB free space for models and cache
- **Network**: Internet connection for integrations

### Software
- **OS**: macOS 12.0+ (optimized for macOS)
- **Python**: 3.8+ with pip
- **Browser**: Chrome, Safari, Firefox (modern browsers)

## 🎯 Usage Guide

### Getting Started

1. **Launch Dashboard**
   - Run `python launch_dashboard.py`
   - Wait for the browser to open automatically

2. **Navigate the Interface**
   - Use the sidebar to switch between different sections
   - Each section provides specialized controls and monitoring

3. **Monitor System Status**
   - Check the sidebar for real-time CPU and memory usage
   - Use the System Monitor for detailed performance analysis

### Key Features

#### 🎛️ Control Panel
- **System Controls**: Toggle neural engine, parallel processing
- **Quick Actions**: Restart system, backup, clear cache
- **Agent Management**: Control individual AI agents
- **Model Switching**: Switch between different AI models

#### 📊 System Monitor
- **Real-time Gauges**: Visual CPU, memory, disk usage
- **Performance Trends**: Historical data charts
- **System Alerts**: Automatic bottleneck detection
- **Hardware Info**: Detailed system specifications

#### 🤖 Agent Manager
- **Agent Status**: View all AI agents and their status
- **Performance Metrics**: Monitor agent performance
- **Batch Operations**: Start/stop all agents at once
- **Priority Management**: Set agent priorities

#### 🧠 Model Manager
- **Model Overview**: See all available models
- **Load/Unload**: Manage model memory usage
- **Performance Comparison**: Compare model speeds
- **Configuration**: Adjust model parameters

#### 🔗 Integration Controller
- **Service Status**: Monitor external service connections
- **Sync Controls**: Manage data synchronization
- **Configuration**: Set up API keys and settings
- **Connection Testing**: Test service connectivity

#### 📈 Performance Analyzer
- **Resource Analysis**: Detailed CPU and memory breakdown
- **Bottleneck Detection**: Identify performance issues
- **Trend Analysis**: Performance patterns over time
- **Optimization**: Get improvement recommendations

#### ⚙️ Settings Panel
- **System Settings**: Core system configuration
- **AI Settings**: Model and performance parameters
- **Security Settings**: Encryption and access control
- **Integration Settings**: External service configuration

## 🔧 Configuration

### Environment Variables
```bash
# Optional environment variables
export CODE_ALCHEMY_LOG_LEVEL=INFO
export CODE_ALCHEMY_CACHE_SIZE=4GB
export CODE_ALCHEMY_MAX_CONCURRENT=8
```

### Configuration Files
- **Settings**: Stored in session state (persistent across sessions)
- **Models**: Located in `/Volumes/MICRO/models` (configurable)
- **Logs**: Stored in `data/logs/` directory

## 📊 Monitoring & Alerts

### Real-time Monitoring
- **CPU Usage**: Real-time CPU utilization with alerts at 80%+
- **Memory Usage**: Memory monitoring with alerts at 85%+
- **Disk Usage**: Storage monitoring with alerts at 90%+
- **Network I/O**: Network activity monitoring

### Automated Alerts
- **Performance Bottlenecks**: Automatic detection and alerts
- **Resource Thresholds**: Configurable alert thresholds
- **Integration Status**: Service connection monitoring
- **Agent Health**: Agent performance monitoring

## 🔒 Security Features

### Access Control
- **Local Access**: Dashboard runs on localhost only
- **No External Access**: No internet exposure by default
- **Secure Connections**: HTTPS for external integrations
- **Audit Logging**: Comprehensive activity logging

### Data Protection
- **Local Storage**: All data stored locally
- **Encryption**: Optional encryption for sensitive data
- **Backup Security**: Encrypted backup options
- **Privacy**: No telemetry or data collection

## 🚀 Performance Optimization

### M3 Optimization
- **Neural Engine**: Leverages Apple's Neural Engine
- **Unified Memory**: Optimized for M3 unified memory
- **Parallel Processing**: Multi-core utilization
- **Dynamic Caching**: Intelligent cache management

### Resource Management
- **Memory Limits**: Configurable memory usage limits
- **CPU Cores**: Adjustable CPU core allocation
- **Model Loading**: Dynamic model loading/unloading
- **Cache Management**: Intelligent cache optimization

## 🔧 Troubleshooting

### Common Issues

#### Dashboard Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+

# Check port availability
lsof -i :8501
```

#### Performance Issues
- **High CPU Usage**: Check agent count and model loading
- **Memory Issues**: Reduce concurrent tasks or model count
- **Slow Response**: Check network connectivity for integrations

#### Integration Problems
- **GitHub Issues**: Verify API token and permissions
- **Drive Sync**: Check Google Drive API credentials
- **LM Studio**: Ensure LM Studio server is running

### Debug Mode
Enable debug mode in Settings Panel for detailed logging:
1. Go to Settings Panel → Advanced Settings
2. Enable "Debug mode"
3. Check logs in `data/logs/` directory

## 📈 Performance Tips

### Optimization Recommendations
1. **Memory Management**: Keep memory usage below 80%
2. **Model Loading**: Load only necessary models
3. **Agent Count**: Limit concurrent agents based on system capacity
4. **Cache Size**: Adjust cache size based on available memory
5. **Network**: Ensure stable internet for integrations

### Best Practices
- **Regular Monitoring**: Check system status regularly
- **Backup Settings**: Export settings periodically
- **Update Dependencies**: Keep packages updated
- **Resource Monitoring**: Monitor resource usage patterns

## 🔄 Updates & Maintenance

### Updating the Dashboard
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart dashboard
python launch_dashboard.py
```

### Backup & Restore
- **Settings Export**: Use Settings Panel to export configuration
- **Model Backup**: Backup models directory
- **Log Archive**: Archive logs periodically

## 📞 Support

### Getting Help
- **Documentation**: Check this README and inline help
- **Debug Mode**: Enable debug mode for detailed logs
- **System Logs**: Check `data/logs/` for error details
- **Performance Data**: Use Performance Analyzer for insights

### Reporting Issues
1. Enable debug mode
2. Reproduce the issue
3. Check system logs
4. Report with system information

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
- **Real-time Streaming**: Live data streaming

---

**🧪 CODE_ALCHEMY Professional** - AI-Powered Desktop Intelligence System

*Optimized for Apple Silicon M3 iMac - Professional Grade System Management* 