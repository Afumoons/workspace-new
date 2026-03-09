---
name: vector-memory
description: Chroma-backed long-term and semantic memory for the main Clio Nova agent and related tools. Use when storing or recalling user-specific episodic memories (preferences, decisions, habits) or searching semantic knowledge ingested into Chroma.
---

# Vector Memory Skill

This skill provides a Chroma-backed vector memory layer for Afu's agents.

## What This Skill Does

- Store **episodic memories** from conversations (user facts, preferences, decisions)
- Retrieve relevant episodic memories given a query (for use in prompts)
- Store **semantic knowledge** from longer docs into `agent_semantic`
- Search semantic knowledge for retrieval-augmented generation

Chroma server is expected at `http://localhost:8000`.

The core implementation lives in the workspace-level modules:

- `memory/vectorMemory.mjs` – main `VectorMemory` class
- `memory/embeddings.mjs` – OpenAI embedding helper (for real usage)

This skill mainly provides wrappers and usage guidance.

## Using VectorMemory

1. Import and initialize once at startup:

```js
import { VectorMemory } from "../../memory/vectorMemory.mjs";
import { embedText } from "../../memory/embeddings.mjs";

const memory = new VectorMemory({
  chromaUrl: "http://localhost:8000",
  embeddingFn: embedText,
});

await memory.init();
```

2. Store important user messages as episodic memory:

```js
await memory.storeMessage({
  userId: "afu",
  role: "user",
  text: userMessage,
  sessionId,
  source: surface, // "whatsapp" | "webchat" | ...
  importance: estimateImportance(userMessage),
});
```

3. Recall memories before answering:

```js
const recalled = await memory.recallEpisodic({
  userId: "afu",
  query: userMessage,
  k: 8,
  minImportance: 0.3,
});
```

4. Format for prompts:

```js
function formatMemoriesForPrompt(recalled) {
  if (!recalled.length) return "";

  const lines = recalled.map((m, i) => {
    const meta = m.metadata || {};
    const ts = meta.timestamp ?? "";
    return `- [${i + 1}] (${ts}) ${m.text}`;
  });

  return (
    "Relevant long-term memories about this user:\n" +
    lines.join("\n") +
    "\n\nUse these if they help; ignore if not relevant."
  );
}
```

## Simple Importance Heuristic

Use a cheap heuristic to gate what gets stored:

```js
function estimateImportance(text) {
  const lower = text.toLowerCase();
  if (lower.includes("remember") || lower.includes("my preference")) return 0.9;
  if (lower.length > 200) return 0.6; // long, likely meaningful
  return 0.4;
}
```

## References

- See `references/usage-notes.md` for additional patterns and maintenance tips (cleanup, archiving, semantic ingestion).
