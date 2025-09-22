# ENTAERA Framework: Frequently Asked Questions (FAQ)

## Table of Contents
1. [General Questions](#general-questions)
2. [Technical Questions](#technical-questions)
3. [Usage Questions](#usage-questions)
4. [Deployment Questions](#deployment-questions)
5. [Troubleshooting](#troubleshooting)
6. [Cost and Performance](#cost-and-performance)
7. [Development and Contribution](#development-and-contribution)

## General Questions

### What is ENTAERA?

ENTAERA is a production-ready AI framework that provides intelligent multi-API routing across various AI providers including Azure OpenAI, Google Gemini, Perplexity, and local AI models. It automatically selects the most appropriate provider based on query complexity and content requirements.

### What does "ENTAERA" stand for?

ENTAERA stands for "ENhanced Task Aware Efficient Reasoning Agent" - a name that reflects the framework's capability to intelligently route queries to the most suitable AI provider based on task complexity and requirements.

### How is ENTAERA different from other AI frameworks?

ENTAERA distinguishes itself through:
- **Multi-provider integration**: Seamlessly uses multiple AI providers
- **Smart routing intelligence**: Automatically selects optimal provider
- **Context awareness**: Maintains project and personal context
- **Error correction**: Detects and fixes bad responses
- **Cost optimization**: Uses token limiting and efficient routing
- **Local AI support**: Works offline with local models

### Who created ENTAERA?

ENTAERA was created by Saurabh Pareek as an evolution of the VertexAutoGPT framework. It represents a significant advancement in multi-provider AI integration and intelligent routing.

## Technical Questions

### What AI providers does ENTAERA support?

ENTAERA currently supports:
- **Azure OpenAI**: For complex reasoning, coding, and technical tasks
- **Google Gemini**: For simple, quick responses and general knowledge
- **Perplexity**: For current data, research, and real-time information
- **Local AI Models**: For offline capability (Llama 3.1 and others)

### How does the smart routing work?

ENTAERA uses a sophisticated routing algorithm that:
1. Analyzes the query content and complexity
2. Identifies specific keywords and patterns
3. Evaluates the query length and structure
4. Considers context awareness requirements
5. Selects the most appropriate provider based on these factors

For example:
- Financial data and current events → Perplexity
- Coding and technical queries → Azure OpenAI
- Simple questions → Google Gemini

### What are the system requirements?

- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 10GB free space
- **Network**: Internet connection for API providers
- **Optional**: GPU for local AI acceleration

### Can ENTAERA work offline?

Yes, ENTAERA supports offline operation through local AI models. While you won't have access to the latest data (Perplexity) or Azure/Gemini capabilities, the system can run using local Llama models for basic functionality.

To use offline mode:
```bash
# Install local model dependencies
pip install -r requirements-local-models.txt

# Download models
python setup_models.py

# Run local AI chat
python final_ai_chat.py
```

## Usage Questions

### How do I get started with ENTAERA?

1. Clone the repository
2. Install dependencies
3. Configure API keys in `.env.development`
4. Run the application:
   ```bash
   python entaera_enhanced_chat.py
   ```

For detailed instructions, see the [Quickstart Guide](./docs/ENTAERA_QUICKSTART_GUIDE.md).

### How do I configure API keys?

1. Copy the example configuration file:
   ```bash
   cp .env.development.example .env.development
   ```

2. Edit the file with your API keys:
   ```
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   GEMINI_API_KEY=your_key_here
   PERPLEXITY_API_KEY=your_key_here
   ```

3. Test the configuration:
   ```bash
   python test_api_keys.py
   ```

### Can I force a specific AI provider?

Yes, you can bypass the smart routing by prefixing your query with the provider name:

- `azure:` - Force Azure OpenAI
- `gemini:` - Force Google Gemini
- `perplexity:` - Force Perplexity API

Example:
```
azure: Write a Python function to calculate prime numbers
perplexity: What are the latest developments in AI?
gemini: What is the capital of France?
```

### How do I integrate ENTAERA into my own application?

You can integrate ENTAERA by importing its components:

```python
from entaera.utils.api_router import SmartAPIRouter
from entaera.core.conversation import ConversationManager

# Initialize components
router = SmartAPIRouter()
conv_manager = ConversationManager()

# Create conversation
conversation = conv_manager.create_conversation("My Application")

# Get response with automatic routing
response, error = await router.get_response(
    prompt="Your query here",
    context={"conversation": conversation}
)

# Use the response in your application
if not error:
    print(response)
else:
    print(f"Error: {error}")
```

## Deployment Questions

### How do I deploy ENTAERA in production?

For production deployment, we recommend using Docker:

```bash
# Copy production config template
cp .env.production.example .env

# Edit with production API keys
nano .env

# Start production stack
docker-compose -f docker-compose.prod.yml up -d
```

For detailed deployment instructions, see the [Deployment Guide](./docs/ENTAERA_DEPLOYMENT_GUIDE.md).

### How does ENTAERA handle API rate limits?

ENTAERA implements several strategies for rate limit management:

1. **Token limiting**: Azure OpenAI configured for 3,000 tokens/minute
2. **Provider rotation**: Distributes load across providers
3. **Backoff strategy**: Implements exponential backoff on rate limit errors
4. **Usage tracking**: Monitors API usage to prevent limits

### Is ENTAERA scalable?

Yes, ENTAERA is designed for scalability:

- **Horizontal scaling**: Run multiple instances behind a load balancer
- **Container orchestration**: Deploy with Kubernetes for auto-scaling
- **Provider distribution**: Load is distributed across multiple AI providers
- **Resource optimization**: Efficient token usage and caching

### How do I monitor ENTAERA in production?

ENTAERA supports comprehensive monitoring:

1. **Health endpoints**: Check system health via API
2. **Prometheus metrics**: Track API calls, response times, error rates
3. **Grafana dashboards**: Visualize performance metrics
4. **Structured logging**: JSON logs for easy parsing and analysis

## Troubleshooting

### API keys aren't working

1. Check that you've copied the keys correctly without extra spaces
2. Verify API key validity in the respective provider portals
3. Check for proper environment loading in your application
4. Run `python test_api_keys.py` to validate all keys

### Smart routing isn't selecting the expected provider

The routing algorithm considers multiple factors. To troubleshoot:

1. Use provider prefixes to force specific providers
2. Check the query patterns that trigger each provider
3. Review the smart routing logic in `entaera_enhanced_chat.py`
4. Add more specific keywords to your query

### How do I fix "Model not found" errors?

For Azure OpenAI:
1. Verify your model deployment in Azure portal
2. Check that `AZURE_DEPLOYMENT_NAME` matches your deployment
3. Ensure the API version is compatible with your deployment

For other providers:
1. Check that the model name in the request matches available models
2. Update to the latest version of ENTAERA for current model names

### The system runs out of memory with local models

Local AI models can be memory-intensive. To resolve:

1. Use a smaller model variant (e.g., Llama 3.1 8B instead of 70B)
2. Increase swap space on your system
3. Use a quantized model version for lower memory usage
4. Upgrade your system memory to 16GB+ for larger models

## Cost and Performance

### How much does it cost to run ENTAERA?

Cost depends on your API usage, but ENTAERA is designed for cost efficiency:

- Azure OpenAI: ~$0.002 per 1K tokens with rate limiting
- Google Gemini: ~$0.001 per 1K tokens for simple queries
- Perplexity: ~$0.003 per 1K tokens for current data

With smart routing and token limiting, typical monthly costs are under $10 for regular usage.

### What response times can I expect?

Typical response times by provider:
- Azure OpenAI: < 2 seconds
- Google Gemini: < 1 second
- Perplexity: 2-3 seconds
- Local AI: 3-5 seconds (depends on hardware)

### How accurate is ENTAERA compared to using a single provider?

ENTAERA often achieves higher accuracy than any single provider through:
- Using Perplexity for current data (more up-to-date than other models)
- Using Azure OpenAI for complex reasoning tasks
- Automatic error detection and correction
- Provider-specific optimization for different query types

### How does ENTAERA handle rate limits?

ENTAERA manages rate limits through:
1. Token quota management (e.g., 3,000 tokens/minute for Azure)
2. Response caching for frequent queries
3. Smart routing to distribute load across providers
4. Automatic fallback if a provider rate limit is reached

## Development and Contribution

### How can I contribute to ENTAERA?

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details on:
- Code standards and style
- Pull request process
- Development workflow
- Testing requirements

### Where can I report issues or request features?

- **Issues**: [GitHub Issues](https://github.com/your-username/ENTAERA-Kata/issues)
- **Feature Requests**: Also use GitHub Issues with the "enhancement" label
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ENTAERA-Kata/discussions)

### Is there a development roadmap?

Yes, upcoming features include:
- Web interface development
- Additional AI provider integration
- Advanced cost analytics
- Usage monitoring dashboard
- API usage optimization algorithms

### Where can I find more documentation?

Comprehensive documentation is available in the `docs/` directory:
- [Comprehensive Documentation](./docs/ENTAERA_COMPREHENSIVE_DOCUMENTATION.md)
- [API Reference](./docs/ENTAERA_API_REFERENCE.md)
- [Architecture Guide](./docs/ENTAERA_ARCHITECTURE_GUIDE.md)
- [Deployment Guide](./docs/ENTAERA_DEPLOYMENT_GUIDE.md)