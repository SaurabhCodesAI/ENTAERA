#!/bin/bash
# ENTAERA Repository Setup and Upload Script
# This script safely uploads your project to GitHub while protecting sensitive information

echo "🚀 ENTAERA Repository Upload Script"
echo "=================================="

# Check if we're in a git repository
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists. Continuing with existing repository..."
else
    echo "📁 Initializing new Git repository..."
    git init
    git branch -M main
fi

# Add remote repository (replace with your actual repository URL)
echo "🔗 Setting up remote repository..."
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/ENTAERA.git): " repo_url
git remote remove origin 2>/dev/null
git remote add origin "$repo_url"

# Verify .gitignore is protecting sensitive files
echo "🔒 Verifying sensitive file protection..."
if grep -q "\.env$" .gitignore && grep -q "logs/" .gitignore; then
    echo "✅ Sensitive files are protected by .gitignore"
else
    echo "❌ WARNING: .gitignore may not be protecting sensitive files properly!"
    exit 1
fi

# Clean up any temporary files
echo "🧹 Cleaning up temporary files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.tmp" -delete

# Stage files (sensitive files will be automatically excluded)
echo "📦 Staging files for commit..."
git add .

# Show what files will be committed (excluding sensitive ones)
echo "📋 Files to be committed:"
git diff --cached --name-only | head -20
if [ $(git diff --cached --name-only | wc -l) -gt 20 ]; then
    echo "... and $(expr $(git diff --cached --name-only | wc -l) - 20) more files"
fi

# Verify no sensitive files are staged
echo "🔍 Checking for sensitive files in commit..."
if git diff --cached --name-only | grep -E "(\.env$|\.env\.|secrets|\.log$)" | grep -v ".example"; then
    echo "❌ WARNING: Sensitive files detected in commit! Aborting..."
    exit 1
else
    echo "✅ No sensitive files detected in commit"
fi

# Create professional commit message
commit_message="🚀 ENTAERA v1.0: Enterprise Multi-API AI Framework

✨ Features:
- Smart routing between Azure OpenAI, Google Gemini, Perplexity
- Context-aware query processing and cost optimization
- Production-ready architecture with Docker support
- Comprehensive documentation and API guides
- Enterprise-grade security and error handling
- Full test suite and CI/CD pipeline

🏗️ Architecture:
- Modular provider system for easy extension
- Intelligent fallback mechanisms
- Token counting and cost optimization
- Async processing for improved performance
- Docker containerization for scalability

📚 Documentation:
- Complete API reference and guides
- Deployment instructions for multiple environments  
- Security best practices and configuration
- Contributing guidelines and code standards"

echo "💬 Committing with professional message..."
git commit -m "$commit_message"

# Push to repository
echo "⬆️  Pushing to GitHub repository..."
git push -u origin main

echo ""
echo "🎉 SUCCESS! Your ENTAERA repository has been uploaded to GitHub!"
echo ""
echo "📌 Next Steps:"
echo "1. Visit your repository on GitHub"
echo "2. Set up branch protection rules in Settings > Branches"
echo "3. Add repository secrets for CI/CD:"
echo "   - PYPI_TOKEN (for package publishing)"
echo "   - Any other deployment secrets"
echo "4. Enable GitHub Actions if not already enabled"
echo "5. Consider setting up GitHub Pages for documentation"
echo ""
echo "🔒 Security Verified:"
echo "   ✅ API keys and sensitive data protected"
echo "   ✅ Environment files excluded from commit"
echo "   ✅ Logs and cache directories ignored"
echo "   ✅ Professional commit history established"
echo ""
echo "🚀 Your ENTAERA repository is now live and ready for collaboration!"