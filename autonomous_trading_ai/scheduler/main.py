from __future__ import annotations

from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

from ..logging_utils import get_logger
from ..config import scheduler_config, risk_config
from ..data.collector_mt5 import initialize_mt5, shutdown_mt5, fetch_ohlc, save_ohlc
from ..research.features import compute_features, save_features
from ..research.regime import add_regime_column
from ..research.features import load_features
from ..strategies.pool import load_pool, save_pool
from ..strategies.evolution import evolve_population, load_population, save_population
from ..backtests.engine import run_backtest
from ..backtests.evaluation import evaluate_strategy
from ..backtests.walkforward import walk_forward_test
from ..backtests.monte_carlo import monte_carlo_pnl
from ..execution.live_monitor import update_live_stats
from ..execution.signals import execute_signals_for_symbol
from ..vector_memory.research_memory import ResearchMemory

logger = get_logger(__name__)
BASE_DIR = Path(__file__).resolve().parents[1]

# Symbols/timeframes to manage (can be externalized/configured later)
# MANAGED_SYMBOLS = ["XAUUSDm", "BTCUSDm"]
MANAGED_SYMBOLS = ["XAUUSDm"]
TIMEFRAME = "M15"


def job_update_data() -> None:
    """Fetch latest OHLC, compute features + regimes for managed symbols."""
    logger.info("Scheduler: job_update_data start")
    for symbol in MANAGED_SYMBOLS:
        try:
            df = fetch_ohlc(symbol, timeframe=TIMEFRAME)
            save_ohlc(df, symbol, TIMEFRAME)
            feat = compute_features(df, symbol, TIMEFRAME)
            feat = add_regime_column(feat)
            save_features(feat, symbol, TIMEFRAME)
        except Exception as e:
            logger.exception("job_update_data error for %s: %s", symbol, e)
    logger.info("Scheduler: job_update_data done")


def job_research_strategies() -> None:
    """Generate/evolve strategies, backtest, evaluate, and update pool + memory."""
    logger.info("Scheduler: job_research_strategies start")
    pool = load_pool()
    memory = ResearchMemory()

    for symbol in MANAGED_SYMBOLS:
        try:
            feat = load_features(symbol, TIMEFRAME)
        except FileNotFoundError:
            logger.warning("No features found for %s %s; skipping research", symbol, TIMEFRAME)
            continue
        except Exception as e:
            logger.exception("Failed to load features for %s: %s", symbol, e)
            continue

        # Select top parent strategies from pool for this symbol/timeframe
        from ..strategies.generator import load_strategy

        parent_records = [
            rec
            for rec in pool.strategies.values()
            if rec.symbol == symbol and rec.timeframe == TIMEFRAME
        ]
        parent_records.sort(key=lambda r: r.score, reverse=True)
        parent_records = parent_records[:20]

        existing_strats = []
        for rec in parent_records:
            path = BASE_DIR / "strategies" / "generated" / f"{rec.name}.json"
            try:
                strat = load_strategy(path)
                existing_strats.append((strat, rec.score))
            except Exception as e:
                logger.exception("Failed to load parent strategy %s from %s: %s", rec.name, path, e)

        # Evolve population for this symbol/timeframe (or random if no parents yet)
        new_population = evolve_population(symbol, TIMEFRAME, existing_strats)
        save_population(new_population)

        for strat in new_population:
            try:
                result = run_backtest(
                    feat,
                    strat,
                    regime_column="regime",
                )
                eval_result = evaluate_strategy(result.stats)

                # Skip strategies that essentially never trade (num_trades too low)
                num_trades = eval_result.get("num_trades", 0.0)
                if num_trades < 5:
                    logger.info("Skipping strategy %s due to low trade count: %.0f", strat.name, num_trades)
                    continue

                # Walk-forward
                wf = walk_forward_test(feat, strat)
                mc = monte_carlo_pnl(result.trades, n_runs=200)

                # Merge robustness stats into eval_result
                eval_result["wf_overall_sharpe"] = wf.get("aggregate", {}).get("overall_sharpe", 0.0)
                eval_result["wf_overall_max_drawdown_pct"] = wf.get("aggregate", {}).get("overall_max_drawdown_pct", 0.0)
                eval_result.update(mc)

                pool.upsert_strategy(
                    strategy=strat,
                    stats=eval_result,
                    score=eval_result.get("score", 0.0),
                    status="candidate" if eval_result.get("accepted") else "disabled",
                )

                # Store research result in Chroma
                memory.store_strategy_result(
                    strategy_name=strat.name,
                    symbol=strat.symbol,
                    timeframe=strat.timeframe,
                    stats=eval_result,
                )

            except Exception as e:
                logger.exception("Research error for strategy %s: %s", strat.name, e)

    save_pool(pool)
    logger.info("Scheduler: job_research_strategies done")


def job_execute_signals() -> None:
    """Generate and execute signals for active strategies based on latest features."""
    logger.info("Scheduler: job_execute_signals start")
    pool = load_pool()
    risk_perc = min(0.5, risk_config.max_risk_per_trade_pct)

    from ..research.features import load_features

    for symbol in MANAGED_SYMBOLS:
        try:
            feat = load_features(symbol, TIMEFRAME)
        except FileNotFoundError:
            logger.warning("No features for %s %s; skipping signal execution", symbol, TIMEFRAME)
            continue
        except Exception as e:
            logger.exception("Failed to load features for %s: %s", symbol, e)
            continue

        results = execute_signals_for_symbol(symbol, TIMEFRAME, feat, pool, risk_perc=risk_perc)
        for sig, reason in results:
            logger.info(
                "Signal result: strategy=%s symbol=%s dir=%s reason=%s",
                sig.strategy.name,
                symbol,
                sig.direction,
                reason,
            )

    logger.info("Scheduler: job_execute_signals done")


def job_live_monitor() -> None:
    """Update live stats and enforce basic portfolio-level safety."""
    logger.info("Scheduler: job_live_monitor start")
    try:
        update_live_stats()
    except Exception as e:
        logger.exception("job_live_monitor error: %s", e)
    logger.info("Scheduler: job_live_monitor done")


def start_scheduler() -> BackgroundScheduler:
    if not scheduler_config.enable_scheduler:
        logger.warning("Scheduler is disabled via config")
        return BackgroundScheduler()

    logger.info("Starting MT5 and scheduler...")
    initialize_mt5()

    sched = BackgroundScheduler(timezone="UTC")

    # Every 5 minutes: update data/features/regimes
    sched.add_job(job_update_data, "interval", minutes=5, id="update_data")

    # Every 30 minutes: research/evaluate/evolve strategies
    sched.add_job(job_research_strategies, "interval", minutes=30, id="research_strategies")

    # Every 5 minutes: generate/execute signals from active strategies
    sched.add_job(job_execute_signals, "interval", minutes=5, id="execute_signals")

    # Every 5 minutes: live monitoring
    sched.add_job(job_live_monitor, "interval", minutes=5, id="live_monitor")

    sched.start()
    logger.info("Scheduler started")
    return sched


def shutdown_scheduler(sched: BackgroundScheduler) -> None:
    logger.info("Shutting down scheduler and MT5...")
    sched.shutdown(wait=False)
    shutdown_mt5()


if __name__ == "__main__":
    # Simple standalone runner
    sched = start_scheduler()
    try:
        import time

        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received; shutting down")
        shutdown_scheduler(sched)
