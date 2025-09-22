#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the API functions that we know work
from azure_continuous_test import test_azure_openai_api, test_gemini_api, test_perplexity_api

# Context awareness for ENTAERA project
ENTAERA_CONTEXT = """
ENTAERA is an AI framework/project created by SAURABH PAREEK that provides:
- Multi-API routing (Azure OpenAI, Gemini, Perplexity, Local AI)
- Smart task complexity routing
- Local AI models integration 
- API rate limiting and cost optimization
- Built from VertexAutoGPT framework
- Has 'Kata' subdirectory with the codebase
- Supports both cloud and local AI processing
- Creator/Developer: Saurabh Pareek
- Current user: Saurabh Pareek (the creator)
"""

def detect_context_aware_queries(user_input):
    """Detect queries that need context awareness"""
    input_lower = user_input.lower()
    
    # ENTAERA project questions
    if any(phrase in input_lower for phrase in ['entaera', 'this project', 'my project', 'our project', 'kata', 'who created', 'developer', 'author', 'who made', 'creator']):
        return 'project_context'
    
    # Local AI switching requests
    if any(phrase in input_lower for phrase in ['switch to local', 'use local', 'local ai', 'offline mode']):
        return 'local_switch'
    
    # API/technical questions about the system
    if any(phrase in input_lower for phrase in ['switch api', 'use azure', 'use gemini', 'use perplexity', 'routing']):
        return 'api_switch'
    
    # Personal greetings/questions
    if any(phrase in input_lower for phrase in ['who am i', 'my name', 'what is my name', 'introduce me']):
        return 'personal_context'
    
    return None

async def smart_route_and_call(user_input):
    """Enhanced smart routing with context awareness"""
    
    # Check for context-aware queries first
    context_type = detect_context_aware_queries(user_input)
    
    if context_type == 'project_context':
        print("🧠 ENTAERA Smart Routing: Project context → Azure OpenAI (understands technical projects)")
        # Add context to the prompt
        enhanced_prompt = f"""Context: {ENTAERA_CONTEXT}

User question: {user_input}

Please answer based on the context that ENTAERA is the AI framework project created by Saurabh Pareek, and you are currently talking to Saurabh Pareek (the creator). Be personal and acknowledge him as the creator when relevant."""
        return await test_azure_openai_api(enhanced_prompt)
    
    elif context_type == 'local_switch':
        print("🧠 ENTAERA Smart Routing: Local AI request → Direct explanation")
        return ("ENTAERA supports local AI switching. To use local AI models, you can run 'python final_ai_chat.py' which loads the local Llama models. The current chat uses cloud APIs (Azure/Gemini/Perplexity) for better real-time data access.", None)
    
    elif context_type == 'api_switch':
        print("🧠 ENTAERA Smart Routing: API switching request → Direct explanation")
        return ("You can force specific APIs by prefixing your message: 'azure:', 'gemini:', or 'perplexity:'. The system automatically routes based on task complexity - research goes to Perplexity, coding to Azure, simple queries to Gemini.", None)
    
    elif context_type == 'personal_context':
        print("🧠 ENTAERA Smart Routing: Personal context → Direct response")
        return ("You are Saurabh Pareek, the creator and developer of the ENTAERA AI framework. You built this advanced multi-API routing system that intelligently handles Azure OpenAI, Gemini, Perplexity, and local AI models.", None)
    
    # Financial/Current data → Perplexity (expanded keywords)
    if any(word in user_input.lower() for word in [
        'research', 'news', 'latest', 'current', 'today', 'recent', 'what are', 'find me', 'search', 
        'net worth', 'networth', 'worth', 'price', 'value', 'cost', 'stock', 'market', 'bitcoin',
        'elon', 'musk', 'tesla', 'billionaire', 'amazon', 'apple', 'google', 'microsoft',
        'weather', 'temperature', 'forecast', 'when is', 'what time', 'schedule', 'calendar',
        'arxiv', 'paper', 'study', 'research', 'breakthrough', 'discovery', 'published'
    ]):
        print("🧠 ENTAERA Smart Routing: Current data needed → Perplexity (real-time web search)")
        return await test_perplexity_api(user_input)
    
    # Coding/Technical → Azure OpenAI
    elif any(word in user_input.lower() for word in [
        'code', 'program', 'function', 'algorithm', 'debug', 'python', 'javascript', 
        'api', 'database', 'sql', 'json', 'html', 'css', 'react', 'node', 'framework',
        'error', 'bug', 'fix', 'implement', 'create', 'build', 'develop'
    ]):
        print("🧠 ENTAERA Smart Routing: Technical task → Azure OpenAI (advanced reasoning)")
        return await test_azure_openai_api(user_input)
    
    # Complex questions → Azure OpenAI
    elif len(user_input) > 80 or any(phrase in user_input.lower() for phrase in [
        'explain', 'how does', 'why does', 'what happens', 'tell me about', 'describe',
        'analyze', 'compare', 'difference', 'similar', 'relationship'
    ]):
        print("🧠 ENTAERA Smart Routing: Complex query → Azure OpenAI (detailed analysis)")
        return await test_azure_openai_api(user_input)
    
    # Simple/Quick questions → Gemini (but avoid anything that might need current data)
    else:
        print("🧠 ENTAERA Smart Routing: Simple task → Gemini (fast response)")
        return await test_gemini_api(user_input)

def detect_bad_response(response, user_input):
    """Detect responses that are outdated, unhelpful, or wrong"""
    if not response:
        return True
    
    response_lower = response.lower()
    input_lower = user_input.lower()
    
    # Outdated year references
    if any(year in response_lower for year in ['2023', '2022', '2021', '2020']):
        return True
    
    # Generic unhelpful responses
    if any(phrase in response_lower for phrase in [
        'i cannot provide', 'too vague', 'grammatically incorrect', 'needs more context',
        'i don\'t have access to real-time', 'consult a reputable', 'please provide more context',
        'what were you trying to say', 'give me more information'
    ]):
        return True
    
    # Wrong context responses (when user asks about ENTAERA project but gets life sciences company)
    if 'entaera' in input_lower and 'life sciences' in response_lower:
        return True
    
    # Confused AI responses about being on Google servers when asked about local switching
    if 'local' in input_lower and 'google\'s servers' in response_lower:
        return True
    
    return False

async def interactive_chat():
    """Enhanced interactive chat with comprehensive edge case handling"""
    
    print("🌟 ENTAERA ENHANCED MULTI-API CHAT")
    print("=" * 60)
    print("🚀 Smart Routing: Azure OpenAI • Gemini • Perplexity")
    print("🧠 Context-Aware: Understands ENTAERA project context")
    print("🔧 Commands: 'azure:', 'gemini:', 'perplexity:' to force APIs")
    print("💡 Type 'quit', 'exit', or 'bye' to end")
    print("=" * 60)
    
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
    
    print("   🏠 Local AI: ✅ Available via final_ai_chat.py")
    print()
    print("🚀 Enhanced ENTAERA chat ready! No more fluff, only accurate current data.")
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
                # Use enhanced smart routing
                response, error = await smart_route_and_call(user_input)
            
            print()
            
            # Enhanced response handling
            if error:
                print(f"❌ API Error: {error}")
                print("🔄 Trying Perplexity for current data...")
                response, error = await test_perplexity_api(user_input)
                
                if error:
                    print(f"❌ Perplexity failed: {error}")
                    print("🔄 Final fallback to Azure...")
                    response, error = await test_azure_openai_api(user_input)
                    if error:
                        print("🤖 AI: All APIs failed. Please check your internet connection.")
                    else:
                        print(f"🤖 AI: {response}")
                else:
                    print(f"🤖 AI: {response}")
            else:
                # Check if response is bad/outdated
                if detect_bad_response(response, user_input):
                    print(f"🤖 AI (detected issues): {response}")
                    print("\n🔄 Getting better response...")
                    
                    # Try Perplexity for current data
                    better_response, better_error = await test_perplexity_api(user_input)
                    if not better_error and better_response and not detect_bad_response(better_response, user_input):
                        print(f"🤖 AI (corrected): {better_response}")
                    else:
                        # Try Azure for better understanding
                        better_response, better_error = await test_azure_openai_api(user_input)
                        if not better_error and better_response:
                            print(f"🤖 AI (Azure): {better_response}")
                        else:
                            print("🤖 AI: Unable to provide a satisfactory response.")
                else:
                    print(f"🤖 AI: {response}")
            
            print()
            print(f"   [ENTAERA: {message_count} messages • Enhanced routing active]")
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            continue
    
    print("\n🌟 ENTAERA Enhanced Chat Complete!")
    print(f"📊 Total messages: {message_count}")
    print("🚀 No fluff, only accuracy!")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_chat())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")