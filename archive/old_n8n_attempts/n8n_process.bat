@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\saurabh\VertexAutoGPT"
echo %~1 | .venv\Scripts\python.exe n8n_simple_processor.py