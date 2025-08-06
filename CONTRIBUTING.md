# 🤝 Contributing to VertexAutoGPT

Thanks for your interest in contributing to **VertexAutoGPT**! This project is built to explore LLM-based autonomous agents, and we welcome ideas, bug fixes, docs, and features especially from newcomers 

---

## Ways to Contribute

You can contribute in several ways:

- 🐞 **Bug Reports** — Found a glitch? File an issue!
- 📚 **Documentation** — Improve README, tutorials, or setup instructions.
- 🛠 **Code Contributions** — Add tools, improve memory, optimize feedback loops, etc.
- 🔬 **Experiments** — Try new agent strategies, tool-chaining approaches, or model variants.
- 📦 **Infrastructure** — Optimize Docker, GCP scripts, or deployment pipelines.

---

## Project Setup (For Contributors)

1. **Fork the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/VertexAutoGPT.git
cd VertexAutoGPT
```

2. **Create a New Branch**

```bash
git checkout -b your-feature-name
```

3. **Install Dependencies**

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

4. **Make Your Changes**

- Write clean, commented code.
- Follow the existing file structure.
- Use `black` or `flake8` for formatting (optional but encouraged).

5. **Run Tests (if applicable)**

```bash
pytest
```

6. **Commit and Push**

```bash
git add .
git commit -m "Add: Your meaningful commit message"
git push origin your-feature-name
```

7. **Create a Pull Request**

Go to your fork → Click **"New Pull Request"** → Select your branch → Submit 

---

## 📂 Project Structure

```
VertexAutoGPT/
│
├── agent/             # Core logic for autonomous agents
├── tools/             # Tool integrations (search, code exec, etc.)
├── memory/            # Vector memory (FAISS)
├── api/               # FastAPI endpoints
├── docker/            # Docker config
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── .env.example       # Sample environment file
```

---

## Tips for New Contributors

- No PR is too small — even fixing typos or improving clarity helps.
- If you're unsure where to start, look at the [Issues tab](https://github.com/SaurabhCodesAI/VertexAutoGPT/issues) for `good first issue` or `help wanted` labels.
- Ask questions! Open a discussion or tag your PR with `[WIP]` (Work in Progress).

---

## Code Style

- Follow **PEP8** conventions.
- Use **docstrings** and inline comments.
- Format code with `black`:

```bash
black .
```

---

## License

By contributing, you agree that your code will be released under the [MIT License](./LICENSE).

---

## 🙌 Acknowledgement

Your time and contributions mean a lot. Whether you're improving one line or adding new modules, you're helping build the future of autonomous research agents.

Happy coding!  
*Saurabh & VertexAutoGPT Team*
