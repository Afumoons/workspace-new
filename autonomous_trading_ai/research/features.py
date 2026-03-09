from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from ..logging_utils import get_logger

logger = get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FEATURES_DIR = DATA_DIR / "features"
FEATURES_DIR.mkdir(parents=True, exist_ok=True)


def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / period, min_periods=period).mean()
    return atr


def compute_volatility(close: pd.Series, window: int = 20) -> pd.Series:
    returns = close.pct_change()
    return returns.rolling(window=window, min_periods=window).std()


def compute_trend_strength(close: pd.Series, window: int = 50) -> pd.Series:
    """Simple trend strength proxy: normalized slope of a rolling mean."""
    ma = close.rolling(window=window, min_periods=window).mean()
    slope = ma.diff()
    scale = close.rolling(window=window, min_periods=window).std()
    return slope / (scale + 1e-9)


def compute_ichimoku(df: pd.DataFrame) -> pd.DataFrame:
    """Add Ichimoku Kinko Hyo lines to the DataFrame."""
    high = df["high"]
    low = df["low"]

    conv_period = 9
    base_period = 26
    span_b_period = 52

    tenkan_sen = (high.rolling(conv_period).max() + low.rolling(conv_period).min()) / 2
    kijun_sen = (high.rolling(base_period).max() + low.rolling(base_period).min()) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(base_period)
    senkou_span_b = (
        (high.rolling(span_b_period).max() + low.rolling(span_b_period).min()) / 2
    ).shift(base_period)

    chikou_span = df["close"].shift(-base_period)

    df = df.copy()
    df["tenkan_sen"] = tenkan_sen
    df["kijun_sen"] = kijun_sen
    df["senkou_span_a"] = senkou_span_a
    df["senkou_span_b"] = senkou_span_b
    df["chikou_span"] = chikou_span
    return df


def compute_fib_zones(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    """Add simple Fibonacci zone flags based on rolling high/low.

    fib_zone_382 == 1 when close is near 38.2% retracement
    fib_zone_618 == 1 when close is near 61.8% retracement
    """
    high = df["high"]
    low = df["low"]
    close = df["close"]

    rolling_high = high.rolling(window).max()
    rolling_low = low.rolling(window).min()
    range_ = rolling_high - rolling_low
    position = (close - rolling_low) / (range_ + 1e-9)

    df = df.copy()
    df["fib_zone_382"] = position.between(0.36, 0.40).astype(int)
    df["fib_zone_618"] = position.between(0.60, 0.64).astype(int)
    return df


def compute_features(
    df: pd.DataFrame,
    symbol: str,
    timeframe: str,
    rsi_period: int = 14,
    ma_short: int = 20,
    ma_long: int = 50,
    atr_period: int = 14,
    vol_window: int = 20,
    trend_window: int = 50,
) -> pd.DataFrame:
    """Given OHLCV DataFrame, compute technical features.

    Expected df columns: ["time", "open", "high", "low", "close", "tick_volume"].
    """
    logger.info(
        "Computing features for %s %s (len=%d)", symbol, timeframe, len(df)
    )

    df = df.copy()
    df = df.sort_values("time")
    df["time"] = pd.to_datetime(df["time"])

    # Core indicators
    df["rsi"] = compute_rsi(df["close"], period=rsi_period)
    df["ma_short"] = df["close"].rolling(ma_short, min_periods=ma_short).mean()
    df["ma_long"] = df["close"].rolling(ma_long, min_periods=ma_long).mean()
    df["atr"] = compute_atr(df, period=atr_period)
    df["volatility"] = compute_volatility(df["close"], window=vol_window)
    df["trend_strength"] = compute_trend_strength(df["close"], window=trend_window)

    # Ichimoku
    df = compute_ichimoku(df)

    # Fibonacci zones
    df = compute_fib_zones(df, window=100)

    df.dropna(inplace=True)
    logger.info(
        "Finished feature computation for %s %s (len=%d)", symbol, timeframe, len(df)
    )
    return df


def save_features(df: pd.DataFrame, symbol: str, timeframe: str) -> Path:
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}_{timeframe}_features.parquet"
    path = FEATURES_DIR / filename
    df.to_parquet(path)
    logger.info("Saved features to %s", path)
    return path


def load_features(symbol: str, timeframe: str) -> pd.DataFrame:
    filename = f"{symbol}_{timeframe}_features.parquet"
    path = FEATURES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"No features file at {path}")
    df = pd.read_parquet(path)
    logger.info("Loaded features from %s (len=%d)", path, len(df))
    return df
