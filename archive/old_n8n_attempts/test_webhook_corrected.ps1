# Updated webhook test with correct URL

Write-Host "=== Testing n8n Webhook Integration (CORRECTED URL) ===" -ForegroundColor Green
Write-Host "Correct Webhook URL: http://localhost:5678/webhook/vertex-webhook" -ForegroundColor Yellow

$webhookUrl = "http://localhost:5678/webhook/vertex-webhook"

$testData = @{
    content = "SUCCESS! Testing n8n webhook integration with VertexAutoGPT - this is a sample research summary about AI applications in renewable energy optimization and smart grid management systems"
    source = "n8n-webhook-corrected"
    type = "summary"
    metadata = @{
        test = $true
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        origin = "corrected-webhook-test"
        attempt = "second-try"
    }
} | ConvertTo-Json -Depth 3

Write-Host "`nSending data to CORRECT webhook..." -ForegroundColor Yellow
Write-Host "Data being sent:" -ForegroundColor Gray
Write-Host $testData -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri $webhookUrl -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 60
    
    Write-Host "`n🎉 WEBHOOK SUCCESS!" -ForegroundColor Green
    Write-Host "Response received:" -ForegroundColor Green
    
    if ($response) {
        $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor Cyan
    } else {
        Write-Host "Empty response (this might be normal for n8n)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "`n❌ Webhook still failed:" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Wait for processing
Write-Host "`nWaiting 5 seconds for processing..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n=== Checking Results ===" -ForegroundColor Green

# Check for new files (should be VERY recent)
Write-Host "`n1. Checking for NEW files..." -ForegroundColor Cyan
$veryRecentFiles = Get-ChildItem "C:\Users\saurabh\VertexAutoGPT\data\summary\*.json" -ErrorAction SilentlyContinue | 
                   Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-2) } |
                   Sort-Object LastWriteTime -Descending

if ($veryRecentFiles) {
    Write-Host "🎉 NEW FILES CREATED IN LAST 2 MINUTES:" -ForegroundColor Green
    $veryRecentFiles | ForEach-Object { 
        $ageSeconds = [math]::Round(((Get-Date) - $_.LastWriteTime).TotalSeconds, 1)
        Write-Host "  ✅ $($_.Name) - $($_.LastWriteTime) ($ageSeconds sec ago)" -ForegroundColor Green
    }
} else {
    Write-Host "No new files created in the last 2 minutes" -ForegroundColor Yellow
    
    # Show latest files anyway
    $latestFiles = Get-ChildItem "C:\Users\saurabh\VertexAutoGPT\data\summary\*.json" -ErrorAction SilentlyContinue | 
                   Sort-Object LastWriteTime -Descending | 
                   Select-Object -First 3
    
    if ($latestFiles) {
        Write-Host "Latest existing files:" -ForegroundColor Gray
        $latestFiles | ForEach-Object { 
            $ageMinutes = [math]::Round(((Get-Date) - $_.LastWriteTime).TotalMinutes, 1)
            Write-Host "  $($_.Name) - ($ageMinutes min ago)" -ForegroundColor Gray
        }
    }
}

# Check for new git commits
Write-Host "`n2. Checking for NEW git commits..." -ForegroundColor Cyan
$recentCommits = git log --since="2 minutes ago" --oneline 2>$null
if ($recentCommits) {
    Write-Host "🎉 NEW COMMITS IN LAST 2 MINUTES:" -ForegroundColor Green
    $recentCommits | ForEach-Object { Write-Host "  ✅ $_" -ForegroundColor Green }
} else {
    Write-Host "No new commits in the last 2 minutes" -ForegroundColor Yellow
}

Write-Host "`n=== WEBHOOK TEST COMPLETE ===" -ForegroundColor Green
Write-Host "If you see new files and commits above, your n8n integration is WORKING! 🚀" -ForegroundColor Cyan