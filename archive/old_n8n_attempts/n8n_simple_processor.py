#!/usr/bin/env python3
"""
Simple n8n processor that actually works
"""
import sys
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path

def generate_hash(content):
    """Generate a simple hash for the filename"""
    return hashlib.md5(str(content).encode()).hexdigest()[:8]

def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            return {"status": "error", "message": "No input data received"}
        
        # Parse JSON
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"Invalid JSON: {str(e)}"}
        
        # Ensure we have required fields
        if "content" not in data:
            return {"status": "error", "message": "Missing required field: content"}
        
        # Set default type if not provided
        if "type" not in data:
            data["type"] = "summary"
        
        # Generate hash and filename
        content_hash = generate_hash(data["content"])
        filename = f"{content_hash}.json"
        
        # Create the output data structure
        output_data = {
            "type": data["type"],
            "content": data["content"],
            "source": data.get("source", "n8n-webhook"),
            "metadata": {
                "version": 1,
                "hash": content_hash
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "file": {
                "filename": filename,
                "mimetype": "application/json"
            }
        }
        
        # Ensure directory exists
        output_dir = Path("data/summary")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        output_path = output_dir / filename
        output_data["fileName"] = str(output_path.absolute())
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": f"File created successfully: {filename}",
            "filename": filename,
            "path": str(output_path),
            "hash": content_hash
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e), "error_type": type(e).__name__}

if __name__ == "__main__":
    result = main()
    print(json.dumps(result))
    sys.exit(0 if result.get("status") == "success" else 1)