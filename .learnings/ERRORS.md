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
```

## [ERR-20260409-001] mt5-history-deals-rebuild-returned-none

**Logged**: 2026-04-09T13:11:00+07:00
**Priority**: medium
**Status**: pending
**Area**: diagnostics

### Summary
`rebuild_strategy_live_stats.py` failed during the daily governance pass because `mt5.history_deals_get(...)` returned `None`, so derived live PnL stats could not be refreshed.

### Error
`RuntimeError: mt5.history_deals_get returned None for range 2026-03-26 06:10:15.128774+00:00 -> 2026-04-09 06:10:15.128774+00:00`

### Context
- Task: autonomous_trading_ai daily governance + maintenance cron
- Command: `python -m autonomous_trading_ai.scripts.rebuild_strategy_live_stats`
- Environment: Windows OpenClaw workspace, project venv, MT5-backed repo
- This was a safe maintenance attempt to refresh derived `execution/strategy_live_stats.json`

### Cause
- MT5 history API returned `None`; exact cause not yet diagnosed from repo-visible evidence.
- Could be terminal/session state, history range availability, or MT5 bridge readiness during the cron run.

### Suggested Fix
- Add defensive logging around `mt5.last_error()` in `rebuild_strategy_live_stats.py` before raising.
- Check whether MT5 terminal/session is connected and whether history range queries succeed interactively.
- Consider fallback reconciliation from repo-side artifacts when MT5 history is temporarily unavailable.

### Metadata
- Reproducible: unknown
- Related Files: autonomous_trading_ai/scripts/rebuild_strategy_live_stats.py, autonomous_trading_ai/execution/strategy_live_stats.json

---
## [ERR-20260327-001] powershell-command-chaining

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

---

## [ERR-20260409-001] powershell-git-chain-regression

**Logged**: 2026-04-09T09:33:00+07:00
**Priority**: low
**Status**: resolved
**Area**: config

### Summary
A git add/commit command during `ui-front` roadmap finalization used bash-style `&&` again and failed under the Windows PowerShell exec environment.

### Error
`
The token '&&' is not a valid statement separator in this version.
`

### Context
- Task: finalize `autonomous_trading_ai/ui-front` Phase 1–3 roadmap closure
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: `git add ... && git commit ...`

### Suggested Fix
Use separate exec calls or PowerShell-compatible separators like `;` instead of bash-style `&&` in this workspace.

### Metadata
- Reproducible: yes
- Related Files: autonomous_trading_ai/ui-front/package.json, autonomous_trading_ai/ui-front/TASKLIST.md
- See Also: ERR-20260327-001, ERR-20260327-002

### Resolution
- **Resolved**: 2026-04-09T09:34:00+07:00
- **Commit/PR**: pending current commit
- **Notes**: Retried the git add and git commit as separate commands.
- **Commit/PR**: pending current workspace commit

---

## [ERR-20260408-001] powershell-command-chaining-repeat

**Logged**: 2026-04-08T19:43:11+07:00
**Priority**: low
**Status**: resolved
**Area**: config

### Summary
A git add/commit command for the ATA2 batch used bash-style `&&` again and failed in the Windows PowerShell exec environment.

### Error
`
The token '&&' is not a valid statement separator in this version.
`

### Context
- Task: commit ATA2 smoke-test batch
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: `git add ... && git commit ...`

### Suggested Fix
Use separate exec calls or PowerShell-compatible separators such as `;` in this workspace.

### Metadata
- Reproducible: yes
- Related Files: C:\laragon\www\ATA2
- See Also: ERR-20260327-001, ERR-20260327-002

### Resolution
- **Resolved**: 2026-04-08T19:43:11+07:00
- **Commit/PR**: pending ATA2 smoke-test commit
- **Notes**: Will retry with separate git commands.
- **Notes**: Switched to direct file inspection (`live_manifest.py`, `pool.py`) and confirmed manifest rebuild depends on `save_pool()`.

---
## [ERR-20260403-001] ripgrep_missing_in_powershell_env

**Logged**: 2026-04-03T06:05:00Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Attempted to use 
g for repo search during governance audit, but ripgrep is not installed in this PowerShell environment.

### Error
`
rg : The term 'rg' is not recognized as the name of a cmdlet, function, script file, or operable program.
`

### Context
- Command attempted in workspace repo inspection
- Environment: OpenClaw on Windows PowerShell

### Suggested Fix
Prefer native PowerShell search fallback (Get-ChildItem + Select-String) unless ripgrep presence is confirmed first.

### Metadata
- Reproducible: yes
- Related Files: C:\Users\afusi\.openclaw\workspace\.learnings\ERRORS.md

---

## [ERR-20260408-001] gateway-obfuscation-detector-blocked-python-c

**Logged**: 2026-04-08T13:36:00+07:00
**Priority**: medium
**Status**: pending
**Area**: diagnostics

### Summary
A diagnostic `python -c` command to scan recent log lines was denied by the exec gateway with `approval-timeout (obfuscation-detected)` even though the task was a benign local log inspection.

### Error
`
Exec denied (gateway id=367e7aad-3dc7-41f1-9508-224908f06e87, approval-timeout (obfuscation-detected))
`

### Context
- Task: inspect `autonomous_trading_ai/logs/system.log` for recent errors/stall indicators
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: `python -c "from pathlib import Path; ..."` with regex scanning over recent log lines

### Suggested Fix
Prefer direct file reads for log inspection first, or use simpler/non-obfuscated command forms when shell execution is actually necessary.

### Metadata
- Reproducible: unknown
- Related Files: C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai\logs\system.log
- See Also: ERR-20260331-001

---
## [ERR-20260409-001] exec-powershell-separator

**Logged**: 2026-04-08T17:45:00Z
**Priority**: low
**Status**: resolved
**Area**: infra

### Summary
PowerShell exec commands in this environment do not accept `&&` as a statement separator.

### Error
```
The token '&&' is not a valid statement separator in this version.
```

### Context
- Command attempted: `git add ... && git commit ...`
- Environment: OpenClaw exec on Windows / PowerShell
- Correct approach: use `;` or separate exec calls

### Suggested Fix
Prefer `;` for chained PowerShell commands in this environment, or run commands separately.

### Metadata
- Reproducible: yes
- Related Files: none
- Tags: powershell, exec, windows

### Resolution
- **Resolved**: 2026-04-08T17:45:00Z
- **Commit/PR**: n/a
- **Notes**: Switched to PowerShell-compatible command chaining.

---
## [ERR-20260409-001] ata2-verification-command-drift
**Logged**: 2026-04-09T01:05:00+07:00
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
ATA2 production-candidate docs recorded `python -m ata2.cli demo --dry-run` as a successful verification command, but the CLI does not expose a `--dry-run` flag on `demo`.

### Error
`usage: ata2 [-h] {serve,summary,runtime-artifacts,runtime-summary,dry-run-demo,deployment-checklist,demo} ...`
`ata2: error: unrecognized arguments: --dry-run`

### Context
- Task: cron verification pass for ATA2 production-candidate status
- Environment: OpenClaw exec on Windows PowerShell
- Actual CLI behavior: `dry-run-demo` is the end-to-end dry-run command; `demo` is a separate sample flow that still reports `execution_mode: "dry-run"` under default safe config.

### Suggested Fix
Keep verification docs aligned with real CLI surfaces and prefer copy-pasting commands from `ata2/cli.py` or tested help output.

### Metadata
- Reproducible: yes
- Related Files: C:\laragon\www\ATA2\docs\PRODUCTION_CANDIDATE_TASKLIST.md, C:\laragon\www\ATA2\README.md

### Resolution
- **Resolved**: 2026-04-09T01:05:00+07:00
- **Commit/PR**: pending ATA2 doc cleanup commit
- **Notes**: Updated the tasklist snapshot and README verification/command guidance to use `dry-run-demo` and `demo` correctly.

---
## [ERR-20260411-001] python-c-newline-escaping-in-powershell

**Logged**: 2026-04-11T13:05:00+07:00
**Priority**: low
**Status**: resolved
**Area**: diagnostics

### Summary
A repo inspection command used `python -c` with literal `\n` escapes in the PowerShell exec environment, which Python parsed incorrectly and raised a `SyntaxError`.

### Error
`SyntaxError: unexpected character after line continuation character`

### Context
- Task: autonomous_trading_ai daily governance + maintenance cron
- Environment: OpenClaw exec on Windows PowerShell
- Command pattern: multi-line Python loop embedded via `python -c "...\n..."`

### Suggested Fix
For Windows PowerShell exec, keep `python -c` bodies on one logical line with semicolons/comprehensions, or use PowerShell-native file listing when possible.

### Metadata
- Reproducible: yes
- Related Files: C:\Users\afusi\.openclaw\workspace\.learnings\ERRORS.md
- See Also: ERR-20260331-001

### Resolution
- **Resolved**: 2026-04-11T13:05:00+07:00
- **Commit/PR**: n/a
- **Notes**: Switched to PowerShell-native listing for repo inspection.

---
## [ERR-20260409-002] ui-api-relative-import-top-level

**Logged**: 2026-04-08T20:41:00Z
**Priority**: medium
**Status**: pending
**Area**: backend-ui-api

### Summary
The autonomous_trading_ai UI frontend built successfully, but the UI API failed to start in a standalone launch because `ui_api/adapters.py` uses package-relative imports that go beyond the top-level package.

### Error
`ImportError: attempted relative import beyond top-level package`

### Context
- Task: UI v1 frontend build / verification follow-up
- Environment: OpenClaw exec on Windows PowerShell
- Failing file: `C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai\ui_api\adapters.py`
- Current pattern: `from ..execution...`, `from ..strategies...`

### Cause
The `ui_api` package appears to be launched in a way where it is treated as a top-level package, so `..execution` and `..strategies` are invalid from that import context.

### Suggested Fix
Use imports that match the real runtime package layout, e.g. absolute package imports rooted at `autonomous_trading_ai`, or launch the app consistently as part of the full package so relative imports remain valid.

### Metadata
- Reproducible: yes
- Related Files: `C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai\ui_api\adapters.py`, `C:\Users\afusi\.openclaw\workspace\autonomous_trading_ai\ui_api\app.py`
- Tags: python, import, fastapi, ui-api

---
## [ERR-20260413-001] exec-shell-assumptions-on-windows

**Logged**: 2026-04-13T18:50:00+07:00
**Priority**: low
**Status**: pending
**Area**: diagnostics

### Summary
Two quick inspection attempts failed because I assumed Windows-style `dir` flags and bash heredoc syntax would work inside the current OpenClaw PowerShell exec environment.

### Error
- `/usr/bin/dir: cannot access '/s': No such file or directory`
- `Missing file specification after redirection operator.` when using `python - <<'PY'`

### Context
- Task: daily autonomous_trading_ai governance and maintenance cron
- Environment: Windows OpenClaw workspace with PowerShell shell semantics
- Commands attempted:
  - `C:\laragon\bin\git\usr\bin\dir.exe /s /b`
  - `python - <<'PY' ... PY`

### Cause
- The available `dir.exe` behaved like a Unix coreutils variant, not Windows CMD `dir`.
- PowerShell does not support bash heredoc redirection syntax.

### Suggested Fix
- Prefer `rg --files`, PowerShell-native commands, or temporary script files for multi-line Python.
- Treat bundled Unix utilities on Windows as potentially non-CMD-compatible.

### Metadata
- Reproducible: yes
- Related Files: `C:\Users\afusi\.openclaw\workspace\tmp\autonomous_daily_audit.py` (legacy, cleanup candidate)
- Tags: windows, powershell, exec, tooling

---
## [ERR-20260413-002] openclaw-doctor-reported-gateway-update-followups

**Logged**: 2026-04-13T18:53:00+07:00
**Priority**: medium
**Status**: pending
**Area**: openclaw-maintenance

### Summary
Heartbeat follow-up on the earlier gateway restart update error showed actionable maintenance items from `openclaw doctor --non-interactive` rather than a direct crash signature.

### Error
- Auth profile cooldown: `openai-codex:creative.upquality@gmail.com` in 4h cooldown
- Bundled plugin runtime dependency missing: `@discordjs/opus@^0.10.0`
- Found 1 orphan transcript file in `~\.openclaw\agents\main\sessions`
- Doctor process itself ended with `SIGKILL` after printing diagnostics, so the final exit path may be incomplete

### Context
- Trigger: system notice `Gateway restart update error (npm)`
- Command run: `openclaw doctor --non-interactive`
- Environment: OpenClaw main cron/heartbeat session on Windows host

### Cause
- Likely not a single fatal gateway config error. The doctor surfaced maintenance issues and may have been terminated by the exec wrapper before graceful completion.
- Missing bundled plugin dependency is the clearest concrete fix surfaced by doctor.

### Suggested Fix
- Consider running `openclaw doctor --fix` when Afu approves maintenance changes, or at minimum install the missing bundled dependency via the doctor fix path.
- Review whether the auth-profile cooldown matters operationally or can be ignored temporarily.
- Optionally archive orphan transcript files if desired.

### Metadata
- Reproducible: unknown
- Related Files: `C:\Users\afusi\.openclaw\workspace\.learnings\ERRORS.md`
- Tags: openclaw, doctor, gateway, maintenance
