
# This is your practice file for the Day 10 Kata.
# Complete the exercises from katas/day10_code_intelligence.md here.

import ast

# --- Exercise 1: Code Analysis with AST ---

code_string = """
def greet(name):
    '''A simple function to greet someone.'''
    return f"Hello, {name}!"

class MyClass:
    def method(self):
        pass
"""

class FunctionVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # TODO: Print the function name and docstring
        print(f"Found function: {node.name}")
        # TODO: Continue visiting child nodes
        self.generic_visit(node)

print("--- Exercise 1 ---")
# TODO: Parse the code and use your visitor


# --- Exercise 2: Simple Code Generator ---

def generate_function(name: str, args: list[str], body: str) -> str:
    """
    Generates a Python function as a string.
    """
    # TODO: Implement the function generation logic
    pass

print("\n--- Exercise 2 ---")
# TODO: Generate an 'add' function and print the resulting code


# --- Exercise 3: Secure Code Executor ---

def execute_code(code_string: str):
    """
    Executes a string of Python code in a sandboxed environment.
    """
    # TODO: Define allowed globals and use exec()
    pass

print("\n--- Exercise 3 ---")
# TODO: Test with both a safe and a malicious command


# --- Exercise 4: Putting It All Together ---

print("\n--- Exercise 4 ---")
# TODO:
# 1. Generate a 'square' function string.
# 2. Analyze it with your FunctionVisitor.
# 3. Execute it and capture the result.
#    - You'll need to add a line to the executed code that calls the function
#      and stores the result in a variable, e.g., "result = square(5)".
#    - Then extract 'result' from the local scope after exec().

