# -*- coding: utf-8 -*-
import sys
import json

def main():
    # Create a dictionary with your data
    output_data = {
        "status": "success",
        "message": "🔥 VertexAutoGPT CLI is alive! 🔥",
        "python_executable": sys.executable
    }
    
    # Print the dictionary as a JSON string
    print(json.dumps(output_data))

if __name__ == "__main__":
    main()