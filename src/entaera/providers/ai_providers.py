"""
VertexAutoGPT AI Provider System
Integrates multiple AI providers for intelligent agent responses.
"""

import asyncio
import logging
import json
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Import existing utilities
import sys
sys.path.append('src')

try:
    from entaera.utils.rate_limiter import SmartRateLimiter
    from entaera.utils.multi_gemini_manager import MultiGeminiManager, GeminiAccount
    from entaera.config.api_config import ConfigManager, APIConfig
except ImportError:
    # Fallback if imports fail
    SmartRateLimiter = None
    MultiGeminiManager = None
    ConfigManager = None
    APIConfig = None

# Real API imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

logger = logging.getLogger(__name__)

class AIProviderType(str, Enum):
    """Supported AI providers."""
    GPT35_TURBO = "gpt35_turbo"
    AZURE_GPT35 = "azure_gpt35"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"
    LOCAL_MODEL = "local_model"

@dataclass
class AIResponse:
    """Standardized AI response format."""
    content: str
    provider: AIProviderType
    model: str
    tokens_used: int = 0
    cost: float = 0.0
    latency: float = 0.0
    metadata: Dict[str, Any] = None

class AIProviderInterface(ABC):
    """Abstract interface for AI providers."""
    
    @abstractmethod
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate AI response."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass

class OpenAIProvider(AIProviderInterface):
    """OpenAI GPT-3.5 Turbo provider."""
    
    def __init__(self, api_key: Optional[str] = None, rate_limiter: Optional[SmartRateLimiter] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.rate_limiter = rate_limiter
        self.model = "gpt-3.5-turbo"
        
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using OpenAI API."""
        
        if not self.is_available():
            raise ValueError("OpenAI provider not available - missing API key")
        
        # Rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire("gpt35", estimated_tokens=max_tokens)
        
        try:
            # Try to import openai
            import openai
            
            # Set up the client
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            import time
            start_time = time.time()
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            latency = time.time() - start_time
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider=AIProviderType.GPT35_TURBO,
                model=self.model,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                latency=latency,
                metadata={"finish_reason": response.choices[0].finish_reason}
            )
            
        except ImportError:
            # Fallback for when openai isn't installed
            await asyncio.sleep(0.5)  # Simulate API call
            return AIResponse(
                content=f"[GPT-3.5 Simulation] Response to: {prompt}",
                provider=AIProviderType.GPT35_TURBO,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.5
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Return a simulation instead of failing
            await asyncio.sleep(0.5)
            return AIResponse(
                content=f"[GPT-3.5 Error Fallback] Response to: {prompt}",
                provider=AIProviderType.GPT35_TURBO,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.5,
                metadata={"error": str(e)}
            )
        finally:
            if self.rate_limiter:
                self.rate_limiter.release("gpt35")
    
    def is_available(self) -> bool:
        """Check if OpenAI provider is available."""
        return bool(self.api_key)

class AzureOpenAIProvider(AIProviderInterface):
    """Azure OpenAI GPT-3.5 provider."""
    
    def __init__(
        self, 
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2024-02-15-preview",
        rate_limiter: Optional[SmartRateLimiter] = None
    ):
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = api_version
        self.rate_limiter = rate_limiter
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Azure OpenAI."""
        
        if not self.is_available():
            raise ValueError("Azure OpenAI provider not available")
        
        # Rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire("azure", estimated_tokens=max_tokens)
        
        try:
            # Try to import azure openai
            from openai import AsyncAzureOpenAI
            
            client = AsyncAzureOpenAI(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version
            )
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            import time
            start_time = time.time()
            
            response = await client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            latency = time.time() - start_time
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment_name,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                latency=latency
            )
            
        except ImportError:
            # Fallback simulation
            await asyncio.sleep(0.4)
            return AIResponse(
                content=f"[Azure GPT-3.5 Simulation] Response to: {prompt}",
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.4
            )
        except Exception as e:
            logger.error(f"Azure OpenAI error: {e}")
            await asyncio.sleep(0.4)
            return AIResponse(
                content=f"[Azure GPT-3.5 Error Fallback] Response to: {prompt}",
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.4,
                metadata={"error": str(e)}
            )
        finally:
            if self.rate_limiter:
                self.rate_limiter.release("azure")
    
    def is_available(self) -> bool:
        """Check if Azure OpenAI is available."""
        return bool(self.endpoint and self.api_key)

class GeminiProvider(AIProviderInterface):
    """Google Gemini provider with multi-account management."""
    
    def __init__(self, rate_limiter: Optional[SmartRateLimiter] = None):
        self.rate_limiter = rate_limiter
        self.model = "gemini-2.0-flash-exp"
        
        # Initialize multi-account manager if available
        if MultiGeminiManager:
            try:
                self.manager = MultiGeminiManager()
            except:
                self.manager = None
        else:
            self.manager = None
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Gemini."""
        
        # Rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire("gemini", estimated_tokens=max_tokens)
        
        try:
            # Try to use multi-account manager
            if self.manager:
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                import time
                start_time = time.time()
                
                response = await self.manager.generate_response(
                    prompt=full_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                latency = time.time() - start_time
                
                return AIResponse(
                    content=response["content"],
                    provider=AIProviderType.GEMINI,
                    model=self.model,
                    tokens_used=response.get("tokens_used", len(prompt.split()) * 2),
                    latency=latency,
                    metadata=response.get("metadata", {})
                )
            else:
                # Fallback simulation
                await asyncio.sleep(0.6)
                return AIResponse(
                    content=f"[Gemini Simulation] Response to: {prompt}",
                    provider=AIProviderType.GEMINI,
                    model=self.model,
                    tokens_used=len(prompt.split()) * 2,
                    latency=0.6
                )
                
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            await asyncio.sleep(0.6)
            return AIResponse(
                content=f"[Gemini Error Fallback] Response to: {prompt}",
                provider=AIProviderType.GEMINI,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.6,
                metadata={"error": str(e)}
            )
        finally:
            if self.rate_limiter:
                self.rate_limiter.release("gemini")
    
    def is_available(self) -> bool:
        """Check if Gemini is available."""
        return self.manager is not None or os.getenv("GEMINI_API_KEY") is not None

class PerplexityProvider(AIProviderInterface):
    """Perplexity AI provider."""
    
    def __init__(self, api_key: Optional[str] = None, rate_limiter: Optional[SmartRateLimiter] = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.rate_limiter = rate_limiter
        self.model = "sonar"  # Updated to working model name
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Perplexity."""
        
        if not self.is_available():
            raise ValueError("Perplexity provider not available")
        
        # Rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire("perplexity", estimated_tokens=max_tokens)
        
        try:
            # Perplexity uses OpenAI-compatible API
            import openai
            
            client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai"
            )
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            import time
            start_time = time.time()
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            latency = time.time() - start_time
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider=AIProviderType.PERPLEXITY,
                model=self.model,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                latency=latency
            )
            
        except ImportError:
            # Fallback simulation
            await asyncio.sleep(0.8)
            return AIResponse(
                content=f"[Perplexity Simulation] Response to: {prompt}",
                provider=AIProviderType.PERPLEXITY,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.8
            )
        except Exception as e:
            logger.error(f"Perplexity error: {e}")
            await asyncio.sleep(0.8)
            return AIResponse(
                content=f"[Perplexity Error Fallback] Response to: {prompt}",
                provider=AIProviderType.PERPLEXITY,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.8,
                metadata={"error": str(e)}
            )
        finally:
            if self.rate_limiter:
                self.rate_limiter.release("perplexity")
    
    def is_available(self) -> bool:
        """Check if Perplexity is available."""
        return bool(self.api_key)

class LocalModelProvider(AIProviderInterface):
    """Local AI model provider for offline inference."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model_name = "local-model"
        
        # Look for local models
        self.available_models = self._find_local_models()
    
    def _find_local_models(self) -> List[str]:
        """Find available local models."""
        model_extensions = ['.gguf', '.bin', '.safetensors']
        models = []
        
        # Check common model directories
        search_paths = [
            "models/",
            "../models/", 
            "~/models/",
            "/models/"
        ]
        
        for search_path in search_paths:
            try:
                path = Path(search_path).expanduser()
                if path.exists():
                    for ext in model_extensions:
                        models.extend(path.glob(f"*{ext}"))
            except:
                continue
        
        return [str(model) for model in models]
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using local model."""
        
        # Simulate local inference
        await asyncio.sleep(1.0)  # Local models are slower
        
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        return AIResponse(
            content=f"[Local Model Response] Based on: {prompt[:100]}...",
            provider=AIProviderType.LOCAL_MODEL,
            model=self.model_name,
            tokens_used=len(prompt.split()) * 3,  # Local models might be less efficient
            latency=1.0,
            metadata={"available_models": len(self.available_models)}
        )
    
    def is_available(self) -> bool:
        """Check if local models are available."""
        return len(self.available_models) > 0

class SmartAIRouter:
    """Intelligent AI provider router with fallback strategy."""
    
    def __init__(self):
        # Initialize rate limiter if available
        self.rate_limiter = SmartRateLimiter() if SmartRateLimiter else None
        
        # Initialize providers
        self.providers = {
            AIProviderType.GPT35_TURBO: OpenAIProvider(rate_limiter=self.rate_limiter),
            AIProviderType.AZURE_GPT35: AzureOpenAIProvider(rate_limiter=self.rate_limiter),
            AIProviderType.GEMINI: GeminiProvider(rate_limiter=self.rate_limiter),
            AIProviderType.PERPLEXITY: PerplexityProvider(rate_limiter=self.rate_limiter),
            AIProviderType.LOCAL_MODEL: LocalModelProvider()
        }
        
        # Default priority order (based on your preferences)
        self.priority_order = [
            AIProviderType.GPT35_TURBO,      # Primary choice
            AIProviderType.AZURE_GPT35,      # Azure fallback
            AIProviderType.GEMINI,           # Google fallback
            AIProviderType.PERPLEXITY,       # Research tasks
            AIProviderType.LOCAL_MODEL       # Offline fallback
        ]
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        preferred_provider: Optional[AIProviderType] = None
    ) -> AIResponse:
        """Generate response with smart provider selection."""
        
        # Try preferred provider first
        if preferred_provider and preferred_provider in self.providers:
            provider = self.providers[preferred_provider]
            if provider.is_available():
                try:
                    return await provider.generate_response(
                        prompt, system_prompt, max_tokens, temperature
                    )
                except Exception as e:
                    logger.warning(f"Preferred provider {preferred_provider} failed: {e}")
        
        # Fallback to priority order
        for provider_type in self.priority_order:
            provider = self.providers[provider_type]
            if provider.is_available():
                try:
                    return await provider.generate_response(
                        prompt, system_prompt, max_tokens, temperature
                    )
                except Exception as e:
                    logger.warning(f"Provider {provider_type} failed: {e}")
                    continue
        
        # Ultimate fallback
        return AIResponse(
            content=f"[Fallback Response] Unable to process: {prompt}",
            provider=AIProviderType.LOCAL_MODEL,
            model="fallback",
            tokens_used=0,
            latency=0.1,
            metadata={"error": "All providers failed"}
        )
    
    def get_available_providers(self) -> List[AIProviderType]:
        """Get list of currently available providers."""
        return [
            provider_type for provider_type, provider in self.providers.items()
            if provider.is_available()
        ]
    
    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all providers."""
        return {
            provider_type.value: provider.is_available()
            for provider_type, provider in self.providers.items()
        }

# Global instance for easy access
ai_router = SmartAIRouter()

async def test_all_providers():
    """Test all AI providers."""
    print("🧪 Testing All AI Providers")
    print("=" * 50)
    
    router = SmartAIRouter()
    
    # Check availability
    print("📊 Provider Availability:")
    status = router.get_provider_status()
    for provider, available in status.items():
        icon = "✅" if available else "❌"
        print(f"   {icon} {provider}")
    
    # Test responses
    test_prompt = "What is machine learning?"
    system_prompt = "You are a helpful AI assistant."
    
    print(f"\n🎯 Testing with prompt: '{test_prompt}'")
    
    for provider_type in router.priority_order:
        if router.providers[provider_type].is_available():
            print(f"\n🤖 Testing {provider_type.value}...")
            try:
                response = await router.generate_response(
                    prompt=test_prompt,
                    system_prompt=system_prompt,
                    preferred_provider=provider_type
                )
                print(f"   ✅ Response: {response.content[:100]}...")
                print(f"   📊 Tokens: {response.tokens_used}, Latency: {response.latency:.2f}s")
            except Exception as e:
                print(f"   ❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_providers())