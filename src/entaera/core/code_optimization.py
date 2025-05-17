"""
ENTAERA Code Optimization Engine

Day 6 Kata 6.4: Intelligent Code Optimization System

This module provides automated code optimization and refactoring capabilities:
- Performance analysis and optimization suggestions
- Code quality improvements and best practice enforcement
- Automated refactoring with pattern recognition
- Memory usage optimization and algorithm improvements
- Style consistency and maintainability enhancements
- Integration with code analysis for intelligent recommendations

The optimization engine works with the analysis and generation systems to provide
comprehensive code improvement suggestions and automated transformations.
"""

import ast
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import logging

try:
    from .code_analysis import CodeAnalysisEngine, CodeLanguage, CodeMetrics, CodeAnalysisResult
except ImportError:
    # Fallback for standalone usage
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from code_analysis import CodeAnalysisEngine, CodeLanguage, CodeMetrics, CodeAnalysisResult

try:
    from .logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)


class OptimizationType(Enum):
    """Types of code optimizations."""
    PERFORMANCE = "performance"
    MEMORY = "memory"
    READABILITY = "readability"
    MAINTAINABILITY = "maintainability"
    SECURITY = "security"
    STYLE = "style"
    ALGORITHM = "algorithm"
    PATTERN = "pattern"
    REFACTOR = "refactor"


class OptimizationPriority(Enum):
    """Priority levels for optimizations."""
    CRITICAL = "critical"      # Security issues, major bugs
    HIGH = "high"             # Performance improvements, memory leaks
    MEDIUM = "medium"         # Code quality, maintainability
    LOW = "low"               # Style issues, minor improvements


@dataclass
class OptimizationSuggestion:
    """A code optimization suggestion."""
    optimization_type: OptimizationType
    priority: OptimizationPriority
    title: str
    description: str
    original_code: str
    optimized_code: str
    line_number: Optional[int] = None
    estimated_improvement: Optional[str] = None
    rationale: str = ""
    confidence: float = 0.8  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'type': self.optimization_type.value,
            'priority': self.priority.value,
            'title': self.title,
            'description': self.description,
            'original_code': self.original_code,
            'optimized_code': self.optimized_code,
            'line_number': self.line_number,
            'estimated_improvement': self.estimated_improvement,
            'rationale': self.rationale,
            'confidence': self.confidence
        }


@dataclass
class OptimizationResult:
    """Result of code optimization analysis."""
    original_code: str
    language: CodeLanguage
    suggestions: List[OptimizationSuggestion] = field(default_factory=list)
    total_suggestions: int = 0
    critical_issues: int = 0
    high_priority_issues: int = 0
    estimated_time_savings: Optional[str] = None
    estimated_performance_gain: Optional[str] = None
    analysis_timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def get_suggestions_by_priority(self, priority: OptimizationPriority) -> List[OptimizationSuggestion]:
        """Get suggestions filtered by priority."""
        return [s for s in self.suggestions if s.priority == priority]
    
    def get_suggestions_by_type(self, opt_type: OptimizationType) -> List[OptimizationSuggestion]:
        """Get suggestions filtered by type."""
        return [s for s in self.suggestions if s.optimization_type == opt_type]


class CodeOptimizer(ABC):
    """Abstract base class for language-specific code optimizers."""
    
    @abstractmethod
    def optimize(self, code: str, analysis_result: Optional[CodeAnalysisResult] = None) -> OptimizationResult:
        """Analyze code and suggest optimizations."""
        pass
    
    @abstractmethod
    def apply_optimization(self, code: str, suggestion: OptimizationSuggestion) -> str:
        """Apply a specific optimization to code."""
        pass


class PythonOptimizer(CodeOptimizer):
    """Python-specific code optimizer."""
    
    def __init__(self):
        self.language = CodeLanguage.PYTHON
        self.optimization_patterns = self._load_optimization_patterns()
    
    def optimize(self, code: str, analysis_result: Optional[CodeAnalysisResult] = None) -> OptimizationResult:
        """Analyze Python code and suggest optimizations."""
        logger.info("Analyzing Python code for optimization opportunities")
        
        result = OptimizationResult(
            original_code=code,
            language=self.language
        )
        
        suggestions = []
        
        # Performance optimizations
        suggestions.extend(self._suggest_performance_optimizations(code))
        
        # Memory optimizations
        suggestions.extend(self._suggest_memory_optimizations(code))
        
        # Readability improvements
        suggestions.extend(self._suggest_readability_improvements(code))
        
        # Algorithm optimizations
        suggestions.extend(self._suggest_algorithm_optimizations(code))
        
        # Style improvements
        suggestions.extend(self._suggest_style_improvements(code))
        
        # Security improvements
        suggestions.extend(self._suggest_security_improvements(code))
        
        # Pattern-based refactoring
        suggestions.extend(self._suggest_pattern_refactoring(code))
        
        result.suggestions = suggestions
        result.total_suggestions = len(suggestions)
        result.critical_issues = len([s for s in suggestions if s.priority == OptimizationPriority.CRITICAL])
        result.high_priority_issues = len([s for s in suggestions if s.priority == OptimizationPriority.HIGH])
        
        logger.info(f"Found {len(suggestions)} optimization suggestions for Python code")
        return result
    
    def apply_optimization(self, code: str, suggestion: OptimizationSuggestion) -> str:
        """Apply a specific optimization to Python code."""
        try:
            # Simple replacement for now - could be more sophisticated
            return code.replace(suggestion.original_code, suggestion.optimized_code)
        except Exception as e:
            logger.error(f"Failed to apply optimization: {e}")
            return code
    
    def _suggest_performance_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest performance optimizations."""
        suggestions = []
        
        # List comprehensions vs loops
        if self._has_simple_loop_with_append(code):
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.MEDIUM,
                title="Use List Comprehension",
                description="Replace simple for loop with list comprehension for better performance",
                original_code=self._extract_loop_pattern(code),
                optimized_code=self._convert_to_list_comprehension(code),
                estimated_improvement="20-30% faster execution",
                rationale="List comprehensions are optimized at C level and avoid repeated append() calls"
            ))
        
        # String concatenation in loops
        if '+=' in code and 'for ' in code and 'str' in code.lower():
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.HIGH,
                title="Optimize String Concatenation",
                description="Use join() instead of += for string concatenation in loops",
                original_code=self._extract_string_concat_pattern(code),
                optimized_code=self._optimize_string_concatenation(code),
                estimated_improvement="Significant improvement for large strings",
                rationale="String += creates new objects each time, join() is much more efficient"
            ))
        
        # range(len()) pattern
        range_len_pattern = r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(\s*\w+\s*\)\s*\):'
        if re.search(range_len_pattern, code):
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.MEDIUM,
                title="Use enumerate() instead of range(len())",
                description="Replace range(len()) pattern with enumerate() for cleaner, faster code",
                original_code=self._extract_range_len_pattern(code),
                optimized_code=self._convert_to_enumerate(code),
                estimated_improvement="10-15% faster, more readable",
                rationale="enumerate() is optimized and avoids index lookup overhead"
            ))
        
        # Unnecessary list() calls
        if 'list(map(' in code or 'list(filter(' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MEMORY,
                priority=OptimizationPriority.MEDIUM,
                title="Remove unnecessary list() calls",
                description="Use iterators directly instead of converting to list when possible",
                original_code="list(map(...))",
                optimized_code="map(...)",
                estimated_improvement="Reduced memory usage",
                rationale="Iterators are lazy and don't create intermediate lists"
            ))
        
        return suggestions
    
    def _suggest_memory_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest memory optimizations."""
        suggestions = []
        
        # Generator expressions vs list comprehensions for large data
        if '[' in code and 'for ' in code and ']' in code and len(code.split('\\n')) > 10:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MEMORY,
                priority=OptimizationPriority.MEDIUM,
                title="Consider Generator Expressions",
                description="Use generator expressions instead of list comprehensions for large datasets",
                original_code="[x for x in large_data]",
                optimized_code="(x for x in large_data)",
                estimated_improvement="Significant memory savings for large data",
                rationale="Generators are lazy and don't store all items in memory at once"
            ))
        
        # Unnecessary variable assignments
        assignments = re.findall(r'(\w+)\s*=\s*(.+)', code)
        if len(assignments) > 5:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MEMORY,
                priority=OptimizationPriority.LOW,
                title="Review Variable Assignments",
                description="Consider if all intermediate variables are necessary",
                original_code="Multiple variable assignments",
                optimized_code="Inline expressions where appropriate",
                estimated_improvement="Reduced memory footprint",
                rationale="Fewer variables mean less memory usage and cleaner namespace"
            ))
        
        return suggestions
    
    def _suggest_readability_improvements(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest readability improvements."""
        suggestions = []
        
        # Long lines
        lines = code.split('\\n')
        long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 88]
        if long_lines:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.READABILITY,
                priority=OptimizationPriority.LOW,
                title="Break Long Lines",
                description=f"Lines {long_lines} exceed 88 characters",
                original_code=f"Line(s): {long_lines}",
                optimized_code="Break into multiple lines",
                rationale="Shorter lines improve readability and maintainability"
            ))
        
        # Magic numbers
        magic_numbers = re.findall(r'\b(?!0|1|2|10|100)\d{2,}\b', code)
        if magic_numbers:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MAINTAINABILITY,
                priority=OptimizationPriority.MEDIUM,
                title="Replace Magic Numbers",
                description="Replace magic numbers with named constants",
                original_code=f"Magic numbers: {set(magic_numbers)}",
                optimized_code="CONSTANT_NAME = value",
                rationale="Named constants improve code readability and maintainability"
            ))
        
        # Functions without docstrings
        function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        functions = re.findall(function_pattern, code)
        for func_name in functions:
            func_start = code.find(f"def {func_name}")
            func_section = code[func_start:func_start+200]
            if '"""' not in func_section and "'''" not in func_section:
                suggestions.append(OptimizationSuggestion(
                    optimization_type=OptimizationType.MAINTAINABILITY,
                    priority=OptimizationPriority.MEDIUM,
                    title=f"Add Docstring to {func_name}()",
                    description="Add docstring to improve code documentation",
                    original_code=f"def {func_name}(...):",
                    optimized_code=f'def {func_name}(...):\n    """Function description."""',
                    rationale="Docstrings improve code maintainability and help other developers"
                ))
        
        return suggestions
    
    def _suggest_algorithm_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest algorithm-level optimizations."""
        suggestions = []
        
        # Nested loops that could be optimized
        nested_loop_count = len(re.findall(r'for\s+\w+\s+in\s+.*:\s*\n\s*for\s+\w+\s+in', code))
        if nested_loop_count > 0:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.ALGORITHM,
                priority=OptimizationPriority.HIGH,
                title="Review Nested Loops",
                description="Consider if nested loops can be optimized or vectorized",
                original_code="Nested for loops",
                optimized_code="Consider using itertools, numpy, or algorithmic improvements",
                estimated_improvement="Potential O(n²) to O(n log n) or O(n) improvement",
                rationale="Nested loops often indicate opportunities for algorithmic optimization"
            ))
        
        # Linear search in loops
        if 'in ' in code and 'for ' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.ALGORITHM,
                priority=OptimizationPriority.MEDIUM,
                title="Consider Set/Dict for Fast Lookups",
                description="Use set or dict for O(1) lookups instead of list searches",
                original_code="if item in large_list:",
                optimized_code="if item in large_set:",
                estimated_improvement="O(n) to O(1) lookup time",
                rationale="Sets and dicts provide constant-time lookups vs linear search in lists"
            ))
        
        return suggestions
    
    def _suggest_style_improvements(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest style improvements."""
        suggestions = []
        
        # Variable naming
        bad_names = re.findall(r'\b[a-z]\b|\b\w*\d+\w*\b', code)
        if bad_names:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.STYLE,
                priority=OptimizationPriority.LOW,
                title="Improve Variable Names",
                description="Use more descriptive variable names",
                original_code=f"Variables: {set(bad_names)}",
                optimized_code="descriptive_variable_name",
                rationale="Clear variable names improve code readability"
            ))
        
        # Import organization
        import_lines = [line for line in code.split('\n') if line.strip().startswith('import ') or line.strip().startswith('from ')]
        if len(import_lines) > 5:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.STYLE,
                priority=OptimizationPriority.LOW,
                title="Organize Imports",
                description="Group and sort imports according to PEP8",
                original_code="Mixed import statements",
                optimized_code="Grouped: stdlib, third-party, local",
                rationale="Organized imports improve code maintainability"
            ))
        
        return suggestions
    
    def _suggest_security_improvements(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest security improvements."""
        suggestions = []
        
        # Use of eval/exec
        if 'eval(' in code or 'exec(' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.SECURITY,
                priority=OptimizationPriority.CRITICAL,
                title="Avoid eval()/exec()",
                description="Replace eval/exec with safer alternatives",
                original_code="eval() or exec()",
                optimized_code="Use ast.literal_eval() or specific parsing",
                estimated_improvement="Eliminates code injection vulnerabilities",
                rationale="eval/exec can execute arbitrary code and create security risks"
            ))
        
        # SQL injection potential
        if 'SELECT' in code.upper() and '+' in code and 'str' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.SECURITY,
                priority=OptimizationPriority.CRITICAL,
                title="Prevent SQL Injection",
                description="Use parameterized queries instead of string concatenation",
                original_code="SQL string concatenation",
                optimized_code="Use prepared statements with parameters",
                estimated_improvement="Eliminates SQL injection vulnerabilities",
                rationale="String concatenation in SQL queries can lead to injection attacks"
            ))
        
        return suggestions
    
    def _suggest_pattern_refactoring(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest design pattern improvements."""
        suggestions = []
        
        # Repeated code patterns
        lines = code.split('\n')
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        duplicated = [line for line, count in line_counts.items() if count > 2 and len(line) > 20]
        if duplicated:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PATTERN,
                priority=OptimizationPriority.MEDIUM,
                title="Extract Duplicated Code",
                description="Extract repeated code into functions or constants",
                original_code="Duplicated code blocks",
                optimized_code="Extract to helper function",
                estimated_improvement="Improved maintainability and DRY principle",
                rationale="Duplicated code violates DRY principle and increases maintenance burden"
            ))
        
        # Long functions
        function_lengths = self._analyze_function_lengths(code)
        long_functions = [name for name, length in function_lengths.items() if length > 50]
        if long_functions:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PATTERN,
                priority=OptimizationPriority.MEDIUM,
                title="Break Down Long Functions",
                description=f"Functions {long_functions} are too long",
                original_code="Long function",
                optimized_code="Break into smaller, focused functions",
                estimated_improvement="Improved testability and maintainability",
                rationale="Long functions are harder to understand, test, and maintain"
            ))
        
        return suggestions
    
    def _load_optimization_patterns(self) -> Dict[str, Any]:
        """Load optimization patterns and rules."""
        return {
            'list_comprehension': r'for\s+\w+\s+in\s+.+:\s*\n\s*\w+\.append\(',
            'string_concatenation': r'\w+\s*\+=\s*.*str',
            'range_len': r'range\s*\(\s*len\s*\(',
            'magic_numbers': r'\b(?!0|1|2|10|100)\d{2,}\b'
        }
    
    def _has_simple_loop_with_append(self, code: str) -> bool:
        """Check if code has simple loop with append pattern."""
        pattern = r'for\s+\w+\s+in\s+.+:\s*\n\s*\w+\.append\('
        return bool(re.search(pattern, code, re.MULTILINE))
    
    def _extract_loop_pattern(self, code: str) -> str:
        """Extract loop pattern for optimization."""
        # Simplified extraction
        return "for item in items:\n    result.append(transform(item))"
    
    def _convert_to_list_comprehension(self, code: str) -> str:
        """Convert loop to list comprehension."""
        return "result = [transform(item) for item in items]"
    
    def _extract_string_concat_pattern(self, code: str) -> str:
        """Extract string concatenation pattern."""
        return "result += str(item)"
    
    def _optimize_string_concatenation(self, code: str) -> str:
        """Optimize string concatenation."""
        return "result = ''.join(str(item) for item in items)"
    
    def _extract_range_len_pattern(self, code: str) -> str:
        """Extract range(len()) pattern."""
        return "for i in range(len(items)):"
    
    def _convert_to_enumerate(self, code: str) -> str:
        """Convert to enumerate."""
        return "for i, item in enumerate(items):"
    
    def _analyze_function_lengths(self, code: str) -> Dict[str, int]:
        """Analyze function lengths."""
        function_lengths = {}
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    length = getattr(node, 'end_lineno', node.lineno) - node.lineno
                    function_lengths[node.name] = length
        except SyntaxError:
            pass
        return function_lengths


class JavaScriptOptimizer(CodeOptimizer):
    """JavaScript-specific code optimizer."""
    
    def __init__(self):
        self.language = CodeLanguage.JAVASCRIPT
    
    def optimize(self, code: str, analysis_result: Optional[CodeAnalysisResult] = None) -> OptimizationResult:
        """Analyze JavaScript code and suggest optimizations."""
        logger.info("Analyzing JavaScript code for optimization opportunities")
        
        result = OptimizationResult(
            original_code=code,
            language=self.language
        )
        
        suggestions = []
        
        # Performance optimizations
        suggestions.extend(self._suggest_js_performance_optimizations(code))
        
        # Memory optimizations
        suggestions.extend(self._suggest_js_memory_optimizations(code))
        
        # Modern JS improvements
        suggestions.extend(self._suggest_modern_js_improvements(code))
        
        result.suggestions = suggestions
        result.total_suggestions = len(suggestions)
        result.critical_issues = len([s for s in suggestions if s.priority == OptimizationPriority.CRITICAL])
        result.high_priority_issues = len([s for s in suggestions if s.priority == OptimizationPriority.HIGH])
        
        logger.info(f"Found {len(suggestions)} optimization suggestions for JavaScript code")
        return result
    
    def apply_optimization(self, code: str, suggestion: OptimizationSuggestion) -> str:
        """Apply a specific optimization to JavaScript code."""
        try:
            return code.replace(suggestion.original_code, suggestion.optimized_code)
        except Exception as e:
            logger.error(f"Failed to apply JavaScript optimization: {e}")
            return code
    
    def _suggest_js_performance_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest JavaScript performance optimizations."""
        suggestions = []
        
        # Use const/let instead of var
        if 'var ' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.MEDIUM,
                title="Use const/let instead of var",
                description="Replace var with const or let for better performance and scoping",
                original_code="var variableName",
                optimized_code="const variableName",
                estimated_improvement="Better performance and clearer intent",
                rationale="const/let have block scope and are more optimized by JS engines"
            ))
        
        # Arrow functions for callbacks
        if 'function(' in code and ('map(' in code or 'filter(' in code or 'forEach(' in code):
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.LOW,
                title="Use Arrow Functions",
                description="Use arrow functions for cleaner, more efficient callbacks",
                original_code="array.map(function(item) { return item * 2; })",
                optimized_code="array.map(item => item * 2)",
                estimated_improvement="Cleaner syntax and slightly better performance",
                rationale="Arrow functions have lexical this binding and are more concise"
            ))
        
        return suggestions
    
    def _suggest_js_memory_optimizations(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest JavaScript memory optimizations."""
        suggestions = []
        
        # Avoid creating unnecessary objects in loops
        if 'for (' in code and '{' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MEMORY,
                priority=OptimizationPriority.MEDIUM,
                title="Avoid Object Creation in Loops",
                description="Move object creation outside loops when possible",
                original_code="for loop with object creation",
                optimized_code="Pre-create objects outside loop",
                estimated_improvement="Reduced memory allocation and GC pressure",
                rationale="Creating objects in tight loops can cause memory pressure"
            ))
        
        return suggestions
    
    def _suggest_modern_js_improvements(self, code: str) -> List[OptimizationSuggestion]:
        """Suggest modern JavaScript improvements."""
        suggestions = []
        
        # Template literals
        if "'" in code and '+' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.READABILITY,
                priority=OptimizationPriority.LOW,
                title="Use Template Literals",
                description="Replace string concatenation with template literals",
                original_code="'Hello ' + name + '!'",
                optimized_code="`Hello ${name}!`",
                estimated_improvement="Cleaner, more readable string interpolation",
                rationale="Template literals are more readable and less error-prone"
            ))
        
        # Destructuring assignment
        if '.property' in code or '[0]' in code:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.READABILITY,
                priority=OptimizationPriority.LOW,
                title="Use Destructuring Assignment",
                description="Use destructuring for cleaner object/array access",
                original_code="const value = object.property",
                optimized_code="const { property: value } = object",
                estimated_improvement="More concise and expressive code",
                rationale="Destructuring makes code more readable and reduces repetition"
            ))
        
        return suggestions


class CodeOptimizationEngine:
    """Main optimization engine supporting multiple languages."""
    
    def __init__(self):
        self.optimizers: Dict[CodeLanguage, CodeOptimizer] = {
            CodeLanguage.PYTHON: PythonOptimizer(),
            CodeLanguage.JAVASCRIPT: JavaScriptOptimizer(),
        }
        self.analysis_engine = CodeAnalysisEngine()
    
    def optimize_code(self, code: str, language: Optional[CodeLanguage] = None) -> OptimizationResult:
        """Optimize code and return suggestions."""
        # Detect language if not provided
        if language is None:
            language = self.analysis_engine.detect_language(code)
        
        logger.info(f"Optimizing {language.value} code")
        
        # Get code analysis first
        analysis_result = self.analysis_engine.analyze_code(code, language=language)
        
        # Get appropriate optimizer
        if language in self.optimizers:
            optimizer = self.optimizers[language]
            result = optimizer.optimize(code, analysis_result)
        else:
            logger.warning(f"No optimizer available for {language.value}")
            result = OptimizationResult(
                original_code=code,
                language=language,
                suggestions=[OptimizationSuggestion(
                    optimization_type=OptimizationType.STYLE,
                    priority=OptimizationPriority.LOW,
                    title="No Optimizer Available",
                    description=f"No optimization engine available for {language.value}",
                    original_code=code[:100] + "...",
                    optimized_code="Manual optimization required",
                    rationale=f"Optimization support for {language.value} not yet implemented"
                )]
            )
        
        # Add analysis-based suggestions
        if analysis_result.is_valid:
            result.suggestions.extend(self._create_analysis_based_suggestions(analysis_result))
        
        # Update counts
        result.total_suggestions = len(result.suggestions)
        result.critical_issues = len(result.get_suggestions_by_priority(OptimizationPriority.CRITICAL))
        result.high_priority_issues = len(result.get_suggestions_by_priority(OptimizationPriority.HIGH))
        
        logger.info(f"Optimization completed: {result.total_suggestions} suggestions, "
                   f"{result.critical_issues} critical, {result.high_priority_issues} high priority")
        
        return result
    
    def apply_optimization(self, code: str, suggestion: OptimizationSuggestion, 
                          language: Optional[CodeLanguage] = None) -> str:
        """Apply a specific optimization suggestion."""
        if language is None:
            language = self.analysis_engine.detect_language(code)
        
        if language in self.optimizers:
            optimizer = self.optimizers[language]
            return optimizer.apply_optimization(code, suggestion)
        else:
            logger.warning(f"Cannot apply optimization: no optimizer for {language.value}")
            return code
    
    def get_optimization_summary(self, result: OptimizationResult) -> Dict[str, Any]:
        """Get a summary of optimization results."""
        priority_counts = {
            'critical': len(result.get_suggestions_by_priority(OptimizationPriority.CRITICAL)),
            'high': len(result.get_suggestions_by_priority(OptimizationPriority.HIGH)),
            'medium': len(result.get_suggestions_by_priority(OptimizationPriority.MEDIUM)),
            'low': len(result.get_suggestions_by_priority(OptimizationPriority.LOW))
        }
        
        type_counts = {}
        for opt_type in OptimizationType:
            type_counts[opt_type.value] = len(result.get_suggestions_by_type(opt_type))
        
        return {
            'total_suggestions': result.total_suggestions,
            'language': result.language.value,
            'priority_distribution': priority_counts,
            'type_distribution': type_counts,
            'analysis_timestamp': result.analysis_timestamp.isoformat()
        }
    
    def _create_analysis_based_suggestions(self, analysis: CodeAnalysisResult) -> List[OptimizationSuggestion]:
        """Create optimization suggestions based on code analysis."""
        suggestions = []
        
        # Complexity-based suggestions
        if analysis.metrics and analysis.metrics.cyclomatic_complexity > 10:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.MAINTAINABILITY,
                priority=OptimizationPriority.HIGH,
                title="Reduce Cyclomatic Complexity",
                description=f"Complexity score of {analysis.metrics.cyclomatic_complexity} is high",
                original_code="Complex function",
                optimized_code="Break into smaller functions",
                estimated_improvement="Improved maintainability and testability",
                rationale="High complexity makes code harder to understand and maintain"
            ))
        
        # Security issues from analysis
        for issue in analysis.security_issues:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.SECURITY,
                priority=OptimizationPriority.CRITICAL,
                title="Security Issue",
                description=issue,
                original_code="Security vulnerability",
                optimized_code="Apply security best practices",
                rationale="Security issues pose risk to application safety"
            ))
        
        # Performance issues from analysis
        for issue in analysis.performance_issues:
            suggestions.append(OptimizationSuggestion(
                optimization_type=OptimizationType.PERFORMANCE,
                priority=OptimizationPriority.HIGH,
                title="Performance Issue",
                description=issue,
                original_code="Performance anti-pattern",
                optimized_code="Apply performance optimization",
                rationale="Performance issues can impact user experience"
            ))
        
        return suggestions
    
    def get_supported_languages(self) -> List[CodeLanguage]:
        """Get list of supported optimization languages."""
        return list(self.optimizers.keys())


# Export main classes
__all__ = [
    'OptimizationType',
    'OptimizationPriority',
    'OptimizationSuggestion',
    'OptimizationResult',
    'CodeOptimizer',
    'PythonOptimizer',
    'JavaScriptOptimizer',
    'CodeOptimizationEngine'
]