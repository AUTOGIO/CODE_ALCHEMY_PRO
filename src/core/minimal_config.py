"""
CODE_ALCHEMY Professional - Minimal Configuration
Only essential features for maximum performance
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class MinimalConfig:
    """Minimal configuration for core functionality"""
    
    # System settings
    debug_mode: bool = False
    log_level: str = "ERROR"
    
    # Data directories
    data_dir: str = "data"
    documents_dir: str = "data/documents"
    reports_dir: str = "data/reports"
    
    # Model settings
    server_url: str = "http://localhost:1234"
    default_model: str = "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf"
    
    # Agent settings
    file_organization_enabled: bool = True
    content_analysis_enabled: bool = True
    
    # Integration settings
    github_enabled: bool = True
    google_drive_enabled: bool = True
    
    def __post_init__(self):
        """Ensure directories exist"""
        for dir_path in [self.data_dir, self.documents_dir, self.reports_dir]:
            Path(dir_path).mkdir(exist_ok=True)

# Global minimal configuration
minimal_config = MinimalConfig() 