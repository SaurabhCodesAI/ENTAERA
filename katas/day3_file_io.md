
# ENTAERA Kata - Day 3: Advanced File I/O

## 🎯 Learning Objectives

Robust applications require robust file handling. Today, you will master advanced file I/O techniques, ensuring data integrity and safety. You will learn to work with different file formats and manage directories effectively.

- **Implement atomic file writes to prevent data corruption.**
- **Create context managers for safe resource handling.**
- **Read and write structured data (JSON, YAML, CSV).**
- **Perform directory and file system operations (list, find, delete).**
- **Implement a file backup mechanism.**

---

## 🧠 For the Absolute Beginner

### What is a File System?
Think of a file system as a giant digital filing cabinet. It's how your computer organizes data into **files** (like a document or a picture) and **directories** (or folders, which hold other files and folders). Every file has a **path**, which is its unique address, like `C:\Users\YourName\Documents\report.txt`.

### Why Do We Need "Safe" File Operations?
Imagine your program is saving a file, and the computer crashes halfway through. You could end up with a corrupted, half-written file. An **atomic write** is a safety mechanism that ensures a save operation either completes perfectly or not at all, preventing this kind of data corruption. A **context manager** (`with open(...) as f:`) is a Python feature that guarantees a file is properly closed after you're done with it, even if errors happen.

---

## 📚 Theory & Links

Before you begin, study the implementations in:
- `src/entaera/utils/files.py`
- `src/entaera/utils/file_ops.py`

Key concepts to focus on:
- **Atomic Writes**: The pattern of writing to a temporary file and then renaming it. This ensures that the original file is only replaced upon a successful write.
- **`pathlib` Module**: The modern, object-oriented way to handle filesystem paths.
- **Context Managers (`with` statement)**: How they ensure resources (like files) are properly closed, even if errors occur.
- **Serialization**: The process of converting Python objects into formats like JSON or YAML.
- **Error Handling**: Specific exceptions for file operations (`FileNotFoundError`, `PermissionError`).

---

## � Project-Level Deep Dive: Advanced Concepts

### Filesystem Semantics and Performance
- **Inodes**: On Unix-like systems, an inode stores metadata about a file (permissions, timestamps, location on disk). The "rename" operation is often atomic at the filesystem level because it's just a quick operation to change the pointer in the directory structure to a different inode. This is why the "write-and-rename" pattern is so effective.
- **Buffering**: When you write to a file, the operating system often doesn't write it to the disk immediately. It keeps the data in a memory "buffer" and writes it out in larger, more efficient chunks. You can force a write using `file.flush()` and `os.fsync()`. This is critical for database and transaction logs where you need to guarantee data is on disk.
- **File Locking**: In a system where multiple processes might try to write to the same file at once, you need file locks. **Advisory locks** (like `fcntl` on Linux) are a cooperative way for processes to manage access. **Mandatory locks** are enforced by the OS but are less common.

### Alternative Serialization Formats
JSON and YAML are human-readable, but not always the most efficient. For high-performance systems, especially in distributed services, you'll encounter binary formats:
- **Protocol Buffers (Protobuf)**: Developed by Google. You define your data structure in a `.proto` file, and it generates code in various languages to serialize/deserialize data into a very compact binary format. It's fast and enforces a strict schema.
- **Apache Avro**: Similar to Protobuf but often used in big data ecosystems (like Hadoop and Kafka). It stores the schema along with the data, making it very flexible for schema evolution.
- **MessagePack**: Describes itself as "like JSON, but fast and small." It's a binary format that is a drop-in replacement for JSON in many cases.

---

## �💻 Exercises

Create a new Python file named `katas/day3_practice.py` and complete the following exercises.

### Exercise 1: Atomic JSON Write

1.  Create a function `atomic_write_json(file_path: str, data: dict)`.
2.  Inside the function, implement the atomic write pattern:
    - Create a temporary file path (e.g., `file_path + ".tmp"`).
    - Write the JSON data to the temporary file.
    - If the write is successful, rename the temporary file to the final `file_path`.
    - Use a `try...finally` block to ensure the temporary file is deleted if an error occurs during the write.
3.  Test your function by writing a sample dictionary to a file.

### Exercise 2: File Handler Context Manager

1.  Create a class `SafeFileHandler`.
2.  Implement the context manager protocol (`__enter__` and `__exit__`).
3.  `__init__` should accept a `file_path` and `mode`.
4.  `__enter__` should open the file and return the file handle.
5.  `__exit__` should ensure the file is closed. It also receives exception details, which you can log.
6.  Use your context manager to write text to a file:
    ```python
    with SafeFileHandler('my_test_file.txt', 'w') as f:
        f.write('Hello from my context manager!')
    ```

### Exercise 3: Reading and Writing Different Formats

1.  Create two functions:
    - `write_data(file_path: str, data)`
    - `read_data(file_path: str)`
2.  In `write_data`, detect the file type from the `file_path` extension (`.json`, `.yaml`, `.txt`).
3.  Based on the extension, use the appropriate library (`json`, `yaml`) to dump the data to the file. For `.txt`, just write the string representation.
4.  Do the reverse in `read_data`.
5.  You will need to install `PyYAML`: `pip install pyyaml`.
6.  Test by writing and reading a dictionary to both a `.json` and a `.yaml` file.

### Exercise 4: Directory Scanner

1.  Create a function `scan_directory(path: str, extension: str) -> list`.
2.  The function should walk through the given `path` and all its subdirectories.
3.  It should return a list of all files that end with the specified `extension`.
4.  Use the `os.walk()` or `pathlib.Path.rglob()` method.
5.  Test it on a directory you create with some dummy files.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What is a "race condition" in the context of file I/O, and how do atomic writes help prevent it?**
    - *Answer Hint:* A race condition occurs when two or more processes try to access a shared resource (like a file) at the same time, leading to unpredictable outcomes. If one process reads a file while another is halfway through writing it, it gets corrupted data. Atomic writes ensure that the file is only ever seen in its complete old state or its complete new state, never in-between.
2.  **Explain what happens step-by-step when you use a `with` statement with a file. What is the benefit over a manual `try...finally`?**
    - *Answer Hint:* The `with` statement calls the object's `__enter__` method, and the return value is assigned to the `as` variable. The code inside the `with` block is executed. Regardless of whether an error occurs, the `__exit__` method is *always* called afterward. It's cleaner, less verbose, and less error-prone than writing a `try...finally` block manually every time.

### Intermediate
3.  **What are the key differences between JSON and YAML? When would you choose one over the other?**
    - *Answer Hint:* JSON is stricter, more data-interchange focused, and supported everywhere (especially in web APIs). YAML is more human-readable, supports comments, and is often preferred for configuration files where people need to edit them by hand.
4.  **What is the difference between `os.path` and `pathlib`? Why is `pathlib` generally preferred in modern Python?**
    - *Answer Hint:* `os.path` uses functions that operate on string paths (`os.path.join(a, b)`). `pathlib` uses objects, which is more intuitive and less error-prone (`Path(a) / b`). Path objects have methods directly on them (e.g., `p.exists()`, `p.read_text()`), making code cleaner and more object-oriented.
5.  **You need to process a 10 GB log file. What is an efficient way to read it line-by-line without loading the entire file into memory?**
    - *Answer Hint:* The most Pythonic way is to use a `with` statement and iterate directly over the file object: `with open('huge.log') as f: for line in f: process(line)`. This reads the file one line at a time into memory, making it extremely memory-efficient.

### Advanced
6.  **What is memory-mapped file I/O (`mmap`)? In what specific scenarios might it be more performant than standard file reading?**
    - *Answer Hint:* `mmap` maps a file directly into the process's address space. This allows you to treat the file as if it were a large array or string in memory, without needing to `read()` it explicitly. The OS handles loading pages of the file into memory as you access them. It can be much faster for random access patterns (jumping around in a file) because you don't need to perform explicit `seek()` and `read()` calls.
7.  **Your application writes logs, but you're concerned about the performance impact of disk I/O. Describe a strategy to decouple the logging calls in your application from the actual disk writes.**
    - *Answer Hint:* Use a queue-based logging handler. The main application thread would simply put a log message onto an in-memory `queue.Queue`. A separate background thread would be responsible for pulling messages from the queue and writing them to disk. This way, the main application's execution is not blocked by slow disk I/O. Python's `logging.handlers.QueueHandler` and `QueueListener` are designed for this.
