"""
Robust File Operations for ENTAERA - Kata 3.1

This module provides safe, atomic file operations with comprehensive error handling.
Includes directory management, JSON serialization, atomic writes, and backup operations.

Kata Learning Objectives:
- File I/O with proper error handling
- Atomic file operations for data safety
- Directory creation and management
- JSON serialization with validation
- Backup and recovery mechanisms
- Context managers for resource safety
"""

import os
import json
import shutil
import tempfile
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, IO, Callable
from contextlib import contextmanager
from datetime import datetime
import stat

# Conditional import for Unix-only modules
try:
    import fcntl
except ImportError:
    fcntl = None  # Windows doesn't have fcntl

from ..core.logger import get_logger

logger = get_logger(__name__)


class FileOperationError(Exception):
    """Custom exception for file operation errors."""
    pass


class FileValidationError(FileOperationError):
    """Exception for file validation errors."""
    pass


class AtomicFileWriter:
    """
    Context manager for atomic file writes.
    
    Ensures that either the entire file write succeeds or no changes are made.
    Uses temporary files and atomic moves to prevent data corruption.
    """
    
    def __init__(self, target_path: Union[str, Path], mode: str = 'w', 
                 encoding: str = 'utf-8', backup: bool = True):
        self.target_path = Path(target_path)
        self.mode = mode
        self.encoding = encoding
        self.backup = backup
        self.temp_file = None
        self.backup_path = None
        
    def __enter__(self) -> IO:
        """Enter the context manager and return a temporary file handle."""
        # Create parent directory if it doesn't exist
        self.target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create backup if file exists and backup is enabled
        if self.backup and self.target_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_path = self.target_path.with_suffix(f'.backup_{timestamp}')
            shutil.copy2(self.target_path, self.backup_path)
            logger.debug(f"Created backup: {self.backup_path}")
        
        # Create temporary file in the same directory as target
        temp_dir = self.target_path.parent
        self.temp_file = tempfile.NamedTemporaryFile(
            mode=self.mode,
            encoding=self.encoding if 'b' not in self.mode else None,
            dir=temp_dir,
            delete=False,
            prefix=f'.{self.target_path.name}.',
            suffix='.tmp'
        )
        
        logger.debug(f"Created temporary file: {self.temp_file.name}")
        return self.temp_file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager and perform atomic move or cleanup."""
        try:
            if self.temp_file:
                self.temp_file.close()
                
                if exc_type is None:
                    # Success: atomically move temp file to target
                    temp_path = Path(self.temp_file.name)
                    if os.name == 'nt':  # Windows
                        # On Windows, we need to remove target first
                        if self.target_path.exists():
                            self.target_path.unlink()
                    temp_path.replace(self.target_path)
                    logger.info(f"Atomically wrote file: {self.target_path}")
                    
                    # Clean up backup if write was successful
                    if self.backup_path and self.backup_path.exists():
                        self.backup_path.unlink()
                        logger.debug(f"Removed backup: {self.backup_path}")
                        
                else:
                    # Failure: clean up temp file and restore backup
                    temp_path = Path(self.temp_file.name)
                    if temp_path.exists():
                        temp_path.unlink()
                    
                    if self.backup_path and self.backup_path.exists():
                        shutil.move(str(self.backup_path), str(self.target_path))
                        logger.warning(f"Restored backup due to write failure: {self.target_path}")
                    
                    logger.error(f"Failed to write file: {self.target_path}, error: {exc_val}")
                    
        except Exception as cleanup_error:
            logger.error(f"Error during cleanup: {cleanup_error}")
            raise FileOperationError(f"File operation failed with cleanup error: {cleanup_error}") from cleanup_error


class FileManager:
    """Comprehensive file operations manager with safety features."""
    
    def __init__(self, base_path: Optional[Union[str, Path]] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        logger.debug(f"FileManager initialized with base path: {self.base_path}")
    
    def ensure_directory(self, path: Union[str, Path], permissions: int = 0o755) -> Path:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            path: Directory path to create
            permissions: Unix permissions for the directory
            
        Returns:
            Path object for the created directory
            
        Raises:
            FileOperationError: If directory creation fails
        """
        dir_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Set permissions on Unix-like systems
            if os.name != 'nt':
                dir_path.chmod(permissions)
            
            logger.debug(f"Ensured directory exists: {dir_path}")
            return dir_path
            
        except OSError as e:
            error_msg = f"Failed to create directory {dir_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def write_text_file(self, path: Union[str, Path], content: str, 
                       encoding: str = 'utf-8', atomic: bool = True) -> None:
        """
        Write text content to a file safely.
        
        Args:
            path: File path to write to
            content: Text content to write
            encoding: Text encoding
            atomic: Whether to use atomic writes
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if atomic:
                with AtomicFileWriter(file_path, mode='w', encoding=encoding) as f:
                    f.write(content)
            else:
                self.ensure_directory(file_path.parent)
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(content)
            
            logger.info(f"Wrote text file: {file_path} ({len(content)} chars)")
            
        except Exception as e:
            error_msg = f"Failed to write text file {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def read_text_file(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Read text content from a file safely.
        
        Args:
            path: File path to read from
            encoding: Text encoding
            
        Returns:
            File content as string
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            logger.debug(f"Read text file: {file_path} ({len(content)} chars)")
            return content
            
        except Exception as e:
            error_msg = f"Failed to read text file {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def write_json_file(self, path: Union[str, Path], data: Any, 
                       indent: int = 2, atomic: bool = True,
                       validator: Optional[Callable[[Any], bool]] = None) -> None:
        """
        Write data to a JSON file safely with optional validation.
        
        Args:
            path: File path to write to
            data: Data to serialize as JSON
            indent: JSON indentation
            atomic: Whether to use atomic writes
            validator: Optional function to validate data before writing
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            # Validate data if validator provided
            if validator and not validator(data):
                raise FileValidationError(f"Data validation failed for {file_path}")
            
            # Serialize to JSON string first to catch serialization errors
            json_content = json.dumps(data, indent=indent, ensure_ascii=False)
            
            if atomic:
                with AtomicFileWriter(file_path, mode='w', encoding='utf-8') as f:
                    f.write(json_content)
            else:
                self.ensure_directory(file_path.parent)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(json_content)
            
            logger.info(f"Wrote JSON file: {file_path} ({len(json_content)} chars)")
            
        except FileValidationError:
            # Re-raise validation errors as-is
            raise
        except TypeError as e:
            # JSON serialization error (no JSONEncodeError in Python's json module)
            error_msg = f"JSON serialization failed for {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to write JSON file {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def read_json_file(self, path: Union[str, Path], 
                      validator: Optional[Callable[[Any], bool]] = None) -> Any:
        """
        Read and parse JSON file safely with optional validation.
        
        Args:
            path: File path to read from
            validator: Optional function to validate loaded data
            
        Returns:
            Parsed JSON data
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate data if validator provided
            if validator and not validator(data):
                raise FileValidationError(f"Data validation failed for {file_path}")
            
            logger.debug(f"Read JSON file: {file_path}")
            return data
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing failed for {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
        except Exception as e:
            error_msg = f"Failed to read JSON file {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def copy_file(self, src: Union[str, Path], dst: Union[str, Path], 
                 preserve_metadata: bool = True) -> None:
        """
        Copy a file safely with optional metadata preservation.
        
        Args:
            src: Source file path
            dst: Destination file path
            preserve_metadata: Whether to preserve file metadata
        """
        src_path = self.base_path / src if not Path(src).is_absolute() else Path(src)
        dst_path = self.base_path / dst if not Path(dst).is_absolute() else Path(dst)
        
        try:
            if not src_path.exists():
                raise FileNotFoundError(f"Source file not found: {src_path}")
            
            self.ensure_directory(dst_path.parent)
            
            if preserve_metadata:
                shutil.copy2(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)
            
            logger.info(f"Copied file: {src_path} -> {dst_path}")
            
        except Exception as e:
            error_msg = f"Failed to copy file {src_path} to {dst_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def move_file(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Move a file safely.
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        src_path = self.base_path / src if not Path(src).is_absolute() else Path(src)
        dst_path = self.base_path / dst if not Path(dst).is_absolute() else Path(dst)
        
        try:
            if not src_path.exists():
                raise FileNotFoundError(f"Source file not found: {src_path}")
            
            self.ensure_directory(dst_path.parent)
            shutil.move(str(src_path), str(dst_path))
            
            logger.info(f"Moved file: {src_path} -> {dst_path}")
            
        except Exception as e:
            error_msg = f"Failed to move file {src_path} to {dst_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def delete_file(self, path: Union[str, Path], missing_ok: bool = True) -> bool:
        """
        Delete a file safely.
        
        Args:
            path: File path to delete
            missing_ok: Whether to ignore missing files
            
        Returns:
            True if file was deleted, False if it didn't exist
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            elif not missing_ok:
                raise FileNotFoundError(f"File not found: {file_path}")
            else:
                logger.debug(f"File already doesn't exist: {file_path}")
                return False
                
        except Exception as e:
            error_msg = f"Failed to delete file {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def get_file_info(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get comprehensive file information.
        
        Args:
            path: File path to inspect
            
        Returns:
            Dictionary with file information
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            stat_info = file_path.stat()
            
            info = {
                'path': str(file_path.absolute()),
                'name': file_path.name,
                'stem': file_path.stem,
                'suffix': file_path.suffix,
                'size': stat_info.st_size,
                'created': datetime.fromtimestamp(stat_info.st_ctime),
                'modified': datetime.fromtimestamp(stat_info.st_mtime),
                'accessed': datetime.fromtimestamp(stat_info.st_atime),
                'is_file': file_path.is_file(),
                'is_dir': file_path.is_dir(),
                'is_symlink': file_path.is_symlink(),
                'permissions': oct(stat_info.st_mode)[-3:],
            }
            
            # Add hash for regular files
            if file_path.is_file() and stat_info.st_size < 100 * 1024 * 1024:  # Less than 100MB
                info['sha256'] = self.calculate_file_hash(file_path)
            
            logger.debug(f"Retrieved file info: {file_path}")
            return info
            
        except Exception as e:
            error_msg = f"Failed to get file info for {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def calculate_file_hash(self, path: Union[str, Path], algorithm: str = 'sha256') -> str:
        """
        Calculate hash of a file.
        
        Args:
            path: File path to hash
            algorithm: Hash algorithm (sha256, md5, etc.)
            
        Returns:
            Hex digest of the file hash
        """
        file_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_obj.update(chunk)
            
            digest = hash_obj.hexdigest()
            logger.debug(f"Calculated {algorithm} hash for {file_path}: {digest[:16]}...")
            return digest
            
        except Exception as e:
            error_msg = f"Failed to calculate hash for {file_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    def list_directory(self, path: Union[str, Path] = ".", 
                      pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        List files in a directory with optional filtering.
        
        Args:
            path: Directory path to list
            pattern: Glob pattern for filtering
            recursive: Whether to search recursively
            
        Returns:
            List of Path objects
        """
        dir_path = self.base_path / path if not Path(path).is_absolute() else Path(path)
        
        try:
            if not dir_path.exists():
                raise FileNotFoundError(f"Directory not found: {dir_path}")
            
            if not dir_path.is_dir():
                raise FileOperationError(f"Path is not a directory: {dir_path}")
            
            if recursive:
                files = list(dir_path.rglob(pattern))
            else:
                files = list(dir_path.glob(pattern))
            
            logger.debug(f"Listed directory {dir_path}: {len(files)} items")
            return sorted(files)
            
        except Exception as e:
            error_msg = f"Failed to list directory {dir_path}: {e}"
            logger.error(error_msg)
            raise FileOperationError(error_msg) from e


@contextmanager
def file_lock(path: Union[str, Path], mode: str = 'r', timeout: float = 10.0):
    """
    Context manager for file locking (Unix systems only).
    
    Args:
        path: File path to lock
        mode: File open mode
        timeout: Lock timeout in seconds
    """
    file_path = Path(path)
    f = None
    
    try:
        f = open(file_path, mode)
        
        # Try to acquire exclusive lock on Unix systems
        if fcntl is not None:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            logger.debug(f"Acquired file lock: {file_path}")
        else:
            # Windows - simple file opening (no locking)
            logger.debug(f"File opened (no locking on Windows): {file_path}")
        
        yield f
        
    except BlockingIOError:
        error_msg = f"Could not acquire lock on {file_path} within {timeout}s"
        logger.error(error_msg)
        raise FileOperationError(error_msg)
    except Exception as e:
        error_msg = f"File lock error for {file_path}: {e}"
        logger.error(error_msg)
        raise FileOperationError(error_msg) from e
    finally:
        if f:
            try:
                if fcntl is not None:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    logger.debug(f"Released file lock: {file_path}")
            except:
                pass  # Ignore unlock errors
            f.close()


# Utility functions for common operations
def safe_write_json(path: Union[str, Path], data: Any, **kwargs) -> None:
    """Convenience function for safe JSON writing."""
    fm = FileManager()
    fm.write_json_file(path, data, **kwargs)


def safe_read_json(path: Union[str, Path], **kwargs) -> Any:
    """Convenience function for safe JSON reading."""
    fm = FileManager()
    return fm.read_json_file(path, **kwargs)


def safe_write_text(path: Union[str, Path], content: str, **kwargs) -> None:
    """Convenience function for safe text writing."""
    fm = FileManager()
    fm.write_text_file(path, content, **kwargs)


def safe_read_text(path: Union[str, Path], **kwargs) -> str:
    """Convenience function for safe text reading."""
    fm = FileManager()
    return fm.read_text_file(path, **kwargs)