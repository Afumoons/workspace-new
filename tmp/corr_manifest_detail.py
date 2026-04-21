import json
from pathlib import Path
from collections import Counter, defaultdict

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
manifest_path = root / 'strategies' / 'live_manifest.json'
pool_path = root / 'strategies' / 'pool_state.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'entries': []}
pool = json.loads(pool_path.read_text(encoding='utf-8')) if pool_path.exists() else {}
entries = manifest.get('entries') or []

# attach best_regime and routing meta from embedded stats
by_symbol = defaultdict(list)
for e in entries:
    stats = e.get('stats') or {}
    meta = ((stats.get('strategy_explain') or {}).get('meta') or {})
    by_symbol[e.get('symbol','unknown')].append({
        'name': e.get('name'),
        'status': e.get('status'),
        'rank': e.get('manifest_rank'),
        'score': round(float(e.get('score',0) or 0),4),
        'family': e.get('family','unknown'),
        'best_regime': meta.get('best_regime','unknown'),
        'routing_conf': round(float(meta.get('routing_confidence',0) or 0),4),
        'specialist': round(float(meta.get('specialist_score',0) or 0),4),
        'wf': round(float(stats.get('wf_overall_sharpe',0) or 0),4),
    })

for symbol, rows in sorted(by_symbol.items()):
    print(f'\\nSYMBOL={symbol} manifest_entries={len(rows)}')
    regime_cnt = Counter(r['best_regime'] for r in rows)
    print('regime_mix', dict(regime_cnt))
    print('top_rows')
    for r in sorted(rows, key=lambda x: x['rank'])[:16]:
        print(r)
