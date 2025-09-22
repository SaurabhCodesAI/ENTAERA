# ENTAERA Deployment Guide

This guide provides comprehensive instructions for deploying the ENTAERA framework in various environments, from development to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Cloud Deployment Options](#cloud-deployment-options)
6. [Environment Configuration](#environment-configuration)
7. [Security Considerations](#security-considerations)
8. [Monitoring Setup](#monitoring-setup)
9. [Scaling Strategies](#scaling-strategies)
10. [Backup and Recovery](#backup-and-recovery)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 10GB free space
- **Network**: Internet connection for API providers

### Required API Keys

- **Azure OpenAI**: API key and endpoint
- **Google Gemini**: API key
- **Perplexity**: API key

### Optional Components

- **Docker**: For containerized deployment
- **Redis**: For caching in production
- **PostgreSQL**: For data persistence
- **Prometheus/Grafana**: For monitoring

---

## Local Development Setup

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ENTAERA-Kata.git
cd ENTAERA-Kata

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.development.example .env.development
# Edit .env.development with your API keys
```

### Setting Up API Keys

1. **Azure OpenAI**:
   - Create an Azure account if you don't have one
   - Create an Azure OpenAI resource
   - Deploy a model (e.g., gpt-35-turbo)
   - Copy API key and endpoint to `.env.development`

2. **Google Gemini**:
   - Visit Google AI Studio (https://makersuite.google.com/)
   - Create an API key
   - Copy to `.env.development`

3. **Perplexity**:
   - Sign up for Perplexity API access
   - Generate API key
   - Copy to `.env.development`

### Running Locally

```bash
# Test API connections
python test_api_keys.py

# Run basic chat
python entaera_simple_chat.py

# Run enhanced chat with all features
python entaera_enhanced_chat.py
```

### Local Development Best Practices

- Use `.env.development` for development settings
- Enable debug logging for development
- Set token limits higher for testing
- Test with multiple providers

---

## Docker Deployment

### Development with Docker

```bash
# Build and start the development container
docker-compose up --build

# Stop containers
docker-compose down
```

### Docker Configuration

The `docker-compose.yml` file includes:

```yaml
version: '3'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    env_file:
      - .env.development
    command: python entaera_api_chat_demo.py
```

### Building Custom Docker Images

```bash
# Build a custom image
docker build -t entaera:custom -f Dockerfile .

# Run custom image
docker run -it --env-file .env entaera:custom
```

### Docker Optimization

- Use multi-stage builds for smaller images
- Implement proper caching of layers
- Use specific version tags for dependencies
- Optimize Docker cache for faster builds

---

## Production Deployment

### Production Setup

```bash
# Copy production config template
cp .env.production.example .env

# Edit with production API keys
nano .env

# Start production stack
docker-compose -f docker-compose.prod.yml up -d
```

### Production Docker Compose

The `docker-compose.prod.yml` includes:

```yaml
version: '3'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
      - db
    environment:
      - ENVIRONMENT=production
      - REDIS_HOST=redis
      - DB_HOST=db

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

  db:
    image: postgres:15-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env

  prometheus:
    image: prom/prometheus:latest
    restart: always
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    restart: always
    volumes:
      - ./monitoring/grafana:/etc/grafana
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  redis_data:
  postgres_data:
  prometheus_data:
  grafana_data:
```

### Production Configuration

Key considerations for production:

- Set appropriate API rate limits
- Configure proper logging (JSON format)
- Set up monitoring and alerts
- Implement backup strategies
- Configure security settings

### Production Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check detailed component status
curl http://localhost:8000/health/detailed
```

---

## Cloud Deployment Options

### AWS Deployment

1. **Prerequisites**:
   - AWS account
   - AWS CLI configured
   - ECR repository for images

2. **Setup Steps**:
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-aws-account.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and tag image
   docker build -t entaera-prod:latest -f Dockerfile.prod .
   docker tag entaera-prod:latest your-aws-account.dkr.ecr.us-east-1.amazonaws.com/entaera:latest
   
   # Push image
   docker push your-aws-account.dkr.ecr.us-east-1.amazonaws.com/entaera:latest
   ```

3. **Deployment Options**:
   - ECS Fargate for serverless containers
   - EKS for Kubernetes deployment
   - EC2 for virtual machine deployment

### Azure Deployment

1. **Prerequisites**:
   - Azure account
   - Azure CLI configured
   - Azure Container Registry (ACR)

2. **Setup Steps**:
   ```bash
   # Login to ACR
   az acr login --name YourRegistryName
   
   # Build and tag image
   docker build -t entaera-prod:latest -f Dockerfile.prod .
   docker tag entaera-prod:latest yourregistryname.azurecr.io/entaera:latest
   
   # Push image
   docker push yourregistryname.azurecr.io/entaera:latest
   ```

3. **Deployment Options**:
   - Azure Container Instances (ACI)
   - Azure Kubernetes Service (AKS)
   - Azure App Service

### Google Cloud Platform (GCP)

1. **Prerequisites**:
   - GCP account
   - gcloud CLI configured
   - Google Container Registry (GCR) or Artifact Registry

2. **Setup Steps**:
   ```bash
   # Login to GCR
   gcloud auth configure-docker
   
   # Build and tag image
   docker build -t entaera-prod:latest -f Dockerfile.prod .
   docker tag entaera-prod:latest gcr.io/your-project-id/entaera:latest
   
   # Push image
   docker push gcr.io/your-project-id/entaera:latest
   ```

3. **Deployment Options**:
   - Cloud Run for serverless containers
   - Google Kubernetes Engine (GKE)
   - Compute Engine VM instances

---

## Environment Configuration

### Environment Variables

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `ENVIRONMENT` | Runtime environment | Yes | `development` | `production` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes | - | `your_azure_key` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | Yes | - | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | Azure API version | No | `2023-12-01-preview` | `2023-12-01-preview` |
| `AZURE_DEPLOYMENT_NAME` | Azure model deployment | No | `gpt-35-turbo` | `gpt-35-turbo` |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - | `your_gemini_key` |
| `PERPLEXITY_API_KEY` | Perplexity API key | Yes | - | `your_perplexity_key` |
| `LOG_LEVEL` | Logging verbosity | No | `INFO` | `DEBUG` |
| `REDIS_HOST` | Redis host | No | `localhost` | `redis` |
| `REDIS_PORT` | Redis port | No | `6379` | `6379` |
| `DB_HOST` | Database host | No | `localhost` | `db` |
| `DB_PORT` | Database port | No | `5432` | `5432` |
| `DB_NAME` | Database name | No | `entaera` | `entaera_prod` |
| `DB_USER` | Database user | No | `postgres` | `entaera_user` |
| `DB_PASSWORD` | Database password | No | - | `secure_password` |

### Environment-Specific Configuration

- **Development**: `.env.development`
- **Production**: `.env.production`
- **Testing**: `.env.test`

### Configuration Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for configuration
3. **Validate configuration** on startup
4. **Provide example files** with placeholders
5. **Document all variables** thoroughly

---

## Security Considerations

### API Key Management

1. **Secure Storage**:
   - Store API keys in environment variables
   - Use secrets management services in production
   - Never hardcode keys in source code

2. **Key Rotation**:
   - Implement regular key rotation
   - Have mechanisms to update keys without downtime
   - Log key usage for audit purposes

### Network Security

1. **TLS/SSL**:
   - Always use HTTPS in production
   - Enforce strong TLS protocols and ciphers
   - Implement proper certificate management

2. **Network Policies**:
   - Restrict inbound/outbound connections
   - Use security groups or firewalls
   - Implement IP allowlisting where appropriate

### Data Security

1. **Data Encryption**:
   - Encrypt data at rest (database, files)
   - Encrypt data in transit (TLS)
   - Use proper key management for encryption keys

2. **Data Minimization**:
   - Only store necessary data
   - Implement data retention policies
   - Provide data deletion capabilities

### Container Security

1. **Image Security**:
   - Use minimal base images (Alpine-based)
   - Scan images for vulnerabilities
   - Run containers with least privilege

2. **Runtime Security**:
   - Use read-only file systems where possible
   - Limit resource consumption
   - Implement proper logging for container activities

---

## Monitoring Setup

### Prometheus Configuration

1. **Basic Setup**:
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'entaera'
       static_configs:
         - targets: ['app:8000']
   ```

2. **Custom Metrics**:
   - API call latency
   - Provider selection counts
   - Error rates by provider
   - Token usage by provider

### Grafana Dashboards

1. **System Dashboard**:
   - Container resource usage
   - API request rates
   - Error rates and types
   - Response times

2. **Provider Dashboard**:
   - Provider selection distribution
   - Provider response times
   - Provider error rates
   - Token usage by provider

### Alerting Configuration

```yaml
# alerts.yml
groups:
  - name: entaera-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(entaera_api_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High API error rate"
          description: "Error rate is above 10% for more than 2 minutes"
```

### Logging Best Practices

1. **Structured Logging**:
   - Use JSON format for machine parsing
   - Include consistent fields (timestamp, level, service)
   - Add context to all log entries

2. **Centralized Logging**:
   - Send logs to centralized system (ELK, Loki)
   - Implement log retention policies
   - Set up log alerts for critical issues

---

## Scaling Strategies

### Horizontal Scaling

1. **Container Orchestration**:
   - Use Kubernetes for container orchestration
   - Implement auto-scaling based on CPU/memory
   - Use load balancing for request distribution

2. **Configuration**:
   ```yaml
   # Kubernetes HPA example
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: entaera-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: entaera
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

### Vertical Scaling

1. **Resource Allocation**:
   - Analyze memory and CPU needs
   - Allocate appropriate resources
   - Consider GPU acceleration for local models

2. **Instance Sizing**:
   - Development: 2 vCPU, 4GB RAM
   - Production: 4+ vCPU, 8GB+ RAM
   - Local model support: 8+ vCPU, 16GB+ RAM

### Database Scaling

1. **Connection Pooling**:
   - Implement connection pooling
   - Set appropriate pool sizes
   - Monitor connection usage

2. **Replication**:
   - Set up read replicas for read scaling
   - Configure proper replication lag monitoring
   - Implement proper failover mechanisms

---

## Backup and Recovery

### Backup Strategy

1. **Database Backups**:
   - Regular automated backups
   - Point-in-time recovery capability
   - Offsite backup storage

2. **Configuration Backups**:
   - Version-controlled configuration templates
   - Secret backup in secure storage
   - Documentation of custom settings

### Disaster Recovery

1. **Recovery Plan**:
   - Documented recovery procedures
   - Regular recovery testing
   - Defined RPO (Recovery Point Objective) and RTO (Recovery Time Objective)

2. **Multi-Region Strategy**:
   - Consider multi-region deployment
   - Implement proper failover mechanisms
   - Test regional failover regularly

### Business Continuity

1. **Redundancy**:
   - Multiple AI providers for fallback
   - Multiple deployment regions
   - Redundant infrastructure components

2. **Incident Response**:
   - Defined incident response plan
   - On-call rotation for critical issues
   - Post-incident analysis and improvement

---

## Conclusion

This deployment guide covers the essential aspects of deploying ENTAERA from development to production environments. By following these guidelines, you can ensure a secure, scalable, and resilient deployment that leverages the full capabilities of the ENTAERA framework.

For additional support or questions, refer to the project documentation or contact the development team.

---

**Happy Deploying with ENTAERA!** 🚀