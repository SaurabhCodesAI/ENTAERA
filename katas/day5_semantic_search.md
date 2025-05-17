
# ENTAERA Kata - Day 5: Semantic Search & Embeddings

## 🎯 Learning Objectives

Today, you will dive into one of the most powerful concepts in modern AI: semantic search. You will learn how to convert text into numerical representations (embeddings) and use them to find text with similar meanings, not just similar keywords.

- **Understand what text embeddings are and why they are useful.**
- **Use a pre-trained model (from `sentence-transformers`) to generate embeddings.**
- **Implement a basic vector index for storing and searching embeddings.**
- **Calculate cosine similarity to find the most relevant documents.**
- **Build a simple semantic search engine from scratch.**

---

## 🧠 For the Absolute Beginner

### What is an Embedding?
Imagine a giant map where every word or sentence has its own specific location (a coordinate). On this map, words with similar meanings are placed close together. "King" would be near "Queen," and "car" would be near "automobile." An **embedding** is that coordinate—a list of numbers (a vector) that represents a piece of text's location on the map of meaning. This allows a computer, which only understands numbers, to grasp the relationships between words.

### What is Cosine Similarity?
Now that our text is represented by vectors (arrows pointing from the map's center to a coordinate), we need a way to measure how "close" they are. Instead of measuring the straight-line distance, we often measure the angle between the arrows. **Cosine similarity** does just that. If two arrows point in the exact same direction, their similarity is 1 (a perfect match). If they are perpendicular (unrelated), it's 0. This is more effective than distance for high-dimensional vectors.

---

## 📚 Theory & Links

Before you begin, study the implementation in:
- `src/entaera/core/semantic_search.py`

Key concepts to focus on:
- **Embeddings**: A dense vector representation of text where semantically similar texts are close in the vector space.
- **`sentence-transformers`**: A Python library that provides easy access to pre-trained models for generating high-quality sentence and text embeddings.
- **Vector Index**: A data structure that stores text and its corresponding embedding, optimized for fast searching.
- **Cosine Similarity**: A metric used to measure the similarity between two vectors. A value of 1 means they are identical, 0 means they are orthogonal (unrelated), and -1 means they are opposite.
- **`numpy`**: A fundamental library for numerical operations in Python, which we will use for vector calculations.

---

## 🚀 Project-Level Deep Dive: Advanced Concepts

### Vector Databases and Approximate Nearest Neighbor (ANN) Search
The "brute-force" search we implement in the exercises (checking every single vector) is fine for a few thousand items, but it doesn't scale to millions or billions. This is where **Vector Databases** (like Pinecone, Weaviate, Milvus, or Chroma) come in. They use specialized algorithms for **Approximate Nearest Neighbor (ANN)** search, such as **HNSW (Hierarchical Navigable Small World)**. These algorithms trade a tiny bit of accuracy for a massive speedup. Instead of checking every vector, they intelligently navigate a graph-like structure to find vectors that are *probably* the closest, and they do it in milliseconds.

### Embedding Model Selection
The `all-MiniLM-L6-v2` model is a great general-purpose starting point, but it's small and fast. For higher quality, you might choose:
- **Larger Models**: Models like `all-mpnet-base-v2` provide better quality at the cost of speed.
- **Domain-Specific Models**: If you're searching medical documents, a model pre-trained on medical text will outperform a general one.
- **Multilingual Models**: If you need to search across different languages, you'd use a model designed for that purpose.
- **Fine-tuning**: For maximum performance on a specific task, you can **fine-tune** an existing embedding model on your own dataset.

### Quantization and Memory Usage
Embeddings can take up a lot of memory. A single vector of 384 dimensions using 32-bit floats takes up 1.5 KB. A million of them would be 1.5 GB. **Quantization** is a technique to reduce this memory footprint by converting the 32-bit floating-point numbers into lower-precision formats, like 8-bit integers. This can dramatically reduce memory and speed up calculations, with only a small drop in accuracy.

---

## 💻 Exercises

Create a new Python file named `katas/day5_practice.py` and complete the following exercises. You will need to install `sentence-transformers` and `numpy`:
`pip install sentence-transformers numpy`

### Exercise 1: Generate Your First Embeddings

1.  Import `SentenceTransformer` from the `sentence_transformers` library.
2.  Load a pre-trained model: `model = SentenceTransformer('all-MiniLM-L6-v2')`.
3.  Define a list of sentences: `["I love to eat pizza", "My favorite food is pasta", "Autonomous cars drive themselves"]`.
4.  Use `model.encode(sentences)` to generate embeddings for these sentences.
5.  Print the shape of the resulting embeddings array. What does each dimension represent?

### Exercise 2: Calculate Cosine Similarity

1.  Create a function `cosine_similarity(vec1, vec2)` that takes two numpy arrays (vectors).
2.  Implement the cosine similarity formula: `dot_product / (norm_a * norm_b)`.
    - Use `numpy.dot()` for the dot product.
    - Use `numpy.linalg.norm()` for the vector norms (magnitudes).
3.  Using the embeddings from Exercise 1, calculate the similarity between:
    - "I love to eat pizza" and "My favorite food is pasta"
    - "I love to eat pizza" and "Autonomous cars drive themselves"
4.  Print the results. Which pair is more similar? Does this match your expectation?

### Exercise 3: Build a Vector Index

1.  Create a class `VectorIndex`.
2.  The `__init__` method should initialize an empty list to store documents and another to store their embeddings.
3.  Create a method `add_document(self, document: str, embedding: np.ndarray)`. This method should append the document and its embedding to the respective lists.
4.  Create a method `search(self, query_embedding: np.ndarray, top_k: int = 1) -> list[tuple[str, float]]`.
5.  Inside `search`, iterate through all the stored embeddings, calculate the cosine similarity with the `query_embedding`, and keep track of the top `k` most similar documents.
6.  The method should return a list of tuples, where each tuple contains the document and its similarity score.

### Exercise 4: Create a Semantic Search Engine

1.  Create a class `SearchEngine`.
2.  In `__init__`, initialize the `SentenceTransformer` model and your `VectorIndex`.
3.  Create a method `index_documents(self, documents: list[str])`. This method should generate embeddings for the documents and add them to the `VectorIndex`.
4.  Create a method `query(self, query_text: str, top_k: int = 1) -> list[tuple[str, float]]`. This method should:
    - Generate an embedding for the `query_text`.
    - Use the `VectorIndex`'s `search` method to find the most relevant documents.
    - Return the results.
5.  Instantiate your `SearchEngine`, index the sentences from Exercise 1, and then query it with "What is a popular Italian dish?". Print the results.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **In your own words, what is a text embedding? How does it capture "meaning"?**
    - *Answer Hint:* It's a numerical representation (a vector) of text. It captures meaning by placing semantically similar text close together in a high-dimensional space. The model learns these relationships by training on vast amounts of text.
2.  **What is the difference between semantic search and traditional keyword search?**
    - *Answer Hint:* Keyword search looks for exact word matches. Semantic search looks for conceptual or contextual similarity. A keyword search for "car" won't find "automobile," but a semantic search will because their embeddings are very close.
3.  **Why is cosine similarity often preferred over Euclidean distance for measuring the similarity of text embeddings?**
    - *Answer Hint:* Text embeddings care more about the *direction* of the vector (the meaning) than its *magnitude* (which can be influenced by things like sentence length). Cosine similarity measures the angle between vectors, making it a measure of orientation, not distance.

### Intermediate
4.  **The approach in Exercise 3 is a "brute-force" search. What are some more advanced techniques or libraries used to speed up vector search in very large datasets?**
    - *Answer Hint:* The most common technique is Approximate Nearest Neighbor (ANN) search. Libraries like **FAISS** (from Facebook), **Annoy** (from Spotify), and dedicated **vector databases** (like Pinecone, Weaviate) use algorithms like HNSW or IVF to build smart data structures that allow for ultra-fast searching without having to compare the query to every single vector.
5.  **How might you handle a word that the model has never seen before (an "out-of-vocabulary" or OOV word) when generating embeddings?**
    - *Answer Hint:* Modern transformer-based models (like the one we used) use subword tokenization (e.g., WordPiece or BPE). They break down unknown words into smaller, known pieces. For example, "embedding" might be broken into "embed" and "##ding". This allows them to construct a representation for almost any word, even if they haven't seen it whole before.

### Advanced
6.  **What is the difference between sparse and dense vectors in the context of information retrieval? (e.g., TF-IDF vs. embeddings).**
    - *Answer Hint:* **Sparse vectors** (like TF-IDF) are very long, with most elements being zero. The length of the vector is the size of the entire vocabulary. They are good for keyword matching. **Dense vectors** (embeddings) are much shorter, and all elements are non-zero. They capture semantic meaning. Modern systems often use a hybrid approach, combining both for the best results.
7.  **You've been asked to build a semantic search system for a new, highly specialized domain (e.g., legal contracts). Would you use a general-purpose model like `all-MiniLM-L6-v2` or would you do something else? Explain your reasoning.**
    - *Answer Hint:* A general-purpose model is a good baseline, but it likely wouldn't understand the specific jargon of the legal domain. The best approach would be to **fine-tune** a pre-trained model on a dataset of legal contracts. This adapts the model to the specific vocabulary and context of the domain, leading to much higher quality embeddings and more relevant search results.
