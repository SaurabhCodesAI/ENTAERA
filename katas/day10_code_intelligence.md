
# ENTAERA Kata - Day 10: The Code Intelligence Suite

## 🎯 Learning Objectives

A key feature of advanced AI assistants is the ability to understand and manipulate code. Today, you will build the foundational components of a "Code Intelligence Suite," learning how to analyze, generate, and execute code programmatically.

- **Use Python's `ast` (Abstract Syntax Tree) module to parse and analyze Python code.**
- **Extract meaningful information from code, such as function names and docstrings.**
- **Implement a simple code generator that creates a Python function from a template.**
- **Design a secure code execution engine that runs code in a restricted environment.**
- **Understand the security risks of executing arbitrary code and how to mitigate them.**

---

## 🧠 For the Absolute Beginner

### What is an Abstract Syntax Tree (AST)?
When Python looks at your code, it doesn't see text. It sees a structure, like a family tree. An **Abstract Syntax Tree (AST)** is that tree. There's a root for the whole file, branches for classes and functions, and leaves for individual operations like `a + b`. By walking this tree, a program can understand the code's structure and meaning without actually running it. This is how tools like code formatters and linters work.

### Why is `exec()` Dangerous?
The `exec()` function is a powerful but dangerous tool that executes a string as Python code. If you pass it a string that comes from a user, they could type anything, like `'import os; os.system("rm -rf /")'`, which would try to delete your entire hard drive. This is called a **code injection** vulnerability. To use `exec()` safely, you must run it in a **sandbox**—a restricted environment where it can't access dangerous modules like `os` or the file system.

---

## 📚 Theory & Links

Before you begin, study the implementations in:
- `src/entaera/core/code_analysis.py`
- `src/entaera/core/code_generation.py`
- `src/entaera/core/code_execution.py`

Key concepts to focus on:
- **Abstract Syntax Tree (AST)**: A tree representation of the abstract syntactic structure of source code. Each node of the tree denotes a construct occurring in the code.
- **`ast` Module**: Python's built-in library for working with ASTs. You can parse code into a tree, walk the tree, and even modify it.
- **`ast.NodeVisitor`**: A class that provides a way to visit every node in an AST, making it easy to find specific elements like function definitions.
- **Code Generation**: The process of programmatically creating source code. This can range from simple string formatting to complex AST manipulation.
- **Sandboxing**: The practice of running code in a restricted environment to prevent it from accessing sensitive resources or performing malicious actions. Python's `exec()` function can be dangerous if not used carefully.

---

## 🚀 Project-Level Deep Dive: Advanced Concepts

### AST Transformation
Beyond just visiting nodes, you can transform the tree. The `ast.NodeTransformer` class allows you to replace nodes in the AST. For example, you could write a transformer that finds every number literal in the code and doubles it. After transforming the tree, you can use `ast.unparse()` to convert the modified tree back into source code. This is the foundation of automated refactoring tools and code transpilers (e.g., converting modern Python syntax to an older version).

### Static Analysis
The `ast` module is the heart of **static analysis**: analyzing code without executing it. Tools like `pylint` (for finding errors), `black` (for formatting), and `mypy` (for type checking) all parse the code into an AST as their first step. By building custom visitors, you can enforce project-specific coding standards, find potential bugs, or gather metrics about code complexity.

### Advanced Sandboxing
A simple dictionary of allowed globals is a good first step, but it's not foolproof. Determined attackers can sometimes escape such sandboxes (e.g., through object introspection like `().__class__.__base__...`). Production-grade sandboxing requires multiple layers:
- **Process-level isolation**: Running the code in a separate process with a different user ID that has very limited permissions.
- **Filesystem jails**: Using `chroot` to restrict the process's view of the filesystem to a single directory.
- **Seccomp filters**: Using a Linux kernel feature (`seccomp-bpf`) to restrict the specific system calls the process is allowed to make (e.g., blocking all network access).
- **Containers**: Using technologies like Docker or gVisor to provide strong kernel-level isolation.

---

## 💻 Exercises

Create a new Python file named `katas/day10_practice.py` and complete the following exercises.

### Exercise 1: Code Analysis with AST

1.  Import the `ast` module.
2.  Define a string containing a simple Python function:
    ```python
    code_string = """
    def greet(name):
        '''A simple function to greet someone.'''
        return f"Hello, {name}!"
    """
    ```
3.  Use `ast.parse(code_string)` to create an AST object.
4.  Create a class `FunctionVisitor` that inherits from `ast.NodeVisitor`.
5.  Implement the `visit_FunctionDef` method in your class. This method is automatically called for every function definition node in the tree.
6.  Inside `visit_FunctionDef`, print the function's name (`node.name`) and its docstring (`ast.get_docstring(node)`).
7.  Instantiate your visitor and call its `visit()` method with the parsed AST.

### Exercise 2: Simple Code Generator

1.  Create a function `generate_function(name: str, args: list[str], body: str) -> str`.
2.  This function should use an f-string or string template to generate a Python function.
3.  The template should look like this:
    ```python
    def {name}({args_string}):
        {body}
    ```
4.  You will need to format the `args` list into a comma-separated string.
5.  Test it by generating a function `add(a, b)` with the body `return a + b`. Print the resulting code string.

### Exercise 3: Secure Code Executor

1.  Create a function `execute_code(code_string: str, allowed_globals: dict = None)`.
2.  This function will use Python's built-in `exec()` function to run code.
3.  `exec()` takes optional arguments for the global and local scope. To create a sandbox, provide a restricted dictionary for the globals.
4.  The `allowed_globals` dictionary will define everything the executed code can "see." For safety, it should be minimal. A good start is to only allow built-in functions that are considered safe.
    - `{'__builtins__': {'print': print, 'len': len}}`
5.  Call `exec(code_string, allowed_globals)`.
6.  Test it with a safe command: `execute_code('print("Hello from exec!")')`.
7.  Test it with a malicious command: `execute_code('import os; os.system("echo Malicious command")')`. This should fail with a `NameError` because `os` is not in your `allowed_globals`.

### Exercise 4: Putting It All Together

1.  Use your `generate_function` to create a function that calculates the square of a number.
2.  Use your `FunctionVisitor` to analyze the generated code and print its name.
3.  Use your `execute_code` to run the generated code string. This is tricky because `exec` doesn't return a value. You'll need to modify your execution environment to capture the result.
    - One way is to pass a `locals` dictionary to `exec` and extract the result from it after execution.
    ```python
    local_scope = {}
    exec(code_to_run, global_scope, local_scope)
    result = local_scope['result_variable']
    ```

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What is an Abstract Syntax Tree (AST), and how is it useful for tools like linters and code formatters?**
    - *Answer Hint:* It's a tree representation of code structure. It's useful because it allows tools to understand the code's intent and structure programmatically. A formatter can use it to rebuild the code with consistent spacing, and a linter can use it to find patterns that are likely to be bugs (e.g., a variable that is assigned but never used).
2.  **What are the major security risks of using `exec()` or `eval()` in a Python application, especially one that processes external input?**
    - *Answer Hint:* The primary risk is **Arbitrary Code Execution**. If an attacker can control the string passed to `exec()`, they can run any code they want with the same permissions as your application. This could be used to steal data, delete files, or take over the server.

### Intermediate
3.  **Besides restricting globals, what are some other techniques for sandboxing Python code?**
    - *Answer Hint:* Multi-layered approaches are best. This includes running the code in a **separate, unprivileged process**, using **filesystem jails (`chroot`)** to limit file access, and using kernel-level features like **seccomp** to restrict the system calls the process can make (e.g., blocking network access). Using **containers** (like Docker) is a very common and effective method.
4.  **How could you use the `ast` module to automatically refactor code, for example, to rename a variable everywhere it appears in a file?**
    - *Answer Hint:* You would use an `ast.NodeTransformer`. You'd create a class that inherits from it and implement methods like `visit_Name`. In this method, you'd check if the node's ID (`node.id`) is the variable name you want to change. If it is, you create a *new* `Name` node with the new variable name and return it. The transformer will automatically replace the old node with your new one in the tree. Finally, you'd unparse the transformed tree back to source code.
5.  **What is the difference between `ast.parse()`, `compile()`, and `exec()`? Describe the pipeline from source code to execution.**
    - *Answer Hint:* It's a three-step process: 1) **Parsing**: `ast.parse(source_code)` takes a string of source code and converts it into an AST object. 2) **Compilation**: `compile(ast_object, ...)` takes an AST object and compiles it into a `code` object (Python bytecode). 3) **Execution**: `exec(code_object)` takes a `code` object and executes it.

### Advanced
6.  **What is "symbolic execution" and how does it relate to static analysis?**
    - *Answer Hint:* Symbolic execution is an advanced static analysis technique where a program is "executed" using symbolic variables instead of concrete values. For example, instead of running `x + 10` with `x=5`, it runs it with `x` as a symbol. This allows the analysis to explore many possible paths through the code at once and can be used to mathematically prove properties about the code, such as the absence of certain bugs or security vulnerabilities.
7.  **The CPython interpreter is written in C. How does it go from a Python source file to something the machine can execute?**
    - *Answer Hint:* It's a multi-stage process. First, the `.py` source file is parsed into an AST. The AST is then compiled into Python bytecode (this is what's stored in `.pyc` files). This bytecode is a platform-independent set of instructions. Finally, the Python Virtual Machine (PVM), which is the main loop of the CPython interpreter, takes this bytecode and executes it one instruction at a time. It's an interpreter for the bytecode. This is different from a language like C, which is compiled directly to machine code that the CPU executes natively.
