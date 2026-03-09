from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from ..logging_utils import get_logger

logger = get_logger(__name__)

RegimeLabel = Literal[
    "trending_up",
    "trending_down",
    "ranging",
    "high_vol",
    "low_vol",
]


@dataclass
class RegimeConfig:
    trend_up_thresh: float = 0.02
    trend_down_thresh: float = -0.02
    vol_high_quantile: float = 0.7
    vol_low_quantile: float = 0.3


DEFAULT_REGIME_CONFIG = RegimeConfig()


def detect_regime(df: pd.DataFrame, cfg: RegimeConfig = DEFAULT_REGIME_CONFIG) -> pd.Series:
    """Classify market regime for each row based on trend_strength and volatility.

    Returns a pd.Series of string labels aligned with df index.
    """
    if "trend_strength" not in df.columns or "volatility" not in df.columns:
        raise ValueError("DataFrame must contain 'trend_strength' and 'volatility' columns")

    trend = df["trend_strength"].astype(float)
    vol = df["volatility"].astype(float)

    # Compute volatility thresholds from sample
    vol_hi = vol.quantile(cfg.vol_high_quantile)
    vol_lo = vol.quantile(cfg.vol_low_quantile)

    labels: list[str] = []
    for t, v in zip(trend, vol):
        if t >= cfg.trend_up_thresh and v <= vol_hi:
            labels.append("trending_up")
        elif t <= cfg.trend_down_thresh and v <= vol_hi:
            labels.append("trending_down")
        elif v >= vol_hi:
            labels.append("high_vol")
        elif v <= vol_lo:
            labels.append("low_vol")
        else:
            labels.append("ranging")

    series = pd.Series(labels, index=df.index, name="regime")
    logger.info("Detected regimes: counts=%s", series.value_counts().to_dict())
    return series


def add_regime_column(df: pd.DataFrame, cfg: RegimeConfig = DEFAULT_REGIME_CONFIG) -> pd.DataFrame:
    df = df.copy()
    df["regime"] = detect_regime(df, cfg)
    return df
