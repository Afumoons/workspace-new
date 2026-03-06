import os
from datetime import datetime

import MetaTrader5 as mt5
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import uvicorn


# --- Simple risk/config guardrails ---
# Whitelist of broker symbols we allow the bridge to trade.
# Adjust this list to match your broker's symbol names (e.g. "EURUSDm").
ALLOWED_SYMBOLS = {"EURUSDm", "XAUUSDm", "BTCUSDm", "ETHUSDm"}
MAX_VOLUME = 1.0        # max lots per trade
MIN_VOLUME = 0.01       # min lots per trade
MAX_OPEN_TRADES = 5     # per symbol (simple guardrail)


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
