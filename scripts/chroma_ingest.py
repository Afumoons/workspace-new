import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone

import chromadb

DEFAULT_DB = Path("C:/Users/afusi/.openclaw/workspace/chroma_data")
DEFAULT_ROOT = Path("C:/Users/afusi/.openclaw/workspace")
DEFAULT_COLLECTION = "clio_memory"
DEFAULT_GLOBS = [
    "memory/*.md",              # daily notes + working-buffer
    "MEMORY.md",                # curated long-term memory
    "PROACTIVE_TASKS.md",       # proactive daily responsibilities
    "USER.md",                  # user profile and preferences
    "SESSION-STATE.md",         # proactive-agent working memory (WAL)
    "HEARTBEAT.md",             # heartbeat checklist
    ".learnings/*.md",          # self-improvement logs
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150):
    text = text.strip()
    if not text:
        return []
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        j = min(n, i + chunk_size)
        chunks.append(text[i:j])
        if j == n:
            break
        i = max(i + 1, j - overlap)
    return chunks


def stable_id(path: Path, idx: int, chunk: str) -> str:
    h = hashlib.sha1(chunk.encode("utf-8")).hexdigest()[:16]
    rel = str(path).replace("\\", "/")
    return f"{rel}::c{idx}::{h}"


def collect_files(root: Path, patterns: list[str]) -> list[Path]:
    out = []
    for pat in patterns:
        out.extend(root.glob(pat))
    uniq = sorted({p.resolve() for p in out if p.is_file()})
    return uniq


def main():
    parser = argparse.ArgumentParser(description="Ingest markdown/text notes into Chroma")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Chroma persistent directory")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Workspace root")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--glob", action="append", dest="globs", help="File glob relative to --root")
    parser.add_argument("--chunk-size", type=int, default=1200)
    parser.add_argument("--overlap", type=int, default=150)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    db = Path(args.db).resolve()
    db.mkdir(parents=True, exist_ok=True)

    globs = args.globs if args.globs else DEFAULT_GLOBS

    client = chromadb.PersistentClient(path=str(db))
    col = client.get_or_create_collection(args.collection)

    files = collect_files(root, globs)
    if not files:
        print("No files matched.")
        return

    ids, docs, metas = [], [], []
    now = datetime.now(timezone.utc).isoformat()

    for f in files:
        rel = f.relative_to(root)
        text = read_text(f)
        for idx, ch in enumerate(chunk_text(text, args.chunk_size, args.overlap)):
            ids.append(stable_id(rel, idx, ch))
            docs.append(ch)
            metas.append({
                "source": str(rel).replace("\\", "/"),
                "chunk": idx,
                "updated_at": now,
            })

    col.upsert(ids=ids, documents=docs, metadatas=metas)
    print(f"Ingested {len(ids)} chunks from {len(files)} files into '{args.collection}'.")


if __name__ == "__main__":
    main()
