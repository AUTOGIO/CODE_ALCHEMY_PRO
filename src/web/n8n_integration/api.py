"""
N8N Integration API
FastAPI application for webhook endpoints and agent control
"""

import asyncio
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import our modules
from .security_manager import SecurityManager
from .webhook_handler import WebhookHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class N8NIntegrationAPI:
    """FastAPI application for N8N integration"""
    
    def __init__(self):
        self.app = FastAPI(
            title="CODE_ALCHEMY N8N Integration API",
            description="API for N8N workflow automation integration",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Initialize components
        self.security_manager = SecurityManager()
        self.webhook_handler = WebhookHandler()
        
        # Setup middleware
        self.setup_middleware()
        
        # Setup routes
        self.setup_routes()
        
        logger.info("N8N Integration API initialized")
    
    def setup_middleware(self):
        """Setup CORS and other middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure as needed
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            """API root endpoint"""
            return {
                "message": "CODE_ALCHEMY N8N Integration API",
                "version": "1.0.0",
                "status": "running"
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": asyncio.get_event_loop().time(),
                "components": {
                    "security": "active",
                    "webhook_handler": "active"
                }
            }
        
        # Webhook endpoints
        @self.app.post("/webhook/system-alert")
        async def system_alert_webhook(
            request: Request,
            data: Dict[str, Any],
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Webhook endpoint for system alerts"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Process webhook
                result = await self.webhook_handler.process_webhook({
                    "type": "system_alert",
                    "data": data,
                    "source": "n8n"
                })
                
                return JSONResponse(content=result, status_code=200)
                
            except Exception as e:
                logger.error(f"System alert webhook error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/webhook/file-organization")
        async def file_organization_webhook(
            request: Request,
            data: Dict[str, Any],
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Webhook endpoint for file organization"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Process webhook
                result = await self.webhook_handler.process_webhook({
                    "type": "file_organization",
                    "data": data,
                    "source": "n8n"
                })
                
                return JSONResponse(content=result, status_code=200)
                
            except Exception as e:
                logger.error(f"File organization webhook error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/webhook/content-analysis")
        async def content_analysis_webhook(
            request: Request,
            data: Dict[str, Any],
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Webhook endpoint for content analysis"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Process webhook
                result = await self.webhook_handler.process_webhook({
                    "type": "content_analysis",
                    "data": data,
                    "source": "n8n"
                })
                
                return JSONResponse(content=result, status_code=200)
                
            except Exception as e:
                logger.error(f"Content analysis webhook error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/webhook/productivity")
        async def productivity_webhook(
            request: Request,
            data: Dict[str, Any],
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Webhook endpoint for productivity optimization"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Process webhook
                result = await self.webhook_handler.process_webhook({
                    "type": "productivity",
                    "data": data,
                    "source": "n8n"
                })
                
                return JSONResponse(content=result, status_code=200)
                
            except Exception as e:
                logger.error(f"Productivity webhook error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Agent control endpoints
        @self.app.get("/api/agents/status")
        async def get_agents_status(
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get current agent status for N8N workflows"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Get real agent status from agent manager
                from src.agents.agent_manager import agent_manager
                agents_status = agent_manager.get_agent_status()
                
                return agents_status
                
            except Exception as e:
                logger.error(f"Get agents status error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/agents/{agent_name}/trigger")
        async def trigger_agent(
            agent_name: str,
            request: Request,
            params: Dict[str, Any],
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Trigger specific agent with parameters"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Get real agent manager and execute agent
                from src.agents.agent_manager import agent_manager
                
                # Execute the agent
                result = await agent_manager.execute_agent(agent_name, params)
                
                logger.info(f"Agent {agent_name} triggered with params: {params}")
                return result
                
            except Exception as e:
                logger.error(f"Trigger agent error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Agent Management endpoints
        @self.app.get("/api/agents/{agent_name}/capabilities")
        async def get_agent_capabilities(
            agent_name: str,
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get agent capabilities and workflow triggers"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Get agent capabilities from agent manager
                from src.agents.agent_manager import agent_manager
                capabilities = agent_manager.get_agent_capabilities(agent_name)
                
                return capabilities
                
            except Exception as e:
                logger.error(f"Get agent capabilities error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/agents/{agent_name}/enable")
        async def enable_agent(
            agent_name: str,
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Enable a specific agent"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Enable agent via agent manager
                from src.agents.agent_manager import agent_manager
                result = agent_manager.enable_agent(agent_name)
                
                return result
                
            except Exception as e:
                logger.error(f"Enable agent error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/agents/{agent_name}/disable")
        async def disable_agent(
            agent_name: str,
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Disable a specific agent"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Disable agent via agent manager
                from src.agents.agent_manager import agent_manager
                result = agent_manager.disable_agent(agent_name)
                
                return result
                
            except Exception as e:
                logger.error(f"Disable agent error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/agents/summary")
        async def get_agents_summary(
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get summary of all agents"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Get agents summary from agent manager
                from src.agents.agent_manager import agent_manager
                summary = agent_manager.get_agent_summary()
                
                return summary
                
            except Exception as e:
                logger.error(f"Get agents summary error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/agents/history")
        async def get_agents_history(
            request: Request,
            agent_name: str = None,
            limit: int = 100,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get execution history for agents"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                # Get execution history from agent manager
                from src.agents.agent_manager import agent_manager
                history = agent_manager.get_execution_history(agent_name, limit)
                
                return history
                
            except Exception as e:
                logger.error(f"Get agents history error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Monitoring endpoints removed - no real-time data collection
        # @self.app.get("/api/monitoring/system") - Removed
        
        # Webhook management endpoints
        @self.app.get("/api/webhooks/history")
        async def get_webhook_history(
            request: Request,
            limit: int = 100,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get webhook processing history"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                history = self.webhook_handler.get_webhook_history(limit)
                return {"webhooks": history}
                
            except Exception as e:
                logger.error(f"Get webhook history error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/webhooks/stats")
        async def get_webhook_stats(
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get webhook processing statistics"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                stats = self.webhook_handler.get_webhook_stats()
                return {"statistics": stats}
                
            except Exception as e:
                logger.error(f"Get webhook stats error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Security endpoints
        @self.app.get("/api/security/status")
        async def get_security_status(
            request: Request,
            api_key: str = Depends(self.security_manager.get_api_key_from_header)
        ):
            """Get security configuration status"""
            try:
                # Validate security
                self.security_manager.validate_ip_address(request)
                self.security_manager.check_rate_limit(api_key)
                
                status = self.security_manager.get_security_status()
                return {"security": status}
                
            except Exception as e:
                logger.error(f"Get security status error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the FastAPI application"""
        logger.info(f"Starting N8N Integration API on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)

# Create global instance
n8n_api = N8NIntegrationAPI()
