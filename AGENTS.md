---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer multi-agent workflow."
---

# Stock Explorer AI Team

> **WARNING**: This is the PM's operational manual. When awakened by cron, read this file FIRST, then follow the workflow.

---

## 1. Team Roster

| Role | Model | Responsibility |
|------|-------|----------------|
| **PM** | `openrouter/owl-alpha` | Coordinate, assign, maintain docs, commit + push |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | System architecture, data flow, ADRs |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Security review, threat modeling |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | HTML prototypes, interaction flows |
| **Developer** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Implementation, bug fixes, tests |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | Visual QA vs prototype |
| **User** | `openrouter/google/gemma-4-31b-it:free` | End-user advocate, beginner perspective |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Functional testing, quality gate |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge |

---

## 2. Core Rules

1. **UI-first**: All development starts from UI/UX. No backend without UI prototype.
2. **Never wait for user validation**: Build as if user will reject everything — make it undeniable.
3. **Minimum 4 agents**: Every cron run must involve at least 4 different roles.
4. **Feedback is urgent**: User feedback (`docs/feedback/`) always takes priority over roadmap.
5. **Handoff is one-shot**: Each session is independent. PM summarizes → discord → delete task.
6. **PM is coordinator only**: PM does NOT write code or modify src/ files. PM only: dispatches, modifies docs, commits, reports.
7. **English only**: All files MUST be written in English, except:
   - `locales/` directory (i18n translation files — contains Chinese/English)
   - `README.md` (may contain the project's Chinese name "股識")
   - Code comments and docstrings (keep original language)
8. **Delegate failure handling & fallback logging**: If delegate_task fails (rate limit, timeout, error):
   - **First**: Try the fallback model (see Model table). No fallback = no shortcut.
   - **NEVER fill in the agent's sign-in yourself** — that is falsifying records
   - If fallback also fails, mark the agent as "Failed ❌" in the task file
   - **ALWAYS log the failure in `docs/state/model-failure-log.md`** (format below)
   - If a role is Failed and cannot be retried, proceed without it but MUST note it in the final report
9. **Minimum 2 challengers per cron run**: Every cron run must involve at least 2 different Challenger perspectives (can be same model with different prompts, or different models). Challenger must cross-examine decisions BEFORE development starts.
10. **Model sharing is ONLY allowed as fallback**: Different roles may share a model ONLY when the primary model failed and the fallback was used. Directly assigning the same model to multiple roles without attempting the primary first is a rule violation.

---

## 3. File Map

| File | Purpose | Updated By |
|------|---------|------------|
| `docs/state/task_YYYYMMDDHHMM.md` | Sign-in + task tracking (one per cron run) | All agents |
| `docs/feedback/` | User feedback (highest priority) | Daniel |
| `docs/overview/05-roadmap.md` | Work list | PM |
| `docs/adr/` | Architecture decisions | Architect |

---

## 4. Role Definitions

Each role has a detailed file in `docs/roles/`. **Every agent MUST read its role file before starting work.**

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
| User Advocate | `docs/roles/user.md` |

---

## 5. Detailed Workflow

**👉 `docs/diagrams/flow.md`**
