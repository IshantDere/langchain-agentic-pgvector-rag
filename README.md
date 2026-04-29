# LangChain Agentic RAG with Gemini + PGVector + FastAPI

A production-ready AI project that combines **LangChain Agents**, **Google Gemini Embeddings**, **PostgreSQL PGVector**, **FastAPI**, and **Docker Compose** to build an intelligent Retrieval-Augmented Generation (RAG) system.

---

## Overview

This project demonstrates how to build a real-world AI assistant that can:

- Search and retrieve custom knowledge from documents
- Use vector embeddings for semantic similarity search
- Respond intelligently using a LangChain ReAct Agent
- Run inside Docker containers
- Expose REST APIs using FastAPI
- Scale as a production-ready backend

---

## Tech Stack

- Python
- FastAPI
- LangChain
- LangGraph
- Google Gemini Embeddings
- Groq LLM
- PostgreSQL
- PGVector
- Docker Compose

---

## Features

- LangChain ReAct Agent
- Tool calling with custom RAG tool
- Semantic search using PGVector
- Gemini embeddings integration
- FastAPI REST APIs
- Dockerized deployment
- Clean modular architecture
- Shell automation scripts
- Easy local setup
- Resume-ready production project

# key points

- After both the containers are running:
- First do run bash load.sh
- then run bash test.sh

---

# Project Structure

```bash
langchain-agentic-rag/
│── app/
│   ├── main.py
│   ├── schemas.py
│
│── agents/
│   └── agent.py
│
│── rag/
│   ├── rag_engine.py
│   ├── ingest.py
│
│── db/
│   └── database.py
│
│── data/
│   └── sample.txt
│
│── tests/
│   └── test.sh
│
│── load.sh
│── run.sh
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── .env
│── README.md