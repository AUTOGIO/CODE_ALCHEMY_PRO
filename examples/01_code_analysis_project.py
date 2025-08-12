#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Example 1: Code Analysis & Optimization Project
Real-world scenario: Analyzing and optimizing a Python codebase
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.file_organization.agent import create_file_organization_agent
from src.integrations.github_integration import create_github_integration


def code_analysis_project():
    """Real code analysis and optimization workflow"""
    
    print("🔍 CODE_ALCHEMY Professional - Code Analysis Project")
    print("=" * 60)
    
    # Step 1: Initialize components
    print("\n📋 Step 1: Initializing System Components")
    file_agent = create_file_organization_agent()
    github = create_github_integration()
    
    # Step 2: Set up project structure
    print("\n📁 Step 2: Setting up Project Structure")
    project_dir = Path("examples/code_analysis_project")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample code files for analysis
    sample_files = {
        "main.py": """
import requests
import json
import time

def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_data(data):
    if not data:
        return []
    
    results = []
    for item in data:
        processed = {
            'id': item.get('id'),
            'name': item.get('name'),
            'status': item.get('status', 'unknown')
        }
        results.append(processed)
    
    return results

def main():
    url = "https://api.example.com/data"
    data = fetch_data(url)
    results = process_data(data)
    
    for result in results:
        print(f"ID: {result['id']}, Name: {result['name']}")
    
    return results

if __name__ == "__main__":
    main()
""",
        "utils.py": """
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
""",
        "tests.py": """
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [
            {'id': 1, 'name': 'Test Item 1', 'status': 'active'},
            {'id': 2, 'name': 'Test Item 2', 'status': 'inactive'}
        ]
    
    def test_process_data_valid_input(self):
        from main import process_data
        results = process_data(self.sample_data)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 1)
        self.assertEqual(results[0]['name'], 'Test Item 1')
    
    def test_process_data_empty_input(self):
        from main import process_data
        results = process_data([])
        
        self.assertEqual(results, [])
    
    @patch('main.requests.get')
    def test_fetch_data_success(self, mock_get):
        from main import fetch_data
        
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response
        
        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, self.sample_data)

if __name__ == '__main__':
    unittest.main()
"""
    }
    
    # Create sample files
    for filename, content in sample_files.items():
        file_path = project_dir / filename
        with open(file_path, 'w') as f:
            f.write(content.strip())
        print(f"✅ Created: {file_path}")
    
    # Step 3: Analyze code with AI
    print("\n🤖 Step 3: AI Code Analysis")
    
    # Simulate AI analysis (in real scenario, this would call LM Studio)
    analysis_result = {
        "model_used": "deepseek-r1-0528-qwen3-8b",
        "analysis": {
            "code_quality": {
                "score": 7.5,
                "issues": [
                    "Missing error handling in fetch_data function",
                    "No input validation in process_data",
                    "Hardcoded URL should be configurable"
                ]
            },
            "performance": {
                "score": 8.0,
                "optimizations": [
                    "Add connection pooling for requests",
                    "Implement caching for API responses",
                    "Use async/await for better performance"
                ]
            },
            "security": {
                "score": 6.5,
                "vulnerabilities": [
                    "No SSL certificate verification",
                    "No rate limiting implemented",
                    "Sensitive data logging possible"
                ]
            },
            "best_practices": {
                "score": 7.0,
                "recommendations": [
                    "Add type hints",
                    "Implement proper logging",
                    "Add docstrings",
                    "Use environment variables for configuration"
                ]
            }
        }
    }
    
    print(f"🎯 Using model: {analysis_result['model_used']}")
    print(f"📊 Code quality score: {analysis_result['analysis']['code_quality']['score']}/10")
    print(f"⚡ Performance score: {analysis_result['analysis']['performance']['score']}/10")
    print(f"🔒 Security score: {analysis_result['analysis']['security']['score']}/10")
    
    # Step 4: Generate optimized code
    print("\n⚡ Step 4: Generating Optimized Code")
    
    optimized_code = '''import asyncio
import aiohttp
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_data(self, endpoint: str) -> Optional[List[Dict]]:
        """Fetch data from API with proper error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.get(url, timeout=self.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successfully fetched {len(data)} items from {endpoint}")
                    return data
                else:
                    logger.error(f"API request failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def process_data(self, data: Optional[List[Dict]]) -> List[Dict]:
        """Process data with validation and error handling"""
        if not data:
            logger.warning("No data to process")
            return []
        
        results = []
        for item in data:
            try:
                processed = {
                    'id': item.get('id'),
                    'name': item.get('name', 'Unknown'),
                    'status': item.get('status', 'unknown'),
                    'processed_at': datetime.now().isoformat()
                }
                
                # Validate required fields
                if processed['id'] is None:
                    logger.warning(f"Skipping item without ID: {item}")
                    continue
                
                results.append(processed)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")
        
        logger.info(f"Processed {len(results)} items successfully")
        return results

async def main():
    """Main function with proper async handling"""
    config = {
        'base_url': os.getenv('API_BASE_URL', 'https://api.example.com'),
        'timeout': int(os.getenv('API_TIMEOUT', '10'))
    }
    
    async with DataProcessor(config['base_url'], config['timeout']) as processor:
        data = await processor.fetch_data('data')
        results = processor.process_data(data)
        
        for result in results:
            print(f"ID: {result['id']}, Name: {result['name']}, Status: {result['status']}")
        
        return results

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    # Save optimized code
    optimized_file = project_dir / "optimized_main.py"
    with open(optimized_file, 'w') as f:
        f.write(optimized_code.strip())
    print(f"✅ Generated optimized code: {optimized_file}")
    
    # Step 5: Create GitHub repository and commit
    print("\n🐙 Step 5: GitHub Integration")
    
    # Test GitHub connection
    github_status = github.test_connection()
    if github_status["success"]:
        print(f"✅ GitHub connected: {github_status['username']}")
        
        # Create issue for code improvements
        issue_result = github.create_issue(
            repo_name="code-alchemy-examples",
            title="Code Analysis: Performance and Security Improvements",
            body="""
## Code Analysis Results

### Issues Found:
- Missing error handling in fetch_data function
- No input validation in process_data
- Hardcoded URL should be configurable
- No SSL certificate verification
- No rate limiting implemented

### Optimizations Applied:
- Implemented async/await for better performance
- Added proper error handling and logging
- Added type hints and docstrings
- Implemented connection pooling
- Added environment variable configuration

### Files Modified:
- main.py → optimized_main.py
- Added proper logging and validation
            """,
            labels=["enhancement", "performance", "security"]
        )
        
        if issue_result["success"]:
            print(f"✅ Created GitHub issue: {issue_result['issue']['url']}")
    
    # Step 6: Generate analysis report
    print("\n📊 Step 6: Generating Analysis Report")
    
    report = {
        "project": "Code Analysis & Optimization",
        "timestamp": datetime.now().isoformat(),
        "analysis_summary": {
            "files_analyzed": 3,
            "issues_found": 8,
            "optimizations_applied": 6,
            "security_vulnerabilities": 3,
            "performance_improvements": 4
        },
        "recommendations": [
            "Implement comprehensive error handling",
            "Add input validation and sanitization",
            "Use environment variables for configuration",
            "Implement proper logging and monitoring",
            "Add unit tests for all functions",
            "Consider using async/await for I/O operations"
        ],
        "files": {
            "original": ["main.py", "utils.py", "tests.py"],
            "optimized": ["optimized_main.py"],
            "analysis": ["code_analysis_report.json"]
        }
    }
    
    # Save report
    report_file = project_dir / "code_analysis_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ Analysis report saved: {report_file}")
    
    print("\n🎉 Code Analysis Project Complete!")
    print(f"📁 Project files: {project_dir}")
    print(f"📊 Analysis report: {report_file}")
    print(f"⚡ Optimized code: {optimized_file}")


if __name__ == "__main__":
    code_analysis_project() 