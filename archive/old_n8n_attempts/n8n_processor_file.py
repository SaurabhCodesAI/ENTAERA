#!/usr/bin/env python
"""
n8n webhook processor - file-based approach
This reads from a temp file to avoid JSON escaping issues
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
    
    # Try to read from temp file first
    temp_file = Path("n8n_temp_data.json")
    if temp_file.exists():
        try:
            # Try different encodings
            for encoding in ['utf-8', 'utf-16', 'utf-8-sig']:
                try:
                    with open(temp_file, 'r', encoding=encoding) as f:
                        content = f.read().strip()
                        if content:
                            webhook_data = json.loads(content)
                            break
                except UnicodeDecodeError:
                    continue
                except json.JSONDecodeError:
                    continue
            else:
                raise ValueError("Could not decode temp file")
        finally:
            # Clean up temp file
            temp_file.unlink()
    else:
        # Fallback: use command line argument or test data
        if len(sys.argv) > 1:
            # Try to parse argument
            webhook_data = json.loads(sys.argv[1])
        else:
            # Ultimate fallback
            webhook_data = {
                "content": "n8n integration test - file-based processor working",
                "source": "n8n-file-processor",
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