"""
Day 2 Kata Demonstration
========================

This script demonstrates the combined functionality of:
1. Configuration management (config.py)
2. Logging infrastructure (logger.py)

Run this script to see the kata implementations in action.
"""

import os
import sys
from pathlib import Path
import tempfile
import uuid

# Add the parent directory to sys.path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from entaera.core.config import (
        ApplicationSettings,
        APIProviderSettings,
        ServerSettings,
        load_settings,
        kata_practice_config
    )
    from entaera.core.logger import (
        configure_logging,
        get_logger,
        set_request_id,
        clear_request_id,
        log_info,
        log_error,
        log_warning,
        log_debug,
        kata_practice_logging
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure the project structure is correct and dependencies are installed.")
    sys.exit(1)


def run_config_kata_demo():
    """Run the configuration kata demonstration."""
    print("\n🔧 Configuration Kata Demo")
    print("=" * 40)
    
    # Create a temporary .env file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("""
# ENTAERA Configuration
VERTEX_AUTO_GPT_APP_NAME=Kata Demo App
VERTEX_AUTO_GPT_VERSION=1.0.0
VERTEX_AUTO_GPT_ENVIRONMENT=development

# API Provider Settings
VERTEX_AUTO_GPT_OPENAI_API_KEY=sk-demo123456789
VERTEX_AUTO_GPT_DEFAULT_PROVIDER=openai
VERTEX_AUTO_GPT_MAX_TOKENS=2048
VERTEX_AUTO_GPT_TEMPERATURE=0.7

# Server Settings
VERTEX_AUTO_GPT_SERVER_PORT=9000
VERTEX_AUTO_GPT_SERVER_DEBUG=true
""")
        dotenv_path = f.name
    
    try:
        print("1. Loading settings from .env file...")
        settings = load_settings(dotenv_path=dotenv_path)
        
        print(f"✅ App Name: {settings.app_name}")
        print(f"✅ Environment: {settings.environment}")
        print(f"✅ API Provider: {settings.api.default_provider}")
        print(f"✅ API Key: {settings.api.openai_api_key[:5]}...")
        print(f"✅ Server Port: {settings.server.port}")
        print(f"✅ Debug Mode: {settings.server.debug}")
        
        print("\n2. Creating custom settings...")
        custom_settings = ApplicationSettings(
            app_name="Custom Demo",
            version="2.0.0",
            environment="testing",
            api=APIProviderSettings(
                openai_api_key="sk-custom12345",
                temperature=0.5,
                max_tokens=4096
            ),
            server=ServerSettings(
                port=8080,
                workers=4
            )
        )
        
        print(f"✅ Custom App Name: {custom_settings.app_name}")
        print(f"✅ Custom Environment: {custom_settings.environment}")
        print(f"✅ Custom Temperature: {custom_settings.api.temperature}")
        print(f"✅ Custom Workers: {custom_settings.server.workers}")
        
        print("\n3. Running config kata practice function...")
        practice_results = kata_practice_config()
        
        print(f"✅ Settings Created: {practice_results['settings_created']}")
        print(f"✅ Validation Passed: {practice_results['validation_passed']}")
        print(f"✅ Learning notes: {len(practice_results['learning_notes'])} items")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in config demo: {e}")
        return False
    finally:
        os.unlink(dotenv_path)


def run_logging_kata_demo():
    """Run the logging kata demonstration."""
    print("\n📝 Logging Kata Demo")
    print("=" * 40)
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = "kata_demo.log"
            
            print("1. Configuring logging system...")
            configure_logging(
                level="DEBUG",
                format_type="simple",
                log_file=log_file,
                log_dir=temp_dir,
                max_size="1MB",
                backup_count=3,
                console_output=True,
                use_colors=True
            )
            
            logger = get_logger("demo.kata")
            print("✅ Logging configured")
            
            print("\n2. Using different log levels...")
            logger.debug("This is a debug message with technical details")
            logger.info("This is an info message about normal operation")
            logger.warning("This is a warning - something might need attention")
            logger.error("This is an error - something went wrong")
            
            print("\n3. Using request ID for context tracking...")
            request_id = str(uuid.uuid4())
            print(f"Request ID: {request_id}")
            
            set_request_id(request_id)
            logger.info("Processing user request", user_id="demo_user", action="login")
            logger.info("User authenticated", method="password")
            
            clear_request_id()
            print("✅ Request context demonstrated")
            
            print("\n4. Handling exceptions...")
            try:
                # Simulate an error
                result = 1 / 0
            except Exception:
                logger.exception("Division by zero error occurred")
                print("✅ Exception logged properly")
            
            print("\n5. Using convenience functions...")
            log_debug("Debug from convenience function")
            log_info("Info from convenience function", component="demo")
            log_warning("Warning from convenience function")
            log_error("Error from convenience function")
            
            print("\n6. Running logging kata practice function...")
            practice_results = kata_practice_logging()
            
            if practice_results["logging_configured"]:
                print(f"✅ Log entries: {practice_results['log_entries']}")
                print(f"✅ Log levels tested: {', '.join(practice_results['log_levels_tested'])}")
                print(f"✅ Exception logged: {practice_results['exception_logged']}")
                print(f"✅ Learning notes: {len(practice_results['learning_notes'])} items")
            else:
                print(f"❌ Logging practice error: {practice_results.get('error')}")
            
            # Check log file
            log_path = Path(temp_dir) / log_file
            if log_path.exists():
                file_size = log_path.stat().st_size
                print(f"\n✅ Log file created: {log_file} ({file_size} bytes)")
            
            return True
    
    except Exception as e:
        print(f"❌ Error in logging demo: {e}")
        return False


def run_integration_demo():
    """Run an integration demo with both config and logging."""
    print("\n🔄 Integration Demo")
    print("=" * 40)
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""
# ENTAERA Configuration
VERTEX_AUTO_GPT_APP_NAME=Integration Demo
VERTEX_AUTO_GPT_VERSION=1.0.0
VERTEX_AUTO_GPT_ENVIRONMENT=demo

# Logging Settings
VERTEX_AUTO_GPT_LOG_LEVEL=DEBUG
VERTEX_AUTO_GPT_LOG_FORMAT=structured
""")
            dotenv_path = f.name
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Load settings from .env
            settings = load_settings(dotenv_path=dotenv_path)
            print(f"✅ Loaded settings for: {settings.app_name}")
            
            # Configure logging based on settings
            log_level = getattr(settings, "log_level", "INFO")
            log_format = getattr(settings, "log_format", "simple")
            
            configure_logging(
                level=log_level,
                format_type=log_format,
                log_file="integration.log",
                log_dir=temp_dir,
                console_output=True
            )
            
            logger = get_logger("integration.demo")
            logger.info(f"Application started: {settings.app_name}", 
                       version=settings.version,
                       env=settings.environment)
            
            # Simulate API request with tracking
            req_id = str(uuid.uuid4())[:8]
            set_request_id(req_id)
            
            logger.info("Processing API request", 
                       provider=settings.api.default_provider,
                       max_tokens=settings.api.max_tokens)
            
            # Simulate response handling
            logger.info("API response received", 
                       tokens_used=1024,
                       completion_time_ms=350)
            
            # Clear context
            clear_request_id()
            
            print(f"✅ Integration demo completed")
            print(f"✅ Log file: {Path(temp_dir) / 'integration.log'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error in integration demo: {e}")
        return False
    finally:
        os.unlink(dotenv_path)


if __name__ == "__main__":
    print("\n🥋 Day 2 Kata Demonstration: Configuration & Logging 🥋")
    print("=" * 60)
    
    config_success = run_config_kata_demo()
    logging_success = run_logging_kata_demo()
    integration_success = run_integration_demo()
    
    print("\n" + "=" * 60)
    print("Day 2 Kata Results:")
    print(f"✅ Configuration: {'Success' if config_success else 'Failed'}")
    print(f"✅ Logging: {'Success' if logging_success else 'Failed'}")
    print(f"✅ Integration: {'Success' if integration_success else 'Failed'}")
    
    overall = all([config_success, logging_success, integration_success])
    print(f"\n{'🎉 Day 2 Kata Completed Successfully!' if overall else '❌ Some demonstrations failed.'}")