# P2-1: Browser Back Button Doesn't Work — Design Document

**Date:** 2026-06-09  
**Status:** Design Complete  
**Priority:** P2  
**Streamlit version:** >=1.58.0 (supports `st.query_params` since 1.30)

---

## Problem Statement

The app uses `session_state['page']` and `session_state['stock_id']` for in-app navigation. When users click browser back/forward buttons, the URL doesn't change so the browser has nothing to navigate back to. Bookmarks also lose context since the URL is always the same.

## Root Cause

All navigation is done via `st.session_state` mutations + `st.rerun()`. The browser URL is never modified, so:
1. No browser history entries are created
2. Back/forward buttons have no effect
3. Bookmarking the page loses all context (which stock, which tab)

## Solution: Sync `session_state` with `st.query_params`

### Core Idea

Create a bidirectional sync between `session_state['page']` / `session_state['stock_id']` and URL query parameters (`?page=名片&stock_id=2330`). This makes every navigation state a distinct URL, enabling browser history, back/forward, and bookmarking.

### Query Parameter Mapping

| session_state key | URL param | Example | Valid values |
|---|---|---|---|
| `page` | `page` | `?page=名片` | One of the 9 page names (see below) |
| `stock_id` | `stock_id` | `?stock_id=2330` | Any 4-digit stock code or ETF code |

**Valid page names:** `名片`, `營運健檢`, `財務體質`, `同業比較`, `集團架構`, `分類瀏覽`, `ETF 專區`, `我的關注`, `事件儀表板`

---

## Architecture

### Two-phase approach: URL → session_state (on load), session_state → URL (on navigate)

```
┌─────────────────────────────────────────────────────┐
│  Phase 1: URL → session_state (at top of main.py)   │
│  Read st.query_params, write to session_state       │
│  (handles: direct URL access, back/forward, refresh)│
├─────────────────────────────────────────────────────┤
│  Phase 2: session_state → URL (on navigation)       │
│  After any session_state['page']/['stock_id'] change│
│  write to st.query_params before st.rerun()         │
│  (handles: in-app button clicks)                    │
└─────────────────────────────────────────────────────┘
```

### Key Principle: URL is the source of truth on page load

When Streamlit reruns (including browser back/forward), Phase 1 reads the URL and syncs to session_state. This means:
- Direct URL access: `?page=名片&stock_id=2330` → shows TSMC business card
- Back button: browser restores previous URL → Phase 1 reads it → app renders correct state
- Bookmark: saved URL → Phase 1 reads it → app renders correct state

---

## Changes Required

### File 1: NEW — `src/pages/url_sync.py`

A small utility module that handles all URL↔session_state synchronization logic.

```python
"""
URL ↔ session_state synchronization for browser back/forward support.
Uses st.query_params (Streamlit >=1.30) to keep URL in sync with page state.
"""

import streamlit as st

# Canonical list of valid page names
VALID_PAGES = frozenset({
    "名片", "營運健檢", "財務體質", "同業比較", "集團架構",
    "分類瀏覽", "ETF 專區", "我的關注", "事件儀表板",
})

DEFAULT_PAGE = "名片"


def sync_url_to_session() -> None:
    """
    Phase 1: Read URL query params and sync to session_state.
    Called once at the top of main.py, BEFORE any rendering.
    
    Priority:
      1. URL params (source of truth) — handles back/forward, direct URL, bookmarks
      2. Existing session_state — handles in-app navigation that hasn't hit URL yet
      3. Defaults — first visit with no URL params and no session_state
    
    Also handles validation: invalid page/stock_id in URL falls back gracefully.
    """
    # --- Page sync ---
    url_page = st.query_params.get("page")
    if url_page is not None:
        if url_page in VALID_PAGES:
            st.session_state["page"] = url_page
        else:
            # Invalid page in URL → fall back to default, fix URL
            st.session_state["page"] = DEFAULT_PAGE
            st.query_params["page"] = DEFAULT_PAGE
    # If no URL param, session_state keeps its current value (if any)
    elif "page" not in st.session_state:
        st.session_state["page"] = DEFAULT_PAGE

    # --- Stock ID sync ---
    url_stock_id = st.query_params.get("stock_id")
    if url_stock_id is not None:
        # Basic validation: non-empty string
        if url_stock_id.strip():
            st.session_state["stock_id"] = url_stock_id.strip()
        else:
            # Empty stock_id in URL → remove it
            del st.query_params["stock_id"]
    # If no URL param and no session_state, that's fine (shows welcome page)

    # --- Reverse sync: make sure URL reflects current state ---
    # This handles the case where session_state was set by in-app navigation
    # but URL hasn't been updated yet (e.g., on the NEXT rerun after a button click)
    _sync_session_to_url()


def _sync_session_to_url() -> None:
    """
    Phase 2: Write current session_state to URL query params.
    Called internally by sync_url_to_session, and also by navigate_to().
    """
    page = st.session_state.get("page", DEFAULT_PAGE)
    st.query_params["page"] = page

    stock_id = st.session_state.get("stock_id")
    if stock_id:
        st.query_params["stock_id"] = stock_id
    elif "stock_id" in st.query_params:
        del st.query_params["stock_id"]


def navigate_to(page: str = None, stock_id: str = None) -> None:
    """
    Navigation helper: update session_state + URL + trigger rerun.
    Use this INSTEAD of manual session_state assignment + st.rerun().
    
    Examples:
        # Switch to 財務體質 tab (same stock)
        navigate_to(page="財務體質")
        
        # View a different stock's 名片 page
        navigate_to(page="名片", stock_id="2317")
        
        # View a stock, keeping current page
        navigate_to(stock_id="2454")
    """
    if page is not None:
        if page not in VALID_PAGES:
            raise ValueError(f"Invalid page: {page!r}. Must be one of {sorted(VALID_PAGES)}")
        st.session_state["page"] = page

    if stock_id is not None:
        st.session_state["stock_id"] = stock_id

    # Sync to URL before rerun
    _sync_session_to_url()
    st.rerun()
```

### File 2: MODIFY — `src/main.py`

Add the sync call at the top of the main flow (after `set_page_config` and CSS, before sidebar).

**Lines 60-61 area — add url_sync import and call:**

```python
# ── 初始化 ────────────────────────────────────────────
from src.pages.url_sync import sync_url_to_session, navigate_to

# Sync URL ↔ session_state (browser back/forward support)
sync_url_to_session()
```

**Replace all manual `st.session_state["page"] = ...` + `st.rerun()` patterns:**

| Line | Before | After |
|------|--------|-------|
| 107-109 | `st.session_state["stock_id"] = sid`<br>`st.session_state["page"] = "名片"`<br>`st.rerun()` | `navigate_to(page="名片", stock_id=sid)` |
| 124-126 | `st.session_state["stock_id"] = sid`<br>`st.session_state["page"] = "名片"`<br>`st.rerun()` | `navigate_to(page="名片", stock_id=sid)` |
| 131-132 | `st.session_state["page"] = "我的關注"`<br>`st.rerun()` | `navigate_to(page="我的關注")` |
| 136-137 | `st.session_state["page"] = "事件儀表板"`<br>`st.rerun()` | `navigate_to(page="事件儀表板")` |

### File 3: MODIFY — `src/pages/router.py`

**Replace navbar button handler (line 154-156):**

```python
# Before:
if st.button(p, key=f"nav_{p}", use_container_width=True):
    st.session_state["page"] = p
    st.rerun()

# After:
from src.pages.url_sync import navigate_to
if st.button(p, key=f"nav_{p}", use_container_width=True):
    navigate_to(page=p)
```

**Import at top of router.py:**
```python
from src.pages.url_sync import navigate_to
```

### File 4: MODIFY — `src/pages/category_browser.py` (3 locations)

All instances of the pattern:
```python
st.session_state["stock_id"] = row["stock_id"]
st.session_state["page"] = "名片"
st.rerun()
```
Replace with:
```python
from src.pages.url_sync import navigate_to
navigate_to(page="名片", stock_id=row["stock_id"])
```

Lines: ~112-113, ~189-191, ~251-253

### File 5: MODIFY — `src/pages/etf_browser.py` (3 locations)

Same pattern as category_browser. Lines: ~174-176, ~334-336, ~454-456

### File 6: MODIFY — `src/pages/watchlist_page.py` (1 location)

Line ~180-182:
```python
# Before:
st.session_state["stock_id"] = stock_id
st.session_state["page"] = "名片"
st.rerun()

# After:
from src.pages.url_sync import navigate_to
navigate_to(page="名片", stock_id=stock_id)
```

### File 7: MODIFY — `src/pages/event_dashboard.py` (1 location)

Lines ~91-93:
```python
# Before:
st.session_state["stock_id"] = stock_id
st.session_state["page"] = "名片"
st.rerun()

# After:
from src.pages.url_sync import navigate_to
navigate_to(page="名片", stock_id=stock_id)
```

---

## Edge Cases & Handling

| Edge Case | Behavior |
|-----------|----------|
| **Direct URL access** (`?page=財務體質&stock_id=2330`) | Phase 1 reads URL params → sets session_state → app renders TSMC 財務體質 page |
| **Invalid page in URL** (`?page=FOO`) | Falls back to `DEFAULT_PAGE` ("名片"), URL is corrected |
| **Invalid/unknown stock_id** (`?stock_id=9999`) | URL is accepted → session_state set → router calls `get_stock_data()` → returns `None` → `st.error("找不到股票代號 9999")` (existing error path) |
| **Missing page param with stock_id** (`?stock_id=2330`) | `page` defaults to `"名片"` → shows business card |
| **Missing stock_id with page** (`?page=分類瀏覽`) | Works fine — 分類瀏覽 doesn't need a stock_id |
| **Missing all params** (bare URL `/`) | Shows welcome page (no stock_id in session_state or URL) |
| **Browser back from 2330 名片 to 2317 營運健檢** | Browser restores URL `?page=營運健檢&stock_id=2317` → Phase 1 syncs → renders correctly |
| **Refresh/F5** | URL params persist → Phase 1 reads them → same page re-rendered |
| **Emoji/Unicode in URL** | `st.query_params` handles URL encoding/decoding transparently |

---

## What Does NOT Change

1. **`_router_base.py`** — Pure utility functions, no navigation logic
2. **`session_state` is still the runtime source** — The URL is synced to session_state on load; rendering logic still reads `session_state['page']` as before
3. **Pages that only call `st.rerun()` without changing page/stock_id** — e.g., watchlist add/remove (lines 184-187 of watchlist_page.py) — These don't need `navigate_to()` since they're not navigation actions
4. **`business_card.py` watch/rerun lines 51, 59** — These are toggle actions on the current page, not navigation; no change needed

---

## Risks & Trade-offs

### Low Risk
- **Streamlit version**: `st.query_params` is available since 1.30, and the project requires >=1.58 ✅
- **Backward compatibility**: The `sync_url_to_session()` function reads URL params but falls back to session_state if no URL params exist. Existing flows work unchanged.
- **Direct URL with bad stock_id**: Already handled by existing error path in router.py (line 83-85)

### Medium Risk
- **URL-encoded Chinese characters**: Page names like `名片` will appear as `%E5%90%8D%E7%89%87` in the browser URL bar. This is functional but not human-readable. **Mitigation**: Could add an optional English alias mapping (`?page=business-card`) but this adds complexity. Recommend shipping with Chinese params first; English aliases can be added later.
- **Multiple rapid navigations**: Streamlit's rerun model means rapid back/forward clicks may queue reruns. This is an existing Streamlit characteristic, not introduced by this change.

### Low Risk but Worth Noting
- **`st.query_params` dict-like behavior**: Setting `st.query_params["page"] = "名片"` immediately updates the URL. No `st.rerun()` is needed for the URL change itself — the URL updates on the next rerun. Our `_sync_session_to_url()` sets params before `st.rerun()`, which is the correct order.
- **Search input interaction**: When a user types in the search box and gets a stock_id, that goes through `stock_id = query` path (main.py line 158), NOT through `navigate_to()`. This is fine because `sync_url_to_session()` runs at the top and `_sync_session_to_url()` is called in Phase 1, which will sync the resulting stock_id to URL after session_state is set.

---

## Testing Plan

1. **Manual tests:**
   - Click `2330 台積電` in sidebar → URL should show `?page=名片&stock_id=2330`
   - Click `財務體質` tab → URL should change to `?page=財務體質&stock_id=2330`
   - Click browser back → should return to `?page=名片&stock_id=2330` and show business card
   - Click browser forward → should return to `?page=財務體質&stock_id=2330`
   - Open `?page=同業比較&stock_id=2454` in new tab → should show 聯發科 peer comparison
   - Bookmark a page → refresh bookmark → same page loads
   - Open `?page=INVALID` → falls back to 名片 page

2. **Automated test** (Layer 1 AppTest):
   ```python
   def test_url_params_sync():
       app = AppTest.from_file("src/main.py")
       # Simulate URL with params
       app.query_params = {"page": "名片", "stock_id": "2330"}
       app.run()
       assert app.session_state["page"] == "名片"
       assert app.session_state["stock_id"] == "2330"
   ```

---

## Implementation Order

1. Create `src/pages/url_sync.py` with `sync_url_to_session()` and `navigate_to()`
2. Modify `src/main.py` — add sync call + replace 4 nav patterns
3. Modify `src/pages/router.py` — replace navbar button handler
4. Modify `src/pages/category_browser.py` — replace 3 patterns
5. Modify `src/pages/etf_browser.py` — replace 3 patterns
6. Modify `src/pages/watchlist_page.py` — replace 1 pattern
7. Modify `src/pages/event_dashboard.py` — replace 1 pattern
8. Test manually in browser
9. Run Layer 0 + Layer 1 verification

**Estimated effort:** ~30 minutes for implementation + testing
