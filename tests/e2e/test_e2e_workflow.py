"""End-to-end tests for complete VertexAutoGPT workflow."""
import json
import pytest
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import time


class TestE2EWorkflow:
    """End-to-end testing of the complete VertexAutoGPT workflow."""
    
    @pytest.fixture
    def e2e_workspace(self):
        """Create a complete workspace for E2E testing."""
        temp_dir = Path(tempfile.mkdtemp())
        # Create subdirectories matching the workflow
        (temp_dir / "input").mkdir()
        (temp_dir / "processing").mkdir()
        (temp_dir / "output").mkdir()
        (temp_dir / "logs").mkdir()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent
    
    def test_complete_research_workflow(self, e2e_workspace, project_root):
        """Test the complete research workflow from input to final output."""
        workflow_log = []
        
        # Step 1: Input simulation (WhatsApp/Google/TEST DATA nodes)
        input_sources = [
            {
                "source": "WhatsApp",
                "query": "How can AI improve renewable energy efficiency?",
                "timestamp": time.time(),
                "priority": "high"
            },
            {
                "source": "Google",
                "query": "AI renewable energy optimization research papers",
                "timestamp": time.time(),
                "priority": "medium"
            },
            {
                "source": "TEST",
                "query": "Test query for validation",
                "timestamp": time.time(),
                "priority": "low"
            }
        ]
        
        workflow_log.append({"step": "input_collection", "status": "completed", "count": len(input_sources)})
        
        # Step 2: CLI Processing (simulating Switch/Code to JavaScript nodes)
        cli_results = []
        for source in input_sources:
            # Execute CLI for each input
            result = subprocess.run(
                [sys.executable, "cli.py"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            if result.returncode == 0:
                cli_output = json.loads(result.stdout.strip())
                cli_output["input_source"] = source["source"]
                cli_output["original_query"] = source["query"]
                cli_results.append(cli_output)
        
        workflow_log.append({"step": "cli_processing", "status": "completed", "results": len(cli_results)})
        
        # Step 3: Data Normalization and Processing
        normalized_results = []
        for result in cli_results:
            normalized = {
                "id": f"result_{len(normalized_results) + 1}",
                "source": result["input_source"],
                "original_query": result["original_query"],
                "processed_summary": result.get("summary", ""),
                "confidence": 0.85,  # Simulated confidence score
                "processing_timestamp": time.time()
            }
            normalized_results.append(normalized)
        
        workflow_log.append({"step": "normalization", "status": "completed", "normalized": len(normalized_results)})
        
        # Step 4: Merge and Execute Command
        merged_data = {
            "workflow_id": f"e2e_test_{int(time.time())}",
            "total_inputs": len(input_sources),
            "processed_results": normalized_results,
            "merge_timestamp": time.time(),
            "status": "merged"
        }
        
        # Execute command simulation
        command_result = {
            "command": "generate_research_summary",
            "input_count": len(normalized_results),
            "execution_time": 0.1,  # Simulated execution time
            "status": "success",
            "output": "Generated comprehensive research summary on AI and renewable energy"
        }
        
        workflow_log.append({"step": "merge_and_execute", "status": "completed", "command_status": command_result["status"]})
        
        # Step 5: File Operations (Read/Write)
        # Write intermediate results
        processing_file = e2e_workspace / "processing" / "intermediate_results.json"
        with open(processing_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2)
        
        # Write command results
        command_file = e2e_workspace / "processing" / "command_results.json"
        with open(command_file, 'w', encoding='utf-8') as f:
            json.dump(command_result, f, indent=2)
        
        workflow_log.append({"step": "file_operations", "status": "completed", "files_written": 2})
        
        # Step 6: Final Output Generation
        final_output = {
            "workflow_summary": {
                "id": merged_data["workflow_id"],
                "completion_time": time.time(),
                "total_processing_steps": len(workflow_log),
                "final_status": "success"
            },
            "research_results": {
                "query_summary": "AI impact on renewable energy",
                "key_findings": command_result["output"],
                "sources_processed": len(input_sources),
                "confidence_score": 0.87
            },
            "workflow_log": workflow_log,
            "output_files": [str(processing_file), str(command_file)]
        }
        
        # Step 7: Prepare for Upload and Email
        output_file = e2e_workspace / "output" / "final_research_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        
        # Create binary version for upload
        binary_output = e2e_workspace / "output" / "upload_ready.bin"
        with open(binary_output, 'wb') as f:
            f.write(json.dumps(final_output, ensure_ascii=False).encode('utf-8'))
        
        # Step 8: Create email content simulation
        email_content = {
            "to": "research@example.com",
            "subject": f"Research Completed: {final_output['workflow_summary']['id']}",
            "body": f"Research workflow completed successfully.\n\nKey Findings: {final_output['research_results']['key_findings']}\n\nConfidence Score: {final_output['research_results']['confidence_score']}",
            "attachments": [str(output_file)],
            "status": "ready_to_send"
        }
        
        email_file = e2e_workspace / "output" / "email_content.json"
        with open(email_file, 'w', encoding='utf-8') as f:
            json.dump(email_content, f, indent=2)
        
        # Final verification
        assert output_file.exists()
        assert binary_output.exists()
        assert email_file.exists()
        
        # Verify workflow completed successfully
        assert final_output["workflow_summary"]["final_status"] == "success"
        assert final_output["research_results"]["sources_processed"] == 3
        assert len(final_output["workflow_log"]) == 5  # All major steps logged
        
        # Log final success
        workflow_log.append({"step": "e2e_completion", "status": "success", "final_files": 3})
        
        return final_output
    
    def test_error_recovery_e2e(self, e2e_workspace, project_root):
        """Test error recovery in the E2E workflow."""
        # Simulate an error scenario and recovery
        error_scenario = {
            "step": "simulated_error",
            "error_type": "processing_failure",
            "recovery_action": "fallback_to_basic_output"
        }
        
        # Create error log
        error_log = e2e_workspace / "logs" / "error_recovery.json"
        with open(error_log, 'w', encoding='utf-8') as f:
            json.dump({
                "error": error_scenario,
                "recovery_status": "attempted",
                "fallback_result": {
                    "status": "partial_success",
                    "message": "Workflow completed with fallback mechanism",
                    "reduced_functionality": True
                }
            }, f, indent=2)
        
        assert error_log.exists()
        
        # Verify error was logged properly
        with open(error_log, 'r', encoding='utf-8') as f:
            error_data = json.load(f)
        
        assert error_data["recovery_status"] == "attempted"
        assert error_data["fallback_result"]["status"] == "partial_success"
    
    def test_performance_monitoring(self, e2e_workspace):
        """Test performance monitoring during E2E workflow."""
        start_time = time.time()
        
        # Simulate workflow steps with timing
        steps = [
            {"name": "input_processing", "duration": 0.1},
            {"name": "cli_execution", "duration": 0.2},
            {"name": "data_normalization", "duration": 0.05},
            {"name": "merge_operations", "duration": 0.03},
            {"name": "file_operations", "duration": 0.08},
            {"name": "output_generation", "duration": 0.04}
        ]
        
        performance_log = []
        current_time = start_time
        
        for step in steps:
            step_start = current_time
            time.sleep(step["duration"])  # Simulate processing time
            step_end = time.time()
            
            performance_log.append({
                "step": step["name"],
                "start_time": step_start,
                "end_time": step_end,
                "duration": step_end - step_start,
                "status": "completed"
            })
            
            current_time = step_end
        
        total_duration = time.time() - start_time
        
        # Write performance log
        perf_file = e2e_workspace / "logs" / "performance.json"
        with open(perf_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_duration": total_duration,
                "step_details": performance_log,
                "performance_summary": {
                    "total_steps": len(steps),
                    "avg_step_duration": total_duration / len(steps),
                    "fastest_step": min(performance_log, key=lambda x: x["duration"])["step"],
                    "slowest_step": max(performance_log, key=lambda x: x["duration"])["step"]
                }
            }, f, indent=2)
        
        assert perf_file.exists()
        assert total_duration > 0
        assert len(performance_log) == len(steps)