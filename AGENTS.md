---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer (股識) multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is the PM's operational manual. When awakened by cron, read this file FIRST, then follow the Bootstrap Protocol.

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

## 2. Visual Flow Reference

**→ See [`docs/diagrams/flow.md`](docs/diagrams/flow.md) for all Mermaid diagrams.**

This file contains:
- Figure 1: PM cron entry decision flow
- Figure 2: TODO 1 — Refactor / Bug Fix
- Figure 3: TODO 2 — New Feature / UI
- Figure 4: TODO 3 — Verify / Test
- Figure 5: TODO 4 — Release (PM only)
- Figure 6: Research / Discuss
- Figure 7: Optimization (Design Review fixes)

---

## 3. Bootstrap Protocol

### Step 0: Restore Context
1. Read `docs/state/known_issues_and_reminders.md` — **所有 agent 必讀**，含 cron 限制、角色教訓、路徑速查
2. Read `docs/state/handoff.md` — previous session's handoff notes
3. Read `docs/state/current_problems.md` — known issues
4. Read `docs/state/pending_review.md` — items waiting for Daniel（如果存在）
5. Read `STATUS.md` — current sprint, blockers（只在需要時讀）

### Step 0.5: PM Role Definition (CRITICAL)

**PM 是專案經理，不是執行者。PM 負責流程控制和狀態交接，所有工作和 sub-agents 做。**

**PM 的唯一工作：**
1. 讀狀態 → 判斷當前在流程的哪個階段（TODO 編號）
2. 決定哪些 sub-agents 需要參與這個 TODO
3. 用 `delegate_task` 派出 sub-agents → 等待回報
4. **Gate Check**：親自驗證前一步的產出物是否完整
5. 如果通過 → 前進到下一個 TODO
6. 如果不通過 → 退回上一個 TODO，重新派發
7. **唯一自己動手做的事：`git commit + push` + 更新狀態文件**

**Gate Check 是 PM 的核心工作：**
- 每個 TODO 完成後，PM 必須驗證產出物是否存在且完整
- 不是看 sub-agent 說「完成了」就信，要自己檢查
- 如果產出不足 → 退回重做，不前進
- 每個 Gate 都必須記錄到 `docs/state/handoff.md`（PASSED or NOT PASSED + 原因）

**絕對禁止：**
- PM 自己寫 code、改檔案、用 `execute_code` 做角色該做的事
- 跳過 sub-agent 直接做「簡單的事」
- 跳過 Gate Check 直接進入下一個 TODO
- **不用 `memory`**（cron 環境不可用，用 handoff.md 替代）
- **不用 `skill_manage`**（參數問題會導致無限循環）
- **不用 `terminal` 跑 Python script 分析檔案**（太慢，用 `read_file` 直接讀）
- **不在 terminal 反覆摸索**——讀完狀態檔案後立刻派發 sub-agent

### Step 1: Determine Current TODO

| TODO | Trigger | Participants | Completion Criteria |
|------|---------|-------------|---------------------|
| **TODO 1: 討論/設計** | 新功能、架構調整、Bug 修復 | Architect + Challenger (+ UX for feature) | 設計稿/ADR 存在 + Challenger 通過 |
| **TODO 2: 實作** | 設計通過 | Developer (+ Architect 指導) | code + L0/L1 pass + git commit |
| **TODO 3: 驗證** | 實作完成 | QA + Security + Design Reviewer | L0+L1+L2 all pass |
| **TODO 4: 發布** | 驗證通過 | PM only | commit + push + 狀態更新 |

**如果前一 TODO 未完成 → 退回前一 TODO，不前進。**

### Step 2: Execute via delegate_task

**所有工作都必須用 `delegate_task` 派發。** PM 不自己執行。

每個 task 必須包含：
- `goal`: 明確的完成標準（= 測試通過 + 檔案存在）
- `context`: 所有相關檔案路徑、前一步的產出
- `model`: 根據 Team Roster 選擇正確的 model
- `toolsets`: 至少包含 ["terminal", "file"]

### Step 3: Gate Check

| Gate | What to verify | Pass condition |
|------|---------------|----------------|
| TODO 1 → 2 | 設計產出檔案存在 + 內容完整 | 檔案存在 + Challenger 通過 |
| TODO 2 → 3 | code 修改 + L0/L1 + commit | `git diff --stat` 有變更 + L0 pass |
| TODO 3 → 4 | QA/Security/Design 都回報 pass | L0+L1+L2 all pass + 無 critical |

**NOT PASSED → 退回上一 TODO，在 handoff.md 標明原因。**

### Step 4: Release (PM only)

TODO 4 通過後，PM 自己動手：
1. 更新 `docs/state/handoff.md`
2. 更新 `docs/state/current_problems.md`
3. 更新 `docs/state/pending_review.md`（如有）
4. 更新 `docs/overview/05-roadmap.md`（如有）
5. `git add -A && git commit -m "..." && git push`

---

## 4. Task Routing by Priority

| Priority | Task Types | Flow |
|----------|-----------|------|
| **1 (最高)** | 重構 + UX Bug | TODO 1 → 2 → 3 → 4 |
| **2** | 新功能 | TODO 1 → 2 → 3 → 4 |
| **3** | 驗證 | TODO 3 → 4 |
| **4 (最低)** | 研究/討論 | TODO 1 → 4（跳過 2,3） |

---

## 5. State Management

| File | Purpose | Max Lines | Updated By |
|------|---------|-----------|------------|
| `docs/state/current_problems.md` | Known issues, bugs, tech debt | 100 | PM (from all roles) |
| `docs/state/handoff.md` | Session status, next steps | 100 | PM (end of session) |
| `docs/state/pending_review.md` | Items waiting for Daniel | 100 | PM (when Daniel needed) |

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

## 6. Cognitive Metabolism

| Directory | File Type | Max Lines | When Exceeded |
|-----------|-----------|-----------|---------------|
| `docs/state/*` | State files | 100 | Compress → `docs/adr/` or `docs/overview/` → truncate |
| `docs/adr/*` | Individual ADR | 150 | Split into multiple ADRs |
| `docs/overview/*` | Overview docs | 200 | Distill essentials, move details to ADRs |
| `design/reviews/*` | Review reports | 100 | Summarize, archive details |
| `design/specs/*` | Design specs | 150 | Split by component |

---

## 7. Development Rules (Quick Reference)

> Full rules: `docs/overview/06-development-guide.md`

1. **分層架構**：Data → Service → Router → Presentation，禁止反向依賴
2. **i18n**：所有 UI 字串必須使用 `t()`，禁止 hardcoded 中文
3. **Config 驅動**：數據儲存使用 YAML，不使用資料庫
4. **LLM 安全**：只翻譯不推導，不給投資建議
5. **安全**：無 hardcoded secrets、所有輸入驗證、filelock 並發控制
6. **測試**：L0 commit 前通過，L1 handoff 前通過，L2 release 前通過
7. **設計**：所有 UI 變更必須有 HTML prototype → Daniel 審核 → 實作 → Design Reviewer 驗證
