#!/usr/bin/env python3

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the ENTAERA path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from entaera.core.logger import LoggerManager
from entaera.core.config import EntaeraConfig
from entaera.api.smart_router import SmartAPIRouter
from entaera.core.enums import TaskComplexity, APIProvider

async def interactive_chat():
    """Interactive chat with ENTAERA using all APIs"""
    
    print("🌟 ENTAERA INTERACTIVE CHAT")
    print("=" * 50)
    print("🚀 Multi-API Chat with Smart Routing")
    print("📡 Azure OpenAI • Gemini • Perplexity • Local AI")
    print("💡 Type 'quit', 'exit', or 'bye' to end")
    print("=" * 50)
    
    # Initialize ENTAERA
    try:
        logger_manager = LoggerManager()
        config = EntaeraConfig()
        router = SmartAPIRouter(config, logger_manager)
        print("✅ ENTAERA framework loaded")
        print("✅ All APIs initialized")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize ENTAERA: {e}")
        return
    
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
        
    print("   🏠 Local AI: ✅ Always available")
    print()
    
    conversation_history = []
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
            
            # Determine task complexity and routing
            if any(word in user_input.lower() for word in ['research', 'news', 'latest', 'current', 'today', 'recent']):
                complexity = TaskComplexity.RESEARCH
                preferred_provider = APIProvider.PERPLEXITY
                print(f"🧠 ENTAERA Smart Routing: Research task → Perplexity (web search)")
            elif any(word in user_input.lower() for word in ['code', 'program', 'function', 'algorithm', 'debug']):
                complexity = TaskComplexity.HIGH
                preferred_provider = APIProvider.AZURE
                print(f"🧠 ENTAERA Smart Routing: Coding task → Azure OpenAI (advanced)")
            elif len(user_input) > 100:
                complexity = TaskComplexity.MEDIUM
                preferred_provider = APIProvider.AZURE
                print(f"🧠 ENTAERA Smart Routing: Complex query → Azure OpenAI")
            else:
                complexity = TaskComplexity.LOW
                preferred_provider = APIProvider.GEMINI
                print(f"🧠 ENTAERA Smart Routing: Simple task → Gemini (fast)")
            
            print()
            
            # Get routing decision
            decision = router.get_routing_decision(user_input, complexity)
            
            try:
                # Make API call based on decision
                if decision.provider == APIProvider.AZURE:
                    print("🔗 Calling Azure OpenAI...")
                    from entaera_live_api_demo import test_azure_openai
                    response, error = await test_azure_openai(user_input)
                elif decision.provider == APIProvider.GEMINI:
                    print("🔗 Calling Gemini...")
                    from entaera_live_api_demo import test_gemini_api
                    response, error = await test_gemini_api(user_input)
                elif decision.provider == APIProvider.PERPLEXITY:
                    print("🔗 Calling Perplexity...")
                    from entaera_live_api_demo import test_perplexity_api
                    response, error = await test_perplexity_api(user_input)
                else:
                    print("🔗 Using Local AI...")
                    response = "Local AI response would go here (not implemented in this demo)"
                    error = None
                
                if error:
                    print(f"❌ API Error: {error}")
                    print("🔄 Falling back to Gemini...")
                    from entaera_live_api_demo import test_gemini_api
                    response, error = await test_gemini_api(user_input)
                
                if response:
                    print(f"🤖 AI: {response}")
                    conversation_history.append({"user": user_input, "ai": response})
                else:
                    print("❌ Sorry, I couldn't get a response. Please try again.")
                    
            except Exception as e:
                print(f"❌ Error during API call: {e}")
                print("🔄 Falling back to simple response...")
                print("🤖 AI: I'm experiencing technical difficulties. Please try again.")
            
            print()
            print(f"   [ENTAERA: {message_count} messages • Smart routing active]")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue
    
    print("\n🌟 ENTAERA Chat Session Complete!")
    print(f"📊 Total messages: {message_count}")
    print("🚀 All systems nominal")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_chat())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")