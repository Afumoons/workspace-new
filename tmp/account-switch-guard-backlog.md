# autonomous_trading_ai — account/baseline guard backlog

## Implemented
- Phase 1: account identity switch guard in `execution/live_monitor.py`
  - tracks account identity (`login`, `server`, `currency`, `company`)
  - detects account switch via login/server mismatch
  - refreshes baseline automatically on account switch
  - resets daily state and closed-trade bookkeeping
  - adds warmup cycles to skip circuit breaker briefly after baseline refresh
  - records `baseline_created_at`, `warmup_cycles_remaining`, `last_baseline_reason`

## TODO — Phase 2
- Add abnormal equity-shock detection even when account identity is unchanged.
- Heuristic candidates:
  - very large equity drop/jump vs prior peak or recent sample
  - large balance/equity discontinuity not explained by recently processed closed deals
  - optional deposit/withdraw vs trade-PnL distinction when MT5 data allows it
- On anomaly:
  - do NOT disable live-tier strategies immediately
  - re-anchor baseline safely
  - log explicit anomaly reason

## TODO — Phase 3
- Add persistent disable metadata to pool records, e.g.:
  - `disabled_reason`
  - `disabled_at`
  - `disabled_context`
- Add baseline-refresh metadata / audit trail.
- Optionally send operator notification on auto baseline refresh / anomaly refresh.
- Consider manual operator command/script to force baseline refresh cleanly.
