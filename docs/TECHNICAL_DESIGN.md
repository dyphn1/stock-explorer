# 股識 - 技術設計文件

## 資料層：FinMind API 研究結果

### 免費可用 API（已驗證）
| API 方法 | 資料內容 | 欄位 |
|----------|----------|------|
| taiwan_stock_info | 股票基本資訊 | industry_category, stock_id, stock_name, type, date |
| taiwan_stock_daily | 日收盤價 | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| taiwan_stock_month_revenue | 月營收 | date, stock_id, country, revenue, revenue_month, revenue_year |
| taiwan_stock_per_pbr | PER/PBR/殖利率 | date, stock_id, dividend_yield, PER, PBR |
| taiwan_stock_balance_sheet | 資產負債表 | date, stock_id, type, value, origin_name |
| taiwan_stock_financial_statement | 損益表 | date, stock_id, type, value, origin_name |
| taiwan_stock_cash_flows_statement | 現金流量表 | date, stock_id, type, value, origin_name |
| taiwan_stock_institutional_investors | 三大法人買賣超 | date, stock_id, buy, name, sell |
| taiwan_stock_margin_purchase_short_sale | 融資融券 | date, stock_id, MarginPurchaseBuy/Sell, ShortSaleBuy/Sell 等 |
| taiwan_stock_dividend | 股利政策 | date, stock_id, year, CashEarningsDistribution, CashExDividendTradingDate 等 |
| taiwan_stock_dividend_result | 除權息結果 | date, stock_id, before_price, after_price, stock_and_cache_dividend |
| taiwan_stock_shareholding | 外資持股 | date, stock_id, ForeignInvestmentShares, ForeignInvestmentSharesRatio |
| taiwan_stock_news | 新聞 | date, stock_id, link, source, title |

### 需要付費會員（⚠️ 第一階段不使用）
| API 方法 | 資料內容 |
|----------|----------|
| taiwan_stock_holding_shares_per | 股權分散表 |
| taiwan_stock_industry_chain | 產業供應鏈 |
| taiwan_stock_market_value | 市值 |
| taiwan_stock_monthly | 月均價 |
| taiwan_stock_weekly | 週均價 |

### 產業分類（共 57 類）
主要產業：半導體業(265)、電子工業(542)、生技醫療業(271)、電腦及週邊設備業(141)、
電子零組件業(252)、通信網路業(111)、電機機械(132)、建材營造(91)、
金融保險(70)、觀光餐旅(68)、化學工業(59) 等

## 系統架構

```
┌─────────────────────────────────────────────────┐
│                  Streamlit Frontend              │
│  ┌─────────┬─────────┬─────────┬─────────┐      │
│  │ 公司名片 │ 營運健檢 │ 財務體質 │ 同業比較 │ ... │
│  └────┬────┴────┬────┴────┬────┴────┬────┘      │
│       │         │         │         │            │
│  ┌────▼─────────▼─────────▼─────────▼────┐      │
│  │           Page Router                  │      │
│  └────────────────┬───────────────────────┘      │
└───────────────────┼─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              Service Layer                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Analyzer │ │ LLM      │ │ Chart    │        │
│  │ Engine   │ │ Explainer│ │ Generator│        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘        │
│       │            │            │               │
│  ┌────▼────────────▼────────────▼─────┐         │
│  │         Cache Manager              │         │
│  │  (本地 JSON 快取 + TTL 機制)       │         │
│  └────────────────┬───────────────────┘         │
└───────────────────┼─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              Data Layer                           │
│  ┌──────────────────────────────────┐            │
│  │     FinMind API Client           │            │
│  │  (封裝所有 FinMind 資料接口)     │            │
│  └──────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
```

## 頁面詳細設計

### 第一頁：公司名片
**目標**：使用者在 10 秒內知道這家公司靠什麼賺錢

**元件**：
1. Header：公司名稱 + 股號 + 產業標籤
2. 一句話定位（大字體，置中）
3. 營收來源圓餅圖（Plotly，點擊展開白話說明）
4. 關鍵數字三連卡（市值、近四季營收、毛利率）— 每個數字附生活化比喻
5. 近期動態卡片（最近一則重大公告/新聞，白話摘要）
6. 導航標籤（營運健檢 / 財務體質 / 同業比較 / 集團架構）

**資料來源**：
- 公司資訊：taiwan_stock_info
- 股價：taiwan_stock_daily
- 月營收：taiwan_stock_month_revenue
- PER/PBR：taiwan_stock_per_pbr
- 損益表：taiwan_stock_financial_statement
- 新聞：taiwan_stock_news

### 第二頁：營運健檢
**目標**：理解這家公司的商業模式

**元件**：
1. 營收趨勢圖（月營收折線圖，標註 YoY 變化）
2. 營收組成分析（如果有多個業務線）
3. 客戶集中度說明（前五大客戶佔比，如果有資料）
4. 產能與利用率（如果可用）

### 第三頁：財務體質
**目標**：用生活化比喻理解財務數據

**元件**：
1. 損益表摘要（營收 → 毛利 → 營業利益 → 淨利，用漏斗圖）
2. 資產負債表摘要（資產結構、負債比例）
3. 現金流量摘要（經營/投資/籌資活動）
4. 關鍵比率（ROE、毛利率、負債比）— 每個附白話解釋

### 第四頁：同業比較
**目標**：跟產業第一名差在哪

**元件**：
1. 標竿選擇（自動選產業市值第一，或手動選）
2. 並排比較表（營收、毛利率、ROE、PER 等）
3. 差異分析（用實際案例解釋差異原因）
4. 雷達圖（多維度比較）

### 第五頁：集團架構
**目標**：認識集團內部的關係

**元件**：
1. 集團關係圖（Plotly 散點圖或網絡圖）
2. 母公司資訊卡
3. 子公司列表（點擊展開詳情）
4. 關係說明（業務往來、持股比例）

## 快取策略
- 日收盤價：每日更新（收盤後）
- 月營收：每月更新（每月 10 日左右）
- 財報：每季更新
- 公司基本資訊：每週更新
- LLM 生成內容：快取直到資料來源更新

## 待辦事項
- [ ] 建立專案目錄結構
- [ ] 實作 FinMind Client 封裝
- [ ] 實作快取機制
- [ ] 實作第一頁：公司名片
- [ ] 實作第二頁：營運健檢
- [ ] 實作第三頁：財務體質
- [ ] 實作第四頁：同業比較
- [ ] 實作第五頁：集團架構
- [ ] 自定義 CSS（PPT 風格）
- [ ] LLM 白話解釋整合
- [ ] 測試與驗證

---
*最後更新：2026-06-06*
