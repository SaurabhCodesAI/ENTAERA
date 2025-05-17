# ENTAERA

**An experimental multi-provider AI agent system built to learn API integration, async programming, and conversation memory patterns.**

---

## Why I Built This

I spent six months learning how to connect multiple AI APIs (Ollama, Gemini, Perplexity, Azure OpenAI) and build a working conversation system. This started as practice with a single local model and evolved into understanding authentication, async patterns, error handling, and basic semantic search. I built this to learn—not as production software, but as a real codebase that solves real problems.

---

## What Works Today

**Multi-Provider Integration**
- Connects to 4 AI services: Ollama (local), Google Gemini, Perplexity, Azure OpenAI
- Async API calls with proper error handling and fallbacks
- Each provider tested and working (Azure temporarily disabled by choice)

**Conversation Memory**
- TF-IDF-based semantic search for retrieving relevant past conversations
- Persistent storage using Python pickle (conversation_memory.pkl)
- Hybrid retrieval: combines recent messages + semantically similar history
- Search works, but accuracy depends on keyword overlap (not embeddings)

**Agent Routing**
- 5 specialized agents: Assistant, Code, Data Analyst, Creative Writer, Research
- Keyword-based routing (e.g., "code" → Code Assistant, "analyze" → Data Analyst)
- Performance tracking per agent (query count, success rate)

**System Architecture**
- Async/await throughout (asyncio, aiohttp)
- Rate limiting and quota management
- Environment-based config (.env file for API keys)
- CLI with `/memory`, `/search`, `/agents`, `/stats` commands

---

## Technical Overview

ENTAERA uses a simple architecture:

```
User Query
    ↓
Keyword Router → Select Agent (Assistant/Code/Data/Creative/Research)
    ↓
API Manager → Call Ollama/Gemini/Perplexity/Azure (async, with fallbacks)
    ↓
Memory Manager → Store conversation + TF-IDF index
    ↓
Response returned to user
```

The core logic lives in `agent.py` (~800 lines). Memory uses TF-IDF cosine similarity (not vector embeddings). Routing is rule-based (keyword matching), not learned.

---

## Limitations (Current Reality)

**Memory & Search**
- Uses TF-IDF (bag-of-words), not embeddings—misses semantic meaning
- Memory retrieval accuracy depends on exact keyword overlap
- No vector database (FAISS/Chroma)—planned but not implemented

**Routing & Agents**
- Agent selection uses simple keyword matching, not classification models
- Can route incorrectly if query doesn't match expected patterns
- No multi-agent orchestration (agents don't collaborate)

**Production Readiness**
- No FastAPI endpoint (CLI only)
- No user authentication or multi-user support
- Tests exist but coverage is incomplete
- Documentation is learning-focused, not API reference quality

**Dependencies**
- Requires Ollama running locally (external dependency)
- API keys needed for Gemini/Perplexity (cost barrier for users)
- Pickle for persistence (not scalable, not portable)

---

## Installation & Usage

```bash
# Clone repository
git clone https://github.com/SaurabhCodesAI/ENTAERA.git
cd ENTAERA

# Install dependencies
pip install -r requirements-local-models.txt

# Set up API keys (copy .env.example to .env, add your keys)
cp .env.example .env

# Start Ollama (required for local model)
ollama serve

# Run the agent
python agent.py
```

**CLI Commands:**
- `/agents` — List available agents
- `/memory [n]` — Show last n conversations
- `/search <query>` — Semantic search in history
- `/stats` — Usage statistics
- `/clear` — Clear memory
- `/quit` — Exit

---

## Roadmap (Realistic & Achievable)

**Next 3–6 months:**

1. **Replace TF-IDF with embeddings** — Use `sentence-transformers` + FAISS for real semantic search
2. **Add FastAPI endpoint** — Expose agent as HTTP API for external use
3. **Improve test coverage** — Write unit tests for routing, memory, API calls
4. **Plugin system** — Allow custom agents/tools without modifying core code
5. **Better error messages** — User-friendly feedback instead of stack traces
6. **Documentation rewrite** — API reference, architecture diagrams, contribution guide

**Not promising:** Real-time streaming, multi-user auth, or production deployment soon. Those require significant additional work.

---

## How a Microgrant Would Be Used

**Budget Request: $500–$800**

Funding would support:
- **API credits ($200):** Test Gemini/Perplexity at scale, benchmark performance
- **Cloud compute ($150):** Run experiments with embeddings (FAISS indexing, model fine-tuning)
- **Documentation time ($200):** Rewrite docs, create architecture diagrams, write tutorials
- **Testing infrastructure ($100):** Set up CI/CD, increase test coverage
- **Developer time ($150):** Fix bugs reported by users, implement top-requested features

This is a learning project, not a startup. The goal is to make it easier for others to understand AI integration patterns and contribute improvements. Any funding accelerates learning and helps the project serve the open-source community better.

---

## Contributing

This is a learning project—contributions are welcome, especially:
- Bug fixes (check GitHub Issues)
- Documentation improvements
- Test coverage expansion
- Code review and refactoring suggestions

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines. No contribution is too small.

---

## Project Structure

```
ENTAERA/
├── agent.py                       # Main agent (CLI, routing, memory, API calls)
├── requirements-local-models.txt  # Python dependencies
├── .env.example                   # Template for API keys
├── conversation_memory.pkl        # Persistent memory (auto-generated)
├── katas/                         # Learning exercises (17 days, 95+ hours)
└── src/entaera/core/              # Advanced modules (mostly experimental)
    ├── semantic_search.py         # Planned: embedding-based search
    ├── conversation_memory.py     # Planned: improved memory system
    ├── code_analysis.py           # Experimental code intelligence
    └── ...                        # Other exploratory modules
```

**Note:** `src/entaera/core/` contains experimental code—not all modules are used in `agent.py`. The working system is in `agent.py`.

---

## Tech Stack

- **Python 3.13+** (async/await, dataclasses, type hints)
- **Libraries:** `asyncio`, `aiohttp`, `python-dotenv`, `pickle`
- **AI Providers:** Ollama, Google Gemini, Perplexity, Azure OpenAI (optional)
- **Memory:** TF-IDF (sklearn-style tokenization + cosine similarity)

---

## License

MIT License. Free to use, modify, and distribute. See [LICENSE](./LICENSE) for details.

---

## Maintainer

Built by **Saurabh Pareek** as a 6-month learning project (May–November 2024).

- GitHub: [@SaurabhCodesAI](https://github.com/SaurabhCodesAI)
- Email: [contact info in profile]

**Transparency note:** This project used AI assistants (ChatGPT, Claude) for learning concepts, debugging, and discovering patterns. I tested and validated everything myself—the code I kept is code I understand and can maintain. AI helped me learn faster; it didn't write the project for me.

---

## Grant Application Snippets

### A) One-Line Elevator Pitch
"ENTAERA is an experimental AI agent learning project demonstrating multi-provider integration, TF-IDF memory, and async patterns—built transparently over 6 months to understand modern AI systems."

### B) 3-Sentence Grant Description
ENTAERA is a hands-on learning project where I spent six months building a multi-provider AI agent system from scratch, connecting Ollama, Gemini, Perplexity, and Azure OpenAI with async Python. The system includes TF-IDF-based conversation memory, keyword-based routing, and error handling—all documented honestly with clear limitations (no embeddings yet, simple routing, CLI-only). Funding would support API testing, documentation improvements, and transitioning from TF-IDF to proper vector search, making the codebase more educational for other learners.

### C) Budget Justification (80 words)
This $500–$800 request covers practical development costs: $200 for API credits to test Gemini/Perplexity at scale and benchmark performance; $150 for cloud compute to experiment with FAISS embeddings; $200 for documentation time (architecture diagrams, tutorials, API reference); $100 for CI/CD and testing infrastructure; $150 for developer time fixing bugs and implementing features requested by the community. This is a learning project, not commercial software—funding helps make AI integration patterns accessible to other developers learning these skills.
