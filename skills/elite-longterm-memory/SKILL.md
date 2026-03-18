The ultimate memory system for AI agents. Combines 6 proven approaches into one bulletproof architecture.

Never lose context. Never forget decisions. Never repeat mistakes.

## Architecture Overview

┌─────────────────────────────────────────────────────────────────┐
│ ELITE LONGTERM MEMORY                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  HOT RAM    │    │ WARM STORE  │    │ COLD STORE  │         │
│  │             │    │             │    │             │         │
│  │ SESSION-    │    │  LanceDB    │    │  Git-Notes  │         │
│  │ STATE.md    │    │  Vectors    │    │ Knowledge   │         │
│  │             │    │             │    │  Graph      │         │
│  │ (survives   │    │ (semantic   │    │ (permanent  │         │
│  │ compaction) │    │  search)    │    │ decisions)  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                │
│          └────────────────┬────────────────┘                   │
│                           ▼                                    │
│                     ┌─────────────┐                            │
│                     │  MEMORY.md  │  ← Curated long-term       │
│                     │  + daily/   │    (human-readable)        │
│                     └─────────────┘                            │
│                           │                                    │
│                           ▼                                    │
│                     ┌─────────────┐                            │
│                     │ SuperMemory │  ← Cloud backup (optional) │
│                     │    API      │                            │
│                     └─────────────┘                            │
│                                                                │
└─────────────────────────────────────────────────────────────────┘

## The 6 Memory Layers

### Layer 1: HOT RAM (SESSION-STATE.md)

From: bulletproof-memory

Active working memory that survives compaction. Write-Ahead Log protocol.

Example structure:

```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
[What we're working on RIGHT NOW]

## Key Context
- User preference: ...
- Decision made: ...
- Blocker: ...

## Pending Actions
- [ ] ...

## Recent Decisions
- ...

---
*Last updated: [timestamp]*
```

Rule: Write BEFORE responding. Triggered by user input, not agent memory.

### Layer 2: WARM STORE (LanceDB Vectors)

From: lancedb-memory

Semantic search across all memories. Auto-recall injects relevant context.

Examples:

```bash
# Auto-recall (happens automatically)
memory_recall query="project status" limit=5

# Manual store
memory_store text="User prefers dark mode" category="preference" importance=0.9
```

### Layer 3: COLD STORE (Git-Notes Knowledge Graph)

From: git-notes-memory

Structured decisions, learnings, and context. Branch-aware.

Examples:

```bash
# Store a decision (SILENT - never announce)
python3 memory.py -p $DIR remember '{"type":"decision","content":"Use React for frontend"}' -t tech -i h

# Retrieve context
python3 memory.py -p $DIR get "frontend"
```

### Layer 4: CURATED ARCHIVE (MEMORY.md + daily/)

From: OpenClaw native

Human-readable long-term memory. Daily logs + distilled wisdom.

Example layout:

```text
workspace/
├── MEMORY.md        # Curated long-term (the good stuff)
└── memory/
    ├── 2026-01-30.md  # Daily log
    ├── 2026-01-29.md
    └── topics/        # Topic-specific files
```

### Layer 5: CLOUD BACKUP (SuperMemory) — Optional

From: supermemory

Cross-device sync. Chat with your knowledge base.

```bash
export SUPERMEMORY_API_KEY="your-key"
supermemory add "Important context"
supermemory search "what did we decide about..."
```

### Layer 6: AUTO-EXTRACTION (Mem0) — Recommended

From: supermemory / mem0

Automatic fact extraction from conversations; reduces token usage.

```bash
npm install mem0ai
export MEM0_API_KEY="your-key"
```

```js
const { MemoryClient } = require('mem0ai');
const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

// Conversations auto-extract facts
await client.add(messages, { user_id: "user123" });

// Retrieve relevant memories
const memories = await client.search(query, { user_id: "user123" });
```

Benefits:

- Auto-extracts preferences, decisions, facts
- Deduplicates and updates existing memories
- 80% reduction in tokens vs raw history
- Works across sessions automatically

## Quick Setup

### 1. Create SESSION-STATE.md (Hot RAM)

Example initialization:

```bash
cat > SESSION-STATE.md << 'EOF'
# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — survives compaction, restarts, distractions.

## Current Task
[None]

## Key Context
[None yet]

## Pending Actions
- [ ] None

## Recent Decisions
[None yet]

---
*Last updated: [timestamp]*
EOF
```

### 2. Enable LanceDB (Warm Store)

Example openclaw.json fragment:

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```

Adapt paths/providers to your setup (e.g., Chroma instead of LanceDB).

### 3. Initialize Git-Notes (Cold Store)

```bash
cd ~/clawd
# if not already a git repo
git init
python3 skills/git-notes-memory/memory.py -p . sync --start
```

### 4. Verify MEMORY.md Structure

Ensure you have:

- `MEMORY.md` in workspace root
- `memory/` folder for daily logs

```bash
mkdir -p memory
```

### 5. (Optional) Setup SuperMemory

```bash
export SUPERMEMORY_API_KEY="your-key"
# Add to your shell rc file for persistence
```

## Agent Instructions

### On Session Start

- Read `SESSION-STATE.md` — this is your hot context
- Run `memory_search` for relevant prior context
- Check `memory/YYYY-MM-DD.md` for recent activity

### During Conversation

- User gives concrete detail? → Write to `SESSION-STATE.md` BEFORE responding
- Important decision made? → Store in Git-Notes (SILENTLY)
- Preference expressed? → `memory_store` with `importance=0.9`

### On Session End

- Update `SESSION-STATE.md` with final state
- Move significant items to `MEMORY.md` if worth keeping long-term
- Create/update daily log in `memory/YYYY-MM-DD.md`

### Memory Hygiene (Weekly)

- Review `SESSION-STATE.md` — archive completed tasks
- Check LanceDB (or your vector DB) for junk: `memory_recall query="*" limit=50`
- Clear irrelevant vectors: `memory_forget id=...`
- Consolidate daily logs into `MEMORY.md`

## The WAL Protocol (Critical)

Write-Ahead Log: **write state BEFORE responding, not after.**

| Trigger               | Action                                             |
|-----------------------|-----------------------------------------------------|
| User states preference| Write to `SESSION-STATE.md` → then respond          |
| User makes decision   | Write to `SESSION-STATE.md` → then respond          |
| User gives deadline   | Write to `SESSION-STATE.md` → then respond          |
| User corrects you     | Write to `SESSION-STATE.md` → then respond          |

Rationale: If you respond first and crash/compact before saving, context is lost.
WAL ensures durability.

## Example Workflow

User: "Let's use Tailwind for this project, not vanilla CSS"

Agent (internal):

1. Write to `SESSION-STATE.md`: "Decision: Use Tailwind, not vanilla CSS"
2. Store in Git-Notes: decision about CSS framework
3. `memory_store`: "User prefers Tailwind over vanilla CSS" with `importance=0.9`
4. THEN respond: "Got it — Tailwind it is..."

## Maintenance Commands (Examples)

```bash
# Audit vector memory
memory_recall query="*" limit=50

# Clear all vectors (nuclear option)
rm -rf ~/.openclaw/memory/lancedb/
openclaw gateway restart

# Export Git-Notes
python3 memory.py -p . export --format json > memories.json

# Check memory health
du -sh ~/.openclaw/memory/
wc -l MEMORY.md
ls -la memory/
```

Use destructive commands like `rm -rf` **with extreme caution** and only when you fully understand the impact.

## Why Memory Fails

Understanding common failure modes helps you fix them:

| Failure Mode             | Cause                                     | Fix                                |
|--------------------------|-------------------------------------------|------------------------------------|
| Forgets everything       | `memory_search` disabled                  | Enable + add OpenAI key           |
| Files not loaded         | Agent skips reading memory                | Add to `AGENTS.md` rules          |
| Facts not captured       | No auto-extraction                        | Use Mem0 or manual logging        |
| Sub-agents isolated      | Don't inherit context                     | Pass context in spawn task prompt |
| Repeats mistakes         | Lessons not logged                        | Write to `memory/lessons.md`      |

## Solutions (Ranked by Effort)

### 1. Quick Win: Enable `memory_search`

If you have an OpenAI key, enable semantic search over your memory files.

### 2. Recommended: Mem0 Integration

Auto-extract facts from conversations; reduce token usage.

```bash
npm install mem0ai
```

```js
const { MemoryClient } = require('mem0ai');
const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

// Auto-extract and store
await client.add([
  { role: "user", content: "I prefer Tailwind over vanilla CSS" }
], { user_id: "ty" });

// Retrieve relevant memories
const memories = await client.search("CSS preferences", { user_id: "ty" });
```

### 3. Better File Structure (No Extra Dependencies)

Example structure:

```text
memory/
├── projects/
│   ├── strykr.md
│   └── taska.md
├── people/
│   └── contacts.md
├── decisions/
│   └── 2026-01.md
├── lessons/
│   └── mistakes.md
└── preferences.md
```

Keep `MEMORY.md` as a compact summary (<5KB) and link to detailed files.

## Immediate Fixes Checklist

| Problem                  | Fix                                      |
|--------------------------|------------------------------------------|
| Forgets preferences      | Add `## Preferences` section to MEMORY.md|
| Repeats mistakes         | Log every mistake to `memory/lessons.md`|
| Sub-agents lack context  | Include key context in spawn task prompt |
| Forgets recent work      | Strict daily file discipline             |
| Memory search not working| Check `OPENAI_API_KEY` and config        |

## Troubleshooting

- Agent keeps forgetting mid-conversation:
  - `SESSION-STATE.md` not being updated. Check WAL protocol.

- Irrelevant memories injected:
  - Disable overly aggressive auto-capture; increase `minImportance`.

- Memory too large, slow recall:
  - Run hygiene: clear old vectors, archive/compress daily logs.

- Git-Notes not persisting:
  - Run `git notes push` to sync with remote.

- `memory_search` returns nothing:
  - Check OpenAI API key
  - Verify memorySearch is enabled in `openclaw.json`

## Related Skills / References

- bulletproof-memory: https://clawdhub.com/skills/bulletproof-memory
- lancedb-memory:     https://clawdhub.com/skills/lancedb-memory
- git-notes-memory:   https://clawdhub.com/skills/git-notes-memory
- memory-hygiene:     https://clawdhub.com/skills/memory-hygiene
- supermemory:        https://clawdhub.com/skills/supermemory

Built by @NextXFrontier / NextFrontierBuilds — part of the Next Frontier AI toolkit.
