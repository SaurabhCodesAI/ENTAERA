# 🚀 ENTAERA Quickstart Guide

This guide provides a rapid introduction to getting started with the ENTAERA framework, an intelligent multi-API routing system for AI interactions.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Installation](#quick-installation)
3. [API Configuration](#api-configuration)
4. [Running ENTAERA](#running-entaera)
5. [Usage Tips](#usage-tips)
6. [Testing & Validation](#testing--validation)
7. [Cost Management](#cost-management)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

## 📋 Prerequisites

- Python 3.11+
- API keys for:
  - Azure OpenAI
  - Google Gemini
  - Perplexity
- 4GB RAM minimum (8GB recommended)
- Internet connection for API services

## ⚡ Quick Installation

### Option 1: Docker (Recommended for Beginners)

```bash
# Clone the repository
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata

# Copy environment configuration
cp .env.development.example .env.development

# Edit your API keys in .env.development (replace with your actual API keys)
# AZURE_OPENAI_API_KEY=your_key_here
# AZURE_OPENAI_ENDPOINT=your_endpoint_here
# GEMINI_API_KEY=your_key_here
# PERPLEXITY_API_KEY=your_key_here

# Start with Docker Compose
docker-compose up --build
```

### Option 2: Direct Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Run API validation
python test_api_keys.py
```

## 🔍 API Configuration

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in Azure Portal
2. Deploy a model (recommended: `gpt-35-turbo`)
3. Get API key and endpoint from Azure Portal
4. Update `.env` file:
   ```
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2023-12-01-preview
   AZURE_DEPLOYMENT_NAME=gpt-35-turbo
   ```

### Google Gemini Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/)
2. Update `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```

### Perplexity Setup

1. Get API key from [Perplexity](https://www.perplexity.ai/)
2. Update `.env` file:
   ```
   PERPLEXITY_API_KEY=your_key_here
   ```

## 🚀 Running ENTAERA

### Enhanced Chat (Recommended)

```bash
python entaera_enhanced_chat.py
```

Features:
- Multi-API intelligent routing
- Context-aware responses
- Error detection and correction
- Personal recognition

### Simple Chat (Basic)

```bash
python entaera_simple_chat.py
```

Features:
- Basic multi-API routing
- Error handling
- Manual API selection

### Interactive Chat

```bash
python entaera_interactive_chat.py
```

Features:
- Interactive mode with step-by-step explanations
- Educational insights into routing decisions
- Detailed API response information

## 💡 Usage Tips

### Force Specific APIs

Prefix your queries to force a specific provider:

```
azure: Write a python function to calculate prime numbers
gemini: What is the capital of France?
perplexity: What are the latest developments in AI?
```

### Smart Routing Guidelines

ENTAERA automatically routes queries based on content:

- **Financial/Current data → Perplexity**
  - "What is Elon Musk's current net worth?"
  - "What are the latest AI research papers?"
  - "When is the next SpaceX launch?"

- **Technical/Coding → Azure OpenAI**
  - "Write a Python function to sort a list"
  - "Explain how blockchain works"
  - "Help me debug this JavaScript code"

- **Simple Questions → Gemini**
  - "What's the capital of Japan?"
  - "Who wrote Romeo and Juliet?"
  - "How many continents are there?"

## 🧪 Testing & Validation

Verify your setup:

```bash
# Test Azure OpenAI connection
python azure_continuous_test.py

# Test all APIs
python test_entaera_apis.py

# Run API demonstrations
python entaera_live_api_demo.py
```

## 📊 Cost Management

ENTAERA optimizes costs through:

- Rate limiting (3,000 tokens/minute for Azure)
- Smart routing to cheaper providers for simple tasks
- Usage tracking and cost estimation

## 🔧 Troubleshooting

### Common Issues

1. **API connection failures**:
   - Check internet connection
   - Verify API keys in `.env`
   - Test with `test_api_keys.py`

2. **Missing dependencies**:
   - Run `pip install -r requirements.txt`
   - Check for Python version compatibility (3.11+)

3. **Docker issues**:
   - Try `docker-compose build --no-cache`
   - Check Docker logs: `docker-compose logs`

### Support Resources

- **Documentation**: Full documentation in `docs/`
- **Examples**: Example code in `examples/`
- **GitHub**: Report issues on project GitHub page

## 🚀 Next Steps

1. Explore the full documentation: `docs/ENTAERA_COMPREHENSIVE_DOCUMENTATION.md`
2. Try different chat examples in `examples/`
3. Run API tests to understand provider capabilities
4. Customize routing logic in `src/entaera/utils/api_router.py`
5. Follow the 30-kata journey to master AI agent development

---

Happy exploring with ENTAERA! 🚀