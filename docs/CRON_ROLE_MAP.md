# Stock Explorer — Cron 角色職責圖

## Cron 主題輪替（每 3 個 cycle 一輪）

| Cycle | 主題 | 說明 |
|-------|------|------|
| 1 | 🔧 開發 | 修 bug、實作新功能 |
| 2 | 💡 討論 | 功能規劃、未來發展方向 |
| 3 | 🔍 檢討 | 缺失檢討、優化產品、競品研究 |

---

## 各角色在每次 Cron 的職責

### 1. Cron（發起者）
- 讀取 `STATUS.md` 決定本次主題
- 叫起 Main agent（PM）
- 寫入 `STATUS.md` 記錄本次主題

### 2. Main Agent / PM（協調者）
- 讀取所有狀態檔案（STATUS.md、ISSUES.md、PENDING_REVIEW.md、CURRENT_PROBLEMS.md）
- 發起團隊討論（standup）
- 彙整各角色意見
- 決定分工
- 寫回狀態檔案

### 3. System Architect（架構師）
- **開發主題**：分析技術可行性、提出架構方案
- **討論主題**：評估新功能的技术影響
- **檢討主題**：審視架構債務、提出重構建議

### 4. Developer（開發者）
- **開發主題**：實作功能、修 bug
- **討論主題**：評估實作成本
- **檢討主題**：重構程式碼、優化效能

### 5. Design Reviewer（設計審查）
- **開發主題**：審查 UI/UX 實作
- **討論主題**：提供設計方向建議
- **檢討主題**：比對競品設計、提出改進

### 6. QA Engineer（品質保證）
- **開發主題**：執行驗證（L0/L1/L2）
- **討論主題**：評估測試策略
- **檢討主題**：執行競品功能比對

---

## 狀態交接機制

### 狀態檔案（全部留在專案內）

| 檔案 | 用途 | 更新時機 |
|------|------|----------|
| `STATUS.md` | 專案整體狀態、里程碑、上次 cron 結果 | 每次 cron 結束 |
| `docs/ISSUES.md` | 已知 bug、待修問題 | 發現新問題時 |
| `docs/PENDING_REVIEW.md` | 等待 Daniel 決策的事項 | 需要人工判斷時 |
| `docs/CURRENT_PROBLEMS.md` | 目前已知的所有問題（含非 bug） | 檢討主題時 |
| `docs/COMPETITOR_RESEARCH.md` | 競品研究報告 | 檢討主題時 |

### 交接流程

```
Cron 發起主題
    ↓
PM 讀取所有狀態檔案
    ↓
PM 發起團隊討論（delegate_task 給各角色）
    ↓
各角色回傳意見/結果
    ↓
PM 彙整 → 決定行動方案
    ↓
PM 分派工作給 Developer
    ↓
Developer 實作 → 驗證 → commit
    ↓
PM 更新所有狀態檔案
    ↓
結束
```

---

## 競品研究機制

**頻率**：每 3 次 cron（檢討主題時）

**流程**：
1. QA Engineer 去網路搜尋競品（Yahoo Finance、TradingView、Finviz 等）
2. 比對我們的功能差距
3. 寫入 `docs/COMPETITOR_RESEARCH.md`
4. 新功能建議寫入 `docs/ISSUES.md`（標記為 `來源: 競品研究`）

---

*最後更新：2026-06-09*
