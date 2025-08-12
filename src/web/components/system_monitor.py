"""
System Monitor Component
Real-time system monitoring and alerting
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psutil
import threading
import time
from typing import Dict, Any, List, Optional

class SystemMonitor:
    """Real-time system monitoring and alerting"""
    
    def __init__(self):
        self.setup_session_state()
        self.alert_thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'disk_usage': 90,
            'temperature': 85
        }
    
    def setup_session_state(self):
        """Initialize monitoring session state"""
        if 'system_metrics' not in st.session_state:
            st.session_state.system_metrics = {
                'cpu_usage': [],
                'memory_usage': [],
                'disk_usage': [],
                'network_io': [],
                'temperature': [],
                'timestamps': []
            }
        
        if 'alerts' not in st.session_state:
            st.session_state.alerts = []
        
        if 'monitoring_active' not in st.session_state:
            st.session_state.monitoring_active = True
    
    def render_system_monitor(self):
        """Render main system monitoring interface"""
        st.header("📊 System Monitor")
        
        # Monitoring controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monitoring_active = st.toggle(
                "🟢 Active Monitoring",
                value=st.session_state.monitoring_active,
                key="monitoring_toggle"
            )
            st.session_state.monitoring_active = monitoring_active
        
        with col2:
            if st.button("📊 Refresh Metrics"):
                self.update_metrics()
                st.success("Metrics updated!")
        
        with col3:
            if st.button("🔔 Clear Alerts"):
                st.session_state.alerts = []
                st.success("Alerts cleared!")
        
        # Real-time metrics
        self.render_real_time_metrics()
        
        # Performance charts
        self.render_performance_charts()
        
        # System alerts
        self.render_alerts()
        
        # System information
        self.render_system_info()
    
    def render_real_time_metrics(self):
        """Render real-time system metrics"""
        st.subheader("⚡ Real-time Metrics")
        
        # Get current system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.render_metric_gauge(
                "CPU Usage",
                cpu_percent,
                "%",
                "red" if cpu_percent > 80 else "orange" if cpu_percent > 60 else "green"
            )
        
        with col2:
            self.render_metric_gauge(
                "Memory Usage",
                memory.percent,
                "%",
                "red" if memory.percent > 85 else "orange" if memory.percent > 70 else "green"
            )
        
        with col3:
            self.render_metric_gauge(
                "Disk Usage",
                (disk.used / disk.total) * 100,
                "%",
                "red" if (disk.used / disk.total) * 100 > 90 else "orange" if (disk.used / disk.total) * 100 > 75 else "green"
            )
        
        with col4:
            # Network I/O
            network = psutil.net_io_counters()
            network_mb = (network.bytes_sent + network.bytes_recv) / 1024 / 1024
            self.render_metric_card(
                "Network I/O",
                f"{network_mb:.1f}",
                "MB",
                "🌐"
            )
        
        # Update metrics history
        self.update_metrics_history(cpu_percent, memory.percent, (disk.used / disk.total) * 100)
    
    def render_metric_gauge(self, title: str, value: float, unit: str, color: str):
        """Render a metric gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_metric_card(self, title: str, value: str, unit: str, icon: str):
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
            <p style="margin: 0; font-size: 0.8rem; color: #666;">{unit}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_performance_charts(self):
        """Render performance trend charts"""
        st.subheader("📈 Performance Trends")
        
        if len(st.session_state.system_metrics['timestamps']) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_cpu_chart()
            
            with col2:
                self.render_memory_chart()
            
            # Network and disk charts
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_network_chart()
            
            with col2:
                self.render_disk_chart()
        else:
            st.info("Collecting performance data... Please wait a moment.")
    
    def render_cpu_chart(self):
        """Render CPU usage chart"""
        if len(st.session_state.system_metrics['cpu_usage']) > 0:
            df = pd.DataFrame({
                'Time': st.session_state.system_metrics['timestamps'],
                'CPU Usage (%)': st.session_state.system_metrics['cpu_usage']
            })
            
            fig = px.line(
                df,
                x='Time',
                y='CPU Usage (%)',
                title="CPU Usage Over Time",
                line_shape='linear'
            )
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="CPU Usage (%)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_memory_chart(self):
        """Render memory usage chart"""
        if len(st.session_state.system_metrics['memory_usage']) > 0:
            df = pd.DataFrame({
                'Time': st.session_state.system_metrics['timestamps'],
                'Memory Usage (%)': st.session_state.system_metrics['memory_usage']
            })
            
            fig = px.line(
                df,
                x='Time',
                y='Memory Usage (%)',
                title="Memory Usage Over Time",
                line_shape='linear'
            )
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="Memory Usage (%)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_network_chart(self):
        """Render network I/O chart"""
        if len(st.session_state.system_metrics['network_io']) > 0:
            df = pd.DataFrame({
                'Time': st.session_state.system_metrics['timestamps'],
                'Network I/O (MB)': st.session_state.system_metrics['network_io']
            })
            
            fig = px.line(
                df,
                x='Time',
                y='Network I/O (MB)',
                title="Network I/O Over Time",
                line_shape='linear'
            )
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="Network I/O (MB)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_disk_chart(self):
        """Render disk usage chart"""
        if len(st.session_state.system_metrics['disk_usage']) > 0:
            df = pd.DataFrame({
                'Time': st.session_state.system_metrics['timestamps'],
                'Disk Usage (%)': st.session_state.system_metrics['disk_usage']
            })
            
            fig = px.line(
                df,
                x='Time',
                y='Disk Usage (%)',
                title="Disk Usage Over Time",
                line_shape='linear'
            )
            
            fig.update_layout(
                height=300,
                xaxis_title="Time",
                yaxis_title="Disk Usage (%)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_alerts(self):
        """Render system alerts"""
        st.subheader("🔔 System Alerts")
        
        # Check for new alerts
        self.check_alerts()
        
        if st.session_state.alerts:
            for alert in st.session_state.alerts[-5:]:  # Show last 5 alerts
                alert_color = {
                    'critical': '🔴',
                    'warning': '🟡',
                    'info': '🔵'
                }
                
                st.markdown(f"""
                <div style="
                    background: {'#ffebee' if alert['level'] == 'critical' else '#fff3e0' if alert['level'] == 'warning' else '#e3f2fd'};
                    border-left: 4px solid {'#f44336' if alert['level'] == 'critical' else '#ff9800' if alert['level'] == 'warning' else '#2196f3'};
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-radius: 4px;
                ">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">{alert_color.get(alert['level'], '⚪')}</span>
                        <div>
                            <strong>{alert['title']}</strong>
                            <br>
                            <small>{alert['message']}</small>
                            <br>
                            <small style="color: #666;">{alert['timestamp']}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No active alerts")
    
    def render_system_info(self):
        """Render detailed system information"""
        st.subheader("💻 System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Hardware Information**")
            
            # CPU Info
            cpu_info = {
                'Model': psutil.cpu_count(logical=False),
                'Cores': psutil.cpu_count(logical=True),
                'Architecture': 'ARM64 (Apple Silicon)',
                'Frequency': f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "Unknown"
            }
            
            for key, value in cpu_info.items():
                st.write(f"**{key}:** {value}")
            
            # Memory Info
            memory = psutil.virtual_memory()
            st.write(f"**Total Memory:** {memory.total / (1024**3):.1f} GB")
            st.write(f"**Available Memory:** {memory.available / (1024**3):.1f} GB")
        
        with col2:
            st.markdown("**Storage Information**")
            
            # Disk Info
            disk = psutil.disk_usage('/')
            st.write(f"**Total Disk:** {disk.total / (1024**3):.1f} GB")
            st.write(f"**Used Disk:** {disk.used / (1024**3):.1f} GB")
            st.write(f"**Free Disk:** {disk.free / (1024**3):.1f} GB")
            
            # Network Info
            network = psutil.net_io_counters()
            st.write(f"**Bytes Sent:** {network.bytes_sent / (1024**2):.1f} MB")
            st.write(f"**Bytes Received:** {network.bytes_recv / (1024**2):.1f} MB")
    
    def update_metrics(self):
        """Update system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Update metrics history
        self.update_metrics_history(
            cpu_percent,
            memory.percent,
            (disk.used / disk.total) * 100,
            (network.bytes_sent + network.bytes_recv) / (1024**2)
        )
    
    def update_metrics_history(self, cpu: float, memory: float, disk: float, network: float = 0):
        """Update metrics history"""
        timestamp = datetime.now()
        
        # Keep only last 100 data points
        max_points = 100
        
        st.session_state.system_metrics['timestamps'].append(timestamp)
        st.session_state.system_metrics['cpu_usage'].append(cpu)
        st.session_state.system_metrics['memory_usage'].append(memory)
        st.session_state.system_metrics['disk_usage'].append(disk)
        st.session_state.system_metrics['network_io'].append(network)
        
        # Trim to max_points
        if len(st.session_state.system_metrics['timestamps']) > max_points:
            st.session_state.system_metrics['timestamps'] = st.session_state.system_metrics['timestamps'][-max_points:]
            st.session_state.system_metrics['cpu_usage'] = st.session_state.system_metrics['cpu_usage'][-max_points:]
            st.session_state.system_metrics['memory_usage'] = st.session_state.system_metrics['memory_usage'][-max_points:]
            st.session_state.system_metrics['disk_usage'] = st.session_state.system_metrics['disk_usage'][-max_points:]
            st.session_state.system_metrics['network_io'] = st.session_state.system_metrics['network_io'][-max_points:]
    
    def check_alerts(self):
        """Check for system alerts"""
        if not st.session_state.monitoring_active:
            return
        
        current_time = datetime.now()
        
        # CPU Alert
        if len(st.session_state.system_metrics['cpu_usage']) > 0:
            current_cpu = st.session_state.system_metrics['cpu_usage'][-1]
            if current_cpu > self.alert_thresholds['cpu_usage']:
                self.add_alert(
                    'critical',
                    'High CPU Usage',
                    f'CPU usage is {current_cpu:.1f}%, above threshold of {self.alert_thresholds["cpu_usage"]}%'
                )
        
        # Memory Alert
        if len(st.session_state.system_metrics['memory_usage']) > 0:
            current_memory = st.session_state.system_metrics['memory_usage'][-1]
            if current_memory > self.alert_thresholds['memory_usage']:
                self.add_alert(
                    'warning',
                    'High Memory Usage',
                    f'Memory usage is {current_memory:.1f}%, above threshold of {self.alert_thresholds["memory_usage"]}%'
                )
        
        # Disk Alert
        if len(st.session_state.system_metrics['disk_usage']) > 0:
            current_disk = st.session_state.system_metrics['disk_usage'][-1]
            if current_disk > self.alert_thresholds['disk_usage']:
                self.add_alert(
                    'critical',
                    'High Disk Usage',
                    f'Disk usage is {current_disk:.1f}%, above threshold of {self.alert_thresholds["disk_usage"]}%'
                )
    
    def add_alert(self, level: str, title: str, message: str):
        """Add a new alert"""
        alert = {
            'level': level,
            'title': title,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check if similar alert already exists
        for existing_alert in st.session_state.alerts:
            if (existing_alert['title'] == title and 
                existing_alert['level'] == level and
                (datetime.now() - datetime.strptime(existing_alert['timestamp'], '%Y-%m-%d %H:%M:%S')).seconds < 300):  # 5 minutes
                return
        
        st.session_state.alerts.append(alert)
        
        # Keep only last 50 alerts
        if len(st.session_state.alerts) > 50:
            st.session_state.alerts = st.session_state.alerts[-50:] 