"""
Day 2 Kata: Configuration Management
===================================

Learning Objectives:
- Environment variables management
- Configuration validation with Pydantic
- Type hints and data validation
- Error handling patterns
- Security best practices

This module implements robust configuration management for the ENTAERA system.
"""

import os
from typing import Optional, List, Literal
from pathlib import Path

try:
    from pydantic_settings import BaseSettings
    from pydantic import BaseModel, Field, field_validator, model_validator
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseModel, Field, validator as field_validator
    from pydantic import root_validator as model_validator
    from pydantic import BaseSettings

# Make validator available for backward compatibility
try:
    from pydantic import validator
except ImportError:
    validator = field_validator

from dotenv import load_dotenv


class APIProviderSettings(BaseModel):
    """Configuration for AI API providers."""
    
    # Gemini Configuration
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    gemini_model: str = Field(default="gemini-pro", description="Gemini model name")
    gemini_max_tokens: int = Field(default=4096, ge=1, le=32768)
    gemini_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # Perplexity Configuration  
    perplexity_api_key: str = Field(..., description="Perplexity API key")
    perplexity_model: str = Field(default="llama-3.1-sonar-large-128k-online")
    perplexity_max_tokens: int = Field(default=4096, ge=1, le=32768)
    perplexity_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    @field_validator('gemini_api_key', 'perplexity_api_key')
    def validate_api_keys(cls, v):
        """Validate API key format and presence."""
        if not v or v == "your_api_key_here" or len(v) < 10:
            raise ValueError("API key must be provided and valid")
        return v
    
    class Config:
        env_prefix = ""


class ApplicationSettings(BaseSettings):
    """Core application configuration."""
    
    # Application Metadata
    app_name: str = Field(default="ENTAERA", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    app_description: str = Field(default="Kata-driven AI research agent")
    
    # Environment Settings
    environment: Literal["development", "testing", "production"] = Field(default="development")
    debug: bool = Field(default=True, description="Enable debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    
    # Security Settings
    secret_key: str = Field(..., description="Secret key for encryption")
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"])
    cors_origins: List[str] = Field(default=["http://localhost:3000"])
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Validate secret key strength."""
        if not v or v == "your_secret_key_here" or len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    @validator('environment')
    def validate_environment(cls, v):
        """Validate environment setting."""
        valid_envs = {"development", "testing", "production"}
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v
    
    def __init__(self, **kwargs):
        """Initialize settings with environment variable loading."""
        # Load environment variables from .env file
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
        
        super().__init__(**kwargs)
    
    class Config:
        env_prefix = ""


class ServerSettings(BaseSettings):
    """Server and API configuration."""
    
    # API Server Settings
    api_host: str = Field(default="0.0.0.0", description="API server host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API server port")
    api_workers: int = Field(default=1, ge=1, le=32, description="Number of API workers")
    api_reload: bool = Field(default=True, description="Enable auto-reload in development")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, ge=1, description="Requests per window")
    rate_limit_window: int = Field(default=60, ge=1, description="Rate limit window in seconds")
    
    class Config:
        env_prefix = ""


class DatabaseSettings(BaseSettings):
    """Database and storage configuration."""
    
    # Vector Database Settings
    vector_store_type: Literal["faiss", "chroma", "pinecone"] = Field(default="faiss")
    vector_store_path: str = Field(default="./data/vector_store")
    vector_dimension: int = Field(default=1536, ge=1)
    vector_index_type: str = Field(default="IndexFlatL2")
    
    # File Storage
    data_dir: str = Field(default="./data")
    cache_dir: str = Field(default="./cache")
    logs_dir: str = Field(default="./logs")
    
    @validator('vector_store_path', 'data_dir', 'cache_dir', 'logs_dir')
    def validate_paths(cls, v):
        """Ensure directory paths are valid."""
        path = Path(v)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create directory {v}: {e}")
        return str(path)
    
    class Config:
        env_prefix = ""


class ProviderRoutingSettings(BaseSettings):
    """AI provider routing configuration."""
    
    # Provider Selection Strategy
    default_provider: Literal["gemini", "perplexity"] = Field(default="gemini")
    fallback_provider: Literal["gemini", "perplexity"] = Field(default="perplexity")
    provider_timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    
    # Provider Routing Rules
    research_provider: Literal["gemini", "perplexity"] = Field(default="perplexity")
    generation_provider: Literal["gemini", "perplexity"] = Field(default="gemini")
    summarization_provider: Literal["gemini", "perplexity"] = Field(default="gemini")
    
    class Config:
        env_prefix = ""


class PerformanceSettings(BaseSettings):
    """Performance and optimization configuration."""
    
    # Caching Settings
    cache_enabled: bool = Field(default=True)
    cache_ttl: int = Field(default=3600, ge=0)  # seconds
    cache_max_size: int = Field(default=1000, ge=1)
    
    # Concurrency Settings
    max_concurrent_requests: int = Field(default=10, ge=1, le=100)
    async_workers: int = Field(default=4, ge=1, le=32)
    
    # Memory Management
    max_memory_usage: str = Field(default="1GB")
    garbage_collection_threshold: int = Field(default=100, ge=1)
    
    class Config:
        env_prefix = ""


class MonitoringSettings(BaseSettings):
    """Monitoring and logging configuration."""
    
    # Logging Configuration
    log_format: Literal["structured", "simple"] = Field(default="structured")
    log_file: str = Field(default="entaera.log")
    log_max_size: str = Field(default="10MB")
    log_backup_count: int = Field(default=5, ge=1, le=100)
    
    # Monitoring Settings
    metrics_enabled: bool = Field(default=True)
    metrics_port: int = Field(default=9090, ge=1, le=65535)
    health_check_interval: int = Field(default=30, ge=1)
    
    # Tracing Settings
    tracing_enabled: bool = Field(default=False)
    jaeger_endpoint: Optional[str] = Field(default=None)
    
    class Config:
        env_prefix = ""


class KataSettings(BaseSettings):
    """Kata learning and progress tracking configuration."""
    
    # Learning Progress Tracking
    kata_progress_file: str = Field(default="./data/kata_progress.json")
    current_kata_day: int = Field(default=1, ge=1, le=30)
    kata_completion_tracking: bool = Field(default=True)
    
    # Educational Features
    show_learning_tips: bool = Field(default=True)
    detailed_error_messages: bool = Field(default=True)
    step_by_step_guidance: bool = Field(default=True)
    
    # Practice Mode Settings
    practice_mode_enabled: bool = Field(default=True)
    hint_system_enabled: bool = Field(default=True)
    solution_reveal_delay: int = Field(default=300, ge=0)  # seconds
    
    class Config:
        env_prefix = ""


class Settings(BaseSettings):
    """
    Main application settings combining all configuration sections.
    
    This class aggregates all configuration sections and provides
    a single interface for accessing application settings.
    """
    
    # Configuration sections
    api_providers: APIProviderSettings = Field(default_factory=APIProviderSettings)
    application: ApplicationSettings = Field(default_factory=ApplicationSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    routing: ProviderRoutingSettings = Field(default_factory=ProviderRoutingSettings)
    performance: PerformanceSettings = Field(default_factory=PerformanceSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    kata: KataSettings = Field(default_factory=KataSettings)
    
    def __init__(self, **kwargs):
        """Initialize settings with environment variable loading."""
        # Load environment variables from .env file
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
        
        super().__init__(**kwargs)
    
    @validator('routing')
    def validate_routing_consistency(cls, v, values):
        """Ensure routing configuration is consistent."""
        if 'api_providers' in values:
            # Ensure default and fallback providers are different
            if v.default_provider == v.fallback_provider:
                raise ValueError("Default and fallback providers must be different")
        return v
    
    def get_provider_config(self, provider_name: str) -> dict:
        """
        Get configuration for a specific AI provider.
        
        Args:
            provider_name: Name of the provider ('gemini' or 'perplexity')
            
        Returns:
            Dictionary with provider configuration
            
        Raises:
            ValueError: If provider name is invalid
        """
        if provider_name == "gemini":
            return {
                "api_key": self.api_providers.gemini_api_key,
                "model": self.api_providers.gemini_model,
                "max_tokens": self.api_providers.gemini_max_tokens,
                "temperature": self.api_providers.gemini_temperature,
            }
        elif provider_name == "perplexity":
            return {
                "api_key": self.api_providers.perplexity_api_key,
                "model": self.api_providers.perplexity_model,
                "max_tokens": self.api_providers.perplexity_max_tokens,
                "temperature": self.api_providers.perplexity_temperature,
            }
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.application.environment == "development"
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.application.environment == "production"
    
    def get_log_config(self) -> dict:
        """Get logging configuration dictionary."""
        return {
            "level": self.application.log_level,
            "format": self.monitoring.log_format,
            "file": self.monitoring.log_file,
            "max_size": self.monitoring.log_max_size,
            "backup_count": self.monitoring.log_backup_count,
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    This function implements the singleton pattern to ensure
    configuration is loaded only once per application lifecycle.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment.
    
    Useful for testing or when configuration changes at runtime.
    
    Returns:
        New Settings instance
    """
    global _settings
    _settings = None
    return get_settings()


def validate_configuration() -> tuple[bool, List[str]]:
    """
    Validate the current configuration.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        settings = get_settings()
        
        # Validate API keys are not default values
        if settings.api_providers.gemini_api_key == "your_gemini_api_key_here":
            errors.append("Gemini API key not configured")
            
        if settings.api_providers.perplexity_api_key == "your_perplexity_api_key_here":
            errors.append("Perplexity API key not configured")
        
        # Validate secret key
        if settings.application.secret_key == "your_secret_key_here":
            errors.append("Secret key not configured")
        
        # Validate directories exist
        for dir_path in [settings.database.data_dir, settings.database.cache_dir, settings.database.logs_dir]:
            if not Path(dir_path).exists():
                errors.append(f"Directory does not exist: {dir_path}")
        
        # Production-specific validations
        if settings.is_production():
            if settings.application.debug:
                errors.append("Debug mode should be disabled in production")
            
            if settings.server.api_reload:
                errors.append("API reload should be disabled in production")
    
    except Exception as e:
        errors.append(f"Configuration validation error: {e}")
    
    return len(errors) == 0, errors


# Kata practice function
def kata_practice_config() -> dict:
    """
    Practice function for configuration management kata.
    
    Returns:
        Dictionary with configuration analysis for learning
    """
    try:
        settings = get_settings()
        is_valid, errors = validate_configuration()
        
        return {
            "configuration_loaded": True,
            "is_valid": is_valid,
            "errors": errors,
            "environment": settings.application.environment,
            "debug_mode": settings.application.debug,
            "providers_configured": {
                "gemini": settings.api_providers.gemini_api_key != "your_gemini_api_key_here",
                "perplexity": settings.api_providers.perplexity_api_key != "your_perplexity_api_key_here",
            },
            "security": {
                "secret_key_configured": settings.application.secret_key != "your_secret_key_here",
                "allowed_hosts": len(settings.application.allowed_hosts),
                "cors_origins": len(settings.application.cors_origins),
            },
            "directories": {
                "data_dir": settings.database.data_dir,
                "cache_dir": settings.database.cache_dir,
                "logs_dir": settings.database.logs_dir,
            },
            "learning_notes": [
                "Configuration uses Pydantic for validation",
                "Environment variables override defaults",
                "Settings are validated on startup",
                "Production mode enforces stricter rules"
            ]
        }
    
    except Exception as e:
        return {
            "configuration_loaded": False,
            "error": str(e),
            "learning_notes": [
                "Configuration failed to load",
                "Check .env file exists and is properly formatted",
                "Ensure all required environment variables are set"
            ]
        }


if __name__ == "__main__":
    # Kata demonstration
    print("🥋 Day 2 Kata: Configuration Management Demo")
    print("=" * 50)
    
    # Practice configuration loading
    practice_results = kata_practice_config()
    
    print(f"Configuration loaded: {practice_results['configuration_loaded']}")
    
    if practice_results['configuration_loaded']:
        print(f"Configuration valid: {practice_results['is_valid']}")
        print(f"Environment: {practice_results['environment']}")
        print(f"Debug mode: {practice_results['debug_mode']}")
        
        print(f"\nProviders configured:")
        for provider, configured in practice_results['providers_configured'].items():
            status = "✅" if configured else "❌"
            print(f"  {status} {provider}")
        
        print(f"\nSecurity settings:")
        security = practice_results['security']
        print(f"  Secret key: {'✅' if security['secret_key_configured'] else '❌'}")
        print(f"  Allowed hosts: {security['allowed_hosts']}")
        print(f"  CORS origins: {security['cors_origins']}")
        
        if practice_results['errors']:
            print(f"\nConfiguration errors:")
            for error in practice_results['errors']:
                print(f"  ❌ {error}")
    else:
        print(f"Configuration error: {practice_results.get('error', 'Unknown error')}")
    
    print(f"\nLearning notes:")
    for note in practice_results['learning_notes']:
        print(f"  📝 {note}")
    
    print(f"\n🎉 Day 2 Kata completed! Configuration management mastery achieved.")