# Decision Record — Workspace Operational Legibility

## Decision
Adopt a lightweight Hermes-inspired workspace discipline without modifying OpenClaw core.

## Why
Hermes demonstrates strong practical benefits from:
- clear module legibility
- persistent operational notes
- audit surfaces
- structured continuity across sessions

We want the benefits without creating update friction or maintaining a fork of OpenClaw.

## Chosen implementation
Use workspace-local files under `tmp/` for:
- repo maps
- playbooks
- decision records
- validations/audits
- improvement registries

## Explicit non-goals
- no OpenClaw core modifications for this pattern
- no custom replacement session DB
- no custom framework/plugin layer built on top of OpenClaw
- no update-hostile changes

## Expected benefits
- faster re-entry into large repos
- lower context loss
- clearer project-specific heuristics
- better auditability of why decisions were made
- more durable long-task continuity

## Initial artifacts created
- `tmp/repo-maps/awesome-design-md.md`
- `tmp/repo-maps/hermes-agent.md`
- `tmp/playbooks/autonomous_trading_ai.md`
- `tmp/playbooks/hermes-agent.md`
- `tmp/decision-records/workspace-operational-legibility.md`
