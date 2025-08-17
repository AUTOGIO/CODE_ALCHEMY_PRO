"""
Node-RED Lite Component
Lightweight workflow automation integrated with CODE_ALCHEMY dashboard
"""

import streamlit as st
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import threading

class NodeRedLite:
    """Ultra-lightweight Node-RED implementation"""
    
    def __init__(self):
        self.setup_session_state()
        self.flows_dir = Path('data/workflows')
        self.flows_dir.mkdir(exist_ok=True)
        
        # Essential nodes
        self.nodes = {
            'file_watcher': {
                'name': 'File Watcher',
                'description': 'Monitor file system changes',
                'icon': '📁',
                'config': ['path', 'events', 'filters']
            },
            'webhook': {
                'name': 'Webhook',
                'description': 'HTTP endpoint for triggers',
                'icon': '🔗',
                'config': ['url', 'method', 'headers']
            },
            'function': {
                'name': 'Function',
                'description': 'Custom JavaScript logic',
                'icon': '⚡',
                'config': ['code', 'inputs', 'outputs']
            },
            'n8n_trigger': {
                'name': 'N8N Trigger',
                'description': 'Trigger N8N workflows',
                'icon': '🤖',
                'config': ['workflow_id', 'webhook_url', 'data_mapping']
            },
            'file_processor': {
                'name': 'File Processor',
                'description': 'Process and organize files',
                'icon': '📊',
                'config': ['source_path', 'destination', 'filters']
            }
        }
    
    def setup_session_state(self):
        """Initialize Node-RED Lite session state"""
        if 'node_red_flows' not in st.session_state:
            st.session_state.node_red_flows = []
        
        if 'node_red_templates' not in st.session_state:
            st.session_state.node_red_templates = self._load_flow_templates()
    
    def _load_flow_templates(self) -> List[Dict[str, Any]]:
        """Load pre-built flow templates"""
        return [
            {
                'name': 'Auto File Organization',
                'description': 'Automatically organize new files',
                'icon': '📁',
                'nodes': [
                    {'type': 'file_watcher', 'config': {'path': 'data/documents', 'events': ['created']}},
                    {'type': 'file_processor', 'config': {'source_path': 'data/documents', 'destination': 'data/organized'}},
                    {'type': 'n8n_trigger', 'config': {'workflow_id': 'file_organization', 'webhook_url': 'http://localhost:5678/webhook'}}
                ]
            },
            {
                'name': 'Project Setup Automation',
                'description': 'Auto-create project structure',
                'icon': '🚀',
                'nodes': [
                    {'type': 'webhook', 'config': {'url': '/webhook/new-project', 'method': 'POST'}},
                    {'type': 'function', 'config': {'code': 'createProjectStructure(msg.payload)'}},
                    {'type': 'n8n_trigger', 'config': {'workflow_id': 'project_setup', 'webhook_url': 'http://localhost:5678/webhook'}}
                ]
            },
            {
                'name': 'System Health Monitor',
                'description': 'Monitor system resources',
                'icon': '💻',
                'nodes': [
                    {'type': 'function', 'config': {'code': 'checkSystemHealth()'}},
                    {'type': 'function', 'config': {'code': 'sendAlertIfNeeded(msg.payload)'}},
                    {'type': 'n8n_trigger', 'config': {'workflow_id': 'system_monitor', 'webhook_url': 'http://localhost:5678/webhook'}}
                ]
            }
        ]
    
    def render_node_red_lite(self):
        """Render Node-RED Lite interface"""
        st.header("🔄 Workflow Automation (Lite)")
        st.info("Lightweight workflow automation integrated with your dashboard")
        
        # Quick flow creation
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Quick Flows")
            self._render_quick_flows()
        
        with col2:
            st.subheader("📋 Active Flows")
            self._render_active_flows()
        
        # Flow builder
        st.subheader("🔧 Flow Builder")
        self._render_flow_builder()
        
        # Flow templates
        st.subheader("📚 Flow Templates")
        self._render_flow_templates()
    
    def _render_quick_flows(self):
        """Render quick flow creation buttons"""
        if st.button("📁 File Monitor", key="quick_file_monitor"):
            self._create_file_monitor_flow()
        
        if st.button("⚡ System Check", key="quick_system_check"):
            self._create_system_check_flow()
        
        if st.button("🔄 Auto Backup", key="quick_auto_backup"):
            self._create_auto_backup_flow()
        
        if st.button("📊 Report Generator", key="quick_report_gen"):
            self._create_report_generator_flow()
    
    def _render_active_flows(self):
        """Render currently active flows"""
        flows = self._get_active_flows()
        
        if not flows:
            st.info("No active flows. Create one using the quick flow buttons!")
            return
        
        for flow in flows:
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{flow['name']}**")
                st.caption(flow['description'])
            
            with col2:
                status_color = "🟢" if flow['enabled'] else "🔴"
                st.write(f"{status_color} {flow['status']}")
            
            with col3:
                if st.button("⚙️", key=f"config_{flow['id']}"):
                    self._configure_flow(flow)
    
    def _render_flow_builder(self):
        """Render custom flow builder"""
        with st.expander("🔧 Build Custom Flow", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                flow_name = st.text_input("Flow Name", placeholder="My Custom Flow")
                flow_description = st.text_area("Description", placeholder="What does this flow do?")
                
                # Node selection
                st.subheader("📦 Select Nodes")
                selected_nodes = []
                
                for node_type, node_info in self.nodes.items():
                    if st.checkbox(f"{node_info['icon']} {node_info['name']}", key=f"node_{node_type}"):
                        selected_nodes.append({
                            'type': node_type,
                            'config': self._get_node_config(node_type)
                        })
            
            with col2:
                st.subheader("🔗 Flow Preview")
                if selected_nodes:
                    self._render_flow_preview(selected_nodes)
                else:
                    st.info("Select nodes to see flow preview")
                
                if st.button("🚀 Create Flow", disabled=not flow_name or not selected_nodes):
                    if flow_name and selected_nodes:
                        self._create_custom_flow(flow_name, flow_description, selected_nodes)
    
    def _render_flow_templates(self):
        """Render available flow templates"""
        for template in st.session_state.node_red_templates:
            with st.expander(f"{template['icon']} {template['name']}", expanded=False):
                st.write(template['description'])
                
                # Show nodes in template
                st.subheader("📦 Flow Nodes")
                for node in template['nodes']:
                    node_info = self.nodes.get(node['type'], {})
                    st.write(f"{node_info.get('icon', '📦')} {node_info.get('name', node['type'])}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Use Template", key=f"use_{template['name']}"):
                        self._use_flow_template(template)
                
                with col2:
                    if st.button("🔧 Customize", key=f"customize_{template['name']}"):
                        self._customize_flow_template(template)
    
    def _get_node_config(self, node_type: str) -> Dict[str, Any]:
        """Get configuration for a specific node type"""
        node_info = self.nodes.get(node_type, {})
        config = {}
        
        for config_key in node_info.get('config', []):
            if config_key == 'path':
                config[config_key] = st.text_input(f"{config_key.title()}", value="data/documents", key=f"{node_type}_{config_key}")
            elif config_key == 'events':
                config[config_key] = st.multiselect(f"{config_key.title()}", 
                    options=['created', 'modified', 'deleted'], 
                    default=['created'], 
                    key=f"{node_type}_{config_key}")
            elif config_key == 'code':
                config[config_key] = st.text_area(f"{config_key.title()}", 
                    value="// Custom code here", 
                    key=f"{node_type}_{config_key}")
            else:
                config[config_key] = st.text_input(f"{config_key.title()}", key=f"{node_type}_{config_key}")
        
        return config
    
    def _render_flow_preview(self, nodes: List[Dict[str, Any]]):
        """Render visual preview of the flow"""
        st.write("**Flow Structure:**")
        
        for i, node in enumerate(nodes):
            node_info = self.nodes.get(node['type'], {})
            icon = node_info.get('icon', '📦')
            name = node_info.get('name', node['type'])
            
            if i > 0:
                st.write("⬇️")
            
            st.write(f"{icon} **{name}**")
            
            # Show key config
            config = node.get('config', {})
            if config:
                for key, value in list(config.items())[:2]:  # Show first 2 config items
                    if isinstance(value, list):
                        st.caption(f"{key}: {', '.join(value)}")
                    else:
                        st.caption(f"{key}: {value}")
    
    def _create_file_monitor_flow(self):
        """Create a file monitoring flow"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': 'Auto File Processing',
            'description': 'Automatically organize new files',
            'type': 'file_monitoring',
            'nodes': [
                {
                    'type': 'file_watcher',
                    'config': {
                        'path': 'data/documents',
                        'events': ['created', 'modified'],
                        'filters': ['*.pdf', '*.docx', '*.jpg', '*.png']
                    }
                },
                {
                    'type': 'file_processor',
                    'config': {
                        'source_path': 'data/documents',
                        'destination': 'data/organized',
                        'filters': 'auto_categorize'
                    }
                },
                {
                    'type': 'n8n_trigger',
                    'config': {
                        'workflow_id': 'file_organization',
                        'webhook_url': 'http://localhost:5678/webhook',
                        'data_mapping': 'file_info'
                    }
                }
            ],
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success("✅ File monitor flow created!")
        st.rerun()
    
    def _create_system_check_flow(self):
        """Create a system health check flow"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': 'System Health Monitor',
            'description': 'Monitor system resources and trigger alerts',
            'type': 'system_monitoring',
            'nodes': [
                {
                    'type': 'function',
                    'config': {
                        'code': 'checkSystemHealth()',
                        'inputs': 'timer',
                        'outputs': 'health_data'
                    }
                },
                {
                    'type': 'function',
                    'config': {
                        'code': 'sendAlertIfNeeded(msg.payload)',
                        'inputs': 'health_data',
                        'outputs': 'alert_triggered'
                    }
                },
                {
                    'type': 'n8n_trigger',
                    'config': {
                        'workflow_id': 'system_monitor',
                        'webhook_url': 'http://localhost:5678/webhook',
                        'data_mapping': 'system_metrics'
                    }
                }
            ],
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success("✅ System monitor flow created!")
        st.rerun()
    
    def _create_auto_backup_flow(self):
        """Create an auto backup flow"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': 'Auto Backup System',
            'description': 'Automatically backup important files',
            'type': 'backup_automation',
            'nodes': [
                {
                    'type': 'function',
                    'config': {
                        'code': 'checkBackupNeeded()',
                        'inputs': 'timer',
                        'outputs': 'backup_required'
                    }
                },
                {
                    'type': 'file_processor',
                    'config': {
                        'source_path': 'data/projects',
                        'destination': 'data/backups',
                        'filters': 'important_files_only'
                    }
                },
                {
                    'type': 'n8n_trigger',
                    'config': {
                        'workflow_id': 'backup_workflow',
                        'webhook_url': 'http://localhost:5678/webhook',
                        'data_mapping': 'backup_status'
                    }
                }
            ],
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success("✅ Auto backup flow created!")
        st.rerun()
    
    def _create_report_generator_flow(self):
        """Create a report generation flow"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': 'Auto Report Generator',
            'description': 'Generate reports automatically',
            'type': 'report_automation',
            'nodes': [
                {
                    'type': 'function',
                    'config': {
                        'code': 'generateWeeklyReport()',
                        'inputs': 'timer',
                        'outputs': 'report_data'
                    }
                },
                {
                    'type': 'function',
                    'config': {
                        'code': 'formatReport(msg.payload)',
                        'inputs': 'report_data',
                        'outputs': 'formatted_report'
                    }
                },
                {
                    'type': 'n8n_trigger',
                    'config': {
                        'workflow_id': 'report_generation',
                        'webhook_url': 'http://localhost:5678/webhook',
                        'data_mapping': 'report_content'
                    }
                }
            ],
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success("✅ Report generator flow created!")
        st.rerun()
    
    def _create_custom_flow(self, name: str, description: str, nodes: List[Dict[str, Any]]):
        """Create a custom flow"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': name,
            'description': description,
            'type': 'custom',
            'nodes': nodes,
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success(f"✅ Custom flow '{name}' created!")
        st.rerun()
    
    def _use_flow_template(self, template: Dict[str, Any]):
        """Use a flow template as-is"""
        flow = {
            'id': f"flow_{int(time.time())}",
            'name': f"{template['name']} - {datetime.now().strftime('%Y%m%d')}",
            'description': template['description'],
            'type': template['name'].lower().replace(' ', '_'),
            'nodes': template['nodes'].copy(),
            'enabled': True,
            'created_date': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._save_flow(flow)
        st.success(f"✅ Flow template '{template['name']}' applied!")
        st.rerun()
    
    def _customize_flow_template(self, template: Dict[str, Any]):
        """Customize a flow template"""
        st.info(f"Customizing template: {template['name']}")
        st.write("This feature will be available in the next update!")
    
    def _save_flow(self, flow: Dict[str, Any]):
        """Save a flow to storage"""
        # Add to session state
        st.session_state.node_red_flows.append(flow)
        
        # Save to file
        flow_path = self.flows_dir / f"{flow['id']}.json"
        with open(flow_path, 'w') as f:
            json.dump(flow, f, indent=2)
    
    def _get_active_flows(self) -> List[Dict[str, Any]]:
        """Get currently active flows"""
        return st.session_state.node_red_flows
    
    def _configure_flow(self, flow: Dict[str, Any]):
        """Configure an existing flow"""
        st.info(f"Configuring flow: {flow['name']}")
        st.write("Flow configuration will be available in the next update!")
    
    def get_status(self) -> Dict[str, Any]:
        """Get Node-RED Lite status"""
        return {
            'flows_active': len(self._get_active_flows()),
            'templates_available': len(st.session_state.node_red_templates),
            'nodes_supported': len(self.nodes),
            'status': 'active'
        }
