#!/usr/bin/env python3
"""
Test Local AI Models
====================
A simple test to see if your local models can be loaded.
This doesn't run inference yet, just checks if the models are accessible.
"""

import sys
from pathlib import Path

def test_models():
    """Test if the local AI models are properly set up"""
    print("🤖 Testing Local AI Model Setup")
    print("=" * 40)
    
    models_dir = Path("models")
    
    # Check if models directory exists
    if not models_dir.exists():
        print("❌ Models directory not found")
        return False
    
    # Check for specific model files
    expected_models = {
        "llama-3.1-8b-instruct.Q4_K_M.gguf": "General AI (Chat & Reasoning)",
        "codellama-7b-instruct.Q4_K_M.gguf": "Programming AI (Code Generation)"
    }
    
    found_models = []
    for model_file, description in expected_models.items():
        model_path = models_dir / model_file
        if model_path.exists():
            size_gb = model_path.stat().st_size / (1024**3)
            print(f"✅ {model_file}")
            print(f"   📊 Size: {size_gb:.1f} GB")
            print(f"   🎯 Purpose: {description}")
            found_models.append(model_file)
        else:
            print(f"❌ {model_file} - Not found")
    
    print(f"\n📈 Model Status: {len(found_models)}/{len(expected_models)} models ready")
    
    # Check environment configuration
    print(f"\n🔧 Environment Configuration:")
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            
        # Check for local AI settings
        local_settings = [
            "LOCAL_AI_ENABLED",
            "CUDA_ENABLED", 
            "CODE_MODEL_PATH",
            "CHAT_MODEL_PATH",
            "EMBEDDING_MODEL"
        ]
        
        for setting in local_settings:
            if setting in content:
                print(f"   ✅ {setting} configured")
            else:
                print(f"   ❌ {setting} not found")
    else:
        print("   ❌ .env file not found")
    
    # Check if we have the dependencies for local AI
    print(f"\n📦 Local AI Dependencies:")
    try:
        import torch
        print(f"   ✅ PyTorch {torch.__version__}")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"   ✅ CUDA GPU: {gpu_name}")
        else:
            print(f"   ⚠️  CUDA not available (will use CPU)")
            
    except ImportError:
        print("   ❌ PyTorch not found")
    
    try:
        import sentence_transformers
        print(f"   ✅ Sentence Transformers")
    except ImportError:
        print("   ❌ Sentence Transformers not found")
    
    try:
        import llama_cpp
        print(f"   ✅ Llama.cpp Python bindings")
    except (ImportError, FileNotFoundError) as e:
        if "CUDA_PATH" in str(e):
            print("   ⚠️  Llama.cpp found but CUDA path issue (OK for CPU)")
        else:
            print("   ❌ Llama.cpp Python bindings not found")
    
    # Summary
    print(f"\n" + "="*40)
    if len(found_models) == len(expected_models):
        print("🎉 Your local AI setup is ready!")
        print("✅ All models downloaded and configured")
        print("🚀 You can use local AI without API keys")
    else:
        print("⚠️  Partial setup - some models missing")
        print("💡 Run: python setup_models.py --interactive")
    
    return len(found_models) == len(expected_models)

if __name__ == "__main__":
    test_models()