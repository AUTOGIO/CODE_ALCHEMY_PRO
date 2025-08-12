"""
Security Manager for N8N Integration
API key validation, rate limiting, and security controls
"""

import time
import hashlib
from typing import Dict, Any
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)


class SecurityManager:
    """Manages API security, authentication, and rate limiting"""
    
    def __init__(self):
        # API Keys for different N8N instances
        self.api_keys = {
            "n8n_main": "sk_codealchemy_n8n_2025",
            "n8n_monitoring": "sk_codealchemy_monitor_2025", 
            "n8n_automation": "sk_codealchemy_auto_2025"
        }
        
        # Rate limiting configuration
        self.rate_limit_window = 60  # seconds
        self.rate_limit_requests = 100  # requests per window
        self.request_counts: Dict[str, list] = {}
        
        # Security settings
        self.enable_ip_whitelist = True
        self.allowed_ips = {"127.0.0.1", "localhost", "::1"}
        
        # HTTP Bearer for token validation
        self.security = HTTPBearer()
        
        logger.info("Security Manager initialized with API key protection")
    
    def validate_api_key(self, api_key: str) -> str:
        """Validate API key and return the key name if valid"""
        if api_key not in self.api_keys.values():
            logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
            raise HTTPException(
                status_code=401, 
                detail="Invalid API key"
            )
        
        # Find the key name
        key_name = next(name for name, key in self.api_keys.items() if key == api_key)
        logger.debug(f"Valid API key used: {key_name}")
        return key_name
    
    def check_rate_limit(self, api_key: str) -> None:
        """Check rate limiting for the given API key"""
        current_time = time.time()
        
        if api_key not in self.request_counts:
            self.request_counts[api_key] = []
        
        # Clean old requests outside the window
        self.request_counts[api_key] = [
            req_time for req_time in self.request_counts[api_key]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Check if limit exceeded
        if len(self.request_counts[api_key]) >= self.rate_limit_requests:
            logger.warning(
                f"Rate limit exceeded for API key: {api_key[:10]}..."
            )
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Maximum 100 requests per minute."
            )
        
        # Add current request
        self.request_counts[api_key].append(current_time)
        logger.debug(f"Rate limit check passed for API key: {api_key[:10]}...")
    
    def validate_ip_address(self, request: Request) -> None:
        """Validate client IP address if IP whitelisting is enabled"""
        if not self.enable_ip_whitelist:
            return
        
        client_ip = request.client.host
        if client_ip not in self.allowed_ips:
            logger.warning(f"Blocked request from unauthorized IP: {client_ip}")
            raise HTTPException(
                status_code=403,
                detail="IP address not authorized"
            )
        
        logger.debug(f"IP validation passed for: {client_ip}")
    
    def get_api_key_from_header(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
        """Extract and validate API key from Authorization header"""
        api_key = credentials.credentials
        return self.validate_api_key(api_key)
    
    def secure_endpoint(self, request: Request, api_key: str = Depends(HTTPBearer())) -> str:
        """Complete security validation for protected endpoints"""
        # Validate IP address
        self.validate_ip_address(request)
        
        # Validate API key
        key_name = self.validate_api_key(api_key.credentials)
        
        # Check rate limiting
        self.check_rate_limit(api_key.credentials)
        
        logger.info(f"Secure endpoint access granted to: {key_name}")
        return key_name
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status and metrics"""
        return {
            "api_keys_configured": len(self.api_keys),
            "rate_limit_window": self.rate_limit_window,
            "rate_limit_requests": self.rate_limit_requests,
            "ip_whitelist_enabled": self.enable_ip_whitelist,
            "allowed_ips": list(self.allowed_ips),
            "active_requests": {
                key: len(requests) for key, requests in self.request_counts.items()
            }
        }
    
    def rotate_api_key(self, key_name: str, new_key: str) -> bool:
        """Rotate an API key (admin function)"""
        if key_name not in self.api_keys:
            return False
        
        # Hash the new key for security
        hashed_key = hashlib.sha256(new_key.encode()).hexdigest()
        self.api_keys[key_name] = hashed_key
        
        logger.info(f"API key rotated for: {key_name}")
        return True
