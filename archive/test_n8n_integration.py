#!/usr/bin/env python
"""
Test n8n integration functionality
"""

from n8n_integration import N8nIntegration
import json

def test_n8n_integration():
    """Test the n8n integration functionality."""
    
    print("Testing N8nIntegration...")
    
    # Create integration instance
    n8n = N8nIntegration()
    print("✓ N8n integration created")
    
    # Test webhook data processing
    test_webhook_data = {
        "type": "summary",  # Use valid data type
        "content": "Test webhook data from n8n",
        "source": "n8n_webhook",
        "metadata": {
            "webhook_id": "test_123",
            "origin": "n8n"
        },
        "timestamp": "2025-01-18T10:00:00Z"
    }
    
    try:
        result = n8n.process_webhook_data(test_webhook_data)
        print("✓ Webhook processing completed")
        print(f"DEBUG: Webhook result: {result}")
        
        if result.get('status') == 'success':
            print("✓ Webhook processing successful")
            print(f"✓ File created: {result.get('file_path', 'N/A')}")
            print(f"✓ Hash: {result.get('hash', 'N/A')}")
            print(f"✓ Git commit: {result.get('git_commit', 'N/A')}")
        else:
            print("✗ Webhook processing failed")
            print(f"  Error: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error during webhook processing: {str(e)}")
    
    # Test workspace validation
    try:
        validation_result = n8n.validate_workspace()
        print("✓ Workspace validation completed")
        print(f"DEBUG: Validation result: {validation_result}")
        
        if validation_result.get('validation_passed'):
            print("✓ Workspace validation passed")
        else:
            print("✗ Workspace validation failed")
            if validation_result.get('errors'):
                print(f"  Errors: {validation_result['errors'][:200]}...")
            
    except Exception as e:
        print(f"✗ Error during workspace validation: {str(e)}")
    
    # Test git status
    try:
        git_result = n8n.git_status()
        print("✓ Git status check completed")
        print(f"DEBUG: Git result: {git_result}")
        
        if git_result.get('status') == 'success':
            print("✓ Git status successful")
            print(f"  Current branch: {git_result.get('current_branch', 'N/A')}")
            print(f"  Recent commits: {len(git_result.get('recent_commits', []))}")
            print(f"  Has changes: {git_result.get('has_changes', False)}")
        else:
            print("✗ Git status failed")
            print(f"  Error: {git_result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error during git status check: {str(e)}")
    
    print("\nN8n Integration Test Complete!")

if __name__ == "__main__":
    test_n8n_integration()