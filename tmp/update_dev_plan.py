from pathlib import Path

p = Path(r"C:/Users/afusi/.openclaw/workspace/autonomous_trading_ai/docs/clio/03-DEVELOPMENT_PLAN.md")
text = p.read_text(encoding="utf-8")

old = """- `06-M15_IMPROVEMENT_ROADMAP.md`
- `07-ROUTING_LAYER_AUDIT_AND_TASKLIST.md`

Treat this file as the **broad roadmap / status ledger**, not the detailed
implementation checklist.
"""
new = """- `06-M15_IMPROVEMENT_ROADMAP.md`
- `07-ROUTING_LAYER_AUDIT_AND_TASKLIST.md`

For the future-state architectural redesign target, see:

- `16-AUTONOMOUS-TRADING-AI-V2-BLUEPRINT-2026-04-06.md`

Treat this file as the **broad roadmap / status ledger**, not the detailed
implementation checklist.
"""
text = text.replace(old, new, 1)

old2 = """- 2026-04-04: Updated the broad plan to acknowledge post-audit hardening already completed (live decay detection, concentration control) and narrow remaining priorities more honestly.
- 2026-03-27: Reframed the development plan around implemented phase status, pass 3 outcomes, and next-priority work after specialist-routing hardening.
"""
new2 = """- 2026-04-06: Added a pointer to `16-AUTONOMOUS-TRADING-AI-V2-BLUEPRINT-2026-04-06.md` as the future-state architecture target distinct from the current tactical hardening roadmap.
- 2026-04-04: Updated the broad plan to acknowledge post-audit hardening already completed (live decay detection, concentration control) and narrow remaining priorities more honestly.
- 2026-03-27: Reframed the development plan around implemented phase status, pass 3 outcomes, and next-priority work after specialist-routing hardening.
"""
text = text.replace(old2, new2, 1)

p.write_text(text, encoding="utf-8")
print("ok")
