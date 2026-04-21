import json
from pathlib import Path
from collections import Counter, defaultdict

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
pool_path = root / 'strategies' / 'pool_state.json'
manifest_path = root / 'strategies' / 'live_manifest.json'

pool = json.loads(pool_path.read_text(encoding='utf-8')) if pool_path.exists() else {}
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'entries': []}


def family_from_stats(stats):
    strategy = (stats or {}).get('strategy') or {}
    params = (strategy.get('params') if isinstance(strategy, dict) else None) or {}
    return str(
        (strategy.get('family') if isinstance(strategy, dict) else None)
        or (strategy.get('playbook_type') if isinstance(strategy, dict) else None)
        or params.get('family')
        or params.get('playbook_type')
        or params.get('long_family')
        or params.get('short_family')
        or (stats or {}).get('family')
        or (stats or {}).get('playbook_type')
        or 'unknown'
    )

status_symbol_family = defaultdict(Counter)
status_symbol = defaultdict(Counter)
status_symbol_regime = defaultdict(Counter)

for name, rec in pool.items():
    status = rec.get('status','unknown')
    symbol = rec.get('symbol','unknown')
    stats = rec.get('stats') or {}
    family = family_from_stats(stats)
    meta = ((stats.get('strategy_explain') or {}).get('meta') or {})
    best_regime = meta.get('best_regime','unknown')
    status_symbol_family[status][(symbol, family)] += 1
    status_symbol[status][symbol] += 1
    status_symbol_regime[status][(symbol, best_regime)] += 1

print('POOL_STATUS_BY_SYMBOL')
for status, cnt in status_symbol.items():
    print(status, dict(cnt))

print('\nTOP_FAMILY_CONCENTRATION')
for status in sorted(status_symbol_family):
    print(f'\nSTATUS={status}')
    for (symbol, family), n in status_symbol_family[status].most_common(15):
        print({'symbol': symbol, 'family': family, 'count': n})

print('\nTOP_REGIME_CONCENTRATION')
for status in sorted(status_symbol_regime):
    print(f'\nSTATUS={status}')
    for (symbol, regime), n in status_symbol_regime[status].most_common(12):
        print({'symbol': symbol, 'best_regime': regime, 'count': n})

entries = manifest.get('entries') or []
manifest_family = Counter()
manifest_symbol = Counter()
manifest_status = Counter()
for e in entries:
    manifest_symbol[e.get('symbol','unknown')] += 1
    manifest_status[e.get('status','unknown')] += 1
    manifest_family[(e.get('symbol','unknown'), e.get('family','unknown'), e.get('status','unknown'))] += 1

print('\nLIVE_MANIFEST_SYMBOLS', dict(manifest_symbol))
print('LIVE_MANIFEST_STATUS', dict(manifest_status))
print('LIVE_MANIFEST_TOP_FAMILIES')
for (symbol, family, status), n in manifest_family.most_common(20):
    print({'symbol': symbol, 'family': family, 'status': status, 'count': n})
