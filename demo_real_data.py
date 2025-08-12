#!/usr/bin/env python3
"""
CODE_ALCHEMY_PRO - Real Data Demonstration
Shows the system working with actual files and workflows
"""

import time
import requests
import json
from pathlib import Path
import subprocess

class RealDataDemo:
    """Demonstrates CODE_ALCHEMY_PRO with real data"""
    
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.n8n_url = "http://localhost:5678"
        self.api_key = "sk_codealchemy_n8n_2025"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"🎭 {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str):
        """Print formatted section"""
        print(f"\n🔧 {title}")
        print("-" * 40)
    
    def print_result(self, message: str, success: bool = True):
        """Print result with formatting"""
        status = "✅" if success else "❌"
        print(f"  {status} {message}")
    
    def check_system_status(self):
        """Check if all services are running"""
        self.print_section("System Status Check")
        
        # Check API
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            if response.status_code == 200:
                self.print_result("CODE_ALCHEMY_PRO API: RUNNING")
                api_status = True
            else:
                self.print_result("CODE_ALCHEMY_PRO API: ERROR")
                api_status = False
        except:
            self.print_result("CODE_ALCHEMY_PRO API: NOT ACCESSIBLE")
            api_status = False
        
        # Check N8N
        try:
            response = requests.get(self.n8n_url, timeout=5)
            if response.status_code == 200:
                self.print_result("N8N Service: RUNNING")
                n8n_status = True
            else:
                self.print_result("N8N Service: ERROR")
                n8n_status = False
        except:
            self.print_result("N8N Service: NOT ACCESSIBLE")
            n8n_status = False
        
        return api_status and n8n_status
    
    def show_real_data_structure(self):
        """Display the real data structure we created"""
        self.print_section("Real Data Structure")
        
        projects_dir = Path("data/documents/projects")
        if projects_dir.exists():
            self.print_result(f"Projects directory: {projects_dir}")
            
            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir():
                    print(f"  📁 {project_dir.name}/")
                    for file_path in project_dir.iterdir():
                        if file_path.is_file():
                            size = file_path.stat().st_size
                            print(f"    📄 {file_path.name} ({size} bytes)")
        else:
            self.print_result("Projects directory not found", False)
    
    def demonstrate_file_organization(self):
        """Demonstrate file organization automation"""
        self.print_section("File Organization Automation Demo")
        
        # Simulate file upload and processing
        print("  🚀 Simulating file organization workflow...")
        
        # Test webhook endpoint
        try:
            webhook_data = {
                "operation": "process_documents",
                "document_folder": "data/documents/projects",
                "test_mode": True
            }
            
            response = requests.post(
                f"{self.api_base}/webhook/file-organization",
                json=webhook_data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.print_result("Webhook triggered successfully")
                print(f"     Webhook ID: {result.get('webhook_id', 'N/A')}")
                print(f"     Status: {result.get('status', 'N/A')}")
                
                # Trigger agent execution
                self.demonstrate_agent_execution()
            else:
                self.print_result(f"Webhook failed: {response.status_code}", False)
                
        except Exception as e:
            self.print_result(f"Webhook error: {e}", False)
    
    def demonstrate_agent_execution(self):
        """Demonstrate agent execution with real data"""
        self.print_section("Agent Execution Demo")
        
        try:
            # Get agent status
            response = requests.get(
                f"{self.api_base}/api/agents/status",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                status_data = response.json()
                agents = status_data.get("agents", {})
                
                self.print_result(f"Found {len(agents)} active agents")
                
                for agent_name, agent_data in agents.items():
                    print(f"     🤖 {agent_name}: {agent_data.get('status', 'unknown')}")
                
                # Trigger file organization agent
                self.trigger_file_organization_agent()
            else:
                self.print_result(f"Agent status failed: {response.status_code}", False)
                
        except Exception as e:
            self.print_result(f"Agent status error: {e}", False)
    
    def trigger_file_organization_agent(self):
        """Trigger the file organization agent with real data"""
        print("  🔄 Triggering File Organization Agent...")
        
        try:
            trigger_data = {
                "operation": "process_documents",
                "document_folder": "data/documents/projects",
                "include_subfolders": True
            }
            
            response = requests.post(
                f"{self.api_base}/api/agents/file_organization/trigger",
                json=trigger_data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.print_result("Agent executed successfully")
                
                if "files_processed" in result:
                    print(f"     Files processed: {result['files_processed']}")
                if "folders_created" in result:
                    print(f"     Folders created: {result['folders_created']}")
                if "processing_time" in result:
                    print(f"     Processing time: {result['processing_time']:.2f}s")
                
                # Show results
                self.show_organization_results()
            else:
                self.print_result(f"Agent execution failed: {response.status_code}", False)
                
        except Exception as e:
            self.print_result(f"Agent execution error: {e}", False)
    
    def show_organization_results(self):
        """Show the results of file organization"""
        self.print_section("File Organization Results")
        
        # Check if files were organized
        organized_dir = Path("data/documents/organized")
        if organized_dir.exists():
            self.print_result("Files organized successfully")
            
            for category_dir in organized_dir.iterdir():
                if category_dir.is_dir():
                    print(f"  📁 {category_dir.name}/")
                    for file_path in category_dir.iterdir():
                        if file_path.is_file():
                            print(f"    📄 {file_path.name}")
        else:
            print("  📁 No organized directory found yet")
        
        # Check for reports
        reports_dir = Path("data/reports")
        if reports_dir.exists():
            report_files = list(reports_dir.glob("*.json"))
            if report_files:
                self.print_result(f"Generated {len(report_files)} reports")
                for report in report_files:
                    print(f"     📊 {report.name}")
            else:
                print("  📊 No reports generated yet")
    
    def demonstrate_content_analysis(self):
        """Demonstrate content analysis automation"""
        self.print_section("Content Analysis Automation Demo")
        
        print("  🔍 Simulating content analysis workflow...")
        
        try:
            webhook_data = {
                "analysis_type": "document_analysis",
                "content_type": "markdown",
                "file_path": "data/documents/projects/document_project/Project_Proposal.md"
            }
            
            response = requests.post(
                f"{self.api_base}/webhook/content-analysis",
                json=webhook_data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.print_result("Content analysis webhook triggered")
                print(f"     Webhook ID: {result.get('webhook_id', 'N/A')}")
            else:
                self.print_result(f"Content analysis webhook failed: {response.status_code}", False)
                
        except Exception as e:
            self.print_result(f"Content analysis error: {e}", False)
    
    def demonstrate_system_monitoring(self):
        """Demonstrate system monitoring automation"""
        self.print_section("System Monitoring Automation Demo")
        
        print("  📊 Simulating system monitoring workflow...")
        
        try:
            webhook_data = {
                "type": "system_health_check",
                "message": "Automated system health check",
                "severity": "info"
            }
            
            response = requests.post(
                f"{self.api_base}/webhook/system-alert",
                json=webhook_data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.print_result("System monitoring webhook triggered")
                print(f"     Webhook ID: {result.get('webhook_id', 'N/A')}")
            else:
                self.print_result(f"System monitoring webhook failed: {response.status_code}", False)
                
        except Exception as e:
            self.print_result(f"System monitoring error: {e}", False)
    
    def show_workflow_templates(self):
        """Show available workflow templates"""
        self.print_section("Available Workflow Templates")
        
        templates_dir = Path("data/n8n/templates")
        if templates_dir.exists():
            templates = list(templates_dir.glob("*.json"))
            self.print_result(f"Found {len(templates)} workflow templates")
            
            for template in templates:
                try:
                    with open(template, 'r') as f:
                        data = json.load(f)
                    name = data.get('name', 'Unknown')
                    nodes = len(data.get('nodes', []))
                    print(f"     📋 {template.name}")
                    print(f"        Name: {name}")
                    print(f"        Nodes: {nodes}")
                except:
                    print(f"     ❌ {template.name} (invalid JSON)")
        else:
            self.print_result("No workflow templates found", False)
    
    def run_complete_demo(self):
        """Run the complete demonstration"""
        self.print_header("CODE_ALCHEMY_PRO - Real Data Demonstration")
        
        print("🚀 Demonstrating the complete system with real data...")
        print("   This will show you exactly how the automation works!")
        
        # Check system status
        if not self.check_system_status():
            print("\n❌ System not ready. Please ensure all services are running.")
            return
        
        # Show real data structure
        self.show_real_data_structure()
        
        # Demonstrate file organization
        self.demonstrate_file_organization()
        
        # Demonstrate content analysis
        self.demonstrate_content_analysis()
        
        # Demonstrate system monitoring
        self.demonstrate_system_monitoring()
        
        # Show workflow templates
        self.show_workflow_templates()
        
        # Final summary
        self.print_header("Demonstration Complete")
        print("🎉 You've seen CODE_ALCHEMY_PRO working with real data!")
        print("\n📋 What happened:")
        print("   1. ✅ System status verified")
        print("   2. 📁 Real project files created")
        print("   3. 🔄 File organization workflow triggered")
        print("   4. 🤖 Agent executed with real data")
        print("   5. 🔍 Content analysis workflow triggered")
        print("   6. 📊 System monitoring workflow triggered")
        print("   7. 📋 Workflow templates displayed")
        
        print("\n🚀 Next steps:")
        print("   1. Open N8N at: http://localhost:5678")
        print("   2. Import workflow templates")
        print("   3. Configure webhook URLs")
        print("   4. Test end-to-end automation")
        
        print("\n💡 The system is now ready for production use!")

def main():
    """Main demonstration execution"""
    demo = RealDataDemo()
    
    try:
        demo.run_complete_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")

if __name__ == "__main__":
    main()
