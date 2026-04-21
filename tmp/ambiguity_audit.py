import json
from pathlib import Path
from collections import defaultdict

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
pool_path = root / 'strategies' / 'pool_state.json'
if not pool_path.exists():
    print('POOL_MISSING')
    raise SystemExit(0)

pool = json.loads(pool_path.read_text(encoding='utf-8'))
records = list(pool.values()) if isinstance(pool, dict) else []

rows = []
for rec in records:
    stats = rec.get('stats') or {}
    explain = stats.get('strategy_explain') or {}
    meta = explain.get('meta') or {}
    row = {
        'name': rec.get('name'),
        'symbol': rec.get('symbol'),
        'status': rec.get('status'),
        'score': float(rec.get('score', 0.0) or 0.0),
        'num_trades': float(stats.get('num_trades', 0.0) or 0.0),
        'same_bar_ambiguity_count': float(stats.get('same_bar_ambiguity_count', 0.0) or 0.0),
        'same_bar_ambiguity_rate': float(stats.get('same_bar_ambiguity_rate', 0.0) or 0.0),
        'wf': float(stats.get('wf_overall_sharpe', 0.0) or 0.0),
        'best_regime': meta.get('best_regime', 'unknown'),
    }
    rows.append(row)

with_ambiguity = [r for r in rows if r['same_bar_ambiguity_count'] > 0]
print('TOTAL_RECORDS', len(rows))
print('WITH_AMBIGUITY', len(with_ambiguity))

by_status = defaultdict(lambda: {'count':0, 'amb':0, 'amb_sum':0.0, 'rate_sum':0.0})
by_symbol = defaultdict(lambda: {'count':0, 'amb':0, 'amb_sum':0.0, 'rate_sum':0.0})
for r in rows:
    s = by_status[r['status']]
    s['count'] += 1
    if r['same_bar_ambiguity_count'] > 0:
        s['amb'] += 1
    s['amb_sum'] += r['same_bar_ambiguity_count']
    s['rate_sum'] += r['same_bar_ambiguity_rate']

    y = by_symbol[r['symbol']]
    y['count'] += 1
    if r['same_bar_ambiguity_count'] > 0:
        y['amb'] += 1
    y['amb_sum'] += r['same_bar_ambiguity_count']
    y['rate_sum'] += r['same_bar_ambiguity_rate']

print('\nBY_STATUS')
for k,v in sorted(by_status.items()):
    print(k, {
        'records': v['count'],
        'with_ambiguity': v['amb'],
        'avg_ambiguity_count': round(v['amb_sum']/v['count'], 4) if v['count'] else 0.0,
        'avg_ambiguity_rate': round(v['rate_sum']/v['count'], 6) if v['count'] else 0.0,
    })

print('\nBY_SYMBOL')
for k,v in sorted(by_symbol.items()):
    print(k, {
        'records': v['count'],
        'with_ambiguity': v['amb'],
        'avg_ambiguity_count': round(v['amb_sum']/v['count'], 4) if v['count'] else 0.0,
        'avg_ambiguity_rate': round(v['rate_sum']/v['count'], 6) if v['count'] else 0.0,
    })

print('\nTOP_BY_AMBIGUITY_COUNT')
for r in sorted(with_ambiguity, key=lambda x: (x['same_bar_ambiguity_count'], x['same_bar_ambiguity_rate'], x['score']), reverse=True)[:20]:
    print({k: r[k] for k in ['name','symbol','status','same_bar_ambiguity_count','same_bar_ambiguity_rate','num_trades','wf','score','best_regime']})

print('\nTOP_BY_AMBIGUITY_RATE')
for r in sorted(with_ambiguity, key=lambda x: (x['same_bar_ambiguity_rate'], x['same_bar_ambiguity_count']), reverse=True)[:20]:
    print({k: r[k] for k in ['name','symbol','status','same_bar_ambiguity_count','same_bar_ambiguity_rate','num_trades','wf','score','best_regime']})
