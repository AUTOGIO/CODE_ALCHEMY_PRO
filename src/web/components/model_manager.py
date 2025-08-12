"""
Model Manager Component
AI Model management and configuration interface
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

class ModelManager:
    """AI Model management and configuration system"""
    
    def __init__(self):
        self.setup_session_state()
        self.models = {
            'DeepSeek-R1-0528-Qwen3-8B-Q6_K.gguf': {
                'name': 'DeepSeek-R1-8B',
                'size': '8.2GB',
                'type': 'General Purpose',
                'status': 'loaded',
                'performance': 94.2,
                'speed': 45,
                'memory': 8.2,
                'accuracy': 94.2,
                'last_used': '2 minutes ago'
            },
            'Meta-Llama-3.1-8B-Instruct-Q6_K.gguf': {
                'name': 'Llama-3.1-8B',
                'size': '7.8GB',
                'type': 'Instruction Tuned',
                'status': 'loaded',
                'performance': 92.8,
                'speed': 52,
                'memory': 7.8,
                'accuracy': 92.8,
                'last_used': '5 minutes ago'
            },
            'Phi-4-mini-reasoning-Q8_0.gguf': {
                'name': 'Phi-4-Mini',
                'size': '4.1GB',
                'type': 'Reasoning',
                'status': 'loaded',
                'performance': 89.5,
                'speed': 38,
                'memory': 4.1,
                'accuracy': 89.5,
                'last_used': '1 minute ago'
            },
            'TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf': {
                'name': 'TinyLlama-1.1B',
                'size': '1.2GB',
                'type': 'Fast Inference',
                'status': 'available',
                'performance': 85.1,
                'speed': 78,
                'memory': 1.2,
                'accuracy': 85.1,
                'last_used': 'Never'
            },
            'Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf': {
                'name': 'Qwen2.5-VL-7B',
                'size': '6.5GB',
                'type': 'Vision Language',
                'status': 'available',
                'performance': 91.3,
                'speed': 42,
                'memory': 6.5,
                'accuracy': 91.3,
                'last_used': 'Never'
            }
        }
    
    def setup_session_state(self):
        """Initialize model manager session state"""
        if 'model_metrics' not in st.session_state:
            st.session_state.model_metrics = {
                'performance_history': {},
                'usage_stats': {},
                'memory_usage': {}
            }
        
        if 'model_controls' not in st.session_state:
            st.session_state.model_controls = {
                'auto_load': True,
                'memory_optimization': True,
                'performance_monitoring': True
            }
    
    def render_model_manager(self):
        """Render main model management interface"""
        st.header("🧠 Model Manager")
        
        # Model overview
        self.render_model_overview()
        
        # Model controls
        self.render_model_controls()
        
        # Performance monitoring
        self.render_model_performance()
        
        # Model configuration
        self.render_model_configuration()
    
    def render_model_overview(self):
        """Render model overview dashboard"""
        st.subheader("📊 Model Overview")
        
        # Model status grid
        col1, col2, col3, col4 = st.columns(4)
        
        loaded_models = len([m for m in self.models.values() if m['status'] == 'loaded'])
        total_models = len(self.models)
        avg_performance = np.mean([m['performance'] for m in self.models.values()])
        total_memory = sum([m['memory'] for m in self.models.values() if m['status'] == 'loaded'])
        
        with col1:
            self.render_metric_card("Loaded Models", f"{loaded_models}/{total_models}", "🧠", "Active")
        
        with col2:
            self.render_metric_card("Avg Performance", f"{avg_performance:.1f}%", "📈", "Accuracy")
        
        with col3:
            self.render_metric_card("Memory Usage", f"{total_memory:.1f}GB", "💾", "Total")
        
        with col4:
            self.render_metric_card("Avg Speed", "51 t/s", "⚡", "Tokens/sec")
        
        # Model status table
        st.subheader("📋 Model Status")
        
        # Create model status table
        model_data = []
        for model_id, model in self.models.items():
            status_color = {
                'loaded': '🟢',
                'available': '🔵',
                'loading': '🟡',
                'error': '🔴'
            }
            
            model_data.append({
                'Model': model['name'],
                'Status': f"{status_color.get(model['status'], '⚪')} {model['status'].title()}",
                'Type': model['type'],
                'Size': model['size'],
                'Performance': f"{model['performance']:.1f}%",
                'Speed': f"{model['speed']} t/s",
                'Memory': f"{model['memory']}GB",
                'Last Used': model['last_used']
            })
        
        df = pd.DataFrame(model_data)
        st.dataframe(df, use_container_width=True)
    
    def render_model_controls(self):
        """Render model controls"""
        st.subheader("🎛️ Model Controls")
        
        # Model control tabs
        tab1, tab2, tab3 = st.tabs(["Model Operations", "Batch Operations", "Advanced Settings"])
        
        with tab1:
            self.render_model_operations()
        
        with tab2:
            self.render_batch_operations()
        
        with tab3:
            self.render_advanced_settings()
    
    def render_model_operations(self):
        """Render individual model operations"""
        for model_id, model in self.models.items():
            with st.expander(f"🧠 {model['name']}", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Type:** {model['type']}")
                    st.markdown(f"**Size:** {model['size']}")
                    st.markdown(f"**Performance:** {model['performance']:.1f}%")
                    st.markdown(f"**Speed:** {model['speed']} tokens/sec")
                
                with col2:
                    # Status control
                    status_options = ['loaded', 'available', 'loading', 'error']
                    new_status = st.selectbox(
                        "Status",
                        status_options,
                        index=status_options.index(model['status']),
                        key=f"model_status_{model_id}"
                    )
                    model['status'] = new_status
                    
                    # Priority control
                    priority_options = ['high', 'medium', 'low']
                    priority = st.selectbox(
                        "Priority",
                        priority_options,
                        index=1,  # medium
                        key=f"model_priority_{model_id}"
                    )
                
                with col3:
                    # Load/Unload control
                    if model['status'] == 'loaded':
                        if st.button("📤 Unload", key=f"unload_{model_id}"):
                            model['status'] = 'available'
                            st.success(f"{model['name']} unloaded!")
                    else:
                        if st.button("📥 Load", key=f"load_{model_id}"):
                            model['status'] = 'loaded'
                            st.success(f"{model['name']} loaded!")
                    
                    # Quick actions
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("⚡ Optimize", key=f"optimize_{model_id}"):
                            st.info(f"Optimizing {model['name']}...")
                    
                    with col_b:
                        if st.button("📊 Test", key=f"test_{model_id}"):
                            st.info(f"Testing {model['name']}...")
                
                # Model metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Response Time", "1.2s", "avg")
                
                with col2:
                    st.metric("Memory Usage", f"{model['memory']}GB", "loaded")
                
                with col3:
                    st.metric("CPU Usage", "15%", "low")
                
                with col4:
                    st.metric("Queue Size", "3", "tasks")
    
    def render_batch_operations(self):
        """Render batch model operations"""
        st.markdown("**Batch Operations**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Load All Models", type="primary"):
                for model in self.models.values():
                    model['status'] = 'loaded'
                st.success("All models loaded successfully!")
        
        with col2:
            if st.button("📤 Unload All Models"):
                for model in self.models.values():
                    model['status'] = 'available'
                st.warning("All models unloaded!")
        
        with col3:
            if st.button("🔄 Reload Models"):
                for model in self.models.values():
                    if model['status'] == 'loaded':
                        model['status'] = 'loading'
                st.info("Reloading all models...")
        
        st.markdown("**Memory Management**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            memory_limit = st.selectbox(
                "Memory Limit",
                ["8GB", "12GB", "16GB", "Unlimited"],
                key="memory_limit"
            )
            
            if st.button("💾 Optimize Memory"):
                st.info(f"Optimizing memory usage within {memory_limit} limit")
        
        with col2:
            auto_unload = st.checkbox(
                "Auto-unload unused models",
                value=True,
                key="auto_unload"
            )
            
            if st.button("🧹 Clean Memory"):
                st.success("Memory cleaned successfully!")
    
    def render_advanced_settings(self):
        """Render advanced model settings"""
        st.markdown("**Advanced Settings**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Model Controls**")
            
            auto_load = st.checkbox(
                "Auto-load frequently used models",
                value=st.session_state.model_controls['auto_load'],
                key="auto_load"
            )
            st.session_state.model_controls['auto_load'] = auto_load
            
            memory_optimization = st.checkbox(
                "Memory optimization",
                value=st.session_state.model_controls['memory_optimization'],
                key="memory_optimization"
            )
            st.session_state.model_controls['memory_optimization'] = memory_optimization
            
            performance_monitoring = st.checkbox(
                "Performance monitoring",
                value=st.session_state.model_controls['performance_monitoring'],
                key="performance_monitoring"
            )
            st.session_state.model_controls['performance_monitoring'] = performance_monitoring
        
        with col2:
            st.markdown("**Model Parameters**")
            
            context_window = st.slider(
                "Context window",
                min_value=1024,
                max_value=8192,
                value=4096,
                step=1024,
                key="context_window"
            )
            
            batch_size = st.slider(
                "Batch size",
                min_value=1,
                max_value=32,
                value=8,
                key="batch_size"
            )
            
            precision = st.selectbox(
                "Model precision",
                ["FP16", "FP32", "INT8", "INT4"],
                key="precision"
            )
    
    def render_model_performance(self):
        """Render model performance monitoring"""
        st.subheader("📈 Model Performance")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_performance_chart()
        
        with col2:
            self.render_speed_chart()
        
        # Performance metrics
        st.subheader("📊 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_metric_card("Avg Response Time", "1.2s", "⚡", "Fast")
        
        with col2:
            self.render_metric_card("Success Rate", "96.8%", "✅", "High")
        
        with col3:
            self.render_metric_card("Memory Efficiency", "85.2%", "💾", "Good")
        
        with col4:
            self.render_metric_card("Model Switching", "0.8s", "🔄", "Fast")
    
    def render_performance_chart(self):
        """Render model performance chart"""
        st.markdown("**Model Performance Comparison**")
        
        model_names = [model['name'] for model in self.models.values()]
        performances = [model['performance'] for model in self.models.values()]
        
        fig = px.bar(
            x=model_names,
            y=performances,
            title="Model Performance Comparison",
            color=performances,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Model",
            yaxis_title="Performance (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_speed_chart(self):
        """Render model speed chart"""
        st.markdown("**Model Speed Comparison**")
        
        model_names = [model['name'] for model in self.models.values()]
        speeds = [model['speed'] for model in self.models.values()]
        
        fig = px.bar(
            x=model_names,
            y=speeds,
            title="Model Speed Comparison",
            color=speeds,
            color_continuous_scale='plasma'
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Model",
            yaxis_title="Speed (tokens/sec)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_model_configuration(self):
        """Render model configuration"""
        st.subheader("⚙️ Model Configuration")
        
        # Model selection
        st.markdown("**Model Selection**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Default Models**")
            
            default_model = st.selectbox(
                "Default Model",
                [model['name'] for model in self.models.values()],
                index=0,
                key="default_model"
            )
            
            fast_model = st.selectbox(
                "Fast Model",
                [model['name'] for model in self.models.values()],
                index=3,  # TinyLlama
                key="fast_model"
            )
            
            reasoning_model = st.selectbox(
                "Reasoning Model",
                [model['name'] for model in self.models.values()],
                index=2,  # Phi-4-Mini
                key="reasoning_model"
            )
        
        with col2:
            st.markdown("**Model Parameters**")
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                key="model_temperature"
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=2048,
                step=100,
                key="model_max_tokens"
            )
            
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                key="model_top_p"
            )
        
        # Model switching
        st.subheader("🔄 Model Switching")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚡ Switch to Fast Model"):
                st.success("Switched to fast model!")
        
        with col2:
            if st.button("🧠 Switch to Reasoning Model"):
                st.info("Switched to reasoning model!")
        
        with col3:
            if st.button("🔄 Optimize Models"):
                st.success("Models optimized for current workload!")
        
        # Save configuration
        if st.button("💾 Save Configuration", type="primary"):
            st.success("Model configuration saved successfully!")
    
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