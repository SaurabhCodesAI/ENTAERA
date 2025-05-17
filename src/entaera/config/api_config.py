"""
VertexAutoGPT API Configuration
Secure configuration system for AI provider API keys.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class APIConfig:
    """Configuration for AI provider APIs."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_org_id: Optional[str] = None
    
    # Azure OpenAI Configuration
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_deployment_name: str = "gpt-35-turbo"
    
    # Google Gemini Configuration
    gemini_api_key: Optional[str] = None
    gemini_project_id: Optional[str] = None
    
    # Perplexity Configuration
    perplexity_api_key: Optional[str] = None
    
    # Local Model Configuration
    local_model_url: str = "http://localhost:11434"  # Default Ollama URL
    local_model_name: str = "llama2"
    
    def __post_init__(self):
        """Load configuration from environment variables if not provided."""
        # OpenAI
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_org_id:
            self.openai_org_id = os.getenv("OPENAI_ORG_ID")
        
        # Azure OpenAI
        if not self.azure_openai_api_key:
            self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not self.azure_openai_endpoint:
            self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        # Gemini
        if not self.gemini_api_key:
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_project_id:
            self.gemini_project_id = os.getenv("GEMINI_PROJECT_ID")
        
        # Perplexity
        if not self.perplexity_api_key:
            self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        
        # Local model settings from env
        self.local_model_url = os.getenv("LOCAL_MODEL_URL", self.local_model_url)
        self.local_model_name = os.getenv("LOCAL_MODEL_NAME", self.local_model_name)

class ConfigManager:
    """Manages API configuration with multiple sources."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "config/api_keys.json"
        self.config_path = Path(self.config_file)
        self._config: Optional[APIConfig] = None
    
    def load_config(self) -> APIConfig:
        """Load configuration from file and environment."""
        config_data = {}
        
        # Try to load from file first
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    config_data.update(file_config)
                logger.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logger.warning(f"Could not load config file {self.config_path}: {e}")
        
        # Create config (will auto-load from environment)
        self._config = APIConfig(**config_data)
        return self._config
    
    def save_config(self, config: APIConfig) -> bool:
        """Save configuration to file (excluding sensitive data)."""
        try:
            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save non-sensitive configuration
            config_data = {
                "azure_openai_endpoint": config.azure_openai_endpoint,
                "azure_openai_api_version": config.azure_openai_api_version,
                "azure_deployment_name": config.azure_deployment_name,
                "gemini_project_id": config.gemini_project_id,
                "local_model_url": config.local_model_url,
                "local_model_name": config.local_model_name
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Saved configuration to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def get_config(self) -> APIConfig:
        """Get current configuration."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate which providers are properly configured."""
        config = self.get_config()
        
        return {
            "openai": bool(config.openai_api_key),
            "azure_openai": bool(config.azure_openai_api_key and config.azure_openai_endpoint),
            "gemini": bool(config.gemini_api_key),
            "perplexity": bool(config.perplexity_api_key),
            "local_model": True  # Assume local model is always available
        }
    
    def get_provider_status(self) -> str:
        """Get a formatted status of all providers."""
        validation = self.validate_config()
        status_lines = ["🔧 AI Provider Configuration Status:"]
        
        providers = {
            "openai": "🤖 OpenAI GPT-3.5 Turbo",
            "azure_openai": "☁️  Azure OpenAI",
            "gemini": "✨ Google Gemini",
            "perplexity": "🔍 Perplexity",
            "local_model": "🏠 Local Model"
        }
        
        for key, name in providers.items():
            status = "✅ Configured" if validation[key] else "❌ Missing API Key"
            status_lines.append(f"   {name}: {status}")
        
        return "\n".join(status_lines)

def create_example_config():
    """Create an example configuration file."""
    example_config = {
        "azure_openai_endpoint": "https://your-resource.openai.azure.com/",
        "azure_openai_api_version": "2024-02-15-preview",
        "azure_deployment_name": "gpt-35-turbo",
        "gemini_project_id": "your-google-cloud-project-id",
        "local_model_url": "http://localhost:11434",
        "local_model_name": "llama2"
    }
    
    config_path = Path("config/api_keys.json.example")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=2)
    
    return config_path

def create_env_example():
    """Create an example .env file."""
    env_content = """# VertexAutoGPT API Configuration
# Copy this file to .env and add your actual API keys

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_ORG_ID=org-your-organization-id-here

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_PROJECT_ID=your-google-cloud-project-id

# Perplexity Configuration
PERPLEXITY_API_KEY=pplx-your-perplexity-api-key-here

# Local Model Configuration (Ollama)
LOCAL_MODEL_URL=http://localhost:11434
LOCAL_MODEL_NAME=llama2
"""
    
    env_path = Path(".env.example")
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    return env_path

if __name__ == "__main__":
    # Demo the configuration system
    print("🔧 VertexAutoGPT API Configuration Setup")
    print("=" * 50)
    
    # Create example files
    example_config = create_example_config()
    example_env = create_env_example()
    
    print(f"✅ Created example configuration: {example_config}")
    print(f"✅ Created example environment file: {example_env}")
    
    # Test configuration loading
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    print(f"\n{config_manager.get_provider_status()}")
    
    print(f"\n📋 Next Steps:")
    print(f"1. Copy .env.example to .env")
    print(f"2. Add your actual API keys to .env")
    print(f"3. Run VertexAutoGPT with real AI providers!")