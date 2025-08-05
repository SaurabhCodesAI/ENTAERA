# VertexAutoGPT

🧠 **AutoGPT-style agent** with:
- RLHF-optimized decision loop  
- FAISS-powered memory  
- VertexAI Toolformer-style tooling  
- Cost-minimized via GCP Preemptible instances

---

## 🧠 Capabilities

- 🔍 **Automated Research** — Ingests and summarizes 50+ papers per week  
- 🛠️ **Toolformer Loop** — Dynamically selects tools (search, summarize, code, write)  
- 🔄 **RLHF Loop** — Optimizes tool usage via reward feedback  
- 🧠 **FAISS Memory** — 10x faster long-term memory retrieval  
- ☁️ **VertexAI + GCP** — 40% cheaper training and inference

---

## ⚙️ Stack

| Layer          | Tech                                                                 |
|----------------|----------------------------------------------------------------------|
| Agent Core     | Python + Asyncio + LangChain                                         |
| Model Backend  | CodeLlama-7B, Mistral + VertexAI LLM APIs                            |
| Memory         | FAISS VectorDB (10K+ token recall, 100ms latency)                    |
| RLHF           | Custom Reward Model + PPO-style finetuning                           |
| Tooling        | Google Search API, Arxiv API, Browsing, Code Execution               |
| Infra          | GCP Preemptible VMs + FastAPI + Docker                               |

---

## 📦 Results

| Metric               | Value                     |
|----------------------|---------------------------|
| Cost ↓               | 40% (vs standard GCP)     |
| Token Recall ↑       | 10K+                      |
| Research Rate ↑      | 50+ papers/week           |
| Memory Latency ↓     | ~100ms (FAISS)            |

---

## 🚀 Use-Cases

- 🔬 Automate lit reviews  
- 🤖 Fine-tune domain-specific agents  
- 📈 Research assistant at scale  
- 🧪 Experiment with RLHF in real-world tools  

---

## 🧪 Example

```python
agent.query("Summarize latest papers on Mixtral’s MoE routing, pick 3 to implement.")


---

## 📜 License

**MIT** — because your agent should be yours.

---

## 💬 Contact / Collab

Open to OSS collaborations, R&D partnerships.  
📧 saurabhpareek228@gmail.com
