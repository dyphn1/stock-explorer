# Stock Explorer — PM Workflow

> Single source of truth for all workflow logic.

---

## Bootstrap Protocol

### Step 0: Setup
1. Create `docs/state/` directory if it doesn't exist: `mkdir -p docs/state/`
2. Look for `docs/state/task_*.md` (newest first)
3. If exists and status is "Completed" → delete it, proceed to Step 1
4. If exists and status is "Failed" / "In Progress" → read what happened, delete it, create NEW task with same goal + improved approach
5. If no task file → proceed to Step 1

### Step 1: Verify Roadmap
1. Read `docs/overview/05-roadmap.md`
2. For each item, verify if it's actually done:
   - Check if the referenced files exist / have been modified
   - Check if tests pass
3. Update roadmap: mark verified-done items as `[x]`, remove stale items
4. PM only assigns INCOMPLETED items — never re-assign completed work

### Step 2: Determine Task
**Priority order:**
1. `docs/feedback/` — ALWAYS first (urgent)
2. `docs/overview/05-roadmap.md` — by P0 > P1 > P2 (incomplete items only)

### Step 3: Assign Work (≥4 agents, sequential)
- **Minimum 4 agents** — fewer = failure
- **Assign sequentially** — never concurrent. Each agent finishes before next starts.
- Every task MUST include: goal, context, model, toolsets
- **Challenger participates in planning** — review approach BEFORE development starts
- PM dispatches via `delegate_task`

### Step 4: Execute
- All work via `delegate_task`
- PM does NOT write code or read code
- PM verifies via: `git diff --stat` + agent sign-in summaries
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
| Fails 3 times | Add Challenger to diagnose, change approach |

---

## Verification Rules

**QA must block on ANY issue — no exceptions.**

| QA Finding | Action |
|-----------|--------|
| All tests pass, no issues | ✅ Pass — proceed |
| Minor issues (missing translation, typo) | ❌ Fail — roll back to Developer to fix |
| Test failures | ❌ Fail — roll back to Developer to fix |
| Security issues | ❌ Fail — roll back to Developer to fix |

**QA never marks "Completed" with outstanding issues.**

---

## Verification Failure — Rollback

| Failed Step | Roll Back To |
|-------------|-------------|
| Design Review | Fix specific visual issues |
| QA (functional test) | Fix bugs / missing translations |
| Security review | Fix security issues |
| Challenger rejects plan | Re-design |

**Never proceed with a failed verification.**

---

## Model Fallback

Each role has a primary and fallback model:

| Role | Primary | Fallback |
|------|---------|----------|
| PM | `openrouter/owl-alpha` | `openrouter/meta-llama/llama-3.2-3b-instruct:free` |
| Architect | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | `openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` |
| Developer | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | `openrouter/google/gemma-4-31b-it:free` |
| UX Designer | `openrouter/google/gemma-4-31b-it:free` | `openrouter/meta-llama/llama-3.2-3b-instruct:free` |
| Design Reviewer | `openrouter/google/gemma-4-31b-it:free` | `openrouter/meta-llama/llama-3.2-3b-instruct:free` |
| QA | `openrouter/google/gemma-4-31b-it:free` | `openrouter/meta-llama/llama-3.2-3b-instruct:free` |
| Security Architect | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | `openrouter/google/gemma-4-31b-it:free` |
| Challenger | `openrouter/openai/gpt-oss-120b:free` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` |
| User | `openrouter/google/gemma-4-31b-it:free` | `openrouter/meta-llama/llama-3.2-3b-instruct:free` |

### Fallback Protocol

When `delegate_task` fails for a role:
1. Retry with the **fallback model** from the table above
2. If fallback also fails → mark role as "Failed ❌" in task file
3. **Log the failure in the Model Failure Log** (see format below)
4. Do NOT assign the same working model to multiple roles just to save calls

---

## Model Failure Log

All model call failures MUST be logged in `docs/state/model-failure-log.md`.

### Log Entry Format

```markdown
## [YYYY-MM-DD HH:MM] Run: [task description]
| Role | Primary Model | Fallback Model | Result |
|------|-------------|---------------|--------|
| Challenger 1 | gpt-oss-120b:free (429 rate limit) | nemotron-120b ✅ used | Fallback succeeded |
| Developer | nemotron-120b ✅ (primary worked) | — | — |
| QA | gemma-31b ✅ (primary worked) | — | — |
```

### Summary Section (PM adds at end of each run)

```
### Model Health Summary
| Model Used | Times Called | Failures | Notes |
|------------|-------------|----------|-------|
| owl-alpha | 1 | 0 | PM only |
| nemotron-120b | 3 | 0 | +1 fallback from gpt-oss |
| gpt-oss-120b | 0 | 1 | 429 rate limited |
```

### Purpose

This log is used to:
- Track which models are chronically failing (rate limits, timeouts)
- Decide when to permanently swap a primary/fallback model
- Provide evidence-based data instead of anecdotal complaints

---

## PM Workflow Summary

```
1. mkdir -p docs/state/ (ensure directory exists)
2. Check previous task → delete if exists
3. Verify roadmap → update status → only look at incomplete items
4. Read feedback → read roadmap → determine task
5. Create task file
6. Assign to ≥4 agents (sequentially, not concurrent)
7. Challenger reviews plan BEFORE development
8. Monitor sign-ins (git diff to verify)
9. If failure → re-dispatch with fix instructions
10. QA must block on ANY issue — no pass with outstanding issues
11. When all sign-ins complete → summarize → discord → delete task
12. Update roadmap + commit + push
```

---

## Task File Lifecycle

```
Created by PM → Agents sign in → Challenger reviews plan → Development → QA verifies → Agents sign out → PM reads → PM reports → Deleted
```

Only ONE task file exists at a time. No accumulation.

---

## PM Verification (No Code Reading)

PM does NOT read code. PM verifies via:
- `git diff --stat HEAD` — confirms files were changed
- Agent sign-in summaries — confirms what was done
- Agent reports — confirms completion

PM is a product manager, not an engineer.
