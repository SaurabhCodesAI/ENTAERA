"""
ENTAERA Smart API Router
Optimized routing for Azure + Gemini Student Pro + Perplexity Airtel
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .rate_limiter import rate_limiter

logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    """Task complexity levels for routing decisions."""
    SIMPLE = "simple"           # Local models can handle
    MODERATE = "moderate"       # Azure GPT-3.5 sufficient  
    COMPLEX = "complex"         # Need Gemini or GPT-4
    RESEARCH = "research"       # Requires web search (Perplexity)

class APIProvider(Enum):
    """Available API providers."""
    LOCAL = "local"
    AZURE = "azure"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"

@dataclass
class RoutingDecision:
    """Result of routing decision."""
    provider: APIProvider
    model: str
    reasoning: str
    estimated_cost: float
    estimated_tokens: int

class SmartAPIRouter:
    """Smart API router with cost optimization and rate limiting."""
    
    def __init__(self):
        self.provider_costs = {
            APIProvider.LOCAL: 0.0,                    # Free
            APIProvider.AZURE: 0.002,                  # ~$0.002 per 1k tokens
            APIProvider.GEMINI: 0.0,                   # Free tier (limited)
            APIProvider.PERPLEXITY: 0.0,               # Airtel subscription
        }
        
        self.provider_capabilities = {
            APIProvider.LOCAL: {
                "max_tokens": 512,
                "good_for": ["embeddings", "simple_analysis", "basic_chat"],
                "languages": ["python", "javascript", "general"]
            },
            APIProvider.AZURE: {
                "max_tokens": 4000,
                "good_for": ["code_generation", "analysis", "reasoning", "completion"],
                "languages": ["python", "javascript", "typescript", "sql", "general"]
            },
            APIProvider.GEMINI: {
                "max_tokens": 800000,  # Your adjusted limit
                "good_for": ["complex_reasoning", "large_context", "analysis"],
                "languages": ["python", "javascript", "general", "research"]
            },
            APIProvider.PERPLEXITY: {
                "max_tokens": 120000,  # Sonar Pro limit
                "good_for": ["web_search", "research", "real_time_data", "citations"],
                "languages": ["general", "research"]
            }
        }
    
    async def route_request(
        self,
        task_type: str,
        content: str,
        complexity: TaskComplexity = TaskComplexity.MODERATE,
        preferred_provider: Optional[APIProvider] = None,
        estimated_tokens: int = 1000
    ) -> RoutingDecision:
        """Route a request to the optimal API provider."""
        
        # Check for research tasks (always use Perplexity)
        if self._is_research_task(task_type, content):
            if await rate_limiter.can_make_request("perplexity", estimated_tokens):
                return RoutingDecision(
                    provider=APIProvider.PERPLEXITY,
                    model="sonar",
                    reasoning="Research task requiring web search - cost optimized",
                    estimated_cost=0.0,
                    estimated_tokens=estimated_tokens
                )
        
        # Check for simple tasks (try local first)
        if complexity == TaskComplexity.SIMPLE and estimated_tokens <= 512:
            return RoutingDecision(
                provider=APIProvider.LOCAL,
                model="sentence-transformers",
                reasoning="Simple task, local model sufficient",
                estimated_cost=0.0,
                estimated_tokens=estimated_tokens
            )
        
        # Check preferred provider if specified
        if preferred_provider and await self._can_use_provider(preferred_provider, estimated_tokens):
            model = self._get_best_model_for_provider(preferred_provider, task_type)
            return RoutingDecision(
                provider=preferred_provider,
                model=model,
                reasoning=f"Preferred provider {preferred_provider.value} available",
                estimated_cost=self._estimate_cost(preferred_provider, estimated_tokens),
                estimated_tokens=estimated_tokens
            )
        
        # Route based on complexity and availability
        return await self._route_by_complexity(task_type, complexity, estimated_tokens)
    
    async def _route_by_complexity(
        self,
        task_type: str,
        complexity: TaskComplexity,
        estimated_tokens: int
    ) -> RoutingDecision:
        """Route based on task complexity and API availability."""
        
        if complexity == TaskComplexity.SIMPLE:
            # Try local -> Azure -> Gemini
            if estimated_tokens <= 512:
                return RoutingDecision(
                    provider=APIProvider.LOCAL,
                    model="local-embedding",
                    reasoning="Simple task, using local model",
                    estimated_cost=0.0,
                    estimated_tokens=estimated_tokens
                )
        
        if complexity in [TaskComplexity.MODERATE, TaskComplexity.SIMPLE]:
            # Try Azure first (cost-effective)
            if await rate_limiter.can_make_request("azure", estimated_tokens):
                return RoutingDecision(
                    provider=APIProvider.AZURE,
                    model="gpt-35-turbo",
                    reasoning="Moderate task, Azure GPT-3.5 sufficient",
                    estimated_cost=self._estimate_cost(APIProvider.AZURE, estimated_tokens),
                    estimated_tokens=estimated_tokens
                )
        
        if complexity == TaskComplexity.COMPLEX:
            # Try Gemini for complex tasks (but limited quota)
            if await rate_limiter.can_make_request("gemini", estimated_tokens):
                return RoutingDecision(
                    provider=APIProvider.GEMINI,
                    model="gemini-1.5-flash-8b",
                    reasoning="Complex task - cost optimized base model",
                    estimated_cost=0.0,
                    estimated_tokens=estimated_tokens
                )
            
            # Fallback to Azure
            if await rate_limiter.can_make_request("azure", estimated_tokens):
                return RoutingDecision(
                    provider=APIProvider.AZURE,
                    model="gpt-35-turbo",
                    reasoning="Gemini unavailable, using Azure fallback",
                    estimated_cost=self._estimate_cost(APIProvider.AZURE, estimated_tokens),
                    estimated_tokens=estimated_tokens
                )
        
        # Last resort: try any available provider
        for provider in [APIProvider.AZURE, APIProvider.GEMINI, APIProvider.PERPLEXITY]:
            if await rate_limiter.can_make_request(provider.value, estimated_tokens):
                model = self._get_best_model_for_provider(provider, task_type)
                return RoutingDecision(
                    provider=provider,
                    model=model,
                    reasoning=f"Last resort: using available {provider.value}",
                    estimated_cost=self._estimate_cost(provider, estimated_tokens),
                    estimated_tokens=estimated_tokens
                )
        
        # Absolute fallback: local model (even if not ideal)
        return RoutingDecision(
            provider=APIProvider.LOCAL,
            model="local-fallback",
            reasoning="All APIs unavailable, using local fallback",
            estimated_cost=0.0,
            estimated_tokens=min(estimated_tokens, 512)
        )
    
    def _is_research_task(self, task_type: str, content: str) -> bool:
        """Determine if this is a research task requiring web search."""
        research_keywords = [
            "search", "research", "latest", "current", "recent", "news",
            "web", "internet", "online", "real-time", "citation", "source"
        ]
        
        research_task_types = [
            "web_search", "research", "fact_check", "current_events",
            "market_research", "competitive_analysis"
        ]
        
        return (
            task_type in research_task_types or
            any(keyword in content.lower() for keyword in research_keywords)
        )
    
    async def _can_use_provider(self, provider: APIProvider, estimated_tokens: int) -> bool:
        """Check if we can use a specific provider."""
        if provider == APIProvider.LOCAL:
            return True  # Always available
        
        return await rate_limiter.can_make_request(provider.value, estimated_tokens)
    
    def _get_best_model_for_provider(self, provider: APIProvider, task_type: str) -> str:
        """Get the best model for a provider and task type."""
        model_map = {
            APIProvider.LOCAL: "sentence-transformers/all-MiniLM-L6-v2",
            APIProvider.AZURE: "gpt-35-turbo",
            APIProvider.GEMINI: "gemini-1.5-flash-8b",
            APIProvider.PERPLEXITY: "sonar"
        }
        
        return model_map.get(provider, "default")
    
    def _estimate_cost(self, provider: APIProvider, estimated_tokens: int) -> float:
        """Estimate cost for a request."""
        if provider in [APIProvider.LOCAL, APIProvider.GEMINI, APIProvider.PERPLEXITY]:
            return 0.0  # Free or subscription-based
        
        # Azure pricing (approximate)
        if provider == APIProvider.AZURE:
            return (estimated_tokens / 1000) * self.provider_costs[provider]
        
        return 0.0
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing and usage statistics."""
        usage_stats = rate_limiter.get_all_usage_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "api_usage": usage_stats,
            "routing_preferences": {
                "simple_tasks": "Local models",
                "moderate_tasks": "Azure GPT-3.5",
                "complex_tasks": "Gemini (limited quota)",
                "research_tasks": "Perplexity Sonar Pro"
            },
            "cost_optimization": {
                "local_usage": "Maximized for embeddings and simple tasks",
                "azure_budget": "$5/day limit",
                "api_conservation": "Smart rate limiting enabled"
            }
        }
    
    async def execute_routed_request(
        self,
        routing_decision: RoutingDecision,
        request_func,
        *args,
        **kwargs
    ) -> Any:
        """Execute a request using the routed provider."""
        provider_name = routing_decision.provider.value
        
        try:
            # Acquire rate limit permission
            if provider_name != "local":
                acquired = await rate_limiter.acquire(provider_name, routing_decision.estimated_tokens)
                if not acquired:
                    raise Exception(f"Rate limit exceeded for {provider_name}")
            
            # Log the routing decision
            logger.info(f"Routing to {provider_name}: {routing_decision.reasoning}")
            
            # Execute the request
            result = await request_func(*args, **kwargs)
            
            return result
            
        except Exception as e:
            logger.error(f"Request failed on {provider_name}: {e}")
            raise
            
        finally:
            # Release rate limit
            if provider_name != "local":
                rate_limiter.release(provider_name)

# Global router instance
api_router = SmartAPIRouter()

async def test_api_router():
    """Test the API router functionality."""
    print("🧪 Testing Smart API Router")
    print("=" * 40)
    
    test_cases = [
        ("Simple embedding task", TaskComplexity.SIMPLE, 100),
        ("Code generation", TaskComplexity.MODERATE, 2000),
        ("Complex analysis", TaskComplexity.COMPLEX, 5000),
        ("Web research task", TaskComplexity.RESEARCH, 3000),
    ]
    
    for task_desc, complexity, tokens in test_cases:
        print(f"\n📝 Task: {task_desc}")
        
        decision = await api_router.route_request(
            task_type=task_desc.lower().replace(" ", "_"),
            content=task_desc,
            complexity=complexity,
            estimated_tokens=tokens
        )
        
        print(f"   🎯 Routed to: {decision.provider.value}")
        print(f"   🤖 Model: {decision.model}")
        print(f"   💭 Reasoning: {decision.reasoning}")
        print(f"   💰 Cost: ${decision.estimated_cost:.4f}")
    
    # Print routing stats
    print("\n📊 Routing Statistics:")
    stats = api_router.get_routing_stats()
    for api, usage in stats["api_usage"].items():
        print(f"   {api}: {usage['daily_usage']['requests']}")

if __name__ == "__main__":
    asyncio.run(test_api_router())