# Configuration Directory

This directory contains configuration files and environment backups:

## 📁 Contents

### Environment Files
- `.env.backup` - Backup of main environment configuration
- `.env.fixed` - Fixed/corrected environment settings
- `.env.local_ai` - Local AI model configuration
- `.env.development` - Development environment settings

### Configuration Backups
- Historical configuration states
- Environment-specific settings
- API key templates and examples

## ⚠️ Security Note

This directory may contain sensitive configuration data. Never commit actual API keys or secrets to version control.

## 🔧 Usage

Use these files as templates or backups:

```bash
# Copy a configuration template
cp config/.env.example .env

# Restore from backup
cp config/.env.backup .env
```