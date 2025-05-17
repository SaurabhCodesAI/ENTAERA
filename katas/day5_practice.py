
# This is your practice file for the Day 5 Kata.
# Complete the exercises from katas/day5_semantic_search.md here.
# You will need to install libraries: pip install sentence-transformers numpy

import numpy as np
from sentence_transformers import SentenceTransformer

# --- Exercise 1: Generate Your First Embeddings ---

print("--- Exercise 1 ---")
# TODO: Load the model
# TODO: Define sentences
# TODO: Generate embeddings and print their shape


# --- Exercise 2: Calculate Cosine Similarity ---

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculates the cosine similarity between two vectors.
    """
    # TODO: Implement the cosine similarity formula
    pass

print("\n--- Exercise 2 ---")
# TODO: Use your embeddings from Ex1 to test the similarity function


# --- Exercise 3: Build a Vector Index ---

class VectorIndex:
    def __init__(self):
        # TODO: Initialize lists for documents and embeddings
        pass

    def add_document(self, document: str, embedding: np.ndarray):
        # TODO: Add a document and its embedding to the index
        pass

    def search(self, query_embedding: np.ndarray, top_k: int = 1) -> list[tuple[str, float]]:
        """
        Finds the top_k most similar documents to the query embedding.
        """
        # TODO: Implement the search logic
        pass

print("\n--- Exercise 3 ---")
# This exercise is primarily about building the class.
# We will test it in Exercise 4.
print("VectorIndex class defined.")


# --- Exercise 4: Create a Semantic Search Engine ---

class SearchEngine:
    def __init__(self):
        # TODO: Initialize the model and your VectorIndex
        pass

    def index_documents(self, documents: list[str]):
        # TODO: Generate embeddings and add documents to the index
        pass

    def query(self, query_text: str, top_k: int = 1) -> list[tuple[str, float]]:
        """
        Performs a semantic search query.
        """
        # TODO: Implement the query logic
        pass

print("\n--- Exercise 4 ---")
# TODO: Instantiate the SearchEngine, index documents, and perform a query.
# Print the results.

