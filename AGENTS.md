---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer (股識) multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is an ultra-lightweight router. It contains NO domain knowledge or architecture rules. Do not read the entire codebase upon waking. Execute the Bootstrap Protocol immediately.

---

## 1. 文件結構

```
docs/
├── overview/                  # 📖 專案總覽文件
│   ├── 00-index.md            # 文件索引
│   ├── 01-product-vision.md   # 產品願景
│   ├── 02-architecture.md     # 系統架構
│   ├── 03-design-system.md    # 設計系統
│   ├── 04-tech-stack.md       # 技術選型
│   ├── 05-roadmap.md          # 開發路線圖
│   └── 06-development-guide.md # 開發指南
│
├── adr/                       # 📋 架構決策記錄
│   ├── 000-index.md           # ADR 索引
│   ├── 001-streamlit-as-frontend.md
│   ├── 002-finmind-as-data-source.md
│   ├── 003-layered-architecture.md
│   ├── 004-plugin-chassis.md
│   ├── 005-i18n-yaml.md
│   ├── 006-browser-back-button.md
│   ├── 007-llm-safety-boundary.md
│   ├── 008-yaml-config-driven.md
│   ├── 009-layout-restructure.md
│   └── 010-ppt-style-design.md
│
├── roles/                     # 🤖 AI Agent 角色定義
│   ├── pm.md
│   ├── architect.md
│   ├── ux-designer.md         # ← 新增：UX 設計師
│   ├── designer.md            # Design Reviewer（審核實現）
│   ├── developer.md
│   ├── qa.md
│   └── challenger.md
│
└── state/                     # 📊 狀態追蹤
    ├── current_problems.md
    ├── handoff.md
    └── pending_review.md

design/                        # 🎨 UX 設計原型（HTML）
├── index.html                 # 原型入口
├── prototypes/                # 各頁面 HTML 原型
├── components/                # 可重用元件
├── assets/                    # CSS、設計變數
└── reviews/                   # 設計審核報告
```

---

## 2. Team Roster & Model Assignments

| Role | Model | Responsibility | Role File |
|------|-------|----------------|-----------|
| **PM** | `openrouter/owl-alpha` | Coordinate, synthesize, assign work | `docs/roles/pm.md` |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | **Full system architecture** — code structure, data flow, infrastructure, security, cross-cutting concerns | `docs/roles/architect.md` |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | **UI/UX design** — HTML prototypes, interaction flows, design system compliance | `docs/roles/ux-designer.md` |
| **Developer** | `openrouter/owl-alpha` | Implementation, bug fixes, automated verification | `docs/roles/developer.md` |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | **Visual QA** — verify implementation matches prototype & design system | `docs/roles/designer.md` |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Functional testing, competitor analysis | `docs/roles/qa.md` |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge | `docs/roles/challenger.md` |

**CRITICAL**: When spawning sub-agents, the PM MUST pass the `model` parameter from the table above.

### 角色分工說明

```
┌─────────────────────────────────────────────────────────────┐
│                        PM (協調者)                           │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│ Architect│UX Designer│Developer │Design    │ QA + Challenger │
│ (系統架構)│ (UI設計)  │ (實作)   │Reviewer  │ (品質把關)       │
│          │          │          │(視覺審核) │                 │
└──────────┴──────────┴──────────┴──────────┴─────────────────┘

設計流程：
  UX Designer → HTML prototype → Daniel review → Developer 實作
                                                      ↓
                                              Design Reviewer 審核
                                                      ↓
                                              QA 功能測試

開發流程：
  Architect 設計系統方案 → UX Designer 設計 UI → Developer 實作
       ↓                                              ↓
  Challenger 挑戰 ←──────────────────────── Design Reviewer 審核
```

---

## 3. The Bootstrap Protocol (PM's Waking Steps)

1. **Read Payload**: Read the cron-injected target and `docs/state/handoff.md` to restore working memory.
2. **Read Context**: Read `docs/overview/05-roadmap.md` for current sprint status.
3. **Delegate**: Spawn specialized sub-agents with the target and relevant file paths.
4. **Release (Non-blocking)**: If a decision requires Daniel review, make a best-effort decision, implement it, record in `docs/state/pending_review.md`, and move on.

---

## 4. Cognitive Metabolism (Strict File Limits)

| Directory | File Type | Max Lines |
|-----------|-----------|-----------|
| `docs/state/*` | Issues, handoff, pending_review | 100 |
| `docs/logs/*` | Verify logs, discussion | 200 |
| `docs/adr/*` | Individual ADR | 150 |
| `docs/overview/*` | Overview docs | 200 |

**Action:** If limits are exceeded, trigger a **Compression Cycle**: distil lessons into `docs/adr/` or `docs/overview/`, then truncate.

---

## 5. Adaptive Alignment

- **Start/End Standups:** Read `docs/overview/01-product-vision.md` at sprint start. Review alignment at sprint end.
- **Tier 1 (Minor fixes):** Direct to Developer. 0 challenges.
- **Tier 2 (UI changes):** UX Designer creates prototype → Developer implements → Design Reviewer verifies.
- **Tier 3 (New features):** Full flow — Architect (feasibility) → UX Designer (prototype) → Daniel review → Developer (implement) → Design Reviewer (visual QA) → QA (functional test) → Challenger (3-round challenge).
- **Tier 4 (Core Architecture):** Triggers Challenger for rigor. Path heuristics (`src/pages/*`, `docs/overview/02-architecture.md`) automatically escalate to Tier 4.

---

## 6. Development Rules (Quick Reference)

> ⚠️ 完整規則請見 `docs/overview/06-development-guide.md`

1. **分層架構**：Data → Service → Router → Presentation，禁止反向依賴
2. **i18n**：所有 UI 字串必須使用 `t()`，禁止 hardcoded 中文
3. **Config 驅動**：數據儲存使用 YAML，不使用資料庫
4. **LLM 安全**：只翻譯不推導，不給投資建議
5. **測試**：L0 必須在 commit 前通過，L1 在 handoff 前通過
