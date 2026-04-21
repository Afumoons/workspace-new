# autonomous_trading_ai

## Purpose
Working memory and durable notes for the `autonomous_trading_ai` project.

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

## Profitability backlog
1. Deep audit correlation/concentration control
   - Status: audited on 2026-04-04.
   - Findings:
     - Structural deduplication exists in `strategies/pool.py`, but it only removes exact logic clones.
     - Inactive pruning is family-aware, but live pool / live manifest selection is not diversity-aware.
     - `live_manifest.py` ranks by status + specialist_score + wf + score, then takes top-N per symbol/timeframe.
     - Current manifest concentration is high:
       - BTC live manifest: 16/16 best_regime=`ranging`
       - XAU live manifest: 13/16 best_regime=`trending_down`
     - Family metadata is currently mostly `unknown`, which weakens family-based concentration controls unless payload enrichment is improved.
   - Suggested next substeps:
     - add concentration diagnostics first (regime mix, family mix, duplicate wf/score clusters)
     - consider manifest caps per best_regime / family once metadata quality is improved
     - optionally penalize near-duplicate active candidates beyond exact structural fingerprint matches
2. Add explicit guard for exploratory fallback
   - Current question: should fallback keep-best exploratory be allowed when best edge is still negative?
   - Candidate guard: require best_edge >= 0 (or small tolerated floor) before fallback survives.
3. Analyze and instrument same-bar ambiguity in backtests
   - Detect candles where both SL and TP are touched.
   - Measure how much pessimistic SL-first resolution changes strategy ranking.
   - Decide whether to keep pessimistic mode, add diagnostics only, or implement neutral heuristic.
4. Design proactive live decay detection
   - Start with soft alerts / downgrade suggestions, not immediate auto-kill.
   - Candidate metrics: rolling live PnL, hit rate drift, drawdown acceleration, expectancy decay.
5. Monte Carlo upgrade assessment
   - Evaluate whether session-aware / regime-aware slippage modeling would materially improve robustness ranking.
   - Lower priority than threshold audit, fallback guard, same-bar ambiguity, and decay detection.

## Account/baseline guard backlog
### Implemented
- Phase 1: account identity switch guard in `execution/live_monitor.py`
  - tracks account identity (`login`, `server`, `currency`, `company`)
  - detects account switch via login/server mismatch
  - refreshes baseline automatically on account switch
  - resets daily state and closed-trade bookkeeping
  - adds warmup cycles to skip circuit breaker briefly after baseline refresh
  - records `baseline_created_at`, `warmup_cycles_remaining`, `last_baseline_reason`

### TODO — Phase 2
- Add abnormal equity-shock detection even when account identity is unchanged.
- Heuristic candidates:
  - very large equity drop/jump vs prior peak or recent sample
  - large balance/equity discontinuity not explained by recently processed closed deals
  - optional deposit/withdraw vs trade-PnL distinction when MT5 data allows it
- On anomaly:
  - do NOT disable live-tier strategies immediately
  - re-anchor baseline safely
  - log explicit anomaly reason

### TODO — Phase 3
- Add persistent disable metadata to pool records, e.g.:
  - `disabled_reason`
  - `disabled_at`
  - `disabled_context`
- Add baseline-refresh metadata / audit trail.
- Optionally send operator notification on auto baseline refresh / anomaly refresh.
- Consider manual operator command/script to force baseline refresh cleanly.
