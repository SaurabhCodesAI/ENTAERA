#!/usr/bin/env python
"""
Simple test runner for VertexAutoGPT
Validates all core components and functionality
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def run_test(name, command, description=""):
    """Run a single test and return results."""
    print(f"\n{name}:")
    print(f"  {description}")
    print("  " + "-" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print(f"  ✅ PASSED")
            if result.stdout.strip():
                # Only show first few lines to avoid clutter
                lines = result.stdout.strip().split('\n')[:3]
                for line in lines:
                    print(f"     {line}")
            return True
        else:
            print(f"  ❌ FAILED")
            if result.stderr:
                print(f"     Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("VertexAutoGPT Test Runner")
    print("=" * 60)
    
    # Use the virtual environment Python
    python_path = "C:/Users/saurabh/VertexAutoGPT/.venv/Scripts/python.exe"
    
    tests = [
        {
            "name": "1. Phase 1 Validation",
            "command": f'"{python_path}" phase1_validation.py',
            "description": "15-point validation checklist"
        },
        {
            "name": "2. Canvas Workflow", 
            "command": f'"{python_path}" canvas_validation.py',
            "description": "12-component workflow validation"
        },
        {
            "name": "3. Data Processor Import",
            "command": f'"{python_path}" -c "from src.vertexautogpt.core.data_processor import VertexDataProcessor; print(\\"Data processor imported successfully\\")"',
            "description": "Core module loading test"
        },
        {
            "name": "4. Schema Validation",
            "command": f'"{python_path}" -c "import json; schema = json.load(open(\\"docs/schema.json\\", \\"r\\", encoding=\\"utf-8\\")); print(f\\"Schema loaded\\")"',
            "description": "JSON schema structure check"
        },
        {
            "name": "5. n8n Integration",
            "command": f'"{python_path}" -c "from n8n_integration import N8nIntegration; print(\\"n8n integration ready\\")"',
            "description": "n8n compatibility layer"
        }
    ]
    
    results = []
    for test in tests:
        success = run_test(test["name"], test["command"], test["description"])
        results.append(success)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    # Quick file structure check
    print("\nFile Structure Check:")
    critical_files = [
        "phase1_validation.py",
        "canvas_validation.py", 
        "src/vertexautogpt/core/data_processor.py",
        "docs/schema.json",
        "n8n_integration.py"
    ]
    
    for file in critical_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")

if __name__ == "__main__":
    main()