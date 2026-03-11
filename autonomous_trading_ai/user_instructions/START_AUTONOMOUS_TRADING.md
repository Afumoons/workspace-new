# How to Restart the Autonomous AI Trading Agent

If I’m not around (tokens depleted, session reset, etc.), you can follow this runbook to bring the system back online and let it trade autonomously again.

---

## 0. MetaTrader 5 Prerequisites

1. Open **MetaTrader 5**.
2. Log into your **demo** account.
3. In **Market Watch**:
   - Make sure the symbols you want to trade are visible.
   - Current config expects (can be changed in code):
     - `XAUUSDm`
     - `BTCUSDm`

If your broker uses different names, the code under `MANAGED_SYMBOLS` in
`scheduler/main.py` needs to be updated.

---

## 1. Start Chroma (Vector Database)

Chroma stores strategy research results and performance summaries.

If using Docker:

```powershell
cd C:\Users\afusi\.openclaw\workspace

# Start the Chroma container if it exists
# (first time use the full run command below instead)
docker start chroma
```

First-time run example (if the container does not exist yet):

```powershell
docker run -d ^
  --name chroma ^
  -p 8000:8000 ^
  -v C:\Users\afusi\.openclaw\workspace\chroma_data:/chroma/chroma ^
  chromadb/chroma:latest ^
  chroma run --path /chroma/chroma --host 0.0.0.0 --port 8000
```

---

## 2. (Optional) Start MT5 Bridge

The autonomous system talks directly to MT5 via the Python API, but the
bridge is useful for diagnostics.

```powershell
cd C:\Users\afusi\.openclaw\workspace\trading-bridge
python bridge.py
```

Leave this window running while you test.

---

## 3. Activate the autonomous_trading_ai Environment

> **Important:** Run commands that import `autonomous_trading_ai.*` from the
> **workspace root** so Python can see `autonomous_trading_ai` as a package.

```powershell
cd C:\Users\afusi\.openclaw\workspace
.\autonomous_trading_ai\.venv\Scripts\activate
```

You should see the venv name in your prompt.

---

## 4. Run One Research Cycle Manually (Recommended)

This primes the system with fresh data, features, regimes, and candidate
strategies.

**Step 4.1 – Update data + features + regimes**

```powershell
python -c "from autonomous_trading_ai.scheduler.main import job_update_data; job_update_data()"
```

**Step 4.2 – Research/evaluate/evolve strategies**

```powershell
python -c "from autonomous_trading_ai.scheduler.main import job_research_strategies; job_research_strategies()"
```

This will:

- Fetch OHLC from MT5 for `MANAGED_SYMBOLS` at `TIMEFRAME`.
- Save raw data in `data/raw/`.
- Compute features + regimes and save in `data/features/`.
- Evolve / generate strategy population.
- Backtest + evaluate + walk-forward + Monte Carlo.
- Update `strategies/pool_state.json`.
- Store research results in Chroma.

---

## 5. Strategy Selection & Self-Improvement (No Manual Promotion Needed)

The system now promotes strategies automatically based on rich
explanations of their behavior (`strategy_explain`). You **do not** need
to manually run a promotion script in normal operation.

On each `job_research_strategies` cycle, the agent now:

- Backtests and evaluates strategies as before.
- Builds a `strategy_explain` object per strategy, describing:
  - PnL per market regime (trending_up, trending_down, ranging, etc.).
  - Session behavior (Asia / London / New York).
  - Risk behavior (R:R, SL/TP vs rule exits, holding time, losing streaks).
  - Stability over time (sub-period sharpe, sharpe_std).
  - Behavior around macro news (performance near high-impact events,
    avoidance rate, pre/post news PnL).
- Computes a score that rewards:
  - Profit in trending regimes.
  - Reasonable performance in ranges.
  - Stable behavior across time.
  - Sensible behavior around news (not kamikaze into high-impact events).
- Automatically sets pool status:
  - `active`   → strategies that pass stricter criteria (PnL > 0, DD <= 20%,
                 PF >= 1.1, healthy trend performance, not destroyed in ranges).
  - `candidate` → strategies that pass base thresholds but not the stricter
                  promotion policy.
  - `disabled` → everything else.

For inspection/debugging, you can still review the pool manually:

```powershell
# Show top XAUUSDm M15 strategies and their explanations
python -m autonomous_trading_ai.scripts.print_top_strategies --symbol XAUUSDm --timeframe M15 --status active --limit 5
```

The scheduler will keep evolving, evaluating, and promoting/retiring
strategies automatically over time – a constantly self-improving system.

---

## 6. Start the Autonomous Scheduler (24/7 Loop)

This is the main process that keeps everything running.

```powershell
python -m autonomous_trading_ai.scheduler.main
```

What it does:

- Initializes MT5 connection.
- Starts APScheduler with jobs:

  - **Every 5 minutes:**
    - `job_update_data`
      - Fetch OHLC for `MANAGED_SYMBOLS` @ `TIMEFRAME`.
      - Save raw data → compute features → add `regime` → save features.
    - `job_execute_signals`
      - Load latest features.
      - Load `active` strategies from the pool.
      - Generate entry signals (based on long/short rules).
      - Call `execute_trade(...)` for each signal
        (risk manager + MT5 execution).
    - `job_live_monitor`
      - Update equity history & peak in `execution/live_state.json`.
      - If drawdown exceeds a safety threshold, can disable strategies.

  - **Every 30 minutes:**
    - `job_research_strategies`
      - Load features.
      - Load existing population + scores from pool.
      - Evolve the population.
      - Backtest + evaluate + walk-forward + Monte Carlo.
      - Update pool (scores, status, stats).
      - Store research results in Chroma.

Leave this running while you want the autonomous system active.
Stopping this process stops automatic trading.

---

## 7. Restarting After a Full Stop or Token Depletion

If I disappear and you want to get things running again:

1. **MT5:**
   - Launch MetaTrader 5.
   - Log into the demo account.
   - Confirm your symbols (e.g. `XAUUSDm`, `BTCUSDm`) show ticks.

2. **Chroma:**
   - If using Docker: `docker start chroma`.

3. **Bridge (optional):**
   - `cd C:\Users\afusi\.openclaw\workspace\trading-bridge`
   - `python bridge.py`

4. **Autonomous Trading Agent:**

   ```powershell
   cd C:\Users\afusi\.openclaw\workspace
   .autonomous_trading_ai\.venv\Scripts\activate

   # Optional: one-shot research cycle
   python -c "from autonomous_trading_ai.scheduler.main import job_update_data; job_update_data()"
   python -c "from autonomous_trading_ai.scheduler.main import job_research_strategies; job_research_strategies()"

   # Promote best candidates
   python -m autonomous_trading_ai.scripts.promote_strategies

   # Start the scheduler loop
   python -m autonomous_trading_ai.scheduler.main
   ```

Once that last command is running, the Autonomous AI Trading Agent is
back online and managing:

- Data ingestion & feature engineering
- Strategy evolution + evaluation
- Strategy pool management
- Risk-checked MT5 execution
- Live monitoring & basic safety

You can always adjust parameters (symbols, timeframes, risk thresholds)
via the config files and modules in this project if you want to evolve
it further.
