from __future__ import annotations

from datetime import datetime
from pathlib import Path

import MetaTrader5 as mt5
import pandas as pd

from ..logging_utils import get_logger
from ..config import data_config

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}


def initialize_mt5() -> None:
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize() failed: {mt5.last_error()}")
    logger.info("Initialized MetaTrader5 connection")


def shutdown_mt5() -> None:
    mt5.shutdown()
    logger.info("Shutdown MetaTrader5 connection")


def fetch_ohlc(
    symbol: str,
    timeframe: str | None = None,
    bars: int | None = None,
) -> pd.DataFrame:
    tf = timeframe or data_config.mt5_timeframe_default
    n_bars = bars or data_config.history_bars_default

    if tf not in TIMEFRAME_MAP:
        raise ValueError(f"Unsupported timeframe: {tf}")

    logger.info("Fetching %d bars for %s %s", n_bars, symbol, tf)

    rates = mt5.copy_rates_from(
        symbol,
        TIMEFRAME_MAP[tf],
        datetime.utcnow(),
        n_bars,
    )
    if rates is None:
        raise RuntimeError(f"mt5.copy_rates_from returned None for {symbol} {tf}")

    df = pd.DataFrame(rates)
    df.rename(
        columns={"real_volume": "real_volume", "tick_volume": "tick_volume"},
        inplace=True,
    )
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df[["time", "open", "high", "low", "close", "tick_volume"]]


def save_ohlc(df: pd.DataFrame, symbol: str, timeframe: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}_{timeframe}_ohlc.parquet"
    path = RAW_DIR / filename
    df.to_parquet(path)
    logger.info("Saved OHLC to %s", path)
    return path
