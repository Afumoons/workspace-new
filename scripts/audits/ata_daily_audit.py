import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone

root = Path(r"C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai")
pool = json.loads((root / 'strategies' / 'pool_state.json').read_text(encoding='utf-8'))
manifest = json.loads((root / 'strategies' / 'live_manifest.json').read_text(encoding='utf-8'))
index = json.loads((root / 'strategies' / 'strategy_index.json').read_text(encoding='utf-8'))
_raw_live_stats = json.loads((root / 'execution' / 'strategy_live_stats.json').read_text(encoding='utf-8')) if (root / 'execution' / 'strategy_live_stats.json').exists() else {}
live_stats = _raw_live_stats.get('strategies', _raw_live_stats) if isinstance(_raw_live_stats, dict) else {}
open_trades = json.loads((root / 'execution' / 'open_trades.json').read_text(encoding='utf-8')) if (root / 'execution' / 'open_trades.json').exists() else []

records = list(pool.values())
status_counts = Counter(r.get('status', 'unknown') for r in records)
family_by_status = defaultdict(Counter)
symbol_by_status = defaultdict(Counter)
routing = []
specialist = []
exit_ratio = []
stability = []
missing_defs = []
active_names = []
now = datetime.now(timezone.utc)
ages = []
live_under = []
manual_buckets = []

for r in records:
    stats = r.get('stats') or {}
    strat = stats.get('strategy') or {}
    params = strat.get('params') or {}
    family = stats.get('family') or strat.get('family') or params.get('family') or 'unknown'
    family_by_status[r.get('status','unknown')][family] += 1
    symbol_by_status[r.get('status','unknown')][r.get('symbol','?')] += 1
    meta = ((stats.get('strategy_explain') or {}).get('meta') or {})
    riskb = ((stats.get('strategy_explain') or {}).get('risk_behavior') or {})
    stab = ((stats.get('strategy_explain') or {}).get('stability') or {})
    if 'routing_confidence' in meta:
        routing.append((r['name'], r.get('status'), r['symbol'], family, meta.get('routing_confidence', 0), meta.get('specialist_score', 0)))
    if 'specialist_score' in meta:
        specialist.append((r['name'], r.get('status'), r['symbol'], family, meta.get('specialist_score', 0), meta.get('routing_confidence', 0)))
    if 'exit_rule_ratio' in riskb:
        exit_ratio.append((r['name'], r.get('status'), r['symbol'], family, riskb.get('exit_rule_ratio', 0), riskb.get('avg_holding_bars', 0)))
    if 'sharpe_std' in stab:
        stability.append((r['name'], r.get('status'), r['symbol'], family, stab.get('sharpe_std', 0), stats.get('sharpe_ratio', 0)))
    gen = root / 'strategies' / 'generated' / f"{r['name']}.json"
    if not gen.exists():
        missing_defs.append(r['name'])
    if r.get('status') == 'active':
        active_names.append(r['name'])
    if r.get('status') == 'candidate' and gen.exists():
        age_days = (now - datetime.fromtimestamp(gen.stat().st_mtime, timezone.utc)).days
        ages.append((r['name'], r['symbol'], family, age_days, r.get('score', 0)))

for name, rec in live_stats.items():
    total_pnl = float(rec.get('total_pnl', 0.0) or 0.0)
    num_trades = int(rec.get('num_trades', 0) or 0)
    recent = rec.get('recent_pnls') or []
    recent_avg = (sum(recent) / len(recent)) if recent else 0.0
    row = pool.get(name)
    if row:
        stats = row.get('stats') or {}
        strat = stats.get('strategy') or {}
        params = strat.get('params') or {}
        family = stats.get('family') or strat.get('family') or params.get('family') or 'unknown'
        if num_trades >= 3 and total_pnl < 0:
            live_under.append((name, row.get('status'), row.get('symbol'), family, row.get('score', 0), total_pnl, num_trades, recent_avg))
    else:
        if name.startswith('manual_'):
            manual_buckets.append((name, total_pnl, num_trades, recent_avg))

entries = manifest.get('entries') or manifest.get('strategies') or []
manifest_names = set()
manifest_symbol = Counter()
manifest_family = Counter()
for e in entries:
    if isinstance(e, dict):
        name = e.get('name') or e.get('strategy_name') or e.get('id') or ''
        if name:
            manifest_names.add(name)
        manifest_symbol[e.get('symbol','?')] += 1
        manifest_family[e.get('family','unknown')] += 1
    elif isinstance(e, str):
        manifest_names.add(e)
manifest_names.discard('')

print(json.dumps({
    'status_counts': status_counts,
    'active_symbol_mix': symbol_by_status.get('active', {}),
    'candidate_symbol_mix': symbol_by_status.get('candidate', {}),
    'active_family_mix': family_by_status.get('active', {}),
    'candidate_family_mix': family_by_status.get('candidate', {}),
    'manifest_entry_count': len(entries),
    'manifest_symbol_mix': manifest_symbol,
    'manifest_family_mix': manifest_family,
    'active_missing_from_manifest': sorted(set(active_names) - manifest_names),
    'missing_generated_defs_count': len(missing_defs),
    'low_routing_confidence': sorted(routing, key=lambda x: x[4])[:10],
    'low_specialist_score': sorted(specialist, key=lambda x: x[4])[:10],
    'high_exit_rule_ratio': sorted(exit_ratio, key=lambda x: (-x[4], -x[5]))[:10],
    'high_sharpe_std': sorted(stability, key=lambda x: (-x[4], x[5]))[:10],
    'stale_candidates_30d': [x for x in sorted(ages, key=lambda x: (-x[3], -x[4])) if x[3] >= 30][:20],
    'live_underperformers': sorted(live_under, key=lambda x: x[5])[:10],
    'manual_buckets': sorted(manual_buckets, key=lambda x: x[1])[:10],
    'live_stats_count': len(live_stats),
    'open_trades': open_trades,
}, indent=2, default=lambda o: dict(o)))
