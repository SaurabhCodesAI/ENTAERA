# Test script for your n8n webhook (updated URL)

Write-Host "=== Testing n8n Webhook Integration ===" -ForegroundColor Green
Write-Host "Webhook URL: http://localhost:5678/webhook-test/vertex-webhook" -ForegroundColor Yellow

# Test 1: Basic webhook test
Write-Host "`n1. Testing basic webhook call..." -ForegroundColor Cyan

$webhookUrl = "http://localhost:5678/webhook-test/vertex-webhook"

$testData = @{
    content = "Testing n8n webhook integration with VertexAutoGPT - this is a sample research summary about AI applications in renewable energy optimization and smart grid management"
    source = "n8n-webhook-test"
    type = "summary"
    metadata = @{
        test = $true
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        origin = "webhook-test"
    }
} | ConvertTo-Json -Depth 3

Write-Host "Sending data to webhook..." -ForegroundColor Yellow
Write-Host "Data being sent:" -ForegroundColor Gray
Write-Host $testData -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $webhookUrl -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 60
    
    Write-Host "`nWebhook Response:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3 | Write-Host
    
    Write-Host "`n✅ Webhook call successful!" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ Webhook call failed:" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        Write-Host "Status Description: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    }
    
    Write-Host "`nTroubleshooting tips:" -ForegroundColor Yellow
    Write-Host "1. Make sure n8n workflow is ACTIVE (toggle switch on)" -ForegroundColor White
    Write-Host "2. Check if n8n is running on localhost:5678" -ForegroundColor White
    Write-Host "3. Verify the webhook URL: http://localhost:5678/webhook-test/vertex-webhook" -ForegroundColor White
    Write-Host "4. Check n8n Executions tab for any error details" -ForegroundColor White
}

Write-Host "`n=== Checking Results ===" -ForegroundColor Green

# Wait a moment for processing
Start-Sleep -Seconds 2

# Check if new files were created
Write-Host "`n2. Checking for new files..." -ForegroundColor Cyan
$latestFiles = Get-ChildItem "C:\Users\saurabh\VertexAutoGPT\data\summary\*.json" -ErrorAction SilentlyContinue | 
               Sort-Object LastWriteTime -Descending | 
               Select-Object -First 5

if ($latestFiles) {
    Write-Host "Latest files created:" -ForegroundColor Green
    $latestFiles | ForEach-Object { 
        $ageMinutes = [math]::Round(((Get-Date) - $_.LastWriteTime).TotalMinutes, 1)
        Write-Host "  $($_.Name) - $($_.LastWriteTime) ($ageMinutes min ago)" -ForegroundColor White
    }
} else {
    Write-Host "No files found in data/summary/" -ForegroundColor Yellow
}

# Check git commits
Write-Host "`n3. Checking git commits..." -ForegroundColor Cyan
try {
    $gitLog = git log --oneline -5 2>$null
    if ($gitLog) {
        Write-Host "Recent commits:" -ForegroundColor Green
        $gitLog | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    } else {
        Write-Host "No recent commits found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Could not check git log" -ForegroundColor Yellow
}

# Check workflow logs
Write-Host "`n4. Checking workflow logs..." -ForegroundColor Cyan
$logFile = "C:\Users\saurabh\VertexAutoGPT\logs\workflow.log"
if (Test-Path $logFile) {
    $recentLogs = Get-Content $logFile -Tail 5 -ErrorAction SilentlyContinue
    if ($recentLogs) {
        Write-Host "Recent workflow logs:" -ForegroundColor Green
        $recentLogs | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    }
} else {
    Write-Host "No workflow.log found" -ForegroundColor Yellow
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Check n8n Executions tab to see the workflow run" -ForegroundColor White
Write-Host "2. If successful, you should see a new file in data/summary/" -ForegroundColor White
Write-Host "3. Check git log for automated commits" -ForegroundColor White