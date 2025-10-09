# 🚀 Mini RAG - Intelligent Document Q&A System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A production-ready RAG (Retrieval-Augmented Generation) system with web search capabilities, built with FastAPI and Streamlit.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Usage](#-usage) • [API Docs](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 Core Capabilities

- **📄 Multi-Format Document Support**: Upload and process PDF, TXT, DOCX, CSV files
- **🔍 Semantic Search**: Vector-based similarity search using embeddings
- **🤖 RAG Question Answering**: Context-aware answers from your documents
- **🌐 Web Search Integration**: DuckDuckGo-powered internet search (no API key needed)
- **💬 ChatGPT-Style Interface**: Modern, responsive chat UI with e& Egypt branding
- **📊 Multiple Interfaces**: Streamlit apps for different use cases

### 🛠️ Technical Features

- **🐳 Docker Containerized**: Fully containerized with Docker Compose
- **⚡ FastAPI Backend**: High-performance async API
- **🗄️ PostgreSQL + pgvector**: Scalable vector storage
- **📦 Qdrant Vector DB**: Alternative vector database option
- **📈 Monitoring**: Prometheus + Grafana observability stack
- **🔄 Real-time Processing**: Background task processing with FastAPI
- **🎨 Modern UI**: Streamlit with custom CSS and responsive design

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ChatGPT UI   │  │ SQL Chat     │  │ Enhanced UI  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend (Port 8000)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ NLP Routes   │  │ Data Routes  │  │ Base Routes  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Controllers │  │  Models      │                         │
│  └──────────────┘  └──────────────┘                         │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌─────▼─────┐  ┌──────▼──────┐
│  PostgreSQL  │  │  Qdrant   │  │ DuckDuckGo  │
│  + pgvector  │  │ Vector DB │  │ Web Search  │
│  (Port 5432) │  │(Port 6333)│  │             │
└──────────────┘  └───────────┘  └─────────────┘
```

### 🔧 Technology Stack

**Backend:**
- FastAPI 0.115
- Python 3.13
- SQLAlchemy + Alembic (Migrations)
- Pydantic (Data Validation)

**Vector Stores:**
- Qdrant 1.13.6
- PostgreSQL 17 + pgvector 0.8.0

**Frontend:**
- Streamlit 1.40
- Custom CSS/HTML Components

**LLM Integration:**
- OpenAI API (GPT-4)
- Ollama Support (Local LLMs)
- Embeddings: text-embedding-ada-002

**Infrastructure:**
- Docker + Docker Compose
- Nginx (Reverse Proxy)
- Prometheus + Grafana (Monitoring)

---

## 📦 Prerequisites

### Required

- **Docker** & **Docker Compose** (Recommended)
- **Python 3.13** (if running without Docker)
- **WSL2** (Windows users)
- **OpenAI API Key** (or Ollama for local LLMs)

### Optional

- **Conda/Miniconda** (for Python environment management)
- **Postman** (for API testing)

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/hossammedhat81/Mini_RAG.git
cd Mini_RAG/mini-rag-app

# 2. Setup environment variables
cd docker
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Start all services
docker-compose up -d --build

# 4. Wait for services to start (30 seconds)
# Check status: docker-compose ps

# 5. Access the applications
```

**Services will be available at:**
- 🎨 **Streamlit ChatGPT UI**: `http://localhost:8501` (run separately)
- 🔧 **FastAPI Backend**: `http://localhost:8000`
- 📚 **API Docs (Swagger)**: `http://localhost:8000/docs`
- 📊 **Grafana Dashboard**: `http://localhost:3000`
- 📈 **Prometheus**: `http://localhost:9090`

### Option 2: Local Development (Windows)

```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
cd src
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start Docker services (databases only)
cd ..\docker
docker-compose up -d qdrant pgvector

# 5. Run FastAPI backend
cd ..\src
python main.py
# Backend runs on http://localhost:8000

# 6. In new terminal, run Streamlit
cd ..\streamlit_app
streamlit run app_chatgpt_style.py
# Streamlit runs on http://localhost:8501
```

### Option 3: Conda Environment

```bash
# 1. Create conda environment
conda create -n mini-rag python=3.13
conda activate mini-rag

# 2. Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install libpq-dev gcc python3-dev

# 3. Install Python packages
cd src
pip install -r requirements.txt

# 4. Follow steps 3-6 from Option 2
```

---

## 📁 Project Structure

```
mini-rag-app/
├── 📂 src/                          # Backend source code
│   ├── 📂 controllers/              # Business logic
│   │   ├── NLPController.py         # RAG & Web Search logic
│   │   ├── DataController.py        # Document processing
│   │   └── ProjectController.py     # Project management
│   ├── 📂 routes/                   # API endpoints
│   │   ├── nlp.py                   # NLP routes (search, RAG, web)
│   │   ├── data.py                  # Data upload routes
│   │   └── base.py                  # Health check routes
│   ├── 📂 models/                   # Database models
│   │   ├── ProjectModel.py
│   │   ├── AssetModel.py
│   │   └── ChunkModel.py
│   ├── 📂 stores/                   # External service integrations
│   │   ├── llm/                     # LLM providers (OpenAI, Ollama)
│   │   └── vectordb/                # Vector DB providers
│   ├── 📂 utils/                    # Utilities
│   ├── main.py                      # FastAPI app entry point
│   └── requirements.txt             # Python dependencies
│
├── 📂 streamlit_app/                # Frontend applications
│   ├── app_chatgpt_style.py         # 🌟 Main ChatGPT-style UI
│   ├── app_sql_chat.py              # SQL query interface
│   ├── app_enhanced_v2.py           # Enhanced features UI
│   ├── requirements.txt
│   └── 📂 test_*.py                 # Diagnostic tests
│
├── 📂 docker/                       # Docker configuration
│   ├── docker-compose.yml           # Service orchestration
│   ├── 📂 minirag/
│   │   ├── Dockerfile               # FastAPI container
│   │   └── entrypoint.sh
│   ├── 📂 nginx/                    # Reverse proxy config
│   ├── 📂 prometheus/               # Monitoring config
│   └── 📂 env/                      # Environment files
│
├── 📄 README.md                     # This file
├── 📄 LICENSE                       # MIT License
└── 📄 *.md                          # Documentation files
```

---

## 💻 Usage

### 1️⃣ ChatGPT-Style Interface (Recommended)

```powershell
cd streamlit_app
streamlit run app_chatgpt_style.py
```

**Features:**
- 🌐 **Web Search Mode**: Toggle to search the internet directly
- 📚 **Document Q&A**: Upload documents and ask questions
- 💬 **Chat History**: Persistent conversation history
- 🎨 **Modern UI**: Gradient badges, clickable source links
- ⚙️ **Settings**: Adjust context limit, web search results

**Usage Flow:**
1. **Upload Documents** (Optional):
   - Click "📤 Upload Documents" in sidebar
   - Select PDF/TXT/DOCX/CSV files
   - Wait for processing

2. **Enable Web Search** (Optional):
   - Toggle "🌐 Enable Internet Search" in Settings
   - All queries will search the web instead of documents

3. **Ask Questions**:
   - Type your question in the chat input
   - View answer with source badges:
     - 🌐 **From Web Search** (Teal) - Web results
     - 📚 **From Documents** (Pink) - RAG results
   - Click source links to verify information

### 2️⃣ API Usage (Programmatic)

```python
import requests

# 1. Create a project
response = requests.post("http://localhost:8000/api/v1/base/project/1")

# 2. Upload a document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/v1/data/upload/1",
        files=files
    )

# 3. Index documents
response = requests.post(
    "http://localhost:8000/api/v1/nlp/index/push/1",
    json={"do_reset": 0}
)

# 4. Ask a question (RAG)
response = requests.post(
    "http://localhost:8000/api/v1/nlp/index/answer/1",
    json={"text": "What is this document about?", "limit": 5}
)
print(response.json()["answer"])

# 5. Web search
response = requests.post(
    "http://localhost:8000/api/v1/nlp/search/web",
    json={"text": "What is RAG?", "max_results": 3}
)
print(response.json()["answer"])
```

---

## 📚 API Documentation

### Base Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/api/v1/base/project/{id}` | Create/get project |

### Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/data/upload/{project_id}` | Upload document |
| `POST` | `/api/v1/data/process/{project_id}` | Process uploaded files |
| `GET` | `/api/v1/data/assets/{project_id}` | List project assets |

### NLP Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/nlp/index/push/{project_id}` | Index documents to vector DB |
| `POST` | `/api/v1/nlp/index/search/{project_id}` | Semantic search |
| `POST` | `/api/v1/nlp/index/answer/{project_id}` | RAG question answering |
| `POST` | `/api/v1/nlp/search/web` | 🌐 Web search (DuckDuckGo) |
| `GET` | `/api/v1/nlp/index/info/{project_id}` | Vector DB collection info |

### Web Search Endpoint (New!)

```bash
# Example: Web Search
curl -X POST "http://localhost:8000/api/v1/nlp/search/web" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is Python programming?",
    "max_results": 3
  }'
```

**Response:**
```json
{
  "signal": "WEB_SEARCH_SUCCESS",
  "answer": "Python is a high-level programming language...",
  "sources": [
    {
      "title": "Python.org",
      "href": "https://python.org",
      "body": "..."
    }
  ]
}
```

**Full API Documentation:** `http://localhost:8000/docs` (Swagger UI)

---

## ⚙️ Configuration

### Environment Variables

**Backend** (`docker/env/.env.app`):
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Database Configuration
POSTGRES_HOST=pgvector
POSTGRES_PORT=5432
POSTGRES_USER=minirag
POSTGRES_PASSWORD=minirag
POSTGRES_DB=minirag

# Qdrant Configuration
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# Vector DB Selection (qdrant or pgvector)
VECTORDB_PROVIDER=qdrant
```

**Streamlit** (`streamlit_app/.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#E31B6D"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E1E1E"
textColor = "#FAFAFA"

[server]
port = 8501
```

### LLM Provider Options

**OpenAI (Default):**
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
```

**Ollama (Local LLMs):**
```bash
# Install Ollama: https://ollama.ai
# Run: ollama serve
# Pull model: ollama pull llama2

# In .env:
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **404 Error on `/api/v1/nlp/search/web`**

**Cause:** Docker container running old code without web search endpoint.

**Solution:**
```bash
cd docker
docker-compose down
docker-compose up -d --build
```

#### 2. **DuckDuckGo Rate Limit (202 Ratelimit)**

**Cause:** Too many search requests in short time.

**Solution:**
- Wait 5-10 minutes before retrying
- Use different search queries
- The badge will still show correctly (🌐 From Web Search)

#### 3. **Backend Not Starting**

**Check logs:**
```bash
docker logs fastapi --tail 50
```

**Common fixes:**
- Verify `.env` file exists with correct API keys
- Check PostgreSQL is running: `docker ps | grep pgvector`
- Restart services: `docker-compose restart`

#### 4. **Streamlit Connection Error**

**Verify backend is running:**
```powershell
curl http://localhost:8000/
# Should return: {"message": "Mini Rag is Running"}
```

**Check API base URL in Streamlit:**
```python
# In app_chatgpt_style.py
API_BASE_URL = "http://127.0.0.1:8000"  # Should match backend
```

#### 5. **Document Upload Fails**

**Check:**
- File size < 200MB
- Supported formats: PDF, TXT, DOCX, CSV
- Project exists (create with `/api/v1/base/project/1`)

### Diagnostic Tools

```powershell
# Test backend health
cd streamlit_app
python test_web_search_diagnostic.py

# Check all containers
docker ps

# View logs
docker logs fastapi
docker logs qdrant
docker logs pgvector

# Restart specific service
docker-compose restart fastapi
```

---

## 🧪 Testing

### Backend Tests

```bash
cd src
pytest tests/
```

### Frontend Diagnostic

```bash
cd streamlit_app

# Test web search endpoint
python test_web_search_diagnostic.py

# Test CSV processing
python test_csv_web.py
```

---

## 📖 Additional Documentation

- [Web Search Implementation Guide](streamlit_app/WEB_SEARCH_DEBUG_VERSION.md)
- [Rate Limit Solutions](streamlit_app/RATE_LIMIT_SOLUTION.md)
- [Debug Guide](streamlit_app/DEBUG_GUIDE.md)
- [API Collection](src/assets/mini-rag-app.postman_collection.json)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Hossam Medhat**
- GitHub: [@hossammedhat81](https://github.com/hossammedhat81)
- Repository: [Mini_RAG](https://github.com/hossammedhat81/Mini_RAG)

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **Streamlit** - Data app framework
- **Qdrant** - Vector database
- **DuckDuckGo** - Web search API
- **OpenAI** - LLM and embeddings
- **e& Egypt** - UI design inspiration

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by Hossam Medhat

</div>