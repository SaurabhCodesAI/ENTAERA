# 📦 Installation Guide

This guide provides step-by-step instructions for installing ENTAERA-Kata in different environments. Choose the method that best fits your needs and experience level.

## 🎯 Quick Reference

| Method | Difficulty | Time | Best For |
|--------|------------|------|----------|
| [Docker](#-docker-installation-recommended) | Beginner | 5 min | Quick start, isolated environment |
| [Local Development](#-local-development-installation) | Intermediate | 10 min | Development, customization |
| [Production Deployment](#-production-deployment) | Advanced | 30 min | Live deployment, scaling |

---

## 🐳 Docker Installation (Recommended)

**Best for:** Beginners, quick testing, isolated environments

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata
```

### Step 2: Configure Environment
```bash
# Copy the development environment template
cp .env.development.example .env.development

# Edit the environment file with your API keys
# Windows:
notepad .env.development
# macOS/Linux:
nano .env.development
```

### Step 3: Add Your API Keys
Edit `.env.development` and add your API credentials:

```bash
# Required: Add at least one AI provider
OPENAI_API_KEY=sk-your-openai-key-here
# OR
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key-here
# OR
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
```

### Step 4: Start the Application
```bash
# Build and start all services
docker-compose up --build

# Or run in the background
docker-compose up --build -d
```

### Step 5: Verify Installation
```bash
# Check if the application is running
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "2025-09-22T08:00:00Z"}
```

### Step 6: Access the Application
- **API Documentation**: http://localhost:8000/docs
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### 🛑 Troubleshooting Docker Installation

**Problem: "Port 8000 already in use"**
```bash
# Stop existing services
docker-compose down

# Or use a different port
docker-compose up --build -p 8001:8000
```

**Problem: "Permission denied" on Windows**
```bash
# Run PowerShell as Administrator
# Or add your user to the docker-users group
```

**Problem: "Build failed"**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

---

## 💻 Local Development Installation

**Best for:** Developers, customization, learning the codebase

### Prerequisites
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Poetry** (Package manager) - Optional but recommended

### Step 1: Clone and Navigate
```bash
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata
```

### Step 2: Choose Your Package Manager

#### Option A: Using Poetry (Recommended)
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Option B: Using pip and venv
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -e .
```

### Step 3: Environment Configuration
```bash
# Copy environment template
cp .env.development.example .env.development

# Edit with your preferred editor
code .env.development  # VS Code
# or
nano .env.development  # Terminal editor
```

### Step 4: Add Required Configuration
Edit `.env.development` with your settings:

```bash
# Application settings
ENVIRONMENT=development
SECRET_KEY=your-development-secret-key-at-least-32-characters
LOG_LEVEL=DEBUG

# AI Provider credentials (add at least one)
OPENAI_API_KEY=sk-your-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
GOOGLE_CLOUD_PROJECT=your-gcp-project
ANTHROPIC_API_KEY=your-anthropic-key
```

### Step 5: Verify Installation
```bash
# Set Python path (if needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Windows PowerShell:
$env:PYTHONPATH += ";$(Get-Location)\src"

# Run validation script
python validate_implementation.py
```

### Step 6: Start the Application
```bash
# Using Poetry
poetry run python -m entaera.main

# Using pip
python -m entaera.main

# Or start the web server
uvicorn entaera.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=entaera --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

### 🛑 Troubleshooting Local Installation

**Problem: "Python version not supported"**
```bash
# Check Python version
python --version

# Install Python 3.11+ from python.org
# Or use pyenv for version management
```

**Problem: "Import errors"**
```bash
# Ensure you're in the virtual environment
which python  # Should show .venv/bin/python

# Set PYTHONPATH explicitly
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
```

**Problem: "Poetry not found"**
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or install with pip
pip install poetry
```

---

## 🚀 Production Deployment

**Best for:** Live applications, scaling, monitoring

### Prerequisites
- **Linux Server** (Ubuntu 20.04+ recommended)
- **Docker & Docker Compose**
- **Reverse Proxy** (Nginx recommended)
- **SSL Certificate** (Let's Encrypt or purchased)
- **Domain Name** (optional but recommended)

### Step 1: Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

### Step 2: Application Deployment
```bash
# Clone repository
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata

# Create production environment
cp .env.production.example .env.production

# Edit production configuration
nano .env.production
```

### Step 3: Production Configuration
Edit `.env.production` with secure values:

```bash
# Application (use strong, unique values)
ENVIRONMENT=production
SECRET_KEY=generate-a-secure-random-key-for-production
LOG_LEVEL=INFO

# Database (use strong passwords)
DATABASE_URL=postgresql://produser:strongpassword@postgres:5432/entaera_prod

# AI Providers (use production keys)
OPENAI_API_KEY=your-production-openai-key
AZURE_OPENAI_ENDPOINT=your-production-azure-endpoint

# Security
CORS_ORIGINS=["https://yourdomain.com"]
SSL_CERT_PATH=/app/config/ssl/cert.pem
SSL_KEY_PATH=/app/config/ssl/key.pem
```

### Step 4: SSL Setup
```bash
# Create SSL directory
mkdir -p config/ssl

# Using Let's Encrypt (recommended)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem config/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem config/ssl/key.pem
sudo chown $USER:$USER config/ssl/*
```

### Step 5: Deploy Application
```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose -f docker-compose.prod.yml ps
curl https://yourdomain.com/health
```

### Step 6: Set Up Monitoring
```bash
# Access monitoring dashboards
# Prometheus: http://yourdomain.com:9090
# Grafana: http://yourdomain.com:3000

# Default Grafana credentials
# Username: admin
# Password: (set in secrets/grafana_password.txt)
```

### 🔒 Security Hardening
```bash
# Set up firewall
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Set up fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban

# Regular security updates
echo '0 2 * * * apt update && apt upgrade -y' | sudo crontab -
```

### 🛑 Troubleshooting Production

**Problem: "SSL certificate issues"**
```bash
# Check certificate validity
openssl x509 -in config/ssl/cert.pem -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew
```

**Problem: "Database connection failed"**
```bash
# Check database status
docker-compose -f docker-compose.prod.yml logs postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U produser -d entaera_prod
```

**Problem: "High memory usage"**
```bash
# Check resource usage
docker stats

# Adjust resource limits in docker-compose.prod.yml
# Restart services
docker-compose -f docker-compose.prod.yml restart
```

---

## 🎯 Next Steps

After successful installation:

1. **📚 Read the [API Documentation](api-reference.md)**
2. **🔧 Follow the [Contributing Guide](contributing.md)**
3. **🧪 Run the [Code Examples](examples/)**
4. **📊 Set up [Monitoring](monitoring.md)**
5. **🔍 Review [Troubleshooting](troubleshooting.md)**

## 🆘 Getting Help

If you encounter issues not covered in this guide:

- **Check the [Troubleshooting Guide](troubleshooting.md)**
- **Search existing [GitHub Issues](https://github.com/your-username/ENTAERA-Kata/issues)**
- **Join our [Discord Community](https://discord.gg/entaera)**
- **Email support**: support@entaera.dev

---

**✅ Installation complete! Your ENTAERA-Kata is ready to use.**