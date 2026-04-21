import pandas as pd
from autonomous_trading_ai.strategies.generator import random_strategy
from autonomous_trading_ai.backtests.engine import run_backtest

times = pd.date_range('2026-01-01', periods=120, freq='15min')
df = pd.DataFrame({
    'time': times,
    'open': [100 + i * 0.1 for i in range(120)],
    'high': [100 + i * 0.1 + 0.4 for i in range(120)],
    'low': [100 + i * 0.1 - 0.4 for i in range(120)],
    'close': [100 + i * 0.1 + 0.05 for i in range(120)],
    'ma_short': [100 + i * 0.1 for i in range(120)],
    'ma_long': [99.5 + i * 0.09 for i in range(120)],
    'rsi': [55] * 120,
    'trend_strength': [0.2] * 120,
    'atr': [0.8] * 120,
    'volatility': [1.0] * 120,
    'regime': ['trending_up'] * 120,
    'regime_class': ['trend'] * 120,
    'regime_type': ['uptrend_weak'] * 120,
    'regime_confidence': [0.7] * 120,
    'vol_regime': ['normal'] * 120,
    'session_london': [1] * 120,
    'session_new_york': [0] * 120,
    'in_news_lockout': [False] * 120,
})

strat = random_strategy('XAUUSDm', 'M15', family='ma_trend')
res = run_backtest(
    df,
    strat,
    regime_column='regime',
    spread=0.35,
    commission_per_lot=7.0,
    slippage_pips=2.0,
    max_positions_total=1,
    max_positions_per_strategy=1,
)
print({
    'trades': len(res.trades),
    'avg_holding_bars': ((res.stats.get('strategy_explain', {}) or {}).get('risk_behavior', {}) or {}).get('avg_holding_bars'),
    'meta': ((res.stats.get('strategy_explain', {}) or {}).get('meta', {}) or {}),
})
