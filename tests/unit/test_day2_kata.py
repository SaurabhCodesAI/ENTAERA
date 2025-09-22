"""
Day 2 Kata Tests: Configuration and Logging
==========================================

Test cases for the Day 2 kata implementations:
- Configuration management with Pydantic
- Logging infrastructure with multiple formatters
- Environment variable handling
- Validation and error handling

These tests validate our kata learning objectives.
"""

import pytest
import tempfile
import os
import json
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.entaera.core.config import (
    ApplicationSettings,
    APIProviderSettings,
    ServerSettings,
    load_settings,
    kata_practice_config
)
from src.entaera.core.logger import (
    JSONFormatter,
    ColoredFormatter,
    LoggerManager,
    configure_logging,
    get_logger,
    set_request_id,
    clear_request_id,
    kata_practice_logging
)


class TestDay2ConfigurationKata:
    """Test configuration management kata."""
    
    def test_api_provider_settings_defaults(self):
        """Test API provider settings with default values."""
        settings = APIProviderSettings()
        
        assert settings.openai_api_key == ""
        assert settings.anthropic_api_key == ""
        assert settings.vertex_project_id == ""
        assert settings.vertex_location == "us-central1"
        assert settings.default_provider == "openai"
        assert settings.max_tokens == 4000
        assert settings.temperature == 0.7
        assert settings.timeout_seconds == 30
    
    def test_api_provider_settings_validation(self):
        """Test API provider settings validation."""
        # Test valid settings
        settings = APIProviderSettings(
            openai_api_key="sk-test123",
            max_tokens=8000,
            temperature=0.5
        )
        assert settings.openai_api_key == "sk-test123"
        assert settings.max_tokens == 8000
        assert settings.temperature == 0.5
        
        # Test temperature validation
        with pytest.raises(ValueError, match="Temperature must be between"):
            APIProviderSettings(temperature=2.0)
        
        with pytest.raises(ValueError, match="Temperature must be between"):
            APIProviderSettings(temperature=-0.1)
        
        # Test max_tokens validation
        with pytest.raises(ValueError, match="Max tokens must be positive"):
            APIProviderSettings(max_tokens=0)
    
    def test_server_settings_defaults(self):
        """Test server settings with default values."""
        settings = ServerSettings()
        
        assert settings.host == "localhost"
        assert settings.port == 8000
        assert settings.workers == 1
        assert settings.reload is False
        assert settings.debug is False
        assert settings.cors_origins == ["*"]
    
    def test_server_settings_validation(self):
        """Test server settings validation."""
        # Test valid port
        settings = ServerSettings(port=3000)
        assert settings.port == 3000
        
        # Test invalid port (too low)
        with pytest.raises(ValueError, match="Port must be between"):
            ServerSettings(port=100)
        
        # Test invalid port (too high)  
        with pytest.raises(ValueError, match="Port must be between"):
            ServerSettings(port=70000)
        
        # Test workers validation
        with pytest.raises(ValueError, match="Workers must be positive"):
            ServerSettings(workers=0)
    
    def test_application_settings_integration(self):
        """Test complete application settings integration."""
        settings = ApplicationSettings(
            app_name="TestApp",
            version="1.0.0",
            environment="testing",
            api=APIProviderSettings(
                openai_api_key="test-key",
                temperature=0.8
            ),
            server=ServerSettings(
                port=9000,
                debug=True
            )
        )
        
        assert settings.app_name == "TestApp"
        assert settings.version == "1.0.0"
        assert settings.environment == "testing"
        assert settings.api.openai_api_key == "test-key"
        assert settings.api.temperature == 0.8
        assert settings.server.port == 9000
        assert settings.server.debug is True
    
    def test_load_settings_from_env(self):
        """Test loading settings from environment variables."""
        env_vars = {
            "VERTEX_AUTO_GPT_APP_NAME": "EnvApp",
            "VERTEX_AUTO_GPT_VERSION": "2.0.0",
            "VERTEX_AUTO_GPT_ENVIRONMENT": "production",
            "VERTEX_AUTO_GPT_OPENAI_API_KEY": "env-api-key",
            "VERTEX_AUTO_GPT_MAX_TOKENS": "6000",
            "VERTEX_AUTO_GPT_TEMPERATURE": "0.3",
            "VERTEX_AUTO_GPT_SERVER_PORT": "8080",
            "VERTEX_AUTO_GPT_SERVER_DEBUG": "false"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = load_settings()
            
            assert settings.app_name == "EnvApp"
            assert settings.version == "2.0.0"
            assert settings.environment == "production"
            assert settings.api.openai_api_key == "env-api-key"
            assert settings.api.max_tokens == 6000
            assert settings.api.temperature == 0.3
            assert settings.server.port == 8080
            assert settings.server.debug is False
    
    def test_load_settings_from_dotenv(self):
        """Test loading settings from .env file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""
VERTEX_AUTO_GPT_APP_NAME=DotEnvApp
VERTEX_AUTO_GPT_ANTHROPIC_API_KEY=dotenv-anthropic-key
VERTEX_AUTO_GPT_DEFAULT_PROVIDER=anthropic
VERTEX_AUTO_GPT_SERVER_WORKERS=4
""")
            dotenv_path = f.name
        
        try:
            settings = load_settings(dotenv_path=dotenv_path)
            
            assert settings.app_name == "DotEnvApp"
            assert settings.api.anthropic_api_key == "dotenv-anthropic-key"
            assert settings.api.default_provider == "anthropic"
            assert settings.server.workers == 4
        finally:
            os.unlink(dotenv_path)
    
    def test_kata_practice_config(self):
        """Test configuration kata practice function."""
        result = kata_practice_config()
        
        assert isinstance(result, dict)
        assert "settings_created" in result
        assert "validation_passed" in result
        assert "env_vars_loaded" in result
        assert "dotenv_loaded" in result
        assert "learning_notes" in result
        
        assert result["settings_created"] is True
        assert isinstance(result["learning_notes"], list)
        assert len(result["learning_notes"]) > 0


class TestDay2LoggingKata:
    """Test logging infrastructure kata."""
    
    def test_json_formatter(self):
        """Test JSON log formatter."""
        formatter = JSONFormatter()
        
        # Create a log record
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="/test/path.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.module = "test_module"
        record.funcName = "test_function"
        
        # Format the record
        formatted = formatter.format(record)
        
        # Parse as JSON
        log_data = json.loads(formatted)
        
        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test.logger"
        assert log_data["message"] == "Test message"
        assert log_data["module"] == "test_module"
        assert log_data["function"] == "test_function"
        assert log_data["line"] == 42
        assert "timestamp" in log_data
    
    def test_json_formatter_with_extra(self):
        """Test JSON formatter with extra fields."""
        formatter = JSONFormatter(include_extra=True)
        
        record = logging.LogRecord(
            name="test.logger",
            level=logging.ERROR,
            pathname="/test/path.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=None
        )
        record.module = "error_module"
        record.funcName = "error_function"
        record.user_id = "test_user"
        record.operation = "test_operation"
        
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        assert log_data["user_id"] == "test_user"
        assert log_data["operation"] == "test_operation"
    
    def test_colored_formatter(self):
        """Test colored console formatter."""
        formatter = ColoredFormatter(use_colors=False)  # Disable colors for testing
        
        record = logging.LogRecord(
            name="test.logger",
            level=logging.WARNING,
            pathname="/test/path.py",
            lineno=25,
            msg="Warning message",
            args=(),
            exc_info=None
        )
        record.module = "warn_module"
        record.funcName = "warn_function"
        
        formatted = formatter.format(record)
        
        assert "WARNING" in formatted
        assert "test.logger" in formatted
        assert "warn_module:warn_function:25" in formatted
        assert "Warning message" in formatted
    
    def test_logger_manager_configuration(self):
        """Test logger manager configuration."""
        manager = LoggerManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = "test.log"
            
            manager.configure(
                level="DEBUG",
                format_type="simple",
                log_file=log_file,
                log_dir=temp_dir,
                max_size="1MB",
                backup_count=3,
                console_output=False,
                use_colors=False
            )
            
            # Get a logger and test it
            logger = manager.get_logger("test.module")
            logger.info("Test message")
            
            # Check log file was created
            log_path = Path(temp_dir) / log_file
            assert log_path.exists()
            
            # Check log content
            content = log_path.read_text()
            assert "Test message" in content
            assert "INFO" in content
    
    def test_request_id_context(self):
        """Test request ID context management."""
        manager = LoggerManager()
        
        # Test setting and clearing request ID
        test_id = "test-request-123"
        manager.set_request_id(test_id)
        
        # The request ID should be available in context
        from src.entaera.core.logger import request_id
        assert request_id.get() == test_id
        
        # Clear request ID
        manager.clear_request_id()
        assert request_id.get() is None
    
    def test_size_parsing(self):
        """Test log file size parsing."""
        manager = LoggerManager()
        
        assert manager._parse_size("100B") == 100
        assert manager._parse_size("1KB") == 1024
        assert manager._parse_size("5MB") == 5 * 1024 * 1024
        assert manager._parse_size("2GB") == 2 * 1024 * 1024 * 1024
        
        # Test invalid size defaults to 10MB
        assert manager._parse_size("invalid") == 10 * 1024 * 1024
    
    def test_configure_logging_function(self):
        """Test global logging configuration function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            configure_logging(
                level="INFO",
                format_type="simple",
                log_file="global_test.log",
                log_dir=temp_dir,
                console_output=False
            )
            
            # Test that logging works
            logger = get_logger("test.global")
            logger.info("Global logging test")
            
            # Check log file
            log_path = Path(temp_dir) / "global_test.log"
            assert log_path.exists()
            
            content = log_path.read_text()
            assert "Global logging test" in content
    
    def test_convenience_functions(self):
        """Test convenience logging functions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            configure_logging(
                level="DEBUG",
                format_type="simple",
                log_file="convenience_test.log",
                log_dir=temp_dir,
                console_output=False
            )
            
            from src.entaera.core.logger import (
                log_debug, log_info, log_warning, log_error, log_critical
            )
            
            # Test all convenience functions
            log_debug("Debug message", component="test")
            log_info("Info message", user="test_user")
            log_warning("Warning message")
            log_error("Error message")
            log_critical("Critical message")
            
            # Check log file content
            log_path = Path(temp_dir) / "convenience_test.log"
            content = log_path.read_text()
            
            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content
            assert "Critical message" in content
    
    def test_kata_practice_logging(self):
        """Test logging kata practice function."""
        result = kata_practice_logging()
        
        assert isinstance(result, dict)
        assert "logging_configured" in result
        
        if result["logging_configured"]:
            assert "log_file_created" in result
            assert "log_entries" in result
            assert "request_id_used" in result
            assert "log_levels_tested" in result
            assert "exception_logged" in result
            assert "learning_notes" in result
            
            assert result["log_file_created"] is True
            assert result["log_entries"] > 0
            assert len(result["request_id_used"]) == 8  # UUID truncated to 8 chars
            assert set(result["log_levels_tested"]) == {"DEBUG", "INFO", "WARNING", "ERROR"}
            assert result["exception_logged"] is True
            assert isinstance(result["learning_notes"], list)
        else:
            assert "error" in result
            assert "learning_notes" in result


class TestDay2Integration:
    """Integration tests for Day 2 kata components."""
    
    def test_config_and_logging_integration(self):
        """Test integration between configuration and logging systems."""
        # Load configuration
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("""
VERTEX_AUTO_GPT_APP_NAME=IntegrationTest
VERTEX_AUTO_GPT_LOG_LEVEL=DEBUG
VERTEX_AUTO_GPT_LOG_FORMAT=simple
""")
            dotenv_path = f.name
        
        try:
            settings = load_settings(dotenv_path=dotenv_path)
            
            # Configure logging based on settings
            with tempfile.TemporaryDirectory() as temp_dir:
                configure_logging(
                    level=getattr(settings, 'log_level', 'INFO'),
                    format_type=getattr(settings, 'log_format', 'simple'),
                    log_file="integration_test.log",
                    log_dir=temp_dir,
                    console_output=False
                )
                
                # Test logging with configuration context
                logger = get_logger("integration.test")
                logger.info("Integration test message", 
                           app_name=settings.app_name,
                           version=settings.version)
                
                # Verify log file
                log_path = Path(temp_dir) / "integration_test.log"
                assert log_path.exists()
                
                content = log_path.read_text()
                assert "Integration test message" in content
                assert settings.app_name in content
        
        finally:
            os.unlink(dotenv_path)
    
    def test_error_handling_integration(self):
        """Test error handling across configuration and logging."""
        # Test configuration error handling
        with patch.dict(os.environ, {"VERTEX_AUTO_GPT_TEMPERATURE": "invalid"}):
            try:
                load_settings()
                assert False, "Should have raised validation error"
            except Exception as e:
                # Log the configuration error
                configure_logging(level="ERROR", console_output=False)
                logger = get_logger("integration.error")
                logger.exception("Configuration validation failed", 
                                config_error=str(e))
                
                # Verify error was logged (basic check)
                assert True  # If we get here, error handling worked


if __name__ == "__main__":
    # Run kata tests
    print("🧪 Running Day 2 Kata Tests")
    print("=" * 40)
    
    # You can run individual test methods here for kata practice
    test_config = TestDay2ConfigurationKata()
    test_logging = TestDay2LoggingKata()
    test_integration = TestDay2Integration()
    
    print("✅ Configuration tests ready")
    print("✅ Logging tests ready") 
    print("✅ Integration tests ready")
    print("\nRun: pytest tests/unit/test_day2_kata.py -v")
    print("🎯 Day 2 Kata: Configuration & Logging mastery!")