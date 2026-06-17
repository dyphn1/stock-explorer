# ADR-002: 選擇 FinMind 作為主要數據來源

## 狀態
已接受

## 日期
2026-06-06

## 背景

Stock Explorer 需要台灣股票的財務數據、價格數據、新聞等。需要選擇一個可靠的數據來源。

## 決策

選擇 **FinMind API** 作為主要數據來源，使用免費 tier 的 13 個 API。

## 理由

1. **台灣市場專注**：提供 50+ 台灣股票數據集
2. **免費 tier 可用**：13 個免費 API 涵蓋核心需求
3. **每日更新**：數據更新頻率符合需求
4. **Python SDK**：官方提供 Python SDK

## 已驗證的免費 API

| API | 數據內容 |
|-----|----------|
| `taiwan_stock_info` | 股票基本資訊 |
| `taiwan_stock_daily` | 日收盤價 |
| `taiwan_stock_month_revenue` | 月營收 |
| `taiwan_stock_per_pbr` | PER/PBR/殖利率 |
| `taiwan_stock_balance_sheet` | 資產負債表 |
| `taiwan_stock_financial_statement` | 損益表 |
| `taiwan_stock_cash_flows_statement` | 現金流量表 |
| `taiwan_stock_institutional_investors` | 三大法人買賣超 |
| `taiwan_stock_margin_purchase_short_sale` | 融資融券 |
| `taiwan_stock_dividend` | 股利政策 |
| `taiwan_stock_dividend_result` | 除權息結果 |
| `taiwan_stock_shareholding` | 外資持股 |
| `taiwan_stock_news` | 新聞 |

## 替代方案

| 方案 | 不選原因 |
|------|----------|
| Yahoo Finance API | 台灣股票數據不完整 |
| 證交所直接爬蟲 | 維護成本高、可能違反使用條款 |
| 付費數據源（如 CMoney） | MVP 階段成本過高 |

## 後果

- ✅ 零成本取得核心數據
- ⚠️ 部分數據（如持股分級、產業供應鏈）需要付費
- ⚠️ API 有速率限制，需要快取機制
