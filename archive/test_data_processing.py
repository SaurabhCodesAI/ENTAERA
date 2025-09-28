#!/usr/bin/env python
"""
Test data processing functionality
"""

from src.vertexautogpt.core.data_processor import VertexDataProcessor

def test_data_processing():
    """Test the data processor with sample data."""
    
    print("Testing VertexDataProcessor...")
    
    # Create processor instance
    dp = VertexDataProcessor()
    print("✓ Data processor created")
    
    # Test data processing
    test_content = "This is a test message for data processing validation"
    test_source = "manual_test"
    test_type = "summary"  # Use valid data type
    
    try:
        result = dp.process_data(test_content, test_source, test_type)
        print("✓ Data processing completed")
        
        # Check result structure
        if isinstance(result, dict):
            print("✓ Result is dictionary")
            
            # Check top-level structure
            if result.get('success'):
                print("✓ Processing successful")
            
            if 'file_path' in result:
                print(f"✓ File created: {result['file_path']}")
            
            if 'hash' in result:
                print(f"✓ Hash generated: {result['hash']}")
            
            # Check payload structure
            payload = result.get('payload', {})
            if payload:
                print("✓ Payload present")
                
                # Check for expected keys in payload
                expected_keys = ['type', 'content', 'source', 'metadata', 'timestamp']
                for key in expected_keys:
                    if key in payload:
                        print(f"✓ Payload has {key}")
                    else:
                        print(f"✗ Payload missing {key}")
            
            print(f"\nProcessing Results:")
            print(f"  Success: {result.get('success', False)}")
            print(f"  Hash: {result.get('hash', 'N/A')}")
            print(f"  File: {result.get('file_path', 'N/A')}")
            print(f"  Payload type: {payload.get('type', 'N/A')}")
            print(f"  Payload source: {payload.get('source', 'N/A')}")
            print(f"  Content length: {len(payload.get('content', ''))}")
            print(f"  Timestamp: {result.get('timestamp', 'N/A')}")
            
        else:
            print(f"✗ Unexpected result type: {type(result)}")
            
    except Exception as e:
        print(f"✗ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_processing()