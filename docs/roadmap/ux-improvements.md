# UX Improvement Roadmap

> **Source**: `docs/decisions/ux_improvements.md` (2026-06-08)
> **Status**: Pending implementation | **Priority**: P0-P2

---

## P0 — Fix Immediately (Crash / Critical Bug)

| ID | Issue | Description | Affected Files |
|----|-------|-------------|----------------|
| UX-08 | DuplicateWidgetID crash | Event dashboard button key duplication causes page crash | `event_dashboard.py` |

**Fix**: Use `enumerate` index to ensure key uniqueness: `f"evt_{stock_id}_{idx}"`

---

## P1 — Sprint 1 (Low effort, high impact)

| ID | Issue | Description | Affected Files |
|----|-------|-------------|----------------|
| UX-05 | ROE annualization inaccurate | Seasonal industries using `*4` annualization is distorted, switch to TTM | `financial_health.py`, `peer_comparison.py` |
| UX-07 | No visual feedback for watchlist | No toast notification after adding/removing from watchlist | `business_card.py`, `watchlist_page.py` |
| UX-11 | Cache never cleaned | `.cache/` directory grows indefinitely | `finmind_client.py` |
| UX-14 | Concurrent watchlist writes | Multiple sessions writing to watchlist.yaml simultaneously may corrupt it | `watchlist.py` |

---

## P2 — Sprint 2 (Medium effort, core UX)

| ID | Issue | Description | Affected Files |
|----|-------|-------------|----------------|
| UX-01 | No Chinese search support | Search box only matches stock_id, can't search by Chinese name | `main.py`, `finmind_client.py` |
| UX-02 | No loading indicator on page switch | Blank screen with no spinner when switching pages | `router.py`, `_router_base.py` |
| UX-04 | Single-period chart empty | Chart is blank when data is insufficient, should degrade gracefully | `chart.py` |
| UX-06 | No peer comparison fallback | Shows dead page when no benchmark company, should auto-select largest in same industry | `peer_comparison.py` |
| UX-09 | Timeline filter fails silently | No error message when filter_by_timeline encounters an exception | `_router_base.py` |
| UX-13 | Insufficient dark mode contrast | Plotly chart labels unreadable in dark mode | `chart.py` |

---

## P3 — Sprint 3 (High effort, architectural)

| ID | Issue | Description | Affected Files |
|----|-------|-------------|----------------|
| UX-03 | Browser back button | Use `st.query_params` to sync URL | `main.py`, `router.py`, all pages |
| UX-10 | No API rate limit warning | No rate limit notification when switching stocks rapidly | `finmind_client.py`, `_router_base.py` |
| UX-12 | Small screen layout broken | 6-column layout is cramped on narrow screens | `router.py`, `category_browser.py`, `etf_browser.py` |

---

## Sidebar Improvement Items

> **Source**: `docs/decisions/sidebar_gap_analysis.md` + `docs/decisions/sidebar_research.md`

### P0 — Sidebar Bug

| ID | Issue | Description |
|----|-------|-------------|
| SB-04 | Sidebar cannot be expanded after collapsing | `initial_sidebar_state="auto"` causes this |

### P1 — Sidebar Core Features

| ID | Issue | Description |
|----|-------|-------------|
| SB-01 | Watchlist has no inline data | Sidebar should directly display price, change |
| SB-02 | Cannot manage multiple lists | Currently only one "My Watchlist" |
| SB-03 | No market overview | Bottom of sidebar should display market indices |
| SB-05 | Category browser entry | Sidebar lacks category browser shortcut |
| SB-06 | Recently viewed history | Cannot quickly return to previously viewed stocks |
| SB-07 | Sidebar width adjustable | Fixed width is not friendly to different screens |
| SB-08 | Icon + label navigation | Currently only text buttons, lacks visual hierarchy |

### P2 — Sidebar Bonus Features

| ID | Issue | Description |
|----|-------|-------------|
| SB-09 | Hover preview | Hovering over stock shows mini chart tooltip |
| SB-10 | Drag-and-drop sorting | Watchlist items can be reordered by dragging |
| SB-11 | Right-click menu | Right-click stock to add alert, remove, etc. |
| SB-12 | Notification badge | Red dot when event dashboard has new events |
| SB-13 | Data update time | Display last update time |

---

## Design Review Fixes

> **Source**: `docs/decisions/design_comparison_review.md` + `design_comparison_review_round5.md`

### Color System Violations

| ID | Issue | Affected Files |
|----|-------|----------------|
| DC-006 | Uses `#F39C12` (non-system color) | `financial_health.py` |
| DC-013 | Uses `#2E86C1`/`#1B4F72`/`#8E44AD` (non-system colors) | `etf_browser.py`, `watchlist_page.py` |
| DC-chart | Plotly charts use non-system colors | `chart.py` |

### Component Inconsistencies

| ID | Issue | Affected Files |
|----|-------|----------------|
| DC-001 | Watchlist button placed in Zone A | `business_card.py` |
| DC-004 | Custom gradient not using shared component | `operation_checkup.py` |
| DC-009 | Custom health assessment card | `financial_health.py` |
| DC-011 | Uses `st.metric()` instead of `_plain_card()` | `peer_comparison.py` |
| DC-025 | Raw flexbox HTML instead of `_plain_card()` | `watchlist_page.py` |
| DC-027 | Custom gradient banner | `event_dashboard.py` |
| DC-028 | Inline HTML hardcoded border color | `watchlist_page.py` |

### Layout Issues

| ID | Issue | Affected Files |
|----|-------|----------------|
| DC-003 | `_info_card()` text too long | `operation_checkup.py` |
| DC-007 | Financial health page has too much text | `financial_health.py` |
| DC-008 | Chart ratio less than 60% | `financial_health.py` |
| DC-010 | Peer comparison analysis text too long | `peer_comparison.py` |
| DC-015 | 6-column ETF layout | `etf_browser.py` |
| DC-019 | 6-column category layout | `category_browser.py` |
| DC-020 | `label_visibility="collapsed"` accessibility issue | `category_browser.py` |
| DC-022 | Severity badge has only emoji, no text | `event_dashboard.py` |
