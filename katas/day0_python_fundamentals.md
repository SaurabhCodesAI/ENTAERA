# ENTAERA Kata - Day 0: Python Fundamentals Mastery

## 🎯 Learning Objectives

Before diving into AI systems, you need rock-solid Python fundamentals. This kata covers the essential building blocks that every Python developer must master. By the end, you'll confidently use Python's most powerful features.

- **Master list comprehensions, dict comprehensions, and generator expressions**
- **Understand and use Python's data structures (lists, dicts, sets, tuples)**
- **Work with functions, lambda expressions, and higher-order functions**
- **Use built-in functions like `map()`, `filter()`, `zip()`, `enumerate()`**
- **Handle exceptions and write defensive code**
- **Understand variable scope, unpacking, and slicing**

---

## 🧠 For the Absolute Beginner

### What is a List Comprehension?
Instead of writing a loop to build a list, you can write it in one concise line. For example:
```python
# Old way (verbose)
numbers = []
for i in range(10):
    numbers.append(i * 2)

# List comprehension (Pythonic)
numbers = [i * 2 for i in range(10)]
```

Both create `[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]`, but the comprehension is cleaner and faster.

### What is a Lambda Function?
A **lambda** is a tiny, anonymous function. Instead of defining a full function with `def`, you create it inline:
```python
# Regular function
def add(x, y):
    return x + y

# Lambda (one-liner)
add = lambda x, y: x + y
```

Lambdas are perfect for simple operations passed to functions like `map()` or `sorted()`.

---

## 📚 Core Concepts

### 1. List Comprehensions
```python
# Basic: Create a list of squares
squares = [x**2 for x in range(10)]

# With condition: Only even squares
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested: Flatten a 2D list
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]  # [1, 2, 3, 4, 5, 6]
```

### 2. Dictionary Comprehensions
```python
# Create a dict of word lengths
words = ["hello", "world", "python"]
lengths = {word: len(word) for word in words}
# {'hello': 5, 'world': 5, 'python': 6}

# Filter dict items
scores = {"alice": 85, "bob": 92, "charlie": 78}
high_scores = {k: v for k, v in scores.items() if v >= 80}
```

### 3. Set Comprehensions
```python
# Remove duplicates and square
numbers = [1, 2, 2, 3, 4, 4, 5]
unique_squares = {x**2 for x in numbers}  # {1, 4, 9, 16, 25}
```

### 4. Generator Expressions
```python
# Like list comprehensions but memory-efficient (lazy evaluation)
squares = (x**2 for x in range(1000000))  # Doesn't create list in memory
first_five = list(next(squares) for _ in range(5))
```

### 5. Built-in Functions
```python
# map: Apply function to all items
numbers = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, numbers))  # [2, 4, 6, 8]

# filter: Keep items matching condition
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# zip: Combine multiple iterables
names = ["Alice", "Bob"]
ages = [25, 30]
combined = list(zip(names, ages))  # [('Alice', 25), ('Bob', 30)]

# enumerate: Get index and value
for i, name in enumerate(names):
    print(f"{i}: {name}")  # 0: Alice, 1: Bob
```

### 6. Unpacking
```python
# Unpack tuples
x, y = (10, 20)

# Unpack with * (rest)
first, *rest, last = [1, 2, 3, 4, 5]  # first=1, rest=[2,3,4], last=5

# Unpack in function arguments
def greet(name, age):
    print(f"{name} is {age}")

data = {"name": "Alice", "age": 25}
greet(**data)  # Unpack dict as keyword arguments
```

### 7. Slicing
```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slicing: [start:stop:step]
numbers[2:7]      # [2, 3, 4, 5, 6]
numbers[:5]       # [0, 1, 2, 3, 4]
numbers[5:]       # [5, 6, 7, 8, 9]
numbers[::2]      # [0, 2, 4, 6, 8] (every 2nd element)
numbers[::-1]     # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reverse)
```

---

## 🚀 Advanced Concepts

### Nested Comprehensions
```python
# Create a multiplication table
table = [[i * j for j in range(1, 11)] for i in range(1, 11)]
```

### Conditional Expressions in Comprehensions
```python
# Use if-else inside comprehension
labels = ["even" if x % 2 == 0 else "odd" for x in range(10)]
```

### `any()` and `all()`
```python
numbers = [2, 4, 6, 8]
all(x % 2 == 0 for x in numbers)  # True (all are even)
any(x > 5 for x in numbers)       # True (at least one > 5)
```

### `reduce()` for Cumulative Operations
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)  # 120 (1*2*3*4*5)
```

---

## 💻 Exercises

Create a file `katas/day0_practice.py` and complete these exercises.

### Exercise 1: List Comprehension Mastery

```python
# TODO: Create a list of squares for numbers 1-20
squares = 

# TODO: Create a list of even numbers from 1-50
evens = 

# TODO: Extract all vowels from this string using a list comprehension
text = "Python is awesome for AI development"
vowels = 

# TODO: Create a list of tuples: (number, square, cube) for 1-10
number_powers = 

# TODO: Flatten this nested list
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = 
```

### Exercise 2: Dictionary Comprehension Mastery

```python
# TODO: Create a dict mapping numbers 1-10 to their squares
num_to_square = 

# TODO: Invert this dictionary (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = 

# TODO: Filter this dict to only include items where value > 50
data = {"item1": 45, "item2": 78, "item3": 23, "item4": 91}
filtered = 

# TODO: Create a dict from two lists
keys = ["name", "age", "city"]
values = ["Alice", 25, "NYC"]
combined = 

# TODO: Count character frequency in a string
text = "hello world"
char_count = 
```

### Exercise 3: Advanced Comprehensions

```python
# TODO: Create a 5x5 multiplication table using nested list comprehension
mult_table = 

# TODO: Extract all words longer than 4 characters from this sentence
sentence = "The quick brown fox jumps over the lazy dog"
long_words = 

# TODO: Create a list of (index, value) tuples for even numbers only
numbers = [10, 15, 20, 25, 30, 35, 40]
indexed_evens = 

# TODO: Use a set comprehension to find unique word lengths
words = ["apple", "banana", "cherry", "date", "fig", "grape"]
unique_lengths = 
```

### Exercise 4: Built-in Functions

```python
# TODO: Use map() to convert these strings to integers
str_numbers = ["1", "2", "3", "4", "5"]
int_numbers = 

# TODO: Use filter() to keep only positive numbers
mixed_numbers = [-5, 3, -1, 7, -8, 2, 0, 4]
positive = 

# TODO: Use zip() to combine these three lists into tuples
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]
people = 

# TODO: Use enumerate() to create a dict mapping index to value
fruits = ["apple", "banana", "cherry"]
indexed_fruits = 

# TODO: Use reduce() to find the maximum value
from functools import reduce
numbers = [45, 23, 67, 12, 89, 34]
maximum = 

# TODO: Use any() to check if there are any negative numbers
values = [5, 10, -3, 20]
has_negative = 

# TODO: Use all() to check if all strings are uppercase
words = ["HELLO", "WORLD", "PYTHON"]
all_upper = 
```

### Exercise 5: Real-World String Parsing

```python
# TODO: Parse this log line to extract timestamp, level, and message
log_line = "2024-01-15 10:30:45 ERROR Database connection failed"
# Expected: {"timestamp": "2024-01-15 10:30:45", "level": "ERROR", "message": "Database connection failed"}
parsed_log = 

# TODO: Extract all email addresses from this text
text = "Contact us at support@example.com or sales@company.org for more info"
emails = 

# TODO: Parse this CSV line into a list of values
csv_line = "John,Doe,30,New York,Engineer"
values = 

# TODO: Convert snake_case to camelCase
snake_case = "this_is_a_variable_name"
camel_case = 

# TODO: Extract all hashtags from this social media post
post = "Just learned #Python and #MachineLearning! #AI is amazing #100DaysOfCode"
hashtags = 
```

### Exercise 6: Data Transformation Challenge

```python
# TODO: You have a list of user data as tuples. Convert to list of dicts
users_data = [
    ("Alice", 25, "alice@email.com"),
    ("Bob", 30, "bob@email.com"),
    ("Charlie", 35, "charlie@email.com")
]
# Expected: [{"name": "Alice", "age": 25, "email": "alice@email.com"}, ...]
users_dict = 

# TODO: Group these transactions by user_id
transactions = [
    {"user_id": 1, "amount": 100},
    {"user_id": 2, "amount": 50},
    {"user_id": 1, "amount": 75},
    {"user_id": 3, "amount": 200},
    {"user_id": 2, "amount": 125}
]
# Expected: {1: [100, 75], 2: [50, 125], 3: [200]}
grouped = 

# TODO: Find all duplicate values in this list
numbers = [1, 2, 3, 2, 4, 5, 1, 6, 3]
duplicates = 

# TODO: Merge these two dictionaries, summing values for duplicate keys
dict1 = {"a": 10, "b": 20, "c": 30}
dict2 = {"b": 15, "c": 25, "d": 40}
# Expected: {"a": 10, "b": 35, "c": 55, "d": 40}
merged = 
```

---

## 🤔 Mastery Questions

### Beginner
1. **What's the difference between a list and a tuple?**
   - Lists are mutable (can be changed), tuples are immutable (cannot be changed after creation)
   
2. **When should you use a set vs a list?**
   - Use set for unique items and fast membership testing. Use list for ordered, potentially duplicate items

3. **What does `[::-1]` do?**
   - Reverses a sequence (string, list, tuple)

### Intermediate
4. **What's the difference between `map()` and a list comprehension?**
   - Both apply a function to items, but comprehensions are more Pythonic and readable. `map()` returns an iterator (lazy), comprehensions create the list immediately

5. **When should you use a generator expression instead of a list comprehension?**
   - When working with large datasets and you don't need all values at once (memory efficient)

6. **Explain the difference between `is` and `==`**
   - `is` checks if two variables point to the same object in memory. `==` checks if values are equal

### Advanced
7. **What is "list comprehension abuse" and why should it be avoided?**
   - Overly complex comprehensions with nested loops and multiple conditions become unreadable. Use regular loops for complex logic

8. **How does Python's GIL (Global Interpreter Lock) affect multithreading?**
   - GIL prevents true parallel execution of Python threads. For CPU-bound tasks, use multiprocessing instead

9. **What's the time complexity of common operations?**
   - List append: O(1), List insert at beginning: O(n), Dict lookup: O(1), Set membership: O(1), List search: O(n)

---

## 🎯 Next Steps

Once you've mastered these Python fundamentals, you're ready for:
- **Day 1: Text Processing** - Use regex and string methods with confidence
- **Day 4: Data Modeling** - Build complex data structures with Pydantic
- **Day 13: SQL Mastery** - Translate your Python skills to database queries

**Time to Complete:** 4-6 hours

Master these basics, and everything else becomes easier! 🚀
