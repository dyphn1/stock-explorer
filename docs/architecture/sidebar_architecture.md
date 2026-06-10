# Stock Explorer Sidebar Architecture Redesign

**Date:** 2026-06-09
**Author:** System Architect (Hermes)
**Status:** Proposal — ready for implementation
**Scope:** `src/main.py` sidebar section (lines 92–156), with supporting modules

---

## 1. Current Sidebar Architecture

### 1.1 Structure

The sidebar lives entirely inside `src/main.py`, lines 92–156, in a single `with st.sidebar:` block. It is a flat list of Streamlit components:

```
with st.sidebar:
    st.markdown("## 🔍 股識")              # Brand
    st.markdown("*認識一家公司，從這裡開始*")
    "---"
    st.text_input(...)                       # Search box
    "---"
    st.markdown("### 📈 熱門股票")           # Hot stocks header
    [st.button(...) for 9 stocks]           # Hot stock buttons
    "---"
    st.markdown("### 🏷️ 熱門 ETF")           # Hot ETFs header
    [st.button(...) for 5 ETFs]            # Hot ETF buttons
    "---"
    st.button("📋 我的關注")                # Watchlist nav
    st.button("🔔 事件儀表板")              # Events nav
    "---"
    st.markdown(disclaimer_html)             # Disclaimer
```

### 1.2 Streamlit Components Used

| Component | Purpose | Line(s) |
|-----------|---------|---------|
| `st.markdown` | Brand title, section headers, disclaimer | 95–96, 107, 126, 150–156 |
| `st.text_input` | Search box (collapsed label) | 100–104 |
| `st.button` × 16 | Hot stocks (9), Hot ETFs (5), Watchlist (1), Events (1) | 121–123, 136–138, 142–143, 146–147 |
| `st.sidebar.warning` | Rate limit banner (conditional) | 90 |
| `st.sidebar.error` | Search no-results (conditional, lines 182–183) | 182–183 |
| `st.sidebar.selectbox` | Multi-match search results (conditional) | 178 |

### 1.3 Data Flow

1. **On every rerun**, `main.py` executes top-to-bottom.
2. `sync_url_to_session()` reads `?page=` and `?stock_id=` from URL → writes to `st.session_state`.
3. Sidebar renders **before** main content (it's defined first, lines 92–156).
4. Sidebar buttons call `navigate_to(page=..., stock_id=...)` which:
   - Updates `st.session_state`
   - Writes to `st.query_params`
   - Calls `st.rerun()`
5. Main content (lines 159–200) then reads `st.session_state["page"]` and `st.session_state["stock_id"]` to render via `load_and_render_page()`.

**Key characteristic:** There is **no state shared between sidebar and main content** except through `st.session_state["page"]` and `st.session_state["stock_id"]`. The sidebar has no knowledge of what's in the watchlist.

### 1.4 Problems with Current Architecture

| # | Problem | Severity |
|---|---------|----------|
| 1 | **No inline price data** — sidebar shows only static labels, no prices | P0 (gap) |
| 2 | **Sidebar collapse bug** — `initial_sidebar_state="auto"` + collapsed sidebar = no way to re-expand | P0 (bug) |
| 3 | **Search belongs in main content** — industry convention puts search at top-center | P1 (UX) |
| 4 | **Flat structure** — 16 buttons + search with no hierarchy | P1 (UX) |
| 5 | **Hardcoded stock lists** — hot stocks/ETF IDs are hardcoded in main.py | P2 (maint) |
| 6 | **No watchlist integration** — sidebar watchlist button just navigates, shows nothing inline | P0 (gap) |

---

## 2. Bug Analysis: Sidebar Collapse

### 2.1 Root Cause

`st.set_page_config(initial_sidebar_state="auto")` on line 22 sets the initial state to `"auto"`, which means:
- **Desktop (>1024px):** sidebar starts expanded
- **Tablet/mobile:** sidebar starts collapsed/overlay

The problem: Streamlit provides a **Collapse** button (a small `◀`/`▶` arrow at the sidebar's left edge) by default. When a user clicks it to collapse the sidebar, Streamlit:

1. Hides the sidebar content
2. Leaves a **thin collapsed tab** visible on screen edge

**The critical bug occurs on certain viewport sizes or after certain interactions** where the collapsed tab becomes invisible or unclickable. This is a known Streamlit issue, especially:
- In `"auto"` mode where the default state is viewport-dependent
- When sidebar content is long (the current sidebar has 16+ items + search + disclaimer)
- After `st.rerun()` calls from `navigate_to()`, which re-render the entire page and can reset sidebar focus

### 2.2 Why It Happens (Technical)

Streamlit's sidebar collapse is controlled by **client-side JavaScript**. When the sidebar is collapsed:
- Streamlit sets a CSS class that hides `.stSidebar` content
- A small toggle button should remain visible

The bug triggers when:
1. The page layout recalculates during `st.rerun()`
2. The sidebar toggle button is rendered **outside** the viewport or **behind** other elements
3. `initial_sidebar_state="auto"` causes the initial state to be ambiguous on mid-size screens (768–1024px range), where Streamlit's CSS media queries may conflict with the collapse JavaScript

### 2.3 Proposed Fix

**Change `initial_sidebar_state` to `"expanded"`** and add a custom collapse/expand mechanism:

```python
# BEFORE (line 22):
initial_sidebar_state="auto",

# AFTER:
initial_sidebar_state="expanded",
```

This ensures:
- Sidebar always starts expanded (users can still collapse it)
- Desktop users (primary audience) never land on a collapsed sidebar on first load
- The collapse toggle button is rendered reliably

**Additionally**, add a visible "hamburger" expand button in the main content area that appears when the sidebar is collapsed:

```css
/* CSS injection to ensure collapse toggle is always visible */
section[data-testid="stSidebar"] > div {
    overflow-x: visible;
}
```

And in the main content area, detect collapsed state and show an expand button:

```python
# In main content area, before page rendering:
# Use a hidden anchor + JS to detect sidebar state
# If collapsed, show a "☰ 展開側邊欄" button
```

**However**, Streamlit doesn't natively expose sidebar collapse state to Python. The most reliable approach is:

1. **Set `initial_sidebar_state="expanded"`** — prevents the bug on first load
2. **Add a custom CSS-styled expand button** in the main content area that uses `st.query_params` to force a rerender with sidebar expanded
3. **Use `st.session_state["sidebar_collapsed"]`** as a Python-side flag, toggled by a custom button

The cleanest implementation:

```python
# In main.py, after set_page_config:
if "sidebar_collapsed" not in st.session_state:
    st.session_state["sidebar_collapsed"] = False

# In main content area (before page rendering):
if st.session_state.get("sidebar_collapsed"):
    if st.button("☰ 展開側邊欄", key="expand_sidebar"):
        st.session_state["sidebar_collapsed"] = False
        st.rerun()
```

**Note:** This is a workaround. The true fix requires Streamlit to improve their collapse toggle. For now, `"expanded"` default + a visible expand button in main content is the most reliable approach.

---

## 3. Architecture for Inline Price Data

### 3.1 Requirements

The sidebar should display live prices for watchlist stocks (Yahoo Finance style):
- **Show:** stock name, current price, price change (absolute + %)
- **Update:** periodically without full page reload
- **Not block:** main content area rendering
- **Handle:** API rate limits gracefully (FinMind has rate limits)

### 3.2 Streamlit Constraints

Streamlit's execution model is **top-to-bottom rerun on every interaction**. There is no native "partial update" or "background refresh" mechanism. This means:

1. **Every sidebar rerun re-executes the entire `main.py`** — including data fetching
2. **`st.rerun()` triggers a full page reload** — sidebar + main content both re-render
3. **There is no WebSocket or SSE push** from server to client in vanilla Streamlit

### 3.3 Proposed Architecture: Cached Polling with Session State

Given Streamlit's constraints, the best approach is:

```
┌─────────────────────────────────────────────────────────────┐
│                     main.py (every rerun)                    │
│                                                              │
│  ┌─── Sidebar ────────────────────────────────────────────┐  │
│  │  _render_sidebar(client)                               │  │
│  │    ├── Brand + Search                                  │  │
│  │    ├── ⭐ Watchlist (collapsible)                      │  │
│  │    │     └── _render_watchlist_prices(client)          │  │
│  │    │           ├── Check: cache_age < TTL? → use cache │  │
│  │    │           ├── Else: fetch from FinMind            │  │
│  │    │           └── Render: name + price + change       │  │
│  │    ├── 🔥 Hot Stocks (collapsible)                     │  │
│  │    │     └── _render_hot_prices(client)                │  │
│  │    ├── 🏷️ Hot ETFs (collapsible)                       │  │
│  │    │     └── _render_etf_prices(client)                │  │
│  │    ├── 📉 Market Overview                              │  │
│  │    └── Navigation + Disclaimer                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌─── Main Content ───────────────────────────────────────┐  │
│  │  load_and_render_page(client, stock_id)                │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 New Module: `src/services/sidebar_price_cache.py`

Create a dedicated service for sidebar price data:

```python
# src/services/sidebar_price_cache.py
"""
Sidebar price cache — lightweight, TTL-based caching for sidebar price displays.
Separate from FinMindClient cache to avoid polluting main data fetches.
"""

import time
import streamlit as st
from typing import Optional

# Cache TTL in seconds — how often to re-fetch prices
PRICE_CACHE_TTL = 300  # 5 minutes

def _cache_key(stock_id: str) -> str:
    return f"sidebar_price_{stock_id}"

def get_cached_price(stock_id: str) -> Optional[dict]:
    """Return cached price data if fresh, else None."""
    key = _cache_key(stock_id)
    if key in st.session_state:
        entry = st.session_state[key]
        if time.time() - entry["timestamp"] < PRICE_CACHE_TTL:
            return entry["data"]
    return None

def set_cached_price(stock_id: str, data: dict) -> None:
    """Store price data in session cache."""
    key = _cache_key(stock_id)
    st.session_state[key] = {
        "data": data,
        "timestamp": time.time(),
    }

def fetch_prices_batch(client, stock_ids: list[str]) -> dict[str, dict]:
    """
    Fetch prices for multiple stocks, using cache where available.
    Returns {stock_id: {price, change, name}} dict.
    """
    results = {}
    to_fetch = []

    # Check cache first
    for sid in stock_ids:
        cached = get_cached_price(sid)
        if cached is not None:
            results[sid] = cached
        else:
            to_fetch.append(sid)

    # Fetch uncached stocks
    for sid in to_fetch:
        try:
            price_data = client.get_latest_price(sid)
            if price_data:
                info = client.get_stock_info(sid)
                name = info.iloc[0]["stock_name"] if len(info) > 0 else sid
                data = {
                    "price": price_data.get("close"),
                    "change": price_data.get("change"),
                    "name": name,
                }
                set_cached_price(sid, data)
                results[sid] = data
        except Exception:
            results[sid] = {"price": None, "change": None, "name": sid}

    return results
```

**Why a separate cache?**
- FinMind API has rate limits — sidebar shouldn't trigger extra API calls on every main content rerun
- Sidebar prices can be slightly stale (5-min TTL is fine for a sidebar display)
- Session-state cache is per-user, per-session — no cross-user leakage
- Avoids re-fetching prices when user navigates between pages

### 3.5 New Module: `src/services/sidebar_render.py`

Extract sidebar rendering from `main.py` into a dedicated module:

```python
# src/services/sidebar_render.py
"""
Sidebar rendering — extracted from main.py for modularity.
"""

import streamlit as st
from src.pages.url_sync import navigate_to
from src.services.watchlist import load_watchlist
from src.services.sidebar_price_cache import fetch_prices_batch

# Hot stock/ETF definitions (moved from main.py)
HOT_STOCKS = [
    ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
    ("2308", "台達電"), ("2881", "富邦金"), ("1101", "台泥"),
    ("2002", "中鋼"), ("1301", "台塑"),
]

HOT_ETFS = [
    ("0050", "元大台灣50"), ("0056", "元大高股息"),
    ("00878", "國泰永續高股息"), ("00919", "群益台灣精選高息"),
    ("006208", "富邦台50"),
]

def render_sidebar(client):
    """Render the complete sidebar."""
    _render_brand()
    _render_search()
    _render_watchlist_section(client)
    _render_hot_stocks_section(client)
    _render_hot_etfs_section(client)
    _render_market_overview(client)
    _render_nav_section()
    _render_disclaimer()

def _render_brand():
    st.markdown("## 🔍 股識")
    st.markdown("*認識一家公司，從這裡開始*")
    st.markdown("---")

def _render_search():
    search_input = st.text_input(
        "輸入股票代號或名稱",
        placeholder="例如：2330 或 台積電",
        label_visibility="collapsed",
        key="sidebar_search",
    )
    st.markdown("---")
    return search_input

def _render_watchlist_section(client):
    """Collapsible watchlist with inline prices."""
    # Use expander for collapsible section
    with st.expander("⭐ 我的關注", expanded=True):
        entries = load_watchlist()
        if not entries:
            st.caption("尚未加入關注標的")
            return

        # Batch fetch prices (cached)
        stock_ids = [e["stock_id"] for e in entries]
        prices = fetch_prices_batch(client, stock_ids)

        for entry in entries:
            sid = entry["stock_id"]
            name = entry.get("name", sid)
            data = prices.get(sid, {})
            _render_price_row(sid, name, data, is_watched=True)

def _render_hot_stocks_section(client):
    """Collapsible hot stocks with inline prices."""
    with st.expander("🔥 熱門股票", expanded=False):
        stock_ids = [sid for sid, _ in HOT_STOCKS]
        prices = fetch_prices_batch(client, stock_ids)
        for sid, name in HOT_STOCKS:
            data = prices.get(sid, {})
            _render_price_row(sid, name, data, is_watched=False)

def _render_hot_etfs_section(client):
    """Collapsible hot ETFs with inline prices."""
    with st.expander("🏷️ 熱門 ETF", expanded=False):
        etf_ids = [sid for sid, _ in HOT_ETFS]
        prices = fetch_prices_batch(client, etf_ids)
        for sid, name in HOT_ETFS:
            data = prices.get(sid, {})
            _render_price_row(sid, name, data, is_watched=False)

def _render_price_row(stock_id: str, name: str, data: dict, is_watched: bool):
    """
    Render a single stock row in the sidebar.
    Compact format: 2330 台積電  270 ▲1.5%
    Clickable to navigate to stock page.
    """
    price = data.get("price")
    change = data.get("change")

    # Format price display
    if price is not None:
        price_str = f"{price:,.0f}"
        if change is not None:
            sign = "+" if change >= 0 else ""
            # 台股慣例：紅漲綠跌
            color = "#E74C3C" if change >= 0 else "#27AE60"
            arrow = "▲" if change >= 0 else "▼"
            change_str = f'<span style="color:{color};font-size:0.75rem;">{arrow}{sign}{change:,.0f}</span>'
        else:
            change_str = ""
    else:
        price_str = "—"
        change_str = ""

    # Use columns for compact layout
    col1, col2 = st.columns([3, 2])
    with col1:
        btn_label = f"{stock_id} {name}"
        if st.button(btn_label, key=f"sidebar_{stock_id}", use_container_width=True):
            navigate_to(page="名片", stock_id=stock_id)
    with col2:
        st.markdown(f"**{price_str}** {change_str}", unsafe_allow_html=True)

def _render_market_overview(client):
    """Market indices at bottom of sidebar."""
    st.markdown("---")
    st.markdown("### 📉 市場總覽")
    # Fetch and display 加權指數, 櫃買指數
    # Use cached prices with longer TTL (10 min)
    # Compact format: 加權指數 22,341 ▲0.5%

def _render_nav_section():
    """Navigation buttons."""
    st.markdown("---")
    if st.button("📋 我的關注", key="sidebar_watchlist", use_container_width=True):
        navigate_to(page="我的關注")
    if st.button("🔔 事件儀表板", key="sidebar_events", use_container_width=True):
        navigate_to(page="事件儀表板")

def _render_disclaimer():
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
    ⚠️ 本工具僅供認識公司使用，<br>
    不構成任何投資建議。<br>
    投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)
```

### 3.6 Session State Keys

New session state keys needed:

| Key | Type | Purpose | TTL |
|-----|------|---------|-----|
| `sidebar_price_{stock_id}` | `dict{data, timestamp}` | Per-stock price cache | 300s |
| `sidebar_search` | `str` | Search input value | N/A (widget state) |
| `sidebar_collapsed` | `bool` | Collapse state flag | session |
| `sidebar_market_{index_id}` | `dict{data, timestamp}` | Market index cache | 600s |

### 3.7 Data Flow for Price Updates

```
User navigates to stock page
        │
        ▼
main.py reruns (top to bottom)
        │
        ▼
sync_url_to_session()  ← URL → session_state
        │
        ▼
render_sidebar(client)
        │
        ├── _render_watchlist_section()
        │       │
        │       ├── load_watchlist()  ← reads config/watchlist.yaml
        │       │
        │       └── fetch_prices_batch(client, stock_ids)
        │               │
        │               ├── For each stock_id:
        │               │     ├── Check session_state cache (TTL 300s)
        │               │     │     ├── Fresh → use cached data
        │               │     │     └── Stale/empty → call client.get_latest_price()
        │               │     └── Store result in session_state cache
        │               │
        │               └── Return {stock_id: {price, change, name}}
        │
        ├── _render_hot_stocks_section()  ← same pattern
        ├── _render_hot_etfs_section()    ← same pattern
        └── _render_market_overview()     ← same pattern, longer TTL
```

**Key design decisions:**
- **Cache-first:** Never fetch if cache is fresh — prevents API hammering during rapid reruns
- **Per-session cache:** `st.session_state` is isolated per user session
- **Graceful degradation:** If API fails, show "—" instead of crashing
- **Batch fetching:** Fetch all watchlist prices in one pass, not one-by-one

---

## 4. Proposed Redesign: Complete Sidebar Architecture

### 4.1 New Component Hierarchy

```
st.sidebar
├── Brand (always visible)
│   ├── 🔍 股識
│   └── tagline
│
├── Search (always visible)
│   └── st.text_input
│
├── ⭐ Watchlist (st.expander, expanded=True by default)
│   ├── Row: 2330 台積電  [270 ▲1.5%]  ← clickable
│   ├── Row: 2317 鴻海    [150 ▼0.3%]
│   └── Row: 2454 聯發科  [890 ▲2.1%]
│
├── 🔥 Hot Stocks (st.expander, expanded=False)
│   ├── Row: 2330 台積電  [270 ▲1.5%]
│   └── ... (8 more)
│
├── 🏷️ Hot ETFs (st.expander, expanded=False)
│   ├── Row: 0050 元大台灣50  [145 ▲0.8%]
│   └── ... (4 more)
│
├── 📉 Market Overview (always visible, compact)
│   ├── 加權指數  22,341  ▲0.5%
│   └── 櫃買指數    234.5  ▼0.2%
│
├── Navigation
│   ├── 📋 我的關注 (button)
│   └── 🔔 事件儀表板 (button)
│
└── Disclaimer (always visible)
```

### 4.2 Streamlit Components to Use

| Component | Usage | Why |
|-----------|-------|-----|
| `st.expander` | Collapsible sections (Watchlist, Hot Stocks, Hot ETFs) | Native collapsible, animated, accessible |
| `st.columns` | Price row layout (name + price) | Compact inline display |
| `st.button` | Stock rows (clickable) | Navigates to stock page |
| `st.markdown` | Price formatting, change indicators | Color-coded ▲▼ with inline HTML |
| `st.text_input` | Search box | Existing, keep as-is |
| `st.caption` | Empty state hints | Subtle, non-intrusive |

### 4.3 Responsive Behavior

| Viewport | Behavior |
|----------|----------|
| **> 1024px (desktop)** | Persistent sidebar, 280px wide, all sections visible |
| **768–1024px (tablet)** | Persistent sidebar, 240px wide, sections collapsed by default |
| **< 768px (mobile)** | Hidden behind hamburger, slides as overlay, auto-close on selection |

Implementation:
```python
# In CSS injection:
st.markdown("""
<style>
    /* Ensure sidebar is wide enough for price data */
    section[data-testid="stSidebar"] {
        min-width: 240px !important;
        width: 280px !important;
    }
    
    /* Compact button styling for sidebar stock rows */
    section[data-testid="stSidebar"] .stButton > button {
        text-align: left;
        padding: 0.3rem 0.5rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)
```

### 4.4 State Management

```python
# Session state initialization (in main.py, after set_page_config):
def _init_sidebar_state():
    """Initialize sidebar-related session state."""
    defaults = {
        "sidebar_collapsed": False,
        "sidebar_watchlist_expanded": True,   # Watchlist expanded by default
        "sidebar_hot_stocks_expanded": False,  # Hot stocks collapsed by default
        "sidebar_hot_etfs_expanded": False,    # Hot ETFs collapsed by default
        "sidebar_last_refresh": 0,             # Timestamp of last price fetch
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

_init_sidebar_state()
```

### 4.5 Updated main.py Structure

```python
# src/main.py — new structure

st.set_page_config(
    page_title="股識 Stock Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",  # CHANGED: was "auto"
)

# ... CSS injection (unchanged) ...

# ... sync_url_to_session() (unchanged) ...

# ... get_client() (unchanged) ...

# ... rate limit warning (unchanged) ...

# ── NEW: Initialize sidebar state ──────────────────────────
_init_sidebar_state()

# ── NEW: Render sidebar via dedicated module ──────────────
from src.services.sidebar_render import render_sidebar
search_input = render_sidebar(client)

# ── Search handling (moved from inline to function) ───────
stock_id = _handle_search(client, search_input)

# ── Main content (unchanged) ──────────────────────────────
if not st.session_state.get("sidebar_collapsed"):
    if not stock_id:
        _render_welcome_page()
    else:
        load_and_render_page(client, stock_id)
else:
    # Sidebar collapsed — show expand button + main content
    if st.button("☰ 展開側邊欄", key="expand_sidebar"):
        st.session_state["sidebar_collapsed"] = False
        st.rerun()
    if stock_id:
        load_and_render_page(client, stock_id)
```

---

## 5. Implementation Plan

### Phase 1: Bug Fix (Immediate)

1. Change `initial_sidebar_state="auto"` → `"expanded"` in `main.py` line 22
2. Add expand button in main content area for collapsed state
3. Add CSS to ensure collapse toggle is always visible

### Phase 2: Architecture Refactor

1. Create `src/services/sidebar_price_cache.py` — price caching service
2. Create `src/services/sidebar_render.py` — sidebar rendering module
3. Move hot stock/ETF definitions from `main.py` to `sidebar_render.py`
4. Refactor `main.py` to call `render_sidebar(client)` instead of inline code

### Phase 3: Inline Price Data

1. Implement `fetch_prices_batch()` with session-state TTL cache
2. Implement `_render_price_row()` with color-coded price display
3. Add `st.expander` sections for Watchlist, Hot Stocks, Hot ETFs
4. Add Market Overview section at bottom

### Phase 4: Polish

1. Add empty state messages ("尚未加入關注標的")
2. Add loading spinners for price fetches
3. Add error handling (show "—" on API failure)
4. Add responsive CSS for sidebar width
5. Add price flash animation (green/red on update)

---

## 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| FinMind rate limits hit by sidebar price fetches | API blocked for all users | TTL cache (5min), batch fetching, graceful degradation to "—" |
| Sidebar rerun slows down main content | Perceived slowness | Cache-first approach, sidebar renders before main content |
| `st.expander` doesn't support `expanded` parameter in older Streamlit | Collapse state not controllable | Check Streamlit version; use `st.session_state` workaround if needed |
| Price data stale during volatile market | Misleading prices | Show "last updated" timestamp, shorter TTL during market hours |
| Sidebar too wide for small screens | Layout breakage | CSS `min-width: 240px`, responsive breakpoints |

---

## 7. File Changes Summary

| File | Change |
|------|--------|
| `src/main.py` | Change `initial_sidebar_state` to `"expanded"`, extract sidebar to module, add expand button |
| `src/services/sidebar_render.py` | **NEW** — sidebar rendering logic |
| `src/services/sidebar_price_cache.py` | **NEW** — price caching service |
| `src/services/watchlist.py` | No changes needed (already has `load_watchlist()`) |
| `src/pages/router.py` | No changes needed |
| `src/pages/url_sync.py` | No changes needed |

---

*This document is a proposal. Implementation should follow the phased plan above. Phase 1 (bug fix) can be done immediately. Phases 2–4 should be delegated to a Developer sub-agent.*
