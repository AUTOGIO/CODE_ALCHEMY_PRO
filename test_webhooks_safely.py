#!/usr/bin/env python3
"""
Safe Webhook Testing with Proper Authentication
Tests N8N webhooks using test data only
"""

import json
import requests
import time
from pathlib import Path

def test_webhook_safely(webhook_type, payload, api_key):
    """Test a webhook endpoint safely with authentication"""
    print(f"🔍 Testing {webhook_type} webhook...")
    
    try:
        # Use the proper webhook endpoint
        webhook_url = f"http://localhost:8000/webhook/{webhook_type}"
        
        # Add authentication header
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Test-Mode": "true"  # Signal this is a test
        }
        
        # Send test request
        response = requests.post(
            webhook_url, 
            json=payload, 
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print(f"   ✅ {webhook_type} webhook working")
            return True
        else:
            print(f"   ⚠️  {webhook_type} webhook responded with {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing {webhook_type}: {e}")
        return False

def main():
    """Test all webhooks safely"""
    print("🛡️  Safe Webhook Testing with Authentication")
    print("=" * 50)
    
    # API key for testing
    api_key = "sk_codealchemy_n8n_2025"
    
    # Test payloads (safe, test data only)
    test_payloads = {
        "content-analysis": {
            "analysis_type": "document_analysis",
            "document_folder": "data/test_sandbox/documents",
            "test_mode": True,
            "max_files": 1,
            "dry_run": True
        },
        "file-organization": {
            "operation": "process_documents",
            "document_folder": "data/test_sandbox/documents",
            "test_mode": True,
            "dry_run": True,
            "max_files": 1
        },
        "productivity": {
            "optimization_type": "pattern_analysis",
            "analysis_mode": "read_only",
            "test_mode": True,
            "scope": "test_environment"
        },
        "system-alert": {
            "alert_type": "test_alert",
            "severity": "low",
            "message": "This is a safe test alert",
            "test_mode": True,
            "mock_data": True
        }
    }
    
    # Test each webhook
    results = {}
    for webhook_type, payload in test_payloads.items():
        print(f"\n📋 Testing: {webhook_type}")
        results[webhook_type] = test_webhook_safely(webhook_type, payload, api_key)
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Webhook Test Results")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for webhook_type, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{webhook_type}: {status}")
    
    print(f"\nOverall: {passed}/{total} webhooks working")
    
    if passed == total:
        print("🎉 All webhooks are working safely!")
    else:
        print("⚠️  Some webhooks need attention before production use.")

if __name__ == "__main__":
    main()
