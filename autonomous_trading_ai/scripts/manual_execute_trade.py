from __future__ import annotations

from autonomous_trading_ai.execution.engine import execute_trade


def main() -> None:
    res = execute_trade(
        strategy_name="manual_test_xau",
        symbol="XAUUSDm",
        direction="long",
        risk_perc=0.5,
        stop_loss_pips=150,
        take_profit_pips=150,
        pip_size=0.01,
    )
    print(res)


if __name__ == "__main__":
    main()
