# Stock Explorer Comprehensive Problem Analysis Report

After reviewing the architecture, data flow, and UI implementation across three rounds of cross-checking, we identified several issues that could seriously affect stability, performance, and scalability. The issues are grouped into the review dimensions below:

> **2026-06-08 Update**: Daniel's manual testing uncovered 14 UI/UX issues, documented in the "Layer 4: UI/UX Experience" section.

## Layer 1: Data Flow & Architecture

1. **API Abuse and Cache Design Flaws in `get_stock_info`**
   - **Problem**: `FinMindClient.get_stock_info(stock_id)` internally calls `taiwan_stock_info()` to fetch the entire list of Taiwanese stocks, and only then filters it by `stock_id`. However, the cache key is generated based on the `stock_id`. This means that if 50 different stocks are queried, the program will send 50 requests to the FinMind API for the full stock list. This extremely wastes bandwidth and easily triggers FinMind's rate limit.
   - **Impact**: A severe performance bottleneck; querying multiple stocks will inevitably cause lag or get blocked.
2. **Daily Cache Invalidation and Missing Cleanup Mechanism**
   - **Problem**: When `FinMindClient._fetch_or_cache` calls the API, the `end_date` parameter defaults to `datetime.now().strftime("%Y-%m-%d")`. This causes the cache's hash key to change every day (after midnight), rendering the configured `cache_ttl_hours` completely useless. Furthermore, old JSON cache files are never deleted.
   - **Impact**: A guaranteed daily cache miss, and the `.cache/` directory size will expand indefinitely.
3. **Ineffective Name Search Support**
   - **Problem**: The sidebar search box explicitly suggests "Example: 2330 or TSMC", but the underlying filtering logic in `FinMindClient` is only searching by `stock_id`, completely lacking support for exact or fuzzy matching on the `stock_name` column.
   - **Impact**: If a user inputs a Chinese stock name, they will always receive a "Stock ID not found" error message.

## Layer 2: Business Logic & UI/UX

1. **Streamlit Widget Key Conflict Risk (`event_dashboard.py`)**
   - **Problem**: The keys generated for buttons in the event dashboard use the format `key=f"evt_{stock_id}_{title[:20]}"`. If a single company has two news articles with the same first 20 characters in their titles on the same day, or triggers two identical events, it will raise a `DuplicateWidgetID` error.
   - **Impact**: Once triggered, this will directly cause the entire page to crash.
2. **Failed ETF Determination Logic (`watchlist.py`)**
   - **Problem**: The `_is_etf(stock_id, name)` function is called inside `add_to_watchlist`, but the most critical third parameter, `industry_category`, is not passed. This prevents the highest-priority exact matching mechanism from executing, forcing it to fall back on less reliable name-based heuristic matching and stock ID prefix matching.
   - **Impact**: This easily leads to certain ETFs being misclassified as regular stocks, directing them to the wrong analysis framework.
3. **Unhandled API Rate Limit Edge Cases**
   - **Problem**: If the FinMind API rate limit is reached, it returns an empty DataFrame or throws an exception. The current program uniformly treats these scenarios as "No data found" or "Stock not found", without providing the user with a clear "API rate limit exceeded" warning.
   - **Impact**: Increases debugging difficulty and results in a poor user experience.
4. **Crude Annualization of Financial Indicators like ROE (`financial_health.py`)**
   - **Problem**: In `_calc_roe`, the quarterly net income is simply multiplied by 4 (`net_income * 4 / equity * 100`). This can cause extremely misleading results for companies with high seasonal variances.
   - **Impact**: Causes the financial data presentation to lose professionalism and easily leads to misestimation.

## Layer 3: Concurrency & Robustness

1. **Race Condition Risks in YAML Config Files (`watchlist.py` / `adaptive_engine.py`)**
   - **Problem**: Reading and writing the watchlist (`watchlist.yaml`) and event records (`events.yaml`) both use a "read entire list → modify memory array → overwrite entire file" pattern. Streamlit allows concurrent operations from multiple users (multi-session). If two users add to the watchlist simultaneously, or if a background event detection triggers concurrently, race conditions will occur, causing data loss or YAML file corruption.
   - **Impact**: A fatal risk under high-frequency access, leading to the collapse of the storage system.
2. **Event Detection Relies on Fragile Data Field Access**
   - **Problem**: Methods like `detect_revenue_event` access arrays and dictionaries directly (e.g., `latest["revenue"]`). If FinMind changes its return fields, or if there are fewer than 13 records but another bug somehow leads execution to this logic block, it will raise a `KeyError` or `IndexError`.
   - **Impact**: The background analysis engine halts randomly, failing to generate event alerts.
3. **Silent Failures in the Timeline Filter (`_router_base.py`)**
   - **Problem**: If `filter_by_timeline` encounters formatting anomalies (Exceptions) during time conversion or comparison, it directly returns the original DataFrame (ALL).
   - **Impact**: When users click the 1Y or 3Y filters, the charts won't respond, and no error message is provided, making users mistakenly think the system is lagging.

## Layer 4: UI/UX Experience (Daniel's Manual Testing)

> Recorded on 2026-06-08 after Daniel's hands-on manual testing of the application.

| # | Category | Issue | Severity |
|---|----------|-------|----------|
| 1 | Navigation | Sidebar search does not support Chinese stock names — typing "台積電" always returns "Stock ID not found" | High |
| 2 | Navigation | No loading indicator when switching pages — users cannot tell if the app is processing or frozen | Medium |
| 3 | Navigation | Browser back button does not work with Streamlit page navigation | Medium |
| 4 | Data Display | Financial charts show no data points when only a single period is available — the chart appears empty | High |
| 5 | Data Display | ROE annualization produces wildly inaccurate values for seasonal businesses (e.g., retail, semiconductors) | High |
| 6 | Data Display | Peer comparison page shows "No data" for stocks outside the top tier without explanation | Medium |
| 7 | Interaction | Watchlist add/remove does not provide visual feedback — no toast or confirmation message | Medium |
| 8 | Interaction | Event dashboard buttons can crash the page when duplicate titles exist (DuplicateWidgetID) | Critical |
| 9 | Interaction | Timeline filter (1Y, 3Y) silently fails — charts don't update and no error is shown | High |
| 10 | Performance | Switching between 5+ stocks in quick succession triggers FinMind rate limits with no user-facing warning | High |
| 11 | Performance | Cache never expires old files — `.cache/` directory grows without bound over time | Low |
| 12 | Visual Design | PPT-style layout breaks on smaller screens / narrow browser windows | Medium |
| 13 | Visual Design | Color contrast on chart labels is insufficient for readability in dark mode | Low |
| 14 | Robustness | Concurrent multi-user access to watchlist.yaml can cause data loss or file corruption | High |

---

## Layer 5: Design System Compliance (Round 2 — 2026-06-10)

> Recorded after Design Comparison Review of all page files against `docs/design/design_system.md`.

### Color System Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-006 | `financial_health.py` | 180 | Uses `#F39C12` (orange) for "moderate" debt ratio — orange NOT in design system palette | Medium |
| D-013 | `etf_browser.py` | 67 | Uses `#2E86C1` (dark blue) — not in design system | Medium |
| D-013 | `etf_browser.py` | 68 | Uses `#1B4F72` (navy) — not in design system | Medium |
| D-013 | `etf_browser.py` | 447 | Uses `#8E44AD` (purple) for dividend yield — not in design system | Medium |
| D-024 | `watchlist_page.py` | 123 | Uses `#2E86C1` (dark blue) — not in design system | Medium |
| D-024 | `watchlist_page.py` | 124 | Uses `#1B4F72` (navy) — not in design system | Medium |
| — | `chart.py` | 150,204 | Uses `#4A90D9`, `#2ECC71`, `#F39C12` — close to but not matching design system | Low |

### PPT Style Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-003 | `operation_checkup.py` | 62-70 | Trend messages likely exceed 200-char text limit | Medium |
| D-007 | `financial_health.py` | multiple | Heavy text content across 4 sections — significantly exceeds 200-char limit | High |
| D-008 | `financial_health.py` | — | Only 1 chart for 4 sections — chart proportion below 60% | Medium |
| D-010 | `peer_comparison.py` | 333-367 | Metric analysis text could reach 400+ chars with all metrics | Medium |

### Zone Separation Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-001 | `business_card.py` | 56-72 | Watchlist buttons in navbar (Zone A) — interactive controls should be in Zone C | Medium |

### Architecture Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-012 | `peer_comparison.py` | 51 | `@st.cache_data(ttl=3600)` in View layer — architecture forbids this | High |
| D-016 | `etf_browser.py` | 12, 18 | `@st.cache_data(ttl=3600)` in View layer — architecture forbids this | High |

### Component Consistency Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-004 | `operation_checkup.py` | 135-175 | Custom gradient card doesn't use `_info_card()` / `_白话_card()` | Low |
| D-009 | `financial_health.py` | 188-196 | Custom health card doesn't use shared components | Low |
| D-011 | `peer_comparison.py` | 92 | Uses `st.metric()` instead of `_白话_card()` | Low |
| D-025 | `watchlist_page.py` | 204-224 | Raw flexbox HTML card instead of `_白话_card()` | Low |

### Responsive Design Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-015 | `etf_browser.py` | 165, 437 | 6-column layout will break on narrow screens | Medium |
| D-019 | `category_browser.py` | 105 | 6-column layout will break on narrow screens | Medium |
| — | `main.py` | 58-68 | Media queries only adjust padding — column layouts still break | Medium |

### Accessibility Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-022 | `event_dashboard.py` | 21-26 | Severity badges use emoji without text alternatives | Medium |
| D-020 | `category_browser.py` | 141 | Hidden label on industry radio — screen reader inaccessible | High |
| — | `chart.py` | 30 | `#555555` chart text may fail WCAG AA on dark backgrounds | Medium |

---

## Layer 5: Design System Compliance (Round 3 — 2026-06-11)

> Recorded after Round 3 Design Comparison Review. Verification of Round 2 issues (2 fixed, 19 still present, 3 new found).

### P0 — CRITICAL

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-002-NEW | `business_card.py` | 128 | **Page severely truncated** — only 128 lines. Revenue chart, pie chart, news, dividend sections are imported but NEVER rendered. This is the MAIN page of the app. | **Critical** |

### Color System Violations (unchanged from Round 2)

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-006 | `financial_health.py` | 180 | Uses `#F39C12` (orange) for "moderate" debt ratio — orange NOT in design system palette | Medium |
| D-013 | `etf_browser.py` | 67 | Uses `#2E86C1` (dark blue) — not in design system | Medium |
| D-013 | `etf_browser.py` | 68 | Uses `#1B4F72` (navy) — not in design system | Medium |
| D-013 | `etf_browser.py` | 447 | Uses `#8E44AD` (purple) for dividend yield — not in design system | Medium |
| D-024 | `watchlist_page.py` | 123 | Uses `#2E86C1` (dark blue) — not in design system | Medium |
| D-024 | `watchlist_page.py` | 124 | Uses `#1B4F72` (navy) — not in design system | Medium |

### Custom Gradient Violations (NEW — not in design system)

| # | File | Lines | Issue | Severity |
|---|------|-------|-------|----------|
| D-004 | `operation_checkup.py` | 136, 169 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — custom gradient not in design system | Medium |
| D-027-NEW | `event_dashboard.py` | 141 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — adaptive banner uses custom gradient | Medium |
| — | `etf_browser.py` | 61 | `linear-gradient(135deg,#EBF5FB,#EAF2F8)` — ETF explanation card | Medium |
| — | `watchlist_page.py` | 122 | `linear-gradient(135deg,#EBF5FB,#EAF2F8)` — empty state card | Medium |
| — | `etf_detail.py` | 110 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — one-liner banner | Medium |

### PPT Style Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-003 | `operation_checkup.py` | 62-70 | Trend messages likely exceed 200-char text limit | Medium |
| D-007 | `financial_health.py` | multiple | Heavy text content across 4 sections — significantly exceeds 200-char limit | High |
| D-008 | `financial_health.py` | — | Only 1 chart for 4 sections — chart proportion below 60% | Medium |
| D-010 | `peer_comparison.py` | 333-367 | Metric analysis text could reach 400+ chars with all metrics | Medium |

### Zone Separation Violations

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-001 | `business_card.py` | 56-72 | Watchlist buttons in navbar (Zone A) — interactive controls should be in Zone C | Medium |

### Component Consistency Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-009 | `financial_health.py` | 188-196 | Custom health card doesn't use shared components | Low |
| D-011 | `peer_comparison.py` | 92 | Uses `st.metric()` instead of `_白话_card()` | Low |
| D-025 | `watchlist_page.py` | 204-224 | Raw flexbox HTML card instead of `_白话_card()` | Low |
| D-028-NEW | `watchlist_page.py` | 84-114 | Summary cards use inline HTML with hardcoded colors instead of shared components | Low |

### Responsive Design Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-015 | `etf_browser.py` | 165, 437 | 6-column layout will break on narrow screens | Medium |
| D-019 | `category_browser.py` | 105 | 6-column layout will break on narrow screens | Medium |
| — | `main.py` | 58-68 | Media queries only adjust padding — column layouts still break | Medium |

### Accessibility Issues

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-022 | `event_dashboard.py` | 21-26 | Severity badges use emoji without text alternatives | Medium |
| D-020 | `category_browser.py` | 141 | Hidden label on industry radio — screen reader inaccessible | High |
| — | `chart.py` | 30 | `#555555` chart text may fail WCAG AA on dark backgrounds | Medium |

### New Issues Found in Round 3

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-005-NEW | `_router_base.py` | 129-130 | `_section_title()` auto-prepends `📊` emoji — conflicts with pages that already have custom emoji prefixes (e.g., 🩺 becoming 📊 🩺 營運摘要) | Medium |
| D-027-NEW | `event_dashboard.py` | 141-152 | `_render_adaptive_banner` uses custom gradient HTML instead of standard card | Medium |
| D-028-NEW | `watchlist_page.py` | 84-114 | Summary cards use inline HTML with hardcoded `#E74C3C`/`#27AE60`/`#3498DB` border colors instead of shared `_白话_card()` component | Low |

### Chart Color Violations (chart.py)

| Line | Illegal Color | Should Be | Notes |
|------|---------------|-----------|-------|
| 150 | `#4A90D9` | `#3498DB` | Revenue bar chart |
| 159, 251, 401 | `#2ECC71` | `#27AE60` | Positive/increasing color |
| 204 | `#F39C12`, `#2ECC71` | `#3498DB`, `#27AE60` | OHLC single-day fallback colors |
| 315 | `#2ECC71`, `#F39C12` | `#27AE60`, `#3498DB` | Funnel chart stage colors |

### Fixes Since Round 2 ✅

| # | File | Line | Fix Applied |
|---|------|------|-------------|
| D-012 | `peer_comparison.py` | 51 | `@st.cache_data(ttl=3600)` removed from view layer |
| D-016 | `etf_browser.py` | 12, 18 | `@st.cache_data(ttl=3600)` replaced with module-level cache functions |

---

*Summary: The project functions smoothly under the "Happy Path", but when facing scalability, error handling, and concurrency, the underlying infrastructure (especially the cache algorithm and YAML persistence layer) is extremely fragile. Refactoring API access and implementing file locking mechanisms should be prioritized.*

*Design System Compliance (Round 3 — 2026-06-11): The app has good foundations in loading states, error handling, and zone separation. However, NO design issues were fixed between Round 2 and Round 3 (except 2 architecture violations). Critical new finding: business_card.py is severely truncated (128 lines) — the main content (revenue/news/dividend) is imported but never rendered. 3 new issues found: section title emoji conflict, gradient banners, inline summary cards. Overall PPT style grade: D+ (downgraded from B-).*
