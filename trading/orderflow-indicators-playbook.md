# Orderflow Indicator Playbook: Volume Profile, Deep Trades, Liquidity Heatmap, VWAP

_Last updated: 2026-05-18_

For Afu / Clio Nova. Built for aggressive but controlled **scalp + intraday trading** in crypto perps, gold/forex CFDs, and later Hyperliquid-style orderflow. This is education and process design, not an instruction to place live trades.

## Core Principle

These tools answer different market questions:

| Tool | Primary question | Best use |
|---|---|---|
| Volume Profile, long-term | Where has the market accepted / rejected price? | HTF context, key levels, bias zones |
| Deep Trades | Where are aggressive market orders hitting now? | Scalping trigger / confirmation |
| Liquidity Heatmap | Where are resting limit orders sitting, pulling, or absorbing? | Targeting, trap detection, execution timing |
| VWAP | Where is fair intraday average price weighted by volume? | Intraday bias, mean reversion, trend continuation |

The strongest trades happen when all four align:

1. **Long-term location** from Volume Profile.
2. **Intraday fair value / regime** from VWAP.
3. **Liquidity map** shows where price is likely to move or react.
4. **Deep Trades** confirm real aggressive participation at the trigger.

---

## 1. Volume Profile — Long-Term Context

### What it is

Volume Profile maps traded volume by **price**, not by time. Instead of asking “what happened each candle?”, it asks: **at which prices did the most business happen?**

Important levels:

- **POC, Point of Control**: price with highest traded volume in the selected range.
- **VAH, Value Area High**: upper boundary of the area containing usually ~70% of traded volume.
- **VAL, Value Area Low**: lower boundary of that value area.
- **HVN, High Volume Node**: high-volume area; market accepted price there.
- **LVN, Low Volume Node**: low-volume gap; market rejected / moved quickly through it.
- **Profile High / Low**: extremes of the selected range.

### How it reads the market

Volume Profile is a **market memory map**:

- **HVN = accepted / fair value**. Price often slows, rotates, or chops there.
- **LVN = rejected / unfair value**. Price often moves quickly through it, or rejects sharply from it.
- **VAH/VAL = auction boundaries**. If price accepts outside them, a new auction may begin.
- **POC = magnet** in balanced markets; reference point in trend markets.

### Best profile ranges

For Afu’s style:

- **Long-term bias**: 3M / 6M / 1Y fixed range profile.
- **Swing context**: profile from major swing low to swing high.
- **Weekly prep**: previous week profile.
- **Intraday context**: previous day/session profile.

Do not mix everything into one unreadable chart. Use one long-term profile for map, one session profile for tactical levels.

### Market regimes

#### Balanced market

Signs:

- Price rotates around POC.
- VAH/VAL contain price.
- Breakouts fail often.

Plan:

- Buy near VAL / lower HVN after absorption or reclaim.
- Sell near VAH / upper HVN after rejection.
- Take profit near POC first, then opposite value boundary.

#### Trending / re-pricing market

Signs:

- Price accepts outside VAH/VAL.
- POC starts migrating.
- Pullbacks hold outside old value.
- LVNs get traversed quickly.

Plan:

- Trade with direction after acceptance outside value.
- Use old VAH/VAL as retest support/resistance.
- Target next HVN / prior POC / major liquidity cluster.

### Entry models

#### A. Value edge reversal

Use when market is balanced.

Long:

1. Price reaches long-term VAL / lower HVN / profile low.
2. Liquidity heatmap shows bids holding or absorption.
3. Deep Trades show sellers hitting bid but price stops falling.
4. Price reclaims micro structure or VWAP lower band.
5. Enter on reclaim / retest.

Short is inverse at VAH / upper HVN.

Invalidation:

- Acceptance below VAL for long / above VAH for short.
- Absorption level breaks with continuation trades.
- No reclaim after sweep.

Targets:

- First: local POC / session VWAP.
- Second: opposite side of value.
- Runner: next HTF HVN / liquidity pool.

#### B. LVN traverse / gap trade

Use when price accepts into a low-volume area.

Long:

1. Price breaks above resistance into an LVN.
2. Retest holds above breakout / old VAH.
3. VWAP supports direction.
4. Deep Trades show aggressive buyers on continuation.
5. Target next HVN / POC above.

Invalidation:

- Price falls back below LVN entry boundary.
- Breakout has no volume / aggressive trade confirmation.
- Heatmap liquidity above pulls and buyers fail.

#### C. Failed auction trap

Long after downside failed auction:

1. Price sweeps below prior low / VAL.
2. Sellers market-sell aggressively into the low.
3. Price refuses to continue lower.
4. Liquidity below is consumed/pulled.
5. Price reclaims VAL / prior low.
6. Enter on reclaim or retest.

This is one of the best scalp/intraday setups because trapped sellers become fuel.

### When to trade Volume Profile setups

Trade when:

- Price is at meaningful HTF level: POC, VAH, VAL, HVN, LVN, prior session profile level.
- There is visible reaction: rejection, absorption, reclaim, acceptance.
- Risk can be placed beyond a clear structure/auction invalidation.

Do not trade when:

- Price is mid-value and no strong trend exists.
- The profile is too zoomed out and levels are too wide for your risk.
- You are forcing a reversal while price is accepting outside value.
- News/volatility makes profile levels irrelevant temporarily.

---

## 2. Deep Trades — Scalping Trigger

### What it is

“Deep Trades” usually refers to a tape/orderflow view that highlights **large executed trades** or aggressive market orders at/near bid or ask. Different platforms name it differently: large trades, bubbles, time & sales, trade prints, CVD prints, executed volume, or deep trades.

Key distinction:

- **Limit orders** rest in the book; seen in heatmap/DOM.
- **Market orders** execute immediately; seen as trades/prints.

Deep Trades helps answer: **who is aggressive right now, and is price responding?**

### How it reads the market

Important patterns:

#### Aggressive buying

Large green/buy prints hitting ask.

Bullish only if:

- Price moves up after prints.
- Offers get consumed.
- Pullbacks are shallow.
- Buyers keep accepting higher prices.

Not bullish if:

- Large buys print but price cannot move up.
- Sellers absorb them at resistance.
- Price reverses after the print.

#### Aggressive selling

Large red/sell prints hitting bid.

Bearish only if:

- Price moves down after prints.
- Bids get consumed.
- Pullbacks fail.

Not bearish if:

- Large sells print into a low but price stops falling.
- Bids absorb and price reclaims.
- This often forms a long trap-reversal setup.

### Core concept: effort vs result

Deep Trades is best read through **effort vs result**:

- Big buy effort + strong upward result = bullish continuation.
- Big buy effort + no upward result = sell absorption / possible short.
- Big sell effort + strong downward result = bearish continuation.
- Big sell effort + no downward result = buy absorption / possible long.

### Entry models

#### A. Momentum scalp

Long:

1. HTF/intraday bias is bullish.
2. Price is above VWAP or reclaims VWAP.
3. Heatmap shows liquidity target above.
4. Large buy prints break micro resistance.
5. Enter on breakout or first shallow pullback.

Stop:

- Below micro breakout level.
- Below the candle/cluster where aggressive buying started.

Exit:

- At heatmap liquidity above.
- At VAH / prior high / VWAP band.
- Exit fast if buy prints continue but price stalls.

#### B. Absorption reversal scalp

Long:

1. Price sells into support / VAL / HVN / heatmap bid wall.
2. Large red prints appear.
3. Price does not make lower lows or instantly reclaims.
4. Sellers are absorbed.
5. Enter on reclaim of micro range high or failed breakdown retest.

Stop:

- Below absorption low.
- If bid wall disappears and price accepts below.

Exit:

- VWAP / local POC / nearest liquidity above.

Short inverse: large green prints absorbed at resistance.

#### C. Exhaustion print

Long:

1. A final large sell print occurs after an extended down move.
2. Price cannot continue lower.
3. Delta/prints are extremely bearish but candle closes strong.
4. Enter only after reclaim confirmation.

This is powerful but dangerous. Never catch only because a print is large; wait for failure to continue.

### When to trade Deep Trades

Trade when:

- Large prints occur at meaningful levels, not random mid-range.
- Price reaction confirms the print.
- Spread/liquidity is stable enough for scalp execution.
- You have a nearby invalidation.

Do not trade when:

- You are reacting emotionally to one huge print.
- Prints are mixed/choppy and price is mid-value.
- Latency/slippage is high.
- You cannot tell whether large trades are opening, closing, liquidation, or hedging.

---

## 3. Liquidity Heatmap

### What it is

A Liquidity Heatmap visualizes **resting limit orders** in the order book over time. Bright zones usually mean more visible liquidity at that price. It shows where passive buyers/sellers are waiting, where they pull orders, and where liquidity is consumed.

It answers: **where might price be attracted, rejected, accelerated, or trapped?**

### How it reads the market

Key ideas:

- **Liquidity attracts price**: markets often move toward visible liquidity because stops/orders create executable volume.
- **Liquidity can reject price**: if a wall is real and holds, it can act as support/resistance.
- **Liquidity can be fake/spoofed**: if it disappears before price arrives, do not trust it.
- **Liquidity voids accelerate price**: thin books allow fast movement.
- **Absorption**: large market orders hit a level, but resting liquidity absorbs them and price does not pass.

### Heatmap patterns

#### A. Real liquidity wall

Signs:

- Bright level stays visible as price approaches.
- Market orders hit it repeatedly.
- Price cannot break through.
- The wall may partially refill.

Trade:

- Fade into wall after absorption confirmation.
- Place invalidation just beyond wall, not inside noise.

#### B. Liquidity pull / spoof risk

Signs:

- Large bright level appears.
- Price approaches.
- Liquidity disappears before touch.
- Price often accelerates through where support/resistance “should” have been.

Trade:

- Do not fade pulled liquidity.
- If aligned with trend, trade continuation through the vacuum.

#### C. Liquidity sweep and reclaim

Signs:

- Price runs into/through a visible liquidity pool.
- Stops/trades trigger.
- Price quickly reclaims the prior level.

Trade:

- Reversal in opposite direction of sweep.
- Best when aligned with Volume Profile edge or VWAP deviation.

#### D. Liquidity magnet

Signs:

- Large resting liquidity sits above/below price.
- Price slowly grinds toward it.
- Pullbacks are shallow.

Trade:

- Use as target, not automatic entry.
- Enter on pullbacks only if VWAP/trend and Deep Trades support direction.

### Entry models

#### A. Wall absorption fade

Long:

1. Price approaches bid liquidity at support/VAL/HVN.
2. Sellers hit into it.
3. Bid liquidity holds or refills.
4. Price reclaims micro structure.
5. Enter long.

Stop:

- Below wall after it breaks/accepts.

Exit:

- VWAP / local POC / next sell liquidity.

#### B. Liquidity vacuum continuation

Long:

1. Resistance breaks.
2. Offers above pull or get consumed.
3. Heatmap shows thin liquidity until next cluster.
4. Deep Trades show aggressive buying.
5. Enter pullback or breakout continuation.

Stop:

- Back inside broken range.

Exit:

- Next bright liquidity cluster / LVN end / HVN.

#### C. Stop-run reversal

Long:

1. Price sweeps below obvious low/liquidity pool.
2. Sell prints spike.
3. Heatmap shows no follow-through below.
4. Price reclaims low/VAL/VWAP band.
5. Enter on reclaim.

Stop:

- Below sweep low.

Exit:

- VWAP, POC, or opposite liquidity pool.

### When to trade Liquidity Heatmap setups

Trade when:

- Liquidity behavior is clear: holds, pulls, absorbs, or gets consumed.
- The level aligns with HTF Volume Profile or VWAP.
- There is enough book depth for clean execution.

Do not trade when:

- Heatmap liquidity is constantly spoofing/pulling.
- Order book is extremely thin or exchange feed is unreliable.
- You use heatmap levels alone without price reaction.
- News event makes displayed liquidity unstable.

---

## 4. VWAP

### What it is

VWAP = **Volume Weighted Average Price**. It measures the average traded price weighted by volume from an anchor point.

Basic formula:

```text
VWAP = cumulative(typical price × volume) / cumulative(volume)
typical price = (high + low + close) / 3
```

Common anchors:

- Session VWAP: resets daily/session.
- Weekly VWAP.
- Monthly VWAP.
- Anchored VWAP: manually anchored to swing high/low, breakout, news event, liquidation wick, or major impulse start.

### How it reads the market

VWAP is the intraday “fair price” reference:

- Price above VWAP = buyers controlling intraday auction.
- Price below VWAP = sellers controlling intraday auction.
- Price crossing VWAP repeatedly = chop / balanced market.
- VWAP slope matters: rising VWAP supports longs; falling VWAP supports shorts.

VWAP bands / standard deviation bands help identify extension:

- Near VWAP = fair value.
- Upper band = expensive / trend strength or reversal zone.
- Lower band = cheap / trend strength or reversal zone.

### VWAP regimes

#### Trend day

Signs:

- Price holds one side of VWAP.
- Pullbacks to VWAP are bought/sold.
- VWAP slopes with direction.
- Opposite side tests fail quickly.

Plan:

- Trade continuation from VWAP retests.
- Avoid fading strong VWAP trend unless at HTF level with absorption.

#### Mean-reversion day

Signs:

- Price crosses VWAP repeatedly.
- VWAP flat.
- VAH/VAL or range boundaries contain price.

Plan:

- Fade VWAP band extremes back toward VWAP.
- Avoid breakout chasing.

#### Transition day

Signs:

- Price was below VWAP then reclaims and holds above, or inverse.
- VWAP slope changes.
- Deep Trades confirm new aggression.

Plan:

- Trade reclaim/rejection as regime shift.

### Entry models

#### A. VWAP reclaim long

1. Price trades below VWAP.
2. Sweeps support / VAL / liquidity below.
3. Reclaims VWAP with strong candle or aggressive buy prints.
4. Retests VWAP and holds.
5. Enter long.

Stop:

- Below reclaim candle / below VWAP retest low.

Targets:

- Upper VWAP band.
- Prior high / liquidity above.
- VAH / HVN.

#### B. VWAP pullback trend long

1. Price above VWAP.
2. VWAP slopes upward.
3. Pullback into VWAP / first band.
4. Sellers fail to push below.
5. Deep Trades show buy absorption or aggressive buyers return.
6. Enter long.

Stop:

- Below VWAP and failed retest structure.

Exit:

- Prior high, liquidity above, upper band.

#### C. VWAP rejection short

1. Price below VWAP.
2. VWAP slopes down.
3. Bounce into VWAP fails.
4. Buy prints get absorbed.
5. Enter short on lower high / breakdown.

Stop:

- Above VWAP rejection high.

Targets:

- Lower band / prior low / buy liquidity.

#### D. Anchored VWAP from major swing

Use anchored VWAP from:

- Daily/weekly swing low or high.
- Major breakout candle.
- News impulse.
- Liquidation wick.

Interpretation:

- Above anchored VWAP from swing low = buyers of that move are in profit/control.
- Losing anchored VWAP = move participants are underwater; risk of unwind.
- Retest of anchored VWAP after breakout = high-value continuation/reversal decision point.

### When to trade VWAP setups

Trade when:

- VWAP state matches the setup: trend continuation or mean reversion.
- Price reacts clearly at VWAP/bands.
- Volume/Deep Trades confirms reaction.
- Heatmap target/invalidation is visible.

Do not trade when:

- VWAP is flat and price is chopping around it.
- You short just because price is above upper band during a strong trend day.
- You long just because price is below lower band during a strong sell trend.
- It is late session and VWAP lag is high; use it more as context than trigger.

---

## Combined System

### Top-down workflow

#### Step 1 — Long-term map

Mark from Volume Profile:

- 3M/6M/1Y POC.
- VAH/VAL.
- Major HVNs.
- Major LVNs.
- Prior session/week POC and value area.

Question: **Where are we? Accepted value, edge of value, or rejected gap?**

#### Step 2 — Intraday regime

Read VWAP:

- Above/below?
- Slope up/down/flat?
- Trend day or mean-reversion day?
- Near VWAP or extended to band?

Question: **Should I favor continuation or reversion?**

#### Step 3 — Liquidity plan

Use heatmap:

- Where is visible liquidity above/below?
- Is it holding or pulling?
- Are we moving through a void?
- Where are obvious stops?

Question: **Where is price likely to be attracted or rejected?**

#### Step 4 — Trigger

Use Deep Trades:

- Are aggressive buyers/sellers present?
- Is effort producing result?
- Is there absorption?
- Is there exhaustion?

Question: **Is real participation confirming the trade now?**

---

## High-Probability Setups

### 1. Long from HTF value edge + absorption + VWAP reclaim

Best for BTC/ETH/XAU intraday reversals.

Checklist:

- Price at long-term VAL / lower HVN / prior session low.
- Heatmap bid liquidity holds or sweep below fails.
- Large sell prints fail to push lower.
- Price reclaims VWAP or micro range.
- Enter on reclaim/retest.

Invalidation:

- Acceptance below VAL/support.
- Bid liquidity pulls and sell prints continue.

### 2. Short from HTF resistance + absorbed buys + VWAP rejection

Checklist:

- Price at VAH / upper HVN / prior high.
- Large buy prints hit resistance.
- Price fails to move higher.
- Heatmap offers hold/refill.
- VWAP rejection or loss of micro support.

Invalidation:

- Acceptance above resistance.
- Offers consumed and price holds above.

### 3. LVN breakout continuation

Checklist:

- Price accepts into LVN/low-volume gap.
- VWAP slopes with direction.
- Heatmap shows thin path until next liquidity/HVN.
- Deep Trades confirm aggressive continuation.

Invalidation:

- Price falls back into old value/range.
- Aggressive prints disappear or reverse.

### 4. Liquidity sweep trap

Checklist long:

- Obvious low/liquidity pool is swept.
- Huge sell prints occur.
- No continuation lower.
- Price reclaims swept low / VAL / VWAP band.
- Enter on reclaim.

Invalidation:

- New low acceptance after reclaim fails.

This setup has excellent R:R but requires discipline: no reclaim, no trade.

---

## Universal Invalidation Rules

Exit or avoid if:

- Your level breaks and price **accepts** beyond it.
- The liquidity you relied on pulls.
- Deep Trades show the opposite side gaining result, not just effort.
- VWAP regime flips against your trade.
- Price returns to mid-value and loses momentum.
- Your thesis was “absorption,” but the wall gets consumed.
- Your thesis was “breakout,” but price returns inside range.

Acceptance usually means:

- Multiple closes beyond the level.
- Retest holds from the other side.
- POC/VWAP begins migrating beyond the level.
- Orderflow confirms continuation.

---

## When You Should Trade

Good conditions:

- Price is at HTF level or intraday VWAP decision point.
- Liquidity is clear and stable.
- Deep Trades confirm either continuation or absorption.
- Risk is small and structural.
- Target is visible: VWAP, POC, VAH/VAL, liquidity wall, HVN.
- Spread/slippage acceptable.
- No major news in immediate window unless intentionally trading news.

Best windows for crypto perps:

- London open / pre-US overlap.
- US open and first 1–2 hours.
- Major macro release aftermath after spread normalizes.
- Post-liquidation stabilization, not during uncontrolled cascade.

Best windows for XAU/forex CFDs:

- London session.
- US session.
- Around scheduled macro only after initial volatility stabilizes, unless using a specific news playbook.

---

## When You Should Not Trade

Avoid when:

- Price is mid-HVN / mid-value with no edge.
- VWAP is flat and price chops across it repeatedly.
- Heatmap liquidity is erratic/spoof-heavy.
- Deep Trades are mixed and price has no result.
- You are late after a large move and target is already hit.
- You cannot place a logical stop nearby.
- Upcoming high-impact news makes orderbook unreliable.
- You are revenge trading or trying to make back losses.
- Funding/liquidation environment is extreme and you lack a clear trap/reclaim setup.

---

## Risk Management for Afu’s Aggressive Style

Aggressive does not mean random size. It means taking asymmetric opportunities decisively.

Rules:

- Use smaller size when entering before full confirmation.
- Add only after confirmation, not after drawdown.
- Scalp invalidation should be tight and structural.
- If orderflow contradicts thesis, exit fast; do not “hope.”
- Never average down into a failed auction unless it is explicitly planned and risk-capped.
- For high leverage, prefer entries where stop is very close: sweep/reclaim, VWAP retest, wall absorption.

Suggested R:R:

- Scalps: minimum 1:1.2 to 1:2 if win rate high.
- Intraday: minimum 1:2.
- LVN traverse/trap setups: aim 1:3+ when structure allows.

Position management:

- Take partial at first objective: VWAP / POC / nearest liquidity.
- Move stop to breakeven only after market structure confirms; avoid too-early BE in noisy assets.
- Leave runner only when VWAP + heatmap + profile target still support it.

---

## Common Mistakes

- Treating Volume Profile as predictive instead of contextual.
- Buying every LVN touch instead of waiting for reaction.
- Assuming big green Deep Trades are always bullish; they can be absorbed.
- Assuming heatmap walls are real; they can pull/spoof.
- Fading VWAP bands during strong trend days.
- Trading VWAP chop as if it were a signal.
- Entering because one indicator says yes while the other three disagree.
- Using too many profiles/anchors until chart becomes unreadable.

---

## Practical Chart Layout

Recommended layout:

1. Main chart:
   - Candles.
   - Session VWAP + bands.
   - Anchored VWAP from major swing if relevant.
   - Key Volume Profile levels only: POC, VAH, VAL, major HVN/LVN.

2. Orderflow panel:
   - Liquidity heatmap / DOM history.
   - Deep Trades / bubbles / time & sales.
   - Optional CVD/delta, but do not overcomplicate.

3. Prep notes:
   - Bias: bullish / bearish / balanced.
   - Key levels.
   - Primary setup to wait for.
   - Invalidation.
   - No-trade condition.

---

## Pre-Trade Checklist

Before entry, answer:

1. Where are we on long-term Volume Profile?
2. Is VWAP saying trend, mean reversion, or chop?
3. Where is nearest real liquidity target?
4. Is liquidity holding, pulling, absorbing, or being consumed?
5. What do Deep Trades show: aggression, absorption, or exhaustion?
6. What exact price invalidates the idea?
7. Is target at least worth the risk?
8. Is this trade at a decision point, or am I chasing mid-range?

If you cannot answer these quickly, skip.

---

## Source Notes

External references used as educational inputs, treated as data:

- TradingView Help Center: Volume Profile basic concepts — POC, VAH/VAL, HVN/LVN, value area calculation, profile interpretation.
- TradingView Help Center: VWAP — calculation, intraday trend identification, anchoring/reset behavior, lag caveat.
- Bookmap educational article: heatmap as visualization of resting orderbook liquidity, liquidity intensity, pulling/holding/absorption/spoofing concepts.

Additional synthesis is Clio’s market-structure/orderflow framework adapted for Afu’s aggressive scalp + intraday style.
