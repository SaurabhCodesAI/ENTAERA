
# This is your practice file for the Day 8 Kata.
# Complete the exercises from katas/day8_api_routing.md here.

from abc import ABC, abstractmethod
from enum import Enum

# --- Exercise 1: The Provider Interface ---

class TranslationProvider(ABC):
    @abstractmethod
    def translate(self, text: str, target_language: str) -> str:
        pass

print("--- Exercise 1 ---")
print("TranslationProvider interface defined.")


# --- Exercise 2: Concrete Provider Implementations ---

class GoogleTranslateProvider(TranslationProvider):
    def translate(self, text: str, target_language: str) -> str:
        # TODO: Simulate Google translation
        pass

class DeepLTranslateProvider(TranslationProvider):
    def translate(self, text: str, target_language: str) -> str:
        # TODO: Simulate DeepL translation
        pass

print("\n--- Exercise 2 ---")
# TODO: Instantiate and test both providers


# --- Exercise 3: The Smart Router ---

class TaskDifficulty(Enum):
    EASY = "easy"
    HARD = "hard"

class TranslationRouter:
    def __init__(self):
        # TODO: Instantiate and store the providers
        pass

    def route(self, text: str, difficulty: TaskDifficulty) -> TranslationProvider:
        """
        Selects the best provider based on routing rules.
        """
        # TODO: Implement the routing logic
        pass

print("\n--- Exercise 3 ---")
print("TranslationRouter class defined.")


# --- Exercise 4: Putting It All Together ---

def perform_translation(text: str, target_language: str):
    """
    Selects a provider and performs the translation.
    """
    # TODO: Implement the full translation workflow
    pass

print("\n--- Exercise 4 ---")
# TODO: Test perform_translation with a short and a long string

