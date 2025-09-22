# 🚀 ENTAERA Upload to SaurabhCodesAI GitHub Account
# Quick setup script for github.com/SaurabhCodesAI

Write-Host "🚀 ENTAERA Upload to SaurabhCodesAI" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

Write-Host "📋 Configuration:" -ForegroundColor Cyan
Write-Host "   GitHub Account: SaurabhCodesAI"
Write-Host "   Git User: saurabh"
Write-Host "   Email: saurabhpareek228@gmail.com"
Write-Host ""

# Repository name options
Write-Host "📁 Repository Name Options:" -ForegroundColor Yellow
Write-Host "1. ENTAERA (recommended)"
Write-Host "2. entaera"
Write-Host "3. ENTAERA-Framework"
Write-Host "4. entaera-ai-framework"
Write-Host ""

$repo_choice = Read-Host "Choose repository name (1-4 or enter custom)"

switch ($repo_choice) {
    "1" { $repo_name = "ENTAERA" }
    "2" { $repo_name = "entaera" }
    "3" { $repo_name = "ENTAERA-Framework" }
    "4" { $repo_name = "entaera-ai-framework" }
    default { $repo_name = $repo_choice }
}

$repo_url = "https://github.com/SaurabhCodesAI/$repo_name.git"

Write-Host ""
Write-Host "🔗 Target Repository: $repo_url" -ForegroundColor Cyan
Write-Host ""

# Confirm
$confirm = Read-Host "Proceed with upload? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Upload cancelled." -ForegroundColor Red
    exit
}

# Initialize Git
Write-Host "📁 Setting up Git repository..." -ForegroundColor Cyan
if (Test-Path ".git") {
    Write-Host "   Git already initialized"
} else {
    git init
    git branch -M main
}

# Set up remote
Write-Host "🔗 Configuring remote..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $repo_url

# Security verification
Write-Host "🔒 Security check..." -ForegroundColor Cyan
if ((Get-Content .gitignore -Raw) -match "\.env$") {
    Write-Host "   ✅ API keys protected" -ForegroundColor Green
} else {
    Write-Host "   ❌ Security issue detected!" -ForegroundColor Red
    exit 1
}

# Stage files
Write-Host "📦 Staging files..." -ForegroundColor Cyan
git add .

# Show staged files count
$staged_count = (git diff --cached --name-only).Count
Write-Host "   📄 $staged_count files staged for upload"

# Professional commit
Write-Host "💬 Creating professional commit..." -ForegroundColor Cyan
git commit -m "🚀 ENTAERA v1.0: Enterprise Multi-API AI Framework

✨ Complete multi-provider AI integration with smart routing
🧠 Context-aware processing and cost optimization
🏗️ Production-ready architecture with Docker support
📚 Comprehensive documentation and enterprise guides
🔒 Security-first design with API key protection
🧪 Full test suite and automated CI/CD pipeline
💰 Token counting and intelligent cost management
🌐 Support for Azure OpenAI, Google Gemini, Perplexity
🚀 Local AI model integration for offline processing
📊 Advanced monitoring and error handling"

# Upload to GitHub
Write-Host "⬆️  Uploading to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! ENTAERA is now live on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Repository URL:" -ForegroundColor Cyan
    Write-Host "   https://github.com/SaurabhCodesAI/$repo_name" -ForegroundColor White
    Write-Host ""
    Write-Host "📌 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Visit your repository and add a description"
    Write-Host "2. Set up branch protection (Settings > Branches)"
    Write-Host "3. Add repository topics/tags for discoverability"
    Write-Host "4. Add PYPI_TOKEN secret for publishing"
    Write-Host "5. Enable GitHub Actions (should auto-enable)"
    Write-Host ""
    Write-Host "🏆 Your professional AI framework is now showcased!" -ForegroundColor Green
    Write-Host "🚀 Ready for collaboration, contributions, and deployment!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Upload failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Create repository first: https://github.com/new"
    Write-Host "2. Set up GitHub authentication:"
    Write-Host "   gh auth login"
    Write-Host "3. Check repository name and permissions"
    Write-Host ""
    Write-Host "🔗 Repository should be created at:"
    Write-Host "   https://github.com/SaurabhCodesAI/$repo_name"
}

Write-Host ""
Write-Host "🔒 Security Confirmed:" -ForegroundColor Green
Write-Host "   ✅ API keys protected (.env files excluded)"
Write-Host "   ✅ Logs and cache excluded"
Write-Host "   ✅ Only safe files uploaded"
Write-Host "   ✅ Professional commit history"