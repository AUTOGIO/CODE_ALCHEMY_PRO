"""
Configuration for N8N Integration
Settings and environment variables for the integration system
"""

import os
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class N8NConfig:
    """N8N integration configuration"""
    
    # N8N Instance Configuration
    n8n_webhook_url: str = field(
        default_factory=lambda: os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678")
    )
    n8n_enabled: bool = field(
        default_factory=lambda: os.getenv("N8N_ENABLED", "true").lower() == "true"
    )
    
    # API Configuration
    api_host: str = field(
        default_factory=lambda: os.getenv("API_HOST", "0.0.0.0")
    )
    api_port: int = field(
        default_factory=lambda: int(os.getenv("API_PORT", "8000"))
    )
    api_secret_key: str = field(
        default_factory=lambda: os.getenv("API_SECRET_KEY", "your_secret_key_here")
    )
    
    # Security Configuration
    enable_ip_whitelist: bool = field(
        default_factory=lambda: os.getenv("ENABLE_IP_WHITELIST", "true").lower() == "true"
    )
    allowed_ips: set = field(
        default_factory=lambda: set(os.getenv("ALLOWED_IPS", "127.0.0.1,localhost,::1").split(","))
    )
    
    # Rate Limiting
    rate_limit_window: int = field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    )
    rate_limit_requests: int = field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    )
    
    # Webhook Configuration
    webhook_timeout: int = field(
        default_factory=lambda: int(os.getenv("WEBHOOK_TIMEOUT", "10"))
    )
    max_webhook_history: int = field(
        default_factory=lambda: int(os.getenv("MAX_WEBHOOK_HISTORY", "1000"))
    )
    
    # Logging Configuration
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    enable_debug: bool = field(
        default_factory=lambda: os.getenv("ENABLE_DEBUG", "false").lower() == "true"
    )
    
    # Integration Endpoints
    integration_endpoints: Dict[str, str] = field(
        default_factory=lambda: {
            "file_organization": "/api/agents/file-organization",
            "content_analysis": "/api/agents/content-analysis",
            "system_monitor": "/api/monitoring/system",
            "code_intelligence": "/api/agents/code-intelligence",
            "productivity": "/api/agents/productivity"
        }
    )
    
    # N8N Workflow Templates
    workflow_templates: Dict[str, str] = field(
        default_factory=lambda: {
            "system_monitor": "templates/system_monitor_workflow.json",
            "file_organization": "templates/file_organization_workflow.json",
            "content_analysis": "templates/content_analysis_workflow.json",
            "agent_orchestration": "templates/agent_orchestration_workflow.json"
        }
    )
    
    def get_api_url(self, endpoint: str = "") -> str:
        """Get full API URL for an endpoint"""
        base_url = f"http://{self.api_host}:{self.api_port}"
        if endpoint:
            return f"{base_url}{endpoint}"
        return base_url
    
    def get_webhook_url(self, endpoint: str = "webhook/codealchemy") -> str:
        """Get full webhook URL for N8N"""
        return f"{self.n8n_webhook_url}/{endpoint}"
    
    def validate_config(self) -> bool:
        """Validate configuration settings"""
        try:
            # Validate port numbers
            if not (1 <= self.api_port <= 65535):
                return False
            
            # Validate rate limiting
            if self.rate_limit_window <= 0 or self.rate_limit_requests <= 0:
                return False
            
            # Validate webhook timeout
            if self.webhook_timeout <= 0:
                return False
            
            return True
            
        except Exception:
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "n8n_webhook_url": self.n8n_webhook_url,
            "n8n_enabled": self.n8n_enabled,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "enable_ip_whitelist": self.enable_ip_whitelist,
            "allowed_ips": list(self.allowed_ips),
            "rate_limit_window": self.rate_limit_window,
            "rate_limit_requests": self.rate_limit_requests,
            "webhook_timeout": self.webhook_timeout,
            "max_webhook_history": self.max_webhook_history,
            "log_level": self.log_level,
            "enable_debug": self.enable_debug
        }


# Global configuration instance
n8n_config = N8NConfig()
