"""
CODE_ALCHEMY Professional Settings Configuration
Apple Silicon Optimized Settings
"""

from pathlib import Path
from typing import Dict, Any

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCUMENT_FOLDER = PROJECT_ROOT / "data" / "documents"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "reports"

# LM Studio API Configuration
OPENAI_API_BASE = "http://localhost:1234/v1"

# Model configurations for Apple Silicon optimization
MODELS = {
    "primary": "DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf",
    "fast": "TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf",
    "reasoning": "Phi-4-mini-reasoning-Q8_0.gguf",
    "analysis": "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"
}

MODEL_CONFIGS = {
    "primary": {
        "max_tokens": 1500,
        "temperature": 0.3,
        "timeout": 60
    },
    "fast": {
        "max_tokens": 800,
        "temperature": 0.2,
        "timeout": 30
    },
    "reasoning": {
        "max_tokens": 1200,
        "temperature": 0.1,
        "timeout": 45
    },
    "analysis": {
        "max_tokens": 2000,
        "temperature": 0.4,
        "timeout": 90
    }
}

TASK_MODEL_MAPPING = {
    "fraud_detection": "primary",
    "quick_analysis": "fast",
    "detailed_reasoning": "reasoning",
    "comprehensive_analysis": "analysis"
}

# Apple Silicon specific optimizations
APPLE_SILICON_CONFIG = {
    "neural_engine_enabled": True,
    "unified_memory_limit": "16GB",
    "parallel_processing": True,
    "dynamic_caching": True,
    "core_utilization": 8,
    "neural_engine_cores": 16,
    "neural_engine_ops_per_sec": 18_000_000_000_000
} 