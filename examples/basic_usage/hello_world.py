#!/usr/bin/env python3
"""
Example: Hello World
Description: Basic ENTAERA-Kata usage demonstration
Concepts: Configuration loading, basic AI interaction, logging setup
Prerequisites: API key for at least one AI provider
Time: 5 minutes
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from entaera.core.config import ApplicationSettings
from entaera.core.logger import LoggerManager

# Setup logging for the example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Demonstrate basic ENTAERA-Kata functionality."""
    logger.info("🚀 Starting ENTAERA-Kata Hello World Example")
    
    try:
        # Step 1: Load configuration
        logger.info("📋 Loading configuration...")
        try:
            config = ApplicationSettings()
        except Exception as config_error:
            logger.warning(f"⚠️  Configuration loading failed: {config_error}")
            logger.info("🔧 Creating minimal configuration for demo...")
            # Create minimal config for demo purposes
            config = ApplicationSettings(
                secret_key="demo-secret-key-for-example-32-chars",
                environment="development"
            )
        
        logger.info(f"✅ Configuration loaded successfully")
        logger.info(f"   App Name: {config.app_name}")
        logger.info(f"   Environment: {config.environment}")
        
        # Step 2: Initialize logging system
        logger.info("🔧 Setting up logging system...")
        log_manager = LoggerManager()
        log_manager.configure(
            format_type="simple",
            level="INFO",
            console_output=True,
            use_colors=True
        )
        app_logger = log_manager.get_logger("hello_world")
        app_logger.info("✅ Logging system initialized")
        
        # Step 3: Test basic functionality
        app_logger.info("🧪 Testing core components...")
        
        # Test text processing utilities
        from entaera.utils.text_processor import normalize_text, remove_emojis
        
        test_text = "Hello, World! 🌍 Welcome to ENTAERA-Kata! 🤖"
        normalized = normalize_text(test_text)
        clean_text = remove_emojis(test_text)
        
        app_logger.info(f"📝 Text processing test:")
        app_logger.info(f"   Original: '{test_text}'")
        app_logger.info(f"   Normalized: '{normalized}'")
        app_logger.info(f"   Without emojis: '{clean_text}'")
        
        # Step 4: Test file operations
        from entaera.utils.files import ensure_directory
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "test_output"
            ensure_directory(test_dir)
            app_logger.info(f"📁 Created test directory: {test_dir}")
            
            # Write a test file
            test_file = test_dir / "hello.txt"
            test_file.write_text("Hello from ENTAERA-Kata!")
            app_logger.info(f"📄 Created test file: {test_file}")
        
        # Step 5: Demonstrate request ID tracking
        app_logger.info("🔍 Testing request ID tracking...")
        log_manager.set_request_id("hello-world-123")
        app_logger.info("This message has a request ID")
        app_logger.warning("This warning also has the same request ID")
        log_manager.clear_request_id()
        app_logger.info("This message has no request ID")
        
        # Step 6: Success message
        app_logger.info("🎉 Hello World example completed successfully!")
        app_logger.info("🎓 You're ready to explore more advanced features!")
        
        # Provide next steps
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        print("1. 📖 Explore configuration options in examples/basic_usage/configuration.py")
        print("2. 🤖 Try AI provider examples in examples/ai_providers/")
        print("3. 🔬 Learn about research automation in examples/research/")
        print("4. 📚 Read the full documentation at docs/")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Error in Hello World example: {e}")
        logger.exception("Full error details:")
        return 1
    
    return 0


if __name__ == "__main__":
    """Run the example directly."""
    exit_code = asyncio.run(main())
    sys.exit(exit_code)