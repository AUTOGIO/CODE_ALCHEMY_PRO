#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Run All Examples
Master script to execute all 5 real-world usage examples
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def run_example(example_number: int, example_name: str):
    """Run a specific example"""
    print(f"\n{'='*80}")
    print(f"🚀 EXAMPLE {example_number}: {example_name}")
    print(f"{'='*80}")
    
    example_file = f"examples/{example_number:02d}_{example_name}.py"
    
    if Path(example_file).exists():
        try:
            # Run the example
            result = subprocess.run([sys.executable, example_file], 
                                 capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Example completed successfully!")
                print(f"📊 Output: {len(result.stdout)} characters")
            else:
                print(f"❌ Example failed with return code: {result.returncode}")
                print(f"🔍 Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Example timed out after 5 minutes")
        except Exception as e:
            print(f"❌ Error running example: {e}")
    else:
        print(f"❌ Example file not found: {example_file}")


async def run_async_example(example_number: int, example_name: str):
    """Run an async example"""
    print(f"\n{'='*80}")
    print(f"🚀 EXAMPLE {example_number}: {example_name}")
    print(f"{'='*80}")
    
    example_file = f"examples/{example_number:02d}_{example_name}.py"
    
    if Path(example_file).exists():
        try:
            # Import and run the async example
            if example_number == 3:
                # AI Model Optimization (async)
                import importlib.util
                spec = importlib.util.spec_from_file_location("ai_model_optimization", example_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                await module.ai_model_optimization_project()
            elif example_number == 5:
                # Workflow Orchestration (async)
                import importlib.util
                spec = importlib.util.spec_from_file_location("workflow_orchestration", example_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                await module.workflow_orchestration_project()
            else:
                print(f"❌ Async example {example_number} not implemented")
                
        except Exception as e:
            print(f"❌ Error running async example: {e}")
    else:
        print(f"❌ Example file not found: {example_file}")


def main():
    """Run all examples sequentially"""
    print("🎯 CODE_ALCHEMY Professional - Running All Examples")
    print("=" * 80)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 System: {os.uname().nodename}")
    print(f"🐍 Python: {sys.version}")
    
    # Define all examples
    examples = [
        (1, "code_analysis_project"),
        (2, "document_processing"),
        (3, "ai_model_optimization"),
        (4, "security_monitoring"),
        (5, "workflow_orchestration")
    ]
    
    start_time = datetime.now()
    successful_examples = 0
    total_examples = len(examples)
    
    print(f"\n📋 Running {total_examples} examples...")
    
    for example_num, example_name in examples:
        try:
            if example_num in [3, 5]:  # Async examples
                asyncio.run(run_async_example(example_num, example_name))
            else:  # Sync examples
                run_example(example_num, example_name)
            
            successful_examples += 1
            
        except Exception as e:
            print(f"❌ Failed to run example {example_num}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Successful examples: {successful_examples}/{total_examples}")
    print(f"❌ Failed examples: {total_examples - successful_examples}/{total_examples}")
    print(f"⏱️ Total duration: {duration}")
    print(f"📈 Success rate: {successful_examples/total_examples*100:.1f}%")
    
    # Check generated files
    print(f"\n📁 Generated Files:")
    examples_dir = Path("examples")
    if examples_dir.exists():
        for subdir in examples_dir.iterdir():
            if subdir.is_dir() and subdir.name.endswith("_project"):
                files = list(subdir.glob("*.json"))
                if files:
                    print(f"   📂 {subdir.name}: {len(files)} reports")
    
    print(f"\n🎉 All examples completed!")
    print(f"📊 Dashboard available at: http://localhost:8501")


if __name__ == "__main__":
    main() 