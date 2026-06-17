# 系統架構 — Stock Explorer

> **狀態**: 持續演進中 | **上次更新**: 2026-06-17

---

## 1. 架構總覽

Stock Explorer 採用**嚴格分層架構**，確保關注點分離、可測試性與可維護性。

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer (視圖層)                         │
│  src/pages/*.py                                      │
│  職責：純渲染，接收 data dict，產生 Streamlit UI       │
│  禁止：直接呼叫 API、直接讀寫快取                      │
├─────────────────────────────────────────────────────┤
│  Routing Layer (路由層)                              │
│  src/pages/router.py                                 │
│  職責：管理 session_state、選擇 View、協調數據載入      │
│  禁止：直接產生 UI 元件、直接呼叫 API                  │
├─────────────────────────────────────────────────────┤
│  Business Logic Layer (業務邏輯層)                    │
│  src/services/*.py                                   │
│  職責：計算指標、生成圖表、白話翻譯、數據分析            │
│  禁止：使用任何 Streamlit API、直接讀寫快取            │
├─────────────────────────────────────────────────────┤
│  Data Layer (數據層)                                 │
│  src/data/*.py                                       │
│  職責：FinMind API 封裝、快取管理、數據模型             │
│  禁止：使用任何 Streamlit API、包含業務邏輯             │
└─────────────────────────────────────────────────────┘
```

### 依賴規則（嚴格單向）
```
Presentation → Routing → Business Logic → Data Layer
```

**禁止反向依賴**：
- ❌ View → 直接 → Data Layer（跳過 Service）
- ❌ Service → 直接 → View（Service 不能有 UI）
- ❌ Data Layer → 直接 → View（Data 不能有 UI）

---

## 2. 目錄結構

```
stock-explorer/
├── main.py                    # 入口（sidebar + search + welcome）
├── run.py                     # 啟動腳本
├── pyproject.toml             # 專案配置與依賴
│
├── config/                    # 配置文件（YAML）
│   ├── watchlist.yaml         # 關注列表
│   ├── events.yaml            # 事件記錄
│   ├── quiz.yaml              # 理解力測驗
│   └── lessons/               # 學習學院課程
│
├── locales/                   # 國際化字串
│   ├── zh-TW.yaml             # 繁體中文（預設）
│   └── en.yaml                # 英文
│
├── src/
│   ├── __init__.py
│   ├── main.py                # Streamlit 入口
│   │
│   ├── core/                  # 核心框架層
│   │   ├── i18n.py            # i18n 模組
│   │   └── chassis.py         # Plugin Chassis（規劃中）
│   │
│   ├── data/                  # 數據存取層
│   │   ├── finmind_client.py  # FinMind API 封裝（含快取）
│   │   └── batch_api.py       # 批次 API
│   │
│   ├── services/              # 業務邏輯層（47+ 檔案）
│   │   ├── chart_stock.py     # 股票圖表生成
│   │   ├── chart_market.py    # 市場圖表生成
│   │   ├── revenue_analyzer.py
│   │   ├── analogy_engine.py  # 生活化比喻引擎
│   │   ├── adaptive_engine.py # 事件偵測 + 自適應
│   │   ├── health_scoring.py
│   │   ├── moat_analyzer.py
│   │   ├── risk_analyzer.py
│   │   ├── metric_explainer.py
│   │   ├── glossary_service.py
│   │   ├── settings_service.py
│   │   ├── watchlist.py
│   │   └── llm/               # LLM 整合
│   │       ├── base.py
│   │       ├── factory.py
│   │       └── template_provider.py
│   │
│   └── pages/                 # 視圖層（頁面）
│       ├── router.py          # 頁面路由器
│       ├── _router_base.py    # 共享工具
│       ├── url_sync.py        # URL ↔ session 同步
│       ├── business_card/     # 名片（已拆分為 sub-modules）
│       ├── operation_checkup.py
│       ├── financial_health.py
│       ├── peer_comparison.py
│       ├── group_structure.py
│       ├── category_browser.py
│       ├── etf_browser.py
│       ├── etf_detail.py
│       ├── watchlist_page.py
│       ├── event_dashboard.py
│       └── ...（共 20+ 頁面）
│
├── tests/                     # 測試
│   ├── test_business_logic.py
│   ├── test_daily_market.py
│   ├── test_dividend_roe.py
│   └── ...
│
└── docs/                      # 專案文件
    ├── overview/               # 總覽文件（本目錄）
    ├── adr/                    # 架構決策記錄
    ├── roadmap/                # 路線圖
    ├── dev-guide/              # 開發指南
    ├── roles/                  # AI Agent 角色定義
    └── state/                  # 狀態追蹤
```

---

## 3. 數據流

### 3.1 標準數據流
```
使用者操作（sidebar / tab / search）
    → st.session_state 更新
    → st.rerun()
    → router.load_and_render_page()
        → _router_base.get_stock_data()（單一入口）
            → FinMindClient（含快取）
            → 返回 data dict
        → 選擇 View function
            → View 呼叫 services/ 生成圖表
            → View 用 st.* 渲染
```

### 3.2 快取策略
| 數據類型 | 快取 TTL | 說明 |
|----------|----------|------|
| 股票基本資訊 | 24h | 股票列表不常變動 |
| 日收盤價 | 24h | 歷史數據不回溯修改 |
| 月營收 | 24h | 月營收公布後固定 |
| 新聞 | 1h | 較常更新 |
| 法人動向 | 24h | 每日更新 |

---

## 4. Plugin Chassis 架構（規劃中）

> **問題**: router.py 目前有 274 行，包含 33 個 if-elif 分支，新增頁面需修改 3 處。

**目標**：將每個頁面設計為獨立 Plugin，遵循統一協議，核心框架自動掃描、註冊、路由。

```python
# Plugin Protocol
class BasePlugin(Protocol):
    name: str
    icon: str
    requires_stock_id: bool
    
    def render(self, data: dict, client: FinMindClient) -> None: ...
```

**優點**：
- 新增/移除/停用功能 = 註冊/取消註冊 plugin，零修改路由邏輯
- 可獨立開發/測試單一 feature
- 動態啟用/停用 feature

---

## 5. i18n 國際化

> **現狀**: src/ 內 93 個 .py 檔案，共 **3,146 個** hardcoded 中文字串。

**架構**：
- `src/core/i18n.py`：唯一出入口，提供 `t()` 函數
- `locales/zh-TW.yaml`：繁體中文（預設）
- `locales/en.yaml`：英文

**命名規範**：`<module>.<submodule>.<component>.<purpose>`
- 範例：`pages.business_card.section.header.button.label`

---

## 6. 已知技術債務

| # | 問題 | 嚴重度 | 說明 |
|---|------|--------|------|
| 1 | router.py if-elif 膨脹 | P0 | 274 行，33 個分支，需重構為 Plugin Chassis |
| 2 | Hardcoded 中文字串 | P0 | 3,146 處，需全面 i18n |
| 3 | API 濫用：get_stock_info | P1 | 每次呼叫都拉取全部股票列表 |
| 4 | 快取 key 包含 end_date | P1 | 導致每日快取失效 |
| 5 | business_card.py 過大 | P1 | 561 行，已規劃拆分為 sub-directory |
| 6 | 缺乏單元測試覆蓋 | P1 | 目前 319+ 測試通過但覆蓋率不足 |
