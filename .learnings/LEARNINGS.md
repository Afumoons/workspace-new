# Learnings Log

Captured learnings, corrections, and discoveries. Review before major tasks.

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
