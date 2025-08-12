#!/usr/bin/env python3
"""
Phase 2 Integration Test - Agent Integration
Test the real agent integration with N8N system
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

async def test_agent_manager():
    """Test the agent manager functionality"""
    print("🔧 Testing Agent Manager...")
    try:
        from src.agents.agent_manager import agent_manager
        
        # Test agent initialization
        print(f"  ✅ Agent Manager initialized with {len(agent_manager.agents)} agents")
        
        # Test agent status
        status = agent_manager.get_agent_status()
        if status.get('success'):
            print("  ✅ Agent status retrieval working")
            print(f"     Total agents: {status.get('total_agents', 0)}")
            print(f"     Active agents: {status.get('active_agents', 0)}")
        else:
            print(f"  ❌ Agent status failed: {status.get('error')}")
            return False
        
        # Test agent capabilities
        capabilities = agent_manager.get_agent_capabilities()
        if capabilities.get('success'):
            print("  ✅ Agent capabilities retrieval working")
        else:
            print(f"  ❌ Agent capabilities failed: {capabilities.get('error')}")
            return False
        
        # Test agent summary
        summary = agent_manager.get_agent_summary()
        if 'total_agents' in summary:
            print("  ✅ Agent summary working")
        else:
            print("  ❌ Agent summary failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent Manager test failed: {e}")
        return False

async def test_agent_execution():
    """Test agent execution functionality"""
    print("🚀 Testing Agent Execution...")
    try:
        from src.agents.agent_manager import agent_manager
        
        # Test file organization agent
        print("  📁 Testing File Organization Agent...")
        
        # Execute with test operation
        result = await agent_manager.execute_agent('file_organization', {
            'operation': 'add_test_files'
        })
        
        if result.get('success'):
            print("  ✅ File Organization Agent executed successfully")
            print(f"     Files created: {result.get('files_created', 0)}")
        else:
            print(f"  ❌ File Organization Agent failed: {result.get('error')}")
            return False
        
        # Test agent status after execution
        status = agent_manager.get_agent_status('file_organization')
        if status.get('success'):
            agent_status = status.get('agent', {})
            print(f"  ✅ Agent status updated: {agent_status.get('status')}")
        else:
            print("  ❌ Agent status update failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent execution test failed: {e}")
        return False

async def test_agent_management():
    """Test agent management operations"""
    print("⚙️ Testing Agent Management...")
    try:
        from src.agents.agent_manager import agent_manager
        
        # Test agent disable/enable
        print("  🔄 Testing agent disable/enable...")
        
        # Disable agent
        disable_result = agent_manager.disable_agent('file_organization')
        if disable_result.get('success'):
            print("  ✅ Agent disabled successfully")
        else:
            print(f"  ❌ Agent disable failed: {disable_result.get('error')}")
            return False
        
        # Check status
        status = agent_manager.get_agent_status('file_organization')
        if status.get('success'):
            agent_status = status.get('agent', {})
            if not agent_status.get('enabled'):
                print("  ✅ Agent status shows disabled")
            else:
                print("  ❌ Agent still shows enabled")
                return False
        
        # Re-enable agent
        enable_result = agent_manager.enable_agent('file_organization')
        if enable_result.get('success'):
            print("  ✅ Agent re-enabled successfully")
        else:
            print(f"  ❌ Agent re-enable failed: {enable_result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent management test failed: {e}")
        return False

async def test_workflow_triggers():
    """Test workflow trigger functionality"""
    print("🔗 Testing Workflow Triggers...")
    try:
        from src.agents.agent_manager import agent_manager
        
        # Test getting workflow triggers
        capabilities = agent_manager.get_agent_capabilities('file_organization')
        if capabilities.get('success'):
            triggers = capabilities.get('capabilities', {}).get('workflow_triggers', [])
            print(f"  ✅ Found {len(triggers)} workflow triggers")
            
            for trigger in triggers:
                print(f"     - {trigger.get('name')}: {trigger.get('config', {}).get('type')}")
        else:
            print(f"  ❌ Workflow triggers failed: {capabilities.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Workflow triggers test failed: {e}")
        return False

async def test_n8n_api_integration():
    """Test N8N API integration with real agents"""
    print("🌐 Testing N8N API Integration...")
    try:
        from src.web.n8n_integration.api import N8NIntegrationAPI
        
        # Create API instance
        api = N8NIntegrationAPI()
        print("  ✅ N8N API created successfully")
        
        # Test agent status endpoint
        from src.agents.agent_manager import agent_manager
        
        # Simulate API call
        agents_status = agent_manager.get_agent_status()
        if agents_status.get('success'):
            print("  ✅ Agent status endpoint working")
        else:
            print("  ❌ Agent status endpoint failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ N8N API integration test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Phase 2 Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_agent_manager,
        test_agent_execution,
        test_agent_management,
        test_workflow_triggers,
        test_n8n_api_integration
    ]
    
    results = []
    
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("📊 Phase 2 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        test_name = test.__name__.replace('test_', '').replace('_', ' ').title()
        print(f"{i+1:2d}. {test_name:25s} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 2 tests passed! Agent integration is ready.")
        print("\n🚀 Ready for Phase 3: N8N Workflows")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
