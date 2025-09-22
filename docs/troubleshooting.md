# 🔍 Troubleshooting Guide

This comprehensive troubleshooting guide helps you resolve common issues when working with ENTAERA-Kata. Issues are organized by category for quick navigation.

## 🎯 Quick Issue Navigator

| Category | Common Issues |
|----------|---------------|
| [🚀 Installation](#-installation-issues) | Setup, dependencies, environment |
| [🔑 Authentication](#-authentication-issues) | API keys, provider access |
| [🐳 Docker](#-docker-issues) | Container, compose, networking |
| [🧪 Testing](#-testing-issues) | Test failures, coverage, performance |
| [📊 Performance](#-performance-issues) | Memory, CPU, response times |
| [🌐 API](#-api-issues) | Endpoints, requests, responses |
| [🔧 Configuration](#-configuration-issues) | Settings, environment variables |

---

## 🚀 Installation Issues

### Issue: "Python version not supported"

**Symptoms:**
```bash
RuntimeError: Python 3.11 or higher is required
```

**Solutions:**
```bash
# Check current Python version
python --version

# Install Python 3.11+ (Ubuntu/Debian)
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv python3.11-pip

# Install Python 3.11+ (macOS with Homebrew)
brew install python@3.11

# Install Python 3.11+ (Windows)
# Download from https://www.python.org/downloads/

# Use pyenv for version management
curl https://pyenv.run | bash
pyenv install 3.11.5
pyenv global 3.11.5
```

### Issue: "Module not found" or Import errors

**Symptoms:**
```bash
ModuleNotFoundError: No module named 'entaera'
ImportError: cannot import name 'ApplicationSettings'
```

**Solutions:**
```bash
# Ensure you're in the correct directory
pwd
# Should show: /path/to/ENTAERA-Kata

# Set PYTHONPATH explicitly
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Windows PowerShell:
$env:PYTHONPATH += ";$(Get-Location)\src"

# Install in development mode
pip install -e .

# Verify virtual environment is activated
which python  # Should show .venv/bin/python

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: "Poetry not found" or Poetry installation issues

**Symptoms:**
```bash
poetry: command not found
PoetryInstallationError: Poetry installation failed
```

**Solutions:**
```bash
# Install Poetry (official installer)
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Alternative: Install with pip
pip install poetry

# Verify installation
poetry --version

# Configure Poetry (optional)
poetry config virtualenvs.in-project true
```

---

## 🔑 Authentication Issues

### Issue: OpenAI API authentication failed

**Symptoms:**
```bash
AuthenticationError: Incorrect API key provided
RateLimitError: You exceeded your current quota
```

**Solutions:**
```bash
# Verify API key format
echo $OPENAI_API_KEY
# Should start with: sk-...

# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check your OpenAI account
# Visit: https://platform.openai.com/account/api-keys

# Update environment file
nano .env.development
# Add: OPENAI_API_KEY=sk-your-actual-key-here

# Restart application
docker-compose restart
```

### Issue: Azure OpenAI connection problems

**Symptoms:**
```bash
AzureOpenAIError: Invalid endpoint
AuthenticationError: API key invalid for this resource
```

**Solutions:**
```bash
# Verify Azure configuration
echo $AZURE_OPENAI_ENDPOINT
echo $AZURE_OPENAI_API_KEY

# Test Azure endpoint
curl "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-02-15-preview" \
  -H "api-key: $AZURE_OPENAI_API_KEY"

# Check Azure portal
# Ensure deployment exists and API key is correct

# Common endpoint format
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
```

### Issue: Google Vertex AI authentication

**Symptoms:**
```bash
GoogleAuthError: Could not automatically determine credentials
PermissionDenied: The caller does not have permission
```

**Solutions:**
```bash
# Set up Google Cloud credentials
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Verify project ID
gcloud config get-value project

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Test access
gcloud ai models list --region=us-central1
```

---

## 🐳 Docker Issues

### Issue: "Port already in use"

**Symptoms:**
```bash
Error: bind: address already in use
Cannot start service app: port is already allocated
```

**Solutions:**
```bash
# Find process using port 8000
lsof -i :8000
# or on Windows:
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>
# or on Windows:
taskkill /PID <PID> /F

# Use different port
docker-compose up -p 8001:8000

# Stop existing Docker services
docker-compose down
docker system prune -f
```

### Issue: Docker build failures

**Symptoms:**
```bash
BuildKit build failed
Error response from daemon: dockerfile parse error
```

**Solutions:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build --dry-run .

# Update Docker and Docker Compose
sudo apt update && sudo apt install docker-ce docker-compose-plugin

# Check Docker daemon
sudo systemctl status docker
sudo systemctl start docker
```

### Issue: Container memory issues

**Symptoms:**
```bash
Container killed (OOMKilled)
MemoryError: Unable to allocate memory
```

**Solutions:**
```bash
# Check Docker memory limits
docker stats

# Increase Docker memory (Docker Desktop)
# Settings > Resources > Advanced > Memory

# Add memory limits to docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G

# Monitor memory usage
docker-compose exec app top
```

---

## 🧪 Testing Issues

### Issue: Test failures with "Import errors"

**Symptoms:**
```bash
pytest: ImportError: No module named 'entaera'
ModuleNotFoundError during test discovery
```

**Solutions:**
```bash
# Install in development mode
pip install -e .

# Set PYTHONPATH for tests
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# Run tests with explicit path
python -m pytest tests/

# Use pytest configuration
# Create pytest.ini with:
[tool:pytest]
testpaths = tests
pythonpath = src
```

### Issue: Property-based test failures

**Symptoms:**
```bash
Hypothesis found a counterexample
hypothesis.errors.Flaky: Test was flaky
```

**Solutions:**
```bash
# Run with more examples
pytest --hypothesis-max-examples=1000

# Use deterministic testing
pytest --hypothesis-derandomize

# Fix flaky tests by adding assumptions
from hypothesis import assume
@given(st.text())
def test_function(text):
    assume(len(text) > 0)  # Add constraints
```

### Issue: Test coverage below threshold

**Symptoms:**
```bash
FAIL Required test coverage of 85% not reached. Total coverage: 72%
```

**Solutions:**
```bash
# Generate coverage report
pytest --cov=entaera --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html

# Add tests for uncovered lines
# Focus on:
# - Error handling paths
# - Edge cases
# - Configuration variations

# Exclude non-testable files in .coveragerc
[run]
omit = 
    */tests/*
    */migrations/*
    */venv/*
```

---

## 📊 Performance Issues

### Issue: Slow API responses

**Symptoms:**
```bash
TimeoutError: Request timeout after 30 seconds
High response times in logs
```

**Solutions:**
```bash
# Check AI provider response times
curl -w "@curl-format.txt" http://localhost:8000/api/chat

# Add caching
# In .env:
REDIS_URL=redis://localhost:6379/0
ENABLE_CACHING=true

# Optimize prompt size
# Reduce context length
# Use streaming responses

# Monitor with APM
# Add New Relic, DataDog, or similar

# Profile the application
python -m cProfile -o profile.stats your_script.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Issue: High memory usage

**Symptoms:**
```bash
MemoryError: Unable to allocate memory
Process killed by OS (OOM)
```

**Solutions:**
```bash
# Monitor memory usage
docker stats
htop
free -h

# Use memory profiling
pip install memory-profiler
python -m memory_profiler your_script.py

# Optimize code
# - Use generators instead of lists
# - Clear large variables with del
# - Process data in chunks

# Adjust Docker limits
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 4G
```

### Issue: Database connection pool exhaustion

**Symptoms:**
```bash
PoolTimeoutError: QueuePool limit of size 5 overflow 10 reached
Connection pool is exhausted
```

**Solutions:**
```bash
# Increase pool size in database URL
DATABASE_URL=postgresql://user:pass@host:5432/db?pool_size=20&max_overflow=30

# Monitor connections
SELECT count(*) FROM pg_stat_activity;

# Add connection monitoring
# In application:
@app.middleware("http")
async def db_session_middleware(request, call_next):
    # Log connection pool status
    response = await call_next(request)
    return response
```

---

## 🌐 API Issues

### Issue: CORS errors in browser

**Symptoms:**
```bash
CORS policy: No 'Access-Control-Allow-Origin' header
Blocked by CORS policy
```

**Solutions:**
```bash
# Update CORS settings in .env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS=true

# Check FastAPI CORS middleware
# In main.py:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test CORS with curl
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS http://localhost:8000/api/chat
```

### Issue: Request validation errors

**Symptoms:**
```bash
HTTP 422 Unprocessable Entity
ValidationError: field required
```

**Solutions:**
```bash
# Check API documentation
curl http://localhost:8000/docs

# Validate request format
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "model": "gpt-3.5-turbo"}'

# Review Pydantic models
# Ensure required fields are provided
# Check data types match

# Add request logging
import logging
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response
```

---

## 🔧 Configuration Issues

### Issue: Environment variables not loaded

**Symptoms:**
```bash
KeyError: 'OPENAI_API_KEY'
Environment variable not found
```

**Solutions:**
```bash
# Verify .env file exists and is named correctly
ls -la .env*

# Check file permissions
chmod 644 .env.development

# Load environment manually
source .env.development  # Linux/macOS
# or use python-dotenv

# Verify variables are set
env | grep OPENAI_API_KEY
echo $OPENAI_API_KEY

# In Python:
import os
from dotenv import load_dotenv
load_dotenv('.env.development')
print(os.getenv('OPENAI_API_KEY'))
```

### Issue: Configuration validation errors

**Symptoms:**
```bash
ValidationError: Invalid configuration
pydantic.error_wrappers.ValidationError
```

**Solutions:**
```bash
# Check configuration schema
python -c "from entaera.core.config import ApplicationSettings; print(ApplicationSettings.schema_json(indent=2))"

# Validate configuration
python validate_implementation.py

# Common issues:
# - SECRET_KEY too short (minimum 32 characters)
# - Invalid URL formats
# - Missing required fields

# Use configuration validation
from entaera.core.config import ApplicationSettings
try:
    config = ApplicationSettings()
    print("Configuration valid")
except Exception as e:
    print(f"Configuration error: {e}")
```

---

## 🆘 Getting Additional Help

### 📚 Documentation Resources
- **[Installation Guide](installation.md)** - Setup instructions
- **[API Reference](api-reference.md)** - Endpoint documentation
- **[Contributing Guide](contributing.md)** - Development guidelines

### 🔍 Debugging Tools
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Use Python debugger
python -m pdb your_script.py

# Docker container debugging
docker-compose exec app bash
docker logs container_name

# Network debugging
docker network ls
docker network inspect bridge
```

### 🐛 Reporting Issues
If your issue isn't covered here:

1. **Search existing issues**: [GitHub Issues](https://github.com/your-username/ENTAERA-Kata/issues)
2. **Create a detailed bug report** with:
   - Operating system and version
   - Python version
   - Docker version (if applicable)
   - Full error message and stack trace
   - Steps to reproduce
   - Expected vs actual behavior

3. **Include environment info**:
```bash
# System information
python --version
docker --version
poetry --version

# Application logs
docker-compose logs app

# Configuration (remove sensitive data)
cat .env.development | grep -v "API_KEY"
```

### 💬 Community Support
- **Discord**: [ENTAERA Community](https://discord.gg/entaera)
- **GitHub Discussions**: [Project Discussions](https://github.com/your-username/ENTAERA-Kata/discussions)
- **Stack Overflow**: Tag your questions with `entaera`

---

**🎯 Still having issues? Don't hesitate to reach out to our community - we're here to help!**