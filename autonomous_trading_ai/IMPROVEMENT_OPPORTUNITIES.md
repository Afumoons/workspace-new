# Improvement Opportunities – autonomous_trading_ai

Snapshot as of 2026-03-12 – potential future upgrades we discussed.

## 1. Daily PnL wiring (live MT5 → DailyState) **[IMPLEMENTED 2026-03-12]**

**Goal:** Make `daily_pnl`, `daily_return_pct`, and `trades_today` reflect *real* closed PnL from MT5, so daily limits (if enabled) are meaningful.

**Design outline (agreed):**
- Add `closed_trades_state.json` under `execution/` to track:
  - `last_check_time` (ISO-8601 UTC)
  - `processed_deal_ids` (list of MT5 deal tickets already accounted for)
- In `execution/live_monitor.update_live_stats()`:
  - Load `closed_trades_state`.
  - Call `mt5.history_deals_get(last_check_time, now)`.
  - Filter for *close* deals (profit/loss realized) and exclude processed tickets.
  - For each new deal:
    - `pnl = deal.profit`.
    - `equity_now = _get_account_equity()`.
    - Call `register_trade_pnl(pnl, equity_now)` from `execution/live_state_utils`.
    - Append `deal.ticket` to `processed_deal_ids`.
  - Update `last_check_time = now`, save state.

**Impact:**
- Enables accurate daily loss / trade counts.
- Makes `daily_limits_enabled` safe to turn on later.

---

## 2. AI-assisted research – Level 2 (lightweight)

**Goal:** Let Clio do periodic pattern analysis on the strategy pool (not every cycle), even on a free/limited API budget.

**Ideas:**
- Build a small script (e.g. `scripts/ai_review_pool.py`) that:
  - Loads a *compressed* view of top/bottom strategies (reusing `ai_research_input.json` or a smaller variant).
  - Sends a short summary to Clio via OpenClaw for:
    - High-level pattern detection (what works/fails, by regime/session/news).
    - Suggestions for:
      - Generator templates (e.g. more/less Ichimoku, add RSI/ATR filters).
      - Evaluation tweaks (e.g. slightly different thresholds per regime type).
  - Writes a short "research notes" file (markdown) with recommendations for future implementation.

**Constraints:**
- Run **rarely** (e.g. manual trigger or at most once per day).
- Keep prompts compact (top 10 + bottom 5, minimal fields).
- No runtime dependency for live trading.

---

## 3. Session-aware behavior

**Goal:** Use `session_pnl` from `strategy_explain` to shape which strategies are active in which sessions (Asia/London/NY) or to bias evolution.

**Ideas:**
- Extend promotion logic in `scheduler/main.py` to:
  - Prefer strategies with positive/robust performance in the session you care most about (e.g. London/NY for XAUUSDm).
- Future: introduce session filters in `job_execute_signals` so certain strategies are only allowed to trade in certain sessions.

---

## 4. Post-session auto journaling

**Goal:** Mirror your manual journaling workflow (journal-YYYY-MM.md) using live trade data.

**Ideas:**
- Build a script (e.g. `scripts/export_live_trades_for_journal.py`) that:
  - Reads MT5 history for a given day.
  - Produces a markdown/CSV chunk following `trading-journal-template.md`.
  - Optionally tags trades by regime, setup type (if inferable), and news context.

---

## 5. Regime_structured rollout

Right now, we still use the legacy `regime` label column in many places. We have a richer
`detect_regime_structured` implementation that could be adopted more widely.

**Future work:**
- Replace `add_regime_column` calls with `detect_regime_structured` and store additional
  regime fields (`regime_class`, `regime_type`, `regime_confidence`, `regime_hints`).
- Allow strategies to reference these richer fields in their rules.

---

## 6. Parameterized risk profiles

**Goal:** Make it easy to switch between conservative / normal / aggressive risk profiles.

**Ideas:**
- Add a high-level risk mode in `RiskConfig` (e.g. `risk_mode = "aggressive"`).
- Derive `max_risk_per_trade_pct`, `max_portfolio_drawdown_pct`, and daily limits from that mode.
- Later: use `regime_hints` to adapt risk per trade based on regime (within safe bounds).

---

This file is a parking lot for future improvements. None of these are required for the
current system to function; they are "potensi" upgrades we can revisit when you have
time/energy or when the current setup has run for a while and we want to push it further.
