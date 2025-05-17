# ENTAERA Usage Guide

## Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed locally
- API keys (optional for cloud providers)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SaurabhCodesAI/ENTAERA.git
cd ENTAERA
```

2. **Install dependencies**
```bash
pip install -r requirements-local-models.txt
```

3. **Install and configure Ollama**
```bash
# Download from https://ollama.ai
ollama pull llama3.1:8b
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys (optional)
```

5. **Verify installation**
```bash
python check.py
```

### First Run

```bash
python agent.py
```

## Basic Usage

### Interactive Mode

Start the agent and ask questions naturally:

```bash
$ python agent.py

You: What is machine learning?
→ Routing to: Assistant (ollama)
Response: Machine learning is...

You: Write a poem about AI
→ Routing to: Creative Writer (gemini)
Response: [Creative poem]

You: What's the latest AI news?
→ Routing to: Research Assistant (perplexity)
Response: [Real-time news with sources]
```

### Built-in Commands

| Command | Description |
|---------|-------------|
| `/agents` | List all available agents and their specializations |
| `/status` | Check API connection status |
| `/quit` | Exit the system |

## Advanced Usage

### Query Routing Examples

#### General Questions → Assistant (Ollama)
```
What is Python?
How does machine learning work?
Explain neural networks
```

#### Code Tasks → Code Assistant (Ollama)
```
Write a Python function to reverse a string
Debug this code: [paste code]
How do I implement a binary search?
```

#### Data Analysis → Data Analyst (Ollama)
```
Compare Python and JavaScript
Analyze the pros and cons of microservices
Evaluate different database options
```

#### Creative Writing → Creative Writer (Gemini)
```
Write a haiku about technology
Create a short story about robots
Compose a poem about artificial intelligence
```

#### Real-Time Research → Research Assistant (Perplexity)
```
What's today's date?
What's the latest news about AI?
When was GPT-4 released?
Find current information about [topic]
```

## Configuration

### Customizing Agents

Edit `agent.py` to modify agent behavior:

```python
AGENTS = {
    "assistant": {
        "name": "Assistant",
        "provider": "ollama",
        "description": "General help and questions",
        "keywords": ["help", "how", "what", "explain"],
        "system_prompt": "You are a helpful AI assistant."
    }
}
```

### Adding Keywords

Improve routing accuracy by adding relevant keywords:

```python
"keywords": ["help", "how", "what", "explain", "tell", "show"]
```

### Changing Providers

Switch an agent's AI provider:

```python
# Use Ollama instead of Gemini for creative writing
AGENTS["writer"]["provider"] = "ollama"
```

### Priority Tuning

Adjust priority scores in `select_agent()`:

```python
# Boost priority for time-sensitive queries
if agent_id == "researcher":
    if any(k in query_lower for k in ["latest", "today", "current"]):
        score += 10  # Higher number = higher priority
```

## API Keys

### Required
- **Ollama**: No API key needed (runs locally)

### Optional (System works without these)
- **Gemini**: Get from [Google AI Studio](https://aistudio.google.com/apikey)
- **Perplexity**: Get from [Perplexity Settings](https://www.perplexity.ai/settings/api)

### Key Rotation

Configure multiple Gemini keys for rate limit handling:

```bash
GEMINI_API_KEY=key1
GEMINI_API_KEY_2=key2
GEMINI_API_KEY_3=key3
```

System automatically rotates keys on rate limits.

## Best Practices

### Query Formulation

**Good:**
- Be specific: "Write a Python function to sort a list"
- Include context: "What are the latest trends in AI?"
- Use natural language: "Can you explain how transformers work?"

**Less Optimal:**
- Too vague: "Code"
- Missing context: "Tell me about it"
- Ambiguous: "That thing"

### Response Quality

For better responses:
1. **Be specific** - Include details about what you need
2. **Provide context** - Give background information
3. **Iterate** - Refine based on initial responses
4. **Use appropriate agent** - Match task to agent specialization

### Cost Optimization

- Use `/status` to check which APIs are active
- Most queries automatically route to free local Ollama
- Cloud APIs used only for specialized tasks:
  - Gemini: Creative writing
  - Perplexity: Real-time web search

## Troubleshooting

### System Check Fails

```bash
python check.py
```

Common fixes:
- **Ollama not found**: Install from https://ollama.ai
- **Model not available**: Run `ollama pull llama3.1:8b`
- **Missing dependencies**: Run `pip install -r requirements-local-models.txt`
- **API keys not found**: Check `.env` file exists and has correct format

### Slow Responses

- **Ollama**: First query may be slow while model loads
- **Cloud APIs**: Network latency varies
- **Solution**: Ollama responses speed up after first query

### API Errors

System automatically falls back to Ollama on errors:
- Rate limits: Automatic key rotation (Gemini)
- Network errors: Uses local Ollama
- Invalid keys: Falls back to local processing

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade aiohttp python-dotenv
```

## Performance Tips

### Faster Responses

1. Keep Ollama running (first query is slower)
2. Use local Ollama for most queries (instant after warmup)
3. Reserve cloud APIs for specialized tasks

### Memory Usage

- Ollama uses ~4-8GB RAM with llama3.1:8b
- Close other applications if system is slow
- Consider smaller models: `ollama pull llama3.1:3b`

## Examples

### Code Generation

```
You: Write a Python function to calculate fibonacci numbers

→ Routing to: Code Assistant (ollama)

Response:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Creative Writing

```
You: Write a haiku about programming

→ Routing to: Creative Writer (gemini)

Response:
Code flows like water
Bugs surface, then disappear
Logic finds its way
```

### Real-Time Research

```
You: What's the current date?

→ Routing to: Research Assistant (perplexity)

Response: Today's date is Sunday, November 2, 2025.
```

## Development

### Running Tests

```bash
# System check
python check.py

# Manual API tests
python -c "import asyncio; from agent import query_ollama; print(asyncio.run(query_ollama('test')))"
```

### Monitoring

Watch for routing decisions:
```
→ Routing to: [Agent Name] ([provider])
```

### Debugging

Enable detailed logging in `agent.py`:
- Error messages show fallback behavior
- Provider errors print before fallback

## Support

- **Documentation**: See `API_DOCUMENTATION.md`
- **Issues**: Create an issue on GitHub
- **Contributing**: See `CONTRIBUTING.md`

---

*Version: 1.0*  
*Last Updated: November 2, 2025*
