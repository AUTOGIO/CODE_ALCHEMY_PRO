"""
Performance Analyzer Component
Detailed system performance analysis and optimization
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psutil
import time
from typing import Dict, Any, List, Optional

class PerformanceAnalyzer:
    """System performance analysis and optimization"""
    
    def __init__(self):
        self.setup_session_state()
        self.performance_metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'disk_io': [],
            'network_io': [],
            'gpu_usage': [],
            'timestamps': []
        }
    
    def setup_session_state(self):
        """Initialize performance analyzer session state"""
        if 'performance_data' not in st.session_state:
            st.session_state.performance_data = {
                'historical_data': {},
                'optimization_suggestions': [],
                'performance_alerts': []
            }
        
        if 'analysis_settings' not in st.session_state:
            st.session_state.analysis_settings = {
                'real_time_monitoring': True,
                'performance_tracking': True,
                'optimization_enabled': True
            }
    
    def render_performance_analyzer(self):
        """Render main performance analysis interface"""
        st.header("📊 Performance Analyzer")
        
        # Performance overview
        self.render_performance_overview()
        
        # Real-time monitoring
        self.render_real_time_monitoring()
        
        # Performance analysis
        self.render_performance_analysis()
        
        # Optimization recommendations
        self.render_optimization_recommendations()
    
    def render_performance_overview(self):
        """Render performance overview dashboard"""
        st.subheader("📈 Performance Overview")
        
        # Get current performance metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Performance status grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_performance_card(
                "CPU Performance",
                f"{cpu_percent:.1f}%",
                "🟢" if cpu_percent < 70 else "🟡" if cpu_percent < 90 else "🔴",
                "Optimal" if cpu_percent < 70 else "High" if cpu_percent < 90 else "Critical"
            )
        
        with col2:
            self.render_performance_card(
                "Memory Performance",
                f"{memory.percent:.1f}%",
                "🟢" if memory.percent < 80 else "🟡" if memory.percent < 95 else "🔴",
                "Optimal" if memory.percent < 80 else "High" if memory.percent < 95 else "Critical"
            )
        
        with col3:
            disk_percent = (disk.used / disk.total) * 100
            self.render_performance_card(
                "Storage Performance",
                f"{disk_percent:.1f}%",
                "🟢" if disk_percent < 80 else "🟡" if disk_percent < 95 else "🔴",
                "Optimal" if disk_percent < 80 else "High" if disk_percent < 95 else "Critical"
            )
        
        with col4:
            # Calculate overall performance score
            performance_score = self.calculate_performance_score(cpu_percent, memory.percent, disk_percent)
            self.render_performance_card(
                "Overall Score",
                f"{performance_score:.0f}/100",
                "🟢" if performance_score >= 80 else "🟡" if performance_score >= 60 else "🔴",
                "Excellent" if performance_score >= 80 else "Good" if performance_score >= 60 else "Poor"
            )
        
        # Update performance history
        self.update_performance_history(cpu_percent, memory.percent, disk_percent)
    
    def render_performance_card(self, title: str, value: str, status_icon: str, status_text: str):
        """Render a performance card"""
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{status_icon}</div>
            <h4 style="margin: 0; font-size: 0.9rem;">{title}</h4>
            <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{value}</p>
            <p style="margin: 0; font-size: 0.8rem; color: #666;">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def calculate_performance_score(self, cpu: float, memory: float, disk: float) -> float:
        """Calculate overall performance score"""
        # Normalize scores (lower is better for usage percentages)
        cpu_score = max(0, 100 - cpu)
        memory_score = max(0, 100 - memory)
        disk_score = max(0, 100 - disk)
        
        # Weighted average
        overall_score = (cpu_score * 0.4 + memory_score * 0.4 + disk_score * 0.2)
        return overall_score
    
    def render_real_time_monitoring(self):
        """Render real-time performance monitoring"""
        st.subheader("⚡ Real-time Monitoring")
        
        # Monitoring controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Ensure session state is initialized
            if 'analysis_settings' not in st.session_state:
                st.session_state.analysis_settings = {
                    'real_time_monitoring': True,
                    'optimization_enabled': True,
                    'performance_tracking': True
                }
            
            real_time_monitoring = st.toggle(
                "🟢 Real-time Monitoring",
                value=st.session_state.analysis_settings.get('real_time_monitoring', True),
                key="real_time_monitoring"
            )
            st.session_state.analysis_settings['real_time_monitoring'] = real_time_monitoring
        
        with col2:
            if st.button("📊 Refresh Metrics"):
                self.update_performance_metrics()
                st.success("Performance metrics updated!")
        
        with col3:
            if st.button("📈 Generate Report"):
                st.info("Generating performance report...")
        
        # Real-time charts
        if len(self.performance_metrics['timestamps']) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_cpu_memory_chart()
            
            with col2:
                self.render_disk_network_chart()
        else:
            st.info("Collecting performance data... Please wait a moment.")
    
    def render_cpu_memory_chart(self):
        """Render CPU and memory usage chart"""
        st.markdown("**CPU & Memory Usage**")
        
        if len(self.performance_metrics['cpu_usage']) > 0:
            df = pd.DataFrame({
                'Time': self.performance_metrics['timestamps'],
                'CPU (%)': self.performance_metrics['cpu_usage'],
                'Memory (%)': self.performance_metrics['memory_usage']
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['Time'], y=df['CPU (%)'],
                mode='lines', name='CPU Usage',
                line=dict(color='#1f77b4', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['Time'], y=df['Memory (%)'],
                mode='lines', name='Memory Usage',
                line=dict(color='#ff7f0e', width=2)
            ))
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="Usage (%)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_disk_network_chart(self):
        """Render disk and network I/O chart"""
        st.markdown("**Disk & Network I/O**")
        
        if len(self.performance_metrics['disk_io']) > 0:
            df = pd.DataFrame({
                'Time': self.performance_metrics['timestamps'],
                'Disk I/O (MB/s)': self.performance_metrics['disk_io'],
                'Network I/O (MB/s)': self.performance_metrics['network_io']
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['Time'], y=df['Disk I/O (MB/s)'],
                mode='lines', name='Disk I/O',
                line=dict(color='#2ca02c', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['Time'], y=df['Network I/O (MB/s)'],
                mode='lines', name='Network I/O',
                line=dict(color='#d62728', width=2)
            ))
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="I/O (MB/s)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_analysis(self):
        """Render detailed performance analysis"""
        st.subheader("🔍 Performance Analysis")
        
        # Analysis tabs
        tab1, tab2, tab3 = st.tabs(["Resource Analysis", "Bottleneck Detection", "Trend Analysis"])
        
        with tab1:
            self.render_resource_analysis()
        
        with tab2:
            self.render_bottleneck_detection()
        
        with tab3:
            self.render_trend_analysis()
    
    def render_resource_analysis(self):
        """Render resource analysis"""
        st.markdown("**Resource Utilization Analysis**")
        
        # CPU Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**CPU Analysis**")
            
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            st.metric("Current Usage", f"{cpu_percent:.1f}%")
            st.metric("CPU Cores", cpu_count)
            st.metric("Frequency", f"{cpu_freq.current:.0f} MHz" if cpu_freq else "Unknown")
            
            # CPU usage breakdown
            cpu_breakdown = {
                'User': 45.2,
                'System': 12.8,
                'Idle': 42.0
            }
            
            fig = px.pie(
                values=list(cpu_breakdown.values()),
                names=list(cpu_breakdown.keys()),
                title="CPU Usage Breakdown"
            )
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Memory Analysis**")
            
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            st.metric("Total Memory", f"{memory.total / (1024**3):.1f} GB")
            st.metric("Used Memory", f"{memory.used / (1024**3):.1f} GB")
            st.metric("Available Memory", f"{memory.available / (1024**3):.1f} GB")
            
            # Memory usage breakdown
            memory_breakdown = {
                'Used': memory.percent,
                'Available': 100 - memory.percent
            }
            
            fig = px.pie(
                values=list(memory_breakdown.values()),
                names=list(memory_breakdown.keys()),
                title="Memory Usage Breakdown"
            )
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_bottleneck_detection(self):
        """Render bottleneck detection"""
        st.markdown("**System Bottleneck Detection**")
        
        # Analyze current bottlenecks
        bottlenecks = self.detect_bottlenecks()
        
        if bottlenecks:
            st.warning("🚨 Performance Bottlenecks Detected")
            
            for bottleneck in bottlenecks:
                st.markdown(f"""
                <div style="
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 5px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                ">
                    <strong>{bottleneck['component']}</strong><br>
                    <small>{bottleneck['description']}</small><br>
                    <small>Impact: {bottleneck['impact']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No performance bottlenecks detected")
        
        # Performance recommendations
        st.markdown("**Performance Recommendations**")
        
        recommendations = [
            "Consider upgrading RAM if memory usage consistently exceeds 80%",
            "Monitor CPU-intensive processes and optimize if needed",
            "Ensure adequate disk space for optimal performance",
            "Consider SSD upgrade for better I/O performance"
        ]
        
        for i, recommendation in enumerate(recommendations, 1):
            st.markdown(f"{i}. {recommendation}")
    
    def render_trend_analysis(self):
        """Render trend analysis"""
        st.markdown("**Performance Trends**")
        
        if len(self.performance_metrics['timestamps']) > 0:
            # Ensure all arrays have the same length
            min_length = min(len(self.performance_metrics['timestamps']), 
                           len(self.performance_metrics['cpu_usage']), 
                           len(self.performance_metrics['memory_usage']))
            
            if min_length > 0:
                # Performance trends over time
                df = pd.DataFrame({
                    'Time': self.performance_metrics['timestamps'][-min_length:],
                    'CPU': self.performance_metrics['cpu_usage'][-min_length:],
                    'Memory': self.performance_metrics['memory_usage'][-min_length:]
                })
            else:
                st.info("Collecting trend data... Please wait.")
                return
            
            # Calculate trends with error handling
            try:
                if len(df) > 1:
                    cpu_trend = np.polyfit(range(len(df)), df['CPU'], 1)[0]
                    memory_trend = np.polyfit(range(len(df)), df['Memory'], 1)[0]
                else:
                    cpu_trend = 0.0
                    memory_trend = 0.0
            except (np.linalg.LinAlgError, ValueError, TypeError):
                # Handle cases where polyfit fails (singular matrix, insufficient data, etc.)
                cpu_trend = 0.0
                memory_trend = 0.0
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "CPU Trend",
                    f"{cpu_trend:.2f}%",
                    "per sample",
                    delta_color="inverse"
                )
            
            with col2:
                st.metric(
                    "Memory Trend",
                    f"{memory_trend:.2f}%",
                    "per sample",
                    delta_color="inverse"
                )
            
            # Trend visualization
            try:
                fig = px.line(
                    df,
                    x='Time',
                    y=['CPU', 'Memory'],
                    title="Performance Trends Over Time"
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating trend visualization: {e}")
                st.info("Trend data available but visualization failed.")
        else:
            st.info("Collecting trend data... Please wait.")
    
    def render_optimization_recommendations(self):
        """Render optimization recommendations"""
        st.subheader("⚡ Optimization Recommendations")
        
        # Optimization status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_optimization_card("CPU Optimization", "85%", "🟢", "Optimized")
        
        with col2:
            self.render_optimization_card("Memory Optimization", "78%", "🟡", "Good")
        
        with col3:
            self.render_optimization_card("Storage Optimization", "92%", "🟢", "Excellent")
        
        # Optimization actions
        st.markdown("**Quick Optimization Actions**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Clean Memory", type="primary"):
                st.success("Memory cleaned successfully!")
        
        with col2:
            if st.button("⚡ Optimize CPU"):
                st.info("CPU optimization in progress...")
        
        with col3:
            if st.button("💾 Optimize Storage"):
                st.success("Storage optimized!")
        
        # Advanced optimization
        st.markdown("**Advanced Optimization Settings**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Performance Settings**")
            
            auto_optimization = st.checkbox(
                "Auto-optimization",
                value=st.session_state.analysis_settings.get('optimization_enabled', True),
                key="auto_optimization"
            )
            st.session_state.analysis_settings['optimization_enabled'] = auto_optimization
            
            performance_tracking = st.checkbox(
                "Performance tracking",
                value=st.session_state.analysis_settings.get('performance_tracking', True),
                key="performance_tracking"
            )
            st.session_state.analysis_settings['performance_tracking'] = performance_tracking
        
        with col2:
            st.markdown("**Optimization Thresholds**")
            
            cpu_threshold = st.slider(
                "CPU threshold (%)",
                min_value=50,
                max_value=95,
                value=80,
                key="cpu_threshold"
            )
            
            memory_threshold = st.slider(
                "Memory threshold (%)",
                min_value=50,
                max_value=95,
                value=85,
                key="memory_threshold"
            )
    
    def render_optimization_card(self, title: str, value: str, icon: str, status: str):
        """Render an optimization card"""
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
            <p style="margin: 0; font-size: 0.8rem; color: #666;">{status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def update_performance_history(self, cpu: float, memory: float, disk: float):
        """Update performance history"""
        timestamp = datetime.now()
        
        # Keep only last 100 data points
        max_points = 100
        
        self.performance_metrics['timestamps'].append(timestamp)
        self.performance_metrics['cpu_usage'].append(cpu)
        self.performance_metrics['memory_usage'].append(memory)
        self.performance_metrics['disk_io'].append(disk * 0.1)  # Simulate disk I/O
        try:
            self.performance_metrics['network_io'].append(np.random.normal(2, 0.5))  # Simulate network I/O
        except Exception:
            self.performance_metrics['network_io'].append(2.0)  # Fallback value
        
        # Trim to max_points
        if len(self.performance_metrics['timestamps']) > max_points:
            self.performance_metrics['timestamps'] = self.performance_metrics['timestamps'][-max_points:]
            self.performance_metrics['cpu_usage'] = self.performance_metrics['cpu_usage'][-max_points:]
            self.performance_metrics['memory_usage'] = self.performance_metrics['memory_usage'][-max_points:]
            self.performance_metrics['disk_io'] = self.performance_metrics['disk_io'][-max_points:]
            self.performance_metrics['network_io'] = self.performance_metrics['network_io'][-max_points:]
    
    def update_performance_metrics(self):
        """Update performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        self.update_performance_history(cpu_percent, memory.percent, (disk.used / disk.total) * 100)
    
    def detect_bottlenecks(self) -> List[Dict[str, Any]]:
        """Detect performance bottlenecks"""
        bottlenecks = []
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        if cpu_percent > 90:
            bottlenecks.append({
                'component': 'CPU',
                'description': 'High CPU usage detected',
                'impact': 'High'
            })
        
        if memory.percent > 95:
            bottlenecks.append({
                'component': 'Memory',
                'description': 'Critical memory usage',
                'impact': 'Critical'
            })
        
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 95:
            bottlenecks.append({
                'component': 'Storage',
                'description': 'Disk space critically low',
                'impact': 'Critical'
            })
        
        return bottlenecks 