"""
ENTAERA Code Analysis Engine

Day 6 Kata 6.1: Code Generation & Analysis Engine

This module provides sophisticated code analysis capabilities including:
- Abstract Syntax Tree (AST) parsing and analysis
- Code syntax validation and error detection
- Code complexity and quality metrics
- Multi-language support (Python, JavaScript, Java, C++, etc.)
- Code structure understanding and documentation extraction
- Dependency analysis and import mapping

The code analysis engine integrates with the multi-agent system to provide
intelligent code understanding and processing capabilities.
"""

import ast
import json
import re
import subprocess
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import logging

from .logger import get_logger

logger = get_logger(__name__)


class CodeLanguage(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    SCALA = "scala"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    SQL = "sql"
    SHELL = "shell"
    UNKNOWN = "unknown"


class CodeComplexity(Enum):
    """Code complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class CodeElement:
    """Represents a code element (function, class, variable, etc.)."""
    name: str
    element_type: str  # function, class, variable, import, etc.
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    complexity: Optional[CodeComplexity] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class CodeMetrics:
    """Code quality and complexity metrics."""
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    technical_debt_ratio: float
    code_coverage: Optional[float] = None
    duplication_ratio: float = 0.0
    
    def get_quality_score(self) -> float:
        """Calculate overall code quality score (0.0 to 1.0)."""
        # Simple scoring algorithm
        base_score = 0.8
        
        # Penalize high complexity
        complexity_penalty = min(0.3, self.cyclomatic_complexity * 0.01)
        
        # Reward good maintainability
        maintainability_bonus = max(0.0, (self.maintainability_index - 50) * 0.004)
        
        # Penalize technical debt
        debt_penalty = min(0.2, self.technical_debt_ratio * 0.1)
        
        score = base_score - complexity_penalty + maintainability_bonus - debt_penalty
        return max(0.0, min(1.0, score))


@dataclass
class CodeAnalysisResult:
    """Result of code analysis."""
    language: CodeLanguage
    file_path: Optional[str]
    is_valid: bool
    syntax_errors: List[str] = field(default_factory=list)
    elements: List[CodeElement] = field(default_factory=list)
    metrics: Optional[CodeMetrics] = None
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    performance_issues: List[str] = field(default_factory=list)
    style_issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    analysis_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CodeAnalyzer(ABC):
    """Abstract base class for language-specific code analyzers."""
    
    @abstractmethod
    def analyze(self, code: str, file_path: Optional[str] = None) -> CodeAnalysisResult:
        """Analyze code and return detailed analysis results."""
        pass
    
    @abstractmethod
    def validate_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Validate code syntax and return errors if any."""
        pass
    
    @abstractmethod
    def extract_elements(self, code: str) -> List[CodeElement]:
        """Extract code elements (functions, classes, etc.)."""
        pass
    
    @abstractmethod
    def calculate_metrics(self, code: str) -> CodeMetrics:
        """Calculate code quality and complexity metrics."""
        pass


class PythonCodeAnalyzer(CodeAnalyzer):
    """Python-specific code analyzer using AST."""
    
    def __init__(self):
        self.language = CodeLanguage.PYTHON
    
    def analyze(self, code: str, file_path: Optional[str] = None) -> CodeAnalysisResult:
        """Comprehensive Python code analysis."""
        logger.info(f"Analyzing Python code: {file_path or 'inline code'}")
        
        result = CodeAnalysisResult(
            language=self.language,
            file_path=file_path,
            is_valid=True  # Will be updated based on validation
        )
        
        # Syntax validation
        is_valid, syntax_errors = self.validate_syntax(code)
        result.is_valid = is_valid
        result.syntax_errors = syntax_errors
        
        if not is_valid:
            logger.warning(f"Python code has syntax errors: {syntax_errors}")
            return result
        
        # Extract code elements
        try:
            result.elements = self.extract_elements(code)
            result.imports = self._extract_imports(code)
            result.metrics = self.calculate_metrics(code)
            result.security_issues = self._detect_security_issues(code)
            result.performance_issues = self._detect_performance_issues(code)
            result.style_issues = self._detect_style_issues(code)
            result.suggestions = self._generate_suggestions(code, result)
            
            logger.info(f"Python analysis completed: {len(result.elements)} elements found")
            
        except Exception as e:
            logger.error(f"Error during Python code analysis: {e}")
            result.syntax_errors.append(f"Analysis error: {str(e)}")
        
        return result
    
    def validate_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Validate Python syntax using AST."""
        errors = []
        
        try:
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            error_msg = f"Line {e.lineno}: {e.msg}"
            if e.text:
                error_msg += f" ('{e.text.strip()}')"
            errors.append(error_msg)
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
        
        return False, errors
    
    def extract_elements(self, code: str) -> List[CodeElement]:
        """Extract Python code elements using AST."""
        elements = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    elements.append(self._extract_function(node, code))
                elif isinstance(node, ast.ClassDef):
                    elements.append(self._extract_class(node, code))
                elif isinstance(node, ast.Assign):
                    elements.extend(self._extract_variables(node, code))
        
        except Exception as e:
            logger.error(f"Error extracting Python elements: {e}")
        
        return elements
    
    def calculate_metrics(self, code: str) -> CodeMetrics:
        """Calculate Python code metrics."""
        lines = code.split('\n')
        
        # Basic line counts
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = total_lines - blank_lines - comment_lines
        
        # Complexity calculations
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(code)
        cognitive_complexity = self._calculate_cognitive_complexity(code)
        
        # Maintainability index (simplified)
        maintainability_index = max(0, 171 - 5.2 * np.log(max(1, code_lines)) - 
                                   0.23 * cyclomatic_complexity - 16.2 * np.log(max(1, code_lines)))
        
        # Technical debt ratio (simplified)
        technical_debt_ratio = min(1.0, (cyclomatic_complexity + cognitive_complexity) / max(1, code_lines) * 10)
        
        return CodeMetrics(
            lines_of_code=code_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cognitive_complexity,
            maintainability_index=maintainability_index,
            technical_debt_ratio=technical_debt_ratio
        )
    
    def _extract_function(self, node: ast.FunctionDef, code: str) -> CodeElement:
        """Extract function information from AST node."""
        # Get docstring
        docstring = None
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            docstring = ast.get_docstring(node)
        
        # Get parameters
        parameters = [arg.arg for arg in node.args.args]
        
        # Get decorators
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(f"{decorator.attr}")
        
        # Calculate function complexity
        complexity = self._calculate_function_complexity(node)
        
        return CodeElement(
            name=node.name,
            element_type="function",
            start_line=node.lineno,
            end_line=getattr(node, 'end_lineno', node.lineno),
            docstring=docstring,
            parameters=parameters,
            decorators=decorators,
            complexity=complexity
        )
    
    def _extract_class(self, node: ast.ClassDef, code: str) -> CodeElement:
        """Extract class information from AST node."""
        docstring = ast.get_docstring(node)
        
        # Get base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
        
        # Get decorators
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
        
        return CodeElement(
            name=node.name,
            element_type="class",
            start_line=node.lineno,
            end_line=getattr(node, 'end_lineno', node.lineno),
            docstring=docstring,
            dependencies=base_classes,
            decorators=decorators
        )
    
    def _extract_variables(self, node: ast.Assign, code: str) -> List[CodeElement]:
        """Extract variable assignments from AST node."""
        variables = []
        
        for target in node.targets:
            if isinstance(target, ast.Name):
                variables.append(CodeElement(
                    name=target.id,
                    element_type="variable",
                    start_line=node.lineno,
                    end_line=node.lineno
                ))
        
        return variables
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract import statements."""
        imports = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        except Exception as e:
            logger.error(f"Error extracting imports: {e}")
        
        return imports
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Decision points add complexity
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    # And/Or operators
                    complexity += len(node.values) - 1
                elif isinstance(node, ast.comprehension):
                    # List/dict/set comprehensions
                    complexity += 1
        
        except Exception as e:
            logger.error(f"Error calculating cyclomatic complexity: {e}")
        
        return complexity
    
    def _calculate_cognitive_complexity(self, code: str) -> int:
        """Calculate cognitive complexity (simplified)."""
        cognitive = 0
        nesting_level = 0
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For)):
                    cognitive += 1 + nesting_level
                elif isinstance(node, ast.ExceptHandler):
                    cognitive += 1 + nesting_level
                elif isinstance(node, ast.BoolOp):
                    cognitive += 1
        
        except Exception as e:
            logger.error(f"Error calculating cognitive complexity: {e}")
        
        return cognitive
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> CodeComplexity:
        """Calculate function complexity level."""
        complexity_score = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity_score += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity_score += 1
        
        if complexity_score <= 5:
            return CodeComplexity.SIMPLE
        elif complexity_score <= 10:
            return CodeComplexity.MODERATE
        elif complexity_score <= 20:
            return CodeComplexity.COMPLEX
        else:
            return CodeComplexity.VERY_COMPLEX
    
    def _detect_security_issues(self, code: str) -> List[str]:
        """Detect potential security issues."""
        issues = []
        
        # Simple pattern-based detection
        security_patterns = [
            (r'eval\s*\(', "Use of eval() can be dangerous"),
            (r'exec\s*\(', "Use of exec() can be dangerous"),
            (r'__import__\s*\(', "Dynamic imports can be risky"),
            (r'subprocess\.shell\s*=\s*True', "Shell=True in subprocess can be unsafe"),
            (r'pickle\.loads?\s*\(', "Pickle deserialization can be unsafe"),
            (r'input\s*\(.*password', "Using input() for passwords is insecure"),
            (r'random\.random\s*\(', "Use secrets module for cryptographic randomness"),
        ]
        
        for pattern, message in security_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(message)
        
        return issues
    
    def _detect_performance_issues(self, code: str) -> List[str]:
        """Detect potential performance issues."""
        issues = []
        
        performance_patterns = [
            (r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', "Consider enumerate() instead of range(len())"),
            (r'\+\s*=.*\[.*\]', "List concatenation in loop can be slow"),
            (r'\.append\s*\(.*\)\s*$', "Consider list comprehension for better performance"),
            (r'global\s+\w+', "Global variables can impact performance"),
        ]
        
        for pattern, message in performance_patterns:
            if re.search(pattern, code, re.MULTILINE):
                issues.append(message)
        
        return issues
    
    def _detect_style_issues(self, code: str) -> List[str]:
        """Detect code style issues."""
        issues = []
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line length check
            if len(line) > 88:
                issues.append(f"Line {i}: Line too long ({len(line)} > 88 characters)")
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(f"Line {i}: Trailing whitespace")
            
            # Multiple spaces after comma
            if re.search(r',\s{2,}', line):
                issues.append(f"Line {i}: Multiple spaces after comma")
        
        return issues
    
    def _generate_suggestions(self, code: str, analysis: CodeAnalysisResult) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        if analysis.metrics:
            # Complexity suggestions
            if analysis.metrics.cyclomatic_complexity > 10:
                suggestions.append("Consider breaking down complex functions into smaller ones")
            
            # Maintainability suggestions
            if analysis.metrics.maintainability_index < 50:
                suggestions.append("Code maintainability is low - consider refactoring")
            
            # Documentation suggestions
            functions_without_docs = [
                e for e in analysis.elements 
                if e.element_type == "function" and not e.docstring
            ]
            if functions_without_docs:
                suggestions.append(f"Add docstrings to {len(functions_without_docs)} functions")
        
        # Import suggestions
        if len(analysis.imports) > 20:
            suggestions.append("Consider organizing imports or reducing dependencies")
        
        return suggestions


class JavaScriptCodeAnalyzer(CodeAnalyzer):
    """JavaScript/TypeScript code analyzer."""
    
    def __init__(self, is_typescript: bool = False):
        self.language = CodeLanguage.TYPESCRIPT if is_typescript else CodeLanguage.JAVASCRIPT
        self.is_typescript = is_typescript
    
    def analyze(self, code: str, file_path: Optional[str] = None) -> CodeAnalysisResult:
        """Basic JavaScript/TypeScript analysis."""
        logger.info(f"Analyzing {self.language.value} code: {file_path or 'inline code'}")
        
        result = CodeAnalysisResult(
            language=self.language,
            file_path=file_path,
            is_valid=True  # Will be updated based on validation
        )
        
        # Basic syntax validation
        is_valid, syntax_errors = self.validate_syntax(code)
        result.is_valid = is_valid
        result.syntax_errors = syntax_errors
        
        if is_valid:
            result.elements = self.extract_elements(code)
            result.imports = self._extract_imports(code)
            result.metrics = self.calculate_metrics(code)
            result.suggestions = self._generate_suggestions(code)
        
        return result
    
    def validate_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Basic JavaScript syntax validation."""
        errors = []
        
        # Simple bracket matching
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        
        for i, char in enumerate(code):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    errors.append(f"Unmatched closing bracket '{char}' at position {i}")
                else:
                    open_bracket, pos = stack.pop()
                    if brackets[open_bracket] != char:
                        errors.append(f"Mismatched brackets at positions {pos} and {i}")
        
        if stack:
            for bracket, pos in stack:
                errors.append(f"Unmatched opening bracket '{bracket}' at position {pos}")
        
        return len(errors) == 0, errors
    
    def extract_elements(self, code: str) -> List[CodeElement]:
        """Extract JavaScript elements using regex patterns."""
        elements = []
        
        # Function patterns
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',  # function name()
            r'(\w+)\s*:\s*function\s*\([^)]*\)',  # name: function()
            r'(\w+)\s*=\s*function\s*\([^)]*\)',  # name = function()
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', # const name = () =>
            r'(\w+)\s*=\s*\([^)]*\)\s*=>'  # name = () =>
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, code):
                function_name = match.group(1)
                line_num = code[:match.start()].count('\n') + 1
                
                elements.append(CodeElement(
                    name=function_name,
                    element_type="function",
                    start_line=line_num,
                    end_line=line_num  # Simplified
                ))
        
        # Class patterns
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, code):
            class_name = match.group(1)
            line_num = code[:match.start()].count('\n') + 1
            
            elements.append(CodeElement(
                name=class_name,
                element_type="class",
                start_line=line_num,
                end_line=line_num
            ))
        
        return elements
    
    def calculate_metrics(self, code: str) -> CodeMetrics:
        """Calculate basic JavaScript metrics."""
        lines = code.split('\n')
        
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = sum(1 for line in lines if line.strip().startswith('//') or 
                           line.strip().startswith('/*') or line.strip().startswith('*'))
        code_lines = total_lines - blank_lines - comment_lines
        
        # Simple complexity calculation
        complexity_keywords = ['if', 'else', 'while', 'for', 'switch', 'catch', '&&', '||']
        cyclomatic_complexity = 1
        
        for keyword in complexity_keywords:
            cyclomatic_complexity += len(re.findall(r'\b' + keyword + r'\b', code))
        
        return CodeMetrics(
            lines_of_code=code_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cyclomatic_complexity,  # Simplified
            maintainability_index=max(0, 100 - cyclomatic_complexity * 2),
            technical_debt_ratio=min(1.0, cyclomatic_complexity / max(1, code_lines))
        )
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract import/require statements."""
        imports = []
        
        # ES6 imports
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                imports.append(match.group(1))
        
        return imports
    
    def _generate_suggestions(self, code: str) -> List[str]:
        """Generate JavaScript-specific suggestions."""
        suggestions = []
        
        # Check for var usage
        if re.search(r'\bvar\s+', code):
            suggestions.append("Consider using 'let' or 'const' instead of 'var'")
        
        # Check for == usage
        if re.search(r'==(?!=)', code):
            suggestions.append("Consider using '===' for strict equality")
        
        # Check for console.log in production-like code
        if re.search(r'console\.log', code):
            suggestions.append("Remove console.log statements in production code")
        
        return suggestions


class CodeAnalysisEngine:
    """Main code analysis engine supporting multiple languages."""
    
    def __init__(self):
        self.analyzers: Dict[CodeLanguage, CodeAnalyzer] = {
            CodeLanguage.PYTHON: PythonCodeAnalyzer(),
            CodeLanguage.JAVASCRIPT: JavaScriptCodeAnalyzer(is_typescript=False),
            CodeLanguage.TYPESCRIPT: JavaScriptCodeAnalyzer(is_typescript=True),
        }
        self.analysis_cache: Dict[str, CodeAnalysisResult] = {}
    
    def detect_language(self, code: str, file_path: Optional[str] = None) -> CodeLanguage:
        """Detect programming language from code or file extension."""
        if file_path:
            path = Path(file_path)
            extension = path.suffix.lower()
            
            extension_map = {
                '.py': CodeLanguage.PYTHON,
                '.js': CodeLanguage.JAVASCRIPT,
                '.jsx': CodeLanguage.JAVASCRIPT,
                '.ts': CodeLanguage.TYPESCRIPT,
                '.tsx': CodeLanguage.TYPESCRIPT,
                '.java': CodeLanguage.JAVA,
                '.cpp': CodeLanguage.CPP,
                '.cc': CodeLanguage.CPP,
                '.cxx': CodeLanguage.CPP,
                '.c': CodeLanguage.C,
                '.cs': CodeLanguage.CSHARP,
                '.go': CodeLanguage.GO,
                '.rs': CodeLanguage.RUST,
                '.php': CodeLanguage.PHP,
                '.rb': CodeLanguage.RUBY,
                '.scala': CodeLanguage.SCALA,
                '.kt': CodeLanguage.KOTLIN,
                '.swift': CodeLanguage.SWIFT,
                '.sql': CodeLanguage.SQL,
                '.sh': CodeLanguage.SHELL,
                '.bash': CodeLanguage.SHELL,
            }
            
            if extension in extension_map:
                return extension_map[extension]
        
        # Content-based detection
        code_lower = code.lower()
        
        # Python indicators
        python_indicators = ['def ', 'import ', 'from ', 'class ', '__init__', 'self.']
        if any(indicator in code_lower for indicator in python_indicators):
            return CodeLanguage.PYTHON
        
        # JavaScript indicators
        js_indicators = ['function ', 'var ', 'let ', 'const ', '=>', 'require(']
        if any(indicator in code_lower for indicator in js_indicators):
            return CodeLanguage.JAVASCRIPT
        
        # Java indicators
        java_indicators = ['public class', 'private ', 'public static void main']
        if any(indicator in code_lower for indicator in java_indicators):
            return CodeLanguage.JAVA
        
        return CodeLanguage.UNKNOWN
    
    def analyze_code(self, code: str, file_path: Optional[str] = None, 
                    language: Optional[CodeLanguage] = None) -> CodeAnalysisResult:
        """Analyze code using appropriate language analyzer."""
        # Detect language if not provided
        if language is None:
            language = self.detect_language(code, file_path)
        
        # Check cache
        cache_key = f"{language.value}:{hash(code)}"
        if cache_key in self.analysis_cache:
            logger.debug(f"Returning cached analysis for {language.value}")
            return self.analysis_cache[cache_key]
        
        # Get appropriate analyzer
        if language in self.analyzers:
            analyzer = self.analyzers[language]
            result = analyzer.analyze(code, file_path)
        else:
            # Fallback for unsupported languages
            logger.warning(f"No analyzer available for {language.value}")
            result = CodeAnalysisResult(
                language=language,
                file_path=file_path,
                is_valid=True,  # Assume valid if we can't parse
                suggestions=[f"No analysis available for {language.value}"]
            )
        
        # Cache result
        self.analysis_cache[cache_key] = result
        
        logger.info(f"Code analysis completed for {language.value}: "
                   f"{'valid' if result.is_valid else 'invalid'}")
        
        return result
    
    def analyze_file(self, file_path: str) -> CodeAnalysisResult:
        """Analyze code from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return self.analyze_code(code, file_path)
        
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return CodeAnalysisResult(
                language=CodeLanguage.UNKNOWN,
                file_path=file_path,
                is_valid=False,
                syntax_errors=[f"File read error: {str(e)}"]
            )
    
    def get_supported_languages(self) -> List[CodeLanguage]:
        """Get list of supported programming languages."""
        return list(self.analyzers.keys())
    
    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        self.analysis_cache.clear()
        logger.info("Code analysis cache cleared")
    
    def get_analysis_summary(self, results: List[CodeAnalysisResult]) -> Dict[str, Any]:
        """Generate summary statistics from multiple analysis results."""
        if not results:
            return {}
        
        valid_results = [r for r in results if r.is_valid]
        
        summary = {
            "total_files": len(results),
            "valid_files": len(valid_results),
            "invalid_files": len(results) - len(valid_results),
            "languages": {},
            "total_elements": 0,
            "average_complexity": 0.0,
            "total_issues": 0
        }
        
        if valid_results:
            # Language distribution
            for result in valid_results:
                lang = result.language.value
                if lang not in summary["languages"]:
                    summary["languages"][lang] = 0
                summary["languages"][lang] += 1
            
            # Aggregate metrics
            total_complexity = 0
            complexity_count = 0
            
            for result in valid_results:
                summary["total_elements"] += len(result.elements)
                summary["total_issues"] += (len(result.security_issues) + 
                                          len(result.performance_issues) + 
                                          len(result.style_issues))
                
                if result.metrics:
                    total_complexity += result.metrics.cyclomatic_complexity
                    complexity_count += 1
            
            if complexity_count > 0:
                summary["average_complexity"] = total_complexity / complexity_count
        
        return summary


# Add numpy import fallback for metrics calculation
try:
    import numpy as np
except ImportError:
    # Fallback for numpy functions
    class NumpyFallback:
        @staticmethod
        def log(x):
            import math
            return math.log(x)
    
    np = NumpyFallback()


# Export main classes
__all__ = [
    'CodeLanguage',
    'CodeComplexity', 
    'CodeElement',
    'CodeMetrics',
    'CodeAnalysisResult',
    'CodeAnalyzer',
    'PythonCodeAnalyzer',
    'JavaScriptCodeAnalyzer',
    'CodeAnalysisEngine'
]