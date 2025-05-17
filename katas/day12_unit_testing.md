
# ENTAERA Kata - Day 12: Unit Testing with Pytest

## 🎯 Learning Objectives

Writing code is only half the battle. Ensuring it works correctly and continues to work as you make changes is just as important. Today, you will learn the fundamentals of unit testing in Python using the `pytest` framework. You will write tests for some of the components you've built in previous katas.

- **Understand the purpose and value of unit testing.**
- **Write simple test functions using `pytest`.**
- **Use `assert` statements to check for expected outcomes.**
- **Learn how to test for expected exceptions using `pytest.raises`.**
- **Use "mocking" to isolate the code you are testing from its dependencies.**
- **Structure a test file and run tests from the command line.**

---

## 🧠 For the Absolute Beginner

### What is a Unit Test?
A **unit test** is a small, automated check to see if a tiny, isolated piece (a "unit") of your code works as expected. A unit is typically a single function or method. You write code that calls your function with a specific input and then **asserts** that the output is what you expected. If the assertion is true, the test passes. If it's false, the test fails, and you know you have a bug to fix.

### What is Mocking?
Imagine you're testing the engine of a car. You don't need the wheels, the seats, or the radio to do it. You just need the engine. **Mocking** is the process of replacing the other parts of the car (the "dependencies") with fake, lightweight substitutes. When we test a function that calls an external API, we don't want to *actually* call the API in our test. It would be slow and unreliable. Instead, we "mock" the API, replacing it with a fake object that instantly returns a predictable response. This lets us test our function's logic in isolation.

---

## 📚 Theory & Links

Before you begin, study the existing test file:
- `tests/unit/test_day2_kata.py`

And review the official `pytest` documentation:
- [pytest documentation](https://docs.pytest.org/en/stable/)

Key concepts to focus on:
- **`pytest`**: A popular, feature-rich testing framework for Python that makes writing tests simple and scalable.
- **Test Discovery**: How `pytest` automatically finds files named `test_*.py` or `*_test.py` and functions named `test_*`.
- **Assertions**: The `assert` keyword is used to declare that something must be true. If the condition is false, the test fails.
- **Fixtures**: A powerful `pytest` feature for providing a fixed baseline of data or objects for your tests. (We will touch on this lightly).
- **Mocking (`unittest.mock`)**: The technique of replacing parts of your system (like an external API or a complex class) with "fake" versions. This lets you test a piece of code in isolation.

---

## � Project-Level Deep Dive: Advanced Concepts

### Test-Driven Development (TDD)
TDD flips the usual development process on its head. The cycle is "Red-Green-Refactor":
1.  **Red**: Write a failing test for a feature you haven't implemented yet. Run it and watch it fail (turn red). This proves the test works and the feature is missing.
2.  **Green**: Write the *absolute minimum* amount of code required to make the test pass (turn green). Don't worry about making it pretty.
3.  **Refactor**: Now that you have a passing test as a safety net, clean up your code. Improve the implementation, remove duplication, and make it more efficient, running the test frequently to ensure you haven't broken anything.
This process encourages simple, modular design and results in a comprehensive test suite as a natural byproduct of development.

### Pytest Fixtures
Fixtures are one of `pytest`'s most powerful features. A fixture is a function (marked with `@pytest.fixture`) that provides a resource for your tests, such as a database connection, a temporary file, or a complex object. You can then "request" a fixture just by including its name as an argument in your test function. `pytest` handles the setup and, crucially, the **teardown** of the resource (e.g., closing the database connection) after the test is done. This makes tests cleaner, more modular, and avoids duplicating setup code.

### Property-Based Testing
Instead of testing with a few hand-picked examples, **property-based testing** generates hundreds of random inputs and asserts that certain "properties" of your function always hold true. For example, for a `sort` function, you could assert two properties: 1) the output list is always sorted, and 2) the output list contains the exact same elements as the input list. Libraries like **Hypothesis** integrate with `pytest` to do this. When it finds a failing example, it automatically simplifies it to the smallest possible failing case, making debugging much easier.

---

## �💻 Exercises

Create a new Python file named `katas/day12_practice_tests.py` and complete the following exercises. You will need to install `pytest`:
`pip install pytest`

To run your tests, navigate to the project root in your terminal and simply run the command: `pytest`

### Exercise 1: Testing a Simple Function

1.  In your `day12_practice_tests.py` file, import the `practice_normalize` function you wrote for the Day 1 kata.
2.  Create a test function `test_practice_normalize_simple()`.
3.  Inside the test, use `assert` to check if the function works as expected:
    - `assert practice_normalize("  hello   world  ") == "hello world"`
4.  Create another test function `test_practice_normalize_with_newlines()` to test its handling of tabs and newlines.

### Exercise 2: Testing for Expected Errors

1.  The `normalize_text` function in the project raises a `TypeError` if the input is not a string. Let's test this.
2.  Import `pytest` and the original `normalize_text` from `src/entaera/utils/text_processor.py`.
3.  Create a test function `test_normalize_text_invalid_input()`.
4.  Use `pytest.raises` as a context manager to assert that a `TypeError` is raised when you call the function with a non-string input (like a number or a list).
    ```python
    with pytest.raises(TypeError):
        normalize_text(123)
    ```

### Exercise 3: Testing a Class

1.  Import the `ChatThread` and `User` models you created for the Day 4 kata.
2.  Create a test function `test_chat_thread_add_message()`.
3.  Inside the test:
    - Create a `ChatThread` instance.
    - Create a `User` instance.
    - Call the `add_message` method.
    - Assert that the length of the `messages` list in the thread is now 1.
    - Assert that the content of the first message is correct.

### Exercise 4: Mocking a Dependency

1.  This is the most advanced exercise. We will test the `ContextRetriever` from Day 7.
2.  The `ContextRetriever` depends on `MemoryManager` and `ChatThread`. We don't want to *actually* run the semantic search model in our unit test, so we will "mock" the memory manager.
3.  Import `ContextRetriever` and `MagicMock` from `unittest.mock`.
4.  Create a test function `test_context_retriever()`.
5.  Inside the test:
    - Create mock objects for the dependencies: `mock_memory_manager = MagicMock()` and `mock_chat_thread = MagicMock()`.
    - Configure the return values of the methods that will be called. For example:
      `mock_memory_manager.retrieve_memories.return_value = ["A fake memory"]`
      `mock_chat_thread.get_context_window.return_value = ["A fake message"]`
    - Instantiate your `ContextRetriever` with these *mock* objects.
    - Call the `retrieve` method.
    - Assert that the returned dictionary contains the fake data you defined.
    - You can also assert that the mock methods were called: `mock_memory_manager.retrieve_memories.assert_called_once()`

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What is the difference between a unit test, an integration test, and an end-to-end (E2E) test?**
    - *Answer Hint:* **Unit Test**: Tests a single function or class in isolation (using mocks). It's fast and precise. **Integration Test**: Tests how two or more units work together (e.g., does your code correctly connect to a real database?). It's slower but catches interface bugs. **E2E Test**: Tests the entire application from the user's perspective (e.g., using a tool like Selenium to click buttons in a web UI and verify the outcome). It's the slowest but gives the most confidence that the system as a whole works.
2.  **Why is it important to "mock" dependencies in unit tests? What problems can occur if you don't?**
    - *Answer Hint:* Mocking provides **isolation** and **speed**. If you don't mock, your test might fail because of a bug in a dependency, not in the unit you're testing, which makes debugging hard. Also, real dependencies like network calls or database queries are slow and unreliable, which makes your test suite fragile and painful to run.

### Intermediate
3.  **What does "test coverage" mean? Is 100% test coverage always a good goal? Why or why not?**
    - *Answer Hint:* Test coverage measures the percentage of your code's lines, branches, or statements that are executed by your test suite. While high coverage is good, aiming for 100% is often a waste of time (a "vanity metric"). You can spend hours writing tests for simple, trivial code that is unlikely to break, instead of focusing on testing the complex, critical parts of your application. It's better to have 80% coverage of important logic than 100% coverage that includes testing getters and setters.
4.  **Describe the Arrange-Act-Assert pattern for structuring tests.**
    - *Answer Hint:* It's a simple way to make tests readable and consistent. **Arrange**: Set up all the preconditions and inputs. Create your objects, mock your dependencies, etc. **Act**: Execute the single function or method that you are testing. **Assert**: Check that the outcome (the return value, the state of an object, etc.) is what you expected.
5.  **What is Test-Driven Development (TDD)? Can you describe the red-green-refactor cycle?**
    - *Answer Hint:* TDD is a development methodology where you write the tests *before* you write the implementation code. The cycle is: 1) **Red**: Write a test for a new feature and watch it fail. 2) **Green**: Write the simplest possible code to make that test pass. 3) **Refactor**: Clean up and improve the implementation code, confident that your test will catch any regressions.

### Advanced
6.  **What is a "flaky" test, and what are some common causes?**
    - *Answer Hint:* A flaky test is one that sometimes passes and sometimes fails without any code changes. They are dangerous because they erode trust in the test suite. Common causes include: 1) **Race conditions** in asynchronous code. 2) **Order dependency**: Test B fails if Test A doesn't run before it. 3) **Time-sensitive code**: A test that relies on the current time might fail at midnight. 4) **Unreliable external services**: A test that makes a real network call.
7.  **You have a function that is computationally very expensive. You want to test it with many different inputs, but the test suite takes too long to run. What strategies could you use?**
    - *Answer Hint:* Several strategies can help. 1) **Parametrization**: Use `pytest.mark.parametrize` to run the same test logic with many inputs, which is cleaner than writing separate tests. 2) **Caching**: Use a tool like `pytest-cache` to cache the results of expensive function calls so they don't need to be re-computed on subsequent runs if the code hasn't changed. 3) **Selective Testing**: Mark the slow tests with `@pytest.mark.slow` and configure your CI/CD pipeline to only run them on nightly builds, not on every single commit. 4) **Refactoring**: The best solution is often to refactor the function itself to separate the expensive computation from the business logic, allowing you to test the logic without incurring the computational cost.
