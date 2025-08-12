"""
Webhook Handler for N8N Integration
Processes incoming webhooks and manages webhook responses
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List
import aiohttp

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handles webhook processing and management"""
    
    def __init__(self, n8n_webhook_url: str = "http://localhost:5678"):
        self.n8n_webhook_url = n8n_webhook_url
        self.webhook_history: List[Dict[str, Any]] = []
        self.processing_queue: asyncio.Queue = asyncio.Queue()
        self.max_history = 1000
        
        # Start background processing (will be started when needed)
        self._background_task = None
        
        logger.info(f"Webhook Handler initialized for N8N: {n8n_webhook_url}")
    
    def start_background_processing(self):
        """Start background webhook processing task"""
        if self._background_task is None:
            try:
                loop = asyncio.get_event_loop()
                self._background_task = loop.create_task(
                    self._process_webhook_queue()
                )
                logger.info("Background webhook processing started")
            except RuntimeError:
                # No event loop running, will start when needed
                logger.info("No event loop running, background processing deferred")
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook data"""
        try:
            # Add timestamp and metadata
            webhook_data.update({
                "received_at": datetime.now().isoformat(),
                "processed": False,
                "webhook_id": self._generate_webhook_id()
            })
            
            # Add to history
            self.webhook_history.append(webhook_data)
            if len(self.webhook_history) > self.max_history:
                self.webhook_history.pop(0)
            
            # Queue for processing
            await self.processing_queue.put(webhook_data)
            
            logger.info(f"Webhook queued for processing: {webhook_data['webhook_id']}")
            
            return {
                "success": True,
                "status": "accepted",
                "webhook_id": webhook_data["webhook_id"],
                "processing": "queued"
            }
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _process_webhook_queue(self):
        """Background task to process webhook queue"""
        while True:
            try:
                # Get webhook from queue
                webhook_data = await self.processing_queue.get()
                
                # Process webhook based on type
                result = await self._route_webhook(webhook_data)
                
                # Update webhook status
                webhook_data.update({
                    "processed": True,
                    "processed_at": datetime.now().isoformat(),
                    "result": result
                })
                
                logger.info(f"Webhook processed: {webhook_data['webhook_id']}")
                
            except Exception as e:
                logger.error(f"Error in webhook queue processing: {e}")
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
    
    async def _route_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route webhook to appropriate handler based on type"""
        webhook_type = webhook_data.get("type", "unknown")
        
        try:
            if webhook_type == "system_alert":
                return await self._handle_system_alert(webhook_data)
            elif webhook_type == "file_organization":
                return await self._handle_file_organization(webhook_data)
            elif webhook_type == "content_analysis":
                return await self._handle_content_analysis(webhook_data)
            elif webhook_type == "agent_status":
                return await self._handle_agent_status(webhook_data)
            else:
                return await self._handle_generic_webhook(webhook_data)
                
        except Exception as e:
            logger.error(f"Error routing webhook {webhook_type}: {e}")
            return {"status": "error", "message": str(e)}
    
    async def _handle_system_alert(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system alert webhooks"""
        alert_type = webhook_data.get("alert_type", "info")
        message = webhook_data.get("message", "")
        severity = webhook_data.get("severity", "info")
        
        logger.info(f"System Alert [{severity.upper()}]: {message}")
        
        # Here you would integrate with existing alerting system
        # For now, just log and acknowledge
        
        return {
            "status": "processed",
            "alert_type": alert_type,
            "severity": severity,
            "action": "logged"
        }
    
    async def _handle_file_organization(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file organization webhooks"""
        action = webhook_data.get("action", "unknown")
        file_path = webhook_data.get("file_path", "")
        
        logger.info(f"File Organization: {action} - {file_path}")
        
        # Here you would trigger file organization agent
        # For now, just acknowledge
        
        return {
            "status": "processed",
            "action": action,
            "file_path": file_path,
            "result": "acknowledged"
        }
    
    async def _handle_content_analysis(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle content analysis webhooks"""
        content_type = webhook_data.get("content_type", "unknown")
        content_id = webhook_data.get("content_id", "")
        
        logger.info(f"Content Analysis: {content_type} - {content_id}")
        
        # Here you would trigger content analysis agent
        # For now, just acknowledge
        
        return {
            "status": "processed",
            "content_type": content_type,
            "content_id": content_id,
            "result": "acknowledged"
        }
    
    async def _handle_agent_status(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle agent status webhooks"""
        agent_name = webhook_data.get("agent_name", "unknown")
        status = webhook_data.get("status", "unknown")
        
        logger.info(f"Agent Status: {agent_name} - {status}")
        
        # Here you would update agent status
        # For now, just acknowledge
        
        return {
            "status": "processed",
            "agent_name": agent_name,
            "status": status,
            "result": "acknowledged"
        }
    
    async def _handle_generic_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic webhooks"""
        logger.info(f"Generic webhook received: {webhook_data.get('type', 'unknown')}")
        
        return {
            "status": "processed",
            "type": "generic",
            "result": "acknowledged"
        }
    
    def _generate_webhook_id(self) -> str:
        """Generate unique webhook ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"webhook_{timestamp}"
    
    async def send_to_n8n(self, webhook_data: Dict[str, Any], 
                          endpoint: str = "webhook/codealchemy") -> bool:
        """Send webhook data to N8N instance"""
        try:
            url = f"{self.n8n_webhook_url}/{endpoint}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=webhook_data, timeout=10) as response:
                    if response.status == 200:
                        logger.info(f"Webhook sent to N8N: {endpoint}")
                        return True
                    else:
                        logger.warning(
                            f"N8N webhook failed: {response.status} - {endpoint}"
                        )
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending webhook to N8N: {e}")
            return False
    
    def get_webhook_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent webhook history"""
        return self.webhook_history[-limit:]
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook processing statistics"""
        total_webhooks = len(self.webhook_history)
        processed_webhooks = sum(1 for w in self.webhook_history if w.get("processed"))
        
        return {
            "total_webhooks": total_webhooks,
            "processed_webhooks": processed_webhooks,
            "pending_webhooks": self.processing_queue.qsize(),
            "success_rate": (processed_webhooks / total_webhooks * 100) if total_webhooks > 0 else 0
        }
