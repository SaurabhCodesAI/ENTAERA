#!/usr/bin/env python3
"""
N8N Debug Processor - Shows exactly what data n8n is sending
"""

import sys
import json
from pathlib import Path

def main():
    print("=== N8N DEBUG PROCESSOR ===")
    
    # Show command line arguments
    print(f"Number of arguments: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Arg {i}: {repr(arg)}")
    
    # Try to read from stdin
    try:
        stdin_data = sys.stdin.read()
        print(f"STDIN data: {repr(stdin_data)}")
    except:
        print("No STDIN data")
    
    # Try to parse as JSON
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
            print(f"Parsed JSON: {json.dumps(data, indent=2)}")
        except Exception as e:
            print(f"JSON parse error: {e}")
    
    # Return success
    result = {
        "status": "debug_complete",
        "message": "Check output for debug info",
        "n8n_compatible": True
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()