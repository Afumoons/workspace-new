import json
from pathlib import Path
from collections import Counter, defaultdict

root = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
pool_path = root / 'strategies' / 'pool_state.json'
if not pool_path.exists():
    print('POOL_MISSING')
    raise SystemExit(0)

data = json.loads(pool_path.read_text(encoding='utf-8'))
records = list(data.values()) if isinstance(data, dict) else []

buckets = [(-999, 0), (0, 0.2), (0.2, 0.5), (0.5, 999999)]
labels = ['neg', '0_0.2', '0.2_0.5', '0.5_plus']
summary = defaultdict(lambda: {'count':0,'wf_sum':0.0,'score_sum':0.0,'dd_sum':0.0,'rc_sum':0.0,'spec_sum':0.0,'names':[]})
status_counts = Counter()

for rec in records:
    status = rec.get('status', 'unknown')
    stats = rec.get('stats') or {}
    ex = stats.get('strategy_explain') or {}
    rp = ex.get('regime_pnl') or {}
    meta = ex.get('meta') or {}

    best_edge = -999.0
    for v in rp.values():
        try:
            edge = float((v or {}).get('return_pct', -999.0) or -999.0)
        except Exception:
            edge = -999.0
        if edge > best_edge:
            best_edge = edge

    label = 'missing'
    if best_edge > -999:
        for idx, (lo, hi) in enumerate(buckets):
            if best_edge >= lo and best_edge < hi:
                label = labels[idx]
                break

    key = (status, label)
    wf = float(stats.get('wf_overall_sharpe', 0.0) or 0.0)
    score = float(rec.get('score', 0.0) or 0.0)
    dd = abs(float(stats.get('max_drawdown_pct', 0.0) or 0.0))
    rc = float(meta.get('routing_confidence', 0.0) or 0.0)
    spec = float(meta.get('specialist_score', 0.0) or 0.0)

    e = summary[key]
    e['count'] += 1
    e['wf_sum'] += wf
    e['score_sum'] += score
    e['dd_sum'] += dd
    e['rc_sum'] += rc
    e['spec_sum'] += spec
    if len(e['names']) < 10:
        e['names'].append(rec.get('name'))
    status_counts[status] += 1

print('STATUS_COUNTS', dict(status_counts))
for status in sorted(status_counts):
    print(f'\nSTATUS={status}')
    for label in ['neg', '0_0.2', '0.2_0.5', '0.5_plus', 'missing']:
        item = summary.get((status, label))
        if not item:
            continue
        c = item['count']
        print({
            'bucket': label,
            'count': c,
            'avg_wf': round(item['wf_sum']/c, 4),
            'avg_score': round(item['score_sum']/c, 4),
            'avg_dd': round(item['dd_sum']/c, 4),
            'avg_routing_conf': round(item['rc_sum']/c, 4),
            'avg_specialist': round(item['spec_sum']/c, 4),
            'sample': item['names'][:5],
        })
