import json
from pathlib import Path
from collections import Counter

BASE = Path(r'C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai\strategies')
manifest = json.loads((BASE / 'live_manifest.json').read_text(encoding='utf-8'))

entries = [e for e in manifest.get('entries', []) if e.get('symbol') == 'BTCUSDm' and e.get('timeframe') == 'M15']
print('manifest entries', len(entries))

EXEC_MIN_WF_SHARPE = 0.75
EXEC_MAX_DD_PCT = 12.0
EXEC_MIN_TRADES = 160
EXEC_MAX_CONSEC_LOSS = 15
SPECIALIST_EXEC_MIN_TRADES = 120
EXPLORATORY_SPECIALIST_MIN_TRADES = 100

kept=[]
fail=Counter()
for e in entries:
    s=e.get('stats',{}) or {}
    ex=s.get('strategy_explain',{}) or {}
    risk_beh=ex.get('risk_behavior',{}) or {}
    meta=ex.get('meta',{}) or {}
    wf=float(s.get('wf_overall_sharpe',0) or 0)
    dd=abs(float(s.get('max_drawdown_pct',0) or 0))
    tr=int(s.get('num_trades',0) or 0)
    cls=int(risk_beh.get('max_consecutive_losses',0) or 0)
    routing_conf=float(meta.get('routing_confidence',0.0) or 0.0)
    specialist_score=float(meta.get('specialist_score',0.0) or 0.0)
    allowed_regimes=list(meta.get('allowed_regimes',[]) or [])
    allowed_sessions=list(meta.get('allowed_sessions',[]) or [])
    bounded_specialist=bool(allowed_regimes or allowed_sessions)
    mc_p5=float(s.get('mc_final_pnl_p5',0.0) or 0.0)
    min_trades=EXEC_MIN_TRADES
    if bounded_specialist and routing_conf >= 0.65 and specialist_score >= 0.60:
        min_trades = SPECIALIST_EXEC_MIN_TRADES
    if e.get('status') == 'exploratory' and bounded_specialist and routing_conf >= 0.70:
        min_trades = EXPLORATORY_SPECIALIST_MIN_TRADES
    reasons=[]
    if wf < EXEC_MIN_WF_SHARPE: reasons.append(f'wf<{EXEC_MIN_WF_SHARPE}')
    if dd > EXEC_MAX_DD_PCT: reasons.append(f'dd>{EXEC_MAX_DD_PCT}')
    if tr < min_trades: reasons.append(f'trades<{min_trades}')
    if cls > EXEC_MAX_CONSEC_LOSS: reasons.append(f'cls>{EXEC_MAX_CONSEC_LOSS}')
    if mc_p5 <= 0.0: reasons.append('mc_p5<=0')
    if not (specialist_score >= 0.30 or wf >= 5.0): reasons.append('specialist<0.30_and_wf<5')
    if reasons:
        for r in reasons: fail[r]+=1
    else:
        kept.append((e.get('name'), e.get('status'), e.get('score'), wf, tr, specialist_score, routing_conf))
print('quality kept', len(kept))
print('fail counts', dict(fail))
print('kept sample', kept[:10])
