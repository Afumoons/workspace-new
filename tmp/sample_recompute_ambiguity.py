import json
from pathlib import Path
import pandas as pd

from autonomous_trading_ai.backtests.engine import run_backtest
from autonomous_trading_ai.research.features import load_features
from autonomous_trading_ai.strategies.live_manifest import load_live_manifest, strategy_definition_from_manifest_entry

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
manifest = load_live_manifest(root / 'strategies' / 'live_manifest.json')
entries = manifest.get('entries') or []

selected = []
for symbol in ['XAUUSDm', 'BTCUSDm']:
    slot = [e for e in entries if e.get('symbol') == symbol and e.get('status') == 'active']
    selected.extend(sorted(slot, key=lambda e: int(e.get('manifest_rank', 9999)))[:8])

for symbol in ['XAUUSDm', 'BTCUSDm']:
    slot = [e for e in entries if e.get('symbol') == symbol and e.get('status') == 'exploratory']
    selected.extend(sorted(slot, key=lambda e: int(e.get('manifest_rank', 9999)))[:5])

# de-dup by name just in case
seen = set()
unique = []
for e in selected:
    name = e.get('name')
    if name and name not in seen:
        seen.add(name)
        unique.append(e)

results = []
for e in unique:
    strat = strategy_definition_from_manifest_entry(e)
    try:
        feat = load_features(strat.symbol, strat.timeframe)
    except Exception as ex:
        results.append({'name': strat.name, 'symbol': strat.symbol, 'status': e.get('status'), 'error': f'load_features_failed: {ex}'})
        continue
    try:
        res = run_backtest(
            feat,
            strat,
            regime_column='regime',
            spread=float((e.get('stats') or {}).get('spread', 0.0) or 0.0),
            commission_per_lot=float((e.get('stats') or {}).get('commission_per_lot', 0.0) or 0.0),
            slippage_pips=float((e.get('stats') or {}).get('slippage_pips', 0.0) or 0.0),
            max_positions_total=1,
            max_positions_per_strategy=1,
        )
        stats = res.stats or {}
        results.append({
            'name': strat.name,
            'symbol': strat.symbol,
            'status': e.get('status'),
            'manifest_rank': e.get('manifest_rank'),
            'num_trades': float(stats.get('num_trades', 0.0) or 0.0),
            'same_bar_ambiguity_count': float(stats.get('same_bar_ambiguity_count', 0.0) or 0.0),
            'same_bar_ambiguity_rate': float(stats.get('same_bar_ambiguity_rate', 0.0) or 0.0),
            'return_pct': float(stats.get('return_pct', 0.0) or 0.0),
            'wf': float(stats.get('wf_overall_sharpe', 0.0) or 0.0),
        })
    except Exception as ex:
        results.append({'name': strat.name, 'symbol': strat.symbol, 'status': e.get('status'), 'error': f'backtest_failed: {ex}'})

ok = [r for r in results if 'error' not in r]
print('RECOMPUTED', len(ok), 'of', len(results))
print('WITH_AMBIGUITY', sum(1 for r in ok if r['same_bar_ambiguity_count'] > 0))

by_symbol = {}
for symbol in sorted(set(r['symbol'] for r in ok)):
    rows = [r for r in ok if r['symbol'] == symbol]
    by_symbol[symbol] = {
        'count': len(rows),
        'with_ambiguity': sum(1 for r in rows if r['same_bar_ambiguity_count'] > 0),
        'avg_ambiguity_count': round(sum(r['same_bar_ambiguity_count'] for r in rows)/len(rows), 4) if rows else 0.0,
        'avg_ambiguity_rate': round(sum(r['same_bar_ambiguity_rate'] for r in rows)/len(rows), 6) if rows else 0.0,
        'max_ambiguity_count': max((r['same_bar_ambiguity_count'] for r in rows), default=0.0),
        'max_ambiguity_rate': max((r['same_bar_ambiguity_rate'] for r in rows), default=0.0),
    }
print('BY_SYMBOL', by_symbol)

print('\nTOP_RESULTS_BY_AMBIGUITY')
for r in sorted(ok, key=lambda x: (x['same_bar_ambiguity_count'], x['same_bar_ambiguity_rate']), reverse=True):
    print(r)

errs = [r for r in results if 'error' in r]
if errs:
    print('\nERRORS')
    for r in errs:
        print(r)
