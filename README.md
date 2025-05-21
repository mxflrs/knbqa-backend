
---

## **backend/README.md**

```markdown
# Knowledge Base Backend (FastAPI + Langchain)

This is the **backend** for the Knowledge Base Q&A app. Built with **FastAPI**, **Langchain**, **LangGraph**, and **PostgreSQL**. Handles document ingestion, chunking, embeddings, and question answering using retrieval-augmented generation (RAG).

---

## Features

- Upload and store `.txt`/`.md` documents
- Chunk documents and embed with OpenAI embeddings
- Retrieve top relevant chunks for a given question (vector similarity)
- Use OpenAI models to answer questions, strictly based on retrieved context
- Visualize chain-of-thought for each answer (nodes/edges)
- Store Q&A history in Postgres

---

## Setup Instructions

### Prerequisites

- Python 3.12+
- PostgreSQL
- OpenAI API Key

### Getting Started

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and update environment variables
cp .env.example .env
# Edit .env with your OpenAI key, Postgres URL, and models

# (If using Alembic migrations)
alembic upgrade head

uvicorn app.main:app --reload
