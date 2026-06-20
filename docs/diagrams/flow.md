# Stock Explorer — PM Workflow

> Single source of truth for all workflow logic.

---

## Bootstrap Protocol

### Step 0: Check Previous Task
1. Look for `docs/state/task_*.md` (newest first)
2. If exists and status is "Completed" → delete it, proceed to Step 1
3. If exists and status is "Failed" / "In Progress" → read what happened, delete it, create NEW task with same goal + improved approach
4. If no task file → proceed to Step 1

### Step 1: Create Task File
Create `docs/state/task_YYYYMMDDHHMM.md`:
```markdown
# Task YYYYMMDD-HHMM

## Goal
[One sentence describing the goal]

## Priority
[Feedback / P0 / P1 / P2]

## Context
[Why this task now, what triggered it]

## Sign-ins
(Agents sign in here — see Double Sign-in Protocol)
```

### Step 2: Determine Task
**Priority order:**
1. `docs/feedback/` — ALWAYS first
2. `docs/overview/05-roadmap.md` — by P0 > P1 > P2

### Step 3: Assign Work
- **Minimum 4 agents** — fewer = failure
- Every task MUST include: goal, context, model, toolsets
- PM dispatches via `delegate_task`

### Step 4: Execute
- All work via `delegate_task`
- PM does NOT write code
- UI-first: prototype → review → implement → verify

### Step 5: Report
- PM reads task file, summarizes
- PM reports to discord
- PM deletes task file
- PM updates roadmap

---

## Double Sign-in Protocol (ALL Agents)

### First Sign-in (BEFORE work)
```
## Sign-in: [Role]
- **Model**: [model]
- **Role**: [role]
- **Goal**: [what you will do]
- **Status**: In Progress
```

### Second Sign-in (AFTER work)
```
## Sign-in: [Role]
- **Model**: [model]
- **Role**: [role]
- **Goal**: [what you will do]
- **Status**: Completed ✅ / Failed ❌
- **Done**: [brief summary]
- **Files**: [files changed]
- **Issues**: [if any]
```

PM uses the gap between first and second sign-ins to track progress.

---

## Error Handling

| Failure Type | PM Action |
|-------------|-----------|
| Sub-agent reports failure | Add context, re-dispatch |
| Sub-agent timeout | Reduce scope (max 2 files), re-dispatch |
| Wrong output | Specify exact fix, re-dispatch to SAME role |
| Fails 3 times | Add Challenger, change approach |

---

## Verification Failure — Rollback

| Failed Step | Roll Back To |
|-------------|-------------|
| Design Review | Fix specific visual issues |
| QA (functional test) | Fix bugs |
| Security review | Fix security issues |
| Challenger rejects plan | Re-design |

Never proceed with a failed verification.

---

## PM Workflow Summary

```
1. Check previous task → delete if exists
2. Read feedback → read roadmap → determine task
3. Create task file
4. Dispatch to ≥4 agents
5. Monitor sign-ins (git diff to verify)
6. If failure → re-dispatch with fix instructions
7. When all sign-ins complete → summarize → discord → delete task
8. Update roadmap + commit + push
```

---

## Task File Lifecycle

```
Created by PM → Agents sign in → Work done → Agents sign out → PM reads → PM reports → Deleted
```

Only ONE task file exists at a time. No accumulation.
