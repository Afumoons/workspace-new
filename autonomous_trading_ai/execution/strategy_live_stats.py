from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from autonomous_trading_ai.logging_utils import get_logger

logger = get_logger(__name__)

STATS_PATH = Path(__file__).resolve().parent / "strategy_live_stats.json"


@dataclass
class StrategyLiveStats:
    name: str
    total_pnl: float = 0.0
    num_trades: int = 0
    last_update: str = ""  # ISO-8601 UTC

    @property
    def avg_pnl(self) -> float:
        return self.total_pnl / self.num_trades if self.num_trades > 0 else 0.0


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_all_strategy_stats() -> Dict[str, StrategyLiveStats]:
    """Load live stats for all strategies from disk.

    If the file does not exist or is invalid, returns an empty dict.
    """
    if not STATS_PATH.exists():
        return {}
    try:
        with STATS_PATH.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        logger.exception("Failed to load strategy_live_stats: %s", e)
        return {}

    out: Dict[str, StrategyLiveStats] = {}
    for name, data in raw.get("strategies", {}).items():
        try:
            out[name] = StrategyLiveStats(name=name, **{k: v for k, v in data.items() if k != "name"})
        except Exception:
            logger.exception("Failed to parse StrategyLiveStats for %s", name)
    return out


def save_all_strategy_stats(stats: Dict[str, StrategyLiveStats]) -> None:
    try:
        payload = {"strategies": {name: asdict(s) for name, s in stats.items()}}
        with STATS_PATH.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception as e:
        logger.exception("Failed to save strategy_live_stats: %s", e)


def register_strategy_pnl(strategy_name: str, pnl: float) -> None:
    """Update live stats for a single strategy after a closed deal.

    This uses the strategy name encoded in the MT5 deal comment
    (see execution.engine.execute_trade).
    """
    stats = load_all_strategy_stats()
    rec = stats.get(strategy_name) or StrategyLiveStats(name=strategy_name)
    rec.total_pnl += float(pnl)
    rec.num_trades += 1
    rec.last_update = _now_iso()
    stats[strategy_name] = rec
    save_all_strategy_stats(stats)
    logger.info(
        "StrategyLiveStats: %s trades=%d total_pnl=%.2f avg_pnl=%.2f",
        strategy_name,
        rec.num_trades,
        rec.total_pnl,
        rec.avg_pnl,
    )
