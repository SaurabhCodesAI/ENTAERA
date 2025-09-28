@echo off
setlocal enabledelayedexpansion

REM N8N Batch Processor - Handles webhook data without PowerShell JSON parsing issues
REM Usage: n8n_batch_processor.bat "JSON_DATA"

cd /d "C:\Users\saurabh\VertexAutoGPT"

REM Check if we have data
if "%~1"=="" (
    echo Error: No data provided
    exit /b 1
)

REM Write the JSON data to a temporary file with proper encoding
echo %~1 > n8n_temp_data.json

REM Activate virtual environment and run processor
call .venv\Scripts\python.exe n8n_processor_file.py

REM Clean up
if exist n8n_temp_data.json del n8n_temp_data.json

exit /b %ERRORLEVEL%