# n8n Workflow Troubleshooting Guide

## ✅ CONFIRMED WORKING:
- ✅ n8n_simple_processor.py works perfectly
- ✅ Webhook endpoint is responding
- ✅ Command syntax is correct
- ✅ File creation works
- ✅ JSON processing works

## 🔧 TROUBLESHOOTING STEPS:

### 1. Check n8n Workflow Execution
In your n8n interface:
1. Go to **Executions** tab
2. Look for recent executions of your workflow
3. Click on any failed executions to see error details
4. Check specifically the "Process Data" node for errors

### 2. Verify Workflow Configuration
In the "Process Data" node, the command should be EXACTLY:
```
cd /d "C:\Users\saurabh\VertexAutoGPT" && echo {{ JSON.stringify($json.body) }} | .venv\Scripts\python.exe n8n_simple_processor.py
```

### 3. Common Issues to Check:
- ❌ Wrong path to the processor file
- ❌ Wrong Python executable path  
- ❌ JSON syntax issues in the command
- ❌ Missing quotes around the path

### 4. Test Commands:
These commands work perfectly (tested):

**Direct processor test:**
```cmd
cd /d "C:\Users\saurabh\VertexAutoGPT" && echo {"content": "test", "type": "summary"} | .venv\Scripts\python.exe n8n_simple_processor.py
```

**Webhook test:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5678/webhook/vertex-webhook" -Method POST -Body '{"content": "test", "type": "summary"}' -ContentType "application/json"
```

### 5. Expected Workflow Flow:
1. Webhook receives POST data
2. "Process Data" node runs the command
3. Returns JSON with status: "success"
4. "Check Success" evaluates the status
5. Continues to validation and git automation

## 🚀 NEXT STEPS:
1. Check the n8n execution logs for the specific error
2. Verify the "Process Data" node command is exactly as specified
3. Make sure the workflow is active
4. Test again with a simple payload

The processor itself is 100% working - the issue is in the n8n workflow configuration.