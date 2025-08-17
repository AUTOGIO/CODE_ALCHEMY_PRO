"""
CODE_ALCHEMY Professional Core Configuration
M3-Optimized Configuration Management System
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class M3Optimization:
    """M3-specific optimization settings"""
    neural_engine_enabled: bool = True
    unified_memory_limit: str = "8GB"
    parallel_processing: bool = True
    dynamic_caching: bool = True
    core_utilization: int = 4

@dataclass
class ModelConfiguration:
    """LM Studio model configuration"""
    models_path: str = "/Volumes/MICRO/models"
    server_url: str = "http://localhost:1234"
    default_model: str = "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
    fallback_model: str = "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"
    reasoning_model: str = "Phi-4-mini-reasoning-Q8_0.gguf"
    fast_model: str = "TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf"
    vision_model: str = "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"

@dataclass
class AgentConfiguration:
    """Multi-Agent System configuration"""
    file_organization: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "model": "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf",
        "batch_size": 8,
        "memory_limit": "2GB"
    })
    content_analysis: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "model": "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf",
        "multimodal": True
    })
    # code_intelligence: Dict[str, Any] = field(default_factory=lambda: {  # Code Intelligence Agent removed
    #     "enabled": True,
    #     "model": "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    #     "specialized_models": {
    #         "python": "Mistral-7B-Instruct-v0.1-Q4_K_M.gguf",
    #             "javascript": "Phi-4-mini-reasoning-Q8_0.gguf"
    #         }
    # })
    productivity: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "model": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "real_time_analysis": False  # Disabled - no live monitoring
    })
    # security: Dict[str, Any] = field(default_factory=lambda: {  # Security Agent removed
    #     "enabled": True,
    #     "model": "TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf",
    #     "continuous_monitoring": False  # Disabled - no live monitoring
    # })

@dataclass
class IntegrationConfiguration:
    """External service integrations"""
    github: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": False,
        "token": os.getenv("GITHUB_TOKEN", ""),
        "username": os.getenv("GITHUB_USERNAME", ""),
        "auto_commit": False,
        "project_tracking": False
    })
    google_drive: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": False,
        "sync_folders": [
            "~/Desktop/CODE_ALCHEMY_Projects",
            "~/Documents/AI_Projects",
            "~/Downloads/Code_Projects"
        ],
        "auto_backup": False
    })
    mcp: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "servers": {
            "lm-studio-bridge": {
                "command": "python",
                "args": ["src/mcp/lm_studio_bridge.py"],
                "env": {"LM_STUDIO_URL": "http://localhost:1234"}
            },
            "model-manager": {
                "command": "python",
                "args": ["src/mcp/model_manager.py"],
                "env": {"MODELS_PATH": "/Volumes/MICRO/models"}
            },
            "code-assistant": {
                "command": "python",
                "args": ["src/mcp/code_assistant.py"],
                "env": {"CODE_MODELS": "Phi-4-mini-reasoning-GGUF,DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"}
            }
        }
    })

@dataclass
class SystemConfiguration:
    """System-wide configuration settings"""
    environment: Environment = Environment.PRODUCTION
    debug_mode: bool = False
    log_level: str = "INFO"
    data_dir: str = "data"
    cache_dir: str = "data/cache"
    logs_dir: str = "data/logs"
    models_dir: str = "data/models"
    reports_dir: str = "data/reports"
    documents_dir: str = "data/documents"

@dataclass
class Config:
    """Main configuration class"""
    system: SystemConfiguration = field(default_factory=SystemConfiguration)
    models: ModelConfiguration = field(default_factory=ModelConfiguration)
    agents: AgentConfiguration = field(default_factory=AgentConfiguration)
    integrations: IntegrationConfiguration = field(default_factory=IntegrationConfiguration)
    m3_optimization: M3Optimization = field(default_factory=M3Optimization)
    
    def __post_init__(self):
        """Ensure directories exist"""
        for dir_path in [self.system.data_dir, self.system.cache_dir, 
                        self.system.logs_dir, self.system.reports_dir, 
                        self.system.documents_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "system": {
                "environment": self.system.environment.value,
                "debug_mode": self.system.debug_mode,
                "log_level": self.system.log_level,
                "data_dir": self.system.data_dir,
                "cache_dir": self.system.cache_dir,
                "logs_dir": self.system.logs_dir,
                "models_dir": self.system.models_dir,
                "reports_dir": self.system.reports_dir,
                "documents_dir": self.system.documents_dir
            },
            "models": {
                "models_path": self.models.models_path,
                "server_url": self.models.server_url,
                "default_model": self.models.default_model,
                "fallback_model": self.models.fallback_model,
                "reasoning_model": self.models.reasoning_model,
                "fast_model": self.models.fast_model,
                "vision_model": self.models.vision_model
            },
            "agents": {
                "file_organization": self.agents.file_organization,
                "content_analysis": self.agents.content_analysis,
                "code_intelligence": self.agents.code_intelligence,
                "productivity": self.agents.productivity,
                "security": self.agents.security
            },
            "integrations": {
                "github": self.integrations.github,
                "google_drive": self.integrations.google_drive,
                "mcp": self.integrations.mcp
            },
            "m3_optimization": {
                "neural_engine_enabled": self.m3_optimization.neural_engine_enabled,
                "unified_memory_limit": self.m3_optimization.unified_memory_limit,
                "parallel_processing": self.m3_optimization.parallel_processing,
                "dynamic_caching": self.m3_optimization.dynamic_caching,
                "core_utilization": self.m3_optimization.core_utilization
            }
        }
    
    def save_config(self, file_path: str = "config/settings.json"):
        """Save configuration to file"""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_config(cls, file_path: str = "config/settings.json") -> 'Config':
        """Load configuration from file"""
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                return cls._from_dict(data)
        return cls()
    
    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create config from dictionary"""
        config = cls()
        
        if "system" in data:
            system_data = data["system"]
            config.system.environment = Environment(system_data.get("environment", "production"))
            config.system.debug_mode = system_data.get("debug_mode", False)
            config.system.log_level = system_data.get("log_level", "INFO")
            config.system.data_dir = system_data.get("data_dir", "data")
            config.system.cache_dir = system_data.get("cache_dir", "data/cache")
            config.system.logs_dir = system_data.get("logs_dir", "data/logs")
            config.system.models_dir = system_data.get("models_dir", "data/models")
            config.system.reports_dir = system_data.get("reports_dir", "data/reports")
            config.system.documents_dir = system_data.get("documents_dir", "data/documents")
        
        if "models" in data:
            models_data = data["models"]
            config.models.models_path = models_data.get("models_path", "/Volumes/MICRO/models")
            config.models.server_url = models_data.get("server_url", "http://localhost:1234")
            config.models.default_model = models_data.get("default_model", "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf")
            config.models.fallback_model = models_data.get("fallback_model", "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf")
            config.models.reasoning_model = models_data.get("reasoning_model", "Phi-4-mini-reasoning-Q8_0.gguf")
            config.models.fast_model = models_data.get("fast_model", "TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf")
            config.models.vision_model = models_data.get("vision_model", "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf")
        
        if "agents" in data:
            agents_data = data["agents"]
            config.agents.file_organization = agents_data.get("file_organization", config.agents.file_organization)
            config.agents.content_analysis = agents_data.get("content_analysis", config.agents.content_analysis)
            config.agents.code_intelligence = agents_data.get("code_intelligence", config.agents.code_intelligence)
            config.agents.productivity = agents_data.get("productivity", config.agents.productivity)
            config.agents.security = agents_data.get("security", config.agents.security)
        
        if "integrations" in data:
            integrations_data = data["integrations"]
            config.integrations.github = integrations_data.get("github", config.integrations.github)
            config.integrations.google_drive = integrations_data.get("google_drive", config.integrations.google_drive)
            config.integrations.mcp = integrations_data.get("mcp", config.integrations.mcp)
        
        if "m3_optimization" in data:
            m3_data = data["m3_optimization"]
            config.m3_optimization.neural_engine_enabled = m3_data.get("neural_engine_enabled", True)
            config.m3_optimization.unified_memory_limit = m3_data.get("unified_memory_limit", "8GB")
            config.m3_optimization.parallel_processing = m3_data.get("parallel_processing", True)
            config.m3_optimization.dynamic_caching = m3_data.get("dynamic_caching", True)
            config.m3_optimization.core_utilization = m3_data.get("core_utilization", 4)
        
        return config

# Global configuration instance
config = Config.load_config()