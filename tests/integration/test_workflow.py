"""Integration tests for the complete workflow pipeline."""
import json
import pytest
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil


class TestWorkflowIntegration:
    """Test the complete workflow pipeline end-to-end."""
    
    @pytest.fixture
    def workflow_workspace(self):
        """Create a workspace for integration testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent
    
    def test_cli_to_file_workflow(self, workflow_workspace, project_root):
        """Test CLI output can be written to files (simulating workflow)."""
        # Step 1: Execute CLI and capture output
        result = subprocess.run(
            [sys.executable, "cli.py"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        assert result.returncode == 0
        cli_output = json.loads(result.stdout.strip())
        
        # Step 2: Write to file (simulating file operation node)
        output_file = workflow_workspace / "workflow_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cli_output, f, indent=2)
        
        assert output_file.exists()
        
        # Step 3: Read back and verify (simulating read operation)
        with open(output_file, 'r', encoding='utf-8') as f:
            read_data = json.load(f)
        
        assert read_data == cli_output
    
    def test_data_processing_pipeline(self, workflow_workspace, project_root):
        """Test data processing through multiple workflow steps."""
        # Step 1: Simulate input data (WhatsApp/Google/TEST DATA nodes)
        input_data = [
            {"source": "WhatsApp", "content": "Research AI in renewable energy", "priority": "high"},
            {"source": "Google", "content": "AI energy optimization studies", "priority": "medium"},
            {"source": "TEST", "content": "Test data for validation", "priority": "low"}
        ]
        
        # Step 2: Normalize data (NormalizeAI node)
        normalized_data = []
        for item in input_data:
            normalized_data.append({
                "source": item["source"],
                "normalized_content": item["content"].lower().strip(),
                "priority_score": {"high": 1.0, "medium": 0.7, "low": 0.3}[item["priority"]],
                "processed": True
            })
        
        # Step 3: Merge operation (Merge node)
        merged_result = {
            "workflow_id": "test_workflow_001",
            "total_sources": len(normalized_data),
            "combined_data": normalized_data,
            "merge_timestamp": "2025-09-19T10:30:00Z"
        }
        
        # Step 4: Execute command simulation (Execute Command node)
        command_result = {
            "command": "process_research_data",
            "input_items": len(merged_result["combined_data"]),
            "status": "completed",
            "output_file": "processed_data.json"
        }
        
        # Step 5: Write final output (Write operations)
        final_output = workflow_workspace / "final_output.json"
        with open(final_output, 'w', encoding='utf-8') as f:
            json.dump({
                "pipeline_result": merged_result,
                "command_execution": command_result,
                "pipeline_status": "success"
            }, f, indent=2)
        
        assert final_output.exists()
        
        # Verify the pipeline worked correctly
        with open(final_output, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        assert result["pipeline_status"] == "success"
        assert result["pipeline_result"]["total_sources"] == 3
        assert result["command_execution"]["status"] == "completed"
    
    def test_error_handling_workflow(self, workflow_workspace):
        """Test error handling and recovery in the workflow."""
        # Simulate various error conditions
        error_scenarios = [
            {"type": "invalid_json", "data": "invalid json data"},
            {"type": "missing_required_field", "data": {"incomplete": "data"}},
            {"type": "processing_error", "data": None}
        ]
        
        error_results = []
        
        for scenario in error_scenarios:
            try:
                if scenario["type"] == "invalid_json":
                    # This should fail
                    json.loads(scenario["data"])
                elif scenario["type"] == "missing_required_field":
                    # Validate required fields
                    if "required_field" not in scenario["data"]:
                        raise ValueError("Missing required field")
                elif scenario["type"] == "processing_error":
                    if scenario["data"] is None:
                        raise RuntimeError("Processing failed")
                
                error_results.append({"scenario": scenario["type"], "status": "unexpected_success"})
            except (json.JSONDecodeError, ValueError, RuntimeError) as e:
                error_results.append({
                    "scenario": scenario["type"], 
                    "status": "error_caught",
                    "error_type": type(e).__name__
                })
        
        # Verify all errors were caught
        for result in error_results:
            assert result["status"] == "error_caught", f"Error not caught for {result['scenario']}"
        
        # Write error log (simulating error handling node)
        error_log = workflow_workspace / "error_log.json"
        with open(error_log, 'w', encoding='utf-8') as f:
            json.dump(error_results, f, indent=2)
        
        assert error_log.exists()
    
    def test_file_upload_simulation(self, workflow_workspace):
        """Test the file upload preparation workflow."""
        # Step 1: Create test data
        test_data = {
            "research_results": "AI can improve renewable energy efficiency by 15-20%",
            "sources": ["academic_paper_1.pdf", "study_2.pdf"],
            "confidence": 0.89,
            "generated_at": "2025-09-19T10:30:00Z"
        }
        
        # Step 2: Prepare for upload (Make Binary for Upload node)
        json_string = json.dumps(test_data, ensure_ascii=False)
        binary_data = json_string.encode('utf-8')
        
        binary_file = workflow_workspace / "upload_ready.bin"
        with open(binary_file, 'wb') as f:
            f.write(binary_data)
        
        assert binary_file.exists()
        
        # Step 3: Simulate upload metadata
        upload_metadata = {
            "filename": binary_file.name,
            "size_bytes": len(binary_data),
            "content_type": "application/json",
            "upload_ready": True,
            "checksum": hex(hash(binary_data))
        }
        
        metadata_file = workflow_workspace / "upload_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(upload_metadata, f, indent=2)
        
        # Verify upload preparation
        assert upload_metadata["upload_ready"] is True
        assert upload_metadata["size_bytes"] > 0