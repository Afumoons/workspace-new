# SESSION-STATE.md — Active Working Memory

This file is the agent's "HOT RAM" — survives compaction, restarts, distractions.

I will update this file **before** responding when there are important changes to task, context, decisions, or deadlines.

## Current Task
- **Wait-and-see mode** on `autonomous_trading_ai` after BTC MC hardening + XAG viability repair v3.
- Next candidate action (when Afu asks): XAG expression-context/session availability audit → XAG regime-gating inspection in cheap-prescreen path → one ultra-focused XAG-only rerun.
- `ATA2` (`C:\laragon\www\ATA2`) is in production-candidate phase with v1-compatible MT5/data/execution adapters. Doc at `docs/PRODUCTION_CANDIDATE_TASKLIST.md`.
- `autonomous_trading_ai/ui-front` Phase 1–3 operator UI is complete. Build + lint green. Remaining: final healthy-backend QA pass (Tasklist 4.3).

## Key Context
- User: Afu, Surabaya (UTC+7), full stack web dev + leveraged trader.
- Main trading project: `autonomous_trading_ai` at `C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai`
- ATA2 (next-gen): `C:\laragon\www\ATA2`
- Design reference library: `C:\laragon\www\awesome-design-md`
- Hermes reference: `C:\laragon\www\hermes-agent`
- Improvement track naming rule: always use `Track A / A2a` style, never plain "Phase 2".
- Workspace commit rule: Clio commits creates/edits; Afu handles deletes.
- Python dep rule: if low-risk dep is missing during approved local work, install directly and continue.

## Named Improvement Tracks (autonomous_trading_ai)
- **Track A** — Research Pipeline Improvement → ✅ COMPLETED (A1–A4)
- **Track B** — Live Monitoring & Attribution Improvement → ✅ COMPLETED (B1–B3)
- **Track C** — XAU Exit Hardening Improvement → ✅ COMPLETED (C1–C3, native partial TP deferred)

## Deferred / Backlog Items
- XAG expression-context audit (post-XAG viability repair v3 — wait and see first)
- 4000-bar / one-open-position-aware min-trade threshold matrix (remembered, not yet implemented)
- `save_pool()` atomicity audit (Bucket B2 in Claude findings triage)
- `avg_holding_bars` root calculation bug audit (Bucket B1)
- Monte Carlo session-aware slippage upgrade (low priority)
- Native partial TP engine support for Track C
- `autonomous_trading_ai` top-level + module docs alignment (requested, not yet completed)

## Pending Actions
- [ ] XAG wait-and-see: monitor next 2–3 research cycles before deciding to act
- [ ] ATA2 production-candidate: staged cron implementation in progress
- [ ] ui-front: healthy-backend QA pass (Tasklist 4.3)

## Recent Decisions
- 2026-04-09: ui-front Phase 1–3 implementation complete; build + lint green.
- 2026-04-08: ATA2 moved past MVP/alpha → production-candidate build stream started.
- 2026-04-06: Chose wait-and-see after BTC MC hardening + XAG viability repair v3.
- 2026-04-05: Family-aware governance implemented; XAG viability repair v3 done.
- 2026-04-04: Live decay detection v1 + concentration control v1+v2 implemented. `max_portfolio_drawdown_pct = 30.0` confirmed intentional.
- 2026-04-04: Same-bar ambiguity instrumented (diagnostic only, fill model unchanged).
- 2026-04-03: Tracks A/B/C all confirmed implemented to practical completion.

---
*Last updated: 2026-04-21*