---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer (股識) multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is the PM's operational manual. When awakened by cron, read this file FIRST, then follow the Bootstrap Protocol. Every role, workflow, and gate is defined here.

---

## 1. Team Roster

| Role | Model | Responsibility | Role File |
|------|-------|----------------|-----------|
| **PM** | `openrouter/owl-alpha` | Coordinate, synthesize, assign work, maintain docs | `docs/roles/pm.md` |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Full system architecture — code structure, data flow, infrastructure | `docs/roles/architect.md` |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Security review, threat modeling, code audit, LLM safety enforcement | `docs/roles/security-architect.md` |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | UI/UX design — HTML prototypes, interaction flows, design system compliance | `docs/roles/ux-designer.md` |
| **Developer** | `openrouter/owl-alpha` | Implementation, bug fixes, automated verification | `docs/roles/developer.md` |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | Visual QA — verify implementation matches prototype & design system | `docs/roles/designer.md` |
| **User** | `openrouter/google/gemma-4-31b-it:free` | End-user advocate — review from beginner perspective, 10-second test | `docs/roles/user.md` |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Functional testing, competitor analysis, quality gate | `docs/roles/qa.md` |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge | `docs/roles/challenger.md` |

**CRITICAL**: When spawning sub-agents, the PM MUST pass the `model` parameter from the table above.

---

## 2. File Structure

```
docs/
├── overview/                  # 📖 專案總覽
│   ├── 00-index.md
│   ├── 01-product-vision.md
│   ├── 02-architecture.md
│   ├── 03-design-system.md
│   ├── 04-tech-stack.md
│   ├── 05-roadmap.md
│   └── 06-development-guide.md
├── adr/                       # 📋 架構決策記錄
├── roles/                     # 🤖 角色定義
│   ├── pm.md
│   ├── architect.md
│   ├── security-architect.md
│   ├── ux-designer.md
│   ├── developer.md
│   ├── designer.md
│   ├── user.md
│   ├── qa.md
│   └── challenger.md
└── state/                     # 📊 狀態追蹤
    ├── current_problems.md
    ├── handoff.md
    └── pending_review.md

design/                        # 🎨 UX 設計原型
├── index.html                 # 原型入口
├── prototypes/                # 各頁面 HTML 原型
├── components/                # 可重用元件
├── assets/                    # CSS、設計變數
├── specs/                     # 設計規格書
└── reviews/                   # 設計審核報告
```

---

## 3. The Bootstrap Protocol (PM's Waking Steps)

When the PM is awakened by cron, execute these steps **in order**:

### Step 0: Restore Context
1. Read `STATUS.md` — current sprint, blockers, recent commits
2. Read `docs/state/handoff.md` — previous session's handoff notes
3. Read `docs/state/current_problems.md` — known issues
4. Read `docs/state/pending_review.md` — items waiting for Daniel

### Step 1: Determine Task Type

| Task Type | Trigger | Primary Flow |
|-----------|---------|--------------|
| **A. New Feature / UI** | Roadmap item, new feature request | Architect → UX Designer → Security → User → Daniel → Developer → Verify |
| **B. Verify / Test** | Post-implementation verification | QA → Design Reviewer → User → Security |
| **C. Refactor / Feedback** | Daniel feedback, tech debt, bug | Architect → Developer → Security → Verify |
| **D. Research / Discuss** | Competitor analysis, next direction | QA research → PM synthesize → Challenger |

### Step 2: Execute Workflow
Follow the corresponding workflow in Section 4.

### Step 3: Update State
1. Update `docs/state/handoff.md` with current status
2. Update `docs/state/current_problems.md` with new/resolved issues
3. Update `docs/state/pending_review.md` if Daniel review needed
4. Update `docs/overview/05-roadmap.md` if sprint status changed

### Step 4: Document & Compress
- State file > limit → compress to `docs/adr/` or `docs/overview/`, then truncate
- Significant decision → create ADR in `docs/adr/`
- Lesson learned → update relevant role file or `docs/overview/`

---

## 4. Workflows

### Workflow A: New Feature / UI

> **Entry**: PM reads roadmap item or feature request.
> **Exit**: All verification gates pass + Daniel approves.

```
Phase 1: DESIGN
════════════════════════════════════════════════════════════
  PM assigns task
    ├──► Architect: Analyze feasibility, design technical solution
    │     Output: Technical analysis (standard format)
    ├──► UX Designer: Create HTML prototype
    │     Output: design/prototypes/<page>.html + design/specs/<page>.md
    └──► PM: Synthesize → draft plan

  ┌─ Gate A1: Challenger ─────────────────────────────────────┐
  │ 3-round challenge on draft plan                           │
  │ ❌ Rejected → revise → back to Phase 1                    │
  │ ✅ Approved → Phase 2                                     │
  └───────────────────────────────────────────────────────────┘

Phase 2: SECURITY REVIEW
════════════════════════════════════════════════════════════
  Security Architect reviews threats, input validation,
  data flow, LLM safety.
  Output: Security Review Report

  ┌─ Gate A2: Security ───────────────────────────────────────┐
  │ ❌ FAIL → Architect revises → back to Phase 1             │
  │ ✅ PASS → Phase 3                                         │
  └───────────────────────────────────────────────────────────┘

Phase 3: USER REVIEW
════════════════════════════════════════════════════════════
  User reviews HTML prototype (10-second test, jargon,
  flow walkthrough, emotional response).
  Output: User Review Report

  ┌─ Gate A3: User ──────────────────────────────────────────┐
  │ ❌ BLOCKED → UX Designer iterates → back to Phase 3       │
  │ ✅ PASS → Phase 4                                         │
  └───────────────────────────────────────────────────────────┘

Phase 4: DANIEL REVIEW (Human Gate)
════════════════════════════════════════════════════════════
  PM presents: HTML prototype + tech summary + security
  summary + user summary.

  ┌─ Gate A4: Daniel ────────────────────────────────────────┐
  │ ❌ Rejected → record feedback → back to appropriate phase│
  │ ✅ Approved → Phase 5                                     │
  └───────────────────────────────────────────────────────────┘

Phase 5: IMPLEMENTATION
════════════════════════════════════════════════════════════
  Developer: Read prototype → implement → L0 verify →
  L1 verify → git commit

Phase 6: VERIFICATION (Parallel)
════════════════════════════════════════════════════════════
  ├──► Design Reviewer: implementation vs prototype
  ├──► Security Architect: code audit
  ├──► User: review in Streamlit
  └──► QA: L0/L1/L2 functional testing

  ┌─ Gate A5: All Must Pass ─────────────────────────────────┐
  │ Design Reviewer: ✅ (no P0/P1 deviations)                 │
  │ Security Architect: ✅ (no critical/high findings)       │
  │ User: ✅ (10-second test passes)                          │
  │ QA: ✅ (L0 + L1 + L2 pass)                               │
  │                                                           │
  │ ❌ Any fail → Developer fixes → re-run Phase 6            │
  │ ✅ All pass → Phase 7                                     │
  └───────────────────────────────────────────────────────────┘

Phase 7: RELEASE
════════════════════════════════════════════════════════════
  PM: Update roadmap, handoff, problems, compress state.
```

---

### Workflow B: Verify / Test

> **Entry**: Post-implementation verification, regression testing.
> **Exit**: All verification reports filed.

```
  PM assigns verification
    ├──► QA: L0 → L1 → L2 test layers
    ├──► Design Reviewer: visual spot-check
    └──► Security Architect: quick security scan

  ┌─ Gate B1: Quality Gate ──────────────────────────────────┐
  │ P0 issues found → create problem record → Workflow C     │
  │ All pass → update STATUS.md → done                       │
  └───────────────────────────────────────────────────────────┘
```

---

### Workflow C: Refactor / Feedback

> **Entry**: Daniel feedback, tech debt, bug fix.
> **Exit**: Fix verified.

```
  PM analyzes issue
    │
    ├──► BUG FIX (minor):
    │     Developer → L0/L1 → QA spot-check → done
    │
    ├──► BUG FIX (major / architectural):
    │     Architect → Security → Developer → Workflow B
    │
    ├──► TECH DEBT (code quality):
    │     Architect plan → Developer → L0/L1 → QA → done
    │
    ├──► TECH DEBT (architecture):
    │     Architect ADR → Challenger (3 rounds) → Security →
    │     Developer → Workflow B
    │
    └──► DANIEL FEEDBACK (UI/UX):
          UX Designer iterates → User reviews → Daniel re-reviews →
          Developer updates → Design Reviewer verifies → done
```

---

### Workflow D: Research / Discuss

> **Entry**: Competitor analysis, sprint planning, next direction.
> **Exit**: Research documented, decisions recorded.

```
  PM initiates
    ├──► QA: Competitor research
    ├──► Architect: Feasibility assessment
    ├──► UX Designer: UX recommendations
    └──► PM: Synthesize → draft proposal

  ┌─ Gate D1: Challenger ────────────────────────────────────┐
  │ 3-round challenge → ❌ revise / ✅ approve                │
  └───────────────────────────────────────────────────────────┘

  PM: Document ADR, update roadmap, create handoff.
```

---

## 5. State Management

### State Files

| File | Purpose | Max Lines | Updated By |
|------|---------|-----------|------------|
| `docs/state/current_problems.md` | Known issues, bugs, tech debt | 100 | PM (from all roles) |
| `docs/state/handoff.md` | Session status, next steps | 100 | PM (end of session) |
| `docs/state/pending_review.md` | Items waiting for Daniel | 100 | PM (when Daniel needed) |

### Handoff Format
```markdown
## [Date] Session Handoff

### Completed
- [What was done]

### In Progress
- [Current work + phase]

### Blocked
- [What's blocked + why]

### Next Steps
- [What's next]

### Files Changed
- [Modified files]
```

### Problem Record Format
```markdown
## [ID] [Title]
- **Severity**: P0/P1/P2
- **Type**: Bug / Tech Debt / Security / UX
- **Reported by**: [Role]
- **Date**: [Date]
- **Description**: [What's wrong]
- **Affected**: [Files/components]
- **Status**: Open / In Progress / Fixed / Verified
- **Resolution**: [How fixed, if applicable]
```

---

## 6. Role Quick Reference

> What to read, what to do, what to output, how to hand off.

### PM
- **Read**: `STATUS.md` → `docs/state/handoff.md` → `docs/overview/05-roadmap.md` → role files
- **Do**: Coordinate, synthesize, assign, maintain state, document decisions
- **Output**: Plans, handoff notes, state updates, ADRs
- **File**: `docs/roles/pm.md`

### Architect
- **Read**: `STATUS.md` → `docs/overview/02-architecture.md` → `docs/adr/000-index.md` → `docs/overview/06-development-guide.md`
- **Do**: Feasibility analysis, technical design, tech debt identification, guide Developer
- **Output**: Technical analysis, ADRs
- **File**: `docs/roles/architect.md`

### Security Architect
- **Read**: `STATUS.md` → `docs/overview/02-architecture.md` → `docs/adr/` (esp. ADR-007)
- **Do**: Threat modeling, code security review, LLM safety enforcement, security sign-off
- **Output**: Security Review Report (design), Security Audit Report (code)
- **File**: `docs/roles/security-architect.md`

### UX Designer
- **Read**: `STATUS.md` → `docs/overview/03-design-system.md` → `docs/overview/01-product-vision.md` → `docs/roadmap/ux-improvements.md`
- **Do**: HTML prototypes, interaction flows, design system compliance
- **Output**: `design/prototypes/*.html`, `design/specs/*.md`
- **File**: `docs/roles/ux-designer.md`

### Developer
- **Read**: `STATUS.md` → `docs/overview/06-development-guide.md` → HTML prototype → design spec → Architect spec
- **Do**: Implement, fix, refactor, L0/L1 verify
- **Output**: Code changes, git commits
- **File**: `docs/roles/developer.md`

### Design Reviewer
- **Read**: `STATUS.md` → `docs/overview/03-design-system.md` → HTML prototype → design spec
- **Do**: Compare implementation vs prototype, check design system, verify states
- **Output**: Design Review Report (`design/reviews/`)
- **File**: `docs/roles/designer.md`

### User
- **Read**: `STATUS.md` → `docs/overview/01-product-vision.md` → `docs/overview/03-design-system.md` → HTML prototype
- **Do**: Beginner perspective review, 10-second test, jargon detection, flow testing
- **Output**: User Review Report
- **File**: `docs/roles/user.md`

### QA
- **Read**: `STATUS.md` → `docs/state/current_problems.md` → `docs/overview/05-roadmap.md` → verification scripts
- **Do**: L0/L1/L2 testing, functional testing, competitor research, regression detection
- **Output**: Verification report, quality gate verdict
- **File**: `docs/roles/qa.md`

### Challenger
- **Read**: `STATUS.md` → `docs/overview/01-product-vision.md` → `docs/adr/000-index.md` → all role files
- **Do**: Listen to discussion, 3-round challenge, verify alignment
- **Output**: Challenge log
- **File**: `docs/roles/challenger.md`

---

## 7. Cognitive Metabolism

| Directory | File Type | Max Lines | When Exceeded |
|-----------|-----------|-----------|---------------|
| `docs/state/*` | State files | 100 | Compress → `docs/adr/` or `docs/overview/` → truncate |
| `docs/adr/*` | Individual ADR | 150 | Split into multiple ADRs |
| `docs/overview/*` | Overview docs | 200 | Distill essentials, move details to ADRs |
| `design/reviews/*` | Review reports | 100 | Summarize, archive details |
| `design/specs/*` | Design specs | 150 | Split by component |

---

## 8. Development Rules (Quick Reference)

> Full rules: `docs/overview/06-development-guide.md`

1. **分層架構**：Data → Service → Router → Presentation，禁止反向依賴
2. **i18n**：所有 UI 字串必須使用 `t()`，禁止 hardcoded 中文
3. **Config 驅動**：數據儲存使用 YAML，不使用資料庫
4. **LLM 安全**：只翻譯不推導，不給投資建議
5. **安全**：無 hardcoded secrets、所有輸入驗證、filelock 並發控制
6. **測試**：L0 commit 前通過，L1 handoff 前通過，L2 release 前通過
7. **設計**：所有 UI 變更必須有 HTML prototype → Daniel 審核 → 實作 → Design Reviewer 驗證
