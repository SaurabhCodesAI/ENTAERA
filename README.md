# ENTAERA

**An experimental multi-provider AI agent system built to learn async patterns, API integration, routing, and conversation memory.**

> 💡 **Seeking Microgrant:** $400 to upgrade memory from TF-IDF to semantic embeddings. [See funding details →](./ROADMAP.md)

---

## Why I Built This

I wanted to understand how AI agents actually work under the hood not just call a single API. This project began as a small "connect to Ollama" script and turned into a 6-month learning journey involving async orchestration, memory, routing, and safe error handling. I used ChatGPT/Claude to learn faster, but every piece of logic is something I debugged, wrote, and understand. This is a learning project that works.

---

## What Works Today (Honest Status)

**Multi-Provider Support**
- Ollama (local), Google Gemini, Perplexity, Azure OpenAI
- Async calls with fallback chain (Gemini → Perplexity → Ollama)
- Basic rate-limit and timeout handling

**Conversation Memory**
- TF-IDF keyword search (no embeddings yet)
- Persistent memory via pickle
- Hybrid retrieval (semantic-ish keyword match + recent history)

**Agent Routing**
- 5 specialized agents (Assistant, Code, Data, Creative, Research)
- Simple keyword-based routing
- Basic usage statistics per agent

**Error Handling**
- Exponential backoff
- Provider fallbacks
- Graceful timeout handling

---

## Architecture Overview

```
      User Query
           │
           ▼
┌────────────────────────────┐
│  Agent Router (Keywords)   │
│  "code"→Code | "data"→Data │
└───────────┬────────────────┘
            │
            ▼
┌────────────────────────────┐
│    Memory Search (TF-IDF)  │
│   Retrieve past context    │
└───────────┬────────────────┘
            │
            ▼
┌────────────────────────────┐
│  Async API Handler         │
│ Gemini → Perplexity → Ollama│
└───────────┬────────────────┘
            │
            ▼
┌────────────────────────────┐
│ Response + Memory Update   │
└────────────────────────────┘
```

**Key Files**
- `agent.py` — main CLI agent (≈500 lines)
- `src/entaera/` — experimental modules (not fully integrated)
- `requirements-local-models.txt` — dependencies

---

## Current Limitations (Honest List)

1. **No vector embeddings** — memory is TF-IDF, not semantic.
2. **Keyword routing only** — ambiguous prompts may route incorrectly.
3. **Pickle-based storage** — not database safe, single user only.
4. **Minimal tests** — basic checks only, no unit tests for memory/routing.
5. **CLI-only** — no FastAPI or UI yet.
6. **Manual .env setup** — no validation for missing/invalid keys.
7. **Basic fallback logic** — works, but not robust for edge cases.

---

## Roadmap

**Current Focus:** Semantic memory upgrade (funded by microgrant)

**Next 8-10 Weeks**
- Replace TF-IDF with sentence-transformers
- Add FAISS vector storage
- Build comprehensive test suite
- Deploy live demo for community testing

See [ROADMAP.md](./ROADMAP.md) for detailed timeline and deliverables.

**Future Possibilities** (post-funding)
- REST API endpoint
- Multi-user support
- Streaming responses

---

## Installation

**Requirements**
- Python 3.11+
- Running Ollama (`ollama serve`)
- API keys for Gemini, Perplexity, or Azure

**Setup**
```bash
git clone https://github.com/SaurabhCodesAI/ENTAERA.git
cd ENTAERA
pip install aiohttp python-dotenv

# Add your environment variables
cp .env.example .env
```

**Run**
```bash
ollama serve  # separate terminal
python agent.py
```

**Commands**
- `/agents` — list agents
- `/memory [n]` — show history
- `/search <query>` — TF-IDF search
- `/stats` — usage stats
- `/clear` — clear memory
- `/quit` — exit

---

## Support This Project

**Microgrant Request: $400**

Funding will upgrade ENTAERA's memory from keyword-based (TF-IDF) to semantic embeddings, making context retrieval significantly better.

**Budget:**
- $120 — API testing credits (Gemini Pro + Perplexity)
- $80 — Cloud deployment for live demo (3 months)
- $200 — Development time (open source rate)

**Timeline:** 8-10 weeks  
**Deliverable:** Working semantic search with live demo anyone can test

**Why fund this?**
- Real working code, not tutorials
- Helps developers learn multi-provider AI orchestration
- Open source (MIT), benefits entire community
- Honest about scope and limitations

**[📋 Full Roadmap & Details →](./ROADMAP.md)**

---

## Contributing

This is a learning project, so small, helpful contributions are welcome.

**Good First Issues**
- Improve docs
- Clean up error messages
- Add small tests
- Add type hints or logging improvements

**Larger Contributions**
- Adding a new provider
- Implementing embeddings
- Building FastAPI service

**Not Looking For**
- Full rewrites
- Large architectural changes
- Enterprise auth systems

See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Tech Stack

**Language:** Python 3.11+  
**Core:** `asyncio`, `aiohttp`, `python-dotenv`, `pickle`  
**Providers:** Ollama, Gemini, Perplexity, Azure OpenAI  
**Memory:** TF-IDF keyword search  
**Architecture:** Single file CLI with experimental modules

---

## License

MIT License — see [LICENSE](./LICENSE).

---

## Maintainer

Built by **Saurabh Pareek** ([@SaurabhCodesAI](https://github.com/SaurabhCodesAI))

6 months of debugging, learning, and real hands on development.  
Not perfect, but honest work.

**Note:** AI assistants (ChatGPT, Claude) were used for learning and debugging, not for producing code I don't understand.
