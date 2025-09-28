# n8n Workflow Import Guide for VertexAutoGPT

## Quick Import Steps

1. **Open n8n** (usually at http://localhost:5678)
2. **Click "Workflows"** in the sidebar
3. **Click the "+" button** for new workflow
4. **Click the "⋯" menu** (three dots, top-right)
5. **Select "Import from File"**
6. **Choose file**: `n8n_workflow_template.json` (in this directory)
7. **Click "Import"**

## After Import - Configure Paths

Update these nodes if your paths are different:
- **Process Data node**: Check the `cd C:\Users\saurabh\VertexAutoGPT` path
- **Git Status node**: Check the path
- **Upload File node**: Check the path  
- **Validate Workspace node**: Check the path

## Test the Workflow

1. **Save and Activate** the workflow
2. **Copy the webhook URL** from the Webhook Trigger node
3. **Test with PowerShell**:

```powershell
$webhook = "YOUR_WEBHOOK_URL_HERE"
$data = @{
    content = "Test from n8n webhook"
    source = "n8n-webhook"
    type = "summary"
} | ConvertTo-Json

Invoke-RestMethod -Uri $webhook -Method POST -Body $data -ContentType "application/json"
```

## What the Workflow Does

```
Webhook → Process Data → Check Success → Git Status → Upload → Response
                            ↓
                        Error Response
```

1. **Receives webhook data**
2. **Processes with your VertexAutoGPT system**
3. **Checks git status**
4. **Simulates file upload**
5. **Returns success/error response**

## Verification

After testing, check:
- New files in `data/summary/`
- New git commits: `git log --oneline -5`
- n8n execution logs for any errors

Your VertexAutoGPT is now integrated with n8n! 🚀