# Workspace Operational Legibility

## Decision
Use workspace-level artifacts for continuity and operational legibility instead of modifying OpenClaw core to mimic Hermes-style architecture.

## Rationale
- keeps the approach update-safe
- preserves inspectability because artifacts are plain files
- avoids framework surgery just to gain process clarity
- lets Clio keep repo maps, playbooks, decision records, and validation notes in user-controlled workspace files

## Validation summary
- artifacts are stored only in workspace-owned paths
- no OpenClaw runtime/config/system files need to change for this pattern
- files remain easy to inspect, edit, move, or delete later

## Risks
- notes can become stale if not maintained
- too many files create clutter if not curated

## Mitigation
- keep files short and high-signal
- prefer a few durable notes over sprawling archives
- update only when a repo/project becomes strategically important or materially changes
