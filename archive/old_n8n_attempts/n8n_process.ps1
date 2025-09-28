param(
    [string]$JsonData
)

Set-Location "C:\Users\saurabh\VertexAutoGPT"
$JsonData | & ".venv\Scripts\python.exe" "n8n_simple_processor.py"