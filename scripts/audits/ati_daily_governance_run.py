import json, os, re, collections
root=r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai'

def load(rel):
    with open(os.path.join(root,*rel.split('/')),'r',encoding='utf-8') as f:
        return json.load(f)

logdir=os.path.join(root,'logs')
patterns=re.compile(r'error|exception|traceback|failed|critical', re.I)
for name in ['system.log','system.log.1','system.log.2']:
    p=os.path.join(logdir,name)
    if not os.path.exists(p):
        continue
    print(f'=== {name} size={os.path.getsize(p)}')
    with open(p,'r',encoding='utf-8',errors='ignore') as f:
        lines=f.readlines()
    hits=[(i+1,l.strip()) for i,l in enumerate(lines) if patterns.search(l)]
    print('hits',len(hits))
    for ln,txt in hits[-20:]:
        print(ln, txt[:300])

pool=load('strategies/pool_state.json')
manifest=load('strategies/live_manifest.json')
index=load('strategies/strategy_index.json')
live_state=load('execution/live_state.json')
live_stats=load('execution/strategy_live_stats.json')
closed=load('execution/closed_trades_state.json')
equity=load('execution/equity_history.json')
open_trades=load('execution/open_trades.json')
items=pool.get('strategies') or pool.get('entries') or []
mentries=manifest.get('entries') or []
ientries=index.get('entries') or index.get('strategies') or []
print('POOL_COUNT',len(items))
print('MANIFEST_COUNT',len(mentries),'FIELD',manifest.get('entry_count'),'GENERATED',manifest.get('generated_at'))
print('INDEX_COUNT',len(ientries),'FIELD',index.get('entry_count'),'GENERATED',index.get('generated_at'))
print('LIVE_STATE',live_state)
print('OPEN_TRADES_TYPE', type(open_trades).__name__, 'LEN', len(open_trades) if hasattr(open_trades,'__len__') else 'na')
print('CLOSED_STATE',closed)
print('EQUITY_KEYS', list(equity.keys())[:20] if isinstance(equity,dict) else type(equity).__name__)
strategies=(live_stats.get('strategies') if isinstance(live_stats,dict) and 'strategies' in live_stats else live_stats)
print('LIVE_STATS_STRATEGIES', len(strategies) if isinstance(strategies,dict) else 'na')
if isinstance(strategies,dict):
    worst=sorted(((k,v.get('total_pnl',0),v.get('num_trades',0),v.get('last_update')) for k,v in strategies.items() if isinstance(v,dict)), key=lambda x:(x[1],-x[2]))[:10]
    print('LIVE_WORST', worst)
    best=sorted(((k,v.get('total_pnl',0),v.get('num_trades',0),v.get('last_update')) for k,v in strategies.items() if isinstance(v,dict)), key=lambda x:(x[1],x[2]), reverse=True)[:10]
    print('LIVE_BEST', best)
status=collections.Counter((x.get('status') or 'unknown') for x in items)
family=collections.Counter((x.get('family') or x.get('params',{}).get('family') or 'unknown') for x in items)
print('STATUS',status)
print('TOP_FAMILY',family.most_common(12))
rows=[]
for e in mentries:
    name=e.get('name')
    ls=(strategies.get(name) if isinstance(strategies,dict) else {}) or {}
    n=ls.get('num_trades',0) or 0
    pnl=ls.get('total_pnl',0) or 0
    r=((e.get('stats') or {}).get('return_pct'))
    meta=(((e.get('stats') or {}).get('strategy_explain') or {}).get('meta') or {})
    decay=e.get('live_decay') or {}
    if n or decay:
        rows.append((name,e.get('family'),e.get('symbol'),e.get('status'),e.get('score'),r,n,pnl,decay.get('signal_level'),meta.get('routing_confidence')))
rows=sorted(rows,key=lambda x:(x[7],-x[6]))
print('DRIFT_ROWS', rows[:15])
for rel in ['logs/system.log','logs/system.log.1','logs/system.log.2','execution/trades.log','strategies/pool_state.json','strategies/live_manifest.json','strategies/strategy_index.json']:
    p=os.path.join(root,*rel.split('/'))
    if os.path.exists(p):
        print('SIZE', rel, os.path.getsize(p))
