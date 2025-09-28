@echo off
REM Ultra-robust n8n processor that handles all edge cases
cd /d "C:\Users\saurabh\VertexAutoGPT"

REM Check if data was passed
if "%~1"=="" (
    echo {"status": "error", "message": "No data provided", "n8n_compatible": true}
    exit /b 1
)

REM Write data to temp file using PowerShell for better JSON handling
powershell -Command "$data = '%~1'; $data | Out-File -FilePath 'n8n_temp_data.json' -Encoding UTF8" 2>nul
if errorlevel 1 (
    echo {"status": "error", "message": "Could not write temp file", "n8n_compatible": true}
    exit /b 1
)

REM Run processor with full error handling
.venv\Scripts\python.exe n8n_processor_file.py 2>error.log
if errorlevel 1 (
    echo {"status": "error", "message": "Processor failed", "error_log": "Check error.log", "n8n_compatible": true}
    exit /b 1
)

REM Clean up temp file
if exist n8n_temp_data.json del n8n_temp_data.json 2>nul
exit /b 0