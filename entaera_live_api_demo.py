#!/usr/bin/env python3
"""
🎪 ENTAERA LIVE API DEMO
=======================
REAL API calls with your Gemini and Perplexity keys!
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

async def test_perplexity_api(prompt):
    """Test live Perplexity API call"""
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key or api_key == 'placeholder-for-local-first-mode':
        return None, "No Perplexity API key configured"
    
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are ENTAERA AI assistant with access to real-time web information."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": ["perplexity.ai"],
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

async def live_api_demo():
    """Run live API demonstration"""
    print("🎪 ENTAERA LIVE API DEMO")
    print("=" * 50)
    print("Testing REAL API calls with your keys!")
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
        conversation = conv_manager.create_conversation("Live API Demo")
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("live_demo")
        router = SmartAPIRouter()
        
        print("✅ Components initialized")
        
    except Exception as e:
        print(f"❌ Framework error: {e}")
        return
    
    # Test scenarios
    test_scenarios = [
        {
            "prompt": "Hello! Can you tell me what ENTAERA stands for and respond with just 'ENTAERA Live API Test Successful!'?",
            "api": "gemini",
            "description": "Simple Gemini test"
        },
        {
            "prompt": "What are the latest AI developments in September 2025? Give me 3 recent breakthroughs.",
            "api": "perplexity", 
            "description": "Current research via Perplexity"
        },
        {
            "prompt": "Explain quantum computing in simple terms",
            "api": "gemini",
            "description": "Complex explanation via Gemini"
        }
    ]
    
    print(f"\n🚀 Starting Live API Tests...")
    print("=" * 50)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {scenario['description']}")
        print("-" * 40)
        print(f"👤 User: {scenario['prompt']}")
        
        # Add to conversation
        user_message = Message(
            role=MessageRole.USER,
            content=scenario['prompt']
        )
        conversation.add_message(user_message)
        
        # Get routing decision
        routing_decision = await router.route_request(
            task_type=f"live_test_{i}",
            content=scenario['prompt'],
            complexity=TaskComplexity.MODERATE
        )
        
        print(f"\n🧠 ENTAERA Routing:")
        print(f"   ├── Recommended: {routing_decision.provider.value}")
        print(f"   ├── Model: {routing_decision.model}")
        print(f"   └── Reasoning: {routing_decision.reasoning}")
        
        # Make actual API call
        print(f"\n🔗 Making LIVE {scenario['api'].upper()} API call...")
        
        if scenario['api'] == 'gemini':
            response, error = await test_gemini_api(scenario['prompt'])
        elif scenario['api'] == 'perplexity':
            response, error = await test_perplexity_api(scenario['prompt'])
        else:
            response, error = None, "Unknown API"
        
        if response:
            print(f"✅ {scenario['api'].upper()} API Response:")
            print(f"🤖 {response}")
            
            # Add AI response to conversation
            ai_message = Message(
                role=MessageRole.ASSISTANT,
                content=response
            )
            conversation.add_message(ai_message)
            
            print(f"📊 Response length: {len(response)} characters")
        else:
            print(f"❌ {scenario['api'].upper()} API Error:")
            print(f"💥 {error}")
        
        if i < len(test_scenarios):
            print(f"\n⏳ Next test in 3 seconds...")
            await asyncio.sleep(3)
    
    # Final statistics
    messages = conversation.get_context_messages()
    user_messages = [m for m in messages if m.role == MessageRole.USER]
    ai_messages = [m for m in messages if m.role == MessageRole.ASSISTANT]
    
    print(f"\n" + "=" * 50)
    print(f"🎉 LIVE API DEMO COMPLETE!")
    print(f"=" * 50)
    print(f"📈 Session Statistics:")
    print(f"   ├── Total messages: {len(messages)}")
    print(f"   ├── User prompts: {len(user_messages)}")
    print(f"   ├── API responses: {len(ai_messages)}")
    print(f"   └── Success rate: {len(ai_messages)}/{len(test_scenarios)} tests")
    
    # Check API status
    gemini_key = os.getenv('GEMINI_API_KEY')
    perplexity_key = os.getenv('PERPLEXITY_API_KEY')
    
    print(f"\n🔑 API Keys Status:")
    print(f"   ├── Gemini: {'✅ Active' if gemini_key and gemini_key != 'placeholder-for-local-first-mode' else '❌ Not set'}")
    print(f"   └── Perplexity: {'✅ Active' if perplexity_key and perplexity_key != 'placeholder-for-local-first-mode' else '❌ Not set'}")
    
    print(f"\n🚀 ENTAERA Live API Integration: OPERATIONAL!")

if __name__ == "__main__":
    asyncio.run(live_api_demo())