# Trading Playbook — XAUUSD & BTCUSD (Prop-Style)

(Imported from previous workspace on 2026-03-05; adapt as needed for current capital and venues.)

## 1) Core Principles
- Survive first, profit second.
- Risk consistency beats prediction accuracy.
- No setup = no trade.
- If macro and technical conflict strongly: reduce size 50% or skip.

## 2) Risk Engine (Hard Rules)
- Risk per trade: 0.25%–0.75% (max 1.0%)
- Daily max drawdown: 1.5%–2.0%
- Weekly max drawdown: 4.0%–5.0%
- Max correlated exposure: cap combined XAU+BTC risk
- No martingale, no revenge trading, no SL widening after entry

## 3) Position Sizing Formula
1. Define invalidation-based SL distance
2. ATR-adjusted SL check (avoid too tight stop in high vol)
3. Position size = (Account Equity × Risk%) / SL distance value

## 4) Market Regime Model
### Regime states
- Trend (continuation favored)
- Range (mean reversion or breakout only at range edges)
- Transition (size down / selective)

### Confirmation blocks
- Structure: HH/HL or LH/LL (daily first)
- Momentum: RSI context + candle structure
- Volatility: ATR rising/falling

## 5) XAUUSD Playbook (Gold)
### Best-fit strategy
Hybrid Trend Pullback + Macro Event Filter

### Bias framework
- Primary: Daily structure + EMA20/EMA50
- Confirmation: H4/H1 pullback reaction at key level

### Entry conditions (long example)
- Daily above EMA20 with bullish structure
- Pullback into support / demand / EMA zone
- Rejection candle + reclaim intraday structure
- Risk-reward >= 1:2 preferred

### Avoid trading when
- High-impact US event window (30–60 min pre/post) unless setup is exceptional
- Violent DXY + real yield spike against position

## 6) BTCUSD Playbook
### Best-fit strategy
Regime Breakout/Continuation with Volatility Switch

### Bias framework
- Trend mode: price above D1 EMA20 and EMA20 slope up
- Defensive/bear mode: below EMA20 with failed reclaims

### Entry conditions
- Breakout + close above/below range on expansion
- Prefer retest hold/fail entries over first impulse chase
- ATR-based stop mandatory (BTC volatility)

### Avoid trading when
- Choppy compression without directional expansion
- Structure and momentum conflict on daily

## 7) Daily Workflow (07:00 WIB)
1. Macro Briefing (separate)
2. Technical Briefing (separate)
3. Setup grading (A/B/C)
4. Trade plan: bias, entry, SL, TP1, TP2, invalidation
5. Risk note + execution constraints

## 8) Setup Grades
- Grade A: regime aligned + level quality high + trigger clean + RR>=1:2
- Grade B: minor weakness in one component; reduced size
- Grade C: conflict/noise; skip unless compelling catalyst

## 9) Execution Guardrails
- Max 1–2 high-quality ideas per instrument/day
- If first trade loses and market becomes noisy: stop for session
- Never force trade to "recover"

## 10) Journal Fields (minimum)
- Instrument, setup grade, regime, catalyst
- Entry/SL/TP, planned R multiple, actual R
- Mistake tags: early entry, no trigger, oversized risk, news chase
- Improvement action for next session
