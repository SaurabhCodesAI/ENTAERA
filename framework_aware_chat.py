#!/usr/bin/env python3
"""
🎯 FINAL INTEGRATED AI - Full ENTAERA Awareness
===================================================
"""

import sys
import os
sys.path.append('src')

def framework_aware_chat():
    """AI chat with full framework awareness"""
    print("🎯 FRAMEWORK-AWARE AI CHAT")
    print("=" * 35)
    
    # Fix CUDA
    original_cuda_path = os.environ.get('CUDA_PATH')
    if original_cuda_path:
        os.environ.pop('CUDA_PATH', None)
    
    try:
        # Load environment
        if os.path.exists('.env.local_ai'):
            with open('.env.local_ai') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Import framework
        from llama_cpp import Llama
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        
        # Initialize framework
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Framework Aware Chat")
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("framework_chat")
        
        print("✅ ENTAERA framework active!")
        
        # Load model
        model_path = os.environ.get('LLAMA_MODEL_PATH', './models/llama-3.1-8b-instruct.Q4_K_M.gguf')
        model = Llama(model_path=model_path, n_ctx=2048, n_threads=4, verbose=False, n_gpu_layers=0)
        
        print("✅ AI model loaded!")
        
        # System message with REAL framework capabilities
        system_content = """FRAMEWORK STATUS REPORT:
✅ You ARE currently running through ENTAERA framework
✅ Every message you receive IS a ENTAERA Message object  
✅ Your responses ARE being logged by ENTAERA logger
✅ This conversation IS managed by ENTAERA ConversationManager

ACTUAL VERTEXAUTOGPT MODULES YOU'RE INTEGRATED WITH:
🤖 Agent Orchestration (86KB) - Multi-agent coordination and task delegation
💬 Conversation Management (29KB) - Advanced dialogue tracking (YOU'RE USING THIS!)
🔍 Semantic Search (65KB) - Vector-based document search and retrieval
🐍 Code Generation (32KB) - Automatic code creation and templates
🔧 Code Analysis (32KB) - Code review, debugging, and optimization
⚡ Code Execution (23KB) - Safe code running and testing
🧠 Context Injection/Retrieval (51KB) - Smart context management
📝 Logger System (18KB) - Comprehensive interaction logging (ACTIVE NOW!)
💾 Conversation Memory (22KB) - Long-term conversation storage
⚙️ Configuration Management (18KB) - Framework settings and optimization

WHAT YOU CAN ACTUALLY DO:
- Coordinate multiple AI agents for complex tasks
- Use semantic search to find relevant information
- Generate, analyze, and execute code safely
- Manage long-term conversation context and memory
- All running locally on Saurabh Pareek's machine!

When asked about capabilities, mention these REAL integrated modules!"""

        system_msg = Message(role=MessageRole.SYSTEM, content=system_content)
        conversation.add_message(system_msg)
        
        print("🚀 Ready! Ask about ENTAERA capabilities!")
        print("-" * 35)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue
            
            # Add to framework
            user_msg = Message(role=MessageRole.USER, content=user_input)
            conversation.add_message(user_msg)
            logger.info(f"User: {user_input}")
            
            # Show framework action
            msg_count = len(conversation.messages) if hasattr(conversation, 'messages') else 0
            print(f"[ENTAERA: Message {msg_count} processed]")
            
            # Build prompt
            context = conversation.get_context_messages()
            prompt_parts = []
            for msg in context[-5:]:
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
            
            for token in model(prompt, max_tokens=120, temperature=0.3, stop=["Human:", "\n\n"], stream=True):
                if 'choices' in token and token['choices']:
                    text = token['choices'][0].get('text', '')
                    if text:
                        print(text, end="", flush=True)
                        response_text += text
            
            print()
            
            # Add to framework and log
            if response_text.strip():
                ai_msg = Message(role=MessageRole.ASSISTANT, content=response_text.strip())
                conversation.add_message(ai_msg)
                logger.info(f"AI: {response_text.strip()}")
                
                # Show framework tracking
                final_count = len(conversation.messages) if hasattr(conversation, 'messages') else 0
                print(f"[ENTAERA: Conversation tracked, {final_count} total messages]")
        
        print("\n🎯 Framework-aware chat ended!")
        del model
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if original_cuda_path:
            os.environ['CUDA_PATH'] = original_cuda_path

if __name__ == "__main__":
    framework_aware_chat()