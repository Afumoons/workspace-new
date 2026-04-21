from pathlib import Path
import sys
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autonomous_trading_ai.research.features import load_features
from autonomous_trading_ai.backtests.engine import run_backtest
from autonomous_trading_ai.backtests.evaluation import evaluate_strategy
from autonomous_trading_ai.backtests.walkforward import walk_forward_test
from autonomous_trading_ai.backtests.monte_carlo import monte_carlo_pnl
from autonomous_trading_ai.strategies.generator import random_strategy, load_strategy
from autonomous_trading_ai.scheduler.main import (
    _cheap_prescreen_backtest_kwargs,
    _research_backtest_kwargs,
    _passes_symbol_specific_mc_tail_relief,
)


def btc_probe():
    feat = load_features('BTCUSDm', 'M15')
    base = ROOT / 'autonomous_trading_ai' / 'strategies' / 'generated'
    files = [
        'core15_BTCUSDm_M15_275e.json',
        'core15_BTCUSDm_M15_0338.json',
        'core15_BTCUSDm_M15_924b.json',
    ]
    out = []
    bt_kwargs = _research_backtest_kwargs('BTCUSDm')
    for file in files:
        strat = load_strategy(base / file)
        bt = run_backtest(feat, strat, regime_column='regime', **bt_kwargs)
        ev = evaluate_strategy(bt.stats)
        wf = walk_forward_test(feat, strat, **bt_kwargs)
        mc = monte_carlo_pnl(
            bt.trades,
            n_runs=200,
            slippage_std_pips=max(0.5, bt_kwargs['slippage_pips'] * 0.5),
            pip_size=1.0,
            method='block' if len(bt.trades) >= 12 else 'shuffle',
            block_size=4 if len(bt.trades) >= 24 else 3,
            initial_equity=float(ev.get('initial_equity', 10000.0) or 10000.0),
        )
        family = 'mixed:ma_trend+rsi_range'
        relief = _passes_symbol_specific_mc_tail_relief(
            symbol='BTCUSDm', family=family,
            num_trades=float(ev.get('num_trades', 0.0) or 0.0),
            pf=float(ev.get('profit_factor', 0.0) or 0.0),
            sharpe=float(ev.get('sharpe_ratio', 0.0) or 0.0),
            dd_abs=abs(float(ev.get('max_drawdown_pct', 0.0) or 0.0)),
            wf_sharpe=float(wf.get('aggregate', {}).get('overall_sharpe', 0.0) or 0.0),
            mc_p5=float(mc.get('mc_final_pnl_p5', 0.0) or 0.0),
            mc_loss_prob=float(mc.get('mc_loss_prob', 0.0) or 0.0),
            mc_dd_p95=float(mc.get('mc_max_dd_p95', 0.0) or 0.0),
        )
        out.append({
            'file': file,
            'accepted': bool(ev.get('accepted')),
            'num_trades': ev.get('num_trades'),
            'pf': round(float(ev.get('profit_factor', 0.0) or 0.0), 3),
            'sharpe': round(float(ev.get('sharpe_ratio', 0.0) or 0.0), 3),
            'wf_sharpe': round(float(wf.get('aggregate', {}).get('overall_sharpe', 0.0) or 0.0), 3),
            'mc_p5': round(float(mc.get('mc_final_pnl_p5', 0.0) or 0.0), 2),
            'mc_loss_prob': round(float(mc.get('mc_loss_prob', 0.0) or 0.0), 3),
            'mc_dd_p95': round(float(mc.get('mc_max_dd_p95', 0.0) or 0.0), 2),
            'relief': relief,
        })
    return out


def xag_probe():
    feat = load_features('XAGUSDm', 'M15')
    families = ['session_breakout', 'vol_breakout', 'compression_breakout', 'pullback_trend', 'rsi_range']
    cheap_kwargs = _cheap_prescreen_backtest_kwargs('XAGUSDm')
    out = {}
    for family in families:
        counts = defaultdict(int)
        trade_counts = []
        for _ in range(12):
            strat = random_strategy('XAGUSDm', 'M15', family=family)
            res = run_backtest(feat, strat, regime_column='regime', **cheap_kwargs)
            stats = res.stats or {}
            tr = int(stats.get('num_trades', 0) or 0)
            pf = float(stats.get('profit_factor', 0.0) or 0.0)
            sh = float(stats.get('sharpe_ratio', 0.0) or 0.0)
            dd = abs(float(stats.get('max_drawdown_pct', 0.0) or 0.0))
            trade_counts.append(tr)
            if tr == 0:
                counts['zero_trade'] += 1
            if tr >= 20 and pf >= 0.95 and sh >= -0.10 and dd <= 35.0:
                counts['cheap_pass'] += 1
            else:
                counts['cheap_fail'] += 1
        out[family] = {
            'cheap_pass': counts['cheap_pass'],
            'cheap_fail': counts['cheap_fail'],
            'zero_trade': counts['zero_trade'],
            'max_trades': max(trade_counts),
            'avg_trades': round(sum(trade_counts) / len(trade_counts), 2),
        }
    return out


print({'btc': btc_probe(), 'xag': xag_probe()})
