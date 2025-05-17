"""
ENTAERA Code Execution Environment

Day 6 Kata 6.3: Secure Code Execution System

This module provides a secure, sandboxed environment for executing code safely:
- Multi-language runtime support (Python, JavaScript, shell commands)
- Resource limits (memory, CPU time, execution timeout)
- Isolated execution contexts with restricted system access
- Real-time monitoring and logging of execution
- Security controls to prevent malicious code execution
- Stream capture for stdout, stderr, and return values

The execution environment integrates with the code analysis and generation
systems to provide a complete code development and testing pipeline.
"""

import asyncio
import contextlib
import io
import json
import os
import platform
import signal
import subprocess
import sys
import tempfile
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import logging

# Import resource module only on Unix-like systems
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False

try:
    from .logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)


class ExecutionStatus(Enum):
    """Execution status codes."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    MEMORY_LIMIT = "memory_limit"
    SECURITY_VIOLATION = "security_violation"
    INVALID_CODE = "invalid_code"
    RUNTIME_ERROR = "runtime_error"


class SecurityLevel(Enum):
    """Security levels for code execution."""
    SAFE = "safe"          # Minimal restrictions for trusted code
    RESTRICTED = "restricted"  # Standard restrictions
    SANDBOXED = "sandboxed"   # Maximum restrictions for untrusted code


@dataclass
class ExecutionLimits:
    """Resource limits for code execution."""
    max_execution_time: float = 30.0  # seconds
    max_memory_mb: int = 256  # megabytes
    max_output_size: int = 10_000  # characters
    max_file_size: int = 1_000_000  # bytes
    allow_network: bool = False
    allow_file_system: bool = False
    allowed_modules: Optional[Set[str]] = None
    blocked_modules: Set[str] = field(default_factory=lambda: {
        'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
        'shutil', 'tempfile', 'pickle', 'marshal', 'shelve'
    })


@dataclass
class ExecutionResult:
    """Result of code execution."""
    status: ExecutionStatus
    stdout: str = ""
    stderr: str = ""
    return_value: Any = None
    execution_time: float = 0.0
    memory_used_mb: float = 0.0
    exit_code: Optional[int] = None
    error_message: Optional[str] = None
    security_violations: List[str] = field(default_factory=list)
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CodeExecutor(ABC):
    """Abstract base class for language-specific code executors."""
    
    @abstractmethod
    def execute(self, code: str, limits: ExecutionLimits, 
                context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute code with given limits and context."""
        pass
    
    @abstractmethod
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate code for security and syntax issues."""
        pass


class PythonExecutor(CodeExecutor):
    """Secure Python code executor."""
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.RESTRICTED):
        self.security_level = security_level
        self.restricted_builtins = {
            'open', 'input', 'raw_input', 'file', 'execfile', 'reload',
            '__import__', 'eval', 'exec', 'compile', 'vars', 'locals',
            'globals', 'dir', 'help', 'copyright', 'credits', 'license'
        }
    
    def execute(self, code: str, limits: ExecutionLimits, 
                context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute Python code in a restricted environment."""
        logger.info("Executing Python code with security restrictions")
        
        # Validate code first
        is_valid, violations = self.validate_code(code)
        if not is_valid:
            return ExecutionResult(
                status=ExecutionStatus.SECURITY_VIOLATION,
                error_message="Code validation failed",
                security_violations=violations
            )
        
        # Prepare execution environment
        start_time = time.time()
        
        # Create restricted globals
        restricted_globals = self._create_restricted_globals(limits)
        if context:
            restricted_globals.update(context)
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = ExecutionResult(status=ExecutionStatus.SUCCESS)
        
        try:
            # Set resource limits
            self._set_resource_limits(limits)
            
            # Execute with timeout
            with self._execution_timeout(limits.max_execution_time):
                with contextlib.redirect_stdout(stdout_capture):
                    with contextlib.redirect_stderr(stderr_capture):
                        # Compile and execute code
                        compiled = compile(code, '<string>', 'exec')
                        exec(compiled, restricted_globals)
            
            result.status = ExecutionStatus.SUCCESS
            
        except TimeoutError:
            result.status = ExecutionStatus.TIMEOUT
            result.error_message = f"Execution timed out after {limits.max_execution_time}s"
            
        except MemoryError:
            result.status = ExecutionStatus.MEMORY_LIMIT
            result.error_message = "Memory limit exceeded"
            
        except SyntaxError as e:
            result.status = ExecutionStatus.INVALID_CODE
            result.error_message = f"Syntax error: {str(e)}"
            
        except Exception as e:
            result.status = ExecutionStatus.RUNTIME_ERROR
            result.error_message = f"Runtime error: {str(e)}"
            
        finally:
            # Capture execution time
            result.execution_time = time.time() - start_time
            
            # Capture output
            result.stdout = stdout_capture.getvalue()
            result.stderr = stderr_capture.getvalue()
            
            # Limit output size
            if len(result.stdout) > limits.max_output_size:
                result.stdout = result.stdout[:limits.max_output_size] + "\n[OUTPUT TRUNCATED]"
            if len(result.stderr) > limits.max_output_size:
                result.stderr = result.stderr[:limits.max_output_size] + "\n[ERROR OUTPUT TRUNCATED]"
        
        logger.info(f"Python execution completed: {result.status.value} in {result.execution_time:.3f}s")
        return result
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate Python code for security issues."""
        violations = []
        
        # Check for dangerous imports
        dangerous_imports = [
            'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
            'shutil', 'tempfile', 'pickle', 'marshal', 'shelve', 'ctypes'
        ]
        
        for dangerous in dangerous_imports:
            if f"import {dangerous}" in code or f"from {dangerous}" in code:
                violations.append(f"Dangerous import detected: {dangerous}")
        
        # Check for dangerous function calls
        dangerous_functions = [
            'eval(', 'exec(', 'compile(', '__import__(', 'open(',
            'input(', 'raw_input(', 'vars(', 'locals(', 'globals('
        ]
        
        for dangerous in dangerous_functions:
            if dangerous in code:
                violations.append(f"Dangerous function call detected: {dangerous}")
        
        # Check for system access attempts
        system_access = ['os.', 'sys.', 'subprocess.', '__file__', '__name__']
        for access in system_access:
            if access in code:
                violations.append(f"System access attempt detected: {access}")
        
        # Check syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            violations.append(f"Syntax error: {str(e)}")
        
        return len(violations) == 0, violations
    
    def _create_restricted_globals(self, limits: ExecutionLimits) -> Dict[str, Any]:
        """Create a restricted global namespace."""
        # Start with minimal builtins
        safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
            'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter',
            'float', 'format', 'frozenset', 'hex', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
            'next', 'oct', 'ord', 'pow', 'print', 'range', 'repr',
            'reversed', 'round', 'set', 'slice', 'sorted', 'str',
            'sum', 'tuple', 'type', 'zip'
        }
        
        # Create restricted builtins dict - handle different Python versions
        restricted_builtins = {}
        builtins_source = __builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__
        
        for name in safe_builtins:
            if name in builtins_source:
                restricted_builtins[name] = builtins_source[name]
        
        restricted_globals = {
            '__builtins__': restricted_builtins
        }
        
        # Add safe modules
        safe_modules = ['math', 'random', 'string', 'json', 're', 'datetime']
        if limits.allowed_modules:
            safe_modules.extend(limits.allowed_modules)
        
        for module_name in safe_modules:
            if module_name not in limits.blocked_modules:
                try:
                    restricted_globals[module_name] = __import__(module_name)
                except ImportError:
                    logger.warning(f"Could not import safe module: {module_name}")
        
        return restricted_globals
    
    def _set_resource_limits(self, limits: ExecutionLimits):
        """Set resource limits for the execution."""
        if not HAS_RESOURCE or platform.system() == 'Windows':
            logger.debug("Resource limits not available on this platform")
            return
        
        try:
            # Set memory limit (Unix-like systems only)
            memory_limit = limits.max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # Set CPU time limit
            cpu_limit = int(limits.max_execution_time)
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
            
        except (OSError, ValueError) as e:
            logger.warning(f"Could not set resource limits: {e}")
    
    @contextlib.contextmanager
    def _execution_timeout(self, timeout: float):
        """Context manager for execution timeout."""
        if platform.system() != 'Windows':
            # Unix-like systems: use signal
            def timeout_handler(signum, frame):
                raise TimeoutError("Execution timed out")
            
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))
            
            try:
                yield
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        else:
            # Windows: simpler approach without threading complications
            yield


class JavaScriptExecutor(CodeExecutor):
    """JavaScript code executor using Node.js."""
    
    def __init__(self, node_path: str = "node"):
        self.node_path = node_path
    
    def execute(self, code: str, limits: ExecutionLimits, 
                context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute JavaScript code using Node.js."""
        logger.info("Executing JavaScript code via Node.js")
        
        # Validate code
        is_valid, violations = self.validate_code(code)
        if not is_valid:
            return ExecutionResult(
                status=ExecutionStatus.SECURITY_VIOLATION,
                error_message="Code validation failed",
                security_violations=violations
            )
        
        start_time = time.time()
        
        # Prepare context
        if context:
            context_code = "\\n".join([f"const {k} = {json.dumps(v)};" for k, v in context.items()])
            code = context_code + "\\n" + code
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute with subprocess and timeout
            process = subprocess.Popen(
                [self.node_path, temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=limits.max_execution_time)
                exit_code = process.returncode
                
                if exit_code == 0:
                    status = ExecutionStatus.SUCCESS
                else:
                    status = ExecutionStatus.RUNTIME_ERROR
                
                return ExecutionResult(
                    status=status,
                    stdout=stdout[:limits.max_output_size],
                    stderr=stderr[:limits.max_output_size],
                    exit_code=exit_code,
                    execution_time=time.time() - start_time
                )
                
            except subprocess.TimeoutExpired:
                process.kill()
                return ExecutionResult(
                    status=ExecutionStatus.TIMEOUT,
                    error_message=f"Execution timed out after {limits.max_execution_time}s",
                    execution_time=limits.max_execution_time
                )
        
        except FileNotFoundError:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error_message="Node.js not found. Please install Node.js."
            )
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate JavaScript code for security issues."""
        violations = []
        
        # Check for dangerous Node.js modules
        dangerous_modules = [
            'fs', 'child_process', 'cluster', 'net', 'http', 'https',
            'os', 'path', 'process', 'vm'
        ]
        
        for module in dangerous_modules:
            if f"require('{module}')" in code or f'require("{module}")' in code:
                violations.append(f"Dangerous module import detected: {module}")
        
        # Check for dangerous function calls
        dangerous_functions = ['eval(', 'Function(', 'setTimeout(', 'setInterval(']
        for func in dangerous_functions:
            if func in code:
                violations.append(f"Dangerous function call detected: {func}")
        
        return len(violations) == 0, violations


class ShellExecutor(CodeExecutor):
    """Shell command executor with restrictions."""
    
    def __init__(self):
        self.allowed_commands = {
            'echo', 'cat', 'ls', 'pwd', 'date', 'whoami', 'head', 'tail',
            'grep', 'wc', 'sort', 'uniq', 'cut', 'awk', 'sed'
        }
    
    def execute(self, code: str, limits: ExecutionLimits, 
                context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute shell commands with restrictions."""
        logger.info("Executing shell command with restrictions")
        
        # Validate code
        is_valid, violations = self.validate_code(code)
        if not is_valid:
            return ExecutionResult(
                status=ExecutionStatus.SECURITY_VIOLATION,
                error_message="Command validation failed",
                security_violations=violations
            )
        
        start_time = time.time()
        
        try:
            # Execute command
            process = subprocess.Popen(
                code,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=limits.max_execution_time)
            
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS if process.returncode == 0 else ExecutionStatus.RUNTIME_ERROR,
                stdout=stdout[:limits.max_output_size],
                stderr=stderr[:limits.max_output_size],
                exit_code=process.returncode,
                execution_time=time.time() - start_time
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                error_message=f"Command timed out after {limits.max_execution_time}s",
                execution_time=limits.max_execution_time
            )
        
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error_message=f"Execution error: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate shell commands for security."""
        violations = []
        
        # Check for dangerous commands
        dangerous_commands = [
            'rm', 'rmdir', 'mv', 'cp', 'chmod', 'chown', 'sudo', 'su',
            'kill', 'killall', 'ps', 'top', 'mount', 'umount', 'fdisk',
            'mkfs', 'dd', 'curl', 'wget', 'ssh', 'scp', 'rsync'
        ]
        
        command_words = code.split()
        if command_words:
            base_command = command_words[0].split('/')[-1]  # Get command name without path
            
            if base_command in dangerous_commands:
                violations.append(f"Dangerous command detected: {base_command}")
            elif base_command not in self.allowed_commands:
                violations.append(f"Command not in allowed list: {base_command}")
        
        # Check for dangerous operators
        dangerous_operators = ['>', '>>', '|', '&', ';', '&&', '||']
        for op in dangerous_operators:
            if op in code:
                violations.append(f"Dangerous operator detected: {op}")
        
        return len(violations) == 0, violations


class CodeExecutionEngine:
    """Main execution engine supporting multiple languages and security levels."""
    
    def __init__(self):
        self.executors = {
            'python': PythonExecutor(),
            'javascript': JavaScriptExecutor(),
            'shell': ShellExecutor()
        }
        self.execution_history: List[ExecutionResult] = []
    
    def execute_code(self, language: str, code: str, 
                    limits: Optional[ExecutionLimits] = None,
                    context: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute code in the specified language."""
        if limits is None:
            limits = ExecutionLimits()
        
        logger.info(f"Executing {language} code with limits: {limits.max_execution_time}s timeout, {limits.max_memory_mb}MB memory")
        
        if language not in self.executors:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error_message=f"Unsupported language: {language}"
            )
        
        executor = self.executors[language]
        result = executor.execute(code, limits, context)
        
        # Store in history
        self.execution_history.append(result)
        
        # Log result
        logger.info(f"Execution completed: {result.status.value} in {result.execution_time:.3f}s")
        if result.status != ExecutionStatus.SUCCESS:
            logger.warning(f"Execution failed: {result.error_message}")
        
        return result
    
    def execute_python(self, code: str, **kwargs) -> ExecutionResult:
        """Convenience method for Python execution."""
        return self.execute_code('python', code, **kwargs)
    
    def execute_javascript(self, code: str, **kwargs) -> ExecutionResult:
        """Convenience method for JavaScript execution."""
        return self.execute_code('javascript', code, **kwargs)
    
    def execute_shell(self, command: str, **kwargs) -> ExecutionResult:
        """Convenience method for shell command execution."""
        return self.execute_code('shell', command, **kwargs)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported execution languages."""
        return list(self.executors.keys())
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
        logger.info("Execution history cleared")
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        if not self.execution_history:
            return {}
        
        total_executions = len(self.execution_history)
        successful = sum(1 for r in self.execution_history if r.status == ExecutionStatus.SUCCESS)
        total_time = sum(r.execution_time for r in self.execution_history)
        
        status_counts = {}
        for result in self.execution_history:
            status = result.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_executions': total_executions,
            'successful_executions': successful,
            'success_rate': successful / total_executions if total_executions > 0 else 0,
            'total_execution_time': total_time,
            'average_execution_time': total_time / total_executions if total_executions > 0 else 0,
            'status_distribution': status_counts
        }


# Export main classes
__all__ = [
    'ExecutionStatus',
    'SecurityLevel',
    'ExecutionLimits',
    'ExecutionResult',
    'CodeExecutor',
    'PythonExecutor',
    'JavaScriptExecutor',
    'ShellExecutor',
    'CodeExecutionEngine'
]