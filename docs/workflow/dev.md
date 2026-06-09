# 🔧 Development Topic Workflow (DEV WORKFLOW)

> When STATUS.md specifies the topic as "Development," the PM follows this workflow.

---

## Development Topic Goals
- Fix bugs in `docs/status/issues.md`
- Implement new features
- Pass L0/L1 verification

---

## Flow Diagram (Complete)

```mermaid
flowchart TD
    A([🔧 開發主題開始]) --> B[PM 讀取 STATUS.md]
    B --> C[PM 讀取 docs/status/issues.md]
    C --> D{有未解決的 issues?}
    
    D -- 否 --> E[檢查 CURRENT_PROBLEMS.md]
    E --> F{有已知問題?}
    F -- 否 --> G[PM 更新 STATUS.md: 無任務，等待新需求]
    G --> Z([結束：SILENT])
    
    D -- 是 --> H[PM 讀取對應 source code]
    H --> I[PM 分派給 Developer: 修復 bug]
    I --> J[Developer 分析根因]
    J --> K[Developer 實作修復]
    K --> L[Developer 執行 L0/L1 驗證]
    L --> M{驗證通過?}
    
    M -- 否 --> N[Developer 修正]
    N --> K
    
    M -- 是 --> O[Developer git commit]
    O --> P[PM 更新 ISSUES.md: 標記已修復]
    P --> Q[PM 更新 STATUS.md]
    Q --> R[PM 回報 Daniel]
    R --> Z
    
    F -- 是 --> S[Architect 分析技術可行性]
    S --> T[Developer 評估實作成本]
    T --> U[團隊討論: 優先級排序]
    U --> V[Challenger 質疑: 這是正確的優先級嗎？]
    V --> W{Challenger 確認?}
    W -- 否 --> U
    W -- 是 --> I
```

---

## PM Tasks (Detailed)

### Step 1: Read Status
```
Read the following files:
1. STATUS.md → Confirm the current topic is "Development"
2. docs/status/issues.md → List all unresolved issues
3. docs/status/current_problems.md → Understand known problems
```

### Step 2: Dispatch Work
```
Dispatch based on issue type:
- Bug fix → Developer
- Requires architecture analysis → Dispatch to Architect first
- Requires design review → Confirm Design Reviewer participation
```

### Step 3: Verification and Commit
```
1. Confirm Developer executes L0/L1 verification passed
2. Confirm ISSUES.md has been updated
3. Confirm STATUS.md has been updated
4. git commit
```

---

## Sub-agent Tasks

### Developer 🔧
1. Read the assigned issue
2. Read the relevant source code
3. Analyze the root cause (don't blindly trial-and-error)
4. Implement the fix
5. Execute `uv run python _verify_layer0.py`
6. Execute `uv run python _verify_layer1.py`
7. git commit after verification passes (English message)
8. Remove the corresponding issue from ISSUES.md

### QA Engineer 🧪
1. Execute L0 verification
2. Execute L1 verification
3. Report all failed items
4. Confirm the bug has been fixed

### Challenger 🔥
**In the development topic, the Challenger is only responsible for questioning "priorities":**
- Does this bug really need to be fixed now?
- Is the fix priority correct?
- Are there more important issues being overlooked?

---

## Status Update

PM must update in STATUS.md:

```markdown
## Verification Log
| Date | Gate 1 (Import) | Gate 2 (Render) | Gate 3 (Smoke) | Notes |
|------|-----------------|-----------------|----------------|-------|
| YYYY-MM-DD HH:MM | ✅ 52/52 (L0) | ✅ 18/18 (L1) | — | Fix ISSUE-XXX |
```

---

*Last updated: 2026-06-09*
