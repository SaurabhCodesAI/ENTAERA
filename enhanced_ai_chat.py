#!/usr/bin/env python3
"""
🤖 ENHANCED AI CHAT WITH REAL MODEL INTEGRATION
===============================================
Chat interface with your Llama 3.1 8B model and intelligent fallbacks
"""

import sys
import os
sys.path.append('src')

# Import our model loader
from local_model_loader import SmartResponseGenerator

def enhanced_ai_chat():
    """Enhanced chat with real AI model integration"""
    
    print("🤖 ENHANCED VERTEXAUTOGPT AI CHAT")
    print("=" * 50)
    print("💬 Real AI model integration with fallbacks!")
    print("📝 Type 'quit' to exit, 'clear' to clear history")
    print("🎯 Attempting to load your Llama 3.1 8B model...")
    print("-" * 50)
    
    try:
        # Initialize conversation system
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        
        print("🧠 Initializing conversation system...")
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Enhanced AI Chat")
        
        # Initialize AI response generator
        ai_generator = SmartResponseGenerator()
        model_loaded = ai_generator.initialize()
        
        # Add system message
        system_prompt = """You are a helpful AI assistant running locally on the user's computer. 
        You are powered by ENTAERA framework with Llama 3.1 8B model. Be conversational, 
        helpful, and mention that you're running locally when appropriate."""
        
        system_message = Message(role=MessageRole.SYSTEM, content=system_prompt)
        conversation.add_message(system_message)
        
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("enhanced_chat")
        
        print("✅ Enhanced chat system ready!")
        
        if model_loaded:
            print("🎉 Real AI model loaded and ready!")
        else:
            print("⚠️  Using intelligent fallback responses")
        
        print("\n🚀 Starting enhanced chat session...\n")
        
        # Enhanced chat loop
        message_count = 0
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye! Enhanced chat session ended.")
                    break
                
                if user_input.lower() == 'clear':
                    conversation = conv_manager.create_conversation("Enhanced AI Chat - New Session")
                    conversation.add_message(system_message)
                    print("🧹 Chat history cleared!")
                    continue
                
                if user_input.lower() == 'stats':
                    # Show conversation statistics
                    stats = conversation.get_stats()
                    print(f"\n📊 Conversation Stats:")
                    print(f"   Messages: {stats.get('total_messages', 'Unknown')}")
                    print(f"   Tokens: {stats.get('total_tokens', 'Unknown')}")
                    print(f"   AI Model: {'Llama 3.1 8B' if model_loaded else 'Intelligent Fallback'}")
                    print()
                    continue
                
                if not user_input:
                    continue
                
                message_count += 1
                
                # Add user message
                user_message = Message(role=MessageRole.USER, content=user_input)
                conversation.add_message(user_message)
                
                # Get conversation context for AI
                context = conversation.get_context_messages()
                
                # Generate AI response
                print("🤖 AI: ", end="", flush=True)
                ai_response = ai_generator.generate_response(user_input, context)
                
                # Clean up the response display
                if ai_response.startswith("✅") or ai_response.startswith("❌"):
                    print()  # New line if there were status indicators
                print(ai_response)
                
                # Add AI response to conversation
                ai_message = Message(role=MessageRole.ASSISTANT, content=ai_response)
                conversation.add_message(ai_message)
                
                # Log interaction
                logger.info(f"Enhanced chat: User='{user_input[:50]}...', AI='{ai_response[:50]}...'")
                
                # Show stats every 10 messages
                if message_count % 10 == 0:
                    stats = conversation.get_stats()
                    print(f"\n📊 Quick stats: {stats.get('total_messages', '?')} messages exchanged")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n👋 Enhanced chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("🔄 Continuing chat...")
                logger.error(f"Chat error: {e}")
        
        # Final session summary
        try:
            stats = conversation.get_stats()
            print(f"\n📊 Final Enhanced Chat Stats:")
            print(f"   Total messages: {stats.get('total_messages', 'Unknown')}")
            print(f"   Total tokens: {stats.get('total_tokens', 'Unknown')}")
            print(f"   AI Engine: {'Real Llama 3.1 8B' if model_loaded else 'Intelligent Fallback'}")
            print(f"   Framework: ENTAERA with local models")
        except Exception as e:
            print(f"   Stats unavailable: {e}")
        
        # Cleanup
        if model_loaded:
            print("🗑️  Unloading AI model...")
            ai_generator.model_loader.unload_model()
        
        print("✅ Enhanced chat session completed!")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("💡 Make sure you're in the ENTAERA-Kata directory")

def quick_model_test():
    """Quick test of just the model loading"""
    print("🧪 QUICK MODEL TEST")
    print("=" * 30)
    
    try:
        from local_model_loader import SmartResponseGenerator
        
        generator = SmartResponseGenerator()
        success = generator.initialize()
        
        test_prompt = "Hello! Can you tell me about yourself?"
        response = generator.generate_response(test_prompt)
        
        print(f"\n🔍 Test prompt: {test_prompt}")
        print(f"🤖 AI response: {response}")
        
        if generator.model_loader.is_loaded():
            print("\n✅ Real AI model is working!")
        else:
            print("\n⚠️  Using fallback (model not loaded)")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    # Load environment first
    from pathlib import Path
    env_file = Path('.env.local_ai')
    if env_file.exists():
        print("🔧 Loading local AI configuration...")
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Ask user what they want to do
    print("Choose an option:")
    print("1. Enhanced AI Chat (full system)")
    print("2. Quick Model Test (just test loading)")
    
    choice = input("Enter 1 or 2 (or press Enter for chat): ").strip()
    
    if choice == "2":
        quick_model_test()
    else:
        enhanced_ai_chat()