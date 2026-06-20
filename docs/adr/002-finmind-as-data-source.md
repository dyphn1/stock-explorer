# ADR-002: Choose FinMind as the Primary Data Source

## Status
Accepted

## Date
2026-06-06

## Background

Stock Explorer needs financial data, price data, news, etc. for Taiwan stocks. A reliable data source must be chosen.

## Decision

Choose **FinMind API** as the primary data source, using 13 APIs from the free tier.

## Rationale

1. **Taiwan market focus**: Provides 50+ Taiwan stock datasets
2. **Free tier available**: 13 free APIs cover core needs
3. **Daily updates**: Data update frequency meets requirements
4. **Python SDK**: Official Python SDK provided

## Verified Free APIs

| API | Data Content |
|-----|--------------|
| `taiwan_stock_info` | Stock basic information |
| `taiwan_stock_daily` | Daily closing price |
| `taiwan_stock_month_revenue` | Monthly revenue |
| `taiwan_stock_per_pbr` | PER/PBR/dividend yield |
| `taiwan_stock_balance_sheet` | Balance sheet |
| `taiwan_stock_financial_statement` | Income statement |
| `taiwan_stock_cash_flows_statement` | Cash flow statement |
| `taiwan_stock_institutional_investors` | Institutional investor trading |
| `taiwan_stock_margin_purchase_short_sale` | Margin trading |
| `taiwan_stock_dividend` | Dividend policy |
| `taiwan_stock_dividend_result` | Ex-dividend result |
| `taiwan_stock_shareholding` | Foreign shareholding |
| `taiwan_stock_news` | News |

## Alternatives

| Option | Reason for Rejection |
|--------|---------------------|
| Yahoo Finance API | Incomplete Taiwan stock data |
| Direct TWSE scraping | High maintenance cost, may violate terms of service |
| Paid data sources (e.g., CMoney) | Too costly for MVP stage |

## Consequences

- ✅ Zero cost for core data
- ⚠️ Some data (e.g., shareholding tiers, industry supply chain) requires paid tier
- ⚠️ API has rate limits, caching mechanism needed
