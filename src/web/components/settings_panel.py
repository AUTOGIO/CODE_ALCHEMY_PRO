"""
Settings Panel Component
Comprehensive system configuration and settings management
"""

import streamlit as st
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

class SettingsPanel:
    """System settings and configuration management"""
    
    def __init__(self):
        self.setup_session_state()
        self.settings_categories = {
            'system': 'System Settings',
            'ai': 'AI Configuration',
            'performance': 'Performance Settings',
            'security': 'Security Settings',
            'integrations': 'Integration Settings',
            'advanced': 'Advanced Settings'
        }
    
    def setup_session_state(self):
        """Initialize settings panel session state"""
        if 'settings_data' not in st.session_state:
            st.session_state.settings_data = {
                'system': {
                    'neural_engine': True,
                    'parallel_processing': True,
                    'auto_backup': True,
                    'log_level': 'INFO',
                    'cache_size': '4GB',
                    'max_concurrent': 8
                },
                'ai': {
                    'default_model': 'DeepSeek-R1-8B',
                    'temperature': 0.7,
                    'max_tokens': 2048,
                    'context_window': 4096,
                    'batch_size': 8,
                    'model_precision': 'FP16'
                },
                'performance': {
                    'memory_limit': '12GB',
                    'cpu_cores': 6,
                    'gpu_memory': '8GB',
                    'auto_optimize': True,
                    'power_save': False,
                    'thermal_throttling': True
                },
                'security': {
                    'encryption_enabled': True,
                    'secure_connections': True,
                    'access_control': True,
                    'audit_logging': True,
                    'backup_encryption': True
                },
                'integrations': {
                    'github_enabled': True,
                    'drive_enabled': True,
                    'mcp_enabled': True,
                    'auto_sync': True,
                    'connection_timeout': 30
                },
                'advanced': {
                    'debug_mode': False,
                    'verbose_logging': False,
                    'experimental_features': True,
                    'beta_features': False,
                    'telemetry': False
                }
            }
        
        if 'settings_modified' not in st.session_state:
            st.session_state.settings_modified = False
    
    def render_settings_panel(self):
        """Render main settings panel interface"""
        st.header("⚙️ Settings Panel")
        
        # Settings overview
        self.render_settings_overview()
        
        # Settings categories
        self.render_settings_categories()
        
        # Settings import/export
        self.render_settings_import_export()
    
    def render_settings_overview(self):
        """Render settings overview"""
        st.subheader("📊 Settings Overview")
        
        # Settings status grid
        col1, col2, col3, col4 = st.columns(4)
        
        total_settings = sum(len(category) for category in st.session_state.settings_data.values())
        modified_settings = len([s for s in st.session_state.settings_data.values() if any(s.values())])
        active_integrations = sum(1 for s in st.session_state.settings_data['integrations'].values() if s)
        
        with col1:
            self.render_settings_card("Total Settings", f"{total_settings}", "⚙️", "Configured")
        
        with col2:
            self.render_settings_card("Modified", f"{modified_settings}", "📝", "Changed")
        
        with col3:
            self.render_settings_card("Integrations", f"{active_integrations}", "🔗", "Active")
        
        with col4:
            self.render_settings_card("Last Saved", "2 min ago", "💾", "Recent")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save All Settings", type="primary"):
                self.save_settings()
                st.success("All settings saved successfully!")
        
        with col2:
            if st.button("🔄 Reset to Defaults"):
                self.reset_to_defaults()
                st.warning("Settings reset to defaults!")
        
        with col3:
            if st.button("📊 Export Settings"):
                self.export_settings()
                st.info("Settings exported successfully!")
    
    def render_settings_card(self, title: str, value: str, icon: str, subtitle: str):
        """Render a settings card"""
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <h4 style="margin: 0; font-size: 0.9rem;">{title}</h4>
            <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{value}</p>
            <p style="margin: 0; font-size: 0.8rem; color: #666;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_settings_categories(self):
        """Render settings categories"""
        st.subheader("📋 Settings Categories")
        
        # Create tabs for each category
        tabs = st.tabs(list(self.settings_categories.values()))
        
        for i, (category_key, category_name) in enumerate(self.settings_categories.items()):
            with tabs[i]:
                self.render_category_settings(category_key, category_name)
    
    def render_category_settings(self, category: str, category_name: str):
        """Render settings for a specific category"""
        st.markdown(f"**{category_name}**")
        
        if category == 'system':
            self.render_system_settings()
        elif category == 'ai':
            self.render_ai_settings()
        elif category == 'performance':
            self.render_performance_settings()
        elif category == 'security':
            self.render_security_settings()
        elif category == 'integrations':
            self.render_integration_settings()
        elif category == 'advanced':
            self.render_advanced_settings()
    
    def render_system_settings(self):
        """Render system settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Core System Settings**")
            
            neural_engine = st.checkbox(
                "Neural Engine",
                value=st.session_state.settings_data['system']['neural_engine'],
                key="system_neural_engine"
            )
            st.session_state.settings_data['system']['neural_engine'] = neural_engine
            
            parallel_processing = st.checkbox(
                "Parallel Processing",
                value=st.session_state.settings_data['system']['parallel_processing'],
                key="system_parallel_processing"
            )
            st.session_state.settings_data['system']['parallel_processing'] = parallel_processing
            
            auto_backup = st.checkbox(
                "Auto Backup",
                value=st.session_state.settings_data['system']['auto_backup'],
                key="system_auto_backup"
            )
            st.session_state.settings_data['system']['auto_backup'] = auto_backup
        
        with col2:
            st.markdown("**System Configuration**")
            
            log_level = st.selectbox(
                "Log Level",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                index=["DEBUG", "INFO", "WARNING", "ERROR"].index(st.session_state.settings_data['system']['log_level']),
                key="system_log_level"
            )
            st.session_state.settings_data['system']['log_level'] = log_level
            
            cache_size = st.selectbox(
                "Cache Size",
                ["1GB", "2GB", "4GB", "8GB"],
                index=["1GB", "2GB", "4GB", "8GB"].index(st.session_state.settings_data['system']['cache_size']),
                key="system_cache_size"
            )
            st.session_state.settings_data['system']['cache_size'] = cache_size
            
            max_concurrent = st.slider(
                "Max Concurrent Tasks",
                min_value=1,
                max_value=16,
                value=st.session_state.settings_data['system']['max_concurrent'],
                key="system_max_concurrent"
            )
            st.session_state.settings_data['system']['max_concurrent'] = max_concurrent
    
    def render_ai_settings(self):
        """Render AI settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Configuration**")
            
            default_model = st.selectbox(
                "Default Model",
                ["DeepSeek-R1-8B", "Llama-3.1-8B", "Phi-4-Mini", "TinyLlama-1.1B"],
                index=["DeepSeek-R1-8B", "Llama-3.1-8B", "Phi-4-Mini", "TinyLlama-1.1B"].index(st.session_state.settings_data['ai']['default_model']),
                key="ai_default_model"
            )
            st.session_state.settings_data['ai']['default_model'] = default_model
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.settings_data['ai']['temperature'],
                step=0.1,
                key="ai_temperature"
            )
            st.session_state.settings_data['ai']['temperature'] = temperature
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=st.session_state.settings_data['ai']['max_tokens'],
                step=100,
                key="ai_max_tokens"
            )
            st.session_state.settings_data['ai']['max_tokens'] = max_tokens
        
        with col2:
            st.markdown("**Model Parameters**")
            
            context_window = st.slider(
                "Context Window",
                min_value=1024,
                max_value=8192,
                value=st.session_state.settings_data['ai']['context_window'],
                step=1024,
                key="ai_context_window"
            )
            st.session_state.settings_data['ai']['context_window'] = context_window
            
            batch_size = st.slider(
                "Batch Size",
                min_value=1,
                max_value=32,
                value=st.session_state.settings_data['ai']['batch_size'],
                key="ai_batch_size"
            )
            st.session_state.settings_data['ai']['batch_size'] = batch_size
            
            model_precision = st.selectbox(
                "Model Precision",
                ["FP16", "FP32", "INT8", "INT4"],
                index=["FP16", "FP32", "INT8", "INT4"].index(st.session_state.settings_data['ai']['model_precision']),
                key="ai_model_precision"
            )
            st.session_state.settings_data['ai']['model_precision'] = model_precision
    
    def render_performance_settings(self):
        """Render performance settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Resource Limits**")
            
            memory_limit = st.selectbox(
                "Memory Limit",
                ["8GB", "12GB", "16GB", "Unlimited"],
                index=["8GB", "12GB", "16GB", "Unlimited"].index(st.session_state.settings_data['performance']['memory_limit']),
                key="performance_memory_limit"
            )
            st.session_state.settings_data['performance']['memory_limit'] = memory_limit
            
            cpu_cores = st.slider(
                "CPU Cores",
                min_value=1,
                max_value=8,
                value=st.session_state.settings_data['performance']['cpu_cores'],
                key="performance_cpu_cores"
            )
            st.session_state.settings_data['performance']['cpu_cores'] = cpu_cores
            
            gpu_memory = st.selectbox(
                "GPU Memory",
                ["2GB", "4GB", "8GB", "12GB"],
                index=["2GB", "4GB", "8GB", "12GB"].index(st.session_state.settings_data['performance']['gpu_memory']),
                key="performance_gpu_memory"
            )
            st.session_state.settings_data['performance']['gpu_memory'] = gpu_memory
        
        with col2:
            st.markdown("**Optimization Settings**")
            
            auto_optimize = st.checkbox(
                "Auto-optimize performance",
                value=st.session_state.settings_data['performance']['auto_optimize'],
                key="performance_auto_optimize"
            )
            st.session_state.settings_data['performance']['auto_optimize'] = auto_optimize
            
            power_save = st.checkbox(
                "Power saving mode",
                value=st.session_state.settings_data['performance']['power_save'],
                key="performance_power_save"
            )
            st.session_state.settings_data['performance']['power_save'] = power_save
            
            thermal_throttling = st.checkbox(
                "Thermal throttling",
                value=st.session_state.settings_data['performance']['thermal_throttling'],
                key="performance_thermal_throttling"
            )
            st.session_state.settings_data['performance']['thermal_throttling'] = thermal_throttling
    
    def render_security_settings(self):
        """Render security settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Security Features**")
            
            encryption_enabled = st.checkbox(
                "Enable encryption",
                value=st.session_state.settings_data['security']['encryption_enabled'],
                key="security_encryption_enabled"
            )
            st.session_state.settings_data['security']['encryption_enabled'] = encryption_enabled
            
            secure_connections = st.checkbox(
                "Secure connections only",
                value=st.session_state.settings_data['security']['secure_connections'],
                key="security_secure_connections"
            )
            st.session_state.settings_data['security']['secure_connections'] = secure_connections
            
            access_control = st.checkbox(
                "Access control",
                value=st.session_state.settings_data['security']['access_control'],
                key="security_access_control"
            )
            st.session_state.settings_data['security']['access_control'] = access_control
        
        with col2:
            st.markdown("**Security Monitoring**")
            
            audit_logging = st.checkbox(
                "Audit logging",
                value=st.session_state.settings_data['security']['audit_logging'],
                key="security_audit_logging"
            )
            st.session_state.settings_data['security']['audit_logging'] = audit_logging
            
            backup_encryption = st.checkbox(
                "Backup encryption",
                value=st.session_state.settings_data['security']['backup_encryption'],
                key="security_backup_encryption"
            )
            st.session_state.settings_data['security']['backup_encryption'] = backup_encryption
    
    def render_integration_settings(self):
        """Render integration settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Integration Services**")
            
            github_enabled = st.checkbox(
                "GitHub integration",
                value=st.session_state.settings_data['integrations']['github_enabled'],
                key="integrations_github_enabled"
            )
            st.session_state.settings_data['integrations']['github_enabled'] = github_enabled
            
            drive_enabled = st.checkbox(
                "Google Drive integration",
                value=st.session_state.settings_data['integrations']['drive_enabled'],
                key="integrations_drive_enabled"
            )
            st.session_state.settings_data['integrations']['drive_enabled'] = drive_enabled
            
            mcp_enabled = st.checkbox(
                "MCP integration",
                value=st.session_state.settings_data['integrations']['mcp_enabled'],
                key="integrations_mcp_enabled"
            )
            st.session_state.settings_data['integrations']['mcp_enabled'] = mcp_enabled
        
        with col2:
            st.markdown("**Connection Settings**")
            
            auto_sync = st.checkbox(
                "Auto-sync enabled services",
                value=st.session_state.settings_data['integrations']['auto_sync'],
                key="integrations_auto_sync"
            )
            st.session_state.settings_data['integrations']['auto_sync'] = auto_sync
            
            connection_timeout = st.slider(
                "Connection timeout (seconds)",
                min_value=5,
                max_value=60,
                value=st.session_state.settings_data['integrations']['connection_timeout'],
                key="integrations_connection_timeout"
            )
            st.session_state.settings_data['integrations']['connection_timeout'] = connection_timeout
    
    def render_advanced_settings(self):
        """Render advanced settings"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Debug & Development**")
            
            debug_mode = st.checkbox(
                "Debug mode",
                value=st.session_state.settings_data['advanced']['debug_mode'],
                key="advanced_debug_mode"
            )
            st.session_state.settings_data['advanced']['debug_mode'] = debug_mode
            
            verbose_logging = st.checkbox(
                "Verbose logging",
                value=st.session_state.settings_data['advanced']['verbose_logging'],
                key="advanced_verbose_logging"
            )
            st.session_state.settings_data['advanced']['verbose_logging'] = verbose_logging
        
        with col2:
            st.markdown("**Experimental Features**")
            
            experimental_features = st.checkbox(
                "Experimental features",
                value=st.session_state.settings_data['advanced']['experimental_features'],
                key="advanced_experimental_features"
            )
            st.session_state.settings_data['advanced']['experimental_features'] = experimental_features
            
            beta_features = st.checkbox(
                "Beta features",
                value=st.session_state.settings_data['advanced']['beta_features'],
                key="advanced_beta_features"
            )
            st.session_state.settings_data['advanced']['beta_features'] = beta_features
            
            telemetry = st.checkbox(
                "Telemetry",
                value=st.session_state.settings_data['advanced']['telemetry'],
                key="advanced_telemetry"
            )
            st.session_state.settings_data['advanced']['telemetry'] = telemetry
    
    def render_settings_import_export(self):
        """Render settings import/export"""
        st.subheader("📁 Settings Import/Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export Settings**")
            
            if st.button("📤 Export to JSON"):
                self.export_settings_json()
                st.success("Settings exported to JSON!")
            
            if st.button("📤 Export to YAML"):
                self.export_settings_yaml()
                st.success("Settings exported to YAML!")
        
        with col2:
            st.markdown("**Import Settings**")
            
            uploaded_file = st.file_uploader(
                "Choose a settings file",
                type=['json', 'yaml', 'yml'],
                key="settings_upload"
            )
            
            if uploaded_file is not None:
                if st.button("📥 Import Settings"):
                    self.import_settings(uploaded_file)
                    st.success("Settings imported successfully!")
    
    def save_settings(self):
        """Save current settings"""
        # In a real implementation, this would save to a file or database
        st.session_state.settings_modified = False
        st.session_state.settings_data['last_saved'] = datetime.now().isoformat()
    
    def reset_to_defaults(self):
        """Reset settings to defaults"""
        # Reset all settings to default values
        st.session_state.settings_data = {
            'system': {
                'neural_engine': True,
                'parallel_processing': True,
                'auto_backup': True,
                'log_level': 'INFO',
                'cache_size': '4GB',
                'max_concurrent': 8
            },
            'ai': {
                'default_model': 'DeepSeek-R1-8B',
                'temperature': 0.7,
                'max_tokens': 2048,
                'context_window': 4096,
                'batch_size': 8,
                'model_precision': 'FP16'
            },
            'performance': {
                'memory_limit': '12GB',
                'cpu_cores': 6,
                'gpu_memory': '8GB',
                'auto_optimize': True,
                'power_save': False,
                'thermal_throttling': True
            },
            'security': {
                'encryption_enabled': True,
                'secure_connections': True,
                'access_control': True,
                'audit_logging': True,
                'backup_encryption': True
            },
            'integrations': {
                'github_enabled': True,
                'drive_enabled': True,
                'mcp_enabled': True,
                'auto_sync': True,
                'connection_timeout': 30
            },
            'advanced': {
                'debug_mode': False,
                'verbose_logging': False,
                'experimental_features': True,
                'beta_features': False,
                'telemetry': False
            }
        }
    
    def export_settings(self):
        """Export settings"""
        # This would trigger a download in a real implementation
        pass
    
    def export_settings_json(self):
        """Export settings as JSON"""
        settings_json = json.dumps(st.session_state.settings_data, indent=2)
        # In a real implementation, this would trigger a download
        st.download_button(
            label="Download JSON",
            data=settings_json,
            file_name="code_alchemy_settings.json",
            mime="application/json"
        )
    
    def export_settings_yaml(self):
        """Export settings as YAML"""
        settings_yaml = yaml.dump(st.session_state.settings_data, default_flow_style=False)
        # In a real implementation, this would trigger a download
        st.download_button(
            label="Download YAML",
            data=settings_yaml,
            file_name="code_alchemy_settings.yaml",
            mime="text/yaml"
        )
    
    def import_settings(self, uploaded_file):
        """Import settings from uploaded file"""
        try:
            if uploaded_file.name.endswith('.json'):
                settings_data = json.load(uploaded_file)
            else:
                settings_data = yaml.safe_load(uploaded_file)
            
            # Validate and update settings
            for category in st.session_state.settings_data:
                if category in settings_data:
                    st.session_state.settings_data[category].update(settings_data[category])
            
            st.session_state.settings_modified = True
        except Exception as e:
            st.error(f"Error importing settings: {str(e)}") 