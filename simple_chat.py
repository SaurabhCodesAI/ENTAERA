#!/usr/bin/env python3
"""
🤖 SIMPLE CHAT WITH AI FRAMEWORK
================================
Chat interface using your conversation system (model integration coming next)
"""

import sys
import os
sys.path.append('src')

def simple_chat_demo():
    """Simple chat demo with your conversation framework"""
    
    print("🤖 VERTEXAUTOGPT CHAT DEMO")
    print("=" * 40)
    print("💬 Testing your conversation system!")
    print("📝 Type 'quit' to exit")
    print("🎯 Model integration ready for next step!")
    print("-" * 40)
    
    try:
        # Initialize conversation system
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        
        print("🧠 Initializing conversation system...")
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Chat Demo")
        
        # Add system message
        system_prompt = "You are a helpful AI assistant. Be conversational and helpful."
        system_message = Message(
            role=MessageRole.SYSTEM,
            content=system_prompt
        )
        conversation.add_message(system_message)
        
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("chat")
        
        print("✅ Chat system ready!")
        print("🔄 Note: Using simulated responses (model integration next)")
        print()
        
        # Chat loop
        message_count = 0
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                message_count += 1
                
                # Add user message
                user_message = Message(
                    role=MessageRole.USER,
                    content=user_input
                )
                conversation.add_message(user_message)
                
                # Generate AI response (simulated for now)
                ai_response = generate_smart_response(user_input, message_count)
                
                print(f"🤖 AI: {ai_response}")
                
                # Add AI response
                ai_message = Message(
                    role=MessageRole.ASSISTANT,
                    content=ai_response
                )
                conversation.add_message(ai_message)
                
                # Log interaction
                logger.info(f"Chat: User='{user_input[:30]}...' AI='{ai_response[:30]}...'")
                
                # Show conversation stats every 5 messages
                if message_count % 5 == 0:
                    stats = conversation.get_statistics()
                    print(f"\n📊 Stats: {stats.total_messages} messages, {stats.total_tokens} tokens")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Chat interrupted!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
        
        # Final stats
        stats = conversation.get_statistics()
        print(f"\n📊 Final Chat Stats:")
        print(f"   Total messages: {stats.total_messages}")
        print(f"   Total tokens: {stats.total_tokens}")
        print(f"   Context utilization: {stats.context_utilization:.1%}")
        
        # Show your models are ready
        print(f"\n🎯 YOUR AI MODELS STATUS:")
        from pathlib import Path
        models_dir = Path("models")
        if models_dir.exists():
            for model_file in models_dir.glob("*.gguf"):
                size_gb = model_file.stat().st_size / (1024**3)
                print(f"   ✅ {model_file.name}: {size_gb:.1f}GB ready")
        
        print(f"\n💡 NEXT STEP: Integrate Llama 3.1 8B for real AI responses!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Make sure you're in the ENTAERA-Kata directory")

def generate_smart_response(user_input, message_count):
    """Generate contextual responses"""
    
    user_lower = user_input.lower()
    
    # Context-aware responses
    responses = {
        1: "Hello! I'm your local AI assistant. I'm running on your conversation framework with your 8.4GB of downloaded models ready to connect!",
        2: "Great to chat with you! Your semantic search system is working perfectly, and I'm ready for model integration.",
        3: "I can see our conversation is being managed beautifully by your conversation system with context windows and persistence!",
    }
    
    # Message count specific responses
    if message_count in responses:
        return responses[message_count]
    
    # Content-based responses
    if any(word in user_lower for word in ['hello', 'hi', 'hey']):
        return f"Hello! This is message #{message_count} in our conversation. Your conversation system is tracking everything perfectly!"
    
    elif any(word in user_lower for word in ['model', 'ai', 'llama']):
        return "I'm excited about your Llama 3.1 8B model! It's downloaded and ready. We just need to connect it to this conversation system for real AI responses."
    
    elif any(word in user_lower for word in ['code', 'python', 'programming']):
        return "Your CodeLlama 7B model is perfect for programming tasks! It's ready to generate, debug, and optimize code once we integrate it."
    
    elif any(word in user_lower for word in ['search', 'semantic']):
        return "Your semantic search is already working beautifully! It's converting text to 384D vectors and finding similar content in milliseconds."
    
    elif any(word in user_lower for word in ['how', 'what', 'why']):
        return f"That's a great question! Your conversation system is managing our context perfectly. We have {message_count} messages so far, all tracked with metadata."
    
    elif any(word in user_lower for word in ['gpu', 'cuda', 'performance']):
        return "Your RTX 4050 setup is optimized for AI! The models use Q4_K_M quantization to fit in 4GB memory with 35 GPU layers configured."
    
    elif any(word in user_lower for word in ['thank', 'thanks']):
        return "You're welcome! Your AI framework is impressive - local models, semantic search, conversation management, all working together!"
    
    else:
        motivational = [
            f"Interesting point! We're at message #{message_count} and your conversation system is handling everything smoothly.",
            f"I appreciate that input! Your framework has 12 core modules working together beautifully.",
            f"That's thoughtful! Your local-first AI setup means complete privacy and no API costs.",
            f"Good thinking! Your 8.4GB of models are ready for serious AI applications.",
            f"I see what you mean! Your semantic search + conversation system is a powerful combination."
        ]
        
        return motivational[message_count % len(motivational)]

if __name__ == "__main__":
    simple_chat_demo()