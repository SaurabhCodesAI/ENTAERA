#!/usr/bin/env python3
"""
Example: Configuration Management
Description: Comprehensive demonstration of ENTAERA-Kata configuration system
Concepts: Environment variables, Pydantic validation, settings management
Prerequisites: Basic understanding of environment variables
Time: 10 minutes
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from entaera.core.config import ApplicationSettings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Demonstrate configuration management features."""
    logger.info("🔧 Configuration Management Example")
    
    try:
        # Step 1: Load default configuration
        logger.info("\n📋 Step 1: Loading Default Configuration")
        logger.info("-" * 50)
        
        try:
            config = ApplicationSettings()
        except Exception as config_error:
            logger.warning(f"⚠️  Environment configuration not found: {config_error}")
            logger.info("🔧 Creating demo configuration...")
            # Create demo config
            config = ApplicationSettings(
                secret_key="demo-secret-key-for-configuration-example-32chars",
                environment="development",
                debug=True
            )
        
        # Display basic configuration
        logger.info(f"Application Name: {config.app_name}")
        logger.info(f"Environment: {config.environment}")
        logger.info(f"Debug Mode: {config.debug}")
        logger.info(f"Log Level: {config.log_level}")
        
        # Step 2: Validate configuration
        logger.info("\n✅ Step 2: Configuration Validation")
        logger.info("-" * 50)
        
        # Show how Pydantic validation works
        logger.info("Configuration validation results:")
        logger.info(f"  ✓ Secret key length: {len(config.secret_key)} characters")
        logger.info(f"  ✓ Environment is valid: {config.environment}")
        logger.info(f"  ✓ All required fields present")
        
        # Step 3: Demonstrate environment-specific settings
        logger.info("\n🌍 Step 3: Environment-Specific Settings")
        logger.info("-" * 50)
        
        if config.environment == "development":
            logger.info("Development environment detected:")
            logger.info("  • Debug mode enabled")
            logger.info("  • Detailed logging available")
            logger.info("  • Hot reloading supported")
            logger.info("  • CORS restrictions relaxed")
        elif config.environment == "production":
            logger.info("Production environment detected:")
            logger.info("  • Debug mode disabled")
            logger.info("  • Optimized logging")
            logger.info("  • Security headers enabled")
            logger.info("  • CORS restrictions enforced")
        
        # Step 4: Configuration serialization
        logger.info("\n📄 Step 4: Configuration Serialization")
        logger.info("-" * 50)
        
        # Export configuration (without sensitive data)
        config_dict = config.dict(exclude={'secret_key'})
        logger.info("Configuration exported (sensitive data excluded):")
        for key, value in config_dict.items():
            if not key.endswith('_key') and not key.endswith('_password'):
                logger.info(f"  {key}: {value}")
        
        # Step 5: Dynamic configuration updates
        logger.info("\n🔄 Step 5: Dynamic Configuration Updates")
        logger.info("-" * 50)
        
        # Show how to create configurations programmatically
        test_config = ApplicationSettings(
            app_name="ENTAERA-Test",
            environment="testing",
            debug=True,
            log_level="DEBUG",
            secret_key="a" * 32  # Minimum length for testing
        )
        
        logger.info("Created test configuration:")
        logger.info(f"  App Name: {test_config.app_name}")
        logger.info(f"  Environment: {test_config.environment}")
        logger.info(f"  Debug: {test_config.debug}")
        
        # Step 6: Configuration best practices
        logger.info("\n🎯 Step 6: Configuration Best Practices")
        logger.info("-" * 50)
        
        best_practices = [
            "✓ Use environment variables for sensitive data",
            "✓ Validate configuration at startup",
            "✓ Provide sensible defaults",
            "✓ Document all configuration options",
            "✓ Use type hints for better IDE support",
            "✓ Group related settings together",
            "✓ Avoid hardcoded values in source code"
        ]
        
        for practice in best_practices:
            logger.info(f"  {practice}")
        
        # Step 7: Environment file examples
        logger.info("\n📝 Step 7: Environment File Examples")
        logger.info("-" * 50)
        
        env_examples = {
            "Development": {
                "ENVIRONMENT": "development",
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG",
                "SECRET_KEY": "your-dev-secret-key-32-chars-min"
            },
            "Production": {
                "ENVIRONMENT": "production",
                "DEBUG": "false",
                "LOG_LEVEL": "INFO",
                "SECRET_KEY": "${AZURE_KEY_VAULT_SECRET}"
            }
        }
        
        for env_name, env_vars in env_examples.items():
            logger.info(f"\n{env_name} environment (.env.{env_name.lower()}):")
            for key, value in env_vars.items():
                logger.info(f"  {key}={value}")
        
        # Step 8: Configuration validation errors
        logger.info("\n⚠️  Step 8: Common Configuration Issues")
        logger.info("-" * 50)
        
        common_issues = [
            "❌ SECRET_KEY too short (minimum 32 characters)",
            "❌ Invalid ENVIRONMENT value (must be: development, staging, production)",
            "❌ Missing required API keys for enabled providers",
            "❌ Invalid URL format for endpoints",
            "❌ Conflicting debug and environment settings"
        ]
        
        for issue in common_issues:
            logger.info(f"  {issue}")
        
        logger.info("\n🛠️  How to fix configuration issues:")
        fixes = [
            "• Check .env file syntax (no spaces around =)",
            "• Verify all required variables are set",
            "• Use quotes for values with special characters",
            "• Test configuration with validate_implementation.py",
            "• Check logs for detailed error messages"
        ]
        
        for fix in fixes:
            logger.info(f"  {fix}")
        
        # Success message
        logger.info("\n🎉 Configuration management example completed!")
        
    except Exception as e:
        logger.error(f"❌ Configuration example failed: {e}")
        logger.exception("Full error details:")
        return 1
    
    return 0


if __name__ == "__main__":
    """Run the configuration example."""
    exit_code = asyncio.run(main())
    sys.exit(exit_code)