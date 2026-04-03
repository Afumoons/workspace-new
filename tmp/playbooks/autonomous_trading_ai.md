# Playbook — autonomous_trading_ai

## Purpose
Working heuristics for helping on the trading project without re-deriving context from scratch.

## Current named improvement tracks
- Track A — Research Pipeline Improvement
- Track B — Live Monitoring & Attribution Improvement
- Track C — XAU Exit Hardening Improvement

Always refer to work using track + phase labels, not raw "Phase 2" language.

## Operational heuristics
- Prefer selective, measurable changes over broad gate loosening.
- Preserve honesty between:
  - implemented in code
  - validated in live/runtime behavior
- For broker/runtime issues, inspect artifacts before theorizing.
- For delete actions, Afu wants to handle the commit.
- For create/edit actions in workspace, Clio should commit.

## Current strategic lessons
- Track A should improve upstream candidate quality before loosening gates too much.
- Track B matters because operational observability and attribution can silently fail even when runtime seems healthy.
- Track C should prioritize time-stop + invalidation logic over generic exit-rule chasing.

## Useful project artifacts
- `autonomous_trading_ai/tmp/improvement-tracks.md`
- `autonomous_trading_ai/execution/strategy_live_stats.json`
- `autonomous_trading_ai/execution/unmatched_closed_deals.json`
- `autonomous_trading_ai/execution/pool_audit_trail.json`
- `autonomous_trading_ai/strategies/pool_state.json`
- `autonomous_trading_ai/logs/system.log`

## Decision reminders
- Do not assume file existence implies correctness.
- Distinguish between bootstrap file creation and actual data attribution.
- Distinguish between runtime artifact docs and source docs when committing.

## Pool-state decision rule
- Observe 3–5 research cycles after major pipeline changes.
- KEEP if pool remains informative and adaptive.
- PARTIAL RESET if stale/noisy candidates dominate but useful core remains.
- FULL RESET only if old pool clearly pollutes evolution and partial cleanup is insufficient.
