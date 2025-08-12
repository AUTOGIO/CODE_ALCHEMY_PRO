#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Apple Silicon Optimized Detector Agent
Integrated with the CODE_ALCHEMY Professional multi-agent system
"""

import sys
import requests
import concurrent.futures
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import time
import platform
import subprocess

# Project-specific imports
from src.core.config import config
from config.settings import MODELS, MODEL_CONFIGS, TASK_MODEL_MAPPING
from ..base.agent_interface import BaseAgent

# Add project root to path (moved after imports)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class AppleSiliconCapabilities:
    """Apple Silicon hardware capabilities"""
    neural_engine_cores: int = 16
    neural_engine_ops_per_sec: int = 18_000_000_000_000  # 18 trillion
    unified_memory_gb: int = 16
    cpu_cores: int = 8
    gpu_cores: int = 10
    is_apple_silicon: bool = False

class AppleSiliconDetectorAgent(BaseAgent):
    """Apple Silicon optimized detector agent for CODE_ALCHEMY Professional"""
    
    def __init__(self):
        super().__init__("Apple Silicon Detector")
        
        # Configuration
        self.api_base = config.models.server_url + "/v1"
        self.models = MODELS
        self.configs = MODEL_CONFIGS
        self.task_mapping = TASK_MODEL_MAPPING
        self.session = requests.Session()
        self.session.timeout = 60
        
        # Capabilities
        self.capabilities = self._detect_apple_silicon()
        self._optimize_for_apple_silicon()
        
        # Metadata
        self.agent_type = "analysis"
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        operation = parameters.get('operation', 'run_analysis')
        document_folder = Path(parameters.get('document_folder', 'data/documents'))
        output_folder = Path(parameters.get('output_folder', 'data/reports'))
        
        if operation == 'run_analysis':
            return self.run_analysis(document_folder, output_folder)
        elif operation == 'analyze_documents':
            return self.analyze_documents(document_folder)
        elif operation == 'get_agent_info':
            return self.get_agent_info()
        else:
            return {
                'success': False,
                'error': f'Unknown operation: {operation}',
                'supported_operations': [
                    'run_analysis', 'analyze_documents', 'get_agent_info'
                ]
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return self.get_health_metrics()
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and supported operations"""
        return {
            'name': self.agent_name,
            'capabilities': vars(self.capabilities),
            'supported_operations': [
                'run_analysis', 'analyze_documents', 'get_agent_info'
            ],
            'apple_silicon_optimized': self.capabilities.is_apple_silicon,
            'workflow_triggers': self.get_workflow_triggers()
        }
    
    def _detect_apple_silicon(self) -> AppleSiliconCapabilities:
        """Detect Apple Silicon capabilities"""
        capabilities = AppleSiliconCapabilities()
        
        if platform.machine() == 'arm64' and platform.system() == 'Darwin':
            capabilities.is_apple_silicon = True
            print("🍎 Apple Silicon detected!")
            
            try:
                # Processor info
                result = subprocess.run(
                    ['sysctl', '-n', 'machdep.cpu.brand_string'],
                    capture_output=True, text=True
                )
                if 'Apple' in result.stdout:
                    print("✅ Apple M-series chip confirmed")
                
                # Memory info
                result = subprocess.run(
                    ['sysctl', '-n', 'hw.memsize'],
                    capture_output=True, text=True
                )
                if result.stdout:
                    memory_bytes = int(result.stdout.strip())
                    capabilities.unified_memory_gb = memory_bytes // (1024**3)
                    print(f"💾 Unified Memory: {capabilities.unified_memory_gb} GB")
                
                # CPU core count
                result = subprocess.run(
                    ['sysctl', '-n', 'hw.ncpu'],
                    capture_output=True, text=True
                )
                if result.stdout:
                    capabilities.cpu_cores = int(result.stdout.strip())
                    print(f"🖥️  CPU Cores: {capabilities.cpu_cores}")
                
            except Exception as e:
                print(f"⚠️  Could not get detailed system info: {e}")
        
        return capabilities
    
    def _optimize_for_apple_silicon(self):
        """Optimize configuration for Apple Silicon"""
        if not self.capabilities.is_apple_silicon:
            print("⚠️  Not running on Apple Silicon - using standard configuration")
            return
        
        print("🚀 Optimizing for Apple Silicon...")
        
        # Use CODE_ALCHEMY M3 optimization settings
        m3_config = config.m3_optimization
        optimal_workers = min(self.capabilities.cpu_cores, m3_config.core_utilization)
        print(f"⚡ Parallel workers optimized to: {optimal_workers}")
        
        # Optimize model configurations
        for model_key, model_config in self.configs.items():
            if self.capabilities.unified_memory_gb >= 16:
                model_config['max_tokens'] = min(model_config['max_tokens'] * 1.5, 2000)
                print(f"📈 Increased {model_key} tokens to {model_config['max_tokens']}")
        
        # Optimize timeouts
        for model_key, model_config in self.configs.items():
            model_config['timeout'] = max(model_config['timeout'] * 0.7, 20)
            print(f"⚡ Reduced {model_key} timeout to {model_config['timeout']}s")
    
    def call_model_with_neural_optimization(self, model_key: str, prompt: str, 
                                            system_prompt: str = None) -> Dict[str, Any]:
        """Call model with Apple Silicon optimizations"""
        start_time = time.time()
        
        model_name = self.models[model_key]
        model_config = self.configs[model_key]
        
        url = f"{self.api_base}/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": model_config["max_tokens"],
            "temperature": model_config["temperature"],
            "stream": False,
            "n": 1,
        }
        
        print(f"🍎 Using Apple Silicon optimized model: {model_key} ({model_name})")
        
        try:
            response = self.session.post(
                url, json=payload, timeout=model_config["timeout"]
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                processing_time = time.time() - start_time
                
                confidence = self._calculate_apple_silicon_confidence(
                    content, model_key, processing_time
                )
                
                return {
                    "success": True,
                    "content": content,
                    "model_name": model_key,
                    "confidence": confidence,
                    "processing_time": processing_time,
                    "apple_silicon_optimized": True
                }
            else:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "processing_time": processing_time,
                "apple_silicon_optimized": True
            }
    
    def _calculate_apple_silicon_confidence(self, response: str, model_key: str, 
                                          processing_time: float) -> float:
        """Calculate confidence optimized for Apple Silicon performance"""
        if not response or len(response) < 10:
            return 0.0
        
        # Base confidence from model type
        base_confidence = {
            "primary": 0.8,
            "fast": 0.6,
            "reasoning": 0.7,
            "analysis": 0.9
        }.get(model_key, 0.5)
        
        # Apple Silicon performance boost
        if self.capabilities.is_apple_silicon:
            base_confidence *= 1.1  # 10% boost for Apple Silicon
        
        # Adjust based on response quality and processing speed
        length_factor = min(len(response) / 100, 1.0)
        quality_factor = 1.0 if "error" not in response.lower() else 0.3
        
        # Apple Silicon speed factor (faster processing = higher confidence)
        speed_factor = 1.0
        if processing_time < 5.0:  # Very fast
            speed_factor = 1.2
        elif processing_time < 10.0:  # Fast
            speed_factor = 1.1
        elif processing_time > 30.0:  # Slow
            speed_factor = 0.8
        
        confidence = base_confidence * length_factor * quality_factor * speed_factor
        return min(confidence, 1.0)
    
    def analyze_documents(self, document_folder: Path) -> Dict[str, Any]:
        """Analyze documents using Apple Silicon optimizations"""
        docs = list(document_folder.glob("*"))
        if not docs:
            return {"success": False, "error": "No documents found"}
        
        print(f"📄 Analyzing {len(docs)} documents with Apple Silicon optimization...")
        
        # Create analysis tasks optimized for Neural Engine
        tasks = []
        for doc in docs:
            try:
                with open(doc, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Optimize content length for Neural Engine
                max_content_length = 2000 if self.capabilities.is_apple_silicon else 500
                optimized_content = content[:max_content_length]
                
                # Fast analysis
                fast_prompt = f"Resuma rapidamente este documento: {optimized_content}..."
                tasks.append(("fast", fast_prompt, "Você é um assistente de análise rápida."))
                
                # Detailed analysis
                detailed_prompt = f"Analise detalhadamente este documento: {optimized_content}"
                tasks.append(("primary", detailed_prompt, "Você é um especialista em análise de documentos."))
                
            except Exception as e:
                print(f"⚠️  Error reading {doc}: {e}")
        
        # Execute tasks in parallel with Apple Silicon optimization
        optimal_workers = min(self.capabilities.cpu_cores, config.m3_optimization.core_utilization) if self.capabilities.is_apple_silicon else 4
        
        print(f"🍎 Using {optimal_workers} parallel workers (Apple Silicon optimized)")
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=optimal_workers) as executor:
            future_to_task = {
                executor.submit(self.call_model_with_neural_optimization, model, prompt, system): (model, prompt)
                for model, prompt, system in tasks
            }
            
            for future in concurrent.futures.as_completed(future_to_task):
                model, prompt = future_to_task[future]
                try:
                    result = future.result()
                    results[f"{model}_{len(results)}"] = result
                except Exception as e:
                    print(f"❌ Task failed: {e}")
        
        return results
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information for CODE_ALCHEMY Professional"""
        return {
            "name": self.agent_name,
            "type": self.agent_type,
            "enabled": self.enabled,
            "capabilities": {
                "apple_silicon": self.capabilities.is_apple_silicon,
                "neural_engine_cores": self.capabilities.neural_engine_cores,
                "unified_memory_gb": self.capabilities.unified_memory_gb,
                "cpu_cores": self.capabilities.cpu_cores
            },
            "models": list(self.models.keys()),
            "optimizations": {
                "neural_engine_enabled": config.m3_optimization.neural_engine_enabled,
                "parallel_processing": config.m3_optimization.parallel_processing,
                "dynamic_caching": config.m3_optimization.dynamic_caching
            }
        }
    
    def run_analysis(self, document_folder: Path, output_folder: Path) -> Dict[str, Any]:
        """Run Apple Silicon optimized analysis"""
        print("🚀 CODE_ALCHEMY Professional - Apple Silicon Optimized Analysis")
        print("=" * 70)
        
        if self.capabilities.is_apple_silicon:
            print("🍎 Apple Silicon detected - using optimized configuration")
            print(f"🧠 Neural Engine: {self.capabilities.neural_engine_cores} cores")
            print(f"💾 Unified Memory: {self.capabilities.unified_memory_gb} GB")
            print(f"🖥️  CPU Cores: {self.capabilities.cpu_cores}")
        else:
            print("⚠️  Apple Silicon not detected - using standard configuration")
        
        start_time = time.time()
        
        try:
            # Analyze documents
            results = self.analyze_documents(document_folder)
            
            total_time = time.time() - start_time
            successful_results = [r for r in results.values() if r.get("success")]
            
            print(f"\n✅ Apple Silicon analysis complete!")
            print(f"📊 Total analyses: {len(results)}")
            print(f"📊 Successful: {len(successful_results)}")
            
            if successful_results:
                avg_confidence = sum(r.get('confidence', 0) for r in successful_results) / len(successful_results)
                print(f"📊 Average confidence: {avg_confidence:.1%}")
            
            print(f"⏱️  Total time: {total_time:.1f}s")
            print(f"🍎 Apple Silicon optimized: {'✅' if self.capabilities.is_apple_silicon else '❌'}")
            
            return {
                "success": True,
                "total_analyses": len(results),
                "successful_analyses": len(successful_results),
                "average_confidence": sum(r.get('confidence', 0) for r in successful_results) / len(successful_results) if successful_results else 0,
                "total_time": total_time,
                "apple_silicon_optimized": self.capabilities.is_apple_silicon,
                "results": results
            }
            
        except Exception as e:
            print(f"❌ Error during Apple Silicon analysis: {e}")
            return {"success": False, "error": str(e)}


# Agent factory function for CODE_ALCHEMY Professional
def create_apple_silicon_detector_agent() -> AppleSiliconDetectorAgent:
    """Create and return an Apple Silicon detector agent"""
    return AppleSiliconDetectorAgent() 