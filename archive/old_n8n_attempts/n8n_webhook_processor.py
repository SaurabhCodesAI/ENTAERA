#!/usr/bin/env python
"""
n8n webhook processor script
This script processes webhook data from n8n and calls VertexAutoGPT
"""

import json
import sys
import os
from pathlib import Path

# Change to the correct directory
os.chdir(r'C:\Users\saurabh\VertexAutoGPT')

# Add current directory to Python path
if str(Path.cwd()) not in sys.path:
    sys.path.insert(0, str(Path.cwd()))

try:
    from n8n_integration import N8nIntegration
    
    # Read JSON data from command line argument
    if len(sys.argv) > 1:
        webhook_data_str = sys.argv[1]
        # Handle potential encoding issues
        webhook_data = json.loads(webhook_data_str)
    else:
        # Fallback test data
        webhook_data = {
            "content": "Fallback test data from n8n script",
            "source": "n8n-script-fallback",
            "type": "summary"
        }
    
    # Process with VertexAutoGPT
    n8n = N8nIntegration()
    result = n8n.process_webhook_data(webhook_data)
    
    # Output result as JSON
    print(json.dumps(result))
    
except Exception as e:
    error_result = {
        "status": "error",
        "message": str(e),
        "error_type": type(e).__name__,
        "n8n_compatible": True
    }
    print(json.dumps(error_result))
    sys.exit(1)