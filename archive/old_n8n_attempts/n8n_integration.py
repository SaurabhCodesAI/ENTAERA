"""
n8n Integration for VertexAutoGPT

This script provides n8n-compatible endpoints and functions that can be called
from n8n workflows to integrate with your VertexAutoGPT workspace.
"""

import sys
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import argparse
from datetime import datetime
import hashlib

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from vertexautogpt.core.data_processor import VertexDataProcessor
except ImportError:
    print("Error: Could not import data processor. Run from project root.")
    sys.exit(1)


class N8nIntegration:
    """Integration layer between n8n and VertexAutoGPT workspace."""
    
    def __init__(self):
        self.processor = VertexDataProcessor()
        self.workspace_root = Path(__file__).parent
        
    def process_webhook_data(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data received from n8n webhook.
        
        Expected webhook format:
        {
            "content": "text content",
            "source": "WhatsApp|Google|TestData",
            "type": "summary|raw|embedding|analysis",
            "metadata": {...}
        }
        """
        try:
            # Validate required fields
            if "content" not in webhook_data:
                raise ValueError("Missing required field: content")
            
            content = webhook_data["content"]
            source = webhook_data.get("source", "n8n")
            data_type = webhook_data.get("type", "summary")
            
            # Process the data
            result = self.processor.process_data(
                content=content,
                source=source,
                data_type=data_type
            )
            
            return {
                "status": "success",
                "message": "Data processed successfully",
                "file_path": str(result["file_path"]),
                "hash": result["hash"],
                "timestamp": result["timestamp"],
                "git_commit": "completed",
                "n8n_compatible": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "error_type": type(e).__name__,
                "n8n_compatible": True
            }
    
    def validate_workspace(self) -> Dict[str, Any]:
        """
        Run workspace validation for n8n monitoring.
        Returns n8n-compatible status object.
        """
        try:
            # Run the validation script
            result = subprocess.run(
                [sys.executable, "phase1_validation.py"],
                capture_output=True,
                text=True,
                cwd=self.workspace_root
            )
            
            validation_passed = result.returncode == 0
            
            return {
                "status": "success" if validation_passed else "warning",
                "validation_passed": validation_passed,
                "details": "Validation completed - check logs for details",
                "errors": result.stderr if result.stderr else None,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "n8n_compatible": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "n8n_compatible": True
            }
    
    def get_latest_files(self, data_type: str = "summary", limit: int = 5) -> Dict[str, Any]:
        """
        Get latest files for n8n file monitoring.
        """
        try:
            data_dir = self.workspace_root / "data" / data_type
            
            if not data_dir.exists():
                return {
                    "status": "warning",
                    "message": f"Directory {data_type} not found",
                    "files": [],
                    "n8n_compatible": True
                }
            
            files = []
            for file_path in sorted(data_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        content = json.load(f)
                    
                    files.append({
                        "filename": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() + "Z",
                        "hash": content.get("metadata", {}).get("hash", ""),
                        "type": content.get("type", data_type)
                    })
                except Exception as e:
                    files.append({
                        "filename": file_path.name,
                        "path": str(file_path),
                        "error": str(e)
                    })
            
            return {
                "status": "success",
                "files": files,
                "count": len(files),
                "data_type": data_type,
                "n8n_compatible": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "n8n_compatible": True
            }
    
    def git_status(self) -> Dict[str, Any]:
        """
        Get git status for n8n git monitoring.
        """
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.workspace_root
            )
            
            # Get recent commits
            log_result = subprocess.run(
                ["git", "log", "-n", "10", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.workspace_root
            )
            
            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.workspace_root
            )
            
            return {
                "status": "success",
                "current_branch": branch_result.stdout.strip(),
                "recent_commits": log_result.stdout.strip().split('\n') if log_result.stdout.strip() else [],
                "uncommitted_changes": status_result.stdout.strip().split('\n') if status_result.stdout.strip() else [],
                "has_changes": bool(status_result.stdout.strip()),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "n8n_compatible": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "n8n_compatible": True
            }
    
    def upload_simulation(self, file_path: str) -> Dict[str, Any]:
        """
        Simulate file upload for n8n compatibility.
        In real scenario, this would upload to your cloud storage.
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}",
                    "n8n_compatible": True
                }
            
            # Simulate upload response
            file_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
            
            return {
                "status": "success",
                "message": "File upload simulated successfully",
                "file_id": f"vertex_upload_{file_hash}",
                "file_size": path.stat().st_size,
                "upload_url": f"https://storage.example.com/vertex/{path.name}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "n8n_compatible": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "n8n_compatible": True
            }


def main():
    """CLI interface for n8n integration."""
    
    parser = argparse.ArgumentParser(description="n8n Integration for VertexAutoGPT")
    parser.add_argument("action", choices=[
        "process", "validate", "files", "git", "upload"
    ], help="Action to perform")
    parser.add_argument("--data", type=str, help="JSON data for processing")
    parser.add_argument("--file", type=str, help="File path for upload")
    parser.add_argument("--type", type=str, default="summary", help="Data type")
    parser.add_argument("--limit", type=int, default=5, help="File limit")
    
    args = parser.parse_args()
    
    integration = N8nIntegration()
    
    if args.action == "process":
        if not args.data:
            print(json.dumps({
                "status": "error",
                "message": "Missing --data parameter",
                "n8n_compatible": True
            }))
            return
        
        try:
            webhook_data = json.loads(args.data)
            result = integration.process_webhook_data(webhook_data)
        except json.JSONDecodeError:
            result = {
                "status": "error",
                "message": "Invalid JSON in --data parameter",
                "n8n_compatible": True
            }
    
    elif args.action == "validate":
        result = integration.validate_workspace()
    
    elif args.action == "files":
        result = integration.get_latest_files(args.type, args.limit)
    
    elif args.action == "git":
        result = integration.git_status()
    
    elif args.action == "upload":
        if not args.file:
            result = {
                "status": "error",
                "message": "Missing --file parameter",
                "n8n_compatible": True
            }
        else:
            result = integration.upload_simulation(args.file)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()