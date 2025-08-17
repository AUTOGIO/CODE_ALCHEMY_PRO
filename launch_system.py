#!/usr/bin/env python3
"""
SMART WORKSPACE Professional - Comprehensive Launcher
Handles setup, validation, and launch of the complete system
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional

class SmartWorkspaceLauncher:
    """Comprehensive launcher for SMART WORKSPACE Professional"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_path = self.project_root / "src" / "web" / "app.py"
        self.config_path = self.project_root / "config" / "settings.json"
        
    def print_banner(self):
        """Print system banner"""
        print("🧪 SMART WORKSPACE Professional")
        print("=" * 50)
        print("AI-Powered Workspace Intelligence System")
        print("Optimized for Apple Silicon M3")
        print("=" * 50)
        print()
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        print("🐍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            print(f"❌ Python {version.major}.{version.minor} detected")
            print("   Required: Python 3.9 or higher")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    
    def check_dependencies(self) -> bool:
        """Check if all dependencies are installed"""
        print("📦 Checking dependencies...")
        
        required_packages = [
            'streamlit', 'plotly', 'pandas', 'numpy', 
            'psutil', 'requests', 'rich', 'pyyaml'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} - Missing")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("   Run: pip install -r requirements.txt")
            return False
        
        print("✅ All dependencies found")
        return True
    
    def check_directories(self) -> bool:
        """Ensure all required directories exist"""
        print("📁 Checking directories...")
        
        required_dirs = [
            'data', 'data/documents', 'data/reports', 
            'data/cache', 'data/logs', 'config'
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ {dir_path}")
        
        return True
    
    def check_lm_studio(self) -> bool:
        """Check LM Studio connection"""
        print("🤖 Checking LM Studio connection...")
        
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get('data', [])
                print(f"✅ LM Studio connected with {len(models)} models available")
                return True
            else:
                print(f"⚠️  LM Studio responding with status {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️  LM Studio not available: {e}")
            print("   Some features may be limited")
            return False
    
    def check_models_path(self) -> bool:
        """Check if models directory exists"""
        print("🧠 Checking models path...")
        
        models_path = Path("/Volumes/MICRO/models")
        if models_path.exists():
            model_count = len(list(models_path.glob("*.gguf")))
            print(f"✅ Models found: {model_count} GGUF models")
            return True
        else:
            print("⚠️  Models path not found: /Volumes/MICRO/models")
            print("   Some AI features may be limited")
            return False
    
    def check_apple_silicon(self) -> bool:
        """Check Apple Silicon optimization"""
        print("🍎 Checking Apple Silicon...")
        
        import platform
        if platform.machine() == 'arm64' and platform.system() == 'Darwin':
            print("✅ Apple Silicon detected")
            
            # Get system info
            try:
                result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                     capture_output=True, text=True)
                if 'Apple' in result.stdout:
                    print("✅ Apple M-series chip confirmed")
                
                result = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                                     capture_output=True, text=True)
                if result.stdout:
                    memory_bytes = int(result.stdout.strip())
                    memory_gb = memory_bytes // (1024**3)
                    print(f"💾 Unified Memory: {memory_gb} GB")
                
                return True
            except Exception as e:
                print(f"⚠️  Could not get detailed system info: {e}")
                return True
        else:
            print("⚠️  Not running on Apple Silicon")
            print("   Performance may be suboptimal")
            return False
    
    def initialize_config(self) -> bool:
        """Initialize configuration if needed"""
        print("⚙️  Initializing configuration...")
        
        if not self.config_path.exists():
            try:
                from src.core.config import config
                config.save_config(str(self.config_path))
                print("✅ Configuration initialized")
            except Exception as e:
                print(f"⚠️  Could not initialize config: {e}")
                return False
        else:
            print("✅ Configuration exists")
        
        return True
    
    def test_system(self) -> bool:
        """Run basic system tests"""
        print("🧪 Running system tests...")
        
        try:
            # Test configuration loading
            from src.core.config import config
            print("✅ Configuration loaded")
            
            # Test agent initialization
            from src.agents.file_organization.agent import FileOrganizationAgent
            agent = FileOrganizationAgent()
            print("✅ File Organization Agent initialized")
            
            # Test web components
            from src.web.app import CodeAlchemyApp
            print("✅ Web application initialized")
            
            return True
        except Exception as e:
            print(f"❌ System test failed: {e}")
            return False
    
    def launch_dashboard(self) -> bool:
        """Launch the Streamlit dashboard"""
        print("🚀 Launching dashboard...")
        print("📊 Dashboard will open in your browser")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        try:
            # Change to project root
            os.chdir(self.project_root)
            
            # Launch Streamlit
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                str(self.app_path),
                "--server.port", "8501",
                "--server.address", "localhost",
                "--browser.gatherUsageStats", "false"
            ]
            
            subprocess.run(cmd)
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
            return True
        except Exception as e:
            print(f"❌ Error launching dashboard: {e}")
            return False
    
    def run(self) -> bool:
        """Run the complete launch process"""
        self.print_banner()
        
        # Run all checks
        checks = [
            ("Python Version", self.check_python_version),
            ("Dependencies", self.check_dependencies),
            ("Directories", self.check_directories),
            ("LM Studio", self.check_lm_studio),
            ("Models Path", self.check_models_path),
            ("Apple Silicon", self.check_apple_silicon),
            ("Configuration", self.initialize_config),
            ("System Test", self.test_system)
        ]
        
        failed_checks = []
        for check_name, check_func in checks:
            if not check_func():
                failed_checks.append(check_name)
        
        if failed_checks:
            print(f"\n⚠️  Some checks failed: {', '.join(failed_checks)}")
            print("   The system may not work optimally")
            print("   Consider fixing the issues above")
        
        print("\n🎯 System ready for launch!")
        print("=" * 50)
        
        return self.launch_dashboard()

def main():
    """Main entry point"""
    launcher = CodeAlchemyLauncher()
    success = launcher.run()
    
    if not success:
        print("\n❌ Launch failed")
        sys.exit(1)
    else:
        print("\n✅ Launch completed successfully")

if __name__ == "__main__":
    main()
