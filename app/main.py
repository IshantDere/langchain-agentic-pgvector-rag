from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, UploadRequest
from agents.agent import agent
from rag.rag_engine import init_db, ingest_text
import os

app = FastAPI(
    title="LangChain Agentic RAG API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "LangChain Agentic RAG Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload(req: UploadRequest):
    try:
        if not os.path.exists(req.path):
            raise HTTPException(status_code=404, detail="File not found")

        with open(req.path, "r", encoding="utf-8") as f:
            content = f.read()

        ingest_text(content)

        return {
            "status": "success",
            "message": "File ingested successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        })

        return {
            "status": "success",
            "output": result["messages"][-1].content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))