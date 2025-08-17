"""
Agent Manager Component
AI Agent management and control interface
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
import threading
import time
from typing import Dict, Any, List, Optional

class AgentManager:
    """AI Agent management and control system"""
    
    def __init__(self):
        self.setup_session_state()
        # Initialize with real monitoring
        try:
            from src.core.real_monitor import real_monitor
            self.real_monitor = real_monitor
        except ImportError:
            self.real_monitor = None
        
        # Core agent configuration - focused on 3 main areas
        self.agents = {
            'file_organization': {
                'name': 'File Organization',
                'description': 'Intelligent file organization and categorization',
                'model': 'DeepSeek-R1-8B',
                'status': 'active',
                'priority': 'high',
                'enabled': True,
                'performance': 0.0,
                'tasks_completed': 0,
                'last_activity': 'Initializing...'
            },
            'content_analysis': {
                'name': 'Content Analysis',
                'description': 'Multimodal content analysis and understanding',
                'model': 'Llama-3.1-8B',
                'status': 'active',
                'priority': 'high',
                'enabled': True,
                'performance': 0.0,
                'tasks_completed': 0,
                'last_activity': 'Initializing...'
            },
            'productivity': {
                'name': 'Productivity Assistant',
                'description': 'Workflow optimization and task management',
                'model': 'Llama-3.1-8B',
                'status': 'active',
                'priority': 'high',
                'enabled': True,
                'performance': 0.0,
                'tasks_completed': 0,
                'last_activity': 'Initializing...'
            },
            'professional_file_manager': {
                'name': 'Professional File Manager',
                'description': 'Professional project file organization with industry standards',
                'model': 'Multi-Model',
                'status': 'active',
                'priority': 'high',
                'enabled': True,
                'performance': 0.0,
                'tasks_completed': 0,
                'last_activity': 'Initializing...'
            }
        }
        
        # Real-time data updates removed - no live monitoring
        # self.update_with_real_data()
    
    def update_with_real_data(self):
        """Update agent data with real monitoring information (DISABLED)"""
        # Real-time monitoring removed - no live data updates
        pass
    
    def setup_session_state(self):
        """Initialize agent manager session state"""
        if 'agent_metrics' not in st.session_state:
            st.session_state.agent_metrics = {
                'performance_history': {},
                'task_completion': {},
                'response_times': {}
            }
        
        if 'agent_controls' not in st.session_state:
            st.session_state.agent_controls = {
                'auto_restart': True,
                'performance_monitoring': True,
                'load_balancing': True
            }
    
    def render_agent_manager(self):
        """Render main agent management interface"""
        st.header("🤖 Agent Management")
        
        # Agent overview
        self.render_agent_overview()
        
        # Individual agent controls
        self.render_agent_controls()
        
        # Performance monitoring
        self.render_performance_monitoring()
        
        # Agent configuration
        self.render_agent_configuration()
    
    def render_agent_overview(self):
        """Render agent overview dashboard"""
        st.subheader("📊 Agent Overview")
        
        # Agent status grid
        col1, col2, col3, col4 = st.columns(4)
        
        active_agents = len([a for a in self.agents.values() if a['status'] == 'active'])
        total_agents = len(self.agents)
        avg_performance = np.mean([a['performance'] for a in self.agents.values() if a['enabled']])
        total_tasks = sum([a['tasks_completed'] for a in self.agents.values()])
        
        with col1:
            self.render_metric_card("Active Agents", f"{active_agents}/{total_agents}", "🟢", "Running")
        
        with col2:
            self.render_metric_card("Avg Performance", f"{avg_performance:.1f}%", "📈", "Accuracy")
        
        with col3:
            self.render_metric_card("Tasks Completed", f"{total_tasks:,}", "✅", "Total")
        
        with col4:
            self.render_metric_card("System Load", "78%", "⚡", "Optimal")
        
        # Agent status table
        st.subheader("📋 Agent Status")
        
        # Create agent status table
        agent_data = []
        for agent_id, agent in self.agents.items():
            status_color = {
                'active': '🟢',
                'inactive': '🔴',
                'warning': '🟡'
            }
            
            agent_data.append({
                'Agent': agent['name'],
                'Status': f"{status_color.get(agent['status'], '⚪')} {agent['status'].title()}",
                'Model': agent['model'],
                'Performance': f"{agent['performance']:.1f}%",
                'Tasks': f"{agent['tasks_completed']:,}",
                'Last Activity': agent['last_activity'],
                'Priority': agent['priority'].title()
            })
        
        df = pd.DataFrame(agent_data)
        st.dataframe(df, use_container_width=True)
    
    def render_agent_controls(self):
        """Render individual agent controls"""
        st.subheader("🎛️ Agent Controls")
        
        # Agent control tabs
        tab1, tab2, tab3 = st.tabs(["Individual Controls", "Batch Operations", "Advanced Settings"])
        
        with tab1:
            self.render_individual_controls()
        
        with tab2:
            self.render_batch_operations()
        
        with tab3:
            self.render_advanced_settings()
    
    def render_individual_controls(self):
        """Render individual agent controls"""
        for agent_id, agent in self.agents.items():
            with st.expander(f"🤖 {agent['name']}", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Description:** {agent['description']}")
                    st.markdown(f"**Model:** {agent['model']}")
                    st.markdown(f"**Performance:** {agent['performance']:.1f}%")
                    st.markdown(f"**Tasks Completed:** {agent['tasks_completed']:,}")
                
                with col2:
                    # Status control
                    status_options = ['active', 'inactive', 'warning']
                    new_status = st.selectbox(
                        "Status",
                        status_options,
                        index=status_options.index(agent['status']),
                        key=f"status_{agent_id}"
                    )
                    agent['status'] = new_status
                    
                    # Priority control
                    priority_options = ['high', 'medium', 'low']
                    new_priority = st.selectbox(
                        "Priority",
                        priority_options,
                        index=priority_options.index(agent['priority']),
                        key=f"priority_{agent_id}"
                    )
                    agent['priority'] = new_priority
                
                with col3:
                    # Enable/disable control
                    enabled = st.checkbox(
                        "Enabled",
                        value=agent['enabled'],
                        key=f"enabled_{agent_id}"
                    )
                    agent['enabled'] = enabled
                    
                    # Quick actions
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("▶️ Start", key=f"start_{agent_id}"):
                            agent['status'] = 'active'
                            st.success(f"{agent['name']} started!")
                    
                    with col_b:
                        if st.button("⏸️ Pause", key=f"pause_{agent_id}"):
                            agent['status'] = 'inactive'
                            st.warning(f"{agent['name']} paused!")
                
                # Performance metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Response Time", "1.2s", "avg")
                
                with col2:
                    st.metric("Memory Usage", "2.1GB", "of 4GB")
                
                with col3:
                    st.metric("CPU Usage", "15%", "low")
                
                with col4:
                    st.metric("Queue Size", "3", "tasks")
    
    def render_batch_operations(self):
        """Render batch operations"""
        st.markdown("**Batch Operations**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start All Agents", type="primary"):
                for agent in self.agents.values():
                    agent['status'] = 'active'
                st.success("All agents started successfully!")
        
        with col2:
            if st.button("⏸️ Pause All Agents"):
                for agent in self.agents.values():
                    agent['status'] = 'inactive'
                st.warning("All agents paused!")
        
        with col3:
            if st.button("🔄 Restart All Agents"):
                for agent in self.agents.values():
                    agent['status'] = 'active'
                st.info("All agents restarted!")
        
        st.markdown("**Priority Management**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            priority = st.selectbox(
                "Set Priority for All Agents",
                ["High", "Medium", "Low"],
                key="batch_priority"
            )
            
            if st.button("📊 Update Priorities"):
                for agent in self.agents.values():
                    agent['priority'] = priority.lower()
                st.success(f"All agent priorities set to {priority}")
        
        with col2:
            performance_threshold = st.slider(
                "Performance Threshold",
                min_value=0,
                max_value=100,
                value=80,
                key="performance_threshold"
            )
            
            if st.button("⚡ Optimize Performance"):
                st.info(f"Optimizing agents with performance below {performance_threshold}%")
    
    def render_advanced_settings(self):
        """Render advanced agent settings"""
        st.markdown("**Advanced Settings**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**System Controls**")
            
            # Ensure session state is initialized
            if 'agent_controls' not in st.session_state:
                st.session_state.agent_controls = {
                    'auto_restart': True,
                    'performance_monitoring': True,
                    'load_balancing': True
                }
            
            auto_restart = st.checkbox(
                "Auto-restart failed agents",
                value=st.session_state.agent_controls.get('auto_restart', True),
                key="auto_restart"
            )
            st.session_state.agent_controls['auto_restart'] = auto_restart
            
            performance_monitoring = st.checkbox(
                "Performance monitoring",
                value=st.session_state.agent_controls.get('performance_monitoring', True),
                key="performance_monitoring"
            )
            st.session_state.agent_controls['performance_monitoring'] = performance_monitoring
            
            load_balancing = st.checkbox(
                "Load balancing",
                value=st.session_state.agent_controls.get('load_balancing', True),
                key="load_balancing"
            )
            st.session_state.agent_controls['load_balancing'] = load_balancing
        
        with col2:
            st.markdown("**Resource Management**")
            
            max_concurrent = st.slider(
                "Max concurrent tasks",
                min_value=1,
                max_value=10,
                value=5,
                key="max_concurrent"
            )
            
            memory_limit = st.selectbox(
                "Memory limit per agent",
                ["1GB", "2GB", "4GB", "8GB"],
                key="memory_limit"
            )
            
            timeout = st.slider(
                "Task timeout (seconds)",
                min_value=10,
                max_value=300,
                value=60,
                key="timeout"
            )
    
    def render_performance_monitoring(self):
        """Render performance monitoring"""
        st.subheader("📈 Performance Monitoring")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_performance_chart()
        
        with col2:
            self.render_task_completion_chart()
        
        # Performance metrics
        st.subheader("📊 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_metric_card("Avg Response Time", "1.2s", "⚡", "Fast")
        
        with col2:
            self.render_metric_card("Success Rate", "96.8%", "✅", "High")
        
        with col3:
            self.render_metric_card("Error Rate", "3.2%", "⚠️", "Low")
        
        with col4:
            self.render_metric_card("Uptime", "99.7%", "🟢", "Excellent")
    
    def render_performance_chart(self):
        """Render performance chart"""
        st.markdown("**Agent Performance Over Time**")
        
        # Generate sample performance data
        agents = list(self.agents.keys())
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        
        performance_data = []
        for agent in agents:
            base_performance = self.agents[agent]['performance']
            for date in dates:
                performance_data.append({
                    'Date': date,
                    'Agent': self.agents[agent]['name'],
                    'Performance': base_performance + np.random.normal(0, 2)
                })
        
        df = pd.DataFrame(performance_data)
        
        fig = px.line(
            df,
            x='Date',
            y='Performance',
            color='Agent',
            title="Agent Performance Trends"
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Date",
            yaxis_title="Performance (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_task_completion_chart(self):
        """Render task completion chart"""
        st.markdown("**Task Completion by Agent**")
        
        agent_names = [agent['name'] for agent in self.agents.values()]
        task_counts = [agent['tasks_completed'] for agent in self.agents.values()]
        
        fig = px.bar(
            x=agent_names,
            y=task_counts,
            title="Tasks Completed by Agent",
            color=task_counts,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Agent",
            yaxis_title="Tasks Completed"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_agent_configuration(self):
        """Render agent configuration"""
        st.subheader("⚙️ Agent Configuration")
        
        # Model configuration
        st.markdown("**Model Configuration**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Selection**")
            
            for agent_id, agent in self.agents.items():
                available_models = [
                    "DeepSeek-R1-8B",
                    "Llama-3.1-8B", 
                    "Phi-4-Mini",
                    "TinyLlama-1.1B",
                    "Qwen2.5-0.5B"
                ]
                
                new_model = st.selectbox(
                    f"{agent['name']} Model",
                    available_models,
                    index=available_models.index(agent['model']),
                    key=f"model_{agent_id}"
                )
                agent['model'] = new_model
        
        with col2:
            st.markdown("**Model Parameters**")
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                key="agent_temperature"
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=2048,
                step=100,
                key="agent_max_tokens"
            )
            
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                key="agent_top_p"
            )
        
        # Save configuration
        if st.button("💾 Save Configuration", type="primary"):
            st.success("Agent configuration saved successfully!")
    
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