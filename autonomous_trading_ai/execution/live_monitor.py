from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import MetaTrader5 as mt5

from ..logging_utils import get_logger
from ..strategies.pool import load_pool, save_pool

logger = get_logger(__name__)

LIVE_STATE_PATH = Path(__file__).resolve().parent / "live_state.json"


@dataclass
class LiveStats:
    equity_history: List[float] = field(default_factory=list)
    times: List[str] = field(default_factory=list)
    peak_equity: float = 0.0


def _get_account_equity() -> float:
    info = mt5.account_info()
    if info is None:
        raise RuntimeError("MT5 account_info() returned None")
    return float(info.equity)


def update_live_stats() -> None:
    """Update live equity history and disable strategies far from expectations.

    For now, this tracks only overall equity; per-strategy attribution is left
    for a future refinement. It demonstrates the pattern: load pool, update
    live state, and potentially disable strategies.
    """
    import json
    from datetime import datetime

    equity = _get_account_equity()
    now_iso = datetime.utcnow().isoformat() + "Z"

    if LIVE_STATE_PATH.exists():
        with LIVE_STATE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        stats = LiveStats(**data)
    else:
        stats = LiveStats()

    stats.equity_history.append(equity)
    stats.times.append(now_iso)
    stats.peak_equity = max(stats.peak_equity, equity)

    with LIVE_STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump({
            "equity_history": stats.equity_history,
            "times": stats.times,
            "peak_equity": stats.peak_equity,
        }, f, indent=2)

    logger.info("Live monitor: equity=%.2f peak=%.2f", equity, stats.peak_equity)

    # Placeholder: strategy-level disabling could be implemented here by
    # comparing live drawdown vs. per-strategy backtest expectations.
    pool = load_pool()
    # e.g., if overall drawdown breaches a threshold, disable all active
    # strategies until reviewed.
    if stats.peak_equity > 0:
        dd_pct = (stats.peak_equity - equity) / stats.peak_equity * 100.0
        # This threshold is arbitrary here; in practice we would align it with
        # risk_config and per-strategy expectations.
        if dd_pct > 30.0:
            for rec in pool.strategies.values():
                if rec.status == "active":
                    rec.status = "disabled"
                    logger.warning(
                        "Live monitor: disabling strategy %s due to portfolio DD %.2f%%",
                        rec.name,
                        dd_pct,
                    )
            save_pool(pool)
