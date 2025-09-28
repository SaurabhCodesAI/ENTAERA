# Test different webhook URL formats for n8n

Write-Host "=== Testing n8n Webhook URL Formats ===" -ForegroundColor Green

$baseUrls = @(
    "http://localhost:5678/webhook/vertex-webhook",
    "http://localhost:5678/webhook-test/vertex-webhook", 
    "http://localhost:5678/webhook/vertex-autogpt-webhook",
    "http://localhost:5678/hook/vertex-webhook"
)

$testData = '{"content":"Test webhook URL discovery","source":"url-test","type":"summary"}'

foreach ($url in $baseUrls) {
    Write-Host "`nTesting: $url" -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 10
        Write-Host "✅ SUCCESS - This URL works!" -ForegroundColor Green
        Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Green
        break
    }
    catch {
        $statusCode = "Unknown"
        if ($_.Exception.Response) {
            $statusCode = $_.Exception.Response.StatusCode
        }
        Write-Host "❌ Failed - Status: $statusCode" -ForegroundColor Red
    }
}

Write-Host "`n=== Alternative: Check n8n Interface ===" -ForegroundColor Cyan
Write-Host "1. Go to http://localhost:5678" -ForegroundColor White
Write-Host "2. Open your VertexAutoGPT workflow" -ForegroundColor White  
Write-Host "3. Click the Webhook Trigger node" -ForegroundColor White
Write-Host "4. Copy the 'Production URL' shown there" -ForegroundColor White
Write-Host "5. Make sure the workflow is ACTIVE (toggle switch)" -ForegroundColor White