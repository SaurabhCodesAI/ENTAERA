# 🧪 Complete Testing Guide for VertexAutoGPT

## Quick Test Commands

Copy and paste these commands in your PowerShell terminal:

### 1. 🚀 **Quick Validation (Start Here)**
```powershell
# Run the complete Phase 1 validation
python phase1_validation.py
```

### 2. 🔧 **Test Enhanced CLI**
```powershell
# Test simple mode (original functionality)
python cli_enhanced.py --mode simple

# Test data processing mode
python cli_enhanced.py --mode process --content "Test from CLI" --source "manual_test"

# Test validation mode
python cli_enhanced.py --mode validate
```

### 3. 📊 **Test Data Processing System**
```powershell
# Create test data using the data processor
python -c "
import sys
sys.path.append('src')
from vertexautogpt.core.data_processor import VertexDataProcessor
processor = VertexDataProcessor()
result = processor.process_data('Test data processing', 'test_source', 'summary')
print(f'File created: {result[\"file_path\"]}')
print(f'Hash: {result[\"hash\"]}')
"
```

### 4. 🌐 **Test n8n Integration**
```powershell
# Run the complete n8n integration test
.\test_n8n_integration.ps1
```

### 5. 🧪 **Run All Unit Tests**
```powershell
# Run the complete test suite
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v       # Unit tests only
python -m pytest tests/integration/ -v # Integration tests only
python -m pytest tests/e2e/ -v        # End-to-end tests only
```

### 6. 📈 **Canvas Workflow Validation**
```powershell
# Test the complete Canvas workflow simulation
python canvas_validation.py
```

### 7. 📋 **Individual Component Tests**

#### Test CLI Components:
```powershell
# Original CLI
python cli.py

# Source CLI
python src/cli.py
```

#### Test File Operations:
```powershell
# List files in each data directory
Get-ChildItem data\summary | Select Name,Length,LastWriteTime
Get-ChildItem data\raw | Select Name,Length,LastWriteTime  
Get-ChildItem data\embeddings | Select Name,Length,LastWriteTime
```

#### Test Schema Validation:
```powershell
# View the schema
Get-Content docs\schema.json
```

#### Test Logs:
```powershell
# Check workflow logs
Get-Content logs\workflow.log -Tail 20

# Check error logs
Get-Content logs\errors.log -Tail 20
```

#### Test Git Integration:
```powershell
# Check recent commits
git log -n 10 --oneline

# Check current branch
git rev-parse --abbrev-ref HEAD

# Check git status
git status
```

### 8. 🔄 **Stress Test (Multiple Operations)**
```powershell
# Create multiple test entries quickly
for ($i=1; $i -le 5; $i++) {
    python cli_enhanced.py --mode process --content "Stress test entry $i" --source "stress_test"
}

# Verify they were all processed
python n8n_integration.py files --limit 10
```

### 9. ❌ **Error Handling Tests**
```powershell
# Test invalid JSON input
python n8n_integration.py process --data '{"invalid": "missing required fields"}'

# Test missing file upload
python n8n_integration.py upload --file "nonexistent_file.json"

# Test invalid data type
python cli_enhanced.py --mode process --content "test" --type "invalid_type"
```

### 10. 📊 **Performance Test**
```powershell
# Time the complete workflow
Measure-Command { python phase1_validation.py }

# Time data processing
Measure-Command { python cli_enhanced.py --mode process --content "Performance test" --source "perf_test" }
```

## 🎯 Expected Results

### ✅ All Tests Should Show:
- **Phase 1 Validation**: 100% success rate (15/15 checks passed)
- **CLI Tests**: Valid JSON output from all modes
- **Data Processing**: Files created in correct directories with proper schema
- **n8n Integration**: All 5 actions working correctly
- **Canvas Validation**: 100% success rate (12/12 components)
- **Unit Tests**: 19+ tests passing
- **Git Integration**: Automated commits with proper messages
- **Schema Validation**: All required fields present
- **Error Handling**: Proper error messages for invalid inputs

### 📁 File Structure After Testing:
```
data/
├── summary/     # 40+ JSON files with processed data
├── raw/         # Empty or test files
└── embeddings/  # Empty or test files

logs/
├── workflow.log # Processing events
└── errors.log   # Error tracking

tests/
├── unit/        # Component tests
├── integration/ # Workflow tests
└── e2e/         # End-to-end tests
```

### 🔍 Troubleshooting

If any test fails:

1. **Check Python Environment**:
   ```powershell
   python --version
   pip list | findstr "jsonschema pytest"
   ```

2. **Check File Permissions**:
   ```powershell
   # Ensure you can write to data/ and logs/
   Test-Path -Path "data" -PathType Container
   Test-Path -Path "logs" -PathType Container
   ```

3. **Check Git Configuration**:
   ```powershell
   git config --list
   git status
   ```

4. **View Detailed Errors**:
   ```powershell
   # Run with verbose output
   python -m pytest tests/ -v -s
   
   # Check error logs
   Get-Content logs\errors.log
   ```

## 🎉 Success Indicators

You'll know everything is working when you see:
- ✅ Phase 1 validation: 100% success
- ✅ All CLI modes returning valid JSON
- ✅ Files being created and committed to git
- ✅ n8n integration responding correctly
- ✅ Canvas workflow: 12/12 components validated
- ✅ Test suite: 19+ tests passing

Your VertexAutoGPT workspace is now fully tested and production-ready! 🚀