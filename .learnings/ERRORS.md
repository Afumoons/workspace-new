# Errors Log

## Entry Template
```
## [ERR-YYYYMMDD-XXX]
**Logged**: YYYY-MM-DDTHH:MM:SSZ
**Context**: command/task
**Impact**: low|med|high
**Status**: pending|in_progress|resolved|wont_fix
**Owner**: (optional)

### What happened
- command/tool/API and error message

### Cause (if known)
- root cause or hypothesis

### Fix / Next steps
- remediation steps
- follow-up actions
```## [ERR-20260327-001] powershell-command-chaining

**Logged**: 2026-03-27T04:31:00+07:00
**Priority**: low
**Status**: resolved
**Area**: config

### Summary
PowerShell in this OpenClaw workspace rejected a git add/commit command chained with bash-style &&.

### Error
`
The token '&&' is not a valid statement separator in this version.
`

### Context
- Command attempted during autonomous_trading_ai Pass 3 finalization
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: git add ... && git commit ...

### Suggested Fix
Use separate exec calls or PowerShell-compatible separators instead of bash-style &&.

### Metadata
- Reproducible: yes
- Related Files: autonomous_trading_ai/tmp/pass3-tasklist.md

### Resolution
- **Resolved**: 2026-03-27T04:31:00+07:00
- **Commit/PR**: pending current commit
- **Notes**: Retried with separate git add and git commit commands.

---

## [ERR-20260327-002] powershell-and-separator-followup

**Logged**: 2026-03-27T05:30:00+07:00
**Priority**: low
**Status**: resolved
**Area**: config

### Summary
A follow-up verification command used bash-style `&&` again and failed under this Windows PowerShell exec environment.

### Error
`
The token '&&' is not a valid statement separator in this version.
`

### Context
- Command attempted while verifying autonomous_trading_ai Pass 3 completion marker and latest commit
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: `git rev-parse --short HEAD && git log -1 --oneline && git status --short`

### Suggested Fix
Use PowerShell separators (`;`) or separate exec calls for chained commands in this workspace.

### Metadata
- Reproducible: yes
- Related Files: autonomous_trading_ai/tmp/pass3-tasklist.md
- See Also: ERR-20260327-001

### Resolution
- **Resolved**: 2026-03-27T05:31:00+07:00
- **Commit/PR**: n/a
- **Notes**: Re-ran verification with `;` separators and confirmed the repo state successfully.

---

## [ERR-20260331-001] powershell-search-session-killed

**Logged**: 2026-03-31T13:07:00+07:00
**Priority**: low
**Status**: resolved
**Area**: diagnostics

### Summary
Two diagnostic exec sessions were SIGKILLed while searching the workspace during investigation of `live_manifest.json` updates.

### Error
- Exec failed (`signal SIGKILL`) on broad recursive search attempts.
- One attempt also used a bash-style heredoc (`python - <<'PY'`) which is not valid in this PowerShell environment.

### Context
- Task: trace who updates `autonomous_trading_ai/strategies/live_manifest.json`
- Environment: OpenClaw exec on Windows PowerShell
- Commands were broader/heavier than needed for the diagnosis.

### Cause
- Used Linux/bash-oriented patterns in PowerShell.
- Used recursive content search wider than necessary, causing noisy/long-running sessions that were then killed.

### Fix / Next steps
- Prefer targeted reads of known files over broad recursive grep-style scans.
- In PowerShell, avoid bash heredocs; use native PowerShell or `python -c` if Python is needed.
- Kill stale diagnostic sessions quickly and continue with narrower file inspection.

### Resolution
- **Resolved**: 2026-03-31T13:07:00+07:00
- **Commit/PR**: pending current workspace commit
- **Notes**: Switched to direct file inspection (`live_manifest.py`, `pool.py`) and confirmed manifest rebuild depends on `save_pool()`.

---
