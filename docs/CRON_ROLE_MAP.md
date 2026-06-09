# Stock Explorer — Cron 角色職責圖

## Cron 主題輪替（每 3 個 cycle 一輪）

| Cycle | 主題 | 說明 |
|-------|------|------|
| 1 | 🔧 開發 | 修 bug、實作新功能 |
| 2 | 💡 討論 | 功能規劃、未來發展方向 |
| 3 | 🔍 檢討 | 缺失檢討、優化產品、競品研究 |

---

## 角色列表

| 角色 | 模型 | 職責 |
|------|------|------|
| **Cron** | — | 發起主題、叫起團隊 |
| **PM** | owl-alpha | 協調、彙整、分派工作 |
| **Architect** | nemotron-120b | 架構分析、技術方案 |
| **Developer** | owl-alpha | 實作、修復 |
| **Design Reviewer** | gemma-31b | 視覺/UX 審查 |
| **QA Engineer** | gemma-31b | 驗證、競品研究 |
| **Challenger** | gpt-oss-120b:free | 質疑、反證、確保目標一致 |

---

## 反證流程（MANDATORY）

**每個重要決定都必須經過至少 3 輪反證：**

```
Round 1: 團隊提出方案
    ↓
Challenger 質疑（為什麼？有其他方案？風險是什麼？）
    ↓
Round 2: 團隊回應質疑、修正方案
    ↓
Challenger 再次質疑（漏洞？矛盾？）
    ↓
Round 3: 團隊最終回應
    ↓
Challenger 確認：目標一致 → 通過
```

**目標：** 不是為了反對而反對，而是透過反證確保每個決定都經得起考驗。

---

## 各角色在每次 Cron 的職責

### 1. Cron（發起者）
- 讀取 `STATUS.md` 決定本次主題
- 叫起 Main agent（PM）
- 寫入 `STATUS.md` 記錄本次主題

### 2. Main Agent / PM（協調者）
- 讀取所有狀態檔案
- 發起團隊討論（standup）
- 彙整各角色意見
- **至少 3 輪反證**後才能確認決定
- 寫回狀態檔案

### 3. System Architect（架構師）
- **開發主題**：分析技術可行性、提出架構方案
- **討論主題**：評估新功能的技术影響
- **檢討主題**：審視架構債務、提出重構建議

### 4. Developer（開發者）
- **開發主題**：實作功能、修 bug
- **討論主題**：評估實作成本、給出時間估算
- **檢討主題**：重構程式碼、優化效能

### 5. Design Reviewer（設計審查）
- **開發主題**：審查 UI/UX 實作
- **討論主題**：提供設計方向建議
- **檢討主題**：比對競品設計、提出改進

### 6. QA Engineer（品質保證）
- **開發主題**：執行驗證（L0/L1/L2）
- **討論主題**：評估測試策略
- **檢討主題**：執行競品功能比對、寫入 `docs/COMPETITOR_RESEARCH.md`

### 7. Challenger（質疑者）⭐ NEW
- **所有主題**：聆聽團隊討論，質疑每個決定
- 要求至少 3 輪反證才能確認一個決定
- 確保團隊目標一致
- 質疑重點：
  - 這個方案真的解決了問題嗎？
  - 有沒有更簡單/更好的方案？
  - 風險是什麼？有沒有遺漏？
  - 各角色的意見有沒有矛盾？

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
| `docs/CHALLENGE_LOG.md` | 質疑者反證記錄 | 每次有反證時 |

### 交接流程

```
Cron 發起主題
    ↓
PM 讀取所有狀態檔案
    ↓
PM 發起團隊討論（delegate_task 給 Architect、Developer、Designer、QA）
    ↓
各角色回傳意見/結果
    ↓
PM 彙整 → 提出方案
    ↓
Challenger 質疑（Round 1）
    ↓
PM 協調團隊回應 → 修正方案
    ↓
Challenger 質疑（Round 2）
    ↓
PM 協調團隊回應 → 最終方案
    ↓
Challenger 質疑（Round 3）
    ↓
Challenger 確認：目標一致
    ↓
PM 分派工作給 Developer
    ↓
Developer 實作 → 驗證 → commit
    ↓
PM 更新所有狀態檔案（含 CHALLENGE_LOG.md）
    ↓
結束
```

---

## 基本資訊

**可用模型（all via `provider: openrouter`）：**

| 模型 | 角色 |
|------|------|
| `openrouter/owl-alpha` | PM、Developer |
| `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Architect |
| `openrouter/google/gemma-4-31b-it:free` | Design Reviewer、QA Engineer |
| `openrouter/xai/gpt-oss-120b:free` | **Challenger（質疑者）** |

---

*最後更新：2026-06-09*
