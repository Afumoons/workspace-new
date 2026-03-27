# Cron Big Task Rule & Template

## Rule: Auto-Cron for Very Large / Complex Tasks

When Afu gives a task that is too large, too long, or too complex to finish reliably in a single prompt/turn, Clio Nova should **default to a cron-driven execution approach** instead of trying to force everything into one live response.

### Trigger Conditions
Use cron-first execution when one or more of these are true:
- The task clearly requires multi-stage work over time.
- The task will likely exceed one prompt context window.
- The task depends on long-running research, monitoring, iteration, retries, or checkpoints.
- The task benefits from scheduled follow-ups rather than one-shot completion.
- The task is better split into planning, execution, review, and reporting phases.
- The task is ongoing by nature (monitoring, recurring scans, repeated checks, batch work, pipeline work).

### Default Behavior
If the task matches the trigger conditions, Clio should:
1. Reframe the task into a staged execution plan.
2. Create a cron-based workflow when timing/scheduling helps completion.
3. Use isolated agentTurn cron jobs by default unless main-session behavior is explicitly needed.
4. Store progress/checkpoints in workspace files so state survives context loss.
5. Report status in concise milestone updates instead of pretending the full task is done immediately.

### Safety / Decision Guardrails
Clio may auto-use cron **without asking first** when:
- The cron is for internal execution, reminders, research, monitoring, planning, summarization, or checkpointed work.
- The cron does not weaken security posture.
- The cron does not perform destructive actions.
- The cron does not send external/public actions beyond normal user-visible reporting already requested.

Clio should **ask first** before cron automation if:
- The cron would change security-sensitive settings.
- The cron would trigger external side effects Afu did not clearly request.
- The cron would spend money, trade live, delete data, publish content, or message third parties.

### Preferred Execution Pattern
For big tasks, Clio should usually follow this pattern:
- Phase 1: scope + break into milestones
- Phase 2: create working files/checklists/checkpoints
- Phase 3: schedule cron-driven execution or review cycles
- Phase 4: deliver milestone updates
- Phase 5: deliver final synthesis / handoff

### Preferred Session Target
Default preferences:
- `payload.kind="agentTurn"`
- `sessionTarget="isolated"` for most autonomous large-task execution
- `delivery.mode="announce"` unless silence is clearly better

Use `sessionTarget="current"` only if the work specifically needs continuity in the current session thread.

### Reminder / Report Style
When cron jobs fire, the resulting text should read naturally as:
- a progress update,
- a reminder,
- a checkpoint notice, or
- a request for a decision if blocked.

Avoid robotic/internal wording. Write like an operator update.

---

## Default User-Facing Template
When a big task is detected, Clio can internally translate it into this structure.
For specialized execution patterns, also use `tmp/cron-task-templates.md`:
- Template 1: Riset Besar
- Template 2: Proyek Coding Besar
- Template 3: Monitoring / Automation Berulang


### BIG TASK INTAKE TEMPLATE
- **Objective:**
- **Why this is big/complex:**
- **Success criteria:**
- **Constraints / risks:**
- **What can run autonomously:**
- **What requires Afu approval:**
- **Milestones:**
  1.
  2.
  3.
- **Checkpoint files:**
- **Suggested cron cadence:**
- **Expected outputs:**

### CRON JOB PROMPT TEMPLATE
Use this as the `payload.message` basis for isolated cron work:

"Continue the large task for Afu using the existing workspace files and checkpoints. First read the latest relevant plan/checkpoint files, then execute only the next highest-leverage milestone. Update progress notes before finishing. If blocked, produce a concise blocker summary with the exact decision needed. If completed, produce a concise completion summary and the next recommended action."

### STATUS UPDATE TEMPLATE
- **Task:** <name>
- **Current phase:** <phase>
- **Done:** <completed work>
- **Next:** <next milestone>
- **Blockers:** <if any>
- **Need from Afu:** <only if needed>

---

## Operational Preference From Afu
Afu explicitly wants this behavior:
- If Afu gives a very large and complex command/task that cannot be completed well in one prompt, Clio should automatically choose a cron-job approach as the default execution strategy.
- The goal is reliability, staged execution, and continuity — not fake instant completion.
