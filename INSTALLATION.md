# Installation Guide – VertexAutoGPT

Follow this guide to set up and run **VertexAutoGPT**, an autonomous research agent built for intelligent tool use, long-term memory, and cost-aware infrastructure.

---

## 🔹 Prerequisites

Before starting, make sure you have the following installed:

- ✅ **Python 3.8+**
- ✅ **pip** (latest version)
- ✅ **CUDA 11+** *(optional, for GPU acceleration)*
- ✅ **Docker** *(optional, for containerized deployment)*
- ✅ **Google Cloud account** *(for scalable deployment with Preemptible VMs)*

---

## Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SaurabhCodesAI/VertexAutoGPT.git
cd VertexAutoGPT
```

---

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Environment Variables

Create a `.env` file in the root directory with your configuration:

```env
GOOGLE_API_KEY=your_google_api_key
ARXIV_API_KEY=your_arxiv_api_key
MODEL_PATH=/path/to/your/llama2-model
```

> ℹ️ Replace paths and keys with your actual credentials or local model path.

---

### 5️⃣ Run VertexAutoGPT

```bash
python main.py
```

Once started, the agent will:
- Use vector memory for context (via FAISS)
- Dynamically choose tools (search, code, papers)
- Automate multi step research workflows

---

### 6️⃣ Run with FastAPI (Optional API Mode)

```bash
uvicorn api.main:app --reload
```

The API will be available at:  
📍 `http://127.0.0.1:8000`

---

### 7️⃣ Docker Setup (Optional)

To build and run inside Docker:

```bash
docker build -t vertexautogpt .
docker run -p 8080:8080 vertexautogpt
```

> You can mount your model directory and pass `.env` variables during Docker run if needed.

---

## Troubleshooting

- **FAISS not installing?** → Try using Python 3.9 or reinstall with `conda`.
- **Model loading error?** → Check your `MODEL_PATH` or confirm the model format (e.g., HF Transformers or GGUF).
- **API keys not found?** → Ensure your `.env` file is loaded correctly.

---

## 📄 Contribution

Want to help improve VertexAutoGPT?

- Fork the repo
- Create a new branch (`git checkout -b feature-name`)
- Submit a pull request

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for details.

---

## License

Licensed under the [MIT License](./LICENSE). You own what you build.

---

## 🤝 Contact

Open to feedback, collaborations, and internship opportunities.

📧 saurabhpareek228@gmail.com
