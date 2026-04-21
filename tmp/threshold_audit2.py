import json
from pathlib import Path
from collections import defaultdict

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
pool_path = root / 'strategies' / 'pool_state.json'
data = json.loads(pool_path.read_text(encoding='utf-8'))
records = list(data.values()) if isinstance(data, dict) else []

per_symbol = defaultdict(lambda: {'active':0,'exploratory':0,'candidate':0,'disabled':0})
mins = defaultdict(lambda: 999999.0)
maxs = defaultdict(lambda: -999999.0)
low_samples = defaultdict(list)

for rec in records:
    status = rec.get('status','unknown')
    symbol = rec.get('symbol','unknown')
    stats = rec.get('stats') or {}
    ex = stats.get('strategy_explain') or {}
    rp = ex.get('regime_pnl') or {}
    best_edge = -999.0
    for v in rp.values():
        try:
            edge = float((v or {}).get('return_pct', -999.0) or -999.0)
        except Exception:
            edge = -999.0
        if edge > best_edge:
            best_edge = edge
    per_symbol[symbol][status] += 1
    mins[(symbol,status)] = min(mins[(symbol,status)], best_edge)
    maxs[(symbol,status)] = max(maxs[(symbol,status)], best_edge)
    if best_edge < 1.0 and len(low_samples[(symbol,status)]) < 8:
        low_samples[(symbol,status)].append((rec.get('name'), round(best_edge,4), round(float(stats.get('wf_overall_sharpe',0) or 0),4), round(float(rec.get('score',0) or 0),4)))

print('PER_SYMBOL_STATUS')
for symbol, counts in sorted(per_symbol.items()):
    print(symbol, counts)
print('\nEDGE_RANGES')
for key in sorted(mins):
    mn = mins[key]
    mx = maxs[key]
    print(key, {'min_best_edge': None if mn > 900000 else round(mn,4), 'max_best_edge': None if mx < -900000 else round(mx,4)})
print('\nLOW_EDGE_SAMPLES(<1.0)')
for key in sorted(low_samples):
    if low_samples[key]:
        print(key, low_samples[key])
