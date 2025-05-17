# ENTAERA Agent API Documentation

## Overview

ENTAERA is a multi-agent AI system with intelligent query routing across multiple AI providers. The system automatically selects the best AI agent for each query based on content analysis.

## Quick Start

```bash
# Install dependencies
pip install aiohttp python-dotenv

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run system check
python check.py

# Start the agent
python agent.py
```

## Architecture

### Multi-Provider Design

The system integrates three AI providers:

1. **Ollama (Local)** - llama3.1:8b model running locally
2. **Google Gemini** - Gemini 2.5 Flash for creative tasks
3. **Perplexity** - Sonar model for real-time web research

### Intelligent Routing

Queries are automatically routed to the optimal agent based on:
- Keyword analysis
- Context classification
- Priority scoring

### Agent Specializations

| Agent | Provider | Specialization | Keywords |
|-------|----------|----------------|----------|
| Assistant | Ollama | General queries | help, how, what, explain |
| Code Assistant | Ollama | Programming | code, function, debug, program |
| Data Analyst | Ollama | Analysis | analyze, compare, evaluate |
| Creative Writer | Gemini 2.5 | Creative content | write, create, story, poem |
| Research Assistant | Perplexity | Real-time data | latest, news, today, current |

## API Functions

### Core Functions

#### `query_ollama(prompt, system_prompt="")`
Query local Ollama instance.

**Parameters:**
- `prompt` (str): User query
- `system_prompt` (str, optional): System instruction

**Returns:** str - AI response

**Example:**
```python
result = await query_ollama("What is Python?")
```

#### `query_gemini(prompt, system_prompt="")`
Query Google Gemini API with automatic key rotation.

**Parameters:**
- `prompt` (str): User query
- `system_prompt` (str, optional): System instruction

**Returns:** str - AI response

**Features:**
- Automatic key rotation on rate limits
- Fallback to Ollama on errors
- Uses Gemini 2.5 Flash model

#### `query_perplexity(prompt, system_prompt="")`
Query Perplexity API for real-time web search.

**Parameters:**
- `prompt` (str): User query
- `system_prompt` (str, optional): System instruction

**Returns:** str - AI response with citations

**Features:**
- Real-time web search
- Sonar model (fast online search)
- Fallback to Ollama on errors

### Routing Functions

#### `select_agent(query)`
Automatically select the best agent for a query.

**Parameters:**
- `query` (str): User input

**Returns:** tuple(agent_id, agent_config)

**Algorithm:**
1. Tokenize and lowercase query
2. Score against agent keywords
3. Apply priority boosts (e.g., +10 for time-sensitive queries)
4. Return highest scoring agent

#### `process_query(query)`
Process a query end-to-end with routing.

**Parameters:**
- `query` (str): User input

**Returns:** str - AI response

**Flow:**
1. Select optimal agent
2. Route to appropriate provider
3. Handle errors with fallbacks
4. Return response

## Configuration

### Environment Variables

Required in `.env`:

```bash
# Ollama (Local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Google Gemini (Optional - falls back to Ollama)
GEMINI_API_KEY=your_key_here
GEMINI_API_KEY_2=your_key_here
GEMINI_API_KEY_3=your_key_here

# Perplexity (Optional - falls back to Ollama)
PERPLEXITY_API_KEY=your_key_here
```

### Agent Configuration

Modify `AGENTS` dictionary in `agent.py`:

```python
AGENTS = {
    "agent_id": {
        "name": "Agent Name",
        "provider": "ollama|gemini|perplexity",
        "description": "What this agent does",
        "keywords": ["keyword1", "keyword2"],
        "system_prompt": "System instruction for this agent"
    }
}
```

## Error Handling

### Automatic Fallbacks

All cloud API functions automatically fall back to Ollama:

```python
try:
    # Try cloud API
    response = await api_call()
except Exception:
    # Fallback to local Ollama
    response = await query_ollama(prompt)
```

### Rate Limit Management

Gemini implements automatic key rotation:
- Maintains 3 API keys
- Rotates on 429 (rate limit) errors
- Falls back to Ollama when all keys exhausted

### Timeout Configuration

All API calls have 30-second timeouts:

```python
timeout=aiohttp.ClientTimeout(total=30)
```

## Interactive Commands

When running `python agent.py`:

| Command | Description |
|---------|-------------|
| `/agents` | List all available agents |
| `/status` | Check API connection status |
| `/quit` | Exit the system |

## Advanced Usage

### Custom Agent

Add a new specialized agent:

```python
AGENTS["custom"] = {
    "name": "Custom Agent",
    "provider": "ollama",
    "description": "Custom functionality",
    "keywords": ["custom", "special"],
    "system_prompt": "You are a custom specialist."
}
```

### Priority Scoring

Boost priority for specific queries:

```python
if agent_id == "custom":
    if any(k in query_lower for k in ["urgent", "critical"]):
        score += 20  # High priority boost
```

### Provider Configuration

Change provider for existing agent:

```python
AGENTS["writer"]["provider"] = "ollama"  # Use local instead of Gemini
```

## Performance

### Response Times

| Provider | Typical Response Time |
|----------|----------------------|
| Ollama | 0.5-2 seconds |
| Gemini | 1-3 seconds |
| Perplexity | 2-5 seconds |

### Cost Optimization

- 80% of queries handled by free local Ollama
- Cloud APIs used only for specialized tasks
- Estimated monthly cost: <$5 for typical usage

## Testing

### System Check

```bash
python check.py
```

Verifies:
- Ollama installation and model availability
- Environment configuration
- API keys presence
- Python dependencies

### Manual Testing

Test individual providers:

```python
import asyncio
from agent import query_ollama, query_gemini, query_perplexity

# Test Ollama
result = asyncio.run(query_ollama("Hello"))

# Test Gemini
result = asyncio.run(query_gemini("Write a haiku"))

# Test Perplexity
result = asyncio.run(query_perplexity("What's the date today?"))
```

## Troubleshooting

### Common Issues

**Ollama Not Found**
```bash
# Install Ollama from https://ollama.ai
# Pull model
ollama pull llama3.1:8b
```

**API Key Errors**
- Verify keys in `.env`
- Check key validity at provider websites
- System will fallback to Ollama automatically

**Import Errors**
```bash
pip install aiohttp python-dotenv
```

## Contributing

See `CONTRIBUTING.md` for development guidelines.

## License

See `LICENSE` file for details.

---

*Documentation Version: 1.0*  
*Last Updated: November 2, 2025*
