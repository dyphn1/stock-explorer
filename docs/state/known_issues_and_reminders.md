# Known Issues & Reminders — Stock Explorer (股識)

> **上次更新**: 2026-06-19
> **維護者**: PM Agent
> **適用對象**: 所有角色（PM / Developer / Architect / QA / 所有 sub-agents）

---

## 🔴 Model 選擇規則（2026-06-19 教訓）

**絕對不要用 `openrouter/owl-alpha` 做需要大量 API call 的任務。**

| 角色 | 模型 | 原因 |
|------|------|------|
| **PM** | `openrouter/owl-alpha` | 只做流程控制，API call 量少 |
| **Developer** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Nvidia free tier 速度快 3-5x，適合大量檔案操作 |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | 同上 |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | 測試驗證，速度優先 |

**教訓**：owl-alpha 平均每次 API call ~30s，nemotron 平均 ~5-10s。i18n 遷移一輪要 15-20 次 call，用 owl-alpha 會超過 600s timeout。

---

## 🔴 Cron 環境限制（所有 cron-run agents 必讀）

| 限制 | 說明 | 解法 |
|------|------|------|
| `memory` 不可用 | cron 環境沒有 memory 工具 | 需要記憶的資訊寫入 `docs/state/handoff.md` |
| `execute_code` 被拒絕 | background review 會擋掉 | 用 `terminal` 跑命令，或交給 sub-agent |
| `skill_manage(write_file)` 容易失敗 | 參數錯誤會導致無限循環 | PM 不用 skill_manage；sub-agent 如需用，確保 file_content 參數正確 |
| `read_file` 預設路徑不是專案目錄 | 會讀到 `~/.hermes/hermes-agent/` 而非專案 | **永遠用絕對路徑**：`/Users/daniel.chang/Desktop/GitHub/stock-explorer/...` |
| terminal 預設目錄不是專案 | `grep`、`ls` 會查錯目錄 | 每個命令前加 `cd /Users/daniel.chang/Desktop/GitHub/stock-explorer &&` |
| sub-agent 600s timeout | 檔案太多或 API 太慢會超時 | 每批最多 2 個檔案；timeout 就縮小範圍重派 |

---

## 🦉 PM 角色教訓（2026-06-19 迭代總結）

### 絕對禁止
1. **PM 不寫 code、不修改 src/ 檔案**——只派 `delegate_task` 給 Developer
2. **不用 `execute_code`**——會被 background review 擋掉
3. **不用 `terminal` 跑 Python script 分析檔案**——太慢且容易語法錯誤，用 `read_file` 直接讀
4. **不用 `skill_manage`**——參數問題會導致無限循環
5. **不在 terminal 反覆摸索**——讀 3-4 個狀態檔案後立刻派發 sub-agent

### 最佳實踐
- **讀完 handoff.md + current_problems.md 後立刻派發**，不要先 scan 整個專案
- **每批 delegate_task 只給 1-2 個檔案**，避免 600s timeout
- **sub-agent timeout → 縮小範圍重派**，不是自己接手
- 用 `git diff --stat` _gate check_ 產出物，不要只看 sub-agent 的回報文字

---

## 💻 Developer 角色教訓

### i18n 遷移（TD-02 Phase 2）
- **Locale key 命名規則**：`頁面_區塊_功能_描述`，例如 `etf_browser_filter_label`
- **不要 migrate 的字串**（見 `docs/adr/` 中的 TD-02 Phase 2 文件）：
  - Docstrings、comments（英文保留）
  - Stock IDs、ticker symbols（例如 `2330`、`0050`）
  - 專有名詞（例如 `ETF`、`ROE`、`PER`）
  - 已是英文的 UI labels
- **測試策略**：遷移完後跑 `python3 -m pytest tests/ -x -q`，確保沒有 f-string 語法錯誤

### 常見陷阱
- **f-string 跳脫**：`"{{"` 和 `"}}"` 在 f-string 中要小心，之前的 `_financial.py` 就是因此有 SyntaxError
- **locale key 拼錯**：拼錯的 key 會導致 `KeyError`，測試應涵蓋

---

## 🏗️ Architect 角色提醒

### 分層架構（不可違反）
```
Data → Service → Router → Presentation
```
- **禁止反向依賴**：Presentation 不能 import Service 層的內部函式
- **Plugin Chassis**：所有頁面已遷移到 `PluginRegistry`（TD-01 完成），新增頁面必須遵循

### i18n 架構
- 翻譯檔位置：`locales/en.yaml`、`locales/zh-TW.yaml`
- 所有 UI 字串用 `t('key')` 呼叫
- 新增 key 時同時更新兩個 locale 檔案

---

## 🔒 Security 角色提醒
- **LLM 安全**：只翻譯不推導——AI 解釋功能不能給投資建議
- **Hardcoded secrets**：不允許在程式碼中寫死 API key
- **輸入驗證**：所有使用者輸入（搜尋框、表單）必須驗證
- **File lock**：watchlist.yaml 並發寫入需要 filelock（見 UX-14）

---

## 🎨 Design Reviewer 提醒
- 設計系統色：不使用 hardcoded hex（如 `#F39C12`），統一用設計系統變數
- 元件一致性：優先使用 `_白话_card()`，不是 `st.metric()` 或 raw HTML
- 所有 UI 變更必須有 HTML prototype → Daniel 審核 → 實作 → Design Reviewer 驗證

---

## 🧪 QA 角色提醒
- **L0**：commit 前通過（`pytest tests/ -x -q`）
- **L1**：handoff 前通過
- **L2**：release 前通過
- **已知測試問題**：`test_notification_center_plugin_import` 是既有失敗，與 i18n 無關

---

## 📁 重要檔案路徑速查

| 檔案 | 絕對路徑 |
|------|----------|
| STATUS.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/STATUS.md` |
| AGENTS.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/AGENTS.md` |
| handoff.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/state/handoff.md` |
| current_problems.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/state/current_problems.md` |
| pending_review.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/state/pending_review.md` |
| known_issues_and_reminders.md | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/docs/state/known_issues_and_reminders.md` |
| en.yaml | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/en.yaml` |
| zh-TW.yaml | `/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/zh-TW.yaml` |

---

## 📊 當前優先權（2026-06-19）

**1（最高）> 3 > 2**
1. 重構 + UX Bug
3. 新功能
2. Bug 修復

---

## 🔄 Cron 設定備忘

| 設定 | 值 |
|------|-----|
| job_id | `741305404bf1` |
| schedule | every 30m |
| deliver | `discord:1490613981725855844` |
| workdir | `/Users/daniel.chang/Desktop/GitHub/stock-explorer` |
| model | `openrouter/owl-alpha` |
