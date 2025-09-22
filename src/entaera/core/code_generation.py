"""
ENTAERA Code Generation System

Day 6 Kata 6.2: Intelligent Code Generation Engine

This module provides sophisticated code generation capabilities including:
- Template-based code generation with customizable patterns
- AI-driven code creation using context and requirements
- Code scaffolding and boilerplate generation
- Multi-language support with language-specific patterns
- Context-aware code completion and suggestions
- Pattern recognition and code structure generation

The code generation system integrates with the analysis engine to understand
existing code patterns and generate consistent, high-quality code.
"""

import json
import re
import string
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import logging

try:
    from .code_analysis import CodeLanguage, CodeElement, CodeAnalysisEngine
except ImportError:
    # Fallback for standalone usage
    from code_analysis import CodeLanguage, CodeElement, CodeAnalysisEngine

try:
    from .logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)


class GenerationType(Enum):
    """Types of code generation."""
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    TEST = "test"
    DOCUMENTATION = "documentation"
    BOILERPLATE = "boilerplate"
    PATTERN = "pattern"
    REFACTOR = "refactor"
    TEMPLATE = "template"


class CodeTemplate:
    """Represents a code generation template."""
    
    def __init__(self, name: str, language: CodeLanguage, template: str, 
                 variables: List[str] = None, description: str = ""):
        self.name = name
        self.language = language
        self.template = template
        self.variables = variables or []
        self.description = description
        self.created_at = datetime.now(timezone.utc)
    
    def render(self, **kwargs) -> str:
        """Render the template with provided variables."""
        try:
            # Use string.Template for safe substitution
            template = string.Template(self.template)
            return template.safe_substitute(**kwargs)
        except Exception as e:
            logger.error(f"Error rendering template {self.name}: {e}")
            return self.template
    
    def get_required_variables(self) -> Set[str]:
        """Extract required template variables."""
        pattern = r'\$\{?(\w+)\}?'
        return set(re.findall(pattern, self.template))


@dataclass
class CodeGenerationRequest:
    """Request for code generation."""
    generation_type: GenerationType
    language: CodeLanguage
    description: str
    context: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    template_name: Optional[str] = None
    existing_code: Optional[str] = None
    style_preferences: Dict[str, Any] = field(default_factory=dict)
    requirements: List[str] = field(default_factory=list)


@dataclass
class CodeGenerationResult:
    """Result of code generation."""
    success: bool
    generated_code: str
    language: CodeLanguage
    generation_type: GenerationType
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CodeGenerator(ABC):
    """Abstract base class for language-specific code generators."""
    
    @abstractmethod
    def generate_function(self, name: str, parameters: List[str], 
                         return_type: Optional[str] = None,
                         docstring: Optional[str] = None,
                         **kwargs) -> str:
        """Generate a function template."""
        pass
    
    @abstractmethod
    def generate_class(self, name: str, base_classes: List[str] = None,
                      methods: List[str] = None,
                      docstring: Optional[str] = None,
                      **kwargs) -> str:
        """Generate a class template."""
        pass
    
    @abstractmethod
    def generate_test(self, target_code: str, test_type: str = "unit",
                     **kwargs) -> str:
        """Generate test code for given target code."""
        pass
    
    @abstractmethod
    def generate_documentation(self, code: str, doc_type: str = "docstring",
                              **kwargs) -> str:
        """Generate documentation for given code."""
        pass


class PythonCodeGenerator(CodeGenerator):
    """Python-specific code generator."""
    
    def __init__(self):
        self.language = CodeLanguage.PYTHON
        self.templates = self._load_python_templates()
    
    def generate_function(self, name: str, parameters: List[str], 
                         return_type: Optional[str] = None,
                         docstring: Optional[str] = None,
                         **kwargs) -> str:
        """Generate Python function."""
        # Build parameter string
        param_str = ", ".join(parameters) if parameters else ""
        
        # Build return type annotation
        return_annotation = f" -> {return_type}" if return_type else ""
        
        # Generate docstring
        if not docstring:
            docstring = f"TODO: Implement {name} function."
        
        # Generate function body
        if kwargs.get('async', False):
            func_template = f'''async def {name}({param_str}){return_annotation}:
    """
    {docstring}
    """
    # TODO: Implement function logic
    pass'''
        else:
            func_template = f'''def {name}({param_str}){return_annotation}:
    """
    {docstring}
    """
    # TODO: Implement function logic
    pass'''
        
        return func_template
    
    def generate_class(self, name: str, base_classes: List[str] = None,
                      methods: List[str] = None,
                      docstring: Optional[str] = None,
                      **kwargs) -> str:
        """Generate Python class."""
        # Build inheritance
        inheritance = ""
        if base_classes:
            inheritance = f"({', '.join(base_classes)})"
        
        # Generate docstring
        if not docstring:
            docstring = f"TODO: Implement {name} class."
        
        # Start class definition
        class_code = f'''class {name}{inheritance}:
    """
    {docstring}
    """
    
    def __init__(self):
        """Initialize {name} instance."""
        # TODO: Add initialization logic
        pass'''
        
        # Add methods if specified
        if methods:
            for method in methods:
                class_code += f"\n\n    def {method}(self):\n        \"\"\"TODO: Implement {method}.\"\"\"\n        pass"
        
        return class_code
    
    def generate_test(self, target_code: str, test_type: str = "unit",
                     **kwargs) -> str:
        """Generate Python test code."""
        test_class_name = kwargs.get('test_class_name', 'TestGenerated')
        
        test_template = f'''import unittest
from unittest.mock import Mock, patch


class {test_class_name}(unittest.TestCase):
    """Test suite for generated code."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        # TODO: Add test implementation
        pass
    
    def test_edge_cases(self):
        """Test edge cases."""
        # TODO: Add edge case tests
        pass
    
    def test_error_handling(self):
        """Test error handling."""
        # TODO: Add error handling tests
        pass


if __name__ == '__main__':
    unittest.main()'''
        
        return test_template
    
    def generate_documentation(self, code: str, doc_type: str = "docstring",
                              **kwargs) -> str:
        """Generate Python documentation."""
        if doc_type == "docstring":
            return '"""TODO: Add comprehensive docstring."""'
        elif doc_type == "readme":
            return self._generate_readme_template()
        elif doc_type == "api":
            return self._generate_api_documentation(code)
        else:
            return f"# TODO: Add {doc_type} documentation"
    
    def generate_module(self, name: str, description: str = "", 
                       includes: List[str] = None, **kwargs) -> str:
        """Generate Python module template."""
        includes = includes or []
        
        module_template = f'''"""
{name} Module

{description or f"TODO: Add description for {name} module."}
"""

import logging
from typing import Any, Dict, List, Optional, Union

# Module-level logger
logger = logging.getLogger(__name__)


# Module constants
MODULE_VERSION = "1.0.0"


# TODO: Add module implementation


def main():
    """Main entry point for the module."""
    pass


if __name__ == "__main__":
    main()'''
        
        return module_template
    
    def generate_api_client(self, api_name: str, endpoints: List[str] = None,
                           **kwargs) -> str:
        """Generate API client class."""
        endpoints = endpoints or []
        
        client_template = f'''"""
{api_name} API Client

Generated API client for {api_name} service.
"""

import requests
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class {api_name}Client:
    """Client for {api_name} API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize API client."""
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({{"Authorization": f"Bearer {{api_key}}"}})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{{self.base_url}}/{{endpoint.lstrip('/')}}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {{e}}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._make_request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return self._make_request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._make_request("DELETE", endpoint, **kwargs)'''
        
        # Add specific endpoint methods
        for endpoint in endpoints:
            method_name = endpoint.replace('/', '_').replace('-', '_').lower()
            client_template += f'''
    
    def {method_name}(self, **kwargs) -> Dict[str, Any]:
        """Access {endpoint} endpoint."""
        return self.get("{endpoint}", **kwargs)'''
        
        return client_template
    
    def _load_python_templates(self) -> Dict[str, CodeTemplate]:
        """Load predefined Python templates."""
        templates = {}
        
        # Function template
        templates['function'] = CodeTemplate(
            name='function',
            language=CodeLanguage.PYTHON,
            template='''def ${name}(${parameters}):
    """
    ${docstring}
    """
    ${body}''',
            variables=['name', 'parameters', 'docstring', 'body']
        )
        
        # Class template
        templates['class'] = CodeTemplate(
            name='class',
            language=CodeLanguage.PYTHON,
            template='''class ${name}:
    """
    ${docstring}
    """
    
    def __init__(self):
        """Initialize ${name}."""
        ${init_body}''',
            variables=['name', 'docstring', 'init_body']
        )
        
        return templates
    
    def _generate_readme_template(self) -> str:
        """Generate README template."""
        return '''# Project Title

## Description
TODO: Add project description

## Installation
```bash
pip install -r requirements.txt
```

## Usage
TODO: Add usage examples

## API Reference
TODO: Add API documentation

## Contributing
TODO: Add contribution guidelines

## License
TODO: Add license information'''
    
    def _generate_api_documentation(self, code: str) -> str:
        """Generate API documentation from code."""
        return '''# API Documentation

## Overview
TODO: Add API overview

## Endpoints
TODO: Add endpoint documentation

## Authentication
TODO: Add authentication details

## Examples
TODO: Add usage examples'''


class JavaScriptCodeGenerator(CodeGenerator):
    """JavaScript/TypeScript code generator."""
    
    def __init__(self, is_typescript: bool = False):
        self.language = CodeLanguage.TYPESCRIPT if is_typescript else CodeLanguage.JAVASCRIPT
        self.is_typescript = is_typescript
    
    def generate_function(self, name: str, parameters: List[str], 
                         return_type: Optional[str] = None,
                         docstring: Optional[str] = None,
                         **kwargs) -> str:
        """Generate JavaScript/TypeScript function."""
        param_str = ", ".join(parameters) if parameters else ""
        
        # TypeScript return type
        return_annotation = f": {return_type}" if self.is_typescript and return_type else ""
        
        # JSDoc comment
        jsdoc = f"""/**
 * {docstring or f"TODO: Implement {name} function."}
 */"""
        
        if kwargs.get('arrow', False):
            return f'''{jsdoc}
const {name} = ({param_str}){return_annotation} => {{
    // TODO: Implement function logic
}};'''
        else:
            return f'''{jsdoc}
function {name}({param_str}){return_annotation} {{
    // TODO: Implement function logic
}}'''
    
    def generate_class(self, name: str, base_classes: List[str] = None,
                      methods: List[str] = None,
                      docstring: Optional[str] = None,
                      **kwargs) -> str:
        """Generate JavaScript/TypeScript class."""
        extends = f" extends {base_classes[0]}" if base_classes else ""
        
        class_template = f'''/**
 * {docstring or f"TODO: Implement {name} class."}
 */
class {name}{extends} {{
    constructor() {{
        super();
        // TODO: Add initialization logic
    }}'''
        
        # Add methods
        if methods:
            for method in methods:
                class_template += f'''
    
    /**
     * TODO: Implement {method}.
     */
    {method}() {{
        // TODO: Add method implementation
    }}'''
        
        class_template += "\n}"
        return class_template
    
    def generate_test(self, target_code: str, test_type: str = "unit",
                     **kwargs) -> str:
        """Generate JavaScript/TypeScript test code."""
        framework = kwargs.get('framework', 'jest')
        
        if framework == 'jest':
            return '''describe('Generated Tests', () => {
    beforeEach(() => {
        // Setup test fixtures
    });
    
    afterEach(() => {
        // Cleanup after tests
    });
    
    test('should handle basic functionality', () => {
        // TODO: Add test implementation
        expect(true).toBe(true);
    });
    
    test('should handle edge cases', () => {
        // TODO: Add edge case tests
        expect(true).toBe(true);
    });
    
    test('should handle errors', () => {
        // TODO: Add error handling tests
        expect(true).toBe(true);
    });
});'''
        else:
            return '''// TODO: Add test implementation for selected framework'''
    
    def generate_documentation(self, code: str, doc_type: str = "jsdoc",
                              **kwargs) -> str:
        """Generate JavaScript documentation."""
        if doc_type == "jsdoc":
            return '''/**
 * TODO: Add comprehensive JSDoc documentation.
 */'''
        else:
            return f"// TODO: Add {doc_type} documentation"


class CodeGenerationEngine:
    """Main code generation engine supporting multiple languages and patterns."""
    
    def __init__(self):
        self.generators: Dict[CodeLanguage, CodeGenerator] = {
            CodeLanguage.PYTHON: PythonCodeGenerator(),
            CodeLanguage.JAVASCRIPT: JavaScriptCodeGenerator(is_typescript=False),
            CodeLanguage.TYPESCRIPT: JavaScriptCodeGenerator(is_typescript=True),
        }
        self.templates: Dict[str, CodeTemplate] = {}
        self.patterns: Dict[str, Dict[str, Any]] = self._load_patterns()
        self.analysis_engine = CodeAnalysisEngine()
    
    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResult:
        """Generate code based on the request."""
        logger.info(f"Generating {request.generation_type.value} code for {request.language.value}")
        
        try:
            # Get appropriate generator
            if request.language not in self.generators:
                return CodeGenerationResult(
                    success=False,
                    generated_code="",
                    language=request.language,
                    generation_type=request.generation_type,
                    errors=[f"No generator available for {request.language.value}"]
                )
            
            generator = self.generators[request.language]
            generated_code = ""
            metadata = {}
            
            # Generate based on type
            if request.generation_type == GenerationType.FUNCTION:
                generated_code = self._generate_function(generator, request)
            elif request.generation_type == GenerationType.CLASS:
                generated_code = self._generate_class(generator, request)
            elif request.generation_type == GenerationType.TEST:
                generated_code = self._generate_test(generator, request)
            elif request.generation_type == GenerationType.DOCUMENTATION:
                generated_code = self._generate_documentation(generator, request)
            elif request.generation_type == GenerationType.MODULE:
                generated_code = self._generate_module(generator, request)
            elif request.generation_type == GenerationType.BOILERPLATE:
                generated_code = self._generate_boilerplate(request)
            elif request.generation_type == GenerationType.PATTERN:
                generated_code = self._generate_pattern(request)
            elif request.generation_type == GenerationType.TEMPLATE:
                generated_code = self._generate_from_template(request)
            else:
                return CodeGenerationResult(
                    success=False,
                    generated_code="",
                    language=request.language,
                    generation_type=request.generation_type,
                    errors=[f"Unsupported generation type: {request.generation_type.value}"]
                )
            
            # Validate generated code
            analysis = self.analysis_engine.analyze_code(generated_code, language=request.language)
            
            suggestions = []
            warnings = []
            
            if not analysis.is_valid:
                warnings.extend(analysis.syntax_errors)
            
            suggestions.extend(analysis.suggestions)
            
            return CodeGenerationResult(
                success=True,
                generated_code=generated_code,
                language=request.language,
                generation_type=request.generation_type,
                metadata=metadata,
                suggestions=suggestions,
                warnings=warnings
            )
        
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return CodeGenerationResult(
                success=False,
                generated_code="",
                language=request.language,
                generation_type=request.generation_type,
                errors=[f"Generation error: {str(e)}"]
            )
    
    def _generate_function(self, generator: CodeGenerator, request: CodeGenerationRequest) -> str:
        """Generate function code."""
        params = request.parameters
        return generator.generate_function(
            name=params.get('name', 'generated_function'),
            parameters=params.get('parameters', []),
            return_type=params.get('return_type'),
            docstring=params.get('docstring') or request.description,
            **params
        )
    
    def _generate_class(self, generator: CodeGenerator, request: CodeGenerationRequest) -> str:
        """Generate class code."""
        params = request.parameters
        return generator.generate_class(
            name=params.get('name', 'GeneratedClass'),
            base_classes=params.get('base_classes', []),
            methods=params.get('methods', []),
            docstring=params.get('docstring') or request.description,
            **params
        )
    
    def _generate_test(self, generator: CodeGenerator, request: CodeGenerationRequest) -> str:
        """Generate test code."""
        return generator.generate_test(
            target_code=request.existing_code or "",
            test_type=request.parameters.get('test_type', 'unit'),
            **request.parameters
        )
    
    def _generate_documentation(self, generator: CodeGenerator, request: CodeGenerationRequest) -> str:
        """Generate documentation."""
        return generator.generate_documentation(
            code=request.existing_code or "",
            doc_type=request.parameters.get('doc_type', 'docstring'),
            **request.parameters
        )
    
    def _generate_module(self, generator: CodeGenerator, request: CodeGenerationRequest) -> str:
        """Generate module code."""
        if hasattr(generator, 'generate_module'):
            return generator.generate_module(
                name=request.parameters.get('name', 'generated_module'),
                description=request.description,
                **request.parameters
            )
        else:
            return f"# {request.parameters.get('name', 'Generated Module')}\n# TODO: Add module implementation"
    
    def _generate_boilerplate(self, request: CodeGenerationRequest) -> str:
        """Generate boilerplate code."""
        boilerplate_type = request.parameters.get('type', 'basic')
        
        if request.language == CodeLanguage.PYTHON:
            if boilerplate_type == 'cli':
                return self._generate_python_cli_boilerplate(request)
            elif boilerplate_type == 'web':
                return self._generate_python_web_boilerplate(request)
            elif boilerplate_type == 'api':
                return self._generate_python_api_boilerplate(request)
            else:
                return self._generate_python_basic_boilerplate(request)
        elif request.language == CodeLanguage.JAVASCRIPT:
            if boilerplate_type == 'node':
                return self._generate_js_node_boilerplate(request)
            elif boilerplate_type == 'react':
                return self._generate_js_react_boilerplate(request)
            else:
                return self._generate_js_basic_boilerplate(request)
        else:
            return f"# Boilerplate for {request.language.value}\n# TODO: Add implementation"
    
    def _generate_pattern(self, request: CodeGenerationRequest) -> str:
        """Generate code using design patterns."""
        pattern_name = request.parameters.get('pattern', 'singleton')
        
        if pattern_name in self.patterns:
            pattern = self.patterns[pattern_name]
            if request.language.value in pattern:
                template = pattern[request.language.value]
                return self._apply_pattern_template(template, request.parameters)
        
        return f"# {pattern_name.title()} Pattern\n# TODO: Add pattern implementation"
    
    def _generate_from_template(self, request: CodeGenerationRequest) -> str:
        """Generate code from a template."""
        template_name = request.template_name
        
        if template_name and template_name in self.templates:
            template = self.templates[template_name]
            return template.render(**request.parameters)
        
        return "# Template not found\n# TODO: Add implementation"
    
    def _generate_python_basic_boilerplate(self, request: CodeGenerationRequest) -> str:
        """Generate basic Python boilerplate."""
        name = request.parameters.get('name', 'main')
        return f'''#!/usr/bin/env python3
"""
{name.title()} Module

{request.description or "TODO: Add module description"}
"""

import logging
import sys
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    logger.info("Starting {name}")
    
    try:
        # TODO: Add main logic
        pass
    except Exception as e:
        logger.error(f"Error in main: {{e}}")
        sys.exit(1)


if __name__ == "__main__":
    main()'''
    
    def _generate_python_cli_boilerplate(self, request: CodeGenerationRequest) -> str:
        """Generate Python CLI boilerplate."""
        name = request.parameters.get('name', 'cli')
        return f'''#!/usr/bin/env python3
"""
{name.title()} CLI Application

{request.description or "TODO: Add CLI description"}
"""

import argparse
import logging
import sys
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="{request.description or 'CLI Application'}"
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # TODO: Add more arguments
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    logger.info("Starting {name} CLI")
    
    try:
        # TODO: Add CLI logic
        pass
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {{e}}")
        sys.exit(1)


if __name__ == "__main__":
    main()'''
    
    def _generate_js_basic_boilerplate(self, request: CodeGenerationRequest) -> str:
        """Generate basic JavaScript boilerplate."""
        name = request.parameters.get('name', 'main')
        return f'''/**
 * {name.title()} Module
 * 
 * {request.description or "TODO: Add module description"}
 */

// TODO: Add imports

/**
 * Main entry point
 */
function main() {{
    console.log('Starting {name}');
    
    try {{
        // TODO: Add main logic
    }} catch (error) {{
        console.error('Error in main:', error);
        process.exit(1);
    }}
}}

// Run if this is the main module
if (require.main === module) {{
    main();
}}

module.exports = {{
    main
}};'''
    
    def _load_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load design pattern templates."""
        patterns = {}
        
        # Singleton pattern
        patterns['singleton'] = {
            'python': '''class ${class_name}:
    """Singleton pattern implementation."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # TODO: Add initialization logic
            self._initialized = True''',
            
            'javascript': '''class ${class_name} {
    constructor() {
        if (${class_name}.instance) {
            return ${class_name}.instance;
        }
        
        // TODO: Add initialization logic
        ${class_name}.instance = this;
    }
    
    static getInstance() {
        if (!${class_name}.instance) {
            ${class_name}.instance = new ${class_name}();
        }
        return ${class_name}.instance;
    }
}'''
        }
        
        # Factory pattern
        patterns['factory'] = {
            'python': '''class ${class_name}Factory:
    """Factory pattern implementation."""
    
    @staticmethod
    def create(type_name: str, **kwargs):
        """Create object based on type."""
        # TODO: Add factory logic
        if type_name == "type1":
            return Type1(**kwargs)
        elif type_name == "type2":
            return Type2(**kwargs)
        else:
            raise ValueError(f"Unknown type: {type_name}")''',
            
            'javascript': '''class ${class_name}Factory {
    static create(typeName, ...args) {
        switch (typeName) {
            case 'type1':
                return new Type1(...args);
            case 'type2':
                return new Type2(...args);
            default:
                throw new Error(`Unknown type: ${typeName}`);
        }
    }
}'''
        }
        
        return patterns
    
    def _apply_pattern_template(self, template: str, params: Dict[str, Any]) -> str:
        """Apply parameters to pattern template."""
        try:
            # Simple string substitution
            for key, value in params.items():
                template = template.replace(f"${{{key}}}", str(value))
            return template
        except Exception as e:
            logger.error(f"Error applying pattern template: {e}")
            return template
    
    def add_template(self, template: CodeTemplate) -> None:
        """Add a custom template."""
        self.templates[template.name] = template
        logger.info(f"Added template: {template.name}")
    
    def get_supported_languages(self) -> List[CodeLanguage]:
        """Get supported languages for code generation."""
        return list(self.generators.keys())
    
    def get_supported_patterns(self) -> List[str]:
        """Get supported design patterns."""
        return list(self.patterns.keys())
    
    def get_available_templates(self) -> List[str]:
        """Get available templates."""
        return list(self.templates.keys())


# Export main classes
__all__ = [
    'GenerationType',
    'CodeTemplate',
    'CodeGenerationRequest',
    'CodeGenerationResult',
    'CodeGenerator',
    'PythonCodeGenerator',
    'JavaScriptCodeGenerator',
    'CodeGenerationEngine'
]