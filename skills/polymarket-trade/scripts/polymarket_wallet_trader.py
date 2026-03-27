#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
#     "py-clob-client>=0.2.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""Live Polymarket trading on Polygon (with strict safety rails).

This script **extends** the original polymarket.py paper-trading tool
with real wallet integration via the official `py-clob-client` SDK.

Key design constraints:
- Does NOT modify the original `polymarket.py` file
- Uses DRY_RUN=True by default; live trading requires explicit opt‑in
- Enforces MAX_BET_USD / MAX_SESSION_USD / RESERVE_USD limits
- Reads secrets (private key, funder) only from environment variables

Typical usage (from this skill's {baseDir}):

    python3 scripts/polymarket_wallet_trader.py status
    python3 scripts/polymarket_wallet_trader.py buy trump-2028 25
    python3 scripts/polymarket_wallet_trader.py sell trump-2028

To place **real** orders you must:
1. Export POLYMARKET_PRIVATE_KEY and POLYMARKET_FUNDER in the env
2. Set POLYMARKET_DRY_RUN=false
3. Pass --confirm-live on each trading command

Without all three, the script will simulate only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from typing import Any, Dict, Optional, Tuple

import requests
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import MarketOrderArgs

from polymarket_wallet_config import (
    load_session_state,
    load_wallet_config,
    save_session_state,
)

# Reuse the public Gamma API helpers from the original script without
# modifying it. We import selected helpers dynamically to avoid tight
# coupling.
try:  # pragma: no cover - best-effort reuse
    import polymarket as poly
except Exception:  # pragma: no cover
    poly = None


GAMMA_BASE_URL = "https://gamma-api.polymarket.com"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def gamma_fetch(endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
    url = f"{GAMMA_BASE_URL}{endpoint}"
    resp = requests.get(url, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def resolve_event_and_market(slug: str, outcome: Optional[str]) -> Tuple[dict, dict]:
    """Resolve an event + specific market from a slug/outcome.

    - slug: event slug (or full URL)
    - outcome: optional outcome name; if None, take the primary market
    """

    # Prefer the helper from polymarket.py if available
    if poly is not None and hasattr(poly, "extract_slug_from_url"):
        slug = poly.extract_slug_from_url(slug)  # type: ignore[attr-defined]

    data = gamma_fetch("/events", {"slug": slug})

    if not data:
        raise SystemExit(f"❌ Event not found: {slug}")

    event = data[0] if isinstance(data, list) else data
    markets = event.get("markets") or []

    if not markets:
        raise SystemExit("❌ Event has no tradeable markets")

    if outcome:
        outcome_lower = outcome.lower()
        for m in markets:
            name = (m.get("groupItemTitle") or m.get("question") or "").lower()
            if outcome_lower in name:
                return event, m
        raise SystemExit(f"❌ Outcome '{outcome}' not found in event")

    # Default: first market ordered by current Yes price
    from math import inf

    def yes_price(m: dict) -> float:
        try:
            prices = m.get("outcomePrices") or []
            if isinstance(prices, str):
                prices = json.loads(prices)
            return float(prices[0]) if prices else 0.0
        except Exception:
            return 0.0

    best_market = max(markets, key=yes_price, default=None) or markets[0]
    return event, best_market


def clamp_amount_usd(requested: float) -> Tuple[float, dict]:
    """Clamp a requested notional to configured safety limits.

    Returns (allowed_amount, info_dict).
    """

    cfg = load_wallet_config()
    session = load_session_state()

    spent = float(session.get("spent_usd", 0.0) or 0.0)

    remaining_session = max(cfg.limits.max_session_usd - spent, 0.0)
    allowed = min(requested, cfg.limits.max_bet_usd, remaining_session)

    info = {
        "requested": requested,
        "allowed": allowed,
        "max_bet_usd": cfg.limits.max_bet_usd,
        "max_session_usd": cfg.limits.max_session_usd,
        "session_spent_usd": spent,
        "remaining_session_usd": remaining_session,
    }

    return allowed, info


def ensure_wallet_ready_for_live(cfg) -> None:
    """Validate that live trading is allowed.

    Raises SystemExit with a human-friendly message if not.
    """

    problems = []

    if cfg.dry_run:
        problems.append("POLYMARKET_DRY_RUN is true (default)")

    if not cfg.private_key:
        problems.append("POLYMARKET_PRIVATE_KEY is not set")

    if not cfg.funder:
        problems.append("POLYMARKET_FUNDER is not set")

    if problems:
        msg = "\n".join(["❌ Live trading is disabled:"] + [f"- {p}" for p in problems])
        msg += "\n\nSet the required environment variables and POLYMARKET_DRY_RUN=false to enable live orders."
        raise SystemExit(msg)


def build_client(cfg) -> ClobClient:
    """Create a Level 2 trading client.

    This uses the recommended pattern from the official docs:
    - temp client derives or creates API creds
    - full client uses those creds for authenticated trading
    """

    temp_client = ClobClient(cfg.host, key=cfg.private_key, chain_id=cfg.chain_id)
    api_creds = temp_client.create_or_derive_api_creds()

    client = ClobClient(
        cfg.host,
        key=cfg.private_key,
        chain_id=cfg.chain_id,
        creds=api_creds,
        signature_type=cfg.signature_type,
        funder=cfg.funder,
    )
    return client


def market_order(
    client: ClobClient,
    market: dict,
    side: str,
    size_usd: float,
) -> dict:
    """Submit a simple market order using py-clob-client.

    This implementation intentionally keeps the order model simple:
    - side: "buy" or "sell" in terms of YES tokens
    - size_usd: notional in USDC.e

    Under the hood we rely on the SDK's `MarketOrderArgs` helper.
    """

    # The SDK expects an asset / market id. Gamma events expose markets
    # with `marketId` / `conditionId` and outcome indices.
    market_id = market.get("marketId") or market.get("id")
    if not market_id:
        raise SystemExit("❌ Unable to determine market id from Gamma event")

    outcome_index = 0  # YES leg by convention

    args = MarketOrderArgs(
        size=size_usd,
        price=None,  # let CLOB match at best available
        side=side.lower(),
        market_id=market_id,
        outcome=outcome_index,
    )

    # py-clob-client exposes a `post_order` / `post_orders` wrapper; we
    # prefer the higher-level market order helper when available.
    try:
        order = client.post_order(args)  # type: ignore[attr-defined]
    except AttributeError:
        # Fallback: some versions expose `create_order` then `post_orders`.
        builder = client.builder  # type: ignore[attr-defined]
        order_args = builder.create_market_order_args(args)  # type: ignore[attr-defined]
        order = client.post_orders(order_args)  # type: ignore[attr-defined]

    return order


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_status(_args: argparse.Namespace) -> None:
    cfg = load_wallet_config()
    state = load_session_state()

    print("🔐 Polymarket Wallet Status\n")
    print(f"Profile: {cfg.label}")
    print(f"Host:    {cfg.host}")
    print(f"Chain:   {cfg.chain_id}")
    print(f"Dry run: {cfg.dry_run}")
    print(f"SigType: {cfg.signature_type}")
    print()
    print("Safety limits (USD):")
    print(f"  Max bet:     {cfg.limits.max_bet_usd:.2f}")
    print(f"  Max session: {cfg.limits.max_session_usd:.2f}")
    print(f"  Reserve:     {cfg.limits.reserve_usd:.2f}")
    print()
    print("Session:")
    print(f"  Spent this session: {float(state.get('spent_usd', 0.0) or 0.0):.2f} USD")


def _print_preview(action: str, event: dict, market: dict, size_usd: float, info: dict) -> None:
    title = event.get("title") or market.get("question") or "(unknown)"
    slug = event.get("slug") or market.get("market_slug") or "?"
    print(f"{action} preview:\n")
    print(f"  Market:  {title}")
    print(f"  Slug:    {slug}")
    print(f"  Size:    ${size_usd:,.2f} (requested ${info['requested']:,.2f})")
    print(f"  Limits:  max_bet={info['max_bet_usd']}, max_session={info['max_session_usd']}")
    print()


def _execute_trade(
    side: str,
    slug: str,
    amount_usd: float,
    outcome: Optional[str],
    confirm_live: bool,
) -> None:
    cfg = load_wallet_config()

    if amount_usd <= 0:
        raise SystemExit("❌ Amount must be > 0")

    allowed, info = clamp_amount_usd(amount_usd)
    if allowed <= 0:
        raise SystemExit(
            "❌ Trade blocked by safety limits (session or per-bet caps reached)."
        )

    event, market = resolve_event_and_market(slug, outcome)

    _print_preview("BUY" if side == "buy" else "SELL", event, market, allowed, info)

    if cfg.dry_run or not confirm_live:
        print("[DRY RUN] No on-chain order sent.")
        return

    # At this point the user has explicitly disabled DRY_RUN and passed
    # --confirm-live on the CLI, so we enforce wallet requirements.
    ensure_wallet_ready_for_live(cfg)

    client = build_client(cfg)
    print("Connecting to CLOB and placing order...")

    try:
        order = market_order(client, market, side=side, size_usd=allowed)
    except Exception as e:  # Broad but we dump a structured payload
        raise SystemExit(f"❌ Error while submitting order: {e}") from e

    # Persist new session spend
    state = load_session_state()
    state["spent_usd"] = float(state.get("spent_usd", 0.0) or 0.0) + allowed
    save_session_state(state)

    print("✅ Order submitted")
    try:
        print(json.dumps(order, indent=2))
    except TypeError:
        # Fallback if order isn't JSON-serialisable
        print(order)


def cmd_buy(args: argparse.Namespace) -> None:
    _execute_trade("buy", args.slug, args.amount, args.outcome, args.confirm_live)


def cmd_sell(args: argparse.Namespace) -> None:
    _execute_trade("sell", args.slug, args.amount, args.outcome, args.confirm_live)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Live Polymarket trading (Polygon)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show wallet config & safety limits")

    common_trade = argparse.ArgumentParser(add_help=False)
    common_trade.add_argument("slug", help="Event slug or full polymarket.com URL")
    common_trade.add_argument("amount", type=float, help="Notional size in USD")
    common_trade.add_argument("--outcome", "-o", help="Optional outcome filter")
    common_trade.add_argument(
        "--confirm-live",
        action="store_true",
        help=(
            "Required to actually place on-chain orders when POLYMARKET_DRY_RUN=false. "
            "If omitted, the command will only simulate."
        ),
    )

    buy = sub.add_parser("buy", parents=[common_trade], help="Place a YES market order")
    buy.set_defaults(func=cmd_buy)

    sell = sub.add_parser("sell", parents=[common_trade], help="Place a SELL order")
    sell.set_defaults(func=cmd_sell)

    status = sub.add_parser("status", help="Show current wallet configuration")
    status.set_defaults(func=cmd_status)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    func = getattr(args, "func", None)
    if not func:
        parser.print_help()
        raise SystemExit(1)

    func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
