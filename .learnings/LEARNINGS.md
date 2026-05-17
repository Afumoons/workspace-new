# Learnings Log

Captured learnings, corrections, and discoveries. Review before major tasks.

## [LRN-20260428-001] repo-scripts-may-ignore-help-flags

**Logged**: 2026-04-28T19:32:00+07:00
**Priority**: high
**Status**: active
**Area**: tooling

### Summary
In this workspace, some repo utility scripts are not argparse-based and may execute real mutations even when called with `--help`.

### Details
`python -m autonomous_trading_ai.scripts.rebuild_pool_status --help` ran the full maintenance routine instead of printing help. For local repo scripts, inspect the file first or invoke only when the command path is already understood.

### Suggested Action
Before probing custom project scripts, read the script or run a truly read-only inspection path instead of assuming standard CLI help semantics.

---

## [LRN-20260405-001] windows_exec_shell_chaining

**Logged**: 2026-04-05T05:51:00+07:00
**Priority**: high
**Status**: active
**Area**: tooling

### Summary
On this Windows/PowerShell host, do not use shell chaining with `&&` in `exec` commands.

### Details
This failure recurred during git commit execution. The local host shell path does not reliably accept `&&` in this runtime. Use `;` or separate tool calls instead. Treat this as a fixed workspace rule for future commands.

### Suggested Action
Before sending Windows `exec` commands, avoid `&&` completely unless there is hard evidence the target shell supports it in that exact context.

---

## [LRN-20250305-001] skill_setup

**Logged**: 2026-03-05T21:12:00+07:00
**Priority**: medium
**Status**: resolved
**Area**: config

### Summary
Self-improving-agent skill installed and learning logs initialized in workspace root.

### Details
User requested proactive setup of learning infrastructure without asking for permission on non-security tasks. Skill creates three log files (ERRORS.md, LEARNINGS.md, FEATURE_REQUESTS.md) to capture:
- Command/operation failures
- User corrections
- Missing capabilities
- API/tool failures
- Knowledge gaps
- Best practices discovered

### Suggested Action
Review `.learnings/` before major tasks. Promote high-value learnings to AGENTS.md, TOOLS.md, or SOUL.md.

### Metadata
- Source: user_feedback
- Related Files: skills/self-improving-agent/SKILL.md
- Tags: setup, configuration, proactive

---
## [LRN-20260429-001] correction

**Logged**: 2026-04-29T00:31:43.3861957+07:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Afu expects Clio to commit completed clean workspace/code changes by default without needing repeated reminders.

### Details
User explicitly corrected the workflow: after finishing relevant work cleanly, commit directly instead of asking or waiting to be told again. This matches existing USER.md preference and should be treated as default behavior unless commit boundaries are unclear or the work is intentionally incomplete.

### Suggested Action
Default to immediate clean commits after a finished work item, while still keeping UI, trading code, and runtime artifacts separated according to repo rules.

### Metadata
- Source: user_feedback
- Related Files: USER.md, MEMORY.md
- Tags: correction, git, workflow, commit-discipline

---
