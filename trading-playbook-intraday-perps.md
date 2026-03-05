# Intraday Perps Playbook — XAU & BTC (Small Account)

**Context:** IDR ~100k starting capital, aggressive profile, futures allowed. Objective: skill + process first, profit second.

## 1) Instruments & Sessions
- Trade only: **XAUUSD**, **BTCUSDT** (high-liquidity perps/CFDs on your venues).
- Focus sessions (WIB):
  - London open window
  - US session / London–US overlap
- Avoid low-liquidity dead zones and major event minutes unless explicitly planned.

## 2) Leverage & Risk (Hard Caps)
- Per-trade risk: **~1%** of account (max 1.5%).
- Leverage (guideline):
  - **Scalp:** 5–10x
  - **Intraday:** 3–5x
- Daily loss stop: **3R** or **3 losing trades** (whichever first).
- Weekly loss stop: **8R**; if hit, pause and review.
- Never widen SL after entry. No martingale, no revenge.

## 3) Top-Down Bias Process (5 minutes)
1. **Higher TF check (H1/H4/D1)**
   - Is market in **trend / range / mess**?
   - Simple rule-of-thumb:
     - Trend up: price above EMA20, structure HH/HL.
     - Trend down: price below EMA20, structure LH/LL.
     - Chop: unclear / frequent flips.
2. **Mark key levels**
   - Prior high/low, clear S/R zones, VWAP/POC equivalents if used.
3. Decide bias:
   - **With trend** only, unless very clean range edge setup.

## 4) Valid Setups (Only Trade These)

### A. Trend Pullback (Primary)
For both XAU & BTC.

**Checklist:**
- Higher TF trend clear (HH/HL or LH/LL; EMA20 aligned).
- Price pulls back into marked level / zone (S/R, demand/supply, EMA cluster).
- Rejection + confirmation candle (e.g. pin bar, engulfing, strong close back with trend).
- Space to target: RR >= 1:1.8 (prefer 1:2+).

**Entry:**
- After confirmation candle close near level.
- SL: beyond structure / wick (not arbitrary pips).
- TP: structure-based (prior swing, measured move) with at least 2R potential.

### B. Breakout–Retest (Secondary)

**Checklist:**
- Clear range or consolidation visible.
- Strong breakout with close outside range + higher volume/volatility.
- Pullback to broken level and **hold** (no immediate rejection back inside range).
- Confirmation candle in breakout direction.

**Entry:**
- After retest confirmation.
- SL: beyond retest low/high.
- TP: next obvious level, 2R+ preferred.

### Avoid (No-Trade)
- Choppy micro-structure with no clear trend.
- Directly into major scheduled news (CPI, FOMC, NFP) unless explicitly trading the event.
- When tired, tilted, or forced to "make back" losses.

## 5) Position Sizing (Simple Formula)
1. Determine SL distance (in dollars or points).
2. Decide **risk per trade** (e.g. 1% of equity).
3. Position size = (Account Equity × Risk%) / SL distance.
4. Adjust size down if:
   - Volatility extreme (ATR spike).
   - Correlated exposure (XAU + BTC both risk-on/off).

## 6) Execution Rules
- 1–2 quality trades per instrument per day max.
- If first trade is a clean setup and loses **without mistake**: OK to take one more.
- If you tag a trade as **impulsive / off-plan**, count it as 2 strikes.
- After daily stop hit: stop for day. Review journal.

## 7) Management Rules
- At **+1R**:
  - Take partial (e.g. 30–50%) or at least move SL closer to break-even.
- At **key structure** (prior high/low or major level):
  - Decide: scale out more or tighten SL.
- Never let a +2R unrealized winner turn into a full loser.

## 8) Pre-Trade Checklist (10 seconds)
- [ ] Trend regime clear?
- [ ] Setup type = Trend Pullback or Breakout–Retest?
- [ ] Clean level + confirmation candle?
- [ ] RR >= 1:1.8?
- [ ] Risk <= 1–1.5% and within daily/weekly limits?
- [ ] Emotional state: calm, no revenge/FOMO?

If any box is **no** → **no trade**.

## 9) Post-Trade Reflection (Minimum Fields)
For each trade, capture:
- Pair/instrument, long/short, setup type.
- Entry, SL, TP(s), leverage, size.
- Planned R vs realized R.
- Mistake? (yes/no). If yes, pick 1–2 tags:
  - early entry / late entry
  - no clear trigger
  - ignored level
  - broke risk rules (size/SL)
  - news chase / FOMO
- One concrete improvement for next session.

Keep this file as the **high-level playbook** and pair it with `perps_execution_checklist.md` + the journal template for day-to-day operations.
