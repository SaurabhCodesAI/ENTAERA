
# ENTAERA Kata - Day 6: Building Long-Term Memory

## 🎯 Learning Objectives

An AI agent with no memory is not intelligent. Today, you will build upon the previous katas to create a long-term memory system for our agent. This involves combining data modeling (Day 4) with semantic search (Day 5) to store and retrieve past conversations.

- **Design a data structure for storing "memories."**
- **Use a semantic search index to store and retrieve memories based on meaning.**
- **Implement a `MemoryManager` to encapsulate memory operations.**
- **Distinguish between storing a full conversation and storing key "memories."**
- **Create a mechanism to retrieve relevant memories for a new query.**

---

## 🧠 For the Absolute Beginner

### What is AI Memory?
Like humans, AIs have two kinds of memory. **Short-term memory** is the current conversation, the things you've just said (this is the "context window" from Day 4). It's limited and gets forgotten quickly. **Long-term memory** is for important facts the AI should remember forever, like your name, your goals, or key decisions. Today, we are building the long-term memory system.

### How Does it Work?
We take important pieces of information, turn them into "memories" (which are just structured data), and store them. To find a memory, the AI doesn't search by keywords. Instead, when you ask a new question, the AI uses the semantic search we built yesterday to find old memories that are *conceptually related* to your question. This allows it to recall relevant facts even if you use different wording.

---

## 📚 Theory & Links

Before you begin, study the implementation in:
- `src/entaera/core/conversation_memory.py`

Key concepts to focus on:
- **Memory as Data**: A "memory" is not just a raw string; it's a structured piece of data, often containing the content, a timestamp, and other metadata.
- **Indexing Memories**: Instead of just indexing documents, we are now indexing structured `Memory` objects. The search should return the full object, not just the text.
- **Retrieval for Context**: The goal of the memory system is to find past information that is relevant to the *current* conversation turn, so it can be used as context for the AI.
- **Abstraction**: The `ConversationMemoryManager` provides a clean interface (`add_memory`, `retrieve_relevant_memories`) that hides the complexity of the underlying vector search.

---

## 🚀 Project-Level Deep Dive: Advanced Concepts

### The Memory Stream and Scoring
A famous paper, "Generative Agents: Interactive Simulacra of Human Behavior," introduced the concept of a comprehensive **memory stream**. Every event the agent perceives is turned into a memory object. Each memory is then given three scores:
1.  **Recency**: Newer memories are more likely to be relevant. This score decays over time.
2.  **Importance**: How significant is the memory? "My name is Bob" is more important than "The sky is blue." This can be rated by an LLM.
3.  **Relevance**: How similar is the memory to the current situation (the query)? This is the cosine similarity score we've been using.

A final retrieval score is calculated by combining these three scores, giving a much more nuanced and human-like memory retrieval mechanism.

### Memory Summarization and Reflection
A long list of raw memories can become inefficient. Advanced agents use a **reflection** process. Periodically, the agent looks at its recent memories and asks itself, "What are the key insights or takeaways from these memories?" It then generates a new, higher-level summary memory. This is analogous to how humans consolidate experiences into general knowledge. This process creates a hierarchy of memories, from raw observations to high-level wisdom.

### Hybrid Search for Memory
Semantic search is powerful but sometimes you need to find an exact keyword or entity. Production-grade memory systems often use **hybrid search**. They combine the results from a semantic (vector) search with a traditional keyword search (like BM25). This gives you the best of both worlds: you can find things by meaning *and* by specific, exact terms.

---

## 💻 Exercises

Create a new Python file named `katas/day6_practice.py` and complete the following exercises. You will reuse concepts and code from the Day 5 kata.

### Exercise 1: The `Memory` Model

1.  Using Pydantic, create a `BaseModel` called `Memory`.
2.  It should have the following fields:
    - `content: str`: The text of the memory.
    - `timestamp: datetime`: When the memory was created.
    - `importance: float`: A score from 0.0 to 1.0 indicating the memory's importance.
    - `metadata: dict = {}`: A flexible dictionary for any other data.

### Exercise 2: The `MemoryIndex`

1.  This will be an adaptation of the `VectorIndex` from Day 5. Create a new class `MemoryIndex`.
2.  Instead of storing raw documents, the index should store `Memory` objects.
3.  Modify the `add_document` method to be `add_memory(self, memory: Memory, embedding: np.ndarray)`. It should store the `Memory` object and its corresponding embedding.
4.  Modify the `search` method. It should now return a list of `Memory` objects and their similarity scores, not just strings.
    - `search(self, query_embedding: np.ndarray, top_k: int = 3) -> list[tuple[Memory, float]]`

### Exercise 3: The `MemoryManager`

1.  Create a class `MemoryManager`.
2.  In `__init__`, initialize the `SentenceTransformer` model and your `MemoryIndex`.
3.  Create a method `add_memory(self, content: str, importance: float)`. This method should:
    - Create a `Memory` object.
    - Generate an embedding for the `content`.
    - Add the memory and its embedding to the `MemoryIndex`.
4.  Create a method `retrieve_memories(self, query_text: str, top_k: int = 3) -> list[Memory]`. This method should:
    - Generate an embedding for the `query_text`.
    - Use the `MemoryIndex` to find the most relevant memories.
    - Return just the list of `Memory` objects, without the scores.

### Exercise 4: A Day in the Life of an Agent

1.  Instantiate your `MemoryManager`.
2.  Simulate a conversation by adding several memories with varying importance scores:
    - `manager.add_memory("My favorite color is blue.", importance=0.8)`
    - `manager.add_memory("I had pizza for lunch today.", importance=0.3)`
    - `manager.add_memory("The user's name is Alex.", importance=1.0)`
    - `manager.add_memory("I need to remember to set a reminder for the 5 PM meeting.", importance=0.9)`
    - `manager.add_memory("The weather is sunny.", importance=0.1)`
3.  Now, simulate a new query from the user: `"What is my name?"`.
4.  Use your `retrieve_memories` method with this query.
5.  Print the retrieved memories. Did the system correctly retrieve the memory about the user's name?
6.  Try another query: `"What should I be doing later?"`. Did it retrieve the meeting reminder?

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What are the challenges of implementing a long-term memory system for an AI agent?**
    - *Answer Hint:* Key challenges are **scalability** (how to search billions of memories quickly), **relevance** (how to find the right memory and not just noisy, related ones), **cost** (storing and embedding memories costs money), and **forgetting** (how to get rid of old, useless information).
2.  **In our `Memory` model, we added an `importance` score. How might an AI agent decide on the importance of a piece of information?**
    - *Answer Hint:* A simple way is to look for keywords ("My name is...", "Remember that..."). A more advanced way is to use an LLM itself. You can prompt the LLM with the memory and ask it, "On a scale of 1 to 10, how important is this piece of information for future reference?"
3.  **How is this memory system different from the `ContextWindow` we built in Day 4? When would you use one versus the other?**
    - *Answer Hint:* The `ContextWindow` is **short-term, sequential memory**. It's a perfect transcript of the immediate past. The `MemoryManager` is **long-term, semantic memory**. It's a curated collection of important facts. You use the context window for the flow of the current conversation and the memory manager to pull in relevant facts from the distant past.

### Intermediate
4.  **This system retrieves memories but doesn't "forget." Describe a simple strategy you could implement to make the agent forget or decay old, unimportant memories.**
    - *Answer Hint:* A simple strategy is to combine recency and importance. You could have a background process that periodically scans for memories that are both old (e.g., > 30 days) and have a low importance score (e.g., < 0.2). These memories could then be deleted from the index.
5.  **Beyond conversations, what other kinds of "memories" could be useful for an AI coding assistant?**
    - *Answer Hint:* It could remember **code snippets** you frequently use, **project-specific architectural decisions** ("In this project, we always use the Strategy pattern for new services"), **user preferences** ("The user prefers pytest over unittest"), or **past errors** and their solutions.

### Advanced
6.  **How would you handle conflicting information in memory? For example, the agent has a memory "The user's name is Bob" and a new one "The user's name is Alice."**
    - *Answer Hint:* This is a belief revision problem. A robust system would need a mechanism to handle this. When adding a new memory, you could first retrieve similar memories. If a direct contradiction is found, the system could either trust the most recent information, or it could explicitly ask the user for clarification: "I thought your name was Bob, but you just said it was Alice. Which one is correct?" The confirmed memory could then be given a much higher importance score.
7.  **Explain the concept of a "memory hierarchy." How does it help with efficiency and reasoning?**
    - *Answer Hint:* A memory hierarchy involves different levels of memory abstraction. At the bottom are raw observations (every message). The next level up contains "reflections" or summaries of those observations. The highest level might contain general principles or beliefs derived from reflections. This is efficient because the agent doesn't need to search through thousands of raw events to find a high-level concept. It allows for more complex reasoning by operating on these higher-level abstractions.
