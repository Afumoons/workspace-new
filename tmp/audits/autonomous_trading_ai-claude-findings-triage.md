# autonomous_trading_ai — Claude Findings Triage

## Purpose
Convert Claude's broad deep-analysis findings into a practical triage sheet:
- what is already proven,
- what is likely but not yet fully verified,
- what is already partially addressed,
- what should be prioritized next.

---

## Summary Judgment
Claude's findings appear directionally strong, but they mix together:
- true/probable bugs,
- performance bottlenecks,
- tuning opportunities,
- and architectural cleanup.

So not all findings should be treated as equally critical.

---

## Bucket A — Proven / effectively proven

### A1. `EXEC_MIN_TRADES=160` was too strict for BTC runtime execution
**Status:** Proven

**Why:**
- live manifest contained BTC entries
- pool contained BTC live-tier strategies
- direct runtime debug showed all BTC manifest candidates failed execution quality filter for the same reason: `trades < 160`

**Current state:**
- selective BTC execution thresholds already relaxed
- trade-count gates are now more execution-model-aware than before

**Recommended next step:**
- observe post-patch behavior for 1–3 cycles before further tuning

---

### A2. XAG had no runtime foothold because it had no pool foothold
**Status:** Proven

**Why:**
- `pool_state.json` inspection showed zero `XAGUSDm` records
- runtime set was empty for XAG because pool had no XAG strategies at all

**Current state:**
- selective XAG bootstrap path already added

**Recommended next step:**
- watch whether XAG begins appearing in `pool_state.json` as exploratory entries

---

### A3. Trade-count thresholds needed recalibration after switching to max-1-open-position-per-strategy
**Status:** Proven conceptually and operationally

**Why:**
- historical thresholds were shaped by an older execution regime where a strategy could effectively accumulate more entries
- current model caps each strategy to one open position at a time
- this makes older trade-count gates systematically stricter than intended

**Current state:**
- partial recalibration already implemented symbol-aware in scheduler execution logic
- future full matrix policy remains deferred but remembered

---

## Bucket B — Likely valid, high-signal, still worth direct audit

### B1. `avg_holding_bars = 0.0` bug / metric distortion
**Status:** Likely valid and high priority

**Why it matters:**
- directly affects risk-behavior interpretation
- can distort exit-fragility judgment and strategy scoring
- may have influenced earlier hard rejection logic historically

**Current state:**
- impact already softened because sub-1-bar holding is now warning-only, not hard reject
- but root calculation bug still appears worth auditing

**Priority:** High

---

### B2. `save_pool()` atomicity / state-integrity risk
**Status:** Needs direct source audit, but potentially high severity

**Why it matters:**
- non-atomic pool writes could corrupt or partially overwrite critical strategy state
- this would be a true integrity issue, not just a tuning issue

**Current state:**
- not yet verified in source during this triage

**Priority:** High if confirmed

---

### B3. degradation logic may be too aggressive
**Status:** Plausible / likely

**Why it matters:**
- could demote live strategies too easily
- may create a hidden churn problem where otherwise-valid strategies keep falling out of active status

**Current state:**
- not directly re-audited yet in this pass

**Priority:** Medium-high

---

### B4. news-behavior metrics always zero / not wired correctly
**Status:** Plausible / needs verification

**Why it matters:**
- if true, this hides strategy behavior around high-impact events
- undermines part of the strategy explanation and risk analysis layer

**Priority:** Medium-high

---

## Bucket C — Valid bottlenecks, but not first-order profit bugs

### C1. Ticket map rebuild overhead from `trades.log`
**Status:** Valid performance concern

**Why it matters:**
- repeated rebuilding can create avoidable file I/O overhead
- more relevant as execution volume grows

**Priority:** Medium

---

### C2. `strategy_has_open_position()` may cause too many MT5 checks
**Status:** Valid performance concern

**Why it matters:**
- execution loop cost grows with live strategy count
- may add latency and unnecessary broker/API interaction

**Priority:** Medium

---

### C3. Too many Chroma / ResearchMemory queries per research cycle
**Status:** Likely valid

**Why it matters:**
- can increase research cycle cost significantly
- may be worth batching/caching later

**Priority:** Medium

---

### C4. cheap prescreen may still be computationally non-trivial
**Status:** Plausible

**Why it matters:**
- it is cheaper than full robustness checks, but still a real backtest call
- if candidate volume grows, this may still become a noticeable bottleneck

**Priority:** Medium-low for now

---

## Bucket D — Already addressed or partially addressed

### D1. Canonical symbol/alias mismatch issues
**Status:** Partially addressed already

**What changed:**
- canonical alias paths improved for BTC and XAG
- research/update paths already save features canonically
- execution/runtime logic now better accounts for canonical forms

**Remaining risk:**
- still worth keeping an eye on symbol-specific paths, but the major alias problems have already been reduced

---

### D2. Track A research over-strictness
**Status:** Partially addressed already

**What changed:**
- cheap prescreen added
- dead-zone penalty added
- XAU playbooks added
- selective gate relaxation started
- trade-count logic now more execution-model-aware

**Remaining risk:**
- may still need another tuning round after observation

---

### D3. XAG starvation
**Status:** Addressed as an active intervention

**What changed:**
- selective XAG bootstrap path added

**Remaining risk:**
- still needs observation to confirm XAG actually gains foothold

---

## Bucket E — Highest ROI next actions

### E1. Audit `avg_holding_bars` calculation path
**Why:**
- high signal
- probably affects scoring/risk interpretation directly
- still unresolved at root level

### E2. Audit `save_pool()` write safety / atomicity
**Why:**
- if broken, this is a real integrity risk
- deserves certainty, not assumption

### E3. Observe BTC after threshold patch
**Why:**
- verify whether runtime now successfully produces viable BTC execution candidates
- confirm we fixed the real bottleneck rather than only the log wording

### E4. Observe XAG pool ingress after bootstrap patch
**Why:**
- confirm whether `XAGUSDm` begins appearing in `pool_state.json`
- if still zero, deeper generator/research logic may need attention

### E5. Review degradation logic after live observations
**Why:**
- avoid a hidden churn loop where active strategies are demoted too aggressively

---

## Bucket F — Lower priority / later cleanup

### F1. cache or memoize ticket-map rebuild path
### F2. reduce repeated MT5 open-position queries
### F3. reduce repeated ResearchMemory calls if research cost becomes noticeable
### F4. optimize cheap prescreen only if candidate volume materially rises further

---

## Practical conclusion
Claude's analysis was useful, but the right operational interpretation is:
- some findings are already proven and acted on,
- some are high-value hypotheses worth auditing next,
- some are performance cleanups rather than urgent profit blockers,
- and some have already been partially addressed by recent Track A / B / C work.

The most valuable next direct audits are:
1. `avg_holding_bars`
2. `save_pool()` integrity / atomicity
3. post-patch BTC behavior
4. post-bootstrap XAG ingress
