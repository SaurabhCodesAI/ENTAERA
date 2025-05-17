"""
ENTAERA AI Providers
Multi-provider AI system for VertexAutoGPT agents.
"""

from .ai_providers import (
    AIProviderType,
    AIResponse,
    AIProviderInterface,
    OpenAIProvider,
    AzureOpenAIProvider,
    GeminiProvider,
    PerplexityProvider,
    LocalModelProvider,
    SmartAIRouter,
    ai_router
)

# Real AI providers (production)
try:
    from .real_ai_providers import (
        ProductionAIRouter,
        RealOpenAIProvider,
        RealAzureOpenAIProvider,
        RealGeminiProvider,
        RealPerplexityProvider
    )
    REAL_AI_AVAILABLE = True
except ImportError:
    REAL_AI_AVAILABLE = False
    ProductionAIRouter = None

__all__ = [
    "AIProviderType",
    "AIResponse", 
    "AIProviderInterface",
    "OpenAIProvider",
    "AzureOpenAIProvider",
    "GeminiProvider",
    "PerplexityProvider",
    "LocalModelProvider",
    "SmartAIRouter",
    "ai_router",
    "ProductionAIRouter",
    "REAL_AI_AVAILABLE"
]