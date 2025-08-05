# VertexAutoGPT

An autonomous agent designed for automated research and workflow optimization. VertexAutoGPT combines cutting-edge AI and cloud infrastructure to create a powerful, cost-effective tool for researchers, developers, and data scientists.

---

### **Features**

* **RLHF-Optimized Decision Loop:** A fine-tuned reward model ensures the agent's tool usage becomes more efficient and effective over time.
* **FAISS-Powered Memory:** The use of a FAISS vector database allows for blazing-fast long-term memory retrieval, improving the agent's contextual awareness and performance.
* **VertexAI Toolformer-style Tooling:** The agent dynamically selects the best tool for a task, including Google Search, code execution, and data summarization, directly from its prompt.
* **Cost-Minimized Infrastructure:** By leveraging GCP Preemptible instances, VertexAutoGPT reduces training and inference costs by up to 40% compared to standard cloud setups.

---

### **Capabilities**

* **Automated Research:** Ingests and summarizes 50+ research papers per week.
* **Dynamic Tool Use:** The agent's core loop intelligently selects and executes tools.
* **Reinforcement Learning:** Optimizes its own behavior through a reward feedback system.
* **High-Performance Memory:** Achieves 10K+ token recall with ~100ms latency.

---

### **Technology Stack**

| Component | Stack |
| :--- | :--- |
| **Agent Core** | Python, Asyncio, LangChain |
| **Model Backend** | CodeLlama-7B, Mistral, VertexAI LLM APIs |
| **Memory** | FAISS VectorDB |
| **RLHF** | Custom Reward Model, PPO-style finetuning |
| **Tooling** | Google Search API, Arxiv API, Browse, Code Execution |
| **Infrastructure** | GCP Preemptible VMs, FastAPI, Docker |

---

### **Use Cases**

* Automate literature reviews and stay current on research.
* Fine-tune domain-specific agents for niche tasks.
* Scale up research assistants for large-scale data analysis.
* Experiment with RLHF in real-world, tool-using environments.

---

### **License**

This project is licensed under the MIT License. Your agent should be yours to own and control.

---

### **Contact / Collaboration**

We're open to open-source collaborations and R&D partnerships.

📧 saurabhpareek228@gmail.com
