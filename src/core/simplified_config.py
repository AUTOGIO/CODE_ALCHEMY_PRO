"""
CODE_ALCHEMY Professional - Simplified Configuration
Core functionality without advanced monitoring and backup features
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
class SimplifiedOptimization:
    """Simplified optimization settings"""
    basic_processing: bool = True
    memory_limit: str = "8GB"
    core_utilization: int = 4

@dataclass
class ModelConfiguration:
    """LM Studio model configuration"""
    models_path: str = "/Volumes/MICRO/models"
    server_url: str = "http://localhost:1234"
    default_model: str = "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
    fallback_model: str = "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"

@dataclass
class SimplifiedAgentConfiguration:
    """Simplified Multi-Agent System configuration"""
    file_organization: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "model": "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf",
        "batch_size": 4,
        "memory_limit": "1GB"
    })
    content_analysis: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "model": "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf",
        "multimodal": True
    })

@dataclass
class SimplifiedIntegrationConfiguration:
    """Basic service integrations"""
    github: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "token": "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",
        "username": "AUTOGIO",
        "auto_commit": True,
        "project_tracking": True
    })
    google_drive: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "sync_folders": [
            "~/Desktop/CODE_ALCHEMY_Projects",
            "~/Documents/AI_Projects",
            "~/Downloads/Code_Projects"
        ],
        "auto_backup": False
    })

@dataclass
class SimplifiedSystemConfiguration:
    """Simplified system-wide configuration settings"""
    environment: Environment = Environment.DEVELOPMENT
    debug_mode: bool = False
    log_level: str = "WARNING"
    data_dir: str = "data"
    cache_dir: str = "data/cache"
    logs_dir: str = "data/logs"

@dataclass
class SimplifiedConfig:
    """Simplified configuration class"""
    system: SimplifiedSystemConfiguration = field(default_factory=SimplifiedSystemConfiguration)
    models: ModelConfiguration = field(default_factory=ModelConfiguration)
    agents: SimplifiedAgentConfiguration = field(default_factory=SimplifiedAgentConfiguration)
    integrations: SimplifiedIntegrationConfiguration = field(default_factory=SimplifiedIntegrationConfiguration)
    optimization: SimplifiedOptimization = field(default_factory=SimplifiedOptimization)

# Global simplified configuration instance
simplified_config = SimplifiedConfig() 