---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer (股識) multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is an ultra-lightweight router. It contains NO domain knowledge or architecture rules. Do not read the entire codebase upon waking. Execute the Bootstrap Protocol immediately.

---

## 1. 文件結構（新）

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
│   └── 008-yaml-config-driven.md
│
├── roles/                     # 🤖 AI Agent 角色定義
│   ├── pm.md
│   ├── architect.md
│   ├── developer.md
│   ├── designer.md
│   ├── qa.md
│   └── challenger.md
│
└── state/                     # 📊 狀態追蹤
    ├── current_problems.md
    ├── handoff.md
    └── pending_review.md
```

---

## 2. Team Roster & Model Assignments

| Role | Model | Responsibility | Role File |
|------|-------|----------------|-----------|
| **PM** | `openrouter/owl-alpha` | Coordinate, synthesize, assign work | `docs/roles/pm.md` |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | System architecture, data flow, feasibility | `docs/roles/architect.md` |
| **Developer** | `openrouter/owl-alpha` | Implementation, bug fixes, automated verification | `docs/roles/developer.md` |
| **Designer** | `openrouter/google/gemma-4-31b-it:free` | UX/UI alignment, visual system | `docs/roles/designer.md` |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Verification, testing, competitor analysis | `docs/roles/qa.md` |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | Cross-examine decisions, 3-round challenge | `docs/roles/challenger.md` |

**CRITICAL**: When spawning sub-agents, the PM MUST pass the `model` parameter from the table above.

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
- **Tier 2 (UI tweaks):** Developer + Designer peer review.
- **Tier 3 (Core Logic/Architecture):** Triggers Challenger for rigor. Path heuristics (`src/pages/*`, `docs/overview/02-architecture.md`) automatically escalate to Tier 3.

---

## 6. Development Rules (Quick Reference)

> ⚠️ 完整規則請見 `docs/overview/06-development-guide.md`

1. **分層架構**：Data → Service → Router → Presentation，禁止反向依賴
2. **i18n**：所有 UI 字串必須使用 `t()`，禁止 hardcoded 中文
3. **Config 驅動**：數據儲存使用 YAML，不使用資料庫
4. **LLM 安全**：只翻譯不推導，不給投資建議
5. **測試**：L0 必須在 commit 前通過，L1 在 handoff 前通過
