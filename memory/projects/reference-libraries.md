# Reference Libraries

## awesome-design-md

### Path
- `C:\laragon\www\awesome-design-md`

### What it is
A curated content repository of `DESIGN.md` design-system documents inspired by public websites, meant to be copied into projects and used by AI/design agents as frontend style references.

### Mental model
This is not a runtime app/framework repo.
It is a design reference library.

### Core structure
- `README.md` — main catalog and purpose
- `CONTRIBUTING.md` — contribution rules and quality bar
- `design-md/<brand>/`
  - `DESIGN.md`
  - `preview.html`
  - `preview-dark.html`
  - `README.md`

### Standard per entry
Each design pack is expected to provide:
1. `DESIGN.md`
2. `preview.html`
3. `preview-dark.html`
4. `README.md`

### Required DESIGN.md sections
1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide

### Why it matters to Clio
Afu wants this repo remembered as a reusable design inspiration library for future web/frontend work.

### Best use cases
- choose a visual direction for a new web project
- borrow a design language for landing pages or dashboards
- reference typography, palette, spacing, and tone when generating UI
- use as DESIGN.md-style guidance for AI-assisted frontend building

### Caveats
- content-heavy repo, consistency can drift between DESIGN.md and preview files
- not a runtime codebase
- should be treated as inspiration/reference, not source-of-truth product implementation

### Recommended workflow when using it
1. choose 1–3 reference brands
2. read their `DESIGN.md`
3. extract:
   - color logic
   - typography hierarchy
   - component tone
   - spatial mood
4. adapt, do not blindly clone

## hermes-agent

### Path
- `C:\laragon\www\hermes-agent`

### What it is
A large modular agent platform by Nous Research combining:
- core tool-calling agent runtime
- interactive CLI
- messaging gateway
- cron automation
- persistent session/memory systems
- ACP/editor integration
- plugin-based memory/providers
- RL / benchmark environments

### Mental model
This repo is closer to an agent operating system / agent platform than a simple chatbot app.

### Core architecture
#### Runtime core
- `run_agent.py` — main AIAgent loop
- `model_tools.py` — tool discovery + orchestration
- `toolsets.py` — tool grouping/policy surface
- `agent/` — prompt, compression, caching, display, internal support modules
- `tools/` — actual tool implementations

#### User interfaces
- `cli.py` — interactive TUI/REPL
- `hermes_cli/` — command entry, setup, config, auth, slash commands, skins
- `gateway/` — multi-platform messaging runtime
- `acp_adapter/` — ACP/editor integration

#### Persistence & continuity
- `hermes_state.py` — SQLite + FTS5 session DB
- `plugins/memory/` — pluggable memory providers (e.g. Honcho)
- `skills/` — skill ecosystem

#### Automation
- `cron/` — scheduled jobs with delivery routing

#### Research / training
- `environments/` — Atropos/RL env integration
- `batch_runner.py`
- `trajectory_compressor.py`
- `tinker-atropos/`

#### Distribution/docs
- `website/` — Docusaurus site
- `docs/` — additional docs/specs/migration docs
- `packaging/`

### Important entry points
- `hermes` → `hermes_cli.main:main`
- `hermes-agent` → `run_agent:main`
- `hermes-acp` → `acp_adapter.entry:main`

### Notable strengths
- modular tool registry
- profile-aware home/state isolation
- strong messaging gateway surface
- agent-native cron automation
- real session persistence/search
- pluggable memory model
- ambitious research + product hybrid architecture

### Important caveats
- repo is large, onboarding cost is high
- root hotspot files (`run_agent.py`, `cli.py`, `gateway/run.py`) are very large
- changes can have broad blast radius
- should be approached with explicit module boundaries in mind

### Why it matters to Clio
This repo is useful as a reference for:
- agent platform architecture
- tool registry design
- memory/session system ideas
- gateway + cron + ACP integration patterns
- operational legibility patterns worth emulating at workspace level

### What to imitate safely
- repo maps
- playbooks
- decision records
- validation/audit artifacts
- structured improvement registries

### Safe adaptation philosophy
Adopt the benefits at the workspace/process level, not by changing OpenClaw core.
