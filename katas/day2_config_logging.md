
# ENTAERA Kata - Day 2: Configuration & Logging

## 🎯 Learning Objectives

Today's kata focuses on two fundamental pillars of any robust application: configuration management and logging. You will learn how to manage application settings cleanly using Pydantic and how to set up a powerful, structured logging system.

- **Use Pydantic for type-safe, validated configuration.**
- **Load settings from environment variables and `.env` files.**
- **Implement structured JSON logging for machine-readable logs.**
- **Create custom log formatters, including colored output for development.**
- **Manage log rotation and file handling.**

---

## 🧠 For the Absolute Beginner

### What is Configuration?
Imagine you have a setting in your app, like a password or a server name. You don't want to write it directly in your code (this is called "hardcoding" and is bad practice). **Configuration** is the process of managing these settings externally. **Environment variables** are a common way to do this. They are variables that live outside your application, in the operating system, so you can change them without changing your code. A `.env` file is just a convenient way to manage these variables for a specific project.

### What is Logging?
When your program runs, things happen. Sometimes it works, sometimes it fails. **Logging** is the process of recording these events. Instead of just using `print()`, which is temporary and unstructured, logging allows you to write messages to a file or the console with important context, like a timestamp, the severity (e.g., `INFO`, `WARNING`, `ERROR`), and where the message came from.

---

## 📚 Theory & Links

Before you begin, study the implementations in:
- `src/entaera/core/config.py`
- `src/entaera/core/logger.py`

Key concepts to focus on:
- **Pydantic `BaseSettings`**: How it automatically reads from environment variables.
- **Field Validation**: Using `field_validator` to enforce rules (e.g., `temperature` range).
- **Nested Models**: How `ApplicationSettings` is composed of `APIProviderSettings` and `ServerSettings`.
- **Logging `Formatter`**: The base class for creating custom log formats.
- **`logging.handlers.RotatingFileHandler`**: For managing log file size and backups.
- **Context-aware Logging**: How `request_id` is managed using `contextvars`.

---

## � Project-Level Deep Dive: Advanced Concepts

### Hierarchical & Dynamic Configuration
In large systems, you might have default settings, settings for a "staging" environment, and settings for "production." Advanced configuration management involves layering these. You might use a default YAML file, override it with a `production.yaml`, and then override specific values with environment variables. Libraries like `Dynaconf` are built for this.

### Secrets Management
Storing API keys in `.env` files is fine for development, but not for production. Real-world applications use **secrets management** tools like **HashiCorp Vault**, **AWS Secrets Manager**, or **Azure Key Vault**. Your application would authenticate with the vault at startup and securely fetch the secrets it needs, rather than reading them from a file on disk.

### Asynchronous and Centralized Logging
When you have many servers or services running, writing logs to individual files becomes unmanageable. In production, applications often send their logs to a **centralized logging platform** (like **Splunk**, **Datadog**, or the **ELK Stack**—Elasticsearch, Logstash, Kibana). This allows you to search, analyze, and create alerts from all your logs in one place. To avoid blocking the application, logs are often sent over the network asynchronously.

---

## �💻 Exercises

Create a new Python file named `katas/day2_practice.py` and complete the following exercises.

### Exercise 1: Basic Pydantic Settings

1.  Define a Pydantic `BaseModel` called `DatabaseSettings`.
2.  It should have the following fields with default values:
    - `host: str = "localhost"`
    - `port: int = 5432`
    - `user: str = "admin"`
    - `password: str` (no default)
3.  Add a `field_validator` for `port` to ensure it's a valid port number (between 1024 and 65535).
4.  Instantiate your model with and without a password to see how it behaves.

### Exercise 2: Environment-backed Settings

1.  Change `DatabaseSettings` to inherit from Pydantic's `BaseSettings`.
2.  Add a `SettingsConfigDict` to prefix environment variables with `MYAPP_`.
    - Example: `port` should be loaded from `MYAPP_PORT`.
3.  Set the `MYAPP_PASSWORD` environment variable in your script using `os.environ`.
4.  Instantiate `DatabaseSettings` and verify that it loads the password from the environment.

### Exercise 3: Simple Log Formatter

1.  Create a function `setup_simple_logging()`.
2.  Inside, get the root logger (`logging.getLogger()`).
3.  Create a `logging.StreamHandler` to print logs to the console.
4.  Create a `logging.Formatter` with the format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.
5.  Add the formatter to the handler, and the handler to the logger.
6.  Set the logger's level to `INFO`.
7.  Test it by logging a few messages.

### Exercise 4: JSON Logging

1.  Create a custom formatter class `MyJSONFormatter` that inherits from `logging.Formatter`.
2.  Override the `format` method. It receives a `LogRecord` object.
3.  Inside `format`, create a dictionary containing:
    - `timestamp`: `record.created` (as an ISO 8601 string).
    - `level`: `record.levelname`.
    - `message`: `record.getMessage()`.
    - `logger_name`: `record.name`.
4.  Use `json.dumps()` to convert the dictionary to a JSON string and return it.
5.  Modify your `setup_simple_logging` function to use this new formatter and log a message with an `extra` dictionary (e.g., `logger.info("User logged in", extra={'user_id': 123})`). You will need to adapt your formatter to include the `extra` fields.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What are the main advantages of using Pydantic for configuration over simple environment variables or a plain dictionary?**
    - *Answer Hint:* Type casting (e.g., "8000" becomes `int(8000)`), validation (ensuring values are in a valid range), and self-documentation (the model itself shows what settings are available).
2.  **Why is structured (e.g., JSON) logging preferred in production environments?**
    - *Answer Hint:* It's machine-readable. This allows you to easily filter, search, and aggregate logs (e.g., "show me all `ERROR` logs from the `payment-service` where `user_id` is `42`").

### Intermediate
3.  **How does Pydantic's `BaseSettings` prioritize configuration sources (e.g., environment vs. `.env` file vs. model defaults)?**
    - *Answer Hint:* There's a clear priority chain. Typically, arguments passed directly to the model's constructor come first, then environment variables, then values from a `.env` file, and finally the default values defined in the model.
4.  **Explain the difference between a `Logger`, a `Handler`, and a `Formatter` in Python's `logging` module.**
    - *Answer Hint:* `Logger` is the entry point—what you call in your code (`logger.info(...)`). `Handler` determines where the log message goes (e.g., to the console, a file, over the network). `Formatter` determines what the log message looks like (the format). A logger can have multiple handlers.
5.  **You need to log sensitive information, but it must not appear in the log files. How would you approach this?**
    - *Answer Hint:* The best way is to use a `logging.Filter`. You can create a filter that redacts or removes certain fields (like `password` or `api_key`) from the `LogRecord` before it ever reaches the formatter and handler.

### Advanced
6.  **Describe a scenario where you would need to configure logging with a dictionary instead of calling functions like `addHandler`. What is the benefit of `logging.config.dictConfig`?**
    - *Answer Hint:* `dictConfig` is ideal for complex logging topologies, especially when the configuration is loaded from a file (like YAML or JSON). It allows you to declaratively define multiple loggers, handlers, and formatters all at once, which is much cleaner than a long series of imperative function calls. It's the standard for configuring logging in frameworks like Django or FastAPI.
7.  **What is a "correlation ID" (or "request ID") and why is it essential in a microservices architecture? How does the `contextvars` module help implement this?**
    - *Answer Hint:* In a system where one user request might trigger a chain of calls across multiple services, a correlation ID is a unique identifier that is passed along with every call. It allows you to trace the entire journey of that single request across all services' logs. `contextvars` is perfect for this because it allows you to store this ID in a way that is local to the current execution context (like a single request) without having to pass it as an argument to every single function.
