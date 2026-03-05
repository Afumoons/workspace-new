import argparse
from pathlib import Path

import chromadb

DEFAULT_DB = Path("C:/Users/afusi/.openclaw/workspace/chroma_data")
DEFAULT_COLLECTION = "clio_memory"


def main():
    parser = argparse.ArgumentParser(description="Query local Chroma memory")
    parser.add_argument("query", help="Natural language query")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    client = chromadb.PersistentClient(path=str(Path(args.db).resolve()))
    col = client.get_or_create_collection(args.collection)

    res = col.query(query_texts=[args.query], n_results=args.k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    if not docs:
        print("No results.")
        return

    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
        src = (meta or {}).get("source", "unknown")
        print(f"\n[{i}] source={src} distance={dist}")
        print(doc[:500].replace("\n", " "))


if __name__ == "__main__":
    main()
