#!/usr/bin/env python
"""
Simple validation runner - ASCII only for Windows compatibility
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Run basic validation tests."""
    print("VertexAutoGPT Validation Results")
    print("=" * 50)
    
    # Test 1: Check file structure
    print("\n1. File Structure Check:")
    critical_files = [
        "src/vertexautogpt/core/data_processor.py",
        "docs/schema.json", 
        "phase1_validation.py",
        "canvas_validation.py",
        "n8n_integration.py"
    ]
    
    structure_ok = True
    for file in critical_files:
        if Path(file).exists():
            print(f"   [OK] {file}")
        else:
            print(f"   [MISSING] {file}")
            structure_ok = False
    
    # Test 2: Data processor import
    print("\n2. Core Module Test:")
    try:
        from src.vertexautogpt.core.data_processor import VertexDataProcessor
        print("   [OK] Data processor imports successfully")
        
        # Try to create instance
        dp = VertexDataProcessor()
        print("   [OK] Data processor instance created")
        
    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        
    # Test 3: Schema validation
    print("\n3. Schema Validation:")
    try:
        import json
        with open("docs/schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)
        print(f"   [OK] Schema loaded - {len(schema.get('required', []))} required fields")
        
        # Check required fields
        required = schema.get('required', [])
        expected = ['type', 'content', 'source', 'metadata', 'timestamp']
        if all(field in required for field in expected):
            print("   [OK] All expected fields present")
        else:
            print("   [WARNING] Missing some expected fields")
            
    except Exception as e:
        print(f"   [ERROR] {str(e)}")
    
    # Test 4: n8n integration
    print("\n4. n8n Integration:")
    try:
        from n8n_integration import N8nIntegration
        print("   [OK] n8n integration module loads")
        
        n8n = N8nIntegration()
        print("   [OK] n8n integration instance created")
        
    except Exception as e:
        print(f"   [ERROR] {str(e)}")
    
    # Test 5: Data directory check
    print("\n5. Data Directory Structure:")
    data_dirs = ["data", "data/summary", "data/raw", "data/embeddings"]
    for dir_path in data_dirs:
        if Path(dir_path).exists():
            file_count = len(list(Path(dir_path).glob("*.json")))
            print(f"   [OK] {dir_path} - {file_count} JSON files")
        else:
            print(f"   [MISSING] {dir_path}")
    
    # Summary count
    summary_files = list(Path("data/summary").glob("*.json")) if Path("data/summary").exists() else []
    print(f"\n6. Summary Files: {len(summary_files)} found")
    if len(summary_files) > 0:
        print("   [OK] Summary data available for processing")
    else:
        print("   [INFO] No summary files found")
    
    print("\n" + "=" * 50)
    print("VALIDATION COMPLETE")
    print("=" * 50)
    
    if structure_ok:
        print("Core structure: READY")
    else:
        print("Core structure: NEEDS ATTENTION")
    
    print("\nTo run comprehensive tests:")
    print("   python test_runner.py")
    print("\nTo test specific components:")
    print("   python -c \"from src.vertexautogpt.core.data_processor import VertexDataProcessor; dp = VertexDataProcessor(); print('Ready')\"")

if __name__ == "__main__":
    main()