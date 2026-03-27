#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "python-dotenv>=1.0.0",
# ]
# ///
"""Shared configuration and safety limits for live Polymarket trading.

This module is intentionally self-contained and does NOT depend on the
original polymarket.py script. It only reads environment variables and
stores **non‑sensitive** configuration on disk.

Secrets (private keys, funder addresses, API keys) MUST come from
environment variables, never from checked-in files.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:  # Optional; script works without python-dotenv
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover - optional import
    def load_dotenv(*_args, **_kwargs):  # type: ignore
        return False


DATA_DIR = Path.home() / ".polymarket"
CONFIG_PATH = DATA_DIR / "wallet_config.json"
SESSION_PATH = DATA_DIR / "wallet_session_state.json"


@dataclass
class SafetyLimits:
    """Per-session and per-trade safety limits in USD.

    These are **soft caps** enforced by this helper; the on-chain
    contracts obviously do not know about them. They are designed to
    match the multi‑phase trading instructions used by the agent.
    """

    max_bet_usd: float = 25.0        # Max per single order
    max_session_usd: float = 100.0   # Max total notional per session
    reserve_usd: float = 50.0        # Capital that must remain untouched


@dataclass
class WalletConfig:
    """Resolved wallet + trading configuration.

    DRY_RUN defaults to **True** and must be explicitly disabled via env.
    """

    # CLOB / chain
    host: str = "https://clob.polymarket.com"
    chain_id: int = 137

    # Secrets (from env only)
    private_key: Optional[str] = None
    funder: Optional[str] = None

    # Signature / wallet type
    # 0 = EOA, 1/2 = proxy / Magic / browser wallets
    signature_type: int = 0

    # Trading behaviour
    dry_run: bool = True
    limits: SafetyLimits = SafetyLimits()

    # Optional label for logs
    label: str = "default"


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _to_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except Exception:
        return default


def load_wallet_config() -> WalletConfig:
    """Load config from environment variables.

    Environment variables (all optional, but required for LIVE trading):

    - POLYMARKET_PRIVATE_KEY   (required for live orders)
    - POLYMARKET_FUNDER        (required for live orders)
    - POLYMARKET_SIGNATURE_TYPE (0/1/2, default 0)
    - POLYMARKET_HOST          (default https://clob.polymarket.com)
    - POLYMARKET_CHAIN_ID      (default 137)
    - POLYMARKET_DRY_RUN       (default true)

    Safety limits (USD):
    - POLYMARKET_MAX_BET_USD
    - POLYMARKET_MAX_SESSION_USD
    - POLYMARKET_RESERVE_USD
    """

    # Best-effort .env loading for local dev; safe in production since
    # it only affects this process environment.
    try:
        load_dotenv()
    except Exception:
        pass

    host = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com").strip()
    chain_id = int(os.getenv("POLYMARKET_CHAIN_ID", "137"))

    private_key = os.getenv("POLYMARKET_PRIVATE_KEY") or None
    funder = os.getenv("POLYMARKET_FUNDER") or None

    sig_type = int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "0"))

    dry_run = _to_bool(os.getenv("POLYMARKET_DRY_RUN"), default=True)

    limits = SafetyLimits(
        max_bet_usd=_to_float(os.getenv("POLYMARKET_MAX_BET_USD"), 25.0),
        max_session_usd=_to_float(os.getenv("POLYMARKET_MAX_SESSION_USD"), 100.0),
        reserve_usd=_to_float(os.getenv("POLYMARKET_RESERVE_USD"), 50.0),
    )

    label = os.getenv("POLYMARKET_PROFILE_LABEL", "default")

    return WalletConfig(
        host=host,
        chain_id=chain_id,
        private_key=private_key,
        funder=funder,
        signature_type=sig_type,
        dry_run=dry_run,
        limits=limits,
        label=label,
    )


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_session_state() -> dict:
    """Load per-session state (e.g., cumulative notional).

    This is **not** security sensitive – it only tracks how much
    the agent has traded in this environment.
    """

    ensure_data_dir()
    if not SESSION_PATH.exists():
        return {"spent_usd": 0.0, "session_label": None}

    try:
        import json

        return json.loads(SESSION_PATH.read_text())
    except Exception:
        return {"spent_usd": 0.0, "session_label": None}


def save_session_state(state: dict) -> None:
    ensure_data_dir()
    try:
        import json

        SESSION_PATH.write_text(json.dumps(state, indent=2))
    except Exception:
        # Non-fatal; trading logic should still proceed but without
        # persistent session tracking.
        pass


__all__ = [
    "SafetyLimits",
    "WalletConfig",
    "load_wallet_config",
    "load_session_state",
    "save_session_state",
]
