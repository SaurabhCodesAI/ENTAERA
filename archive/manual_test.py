#!/usr/bin/env python
"""
Quick manual test for terminal usage
"""

from src.vertexautogpt.core.data_processor import VertexDataProcessor

def main():
    print("Testing manual data processing...")
    
    dp = VertexDataProcessor()
    result = dp.process_data(
        content="Testing from terminal command - this is working!",
        source="terminal_test", 
        data_type="summary"
    )
    
    print(f"✓ File created: {result['file_path']}")
    print(f"✓ Hash: {result['hash']}")
    print(f"✓ Timestamp: {result['timestamp']}")
    print("✓ Data processing successful!")

if __name__ == "__main__":
    main()