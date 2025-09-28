@echo off
cd /d "C:\Users\saurabh\VertexAutoGPT"
powershell -Command "& {$input | Out-File -FilePath 'n8n_temp_data.json' -Encoding UTF8; & .venv\Scripts\python.exe n8n_processor_file.py}"