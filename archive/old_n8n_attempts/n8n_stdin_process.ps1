# Read JSON from stdin and process it
Set-Location "C:\Users\saurabh\VertexAutoGPT"
$input | & ".venv\Scripts\python.exe" "n8n_simple_processor.py"