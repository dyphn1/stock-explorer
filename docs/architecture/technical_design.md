# Stock Explorer - Technical Design Document

## Data Layer: FinMind API Research Results

### Free APIs Available (Verified)

| API Method | Data Content | Fields |
|------------|-------------|--------|
| taiwan_stock_info | Stock basic info | industry_category, stock_id, stock_name, type, date |
| taiwan_stock_daily | Daily closing price | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| taiwan_stock_month_revenue | Monthly revenue | date, stock_id, country, revenue, revenue_month, revenue_year |
| taiwan_stock_per_pbr | PER/PBR/dividend yield | date, stock_id, dividend_yield, PER, PBR |
| taiwan_stock_balance_sheet | Balance sheet | date, stock_id, type, value, origin_name |
| taiwan_stock_financial_statement | Income statement | date, stock_id, type, value, origin_name |
| taiwan_stock_cash_flows_statement | Cash flow statement | date, stock_id, type, value, origin_name |
| taiwan_stock_institutional_institutional_investors | Institutional investors buy/sell | date, stock_id, buy, name, sell |
| taiwan_stock_margin_purchase_short_sale | Margin trading | date, stock_id, MarginPurchaseBuy/Sell, ShortSaleBuy/Sell, etc. |
| taiwan_stock_dividend | Dividend policy | date, stock_id, year, CashEarningsDistribution, CashExDividendTradingDate, etc. |
| taiwan_stock_dividend_result | Ex-dividend result | date, stock_id, before_price, after_price, stock_and_cache_dividend |
| taiwan_stock_shareholding | Foreign shareholding | date, stock_id, ForeignInvestmentShares, ForeignInvestmentSharesRatio |
| taiwan_stock_news | News | date, stock_id, link, source, title |

### Paid Membership Required (⚠️ Not used in Phase 1)

| API Method | Data Content |
|------------|-------------|
| taiwan_stock_holding_shares_per | Shareholding distribution |
| taiwan_stock_industry_chain | Industry supply chain |
| taiwan_stock_market_value | Market cap |
| taiwan_stock_monthly | Monthly average price |
| taiwan_stock_weekly | Weekly average price |

### Industry Categories (57 total)
Major industries: Semiconductor (265), Electronics (542), Biotech/Medical (271), Computer & Peripherals (141), Electronic Components (252), Communications (111), Electrical Machinery (132), Construction (91), Finance/Insurance (70), Tourism (68), Chemical (59), etc.

## System Architecture

```
┌─────────────────────────────────────────────────┐
│                  Streamlit Frontend              │
│  ┌─────────┬─────────┬─────────┬─────────┐      │
│  │ Business│Operation│Financial│  Peer   │ ...  │
│  │  Card   │Checkup  │ Health  │ Compare │      │
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
│  │  (local JSON cache + TTL)          │         │
│  └────────────────┬───────────────────┘         │
└───────────────────┼─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              Data Layer                           │
│  ┌──────────────────────────────────┐            │
│  │     FinMind API Client           │            │
│  │  (wraps all FinMind data APIs)   │            │
│  └──────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
```

## Page Detailed Design

### Page 1: Business Card
**Goal:** User knows what this company does for money within 10 seconds.

**Components:**
1. Header: Company name + stock ticker + industry tag
2. One-line positioning (large font, centered)
3. Revenue source pie chart (Plotly, click to expand plain-language explanation)
4. Key metrics triple card (market cap, last 4-quarter revenue, gross margin) — each with real-life analogy
5. Recent activity card (latest major announcement/news, plain-language summary)
6. Navigation tabs (Operation Checkup / Financial Health / Peer Comparison / Group Structure)

**Data sources:**
- Company info: taiwan_stock_info
- Stock price: taiwan_stock_daily
- Monthly revenue: taiwan_stock_month_revenue
- PER/PBR: taiwan_stock_per_pbr
- Income statement: taiwan_stock_financial_statement
- News: taiwan_stock_news

### Page 2: Operation Checkup
**Goal:** Understand this company's business model.

**Components:**
1. Revenue trend chart (monthly revenue line, annotated YoY change)
2. Revenue breakdown analysis (if multiple business lines)
3. Customer concentration (top 5 clients ratio, if data available)
4. Capacity and utilization (if available)

### Page 3: Financial Health
**Goal:** Understand financial data through real-life analogies.

**Components:**
1. Income statement summary (Revenue → Gross Profit → Operating Profit → Net Income, funnel chart)
2. Balance sheet summary (asset structure, debt ratio)
3. Cash flow summary (operating/investing/financing activities)
4. Key ratios (ROE, gross margin, debt ratio) — each with plain-language explanation

### Page 4: Peer Comparison
**Goal:** How does it differ from the industry leader?

**Components:**
1. Benchmark selection (auto-select #1 by market cap in industry, or manual)
2. Side-by-side comparison table (revenue, gross margin, ROE, PER, etc.)
3. Difference analysis (explain reasons with real examples)
4. Radar chart (multi-dimensional comparison)

### Page 5: Group Structure
**Goal:** Understand relationships within the group.

**Components:**
1. Group relationship diagram (Plotly scatter or network chart)
2. Parent company info card
3. Subsidiary list (click to expand details)
4. Relationship description (business interactions, ownership percentage)

## Caching Strategy
- Daily closing price: daily update (after market close)
- Monthly revenue: monthly update (around the 10th of each month)
- Financial reports: quarterly update
- Company basic info: weekly update
- LLM-generated content: cached until data source updates

## TODO
- [ ] Create project directory structure
- [ ] Implement FinMind Client wrapper
- [ ] Implement caching mechanism
- [ ] Implement Page 1: Business Card
- [ ] Implement Page 2: Operation Checkup
- [ ] Implement Page 3: Financial Health
- [ ] Implement Page 4: Peer Comparison
- [ ] Implement Page 5: Group Structure
- [ ] Custom CSS (PPT style)
- [ ] LLM plain-language explanation integration
- [ ] Testing and verification

---
*Last updated: 2026-06-06*
