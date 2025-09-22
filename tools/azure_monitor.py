#!/usr/bin/env python3
"""
🔄 AZURE OPENAI MONITOR
======================
Keeps checking until Azure OpenAI is working with ENTAERA
"""

import os
import time
import asyncio
from datetime import datetime

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

def check_azure_config():
    """Check if Azure OpenAI is configured"""
    load_env()
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY', '')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    
    key_configured = api_key and api_key != 'your_azure_openai_api_key_here'
    endpoint_configured = endpoint and 'your-resource-name' not in endpoint
    
    return key_configured and endpoint_configured

async def test_azure_simple():
    """Simple Azure test"""
    try:
        import aiohttp
        
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-35-turbo')
        
        url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/chat/completions?api-version=2023-12-01-preview"
        
        payload = {
            "messages": [{"role": "user", "content": "Hello! Say 'Azure working with ENTAERA!'"}],
            "max_tokens": 50
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return True, data['choices'][0]['message']['content']
                    else:
                        return False, "No response content"
                else:
                    error_text = await response.text()
                    return False, f"HTTP {response.status}: {error_text[:200]}"
    except Exception as e:
        return False, f"Error: {str(e)}"

async def monitor_azure():
    """Monitor Azure OpenAI setup progress"""
    print("🔄 AZURE OPENAI MONITOR")
    print("=" * 40)
    print("Monitoring until Azure OpenAI works with ENTAERA...")
    print(f"📅 Started: {datetime.now().strftime('%H:%M:%S')}")
    
    check_count = 0
    
    while True:
        check_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n🔍 Check #{check_count} at {current_time}")
        print("-" * 30)
        
        # Check configuration
        is_configured = check_azure_config()
        
        if not is_configured:
            print("⏳ Azure OpenAI not configured yet...")
            print("💡 Waiting for you to add Azure credentials to .env")
            print("📖 See: AZURE_SETUP_GUIDE.md for instructions")
            
        else:
            print("✅ Azure OpenAI configuration found!")
            print("🧪 Testing live API connection...")
            
            # Test the API
            success, result = await test_azure_simple()
            
            if success:
                print("🎉 AZURE OPENAI IS WORKING!")
                print(f"🤖 Response: {result}")
                print("\n" + "="*40)
                print("✅ SUCCESS! Azure OpenAI + ENTAERA ready!")
                print("🚀 Run: python azure_continuous_test.py")
                print("   for full API testing!")
                break
            else:
                print(f"❌ Azure API test failed: {result}")
                print("🔧 Check your Azure credentials in .env")
        
        print(f"\n⏰ Next check in 10 seconds... (Ctrl+C to stop)")
        
        try:
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            print(f"\n\n⏹️ Monitoring stopped by user")
            print(f"📊 Total checks performed: {check_count}")
            if is_configured:
                print(f"📋 Azure is configured - run manual test:")
                print(f"   python azure_continuous_test.py")
            else:
                print(f"📋 Next step: Add Azure credentials to .env")
                print(f"📖 Guide: AZURE_SETUP_GUIDE.md")
            break

def print_current_status():
    """Print current API status"""
    load_env()
    
    print("📊 CURRENT API STATUS:")
    print("-" * 25)
    
    # Azure
    azure_key = os.getenv('AZURE_OPENAI_API_KEY', '')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    azure_configured = azure_key != 'your_azure_openai_api_key_here' and 'your-resource-name' not in azure_endpoint
    print(f"🔵 Azure OpenAI: {'✅ Configured' if azure_configured else '❌ Not configured'}")
    
    # Gemini
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    gemini_configured = gemini_key and gemini_key != 'placeholder-for-local-first-mode'
    print(f"🟢 Gemini: {'✅ Configured' if gemini_configured else '❌ Not configured'}")
    
    # Perplexity
    perplexity_key = os.getenv('PERPLEXITY_API_KEY', '')
    perplexity_configured = perplexity_key and perplexity_key != 'placeholder-for-local-first-mode'
    print(f"🟣 Perplexity: {'✅ Configured' if perplexity_configured else '❌ Not configured'}")
    
    total_configured = sum([azure_configured, gemini_configured, perplexity_configured])
    print(f"\n📈 Total APIs configured: {total_configured}/3")
    
    if azure_configured:
        print("\n🎯 Ready to test Azure! Run: python azure_continuous_test.py")
    else:
        print("\n📋 Setup Azure: See AZURE_SETUP_GUIDE.md")

if __name__ == "__main__":
    print_current_status()
    print("\n" + "="*40)
    
    if check_azure_config():
        print("🚀 Azure configured! Running test...")
        asyncio.run(test_azure_simple())
    else:
        print("⏳ Starting monitor mode...")
        print("   (Will check every 10 seconds until Azure works)")
        asyncio.run(monitor_azure())