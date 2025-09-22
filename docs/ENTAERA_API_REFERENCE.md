# ENTAERA API Reference Guide

This document provides a comprehensive reference for integrating with the ENTAERA framework's APIs and using its provider integration capabilities.

## Table of Contents

1. [Core API Functions](#core-api-functions)
2. [Provider Integration](#provider-integration)
3. [Azure OpenAI API](#azure-openai-api)
4. [Google Gemini API](#google-gemini-api)
5. [Perplexity API](#perplexity-api)
6. [Local AI Integration](#local-ai-integration)
7. [Smart Routing API](#smart-routing-api)
8. [Conversation Management](#conversation-management)
9. [Context Injection](#context-injection)
10. [API Response Handling](#api-response-handling)

---

## Core API Functions

### SmartAPIRouter

The central routing system for directing queries to appropriate AI providers.

```python
from entaera.utils.api_router import SmartAPIRouter, TaskComplexity

# Initialize the router
router = SmartAPIRouter()

# Get response with automatic provider selection
response = await router.get_response(
    prompt="Your query here",
    complexity=TaskComplexity.MEDIUM,  # Optional: LOW, MEDIUM, HIGH
    context={"user": "User Name"}  # Optional context
)

# Force specific provider
response = await router.get_response(
    prompt="Your query here",
    provider="azure_openai"  # Options: azure_openai, gemini, perplexity, local_ai
)
```

### ConversationManager

Manages conversation history and context.

```python
from entaera.core.conversation import ConversationManager, Message, MessageRole

# Initialize manager
conv_manager = ConversationManager()

# Create new conversation
conversation = conv_manager.create_conversation("Session Name")

# Add messages
conversation.add_message(MessageRole.USER, "Hello, how are you?")
conversation.add_message(MessageRole.ASSISTANT, "I'm doing well, thank you!")

# Get conversation history
history = conversation.get_messages()

# Get formatted history for API requests
formatted_history = conversation.format_for_provider("azure_openai")
```

### Direct API Testing Functions

Standalone functions for direct API testing:

```python
from azure_continuous_test import test_azure_openai_api, test_gemini_api, test_perplexity_api

# Test Azure OpenAI
response, error = await test_azure_openai_api("Your prompt here")

# Test Google Gemini
response, error = await test_gemini_api("Your prompt here")

# Test Perplexity
response, error = await test_perplexity_api("Your prompt here")
```

---

## Provider Integration

### API Configuration

Configuration variables for each provider:

```python
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-12-01-preview
AZURE_DEPLOYMENT_NAME=gpt-35-turbo

# Google Gemini
GEMINI_API_KEY=your_key_here

# Perplexity
PERPLEXITY_API_KEY=your_key_here

# Local AI
LOCAL_AI_MODEL_PATH=models/llama-3.1-8b-q4.gguf
```

### Provider Selection Logic

Implementation of the provider selection system:

```python
# Task complexity levels
class TaskComplexity(Enum):
    LOW = 1      # Simple, factual questions
    MEDIUM = 2   # Moderate reasoning, explanation
    HIGH = 3     # Complex reasoning, creative tasks

# Provider capabilities
PROVIDER_CAPABILITIES = {
    "azure_openai": {
        "complexity_range": [TaskComplexity.MEDIUM, TaskComplexity.HIGH],
        "strengths": ["reasoning", "coding", "creativity"],
        "cost_per_1k_tokens": 0.002
    },
    "gemini": {
        "complexity_range": [TaskComplexity.LOW, TaskComplexity.MEDIUM],
        "strengths": ["simple_facts", "quick_responses"],
        "cost_per_1k_tokens": 0.001
    },
    "perplexity": {
        "complexity_range": [TaskComplexity.MEDIUM, TaskComplexity.HIGH],
        "strengths": ["current_data", "research", "web_knowledge"],
        "cost_per_1k_tokens": 0.003
    }
}

# Provider selection based on query characteristics
def select_provider(query, complexity=None):
    # Implementation details in src/entaera/utils/api_router.py
    pass
```

---

## Azure OpenAI API

### API Reference

```python
async def call_azure_openai(
    prompt: str, 
    system_message: str = "You are ENTAERA AI assistant powered by Azure OpenAI.",
    model: str = None,
    max_tokens: int = 500,
    temperature: float = 0.7
) -> Tuple[str, Optional[str]]:
    """
    Call Azure OpenAI API with the given prompt.
    
    Args:
        prompt: User query
        system_message: System instruction
        model: Model name (defaults to AZURE_DEPLOYMENT_NAME)
        max_tokens: Maximum response tokens
        temperature: Creativity temperature (0.0-1.0)
        
    Returns:
        Tuple of (response_text, error_message)
    """
```

### Example Usage

```python
# Simple call
response, error = await test_azure_openai_api("Explain quantum computing")

# Advanced call with system message
response, error = await call_azure_openai(
    prompt="Write a Python function to find prime numbers",
    system_message="You are an expert Python programmer. Provide clean, efficient code with explanations.",
    max_tokens=800,
    temperature=0.3
)
```

### Request Format

```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are ENTAERA AI assistant powered by Azure OpenAI."
        },
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ],
    "max_tokens": 500,
    "temperature": 0.7,
    "top_p": 0.95,
    "frequency_penalty": 0,
    "presence_penalty": 0
}
```

---

## Google Gemini API

### API Reference

```python
async def call_gemini_api(
    prompt: str,
    model: str = "gemini-1.5-flash",
    max_tokens: int = None,
    temperature: float = 0.7
) -> Tuple[str, Optional[str]]:
    """
    Call Google Gemini API with the given prompt.
    
    Args:
        prompt: User query
        model: Model name
        max_tokens: Maximum response tokens
        temperature: Creativity temperature (0.0-1.0)
        
    Returns:
        Tuple of (response_text, error_message)
    """
```

### Example Usage

```python
# Simple call
response, error = await test_gemini_api("What is the capital of France?")

# Advanced call
response, error = await call_gemini_api(
    prompt="Summarize the key points about climate change",
    model="gemini-1.5-pro",
    temperature=0.2
)
```

### Request Format

```json
{
    "contents": [{
        "parts": [{
            "text": "Your prompt here"
        }]
    }]
}
```

---

## Perplexity API

### API Reference

```python
async def call_perplexity_api(
    prompt: str,
    model: str = "sonar",
    max_tokens: int = 300,
    temperature: float = 0.2,
    search_recency_filter: str = "month"
) -> Tuple[str, Optional[str]]:
    """
    Call Perplexity API with the given prompt.
    
    Args:
        prompt: User query
        model: Model name
        max_tokens: Maximum response tokens
        temperature: Creativity temperature (0.0-1.0)
        search_recency_filter: Recency filter for search results
        
    Returns:
        Tuple of (response_text, error_message)
    """
```

### Example Usage

```python
# Simple call
response, error = await test_perplexity_api("What is the latest news about SpaceX?")

# Advanced call
response, error = await call_perplexity_api(
    prompt="Research recent breakthroughs in fusion energy",
    model="sonar",
    search_recency_filter="week",
    max_tokens=500
)
```

### Request Format

```json
{
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ],
    "max_tokens": 300,
    "temperature": 0.2,
    "top_p": 0.9,
    "return_images": false,
    "return_related_questions": false,
    "search_recency_filter": "month",
    "top_k": 0,
    "stream": false,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
```

---

## Local AI Integration

### API Reference

```python
async def call_local_ai(
    prompt: str,
    model_path: str = None,
    context_length: int = 2048,
    max_tokens: int = 500,
    temperature: float = 0.7
) -> Tuple[str, Optional[str]]:
    """
    Call local AI model with the given prompt.
    
    Args:
        prompt: User query
        model_path: Path to local model file
        context_length: Maximum context window
        max_tokens: Maximum response tokens
        temperature: Creativity temperature (0.0-1.0)
        
    Returns:
        Tuple of (response_text, error_message)
    """
```

### Example Usage

```python
from local_model_loader import call_local_ai

# Call local model
response, error = await call_local_ai(
    prompt="Explain how neural networks work",
    model_path="models/llama-3.1-8b-q4.gguf"
)
```

### Model Setup

```python
# Download and set up local models
from setup_models import download_model

# Download specific model
download_model("llama-3.1-8b")

# Or run full setup script
# python setup_models.py
```

---

## Smart Routing API

### API Reference

```python
class SmartAPIRouter:
    async def get_response(
        self,
        prompt: str,
        complexity: TaskComplexity = None,
        provider: str = None,
        context: dict = None,
        fallback: bool = True
    ) -> Tuple[str, Optional[str]]:
        """
        Get response from the optimal AI provider.
        
        Args:
            prompt: User query
            complexity: Task complexity level
            provider: Force specific provider
            context: Additional context data
            fallback: Enable fallback to alternative providers
            
        Returns:
            Tuple of (response_text, error_message)
        """
```

### Example Usage

```python
from entaera.utils.api_router import SmartAPIRouter, TaskComplexity

router = SmartAPIRouter()

# Automatic routing
response, error = await router.get_response(
    prompt="What is the current Bitcoin price?",
    context={"user_preference": "detailed_data"}
)

# Forced provider with fallback
response, error = await router.get_response(
    prompt="Write a Python function to calculate Fibonacci numbers",
    provider="azure_openai",
    fallback=True
)

# Complexity-based routing
response, error = await router.get_response(
    prompt="Explain the theory of relativity",
    complexity=TaskComplexity.HIGH
)
```

### Content Detection Examples

```python
def detect_content_type(prompt: str) -> ContentType:
    """
    Detect the type of content in a prompt to inform provider selection.
    
    Returns:
        ContentType enum value
    """
    prompt_lower = prompt.lower()
    
    # Current events/data detection
    if any(word in prompt_lower for word in [
        'latest', 'current', 'recent', 'news', 'today',
        'stock', 'price', 'market', 'worth'
    ]):
        return ContentType.CURRENT_DATA
    
    # Technical/coding detection
    if any(word in prompt_lower for word in [
        'code', 'function', 'programming', 'algorithm', 'python',
        'javascript', 'html', 'sql', 'database', 'api'
    ]):
        return ContentType.TECHNICAL
    
    # Complex reasoning detection
    if any(word in prompt_lower for word in [
        'explain', 'analyze', 'compare', 'evaluate', 'synthesis',
        'philosophy', 'theory', 'concept', 'implications'
    ]):
        return ContentType.COMPLEX_REASONING
    
    # Default to general knowledge
    return ContentType.GENERAL_KNOWLEDGE
```

---

## Conversation Management

### API Reference

```python
class ConversationManager:
    def create_conversation(self, session_name: str) -> Conversation:
        """Create a new conversation session"""
    
    def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """Retrieve an existing conversation"""
    
    def list_conversations(self) -> List[str]:
        """List all active conversation session IDs"""

class Conversation:
    def add_message(self, role: MessageRole, content: str) -> None:
        """Add a message to the conversation"""
    
    def get_messages(self) -> List[Message]:
        """Get all messages in the conversation"""
    
    def clear_history(self) -> None:
        """Clear conversation history"""
    
    def format_for_provider(self, provider: str) -> List[Dict]:
        """Format conversation history for specific provider API"""
```

### Example Usage

```python
from entaera.core.conversation import ConversationManager, MessageRole

# Initialize manager
manager = ConversationManager()

# Create conversation
conversation = manager.create_conversation("User Session")

# Add user message
conversation.add_message(MessageRole.USER, "How does nuclear fusion work?")

# Add AI response
conversation.add_message(
    MessageRole.ASSISTANT, 
    "Nuclear fusion occurs when two light atomic nuclei combine to form a heavier nucleus, releasing energy."
)

# Get formatted history for Azure OpenAI
formatted_history = conversation.format_for_provider("azure_openai")
```

---

## Context Injection

### API Reference

```python
class ContextInjector:
    def inject_context(
        self,
        prompt: str,
        context: dict = None,
        conversation: Conversation = None
    ) -> str:
        """
        Inject relevant context into a prompt.
        
        Args:
            prompt: Original user prompt
            context: Additional context dictionary
            conversation: Conversation object with history
            
        Returns:
            Enhanced prompt with context
        """
```

### Example Usage

```python
from entaera.core.context_injection import ContextInjector

injector = ContextInjector()

# Project context
project_context = {
    "project": "ENTAERA",
    "creator": "Saurabh Pareek",
    "description": "Multi-API intelligent routing framework"
}

# Inject context
enhanced_prompt = injector.inject_context(
    prompt="Who created this project?",
    context=project_context,
    conversation=current_conversation
)
```

### Standard Context Format

```python
# Standard context structure
context = {
    "user": {
        "name": "User Name",
        "preferences": {...}
    },
    "project": {
        "name": "Project Name",
        "description": "...",
        "creator": "Creator Name"
    },
    "system": {
        "capabilities": [...],
        "limitations": [...]
    }
}
```

---

## API Response Handling

### Response Error Detection

```python
def detect_bad_response(response: str, user_input: str) -> bool:
    """
    Detect responses that are outdated, unhelpful, or wrong.
    
    Args:
        response: AI response text
        user_input: Original user query
        
    Returns:
        True if response is problematic, False otherwise
    """
    if not response:
        return True
    
    response_lower = response.lower()
    input_lower = user_input.lower()
    
    # Outdated year references
    if any(year in response_lower for year in ['2023', '2022', '2021', '2020']):
        return True
    
    # Generic unhelpful responses
    if any(phrase in response_lower for phrase in [
        'i cannot provide', 'too vague', 'grammatically incorrect',
        'i don\'t have access to real-time', 'consult a reputable'
    ]):
        return True
    
    # Context mismatch (when asking about ENTAERA project)
    if 'entaera' in input_lower and 'life sciences' in response_lower:
        return True
    
    return False
```

### Response Enhancement

```python
async def enhance_response(
    response: str,
    user_input: str,
    primary_provider: str
) -> str:
    """
    Enhance or correct problematic responses.
    
    Args:
        response: Original response
        user_input: User query
        primary_provider: Provider that generated the original response
        
    Returns:
        Enhanced or corrected response
    """
    # If response seems fine, return it
    if not detect_bad_response(response, user_input):
        return response
    
    # Try alternative provider
    if primary_provider == "gemini":
        better_response, error = await test_perplexity_api(user_input)
    else:
        better_response, error = await test_azure_openai_api(user_input)
    
    # Return better response if available and not problematic
    if better_response and not detect_bad_response(better_response, user_input):
        return better_response
    
    # Return original if fallback fails
    return response
```

### Error Handling

```python
async def handle_api_error(
    error: str,
    prompt: str,
    primary_provider: str
) -> Tuple[str, Optional[str]]:
    """
    Handle API errors with fallback strategy.
    
    Args:
        error: Error message from primary provider
        prompt: Original user prompt
        primary_provider: Provider that generated the error
        
    Returns:
        Tuple of (response_text, error_message)
    """
    # Log the error
    print(f"API Error ({primary_provider}): {error}")
    
    # Try Perplexity for current data if not already tried
    if primary_provider != "perplexity":
        response, new_error = await test_perplexity_api(prompt)
        if not new_error:
            return response, None
    
    # Try Azure as final fallback if not already tried
    if primary_provider != "azure_openai":
        response, new_error = await test_azure_openai_api(prompt)
        if not new_error:
            return response, None
    
    # All fallbacks failed
    return None, "All API providers failed"
```

---

This API reference guide provides the essential information needed to integrate with and extend the ENTAERA framework's capabilities. For more detailed implementation examples, refer to the sample code in the `examples/` directory.