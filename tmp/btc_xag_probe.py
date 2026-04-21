from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autonomous_trading_ai.research.features import load_features
from autonomous_trading_ai.backtests.engine import run_backtest
from autonomous_trading_ai.backtests.evaluation import evaluate_strategy
from autonomous_trading_ai.backtests.walkforward import walk_forward_test
from autonomous_trading_ai.backtests.monte_carlo import monte_carlo_pnl
from autonomous_trading_ai.strategies.generator import load_strategy
from autonomous_trading_ai.scheduler.main import _research_backtest_kwargs, _cheap_prescreen_backtest_kwargs

base = Path('autonomous_trading_ai/strategies/generated')
items = [
    ('BTCUSDm', 'core15_BTCUSDm_M15_275e.json'),
    ('BTCUSDm', 'core15_BTCUSDm_M15_0338.json'),
    ('BTCUSDm', 'core15_BTCUSDm_M15_924b.json'),
    ('XAGUSDm', 'pullback_trend_XAGUSDc_M15_4e9e.json'),
    ('XAGUSDm', 'session_breakout_XAGUSDc_M15_ba70.json'),
]
for canon, file in items:
    feat = load_features(canon, 'M15')
    strat = load_strategy(base / file)
    cheap_kwargs = _cheap_prescreen_backtest_kwargs(canon)
    bt_kwargs = _research_backtest_kwargs(canon)
    cheap = run_backtest(feat, strat, regime_column='regime', **cheap_kwargs)
    bt = run_backtest(feat, strat, regime_column='regime', **bt_kwargs)
    ev = evaluate_strategy(bt.stats)
    wf = walk_forward_test(feat, strat, **bt_kwargs)
    mc = monte_carlo_pnl(
        bt.trades,
        n_runs=200,
        slippage_std_pips=max(0.5, bt_kwargs['slippage_pips'] * 0.5),
        pip_size=0.01 if 'XAU' in canon else 1.0,
        method='block' if len(bt.trades) >= 12 else 'shuffle',
        block_size=4 if len(bt.trades) >= 24 else 3,
        initial_equity=float(ev.get('initial_equity', 10000.0) or 10000.0),
    )
    print(f'### {file}')
    print('cheap', {k: cheap.stats.get(k) for k in ['num_trades', 'profit_factor', 'sharpe_ratio', 'max_drawdown_pct']})
    print('bt', {k: bt.stats.get(k) for k in ['num_trades', 'profit_factor', 'sharpe_ratio', 'max_drawdown_pct', 'return_pct']})
    print('eval', {'accepted': ev.get('accepted'), 'score': ev.get('score')})
    print('wf', wf.get('aggregate', {}))
    print('mc', {k: mc.get(k) for k in ['mc_final_pnl_mean', 'mc_final_pnl_p5', 'mc_loss_prob', 'mc_max_dd_p95']})
    print()
