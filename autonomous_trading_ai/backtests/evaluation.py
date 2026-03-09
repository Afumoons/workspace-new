from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class EvaluationConfig:
    min_trades: int = 30
    min_sharpe: float = 0.5
    max_drawdown_pct: float = 30.0
    min_profit_factor: float = 1.2

    weight_sharpe: float = 0.4
    weight_profit_factor: float = 0.3
    weight_drawdown_penalty: float = 0.3


DEFAULT_EVAL_CONFIG = EvaluationConfig()


def compute_score(stats: Dict[str, float], cfg: EvaluationConfig = DEFAULT_EVAL_CONFIG) -> float:
    sharpe = stats.get("sharpe_ratio", 0.0)
    pf = stats.get("profit_factor", 0.0)
    dd = stats.get("max_drawdown_pct", 0.0)

    # Drawdown penalty: 1.0 when dd=0, decays linearly to 0 at cfg.max_drawdown_pct
    if dd >= cfg.max_drawdown_pct:
        dd_penalty = 0.0
    else:
        dd_penalty = max(0.0, 1.0 - dd / cfg.max_drawdown_pct)

    score = (
        cfg.weight_sharpe * sharpe +
        cfg.weight_profit_factor * pf +
        cfg.weight_drawdown_penalty * dd_penalty
    )
    return float(score)


def passes_thresholds(stats: Dict[str, float], cfg: EvaluationConfig = DEFAULT_EVAL_CONFIG) -> bool:
    num_trades = stats.get("num_trades", 0.0)
    sharpe = stats.get("sharpe_ratio", 0.0)
    dd = stats.get("max_drawdown_pct", 0.0)
    pf = stats.get("profit_factor", 0.0)

    if num_trades < cfg.min_trades:
        logger.info("Rejected strategy: too few trades (%.0f < %d)", num_trades, cfg.min_trades)
        return False
    if sharpe < cfg.min_sharpe:
        logger.info("Rejected strategy: sharpe %.2f < %.2f", sharpe, cfg.min_sharpe)
        return False
    if dd > cfg.max_drawdown_pct:
        logger.info("Rejected strategy: drawdown %.2f%% > %.2f%%", dd, cfg.max_drawdown_pct)
        return False
    if pf < cfg.min_profit_factor:
        logger.info("Rejected strategy: profit factor %.2f < %.2f", pf, cfg.min_profit_factor)
        return False

    return True


def evaluate_strategy(stats: Dict[str, float], cfg: EvaluationConfig = DEFAULT_EVAL_CONFIG) -> Dict[str, float]:
    score = compute_score(stats, cfg)
    ok = passes_thresholds(stats, cfg)
    result = {
        **stats,
        "score": score,
        "accepted": bool(ok),
    }
    logger.info(
        "Evaluation result: score=%.3f, accepted=%s, stats=%s",
        score,
        ok,
        {k: round(v, 3) if isinstance(v, float) else v for k, v in stats.items()},
    )
    return result
