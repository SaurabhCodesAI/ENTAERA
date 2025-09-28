#!/usr/bin/env python3
"""
N8N Direct Processor - Handles n8n webhook data without PowerShell JSON parsing issues
Reads data directly from environment variables set by n8n
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.vertexautogpt.services.n8n_integration import N8nIntegration
except ImportError:
    try:
        from vertexautogpt.services.n8n_integration import N8nIntegration
    except ImportError:
        print("Error: Could not import N8nIntegration. Please check your Python path.")
        sys.exit(1)

def main():
    try:
        # Try to read from command line arguments (n8n passes data as arguments)
        if len(sys.argv) > 1:
            # n8n passed data as command line argument
            data_str = sys.argv[1]
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from argument: {e}")
                print(f"Raw data: {data_str}")
                sys.exit(1)
        else:
            # Fallback: try reading from stdin
            try:
                data_str = sys.stdin.read().strip()
                if not data_str:
                    print("Error: No data received from stdin or arguments")
                    sys.exit(1)
                data = json.loads(data_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from stdin: {e}")
                sys.exit(1)
        
        # Initialize the N8N integration
        processor = N8nIntegration()
        
        # Process the data
        result = processor.process_webhook_data(data)
        
        # Output result as JSON for n8n
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Processing failed: {str(e)}",
            "n8n_compatible": True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()