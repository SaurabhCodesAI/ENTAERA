"""
VertexAutoGPT Data Processor

This module implements the core data processing pipeline that matches
the validation checklist requirements, including:
- JSON schema validation  
- Hash verification
- File routing by type
- ISO8601 timestamp formatting
- Git automation
- Error handling
- Logging
"""

import json
import hashlib
import datetime
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import jsonschema


class VertexDataProcessor:
    """Main data processor following validation checklist requirements."""
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.data_dir = self.workspace_root / "data"
        self.logs_dir = self.workspace_root / "logs"
        self.docs_dir = self.workspace_root / "docs"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        (self.data_dir / "summary").mkdir(exist_ok=True)
        (self.data_dir / "raw").mkdir(exist_ok=True)
        (self.data_dir / "embeddings").mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Load schema
        self.schema = self._load_schema()
    
    def _setup_logging(self):
        """Setup workflow and error logging."""
        # Workflow logger
        self.workflow_logger = logging.getLogger('workflow')
        self.workflow_logger.setLevel(logging.INFO)
        workflow_handler = logging.FileHandler(self.logs_dir / "workflow.log")
        workflow_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.workflow_logger.addHandler(workflow_handler)
        
        # Error logger
        self.error_logger = logging.getLogger('errors')
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self.logs_dir / "errors.log")
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s - %(exc_info)s'
        ))
        self.error_logger.addHandler(error_handler)
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for validation."""
        schema_path = self.docs_dir / "schema.json"
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            self.error_logger.error(f"Schema file not found: {schema_path}")
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    def _generate_iso8601_timestamp(self) -> str:
        """Generate ISO8601 timestamp with milliseconds and Z suffix."""
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    def _calculate_file_hash(self, content: str) -> str:
        """Calculate 8-character SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]
    
    def _validate_payload(self, payload: Dict[str, Any]) -> bool:
        """Validate payload against schema."""
        try:
            jsonschema.validate(payload, self.schema)
            return True
        except jsonschema.ValidationError as e:
            self.error_logger.error(f"Invalid payload: {e.message}")
            raise ValueError(f"Invalid payload: {e.message}")
    
    def _route_file_by_type(self, data_type: str, filename: str) -> Path:
        """Route file to appropriate directory based on type."""
        type_mapping = {
            "summary": self.data_dir / "summary",
            "raw": self.data_dir / "raw", 
            "embedding": self.data_dir / "embeddings",
            "analysis": self.data_dir / "summary"  # Analysis goes to summary folder
        }
        
        if data_type not in type_mapping:
            raise ValueError(f"Unknown data type: {data_type}")
        
        return type_mapping[data_type] / filename
    
    def process_data(self, content: str, source: str, data_type: str = "summary") -> Dict[str, Any]:
        """
        Process data according to validation checklist requirements.
        
        Args:
            content: The main content/summary
            source: Source of the data (WhatsApp, Google, manual_test, etc.)
            data_type: Type of data (summary, raw, embedding, analysis)
            
        Returns:
            Dict containing processing results and file path
        """
        try:
            # Step 1: Create payload with required schema fields
            timestamp = self._generate_iso8601_timestamp()
            
            payload = {
                "type": data_type,
                "content": content,
                "source": source,
                "metadata": {
                    "version": 1
                },
                "timestamp": timestamp
            }
            
            # Step 2: Calculate hash (before adding hash to avoid circular reference)
            temp_content = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
            content_hash = self._calculate_file_hash(temp_content)
            payload["metadata"]["hash"] = content_hash
            
            # Step 3: Add file metadata
            filename = f"{content_hash}.json"
            file_path = self._route_file_by_type(data_type, filename)
            
            payload["file"] = {
                "filename": filename,
                "mimetype": "application/json"
            }
            payload["fileName"] = str(file_path)
            
            # Step 4: Validate against schema
            self._validate_payload(payload)
            
            # Step 5: Write file with proper encoding
            self._write_json_file(file_path, payload)
            
            # Step 6: Log successful processing
            self.workflow_logger.info(f"Processed {data_type} data: {filename}")
            
            # Step 7: Git commit automation
            self._git_commit_automation(file_path, data_type, content_hash)
            
            return {
                "success": True,
                "file_path": str(file_path),
                "hash": content_hash,
                "timestamp": timestamp,
                "payload": payload
            }
            
        except Exception as e:
            self.error_logger.error(f"Failed to process data: {e}", exc_info=True)
            raise
    
    def _write_json_file(self, file_path: Path, payload: Dict[str, Any]):
        """Write JSON file with proper encoding and formatting."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.error_logger.error(f"Failed to write file {file_path}: {e}")
            raise
    
    def _git_commit_automation(self, file_path: Path, data_type: str, content_hash: str):
        """Automated git commit for processed data."""
        try:
            # Add the specific file
            subprocess.run(['git', 'add', str(file_path)], 
                         cwd=self.workspace_root, check=True, capture_output=True)
            
            # Create commit with standardized message format
            commit_message = f"[type:{data_type}] Automated commit for {content_hash}"
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         cwd=self.workspace_root, check=True, capture_output=True)
            
            self.workflow_logger.info(f"Git commit successful: {commit_message}")
            
        except subprocess.CalledProcessError as e:
            self.workflow_logger.warning(f"Git commit failed: {e}")
            # Don't raise error for git failures - processing should continue
    
    def verify_file_integrity(self, file_path: Path) -> bool:
        """Verify file hash matches metadata.hash."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                payload = json.load(f)
            
            # Recalculate hash without the hash field
            temp_payload = payload.copy()
            stored_hash = temp_payload["metadata"].pop("hash")
            
            calculated_hash = self._calculate_file_hash(
                json.dumps(temp_payload, ensure_ascii=False, separators=(',', ':'))
            )
            
            return calculated_hash == stored_hash
            
        except Exception as e:
            self.error_logger.error(f"Hash verification failed for {file_path}: {e}")
            return False
    
    def get_git_status(self) -> Dict[str, Any]:
        """Get current git status and recent commits."""
        try:
            # Current branch
            branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                         cwd=self.workspace_root, capture_output=True, text=True)
            current_branch = branch_result.stdout.strip()
            
            # Recent commits
            log_result = subprocess.run(['git', 'log', '-n', '10', '--oneline'], 
                                      cwd=self.workspace_root, capture_output=True, text=True)
            recent_commits = log_result.stdout.strip().split('\n') if log_result.stdout else []
            
            # Remote info
            remote_result = subprocess.run(['git', 'remote', '-v'], 
                                         cwd=self.workspace_root, capture_output=True, text=True)
            remotes = remote_result.stdout.strip().split('\n') if remote_result.stdout else []
            
            return {
                "current_branch": current_branch,
                "recent_commits": recent_commits,
                "remotes": remotes
            }
            
        except subprocess.CalledProcessError as e:
            self.error_logger.error(f"Git status check failed: {e}")
            return {"error": str(e)}
    
    def test_invalid_payload(self) -> Dict[str, Any]:
        """Test error handling with invalid payload."""
        try:
            # Intentionally invalid payload (missing required 'type' field)
            invalid_payload = {
                "content": "Test content",
                "source": "test"
                # Missing 'type', 'metadata', 'timestamp'
            }
            
            self._validate_payload(invalid_payload)
            return {"error": "Validation should have failed but didn't"}
            
        except ValueError as e:
            self.error_logger.info(f"Invalid payload correctly rejected: {e}")
            return {
                "success": True,
                "error_message": str(e),
                "error_type": "ValidationError"
            }
    
    def get_file_stats(self) -> Dict[str, Any]:
        """Get file statistics for each data type folder."""
        stats = {}
        
        for folder_name in ["summary", "raw", "embeddings"]:
            folder_path = self.data_dir / folder_name
            if folder_path.exists():
                files = list(folder_path.glob("*.json"))
                stats[folder_name] = {
                    "count": len(files),
                    "files": [
                        {
                            "name": f.name,
                            "size": f.stat().st_size,
                            "modified": datetime.datetime.fromtimestamp(
                                f.stat().st_mtime
                            ).isoformat()
                        }
                        for f in files[:5]  # Show first 5 files
                    ]
                }
            else:
                stats[folder_name] = {"count": 0, "files": []}
        
        return stats