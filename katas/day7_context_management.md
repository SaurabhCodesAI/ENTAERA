
# ENTAERA Kata - Day 7: Intelligent Context Management

## 🎯 Learning Objectives

Having a memory is one thing; using it effectively is another. Today's kata is about the art of context management. You will build the bridge between the agent's long-term memory and its immediate task, ensuring that prompts sent to the LLM are enriched with the most relevant information.

- **Understand the difference between a "context retriever" and a "context injector."**
- **Implement a strategy to retrieve relevant context from multiple sources (e.g., conversation history and long-term memory).**
- **Design a "context injector" that formats and prepends the retrieved context to a prompt.**
- **Manage token limits by prioritizing and truncating context.**
- **Build a pipeline that takes a user query, retrieves context, and constructs a final, context-aware prompt.**

---

## 🧠 For the Absolute Beginner

### What is Context?
In conversation, **context** is the background information that helps you understand what's going on. If a friend says, "I'm so excited for it!", you need context to know what "it" is. For an AI, context can be:
- The last few messages in your conversation (short-term memory).
- Important facts it has stored about you (long-term memory).
- The file you currently have open.

### What is RAG (Retrieval-Augmented Generation)?
This is a fancy term for a simple and powerful idea: giving the AI an "open-book exam." Instead of forcing the AI to memorize everything (which is impossible), we first **retrieve** relevant information from our knowledge sources (like our memory system). Then, we put that information into the prompt along with the user's question. This **augments** the AI's knowledge, allowing it to **generate** a much more accurate and detailed answer. The system we are building today is a RAG system.

---

## 📚 Theory & Links

Before you begin, study the implementations in:
- `src/entaera/core/context_retrieval.py`
- `src/entaera/core/context_injection.py`

Key concepts to focus on:
- **Retrieval Strategy**: The logic for deciding *what* information to fetch. This could involve the current conversation, long-term memory, or even external documents.
- **Injection Strategy**: The logic for formatting the retrieved information into a string that is clear and useful for the LLM (e.g., using headers like "Relevant Memories:" or "Recent Conversation:").
- **Token Budgeting**: A crucial step. If the retrieved context is too large, it won't fit into the LLM's context window. You must have a strategy to trim it intelligently.
- **Prompt Engineering**: The final constructed prompt is a piece of "prompt engineering." The way you structure the context can significantly impact the quality of the LLM's response.

---

## � Project-Level Deep Dive: Advanced Concepts

### Advanced Retrieval: Re-ranking and Hybrid Search
A simple semantic search is a great start, but production systems often use a multi-stage process.
1.  **Initial Retrieval**: Fetch a larger number of potential documents (e.g., top 50) using a fast but less accurate method (like vector search).
2.  **Re-ranking**: Use a more powerful, but slower, **cross-encoder** model to re-rank these 50 documents for relevance to the query. A cross-encoder processes the query and the document *together*, giving it a much deeper understanding of their relationship than the simple vector similarity we've used so far.
This two-stage process provides both speed and high accuracy.

### The "Lost in the Middle" Problem
Research has shown that many LLMs pay the most attention to information at the very beginning and very end of a long prompt. Information placed in the middle of the context can sometimes be ignored or "forgotten" by the model. This is the "lost in the middle" problem. Experienced prompt engineers are aware of this and will often structure their prompts to put the most critical information (like the final instruction) at the very end, and important but less critical context at the very beginning.

### Context Compression
Instead of just truncating context by dropping documents, what if we could summarize them? **Context compression** techniques aim to do just that. An LLM can be used to read a retrieved document and extract only the sentences that are directly relevant to the user's query. This allows you to pack more useful information into the limited context window.

---

## �💻 Exercises

Create a new Python file named `katas/day7_practice.py` and complete the following exercises. You will reuse classes and concepts from previous katas.

### Exercise 1: The `ContextRetriever`

1.  Create a class `ContextRetriever`.
2.  Its `__init__` method should take a `MemoryManager` instance (from Day 6) and a `ChatThread` instance (from Day 4) as arguments.
3.  Create a method `retrieve(self, query_text: str, max_memories: int = 3, max_history: int = 5) -> dict`.
4.  This method should:
    - Use the `MemoryManager` to get the `max_memories` most relevant long-term memories.
    - Use the `ChatThread`'s `get_context_window` method to get the `max_history` most recent messages.
    - Return a dictionary: `{'memories': [...], 'history': [...]}`.

### Exercise 2: The `ContextInjector`

1.  Create a class `ContextInjector`.
2.  Create a method `inject(self, query_text: str, context: dict, max_tokens: int = 1000) -> str`.
3.  This method should construct a final prompt string. The structure should be:
    ```
    [Relevant Memories]
    - Memory 1 content
    - Memory 2 content

    [Recent Conversation]
    user: Hello
    agent: Hi, how can I help?

    [Current Query]
    user: What is my name?
    ```
4.  **Crucially, implement token budgeting**:
    - The total length of the final prompt should not exceed `max_tokens`.
    - Start with the current query. Then add historical messages. Finally, add memories.
    - If you run out of tokens, you must truncate the context. Start by dropping memories one by one, then historical messages one by one.

### Exercise 3: The `PromptPipeline`

1.  Create a class `PromptPipeline` that ties everything together.
2.  Its `__init__` should take a `MemoryManager` and a `ChatThread`. It should then instantiate the `ContextRetriever` and `ContextInjector`.
3.  Create a method `create_prompt(self, query_text: str) -> str`.
4.  This method should:
    - Call the retriever to get the context.
    - Call the injector to build the final prompt.
    - Return the final prompt string.

### Exercise 4: Full System Simulation

1.  Instantiate all the necessary components from previous katas: `MemoryManager` and `ChatThread`.
2.  Populate them with data:
    - Add several memories to the `MemoryManager` (e.g., "The user's name is Alex", "The project deadline is Friday").
    - Add several messages to the `ChatThread`.
3.  Instantiate your `PromptPipeline` with the manager and thread.
4.  Call `pipeline.create_prompt("What is my name and when is the project due?")`.
5.  Print the final, context-enriched prompt. Verify that it contains the relevant information from both memory and conversation history.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What is the RAG (Retrieval-Augmented Generation) pattern, and how does it relate to the system we built today?**
    - *Answer Hint:* RAG is a pattern where you first **retrieve** relevant documents from a knowledge source and then add them to the prompt to **augment** the LLM's knowledge before it **generates** a response. Our system is a classic example of RAG: we retrieve from memory/history and inject it into the prompt.
2.  **Why is token budgeting important? What happens if you send a prompt that is too long to an LLM?**
    - *Answer Hint:* Every LLM has a maximum context window (a token limit). If you send a prompt that exceeds this limit, the API will reject it with an error. Token budgeting is the process of ensuring your prompt fits within this limit, which often means truncating less important information.

### Intermediate
3.  **Our token budgeting strategy is simple (dropping items). What is a more sophisticated way to truncate context while preserving the most important information?**
    - *Answer Hint:* A better way is to consider the relevance or importance score. When truncating, you would drop the items with the lowest relevance score first, regardless of whether they are memories or history messages. An even more advanced method is context compression, where you use an LLM to summarize the retrieved documents, keeping only the most salient points.
4.  **How could you handle a situation where the retrieved memories and the recent conversation history contradict each other?**
    - *Answer Hint:* The prompt structure can help. By clearly labeling the sources ("Long-term Memory:", "Recent Conversation:"), you allow the LLM to see the contradiction and potentially reason about it. You could even add an instruction in the system prompt like, "If you see conflicting information, prioritize the information from the recent conversation unless told otherwise."
5.  **This system retrieves context *before* calling the LLM. Describe an alternative approach where the LLM itself helps decide what context is needed.**
    - *Answer Hint:* This describes the "function calling" or "tool use" paradigm. In this model, you first send the user's query to the LLM along with a list of available tools (like `retrieve_memories` or `read_file`). The LLM can then decide if it needs more information and, if so, output a structured request to call one of those tools. You then execute the tool, get the result, and send it *back* to the LLM in a second call to generate the final answer.

### Advanced
6.  **What are some key metrics for evaluating the quality of a RAG system?**
    - *Answer Hint:* RAG evaluation is two-fold. **Retrieval Quality**: metrics like `nDCG` (Normalized Discounted Cumulative Gain) and `MRR` (Mean Reciprocal Rank) measure how well you rank relevant documents. **Generation Quality**: metrics like `Faithfulness` (does the answer stick to the provided context?) and `Answer Relevancy` (does the answer actually address the user's question?). These are often measured by using another LLM as a judge.
7.  **Explain the difference between RAG and fine-tuning. When would you choose one over the other?**
    - *Answer Hint:* **RAG** is about providing *knowledge* at inference time. It's great for open-domain questions where the information changes frequently (e.g., a news chatbot). **Fine-tuning** is about teaching the model a new *skill* or *style*. It's great for making the model better at a specific task (e.g., summarizing legal documents) or adopting a certain persona. They are not mutually exclusive; one of the most powerful patterns is to fine-tune a model to be better at using the context provided by a RAG system.
