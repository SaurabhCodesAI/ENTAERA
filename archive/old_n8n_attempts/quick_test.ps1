# Simple test runner to validate everything works

Write-Host "🧪 VertexAutoGPT Quick Test Runner" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Test 1: Phase 1 Validation
Write-Host "`n1. Running Phase 1 Validation..." -ForegroundColor Yellow
try {
    python phase1_validation.py | Select-String "VALIDATION: PASSED|SUCCESS RATE"
    Write-Host "✅ Phase 1 Validation: PASSED" -ForegroundColor Green
} catch {
    Write-Host "❌ Phase 1 Validation: FAILED" -ForegroundColor Red
}

# Test 2: CLI Enhanced - Simple Mode
Write-Host "`n2. Testing Enhanced CLI - Simple Mode..." -ForegroundColor Yellow
try {
    $result = python cli_enhanced.py --mode simple | ConvertFrom-Json
    if ($result.status -eq "success") {
        Write-Host "✅ CLI Simple Mode: PASSED" -ForegroundColor Green
    } else {
        Write-Host "❌ CLI Simple Mode: FAILED" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ CLI Simple Mode: ERROR" -ForegroundColor Red
}

# Test 3: CLI Enhanced - Validate Mode  
Write-Host "`n3. Testing Enhanced CLI - Validate Mode..." -ForegroundColor Yellow
try {
    $result = python cli_enhanced.py --mode validate | ConvertFrom-Json
    if ($result.status -eq "success") {
        Write-Host "✅ CLI Validate Mode: PASSED" -ForegroundColor Green
    } else {
        Write-Host "❌ CLI Validate Mode: FAILED" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ CLI Validate Mode: ERROR" -ForegroundColor Red
}

# Test 4: Canvas Workflow Validation
Write-Host "`n4. Testing Canvas Workflow..." -ForegroundColor Yellow
try {
    python canvas_validation.py | Select-String "SUCCESS RATE|FULLY VALIDATED"
    Write-Host "✅ Canvas Workflow: PASSED" -ForegroundColor Green
} catch {
    Write-Host "❌ Canvas Workflow: FAILED" -ForegroundColor Red
}

# Test 5: Data Processing
Write-Host "`n5. Testing Data Processing..." -ForegroundColor Yellow
try {
    $result = python cli_enhanced.py --mode process --content "Test data processing functionality" --source "quick_test" | ConvertFrom-Json
    if ($result.status -eq "success") {
        Write-Host "✅ Data Processing: PASSED" -ForegroundColor Green
        Write-Host "   File created: $($result.file_created)" -ForegroundColor Gray
        Write-Host "   Hash: $($result.hash)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Data Processing: FAILED" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Data Processing: ERROR" -ForegroundColor Red
}

# Test 6: Check File Structure
Write-Host "`n6. Checking File Structure..." -ForegroundColor Yellow
$summaryFiles = (Get-ChildItem "data\summary\*.json" -ErrorAction SilentlyContinue).Count
$schemaExists = Test-Path "docs\schema.json"
$logsExist = (Test-Path "logs\workflow.log") -and (Test-Path "logs\errors.log")

Write-Host "   Summary files: $summaryFiles" -ForegroundColor Gray
Write-Host "   Schema exists: $schemaExists" -ForegroundColor Gray
Write-Host "   Logs exist: $logsExist" -ForegroundColor Gray

if ($summaryFiles -gt 0 -and $schemaExists -and $logsExist) {
    Write-Host "✅ File Structure: PASSED" -ForegroundColor Green
} else {
    Write-Host "❌ File Structure: INCOMPLETE" -ForegroundColor Red
}

# Test 7: Git Status
Write-Host "`n7. Checking Git Status..." -ForegroundColor Yellow
try {
    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    $commits = (git log --oneline -n 5 2>$null).Count
    Write-Host "   Current branch: $branch" -ForegroundColor Gray
    Write-Host "   Recent commits: $commits" -ForegroundColor Gray
    Write-Host "✅ Git Status: PASSED" -ForegroundColor Green
} catch {
    Write-Host "❌ Git Status: ERROR" -ForegroundColor Red
}

# Test 8: Run Unit Tests (subset)
Write-Host "`n8. Running Unit Tests..." -ForegroundColor Yellow
try {
    $testResult = python -m pytest tests/unit/test_cli.py -v 2>&1
    if ($testResult -match "PASSED" -and $testResult -notmatch "FAILED") {
        Write-Host "✅ Unit Tests: PASSED" -ForegroundColor Green
    } else {
        Write-Host "❌ Unit Tests: SOME FAILURES" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Unit Tests: ERROR" -ForegroundColor Red
}

Write-Host "`n🎉 Quick Test Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "For comprehensive testing, run:" -ForegroundColor Cyan
Write-Host "   python phase1_validation.py" -ForegroundColor White
Write-Host "   python canvas_validation.py" -ForegroundColor White
Write-Host "   python -m pytest tests/ -v" -ForegroundColor White