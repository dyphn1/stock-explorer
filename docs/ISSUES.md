# Stock Explorer — 問題與功能追蹤

> 所有需要追蹤的 bug、功能請求、設計決策都記錄在此。
> 每個項目標註來源和優先級。

---

## 格式說明

```
### [編號] 簡短標題
- **來源：** 競品研究 / Bug Report / Design Review / PM 決策
- **優先級：** P0 / P1 / P2
- **狀態：** 📋 待辦 / 🔄 進行中 / ✅ 完成 / ❌ 取消
- **說明：** 詳細描述
- **相關檔案：** 影響的程式碼檔案
```

---

## 🔴 P0 — 必須修復/實作

---

### [ISSUE-C01] 除權息行事曆
- **來源：** 競品研究
- **優先級：** P0
- **狀態：** 📋 待辦
- **說明：**
  - GoodInfo、財報狗都有完整的除權息資訊
  - 新手最常問的問題之一：「台積電什麼時候配息、配多少？」
  - 目前 Stock Explorer 完全無法回答這個問題
  - 建議在名片頁新增「配息資訊」區塊
- **建議實作：**
  - 近 5 年除權息日程（除息日、除權日）
  - 歷年股利（現金股利、股票股利）
  - 白話說明（如：「過去 5 年，台積電每季配息約 2.75 元」）
  - 預估殖利率（以目前股價計算）
- **資料可行性：** FinMind 有 `TaiwanStockDividend` API
- **相關檔案：** `src/pages/business_card.py`
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 A

---

### [ISSUE-C02] 推播通知系統
- **來源：** 競品研究
- **優先級：** P0
- **狀態：** 📋 待辦
- **說明：**
  - 財報狗有 Line Notify；CMoney 有 App Push
  - 事件偵測引擎已經有資料，但無法主動通知用戶
  - 第一階段：email 通知（成本低）
  - 第二階段：Line Notify（需要 Bot 帳號）
- **建議實作：**
  - 營收異動 ±30%
  - 股價異動 ±7%
  - 使用者自訂通知條件
- **技術：** Background worker + SMTP（第一階段）
- **相關檔案：** `src/services/adaptive_engine.py`、新增 `src/services/notifier.py`
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 B

---

### [ISSUE-C03] 多 Watchlist 清單
- **來源：** 競品研究
- **優先級：** P0
- **狀態：** 📋 待辦
- **說明：**
  - Yahoo Finance、財報狗都支援多個 watchlist
  - 目前只有一個「我的關注」清單，缺乏分類管理能力
  - 使用者需要分別追蹤「存股標的」「觀察名單」「高殖利率」等
- **建議實作：**
  - watchlist.yaml 重構为 `lists` 結構
  - watchlist_page.py 改為多標籤分頁
  - 名片页加入「加入哪個清單」選擇器
- **相關檔案：** `config/watchlist.yaml`、`src/services/watchlist.py`、`src/pages/watchlist_page.py`
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 C

---

## 🟡 P1 — 重要但非關鍵

---

### [ISSUE-C04] 市場溫度計
- **來源：** 競品研究
- **優先級：** P1
- **狀態：** 📋 待辦
- **說明：**
  - 玩股網有「股市溫度計」；CMoney 有市場情緒指標
  - 新手想知道「現在市場是熱還是冷？」
  - 建議在主頁或事件儀表板加入市場溫度指示器
- **建議實作：**
  - 三大法人買賣超（5 日均值）
  - 大盤成交量（熱 vs 冷）
  - 漲停/跌停家數比
  - 呈現：體感溫度（🔥熱/😊正常/🥶冷）+ 白話說明
- **資料可行性：** FinMind 有 `TaiwanStockInstitutionalInvestorsBuySell`
- **相關檔案：** `src/pages/event_dashboard.py`、新增 `src/services/market_thermal.py`
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 D

---

### [ISSUE-C05] Portfolio 損益管理
- **來源：** 競品研究
- **優先級：** P1
- **狀態：** 📋 待辦
- **說明：**
  - CMoney 有完整的 Portfolio 管理功能
  - 目前 Watchlist 只有價格提醒，沒有持倉損益管理
  - Watchlist 進化为 Portfolio：加入成本價、持有數量
- **建議實作：**
  - 每股成本價、持有數量
  - 未實現損益（即時）
  - 已實現損益（歷史交易）
  - 組合總報酬率
- **相關檔案：** `config/watchlist.yaml`、`src/services/watchlist.py`、`src/pages/watchlist_page.py`
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 E

---

### [ISSUE-C06] 個股分析 PPT 自動生成
- **來源：** 競品研究
- **優先級：** P1
- **狀態：** 📋 待辦
- **說明：**
  - 玩股網有一鍵生成分析簡報功能
  - Stock Explorer 已有 PPT 風格 CSS，可直接用 python-pptx 生成真正的 PPT
  - 差異化：Stock Explorer 的 PPT 風格比玩股網更精美、更有教育性
- **建議實作：**
  - 每頁加入「下載 PPT」按鈕
  - 包含：公司名片、營運健檢重點、財務體質摘要、同業比較雷達圖
  - 使用 python-pptx + 各頁面爬取資料
- **技術：** `python-pptx` 庫
- **相關檔案：** 所有頁面模組
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 F

---

### [ISSUE-C07] 用戶自訂事件門檻
- **來源：** 競品研究
- **優先級：** P1
- **狀態：** 📋 待辦
- **說明：**
  - 延伸自 M5 事件偵測引擎
  - 目前使用固定閾值（營收±30%、股價±7%）
  - 允許用戶自訂敏感度和事件類型
- **建議實作：**
  - 使用者調整敏感度
  - 新增事件類型（法人買賣超連續 N 天、營收連 N 月衰退）
  - 新增加定頁面
- **相關檔案：** `src/services/adaptive_engine.py`、新增設定頁面
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 G

---

## 🟢 P2 — 加分功能/未來考慮

---

### [ISSUE-C08] 影音教學
- **來源：** 競品研究
- **優先級：** P2
- **狀態：** 📋 待辦
- **說明：**
  - CMoney 有大量投資教學影片
  - 每個指標下方可以嵌入 30 秒白話解釋影片
  - 製作成本高，建議 M5 後人工製作或嵌入現有 YouTube 資源
- **相關檔案：** 所有頁面模組
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 H

---

### [ISSUE-C09] 美股支援
- **來源：** 競品研究
- **優先級：** P2
- **狀態：** 📋 待辦
- **說明：**
  - 財報狗支援美股 500+ 公司
  - FinMind 已有美股資料
  - 目標：已熟悉台股分析架構、想延伸到美股的使用者
  - **需 Daniel 確認是否要支援美股**
- **相關檔案：** 所有頁面模組
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 I

---

### [ISSUE-C10] 全球市場地圖
- **來源：** 競品研究
- **優先級：** P2
- **狀態：** 📋 待辦
- **說明：**
  - 玩股網有全球股市地圖
  - Stock Explorer 版本可偏「基本面理解」而非「交易熱度」
  - 呈現：🟢上涨 🔴下跌 ↔️持平 + 白話說明各市場狀態
- **相關檔案：** 新増頁面
- **參考資料：** `docs/COMPETITOR_RESEARCH.md` — 靈感 J

---

## 📊 統計

| 狀態 | 數量 |
|------|------|
| 📋 待辦 | 10 |
| 🔄 進行中 | 0 |
| ✅ 完成 | 0 |
| ❌ 取消 | 0 |

| 優先級 | 數量 |
|---------|------|
| P0 | 3 |
| P1 | 4 |
| P2 | 3 |

---

*最後更新：2026-06-09（競品研究輪次）*
*新功能來源：docs/COMPETITOR_RESEARCH.md 競品研究報告*
