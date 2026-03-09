from dataclasses import dataclass


@dataclass
class RiskConfig:
    max_risk_per_trade_pct: float = 0.5  # 0.5% of equity
    max_portfolio_drawdown_pct: float = 20.0
    max_open_positions: int = 10


@dataclass
class DataConfig:
    mt5_timeframe_default: str = "M15"
    history_bars_default: int = 2000


@dataclass
class SchedulerConfig:
    enable_scheduler: bool = True


risk_config = RiskConfig()
data_config = DataConfig()
scheduler_config = SchedulerConfig()
