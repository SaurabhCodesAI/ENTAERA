# VertexAutoGPT

An autonomous agent designed for automated research. It uses a dynamic tool selection mechanism and a vector-based memory to ingest and summarize information efficiently, while optimizing for cost through cloud infrastructure choices.

## Key Features

- **Automated Research**: Capable of ingesting and summarizing information from multiple sources.

- **Dynamic Tool Selection**: Uses prompt engineering to allow the LLM to choose the right tool for a task (e.g., Google Search, Arxiv API, Browse).

- **Vector-Based Memory**: Employs a FAISS vector database to retrieve relevant information, providing the agent with long-term context.

- **Cost-Efficient Infrastructure**: Leverages GCP Preemptible VMs and Docker to significantly reduce operational costs.

- **Feedback Loop**: A rule-based system provides basic feedback to the agent to improve tool-use over time.

## Technology Stack

- **Agent Core**: Python, Asyncio, LangChain  
- **Model Backend**: OpenAI API (GPT-3.5) or fine-tuned Llama 2 7B  
- **Memory**: FAISS VectorDB  
- **Tooling**: Google Search API, Arxiv API, Browse, Code Execution  
- **Infrastructure**: GCP Preemptible VMs, FastAPI, Docker  

## What It Demonstrates

- **Systems-Level Thinking**: The ability to integrate multiple technologies (LLMs, vector databases, APIs, cloud infrastructure) into a single, functional system.

- **Advanced Concepts**: A practical understanding of vector embeddings, dynamic tool usage, and prompt engineering.

- **Problem-Solving**: The deliberate choice to use cost-saving infrastructure and a feedback loop shows a focus on practical, real-world constraints.

## License

This project is licensed under the MIT License. Your agent should be yours to own and control.

## Contact / Collaboration

We're open to open-source collaborations and R&D partnerships.

📧 saurabhpareek228@gmail.com
