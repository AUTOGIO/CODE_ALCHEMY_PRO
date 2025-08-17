#!/usr/bin/env python3
"""
SMART WORKSPACE Professional - Project Management Demo
Demonstrates professional project file organization capabilities
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def main():
    """Main demo function"""
    print("🧪 SMART WORKSPACE Professional - Project Management Demo")
    print("=" * 70)
    
    # Check if we can import the agent
    try:
        from src.agents.professional_file_manager.agent import ProfessionalFileManagerAgent
        print("✅ Professional File Manager Agent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import agent: {e}")
        print("Please ensure the agent is properly installed")
        return
    
    # Initialize the agent
    print("\n🚀 Initializing Professional File Manager Agent...")
    agent = ProfessionalFileManagerAgent()
    print("✅ Agent initialized successfully")
    
    # Demo 1: Create a marketing campaign project
    print("\n📁 Demo 1: Creating Marketing Campaign Project")
    print("-" * 50)
    
    project_result = agent.execute({
        'operation': 'create_project',
        'project_name': 'Summer_2025_Campaign',
        'project_type': 'marketing_campaign',
        'client_name': 'Acme_Corp'
    })
    
    if project_result['success']:
        print(f"✅ Project created: {project_result['project_path']}")
        print(f"📋 Project metadata: {json.dumps(project_result['metadata'], indent=2)}")
    else:
        print(f"❌ Project creation failed: {project_result['error']}")
    
    # Demo 2: Create a software development project
    print("\n💻 Demo 2: Creating Software Development Project")
    print("-" * 50)
    
    software_result = agent.execute({
        'operation': 'create_project',
        'project_name': 'Mobile_App_v2.0',
        'project_type': 'software_project',
        'client_name': 'Startup_XYZ'
    })
    
    if software_result['success']:
        print(f"✅ Software project created: {software_result['project_path']}")
        print(f"📋 Project metadata: {json.dumps(software_result['metadata'], indent=2)}")
    else:
        print(f"❌ Software project creation failed: {software_result['error']}")
    
    # Demo 3: Setup automated workflow
    print("\n🔄 Demo 3: Setting Up Automated Workflow")
    print("-" * 50)
    
    workflow_result = agent.execute({
        'operation': 'setup_workflow',
        'workflow_name': 'Auto_File_Processing',
        'workflow_type': 'file_processing'
    })
    
    if workflow_result['success']:
        print(f"✅ Workflow created: {workflow_result['workflow_name']}")
        print(f"📋 Workflow config: {json.dumps(workflow_result['config'], indent=2)}")
    else:
        print(f"❌ Workflow creation failed: {workflow_result['error']}")
    
    # Demo 4: Get project information
    print("\n📊 Demo 4: Getting Project Information")
    print("-" * 50)
    
    projects_info = agent.execute({
        'operation': 'get_project_info'
    })
    
    if projects_info['success']:
        print(f"📁 Total projects: {projects_info['total_projects']}")
        for project in projects_info['projects']:
            print(f"  - {project['name']}: {project['metadata']['project_type']}")
    else:
        print(f"❌ Failed to get project info: {projects_info['error']}")
    
    # Demo 5: Get agent capabilities
    print("\n🔧 Demo 5: Agent Capabilities")
    print("-" * 50)
    
    capabilities = agent.get_capabilities()
    print(f"🤖 Agent: {capabilities['name']}")
    print(f"📝 Description: {capabilities['description']}")
    print(f"⚡ Supported operations: {', '.join(capabilities['supported_operations'])}")
    print(f"📋 Templates available: {', '.join(capabilities['templates_available'])}")
    print(f"🔄 Workflow types: {', '.join(capabilities['workflow_types'])}")
    
    # Demo 6: Get agent status
    print("\n📈 Demo 6: Agent Status")
    print("-" * 50)
    
    status = agent.get_status()
    print(f"🔄 Status: {status['status']}")
    print(f"📊 Processing stats:")
    for key, value in status['processing_stats'].items():
        print(f"  - {key}: {value}")
    print(f"📋 Templates: {status['templates_available']}")
    print(f"🔄 Workflows: {status['workflows_active']}")
    
    # Demo 7: Show project structure
    print("\n🏗️ Demo 7: Project Structure Overview")
    print("-" * 50)
    
    projects_dir = Path('data/projects')
    if projects_dir.exists():
        print("📁 Projects directory structure:")
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                print(f"  📁 {project_dir.name}/")
                metadata_path = project_dir / 'project_metadata.json'
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    print(f"    📋 Type: {metadata['project_type']}")
                    print(f"    👤 Client: {metadata['client_name']}")
                    print(f"    📅 Created: {metadata['created_date'][:10]}")
                    print(f"    📊 Phases: {len(metadata['phases'])}")
                    
                    # Show phase structure
                    for phase in metadata['phases']:
                        phase_path = project_dir / phase
                        if phase_path.exists():
                            files = list(phase_path.glob('*'))
                            print(f"      📁 {phase}/ ({len(files)} files)")
    
    # Demo 8: Show templates
    print("\n📚 Demo 8: Available Templates")
    print("-" * 50)
    
    templates_dir = Path('data/templates')
    if templates_dir.exists():
        print("📋 Available project templates:")
        for template_file in templates_dir.glob('*.json'):
            with open(template_file, 'r') as f:
                template = json.load(f)
            print(f"  📋 {template['name']}")
            print(f"    📝 {template.get('description', 'No description')}")
            print(f"    🏗️ Structure: {' → '.join(template.get('structure', []))}")
            print(f"    📄 Files: {len(template.get('files', []))}")
    
    # Demo 9: Show workflows
    print("\n🔄 Demo 9: Active Workflows")
    print("-" * 50)
    
    workflows_dir = Path('data/workflows')
    if workflows_dir.exists():
        print("🔄 Active workflows:")
        for workflow_file in workflows_dir.glob('*.json'):
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
            print(f"  🔄 {workflow['name']}")
            print(f"    📝 {workflow.get('description', 'No description')}")
            print(f"    🏷️ Type: {workflow.get('type', 'Unknown')}")
            print(f"    📊 Status: {workflow.get('status', 'Unknown')}")
            print(f"    📅 Created: {workflow.get('created_date', 'Unknown')[:10] if workflow.get('created_date') else 'Unknown'}")
    
    print("\n🎉 Project Management Demo Completed!")
    print("=" * 70)
    print("🚀 Your system now has professional project management capabilities!")
    print("📁 Check the 'data/projects' directory for created projects")
    print("🔄 Check the 'data/workflows' directory for automation workflows")
    print("📋 Check the 'data/templates' directory for project templates")

if __name__ == "__main__":
    main()
