import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from rag.rag_engine import retrieve

load_dotenv()

model = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


def rag_tool(query: str):
    """Search internal knowledge base using RAG."""
    return retrieve(query)


agent = create_react_agent(
    model=model,
    tools=[rag_tool],
    prompt="You are a helpful AI assistant."
)