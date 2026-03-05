import chromadb
from pathlib import Path

base = Path("C:/Users/afusi/.openclaw/workspace/chroma_data")
base.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(base))
col = client.get_or_create_collection("clio_memory")
col.upsert(
    ids=["bootstrap"],
    documents=["Chroma initialized for Clio Nova self-learning memory."],
    metadatas=[{"source": "setup", "ts": "2026-03-05"}],
)
print("OK", col.count(), str(base))
