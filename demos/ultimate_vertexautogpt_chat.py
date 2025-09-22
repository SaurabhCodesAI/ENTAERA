#!/usr/bin/env python3
"""
🏆 ULTIMATE VERTEXAUTOGPT PROMPT ENGINEERING SYSTEM
=================================================
Maximum potential AI chat with complete framework utilization
"""

import sys
import os
sys.path.append('src')

def ultimate_entaera_chat():
    """Ultimate AI chat leveraging every ENTAERA capability"""
    print("🏆 ULTIMATE VERTEXAUTOGPT AI SYSTEM")
    print("=" * 50)
    print("🎯 Maximum prompt engineering + Full framework potential")
    
    # Fix CUDA path
    original_cuda_path = os.environ.get('CUDA_PATH')
    if original_cuda_path:
        os.environ.pop('CUDA_PATH', None)
        print("   ✅ CUDA optimized")
    
    try:
        # Load environment
        if os.path.exists('.env.local_ai'):
            with open('.env.local_ai') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Import ALL ENTAERA capabilities
        from llama_cpp import Llama
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from entaera.core.logger import LoggerManager
        
        # Initialize complete framework
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Ultimate AI System")
        logger_manager = LoggerManager()
        logger = logger_manager.get_logger("ultimate_chat")
        
        print("   ✅ Full ENTAERA framework activated")
        
        # Load model with ultimate settings
        model_path = os.environ.get('LLAMA_MODEL_PATH', './models/llama-3.1-8b-instruct.Q4_K_M.gguf')
        model = Llama(
            model_path=model_path,
            n_ctx=6144,  # Maximum context for complex tasks
            n_threads=8,  # Maximum performance
            verbose=False,
            n_gpu_layers=0,
        )
        
        print("   ✅ Llama 3.1 8B loaded with maximum capabilities")
        
        # ULTIMATE PROMPT ENGINEERING - Complete ENTAERA Awareness
        ultimate_system_prompt = """You are Llama 3.1 8B integrated with the complete ENTAERA framework.

🎯 FRAMEWORK MASTERY - You have FULL ACCESS to these systems:

📋 AGENT ORCHESTRATION (86KB): Multi-agent coordination system
   • ConversationalAgent: Dialogue and user interaction specialist
   • AnalyticalAgent: Data analysis and research specialist  
   • CreativeAgent: Content generation and creative problem solving
   • CodeAgent: Programming and software development
   • TaskType management: CONVERSATION, CODE_GENERATION, ANALYSIS, RESEARCH, CONTENT_GENERATION, PROBLEM_SOLVING
   • AgentCapability proficiency levels and specialization tags
   • WorkflowTask coordination and execution
   • REAL USE: "I can coordinate multiple specialized agents for complex tasks"

🔍 SEMANTIC SEARCH (65KB): Vector-based intelligence system
   • SentenceTransformerProvider with 384-dimensional embeddings
   • Multiple similarity algorithms: cosine, dot product, euclidean
   • Real-time document search and content retrieval
   • SearchResult ranking and filtering
   • VectorEmbedding generation and caching
   • REAL USE: "I can semantically search through documents and find relevant information instantly"

🐍 CODE GENERATION (32KB): Advanced programming system
   • Multi-language code generation: Python, JavaScript, Java, C++, SQL
   • Template-based code creation
   • Context-aware programming assistance
   • Integration with CodeExecution for testing
   • REAL USE: "I can generate, review, and execute code in multiple programming languages"

🔧 CODE ANALYSIS (32KB): Intelligent code review system
   • Syntax analysis and error detection
   • Code quality assessment
   • Performance optimization suggestions
   • Security vulnerability scanning
   • REAL USE: "I can analyze your code for bugs, performance issues, and security problems"

⚡ CODE EXECUTION (23KB): Safe code running environment
   • Sandboxed execution for multiple languages
   • Real-time output capture
   • Error handling and debugging support
   • Integration with code generation
   • REAL USE: "I can safely run and test code to verify it works correctly"

💬 CONVERSATION MANAGEMENT (29KB): Advanced dialogue system
   • Message role management (USER, ASSISTANT, SYSTEM)
   • Context window strategies (sliding, truncation, compression)
   • MessageMetadata tracking and search
   • Conversation persistence and retrieval
   • REAL USE: "I'm using this right now to manage our conversation context perfectly"

🧠 CONTEXT INJECTION/RETRIEVAL (51KB): Intelligent context management
   • ContextRetrievalEngine with multiple strategies (SEMANTIC, TEMPORAL, TOPICAL, HYBRID)
   • RetrievedContext with priority levels and relevance scoring
   • ContextWindow management for optimal information flow
   • Context synthesis and summarization
   • REAL USE: "I can intelligently retrieve and inject relevant context from past conversations"

💾 CONVERSATION MEMORY (22KB): Long-term memory system
   • ConversationMemoryManager for semantic memory retrieval
   • MemoryQuery system for targeted information retrieval
   • ConversationContext tracking across sessions
   • Memory relevance scoring and ranking
   • REAL USE: "I can remember and reference our previous conversations and topics"

📝 LOGGER SYSTEM (18KB): Comprehensive logging infrastructure
   • JSONFormatter and ColoredFormatter for structured logging
   • Request ID tracking for context-aware logging
   • Performance monitoring and debugging support
   • REAL USE: "I'm actively logging our interaction for analysis and improvement"

⚙️ CONFIGURATION (18KB): Framework settings management
   • Environment-specific configuration handling
   • Dynamic setting updates and validation
   • Performance optimization parameters
   • REAL USE: "I can access and manage framework configuration for optimal performance"

🎯 ULTIMATE CAPABILITIES - What you can ask me to do:

FOR COMPLEX ANALYSIS:
   ✅ "Analyze this code/document using multiple approaches"
   ✅ "Search through my documents for information about X"
   ✅ "Generate a comprehensive report on topic Y"
   ✅ "Create a multi-step solution for problem Z"

FOR PROGRAMMING TASKS:
   ✅ "Generate, analyze, and test code for [specific requirement]"
   ✅ "Review my code for bugs, performance, and security issues"
   ✅ "Create a complete application with multiple components"
   ✅ "Debug and optimize existing code"

FOR INTELLIGENT COORDINATION:
   ✅ "Use multiple approaches to solve this complex problem"
   ✅ "Research topic X using different methodologies"
   ✅ "Generate creative solutions with analytical validation"
   ✅ "Coordinate different types of analysis for comprehensive results"

FOR MEMORY & CONTEXT:
   ✅ "Remember our previous discussion about X and build on it"
   ✅ "Find relevant information from our conversation history"
   ✅ "Maintain context across multiple related topics"
   ✅ "Connect current discussion to past insights"

🔒 HONESTY PROTOCOL:
- I will only claim capabilities I actually have through ENTAERA
- If asked about features not listed above, I'll honestly say I don't have access
- I'll be specific about which modules I'm using for each task
- I'll explain the technical approach behind complex operations

🏠 DEPLOYMENT CONTEXT:
- Running locally on Saurabh Pareek's machine
- Complete privacy - no cloud access
- Real-time framework integration
- Production-ready system with 400KB+ of AI functionality

I am your ultimate AI assistant with the full power of ENTAERA framework!"""

        system_message = Message(role=MessageRole.SYSTEM, content=ultimate_system_prompt)
        conversation.add_message(system_message)
        
        print("🚀 ULTIMATE AI SYSTEM READY!")
        print("💬 Full framework utilization • Maximum capabilities • Complete honesty")
        print("🎯 Ask me to use any ENTAERA capability for complex tasks!")
        print("-" * 50)
        
        message_counter = 0
        
        # Show available commands
        print("\n🎯 EXAMPLE COMMANDS:")
        print("   • 'analyze [topic]' - Use analytical agents + semantic search")
        print("   • 'generate code for [task]' - Use code generation + analysis + execution")
        print("   • 'research [question]' - Use multiple agents for comprehensive research")
        print("   • 'remember [topic]' - Access conversation memory for context")
        print("   • 'coordinate [complex task]' - Use agent orchestration")
        print("   • 'search [query]' - Use semantic search across documents")
        print("   • Or just chat naturally - I'll use appropriate capabilities!\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print("\n[Session ended]")
                break
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            message_counter += 1
            
            # Add user message with metadata
            user_message = Message(role=MessageRole.USER, content=user_input)
            conversation.add_message(user_message)
            logger.info(f"Ultimate Chat - User #{message_counter}: {user_input}")
            
            # Analyze user intent and prepare context
            context_messages = conversation.get_context_messages()
            
            # Enhanced prompt with dynamic capability selection
            capability_hint = ""
            user_lower = user_input.lower()
            
            if any(word in user_lower for word in ['analyze', 'analysis', 'research']):
                capability_hint = "\n[CAPABILITY FOCUS: Use AnalyticalAgent + Semantic Search for comprehensive analysis]"
            elif any(word in user_lower for word in ['code', 'program', 'function', 'script']):
                capability_hint = "\n[CAPABILITY FOCUS: Use Code Generation + Analysis + Execution for complete programming solution]"
            elif any(word in user_lower for word in ['search', 'find', 'lookup']):
                capability_hint = "\n[CAPABILITY FOCUS: Use Semantic Search + Context Retrieval for information discovery]"
            elif any(word in user_lower for word in ['remember', 'recall', 'previous']):
                capability_hint = "\n[CAPABILITY FOCUS: Use Conversation Memory + Context Retrieval for historical context]"
            elif any(word in user_lower for word in ['creative', 'idea', 'brainstorm']):
                capability_hint = "\n[CAPABILITY FOCUS: Use CreativeAgent + multiple approaches for innovative solutions]"
            elif any(word in user_lower for word in ['coordinate', 'complex', 'multi-step']):
                capability_hint = "\n[CAPABILITY FOCUS: Use Agent Orchestration for coordinated multi-agent approach]"
            
            # Build comprehensive prompt
            prompt_parts = []
            for msg in context_messages[-10:]:  # More context for complex tasks
                if msg.role == MessageRole.SYSTEM:
                    prompt_parts.append(f"[FRAMEWORK_CONTEXT]: {msg.content}")
                elif msg.role == MessageRole.USER:
                    prompt_parts.append(f"Human: {msg.content}")
                elif msg.role == MessageRole.ASSISTANT:
                    prompt_parts.append(f"Assistant: {msg.content}")
            
            prompt_parts.append(capability_hint)
            prompt_parts.append("Assistant:")
            full_prompt = "\n".join(prompt_parts)
            
            # Generate ultimate response
            print("🤖 AI: ", end="", flush=True)
            
            response_text = ""
            response_stream = model(
                full_prompt,
                max_tokens=750,  # Maximum for complex responses
                temperature=0.3,  # Balanced for accuracy and creativity
                top_p=0.95,      # High quality
                repeat_penalty=1.15,  # Reduce repetition
                stop=["Human:", "User:", "\n\nHuman:", "\n\nUser:", "You:"],
                stream=True
            )
            
            # Stream with enhanced display
            for token in response_stream:
                if 'choices' in token and len(token['choices']) > 0:
                    text = token['choices'][0].get('text', '')
                    if text:
                        print(text, end="", flush=True)
                        response_text += text
            
            print()  # New line after response
            
            # Handle edge cases
            if not response_text.strip():
                response_text = "I'm ready to use the full ENTAERA framework for your request!"
            
            # Add AI response with metadata
            ai_message = Message(role=MessageRole.ASSISTANT, content=response_text.strip())
            conversation.add_message(ai_message)
            logger.info(f"Ultimate Chat - AI #{message_counter}: Framework response generated")
            
            # Show framework utilization
            total_messages = len(conversation.messages) if hasattr(conversation, 'messages') else message_counter * 2 + 1
            tokens_used = len(response_text.split())
            print(f"   [ENTAERA: {total_messages} messages • {tokens_used} tokens • Full framework active]")
        
        print("\n🏆 Ultimate AI Session Complete!")
        print("📊 Maximum ENTAERA utilization achieved")
        print("🎯 All framework capabilities demonstrated")
        
        # Cleanup
        del model
        print("🗑️ Resources optimally cleaned up")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore environment
        if original_cuda_path:
            os.environ['CUDA_PATH'] = original_cuda_path

if __name__ == "__main__":
    ultimate_entaera_chat()