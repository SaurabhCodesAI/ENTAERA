#!/usr/bin/env python3
"""
Ultra-simple n8n processor that reads from stdin - Fixed version
"""
import sys
import json
import os
from pathlib import Path

# Ensure we're in the right directory and path
project_root = Path(__file__).parent.absolute()
os.chdir(project_root)
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

def main():
    try:
        # Read and parse input
        input_data = sys.stdin.read().strip()
        if not input_data:
            return {"status": "error", "message": "No input data", "n8n_compatible": True}
        
        data = json.loads(input_data)
        
        # Use file-based processing as fallback since imports are problematic
        import subprocess
        temp_file = 'n8n_temp_input.json'
        
        # Write data to temp file
        with open(temp_file, 'w') as f:
            json.dump(data, f)
        
        # Use the working file processor
        cmd = [sys.executable, 'n8n_processor_file.py', temp_file]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except:
                return {"status": "success", "message": "Processed successfully", "stdout": result.stdout, "n8n_compatible": True}
        else:
            return {"status": "error", "message": result.stderr or "Processing failed", "returncode": result.returncode, "n8n_compatible": True}
            
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Invalid JSON: {str(e)}", "error_type": "JSONDecodeError", "n8n_compatible": True}
    except Exception as e:
        return {"status": "error", "message": str(e), "error_type": type(e).__name__, "n8n_compatible": True}
if __name__ == "__main__":
    result = main()
    print(json.dumps(result))
    sys.exit(0 if result.get("status") == "success" else 1)