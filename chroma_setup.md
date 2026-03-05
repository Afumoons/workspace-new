# Chroma Setup (Local)

Status: ✅ configured by Clio Nova on 2026-03-05.

## What was set up
- Python virtual env: `.venv-chroma`
- Package installed: `chromadb==1.5.2`
- Persistent DB path: `chroma_data/`
- Bootstrap script: `scripts/init_chroma.py`
- Initial collection: `clio_memory`

## Quick commands (PowerShell)

```powershell
cd C:\Users\afusi\.openclaw\workspace
.\.venv-chroma\Scripts\python scripts\init_chroma.py
```

Run local Chroma HTTP server:

```powershell
cd C:\Users\afusi\.openclaw\workspace
.\.venv-chroma\Scripts\chroma run --path .\chroma_data --host 127.0.0.1 --port 8000
```

## Notes
- First run downloads embedding model cache to `%USERPROFILE%\.cache\chroma`.
- Use this as local vector memory backend for retrieval workflows.
