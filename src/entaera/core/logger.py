"""
Day 2 Kata: Logging Infrastructure  
==================================

Learning Objectives:
- Python logging module basics
- Log levels and formatting
- File and console outputs
- Structured logging for production
- Integration with configuration

This module implements comprehensive logging infrastructure for the ENTAERA system.
"""

import logging
import logging.handlers
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Union
from contextvars import ContextVar

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

# Context variable for request/session tracking
request_id: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    
    Formats log records as JSON for better parsing and analysis
    in production environments.
    """
    
    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add request ID if available
        req_id = request_id.get()
        if req_id:
            log_entry["request_id"] = req_id
        
        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if enabled
        if self.include_extra:
            for key, value in record.__dict__.items():
                if key not in {
                    'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                    'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                    'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                    'thread', 'threadName', 'processName', 'process', 'getMessage'
                }:
                    try:
                        # Only include JSON-serializable values
                        json.dumps(value)
                        log_entry[key] = value
                    except (TypeError, ValueError):
                        log_entry[key] = str(value)
        
        return json.dumps(log_entry)


class ColoredFormatter(logging.Formatter):
    """
    Colored console formatter for better development experience.
    
    Adds color coding based on log levels for easier visual parsing.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Base format
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        message = record.getMessage()
        location = f"{record.module}:{record.funcName}:{record.lineno}"
        
        # Add request ID if available
        req_id = request_id.get()
        req_id_str = f" [{req_id}]" if req_id else ""
        
        if self.use_colors and sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, '')
            formatted = (
                f"{timestamp} {color}{record.levelname:8}{self.RESET} "
                f"{record.name}{req_id_str} {location} - {message}"
            )
        else:
            formatted = (
                f"{timestamp} {record.levelname:8} "
                f"{record.name}{req_id_str} {location} - {message}"
            )
        
        # Add exception information if present
        if record.exc_info:
            formatted += '\n' + self.formatException(record.exc_info)
        
        return formatted


class LoggerManager:
    """
    Central logger management for the application.
    
    Handles logger configuration, formatting, and output routing
    based on application settings.
    """
    
    def __init__(self):
        self._loggers: Dict[str, logging.Logger] = {}
        self._configured = False
    
    def configure(
        self,
        level: str = "INFO",
        format_type: str = "structured",
        log_file: Optional[str] = None,
        log_dir: str = "./logs",
        max_size: str = "10MB",
        backup_count: int = 5,
        console_output: bool = True,
        use_colors: bool = True
    ) -> None:
        """
        Configure logging system.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_type: Format type ('structured' or 'simple')
            log_file: Log file name (optional)
            log_dir: Directory for log files
            max_size: Maximum size per log file
            backup_count: Number of backup files to keep
            console_output: Whether to output to console
            use_colors: Whether to use colors in console output
        """
        # Ensure log directory exists
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level.upper()))
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            
            if format_type == "structured" and STRUCTLOG_AVAILABLE:
                console_handler.setFormatter(JSONFormatter())
            elif format_type == "simple" or not STRUCTLOG_AVAILABLE:
                console_handler.setFormatter(ColoredFormatter(use_colors=use_colors))
            
            console_handler.setLevel(getattr(logging, level.upper()))
            root_logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            file_path = log_path / log_file
            
            # Convert size string to bytes
            max_bytes = self._parse_size(max_size)
            
            file_handler = logging.handlers.RotatingFileHandler(
                filename=file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            
            if format_type == "structured":
                file_handler.setFormatter(JSONFormatter())
            else:
                file_handler.setFormatter(ColoredFormatter(use_colors=False))
            
            file_handler.setLevel(getattr(logging, level.upper()))
            root_logger.addHandler(file_handler)
        
        # Configure structlog if available
        if STRUCTLOG_AVAILABLE and format_type == "structured":
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.UnicodeDecoder(),
                    structlog.processors.JSONRenderer()
                ],
                context_class=dict,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
        
        self._configured = True
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Logger instance
        """
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)
        
        return self._loggers[name]
    
    def set_request_id(self, req_id: str) -> None:
        """Set request ID for context-aware logging."""
        request_id.set(req_id)
    
    def clear_request_id(self) -> None:
        """Clear request ID from context."""
        request_id.set(None)
    
    @staticmethod
    def _parse_size(size_str: str) -> int:
        """
        Parse size string to bytes.
        
        Args:
            size_str: Size string like "10MB", "1GB", etc.
            
        Returns:
            Size in bytes
        """
        size_str = size_str.upper().strip()
        
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
        }
        
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                number = size_str[:-len(suffix)]
                try:
                    return int(float(number) * multiplier)
                except ValueError:
                    break
        
        # Default to treating as bytes
        try:
            return int(size_str)
        except ValueError:
            return 10 * 1024 * 1024  # Default to 10MB


# Global logger manager instance
_logger_manager: Optional[LoggerManager] = None


def get_logger_manager() -> LoggerManager:
    """Get the global logger manager instance."""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = LoggerManager()
    return _logger_manager


def configure_logging(
    level: str = "INFO",
    format_type: str = "structured",
    log_file: Optional[str] = None,
    log_dir: str = "./logs",
    max_size: str = "10MB",
    backup_count: int = 5,
    console_output: bool = True,
    use_colors: bool = True
) -> None:
    """
    Configure the global logging system.
    
    Args:
        level: Log level
        format_type: Format type ('structured' or 'simple')
        log_file: Log file name
        log_dir: Log directory
        max_size: Maximum file size
        backup_count: Number of backup files
        console_output: Enable console output
        use_colors: Use colors in console
    """
    manager = get_logger_manager()
    manager.configure(
        level=level,
        format_type=format_type,
        log_file=log_file,
        log_dir=log_dir,
        max_size=max_size,
        backup_count=backup_count,
        console_output=console_output,
        use_colors=use_colors
    )


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (defaults to calling module)
        
    Returns:
        Logger instance
    """
    if name is None:
        # Get the calling module name
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    manager = get_logger_manager()
    return manager.get_logger(name)


def set_request_id(req_id: str) -> None:
    """Set request ID for context-aware logging."""
    manager = get_logger_manager()
    manager.set_request_id(req_id)


def clear_request_id() -> None:
    """Clear request ID from context."""
    manager = get_logger_manager()
    manager.clear_request_id()


# Convenience functions for common log levels
def log_debug(message: str, **kwargs) -> None:
    """Log debug message."""
    logger = get_logger()
    logger.debug(message, extra=kwargs)


def log_info(message: str, **kwargs) -> None:
    """Log info message."""
    logger = get_logger()
    logger.info(message, extra=kwargs)


def log_warning(message: str, **kwargs) -> None:
    """Log warning message."""
    logger = get_logger()
    logger.warning(message, extra=kwargs)


def log_error(message: str, **kwargs) -> None:
    """Log error message."""
    logger = get_logger()
    logger.error(message, extra=kwargs)


def log_critical(message: str, **kwargs) -> None:
    """Log critical message."""
    logger = get_logger()
    logger.critical(message, extra=kwargs)


# Kata practice function
def kata_practice_logging() -> dict:
    """
    Practice function for logging infrastructure kata.
    
    Returns:
        Dictionary with logging analysis for learning
    """
    import uuid
    import tempfile
    import os
    
    # Create temporary log directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = "test_kata.log"
        
        try:
            # Configure logging
            configure_logging(
                level="DEBUG",
                format_type="simple",
                log_file=log_file,
                log_dir=temp_dir,
                max_size="1MB",
                backup_count=2,
                console_output=False,
                use_colors=False
            )
            
            # Get test logger
            logger = get_logger("kata_test")
            
            # Set request ID for context
            test_request_id = str(uuid.uuid4())[:8]
            set_request_id(test_request_id)
            
            # Test different log levels
            logger.debug("Debug message for kata testing")
            logger.info("Info message with context", extra={"user_id": "test_user", "action": "kata_practice"})
            logger.warning("Warning message about something")
            logger.error("Error message for testing")
            
            # Test exception logging
            try:
                raise ValueError("Test exception for kata logging")
            except Exception:
                logger.exception("Exception caught during kata practice")
            
            # Check if log file was created and has content
            log_file_path = Path(temp_dir) / log_file
            log_content = ""
            if log_file_path.exists():
                log_content = log_file_path.read_text()
            
            # Clear request ID
            clear_request_id()
            
            return {
                "logging_configured": True,
                "log_file_created": log_file_path.exists(),
                "log_file_size": len(log_content),
                "log_entries": len(log_content.split('\n')) if log_content else 0,
                "request_id_used": test_request_id,
                "log_levels_tested": ["DEBUG", "INFO", "WARNING", "ERROR"],
                "exception_logged": "Exception caught during kata practice" in log_content,
                "extra_fields_logged": "user_id" in log_content and "action" in log_content,
                "learning_notes": [
                    "Logging supports multiple output formats (simple, structured)",
                    "Log files are automatically rotated based on size",
                    "Request IDs provide context for distributed tracing",
                    "Exception information is automatically captured",
                    "Extra fields can be added to log entries for context"
                ],
                "sample_log_entry": log_content.split('\n')[0] if log_content else ""
            }
        
        except Exception as e:
            return {
                "logging_configured": False,
                "error": str(e),
                "learning_notes": [
                    "Logging configuration failed",
                    "Check permissions for log directory",
                    "Ensure all dependencies are installed"
                ]
            }


if __name__ == "__main__":
    # Kata demonstration
    print("🥋 Day 2 Kata: Logging Infrastructure Demo")
    print("=" * 50)
    
    # Practice logging configuration
    practice_results = kata_practice_logging()
    
    print(f"Logging configured: {practice_results['logging_configured']}")
    
    if practice_results['logging_configured']:
        print(f"Log file created: {practice_results['log_file_created']}")
        print(f"Log entries: {practice_results['log_entries']}")
        print(f"Request ID: {practice_results['request_id_used']}")
        print(f"Exception logged: {practice_results['exception_logged']}")
        print(f"Extra fields: {practice_results['extra_fields_logged']}")
        
        print(f"\nLevels tested: {', '.join(practice_results['log_levels_tested'])}")
        
        if practice_results['sample_log_entry']:
            print(f"\nSample log entry:")
            print(f"  {practice_results['sample_log_entry']}")
    else:
        print(f"Logging error: {practice_results.get('error', 'Unknown error')}")
    
    print(f"\nLearning notes:")
    for note in practice_results['learning_notes']:
        print(f"  📝 {note}")
    
    print(f"\n🎉 Day 2 Kata completed! Logging infrastructure mastery achieved.")