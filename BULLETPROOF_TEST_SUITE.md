# 🛡️ BULLETPROOF N8N WORKFLOW TEST SUITE

## 🎯 Test Scenarios

### ✅ Test 1: Normal Operation
```powershell
$normalTest = @{
    content = "This is a complete test of the bulletproof workflow"
    type = "summary"
    source = "test-suite"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $normalTest -ContentType "application/json"
```

### ✅ Test 2: Minimal Data
```powershell
$minimalTest = @{
    content = "Minimal test"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $minimalTest -ContentType "application/json"
```

### ✅ Test 3: Edge Case - Empty Content
```powershell
$emptyTest = @{
    content = ""
    type = "test"
    source = "edge-case"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $emptyTest -ContentType "application/json"
```

### ✅ Test 4: Large Content
```powershell
$largeContent = "A" * 1000  # 1000 characters
$largeTest = @{
    content = $largeContent
    type = "analysis"
    source = "large-data-test"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $largeTest -ContentType "application/json"
```

### ✅ Test 5: Special Characters
```powershell
$specialTest = @{
    content = "Special chars: éñ中文🚀 & quotes 'test' `"test`""
    type = "unicode-test"
    source = "special-chars"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $specialTest -ContentType "application/json"
```

### ✅ Test 6: Malformed JSON (should trigger error handling)
```powershell
$malformedJson = '{"content": "test", "type": incomplete'

try {
    Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $malformedJson -ContentType "application/json"
} catch {
    Write-Host "Expected error caught: $($_.Exception.Message)" -ForegroundColor Yellow
}
```

## 📊 Expected Results

### Success Cases (Tests 1-5):
- ✅ HTTP 200 response
- ✅ JSON file uploaded to Google Drive
- ✅ Email notification sent
- ✅ Success response with all details

### Error Cases (Test 6):
- ✅ HTTP 400 response
- ✅ Error response with troubleshooting info
- ✅ No file uploaded
- ✅ No email sent

## 🔍 Validation Checklist

After each test:
- [ ] Check n8n execution log (all green checkmarks)
- [ ] Verify file in Google Drive VertexAutoGPT-Data folder
- [ ] Check Gmail for notification email
- [ ] Validate response JSON structure
- [ ] Confirm unique filename generation
- [ ] Verify binary data upload worked