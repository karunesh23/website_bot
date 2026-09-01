# ITC Enterprise RAG Chatbot

## Tech Stack

- FastAPI
- PostgreSQL
- pgvector
- Gemini API
- SQLAlchemy
- LangChain Text Splitter

---

## Features

- Enterprise RAG
- PostgreSQL Vector Search
- Lead Management
- Ticket Management
- Conversation History
- Semantic Search
- Knowledge Base
- REST API

---

## Installation

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

Run

```bash
uvicorn app.main:app --reload
```

---

Create Tables

```bash
python scripts/create_tables.py
```

---

Ingest Knowledge Base

```bash
python scripts/ingest_documents.py
```

---

Open

```
http://localhost:8000/docs
```