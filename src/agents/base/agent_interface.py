"""
Base Agent Interface for N8N Integration
Defines the contract that all agents must implement
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import asyncio


class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DISABLED = "disabled"


class AgentPriority(Enum):
    """Agent priority enumeration"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class BaseAgent(ABC):
    """Base agent class that all agents must inherit from"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.status = AgentStatus.IDLE
        self.priority = AgentPriority.NORMAL
        self.enabled = True
        self.last_activity = None
        self.processing_stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_processing_time': 0.0,
            'last_task_time': None
        }
        
        # N8N integration properties
        self.webhook_enabled = True
        self.auto_report_status = True
        self.workflow_triggers = []
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and supported operations"""
        pass
    
    def update_status(self, status: AgentStatus, message: str = ""):
        """Update agent status"""
        self.status = status
        self.last_activity = datetime.now()
        
        if self.auto_report_status and self.webhook_enabled:
            self._report_status_change(status, message)
    
    def _report_status_change(self, status: AgentStatus, message: str):
        """Report status change to N8N webhook system"""
        try:
            # This will be implemented by the N8N integration
            from src.web.n8n_integration.webhook_handler import WebhookHandler
            
            webhook_handler = WebhookHandler()
            asyncio.create_task(
                webhook_handler.send_system_alert(
                    "agent_status_change",
                    f"Agent {self.agent_name}: {status.value} - {message}",
                    "info"
                )
            )
        except Exception as e:
            # Silently fail if N8N integration is not available
            pass
    
    def add_workflow_trigger(self, trigger_name: str, trigger_config: Dict[str, Any]):
        """Add a workflow trigger for this agent"""
        self.workflow_triggers.append({
            'name': trigger_name,
            'config': trigger_config,
            'added_at': datetime.now()
        })
    
    def get_workflow_triggers(self) -> List[Dict[str, Any]]:
        """Get all workflow triggers for this agent"""
        return self.workflow_triggers
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        # Default implementation - override in subclasses
        return True
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """Get agent health metrics"""
        return {
            'agent_name': self.agent_name,
            'status': self.status.value,
            'enabled': self.enabled,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'processing_stats': self.processing_stats,
            'webhook_enabled': self.webhook_enabled,
            'workflow_triggers_count': len(self.workflow_triggers)
        }
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.processing_stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_processing_time': 0.0,
            'last_task_time': None
        }
    
    def __str__(self):
        return f"{self.agent_name} ({self.status.value})"
    
    def __repr__(self):
        return f"<{self.__class__.__name__} name='{self.agent_name}' status='{self.status.value}'>"
