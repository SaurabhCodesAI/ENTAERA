"""Unit tests for CLI functionality."""
import json
import sys
import subprocess
from pathlib import Path

import pytest


class TestCLI:
    """Test both CLI entry points."""
    
    def test_root_cli_json_output(self):
        """Test that cli.py produces valid JSON output."""
        result = subprocess.run(
            [sys.executable, "cli.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent
        )
        
        assert result.returncode == 0
        
        # Parse JSON output
        output_data = json.loads(result.stdout.strip())
        
        # Validate expected structure
        assert output_data["status"] == "success"
        assert "topic" in output_data
        assert "source" in output_data
        assert "summary" in output_data
        
    def test_src_cli_json_output(self):
        """Test that src/cli.py produces valid JSON output with Unicode support."""
        result = subprocess.run(
            [sys.executable, "src/cli.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=Path(__file__).parent.parent.parent
        )
        
        assert result.returncode == 0
        
        # Parse JSON output
        output_data = json.loads(result.stdout.strip())
        
        # Validate expected structure
        assert output_data["status"] == "success"
        assert "🔥" in output_data["message"]  # Unicode fire emoji
        assert "python_executable" in output_data
        assert "version_info" in output_data
        
    def test_cli_outputs_are_different(self):
        """Ensure both CLIs serve different purposes."""
        result1 = subprocess.run(
            [sys.executable, "cli.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent
        )
        
        result2 = subprocess.run(
            [sys.executable, "src/cli.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=Path(__file__).parent.parent.parent
        )
        
        output1 = json.loads(result1.stdout.strip())
        output2 = json.loads(result2.stdout.strip())
        
        # They should have different content/purpose
        assert output1 != output2
        assert "topic" in output1  # Research-focused
        assert "python_executable" in output2  # System info focused