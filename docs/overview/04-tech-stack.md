# 技術選型 — Stock Explorer

> **原則**: 選擇最簡單、最成熟的技術，優先考慮開發速度與可維護性。

---

## 1. 技術棧總覽

| 層級 | 技術 | 版本 | 說明 |
|------|------|------|------|
| **語言** | Python | 3.11+ | 主要開發語言 |
| **前端框架** | Streamlit | ≥1.58.0 | 快速迭代，適合 MVP |
| **數據 API** | FinMind | ≥1.9.11 | 台灣股票數據，50+ 數據集 |
| **數據處理** | pandas | ≥3.0.3 | 數據清洗、特徵工程 |
| **圖表** | Plotly | ≥6.8.0 | 互動式圖表 |
| **配置** | PyYAML | ≥6.0.3 | YAML 配置文件 |
| **HTTP** | requests | ≥2.34.2 | API 請求 |
| **快取** | filelock | ≥3.29.1 | 本地文件快取鎖 |
| **測試** | pytest | — | 單元測試與整合測試 |
| **套件管理** | uv / setuptools | — | 依賴管理與打包 |

---

## 2. FinMind API

### 2.1 免費 API（已驗證可用）

| API 方法 | 數據內容 | 欄位 |
|----------|----------|------|
| `taiwan_stock_info` | 股票基本資訊 | industry_category, stock_id, stock_name, type, date |
| `taiwan_stock_daily` | 日收盤價 | date, stock_id, Trading_Volume, Trading_money, open, max, min, close, spread, Trading_turnover |
| `taiwan_stock_month_revenue` | 月營收 | date, stock_id, country, revenue, revenue_month, revenue_year |
| `taiwan_stock_per_pbr` | PER/PBR/殖利率 | date, stock_id, dividend_yield, PER, PBR |
| `taiwan_stock_balance_sheet` | 資產負債表 | date, stock_id, type, value, origin_name |
| `taiwan_stock_financial_statement` | 損益表 | date, stock_id, type, value, origin_name |
| `taiwan_stock_cash_flows_statement` | 現金流量表 | date, stock_id, type, value, origin_name |
| `taiwan_stock_institutional_investors` | 三大法人買賣超 | date, stock_id, buy, name, sell |
| `taiwan_stock_margin_purchase_short_sale` | 融資融券 | date, stock_id, MarginPurchaseBuy/Sell, ShortSaleBuy/Sell |
| `taiwan_stock_dividend` | 股利政策 | date, stock_id, year, CashEarningsDistribution, CashExDividendTradingDate |
| `taiwan_stock_dividend_result` | 除權息結果 | date, stock_id, before_price, after_price, stock_and_cache_dividend |
| `taiwan_stock_shareholding` | 外資持股 | date, stock_id, ForeignInvestmentShares, ForeignInvestmentSharesRatio |
| `taiwan_stock_news` | 新聞 | date, stock_id, link, source, title |

### 2.2 付費 API（⚠️ 不使用）

| API 方法 | 數據內容 |
|----------|----------|
| `taiwan_stock_holding_shares_per` | 持股分級 |
| `taiwan_stock_industry_chain` | 產業供應鏈 |
| `taiwan_stock_market_value` | 市值 |
| `taiwan_stock_monthly` | 月均價 |
| `taiwan_stock_weekly` | 週均價 |

### 2.3 產業分類（57 種）
主要產業：半導體 (265)、電子 (542)、生技醫療 (271)、電腦及週邊 (141)、電子零組件 (252)、通信 (111)、電機機械 (132)、營建 (91)、金融保險 (70)、觀光 (68)、化工 (59) 等。

---

## 3. 依賴清單

```toml
[project]
dependencies = [
    "filelock>=3.29.1",    # 文件鎖（快取並發安全）
    "finmind>=1.9.11",     # FinMind API 官方 SDK
    "pandas>=3.0.3",       # 數據處理
    "plotly>=6.8.0",       # 互動圖表
    "pyyaml>=6.0.3",       # YAML 解析
    "requests>=2.34.2",    # HTTP 請求
    "streamlit>=1.58.0",   # 前端框架
]
```

---

## 4. 開發工具

| 工具 | 用途 |
|------|------|
| `uv` | Python 套件管理（比 pip 快 10-100x） |
| `pytest` | 測試框架 |
| `pytest markers` | 測試分類（如 `@pytest.mark.tone`） |
| `Streamlit` | 本地開發伺服器 |
| `Git` | 版本控制 |
| `Hermes` | AI Agent 自動化排程 |

---

## 5. 環境設置

### 5.1 快速開始
```bash
# Clone
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# 建立虛擬環境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 安裝依賴
pip install -e .

# 啟動
streamlit run src/main.py
```

### 5.2 環境變數
- `.env`：存放 API keys（如果有）
- 目前 FinMind 免費 API 不需要認證

### 5.3 測試
```bash
# 執行所有測試
uv run pytest

# 執行特定標記的測試
uv run pytest -m tone
```
