import json, collections, pathlib
base = pathlib.Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai')
pool = json.loads((base/'strategies'/'pool_state.json').read_text())
manifest = json.loads((base/'strategies'/'live_manifest.json').read_text())
index_data = json.loads((base/'strategies'/'strategy_index.json').read_text())
live = json.loads((base/'execution'/'strategy_live_stats.json').read_text())
unmatched = json.loads((base/'execution'/'unmatched_closed_deals.json').read_text())
status = collections.Counter()
symbol = collections.Counter()
best_regime = collections.Counter()
family = collections.Counter()
exit_heavy = []
unstable = []
weak_live = []
zero_live = 0
for name, rec in pool.items():
    status[rec.get('status','unknown')] += 1
    symbol[rec.get('symbol','?')] += 1
    st = rec.get('stats', {})
    expl = st.get('strategy_explain', {})
    meta = expl.get('meta', {})
    rb = expl.get('risk_behavior', {})
    stab = expl.get('stability', {})
    fam = 'trend' if meta.get('is_trend_follower') else ('range' if meta.get('is_range_trader') else 'other')
    family[fam] += 1
    best_regime[meta.get('best_regime', 'unknown')] += 1
    er = rb.get('exit_rule_ratio')
    if er is not None and er >= 0.85:
        exit_heavy.append((er, name, rec.get('status')))
    ss = stab.get('sharpe_std')
    if ss is not None and ss >= 1.5:
        unstable.append((ss, name, rec.get('status')))
    ls = live.get('strategies', {}).get(name)
    if not ls or ls.get('num_trades', 0) == 0:
        zero_live += 1
    else:
        pnl = ls.get('total_pnl', 0.0)
        trades = ls.get('num_trades', 0)
        if trades >= 3 and pnl < 0:
            weak_live.append((pnl, trades, name, rec.get('status'), st.get('return_pct')))

manual_unmatched = [(k,v.get('total_pnl',0.0),v.get('num_trades',0)) for k,v in live.get('strategies',{}).items() if k.startswith('manual_') or k.startswith('manual_unmatched_')]
print('STATUS', dict(status))
print('SYMBOL', dict(symbol))
print('FAMILY', dict(family))
print('BEST_REGIME', best_regime.most_common())
print('POOL_COUNT', len(pool))
print('MANIFEST_INFO', type(manifest).__name__, len(manifest) if hasattr(manifest,'__len__') else 'na')
print('INDEX_INFO', type(index_data).__name__, len(index_data) if hasattr(index_data,'__len__') else 'na')
print('EXIT_HEAVY_COUNT', len(exit_heavy))
print('EXIT_HEAVY_TOP', sorted(exit_heavy, reverse=True)[:12])
print('UNSTABLE_COUNT', len(unstable))
print('UNSTABLE_TOP', sorted(unstable, reverse=True)[:12])
print('WEAK_LIVE_COUNT', len(weak_live))
print('WEAK_LIVE_TOP', sorted(weak_live)[:12])
print('ZERO_LIVE_COUNT', zero_live)
print('MANUAL_BUCKETS', manual_unmatched)
print('UNMATCHED_COUNT', len(unmatched))
print('UNMATCHED_RECENT', unmatched[-8:])
