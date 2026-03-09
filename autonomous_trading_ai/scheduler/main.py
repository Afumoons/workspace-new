from __future__ import annotations

from datetime import datetime
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

from ..logging_utils import get_logger
from ..config import scheduler_config
from ..data.collector_mt5 import initialize_mt5, shutdown_mt5, fetch_ohlc, save_ohlc
from ..research.features import compute_features, save_features
from ..research.regime import add_regime_column
from ..strategies.generator import generate_and_save_batch
from ..strategies.pool import load_pool, save_pool
from ..backtests.engine import run_backtest
from ..backtests.evaluation import evaluate_strategy
from ..backtests.walkforward import walk_forward_test
from ..backtests.monte_carlo import monte_carlo_pnl
from ..execution.live_monitor import update_live_stats

logger = get_logger(__name__)
BASE_DIR = Path(__file__).resolve().parents[1]

# Symbols/timeframes to manage (can be externalized/configured later)
MANAGED_SYMBOLS = ["XAUUSDm", "BTCUSDm"]
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
    """Generate candidate strategies, backtest, evaluate, and update pool."""
    logger.info("Scheduler: job_research_strategies start")
    pool = load_pool()

    for symbol in MANAGED_SYMBOLS:
        try:
            from ..research.features import load_features

            feat = load_features(symbol, TIMEFRAME)
        except FileNotFoundError:
            logger.warning("No features found for %s %s; skipping research", symbol, TIMEFRAME)
            continue
        except Exception as e:
            logger.exception("Failed to load features for %s: %s", symbol, e)
            continue

        # Generate a small batch of random strategies for this symbol
        paths = generate_and_save_batch(symbol, TIMEFRAME, n=3)
        from ..strategies.generator import load_strategy

        for path in paths:
            try:
                strat = load_strategy(path)
                result = run_backtest(
                    feat,
                    strat,
                    regime_column="regime",
                )
                eval_result = evaluate_strategy(result.stats)
                # Walk-forward
                wf = walk_forward_test(feat, strat)
                mc = monte_carlo_pnl(result.trades, n_runs=200)

                # Merge some robustness stats into eval_result
                eval_result["wf_overall_sharpe"] = wf.get("aggregate", {}).get("overall_sharpe", 0.0)
                eval_result["wf_overall_max_drawdown_pct"] = wf.get("aggregate", {}).get("overall_max_drawdown_pct", 0.0)
                eval_result.update(mc)

                pool.upsert_strategy(
                    strategy=strat,
                    stats=eval_result,
                    score=eval_result.get("score", 0.0),
                    status="candidate" if eval_result.get("accepted") else "disabled",
                )
            except Exception as e:
                logger.exception("Research error for strategy file %s: %s", path, e)

    save_pool(pool)
    logger.info("Scheduler: job_research_strategies done")


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

    # Every 30 minutes: research/evaluate candidate strategies
    sched.add_job(job_research_strategies, "interval", minutes=30, id="research_strategies")

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
