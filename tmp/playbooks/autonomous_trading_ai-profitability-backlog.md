# autonomous_trading_ai — Profitability backlog

Created: 2026-04-04 (Asia/Jakarta)

## Deferred items after priority (1)

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
