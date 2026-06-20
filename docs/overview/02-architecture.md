# System Architecture — Stock Explorer

> **Status**: Continuously evolving | **Last Updated**: 2026-06-17

---

## 1. Architecture Overview

Stock Explorer uses a **strict layered architecture** to ensure separation of concerns, testability, and maintainability.

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer                                  │
│  src/pages/*.py                                      │
│  Responsibility: pure rendering, receives data dict, produces Streamlit UI │
│  Forbidden: direct API calls, direct cache read/write │
├─────────────────────────────────────────────────────┤
│  Routing Layer                                       │
│  src/pages/router.py                                 │
│  Responsibility: manage session_state, select View, coordinate data loading │
│  Forbidden: direct UI component generation, direct API calls │
├─────────────────────────────────────────────────────┤
│  Business Logic Layer                                │
│  src/services/*.py                                   │
│  Responsibility: calculate metrics, generate charts, plain-language translation, data analysis │
│  Forbidden: using any Streamlit API, direct cache read/write │
├─────────────────────────────────────────────────────┤
│  Data Layer                                          │
│  src/data/*.py                                       │
│  Responsibility: FinMind API wrapper, cache management, data models │
│  Forbidden: using any Streamlit API, containing business logic │
└─────────────────────────────────────────────────────┘
```

### Dependency Rules (Strictly Unidirectional)
```
Presentation → Routing → Business Logic → Data Layer
```

**Reverse dependencies are forbidden**:
- ❌ View → direct → Data Layer (skipping Service)
- ❌ Service → direct → View (Service cannot have UI)
- ❌ Data Layer → direct → View (Data cannot have UI)

---

## 2. Directory Structure

```
stock-explorer/
├── main.py                    # Entry point (sidebar + search + welcome)
├── run.py                     # Launch script
├── pyproject.toml             # Project config and dependencies
│
├── config/                    # Configuration files (YAML)
│   ├── watchlist.yaml         # Watchlist
│   ├── events.yaml            # Event records
│   ├── quiz.yaml              # Comprehension quiz
│   └── lessons/               # Learning academy lessons
│
├── locales/                   # Internationalization strings
│   ├── zh-TW.yaml             # Traditional Chinese (default)
│   └── en.yaml                # English
│
├── src/
│   ├── __init__.py
│   ├── main.py                # Streamlit entry
│   │
│   ├── core/                  # Core framework layer
│   │   ├── i18n.py            # i18n module
│   │   └── chassis.py         # Plugin Chassis (planned)
│   │
│   ├── data/                  # Data access layer
│   │   ├── finmind_client.py  # FinMind API wrapper (with cache)
│   │   └── batch_api.py       # Batch API
│   │
│   ├── services/              # Business logic layer (47+ files)
│   │   ├── chart_stock.py     # Stock chart generation
│   │   ├── chart_market.py    # Market chart generation
│   │   ├── revenue_analyzer.py
│   │   ├── analogy_engine.py  # Real-world analogy engine
│   │   ├── adaptive_engine.py # Event detection + adaptation
│   │   ├── health_scoring.py
│   │   ├── moat_analyzer.py
│   │   ├── risk_analyzer.py
│   │   ├── metric_explainer.py
│   │   ├── glossary_service.py
│   │   ├── settings_service.py
│   │   ├── watchlist.py
│   │   └── llm/               # LLM integration
│   │       ├── base.py
│   │       ├── factory.py
│   │       └── template_provider.py
│   │
│   └── pages/                 # Presentation layer (pages)
│       ├── router.py          # Page router
│       ├── _router_base.py    # Shared utilities
│       ├── url_sync.py        # URL ↔ session sync
│       ├── business_card/     # Business card (split into sub-modules)
│       ├── operation_checkup.py
│       ├── financial_health.py
│       ├── peer_comparison.py
│       ├── group_structure.py
│       ├── category_browser.py
│       ├── etf_browser.py
│       ├── etf_detail.py
│       ├── watchlist_page.py
│       ├── event_dashboard.py
│       └── ... (20+ pages total)
│
├── tests/                     # Tests
│   ├── test_business_logic.py
│   ├── test_daily_market.py
│   ├── test_dividend_roe.py
│   └── ...
│
└── docs/                      # Project documentation
    ├── overview/              # Overview documents (this directory)
    ├── adr/                   # Architecture decision records
    ├── roadmap/               # Roadmap
    ├── dev-guide/             # Development guide
    ├── roles/                 # AI Agent role definitions
    └── state/                 # Status tracking
```

---

## 3. Data Flow

### 3.1 Standard Data Flow
```
User action (sidebar / tab / search)
    → st.session_state update
    → st.rerun()
    → router.load_and_render_page()
        → _router_base.get_stock_data() (single entry point)
            → FinMindClient (with cache)
            → returns data dict
        → Select View function
            → View calls services/ to generate charts
            → View renders with st.*
```

### 3.2 Caching Strategy
| Data Type | Cache TTL | Description |
|-----------|-----------|-------------|
| Stock basic info | 24h | Stock list doesn't change often |
| Daily closing price | 24h | Historical data is not retroactively modified |
| Monthly revenue | 24h | Fixed after monthly revenue announcement |
| News | 1h | Updated more frequently |
| Institutional investor activity | 24h | Updated daily |

---

## 4. Plugin Chassis Architecture (Planned)

> **Problem**: router.py currently has 274 lines with 33 if-elif branches; adding a page requires modifying 3 places.

**Goal**: Design each page as an independent Plugin following a unified protocol, with the core framework automatically scanning, registering, and routing.

```python
# Plugin Protocol
class BasePlugin(Protocol):
    name: str
    icon: str
    requires_stock_id: bool
    
    def render(self, data: dict, client: FinMindClient) -> None: ...
```

**Benefits**:
- Add/remove/disable feature = register/unregister plugin, zero routing logic changes
- Independent development/testing of individual features
- Dynamic feature enable/disable

---

## 5. i18n Internationalization

> **Current state**: 93 .py files in src/, totaling **3,146** hardcoded Chinese strings.

**Architecture**:
- `src/core/i18n.py`: Single entry point, provides `t()` function
- `locales/zh-TW.yaml`: Traditional Chinese (default)
- `locales/en.yaml`: English

**Naming convention**: `<module>.<submodule>.<component>.<purpose>`
- Example: `pages.business_card.section.header.button.label`

---

## 6. Known Technical Debt

| # | Issue | Severity | Description |
|---|-------|----------|-------------|
| 1 | router.py if-elif bloat | P0 | 274 lines, 33 branches, needs refactor to Plugin Chassis |
| 2 | Hardcoded Chinese strings | P0 | 3,146 instances, needs full i18n |
| 3 | API abuse: get_stock_info | P1 | Fetches entire stock list on every call |
| 4 | Cache key includes end_date | P1 | Causes daily cache invalidation |
| 5 | business_card.py too large | P1 | 561 lines, planned split into sub-directory |
