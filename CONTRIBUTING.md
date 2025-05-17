# 🤝 Contributing Guide

Welcome to ENTAERA-Kata! We're excited that you want to contribute to this kata-driven AI research framework. This guide will help you get started with contributing code, documentation, tests, and more.

## 🎯 Ways to Contribute

| Contribution Type | Difficulty | Impact | Time Commitment |
|-------------------|------------|--------|-----------------|
| [🐛 Bug Reports](#-reporting-bugs) | Beginner | High | 10-30 minutes |
| [📚 Documentation](#-improving-documentation) | Beginner | High | 30 minutes - 2 hours |
| [🧪 Writing Tests](#-writing-tests) | Intermediate | High | 1-4 hours |
| [✨ New Features](#-implementing-features) | Intermediate-Advanced | Very High | 4-20 hours |
| [🥋 Creating Kata](#-creating-new-kata) | Advanced | Very High | 8-40 hours |
| [🔧 Code Review](#-code-review) | Intermediate | Medium | 30 minutes - 2 hours |

---

## 🚀 Quick Start for Contributors

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/ENTAERA-Kata.git
cd ENTAERA-Kata

# Add upstream remote
git remote add upstream https://github.com/original-owner/ENTAERA-Kata.git
```

### 2. Set Up Development Environment
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --with dev,test

# Activate virtual environment
poetry shell

# Set up pre-commit hooks
pre-commit install
```

### 3. Create Feature Branch
```bash
# Always start from main branch
git checkout main
git pull upstream main

# Create feature branch (use descriptive names)
git checkout -b feature/add-anthropic-provider
git checkout -b fix/memory-leak-in-logger
git checkout -b docs/improve-installation-guide
git checkout -b kata/day-15-hypothesis-generation
```

### 4. Make Changes and Test
```bash
# Make your changes
# Follow the coding standards below

# Run tests locally
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Check code quality
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/

# Run validation script
python validate_implementation.py
```

### 5. Commit and Push
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add Anthropic Claude provider support

- Implement AnthropicProvider class
- Add configuration for API key and model selection
- Include comprehensive unit tests
- Update documentation with usage examples

Closes #123"

# Push to your fork
git push origin feature/add-anthropic-provider
```

### 6. Create Pull Request
1. Go to GitHub and create a Pull Request
2. Use the [PR template](#pull-request-template)
3. Request review from maintainers
4. Address feedback and make improvements

---

## 📋 Development Guidelines

### 🐍 Python Code Standards

#### Code Style
```python
# Use Black for formatting (line length: 88 characters)
# Use isort for import sorting
# Follow PEP 8 conventions

# Good example
from typing import Dict, List, Optional, Union
import logging

from pydantic import BaseModel, Field
from entaera.core.config import ApplicationSettings

logger = logging.getLogger(__name__)


class AIProvider(BaseModel):
    """Base class for AI provider implementations.
    
    Attributes:
        name: The provider name (e.g., 'openai', 'anthropic')
        api_key: The API key for authentication
        models: List of available models
        rate_limit: Maximum requests per minute
    """
    
    name: str = Field(..., description="Provider name")
    api_key: str = Field(..., description="API key")
    models: List[str] = Field(default_factory=list)
    rate_limit: int = Field(default=60, gt=0)
    
    async def generate_response(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Union[str, int]]:
        """Generate response from the AI provider.
        
        Args:
            prompt: The input prompt
            model: Model to use (optional)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dict containing response and metadata
            
        Raises:
            ProviderError: If the request fails
            RateLimitError: If rate limit is exceeded
        """
        logger.info(f"Generating response with {self.name}")
        # Implementation here
```

#### Type Hints
```python
# Always use type hints for public functions
from typing import Dict, List, Optional, Union, Any, Callable

# Good
def process_data(
    data: List[Dict[str, Any]], 
    callback: Optional[Callable[[str], bool]] = None
) -> Dict[str, Union[str, int]]:
    """Process input data with optional callback."""
    pass

# Bad
def process_data(data, callback=None):
    pass
```

#### Error Handling
```python
# Create specific exception classes
class ENTAERAError(Exception):
    """Base exception for ENTAERA."""
    pass

class ProviderError(ENTAERAError):
    """Raised when AI provider fails."""
    pass

class ConfigurationError(ENTAERAError):
    """Raised when configuration is invalid."""
    pass

# Use proper exception handling
try:
    response = await provider.generate_response(prompt)
except ProviderError as e:
    logger.error(f"Provider failed: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise ProviderError(f"Failed to generate response: {e}") from e
```

### 🧪 Testing Standards

#### Test Structure
```python
# tests/unit/test_providers.py
import pytest
from unittest.mock import AsyncMock, patch

from entaera.providers import OpenAIProvider
from entaera.core.exceptions import ProviderError


class TestOpenAIProvider:
    """Test suite for OpenAI provider."""
    
    @pytest.fixture
    def provider(self):
        """Create provider instance for testing."""
        return OpenAIProvider(
            api_key="test-key",
            models=["gpt-3.5-turbo", "gpt-4"]
        )
    
    async def test_generate_response_success(self, provider):
        """Test successful response generation."""
        with patch('openai.ChatCompletion.acreate') as mock_create:
            mock_create.return_value = {
                'choices': [{'message': {'content': 'Test response'}}]
            }
            
            result = await provider.generate_response("Test prompt")
            
            assert result['content'] == 'Test response'
            mock_create.assert_called_once()
    
    async def test_generate_response_failure(self, provider):
        """Test error handling in response generation."""
        with patch('openai.ChatCompletion.acreate') as mock_create:
            mock_create.side_effect = Exception("API Error")
            
            with pytest.raises(ProviderError):
                await provider.generate_response("Test prompt")
```

#### Property-Based Testing
```python
# Use Hypothesis for property-based testing
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=1000))
def test_text_processing_invariants(text):
    """Test text processing maintains invariants."""
    processed = normalize_text(text)
    
    # Properties that should always hold
    assert isinstance(processed, str)
    assert len(processed) <= len(text)
    assert processed.islower() or not processed.isalpha()
```

### 📚 Documentation Standards

#### Docstring Format
```python
def conduct_research(
    topic: str,
    methodology: str = "systematic_review",
    depth: str = "comprehensive"
) -> ResearchResults:
    """Conduct automated research on a given topic.
    
    This function implements a systematic approach to research automation,
    following academic methodologies to ensure comprehensive coverage.
    
    Args:
        topic: The research topic or question to investigate
        methodology: Research methodology to use. Options:
            - "systematic_review": Comprehensive literature review
            - "meta_analysis": Statistical analysis of multiple studies
            - "exploratory": Open-ended exploration
        depth: Level of detail. Options:
            - "surface": Quick overview
            - "standard": Balanced depth and breadth
            - "comprehensive": Exhaustive analysis
    
    Returns:
        ResearchResults object containing:
            - findings: List of key discoveries
            - sources: Bibliography of consulted sources
            - confidence: Confidence score (0.0-1.0)
            - methodology_notes: Details about approach used
    
    Raises:
        ResearchError: If the research process fails
        ConfigurationError: If methodology is not supported
        
    Example:
        >>> results = await conduct_research(
        ...     topic="Impact of AI on software development",
        ...     methodology="systematic_review",
        ...     depth="comprehensive"
        ... )
        >>> print(f"Found {len(results.findings)} key findings")
        Found 15 key findings
        
    Note:
        This function may take several minutes for comprehensive research.
        Consider using async context for long-running operations.
    """
```

#### README Updates
```markdown
# When adding new features, update README.md with:

## 🆕 New Feature: Anthropic Claude Support

ENTAERA now supports Anthropic's Claude models for advanced reasoning tasks.

### Quick Start
```python
from entaera.providers import AnthropicProvider

provider = AnthropicProvider(api_key="your-key")
response = await provider.generate_response(
    prompt="Analyze this research paper",
    model="claude-3-opus"
)
```

### Configuration
Add to your `.env` file:
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_DEFAULT_MODEL=claude-3-sonnet
```
```

---

## 🐛 Reporting Bugs

### Before Reporting
1. **Search existing issues** to avoid duplicates
2. **Try the latest version** to see if it's already fixed
3. **Check troubleshooting guide** for common solutions

### Bug Report Template
```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Actual Behavior**
What actually happened, including full error messages.

**Environment**
- OS: [e.g. Ubuntu 20.04, Windows 11, macOS 12]
- Python version: [e.g. 3.11.5]
- ENTAERA version: [e.g. 1.2.3]
- Docker version: [if applicable]

**Additional Context**
- Configuration files (remove sensitive data)
- Log files
- Screenshots (if applicable)
```

---

## ✨ Implementing Features

### Feature Request Process
1. **Open an issue** to discuss the feature
2. **Get approval** from maintainers
3. **Create implementation plan**
4. **Write tests first** (TDD approach)
5. **Implement the feature**
6. **Update documentation**

### Feature Implementation Template
```python
# 1. Create the feature interface
class NewFeatureInterface(Protocol):
    """Protocol for new feature implementations."""
    
    async def process(self, input_data: Any) -> Any:
        """Process input and return result."""
        ...

# 2. Implement the feature
class NewFeatureImplementation:
    """Implementation of the new feature."""
    
    def __init__(self, config: FeatureConfig):
        self.config = config
    
    async def process(self, input_data: Any) -> Any:
        """Process input and return result."""
        # Implementation here
        pass

# 3. Add configuration support
class FeatureConfig(BaseModel):
    """Configuration for the new feature."""
    
    enabled: bool = True
    option_a: str = "default"
    option_b: int = 42

# 4. Integrate with main application
# In main application initialization:
if settings.new_feature.enabled:
    feature = NewFeatureImplementation(settings.new_feature)
    app.add_feature(feature)
```

---

## 🥋 Creating New Kata

### Kata Design Principles
1. **Progressive Difficulty**: Each kata builds on previous knowledge
2. **Clear Learning Objectives**: What skills will be mastered?
3. **Practical Application**: Real-world relevance
4. **Testable Outcomes**: Objective success criteria

### Kata Template
```markdown
# Kata X.Y: [Kata Name]

## 🎯 Learning Objectives
By completing this kata, you will:
- [ ] Understand [concept A]
- [ ] Implement [skill B]
- [ ] Master [technique C]

## 📚 Prerequisites
- Completed Kata X.(Y-1)
- Understanding of [prerequisite concepts]
- Familiarity with [required tools]

## 🏗️ Implementation Steps

### Step 1: [Setup/Preparation]
[Detailed instructions]

### Step 2: [Core Implementation]
[Step-by-step guidance]

### Step 3: [Testing and Validation]
[How to verify success]

## 🧪 Success Criteria
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is complete
- [ ] Performance meets benchmarks

## 🎓 Mastery Indicators
- Can explain the concept to others
- Can extend the implementation
- Can troubleshoot common issues

## 🔗 Next Steps
- Proceed to Kata X.(Y+1): [Next Kata Name]
- Optional: [Advanced exercises]
```

---

## 🔧 Code Review

### Review Checklist

#### Functionality
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Performance is acceptable

#### Code Quality
- [ ] Follows coding standards
- [ ] Well-structured and readable
- [ ] Appropriate abstractions
- [ ] No code duplication

#### Testing
- [ ] Tests cover new functionality
- [ ] Tests are meaningful and maintainable
- [ ] Edge cases are tested
- [ ] Performance tests where needed

#### Documentation
- [ ] Code is self-documenting
- [ ] Docstrings are comprehensive
- [ ] README updated if needed
- [ ] Examples provided

### Review Comments
```markdown
# Constructive feedback examples:

✅ Good:
"Consider using a factory pattern here to reduce coupling and improve testability. 
Here's an example: [code snippet]"

❌ Avoid:
"This is wrong."

✅ Good:
"This implementation works, but we could improve performance by using async/await. 
Would you like me to help refactor this?"

❌ Avoid:
"Too slow."
```

---

## 📊 Pull Request Template

```markdown
## 📝 Description
Brief description of changes and motivation.

## 🔄 Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Property-based tests pass
- [ ] Manual testing completed

## 📚 Documentation
- [ ] Code comments added/updated
- [ ] Docstrings added/updated
- [ ] README updated
- [ ] API documentation updated

## ✅ Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## 🔗 Related Issues
Closes #123
Relates to #456
```

---

## 🏆 Recognition

### Contributor Levels

#### 🌱 **Contributor**
- First successful PR merged
- Active participation in discussions

#### 🌿 **Regular Contributor**
- 5+ PRs merged
- Helps others in issues/discussions
- Maintains code quality

#### 🌳 **Core Contributor**
- 20+ PRs merged
- Significant feature contributions
- Mentors new contributors

#### 🏛️ **Maintainer**
- Long-term commitment
- Reviews PRs regularly
- Shapes project direction

### Hall of Fame
Contributors are recognized in:
- README.md Contributors section
- Release notes
- Annual contributor reports
- Conference talks and presentations

---

## 📞 Getting Help

### Development Questions
- **GitHub Discussions**: [Project discussions](https://github.com/your-username/ENTAERA-Kata/discussions)
- **Discord**: [ENTAERA Community](https://discord.gg/entaera)
- **Email**: developers@entaera.dev

### Mentorship Program
New contributors can request mentorship for:
- First-time contributions
- Complex feature development
- Understanding the codebase
- Career guidance in AI/ML

---

**🎉 Thank you for contributing to ENTAERA-Kata! Together, we're building the future of AI research automation.**