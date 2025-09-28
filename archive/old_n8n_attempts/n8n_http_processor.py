#!/usr/bin/env python3
"""
HTTP-based processor for n8n - accepts POST requests directly
"""
import sys
import json
import os
from datetime import datetime
import hashlib
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_hash(content):
    return hashlib.md5(str(content).encode()).hexdigest()[:8]

@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Debug: log what we're receiving
        print(f"Content-Type: {request.content_type}")
        print(f"Raw data: {request.get_data()}")
        print(f"Form data: {request.form}")
        print(f"JSON data: {request.get_json()}")
        
        # Get JSON data from POST request
        data = request.get_json()
        
        if not data:
            print("No JSON data received")
            return jsonify({"status": "error", "message": "No JSON data received"}), 400
            
        if "content" not in data:
            print(f"Missing content field. Got: {data}")
            return jsonify({"status": "error", "message": "Missing required field: content"}), 400
        
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
            "source": data.get("source", "n8n-http"),
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
        
        return jsonify({
            "status": "success",
            "message": f"File created successfully: {filename}",
            "filename": filename,
            "path": str(output_path),
            "hash": content_hash
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "error_type": type(e).__name__}), 500

if __name__ == "__main__":
    # Change to the correct directory
    os.chdir(Path(__file__).parent)
    app.run(host='127.0.0.1', port=5679, debug=False)