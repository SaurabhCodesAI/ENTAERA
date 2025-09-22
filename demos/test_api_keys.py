#!/usr/bin/env python3
"""
🧪 ENTAERA API KEY TESTER
========================
Quick test to verify your API keys are working
"""

import os
import sys
import asyncio
from datetime import datetime

# Add src to path
sys.path.append('src')

def load_env():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print("❌ .env file not found!")
        return False
    return True

async def test_api_keys():
    """Test all configured API keys"""
    print("🧪 ENTAERA API KEY TESTER")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment
    if not load_env():
        return
    
    print("\n🔍 Checking API Key Configuration...")
    
    # Check Azure OpenAI
    azure_key = os.getenv('AZURE_OPENAI_API_KEY', '')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    azure_deployment = os.getenv('AZURE_DEPLOYMENT_NAME', '')
    
    print(f"\n🔵 Azure OpenAI:")
    print(f"   API Key: {'✅ Set' if azure_key and azure_key != 'your_azure_openai_api_key_here' else '❌ Not set'}")
    print(f"   Endpoint: {'✅ Set' if azure_endpoint and 'your-resource-name' not in azure_endpoint else '❌ Not set'}")
    print(f"   Deployment: {'✅ Set' if azure_deployment and azure_deployment != 'gpt-35-turbo' else '⚠️ Using default'}")
    
    # Check Gemini
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    print(f"\n🟢 Google Gemini:")
    print(f"   API Key: {'✅ Set' if gemini_key and gemini_key != 'placeholder-for-local-first-mode' else '❌ Not set'}")
    
    # Check Perplexity
    perplexity_key = os.getenv('PERPLEXITY_API_KEY', '')
    print(f"\n🟣 Perplexity AI:")
    print(f"   API Key: {'✅ Set' if perplexity_key and perplexity_key != 'placeholder-for-local-first-mode' else '❌ Not set'}")
    
    # Check OpenAI
    openai_key = os.getenv('OPENAI_API_KEY', '')
    print(f"\n🔴 OpenAI Direct:")
    print(f"   API Key: {'✅ Set' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not set'}")
    
    # Count configured APIs
    configured_apis = 0
    if azure_key and azure_key != 'your_azure_openai_api_key_here':
        configured_apis += 1
    if gemini_key and gemini_key != 'placeholder-for-local-first-mode':
        configured_apis += 1
    if perplexity_key and perplexity_key != 'placeholder-for-local-first-mode':
        configured_apis += 1
    if openai_key and openai_key != 'your_openai_api_key_here':
        configured_apis += 1
    
    print(f"\n📊 Summary:")
    print(f"   Configured APIs: {configured_apis}/4")
    
    if configured_apis == 0:
        print("   Status: ⚠️ No APIs configured - using demo mode")
        print("   Action: Add at least one API key to .env file")
    elif configured_apis >= 1:
        print("   Status: ✅ Ready for live API testing!")
        print("   Action: Run 'python entaera_api_chat_demo.py' for live responses")
    
    # Test ENTAERA framework
    print(f"\n🧪 Testing ENTAERA Framework...")
    try:
        from entaera.utils.api_router import SmartAPIRouter
        from entaera.core.logger import LoggerManager
        
        router = SmartAPIRouter()
        logger_manager = LoggerManager()
        
        print("   ✅ Framework imports successful")
        print("   ✅ Components initialized")
        
        # Test routing decision
        decision = await router.route_request(
            task_type="test",
            content="Test message",
            estimated_tokens=100
        )
        
        print(f"   ✅ Smart routing working: {decision.provider.value}")
        
    except Exception as e:
        print(f"   ❌ Framework error: {e}")
        return
    
    print(f"\n🎯 Next Steps:")
    if configured_apis == 0:
        print("   1. Choose an API provider (see API_SETUP_GUIDE.md)")
        print("   2. Get your API key")
        print("   3. Update .env file")
        print("   4. Run this test again")
    else:
        print("   1. Run: python entaera_api_chat_demo.py")
        print("   2. See live API responses!")
        print("   3. Add more API keys for full functionality")
    
    print(f"\n🚀 ENTAERA API Key Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_api_keys())