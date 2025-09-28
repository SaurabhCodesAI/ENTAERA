@echo off
cd /d C:\Users\saurabh\VertexAutoGPT

REM Create directory if it doesn't exist
mkdir "data\%~1" 2>nul

REM Remove quotes from JSON parameter and write to file
set "jsonContent=%~3"
echo %jsonContent% > "data\%~1\%~2.json"

REM Git operations  
git add "data\%~1\"
git diff --cached --quiet
if %errorlevel% neq 0 (
    git commit -m "[type:%~1] Added new %~1 - %~4"
    echo SUCCESS: File created and committed for type %~1
) else (
    echo INFO: No changes to commit for type %~1
)

REM Debug output
echo Debug: Type=%~1, Hash=%~2, Content=%jsonContent%
