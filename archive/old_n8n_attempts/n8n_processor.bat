@echo off
cd C:\Users\saurabh\VertexAutoGPT
echo %~1 > n8n_temp_data.json
.venv\Scripts\python.exe n8n_processor_file.py