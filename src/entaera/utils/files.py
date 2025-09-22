"""
Day 3 Kata: File Handling and Data Structures
============================================

Learning Objectives:
- File operations with pathlib
- Error handling patterns
- JSON and YAML processing
- Data validation
- Context managers

This module implements file handling utilities for the ENTAERA system.
"""

import json
import os
import sys
import time
import yaml
import csv
import tempfile
import shutil
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Iterator, Tuple, Set, TypeVar

# Set up logging
import logging
logger = logging.getLogger(__name__)


class FileType(str, Enum):
    """Supported file types."""
    JSON = "json"
    YAML = "yaml"
    CSV = "csv"
    TEXT = "txt"
    MARKDOWN = "md"
    UNKNOWN = "unknown"


class FileError(Exception):
    """Base exception for file operations."""
    pass


class FileNotFoundError(FileError):
    """Exception raised when a file is not found."""
    pass


class FilePermissionError(FileError):
    """Exception raised when permission is denied."""
    pass


class FileFormatError(FileError):
    """Exception raised when file format is incorrect."""
    pass


class FileLockError(FileError):
    """Exception raised when file locking fails."""
    pass


class DataFile:
    """
    Class for handling data files with different formats.
    
    Supports reading and writing to JSON, YAML, CSV and text files
    with proper error handling and validation.
    """
    
    def __init__(self, file_path: Union[str, Path], create_if_missing: bool = False):
        """
        Initialize a data file handler.
        
        Args:
            file_path: Path to the file
            create_if_missing: Whether to create parent directories if they don't exist
        """
        self.path = Path(file_path)
        self.file_type = self._determine_file_type()
        
        if create_if_missing and not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create empty file based on type
            if self.file_type == FileType.JSON:
                self.write_json({})
            elif self.file_type == FileType.YAML:
                self.write_yaml({})
            elif self.file_type == FileType.CSV:
                self.write_csv([])
            elif self.file_type == FileType.TEXT or self.file_type == FileType.MARKDOWN:
                self.write_text("")
    
    def _determine_file_type(self) -> FileType:
        """Determine file type from extension."""
        suffix = self.path.suffix.lower().lstrip('.')
        
        if suffix == 'json':
            return FileType.JSON
        elif suffix in ('yaml', 'yml'):
            return FileType.YAML  # Both yaml and yml map to YAML type
        elif suffix == 'csv':
            return FileType.CSV
        elif suffix == 'txt':
            return FileType.TEXT
        elif suffix == 'md':
            return FileType.MARKDOWN
        else:
            return FileType.UNKNOWN
    
    def exists(self) -> bool:
        """Check if file exists."""
        return self.path.exists()
    
    def read_text(self) -> str:
        """Read file as text."""
        try:
            return self.path.read_text(encoding='utf-8')
        except PermissionError:
            logger.error(f"Permission denied when reading {self.path}")
            raise FilePermissionError(f"Permission denied when reading {self.path}")
        except FileNotFoundError:
            logger.error(f"File not found: {self.path}")
            raise FileNotFoundError(f"File not found: {self.path}")
        except Exception as e:
            logger.error(f"Error reading {self.path}: {str(e)}")
            raise FileError(f"Error reading {self.path}: {str(e)}")
    
    def write_text(self, content: str) -> None:
        """Write text to file."""
        try:
            self.path.write_text(content, encoding='utf-8')
        except PermissionError:
            logger.error(f"Permission denied when writing to {self.path}")
            raise FilePermissionError(f"Permission denied when writing to {self.path}")
        except Exception as e:
            logger.error(f"Error writing to {self.path}: {str(e)}")
            raise FileError(f"Error writing to {self.path}: {str(e)}")
    
    def read_json(self) -> Dict[str, Any]:
        """Read JSON file."""
        if self.file_type != FileType.JSON:
            logger.warning(f"Reading {self.path} as JSON, but extension suggests {self.file_type}")
        
        try:
            content = self.read_text()
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in {self.path}: {str(e)}")
            raise FileFormatError(f"Invalid JSON format in {self.path}: {str(e)}")
    
    def write_json(self, data: Any, indent: int = 2, sort_keys: bool = False) -> None:
        """Write data as JSON to file."""
        if self.file_type != FileType.JSON:
            logger.warning(f"Writing {self.path} as JSON, but extension suggests {self.file_type}")
        
        try:
            content = json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
            self.write_text(content)
        except TypeError as e:
            logger.error(f"Data is not JSON serializable: {str(e)}")
            raise FileFormatError(f"Data is not JSON serializable: {str(e)}")
    
    def read_yaml(self) -> Dict[str, Any]:
        """Read YAML file."""
        if self.file_type != FileType.YAML:
            logger.warning(f"Reading {self.path} as YAML, but extension suggests {self.file_type}")
        
        try:
            content = self.read_text()
            return yaml.safe_load(content) or {}
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML format in {self.path}: {str(e)}")
            raise FileFormatError(f"Invalid YAML format in {self.path}: {str(e)}")
    
    def write_yaml(self, data: Any) -> None:
        """Write data as YAML to file."""
        if self.file_type != FileType.YAML:
            logger.warning(f"Writing {self.path} as YAML, but extension suggests {self.file_type}")
        
        try:
            content = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
            self.write_text(content)
        except yaml.YAMLError as e:
            logger.error(f"Data is not YAML serializable: {str(e)}")
            raise FileFormatError(f"Data is not YAML serializable: {str(e)}")
    
    def read_csv(self, has_header: bool = True, delimiter: str = ',') -> List[Dict[str, str]]:
        """
        Read CSV file.
        
        Args:
            has_header: Whether CSV has a header row
            delimiter: CSV delimiter
            
        Returns:
            List of dictionaries (with header) or list of lists (without header)
        """
        if self.file_type != FileType.CSV:
            logger.warning(f"Reading {self.path} as CSV, but extension suggests {self.file_type}")
        
        try:
            with self.path.open('r', newline='', encoding='utf-8') as f:
                if has_header:
                    reader = csv.DictReader(f, delimiter=delimiter)
                    return list(reader)
                else:
                    reader = csv.reader(f, delimiter=delimiter)
                    return list(reader)
        except csv.Error as e:
            logger.error(f"Invalid CSV format in {self.path}: {str(e)}")
            raise FileFormatError(f"Invalid CSV format in {self.path}: {str(e)}")
    
    def write_csv(
        self, 
        data: Union[List[Dict[str, Any]], List[List[Any]]],
        header: Optional[List[str]] = None,
        delimiter: str = ','
    ) -> None:
        """
        Write data as CSV to file.
        
        Args:
            data: List of dictionaries or list of lists
            header: CSV header (required if data is list of lists)
            delimiter: CSV delimiter
        """
        if self.file_type != FileType.CSV:
            logger.warning(f"Writing {self.path} as CSV, but extension suggests {self.file_type}")
        
        try:
            with self.path.open('w', newline='', encoding='utf-8') as f:
                if data and isinstance(data[0], dict):
                    # Data is a list of dictionaries
                    fieldnames = header or data[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    # Data is a list of lists
                    writer = csv.writer(f, delimiter=delimiter)
                    if header:
                        writer.writerow(header)
                    writer.writerows(data)
        except csv.Error as e:
            logger.error(f"Error writing CSV to {self.path}: {str(e)}")
            raise FileFormatError(f"Error writing CSV to {self.path}: {str(e)}")
    
    @contextmanager
    def atomic_write(self) -> Iterator[Path]:
        """
        Context manager for atomic file writes.
        
        Uses a temporary file for writing and then renames to target
        file to ensure atomic operation.
        
        Yields:
            Path to temporary file
        """
        # Create temporary file in the same directory
        temp_file = self.path.with_name(f".{self.path.name}.{int(time.time())}.tmp")
        
        try:
            yield temp_file
            
            # If no exception occurred, atomically replace the target file
            if os.name == 'nt':  # Windows
                # Windows needs special handling for atomic replace
                if self.path.exists():
                    self.path.unlink()
                temp_file.rename(self.path)
            else:
                # POSIX systems support atomic rename
                temp_file.rename(self.path)
                
        except Exception as e:
            # Clean up temporary file if an exception occurred
            if temp_file.exists():
                temp_file.unlink()
            raise e
    
    def atomic_json_write(self, data: Any, indent: int = 2, sort_keys: bool = False) -> None:
        """
        Atomically write JSON data to file.
        
        Args:
            data: Data to write
            indent: JSON indentation
            sort_keys: Whether to sort keys
        """
        with self.atomic_write() as temp_path:
            # Write to temporary file
            content = json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
            temp_path.write_text(content, encoding='utf-8')
    
    def backup(self, backup_dir: Optional[Union[str, Path]] = None) -> Path:
        """
        Create a backup of the file.
        
        Args:
            backup_dir: Directory for backups (defaults to same directory)
            
        Returns:
            Path to the backup file
        """
        if not self.exists():
            raise FileNotFoundError(f"Cannot backup non-existent file: {self.path}")
        
        # Default backup directory is the same as the file
        if backup_dir is None:
            backup_dir = self.path.parent
        else:
            backup_dir = Path(backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.path.stem}_{timestamp}{self.path.suffix}"
        backup_path = backup_dir / backup_name
        
        # Create backup
        try:
            shutil.copy2(self.path, backup_path)
            logger.info(f"Created backup of {self.path} at {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup of {self.path}: {str(e)}")
            raise FileError(f"Failed to create backup of {self.path}: {str(e)}")


class DirectoryManager:
    """
    Utility class for directory operations.
    
    Provides functionality for scanning directories, finding files,
    and managing directory structures.
    """
    
    def __init__(self, base_dir: Union[str, Path]):
        """
        Initialize directory manager.
        
        Args:
            base_dir: Base directory path
        """
        self.base_dir = Path(base_dir)
        
        if not self.base_dir.exists():
            logger.warning(f"Directory {self.base_dir} does not exist")
    
    def ensure_exists(self) -> None:
        """Ensure the base directory exists."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {self.base_dir}")
    
    def list_files(
        self, 
        pattern: str = "*", 
        recursive: bool = False,
        only_files: bool = True
    ) -> List[Path]:
        """
        List files in the directory.
        
        Args:
            pattern: Glob pattern for file matching
            recursive: Whether to search recursively
            only_files: Whether to include only files (not directories)
            
        Returns:
            List of matching file paths
        """
        if not self.base_dir.exists():
            return []
        
        if recursive:
            matches = list(self.base_dir.glob(f"**/{pattern}"))
        else:
            matches = list(self.base_dir.glob(pattern))
        
        if only_files:
            return [p for p in matches if p.is_file()]
        return matches
    
    def find_by_extension(
        self, 
        extension: str,
        recursive: bool = True
    ) -> List[Path]:
        """
        Find files by extension.
        
        Args:
            extension: File extension (with or without leading dot)
            recursive: Whether to search recursively
            
        Returns:
            List of matching file paths
        """
        # Normalize extension to have leading dot
        if extension and not extension.startswith('.'):
            extension = f".{extension}"
        
        return self.list_files(f"*{extension}", recursive=recursive, only_files=True)
    
    def find_by_name(
        self, 
        name: str,
        recursive: bool = True,
        case_sensitive: bool = True
    ) -> List[Path]:
        """
        Find files by name.
        
        Args:
            name: File name or partial name
            recursive: Whether to search recursively
            case_sensitive: Whether search is case sensitive
            
        Returns:
            List of matching file paths
        """
        all_files = self.list_files(recursive=recursive)
        
        if case_sensitive:
            return [p for p in all_files if name in p.name]
        else:
            name_lower = name.lower()
            return [p for p in all_files if name_lower in p.name.lower()]
    
    def find_newest(
        self, 
        pattern: str = "*", 
        count: int = 1
    ) -> List[Path]:
        """
        Find newest files matching pattern.
        
        Args:
            pattern: Glob pattern for file matching
            count: Number of newest files to return
            
        Returns:
            List of newest file paths
        """
        files = self.list_files(pattern=pattern, recursive=True)
        
        # Sort by modification time (newest first)
        sorted_files = sorted(
            files,
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        return sorted_files[:count]
    
    def get_file_stats(self, pattern: str = "*") -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for files matching pattern.
        
        Args:
            pattern: Glob pattern for file matching
            
        Returns:
            Dictionary with file statistics
        """
        files = self.list_files(pattern=pattern, recursive=True)
        stats = {}
        
        for file_path in files:
            try:
                stat = file_path.stat()
                rel_path = file_path.relative_to(self.base_dir)
                
                stats[str(rel_path)] = {
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'is_file': file_path.is_file(),
                    'extension': file_path.suffix,
                }
            except Exception as e:
                logger.warning(f"Error getting stats for {file_path}: {e}")
        
        return stats
    
    def clear_directory(
        self, 
        pattern: str = "*", 
        recursive: bool = False,
        exclude: Optional[List[str]] = None
    ) -> int:
        """
        Clear files in directory.
        
        Args:
            pattern: Glob pattern for file matching
            recursive: Whether to delete recursively
            exclude: List of patterns to exclude
            
        Returns:
            Number of files deleted
        """
        exclude = exclude or []
        files = self.list_files(pattern=pattern, recursive=recursive)
        
        # Filter out excluded files
        if exclude:
            for excl in exclude:
                files = [f for f in files if not f.match(excl)]
        
        # Delete files
        deleted = 0
        for file_path in files:
            try:
                file_path.unlink()
                deleted += 1
            except Exception as e:
                logger.error(f"Error deleting {file_path}: {e}")
        
        logger.info(f"Deleted {deleted} files from {self.base_dir}")
        return deleted
    
    @contextmanager
    def temp_dir(self) -> Iterator[Path]:
        """
        Create a temporary directory within the base directory.
        
        Yields:
            Path to temporary directory
        """
        temp_dir = self.base_dir / f"tmp_{int(time.time())}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            yield temp_dir
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


# Helper functions for common file operations
def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary with JSON data
    """
    data_file = DataFile(file_path)
    return data_file.read_json()


def write_json_file(file_path: Union[str, Path], data: Any) -> None:
    """
    Write data to JSON file.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
    """
    data_file = DataFile(file_path, create_if_missing=True)
    data_file.write_json(data)


def read_yaml_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read YAML file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Dictionary with YAML data
    """
    data_file = DataFile(file_path)
    return data_file.read_yaml()


def write_yaml_file(file_path: Union[str, Path], data: Any) -> None:
    """
    Write data to YAML file.
    
    Args:
        file_path: Path to YAML file
        data: Data to write
    """
    data_file = DataFile(file_path, create_if_missing=True)
    data_file.write_yaml(data)


def ensure_directory(dir_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists.
    
    Args:
        dir_path: Directory path
        
    Returns:
        Path object to the directory
    """
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_delete(file_path: Union[str, Path]) -> bool:
    """
    Safely delete a file or directory.
    
    Args:
        file_path: Path to file or directory
        
    Returns:
        True if deletion was successful, False otherwise
    """
    path = Path(file_path)
    
    if not path.exists():
        return False
    
    try:
        if path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
        return True
    except Exception as e:
        logger.error(f"Failed to delete {path}: {e}")
        return False


# Kata practice function
def kata_practice_file_handling() -> Dict[str, Any]:
    """
    Practice function for file handling kata.
    
    Returns:
        Dictionary with results of file handling operations
    """
    results = {
        "operations_performed": [],
        "successful_operations": 0,
        "failed_operations": 0,
        "error_handling_tested": False,
        "atomic_operations_tested": False,
        "backup_tested": False,
        "temporary_files": 0,
        "json_operations": 0,
        "yaml_operations": 0,
        "csv_operations": 0,
        "text_operations": 0,
    }
    
    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 1. Test JSON file operations
            json_file = temp_path / "test_data.json"
            test_data = {"name": "Kata Practice", "version": 1, "tags": ["file", "handling"]}
            
            # Write JSON
            data_file = DataFile(json_file)
            data_file.write_json(test_data)
            results["operations_performed"].append("json_write")
            results["successful_operations"] += 1
            results["json_operations"] += 1
            
            # Read JSON
            read_data = data_file.read_json()
            assert read_data == test_data
            results["operations_performed"].append("json_read")
            results["successful_operations"] += 1
            results["json_operations"] += 1
            
            # 2. Test YAML file operations
            yaml_file = temp_path / "test_data.yaml"
            yaml_data = {
                "config": {
                    "server": "localhost",
                    "ports": [8000, 8001, 8002],
                    "debug": True
                }
            }
            
            # Write YAML
            yaml_data_file = DataFile(yaml_file)
            yaml_data_file.write_yaml(yaml_data)
            results["operations_performed"].append("yaml_write")
            results["successful_operations"] += 1
            results["yaml_operations"] += 1
            
            # Read YAML
            read_yaml = yaml_data_file.read_yaml()
            assert read_yaml["config"]["server"] == "localhost"
            results["operations_performed"].append("yaml_read")
            results["successful_operations"] += 1
            results["yaml_operations"] += 1
            
            # 3. Test CSV file operations
            csv_file = temp_path / "test_data.csv"
            csv_data = [
                {"name": "Alice", "age": "30", "role": "Developer"},
                {"name": "Bob", "age": "25", "role": "Designer"},
                {"name": "Carol", "age": "35", "role": "Manager"}
            ]
            
            # Write CSV
            csv_data_file = DataFile(csv_file)
            csv_data_file.write_csv(csv_data)
            results["operations_performed"].append("csv_write")
            results["successful_operations"] += 1
            results["csv_operations"] += 1
            
            # Read CSV
            read_csv = csv_data_file.read_csv()
            assert len(read_csv) == 3
            assert read_csv[0]["name"] == "Alice"
            results["operations_performed"].append("csv_read")
            results["successful_operations"] += 1
            results["csv_operations"] += 1
            
            # 4. Test text file operations
            text_file = temp_path / "test_data.txt"
            text_data = "This is a test file.\nIt has multiple lines.\nEnd of file."
            
            # Write text
            text_data_file = DataFile(text_file)
            text_data_file.write_text(text_data)
            results["operations_performed"].append("text_write")
            results["successful_operations"] += 1
            results["text_operations"] += 1
            
            # Read text
            read_text = text_data_file.read_text()
            assert read_text == text_data
            results["operations_performed"].append("text_read")
            results["successful_operations"] += 1
            results["text_operations"] += 1
            
            # 5. Test error handling
            results["error_handling_tested"] = True
            
            try:
                non_existent = DataFile(temp_path / "non_existent.json")
                non_existent.read_json()
                results["failed_operations"] += 1
            except (FileNotFoundError, FileError):
                # Expected error - either custom FileError or built-in FileNotFoundError
                results["operations_performed"].append("error_handling_file_not_found")
                results["successful_operations"] += 1
            
            try:
                invalid_json = temp_path / "invalid.json"
                invalid_json.write_text("{invalid: json,}", encoding="utf-8")
                
                invalid_file = DataFile(invalid_json)
                invalid_file.read_json()
                results["failed_operations"] += 1
            except FileFormatError:
                # Expected error
                results["operations_performed"].append("error_handling_invalid_format")
                results["successful_operations"] += 1
            
            # 6. Test atomic operations
            results["atomic_operations_tested"] = True
            atomic_file = temp_path / "atomic.json"
            
            data_file = DataFile(atomic_file)
            with data_file.atomic_write() as tmp:
                tmp.write_text('{"atomic": true}', encoding="utf-8")
            
            assert atomic_file.exists()
            assert json.loads(atomic_file.read_text(encoding="utf-8"))["atomic"] is True
            results["operations_performed"].append("atomic_write")
            results["successful_operations"] += 1
            
            # 7. Test backups
            results["backup_tested"] = True
            backup_file = temp_path / "backup.txt"
            backup_file.write_text("Original content", encoding="utf-8")
            
            backup_data = DataFile(backup_file)
            backup_path = backup_data.backup(temp_path / "backups")
            
            assert backup_path.exists()
            assert "backup_" in backup_path.name
            results["operations_performed"].append("backup_creation")
            results["successful_operations"] += 1
            
            # 8. Test directory operations
            dir_manager = DirectoryManager(temp_path)
            dir_manager.ensure_exists()
            
            # Create test files for directory operations
            (temp_path / "file1.txt").write_text("File 1", encoding="utf-8")
            (temp_path / "file2.json").write_text("{}", encoding="utf-8")
            (temp_path / "subdir").mkdir()
            (temp_path / "subdir" / "file3.txt").write_text("File 3", encoding="utf-8")
            
            # List files
            txt_files = dir_manager.find_by_extension(".txt")
            # Make sure we found at least one txt file
            assert len(txt_files) >= 1
            results["operations_performed"].append("directory_find_by_extension")
            results["successful_operations"] += 1
            
            # Find by name
            found = dir_manager.find_by_name("file")
            assert len(found) == 3
            results["operations_performed"].append("directory_find_by_name")
            results["successful_operations"] += 1
            
            # Get stats
            stats = dir_manager.get_file_stats()
            assert len(stats) >= 3
            results["operations_performed"].append("directory_get_stats")
            results["successful_operations"] += 1
            
            # Test temporary directory
            with dir_manager.temp_dir() as tmp_dir:
                (tmp_dir / "temp_file.txt").write_text("Temporary", encoding="utf-8")
                assert (tmp_dir / "temp_file.txt").exists()
                results["temporary_files"] += 1
            
            # Temp dir should be deleted after context manager exits
            assert not (temp_path / "tmp_").exists()
            results["operations_performed"].append("directory_temp_dir")
            results["successful_operations"] += 1
        
        # Calculate statistics for results
        results["total_operations"] = len(results["operations_performed"])
        results["success_rate"] = (
            results["successful_operations"] / 
            (results["successful_operations"] + results["failed_operations"])
            if results["successful_operations"] + results["failed_operations"] > 0
            else 0
        ) * 100
        
        return results
    
    except Exception as e:
        logger.exception("Error in kata practice")
        results["error"] = str(e)
        return results


if __name__ == "__main__":
    # Kata demonstration
    print("\n🥋 Day 3 Kata: File Handling and Data Structures Demo")
    print("=" * 60)
    
    # Configure basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the kata practice function
    print("\nRunning file handling practice...")
    results = kata_practice_file_handling()
    
    # Display results
    print(f"\n✅ Total operations: {results.get('total_operations', 0)}")
    print(f"✅ Successful: {results.get('successful_operations', 0)}")
    print(f"❌ Failed: {results.get('failed_operations', 0)}")
    print(f"📊 Success rate: {results.get('success_rate', 0):.2f}%")
    
    print("\n🔍 Operations by type:")
    print(f"  • JSON: {results.get('json_operations', 0)}")
    print(f"  • YAML: {results.get('yaml_operations', 0)}")
    print(f"  • CSV: {results.get('csv_operations', 0)}")
    print(f"  • Text: {results.get('text_operations', 0)}")
    print(f"  • Temp files: {results.get('temporary_files', 0)}")
    
    print("\n🧪 Features tested:")
    print(f"  • Error handling: {'✅' if results.get('error_handling_tested') else '❌'}")
    print(f"  • Atomic operations: {'✅' if results.get('atomic_operations_tested') else '❌'}")
    print(f"  • Backups: {'✅' if results.get('backup_tested') else '❌'}")
    
    if "error" in results:
        print(f"\n❌ Error: {results['error']}")
    else:
        print("\n🎉 Day 3 Kata completed successfully!")
    
    print("\n📝 Learning objectives achieved:")
    print("  • File operations with pathlib")
    print("  • Error handling patterns")
    print("  • JSON and YAML processing")
    print("  • Data validation")
    print("  • Context managers")