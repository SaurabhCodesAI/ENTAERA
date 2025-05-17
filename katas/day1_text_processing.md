
# ENTAERA Kata - Day 1: Foundational Text Processing

## 🎯 Learning Objectives

Welcome to your first kata! Today, you will master the foundational skill of text processing. This is a critical building block for any AI system that deals with natural language. By the end of this session, you will be able to confidently handle and normalize text data in Python.

- **Understand and implement text normalization.**
- **Use regular expressions for text cleaning.**
- **Handle Unicode and special characters like emojis.**
- **Write clean, documented, and type-hinted Python functions.**

---

## 🧠 For the Absolute Beginner

### What is Text Processing?
At its core, text processing is about manipulating strings. A **string** is just a sequence of characters, like `"hello"`. In AI, the text we get from users is often messy—it has extra spaces, inconsistent capitalization, and special characters. Our goal is to "clean" it so a machine can understand it better.

### What is a Function?
A **function** is a reusable block of code that performs a specific task. We give it a name (e.g., `normalize_text`), it takes some input (e.g., a messy string), and it returns some output (e.g., a clean string).

---

## 📚 Theory & Links

Before you begin, study the implementation in `src/entaera/utils/text_processor.py`. Pay close attention to:

- `normalize_text()`: The core function for cleaning text.
- `contains_emoji()`, `remove_emojis()`, `extract_emojis()`: How emojis are detected and handled using Unicode character ranges.
- The use of `re` (regular expressions) for pattern matching.
- The use of `unicodedata` for handling different Unicode forms.
- Type hints (`str`, `list`, `bool`) and docstrings.

---

## 🚀 Project-Level Deep Dive: Advanced Concepts

### Unicode: Beyond the Basics
The kata uses `unicodedata.normalize('NFC', ...)`. This is just one form of normalization. For global applications, you might encounter:
- **Grapheme Clusters**: Some "characters" are actually multiple Unicode points combined. For example, a family emoji 👨‍👩‍👧‍👦 is made of multiple individual emojis joined by a Zero-Width Joiner. Simple regex can sometimes break these.
- **Bidirectional Text**: Handling text that mixes left-to-right (like English) and right-to-left (like Arabic or Hebrew) languages is a significant challenge.

### Performance at Scale
The `re` module is fast, but for processing terabytes of text data, even small inefficiencies add up.
- **Pre-compiling Regex**: As seen in `text_processor.py`, `re.compile()` is used to create a regex object. If you use the same pattern many times, compiling it once is much faster.
- **Alternative Regex Engines**: For extreme performance needs, some projects use libraries like Google's `re2` or Rust's `regex` library via Python bindings, which can offer better performance and protection against certain types of vulnerabilities (like ReDoS).

---

## 💻 Exercises

Create a new Python file named `katas/day1_practice.py` and complete the following exercises.

### Exercise 1: Simple Normalization

1.  Create a function `practice_normalize(text: str) -> str`.
2.  Inside this function, replicate the logic from `normalize_text()`:
    - Convert the text to lowercase.
    - Use `re.sub()` to replace multiple whitespace characters (`\s+`) with a single space.
    - Remove leading and trailing whitespace.
3.  Test your function with the following inputs and print the results:
    - `"   Hello   World!   "`
    - `"This is a   TEST sentence."`
    - `"\tThis string has tabs\nand newlines."`

### Exercise 2: Emoji Handling

1.  Create three functions:
    - `practice_has_emoji(text: str) -> bool`
    - `practice_remove_emoji(text: str) -> str`
    - `practice_extract_emoji(text: str) -> list[str]`
2.  Refer to `src/entaera/utils/text_processor.py` to find the regex pattern for emojis.
3.  Implement the logic for your three functions using this pattern.
4.  Test your functions with:
    - `"I love Python 🐍"`
    - `"This is a test 👨‍💻 with a complex emoji."`
    - `"No emojis here."`

### Exercise 3: Advanced Normalization

1.  Create a function `practice_advanced_normalize(text: str, remove_punc: bool = False) -> str`.
2.  This function should first perform the simple normalization from Exercise 1.
3.  If `remove_punc` is `True`, use `re.sub()` to remove all characters that are **not** alphanumeric (`\w`) or whitespace (`\s`).
4.  Test your function:
    - `practice_advanced_normalize("Hello, world! This is a test.")`
    - `practice_advanced_normalize("Hello, world! This is a test.", remove_punc=True)`

### Exercise 4: Putting It All Together

1.  Create a final function `process_text(text: str) -> dict`.
2.  This function should use the functions you created above to return a dictionary with the following information about the input text:
    - `original`: The original input string.
    - `normalized`: The result of your `practice_normalize` function.
    - `has_emojis`: The result of your `practice_has_emoji` function.
    - `emojis_extracted`: The result of your `practice_extract_emoji` function.
    - `no_emojis`: The text after removing emojis.
3.  Run this function with a few test strings of your choice and print the resulting dictionary.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **Why is text normalization important in an AI or NLP pipeline?**
    - *Answer Hint:* It reduces the vocabulary size (e.g., "The" and "the" become the same), ensures consistent matching, and removes noise, making it easier for the model to find patterns.
2.  **Explain the regex pattern `\s+`. What does `\s` mean? What does `+` mean?**
    - *Answer Hint:* `\s` matches any whitespace character (space, tab, newline). `+` is a quantifier meaning "one or more" of the preceding character. So, `\s+` means "one or more whitespace characters."

### Intermediate
3.  **How would you find all the hashtags (e.g., `#python`) in a string? What regex would you use?**
    - *Answer Hint:* A good regex would be `r"#\w+"`. `\w+` matches one or more "word" characters (letters, numbers, underscore).
4.  **What is the difference between `re.search()`, `re.match()`, and `re.findall()`?**
    - *Answer Hint:* `re.match()` only checks for a match at the *beginning* of the string. `re.search()` checks for a match *anywhere* in the string. `re.findall()` finds *all* non-overlapping matches and returns them as a list of strings.
5.  **What is Unicode normalization (e.g., 'NFC') and why is it useful?**
    - *Answer Hint:* Some characters can be represented in multiple ways in Unicode (e.g., 'é' can be a single character or an 'e' combined with an accent). Normalization ensures that all characters have a single, canonical representation, which is crucial for accurate text comparison and processing.

### Advanced
6.  **What is "lemmatization" and "stemming"? How do they differ from the normalization we did today?**
    - *Answer Hint:* Stemming (e.g., "running" -> "run") is a crude process of chopping off word endings. Lemmatization (e.g., "is", "are" -> "be") is a more advanced process that uses vocabulary and morphological analysis to return the base or dictionary form of a word (a "lemma"). They are forms of linguistic normalization, whereas our kata focused on syntactic normalization.
7.  **What is a "ReDoS" (Regular Expression Denial of Service) attack, and how can you write safer regular expressions to prevent it?**
    - *Answer Hint:* It's an attack that exploits inefficient regex patterns that can take a very long time to process on a specially crafted string. It can be prevented by avoiding nested quantifiers with ambiguity, using possessive quantifiers, and using more specific character classes instead of `.` where possible.

Once you have completed the exercises, you will be ready for the Day 2 kata. Good luck!
