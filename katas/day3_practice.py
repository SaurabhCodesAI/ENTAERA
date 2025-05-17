
# This is your practice file for the Day 3 Kata.
# Complete the exercises from katas/day3_file_io.md here.

import os
import json
import yaml  # You may need to install this: pip install pyyaml
import tempfile
from pathlib import Path

# --- Exercise 1: Atomic JSON Write ---

def atomic_write_json(file_path: str, data: dict):
    """
    Writes a dictionary to a JSON file atomically.
    """
    # TODO: Implement the atomic write logic
    pass

print("--- Exercise 1 ---")
# TODO: Test your atomic write function


# --- Exercise 2: File Handler Context Manager ---

class SafeFileHandler:
    def __init__(self, file_path, mode):
        # TODO: Initialize the handler
        pass

    def __enter__(self):
        # TODO: Open the file and return the handle
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Close the file and handle potential errors
        pass

print("\n--- Exercise 2 ---")
# TODO: Use your context manager to write to a file


# --- Exercise 3: Reading and Writing Different Formats ---

def write_data(file_path: str, data):
    """
    Writes data to a file, detecting the format from the extension.
    """
    # TODO: Implement logic to handle .json, .yaml, and .txt
    pass

def read_data(file_path: str):
    """
    Reads data from a file, detecting the format from the extension.
    """
    # TODO: Implement logic to handle .json, .yaml, and .txt
    pass

print("\n--- Exercise 3 ---")
# TODO: Test writing and reading with JSON and YAML files


# --- Exercise 4: Directory Scanner ---

def scan_directory(path: str, extension: str) -> list:
    """
    Scans a directory recursively and finds files with a given extension.
    """
    # TODO: Implement the directory scanning logic
    pass

print("\n--- Exercise 4 ---")
# TODO: Create a dummy directory structure and test your scanner

