from fastapi import FastAPI
from app.schemas import ChatRequest, UploadRequest
from agents.agent import agent
from rag.rag_engine import init_db, ingest_text

app = FastAPI()


@app.get("/")
def root():
    return {"message": "LangChain Agentic RAG Running"}


@app.post("/upload")
async def upload(req: UploadRequest):
    try:
        init_db()

        with open(req.path, "r", encoding="utf-8") as f:
            content = f.read()

        ingest_text(content)

        return {
            "status": "success",
            "message": "File ingested successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


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
        return {
            "status": "error",
            "message": str(e)
        }