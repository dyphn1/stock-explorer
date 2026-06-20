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
| **PM** | `openrouter/owl-alpha` | Coordinate, synthesize, assign work, maintain docs |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | System architecture, data flow, infrastructure |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Security review, threat modeling, code audit |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | HTML prototypes, interaction flows, design system |
| **Developer** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Implementation, bug fixes, verification |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | Visual QA — verify implementation matches prototype |
| **User** | `openrouter/google/gemma-4-31b-it:free` | End-user advocate, beginner perspective |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Functional testing, competitor analysis |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge |

**CRITICAL**: When spawning sub-agents, the PM MUST pass the `model` parameter from the table above.

---

## 2. Core Rules

1. **UI-first**: All development starts from UI/UX. No backend without UI prototype.
2. **Never wait for user validation**: Build as if user will reject everything — make it undeniable.
3. **Minimum 4 agents**: Every cron run must involve at least 4 different roles.
4. **Feedback is urgent**: User feedback always takes priority over roadmap items.
5. **Handoff is one-shot**: Each session is independent. No continuous writing.
6. **PM is coordinator only**: PM does NOT write code or modify src/ files.

---

## 3. State Management

| File | Purpose | Updated By |
|------|---------|------------|
| `docs/state/task_YYYYMMDDHHMM.md` | Sign-in + task tracking for one cron run | All agents |
| `docs/feedback/` | User feedback (highest priority) | Daniel |
| `docs/overview/05-roadmap.md` | Work list | PM |
| `docs/adr/` | Architecture decisions | Architect |

---

## 4. Role Definitions

Detailed role definitions are in `docs/roles/`. Each role has its own file:

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

**When spawning a sub-agent, the PM MUST instruct it to read its role file first.**

---

## 5. Detailed Workflow

For the complete step-by-step workflow (sign-in, bootstrap, task routing, gate checks, handoff), see:

**👉 `docs/diagrams/flow.md`**
