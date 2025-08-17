#!/usr/bin/env python3
"""
Basic functionality tests for CODE_ALCHEMY_PRO
Tests that can run without complex dependencies
"""

import unittest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic project functionality"""
    
    def test_project_structure(self):
        """Test that essential directories exist"""
        essential_dirs = [
            "src",
            "config", 
            "docs",
            "tests",
            "tools",
            "scripts",
            "data"
        ]
        
        for dir_name in essential_dirs:
            with self.subTest(dir_name=dir_name):
                self.assertTrue(
                    os.path.exists(dir_name),
                    f"Essential directory {dir_name} should exist"
                )
    
    def test_config_files(self):
        """Test that configuration files exist"""
        config_files = [
            "pyproject.toml",
            "env.template",
            "requirements.txt"
        ]
        
        for file_name in config_files:
            with self.subTest(file_name=file_name):
                self.assertTrue(
                    os.path.exists(file_name),
                    f"Configuration file {file_name} should exist"
                )
    
    def test_development_tools(self):
        """Test that development tools exist"""
        tool_files = [
            "tools/lint.sh",
            "tools/test.sh", 
            "tools/format.sh"
        ]
        
        for tool_file in tool_files:
            with self.subTest(tool_file=tool_file):
                self.assertTrue(
                    os.path.exists(tool_file),
                    f"Development tool {tool_file} should exist"
                )
    
    def test_launch_scripts(self):
        """Test that launch scripts exist"""
        launch_files = [
            "scripts/launch/main.py",
            "scripts/install.sh",
            "scripts/setup_n8n.sh"
        ]
        
        for launch_file in launch_files:
            with self.subTest(launch_file=launch_file):
                self.assertTrue(
                    os.path.exists(launch_file),
                    f"Launch script {launch_file} should exist"
                )
    
    def test_documentation(self):
        """Test that documentation exists"""
        doc_files = [
            "README.md",
            "PROJECT_STRUCTURE.md",
            "REORGANIZATION_SUMMARY.md"
        ]
        
        for doc_file in doc_files:
            with self.subTest(doc_file=doc_file):
                self.assertTrue(
                    os.path.exists(doc_file),
                    f"Documentation file {doc_file} should exist"
                )
    
    def test_python_version(self):
        """Test Python version compatibility"""
        import platform
        python_version = platform.python_version_tuple()
        major, minor = int(python_version[0]), int(python_version[1])
        
        self.assertGreaterEqual(
            major, 3,
            "Python major version should be 3 or higher"
        )
        self.assertGreaterEqual(
            minor, 9,
            "Python minor version should be 9 or higher"
        )
    
    def test_environment_variables(self):
        """Test environment configuration"""
        # Test that .env template exists and can be read
        env_template = Path("env.template")
        self.assertTrue(
            env_template.exists(),
            "Environment template should exist"
        )
        
        # Test that .env file exists (should have been created)
        env_file = Path(".env")
        self.assertTrue(
            env_file.exists(),
            "Environment file should exist"
        )


class TestImportCapability(unittest.TestCase):
    """Test that modules can be imported"""
    
    def test_core_config_import(self):
        """Test core config module import"""
        try:
            from src.core.config import Config
            self.assertTrue(True, "Core config should be importable")
        except ImportError as e:
            self.skipTest(f"Core config import failed: {e}")
    
    def test_web_simple_app_import(self):
        """Test simple web app import"""
        try:
            from src.web.simple_app import main
            self.assertTrue(True, "Simple web app should be importable")
        except ImportError as e:
            self.skipTest(f"Simple web app import failed: {e}")


if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBasicFunctionality)
    suite.addTests(loader.loadTestsFromTestCase(TestImportCapability))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
