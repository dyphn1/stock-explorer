# 股識 Stock Explorer — Architecture Definition

> This is a "must-follow before development" architecture layering specification. All new features must be developed according to the layers and data flow defined in this document.

---

## I. Layered Architecture

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer (View)                          │
│  src/pages/*.py                                     │
│  Responsibility: Pure rendering, receives data dict, produces Streamlit UI │
│  Forbidden: Directly calling FinMind API, directly reading/writing file/cache │
├─────────────────────────────────────────────────────┤
│  Routing Layer (Router)                             │
│  src/pages/router.py                                │
│  Responsibility: Manages session_state, selects View, coordinates data loading │
│  Forbidden: Directly producing UI components, directly calling API │
├─────────────────────────────────────────────────────┤
│  Business Logic Layer (Service)                     │
│  src/services/*.py                                  │
│  Responsibility: Calculates indicators, generates charts, plain-language translation, data analysis │
│  Forbidden: Using any Streamlit API, directly reading/writing cache │
├─────────────────────────────────────────────────────┤
│  Data Layer (Model/Data)                            │
│  src/data/*.py                                      │
│  Responsibility: FinMind API wrapper, cache management, data models │
│  Forbidden: Using any Streamlit API, containing business logic │
└─────────────────────────────────────────────────────┘
```

---

## II. Layer Responsibilities — Clearly Defined

### 2.1 Data Layer — `src/data/`

**Files**:
- `finmind_client.py`: FinMind API wrapper, including caching
- `models.py`: Data type definitions (if needed)

**Responsibilities**:
- Call FinMind API
- Manage local file caching (read, write, TTL expiration)
- Return pandas DataFrame or dict

**Interface conventions**:
```python
# ✅ Correct: Return DataFrame
def get_daily_price(self, stock_id: str) -> pd.DataFrame:
    ...

# ✅ Correct: Return None to indicate no data (do not raise exception)
def get_latest_price(self, stock_id: str) -> dict | None:
    ...

# ❌ Wrong: Deciding in the data layer whether to show a spinner
# ❌ Wrong: Performing business-logic operations like "take 200 records, sort, then take top 20" in the data layer
```

**Forbidden**:
- Must not import streamlit
- Must not contain business logic such as sorting or filtering top N records (unless it is an API parameter itself)
- Must not perform progress bar operations in the data layer

### 2.2 Business Logic Layer — `src/services/`

**Files**:
- `chart.py`: Plotly chart generation library (pure input data → output fig)
- `analogy_engine.py`: Plain-language translation engine (numerical values → everyday-life analogies)
- `revenue_analyzer.py`: Revenue analysis (revenue data → analysis results)
- `news_summarizer.py`: News summarization (news list → summary text)
- `adaptive_engine.py`: Event detection, freshness checking

**Responsibilities**:
- Receive DataFrame/dict, return computed results or chart objects
- All charts are generated at this layer
- All numerical calculations are completed at this layer

**Interface conventions**:
```python
# ✅ Correct: Pure function, input data → output fig
def create_revenue_trend_chart(revenue_df: pd.DataFrame) -> go.Figure:
    ...

# ✅ Correct: Pure function, input value → output text
def get_gross_margin_analogy(margin: float) -> str:
    ...

# ❌ Wrong: Using st.plotly_chart() in the service layer
# ❌ Wrong: Using st.spinner() in the service layer
```

**Forbidden**:
- Must not import streamlit
- Must not directly call FinMind API (must go through data layer)
- Must not have side effects (writing files, writing cache, etc.)

### 2.3 Routing Layer — `src/pages/router.py`

**Responsibilities**:
- Read `session_state["page"]` to determine which View to display
- Read `session_state["stock_id"]` to determine which stock to display
- Call `_router_base.get_stock_data()` to uniformly load data
- Manage "pages that don't require a specific stock" (category browser, ETF section, my watchlist, event dashboard)
- Handle loading state during page switches

**Data flow**:
```
session_state["stock_id"]
    ↓
router.load_and_render_page(client, stock_id)
    ↓
_router_base.get_stock_data(client, stock_id)  ← single entry point
    ↓
Check get_stock_data internal parallel/batch logic
    ↓
FinMindClient → cache → return data dict
    ↓
Pass to the corresponding View function
```

**Conventions**:
- Router is the only place that can decide "when to load what data"
- Must not duplicate data already loaded at the router layer in the View layer
- Must display `st.spinner` during page switches

### 2.4 Presentation Layer — `src/pages/*.py`

**Files** (each file corresponds to one page):
- `business_card.py`: Company business card
- `operation_checkup.py`: Operational checkup
- `financial_health.py`: Financial health
- `peer_comparison.py`: Peer comparison
- `group_structure.py`: Group structure
- `category_browser.py`: Category browser
- `etf_browser.py`: ETF section
- `etf_detail.py`: ETF detail
- `watchlist_page.py`: My watchlist
- `event_dashboard.py`: Event dashboard

**Responsibilities**:
- Receive `data` dict + `client` (if additional queries are needed)
- Call `src/services/` functions to generate charts
- Render UI using Streamlit API

**Conventions**:
```python
# ✅ Correct: View receives data dict, calls service to generate chart
def _render_business_card(data: dict, client: FinMindClient):
    st.markdown(f"## {data['stock_name']}")
    fig = create_revenue_pie_chart(data["monthly_revenue"])
    st.plotly_chart(fig)

# ✅ Correct: View can make additional queries through client when needed
# But only for "page-specific" small queries, must not duplicate all data already loaded by _router_base
def _render_peer_comparison(data: dict, client: FinMindClient):
    benchmark_id = get_benchmark(data["industry"])
    benchmark_data = get_stock_data(client, benchmark_id)  # additional benchmark query
    ...

# ❌ Wrong: Reloading all data already available to the page in the View
# ❌ Wrong: Calling basic queries like client.get_daily_price() in the View (should be done uniformly in router/base)
```

**Forbidden**:
- Must not directly read/write cache files
- Must not perform complex numerical calculations (should be in service layer)
- Must not contain business logic (e.g., determining whether a company is a group enterprise should be in service layer)

---

## III. Data Flow Conventions

### 3.1 Standard Data Flow

```
User action (sidebar / tab / search)
    → st.session_state update
    → st.rerun()
    → router.load_and_render_page()
        → _router_base.get_stock_data() (single entry point)
            → FinMindClient (with caching)
            → Return data dict
        → Select View function
            → View calls services/ to generate charts
            → View renders with st.*
```

### 3.2 Forbidden Reverse Dependencies

```
❌ View → directly → Data layer (skipping service)
❌ Service → directly → View (service must not have UI)
❌ Data layer → directly → View (data must not have UI)
❌ View → writes to → state other than session_state (use st.session_state)
```

### 3.3 Data Caching Strategy

| Data Type | Cache TTL | Update Timing |
|-----------|-----------|---------------|
| Daily closing price | 1 day | After market close |
| Monthly revenue | 1 day | After the 10th of each month |
| Financial report | 1 day | After quarterly announcement |
| Company basic info | 7 days | Updated after expiration |
| News | 1 day | Daily update |

**Conventions**:
- Caching is uniformly managed by `FinMindClient`
- Must not implement your own caching in the View or Service layer
- Must not use `st.cache_data` in the View layer (causes cross-session sharing that is difficult to debug)

---

## IV. Page Switching Mechanism

### 4.1 State Management

All page state is managed by `session_state`:

```python
# Global state
st.session_state["stock_id"]      # Current stock ID
st.session_state["page"]           # Current page name
st.session_state["industry_filter"] # Industry filter (if used)

# In-page state (distinguished by prefix)
st.session_state["peer_benchmark"] # Benchmark for peer comparison
st.session_state["compare_stocks"] # List of stocks to compare
```

### 4.2 Switching Flow

```
Sidebar button / tab button
    → st.session_state["stock_id"] = sid  (if needed)
    → st.session_state["page"] = page_name
    → st.rerun()  # Trigger full page repaint
```

**Principles**:
- Do not use `st.switch_page()` (it loses session_state)
- Do not manually clear unnecessary state
- When switching pages, router is responsible for wrapping data loading with `st.spinner`

### 4.3 Standalone Pages

The following pages do not require `stock_id` and are directly routed by the router:
- `Category Browser` (`category_browser.py`)
- `ETF Section` (`etf_browser.py`)
- `My Watchlist` (`watchlist_page.py`)
- `Event Dashboard` (`event_dashboard.py`)

These pages manage their own data loading and state.

---

## V. Error Handling by Layer

| Layer | Handling Method |
|-------|-----------------|
| Data layer | Return None or empty DataFrame on API failure, **do not raise exception** |
| Service layer | Return None or empty fig when receiving None/empty data, **do not raise exception** |
| View layer | Display `st.info()` or skip the section when receiving None, **do not crash** |
| Router layer | Display `st.error()` and return when `get_stock_data` returns None |

**Principle**: No layer may allow an uncaught exception to reach Streamlit.

---

## VI. Pre-Development Architecture Checklist

Before writing any new code:

- [ ] Confirm it is placed in the correct layer (data / service / page / router)
- [ ] Confirm there are no cross-layer direct calls to API or to Streamlit
- [ ] Confirm data flow direction is correct (View → Service → Data, no reverse)
- [ ] Confirm error handling is in place at every layer
- [ ] Confirm session_state management is at the router or View layer (not Data/Service layer)
- [ ] Confirm button keys are unique
- [ ] Confirm page switches have a spinner
- [ ] Confirm caching is uniformly managed by FinMindClient
- [ ] No use of `st.cache_data` in the View layer (global cache affects other sessions)

---

*Created: 2026-06-08*
*Maintainer: Main agent (PM)*
