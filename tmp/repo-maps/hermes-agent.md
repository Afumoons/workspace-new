# Repo Map — hermes-agent

## Path
- `C:\laragon\www\hermes-agent`

## What it is
A large modular agent platform by Nous Research combining:
- core tool-calling agent runtime
- interactive CLI
- messaging gateway
- cron automation
- persistent session/memory systems
- ACP/editor integration
- plugin-based memory/providers
- RL / benchmark environments

## Mental model
This repo is closer to an **agent operating system / agent platform** than a simple chatbot app.

## Core architecture
### Runtime core
- `run_agent.py` — main AIAgent loop
- `model_tools.py` — tool discovery + orchestration
- `toolsets.py` — tool grouping/policy surface
- `agent/` — prompt, compression, caching, display, internal support modules
- `tools/` — actual tool implementations

### User interfaces
- `cli.py` — interactive TUI/REPL
- `hermes_cli/` — command entry, setup, config, auth, slash commands, skins
- `gateway/` — multi-platform messaging runtime
- `acp_adapter/` — ACP/editor integration

### Persistence & continuity
- `hermes_state.py` — SQLite + FTS5 session DB
- `plugins/memory/` — pluggable memory providers (e.g. Honcho)
- `skills/` — skill ecosystem

### Automation
- `cron/` — scheduled jobs with delivery routing

### Research / training
- `environments/` — Atropos/RL env integration
- `batch_runner.py`
- `trajectory_compressor.py`
- `tinker-atropos/`

### Distribution/docs
- `website/` — Docusaurus site
- `docs/` — additional docs/specs/migration docs
- `packaging/`

## Important entry points
- `hermes` → `hermes_cli.main:main`
- `hermes-agent` → `run_agent:main`
- `hermes-acp` → `acp_adapter.entry:main`

## Notable strengths
- modular tool registry
- profile-aware home/state isolation
- strong messaging gateway surface
- agent-native cron automation
- real session persistence/search
- pluggable memory model
- ambitious research + product hybrid architecture

## Important caveats
- repo is large; onboarding cost is high
- root hotspot files (`run_agent.py`, `cli.py`, `gateway/run.py`) are very large
- changes can have broad blast radius
- should be approached with explicit module boundaries in mind

## Why it matters to Clio
This repo is useful as a reference for:
- agent platform architecture
- tool registry design
- memory/session system ideas
- gateway + cron + ACP integration patterns
- operational legibility patterns worth emulating at workspace level

## What to imitate safely (without changing OpenClaw core)
- repo maps
- playbooks
- decision records
- validation/audit artifacts
- structured improvement registries
