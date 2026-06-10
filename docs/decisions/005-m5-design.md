# Stock Explorer M5 Design Document: Adaptive Updates

## Design Goals

Based on the product vision document:
- Content updates as the company changes.
- Major events trigger content regeneration, such as acquisitions, mergers, or major losses.
- Different company types use different analysis frameworks.
- Content updates within 24 hours after major events.

## 核心概念

### 1. 事件偵測 (Event Detection)
從 FinMind 新聞 API 偵測重大事件，分類為：
- **💰 營收異動**：月營收 YoY 變化超過 ±30%
- **🏷️ 法人突變**：三大法人買賣超突然大幅增加/減少
- **📰 重大新聞**：新聞標題包含關鍵字（收購、合併、虧損、法說、股利政策變更等）
- **📉 股價異常**：單日漲跌幅超過 ±7%
- **💵 股利變更**：現金股利與前期相比變化超過 ±20%

### 2. 事件嚴重程度分級
- 🔴 **重大 (high)**：收購、合併、重大虧損、股價異常 >±7%
- 🟡 **注意 (medium)**：營收異動 ±30~50%、法人突變、股利變更
- 🟢 **參考 (low)**：一般新聞、小幅營收變化

### 3. 自適應框架
根據公司類型自動切換分析框架：
- **單一公司**（default）：標準四大深度分析
- **集團型**（group）：側重集團架構 + 子公司關聯
- ETF：已有 etf_detail 模組
- 根據產業特性調整比喻和比較基準

### 4. 新鮮度指標 (Freshness Indicator)
在每頁顯示資料最後更新時間，以及是否有新事件需要關注。

## 架構設計

```
src/
├── services/
│   └── adaptive_engine.py      # 核心：事件偵測 + 自適應邏輯
├── pages/
│   └── event_dashboard.py       # 事件儀表板（新頁面）
config/
└── events.yaml                  # 事件記錄
```

### adaptive_engine.py 功能
1. `detect_events(stock_id)` → 偵測該股票近期是否有重大事件
2. `get_event_summary(events)` → 事件白話摘要
3. `detect_company_type(data)` → 判斷公司類型（集團/單一/ETF）
4. `get_adaptive_framework(company_type)` → 推薦分析框架
5. `check_data_freshness(stock_id)` → 資料新鮮度檢查

### event_dashboard.py 功能
1. 近期重大事件列表（依時間排序）
2. 事件影響程度標籤
3. 事件白話摘要
4.  clicking event 導向對應公司股票頁

## 實作順序
1. ✅ 設計文件（此文件）
2. `adaptive_engine.py`：事件偵測核心
3. `event_dashboard.py`：事件儀表板頁面
4. 整合至 router.py（新增「事件儀表板」頁面）
5. 整合至各頁面（顯示新鮮度指標 + 事件提示）
6. 測試與驗證

## 資料結構：events.yaml
```yaml
events:
  - stock_id: "2330"
    date: "2026-06-07"
    type: "revenue_surge"
    severity: "medium"
    title: "台積電 5 月營收年增 45%"
    summary: "營收大幅增加，主要因為 AI 需求旺盛"
    detected_at: "2026-06-07T15:00:00"
  - stock_id: "2454"
    date: "2026-06-05"
    type: "news_major"
    severity: "high"
    title: "聯發科宣布收購 AI 新創公司"
    summary: "擴大 AI 布局，預計 Q3 完成交易"
    detected_at: "2026-06-05T10:00:00"
```

---
*建立日期：2026-06-07*
