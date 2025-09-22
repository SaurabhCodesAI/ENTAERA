#!/usr/bin/env python3
"""
🤖 CHAT WITH YOUR LOCAL AI MODELS
=================================
Simple chat interface using your downloaded Llama 3.1 8B model
"""

import sys
import os
sys.path.append('src')

def create_simple_chat():
    """Create a simple chat interface with your local AI"""
    
    print("🤖 VERTEXAUTOGPT LOCAL AI CHAT")
    print("=" * 50)
    print("💬 Chat with your Llama 3.1 8B model!")
    print("📝 Type 'quit' to exit, 'clear' to clear history")
    print("🎯 Your model is running locally - no API keys needed!")
    print("-" * 50)
    
    # Check if we can use the local models
    try:
        print("🔧 Checking local AI setup...")
        
        # Check model files exist
        from pathlib import Path
        chat_model_path = os.getenv('CHAT_MODEL_PATH', './models/llama-3.1-8b-instruct.Q4_K_M.gguf')
        model_file = Path(chat_model_path)
        
        if not model_file.exists():
            print(f"❌ Model file not found: {chat_model_path}")
            print("💡 Make sure your models are downloaded in the models/ directory")
            return
        
        print(f"✅ Found model: {model_file.name} ({model_file.stat().st_size / (1024**3):.1f}GB)")
        
        # Try to import llama-cpp-python for local inference
        try:
            import llama_cpp
            print("✅ llama-cpp-python available for local inference")
            use_local = True
        except ImportError:
            print("⚠️  llama-cpp-python not available, using conversation framework only")
            use_local = False
        
        # Set up conversation management
        from entaera.core.conversation import ConversationManager, Conversation
        from entaera.core.logger import LoggerManager
        
        print("🧠 Initializing conversation system...")
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Local AI Chat")
        
        # Add system message
        system_prompt = """You are a helpful AI assistant running locally on the user's computer. 
You are powered by Llama 3.1 8B model. Be conversational, helpful, and concise in your responses.
Mention that you're running locally without needing internet or API keys."""
        
        conversation.add_message("system", system_prompt)
        
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("chat")
        
        print("✅ Chat system initialized!")
        print("🚀 Starting chat session...\n")
        
        # Simple chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye! Chat session ended.")
                    break
                
                if user_input.lower() == 'clear':
                    conversation = conv_manager.create_conversation("Local AI Chat - New Session")
                    conversation.add_message("system", system_prompt)
                    print("🧹 Chat history cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Add user message to conversation
                conversation.add_message("user", user_input)
                
                print("🤖 AI: ", end="", flush=True)
                
                if use_local:
                    # Use local model for inference
                    response = generate_local_response(chat_model_path, conversation, logger)
                else:
                    # Simulate AI response (since we need to integrate the actual model)
                    response = simulate_ai_response(user_input)
                
                print(response)
                
                # Add AI response to conversation
                conversation.add_message("assistant", response)
                
                # Log the interaction
                logger.info(f"Chat interaction: User='{user_input[:50]}...', AI='{response[:50]}...'")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("🔄 Continuing chat...")
        
        # Show conversation stats
        stats = conversation.get_statistics()
        print(f"\n📊 Chat Session Stats:")
        print(f"   Messages: {stats.total_messages}")
        print(f"   Tokens: {stats.total_tokens}")
        print(f"   Duration: {stats.duration_minutes:.1f} minutes")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("💡 Make sure you're running from the ENTAERA-Kata directory")

def generate_local_response(model_path, conversation, logger):
    """Generate response using local Llama model"""
    try:
        import llama_cpp
        
        # Initialize model (this is expensive, in real app you'd cache this)
        print("🔄 Loading model...", end="", flush=True)
        
        # Get conversation context
        messages = conversation.get_messages_for_context()
        
        # Format messages for Llama
        prompt = format_conversation_for_llama(messages)
        
        # Model parameters from .env.local_ai
        model_params = {
            "model_path": model_path,
            "n_ctx": int(os.getenv('MODEL_CONTEXT_LENGTH', '4096')),
            "n_gpu_layers": int(os.getenv('NUM_GPU_LAYERS', '35')),
            "verbose": False
        }
        
        llm = llama_cpp.Llama(**model_params)
        
        # Generate response
        generation_params = {
            "prompt": prompt,
            "max_tokens": int(os.getenv('MAX_TOKENS_PER_REQUEST', '512')),
            "temperature": float(os.getenv('TEMPERATURE', '0.1')),
            "stop": ["</s>", "User:", "Human:"],
            "echo": False
        }
        
        print("\b\b\b⚡", end="", flush=True)  # Replace "Loading..." with "⚡"
        
        output = llm(**generation_params)
        response = output['choices'][0]['text'].strip()
        
        logger.info(f"Local model generated response: {len(response)} chars")
        return response
        
    except Exception as e:
        logger.error(f"Local model error: {e}")
        return f"Sorry, I encountered an error with the local model: {str(e)[:100]}..."

def format_conversation_for_llama(messages):
    """Format conversation messages for Llama prompt"""
    formatted = ""
    
    for msg in messages:
        role = msg.role
        content = msg.content
        
        if role == "system":
            formatted += f"System: {content}\n\n"
        elif role == "user":
            formatted += f"User: {content}\n\n"
        elif role == "assistant":
            formatted += f"Assistant: {content}\n\n"
    
    formatted += "Assistant: "
    return formatted

def simulate_ai_response(user_input):
    """Simulate AI response when local model isn't available"""
    responses = {
        "hello": "Hello! I'm your local AI assistant powered by Llama 3.1 8B. I'm running right here on your computer - no internet needed!",
        "how are you": "I'm doing great! I'm running locally on your RTX 4050 GPU. It feels good to be free from the cloud!",
        "what can you do": "I can help with conversations, answer questions, assist with coding, creative writing, and much more. All running locally on your machine!",
        "python": "I'd be happy to help with Python! I have CodeLlama 7B as my coding companion. What Python question do you have?",
        "code": "I love helping with code! I can generate, explain, debug, and optimize code in many languages. What coding task can I help with?",
    }
    
    user_lower = user_input.lower()
    for key, response in responses.items():
        if key in user_lower:
            return response
    
    return f"Thanks for saying: '{user_input}'. I'm your local AI assistant! While I'm simulating responses right now, I'm ready to be connected to your Llama 3.1 8B model for real conversations. What would you like to chat about?"

if __name__ == "__main__":
    # Load environment variables
    from pathlib import Path
    env_file = Path('.env.local_ai')
    if env_file.exists():
        print("🔧 Loading local AI configuration...")
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    create_simple_chat()