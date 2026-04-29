import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy import text

from db.database import engine

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

EMBED_MODEL = None


def pick_embedding_model():
    global EMBED_MODEL

    if EMBED_MODEL:
        return EMBED_MODEL

    models = client.models.list()

    for m in models:
        name = getattr(m, "name", "")
        methods = getattr(m, "supported_actions", []) or getattr(
            m, "supported_generation_methods", []
        )

        methods = [str(x).lower() for x in methods]

        if "embed" in "".join(methods):
            EMBED_MODEL = name
            return EMBED_MODEL

    raise Exception("No embedding model found")


def gemini_embedding(text_data: str):
    model_name = pick_embedding_model()

    response = client.models.embed_content(
        model=model_name,
        contents=text_data
    )

    return response.embeddings[0].values


def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS docs (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(3072)
            )
        """))

        conn.commit()


def ingest_text(content: str):
    emb = gemini_embedding(content)

    vector_str = "[" + ",".join(map(str, emb)) + "]"

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO docs(content, embedding)
            VALUES (:content, CAST(:embedding AS vector))
        """), {
            "content": content,
            "embedding": vector_str
        })

        conn.commit()


def retrieve(query: str):
    emb = gemini_embedding(query)

    vector_str = "[" + ",".join(map(str, emb)) + "]"

    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT content,
                   embedding <-> CAST(:embedding AS vector) AS distance
            FROM docs
            ORDER BY distance
            LIMIT 1
        """), {
            "embedding": vector_str
        }).fetchone()

    if not row:
        return "No relevant answer found"

    return row[0]