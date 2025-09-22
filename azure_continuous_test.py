#!/usr/bin/env python3
"""
🔵 ENTAERA AZURE OPENAI TESTER
=============================
Keep testing until Azure OpenAI is working!
"""

import os
import sys
import asyncio
import json
import aiohttp
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

async def test_azure_openai_api(prompt):
    """Test live Azure OpenAI API call"""
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') 
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview')
    deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-35-turbo')
    
    # Check if Azure is configured
    if not api_key or api_key == 'your_azure_openai_api_key_here':
        return None, "Azure API key not configured"
    
    if not endpoint or 'your-resource-name' in endpoint:
        return None, "Azure endpoint not configured"
    
    # Build Azure OpenAI URL
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are ENTAERA AI assistant powered by Azure OpenAI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content'], None
                    else:
                        return None, "No response content"
                else:
                    error_text = await response.text()
                    return None, f"HTTP {response.status}: {error_text}"
    except Exception as e:
        return None, f"Error: {str(e)}"

async def test_perplexity_api(prompt):
    """Test live Perplexity API call with corrected endpoint"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key or api_key == 'placeholder-for-local-first-mode':
        return None, "No Perplexity API key configured"
    
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 300,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content'], None
                    else:
                        return None, "No response content"
                else:
                    error_text = await response.text()
                    return None, f"HTTP {response.status}: {error_text}"
    except Exception as e:
        return None, f"Error: {str(e)}"

async def test_gemini_api(prompt):
    """Test live Gemini API call"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'placeholder-for-local-first-mode':
        return None, "No Gemini API key configured"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        return data['candidates'][0]['content']['parts'][0]['text'], None
                    else:
                        return None, "No response content"
                else:
                    error_text = await response.text()
                    return None, f"HTTP {response.status}: {error_text}"
    except Exception as e:
        return None, f"Error: {str(e)}"

async def azure_continuous_test():
    """Keep testing Azure until it works"""
    print("🔵 ENTAERA AZURE OPENAI CONTINUOUS TESTER")
    print("=" * 55)
    print("Testing until Azure OpenAI is working!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment
    if not load_env():
        return
    
    # Import ENTAERA framework
    try:
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        from entaera.utils.api_router import SmartAPIRouter, TaskComplexity
        
        print("\n✅ ENTAERA framework loaded")
        
        # Initialize components
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Azure Test Session")
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("azure_test")
        router = SmartAPIRouter()
        
        print("✅ Components initialized")
        
    except Exception as e:
        print(f"❌ Framework error: {e}")
        return
    
    # Check current API status
    print(f"\n🔍 Current API Status Check:")
    
    azure_key = os.getenv('AZURE_OPENAI_API_KEY')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    gemini_key = os.getenv('GEMINI_API_KEY')
    perplexity_key = os.getenv('PERPLEXITY_API_KEY')
    
    print(f"   🔵 Azure OpenAI: {'✅ Configured' if azure_key and azure_key != 'your_azure_openai_api_key_here' and azure_endpoint and 'your-resource-name' not in azure_endpoint else '❌ Not configured'}")
    print(f"   🟢 Gemini: {'✅ Configured' if gemini_key and gemini_key != 'placeholder-for-local-first-mode' else '❌ Not configured'}")
    print(f"   🟣 Perplexity: {'✅ Configured' if perplexity_key and perplexity_key != 'placeholder-for-local-first-mode' else '❌ Not configured'}")
    
    # Test all APIs
    test_scenarios = [
        {
            "prompt": "Hello! This is an Azure OpenAI test. Please respond with 'Azure OpenAI working via ENTAERA!'",
            "api": "azure",
            "description": "Azure OpenAI Test"
        },
        {
            "prompt": "Hello! This is a Gemini test. Please respond with 'Gemini working via ENTAERA!'",
            "api": "gemini", 
            "description": "Gemini Backup Test"
        },
        {
            "prompt": "What are the latest tech news today? Give me 2 recent headlines.",
            "api": "perplexity",
            "description": "Perplexity Research Test"
        }
    ]
    
    print(f"\n🚀 Starting API Tests...")
    print("=" * 55)
    
    working_apis = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {scenario['description']}")
        print("-" * 45)
        print(f"👤 User: {scenario['prompt']}")
        
        # Add to conversation
        user_message = Message(
            role=MessageRole.USER,
            content=scenario['prompt']
        )
        conversation.add_message(user_message)
        
        # Get ENTAERA routing decision
        routing_decision = await router.route_request(
            task_type=f"azure_test_{i}",
            content=scenario['prompt'],
            complexity=TaskComplexity.MODERATE
        )
        
        print(f"\n🧠 ENTAERA Smart Routing:")
        print(f"   ├── Recommended: {routing_decision.provider.value}")
        print(f"   ├── Model: {routing_decision.model}")
        print(f"   └── Reasoning: {routing_decision.reasoning}")
        
        # Make actual API call
        print(f"\n🔗 Testing {scenario['api'].upper()} API...")
        
        if scenario['api'] == 'azure':
            response, error = await test_azure_openai_api(scenario['prompt'])
        elif scenario['api'] == 'gemini':
            response, error = await test_gemini_api(scenario['prompt'])
        elif scenario['api'] == 'perplexity':
            response, error = await test_perplexity_api(scenario['prompt'])
        else:
            response, error = None, "Unknown API"
        
        if response:
            print(f"✅ {scenario['api'].upper()} API SUCCESS:")
            print(f"🤖 {response}")
            working_apis.append(scenario['api'])
            
            # Add AI response to conversation
            ai_message = Message(
                role=MessageRole.ASSISTANT,
                content=response
            )
            conversation.add_message(ai_message)
            
            print(f"📊 Response length: {len(response)} characters")
        else:
            print(f"❌ {scenario['api'].upper()} API ERROR:")
            print(f"💥 {error}")
        
        if i < len(test_scenarios):
            print(f"\n⏳ Next test in 2 seconds...")
            await asyncio.sleep(2)
    
    # Final status report
    messages = conversation.get_context_messages()
    ai_messages = [m for m in messages if m.role == MessageRole.ASSISTANT]
    
    print(f"\n" + "=" * 55)
    print(f"🎯 AZURE OPENAI TEST SUMMARY")
    print(f"=" * 55)
    
    print(f"📊 Results:")
    print(f"   ├── Total tests: {len(test_scenarios)}")
    print(f"   ├── Successful APIs: {len(working_apis)}")
    print(f"   └── Working APIs: {', '.join(working_apis).upper()}")
    
    # Specific Azure status
    azure_working = 'azure' in working_apis
    print(f"\n🔵 Azure OpenAI Status:")
    if azure_working:
        print(f"   ✅ AZURE OPENAI IS WORKING!")
        print(f"   🎉 You now have access to GPT models via Azure!")
    else:
        print(f"   ❌ Azure OpenAI not working yet")
        print(f"   📋 Setup Instructions:")
        print(f"      1. Go to: https://portal.azure.com/")
        print(f"      2. Create 'Azure OpenAI' resource")
        print(f"      3. Deploy 'gpt-35-turbo' model")
        print(f"      4. Get API key and endpoint")
        print(f"      5. Update .env file:")
        print(f"         AZURE_OPENAI_API_KEY=your_actual_key")
        print(f"         AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
        print(f"      6. Run this test again!")
    
    # Show working alternatives
    if working_apis:
        print(f"\n✅ Currently Working APIs:")
        for api in working_apis:
            print(f"   ├── {api.upper()}: Ready for production use")
        print(f"   └── ENTAERA smart routing active!")
    
    if azure_working:
        print(f"\n🚀 CONGRATULATIONS! Azure OpenAI + ENTAERA = READY!")
    else:
        print(f"\n⏳ Add Azure credentials and run: python azure_continuous_test.py")

if __name__ == "__main__":
    asyncio.run(azure_continuous_test())