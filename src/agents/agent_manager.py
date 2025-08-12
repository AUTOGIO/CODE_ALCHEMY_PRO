"""
Agent Manager for N8N Integration
Coordinates all agents and provides unified interface for N8N workflows
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from .base.agent_interface import BaseAgent, AgentStatus
from .file_organization.agent import FileOrganizationAgent

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages all agents and provides N8N integration interface"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_status_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
        # Initialize agents
        self._initialize_agents()
        
        logger.info("Agent Manager initialized")
    
    def _initialize_agents(self):
        """Initialize all available agents"""
        try:
            # File Organization Agent
            self.agents['file_organization'] = FileOrganizationAgent()
            
            # Add workflow triggers for each agent
            self._setup_workflow_triggers()
            
            logger.info(f"Initialized {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
    
    def _setup_workflow_triggers(self):
        """Setup default workflow triggers for each agent"""
        
        # File Organization Agent triggers
        file_org = self.agents.get('file_organization')
        if file_org:
            file_org.add_workflow_trigger(
                "file_upload",
                {
                    "type": "webhook",
                    "endpoint": "/webhook/file-organization",
                    "triggers": ["new_file", "file_modified", "file_deleted"]
                }
            )
            file_org.add_workflow_trigger(
                "batch_processing",
                {
                    "type": "scheduled",
                    "schedule": "0 */6 * * *",  # Every 6 hours
                    "action": "process_documents"
                }
            )
    
    async def execute_agent(self, agent_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific agent with given parameters"""
        try:
            if agent_name not in self.agents:
                return {
                    'success': False,
                    'error': f'Agent {agent_name} not found',
                    'available_agents': list(self.agents.keys())
                }
            
            agent = self.agents[agent_name]
            
            if not agent.enabled:
                return {
                    'success': False,
                    'error': f'Agent {agent_name} is disabled'
                }
            
            # Validate parameters
            if not agent.validate_parameters(parameters):
                return {
                    'success': False,
                    'error': f'Invalid parameters for agent {agent_name}'
                }
            
            # Update status to running
            agent.update_status(AgentStatus.RUNNING, "Executing task")
            
            # Execute agent
            start_time = datetime.now()
            result = agent.execute(parameters)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update statistics
            if result.get('success'):
                agent.processing_stats['tasks_completed'] += 1
                agent.update_status(AgentStatus.COMPLETED, "Task completed successfully")
            else:
                agent.processing_stats['tasks_failed'] += 1
                agent.update_status(AgentStatus.FAILED, f"Task failed: {result.get('error', 'Unknown error')}")
            
            agent.processing_stats['total_processing_time'] += execution_time
            agent.processing_stats['last_task_time'] = execution_time
            
            # Add to history
            self._add_to_history(agent_name, result, execution_time)
            
            # Add execution metadata
            result.update({
                'agent_name': agent_name,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat(),
                'agent_status': agent.status.value
            })
            
            logger.info(f"Agent {agent_name} executed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error executing agent {agent_name}: {e}")
            
            # Update agent status
            if agent_name in self.agents:
                self.agents[agent_name].update_status(AgentStatus.FAILED, str(e))
            
            return {
                'success': False,
                'error': str(e),
                'agent_name': agent_name,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_agent_status(self, agent_name: str = None) -> Dict[str, Any]:
        """Get status of specific agent or all agents"""
        if agent_name:
            if agent_name not in self.agents:
                return {
                    'success': False,
                    'error': f'Agent {agent_name} not found'
                }
            
            agent = self.agents[agent_name]
            return {
                'success': True,
                'agent': agent.get_health_metrics()
            }
        
        # Return all agents status
        agents_status = {}
        for name, agent in self.agents.items():
            agents_status[name] = agent.get_health_metrics()
        
        return {
            'success': True,
            'agents': agents_status,
            'total_agents': len(self.agents),
            'active_agents': sum(1 for a in self.agents.values() if a.enabled),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_agent_capabilities(self, agent_name: str = None) -> Dict[str, Any]:
        """Get capabilities of specific agent or all agents"""
        if agent_name:
            if agent_name not in self.agents:
                return {
                    'success': False,
                    'error': f'Agent {agent_name} not found'
                }
            
            agent = self.agents[agent_name]
            return {
                'success': True,
                'capabilities': agent.get_capabilities(),
                'workflow_triggers': agent.get_workflow_triggers()
            }
        
        # Return all agents capabilities
        capabilities = {}
        for name, agent in self.agents.items():
            capabilities[name] = {
                'capabilities': agent.get_capabilities(),
                'workflow_triggers': agent.get_workflow_triggers()
            }
        
        return {
            'success': True,
            'capabilities': capabilities,
            'timestamp': datetime.now().isoformat()
        }
    
    def enable_agent(self, agent_name: str) -> Dict[str, Any]:
        """Enable a specific agent"""
        if agent_name not in self.agents:
            return {
                'success': False,
                'error': f'Agent {agent_name} not found'
            }
        
        agent = self.agents[agent_name]
        agent.enabled = True
        agent.update_status(AgentStatus.IDLE, "Agent enabled")
        
        logger.info(f"Agent {agent_name} enabled")
        
        return {
            'success': True,
            'message': f'Agent {agent_name} enabled',
            'agent_status': agent.get_health_metrics()
        }
    
    def disable_agent(self, agent_name: str) -> Dict[str, Any]:
        """Disable a specific agent"""
        if agent_name not in self.agents:
            return {
                'success': False,
                'error': f'Agent {agent_name} not found'
            }
        
        agent = self.agents[agent_name]
        agent.enabled = False
        agent.update_status(AgentStatus.DISABLED, "Agent disabled")
        
        logger.info(f"Agent {agent_name} disabled")
        
        return {
            'success': True,
            'message': f'Agent {agent_name} disabled',
            'agent_status': agent.get_health_metrics()
        }
    
    def add_workflow_trigger(self, agent_name: str, trigger_name: str, 
                           trigger_config: Dict[str, Any]) -> Dict[str, Any]:
        """Add a workflow trigger to a specific agent"""
        if agent_name not in self.agents:
            return {
                'success': False,
                'error': f'Agent {agent_name} not found'
            }
        
        agent = self.agents[agent_name]
        agent.add_workflow_trigger(trigger_name, trigger_config)
        
        logger.info(f"Added workflow trigger '{trigger_name}' to agent {agent_name}")
        
        return {
            'success': True,
            'message': f'Workflow trigger added to {agent_name}',
            'trigger': {
                'name': trigger_name,
                'config': trigger_config,
                'agent': agent_name
            }
        }
    
    def _add_to_history(self, agent_name: str, result: Dict[str, Any], execution_time: float):
        """Add execution result to history"""
        history_entry = {
            'agent_name': agent_name,
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'success': result.get('success', False),
            'result_summary': {
                'status': result.get('status', 'unknown'),
                'message': result.get('message', ''),
                'error': result.get('error', '')
            }
        }
        
        self.agent_status_history.append(history_entry)
        
        # Keep history size manageable
        if len(self.agent_status_history) > self.max_history:
            self.agent_status_history.pop(0)
    
    def get_execution_history(self, agent_name: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get execution history for specific agent or all agents"""
        if agent_name:
            filtered_history = [
                entry for entry in self.agent_status_history
                if entry['agent_name'] == agent_name
            ]
        else:
            filtered_history = self.agent_status_history
        
        # Apply limit
        if limit > 0:
            filtered_history = filtered_history[-limit:]
        
        return {
            'success': True,
            'history': filtered_history,
            'total_entries': len(filtered_history),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """Get summary of all agents"""
        summary = {
            'total_agents': len(self.agents),
            'enabled_agents': 0,
            'running_agents': 0,
            'idle_agents': 0,
            'failed_agents': 0,
            'total_tasks_completed': 0,
            'total_tasks_failed': 0,
            'agents': {}
        }
        
        for name, agent in self.agents.items():
            agent_metrics = agent.get_health_metrics()
            
            # Count statuses
            if agent.enabled:
                summary['enabled_agents'] += 1
                
                if agent.status == AgentStatus.RUNNING:
                    summary['running_agents'] += 1
                elif agent.status == AgentStatus.IDLE:
                    summary['idle_agents'] += 1
                elif agent.status == AgentStatus.FAILED:
                    summary['failed_agents'] += 1
            
            # Aggregate statistics
            summary['total_tasks_completed'] += agent_metrics['processing_stats']['tasks_completed']
            summary['total_tasks_failed'] += agent_metrics['processing_stats']['tasks_failed']
            
            summary['agents'][name] = {
                'status': agent_metrics['status'],
                'enabled': agent_metrics['enabled'],
                'last_activity': agent_metrics['last_activity'],
                'tasks_completed': agent_metrics['processing_stats']['tasks_completed'],
                'tasks_failed': agent_metrics['processing_stats']['tasks_failed']
            }
        
        summary['timestamp'] = datetime.now().isoformat()
        return summary


# Global agent manager instance
agent_manager = AgentManager()
