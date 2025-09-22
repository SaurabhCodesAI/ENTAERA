#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_perplexity_models():
    """Check available Perplexity models"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("❌ No PERPLEXITY_API_KEY found")
        return
    
    print("🔍 Checking available Perplexity models...")
    
    # Try to get models list
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test with different model names
    test_models = [
        "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-large-128k-online", 
        "llama-3.1-sonar-huge-128k-online",
        "llama-3.1-sonar-small-128k-chat",
        "llama-3.1-sonar-large-128k-chat",
        "sonar-small-online",
        "sonar-medium-online", 
        "sonar-large-online"
    ]
    
    print("\n🧪 Testing model names...")
    
    for model in test_models:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Test"}],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ {model} - WORKS!")
                break
            else:
                error_info = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"❌ {model} - {error_info}")
                
        except Exception as e:
            print(f"❌ {model} - Exception: {e}")
    
    print("\n🔍 Checking documentation...")
    try:
        # Check if we can get any info from their API
        response = requests.get("https://api.perplexity.ai/", headers=headers, timeout=5)
        print(f"API base response: {response.status_code}")
    except:
        pass

if __name__ == "__main__":
    check_perplexity_models()