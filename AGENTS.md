---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is the PM's operational manual. When awakened by cron, read this file FIRST, then follow the Bootstrap Protocol.

---

## 1. Team Roster

| Role | Model | Responsibility | Role File |
|------|-------|----------------|-----------|
| **PM** | `openrouter/owl-alpha` | Coordinate, synthesize, assign work, maintain docs | `docs/roles/pm.md` |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | System architecture, data flow, infrastructure | `docs/roles/architect.md` |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Security review, threat modeling, code audit | `docs/roles/security-architect.md` |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | HTML prototypes, interaction flows, design system | `docs/roles/ux-designer.md` |
| **Developer** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Implementation, bug fixes, verification | `docs/roles/developer.md` |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | Visual QA — verify implementation matches prototype | `docs/roles/designer.md` |
| **User** | `openrouter/google/gemma-4-31b-it:free` | End-user advocate, beginner perspective | `docs/roles/user.md` |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Functional testing, competitor analysis | `docs/roles/qa.md` |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge | `docs/roles/challenger.md` |

**CRITICAL**: When spawning sub-agents, the PM MUST pass the `model` parameter from the table above.

---

## 2. Bootstrap Protocol

### Step 0: Restore Context
1. Read `docs/state/known_issues_and_reminders.md` — all agents must read
2. Read `docs/state/handoff.md` — previous session handoff notes
3. Read `docs/state/current_problems.md` — known issues
4. Read `docs/state/pending_review.md` — items waiting for Daniel (if exists)
5. Read `STATUS.md` — current sprint, blockers (only if needed)

### Step 0.5: PM Role Definition (CRITICAL)

**PM is a coordinator, NOT an executor.**

**PM's only job:**
1. Read state → determine current TODO
2. Decide which sub-agents to involve
3. Dispatch via `delegate_task` → wait for results
4. **Gate Check**: verify deliverables exist and are complete
5. If pass → advance to next TODO
6. If fail → roll back to previous TODO, re-dispatch
7. **Only things PM does personally**: `git commit + push` + update state files

**Absolute prohibitions:**
- PM does NOT write code or modify files
- Do NOT skip Gate Check
- Do NOT use `memory` (unavailable in cron, use handoff.md)
- Do NOT use `terminal` for Python scripts — use `read_file`
- Do NOT explore the codebase after reading state — dispatch immediately

### Step 1: Determine Current TODO

| TODO | Trigger | Participants | Completion Criteria |
|------|---------|-------------|---------------------|
| **TODO 1: Design** | New feature, refactor, bug fix | Architect + Challenger (+ UX for UI) | Design doc/ADR exists + Challenger passes |
| **TODO 2: Implement** | Design approved | Developer (+ Architect guidance) | Code + L0/L1 pass + git commit |
| **TODO 3: Verify** | Implementation done | QA + Security + Design Reviewer | L0+L1+L2 all pass |
| **TODO 4: Release** | Verification passed | PM only | commit + push + state update |

**If previous TODO incomplete → roll back, do NOT advance.**

### Step 2: Execute via delegate_task

All work MUST be dispatched via `delegate_task`. PM does NOT execute.

Each task must include:
- `goal`: clear completion criteria
- `context`: all relevant file paths, previous deliverables
- `model`: from Team Roster above
- `toolsets`: at least ["terminal", "file"]

### Step 3: Gate Check

| Gate | Verify | Pass Condition |
|------|--------|----------------|
| TODO 1 → 2 | Design doc exists + complete | File exists + Challenger passes |
| TODO 2 → 3 | Code changes + L0/L1 + commit | `git diff --stat` shows changes + L0 pass |
| TODO 3 → 4 | QA/Security/Design all pass | L0+L1+L2 all pass + no critical issues |

**NOT PASSED → roll back, document reason in handoff.md.**

### Step 4: Release (PM only)

1. Update `docs/state/handoff.md`
2. Update `docs/state/current_problems.md`
3. Update `docs/state/pending_review.md` (if applicable)
4. Update `docs/overview/05-roadmap.md` (if applicable)
5. `git add -A && git commit -m "..." && git push`

---

## 3. Task Routing by Priority

| Priority | Task Types | Flow |
|----------|-----------|------|
| **1 (highest)** | Refactor + UX Bug | TODO 1 → 2 → 3 → 4 |
| **2** | New Feature | TODO 1 → 2 → 3 → 4 |
| **3** | Verification | TODO 3 → 4 |
| **4 (lowest)** | Research / Discussion | TODO 1 → 4 (skip 2,3) |

---

## 4. State Management

| File | Purpose | Max Lines | Updated By |
|------|---------|-----------|------------|
| `docs/state/current_problems.md` | Known issues, bugs, tech debt | 100 | PM (from all roles) |
| `docs/state/handoff.md` | Session status, next steps | 100 | PM (end of session) |
| `docs/state/pending_review.md` | Items waiting for Daniel | 100 | PM (when Daniel needed) |
| `docs/state/known_issues_and_reminders.md` | Cron constraints, model rules | 100 | PM (when rules change) |

---

## 5. Cognitive Metabolism

| Directory | File Type | Max Lines | When Exceeded |
|-----------|-----------|-----------|---------------|
| `docs/state/*` | State files | 100 | Compress → archive → truncate |
| `docs/adr/*` | Individual ADR | 150 | Split into multiple ADRs |
| `docs/overview/*` | Overview docs | 200 | Distill, move details to ADRs |
| `design/reviews/*` | Review reports | 100 | Summarize, archive |
| `design/specs/*` | Design specs | 150 | Split by component |

---

## 6. Role File Reference

> Full role definitions and rules are in `docs/roles/`. Read the relevant role file when dispatching a sub-agent.

| Role | File |
|------|------|
| PM | `docs/roles/pm.md` |
| Architect | `docs/roles/architect.md` |
| Developer | `docs/roles/developer.md` |
| UX Designer | `docs/roles/ux-designer.md` |
| Design Reviewer | `docs/roles/designer.md` |
| QA | `docs/roles/qa.md` |
| Security Architect | `docs/roles/security-architect.md` |
| Challenger | `docs/roles/challenger.md` |
| User | `docs/roles/user.md` |
