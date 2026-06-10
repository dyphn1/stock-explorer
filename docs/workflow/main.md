# Workflow Overview

This folder describes the standard collaboration loop for Stock Explorer.

## Core Loop

1. Read the current state from `STATUS.md` and the relevant files under `docs/status/`.
2. **Read the previous cycle's handoff file** (`docs/status/handoff_{prev_theme}.md`) to restore context.
3. Read the current cycle's handoff file (`docs/status/handoff_{current_theme}.md`) if it exists from a previous run.
4. Start a standup and gather input from Architect, Developer, Designer, QA, and Challenger.
5. Challenge important decisions for up to 3 rounds.
6. Assign implementation or review work to the right role.
7. Update state files and record the outcome.
8. **Write the handoff file** (`docs/status/handoff_{current_theme}.md`) for the next cycle.

## Theme Rotation

- Development: fix bugs and implement features.
- Discussion: explore future directions and product ideas.
- Review: analyze gaps, optimize, and perform competitor research.

## State Handoff Mechanism

Each cron run produces a **handoff file** that the next run reads:

```
Cron Run (Theme A) → writes handoff_A.md
                         ↓
Cron Run (Theme B) → reads handoff_A.md + issues.md → works → writes handoff_B.md
                         ↓
Cron Run (Theme C) → reads handoff_B.md + issues.md → works → writes handoff_C.md
                         ↓
Cron Run (Theme A) → reads handoff_C.md + issues.md → works → writes handoff_A.md
```

### File Responsibilities

| File | Responsibility | Who Writes |
|------|---------------|------------|
| `STATUS.md` | Single entry point: current theme, milestones, verification log | PM (lightweight update) |
| `docs/status/handoff_dev.md` | Development cycle record: completed items, pending items, decisions | PM (dev cycle end) |
| `docs/status/handoff_discuss.md` | Discussion cycle record: ideas, decisions, action items | PM (discuss cycle end) |
| `docs/status/handoff_review.md` | Review cycle record: competitor findings, improvements, tech debt updates | PM (review cycle end) |
| `docs/status/issues.md` | Issue tracker: bugs, feature requests, priorities | PM (status changes only) |

### Reading Order (at cycle start)

```
STATUS.md → determine current theme
    ↓
docs/status/handoff_{current_theme}.md → restore context from previous same-theme run
    ↓
docs/status/issues.md → understand current work items
    ↓
{docs/workflow, docs/status}/{theme-specific files} → execute cycle
```

### Writing Order (at cycle end)

```
Execute work → record results
    ↓
Update docs/status/issues.md (mark status changes only)
    ↓
Write docs/status/handoff_{current_theme}.md (detailed record)
    ↓
Update STATUS.md (theme indicator + verification log, lightweight)
    ↓
Git commit
```

**CRITICAL:** The handoff file is the **primary state handoff**. If STATUS.md conflicts with handoff, the handoff wins.

---
