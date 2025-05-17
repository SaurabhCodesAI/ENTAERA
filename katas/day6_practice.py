
# This is your practice file for the Day 6 Kata.
# Complete the exercises from katas/day6_long_term_memory.md here.
# You will need libraries from Day 5: pip install pydantic sentence-transformers numpy

import numpy as np
from pydantic import BaseModel
from datetime import datetime
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# --- Exercise 1: The Memory Model ---

class Memory(BaseModel):
    # TODO: Define the fields for the Memory model
    pass

print("--- Exercise 1 ---")
# TODO: Instantiate a Memory object and print it


# --- Exercise 2: The MemoryIndex ---

# You can copy/paste your VectorIndex from Day 5 and adapt it.
class MemoryIndex:
    def __init__(self):
        # TODO: Initialize lists for Memory objects and embeddings
        pass

    def add_memory(self, memory: Memory, embedding: np.ndarray):
        # TODO: Add a memory and its embedding to the index
        pass

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[Memory, float]]:
        """
        Finds the top_k most similar memories.
        Returns a list of tuples containing the Memory object and its similarity score.
        """
        # TODO: Implement the search logic
        # Hint: You'll need a cosine_similarity function from Day 5.
        pass

print("\n--- Exercise 2 ---")
print("MemoryIndex class defined.")


# --- Exercise 3: The MemoryManager ---

class MemoryManager:
    def __init__(self):
        # TODO: Initialize the SentenceTransformer model and MemoryIndex
        pass

    def add_memory(self, content: str, importance: float):
        # TODO: Implement the logic to create, embed, and add a memory
        pass

    def retrieve_memories(self, query_text: str, top_k: int = 3) -> List[Memory]:
        """
        Retrieves the most relevant memories for a given query text.
        """
        # TODO: Implement the retrieval logic
        pass

print("\n--- Exercise 3 ---")
print("MemoryManager class defined.")


# --- Exercise 4: A Day in the Life of an Agent ---

print("\n--- Exercise 4 ---")
# TODO: Instantiate MemoryManager
# TODO: Add the 5 sample memories
# TODO: Perform the two test queries and print the results

