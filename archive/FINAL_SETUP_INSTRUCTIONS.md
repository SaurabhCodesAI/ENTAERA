# 🚀 FINAL SETUP INSTRUCTIONS - Google Drive n8n Workflow

## ✅ EVERYTHING IS CONFIGURED:
- 📁 **Google Drive Folder ID:** `1uOvDtX1fgluSra0l8tZ0FbqvhH5-3qC2`
- 📧 **Email:** `saurabhpareek228@gmail.com`
- 🔗 **Google Drive API:** Already connected in n8n
- 📬 **Gmail SMTP:** Already configured in n8n

## 🎯 IMPORT THE WORKFLOW:

### Step 1: Import in n8n
1. Open n8n at `http://localhost:5678`
2. Click **"Import from file"** or **"+"** → **"Import from file"**
3. Select: `n8n_googledrive_solution.json`
4. Click **"Import"**

### Step 2: Verify Credentials
1. Click on **"Upload to Google Drive"** node
2. Verify it uses your Google Drive credentials
3. Click on **"Send Email Notification"** node  
4. Verify it uses your Gmail credentials

### Step 3: Activate Workflow
1. Click the **"Active"** toggle in the top-right
2. Save the workflow

## 🧪 TEST THE WORKFLOW:

### Test Command (PowerShell):
```powershell
$testData = @{
    content = "Test data from PowerShell"
    type = "summary"
    source = "test-run"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body $testData -ContentType "application/json"
```

## 🎉 WHAT WILL HAPPEN:

1. **Webhook receives data** ✅
2. **Code node processes data** ✅
3. **File uploaded to Google Drive** → `VertexAutoGPT-Data` folder ✅
4. **Email sent to you** with Google Drive link ✅
5. **Success response returned** with all details ✅

## 📱 YOU'LL GET:

- **Email notification** on your phone/email
- **Google Drive file** with processed data
- **Direct link** to view the file
- **Success response** in n8n

## 🔥 READY TO GO!

Your workflow is **100% configured** and ready. Just import and test!