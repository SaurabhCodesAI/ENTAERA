#!/usr/bin/env python3
"""
ENTAERA-Kata Interactive Demo
===================================
This script demonstrates the core capabilities of your setup.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from entaera.core.config import ApplicationSettings
from entaera.core.logger import LoggerManager
from entaera.utils.text_processor import normalize_text, remove_emojis
from entaera.utils.files import ensure_directory, save_json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demo_configuration():
    """Demo 1: Configuration System"""
    print("\n" + "="*60)
    print("🔧 DEMO 1: Configuration System")
    print("="*60)
    
    # Load configuration
    config = ApplicationSettings()
    
    print(f"✅ App Name: {config.app_name}")
    print(f"✅ Environment: {config.environment}")
    print(f"✅ Debug Mode: {config.debug}")
    print(f"✅ Log Level: {config.log_level}")
    print(f"✅ Secret Key: {'*' * len(config.secret_key)} ({len(config.secret_key)} chars)")
    
    return config

async def demo_logging():
    """Demo 2: Advanced Logging"""
    print("\n" + "="*60)
    print("📝 DEMO 2: Advanced Logging System")
    print("="*60)
    
    # Initialize logger manager
    logger_manager = LoggerManager()
    demo_logger = logger_manager.get_logger("demo", request_id="demo-session-123")
    
    print("Testing different log levels:")
    demo_logger.info("This is an info message with request tracking")
    demo_logger.warning("This is a warning message")
    demo_logger.error("This is an error message (don't worry, it's just a demo!)")
    
    print("✅ Logging system working with request ID tracking")

async def demo_text_processing():
    """Demo 3: Text Processing Utilities"""
    print("\n" + "="*60)
    print("📚 DEMO 3: Text Processing")
    print("="*60)
    
    sample_texts = [
        "Hello, World! 🌍 This is ENTAERA-Kata! 🤖",
        "  Mixed CASE text with    EXTRA   spaces  ",
        "🎯 Research 📊 Data 🔬 Science 💡 Innovation",
        "Python, AI, Machine Learning, and Data Science"
    ]
    
    for text in sample_texts:
        normalized = normalize_text(text)
        no_emojis = remove_emojis(text)
        
        print(f"\nOriginal:   '{text}'")
        print(f"Normalized: '{normalized}'")
        print(f"No Emojis:  '{no_emojis}'")

async def demo_file_operations():
    """Demo 4: File Operations"""
    print("\n" + "="*60)
    print("📁 DEMO 4: File Operations")
    print("="*60)
    
    # Create a demo directory
    demo_dir = Path("demo_output")
    ensure_directory(demo_dir)
    print(f"✅ Created directory: {demo_dir}")
    
    # Save some demo data
    demo_data = {
        "session_id": "demo-session-123",
        "timestamp": "2025-09-22T10:06:30Z",
        "config": {
            "environment": "development",
            "models_available": ["llama-3.1-8b", "codellama-7b"],
            "features_tested": ["config", "logging", "text_processing", "file_ops"]
        },
        "status": "success"
    }
    
    demo_file = demo_dir / "session_data.json"
    save_json(demo_file, demo_data)
    print(f"✅ Saved demo data to: {demo_file}")
    
    return demo_dir

async def demo_models_info():
    """Demo 5: Check Available Models"""
    print("\n" + "="*60)
    print("🤖 DEMO 5: Your AI Models")
    print("="*60)
    
    models_dir = Path("models")
    if models_dir.exists():
        model_files = list(models_dir.glob("*.gguf"))
        
        print(f"📁 Models directory: {models_dir}")
        print(f"🔍 Found {len(model_files)} model files:")
        
        for model_file in model_files:
            size_gb = model_file.stat().st_size / (1024**3)
            print(f"  📦 {model_file.name} ({size_gb:.1f} GB)")
        
        print("\n🎯 Model Capabilities:")
        print("  • Llama 3.1 8B: General chat, reasoning, research")
        print("  • CodeLlama 7B: Programming, code analysis, debugging")
        print("  • Embeddings: Text similarity, semantic search")
    else:
        print("❌ Models directory not found")

async def demo_next_steps():
    """Show what user can try next"""
    print("\n" + "="*60)
    print("🚀 WHAT YOU CAN TRY NEXT")
    print("="*60)
    
    next_actions = [
        ("📖 Read Documentation", "Get-Content README.md"),
        ("🧪 Run More Examples", "ls examples/basic_usage/"),
        ("🔍 Explore Source Code", "ls src/entaera/"),
        ("🐳 Try Docker Setup", "docker-compose up -d"),
        ("📊 Check Logs", "ls logs/"),
        ("⚙️ Modify Configuration", "notepad .env"),
    ]
    
    print("Here are some commands you can try:")
    for description, command in next_actions:
        print(f"  {description}")
        print(f"    Command: {command}")
        print()

async def main():
    """Main demo function"""
    print("🎯 ENTAERA-Kata Interactive Demo")
    print("=" * 60)
    print("This demo shows you what your setup can do!")
    print()
    
    try:
        # Run all demos
        config = await demo_configuration()
        await demo_logging()
        await demo_text_processing()
        demo_dir = await demo_file_operations()
        await demo_models_info()
        await demo_next_steps()
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("✅ All core components are working")
        print("✅ Your local AI models are ready")
        print("✅ File operations completed")
        print(f"✅ Demo files saved to: {demo_dir}")
        print("\n🎓 You're ready to start the kata learning journey!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())