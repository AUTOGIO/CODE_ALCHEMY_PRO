#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Professional File Manager Agent
Implements professional project file organization standards
"""

import sys
import shutil
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import mimetypes
import hashlib

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from ..base.agent_interface import BaseAgent, AgentStatus

class ProfessionalFileManagerAgent(BaseAgent):
    """Professional file organization agent with industry standards"""
    
    def __init__(self):
        super().__init__("Professional File Manager")
        self.processing_stats.update({
            'projects_created': 0,
            'files_organized': 0,
            'templates_applied': 0,
            'workflows_triggered': 0
        })
        
        # Setup professional directories
        self.projects_dir = Path('data/projects')
        self.templates_dir = Path('data/templates')
        self.workflows_dir = Path('data/workflows')
        
        # Ensure directories exist
        self.projects_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.workflows_dir.mkdir(exist_ok=True)
        
        # Initialize professional templates
        self._setup_professional_templates()
    
    def _setup_professional_templates(self):
        """Setup professional project templates"""
        templates = {
            'marketing_campaign': {
                'name': 'Marketing Campaign',
                'structure': [
                    '01-brief',
                    '02-creative', 
                    '03-production',
                    '04-results'
                ],
                'files': [
                    'project_brief.docx',
                    'timeline.xlsx',
                    'budget_template.xlsx',
                    'creative_brief.md'
                ]
            },
            'software_project': {
                'name': 'Software Development',
                'structure': [
                    '01-requirements',
                    '02-development',
                    '03-testing',
                    '04-deployment'
                ],
                'files': [
                    'requirements.md',
                    'technical_specs.md',
                    'test_plan.md',
                    'deployment_guide.md'
                ]
            },
            'consulting_project': {
                'name': 'Consulting Project',
                'structure': [
                    '01-discovery',
                    '02-analysis',
                    '03-recommendations',
                    '04-implementation'
                ],
                'files': [
                    'project_scope.docx',
                    'analysis_framework.xlsx',
                    'recommendations_presentation.pptx',
                    'implementation_plan.md'
                ]
            }
        }
        
        # Save templates
        for template_id, template_data in templates.items():
            template_path = self.templates_dir / f"{template_id}.json"
            with open(template_path, 'w') as f:
                json.dump(template_data, f, indent=2)
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        operation = parameters.get('operation', 'create_project')
        
        if operation == 'create_project':
            return self.create_project_structure(parameters)
        elif operation == 'organize_files':
            return self.organize_files(parameters)
        elif operation == 'apply_template':
            return self.apply_template(parameters)
        elif operation == 'setup_workflow':
            return self.setup_workflow(parameters)
        elif operation == 'get_project_info':
            return self.get_project_info(parameters)
        else:
            return {
                'success': False,
                'error': f'Unknown operation: {operation}',
                'supported_operations': [
                    'create_project', 'organize_files', 'apply_template', 
                    'setup_workflow', 'get_project_info'
                ]
            }
    
    def create_project_structure(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create professional project structure"""
        project_name = parameters.get('project_name')
        project_type = parameters.get('project_type', 'marketing_campaign')
        client_name = parameters.get('client_name', 'internal')
        
        if not project_name:
            return {'success': False, 'error': 'Project name is required'}
        
        # Create project directory
        project_path = self.projects_dir / f"{client_name}-{project_name}-{datetime.now().strftime('%Y')}"
        project_path.mkdir(exist_ok=True)
        
        # Load template
        template_path = self.templates_dir / f"{project_type}.json"
        if template_path.exists():
            with open(template_path, 'r') as f:
                template = json.load(f)
            
            # Create structure
            for phase in template['structure']:
                phase_path = project_path / phase
                phase_path.mkdir(exist_ok=True)
                
                # Create phase-specific files
                if phase == '01-brief':
                    self._create_brief_files(phase_path, project_name, client_name)
                elif phase == '02-creative':
                    self._create_creative_files(phase_path, project_name)
                elif phase == '03-production':
                    self._create_production_files(phase_path, project_name)
                elif phase == '04-results':
                    self._create_results_files(phase_path, project_name)
        
        # Create project metadata
        metadata = {
            'project_name': project_name,
            'project_type': project_type,
            'client_name': client_name,
            'created_date': datetime.now().isoformat(),
            'status': 'active',
            'phases': template['structure'] if template_path.exists() else []
        }
        
        metadata_path = project_path / 'project_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.processing_stats['projects_created'] += 1
        
        return {
            'success': True,
            'project_path': str(project_path),
            'metadata': metadata,
            'message': f'Professional project structure created: {project_name}'
        }
    
    def _create_brief_files(self, phase_path: Path, project_name: str, client_name: str):
        """Create brief phase files"""
        # Project brief template
        brief_content = f"""# Project Brief: {project_name}

## Client: {client_name}
## Project Type: {project_name}
## Date: {datetime.now().strftime('%Y-%m-%d')}

## Project Overview
[Describe the project objectives and goals]

## Target Audience
[Define the target audience]

## Key Deliverables
[List the main deliverables]

## Timeline
[Project timeline and milestones]

## Budget
[Budget information]

## Success Metrics
[How will success be measured]
"""
        
        with open(phase_path / 'project_brief.md', 'w') as f:
            f.write(brief_content)
        
        # Timeline template
        timeline_content = f"""Project Timeline: {project_name}

Phase 1: Planning (Week 1-2)
Phase 2: Execution (Week 3-6)  
Phase 3: Review (Week 7-8)
Phase 4: Delivery (Week 9-10)
"""
        
        with open(phase_path / 'timeline.md', 'w') as f:
            f.write(timeline_content)
    
    def _create_creative_files(self, phase_path: Path, project_name: str):
        """Create creative phase files"""
        creative_brief = f"""# Creative Brief: {project_name}

## Creative Direction
[Describe the creative approach]

## Visual Style
[Define visual style guidelines]

## Brand Guidelines
[Brand requirements and restrictions]

## Deliverables
[Creative deliverables list]
"""
        
        with open(phase_path / 'creative_brief.md', 'w') as f:
            f.write(creative_brief)
    
    def _create_production_files(self, phase_path: Path, project_name: str):
        """Create production phase files"""
        production_plan = f"""# Production Plan: {project_name}

## Production Timeline
[Production schedule]

## Resources Needed
[Required resources]

## Quality Standards
[Quality requirements]

## Review Process
[Review and approval process]
"""
        
        with open(phase_path / 'production_plan.md', 'w') as f:
            f.write(production_plan)
    
    def _create_results_files(self, phase_path: Path, project_name: str):
        """Create results phase files"""
        results_template = f"""# Results Report: {project_name}

## Project Outcomes
[Project results and achievements]

## Performance Metrics
[Key performance indicators]

## Lessons Learned
[What worked and what didn't]

## Recommendations
[Future recommendations]
"""
        
        with open(phase_path / 'results_template.md', 'w') as f:
            f.write(results_template)
    
    def organize_files(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Organize files using professional standards"""
        source_path = Path(parameters.get('source_path', 'data/documents'))
        project_name = parameters.get('project_name')
        
        if not source_path.exists():
            return {'success': False, 'error': f'Source path does not exist: {source_path}'}
        
        # Professional file organization
        organized_files = []
        
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                # Analyze file
                file_info = self._analyze_file(file_path)
                
                # Suggest professional location
                suggested_location = self._suggest_professional_location(file_info, project_name)
                
                # Organize file
                result = self._organize_file_professionally(file_path, suggested_location)
                organized_files.append(result)
        
        self.processing_stats['files_organized'] += len(organized_files)
        
        return {
            'success': True,
            'organized_files': organized_files,
            'message': f'Organized {len(organized_files)} files professionally'
        }
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file for professional categorization"""
        # Get file info
        stat = file_path.stat()
        
        # Determine file type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        
        # Analyze content (basic)
        content_analysis = self._analyze_content(file_path)
        
        return {
            'name': file_path.name,
            'path': str(file_path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'mime_type': mime_type,
            'extension': file_path.suffix.lower(),
            'content_analysis': content_analysis
        }
    
    def _analyze_content(self, file_path: Path) -> Dict[str, Any]:
        """Basic content analysis"""
        try:
            if file_path.suffix.lower() in ['.txt', '.md', '.py', '.js', '.html']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return {
                        'type': 'text',
                        'length': len(content),
                        'lines': content.count('\n'),
                        'keywords': self._extract_keywords(content)
                    }
            elif file_path.suffix.lower() in ['.pdf', '.docx', '.pptx']:
                return {
                    'type': 'document',
                    'size': file_path.stat().st_size
                }
            elif file_path.suffix.lower() in ['.jpg', '.png', '.gif']:
                return {
                    'type': 'image',
                    'size': file_path.stat().st_size
                }
            else:
                return {
                    'type': 'other',
                    'size': file_path.stat().st_size
                }
        except Exception as e:
            return {
                'type': 'unknown',
                'error': str(e)
            }
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction
        words = content.lower().split()
        # Filter common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        return list(set(keywords))[:10]  # Top 10 unique keywords
    
    def _suggest_professional_location(self, file_info: Dict[str, Any], project_name: str = None) -> str:
        """Suggest professional file location"""
        if project_name:
            # If we have a project, suggest project-specific location
            if file_info['extension'] in ['.md', '.txt', '.docx']:
                return f"projects/{project_name}/01-brief"
            elif file_info['extension'] in ['.jpg', '.png', '.gif']:
                return f"projects/{project_name}/02-creative"
            elif file_info['extension'] in ['.pdf', '.pptx']:
                return f"projects/{project_name}/03-production"
            else:
                return f"projects/{project_name}/02-creative"
        else:
            # General professional organization
            if file_info['content_analysis']['type'] == 'document':
                return "documents/professional"
            elif file_info['content_analysis']['type'] == 'image':
                return "media/creative"
            elif file_info['content_analysis']['type'] == 'text':
                return "documents/text"
            else:
                return "documents/other"
    
    def _organize_file_professionally(self, file_path: Path, suggested_location: str) -> Dict[str, Any]:
        """Organize file using professional standards"""
        try:
            # Create destination directory
            dest_dir = Path('data') / suggested_location
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate professional filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            professional_name = f"{timestamp}_{file_path.stem}{file_path.suffix}"
            dest_path = dest_dir / professional_name
            
            # Copy file to new location
            shutil.copy2(file_path, dest_path)
            
            return {
                'original_path': str(file_path),
                'new_path': str(dest_path),
                'professional_name': professional_name,
                'status': 'organized'
            }
        except Exception as e:
            return {
                'original_path': str(file_path),
                'error': str(e),
                'status': 'failed'
            }
    
    def apply_template(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Apply professional template to existing project"""
        project_path = Path(parameters.get('project_path'))
        template_type = parameters.get('template_type', 'marketing_campaign')
        
        if not project_path.exists():
            return {'success': False, 'error': f'Project path does not exist: {project_path}'}
        
        # Load template
        template_path = self.templates_dir / f"{template_type}.json"
        if not template_path.exists():
            return {'success': False, 'error': f'Template not found: {template_type}'}
        
        with open(template_path, 'r') as f:
            template = json.load(f)
        
        # Apply template structure
        for phase in template['structure']:
            phase_path = project_path / phase
            phase_path.mkdir(exist_ok=True)
        
        self.processing_stats['templates_applied'] += 1
        
        return {
            'success': True,
            'project_path': str(project_path),
            'template_applied': template_type,
            'message': f'Template {template_type} applied to project'
        }
    
    def setup_workflow(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Setup professional workflow automation"""
        workflow_name = parameters.get('workflow_name')
        workflow_type = parameters.get('workflow_type', 'file_processing')
        
        if not workflow_name:
            return {'success': False, 'error': 'Workflow name is required'}
        
        # Create workflow configuration
        workflow_config = {
            'name': workflow_name,
            'type': workflow_type,
            'created_date': datetime.now().isoformat(),
            'triggers': [],
            'actions': [],
            'enabled': True
        }
        
        # Add workflow-specific configuration
        if workflow_type == 'file_processing':
            workflow_config.update({
                'triggers': ['file_added', 'file_modified'],
                'actions': ['categorize_file', 'apply_template', 'trigger_n8n']
            })
        elif workflow_type == 'project_setup':
            workflow_config.update({
                'triggers': ['new_project_request'],
                'actions': ['create_structure', 'apply_template', 'notify_team']
            })
        
        # Save workflow
        workflow_path = self.workflows_dir / f"{workflow_name}.json"
        with open(workflow_path, 'w') as f:
            json.dump(workflow_config, f, indent=2)
        
        self.processing_stats['workflows_triggered'] += 1
        
        return {
            'success': True,
            'workflow_name': workflow_name,
            'config': workflow_config,
            'message': f'Workflow {workflow_name} created successfully'
        }
    
    def get_project_info(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get project information and status"""
        project_path = parameters.get('project_path')
        
        if project_path:
            # Get specific project info
            project_dir = Path(project_path)
            if project_dir.exists():
                metadata_path = project_dir / 'project_metadata.json'
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    # Get project structure
                    structure = {}
                    for item in project_dir.iterdir():
                        if item.is_dir():
                            structure[item.name] = len(list(item.iterdir()))
                    
                    return {
                        'success': True,
                        'project_info': metadata,
                        'structure': structure,
                        'total_files': sum(structure.values())
                    }
        
        # Get all projects info
        projects = []
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir():
                metadata_path = project_dir / 'project_metadata.json'
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    projects.append({
                        'name': project_dir.name,
                        'metadata': metadata,
                        'path': str(project_dir)
                    })
        
        return {
            'success': True,
            'projects': projects,
            'total_projects': len(projects)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'agent_name': self.agent_name,
            'status': self.status.value,
            'processing_stats': self.processing_stats,
            'templates_available': len(list(self.templates_dir.glob('*.json'))),
            'workflows_active': len(list(self.workflows_dir.glob('*.json')))
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and supported operations"""
        return {
            'name': 'Professional File Manager',
            'description': 'Professional project file organization with industry standards',
            'supported_operations': [
                'create_project',
                'organize_files', 
                'apply_template',
                'setup_workflow',
                'get_project_info'
            ],
            'templates_available': [
                'marketing_campaign',
                'software_project',
                'consulting_project'
            ],
            'workflow_types': [
                'file_processing',
                'project_setup',
                'automated_organization'
            ]
        }
