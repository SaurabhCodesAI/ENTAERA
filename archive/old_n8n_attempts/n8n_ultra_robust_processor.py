#!/usr/bin/env python3
"""
Ultra-robust n8n processor with comprehensive error handling
Handles all possible failure modes and edge cases
"""

import sys
import json
import os
import traceback
from pathlib import Path
import subprocess
import tempfile

def log_error(message, error=None):
    """Log errors to both console and file"""
    error_data = {
        "status": "error",
        "message": message,
        "n8n_compatible": True,
        "timestamp": None
    }
    
    if error:
        error_data["error_details"] = str(error)
        error_data["traceback"] = traceback.format_exc()
    
    try:
        from datetime import datetime
        error_data["timestamp"] = datetime.now().isoformat()
    except:
        pass
    
    print(json.dumps(error_data))
    
    # Also log to file for debugging
    try:
        with open("n8n_error.log", "a") as f:
            f.write(f"{error_data}\n")
    except:
        pass

def main():
    try:
        # Change to correct directory
        os.chdir(Path(__file__).parent)
        
        # Read input data
        try:
            if len(sys.argv) > 1:
                # From command line argument
                data_str = sys.argv[1]
            else:
                # From stdin
                data_str = sys.stdin.read().strip()
            
            if not data_str:
                log_error("No input data received")
                return 1
                
        except Exception as e:
            log_error("Failed to read input data", e)
            return 1
        
        # Parse JSON
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError as e:
            log_error(f"Invalid JSON data: {e}", e)
            return 1
        
        # Try multiple import approaches
        processor = None
        try:
            from src.vertexautogpt.services.n8n_integration import N8nIntegration
            processor = N8nIntegration()
        except ImportError:
            try:
                from vertexautogpt.services.n8n_integration import N8nIntegration
                processor = N8nIntegration()
            except ImportError:
                # Fallback to file-based processing
                try:
                    # Write to temp file and use existing processor
                    with open('n8n_temp_data.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f)
                    
                    # Run existing processor
                    result = subprocess.run([
                        sys.executable, 'n8n_processor_file.py'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(result.stdout)
                        return 0
                    else:
                        log_error(f"Processor failed: {result.stderr}")
                        return 1
                        
                except Exception as e:
                    log_error("All processing methods failed", e)
                    return 1
        
        # Process with direct integration
        if processor:
            try:
                result = processor.process_webhook_data(data)
                print(json.dumps(result))
                return 0
            except Exception as e:
                log_error("Processing failed", e)
                return 1
                
    except Exception as e:
        log_error("Unexpected error", e)
        return 1

if __name__ == "__main__":
    sys.exit(main())