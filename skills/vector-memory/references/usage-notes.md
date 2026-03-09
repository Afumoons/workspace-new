# Vector Memory Usage Notes

## Collections

- `agent_episodic` – episodic memories (conversation turns, preferences, decisions)
- `agent_semantic` – semantic knowledge (docs, notes, longer references)

## Episodic Memory Patterns

### Store

- Only store messages with `importance >= 0.2`.
- Prefer storing:
  - Explicit preferences ("I prefer", "I like", "remember that...")
  - Decisions and commitments
  - Stable facts about the user

### Recall

- Use the current user message as the query.
- Filter by `user_id` and a minimum importance (e.g. `0.3`).
- Retrieve 5–10 memories and format concisely.

## Semantic Knowledge Patterns

### Ingestion

- Chunk documents into ~1000 character pieces (with light sentence boundaries)
- Store with metadata:
  - `doc_id`
  - `chunk_index`
  - optional tags, e.g. `tags: ["openclaw", "trading", "playbook"]`

### Search

- Use `searchKnowledge(query, k, where)`.
- Filter by tags when possible to reduce noise.

## Maintenance / Cleanup

- Periodically prune low-importance, very old items from `agent_episodic`.
- For now, cleanup can be manual via small scripts or one-off queries.

## Integration Notes

- Chroma must be running at `http://localhost:8000`.
- Embeddings default to `text-embedding-3-large` via OpenAI.
- For offline/local setups, swap `embedText` implementation with a local embedding model.
