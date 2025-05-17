
# This is your practice file for the Day 12 Kata.
# Complete the exercises from katas/day12_unit_testing.md here.
# To run these tests, open a terminal in the project root and run `pytest`.

import pytest
from unittest.mock import MagicMock

# Assume your previous kata solutions are in the katas directory
# and that the directory has an __init__.py file to be importable.
from katas.day1_practice import practice_normalize
from src.entaera.utils.text_processor import normalize_text
from katas.day4_practice import ChatThread, User
from katas.day7_practice import ContextRetriever

# --- Exercise 1: Testing a Simple Function ---

def test_practice_normalize_simple():
    # TODO: Add assertions for simple normalization
    pass

def test_practice_normalize_with_newlines():
    # TODO: Add assertions for text with newlines and tabs
    pass


# --- Exercise 2: Testing for Expected Errors ---

def test_normalize_text_invalid_input():
    # TODO: Use pytest.raises to check for a TypeError
    pass


# --- Exercise 3: Testing a Class ---

def test_chat_thread_add_message():
    # TODO: Test the add_message method of your ChatThread class
    pass


# --- Exercise 4: Mocking a Dependency ---

def test_context_retriever_with_mocks():
    """
    Tests the ContextRetriever in isolation by mocking its dependencies.
    """
    # TODO:
    # 1. Create MagicMock objects for MemoryManager and ChatThread.
    # 2. Configure their return_values for the methods that will be called.
    # 3. Instantiate ContextRetriever with the mocks.
    # 4. Call the retrieve method.
    # 5. Assert that the output is what you expect based on the mock return values.
    # 6. Assert that the mock methods were called.
    pass

