#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - N8N Integration Launcher
Launch the N8N integration API server
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('data/logs/n8n_integration.log')
        ]
    )

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import aiohttp
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install fastapi uvicorn aiohttp")
        return False

def check_ports():
    """Check if required ports are available"""
    import socket
    
    ports_to_check = [8000, 5678]  # API port and N8N default port
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  Port {port} is already in use")
        else:
            print(f"✅ Port {port} is available")
    
    return True

def create_directories():
    """Create necessary directories"""
    dirs = [
        'data/logs',
        'data/n8n',
        'data/n8n/templates',
        'data/n8n/workflows'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path} ready")

def main():
    """Main launcher function"""
    print("🔗 CODE_ALCHEMY Professional - N8N Integration")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check ports
    print("🔌 Checking port availability...")
    check_ports()
    
    # Create directories
    print("📁 Creating directories...")
    create_directories()
    
    # Import and launch API
    print("🚀 Launching N8N Integration API...")
    try:
        from src.web.n8n_integration.api import n8n_api
        from src.web.n8n_integration.config import n8n_config
        
        # Validate configuration
        if not n8n_config.validate_config():
            print("❌ Invalid configuration")
            sys.exit(1)
        
        print(f"📊 API will be available at: http://{n8n_config.api_host}:{n8n_config.api_port}")
        print(f"🔗 N8N webhook URL: {n8n_config.get_webhook_url()}")
        print(f"📚 API Documentation: http://{n8n_config.api_host}:{n8n_config.api_port}/docs")
        print("-" * 50)
        
        # Launch the API
        n8n_api.run(
            host=n8n_config.api_host,
            port=n8n_config.api_port
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
