# Workflow Overview

This folder describes the standard collaboration loop for Stock Explorer.

## Core Loop

1. Read the current state from `docs/state/handoff.md` — this is the **single source of truth** for cross-cycle state.
2. Read `docs/state/issues.md` and `docs/state/pending_review.md` for current work items.
3. Determine the current theme from the handoff file's "Next Cycle Handoff" section.
4. Start a standup and gather input from Architect, Developer, Designer, QA, and Challenger.
5. Challenge important decisions for up to 3 rounds.
6. Assign implementation or review work to the right role.
7. Update state files and record the outcome.
8. **Append to `docs/state/handoff.md`** the current cycle's record (dev/discuss/review section).

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
| `docs/state/handoff.md` | Single source of truth: all cycle records (dev/discuss/review sections) | PM (append each cycle) |
| `docs/state/issues.md` | Issue tracker: bugs, feature requests, priorities | PM (status changes only) |
| `docs/state/pending_review.md` | Items requiring Daniel's decision | PM (when human judgment needed) |
| `docs/state/current_problems.md` | Known problems including non-bugs | PM (during review themes) |
| `docs/state/tech_debt.md` | Technical debt items | PM (during review themes) |

### Reading Order (at cycle start)

```
docs/state/handoff.md → determine current theme + restore context
    ↓
docs/state/issues.md → understand current work items
    ↓
docs/state/pending_review.md → check for Daniel's pending decisions
    ↓
docs/workflow/{theme}.md → execute cycle (dev/discuss/review)
```

### Writing Order (at cycle end)

```
Execute work → record results
    ↓
Update docs/state/issues.md (mark status changes only)
    ↓
Append to docs/state/handoff.md (current theme section)
    ↓
Git commit
```

**CRITICAL:** The handoff file is the **primary state handoff**. It must be written/appended every cycle.

---
