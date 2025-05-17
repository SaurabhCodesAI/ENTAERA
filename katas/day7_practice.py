
# This is your practice file for the Day 7 Kata.
# Complete the exercises from katas/day7_context_management.md here.

# You will need to import/copy your classes from previous katas:
# - ChatThread (Day 4)
# - MemoryManager (Day 6)
# Make sure you have the necessary libraries installed.

from katas.day4_practice import ChatThread, User, Message # Assuming you completed it there
from katas.day6_practice import MemoryManager, Memory # Assuming you completed it there
from typing import Dict, List

# --- Exercise 1: The ContextRetriever ---

class ContextRetriever:
    def __init__(self, memory_manager: MemoryManager, chat_thread: ChatThread):
        # TODO: Store the manager and thread
        pass

    def retrieve(self, query_text: str, max_memories: int = 3, max_history: int = 5) -> Dict[str, List]:
        """
        Retrieves context from both long-term memory and short-term chat history.
        """
        # TODO: Implement the retrieval logic
        pass

print("--- Exercise 1 ---")
print("ContextRetriever class defined.")


# --- Exercise 2: The ContextInjector ---

class ContextInjector:
    def inject(self, query_text: str, context: Dict[str, List], max_tokens: int = 1000) -> str:
        """
        Constructs a final prompt string from a query and context, respecting a token limit.
        """
        # TODO: Implement the injection and token budgeting logic
        # A simple way to count tokens is to count words.
        pass

print("\n--- Exercise 2 ---")
print("ContextInjector class defined.")


# --- Exercise 3: The PromptPipeline ---

class PromptPipeline:
    def __init__(self, memory_manager: MemoryManager, chat_thread: ChatThread):
        # TODO: Instantiate the retriever and injector
        pass

    def create_prompt(self, query_text: str) -> str:
        """
        Runs the full pipeline to create a context-aware prompt.
        """
        # TODO: Implement the pipeline logic
        pass

print("\n--- Exercise 3 ---")
print("PromptPipeline class defined.")


# --- Exercise 4: Full System Simulation ---

print("\n--- Exercise 4 ---")
# TODO:
# 1. Instantiate MemoryManager and ChatThread.
# 2. Populate them with sample data.
# 3. Instantiate PromptPipeline.
# 4. Call create_prompt with a relevant query.
# 5. Print the final prompt.

