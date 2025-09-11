# RESEARCH.md – VertexAutoGPT

This document outlines the **research philosophy**, **architecture decisions**, and **open exploration questions** behind **VertexAutoGPT**, an autonomous LLM agent focused on automated research under real-world constraints.

---

## Objective

To build a modular, lightweight, and cost-efficient LLM agent capable of:

- **Ingesting** large volumes of information from multiple sources
- **Deciding** which tools to use for different tasks
- **Remembering** long-term context using vector memory
- **Adapting** via feedback loops to improve over time

---

## Research Questions

1. **Minimal Intelligence**  
   What is the minimal level of autonomy an LLM agent needs to be useful in real-world research tasks?

2. **Tool Use Reasoning**  
   Can we train/prompt an agent to **intelligently decide** between tools like search, code execution, or PDF reading?

3. **Memory Architecture**  
   How can vector-based memory (FAISS) be used for:
   - Cross-session recall
   - Retrieval-Augmented Generation (RAG)
   - Semantic chaining across long tasks?

4. **Feedback Loops**  
   How effective are lightweight rule-based feedback systems for helping the agent self-correct?

5. **Cost-Aware Systems**  
   What trade-offs exist between model quality and compute cost in deployment environments like GCP Preemptible VMs?

---

## Agent Architecture

```
                        ┌────────────────────────────┐
                        │        User Query          │
                        └────────────┬───────────────┘
                                     │
                        ┌────────────▼───────────────┐
                        │     Agent Controller       │
                        └────────────┬───────────────┘
                                     │
                ┌────────────────────┴─────────────────────┐
                │                                          │
        ┌───────▼───────┐                          ┌───────▼────────┐
        │ Tool Router   │                          │ Vector Memory  │
        └───────┬───────┘                          └────────┬───────┘
                │                                           │
   ┌────────────▼────────────┐                  ┌──────────▼────────────┐
   │  Tool Selection Logic   │     <──────▶     │   FAISS (Contextual)  │
   └────────────┬────────────┘                  └──────────┬────────────┘
                │                                           │
      ┌─────────▼────────┐                        ┌────────▼─────────┐
      │  Search / Arxiv  │                        │   Long-term RAG  │
      │  Code Execution  │                        └──────────────────┘
      └──────────────────┘

```

---

## Experimentation Goals

| Area                | Hypothesis                                         | Status     |
|---------------------|----------------------------------------------------|------------|
| Tool Selection      | LLM can be guided via prompt routing               |  Working |
| Vector Recall       | FAISS improves multi-turn continuity               |  Working |
| Feedback Loop       | Rule-based correction improves outcomes            |  Testing |
| GCP Cost Efficiency | Preemptible VMs reduce infra costs without loss    |  Working |
| Model Performance   | Llama 2 7B is sufficient for mid-complexity tasks  |  Evaluating |

---

## 📂 Key Modules

- `agent/`: Core control loop & orchestration
- `tools/`: Tool wrappers (search, arxiv, code, etc.)
- `memory/`: FAISS setup & query handling
- `feedback/`: Basic rules to improve agent responses
- `api/`: FastAPI interface for local deployment

---

## Inspirations

- [AutoGPT](https://github.com/Torantulino/Auto-GPT)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
- [LangChain Agents](https://docs.langchain.com/docs/components/agents)
- [Open Decomp](https://open-decomp.github.io)

---

## Future Research Directions

-  Fine-tuned reward loops (RLHF-lite)
-  Plugin-based modularity for tools
-  Memory compression for long sessions
-  Budget-aware decision making
-  Auto-curation of reading lists from paper databases

---

## 🙋 Contributing to Research

Have a crazy idea? Want to test your own tool? Submit a pull request or open a discussion!

Let’s build autonomous agents with real world practicality 

*Saurabh Pareek*  
📨 saurabhpareek228@gmail.com
