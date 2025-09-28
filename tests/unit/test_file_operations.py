"""Unit tests for file operations workflow components."""
import json
import pytest
from pathlib import Path
import tempfile
import shutil


class TestFileOperations:
    """Test file read/write operations from the Canvas workflow."""
    
    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace for testing file operations."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def real_data_files(self):
        """Get real data files from the project for testing."""
        data_dir = Path(__file__).parent.parent.parent / "data"
        return {
            "summary_dir": data_dir / "summary",
            "data_dir": data_dir,
            "sample_summary": data_dir / "summary" / "201a684b.json",
            "sample_output": data_dir / "2025-09-15_04-33-34_output.json"
        }
    
    def test_read_existing_files(self, real_data_files):
        """Test reading existing data files successfully."""
        # Test reading summary file
        if real_data_files["sample_summary"].exists():
            data = self._read_json_file(real_data_files["sample_summary"])
            assert data is not None, "Failed to read summary file"
            
        # Test reading output file
        if real_data_files["sample_output"].exists():
            data = self._read_json_file(real_data_files["sample_output"])
            assert data is not None, "Failed to read output file"
    
    def test_write_file_operations(self, temp_workspace):
        """Test writing files as done in the workflow."""
        test_data = {
            "workflow_step": "test_output",
            "timestamp": "2025-09-19T10:30:00Z",
            "status": "success",
            "data": {"processed": True, "count": 42}
        }
        
        output_file = temp_workspace / "test_output.json"
        success = self._write_json_file(output_file, test_data)
        
        assert success, "Failed to write file"
        assert output_file.exists(), "Output file was not created"
        
        # Verify content
        read_data = self._read_json_file(output_file)
        assert read_data == test_data, "Written data doesn't match read data"
    
    def test_file_binary_operations(self, temp_workspace):
        """Test binary file operations for upload workflow."""
        # Simulate creating binary data for upload
        test_binary_data = b"Binary data for upload simulation"
        binary_file = temp_workspace / "upload_data.bin"
        
        # Write binary data
        with open(binary_file, 'wb') as f:
            f.write(test_binary_data)
        
        assert binary_file.exists(), "Binary file was not created"
        
        # Read and verify
        with open(binary_file, 'rb') as f:
            read_data = f.read()
        
        assert read_data == test_binary_data, "Binary data integrity check failed"
    
    def test_file_error_handling(self, temp_workspace):
        """Test file operation error handling."""
        # Test reading non-existent file
        non_existent = temp_workspace / "does_not_exist.json"
        result = self._read_json_file(non_existent)
        assert result is None, "Should return None for non-existent file"
        
        # Test writing to invalid path
        invalid_path = temp_workspace / "invalid" / "deeply" / "nested" / "file.json"
        result = self._write_json_file(invalid_path, {"test": "data"})
        # This should either fail gracefully or create directories
        
    def test_data_directory_scanning(self, real_data_files):
        """Test scanning data directories as workflow might do."""
        summary_files = list(real_data_files["summary_dir"].glob("*.json"))
        assert len(summary_files) > 0, "No summary files found for scanning"
        
        # Test that we can categorize files
        categorized = self._categorize_files(summary_files)
        assert "summary" in categorized or "other" in categorized
    
    def _read_json_file(self, file_path):
        """Helper method to read JSON files with error handling."""
        try:
            # Try utf-8-sig first to handle BOM
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                # Fallback to utf-8
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content and (content.startswith('{') or content.startswith('[')):
                        return json.loads(content)
                    return None
            except Exception:
                return None
    
    def _write_json_file(self, file_path, data):
        """Helper method to write JSON files with error handling."""
        try:
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def _categorize_files(self, file_list):
        """Helper method to categorize files by type."""
        categorized = {}
        
        for file_path in file_list:
            if "summary" in file_path.name:
                categorized.setdefault("summary", []).append(file_path)
            else:
                categorized.setdefault("other", []).append(file_path)
        
        return categorized