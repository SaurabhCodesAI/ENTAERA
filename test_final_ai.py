#!/usr/bin/env python3
"""
🚀 FINAL AI CHAT TEST - Real Model Integration
==============================================
"""

import sys
import os
sys.path.append('src')

def test_model_loading():
    """Test all aspects of model loading"""
    print("🧪 COMPREHENSIVE MODEL LOADING TEST")
    print("=" * 50)
    
    try:
        # Test import
        print("1️⃣ Testing imports...")
        from local_model_loader import LocalModelLoader, SmartResponseGenerator
        print("   ✅ Imports successful")
        
        # Test environment
        print("\n2️⃣ Testing environment...")
        llama_path = os.environ.get('LLAMA_MODEL_PATH', 'Not set')
        print(f"   LLAMA_MODEL_PATH: {llama_path}")
        
        if llama_path != 'Not set':
            model_exists = os.path.exists(llama_path)
            print(f"   Model file exists: {model_exists}")
            if model_exists:
                size_gb = os.path.getsize(llama_path) / (1024**3)
                print(f"   Model size: {size_gb:.1f}GB")
        
        # Test llama-cpp-python
        print("\n3️⃣ Testing llama-cpp-python...")
        try:
            from llama_cpp import Llama
            print("   ✅ llama_cpp import successful")
        except Exception as e:
            print(f"   ❌ llama_cpp import failed: {e}")
        
        # Test CUDA
        print("\n4️⃣ Testing CUDA...")
        cuda_path = os.environ.get('CUDA_PATH', 'Not set')
        print(f"   CUDA_PATH: {cuda_path}")
        
        if cuda_path != 'Not set':
            cuda_bin = os.path.join(cuda_path, 'bin')
            print(f"   CUDA bin exists: {os.path.exists(cuda_bin)}")
        
        # Test model loader
        print("\n5️⃣ Testing model loader...")
        loader = LocalModelLoader()
        print(f"   Loader created: {loader}")
        
        # Test generator
        print("\n6️⃣ Testing response generator...")
        generator = SmartResponseGenerator()
        success = generator.initialize()
        print(f"   Generator initialized: {success}")
        
        # Test response
        print("\n7️⃣ Testing response generation...")
        test_prompt = "Hello! What's 2+2?"
        response = generator.generate_response(test_prompt)
        print(f"   Test prompt: {test_prompt}")
        print(f"   Response: {response[:100]}...")
        
        print("\n🎯 MODEL LOADING SUMMARY:")
        print(f"   Model file: {'✅' if llama_path != 'Not set' and os.path.exists(llama_path) else '❌'}")
        print(f"   llama-cpp-python: {'✅' if 'llama_cpp' in sys.modules else '❌'}")
        print(f"   Generator: {'✅' if success else '❌'}")
        print(f"   Response quality: {'✅' if '4' in response or 'four' in response.lower() else '🔄 Fallback'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def simple_chat_fixed():
    """Simple chat with error handling fixes"""
    print("\n🤖 SIMPLE CHAT (FIXED)")
    print("=" * 30)
    
    try:
        from entaera.core.conversation import ConversationManager, Message, MessageRole
        from local_model_loader import SmartResponseGenerator
        
        # Initialize
        conv_manager = ConversationManager()
        conversation = conv_manager.create_conversation("Fixed Chat")
        generator = SmartResponseGenerator()
        generator.initialize()
        
        print("✅ Chat system ready!")
        print("💬 Type 'quit' to exit")
        
        message_count = 0
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            message_count += 1
            
            # Add user message
            user_message = Message(role=MessageRole.USER, content=user_input)
            conversation.add_message(user_message)
            
            # Generate response
            response = generator.generate_response(user_input)
            print(f"🤖 AI: {response}")
            
            # Add AI message
            ai_message = Message(role=MessageRole.ASSISTANT, content=response)
            conversation.add_message(ai_message)
            
            # Show progress every 5 messages
            if message_count % 5 == 0:
                total_messages = len(conversation.messages) if hasattr(conversation, 'messages') else message_count * 2
                print(f"\n📊 Messages exchanged: {total_messages}")
        
        print("\n👋 Chat ended!")
        
        # Clean up if model loaded
        if hasattr(generator, 'model_loader') and generator.model_loader.is_loaded():
            print("🗑️ Unloading model...")
            generator.model_loader.unload_model()
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment
    env_file = ".env.local_ai"
    if os.path.exists(env_file):
        print("🔧 Loading environment...")
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    print("Choose test:")
    print("1. Model Loading Test")
    print("2. Simple Chat (Fixed)")
    print("3. Both")
    
    choice = input("Enter 1, 2, or 3: ").strip()
    
    if choice in ["1", "3"]:
        model_works = test_model_loading()
        
    if choice in ["2", "3"]:
        if choice == "3":
            print("\n" + "="*50)
        simple_chat_fixed()