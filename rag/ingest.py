from rag.rag_engine import init_db, ingest_text

init_db()

with open("data/sample.txt", "r", encoding="utf-8") as f:
    content = f.read()

ingest_text(content)

print("Data inserted successfully")