# Test script for n8n integration with VertexAutoGPT

Write-Host "=== Testing n8n Integration for VertexAutoGPT ===" -ForegroundColor Green

# Test 1: Process webhook data
Write-Host "`n1. Testing webhook data processing..." -ForegroundColor Yellow
$webhookData = '{"content":"AI research on quantum computing applications","source":"n8n-webhook","type":"summary","metadata":{"origin":"test"}}'

Write-Host "Command: python n8n_integration.py process --data '$webhookData'" -ForegroundColor Cyan
python n8n_integration.py process --data $webhookData

# Test 2: Validate workspace
Write-Host "`n2. Testing workspace validation..." -ForegroundColor Yellow
Write-Host "Command: python n8n_integration.py validate" -ForegroundColor Cyan
python n8n_integration.py validate

# Test 3: Get latest files
Write-Host "`n3. Testing file listing..." -ForegroundColor Yellow
Write-Host "Command: python n8n_integration.py files --type summary --limit 3" -ForegroundColor Cyan
python n8n_integration.py files --type summary --limit 3

# Test 4: Git status
Write-Host "`n4. Testing git status..." -ForegroundColor Yellow
Write-Host "Command: python n8n_integration.py git" -ForegroundColor Cyan
python n8n_integration.py git

# Test 5: Upload simulation
Write-Host "`n5. Testing upload simulation..." -ForegroundColor Yellow
# First check if we have any files to upload
$latestFile = Get-ChildItem "data\summary\*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($latestFile) {
    Write-Host "Command: python n8n_integration.py upload --file '$($latestFile.FullName)'" -ForegroundColor Cyan
    python n8n_integration.py upload --file $latestFile.FullName
} else {
    Write-Host "No files found for upload test" -ForegroundColor Red
}

Write-Host "`n=== n8n Integration Tests Complete ===" -ForegroundColor Green