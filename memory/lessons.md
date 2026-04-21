# Lessons & Mistakes Log

Log significant mistakes, corrections, and lessons learned.
Periodically distill the important ones into MEMORY.md.

---

## 2026-04 Lessons

### [L-2026-04-01] Windows PowerShell `&&` separator — RECURRING
- **Lesson:** On this Windows/PowerShell host, `&&` is NOT a valid statement separator. Use `;` or separate exec calls.
- **Why it keeps happening:** Muscle memory from Linux/bash context.
- **Fix:** Before any chained shell command, mentally substitute `&&` → `;` or split into two calls.
- **Status:** Promoted to MEMORY.md + LEARNINGS.md. Treat as fixed workspace rule.

### [L-2026-04-02] `python -c` multiline in PowerShell
- **Lesson:** `python -c "...\n..."` with literal `\n` escapes fails with SyntaxError in PowerShell.
- **Fix:** Keep `python -c` bodies on one logical line with semicolons/comprehensions, or write to a temp file.

### [L-2026-04-03] Track naming convention
- **Lesson:** "Phase 2" references became ambiguous across multiple improvement streams. Always use full track + phase label: `Track A / A2a`, `Track B / B2`, etc.
- **Why it matters:** Without track prefix, references across sessions collide and lose meaning.

### [L-2026-04-04] Pool state reset decision rule
- **Lesson:** After major pipeline changes, do NOT reset pool_state immediately. Observe 3–5 research cycles first. Use KEEP / PARTIAL RESET / FULL RESET decision ladder.
- **Rationale:** Premature reset destroys useful evolutionary history.

### [L-2026-04-05] `avg_holding_bars < 1.0` was a false-positive hard gate
- **Lesson:** Same-bar entry/exit can legitimately produce `avg_holding_bars = 0` due to indexing. This was hard-rejecting valid strategies. Converted to warning-only.
- **Principle:** Hard gates on derived metrics should have validated root causes before they block candidates.

### [L-2026-04-06] `strategy_live_stats.json` silent attribution failures
- **Lesson:** Live stats stayed empty not because file creation failed, but because closed-deal attribution was mismatching MT5 identifiers vs stored ticket map.
- **Fix:** Broaden attribution fallbacks + reconcile from `execution/trades.log`.
- **Principle:** Empty files ≠ broken pipeline. Always check the attribution lineage.

### [L-2026-04-07] `max_portfolio_drawdown_pct = 30.0` is intentional
- **Lesson:** Do not treat this as a bug to "fix" to 25. The risk posture is deliberately aggressive. Upstream controls (selection quality → concentration → decay detection) are the real safety layer.
- **Principle:** Always confirm intent before "fixing" config values that look unusual.

### [L-2026-04-08] Low-risk Python deps → install directly, don't ask
- **Lesson:** If a task fails because a common local dep is missing (`pytest`, `pyarrow`, `apscheduler`, `chromadb`), install it and continue. Don't pause for a second approval prompt.
- **Scope:** Only for low-risk local execution deps during already-approved local work.

### [L-2026-04-09] ATA2 CLI verification drift
- **Lesson:** Docs recorded `ata2 demo --dry-run` as verification command but the CLI does not expose `--dry-run` on `demo`. Correct commands: `ata2 dry-run-demo` (end-to-end dry run) or `ata2 demo` (sample flow).
- **Principle:** Copy-paste verification commands from actual `--help` output, not from memory.

### [L-2026-04-10] `save_pool()` atomicity — unverified, still worth auditing
- **Lesson:** Non-atomic pool writes could corrupt strategy state silently. Not yet verified in source but flagged as Bucket B2 in Claude findings triage. Do not assume it's safe.

### [L-2026-04-11] Same-bar ambiguity is instrumented but not currently material
- **Lesson:** After rerunning 13 active live strategies, `same_bar_ambiguity_count = 0` across the sample. Instrumentation is in place for future monitoring. Not a current priority.

### [L-2026-04-12] Concentration in live manifest is implicit, not diversity-aware
- **Lesson:** Current live manifest ranks and takes top-N per symbol/timeframe — no regime diversity enforcement. BTC manifest observed 16/16 `ranging`, XAU 13/16 `trending_down`. Family metadata mostly `unknown` which weakens any cap logic.
- **Next step (deferred):** Add concentration diagnostics and optional regime/family caps once metadata quality improves.

---

## 2026-03 Lessons

### [L-2026-03-01] PowerShell `&&` (first occurrence)
- Logged 2026-03-27. Already covered above in April recurring pattern.

### [L-2026-03-02] WhatsApp notification module
- The final hop (autonomous_trading_ai → OpenClaw WhatsApp) was deliberately paused. Gateway HTTP wiring is complex. Not a mistake — a deliberate deferral.

### [L-2026-03-03] Agent memory architecture
- Pure file-based memory doesn't scale for semantic recall. Hybrid (files for rules + Chroma vectors for episodic/semantic) is the right architecture for this workspace.

---

*Review this file periodically. Promote recurring patterns or hard lessons to MEMORY.md.*