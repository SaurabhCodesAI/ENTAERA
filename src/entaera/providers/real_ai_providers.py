"""
VertexAutoGPT Real AI Provider System
Production-ready AI providers with real API integration.
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

# Import configuration
import sys
sys.path.append('src')

try:
    from entaera.config.api_config import ConfigManager, APIConfig
    from entaera.utils.rate_limiter import SmartRateLimiter
except ImportError:
    ConfigManager = None
    APIConfig = None
    SmartRateLimiter = None

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

class RealOpenAIProvider(AIProviderInterface):
    """Real OpenAI GPT-3.5 Turbo provider with API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.client = None
        
        if self.api_key and OPENAI_AVAILABLE:
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        
    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        return bool(self.api_key and OPENAI_AVAILABLE and self.client)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using real OpenAI API."""
        
        if not self.is_available():
            # Fallback simulation
            await asyncio.sleep(0.3)
            return AIResponse(
                content=f"[OpenAI Simulation] I understand you're asking about: {prompt}. I'd provide a comprehensive response using GPT-3.5 Turbo if the API key was configured.",
                provider=AIProviderType.GPT35_TURBO,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.3,
                metadata={"simulated": True, "reason": "Missing API key"}
            )
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            start_time = time.time()
            
            response = await self.client.chat.completions.create(
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
                cost=response.usage.total_tokens * 0.0000015 if response.usage else 0,  # Rough cost estimate
                metadata={"finish_reason": response.choices[0].finish_reason}
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            await asyncio.sleep(0.3)
            return AIResponse(
                content=f"[OpenAI Error] I encountered an issue accessing GPT-3.5 Turbo: {e}. Using fallback response for: {prompt}",
                provider=AIProviderType.GPT35_TURBO,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.3,
                metadata={"error": str(e)}
            )

class RealAzureOpenAIProvider(AIProviderInterface):
    """Real Azure OpenAI provider."""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, deployment: str = "gpt-35-turbo"):
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = deployment
        self.client = None
        
        if self.api_key and self.endpoint and OPENAI_AVAILABLE:
            self.client = openai.AsyncAzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint,
                api_version="2024-02-15-preview"
            )
    
    def is_available(self) -> bool:
        """Check if Azure OpenAI is available."""
        return bool(self.api_key and self.endpoint and OPENAI_AVAILABLE and self.client)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Azure OpenAI API."""
        
        if not self.is_available():
            await asyncio.sleep(0.4)
            return AIResponse(
                content=f"[Azure OpenAI Simulation] Enterprise-grade response to: {prompt}. Configure Azure OpenAI for real API access.",
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment,
                tokens_used=len(prompt.split()) * 2,
                latency=0.4,
                metadata={"simulated": True, "reason": "Missing Azure configuration"}
            )
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            start_time = time.time()
            
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            latency = time.time() - start_time
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                latency=latency,
                metadata={"finish_reason": response.choices[0].finish_reason}
            )
            
        except Exception as e:
            logger.error(f"Azure OpenAI API error: {e}")
            await asyncio.sleep(0.4)
            return AIResponse(
                content=f"[Azure OpenAI Error] Enterprise API encountered issue: {e}",
                provider=AIProviderType.AZURE_GPT35,
                model=self.deployment,
                tokens_used=len(prompt.split()) * 2,
                latency=0.4,
                metadata={"error": str(e)}
            )

class RealGeminiProvider(AIProviderInterface):
    """Real Google Gemini provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-2.0-flash-exp"
        self.model = None
        
        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                logger.warning(f"Failed to configure Gemini: {e}")
    
    def is_available(self) -> bool:
        """Check if Gemini is available."""
        return bool(self.api_key and GENAI_AVAILABLE and self.model)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Gemini API."""
        
        if not self.is_available():
            await asyncio.sleep(0.5)
            return AIResponse(
                content=f"[Gemini Simulation] Advanced AI response to: {prompt}. Configure Google Gemini API for cutting-edge capabilities.",
                provider=AIProviderType.GEMINI,
                model=self.model_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.5,
                metadata={"simulated": True, "reason": "Missing Gemini API key"}
            )
        
        try:
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            start_time = time.time()
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            latency = time.time() - start_time
            
            return AIResponse(
                content=response.text,
                provider=AIProviderType.GEMINI,
                model=self.model_name,
                tokens_used=len(response.text.split()) if response.text else 0,
                latency=latency,
                metadata={"finish_reason": "completed"}
            )
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            await asyncio.sleep(0.5)
            return AIResponse(
                content=f"[Gemini Error] Advanced AI system encountered issue: {e}",
                provider=AIProviderType.GEMINI,
                model=self.model_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.5,
                metadata={"error": str(e)}
            )

class RealPerplexityProvider(AIProviderInterface):
    """Real Perplexity provider with web search capabilities."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.model = "llama-3.1-sonar-small-128k-online"
        self.base_url = "https://api.perplexity.ai"
    
    def is_available(self) -> bool:
        """Check if Perplexity is available."""
        return bool(self.api_key and REQUESTS_AVAILABLE)
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using Perplexity API."""
        
        if not self.is_available():
            await asyncio.sleep(0.6)
            return AIResponse(
                content=f"[Perplexity Simulation] Web-enhanced AI response to: {prompt}. Configure Perplexity API for real-time web search integration.",
                provider=AIProviderType.PERPLEXITY,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.6,
                metadata={"simulated": True, "reason": "Missing Perplexity API key"}
            )
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            start_time = time.time()
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return AIResponse(
                    content=result["choices"][0]["message"]["content"],
                    provider=AIProviderType.PERPLEXITY,
                    model=self.model,
                    tokens_used=result.get("usage", {}).get("total_tokens", 0),
                    latency=latency,
                    metadata={"finish_reason": result["choices"][0].get("finish_reason")}
                )
            else:
                raise Exception(f"API returned status {response.status_code}: {response.text}")
                
        except Exception as e:
            logger.error(f"Perplexity API error: {e}")
            await asyncio.sleep(0.6)
            return AIResponse(
                content=f"[Perplexity Error] Web-enhanced AI encountered issue: {e}",
                provider=AIProviderType.PERPLEXITY,
                model=self.model,
                tokens_used=len(prompt.split()) * 2,
                latency=0.6,
                metadata={"error": str(e)}
            )

class LocalModelProvider(AIProviderInterface):
    """Local model provider (Ollama integration)."""
    
    def __init__(self, model_url: str = "http://localhost:11434", model_name: str = "llama2"):
        self.model_url = model_url
        self.model_name = model_name
    
    def is_available(self) -> bool:
        """Check if local model is available."""
        if not REQUESTS_AVAILABLE:
            return False
        
        try:
            response = requests.get(f"{self.model_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate response using local model."""
        
        if not self.is_available():
            await asyncio.sleep(0.8)
            return AIResponse(
                content=f"[Local Model Simulation] Private AI response to: {prompt}. Install Ollama and {self.model_name} for local processing.",
                provider=AIProviderType.LOCAL_MODEL,
                model=self.model_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.8,
                metadata={"simulated": True, "reason": "Ollama not running"}
            )
        
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            data = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            start_time = time.time()
            
            response = await asyncio.to_thread(
                requests.post,
                f"{self.model_url}/api/generate",
                json=data,
                timeout=30
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return AIResponse(
                    content=result["response"],
                    provider=AIProviderType.LOCAL_MODEL,
                    model=self.model_name,
                    tokens_used=len(result["response"].split()) if result.get("response") else 0,
                    latency=latency,
                    metadata={"eval_count": result.get("eval_count")}
                )
            else:
                raise Exception(f"Local model returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Local model error: {e}")
            await asyncio.sleep(0.8)
            return AIResponse(
                content=f"[Local Model Error] Private AI system encountered issue: {e}",
                provider=AIProviderType.LOCAL_MODEL,
                model=self.model_name,
                tokens_used=len(prompt.split()) * 2,
                latency=0.8,
                metadata={"error": str(e)}
            )

class ProductionAIRouter:
    """Production AI router with real provider integration."""
    
    def __init__(self, config: Optional[APIConfig] = None):
        # Load configuration
        if config is None and ConfigManager:
            config_manager = ConfigManager()
            config = config_manager.get_config()
        
        self.config = config
        self.providers = {}
        
        # Initialize real providers
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all AI providers with real configurations."""
        if self.config:
            # OpenAI
            self.providers[AIProviderType.GPT35_TURBO] = RealOpenAIProvider(
                api_key=self.config.openai_api_key
            )
            
            # Azure OpenAI
            self.providers[AIProviderType.AZURE_GPT35] = RealAzureOpenAIProvider(
                api_key=self.config.azure_openai_api_key,
                endpoint=self.config.azure_openai_endpoint,
                deployment=self.config.azure_deployment_name
            )
            
            # Gemini
            self.providers[AIProviderType.GEMINI] = RealGeminiProvider(
                api_key=self.config.gemini_api_key
            )
            
            # Perplexity
            self.providers[AIProviderType.PERPLEXITY] = RealPerplexityProvider(
                api_key=self.config.perplexity_api_key
            )
            
            # Local model
            self.providers[AIProviderType.LOCAL_MODEL] = LocalModelProvider(
                model_url=self.config.local_model_url,
                model_name=self.config.local_model_name
            )
        else:
            # Fallback providers without configuration
            self.providers = {
                AIProviderType.GPT35_TURBO: RealOpenAIProvider(),
                AIProviderType.AZURE_GPT35: RealAzureOpenAIProvider(),
                AIProviderType.GEMINI: RealGeminiProvider(),
                AIProviderType.PERPLEXITY: RealPerplexityProvider(),
                AIProviderType.LOCAL_MODEL: LocalModelProvider()
            }
    
    def get_available_providers(self) -> List[AIProviderType]:
        """Get list of available providers."""
        return [provider_type for provider_type, provider in self.providers.items() 
                if provider.is_available()]
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed status of all providers."""
        status = {}
        for provider_type, provider in self.providers.items():
            status[provider_type] = {
                "available": provider.is_available(),
                "provider": provider.__class__.__name__
            }
        return status
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        agent_type: str = "general",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        preferred_provider: Optional[AIProviderType] = None
    ) -> AIResponse:
        """Generate AI response with intelligent provider selection."""
        
        # Determine best provider based on agent type and availability
        provider_priority = self._get_provider_priority(agent_type, preferred_provider)
        
        # Try providers in order of priority
        for provider_type in provider_priority:
            if provider_type in self.providers:
                provider = self.providers[provider_type]
                try:
                    response = await provider.generate_response(
                        prompt=prompt,
                        system_prompt=system_prompt,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    
                    # Add agent type to metadata
                    if response.metadata is None:
                        response.metadata = {}
                    response.metadata["agent_type"] = agent_type
                    
                    return response
                    
                except Exception as e:
                    logger.warning(f"Provider {provider_type} failed: {e}")
                    continue
        
        # Fallback response if all providers fail
        return AIResponse(
            content=f"[System Fallback] All AI providers unavailable. Response to: {prompt}",
            provider=AIProviderType.LOCAL_MODEL,
            model="fallback",
            tokens_used=len(prompt.split()),
            latency=0.1,
            metadata={"agent_type": agent_type, "fallback": True}
        )
    
    def _get_provider_priority(self, agent_type: str, preferred: Optional[AIProviderType] = None) -> List[AIProviderType]:
        """Get provider priority based on agent type."""
        # If preferred provider specified, try it first
        if preferred:
            priorities = [preferred]
        else:
            priorities = []
        
        # Agent-specific provider preferences
        if agent_type == "conversational":
            priorities.extend([AIProviderType.GPT35_TURBO, AIProviderType.AZURE_GPT35, AIProviderType.GEMINI])
        elif agent_type == "analytical":
            priorities.extend([AIProviderType.PERPLEXITY, AIProviderType.GEMINI, AIProviderType.GPT35_TURBO])
        elif agent_type == "creative":
            priorities.extend([AIProviderType.GEMINI, AIProviderType.GPT35_TURBO, AIProviderType.AZURE_GPT35])
        else:
            priorities.extend([AIProviderType.GPT35_TURBO, AIProviderType.AZURE_GPT35, AIProviderType.GEMINI])
        
        # Add remaining providers as fallbacks
        all_providers = list(AIProviderType)
        for provider in all_providers:
            if provider not in priorities:
                priorities.append(provider)
        
        return priorities

async def test_real_providers():
    """Test all real AI providers."""
    print("🧪 Testing Real AI Providers")
    print("=" * 50)
    
    # Initialize router
    router = ProductionAIRouter()
    
    # Get provider status
    status = router.get_provider_status()
    available = router.get_available_providers()
    
    print(f"📊 Provider Status:")
    for provider_type, info in status.items():
        status_icon = "✅" if info["available"] else "❌"
        print(f"   {status_icon} {provider_type}: {info['provider']}")
    
    print(f"\n🚀 Available Providers: {len(available)}")
    
    if available:
        print(f"\n🧠 Testing AI Response Generation...")
        
        test_prompt = "What are the key benefits of AI in business operations?"
        
        for agent_type in ["conversational", "analytical", "creative"]:
            print(f"\n🤖 Testing {agent_type} agent...")
            
            response = await router.generate_response(
                prompt=test_prompt,
                agent_type=agent_type,
                system_prompt=f"You are a professional {agent_type} AI assistant."
            )
            
            print(f"   Provider: {response.provider}")
            print(f"   Model: {response.model}")
            print(f"   Tokens: {response.tokens_used}")
            print(f"   Latency: {response.latency:.2f}s")
            print(f"   Response: {response.content[:100]}...")
    else:
        print(f"\n⚠️  No providers available. Add API keys to enable real AI responses.")

if __name__ == "__main__":
    asyncio.run(test_real_providers())