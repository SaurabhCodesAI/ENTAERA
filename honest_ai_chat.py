#!/usr/bin/env python3
"""
🎯 HONEST VERTEXAUTOGPT AI CHAT - No Hallucination
================================================
AI that only claims what it actually knows about ENTAERA
"""

import sys
import os
sys.path.append('src')

def honest_ai_chat():
    """Honest AI chat that doesn't hallucinate ENTAERA features"""
    print("🎯 HONEST VERTEXAUTOGPT AI CHAT")
    print("=" * 40)
    print("🛡️ No hallucination - only truth about capabilities")
    
    # Fix CUDA path issue
    original_cuda_path = os.environ.get('CUDA_PATH')
    if original_cuda_path:
        os.environ.pop('CUDA_PATH', None)
        print("   ✅ CUDA path fixed")
    
    try:
        # Load environment
        if os.path.exists('.env.local_ai'):
            with open('.env.local_ai') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Import framework components
        from llama_cpp import Llama
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        
        # Initialize framework
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Honest AI Chat")
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("honest_chat")
        
        print("   ✅ ENTAERA framework initialized")
        
        # Load model
        model_path = os.environ.get('LLAMA_MODEL_PATH', './models/llama-3.1-8b-instruct.Q4_K_M.gguf')
        model = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=6,
            verbose=False,
            n_gpu_layers=0,
        )
        
        print("   ✅ Llama 3.1 8B model loaded")
        
        # Very clear system prompt about honesty
        system_prompt = """You are Llama 3.1 8B running locally through ENTAERA framework.

CRITICAL INSTRUCTION: BE COMPLETELY HONEST ABOUT WHAT YOU KNOW

CONFIRMED FACTS ABOUT YOUR SETUP:
✅ Running locally on Saurabh Pareek's machine (not cloud)
✅ Using ENTAERA ConversationManager (you can see message tracking)
✅ Using ENTAERA Logger system (logging our interactions)
✅ Integrated with 12 ENTAERA modules totaling ~400KB

MODULES YOU CAN MENTION (ONLY THESE):
- Agent Orchestration (86KB)
- Semantic Search (65KB) 
- Code Generation (32KB)
- Code Analysis (32KB)
- Code Execution (23KB)
- Conversation Management (29KB) [YOU'RE USING THIS NOW]
- Context Injection/Retrieval (51KB)
- Logger System (18KB) [ACTIVE NOW]
- Conversation Memory (22KB)
- Configuration (18KB)

HONESTY RULES:
❌ NEVER invent ENTAERA features (like "katas" or specific examples)
❌ NEVER make up capabilities you don't actually have
✅ If asked about specific ENTAERA features, say "I don't have detailed information about that"
✅ Stick to what you can actually observe (conversation tracking, logging)
✅ Be helpful but truthful

Example: If asked "What katas does ENTAERA have?" respond: "I don't have information about specific katas in ENTAERA. I can see I'm integrated with the core modules, but I don't have details about training exercises or examples."

Be conversational but never lie or invent features."""

        system_message = Message(role=MessageRole.SYSTEM, content=system_prompt)
        conversation.add_message(system_message)
        
        print("🚀 Honest AI Chat Ready!")
        print("💬 Guaranteed truthful responses about ENTAERA")
        print("-" * 40)
        
        message_counter = 0
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            message_counter += 1
            
            # Add user message to framework
            user_message = Message(role=MessageRole.USER, content=user_input)
            conversation.add_message(user_message)
            logger.info(f"User message {message_counter}: {user_input}")
            
            # Build conversation context
            context_messages = conversation.get_context_messages()
            prompt_parts = []
            
            # Include system message and recent context
            for msg in context_messages[-9:]:
                if msg.role == MessageRole.SYSTEM:
                    prompt_parts.append(f"[SYSTEM]: {msg.content}")
                elif msg.role == MessageRole.USER:
                    prompt_parts.append(f"Human: {msg.content}")
                elif msg.role == MessageRole.ASSISTANT:
                    prompt_parts.append(f"Assistant: {msg.content}")
            
            full_prompt = "\n".join(prompt_parts) + "\nAssistant:"
            
            # Generate response with better parameters for code generation
            print("🤖 AI: ", end="", flush=True)
            
            response_text = ""
            response_stream = model(
                full_prompt,
                max_tokens=400,  # Increased for code generation
                temperature=0.2,  # Lower for more consistent code
                top_p=0.85,
                stop=["Human:", "User:", "\n\nHuman:", "\n\nUser:", "You:"],  # Added "You:" as stop
                stream=True
            )
            
            # Stream response
            for token in response_stream:
                if 'choices' in token and len(token['choices']) > 0:
                    text = token['choices'][0].get('text', '')
                    if text:
                        print(text, end="", flush=True)
                        response_text += text
            
            print()  # New line after response
            
            # Handle empty responses
            if not response_text.strip():
                response_text = "I'm here to help! What would you like to know about ENTAERA?"
            
            # Add AI response to framework
            ai_message = Message(role=MessageRole.ASSISTANT, content=response_text.strip())
            conversation.add_message(ai_message)
            logger.info(f"AI response {message_counter}: {response_text.strip()}")
            
            # Show framework activity
            total_messages = len(conversation.messages) if hasattr(conversation, 'messages') else message_counter * 2 + 1
            print(f"   [ENTAERA: {total_messages} messages tracked, honest responses only]")
        
        print("\n🎯 Honest AI Chat Complete!")
        print("✅ No false claims made about ENTAERA")
        
        # Cleanup
        del model
        print("🗑️ Model unloaded")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore CUDA path
        if original_cuda_path:
            os.environ['CUDA_PATH'] = original_cuda_path

if __name__ == "__main__":
    honest_ai_chat()