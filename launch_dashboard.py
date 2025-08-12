#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional Interactive Dashboard Launcher
Launch the comprehensive system management dashboard
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the interactive dashboard"""
    print("🧪 CODE_ALCHEMY Professional Dashboard")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path(__file__).parent
    app_path = project_root / "src" / "web" / "app.py"
    
    if not app_path.exists():
        print("❌ Error: Could not find app.py")
        print(f"Expected path: {app_path}")
        sys.exit(1)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        import psutil
        import requests
        print("✅ All dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check LM Studio connection
    print("🤖 Checking LM Studio connection...")
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"✅ LM Studio connected with {len(models)} models available")
        else:
            print("⚠️  LM Studio not responding properly")
    except Exception as e:
        print(f"⚠️  LM Studio not available: {e}")
        print("   Some features may be limited")
    
    # Initialize real monitoring
    print("📊 Initializing real monitoring system...")
    try:
        from src.core.real_monitor import real_monitor
        print("✅ Real monitoring system initialized")
    except Exception as e:
        print(f"⚠️  Real monitoring not available: {e}")
    
    # Check data directories
    print("📁 Checking data directories...")
    data_dirs = ['data/documents', 'data/reports', 'data/cache', 'data/logs']
    for dir_path in data_dirs:
        Path(dir_path).mkdir(exist_ok=True)
        print(f"✅ {dir_path} ready")
    
    # Launch the dashboard
    print("🚀 Launching interactive dashboard...")
    print("📊 Dashboard will open in your browser")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to project root directory
        os.chdir(project_root)
        
        # Launch Streamlit app
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 