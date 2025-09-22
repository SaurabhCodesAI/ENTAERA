#!/usr/bin/env python3
"""
🎯 WORKING AI CHAT - CUDA Path Fix
==================================
Simple chat with working model loading
"""

import sys
import os
sys.path.append('src')

def working_ai_chat():
    """Chat with working model loading"""
    print("🎯 WORKING AI CHAT")
    print("=" * 30)
    print("🔧 Fixing CUDA path issue...")
    
    # Temporarily remove problematic CUDA path
    original_cuda_path = os.environ.get('CUDA_PATH')
    if original_cuda_path:
        os.environ.pop('CUDA_PATH', None)
        print("   ✅ CUDA_PATH temporarily removed")
    
    try:
        # Load environment
        if os.path.exists('.env.local_ai'):
            with open('.env.local_ai') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Test llama_cpp import
        from llama_cpp import Llama
        print("   ✅ llama_cpp imported successfully!")
        
        # Get model path
        model_path = os.environ.get('LLAMA_MODEL_PATH', './models/llama-3.1-8b-instruct.Q4_K_M.gguf')
        print(f"   📁 Model path: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"   ❌ Model file not found: {model_path}")
            return
        
        size_gb = os.path.getsize(model_path) / (1024**3)
        print(f"   📊 Model size: {size_gb:.1f}GB")
        
        # Load model
        print("🤖 Loading Llama 3.1 8B model...")
        print("   ⏳ This may take a moment...")
        
        model = Llama(
            model_path=model_path,
            n_ctx=2048,  # Smaller context for faster loading
            n_threads=4,  # Use 4 CPU threads
            verbose=False,
            n_gpu_layers=0,  # Pure CPU mode to avoid GPU issues
        )
        
        print("   ✅ Model loaded successfully!")
        
        # Initialize conversation system
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Working AI Chat")
        
        system_message = Message(
            role=MessageRole.SYSTEM, 
            content="""You are a Llama 3.1 8B Instruct model running LOCALLY on the user's computer via ENTAERA framework. 

IMPORTANT FACTS ABOUT YOUR DEPLOYMENT:
- You are running on the user's local machine (NOT in the cloud)
- You are powered by a 4.6GB Llama 3.1 8B model file
- You are using CPU processing on RTX 4050 hardware
- You have NO internet connection or cloud access
- All conversations are completely private and stay on this machine
- Your creator/developer in this session is Saurabh Pareek

ABOUT VERTEXAUTOGPT FRAMEWORK:
- ENTAERA is Saurabh's AI development framework project
- It has 12 core modules including conversation management, semantic search, and agent orchestration
- You are integrated with its conversation system for message tracking
- The framework supports local AI models, semantic search with sentence-transformers
- It includes code generation, conversation memory, and agent orchestration capabilities
- Total framework size is ~400KB with advanced AI functionality

Be helpful, conversational, and accurate about your local deployment and integration with ENTAERA."""
        )
        conversation.add_message(system_message)
        
        print("🚀 Real AI chat ready!")
        print("💬 Type 'quit' to exit")
        print("🔥 You're now talking to REAL Llama 3.1 8B!")
        print("-" * 30)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            # Add user message to conversation
            user_message = Message(role=MessageRole.USER, content=user_input)
            conversation.add_message(user_message)
            
            # Create prompt from conversation context
            context_messages = conversation.get_context_messages()
            prompt_parts = []
            
            for msg in context_messages[-5:]:  # Last 5 messages for context
                if msg.role == MessageRole.SYSTEM:
                    prompt_parts.append(f"System: {msg.content}")
                elif msg.role == MessageRole.USER:
                    prompt_parts.append(f"Human: {msg.content}")
                elif msg.role == MessageRole.ASSISTANT:
                    prompt_parts.append(f"Assistant: {msg.content}")
            
            prompt = "\n".join(prompt_parts) + "\nAssistant:"
            
            # Generate response
            print("🤖 AI: ", end="", flush=True)
            
            response_text = ""
            response = model(
                prompt,
                max_tokens=128,
                temperature=0.3,
                stop=["Human:", "User:", "\n\n"],
                stream=True
            )
            
            for token in response:
                if 'choices' in token and len(token['choices']) > 0:
                    text = token['choices'][0].get('text', '')
                    if text:
                        print(text, end="", flush=True)
                        response_text += text
            
            print()  # New line after response
            
            if not response_text.strip():
                response_text = "I'm here and ready to help!"
            
            # Add AI response to conversation
            ai_message = Message(role=MessageRole.ASSISTANT, content=response_text.strip())
            conversation.add_message(ai_message)
        
        print("\n👋 Real AI chat ended!")
        print("🗑️ Unloading model...")
        del model
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore CUDA path
        if original_cuda_path:
            os.environ['CUDA_PATH'] = original_cuda_path
            print("🔧 CUDA_PATH restored")

if __name__ == "__main__":
    working_ai_chat()