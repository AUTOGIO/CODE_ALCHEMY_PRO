#!/usr/bin/env python3
"""
Safe N8N Workflow Testing Script
Tests workflows without risk to production data
"""

import json
import requests
import time
from pathlib import Path


class SafeN8NTester:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.api_key = "sk_codealchemy_n8n_2025"
        self.test_dir = "data/test_sandbox"
        self.results_dir = f"{self.test_dir}/results"
        
        # Ensure test directories exist
        Path(self.test_dir).mkdir(parents=True, exist_ok=True)
        Path(self.results_dir).mkdir(parents=True, exist_ok=True)
    
    def test_health_check(self):
        """Test basic API health without any risk"""
        print("🔍 Testing API Health Check...")
        try:
            response = requests.get(f"{self.api_base}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_system_monitoring(self):
        """Test system monitoring endpoint (read-only, safe)"""
        print("🔍 Testing System Monitoring...")
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(f"{self.api_base}/api/monitoring/system", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ System monitoring working - CPU: {data['system']['cpu_percent']}%")
                return True
            else:
                print(f"❌ System monitoring failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ System monitoring error: {e}")
            return False
    
    def test_mock_webhook(self, workflow_type, payload):
        """Test webhook endpoints with mock data (safe)"""
        print(f"🔍 Testing {workflow_type} Webhook...")
        try:
            webhook_url = f"{self.api_base}/webhook/{workflow_type}"
            response = requests.post(webhook_url, json=payload)
            print(f"✅ {workflow_type} webhook responded: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ {workflow_type} webhook error: {e}")
            return False
    
    def test_content_analysis_safe(self):
        """Test content analysis with test data only"""
        print("🔍 Testing Content Analysis (Safe Mode)...")
        
        # Create a safe test payload
        test_payload = {
            "analysis_type": "document_analysis",
            "document_folder": self.test_dir + "/documents",
            "analysis_mode": "comprehensive",
            "test_mode": True,
            "max_files": 2  # Limit to prevent overwhelming
        }
        
        return self.test_mock_webhook("content-analysis", test_payload)
    
    def test_file_organization_safe(self):
        """Test file organization with test data only"""
        print("🔍 Testing File Organization (Safe Mode)...")
        
        # Create a safe test payload
        test_payload = {
            "operation": "process_documents",
            "document_folder": self.test_dir + "/documents",
            "test_mode": True,
            "dry_run": True,  # Don't actually move files
            "max_files": 3
        }
        
        return self.test_mock_webhook("file-organization", test_payload)
    
    def test_productivity_safe(self):
        """Test productivity optimization (read-only analysis)"""
        print("🔍 Testing Productivity Analysis (Safe Mode)...")
        
        # Create a safe test payload
        test_payload = {
            "optimization_type": "pattern_analysis",
            "analysis_mode": "read_only",
            "test_mode": True,
            "scope": "test_environment"
        }
        
        return self.test_mock_webhook("productivity", test_payload)
    
    def test_system_monitor_safe(self):
        """Test system monitoring with mock alerts"""
        print("🔍 Testing System Monitor (Safe Mode)...")
        
        # Test with mock alert data
        test_alerts = [
            {"alert_type": "high_cpu", "severity": "low", "message": "Test CPU alert"},
            {"alert_type": "high_memory", "severity": "medium", "message": "Test memory alert"},
            {"alert_type": "disk_full", "severity": "high", "message": "Test disk alert"}
        ]
        
        success_count = 0
        for alert in test_alerts:
            if self.test_mock_webhook("system-alert", alert):
                success_count += 1
        
        return success_count == len(test_alerts)
    
    def run_safe_test_suite(self):
        """Run all safe tests"""
        print("🧪 N8N Safe Testing Suite")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("System Monitoring", self.test_system_monitoring),
            ("Content Analysis", self.test_content_analysis_safe),
            ("File Organization", self.test_file_organization_safe),
            ("Productivity Analysis", self.test_productivity_safe),
            ("System Monitor", self.test_system_monitor_safe)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            results[test_name] = test_func()
            time.sleep(1)  # Brief pause between tests
        
        # Save test results
        self.save_test_results(results)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! System is ready for production use.")
        else:
            print("⚠️  Some tests failed. Review before production use.")
    
    def save_test_results(self, results):
        """Save test results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.results_dir}/test_results_{timestamp}.json"
        
        test_data = {
            "timestamp": timestamp,
            "results": results,
            "test_environment": "safe_sandbox",
            "api_base": self.api_base
        }
        
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"📁 Test results saved to: {filename}")

def main():
    """Main testing function"""
    print("🚀 Starting Safe N8N Testing...")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ N8N API is not running. Please start it first with:")
            print("   python3 launch_n8n_integration.py")
            return
    except Exception:
        print("❌ Cannot connect to N8N API. Please start it first.")
        return
    
    # Run tests
    tester = SafeN8NTester()
    tester.run_safe_test_suite()

if __name__ == "__main__":
    main()
