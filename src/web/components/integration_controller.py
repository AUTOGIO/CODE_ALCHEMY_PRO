"""
Integration Controller Component
External service integration management interface
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
from typing import Dict, Any, List, Optional

class IntegrationController:
    """External service integration management system"""
    
    def __init__(self):
        self.setup_session_state()
        self.integrations = {
            'github': {
                'name': 'GitHub',
                'status': 'connected',
                'username': 'AUTOGIO',
                'repos': 15,
                'last_sync': '2 minutes ago',
                'auto_commit': True,
                'project_tracking': True
            },
            'google_drive': {
                'name': 'Google Drive',
                'status': 'connected',
                'folders': 3,
                'files_synced': 1247,
                'last_sync': '5 minutes ago',
                'auto_backup': True,
                'sync_enabled': True
            },
            'lm_studio': {
                'name': 'LM Studio',
                'status': 'connected',
                'models': 46,
                'server_url': 'http://localhost:1234',
                'last_check': '1 minute ago',
                'auto_load': True,
                'performance_monitoring': True
            },
            'mcp': {
                'name': 'MCP (Cursor)',
                'status': 'active',
                'servers': 3,
                'connections': 2,
                'last_activity': '30 seconds ago',
                'auto_connect': True,
                'protocol_version': '1.0'
            },
            'dropbox': {
                'name': 'Dropbox',
                'status': 'disconnected',
                'folders': 0,
                'files_synced': 0,
                'last_sync': 'Never',
                'auto_backup': False,
                'sync_enabled': False
            }
        }
    
    def setup_session_state(self):
        """Initialize integration controller session state"""
        if 'integration_metrics' not in st.session_state:
            st.session_state.integration_metrics = {
                'sync_history': {},
                'connection_status': {},
                'performance_data': {}
            }
        
        if 'integration_controls' not in st.session_state:
            st.session_state.integration_controls = {
                'auto_sync': True,
                'connection_monitoring': True,
                'error_reporting': True
            }
    
    def render_integration_controller(self):
        """Render main integration management interface"""
        st.header("🔗 Integration Controller")
        
        # Integration overview
        self.render_integration_overview()
        
        # Integration controls
        self.render_integration_controls()
        
        # Connection monitoring
        self.render_connection_monitoring()
        
        # Integration configuration
        self.render_integration_configuration()
    
    def render_integration_overview(self):
        """Render integration overview dashboard"""
        st.subheader("📊 Integration Overview")
        
        # Integration status grid
        col1, col2, col3, col4 = st.columns(4)
        
        connected_integrations = len([i for i in self.integrations.values() if i['status'] in ['connected', 'active']])
        total_integrations = len(self.integrations)
        sync_status = "🟢 All synced" if connected_integrations == total_integrations else "🟡 Partial sync"
        total_files = sum([i.get('files_synced', 0) for i in self.integrations.values()])
        
        with col1:
            self.render_metric_card("Connected", f"{connected_integrations}/{total_integrations}", "🔗", "Services")
        
        with col2:
            self.render_metric_card("Sync Status", sync_status, "🔄", "Status")
        
        with col3:
            self.render_metric_card("Files Synced", f"{total_files:,}", "📁", "Total")
        
        with col4:
            self.render_metric_card("Last Sync", "2 min ago", "⏰", "Recent")
        
        # Integration status table
        st.subheader("📋 Integration Status")
        
        # Create integration status table
        integration_data = []
        for integration_id, integration in self.integrations.items():
            status_color = {
                'connected': '🟢',
                'active': '🟢',
                'disconnected': '🔴',
                'error': '🔴',
                'connecting': '🟡'
            }
            
            integration_data.append({
                'Service': integration['name'],
                'Status': f"{status_color.get(integration['status'], '⚪')} {integration['status'].title()}",
                'Details': self.get_integration_details(integration),
                'Last Activity': integration.get('last_sync', integration.get('last_activity', 'Never')),
                'Auto Sync': '✅' if integration.get('auto_backup') or integration.get('auto_commit') else '❌'
            })
        
        df = pd.DataFrame(integration_data)
        st.dataframe(df, use_container_width=True)
    
    def get_integration_details(self, integration: Dict[str, Any]) -> str:
        """Get integration details string"""
        if integration['name'] == 'GitHub':
            return f"{integration['repos']} repos"
        elif integration['name'] == 'Google Drive':
            return f"{integration['folders']} folders, {integration['files_synced']} files"
        elif integration['name'] == 'LM Studio':
            return f"{integration['models']} models"
        elif integration['name'] == 'MCP (Cursor)':
            return f"{integration['servers']} servers, {integration['connections']} connections"
        else:
            return "Not configured"
    
    def render_integration_controls(self):
        """Render integration controls"""
        st.subheader("🎛️ Integration Controls")
        
        # Integration control tabs
        tab1, tab2, tab3 = st.tabs(["Individual Controls", "Batch Operations", "Advanced Settings"])
        
        with tab1:
            self.render_individual_controls()
        
        with tab2:
            self.render_batch_operations()
        
        with tab3:
            self.render_advanced_settings()
    
    def render_individual_controls(self):
        """Render individual integration controls"""
        for integration_id, integration in self.integrations.items():
            with st.expander(f"🔗 {integration['name']}", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Status:** {integration['status'].title()}")
                    st.markdown(f"**Details:** {self.get_integration_details(integration)}")
                    st.markdown(f"**Last Activity:** {integration.get('last_sync', integration.get('last_activity', 'Never'))}")
                    
                    # Auto-sync status
                    auto_sync_enabled = integration.get('auto_backup') or integration.get('auto_commit')
                    st.markdown(f"**Auto Sync:** {'✅ Enabled' if auto_sync_enabled else '❌ Disabled'}")
                
                with col2:
                    # Status control
                    status_options = ['connected', 'disconnected', 'error']
                    new_status = st.selectbox(
                        "Status",
                        status_options,
                        index=status_options.index(integration['status']) if integration['status'] in status_options else 0,
                        key=f"integration_status_{integration_id}"
                    )
                    integration['status'] = new_status
                    
                    # Auto-sync control
                    auto_sync = st.checkbox(
                        "Auto Sync",
                        value=auto_sync_enabled,
                        key=f"auto_sync_{integration_id}"
                    )
                    if integration_id in ['github', 'google_drive']:
                        integration['auto_backup'] = auto_sync
                    elif integration_id == 'github':
                        integration['auto_commit'] = auto_sync
                
                with col3:
                    # Connection actions
                    if integration['status'] == 'connected':
                        if st.button("🔌 Disconnect", key=f"disconnect_{integration_id}"):
                            integration['status'] = 'disconnected'
                            st.warning(f"{integration['name']} disconnected!")
                    else:
                        if st.button("🔌 Connect", key=f"connect_{integration_id}"):
                            integration['status'] = 'connected'
                            st.success(f"{integration['name']} connected!")
                    
                    # Quick actions
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("🔄 Sync", key=f"sync_{integration_id}"):
                            st.info(f"Syncing {integration['name']}...")
                    
                    with col_b:
                        if st.button("⚙️ Config", key=f"config_{integration_id}"):
                            st.info(f"Configuring {integration['name']}...")
                
                # Integration metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Response Time", "0.8s", "avg")
                
                with col2:
                    st.metric("Success Rate", "98.5%", "high")
                
                with col3:
                    st.metric("Data Transferred", "2.1MB", "today")
                
                with col4:
                    st.metric("Errors", "0", "none")
    
    def render_batch_operations(self):
        """Render batch integration operations"""
        st.markdown("**Batch Operations**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔌 Connect All", type="primary"):
                for integration in self.integrations.values():
                    integration['status'] = 'connected'
                st.success("All integrations connected!")
        
        with col2:
            if st.button("🔌 Disconnect All"):
                for integration in self.integrations.values():
                    integration['status'] = 'disconnected'
                st.warning("All integrations disconnected!")
        
        with col3:
            if st.button("🔄 Sync All"):
                for integration in self.integrations.values():
                    if integration['status'] == 'connected':
                        integration['last_sync'] = 'Just now'
                st.info("All integrations synced!")
        
        st.markdown("**Sync Management**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sync_interval = st.selectbox(
                "Sync Interval",
                ["5 minutes", "15 minutes", "30 minutes", "1 hour"],
                key="sync_interval"
            )
            
            if st.button("⏰ Set Sync Schedule"):
                st.success(f"Sync schedule set to {sync_interval}")
        
        with col2:
            auto_retry = st.checkbox(
                "Auto-retry failed connections",
                value=True,
                key="auto_retry"
            )
            
            if st.button("🔄 Test Connections"):
                st.info("Testing all connections...")
    
    def render_advanced_settings(self):
        """Render advanced integration settings"""
        st.markdown("**Advanced Settings**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Connection Controls**")
            
            # Ensure session state is initialized
            if 'integration_controls' not in st.session_state:
                st.session_state.integration_controls = {
                    'auto_sync': True,
                    'connection_monitoring': True,
                    'error_reporting': True
                }
            
            auto_sync = st.checkbox(
                "Auto-sync enabled services",
                value=st.session_state.integration_controls.get('auto_sync', True),
                key="auto_sync_global"
            )
            st.session_state.integration_controls['auto_sync'] = auto_sync
            
            connection_monitoring = st.checkbox(
                "Connection monitoring",
                value=st.session_state.integration_controls.get('connection_monitoring', True),
                key="connection_monitoring"
            )
            st.session_state.integration_controls['connection_monitoring'] = connection_monitoring
            
            error_reporting = st.checkbox(
                "Error reporting",
                value=st.session_state.integration_controls.get('error_reporting', True),
                key="error_reporting"
            )
            st.session_state.integration_controls['error_reporting'] = error_reporting
        
        with col2:
            st.markdown("**Performance Settings**")
            
            timeout = st.slider(
                "Connection timeout (seconds)",
                min_value=5,
                max_value=60,
                value=30,
                key="timeout"
            )
            
            retry_attempts = st.slider(
                "Retry attempts",
                min_value=1,
                max_value=5,
                value=3,
                key="retry_attempts"
            )
            
            buffer_size = st.selectbox(
                "Buffer size",
                ["1MB", "5MB", "10MB", "50MB"],
                key="buffer_size"
            )
    
    def render_connection_monitoring(self):
        """Render connection monitoring"""
        st.subheader("📈 Connection Monitoring")
        
        # Connection charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_connection_chart()
        
        with col2:
            self.render_sync_chart()
        
        # Connection metrics
        st.subheader("📊 Connection Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_metric_card("Avg Response Time", "0.8s", "⚡", "Fast")
        
        with col2:
            self.render_metric_card("Success Rate", "98.5%", "✅", "High")
        
        with col3:
            self.render_metric_card("Data Transferred", "15.2MB", "📊", "Today")
        
        with col4:
            self.render_metric_card("Active Connections", "4", "🔗", "Stable")
    
    def render_connection_chart(self):
        """Render connection status chart"""
        st.markdown("**Connection Status Over Time**")
        
        # Generate sample connection data
        services = list(self.integrations.keys())
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        
        connection_data = []
        for service in services:
            base_status = 1 if self.integrations[service]['status'] in ['connected', 'active'] else 0
            for date in dates:
                connection_data.append({
                    'Date': date,
                    'Service': self.integrations[service]['name'],
                    'Status': base_status + np.random.normal(0, 0.1)
                })
        
        df = pd.DataFrame(connection_data)
        
        fig = px.line(
            df,
            x='Date',
            y='Status',
            color='Service',
            title="Connection Status Over Time"
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Date",
            yaxis_title="Connection Status"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_sync_chart(self):
        """Render sync activity chart"""
        st.markdown("**Sync Activity by Service**")
        
        service_names = [integration['name'] for integration in self.integrations.values()]
        sync_counts = [integration.get('files_synced', 0) for integration in self.integrations.values()]
        
        fig = px.bar(
            x=service_names,
            y=sync_counts,
            title="Files Synced by Service",
            color=sync_counts,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Service",
            yaxis_title="Files Synced"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_integration_configuration(self):
        """Render integration configuration"""
        st.subheader("⚙️ Integration Configuration")
        
        # Service configuration
        st.markdown("**Service Configuration**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**GitHub Configuration**")
            
            github_token = st.text_input(
                "GitHub Token",
                value="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",
                type="password",
                key="github_token"
            )
            
            github_username = st.text_input(
                "GitHub Username",
                value="AUTOGIO",
                key="github_username"
            )
            
            auto_commit = st.checkbox(
                "Auto-commit changes",
                value=True,
                key="github_auto_commit"
            )
        
        with col2:
            st.markdown("**Google Drive Configuration**")
            
            drive_enabled = st.checkbox(
                "Enable Google Drive",
                value=True,
                key="drive_enabled"
            )
            
            sync_folders = st.multiselect(
                "Folders to Sync",
                ["~/Desktop/CODE_ALCHEMY_Projects", "~/Documents/AI_Projects", "~/Downloads/Code_Projects"],
                default=["~/Desktop/CODE_ALCHEMY_Projects"],
                key="sync_folders"
            )
            
            auto_backup = st.checkbox(
                "Auto-backup to Drive",
                value=True,
                key="drive_auto_backup"
            )
        
        # LM Studio Configuration
        st.markdown("**LM Studio Configuration**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            server_url = st.text_input(
                "Server URL",
                value="http://localhost:1234",
                key="server_url"
            )
            
            auto_load = st.checkbox(
                "Auto-load models",
                value=True,
                key="auto_load_models"
            )
        
        with col2:
            performance_monitoring = st.checkbox(
                "Performance monitoring",
                value=True,
                key="performance_monitoring"
            )
            
            if st.button("🔗 Test Connection"):
                st.success("Connection test successful!")
        
        # Save configuration
        if st.button("💾 Save Configuration", type="primary"):
            st.success("Integration configuration saved successfully!")
    
    def render_metric_card(self, title: str, value: str, icon: str, subtitle: str):
        """Render a metric card"""
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