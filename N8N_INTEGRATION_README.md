# 🔗 CODE_ALCHEMY Professional - N8N Integration

> **Workflow Automation Integration for CODE_ALCHEMY_PRO**

## 🚀 Overview

This integration extends CODE_ALCHEMY_PRO with powerful N8N workflow automation capabilities, enabling:

- **Real-time System Monitoring**: Automated alerts and responses
- **Agent Orchestration**: Intelligent workflow management
- **File Processing Automation**: Automated file organization workflows
- **Content Analysis Pipelines**: Streamlined document processing
- **Cross-Platform Integration**: Seamless workflow automation

## 🏗️ Architecture

```
CODE_ALCHEMY_PRO/
├── src/web/n8n_integration/     # N8N Integration Package
│   ├── __init__.py              # Package initialization
│   ├── api.py                   # FastAPI application
│   ├── security_manager.py      # API security & rate limiting
│   ├── webhook_handler.py      # Webhook processing
│   └── config.py               # Configuration management
├── data/n8n/                    # N8N Data Directory
│   ├── templates/               # Workflow templates
│   └── workflows/               # Active workflows
├── launch_n8n_integration.py   # Integration launcher
└── env.n8n.example             # Environment configuration
```

## ✨ Key Features

### **1. Secure API Layer**
- **API Key Authentication**: Secure access control
- **Rate Limiting**: 100 requests per minute per key
- **IP Whitelisting**: Restricted to trusted sources
- **CORS Support**: Cross-origin resource sharing

### **2. Webhook Management**
- **Real-time Processing**: Async webhook handling
- **Queue Management**: Background processing
- **History Tracking**: Comprehensive webhook logs
- **Error Handling**: Robust error management

### **3. Agent Integration**
- **Status Monitoring**: Real-time agent status
- **Trigger Control**: Remote agent activation
- **Parameter Passing**: Dynamic workflow configuration
- **Response Handling**: Automated response processing

### **4. System Monitoring**
- **Resource Alerts**: CPU, memory, disk monitoring
- **Performance Metrics**: Real-time system data
- **Automated Responses**: Intelligent alert handling
- **Health Checks**: System status monitoring

## 🚀 Quick Start

### **Prerequisites**

1. **Python Dependencies**
   ```bash
   pip install fastapi uvicorn python-multipart aiohttp
   ```

2. **N8N Instance** (optional for testing)
   ```bash
   npm install -g n8n
   n8n start
   ```

3. **Environment Setup**
   ```bash
   cp env.n8n.example .env
   # Edit .env with your configuration
   ```

### **Launch Integration**

1. **Start the Integration API**
   ```bash
   python launch_n8n_integration.py
   ```

2. **Access API Documentation**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

3. **Test Webhook Endpoints**
   ```bash
   # Test system alert webhook
   curl -X POST http://localhost:8000/webhook/system-alert \
     -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
     -H "Content-Type: application/json" \
     -d '{"type": "test", "message": "Integration test"}'
   ```

## 📊 API Endpoints

### **Webhook Endpoints**

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/webhook/system-alert` | POST | System alert webhook | API Key |
| `/webhook/file-organization` | POST | File organization webhook | API Key |
| `/webhook/content-analysis` | POST | Content analysis webhook | API Key |

### **Agent Control Endpoints**

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/agents/status` | GET | Get agent status | API Key |
| `/api/agents/{name}/trigger` | POST | Trigger specific agent | API Key |

### **Monitoring Endpoints**

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/monitoring/system` | GET | System metrics | API Key |
| `/api/webhooks/history` | GET | Webhook history | API Key |
| `/api/webhooks/stats` | GET | Webhook statistics | API Key |

### **Security Endpoints**

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/security/status` | GET | Security configuration | API Key |

## 🔐 Authentication

### **API Key Setup**

The integration uses Bearer token authentication with predefined API keys:

```python
# Default API Keys
API_KEYS = {
    "n8n_main": "sk_codealchemy_n8n_2025",
    "n8n_monitoring": "sk_codealchemy_monitor_2025",
    "n8n_automation": "sk_codealchemy_auto_2025"
}
```

### **Usage Example**

```bash
curl -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
     http://localhost:8000/api/agents/status
```

## 🔄 N8N Workflow Integration

### **1. System Monitoring Workflow**

**Template**: `data/n8n/templates/system_monitor_workflow.json`

**Features**:
- CPU usage alerts
- Memory threshold monitoring
- Disk space alerts
- Automated response actions

**Usage**:
1. Import workflow into N8N
2. Configure webhook endpoint
3. Set up alert thresholds
4. Deploy workflow

### **2. File Organization Workflow**

**Features**:
- File upload triggers
- Automatic categorization
- Duplicate detection
- Organization actions

### **3. Content Analysis Workflow**

**Features**:
- Document processing
- Content extraction
- Analysis automation
- Result delivery

## 📈 Performance & Monitoring

### **Rate Limiting**

- **Window**: 60 seconds
- **Limit**: 100 requests per API key
- **Response**: 429 status code when exceeded

### **Webhook Processing**

- **Timeout**: 10 seconds
- **Queue**: Async background processing
- **History**: Last 1000 webhooks stored
- **Metrics**: Success rate tracking

### **System Metrics**

- **Response Time**: < 100ms for simple operations
- **Throughput**: 100+ webhooks per minute
- **Memory Usage**: Optimized for Apple Silicon
- **CPU Usage**: Minimal overhead

## 🔧 Configuration

### **Environment Variables**

```bash
# Core Configuration
N8N_WEBHOOK_URL=http://localhost:5678
N8N_ENABLED=true

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your_secure_key

# Security
ENABLE_IP_WHITELIST=true
ALLOWED_IPS=127.0.0.1,localhost,::1

# Performance
RATE_LIMIT_WINDOW=60
RATE_LIMIT_REQUESTS=100
WEBHOOK_TIMEOUT=10
```

### **Configuration Validation**

The system automatically validates configuration on startup:

```python
if not n8n_config.validate_config():
    print("❌ Invalid configuration")
    sys.exit(1)
```

## 🧪 Testing

### **1. API Testing**

```bash
# Health check
curl http://localhost:8000/health

# Agent status (with auth)
curl -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
     http://localhost:8000/api/agents/status
```

### **2. Webhook Testing**

```bash
# Test webhook
curl -X POST http://localhost:8000/webhook/system-alert \
     -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
     -H "Content-Type: application/json" \
     -d '{"type": "test", "message": "Test alert"}'
```

### **3. N8N Integration Testing**

```bash
# Start N8N
n8n start

# Test webhook from N8N
curl -X POST http://localhost:5678/webhook/codealchemy \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
```

## 🚨 Troubleshooting

### **Common Issues**

1. **Port Already in Use**
   ```bash
   # Check port usage
   lsof -i :8000
   lsof -i :5678
   
   # Kill process if needed
   kill -9 <PID>
   ```

2. **Import Errors**
   ```bash
   # Install dependencies
   pip install fastapi uvicorn python-multipart aiohttp
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

3. **Authentication Failures**
   ```bash
   # Verify API key
   curl -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
        http://localhost:8000/health
   
   # Check configuration
   cat .env | grep API_SECRET_KEY
   ```

### **Debug Mode**

Enable debug logging:

```bash
export ENABLE_DEBUG=true
export LOG_LEVEL=DEBUG
python launch_n8n_integration.py
```

## 🔄 Integration with Existing System

### **1. Streamlit Dashboard Integration**

The N8N integration can be embedded into the existing Streamlit dashboard:

```python
# In src/web/app.py
if config.n8n.enabled:
    from src.web.n8n_integration.api import n8n_api
    
    # Add N8N status to dashboard
    st.sidebar.header("🔗 N8N Integration")
    st.sidebar.info(f"Status: Active")
    st.sidebar.info(f"API: http://localhost:8000")
```

### **2. Agent Integration**

Extend existing agents with N8N triggers:

```python
# In agent files
from src.web.n8n_integration.webhook_handler import WebhookHandler

webhook_handler = WebhookHandler()
await webhook_handler.send_system_alert(
    "agent_completed",
    f"Agent {agent_name} completed task",
    "info"
)
```

### **3. Monitoring Integration**

Integrate with existing monitoring system:

```python
# In src/core/real_monitor.py
from src.web.n8n_integration.webhook_handler import WebhookHandler

class RealSystemMonitor:
    def __init__(self):
        self.webhook_handler = WebhookHandler()
    
    def send_alert(self, alert_type, message, severity="info"):
        asyncio.create_task(
            self.webhook_handler.send_system_alert(alert_type, message, severity)
        )
```

## 🚀 Advanced Features

### **1. Custom Workflow Templates**

Create custom N8N workflows for specific use cases:

```json
{
  "name": "Custom Agent Workflow",
  "nodes": [
    {
      "id": "webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "custom-agent"
      }
    }
  ]
}
```

### **2. Dynamic Agent Configuration**

Configure agents dynamically via N8N:

```python
# Dynamic agent configuration
@self.app.post("/api/agents/{agent_name}/configure")
async def configure_agent(agent_name: str, config: Dict[str, Any]):
    # Update agent configuration
    return {"status": "configured", "agent": agent_name}
```

### **3. Workflow Orchestration**

Orchestrate complex workflows across multiple agents:

```python
# Workflow orchestration
@self.app.post("/api/workflows/orchestrate")
async def orchestrate_workflow(workflow: Dict[str, Any]):
    # Execute multi-agent workflow
    return {"status": "orchestrated", "workflow_id": workflow_id}
```

## 📚 API Documentation

### **Interactive Documentation**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### **Code Examples**

```python
import requests

# Initialize client
base_url = "http://localhost:8000"
headers = {"Authorization": "Bearer sk_codealchemy_n8n_2025"}

# Get agent status
response = requests.get(f"{base_url}/api/agents/status", headers=headers)
agents = response.json()

# Trigger agent
data = {"action": "process_files", "parameters": {"path": "/tmp"}}
response = requests.post(
    f"{base_url}/api/agents/file_organization/trigger",
    headers=headers,
    json=data
)
```

## 🔒 Security Considerations

### **1. API Key Management**

- **Rotate Keys**: Regularly update API keys
- **Scope Keys**: Use different keys for different purposes
- **Secure Storage**: Store keys in environment variables

### **2. Network Security**

- **IP Whitelisting**: Restrict access to trusted sources
- **HTTPS**: Use HTTPS in production
- **Firewall**: Configure firewall rules

### **3. Rate Limiting**

- **Monitor Usage**: Track API usage patterns
- **Adjust Limits**: Modify limits based on needs
- **Alert on Abuse**: Set up abuse detection

## 🚀 Production Deployment

### **1. Environment Setup**

```bash
# Production environment
export NODE_ENV=production
export N8N_WEBHOOK_URL=https://your-n8n-instance.com
export API_HOST=0.0.0.0
export API_PORT=8000
export API_SECRET_KEY=your_production_key
```

### **2. Process Management**

```bash
# Using systemd
sudo systemctl enable n8n-integration
sudo systemctl start n8n-integration

# Using PM2
pm2 start launch_n8n_integration.py --name "n8n-integration"
pm2 save
pm2 startup
```

### **3. Monitoring & Logging**

```bash
# Log rotation
logrotate /etc/logrotate.d/n8n-integration

# Health monitoring
curl -f http://localhost:8000/health || exit 1
```

## 🤝 Contributing

### **1. Development Setup**

```bash
# Clone repository
git clone <repository-url>
cd CODE_ALCHEMY_PRO

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/n8n_integration/

# Code formatting
black src/web/n8n_integration/
flake8 src/web/n8n_integration/
```

### **2. Testing**

```bash
# Run integration tests
python -m pytest tests/n8n_integration/ -v

# Run with coverage
python -m pytest tests/n8n_integration/ --cov=src/web/n8n_integration
```

### **3. Code Standards**

- **Type Hints**: Use type annotations
- **Docstrings**: Comprehensive documentation
- **Error Handling**: Robust error management
- **Testing**: Unit and integration tests

## 📄 License

This integration is part of CODE_ALCHEMY Professional and follows the same licensing terms.

## 🆘 Support

### **Documentation**
- **API Docs**: http://localhost:8000/docs
- **Integration Guide**: This README
- **N8N Docs**: https://docs.n8n.io/

### **Community**
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Community support and ideas
- **Email**: Enterprise support inquiries

---

**Made with ❤️ for CODE_ALCHEMY Professional users**

*For more information, visit the [CODE_ALCHEMY_PRO documentation](docs/) or [N8N documentation](https://docs.n8n.io/).*
