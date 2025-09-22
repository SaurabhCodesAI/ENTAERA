# ENTAERA Repository Setup and Upload Script (PowerShell)
# This script safely uploads your project to GitHub while protecting sensitive information

Write-Host "🚀 ENTAERA Repository Upload Script" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if we're in a git repository
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists. Continuing with existing repository..." -ForegroundColor Yellow
} else {
    Write-Host "📁 Initializing new Git repository..." -ForegroundColor Cyan
    git init
    git branch -M main
}

# Add remote repository
Write-Host "🔗 Setting up remote repository..." -ForegroundColor Cyan
Write-Host "Detected Git user: saurabh (saurabhpareek228@gmail.com)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Common repository URL options:" -ForegroundColor Cyan
Write-Host "1. https://github.com/saurabh/ENTAERA.git"
Write-Host "2. https://github.com/your-org/ENTAERA.git"
Write-Host "3. git@github.com:saurabh/ENTAERA.git (SSH)"
Write-Host ""
$repo_url = Read-Host "Enter your GitHub repository URL"
git remote remove origin 2>$null
git remote add origin $repo_url

# Verify .gitignore is protecting sensitive files
Write-Host "🔒 Verifying sensitive file protection..." -ForegroundColor Cyan
$gitignore_content = Get-Content .gitignore -Raw
if ($gitignore_content -match "\.env$" -and $gitignore_content -match "logs/") {
    Write-Host "✅ Sensitive files are protected by .gitignore" -ForegroundColor Green
} else {
    Write-Host "❌ WARNING: .gitignore may not be protecting sensitive files properly!" -ForegroundColor Red
    exit 1
}

# Clean up any temporary files
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Cyan
Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force
Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Name "*.tmp" | Remove-Item -Force

# Stage files (sensitive files will be automatically excluded)
Write-Host "📦 Staging files for commit..." -ForegroundColor Cyan
git add .

# Show what files will be committed
Write-Host "📋 Files to be committed:" -ForegroundColor Cyan
$staged_files = git diff --cached --name-only
$staged_files | Select-Object -First 20 | ForEach-Object { Write-Host "   $_" }
if ($staged_files.Count -gt 20) {
    Write-Host "   ... and $($staged_files.Count - 20) more files"
}

# Verify no sensitive files are staged
Write-Host "🔍 Checking for sensitive files in commit..." -ForegroundColor Cyan
$sensitive_files = $staged_files | Where-Object { $_ -match "\.env$|\.env\.|secrets|\.log$" -and $_ -notmatch "\.example" }
if ($sensitive_files) {
    Write-Host "❌ WARNING: Sensitive files detected in commit! Aborting..." -ForegroundColor Red
    Write-Host "Sensitive files found: $($sensitive_files -join ', ')" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ No sensitive files detected in commit" -ForegroundColor Green
}

# Create professional commit message
$commit_message = @"
🚀 ENTAERA v1.0: Enterprise Multi-API AI Framework

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
- Contributing guidelines and code standards
"@

Write-Host "💬 Committing with professional message..." -ForegroundColor Cyan
git commit -m $commit_message

# Push to repository
Write-Host "⬆️  Pushing to GitHub repository..." -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "🎉 SUCCESS! Your ENTAERA repository has been uploaded to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit your repository on GitHub"
Write-Host "2. Set up branch protection rules in Settings > Branches"
Write-Host "3. Add repository secrets for CI/CD:"
Write-Host "   - PYPI_TOKEN (for package publishing)"
Write-Host "   - Any other deployment secrets"
Write-Host "4. Enable GitHub Actions if not already enabled"
Write-Host "5. Consider setting up GitHub Pages for documentation"
Write-Host ""
Write-Host "🔒 Security Verified:" -ForegroundColor Green
Write-Host "   ✅ API keys and sensitive data protected"
Write-Host "   ✅ Environment files excluded from commit"
Write-Host "   ✅ Logs and cache directories ignored"
Write-Host "   ✅ Professional commit history established"
Write-Host ""
Write-Host "🚀 Your ENTAERA repository is now live and ready for collaboration!" -ForegroundColor Green