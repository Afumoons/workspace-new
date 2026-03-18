# SESSION-STATE.md — Active Working Memory

This file is the agent's "HOT RAM" — survives compaction, restarts, distractions.

I will update this file **before** responding when there are important changes to task, context, decisions, or deadlines.

## Current Task
- Designing and implementing an elite long-term memory architecture for Afu's OpenClaw setup (aligned with `elite-longterm-memory` skill), using **Chroma** as the warm vector store.

## Key Context
- User name: Afu (located in Surabaya, UTC+7).
- Vector DB: Chroma is already running and wired via `vector-memory` skill.
- Existing long-term memory:
  - `MEMORY.md` as curated long-term.
  - `memory/` folder for daily logs and other notes.
- Hard boundary: no harm to person, animal, data, or Clio Nova.

## Pending Actions
- [ ] Tighten structure inside `memory/` to match projects/people/decisions/lessons/preferences layout **without** breaking existing notes.
- [ ] Establish a weekly "memory hygiene" checklist based on elite-longterm-memory (to be added to HEARTBEAT or a separate note).
- [ ] Start using this file (SESSION-STATE.md) consistently for multi-step work.

## Recent Decisions
- Adopt elite-longterm-memory architecture where it improves clarity and durability, but keep Chroma as the warm store (no LanceDB).
- Treat skills like `elite-longterm-memory` and `skill-vetter` as **SOPs**, not auto-executing code.

---
*Last updated: 2026-03-16T12:39:00Z*
