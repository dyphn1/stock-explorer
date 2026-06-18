# Stock Explorer — PM 流程圖

> 本文件包含所有 PM 工作流的 Mermaid 視覺化。
> AGENTS.md 引用本檔案作為視覺參考。

---

## 圖 1: PM 進入 Cron Session 後的決策流程

```mermaid
flowchart TD
    START([PM 被 cron 喚醒]) --> READ_STATE[Step 0: 讀取狀態<br/>STATUS.md + handoff.md<br/>current_problems.md + pending_review.md]

    READ_STATE --> CHECK_TODO{判斷當前<br/>最高優先任務}

    CHECK_TODO -->|P0: 重構 + UX Bug| TODO_REFACTOR[TODO: 重構/修復]
    CHECK_TODO -->|P1: 新功能| TODO_FEATURE[TODO: 開發新功能]
    CHECK_TODO -->|P2: 驗證/測試| TODO_VERIFY[TODO: 驗證]
    CHECK_TODO -->|P3: 研究/討論| TODO_RESEARCH[TODO: 研究競品]
    CHECK_TODO -->|無任務| SILENT([SILENT 結束])

    TODO_REFACTOR --> GATE1{ Gate Check 1<br/>設計完成?}
    TODO_FEATURE --> GATE1
    TODO_VERIFY --> GATE2{ Gate Check 2<br/>實作完成?}
    TODO_RESEARCH --> GATE3{Gate Check 3<br/>驗證通過?}

    GATE1 -->|NOT PASSED| BACK1[退回上一 TODO<br/>標明改善要求]
    BACK1 --> CHECK_TODO
    GATE1 -->|PASSED| NEXT1[前進下一個 TODO]
    NEXT1 --> GATE2

    GATE2 -->|NOT PASSED| BACK2[退回 TODO 2<br/>標明問題重點]
    BACK2 --> TODO_FEATURE
    GATE2 -->|PASSED| NEXT2[前進下一個 TODO]
    NEXT2 --> GATE3

    GATE3 -->|NOT PASSED| BACK3[退回 TODO 2]
    BACK3 --> TODO_FEATURE
    GATE3 -->|PASSED| TODO4[TODO 4: 發布<br/>PM 自己動手]

    TODO4 --> COMMIT[git commit + push<br/>更新狀態文件]
    COMMIT --> END([Session 結束])
```

---

## 圖 2: TODO 1 — 重構/修復（Refactor / Bug Fix）

```mermaid
flowchart TD
    START([TODO 1 開始]) --> READ[PM 讀取 current_problems.md<br/>確認問題範圍和檔案]

    READ --> DELEGATE1[delegate_task → Architect<br/>分析可行性 + 技術方案<br/>model: nemotron-3]
    READ --> DELEGATE2[delegate_task → Challenger<br/>3 回合挑戰計畫<br/>model: gpt-oss-120b]

    DELEGATE1 --> GATE1{<br/>Gate 1: 設計完成?}
    DELEGATE2 --> GATE1

    GATE1 -->|NOT PASSED<br/>設計不完整| BACK[退回重發<br/>指明不足處]
    BACK --> READ

    GATE1 -->|PASSED<br/>設計通過| TODO2[前進 TODO 2<br/>開始實作]

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
```

**參與角色：** Architect (`nemotron-3`) + Challenger (`gpt-oss-120b`)
**完成條件：** 技術分析/ADR 存在 + Challenger 3 回合通過

---

## 圖 3: TODO 2 — 開發新功能（New Feature / UI）

```mermaid
flowchart TD
    START([TODO 2 開始]) --> READ[PM 讀取設計產出<br/>HTML prototype + 技術分析]

    READ --> DELEGATE_UX[delegate_task → UX Designer<br/>Create HTML prototype<br/>model: gemma-4]
    READ --> DELEGATE_ARCH[delegate_task → Architect<br/>技術可行性分析<br/>model: nemotron-3]

    DELEGATE_UX --> GATE1{<br/>Gate 1: 設計完成?}
    DELEGATE_ARCH --> GATE1

    GATE1 -->|NOT PASSED| BACK1[退回重發]
    BACK1 --> READ

    GATE1 -->|PASSED| DELEGATE_SEC[delegate_task → Security Architect<br/>威脅建模 + 安全審查<br/>model: nemotron-3]

    DELEGATE_SEC --> GATE2{<br/>Gate 2: 安全通過?}

    GATE2 -->|NOT PASSED| BACK2[退回 Phase 1<br/>Architect 修正]
    BACK2 --> READ

    GATE2 -->|PASSED| DELEGATE_DEV[delegate_task → Developer<br/>實作 + L0/L1 驗證<br/>model: owl-alpha]

    DELEGATE_DEV --> GATE3{<br/>Gate 3: 實作完成?}

    GATE3 -->|NOT PASSED<br/>L0/L1 失敗| BACK3[退回 Developer<br/>標明測試失敗項]
    BACK3 --> DELEGATE_DEV

    GATE3 -->|PASSED| TODO3[前進 TODO 3<br/>開始驗證]

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
    style GATE2 fill:#f9e79f,stroke:#d4ac0d
    style GATE3 fill:#f9e79f,stroke:#d4ac0d
```

**參與角色：** UX Designer (`gemma-4`) + Architect (`nemotron-3`) + Security (`nemotron-3`) + Developer (`owl-alpha`)
**完成條件：** HTML prototype 存在 + Security pass + L0/L1 all pass + git commit

---

## 圖 4: TODO 3 — 驗證（Verify / Test）

```mermaid
flowchart TD
    START([TODO 3 開始]) --> READ[PM 確認實作完成<br/>git diff --stat + L0 pass]

    READ --> DELEGATE_QA[delegate_task → QA<br/>L0 + L1 + L2 測試<br/>model: gemma-4]
    READ --> DELEGATE_SEC[delegate_task → Security<br/>Code audit<br/>model: nemotron-3]
    READ --> DELEGATE_REVIEW[delegate_task → Design Reviewer<br/>視覺 vs prototype<br/>model: gemma-4]

    DELEGATE_QA --> GATE{<br/>Gate: 全部通過?}
    DELEGATE_SEC --> GATE
    DELEGATE_REVIEW --> GATE

    GATE -->|NOT PASSED<br/>P0 問題| BACK[退回 TODO 2<br/>標明修復重點]
    BACK --> START

    GATE -->|PASSED<br/>All pass| TODO4[前進 TODO 4<br/>發布]

    style GATE fill:#f9e79f,stroke:#d4ac0d
```

**參與角色：** QA (`gemma-4`) + Security (`nemotron-3`) + Design Reviewer (`gemma-4`)
**完成條件：** L0 + L1 + L2 all pass + 安全無 critical + 視覺無 P0 偏差

---

## 圖 5: TODO 4 — 發布（PM 自己動手）

```mermaid
flowchart TD
    START([TODO 4 開始]) --> PM1[更新 docs/state/handoff.md<br/>Session summary]
    PM1 --> PM2[更新 docs/state/current_problems.md<br/>標記已解決]
    PM2 --> PM3[更新 docs/state/pending_review.md<br/>清除已審核項目]
    PM3 --> PM4[更新 docs/overview/05-roadmap.md<br/>標記功能完成]
    PM4 --> PM5[git add -A<br/>git commit -m "type: summary"<br/>git push]
    PM5 --> END([✅ 任務完成])

    style PM5 fill:#d5f5e3,stroke:#27ae60
```

**只有 PM 自己動手，沒有 sub-agent。**

---

## 圖 6: 研究/討論（Research / Discuss）

```mermaid
flowchart TD
    START([研究/討論開始]) --> READ[PM 定義研究範圍<br/>競品分析 or 下一步方向]

    READ --> DELEGATE_QA[delegate_task → QA<br/>競品研究<br/>model: gemma-4]
    READ --> DELEGATE_ARCH[delegate_task → Architect<br/>可行性評估<br/>model: nemotron-3]
    READ --> DELEGATE_UX[delegate_task → UX Designer<br/>UX 建議<br/>model: gemma-4]

    DELEGATE_QA --> GATE1{<br/>Gate 1: 研究完成?}
    DELEGATE_ARCH --> GATE1
    DELEGATE_UX --> GATE1

    GATE1 -->|NOT PASSED| BACK[退回重發]
    BACK --> READ

    GATE1 -->|PASSED| SYNTHESIZE[PM 綜合結果<br/>→ 草案]

    SYNTHESIZE --> DELEGATE_CHAL[delegate_task → Challenger<br/>3 回合挑戰<br/>model: gpt-oss-120b]

    DELEGATE_CHAL --> GATE2{<br/>Gate 2: 挑戰通過?}

    GATE2 -->|NOT PASSED| REVISE[修正草案]
    REVISE --> SYNTHESIZE

    GATE2 -->|PASSED| DOC[PM 寫 ADR<br/>更新 roadmap<br/>建立 handoff]
    DOC --> COMMIT[git commit + push]
    COMMIT --> END([✅ 完成])

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
    style GATE2 fill:#f9e79f,stroke:#d4ac0d
```

---

## 圖 7: 優化（Optimization / 設計審查修復）

```mermaid
flowchart TD
    START([優化任務開始]) --> READ[PM 讀取 design review 報告<br/>列出待修復項目]

    READ --> CLASSIFY{問題分類}

    CLASSIFY -->|色彩/元件違規| DELEGATE_DEV[delegate_task → Developer<br/>修正為設計系統色彩<br/>model: owl-alpha]
    CLASSIFY -->|佈局/響應式| DELEGATE_UX[delegate_task → UX Designer<br/>更新 prototype<br/>model: gemma-4]
    CLASSIFY -->|交互/流程| DELEGATE_UX

    DELEGATE_DEV --> GATE{<br/>Gate: 修正完成?}
    DELEGATE_UX --> GATE

    GATE -->|NOT PASSED| BACK[退回重做]
    BACK --> READ

    GATE -->|PASSED| VERIFY[PM 跑 L0 驗證<br/>確認無 regression]
    VERIFY --> COMMIT[git commit + push]
    COMMIT --> END([✅ 完成])

    style GATE fill:#f9e79f,stroke:#d4ac0d
```

---

## 角色與 Model 對照表

| Role | Model | 主要參與 TODO |
|------|-------|-------------|
| **PM** | `openrouter/owl-alpha` | TODO 4（自己動手）+ 所有 Gate Check |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | TODO 1, 2, 6 |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | TODO 2, 3 |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | TODO 2, 6, 7 |
| **Developer** | `openrouter/owl-alpha` | TODO 1, 2, 7 |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | TODO 3 |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | TODO 3, 6 |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | TODO 1, 6 |
