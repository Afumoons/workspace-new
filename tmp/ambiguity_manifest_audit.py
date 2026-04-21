import json
from pathlib import Path

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
manifest_path = root / 'strategies' / 'live_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'entries': []}
rows = []
for e in (manifest.get('entries') or []):
    stats = e.get('stats') or {}
    explain = stats.get('strategy_explain') or {}
    meta = explain.get('meta') or {}
    rows.append({
        'name': e.get('name'),
        'symbol': e.get('symbol'),
        'status': e.get('status'),
        'rank': e.get('manifest_rank'),
        'same_bar_ambiguity_count': float(stats.get('same_bar_ambiguity_count', 0.0) or 0.0),
        'same_bar_ambiguity_rate': float(stats.get('same_bar_ambiguity_rate', 0.0) or 0.0),
        'num_trades': float(stats.get('num_trades', 0.0) or 0.0),
        'wf': float(stats.get('wf_overall_sharpe', 0.0) or 0.0),
        'best_regime': meta.get('best_regime', 'unknown'),
    })
print('LIVE_MANIFEST_ENTRIES', len(rows))
print('LIVE_WITH_AMBIGUITY', sum(1 for r in rows if r['same_bar_ambiguity_count'] > 0))
for r in sorted(rows, key=lambda x: (x['symbol'], x['rank'])):
    print(r)
