"""
ENTAERA Kata - Day 0: Python Fundamentals Practice
Complete all exercises to master Python basics.
"""

# =============================================================================
# Exercise 1: List Comprehension Mastery
# =============================================================================

print("=" * 60)
print("Exercise 1: List Comprehension Mastery")
print("=" * 60)

# TODO: Create a list of squares for numbers 1-20
squares = 

print(f"Squares 1-20: {squares}")

# TODO: Create a list of even numbers from 1-50
evens = 

print(f"Even numbers 1-50: {evens}")

# TODO: Extract all vowels from this string using a list comprehension
text = "Python is awesome for AI development"
vowels = 

print(f"Vowels in text: {vowels}")

# TODO: Create a list of tuples: (number, square, cube) for 1-10
number_powers = 

print(f"Number powers: {number_powers[:3]}...")  # First 3

# TODO: Flatten this nested list
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = 

print(f"Flattened: {flattened}")


# =============================================================================
# Exercise 2: Dictionary Comprehension Mastery
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 2: Dictionary Comprehension Mastery")
print("=" * 60)

# TODO: Create a dict mapping numbers 1-10 to their squares
num_to_square = 

print(f"Number to square: {num_to_square}")

# TODO: Invert this dictionary (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = 

print(f"Inverted dict: {inverted}")

# TODO: Filter this dict to only include items where value > 50
data = {"item1": 45, "item2": 78, "item3": 23, "item4": 91}
filtered = 

print(f"Filtered (>50): {filtered}")

# TODO: Create a dict from two lists
keys = ["name", "age", "city"]
values = ["Alice", 25, "NYC"]
combined = 

print(f"Combined dict: {combined}")

# TODO: Count character frequency in a string
text = "hello world"
char_count = 

print(f"Character count: {char_count}")


# =============================================================================
# Exercise 3: Advanced Comprehensions
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 3: Advanced Comprehensions")
print("=" * 60)

# TODO: Create a 5x5 multiplication table using nested list comprehension
mult_table = 

print(f"5x5 multiplication table:")
for row in mult_table:
    print(row)

# TODO: Extract all words longer than 4 characters from this sentence
sentence = "The quick brown fox jumps over the lazy dog"
long_words = 

print(f"Long words (>4 chars): {long_words}")

# TODO: Create a list of (index, value) tuples for even numbers only
numbers = [10, 15, 20, 25, 30, 35, 40]
indexed_evens = 

print(f"Indexed evens: {indexed_evens}")

# TODO: Use a set comprehension to find unique word lengths
words = ["apple", "banana", "cherry", "date", "fig", "grape"]
unique_lengths = 

print(f"Unique word lengths: {unique_lengths}")


# =============================================================================
# Exercise 4: Built-in Functions
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 4: Built-in Functions")
print("=" * 60)

# TODO: Use map() to convert these strings to integers
str_numbers = ["1", "2", "3", "4", "5"]
int_numbers = 

print(f"String to int: {int_numbers}")

# TODO: Use filter() to keep only positive numbers
mixed_numbers = [-5, 3, -1, 7, -8, 2, 0, 4]
positive = 

print(f"Positive numbers: {positive}")

# TODO: Use zip() to combine these three lists into tuples
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]
people = 

print(f"People data: {people}")

# TODO: Use enumerate() to create a dict mapping index to value
fruits = ["apple", "banana", "cherry"]
indexed_fruits = 

print(f"Indexed fruits: {indexed_fruits}")

# TODO: Use reduce() to find the maximum value
from functools import reduce
numbers = [45, 23, 67, 12, 89, 34]
maximum = 

print(f"Maximum value: {maximum}")

# TODO: Use any() to check if there are any negative numbers
values = [5, 10, -3, 20]
has_negative = 

print(f"Has negative: {has_negative}")

# TODO: Use all() to check if all strings are uppercase
words = ["HELLO", "WORLD", "PYTHON"]
all_upper = 

print(f"All uppercase: {all_upper}")


# =============================================================================
# Exercise 5: Real-World String Parsing
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 5: Real-World String Parsing")
print("=" * 60)

# TODO: Parse this log line to extract timestamp, level, and message
log_line = "2024-01-15 10:30:45 ERROR Database connection failed"
# Expected: {"timestamp": "2024-01-15 10:30:45", "level": "ERROR", "message": "Database connection failed"}
parsed_log = 

print(f"Parsed log: {parsed_log}")

# TODO: Extract all email addresses from this text
text = "Contact us at support@example.com or sales@company.org for more info"
emails = 

print(f"Emails found: {emails}")

# TODO: Parse this CSV line into a list of values
csv_line = "John,Doe,30,New York,Engineer"
values = 

print(f"CSV values: {values}")

# TODO: Convert snake_case to camelCase
snake_case = "this_is_a_variable_name"
camel_case = 

print(f"Snake to camel: {snake_case} -> {camel_case}")

# TODO: Extract all hashtags from this social media post
post = "Just learned #Python and #MachineLearning! #AI is amazing #100DaysOfCode"
hashtags = 

print(f"Hashtags: {hashtags}")


# =============================================================================
# Exercise 6: Data Transformation Challenge
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 6: Data Transformation Challenge")
print("=" * 60)

# TODO: Convert list of tuples to list of dicts
users_data = [
    ("Alice", 25, "alice@email.com"),
    ("Bob", 30, "bob@email.com"),
    ("Charlie", 35, "charlie@email.com")
]
users_dict = 

print(f"Users as dicts: {users_dict}")

# TODO: Group these transactions by user_id
transactions = [
    {"user_id": 1, "amount": 100},
    {"user_id": 2, "amount": 50},
    {"user_id": 1, "amount": 75},
    {"user_id": 3, "amount": 200},
    {"user_id": 2, "amount": 125}
]
grouped = 

print(f"Grouped transactions: {grouped}")

# TODO: Find all duplicate values in this list
numbers = [1, 2, 3, 2, 4, 5, 1, 6, 3]
duplicates = 

print(f"Duplicates: {duplicates}")

# TODO: Merge these two dictionaries, summing values for duplicate keys
dict1 = {"a": 10, "b": 20, "c": 30}
dict2 = {"b": 15, "c": 25, "d": 40}
merged = 

print(f"Merged dicts: {merged}")

print("\n" + "=" * 60)
print("All exercises complete! Review your solutions.")
print("=" * 60)
