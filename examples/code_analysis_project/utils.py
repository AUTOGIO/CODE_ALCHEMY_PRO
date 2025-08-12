import os
import sys
from pathlib import Path

def read_config():
    config_path = Path("config.json")
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Config error: {e}")
        return {}

def validate_input(data):
    if not isinstance(data, dict):
        return False
    
    required_fields = ['id', 'name']
    return all(field in data for field in required_fields)

def log_message(message, level="INFO"):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {level}: {message}")