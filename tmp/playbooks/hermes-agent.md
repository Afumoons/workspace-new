# Playbook — hermes-agent

## Purpose
Quick operating map for future work on or inspired by `C:\laragon\www\hermes-agent`.

## Mental framing
Treat Hermes as an **agent platform**, not a single chatbot repo.

## Read-first files for future work
1. `README.md`
2. `AGENTS.md`
3. `pyproject.toml`
4. `run_agent.py`
5. `model_tools.py`
6. `toolsets.py`
7. `hermes_state.py`
8. `gateway/run.py`
9. `hermes_cli/main.py`
10. `environments/README.md`

## Important boundaries
- `run_agent.py` = main loop
- `model_tools.py` = tool discovery/orchestration
- `toolsets.py` = capability packaging / policy surface
- `cli.py` + `hermes_cli/` = user-facing CLI product layer
- `gateway/` = messaging runtime
- `hermes_state.py` = continuity/session/search foundation
- `cron/` = scheduled automation
- `plugins/memory/` = memory provider abstraction
- `environments/` = RL/training/eval side

## High-value learnings to reuse conceptually
- strong operational legibility
- profile-aware state isolation
- structured session persistence/search
- explicit tool grouping
- auditability / observability surfaces
- platform-aware delivery and cron routing

## What NOT to do when taking inspiration
- do not try to recreate Hermes inside OpenClaw
- do not add framework-heavy abstractions just because Hermes has them
- do not touch OpenClaw core just to mimic Hermes architecture

## Safe adaptation philosophy
Adopt the benefits at the workspace/process level:
- repo maps
- playbooks
- decision records
- validation notes
- improvement registries
