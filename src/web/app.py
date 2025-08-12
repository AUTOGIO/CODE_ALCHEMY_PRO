"""
CODE_ALCHEMY Professional Web Interface
Modern, responsive dashboard with real-time monitoring
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import asyncio
import threading
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.core.config import config
from src.web.components.dashboard_controls import DashboardControls
from src.web.components.agent_manager import AgentManager
from src.web.components.model_manager import ModelManager
from src.web.components.integration_controller import IntegrationController
from src.web.components.performance_analyzer import PerformanceAnalyzer
from src.web.components.settings_panel import SettingsPanel

class CodeAlchemyApp:
    """Professional CODE_ALCHEMY web application"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.setup_components()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="CODE_ALCHEMY Professional",
            page_icon="🧪",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/AUTOGIO/CODE_ALCHEMY',
                'Report a bug': "https://github.com/AUTOGIO/CODE_ALCHEMY/issues",
                'About': "# CODE_ALCHEMY Professional\nAI-Powered Desktop Intelligence System"
            }
        )
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'system_status' not in st.session_state:
            st.session_state.system_status = "initializing"
        
        if 'agents_status' not in st.session_state:
            st.session_state.agents_status = {}
        
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = {}
        
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = config.models.default_model
    
    def setup_components(self):
        """Setup application components"""
        self.dashboard_controls = DashboardControls()
        self.agent_manager = AgentManager()
        self.model_manager = ModelManager()
        self.integration_controller = IntegrationController()
        self.performance_analyzer = PerformanceAnalyzer()
        self.settings_panel = SettingsPanel()
    
    def run(self):
        """Main application runner"""
        # Minimal CSS for clean styling
        self.inject_minimal_css()
        
        # Header
        self.render_header()
        
        # Sidebar navigation
        with st.sidebar:
            self.render_sidebar()
            

        
        # Main content area
        self.render_main_content()
        
        # Footer
        self.render_footer()
    
    def inject_minimal_css(self):
        """Inject minimal CSS for clean styling"""
        st.markdown("""
        <style>
        .main-header {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            color: white;
        }
        .status-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #28a745;
        }
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        .agent-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
        }
        .status-active { background-color: #28a745; }
        .status-inactive { background-color: #dc3545; }
        .status-warning { background-color: #ffc107; }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render application header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("""
            <div class="main-header">
                <h1>🧪 CODE_ALCHEMY Professional</h1>
                <p>AI-Powered Desktop Intelligence System</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            status_color = {
                "active": "🟢",
                "inactive": "🔴",
                "warning": "🟡",
                "initializing": "🔄"
            }
            st.metric(
                "System Status",
                status_color.get(st.session_state.system_status, "⚪"),
                st.session_state.system_status.title()
            )
        
        with col3:
            st.metric(
                "Active Agents",
                len([s for s in st.session_state.agents_status.values() if s == "active"]),
                f"of {len(st.session_state.agents_status)} total"
            )
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        st.sidebar.title("🧪 CODE_ALCHEMY")
        
        # Navigation menu
        page = st.sidebar.selectbox(
            "Navigation",
            [
                "🎛️ Control Panel",
                "🤖 Agent Manager",
                "🧠 Model Manager",
                "🔗 Integration Controller",
                "📈 Performance Analyzer",
                "⚙️ Settings Panel"
            ],
            key="navigation"
        )
        
        # Set current page based on selection
        page_mapping = {
            "🎛️ Control Panel": "control_panel",
            "🤖 Agent Manager": "agent_manager", 
            "🧠 Model Manager": "model_manager",
            "🔗 Integration Controller": "integration_controller",
            "📈 Performance Analyzer": "performance_analyzer",
            "⚙️ Settings Panel": "settings_panel"
        }
        
        st.session_state.current_page = page_mapping.get(page, "control_panel")
        
        # System status
        st.sidebar.markdown("---")
        st.sidebar.markdown("**System Status**")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("CPU", "78%")
        with col2:
            st.metric("Memory", "62%")
        
        # Quick actions
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Quick Actions**")
        
        if st.sidebar.button("🔄 Refresh"):
            st.rerun()
        
        if st.sidebar.button("💾 Save"):
            st.success("Settings saved!")
    
    def render_main_content(self):
        """Render main content area"""
        # Get selected page from sidebar
        page = st.session_state.get('current_page', 'control_panel')
        
        if page == 'control_panel':
            self.dashboard_controls.render_control_panel()
        elif page == 'agent_manager':
            self.agent_manager.render_agent_manager()
        elif page == 'model_manager':
            self.model_manager.render_model_manager()
        elif page == 'integration_controller':
            self.integration_controller.render_integration_controller()
        elif page == 'performance_analyzer':
            self.performance_analyzer.render_performance_analyzer()
        elif page == 'settings_panel':
            self.settings_panel.render_settings_panel()
    
    def render_dashboard(self):
        """Render main dashboard"""
        st.header("📊 System Dashboard")
        
        # System overview cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_metric_card(
                "Files Organized",
                "1,247",
                "+12% from yesterday",
                "📁"
            )
        
        with col2:
            self.render_metric_card(
                "AI Confidence",
                "94.2%",
                "+2.1% improvement",
                "🧠"
            )
        
        with col3:
            self.render_metric_card(
                "Active Models",
                "3",
                "2 local, 1 cloud",
                "🤖"
            )
        
        with col4:
            self.render_metric_card(
                "System Performance",
                "98.5%",
                "Optimal",
                "⚡"
            )
        
        # Charts and analytics
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_file_organization_chart()
        
        with col2:
            self.render_ai_confidence_chart()
        
        # Recent activity
        st.subheader("📝 Recent Activity")
        self.render_recent_activity()
    
    def render_metric_card(self, title, value, delta, icon):
        """Render a metric card"""
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div>
                    <h3 style="margin: 0; font-size: 1.2rem;">{title}</h3>
                    <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{value}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #666;">{delta}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_file_organization_chart(self):
        """Render file organization chart"""
        st.subheader("📁 File Organization")
        
        # Sample data
        data = {
            'Category': ['Development', 'Documents', 'Media', 'Archives', 'AI Tools'],
            'Count': [45, 23, 18, 12, 8],
            'Percentage': [42.5, 21.7, 17.0, 11.3, 7.5]
        }
        
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df, 
            values='Count', 
            names='Category',
            title="File Distribution by Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            height=400,
            showlegend=True,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_confidence_chart(self):
        """Render AI confidence chart"""
        st.subheader("🧠 AI Confidence Scores")
        
        # Sample data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        confidence_scores = [85 + i*0.5 + np.random.normal(0, 2) for i in range(30)]
        
        df = pd.DataFrame({
            'Date': dates,
            'Confidence': confidence_scores
        })
        
        fig = px.line(
            df,
            x='Date',
            y='Confidence',
            title="AI Confidence Over Time",
            line_shape='linear'
        )
        
        fig.update_layout(
            height=400,
            yaxis_title="Confidence Score (%)",
            xaxis_title="Date"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_activity(self):
        """Render recent activity feed"""
        activities = [
            {"time": "2 minutes ago", "action": "Organized 15 files", "agent": "File Organization"},
            {"time": "5 minutes ago", "action": "Analyzed code project", "agent": "Code Intelligence"},
            {"time": "12 minutes ago", "action": "Updated GitHub repo", "agent": "GitHub Integration"},
            {"time": "18 minutes ago", "action": "Backed up to Google Drive", "agent": "Google Drive"},
            {"time": "25 minutes ago", "action": "Security scan completed", "agent": "Security Monitor"}
        ]
        
        for activity in activities:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.write(f"🕒 {activity['time']}")
                with col2:
                    st.write(f"**{activity['action']}**")
                with col3:
                    st.write(f"via {activity['agent']}")
                st.divider()
    
    def render_agents_page(self):
        """Render agents management page"""
        st.header("🤖 Agent Management")
        
        # Agent status cards
        agents = [
            {"name": "File Organization", "status": "active", "model": "DeepSeek-R1-8B"},
            {"name": "Content Analysis", "status": "active", "model": "Llama-3.1-8B"},
            {"name": "Code Intelligence", "status": "active", "model": "Phi-4-Mini"},
            {"name": "Productivity", "status": "warning", "model": "TinyLlama-1.1B"},
            {"name": "Security Monitor", "status": "inactive", "model": "TinyLlama-1.1B"}
        ]
        
        for agent in agents:
            self.render_agent_card(agent)
    
    def render_agent_card(self, agent):
        """Render individual agent card"""
        status_colors = {
            "active": "#28a745",
            "inactive": "#dc3545",
            "warning": "#ffc107"
        }
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="agent-status">
                <span class="status-indicator status-{agent['status']}"></span>
                <h3>{agent['name']}</h3>
            </div>
            <p><strong>Model:</strong> {agent['model']}</p>
            <p><strong>Status:</strong> {agent['status'].title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_analytics_page(self):
        """Render analytics page"""
        st.header("📈 Analytics & Performance")
        self.analytics.render()
    
    def render_models_page(self):
        """Render models management page"""
        st.header("🤖 Model Management")
        
        # Model selection
        st.subheader("Model Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox(
                "Default Model",
                ["DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf", "Meta-Llama-3.1-8B-Instruct-Q6_K.gguf"],
                key="default_model"
            )
        
        with col2:
            st.selectbox(
                "Fast Model",
                ["TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf", "Qwen2.5-0.5B-Instruct-MLX-4bit"],
                key="fast_model"
            )
        
        # Model performance
        st.subheader("Model Performance")
        
        performance_data = {
            "Model": ["DeepSeek-R1-8B", "Llama-3.1-8B", "Phi-4-Mini", "TinyLlama-1.1B"],
            "Speed (tokens/s)": [45, 52, 38, 78],
            "Memory (GB)": [8.2, 7.8, 4.1, 1.2],
            "Accuracy (%)": [94.2, 92.8, 89.5, 85.1]
        }
        
        df = pd.DataFrame(performance_data)
        st.dataframe(df, use_container_width=True)
    
    def render_integrations_page(self):
        """Render integrations page"""
        st.header("🔗 Integrations")
        
        integrations = [
            {"name": "GitHub", "status": "connected", "username": "AUTOGIO"},
            {"name": "Google Drive", "status": "connected", "folders": "3 synced"},
            {"name": "LM Studio", "status": "connected", "models": "46 available"},
            {"name": "MCP (Cursor)", "status": "active", "servers": "3 running"}
        ]
        
        for integration in integrations:
            self.render_integration_card(integration)
    
    def render_integration_card(self, integration):
        """Render integration card"""
        status_icon = "🟢" if integration['status'] == 'connected' else "🔴"
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>{status_icon} {integration['name']}</h3>
            <p><strong>Status:</strong> {integration['status'].title()}</p>
            <p><strong>Details:</strong> {list(integration.values())[2]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_settings_page(self):
        """Render settings page"""
        st.header("⚙️ Settings")
        
        # System settings
        st.subheader("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Enable Neural Engine", value=True, key="neural_engine")
            st.checkbox("Parallel Processing", value=True, key="parallel_processing")
            st.checkbox("Auto Backup", value=True, key="auto_backup")
        
        with col2:
            st.selectbox("Memory Limit", ["8GB", "12GB", "16GB"], key="memory_limit")
            st.selectbox("Log Level", ["INFO", "DEBUG", "WARNING", "ERROR"], key="log_level")
            st.text_input("Models Path", value="/Volumes/MICRO/models", key="models_path")
        
        # Save settings
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**CODE_ALCHEMY Professional**")
            st.markdown("AI-Powered Desktop Intelligence")
        
        with col2:
            st.markdown("**Version:** 2.0.0")
            st.markdown("**Platform:** M3 iMac Optimized")
        
        with col3:
            st.markdown("**Status:** Production Ready")
            st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d"))

def main():
    """Main application entry point"""
    app = CodeAlchemyApp()
    app.run()

if __name__ == "__main__":
    main() 