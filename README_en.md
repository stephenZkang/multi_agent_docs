# Multi-Agent Document Intelligence Platform

This project is a multi-agent document intelligence platform supporting PDF parsing, Q&A, summarization, writing, translation, ESG compliance checking, and more. It is designed for enterprise knowledge management and office automation scenarios.

## ✨ Key Features

- 🤖 **Multi-Agent Collaboration**: 
  - Pipeline of specialized agents: not a single model, but multiple agents working in sequence (retrieval, Q&A, summarization, writing, translation, compliance, etc.), making the process modular and extensible.
  - Traceable multi-step results: Each agent's output is preserved for traceability and multi-angle analysis.
  - Multi-task support: Not just Q&A, but also automatic summarization, business writing, translation, compliance checking, etc.
  - Easy to extend: Agents can be plugged, removed, or recombined to customize your own document workflow.
  - Structured output: Final results are structured dicts, suitable for frontend display or automation.
- 📄 **PDF Parsing**: Automatically batch-read PDF files from the `documents/` directory, extract text, and embed into a vector database.
- 🔍 **Vector Search**: Efficient semantic retrieval based on FAISS and Sentence Transformers, with vector files stored in the `data/` directory.
- 💬 **Intelligent Q&A and Summarization**: Q&A and summarization based on document content.
- ✍️ **Auto Writing & Translation**: Generate business introductions from summaries and support bi-directional translation.
- ✅ **ESG Compliance Checking**: Automatically check if text meets ESG sustainability principles.

## 🗂️ Directory Structure

```
main.py                  # Main entry point
requirements.txt         # Dependencies
agents/                  # Agent modules
api/                     # API endpoints (e.g., qa_api)
core/                    # Vector DB, cache, model APIs, etc.
data/                    # Persistent data (vector.index, metadata.pkl)
ui/                      # Optional: frontend or interface layer
prompts/                 # Prompt templates
documents/               # PDF files
```

## 🚀 Quick Start

1. **Install dependencies (Python 3.8+)**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare documents**
   - Place your PDF files in the `documents/` directory.

3. **Run main program in CLI mode**

   ```bash
   python main.py
   ```

   - On first run, PDFs are parsed and the vector DB is built (files stored in `data/`).
   - Multi-turn Q&A supported in the console.

4. **Web UI mode (recommended)**

   ```bash
   streamlit run ui/app.py
   ```

   - A browser Q&A interface will open automatically.

5. **Backend API service mode**

   ```bash
   uvicorn api.qa_api:app --reload --port 8000
   ```

   - Visit http://localhost:8000/docs for API docs.
   - Main endpoints:
     - `POST /qa` with JSON: `{"input": "your question", "template": "default"}`
     - `GET /ping` health check

## 📦 Dependencies

- Python 3.8+
- faiss-cpu
- sentence-transformers
- pypdf
- pdfplumber
- pymupdf
- langchain
- langgraph
- langchain-core
- streamlit
- fastapi
- uvicorn

## 🧪 Testing

All agents and core modules have basic unit tests:

- `tests/agents/`: agent tests
- `tests/core/`: core module tests (cache, logger, vectordb, gemini_client)

Run all agent tests:

```bash
python -m unittest discover -s tests/agents
```

Run all core module tests:

```bash
python -m unittest discover -s tests/core
```

Or run a single test file, e.g.:

```bash
python -m unittest tests/agents/test_weather_agent.py
python -m unittest tests/core/test_cache.py
```

## 🐳 Docker Deployment

1. Build image:

   ```bash
   docker build -t multi-agent-docs .
   ```

2. Run container (Web UI, port 8501):

   ```bash
   docker run -it --rm -p 8501:8501 \
     -v $PWD/documents:/app/documents \
     --env-file .env \
     multi-agent-docs
   ```

   - Mount `documents` and `.env` for persistence.
   - Visit [http://localhost:8501](http://localhost:8501) for the web UI.

3. CLI mode:

   ```bash
   docker run -it --rm \
     -v $PWD/documents:/app/documents \
     --env-file .env \
     multi-agent-docs \
     python main.py
   ```

## 🤝 Contributing & License

- Issues and PRs are welcome.
- MIT License.

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [PyPDF](https://pypdf.readthedocs.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Streamlit](https://docs.streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker Documentation](https://docs.docker.com/)

### 📖 Blogs & Papers

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Auto-GPT: An Autonomous GPT-4 Experiment](https://github.com/Significant-Gravitas/Auto-GPT)
- [LangChain Multi-Agent Collaboration (Zhihu, Chinese)](https://zhuanlan.zhihu.com/p/624073222)
- [Vector Database Introduction & Practice (Zhihu, Chinese)](https://zhuanlan.zhihu.com/p/624073222)
- [Document AI: Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/introducing-document-ai)
- [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 

### 📝 Prompt Engineering References & Papers

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Prompt Engineering for Large Language Models (arXiv)](https://arxiv.org/abs/2302.11382)
- [A Survey of Prompt Engineering (arXiv)](https://arxiv.org/abs/2301.13688)
- [How to Prompt LLMs (OpenAI Cookbook)](https://cookbook.openai.com/examples/how_to_prompt) 