# Pre-Session Routine (Intraday Perps — XAU & BTC)

Run this before each trading session. Total time: ~10–15 minutes.

## 1) Environment Check (1–2 minutes)
- [ ] You are rested and not rushed.
- [ ] No urgent non-trading tasks competing for attention.
- [ ] Platform, internet, and charts working.

## 2) Higher-Timeframe Context (3–5 minutes)
- [ ] Check D1/H4 for **XAUUSD** and **BTCUSDT**:
  - Trend: up / down / messy
  - Key levels: major S/R, recent swing high/low.
- [ ] Mark key zones on intraday charts (H1/M15).
- [ ] Decide regime for each: Trend / Range / Mess.

Reference: `trading-playbook-xau-btc.md` and `trading-playbook-intraday-perps.md`.

## 3) Macro & Event Risk (2–3 minutes)
- [ ] Check economic calendar for the session:
  - Today’s high-impact events (CPI, FOMC, NFP, etc.).
  - Time windows to avoid unless explicitly planned.
- [ ] Note any strong risk-on/off sentiment (DXY, yields, indices).

Reference: `trading-scorecard-xau-btc.md` (Macro Alignment section).

## 4) Plan Candidate Setups (3–5 minutes)
For each instrument (XAU, BTC):
- [ ] Identify if Trend Pullback or Breakout–Retest is in play.
- [ ] Define rough plan:
  - Bias (long/short/flat).
  - Key entry zone.
  - Invalidation level.
  - Rough TP area (structure-based).
- [ ] Discard low-quality / unclear setups.

Reference: `trading-playbook-intraday-perps.md` (Valid Setups).

## 5) Risk & Limits (1–2 minutes)
- [ ] Confirm account size and **per-trade risk** (~1–1.5%).
- [ ] Confirm daily loss stop (3R or 3 losing trades).
- [ ] Confirm weekly loss stop (8R) if near.
- [ ] Decide max number of trades planned for this session.

## 6) First Trade Gate (10-second checklist)
Before each trade, also use:
- `perps_execution_checklist.md`
- `trading-scorecard-xau-btc.md` (Grade A/B/C decision)

Minimum:
- [ ] Regime clear.
- [ ] Setup matches allowed types.
- [ ] RR >= 1:1.8.
- [ ] Risk within limits.
- [ ] Emotional state = calm (no revenge/FOMO).

If any box fails → **no trade**.

## 7) Post-Session (10–15 minutes, once per day)
- [ ] Log each trade in `journal-2026-03.md` using `trading-journal-template.md`.
- [ ] Tag mistakes and write one improvement per trade.
- [ ] Note any recurring patterns (good or bad) for future system tweaks.

Optional: periodically ingest these files into Chroma (already wired via `scripts/chroma_ingest.py`) so I can query your past behavior and help refine the system.
