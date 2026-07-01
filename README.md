# 🚀 Research Agent

A production-style **Multi-Agent Research Assistant** built using **LangGraph**, **DuckDB**, **Tavily**, **Docling**, and a **local Qwen LLM (Ollama)**.

The system combines **Retrieval-Augmented Generation (RAG)** with **web search** to answer research questions from uploaded documents while also fetching up-to-date information from the internet when required.

---

# ✨ Features

- 📄 PDF → Markdown conversion using Docling
- ✂️ Parent-Child Chunking
- 🧠 SentenceTransformer embeddings
- 🗄️ DuckDB Vector Database
- 🔍 Semantic Search
- 🌐 Tavily Web Search
- 🤖 LangGraph Multi-Agent Workflow
- 🦙 Local Qwen LLM using Ollama
- ⚡ FastAPI Backend

---

# 🏗️ Architecture

```
                   User
                     │
                     ▼
               FastAPI Endpoint
                     │
                     ▼
             LangGraph Executor
                     │
                     ▼
               Planner Agent
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Retrieval Tool        Web Search Tool
          │                     │
          └──────────┬──────────┘
                     ▼
              Research Agent
                     │
                     ▼
              Final Response
```

---

# 📂 Project Structure

```text
ResearchAgent/
│
├── main.py
├── requirements.txt
├── research.db
│
├── data/
│   ├── papers/
│   ├── markdown/
│   └── parent_dir/
│
├── rag/
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── prompt.py
│
├── tools/
│   ├── retrieval_tool.py
│   ├── web_search_tool.py
│   └── pdf_tool.py
│
├── agent/
│   ├── llm.py
│   ├── prompt.py
│   ├── tools.py
│   ├── agent.py
│   └── executor.py
│
├── api/
│   ├── routes.py
│   └── schemas.py
│
└── utils/
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| LangGraph | Multi-Agent Workflow |
| LangChain | Tool Calling |
| DuckDB | Vector Database |
| SentenceTransformers | Embeddings |
| Docling | PDF Parsing |
| Ollama | Local LLM |
| Qwen | Language Model |
| Tavily | Web Search |
| FastAPI | REST API |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Betanode/ResearcAgent.git
```

Go inside the project

```bash
cd ResearcAgent
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
TAVILY_API_KEY=YOUR_API_KEY
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen2.5:7b
```

---

# ▶️ Run

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

---

# 📖 Workflow

1. Upload PDF
2. Convert PDF to Markdown
3. Parent-Child Chunking
4. Generate Embeddings
5. Store Embeddings in DuckDB
6. User asks a question
7. Planner Agent decides:
   - Retrieval Tool
   - Web Search Tool
   - Both
8. Research Agent generates the final answer

---

# 🚀 Future Improvements

- Conversation Memory
- Hybrid Search
- Re-ranking
- Source Citations
- Streaming Responses
- Multi-document Support
- MCP Integration
- Evaluation Pipeline

---

# 👨‍💻 Author

**Abhinav Dwivedi**

AI Engineer | Backend Engineer | Building AI Agents & RAG Systems

---

# ⭐ If you found this project useful, consider giving it a star!
