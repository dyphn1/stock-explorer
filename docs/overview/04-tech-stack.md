# Technology Stack — Stock Explorer

> **Principle**: Choose the simplest, most mature technology, prioritizing development speed and maintainability.

---

## 1. Technology Stack Overview

| Layer | Technology | Version | Description |
|-------|------------|---------|-------------|
| **Language** | Python | 3.11+ | Primary development language |
| **Frontend Framework** | Streamlit | ≥1.58.0 | Rapid iteration, suitable for MVP |
| **Data API** | FinMind | ≥1.9.11 | Taiwan stock data, 50+ datasets |
| **Data Processing** | pandas | ≥3.0.3 | Data cleaning, feature engineering |
| **Charts** | Plotly | ≥6.8.0 | Interactive charts |
| **Configuration** | PyYAML | ≥6.0.3 | YAML config files |
| **HTTP** | requests | ≥2.34.2 | API requests |
| **Cache** | filelock | ≥3.29.1 | Local file cache lock |
| **Testing** | pytest | — | Unit and integration tests |
| **Package Management** | uv / setuptools | — | Dependency management and packaging |

---

## 2. FinMind API

### 2.1 Free API (Verified Working)

| API Method | Data Content | Fields |
|------------|--------------|--------|
| `taiwan_stock_info` | Stock basic info | industry_category, stock_id, stock_name, type, date |
| `taiwan_stock_daily` | Daily closing price | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| `taiwan_stock_month_revenue` | Monthly revenue | date, stock_id, country, revenue, revenue_month, revenue_year |
| `taiwan_stock_per_pbr` | PER/PBR/Dividend yield | date, stock_id, dividend_yield, PER, PBR |
| `taiwan_stock_balance_sheet` | Balance sheet | date, stock_id, type, value, origin_name |
| `taiwan_stock_financial_statement` | Income statement | date, stock_id, type, value, origin_name |
| `taiwan_stock_cash_flows_statement` | Cash flow statement | date, stock_id, type, value, origin_name |
| `taiwan_stock_institutional_investors` | Institutional investor activity | date, stock_id, buy, name, sell |
| `taiwan_stock_margin_purchase_short_sale` | Margin trading | date, stock_id, MarginPurchaseBuy/Sell, ShortSaleBuy/Sell |
| `taiwan_stock_dividend` | Dividend policy | date, stock_id, year, CashEarningsDistribution, CashExDividendTradingDate |
| `taiwan_stock_dividend_result` | Ex-dividend result | date, stock_id, before_price, after_price, stock_and_cache_dividend |
| `taiwan_stock_shareholding` | Foreign ownership | date, stock_id, ForeignInvestmentShares, ForeignInvestmentSharesRatio |
| `taiwan_stock_news` | News | date, stock_id, link, source, title |

### 2.2 Paid API (⚠️ Not Used)

| API Method | Data Content |
|------------|--------------|
| `taiwan_stock_holding_shares_per` | Shareholding tiers |
| `taiwan_stock_industry_chain` | Industry supply chain |
| `taiwan_stock_market_value` | Market cap |
| `taiwan_stock_monthly` | Monthly average price |
| `taiwan_stock_weekly` | Weekly average price |

### 2.3 Industry Categories (57 types)
Major industries: Semiconductor (265), Electronics (542), Biotech/Medical (271), Computer & Peripherals (141), Electronic Components (252), Communications (111), Electrical Machinery (132), Construction (91), Finance/Insurance (70), Tourism (68), Chemical (59), etc.

---

## 3. Dependency List

```toml
[project]
dependencies = [
    "filelock>=3.29.1",    # File lock (cache concurrency safety)
    "finmind>=1.9.11",     # FinMind API official SDK
    "pandas>=3.0.3",       # Data processing
    "plotly>=6.8.0",       # Interactive charts
    "pyyaml>=6.0.3",       # YAML parsing
    "requests>=2.34.2",    # HTTP requests
    "streamlit>=1.58.0",   # Frontend framework
]
```

---

## 4. Development Tools

| Tool | Purpose |
|------|---------|
| `uv` | Python package management (10-100x faster than pip) |
| `pytest` | Testing framework |
| `pytest markers` | Test categorization (e.g., `@pytest.mark.tone`) |
| `Streamlit` | Local development server |
| `Git` | Version control |
| `Hermes` | AI Agent automation scheduling |

---

## 5. Environment Setup

### 5.1 Quick Start
```bash
# Clone
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e .

# Launch
streamlit run src/main.py
```

### 5.2 Environment Variables
- `.env`: Stores API keys (if any)
- Currently FinMind free API requires no authentication

### 5.3 Testing
```bash
# Run all tests
uv run pytest

# Run tests with specific marker
uv run pytest -m tone
```
