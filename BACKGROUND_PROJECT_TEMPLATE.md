# Background Project Template – Clio & Afu

This file defines how we (Afu + Clio) handle long-running projects that
should make progress "in the background" using DEV_NOTES + cron jobs.

## When Afu says: "kerjakan di background"

Clio will:

1. **Create a DEV_NOTES file for the project**
   - Location: inside the project root, e.g.
     - `project_root/DEV_NOTES.md`
   - Contents:
     - Brief project description + scope.
     - Current status (what exists now).
     - High-level requirements (features, boundaries).
     - Ordered implementation plan (Task 1, Task 2, ...), broken into
       small, concrete steps.
     - Working notes section for ad-hoc details.

2. **Define safe boundaries**
   - Explicitly state in DEV_NOTES or cron payload:
     - Project root path that may be edited.
     - Things that must **not** be touched (other projects, sensitive
       files, external services, configs, etc.).

3. **Set up a cron job (agentTurn) for the project**
   - Cron runs in an **isolated session** (`sessionTarget: "isolated"`).
   - Schedule: per Afu's request (e.g. every 15 minutes).
   - Payload message includes:
     - Project identity and root path.
     - Pointer to DEV_NOTES.
     - Constraints (stay inside project, no external side effects).
     - Behavioral loop:
       - Read DEV_NOTES.
       - Pick the next smallest concrete step.
       - Edit code/docs/schema accordingly.
       - Update DEV_NOTES (what was done + next steps).
       - Do **not** send external messages; all output goes into files.

4. **Development loop per cron run**
   - For each cron-triggered agentTurn:
     1. Read `DEV_NOTES.md`.
     2. Determine the highest-priority next step from the plan.
     3. Apply changes to files **only within project root**.
     4. Update `DEV_NOTES.md` under the relevant Task section:
        - Mark sub-step as done.
        - Add any follow-up steps discovered.
     5. Avoid destructive changes or risky refactors unless explicitly
        planned and documented in DEV_NOTES.

## Completion & Notifications

When Clio considers the project scope **completed** (relative to the
requirements defined in DEV_NOTES and our earlier conversation):

1. **Update DEV_NOTES**
   - Add a clear status line, e.g.:
     - `Status: COMPLETED – 2026-03-15`.
   - Summarize:
     - Which features are fully implemented.
     - Any deliberate omissions or known TODOs.

2. **Notify Afu in the main session (WhatsApp)**
   - Send a message explaining:
     - That the project is considered finished.
     - High-level summary of what works.
     - Where the main files/modules live.
     - How to run & test the project (commands, env vars needed).

3. **Then stop the cron job**
   - Disable or remove the project-specific cron job **after** sending
     the completion notification.
   - Optionally note in DEV_NOTES that the cron was stopped.

## Guardrails

- Background work is **never fully autonomous** in the sense of running
  arbitrary external actions. It is constrained to:
  - Editing files in the specified project root.
  - Updating documentation/notes.
  - Preparing code that Afu can later run/test.
- Anything that requires running external services (DB, brokers, etc.)
  or changing global config should be left as TODOs in DEV_NOTES for
  Afu to trigger manually or for an interactive session.

## How to check progress

- Afu can:
  - Open `DEV_NOTES.md` in the project to see:
    - current status,
    - which tasks are done,
    - what the background loop is likely to work on next.
  - Inspect project files for changes.
  - Optionally, review git history if the project uses Git.

This template applies to future background projects (e.g. aurora-chat,
other services) unless overridden by more specific instructions.
