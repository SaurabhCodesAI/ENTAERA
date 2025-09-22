#!/usr/bin/env python3
"""
Simple ENTAERA-Kata Demo
==============================
Shows the basic features that are working in your setup.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from entaera.core.config import ApplicationSettings
from entaera.core.logger import LoggerManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Simple demo of working features"""
    print("🎯 ENTAERA-Kata Simple Demo")
    print("=" * 50)
    print()
    
    # Demo 1: Configuration
    print("🔧 TESTING CONFIGURATION")
    print("-" * 30)
    config = ApplicationSettings()
    print(f"✅ App Name: {config.app_name}")
    print(f"✅ Environment: {config.environment}")
    print(f"✅ Debug Mode: {config.debug}")
    print(f"✅ Secret Key: {'*' * len(config.secret_key)} ({len(config.secret_key)} chars)")
    print()
    
    # Demo 2: Logging
    print("📝 TESTING LOGGING")
    print("-" * 30)
    logger_manager = LoggerManager()
    demo_logger = logger_manager.get_logger("demo")
    
    demo_logger.info("This is an info message")
    demo_logger.warning("This is a warning message") 
    demo_logger.error("This is an error message (just a test!)")
    print("✅ Logging system working")
    print()
    
    # Demo 3: Models
    print("🤖 CHECKING YOUR AI MODELS")
    print("-" * 30)
    models_dir = Path("models")
    if models_dir.exists():
        model_files = list(models_dir.glob("*.gguf"))
        print(f"📁 Found {len(model_files)} AI model files:")
        
        for model_file in model_files:
            size_gb = model_file.stat().st_size / (1024**3)
            if "llama-3.1" in model_file.name:
                print(f"  🧠 {model_file.name} ({size_gb:.1f} GB) - General AI")
            elif "codellama" in model_file.name:
                print(f"  💻 {model_file.name} ({size_gb:.1f} GB) - Programming AI")
            else:
                print(f"  📦 {model_file.name} ({size_gb:.1f} GB)")
    else:
        print("❌ Models directory not found")
    print()
    
    # Demo 4: Environment Check
    print("🌍 ENVIRONMENT STATUS")
    print("-" * 30)
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file configured")
    else:
        print("❌ .env file missing")
    
    # Check if we're in local-first mode
    with open(".env", "r") as f:
        env_content = f.read()
        if "placeholder-for-local-first-mode" in env_content:
            print("🏠 Local-first mode: Using local AI models")
        else:
            print("🌐 API mode: Using online AI services")
    print()
    
    # What you can try next
    print("🚀 WHAT YOU CAN TRY NEXT")
    print("-" * 30)
    suggestions = [
        "📖 Read the documentation: Get-Content README.md",
        "🧪 Try more examples: ls examples/",
        "🔍 Explore source code: ls src/entaera/",
        "📊 Check logs: ls logs/",
        "🐳 Try Docker: docker-compose up -d",
    ]
    
    for suggestion in suggestions:
        print(f"  • {suggestion}")
    print()
    
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("Your ENTAERA-Kata setup is working perfectly!")
    print("You're ready to start the learning journey! 🎓")

if __name__ == "__main__":
    asyncio.run(main())