# 🚀 ENTAERA GitHub Upload - Simple Setup
# Customized for saurabh (saurabhpareek228@gmail.com)

Write-Host "🚀 ENTAERA GitHub Upload for Multiple Account Options" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green

# Show current Git configuration
Write-Host "📋 Current Git Configuration:" -ForegroundColor Cyan
Write-Host "   User: saurabh"
Write-Host "   Email: saurabhpareek228@gmail.com"
Write-Host "   Target Account: SaurabhCodesAI"
Write-Host ""

# GitHub Account Options
Write-Host "🎯 Detected GitHub Account: SaurabhCodesAI" -ForegroundColor Yellow
Write-Host "1. Use SaurabhCodesAI (recommended)"
Write-Host "2. Use different account"
Write-Host ""

$account_choice = Read-Host "Proceed with SaurabhCodesAI? (1/2)"

switch ($account_choice) {
    "1" {
        $github_user = "SaurabhCodesAI"
        Write-Host "✅ Using account: github.com/SaurabhCodesAI" -ForegroundColor Green
    }
    "2" {
        $github_user = Read-Host "Enter your GitHub username"
        Write-Host "✅ Using account: github.com/$github_user" -ForegroundColor Green
    }
    default {
        $github_user = "SaurabhCodesAI"
        Write-Host "✅ Using default account: github.com/SaurabhCodesAI" -ForegroundColor Green
    }
}

# Repository Name Options
Write-Host ""
Write-Host "📁 Repository Name Options:" -ForegroundColor Yellow
Write-Host "1. ENTAERA (recommended)"
Write-Host "2. entaera (lowercase)"
Write-Host "3. ENTAERA-Framework"
Write-Host "4. Custom name"
Write-Host ""

$repo_choice = Read-Host "Which repository name? (1/2/3/4 or enter custom name)"

switch ($repo_choice) {
    "1" { $repo_name = "ENTAERA" }
    "2" { $repo_name = "entaera" }
    "3" { $repo_name = "ENTAERA-Framework" }
    "4" { $repo_name = Read-Host "Enter custom repository name" }
    default { $repo_name = $repo_choice }
}

# Build repository URL
$repo_url = "https://github.com/$github_user/$repo_name.git"
Write-Host ""
Write-Host "🔗 Repository URL: $repo_url" -ForegroundColor Cyan

# Confirm before proceeding
Write-Host ""
$confirm = Read-Host "Proceed with this configuration? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Upload cancelled." -ForegroundColor Red
    exit
}

# Initialize Git if needed
if (Test-Path ".git") {
    Write-Host "⚠️  Git repository already exists. Continuing..." -ForegroundColor Yellow
} else {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Cyan
    git init
    git branch -M main
}

# Set up remote
Write-Host "🔗 Setting up remote repository..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $repo_url

# Verify authentication
Write-Host "🔐 Testing GitHub authentication..." -ForegroundColor Cyan
git ls-remote origin >$null 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ GitHub authentication successful!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Authentication failed. You may need to:" -ForegroundColor Yellow
    Write-Host "   1. Create the repository on GitHub first"
    Write-Host "   2. Set up GitHub authentication (token or SSH key)"
    Write-Host "   3. Run: gh auth login (if using GitHub CLI)"
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "❌ Upload cancelled." -ForegroundColor Red
        exit
    }
}

# Security check
Write-Host "🔒 Verifying security..." -ForegroundColor Cyan
$gitignore_content = Get-Content .gitignore -Raw
if ($gitignore_content -match "\.env$" -and $gitignore_content -match "logs/") {
    Write-Host "✅ Sensitive files protected" -ForegroundColor Green
} else {
    Write-Host "❌ Security check failed!" -ForegroundColor Red
    exit 1
}

# Stage and commit
Write-Host "📦 Staging files..." -ForegroundColor Cyan
git add .

Write-Host "💬 Creating professional commit..." -ForegroundColor Cyan
git commit -m "🚀 ENTAERA v1.0: Enterprise Multi-API AI Framework

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

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! ENTAERA uploaded to GitHub!" -ForegroundColor Green
    Write-Host "🌐 Repository URL: https://github.com/$github_user/$repo_name" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📌 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://github.com/$github_user/$repo_name"
    Write-Host "2. Set up branch protection (Settings > Branches)"
    Write-Host "3. Add secrets: PYPI_TOKEN for publishing"
    Write-Host "4. Enable GitHub Actions"
    Write-Host ""
    Write-Host "🚀 Your professional ENTAERA repository is now live!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Upload failed. Common solutions:" -ForegroundColor Red
    Write-Host "1. Create repository on GitHub first: https://github.com/new"
    Write-Host "2. Set up GitHub authentication"
    Write-Host "3. Check repository permissions"
}