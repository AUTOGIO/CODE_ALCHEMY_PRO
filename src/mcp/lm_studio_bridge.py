#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - LM Studio Bridge MCP Server
Provides direct access to LM Studio models via MCP protocol
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.core.config import config


class LMStudioBridge:
    """MCP server for LM Studio integration"""
    
    def __init__(self):
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234")
        self.api_base = f"{self.lm_studio_url}/v1"
        
    async def list_models(self) -> Dict[str, Any]:
        """List available models in LM Studio"""
        try:
            response = requests.get(f"{self.api_base}/models", timeout=10)
            if response.status_code == 200:
                models = response.json().get('data', [])
                return {
                    "success": True,
                    "models": [model['id'] for model in models],
                    "count": len(models),
                    "url": self.lm_studio_url
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "url": self.lm_studio_url
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": self.lm_studio_url
            }
    
    async def test_model(self, model_name: str) -> Dict[str, Any]:
        """Test a specific model with a simple prompt"""
        try:
            test_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Hello, test message"}],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            response = requests.post(f"{self.api_base}/chat/completions", 
                                  json=test_payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "model": model_name,
                    "response": result['choices'][0]['message']['content'],
                    "tokens_used": len(result['choices'][0]['message']['content'].split())
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "model": model_name
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_name
            }
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific model"""
        try:
            # Test the model to get performance metrics
            test_result = await self.test_model(model_name)
            
            return {
                "success": True,
                "model": model_name,
                "available": test_result["success"],
                "performance": {
                    "response_time": "tested",
                    "tokens_generated": test_result.get("tokens_used", 0),
                    "status": "active" if test_result["success"] else "error"
                },
                "url": self.lm_studio_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_name
            }


# MCP Server implementation
async def main():
    """Main MCP server function"""
    bridge = LMStudioBridge()
    
    # Handle MCP commands
    while True:
        try:
            # Read command from stdin
            command = input().strip()
            
            if command == "list_models":
                result = await bridge.list_models()
                print(json.dumps(result, indent=2))
            
            elif command.startswith("test_model"):
                model_name = command.split(" ", 1)[1] if " " in command else "deepseek-r1-0528-qwen3-8b"
                result = await bridge.test_model(model_name)
                print(json.dumps(result, indent=2))
            
            elif command.startswith("get_model_info"):
                model_name = command.split(" ", 1)[1] if " " in command else "deepseek-r1-0528-qwen3-8b"
                result = await bridge.get_model_info(model_name)
                print(json.dumps(result, indent=2))
            
            elif command == "help":
                print(json.dumps({
                    "available_commands": [
                        "list_models",
                        "test_model <model_name>",
                        "get_model_info <model_name>",
                        "help"
                    ],
                    "description": "LM Studio Bridge MCP Server"
                }, indent=2))
            
            else:
                print(json.dumps({
                    "error": "Unknown command",
                    "available_commands": ["list_models", "test_model", "get_model_info", "help"]
                }, indent=2))
                
        except EOFError:
            break
        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main()) 