#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Phase 3: N8N Workflows Test Suite
Tests N8N workflow integration, webhook functionality, and end-to-end automation
"""

import asyncio
import json
import time
import requests
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

class Phase3WorkflowTester:
    """Test suite for Phase 3: N8N Workflows"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
        self.n8n_url = "http://localhost:5678"
        self.api_key = "sk_codealchemy_n8n_2025"
        self.test_results = []
        
        # Test data
        self.test_webhooks = {
            "file_organization": {
                "url": f"{self.api_base_url}/webhook/file-organization",
                "data": {"operation": "process_documents", "test": True}
            },
            "content_analysis": {
                "url": f"{self.api_base_url}/webhook/content-analysis",
                "data": {"analysis_type": "document_analysis", "test": True}
            },
            "productivity": {
                "url": f"{self.api_base_url}/webhook/productivity",
                "data": {"optimization_type": "workflow_optimization", "test": True}
            },
            "system_alert": {
                "url": f"{self.api_base_url}/webhook/system-alert",
                "data": {"type": "test_alert", "message": "Phase 3 integration test"}
            }
        }
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n🔧 {title}")
        print("-" * 40)
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result with formatting"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
        if details:
            print(f"     {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def check_service_running(self, service_name: str, url: str) -> bool:
        """Check if a service is running and accessible"""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def test_n8n_installation(self) -> bool:
        """Test if N8N is properly installed and accessible"""
        self.print_section("Testing N8N Installation")
        
        # Check if N8N process is running
        try:
            result = subprocess.run(['pgrep', '-f', 'n8n'], 
                                 capture_output=True, text=True)
            n8n_running = result.returncode == 0
            self.print_result("N8N Process Running", n8n_running)
            
            if n8n_running:
                pid = result.stdout.strip()
                self.print_result("N8N Process ID", True, f"PID: {pid}")
        except Exception as e:
            self.print_result("N8N Process Check", False, f"Error: {e}")
            n8n_running = False
        
        # Check if N8N web interface is accessible
        n8n_accessible = self.check_service_running("N8N", self.n8n_url)
        self.print_result("N8N Web Interface", n8n_accessible, 
                         f"URL: {self.n8n_url}")
        
        # Check N8N configuration
        n8n_config_dir = Path.home() / ".n8n"
        config_exists = n8n_config_dir.exists()
        self.print_result("N8N Config Directory", config_exists, 
                         f"Path: {n8n_config_dir}")
        
        if config_exists:
            env_file = n8n_config_dir / ".env"
            env_exists = env_file.exists()
            self.print_result("N8N Environment File", env_exists, 
                             f"File: {env_file}")
        
        return n8n_running and n8n_accessible
    
    def test_workflow_templates(self) -> bool:
        """Test if workflow templates are properly created and accessible"""
        self.print_section("Testing Workflow Templates")
        
        templates_dir = Path("data/n8n/templates")
        templates_exist = templates_dir.exists()
        self.print_result("Templates Directory", templates_exist, 
                         f"Path: {templates_dir}")
        
        if not templates_exist:
            return False
        
        # Check for specific workflow templates
        expected_templates = [
            "file_organization_workflow.json",
            "content_analysis_workflow.json", 
            "productivity_workflow.json",
            "system_monitor_workflow.json"
        ]
        
        all_templates_found = True
        for template in expected_templates:
            template_path = templates_dir / template
            exists = template_path.exists()
            self.print_result(f"Template: {template}", exists)
            if not exists:
                all_templates_found = False
        
        # Validate JSON format of templates
        if all_templates_found:
            for template in expected_templates:
                template_path = templates_dir / template
                try:
                    with open(template_path, 'r') as f:
                        json.load(f)
                    self.print_result(f"JSON Valid: {template}", True)
                except json.JSONDecodeError as e:
                    self.print_result(f"JSON Valid: {template}", False, f"Error: {e}")
                    all_templates_found = False
        
        return all_templates_found
    
    def test_webhook_endpoints(self) -> bool:
        """Test if webhook endpoints are working correctly"""
        self.print_section("Testing Webhook Endpoints")
        
        # Check if API is running
        api_running = self.check_service_running("CODE_ALCHEMY API", 
                                               f"{self.api_base_url}/health")
        self.print_result("API Service Running", api_running)
        
        if not api_running:
            return False
        
        # Test each webhook endpoint
        all_webhooks_working = True
        
        for webhook_name, webhook_config in self.test_webhooks.items():
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                response = requests.post(
                    webhook_config["url"],
                    json=webhook_config["data"],
                    headers=headers,
                    timeout=10
                )
                
                success = response.status_code == 200
                self.print_result(f"Webhook: {webhook_name}", success, 
                                 f"Status: {response.status_code}")
                
                if success:
                    try:
                        response_data = response.json()
                        if "success" in response_data:
                            self.print_result(f"Response Format: {webhook_name}", True)
                        else:
                            self.print_result(f"Response Format: {webhook_name}", False, 
                                             "Missing 'success' field")
                            all_webhooks_working = False
                    except json.JSONDecodeError:
                        self.print_result(f"Response Format: {webhook_name}", False, 
                                         "Invalid JSON response")
                        all_webhooks_working = False
                else:
                    all_webhooks_working = False
                    
            except Exception as e:
                self.print_result(f"Webhook: {webhook_name}", False, f"Error: {e}")
                all_webhooks_working = False
        
        return all_webhooks_working
    
    def test_agent_integration(self) -> bool:
        """Test if agents can be triggered through the API"""
        self.print_section("Testing Agent Integration")
        
        # Test file organization agent
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Test agent status
            response = requests.get(
                f"{self.api_base_url}/api/agents/status",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                status_data = response.json()
                agents_count = len(status_data.get("agents", {}))
                self.print_result("Agent Status Endpoint", True, 
                                 f"Found {agents_count} agents")
            else:
                self.print_result("Agent Status Endpoint", False, 
                                 f"Status: {response.status_code}")
                return False
            
            # Test agent trigger
            trigger_data = {"operation": "process_documents"}
            response = requests.post(
                f"{self.api_base_url}/api/agents/file_organization/trigger",
                json=trigger_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                trigger_result = response.json()
                success = trigger_result.get("success", False)
                self.print_result("Agent Trigger", success, 
                                 f"Operation: {trigger_data['operation']}")
                return success
            else:
                self.print_result("Agent Trigger", False, 
                                 f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("Agent Integration", False, f"Error: {e}")
            return False
    
    def test_n8n_workflow_import(self) -> bool:
        """Test if N8N can import workflow templates"""
        self.print_section("Testing N8N Workflow Import")
        
        # Check if N8N API is accessible
        try:
            response = requests.get(f"{self.n8n_url}/api/v1/health", timeout=5)
            n8n_api_accessible = response.status_code == 200
            self.print_result("N8N API Accessible", n8n_api_accessible)
        except:
            n8n_api_accessible = False
            self.print_result("N8N API Accessible", False)
        
        if not n8n_api_accessible:
            return False
        
        # Test workflow import via API
        templates_dir = Path("data/n8n/templates")
        if templates_dir.exists():
            # Try to import a simple workflow
            try:
                with open(templates_dir / "system_monitor_workflow.json", 'r') as f:
                    workflow_data = json.load(f)
                
                # Remove webhookId to avoid conflicts
                if "webhookId" in workflow_data:
                    del workflow_data["webhookId"]
                
                response = requests.post(
                    f"{self.n8n_url}/api/v1/workflows/import",
                    json=workflow_data,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    self.print_result("Workflow Import via API", True)
                    return True
                else:
                    self.print_result("Workflow Import via API", False, 
                                     f"Status: {response.status_code}")
                    return False
                    
            except Exception as e:
                self.print_result("Workflow Import via API", False, f"Error: {e}")
                return False
        
        return False
    
    def test_end_to_end_workflow(self) -> bool:
        """Test end-to-end workflow execution"""
        self.print_section("Testing End-to-End Workflow")
        
        # This is a simplified test that simulates a workflow execution
        try:
            # Simulate webhook trigger
            webhook_data = {
                "operation": "process_documents",
                "document_folder": "data/documents",
                "test_mode": True
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Trigger the workflow
            response = requests.post(
                f"{self.api_base_url}/webhook/file-organization",
                json=webhook_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                success = result.get("success", False)
                
                if success:
                    self.print_result("End-to-End Workflow", True, 
                                     "Workflow executed successfully")
                    
                    # Check if results were generated
                    if "files_processed" in result:
                        files_count = result["files_processed"]
                        self.print_result("Workflow Results", True, 
                                         f"Processed {files_count} files")
                    else:
                        self.print_result("Workflow Results", False, 
                                         "No results data")
                        success = False
                    
                    return success
                else:
                    self.print_result("End-to-End Workflow", False, 
                                     f"Workflow failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                self.print_result("End-to-End Workflow", False, 
                                 f"HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_result("End-to-End Workflow", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Phase 3 tests"""
        self.print_header("Phase 3: N8N Workflows Test Suite")
        
        print("🚀 Testing N8N workflow integration and automation...")
        
        # Run all test categories
        test_categories = [
            ("N8N Installation", self.test_n8n_installation),
            ("Workflow Templates", self.test_workflow_templates),
            ("Webhook Endpoints", self.test_webhook_endpoints),
            ("Agent Integration", self.test_agent_integration),
            ("N8N Workflow Import", self.test_n8n_workflow_import),
            ("End-to-End Workflow", self.test_end_to_end_workflow)
        ]
        
        results = {}
        for test_name, test_func in test_categories:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"  ❌ {test_name} test failed with exception: {e}")
                results[test_name] = False
        
        # Print summary
        self.print_header("Phase 3 Test Results Summary")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print(f"\n📊 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All Phase 3 tests passed! N8N integration is ready.")
            print("\n🚀 Ready for Phase 4: Advanced Features")
        else:
            print("⚠️  Some tests failed. Please check the errors above.")
        
        return passed == total

def main():
    """Main test execution"""
    tester = Phase3WorkflowTester()
    
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
