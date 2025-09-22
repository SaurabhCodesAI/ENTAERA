# 📚 Code Examples

This directory contains comprehensive examples demonstrating all major features of ENTAERA-Kata. Each example is designed to be educational, showing best practices and real-world usage patterns.

## 🎯 Example Categories

| Category | Examples | Difficulty | Description |
|----------|----------|------------|-------------|
| [🚀 Basic Usage](#-basic-usage) | Quick start, configuration | Beginner | Getting started with the framework |
| [🤖 AI Providers](#-ai-providers) | Multi-provider setup | Intermediate | Working with different AI models |
| [🔬 Research Engine](#-research-engine) | Automated research | Advanced | Scientific research automation |
| [🛠️ Custom Components](#️-custom-components) | Extensions, plugins | Advanced | Building custom functionality |
| [🐳 Deployment](#-deployment) | Docker, Kubernetes | Intermediate | Production deployment patterns |

## 📋 Prerequisites

Before running these examples, ensure you have:

1. **ENTAERA-Kata installed** (see [Installation Guide](../docs/installation.md))
2. **API keys configured** for at least one AI provider
3. **Python 3.11+** with required dependencies
4. **Environment variables set** (copy from `.env.development.example`)

## 🏃‍♂️ Quick Start

```bash
# Clone and set up the project
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata

# Install dependencies
poetry install

# Set up environment
cp .env.development.example .env.development
# Edit .env.development with your API keys

# Run basic example
cd examples
python basic_usage/hello_world.py
```

---

## 🚀 Basic Usage

### Hello World
**File**: `basic_usage/hello_world.py`
**Concepts**: Basic setup, simple queries
**Time**: 5 minutes

### Configuration Management
**File**: `basic_usage/configuration.py`
**Concepts**: Environment variables, settings validation
**Time**: 10 minutes

### Logging and Monitoring
**File**: `basic_usage/logging_example.py`
**Concepts**: Structured logging, request tracking
**Time**: 10 minutes

---

## 🤖 AI Providers

### Multi-Provider Setup
**File**: `ai_providers/multi_provider.py`
**Concepts**: Provider abstraction, failover
**Time**: 15 minutes

### Model Comparison
**File**: `ai_providers/model_comparison.py`
**Concepts**: Benchmarking, performance analysis
**Time**: 20 minutes

### Cost Optimization
**File**: `ai_providers/cost_optimization.py`
**Concepts**: Provider selection, budget management
**Time**: 15 minutes

---

## 🔬 Research Engine

### Automated Literature Review
**File**: `research/literature_review.py`
**Concepts**: Research methodology, data collection
**Time**: 30 minutes

### Hypothesis Generation
**File**: `research/hypothesis_generation.py`
**Concepts**: Scientific reasoning, idea generation
**Time**: 25 minutes

### Data Analysis Pipeline
**File**: `research/data_analysis.py`
**Concepts**: Statistical analysis, visualization
**Time**: 40 minutes

---

## 🛠️ Custom Components

### Custom AI Provider
**File**: `custom_components/custom_provider.py`
**Concepts**: Interface implementation, plugin architecture
**Time**: 45 minutes

### Research Methodology Extension
**File**: `custom_components/custom_methodology.py`
**Concepts**: Extending research capabilities
**Time**: 50 minutes

### Custom Logging Handler
**File**: `custom_components/custom_logger.py`
**Concepts**: Logging customization, integrations
**Time**: 30 minutes

---

## 🐳 Deployment

### Docker Development Setup
**File**: `deployment/docker_dev.py`
**Concepts**: Containerization, development workflow
**Time**: 20 minutes

### Production Deployment
**File**: `deployment/production.py`
**Concepts**: Production configuration, monitoring
**Time**: 60 minutes

### Kubernetes Scaling
**File**: `deployment/kubernetes.py`
**Concepts**: Container orchestration, scaling
**Time**: 90 minutes

---

## 🎓 Learning Path

### For Beginners
1. Start with [Hello World](basic_usage/hello_world.py)
2. Learn [Configuration](basic_usage/configuration.py)
3. Explore [Basic AI Provider Usage](ai_providers/simple_query.py)
4. Try [Simple Research](research/basic_research.py)

### For Intermediate Users
1. Study [Multi-Provider Setup](ai_providers/multi_provider.py)
2. Implement [Custom Components](custom_components/)
3. Build [Research Pipelines](research/research_pipeline.py)
4. Deploy with [Docker](deployment/docker_dev.py)

### For Advanced Users
1. Create [Custom Methodologies](custom_components/custom_methodology.py)
2. Optimize [Performance](performance/optimization.py)
3. Build [Production Systems](deployment/production.py)
4. Contribute [New Features](../CONTRIBUTING.md)

---

## 🧪 Running Examples

### Individual Examples
```bash
# Run a specific example
cd examples
python basic_usage/hello_world.py

# With custom environment
ENV_FILE=../my-config.env python ai_providers/multi_provider.py
```

### Interactive Jupyter Notebooks
```bash
# Start Jupyter
jupyter lab

# Open notebook examples
# examples/notebooks/interactive_research.ipynb
```

### Example Test Suite
```bash
# Test all examples
pytest examples/tests/

# Test specific category
pytest examples/tests/test_basic_usage.py
```

---

## 🔍 Example Structure

Each example follows this structure:

```python
#!/usr/bin/env python3
"""
Example: [Name]
Description: [What this example demonstrates]
Concepts: [Key concepts covered]
Prerequisites: [What you need to know]
Time: [Estimated completion time]
"""

import asyncio
import logging
from pathlib import Path

# Setup logging for the example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main example function."""
    logger.info("Starting example: [Name]")
    
    # Example implementation
    # Step-by-step with comments
    
    logger.info("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 Performance Benchmarks

Examples include performance benchmarks to help you understand:

- **Response times** for different providers
- **Memory usage** patterns
- **Throughput** capabilities
- **Cost analysis** per operation

```python
# Example benchmark output
"""
Provider Comparison Benchmark
=============================
OpenAI GPT-4:        1.2s avg response time, $0.03/query
Azure OpenAI:        0.8s avg response time, $0.025/query
Anthropic Claude:    1.5s avg response time, $0.035/query
Google Vertex AI:    0.9s avg response time, $0.02/query

Recommendation: Use Azure OpenAI for best balance of speed and cost
"""
```

---

## 🆘 Getting Help with Examples

### Common Issues

**"Module not found" errors**
```bash
# Ensure you're in the right directory
cd ENTAERA-Kata

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run with poetry
poetry run python examples/basic_usage/hello_world.py
```

**"API key not found" errors**
```bash
# Check environment file
cat .env.development | grep API_KEY

# Test API key
python -c "import os; print('OPENAI_API_KEY' in os.environ)"
```

### Documentation
- **[Troubleshooting Guide](../docs/troubleshooting.md)** - Common issues and solutions
- **[API Reference](../docs/api-reference.md)** - Detailed API documentation
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute examples

### Community
- **GitHub Issues**: Report bugs or request new examples
- **Discord**: Get help from the community
- **Stack Overflow**: Tag questions with `entaera`

---

**🎯 Ready to explore? Pick an example that matches your skill level and start building with ENTAERA-Kata!**