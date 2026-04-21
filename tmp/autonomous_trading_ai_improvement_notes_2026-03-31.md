# autonomous_trading_ai improvement notes — 2026-03-31

This file preserves two separate suggestion sets for later implementation discussion.

## A. Claude's recommendation set

### Core diagnosis
- Biggest bottleneck identified: `EXEC_MIN_TRADES = 200`
- Additional friction points: layered research gates, `avg_holding_bars` hard reject, specialist bootstrap problem, too-short history window, overly restrictive XAU generator parameterization.

### Claude's proposed changes
1. **Execution gate relaxation**
   - `EXEC_MIN_TRADES = 120`
   - `EXEC_MIN_WF_SHARPE = 0.65`
   - `EXEC_MAX_DD_PCT = 15.0`
   - `EXEC_MAX_CONSEC_LOSS = 18`
2. **Holding-bars gate change**
   - Treat `avg_holding_bars < 1.0` as possible false positive due to same-bar entry/exit accounting.
   - Suggested action: remove hard skip and downgrade to warning/debug note.
3. **Bootstrap path for new strategies**
   - Allow exploratory promotion for promising strategies even when `specialist_score == 0.0`, if other metrics (PF, WF Sharpe, MC, trades) are strong enough.
4. **Increase history depth**
   - `history_bars_default = 4000`
5. **Tune XAU generator**
   - Narrow / lower threshold sampling, especially trend thresholds.
   - Prefer more executable ranges for ATR/stop/target parameters.
6. **Underlying rationale**
   - Claude argued this is closer to large prop-firm practice: enough trade significance, but not unrealistically high trade counts for regime specialists.

---

## B. Clio's recommendation set

### Core diagnosis
- Current system likely over-filters valid specialists.
- Too many generated candidates are structurally too restrictive, leading to 0-trade or weak-performance outcomes.
- The immediate problem is less about writing artifacts and more about candidate quality + execution gate calibration.

### Clio's proposed changes
1. **Reduce `EXEC_MIN_TRADES` first**
   - High-priority first change because it is likely the largest single gate suppressing viable specialists.
2. **Tune XAU generator**
   - Reduce over-conditioning and overly high thresholds.
   - Lower the share of candidates that produce zero or negligible trades.
3. **Add bootstrap path for new strategies**
   - Do not require mature routing/specialist metadata before a candidate can become exploratory.
4. **Soften `avg_holding_bars` filter rather than removing it outright**
   - Convert hard reject into warning/penalty first.
   - Validate whether it is truly a calculation bug versus a valid anti-noise filter.
5. **Increase history carefully**
   - Consider 3000–4000 bars, but watch recency dilution / stale-regime effects.
6. **Do not loosen all gates simultaneously**
   - Avoid changing too many quality thresholds at once, or attribution becomes muddy.
7. **Preferred rollout order**
   - Step 1: lower `EXEC_MIN_TRADES`
   - Step 2: add exploratory bootstrap path
   - Step 3: tune XAU generator thresholds
   - Step 4: soften `avg_holding_bars`
   - Step 5: revisit DD / WF Sharpe thresholds only after measuring earlier changes
8. **Important caution**
   - Claude's high-level direction is good, but some statements about prop-firm norms and the certainty of the `avg_holding_bars` bug should be treated as hypotheses pending validation.

---

## C. Claude–Clio synthesis after follow-up discussion

### Convergence points
1. **Cheap pre-screen before full backtest / WF / Monte Carlo**
   - High-ROI addition.
   - Goal: reject obviously dead low-trade candidates early using a fast local sample before expensive validation.
2. **Family-memory / dead-zone penalty should likely be stronger**
   - The current `_memory_is_clearly_bad` mechanism exists, but may not yet be aggressive enough.
3. **Execution realism matters more than initially emphasized**
   - Claude highlighted a likely underestimation of XAU spread/cost realism in the current backtest assumptions.
   - If true, this biases PF/Sharpe/expectancy upward and contaminates strategy selection.

### Important divergence resolved
- Claude's revised position: relaxing gates alone is not enough; candidate quality must improve.
- Clio's position: root cause is candidate quality + realism, not just strict thresholds.
- Shared synthesis: **fix bugs / realism first, improve candidate quality second, relax gates selectively only after that.**

### Notable implementation-level insights from Claude follow-up
1. **`avg_holding_bars` may be a false-positive reject source**
   - If same-bar entry/exit legitimately results in `0` holding bars due to current indexing logic, then `avg_holding_bars < 1.0` should not remain a hard reject in its current form.
   - Agreed interpretation: at minimum, demote this from hard gate to warning/soft penalty unless the metric is reworked.
2. **Specialist bootstrap problem remains real**
   - New strategies may have insufficient routing/specialist metadata maturity and get blocked too early.
3. **Execution cost realism for XAU is potentially under-modeled**
   - If spread cost is materially understated, the backtest stack is learning from distorted economics.

### Clio's stance on risk framing
- These changes are **high-value / low-regret**, but not literally zero-risk.
- Softening `avg_holding_bars` can admit noisier candidates.
- Fixing cost realism can make the current pool look materially worse.
- Still worth doing, but should be framed as integrity fixes, not harmless tweaks.

### Recommended implementation order after synthesis

#### Phase 1 — Integrity / realism fixes
1. Rework or soften `avg_holding_bars < 1.0` hard reject.
2. Audit and fix XAU cost / spread realism in backtests.

#### Phase 2 — Pipeline efficiency
3. Add cheap pre-screen before full backtest + WF + Monte Carlo.
4. Strengthen family-memory / dead-zone penalization where justified.

#### Phase 3 — Candidate quality
5. Move toward explicit XAU playbooks (e.g. trend-down specialist, range fade, London breakout).
6. Reduce over-conditioning / too many rule clauses.
7. Anchor ATR/stop/target logic more tightly to XAU microstructure.

#### Phase 4 — Selective gate relaxation
8. Lower `EXEC_MIN_TRADES` selectively (e.g. bounded specialists first).
9. Consider increasing history bars to 3000–4000 with recency monitoring.
10. Revisit DD / WF Sharpe thresholds only after earlier phases are measured.

---

## Shared conclusion
Across the full discussion, the most credible leverage points are:
- execution trade-count gate is likely too strict for some specialists,
- new strategy bootstrap into exploratory tier is too hard,
- XAU generator produces too many low-activity / non-executable candidates,
- backtest realism / cost integrity may be understating true trading friction,
- cheap pre-screening can improve both compute efficiency and candidate quality.

## Next-session resume prompt
When continuing later:
- compare Claude set vs Clio set vs synthesis set,
- decide whether to begin with integrity fixes or candidate-quality improvements,
- prefer incremental patches with post-change measurement instead of a single broad loosening pass.
