#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Model Manager MCP Server
Intelligent model selection and management
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


class ModelManager:
    """Intelligent model selection and management"""
    
    def __init__(self):
        self.lm_studio_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234")
        self.api_base = f"{self.lm_studio_url}/v1"
        self.models_path = os.getenv("MODELS_PATH", "/Volumes/MICRO/models")
        
        # Model recommendations based on task
        self.task_model_mapping = {
            "code_analysis": ["deepseek-r1-0528-qwen3-8b", "granite-3.2-8b-instruct"],
            "code_generation": ["deepseek-r1-0528-qwen3-8b", "granite-3.2-8b-instruct"],
            "reasoning": ["microsoft_phi-4-mini-reasoning", "meta-llama-3.1-8b-instruct"],
            "content_analysis": ["meta-llama-3.1-8b-instruct", "qwen/qwen3-8b"],
            "fast_response": ["tinyllama-1.1b-chat-v1.0-intel-dpo", "lama3.2-1b-translatev3"],
            "vision": ["qwen2.5-vl-7b-instruct"],
            "translation": ["lama3.2-1b-translatev3"],
            "general": ["meta-llama-3.1-8b-instruct", "qwen/qwen3-8b"]
        }
    
    async def recommend_model(self, task: str, speed_priority: bool = False, 
                            max_size: str = None) -> Dict[str, Any]:
        """Recommend the best model for a specific task"""
        try:
            # Get available models
            response = requests.get(f"{self.api_base}/models", timeout=10)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to get models: HTTP {response.status_code}"
                }
            
            available_models = [model['id'] for model in response.json().get('data', [])]
            
            # Get recommendations for task
            recommended_models = self.task_model_mapping.get(task.lower(), 
                                                          self.task_model_mapping["general"])
            
            # Filter by available models
            available_recommendations = [m for m in recommended_models if m in available_models]
            
            if not available_recommendations:
                # Fallback to any available model
                available_recommendations = available_models[:3]
            
            # Prioritize by speed if requested
            if speed_priority:
                # Sort by model size (smaller = faster)
                available_recommendations.sort(key=lambda x: self._get_model_size(x))
            
            # Limit by max size if specified
            if max_size:
                max_size_value = self._parse_size_string(max_size)
                available_recommendations = [
                    m for m in available_recommendations 
                    if self._get_model_size(m) <= max_size_value
                ]
            
            if available_recommendations:
                best_model = available_recommendations[0]
                return {
                    "success": True,
                    "task": task,
                    "recommended_model": best_model,
                    "alternatives": available_recommendations[1:3],
                    "reason": f"Best match for '{task}' task",
                    "speed_priority": speed_priority,
                    "max_size": max_size
                }
            else:
                return {
                    "success": False,
                    "error": "No suitable models found",
                    "task": task,
                    "available_models": available_models
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": task
            }
    
    def _get_model_size(self, model_name: str) -> float:
        """Estimate model size from name"""
        import re
        size_match = re.search(r'(\d+(?:\.\d+)?)b', model_name.lower())
        if size_match:
            return float(size_match.group(1))
        return 8.0  # Default size
    
    def _parse_size_string(self, size_str: str) -> float:
        """Parse size string like '8B' to number"""
        import re
        size_match = re.search(r'(\d+(?:\.\d+)?)', size_str)
        if size_match:
            return float(size_match.group(1))
        return 8.0  # Default size
    
    async def get_model_performance(self, model_name: str) -> Dict[str, Any]:
        """Get performance metrics for a model"""
        try:
            # Test the model
            test_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Test message"}],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            start_time = asyncio.get_event_loop().time()
            response = requests.post(f"{self.api_base}/chat/completions", 
                                  json=test_payload, timeout=30)
            end_time = asyncio.get_event_loop().time()
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                tokens_generated = len(response_text.split())
                
                return {
                    "success": True,
                    "model": model_name,
                    "response_time": end_time - start_time,
                    "tokens_generated": tokens_generated,
                    "tokens_per_second": tokens_generated / (end_time - start_time),
                    "status": "active"
                }
            else:
                return {
                    "success": False,
                    "model": model_name,
                    "error": f"HTTP {response.status_code}",
                    "status": "error"
                }
                
        except Exception as e:
            return {
                "success": False,
                "model": model_name,
                "error": str(e),
                "status": "error"
            }
    
    async def list_available_tasks(self) -> Dict[str, Any]:
        """List all available task types"""
        return {
            "success": True,
            "available_tasks": list(self.task_model_mapping.keys()),
            "task_descriptions": {
                "code_analysis": "Analyzing and reviewing code",
                "code_generation": "Generating new code",
                "reasoning": "Complex reasoning tasks",
                "content_analysis": "Analyzing text content",
                "fast_response": "Quick responses with small models",
                "vision": "Image and vision tasks",
                "translation": "Language translation",
                "general": "General purpose tasks"
            }
        }


# MCP Server implementation
async def main():
    """Main MCP server function"""
    manager = ModelManager()
    
    # Handle MCP commands
    while True:
        try:
            # Read command from stdin
            command = input().strip()
            
            if command.startswith("recommend_model"):
                # Parse command: recommend_model task="code analysis" speed_priority=true max_size="8B"
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    # Simple parsing for demo
                    task = "general"
                    speed_priority = False
                    max_size = None
                    
                    args = parts[1]
                    if "task=" in args:
                        task = args.split('task="')[1].split('"')[0]
                    if "speed_priority=true" in args:
                        speed_priority = True
                    if "max_size=" in args:
                        max_size = args.split('max_size="')[1].split('"')[0]
                    
                    result = await manager.recommend_model(task, speed_priority, max_size)
                    print(json.dumps(result, indent=2))
                else:
                    result = await manager.recommend_model("general")
                    print(json.dumps(result, indent=2))
            
            elif command.startswith("get_model_performance"):
                model_name = command.split(" ", 1)[1] if " " in command else "deepseek-r1-0528-qwen3-8b"
                result = await manager.get_model_performance(model_name)
                print(json.dumps(result, indent=2))
            
            elif command == "list_tasks":
                result = await manager.list_available_tasks()
                print(json.dumps(result, indent=2))
            
            elif command == "help":
                print(json.dumps({
                    "available_commands": [
                        'recommend_model task="code analysis" speed_priority=true max_size="8B"',
                        "get_model_performance <model_name>",
                        "list_tasks",
                        "help"
                    ],
                    "description": "Model Manager MCP Server"
                }, indent=2))
            
            else:
                print(json.dumps({
                    "error": "Unknown command",
                    "available_commands": ["recommend_model", "get_model_performance", "list_tasks", "help"]
                }, indent=2))
                
        except EOFError:
            break
        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main()) 