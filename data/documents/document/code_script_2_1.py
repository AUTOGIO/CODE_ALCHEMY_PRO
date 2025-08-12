#!/usr/bin/env python3
"""
Sample Python script for demonstration
"""

import os
import json
from pathlib import Path

def process_files():
    """Process files in the documents directory"""
    docs_dir = Path("data/documents")
    
    for file_path in docs_dir.glob("*.txt"):
        with open(file_path, 'r') as f:
            content = f.read()
            print(f"Processing: {file_path.name}")
            # Process content here
    
    return "Files processed successfully"

if __name__ == "__main__":
    result = process_files()
    print(result)