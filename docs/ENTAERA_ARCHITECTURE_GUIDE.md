# ENTAERA Architecture Guide

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Core Architectural Components](#core-architectural-components)
3. [Data Flow](#data-flow)
4. [Key Design Patterns](#key-design-patterns)
5. [Component Interactions](#component-interactions)
6. [Performance Considerations](#performance-considerations)
7. [Future Architecture Extensions](#future-architecture-extensions)

## System Architecture Overview

ENTAERA is designed with a modular, extensible architecture that enables intelligent AI provider routing while maintaining clean separation of concerns. This document outlines the core architectural components and how they interact.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ENTAERA FRAMEWORK                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐     ┌───────────────┐      ┌───────────────────┐     │
│  │  User Input   │────▶│  Smart Router │ ────▶│  Provider Layer   │     │
│  └───────────────┘     └───────┬───────┘      └─────────┬─────────┘     │
│                                │                        │               │
│                         ┌──────┴──────┐         ┌───────┴────────┐      │
│                         │             │         │                │      │
│                         ▼             │         ▼                │      │
│                  ┌──────────────┐     │   ┌─────────────┐  ┌─────────┐ │
│                  │  Context     │     │   │  Azure      │  │ Gemini  │ │
│                  │  Management  │     │   │  OpenAI     │  │ API     │ │
│                  └──────────────┘     │   └─────────────┘  └─────────┘ │
│                         ▲             │         ▲                │      │
│                         │             │         │                │      │
│                  ┌──────┴───────┐     │   ┌─────┴──────┐  ┌─────┴─────┐│
│                  │ Conversation │◀────┘   │ Perplexity │  │ Local AI  ││
│                  │ Memory       │         │ API        │  │ Models    ││
│                  └──────────────┘         └────────────┘  └───────────┘│
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐     ┌───────────────┐      ┌───────────────────┐     │
│  │   Logging     │     │ Configuration │      │ Error Handling    │     │
│  │   System      │     │ Management    │      │ & Recovery        │     │
│  └───────────────┘     └───────────────┘      └───────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Architectural Components

### 1. Smart Router

The central intelligence of the ENTAERA system, the Smart Router analyzes incoming queries and directs them to the most appropriate AI provider based on:

- **Content Analysis**: Detects query type (current data, technical, general knowledge)
- **Complexity Evaluation**: Assesses query complexity (simple, moderate, complex)
- **Context Awareness**: Considers project and user context
- **Routing Logic**: Maps query characteristics to optimal providers

**Location**: `src/entaera/utils/api_router.py`

**Key Classes**:
- `SmartAPIRouter`: Main routing controller
- `TaskComplexity`: Enum defining complexity levels
- `ContentType`: Enum categorizing content types

### 2. Provider Layer

Abstraction layer that handles communication with different AI providers:

- **Unified Interface**: Common methods across all providers
- **Provider-Specific Adapters**: Custom formatting for each API
- **Authentication Management**: Secure credential handling
- **Rate Limiting**: Prevents exceeding API quotas

**Location**: `src/entaera/providers/`

**Key Components**:
- Azure OpenAI integration (`azure_continuous_test.py`)
- Google Gemini integration
- Perplexity API integration
- Local AI model integration

### 3. Context Management

Manages project and user context to enhance AI responses:

- **Context Injection**: Adds relevant context to prompts
- **Context Retrieval**: Extracts and manages context information
- **Personal Recognition**: Maintains awareness of user identity
- **Project Awareness**: Knowledge about the ENTAERA framework

**Location**: `src/entaera/core/context_injection.py`, `src/entaera/core/context_retrieval.py`

### 4. Conversation Memory

Tracks conversation history and maintains context across multiple interactions:

- **Message Storage**: Maintains history of user and AI messages
- **Session Management**: Organizes conversations into sessions
- **Context Persistence**: Ensures context carries across messages
- **Provider Formatting**: Formats history for specific provider requirements

**Location**: `src/entaera/core/conversation.py`, `src/entaera/core/conversation_memory.py`

### 5. Configuration Management

Handles system configuration and environment settings:

- **Environment Variables**: Loads and validates env vars
- **API Configuration**: Manages API keys and endpoints
- **Model Settings**: Controls model parameters
- **Environment-Specific Settings**: Different configs for dev/prod

**Location**: `src/entaera/core/config.py`

### 6. Logging System

Comprehensive logging infrastructure:

- **Structured Logging**: JSON-formatted logs for production
- **Console Output**: Developer-friendly colored output
- **Log Levels**: Multiple verbosity levels
- **Error Tracking**: Detailed error information

**Location**: `src/entaera/core/logger.py`

### 7. Error Handling & Recovery

Robust error management and recovery system:

- **Error Detection**: Identifies API failures
- **Response Quality Check**: Detects problematic/outdated responses
- **Automatic Fallback**: Tries alternative providers on failure
- **Recovery Strategies**: Multiple fallback paths

**Location**: Throughout system, centralized in API router

## Data Flow

### Request Flow

1. **User Input**: Query submitted through chat interface
2. **Context Enrichment**: System adds project/user context
3. **Query Analysis**: Smart router analyzes content and complexity
4. **Provider Selection**: Optimal provider chosen
5. **Request Formatting**: Query formatted for selected provider
6. **API Call**: Request sent to provider
7. **Response Processing**: Raw response processed and validated
8. **Quality Check**: Response checked for accuracy/relevance
9. **Fallback Logic**: Alternative provider used if needed
10. **Response Delivery**: Final answer returned to user

### Error Flow

1. **Error Detection**: System detects API failure or poor response
2. **Error Logging**: Issue logged with details
3. **Fallback Selection**: Alternative provider chosen
4. **Retry Attempt**: Query sent to fallback provider
5. **Response Evaluation**: New response checked for quality
6. **Final Resolution**: Best available response returned or error reported

## Key Design Patterns

### 1. Strategy Pattern

Used in the provider selection system to encapsulate different API strategies and make them interchangeable.

```python
# Example: Provider strategy implementation
class ProviderStrategy(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Tuple[str, Optional[str]]:
        pass

class AzureOpenAIStrategy(ProviderStrategy):
    async def generate_response(self, prompt: str, **kwargs) -> Tuple[str, Optional[str]]:
        return await test_azure_openai_api(prompt, **kwargs)

class GeminiStrategy(ProviderStrategy):
    async def generate_response(self, prompt: str, **kwargs) -> Tuple[str, Optional[str]]:
        return await test_gemini_api(prompt, **kwargs)
```

### 2. Factory Pattern

Creates appropriate provider instances based on configuration and availability.

```python
# Example: Provider factory implementation
class ProviderFactory:
    @staticmethod
    def create_provider(provider_type: str) -> ProviderStrategy:
        if provider_type == "azure_openai":
            return AzureOpenAIStrategy()
        elif provider_type == "gemini":
            return GeminiStrategy()
        elif provider_type == "perplexity":
            return PerplexityStrategy()
        elif provider_type == "local_ai":
            return LocalAIStrategy()
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
```

### 3. Chain of Responsibility

Implements fallback logic for error handling and response quality improvement.

```python
# Example: Provider fallback chain
async def execute_with_fallbacks(prompt: str, providers: List[str]) -> Tuple[str, Optional[str]]:
    for provider in providers:
        provider_instance = ProviderFactory.create_provider(provider)
        response, error = await provider_instance.generate_response(prompt)
        
        if not error and not detect_bad_response(response, prompt):
            return response, None
    
    return None, "All providers failed"
```

### 4. Observer Pattern

Monitors API calls and system behavior for logging and analysis.

```python
# Example: API call observer
class APICallObserver:
    def on_api_call_start(self, provider: str, prompt: str):
        log_api_call_start(provider, prompt)
    
    def on_api_call_complete(self, provider: str, response: str, duration_ms: int):
        log_api_call_complete(provider, response, duration_ms)
    
    def on_api_call_error(self, provider: str, error: str):
        log_api_call_error(provider, error)
```

## Component Interactions

### Smart Routing Process

```python
# Example: Smart routing logic
async def smart_route_and_call(user_input: str) -> Tuple[str, Optional[str]]:
    """Smart routing logic to choose the best API"""
    
    # Research/News/Current events/Financial data → Perplexity
    if any(word in user_input.lower() for word in [
        'research', 'news', 'latest', 'current', 'today', 'recent', 
        'what are', 'find me', 'search', 'net worth', 'networth'
    ]):
        print("🧠 ENTAERA Smart Routing: Research/Current → Perplexity")
        return await test_perplexity_api(user_input)
    
    # Coding/Technical → Azure OpenAI
    elif any(word in user_input.lower() for word in [
        'code', 'program', 'function', 'algorithm', 'debug', 'python'
    ]):
        print("🧠 ENTAERA Smart Routing: Technical → Azure OpenAI")
        return await test_azure_openai_api(user_input)
    
    # Long/Complex queries → Azure OpenAI
    elif len(user_input) > 80:
        print("🧠 ENTAERA Smart Routing: Complex query → Azure OpenAI")
        return await test_azure_openai_api(user_input)
    
    # Simple/Quick questions → Gemini
    else:
        print("🧠 ENTAERA Smart Routing: Simple task → Gemini")
        return await test_gemini_api(user_input)
```

### Context Injection Process

```python
# Example: Context injection
def detect_context_aware_queries(user_input: str) -> Optional[str]:
    """Detect queries that need context awareness"""
    input_lower = user_input.lower()
    
    # ENTAERA project questions
    if any(phrase in input_lower for phrase in [
        'entaera', 'this project', 'who created', 'developer'
    ]):
        return 'project_context'
    
    # Personal questions
    if any(phrase in input_lower for phrase in [
        'who am i', 'my name', 'what is my name'
    ]):
        return 'personal_context'
    
    return None

async def handle_context_aware_query(query_type: str, user_input: str) -> Tuple[str, Optional[str]]:
    """Handle context-aware queries with appropriate context injection"""
    if query_type == 'project_context':
        enhanced_prompt = f"""Context: {ENTAERA_CONTEXT}
        
        User question: {user_input}
        
        Please answer based on the context that ENTAERA is the AI framework 
        project created by Saurabh Pareek."""
        
        return await test_azure_openai_api(enhanced_prompt)
    
    # Handle other context types...
```

## Performance Considerations

### Response Time Optimization

- **Provider Selection**: Choose fastest provider for simple queries
- **Concurrency**: Use asyncio for parallel operations
- **Caching**: Store frequent responses to avoid API calls
- **Timeout Management**: Set appropriate timeouts for each provider

### Cost Optimization

- **Token Limiting**: Azure OpenAI configured for 3,000 tokens/minute
- **Provider Selection**: Use cheaper APIs for simple queries
- **Context Pruning**: Remove unnecessary context to save tokens
- **Response Length Control**: Set appropriate max_tokens for each query

### Error Resilience

- **Multiple Fallbacks**: Try alternative providers on failure
- **Rate Limit Handling**: Back-off strategy for rate limits
- **Connection Error Recovery**: Retry logic for network issues
- **Response Validation**: Check response quality before returning

## Future Architecture Extensions

### 1. Microservices Evolution

Future architecture could evolve into microservices:

- **API Gateway**: Central entry point for requests
- **Provider Services**: Separate service for each AI provider
- **Routing Service**: Dedicated routing intelligence
- **Memory Service**: Conversation and context management
- **Analytics Service**: Usage tracking and optimization

### 2. Enhanced Observability

- **Distributed Tracing**: Track requests across components
- **Metrics Collection**: Detailed performance metrics
- **Alerting System**: Proactive monitoring and alerts
- **Dashboard**: Real-time system visualization

### 3. Advanced AI Features

- **Multi-Agent Coordination**: Multiple specialized agents
- **Continuous Learning**: Improve routing based on feedback
- **Tool Integration**: External tool and API usage
- **Task Decomposition**: Breaking complex tasks into subtasks

## Conclusion

The ENTAERA architecture represents a sophisticated approach to AI provider integration, combining intelligent routing with robust error handling and context awareness. The modular design ensures extensibility, while the layered approach maintains clean separation of concerns.

This architecture enables ENTAERA to deliver superior AI capabilities by leveraging the strengths of multiple providers while mitigating their individual weaknesses, all while optimizing for cost, performance, and reliability.