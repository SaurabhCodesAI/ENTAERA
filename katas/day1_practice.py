
# This is your practice file for the Day 1 Kata.
# Complete the exercises from katas/day1_text_processing.md here.

import re
import unicodedata

# --- Exercise 1: Simple Normalization ---
def practice_normalize(text: str) -> str:
    """
    Replicates the logic from normalize_text().
    """
    # TODO: Implement the normalization logic
    pass

print("--- Exercise 1 ---")
# TODO: Test your function with the provided inputs


# --- Exercise 2: Emoji Handling ---
def practice_has_emoji(text: str) -> bool:
    """
    Checks if the text contains any emoji characters.
    """
    # TODO: Implement the emoji detection logic
    pass

def practice_remove_emoji(text: str) -> str:
    """
    Removes all emoji characters from the text.
    """
    # TODO: Implement the emoji removal logic
    pass

def practice_extract_emoji(text: str) -> list[str]:
    """
    Extracts all emoji characters from the text.
    """
    # TODO: Implement the emoji extraction logic
    pass

print("\n--- Exercise 2 ---")
# TODO: Test your emoji functions


# --- Exercise 3: Advanced Normalization ---
def practice_advanced_normalize(text: str, remove_punc: bool = False) -> str:
    """
    Performs advanced normalization, with an option to remove punctuation.
    """
    # TODO: Implement the advanced normalization logic
    pass

print("\n--- Exercise 3 ---")
# TODO: Test your advanced normalization function


# --- Exercise 4: Putting It All Together ---
def process_text(text: str) -> dict:
    """
    Processes a string and returns a dictionary of text analysis.
    """
    # TODO: Implement the final processing function
    pass

print("\n--- Exercise 4 ---")
# TODO: Run this function with a few test strings and print the results

