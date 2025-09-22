#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the API functions that we know work
from azure_continuous_test import test_azure_openai_api, test_gemini_api, test_perplexity_api

async def smart_route_and_call(user_input):
    """Smart routing logic to choose the best API"""
    
    # Research/News/Current events/Financial data → Perplexity
    if any(word in user_input.lower() for word in ['research', 'news', 'latest', 'current', 'today', 'recent', 'what are', 'find me', 'search', 'net worth', 'networth', 'worth', 'price', 'value', 'cost', 'elon', 'musk', 'tesla', 'billionaire', 'stock', 'market']):
        print("🧠 ENTAERA Smart Routing: Research/Current data → Perplexity (real-time web search)")
        return await test_perplexity_api(user_input)
    
    # Coding/Technical → Azure OpenAI
    elif any(word in user_input.lower() for word in ['code', 'program', 'function', 'algorithm', 'debug', 'python', 'javascript']):
        print("🧠 ENTAERA Smart Routing: Technical task → Azure OpenAI (advanced reasoning)")
        return await test_azure_openai_api(user_input)
    
    # Long/Complex queries → Azure OpenAI
    elif len(user_input) > 80:
        print("🧠 ENTAERA Smart Routing: Complex query → Azure OpenAI (detailed responses)")
        return await test_azure_openai_api(user_input)
    
    # Simple/Quick questions → Gemini (but avoid current data questions)
    else:
        print("🧠 ENTAERA Smart Routing: Simple task → Gemini (fast & efficient)")
        return await test_gemini_api(user_input)

async def interactive_chat():
    """Interactive chat with ENTAERA multi-API system"""
    
    print("🌟 ENTAERA INTERACTIVE MULTI-API CHAT")
    print("=" * 55)
    print("🚀 Smart Routing: Azure OpenAI • Gemini • Perplexity")
    print("💡 Type 'quit', 'exit', or 'bye' to end")
    print("🔧 Type 'azure:', 'gemini:', or 'perplexity:' to force a specific API")
    print("=" * 55)
    
    # Check API status
    print("🔍 API Status Check:")
    azure_key = os.getenv('AZURE_OPENAI_API_KEY', '')
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    perplexity_key = os.getenv('PERPLEXITY_API_KEY', '')
    
    if azure_key and azure_key != 'your_azure_openai_api_key_here':
        print("   🔵 Azure OpenAI: ✅ Ready")
    else:
        print("   🔵 Azure OpenAI: ❌ Not configured")
        
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        print("   🟢 Gemini: ✅ Ready")
    else:
        print("   🟢 Gemini: ❌ Not configured")
        
    if perplexity_key and perplexity_key != 'your_perplexity_api_key_here':
        print("   🟣 Perplexity: ✅ Ready")
    else:
        print("   🟣 Perplexity: ❌ Not configured")
    
    print()
    print("🚀 Ready to chat! Ask me anything...")
    print()
    
    message_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                break
                
            if not user_input:
                continue
                
            message_count += 1
            print()
            
            # Check for forced API selection
            if user_input.startswith('azure:'):
                prompt = user_input[6:].strip()
                print("🔗 Forced Azure OpenAI call...")
                response, error = await test_azure_openai_api(prompt)
                
            elif user_input.startswith('gemini:'):
                prompt = user_input[7:].strip()
                print("🔗 Forced Gemini call...")
                response, error = await test_gemini_api(prompt)
                
            elif user_input.startswith('perplexity:'):
                prompt = user_input[11:].strip()
                print("🔗 Forced Perplexity call...")
                response, error = await test_perplexity_api(prompt)
                
            else:
                # Use smart routing
                response, error = await smart_route_and_call(user_input)
            
            print()
            
            # Handle response
            if error:
                print(f"❌ API Error: {error}")
                print("🔄 Trying Perplexity for current data...")
                response, error = await test_perplexity_api(user_input)
                
                if error:
                    print(f"❌ Fallback also failed: {error}")
                    print("🔄 Final fallback to Azure...")
                    response, error = await test_azure_openai_api(user_input)
                    if error:
                        print("🤖 AI: I'm experiencing technical difficulties. Please try again.")
                    else:
                        print(f"🤖 AI: {response}")
                else:
                    print(f"🤖 AI: {response}")
            else:
                # Check if response seems outdated or unhelpful
                if response and any(phrase in response.lower() for phrase in ['2023', '2022', '2021', 'i cannot provide', 'too vague', 'grammatically incorrect']):
                    print(f"🤖 AI (outdated): {response}")
                    print("\n🔄 Getting current data from Perplexity...")
                    better_response, better_error = await test_perplexity_api(user_input)
                    if not better_error and better_response:
                        print(f"🤖 AI (current): {better_response}")
                    else:
                        print("🤖 AI: Using original response despite potential issues.")
                else:
                    print(f"🤖 AI: {response}")
            
            print()
            print(f"   [ENTAERA: {message_count} messages • Multi-API routing active]")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue
    
    print("\n🌟 ENTAERA Multi-API Chat Complete!")
    print(f"📊 Total messages: {message_count}")
    print("🚀 Thanks for testing ENTAERA!")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_chat())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")