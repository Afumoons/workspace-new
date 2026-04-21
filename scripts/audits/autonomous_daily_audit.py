import json, pathlib, collections, math, time, re
root = pathlib.Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')

pool = json.loads((root/'strategies/pool_state.json').read_text())
manifest = json.loads((root/'strategies/live_manifest.json').read_text())
index = json.loads((root/'strategies/strategy_index.json').read_text())
live_stats = json.loads((root/'execution/strategy_live_stats.json').read_text()).get('strategies', {})
open_trades = json.loads((root/'execution/open_trades.json').read_text())
live_state = json.loads((root/'execution/live_state.json').read_text())
audit = json.loads((root/'execution/pool_audit_trail.json').read_text())
closed_state = json.loads((root/'execution/closed_trades_state.json').read_text())

def family_of(rec):
    s = rec.get('stats', {})
    return s.get('family') or s.get('playbook_type') or (((s.get('strategy') or {}).get('family')) if isinstance(s.get('strategy'), dict) else None) or 'unknown'

def meta_of(rec):
    return (((rec.get('stats') or {}).get('strategy_explain') or {}).get('meta') or {})

def risk_of(rec):
    return (((rec.get('stats') or {}).get('strategy_explain') or {}).get('risk_behavior') or {})

def stability_of(rec):
    return (((rec.get('stats') or {}).get('strategy_explain') or {}).get('stability') or {})

status_counts = collections.Counter(rec.get('status','unknown') for rec in pool.values())
family_counts = collections.Counter(family_of(rec) for rec in pool.values())
status_family = collections.defaultdict(collections.Counter)
for rec in pool.values():
    status_family[rec.get('status','unknown')][family_of(rec)] += 1

manifest_entries = manifest.get('entries', [])
index_entries = index.get('entries', [])
manifest_names = {e.get('name') for e in manifest_entries}
index_names = {e.get('name') for e in index_entries}
pool_names = set(pool)
missing_generated = []
for name, rec in pool.items():
    p = root/'strategies'/'generated'/f'{name}.json'
    if not p.exists():
        missing_generated.append(name)

weak_routing = []
weak_specialist = []
exit_dep = []
weak_stability = []
for name, rec in pool.items():
    meta = meta_of(rec)
    risk = risk_of(rec)
    st = stability_of(rec)
    if meta.get('routing_confidence') is not None and meta.get('routing_confidence', 1) < 0.45:
        weak_routing.append((name, rec.get('status'), rec.get('symbol'), family_of(rec), meta.get('routing_confidence')))
    if meta.get('specialist_score') is not None and meta.get('specialist_score', 1) < 0.25:
        weak_specialist.append((name, rec.get('status'), rec.get('symbol'), family_of(rec), meta.get('specialist_score')))
    if risk.get('exit_rule_ratio') is not None and risk.get('exit_rule_ratio', 0) >= 0.8:
        exit_dep.append((name, rec.get('status'), rec.get('symbol'), family_of(rec), risk.get('exit_rule_ratio')))
    if st.get('sharpe_std') is not None and st.get('sharpe_std', 0) >= 1.2:
        weak_stability.append((name, rec.get('status'), rec.get('symbol'), family_of(rec), st.get('sharpe_std')))

stale_candidates = []
for name, rec in pool.items():
    if rec.get('status') == 'candidate':
        s = rec.get('stats', {})
        # infer stale if no live stats and not in manifest and low score or missing research refresh
        if name not in manifest_names and name not in live_stats:
            stale_candidates.append((name, rec.get('symbol'), family_of(rec), rec.get('score', 0)))

live_bad = []
live_any = []
for name, stats in live_stats.items():
    if name.startswith('manual_'):
        continue
    rec = pool.get(name)
    total_pnl = stats.get('total_pnl', 0)
    trade_count = stats.get('trade_count', stats.get('num_trades', 0))
    recent = stats.get('recent_pnls', []) or []
    recent_avg = sum(recent)/len(recent) if recent else None
    research_ret = (rec or {}).get('stats', {}).get('return_pct') if rec else None
    live_any.append((name, (rec or {}).get('status') if rec else None, total_pnl, trade_count, recent_avg, research_ret, family_of(rec) if rec else None))
    if trade_count >= 3 and total_pnl < 0:
        live_bad.append((name, (rec or {}).get('status') if rec else None, total_pnl, trade_count, recent_avg, research_ret, family_of(rec) if rec else None))

# audit trail counts
ops = collections.Counter()
for row in audit[-200:] if isinstance(audit, list) else []:
    if isinstance(row, dict):
        ops[row.get('action') or row.get('event') or 'unknown'] += 1

# logs summary
log_files = [root/'logs'/'system.log', root/'logs'/'system.log.1']
patterns = {
    'traceback': re.compile(r'traceback', re.I),
    'exception': re.compile(r'exception', re.I),
    'error': re.compile(r'\berror\b', re.I),
    'warning': re.compile(r'\bwarning\b', re.I),
    'live_decay_warning': re.compile(r'live decay warning', re.I),
    'xag_no_runtime': re.compile(r'No active/exploratory strategies in runtime set for XAGUSD', re.I),
    'news_404': re.compile(r'404', re.I),
}
log_counts = collections.Counter()
for lf in log_files:
    if not lf.exists():
        continue
    with lf.open('r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            for key, pat in patterns.items():
                if pat.search(line):
                    log_counts[key] += 1

print('STATUS_COUNTS', dict(status_counts))
print('FAMILY_COUNTS_TOP10', family_counts.most_common(10))
print('ACTIVE_FAMILIES', status_family.get('active', {}).most_common())
print('EXPLORATORY_FAMILIES', status_family.get('exploratory', collections.Counter()).most_common())
print('MANIFEST', manifest.get('entry_count'), len(manifest_entries), 'INDEX', index.get('entry_count'), len(index_entries), 'POOL', len(pool_names), 'MISSING_GENERATED', len(missing_generated))
print('LIVE_STATE', live_state)
print('OPEN_TRADES', len(open_trades), open_trades)
print('WEAK_ROUTING', sorted(weak_routing, key=lambda x: x[-1])[:12])
print('WEAK_SPECIALIST', sorted(weak_specialist, key=lambda x: x[-1])[:12])
print('EXIT_DEP', sorted(exit_dep, key=lambda x: x[-1], reverse=True)[:12])
print('WEAK_STABILITY', sorted(weak_stability, key=lambda x: x[-1], reverse=True)[:12])
print('STALE_CANDIDATES_COUNT', len(stale_candidates), 'TOP', sorted(stale_candidates, key=lambda x: x[-1])[:15])
print('LIVE_BAD', sorted(live_bad, key=lambda x: x[2])[:20])
print('LIVE_ANY', sorted(live_any, key=lambda x: x[2])[:20])
print('AUDIT_OPS', dict(ops))
print('LOG_COUNTS', dict(log_counts))
print('CLOSED_STATE_KEYS', list(closed_state.keys()))
print('CLOSED_STATE', closed_state)
