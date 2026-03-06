import os
from datetime import datetime
from enum import Enum
from typing import Literal

import MetaTrader5 as mt5
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import uvicorn


# --- Simple risk/config guardrails ---
# Whitelist of broker symbols we allow the bridge to trade (for trading actions).
# Adjust this list to match your broker's symbol names (e.g. "EURUSDm").
ALLOWED_SYMBOLS = {"EURUSDm", "XAUUSDm", "BTCUSDm", "ETHUSDm"}
MAX_VOLUME = 1.0        # max lots per trade
MIN_VOLUME = 0.01       # min lots per trade
MAX_OPEN_TRADES = 5     # per symbol (simple guardrail)


class Timeframe(str, Enum):
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"


TIMEFRAME_MAP = {
    Timeframe.M1: mt5.TIMEFRAME_M1,
    Timeframe.M5: mt5.TIMEFRAME_M5,
    Timeframe.M15: mt5.TIMEFRAME_M15,
    Timeframe.M30: mt5.TIMEFRAME_M30,
    Timeframe.H1: mt5.TIMEFRAME_H1,
    Timeframe.H4: mt5.TIMEFRAME_H4,
    Timeframe.D1: mt5.TIMEFRAME_D1,
}


class OrderRequest(BaseModel):
    symbol: str
    volume: float
    side: str  # "buy" or "sell"

    @field_validator("side")
    @classmethod
    def validate_side(cls, v: str) -> str:
        v = v.lower()
        if v not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")
        return v


app = FastAPI(title="Clio MT5 Bridge", version="0.1.0")

# Allow local tools/UI access (localhost only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    """Initialize MT5 connection on app start."""
    if not mt5.initialize():
        err = mt5.last_error()
        raise RuntimeError(f"MT5 initialize() failed: {err}")


@app.on_event("shutdown")
def shutdown() -> None:
    """Shutdown MT5 connection on app stop."""
    mt5.shutdown()


@app.get("/state")
def get_state():
    """Return basic account + open positions snapshot."""
    account = mt5.account_info()
    if account is None:
        raise HTTPException(500, "No MT5 account_info available (not logged in?)")

    positions = mt5.positions_get()
    open_positions = [p._asdict() for p in positions] if positions else []

    return {
        "server_time": datetime.utcnow().isoformat() + "Z",
        "account": account._asdict(),
        "positions": open_positions,
    }


@app.get("/positions")
def get_positions():
    """Return all open positions as a list."""
    positions = mt5.positions_get()
    return [p._asdict() for p in positions] if positions else []


@app.get("/positions/{ticket}")
def get_position(ticket: int):
    """Return a single position by ticket, or 404 if not found."""
    positions = mt5.positions_get(ticket=ticket)
    if not positions:
        raise HTTPException(404, f"No position with ticket {ticket}")
    return positions[0]._asdict()


@app.get("/market/{symbol}")
def get_market(symbol: str, timeframe: Timeframe = Timeframe.M15, bars: int = 100):
    """Return current tick and recent OHLCV history for a symbol.

    - symbol: broker symbol, e.g. "XAUUSDm"
    - timeframe: one of M1, M5, M15, M30, H1, H4, D1
    - bars: number of candles to return (max 1000)
    """
    if bars <= 0 or bars > 1000:
        raise HTTPException(400, "bars must be between 1 and 1000")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise HTTPException(400, f"No tick data for {symbol} (symbol disabled or not found)")

    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        raise HTTPException(400, f"Unsupported timeframe: {timeframe}")

    rates = mt5.copy_rates_from(symbol, tf, datetime.utcnow(), bars)
    candles = []
    if rates is not None:
        for r in rates:
            candles.append(
                {
                    "time": datetime.fromtimestamp(r["time"]).isoformat() + "Z",
                    "open": r["open"],
                    "high": r["high"],
                    "low": r["low"],
                    "close": r["close"],
                    "tick_volume": r["tick_volume"],
                }
            )

    return {
        "tick": tick._asdict(),
        "candles": candles,
    }


class CloseRequest(BaseModel):
    ticket: int


@app.post("/close")
def close_position(req: CloseRequest):
    """Close an existing position by ticket using a market order."""
    positions = mt5.positions_get(ticket=req.ticket)
    if not positions:
        raise HTTPException(404, f"No position with ticket {req.ticket}")

    pos = positions[0]
    symbol = pos.symbol
    volume = pos.volume

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise HTTPException(400, f"No tick data for {symbol} (symbol disabled or not found)")

    if pos.type == mt5.ORDER_TYPE_BUY:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL
    elif pos.type == mt5.ORDER_TYPE_SELL:
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY
    else:
        raise HTTPException(400, f"Unsupported position type: {pos.type}")

    if price is None or price <= 0:
        raise HTTPException(500, f"Invalid close price for {symbol}: {price}")

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "position": int(pos.ticket),
        "price": price,
        "deviation": 10,
        "magic": 987654,
        "comment": "clio-bridge-close",
    }

    result = mt5.order_send(request)
    if result is None:
        raise HTTPException(status_code=500, detail="mt5.order_send() returned None")

    result_dict = result._asdict()
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Close failed: {result.retcode}",
                "result": result_dict,
            },
        )

    return {"success": True, "result": result_dict}


@app.post("/orders")
def send_order(req: OrderRequest):
    """Place a simple market order with guardrails.

    This is intentionally limited: only market orders, only whitelisted symbols,
    and constrained volume / open-trade count.
    """

    # Use symbol as provided (case-sensitive) to respect broker suffixes like "EURUSDm"
    symbol = req.symbol
    if symbol not in ALLOWED_SYMBOLS:
        raise HTTPException(400, f"Symbol {symbol} is not in allowed list: {sorted(ALLOWED_SYMBOLS)}")

    # Volume guardrails
    if not (MIN_VOLUME <= req.volume <= MAX_VOLUME):
        raise HTTPException(
            400,
            f"Volume {req.volume} out of allowed range [{MIN_VOLUME}, {MAX_VOLUME}]",
        )

    # Check current open trades for this symbol
    positions = mt5.positions_get(symbol=symbol)
    open_count = len(positions) if positions else 0
    if open_count >= MAX_OPEN_TRADES:
        raise HTTPException(400, f"Max open trades reached for {symbol}: {open_count} >= {MAX_OPEN_TRADES}")

    # Get current price
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise HTTPException(400, f"No tick data for {symbol} (symbol disabled or not found)")

    if req.side == "buy":
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY
    else:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL

    if price is None or price <= 0:
        raise HTTPException(500, f"Invalid price for {symbol}: {price}")

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(req.volume),
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 987654,  # arbitrary id for bridge trades
        "comment": "clio-bridge",
    }

    result = mt5.order_send(request)
    if result is None:
        raise HTTPException(status_code=500, detail="mt5.order_send() returned None")

    result_dict = result._asdict()
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        # Return full result payload for debugging (comment, request, etc.)
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Order failed: {result.retcode}",
                "result": result_dict,
            },
        )

    return {"success": True, "result": result_dict}


if __name__ == "__main__":
    # Bind to localhost only for safety
    port = int(os.environ.get("CLIO_MT5_BRIDGE_PORT", "5001"))
    uvicorn.run("bridge:app", host="127.0.0.1", port=port, reload=False)
