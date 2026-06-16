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
|| D-007 | `financial_health.py` | multiple | ~~Heavy text content across 4 sections~~ ✅ FIXED 2026-06-12 (ISSUE-D05) | ~~High~~ Resolved |
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
|| D-007 | `financial_health.py` | multiple | ~~Heavy text content across 4 sections~~ ✅ FIXED 2026-06-12 (ISSUE-D05) | ~~High~~ Resolved |
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

---

## Layer 5: Design System Compliance (Round 4 — 2026-06-12)

> Recorded after Round 4 Design Comparison Review. 25 new issues found (D-029 through D-045). 2 previously identified issues confirmed fixed (D-012, D-016). Overall grade remains D+. 0 pages at A or B grade.

### P0 — CRITICAL

| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| D-029 | `business_card.py` | 128 | **Page STILL severely truncated.** Only header + watchlist UI rendered. Revenue chart, pie chart, news, dividend sections are imported but never called. The MAIN page of the app is a broken stub. Unchanged from Round 3. | **Critical** |

### Color System Violations — NEW (Round 4)

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-030 | `group_structure.py` | 239 | `#F39C12` (orange) | `#F39C12` is NOT in design system palette | "Important investment" badge label for 20–49% holdings |
| D-031 | `watchlist_page.py` | 169,171,197 | `#27AE60`/`#3498DB`/`#E74C3C` as inline badge colors | Acceptable colors but delivered as raw HTML, not shared component | Type badge and alert badge |
| D-032 | `etf_detail.py` | 110 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` | No gradients in design system | One-liner banner — duplicate of D-027 pattern |
| D-033 | `group_structure.py` | 202 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` | No gradients in design system | Group overview banner |
| D-034 | `peer_comparison.py` | 92 | `st.metric()` with Streamlit default styling | `_白话_card()` | Single-company fallback view |
| D-035 | `event_dashboard.py` | 145 | `#EBF5FB`, `#D4E6F1` in gradient | No gradients in design system | Adaptive banner |

### PPT Style Violations — NEW (Round 4)

| # | File | Line | Issue |
|---|------|------|-------|
| D-036 | `financial_health.py` | 70–73 | `_info_card` content for funnel analysis is ~280 Chinese chars — exceeds 200-char limit |
| D-037 | `financial_health.py` | 234–244 | Cash flow `_info_card` text blocks — 3 blocks total ~500 chars |
| D-038 | `group_structure.py` | 326–330 | Strategy `_info_card` text ~180 chars for closing sentence; overall page text exceeds 200 chars |
| D-039 | `watchlist_page.py` | 157–226 | Watchlist item card renders per-stock flexbox row — page is entirely table/list oriented, no chart |

### Zone Separation Violations — NEW (Round 4)

| # | File | Line | Issue |
|---|------|------|-------|
| D-040 | `business_card.py` | 95–128 | Watchlist popover management UI (text input, selectbox, create button) embedded in Zone A area |

### Component Consistency — NEW (Round 4)

| # | File | Line | Issue |
|---|------|------|-------|
| D-041 | `category_browser.py` | 170–181 | Stock cards in industry browser use raw HTML `<div>` with inline styles instead of `_白话_card()` |
| D-042 | `etf_browser.py` | 302–321 | ETF category cards use raw HTML with inline styles instead of `_白话_card()` |
| D-043 | `etf_browser.py` | 59–119 | ETF explainer card uses custom gradient HTML with illegal colors |
| D-044 | `etf_detail.py` | 183–188 | Dividend explanation raw HTML card instead of `_info_card()` |
| D-045 | `etf_detail.py` | 250–256 | Institution explanation raw HTML card instead of `_info_card()` |

### Fixes Since Round 3 ✅

| # | File | Line | Fix Applied |
|---|------|------|-------------|
| D-012 | `peer_comparison.py` | 51 | `@st.cache_data` removed from view layer |
| D-016 | `etf_browser.py` | 12, 18 | `@st.cache_data` replaced with module-level cache functions |

### Cumulative Issue Count

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 (2026-06-10) | 26 | 26 | 2 (D-012, D-016) |
| Round 3 (2026-06-11) | 3 new | 29 | 0 |
| Round 4 (2026-06-12) | 25 new | 54 | 0 |
| **Total** | **54** | **54** | **2** |

**Overall design grade: D+** (unchanged from Round 3 — 0 pages at A or B, 5 pages at D, 5 pages at C)

---

## Layer 5: Design System Compliance (Round 5 — 2026-06-12)

> Recorded after Round 5 Design Comparison Review. business_card.py P0 fix verified (370 lines restored). 17 new issues found (D-046 through D-062). 2 previously identified issues now fixed (D-002-NEW, D-029). Overall grade improved to C-.

### P0 — FIXED ✅

| # | File | Line | Issue | Status |
|---|------|------|-------|--------|
| D-002-NEW | `business_card.py` | 128→370 | Page was severely truncated (128 lines). Now fully restored. | ✅ FIXED |
| D-029 | `business_card.py` | 128→370 | Page STILL severely truncated — unchanged from Round 3. Now resolved. | ✅ FIXED |

### Color System Violations — NEW (Round 5)

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-046 | `business_card.py` | 136 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` | Flat `#EBF5FB` — no gradients in design system | One-liner banner |
| D-050 | `group_structure.py` | 245 | `#ECF0F1` (border) | Not in design system palette | Subsidiary card border |
| D-053 | `chart.py` | 315 | `#2ECC71`, `#F39C12` in funnel | `#27AE60`, `#3498DB` | Funnel chart stage colors |
| D-054 | `chart.py` | 150 | `#4A90D9` | `#3498DB` | Revenue bar chart |
| D-055 | `chart.py` | 159 | `#2ECC71` | `#27AE60` | Revenue YoY positive color |
| D-056 | `chart.py` | 204 | `#F39C12`, `#2ECC71` | `#3498DB`, `#27AE60` | OHLC single-day fallback |
| D-058 | `chart.py` | 401 | `#2ECC71` | `#27AE60` | Institutional chart positive |
| D-059 | `_router_base.py` | 145 | `#F39C12` (orange) border | `#3498DB` — orange NOT in palette | `_info_card()` shared component — affects ALL pages |
| D-061 | `main.py` | 49-56 | `#7D6608` text, `#F9E79F` border | `#2C3E50` text — other colors not in palette | Disclaimer CSS class |

### PPT Style Violations — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| D-049 | `category_browser.py` | 38-49 | Page has 3 unrelated sections (top stocks, industry browser, hot stocks) — violates "one key point per page" principle |

### Zone Separation Violations — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| — | — | — | No new zone violations in Round 5 |

### Component Consistency — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| D-047 | `business_card.py` | 317-324 | Revenue breakdown cards use `box-shadow` not in design system |
| D-048 | `category_browser.py` | 170-181 | Industry stock cards use raw HTML instead of `_白话_card()` |
| D-051 | `group_structure.py` | 202 | Group overview card uses `border-radius:16px` — design system specifies `12px` |
| D-052 | `group_structure.py` | 283 | Uses `st.bar_chart` (Streamlit native) instead of Plotly — violates chart rules |

### Responsive Design Issues — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| — | — | — | No new responsive issues in Round 5 (D-015, D-019 remain) |

### Accessibility Issues — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| — | — | — | No new accessibility issues in Round 5 (D-020, D-022 remain) |

### Architecture / CSS Issues — NEW (Round 5)

| # | File | Line | Issue |
|---|------|------|-------|
| D-057 | `chart.py` | 250-251 | Candlestick colors follow Taiwanese convention (red=up) but this is undocumented in design system — creates ambiguity with revenue chart where green=positive |
| D-060 | `main.py` | 262-270 | Welcome page uses `#95A5A6` text color not in design system palette |
| D-062 | `main.py` | 27-98 | No CSS custom properties (design tokens) — all values hardcoded. Modern best practice is `:root { --color-primary: #3498DB; }` |

### Fixes Since Round 4 ✅

| # | File | Line | Fix Applied |
|---|------|------|-------------|
| D-002-NEW | `business_card.py` | 128→370 | Page restored from 128 to 370 lines — all sections now render |
| D-029 | `business_card.py` | 128→370 | Truncation issue resolved by restoration |

### Cumulative Issue Count

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 (2026-06-10) | 26 | 26 | 2 (D-012, D-016) |
| Round 3 (2026-06-11) | 3 new | 29 | 0 |
| Round 4 (2026-06-12) | 25 new | 54 | 0 |
| Round 5 (2026-06-12) | 17 new | 71 | 2 (D-002-NEW, D-029) |
| **Total** | **71** | **71** | **2** |

|| Round 5 (2026-06-12) | 17 new | 71 | 2 (D-002-NEW, D-029) |
|| **Round 6 (2026-06-12)** | **10 new** | **81** | **1 (D-059)** |
|| **Total** | **81** | **81** | **3** |

**Overall design grade: C** (upgraded from C- — D-059 `_info_card()` border fixed, business_card.py confirmed at B, chart.py cleaner than expected)

---

## Layer 5: Design System Compliance (Round 6 — 2026-06-12)

> Recorded after Round 6 Design Comparison Review. 10 new issues found (D-063 through D-072). 1 previously identified issue confirmed fixed (D-059). Overall grade improved to C.

### Color System Violations — NEW (Round 6)

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-063 | `business_card.py` | 137 | `linear-gradient(135deg,#EBF5FB,#D4E6F1)` | Flat color — no gradients | One-liner banner |
| D-064 | `business_card.py` | 153 | `#F0F7FF` | Not in palette | Company facts card background |
| D-065 | `business_card.py` | 307 | `#BDC3C7` | Not in palette | "No dividend" border |
| D-066 | `business_card.py` | 340, 375 | `#5D6D7E` | `#7F8C8D` | Revenue item + news summary text |
| D-067 | `business_card.py` | 376 | `#95A5A6` | Not in palette | News source/date text |
| D-068 | `business_card.py` | 384 | `#F9E79F`/`#7D6608` | Not in palette | Disclaimer section |
| D-069 | `chart.py` | 30 | `#555555` | `#7F8C8D` | Axis label text |
| D-070 | `chart.py` | 31 | `#333333` | `#2C3E50` | Chart titles |
| D-071 | `chart.py` | 96 | `px.colors.qualitative.Set3` | Explicit palette colors | Pie chart arbitrary colors |

### Component Consistency — NEW (Round 6)

| # | File | Line | Issue |
|---|------|------|-------|
| D-005 | `_router_base.py` | 129-130 | `_section_title()` auto-prepends 📊 — emoji prefix conflict |
| D-072 | `_router_base.py` | 147 | `#5D6D7E` in `_info_card()` content — not in palette |

### Fixes Since Round 5 ✅

| # | File | Line | Fix Applied |
|---|------|------|-------------|
| D-059 | `_router_base.py` | 145 | `_info_card()` border changed from `#F39C12` to `#3498DB` — **FIXED** |

### Page Grades (Round 6)

| Page | Grade | Change | Notes |
|------|-------|--------|-------|
| business_card.py | B | ← No change | 388 lines, all services called, 6 minor color violations |
| chart.py | B+ | ← No change | Major colors correct, 3 minor violations |
| _router_base.py | B+ | ← Upgraded from C+ | D-059 border fix confirmed |
| event_dashboard.py | A- | ← No change | Best-graded page |
| financial_health.py | C+ | ← No change | DR-03 fix integrated |
| category_browser.py | D | ← No change | Structural issues remain |
| group_structure.py | D | ← No change | Structural issues remain |

### Top 5 Recommended Fixes (Round 6)

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 1 | D-005: Fix `_section_title()` emoji conflict | 15 min | Affects all pages |
| 2 | D-069+D-070: Fix chart.py theme colors | 15 min | Affects all charts globally |
| 3 | D-071: Replace Set3 palette in pie charts | 30 min | Affects all pie charts |
| 4 | D-063: Remove gradient from business_card.py | 10 min | Single element |
| 5 | D-072: Fix _info_card() content color | 5 min | Affects all info cards |

---

*Last updated: 2026-06-12 by PM after Round 6 design review.*

---

## Layer 5: Design System Compliance (Round 7 — 2026-06-13)

> Recorded after Round 7 Design Comparison Review. Verified all previous issues against source code. 0 new color violations from the old palette (F39C12, 2E86C1, 1B4F72, 8E44AD, 2ECC71, 4A90D9 all confirmed cleaned). 0 linear-gradient instances remain. However, 11 new issues found: 8 non-palette colors (#5D6D7E, #F8F9FA, #FEF9E7, #F9E79F, #7D6608, #BDC3C7, #95A5A6), 1 component consistency (st.bar_chart), 1 emoji conflict, 1 Set3 palette. Overall grade: C+ (unchanged).

### Color System Violations — NEW (Round 7)

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-073 | `_router_base.py` | 150 | `#5D6D7E` | `#7F8C8D` | `_info_card()` content text — affects ALL pages |
| D-074 | `_router_base.py` | 138 | `#F8F9FA` | Not in palette | `_白话_card()` background — affects ALL pages |
| D-075 | `event_dashboard.py` | 148 | `#5D6D7E` | `#7F8C8D` | Adaptive banner content |
| D-076 | `etf_detail.py` | 184,252 | `#5D6D7E` + `#F8F9FA` | `#7F8C8D` + not in palette | Explanation cards |
| D-077 | `etf_detail.py` | 307 | `#FEF9E7`/`#F9E79F`/`#7D6608` | Not in palette | Disclaimer section |
| D-078 | `group_structure.py` | 204,219,258 | `#5D6D7E` | `#7F8C8D` | Group description text |
| D-079 | `business_card.py` | 271 | `#BDC3C7` | Not in palette | Table header border |
| D-080 | `timeline_controls.py` | 34 | `#5D6D7E` | `#7F8C8D` | Timeline label |
| D-081 | `main.py` | 50,54 | `#F9E79F`/`#7D6608` | Not in palette | Disclaimer CSS |
| D-082 | `main.py` | 117 | `#95A5A6` | Not in palette | Sidebar nav text |
| D-083 | `main.py` | 289 | `#95A5A6` | Not in palette | Welcome page text |

### Component Consistency — NEW (Round 7)

| # | File | Line | Issue |
|---|------|------|-------|
| D-084 | `group_structure.py` | 283 | Uses `st.bar_chart` (Streamlit native) instead of Plotly — violates chart architecture |

### Emoji Conflict (Still Open)

| # | File | Line | Issue |
|---|------|------|-------|
| D-005 | `_router_base.py` | 129-130 | `_section_title()` auto-prepends 📊 if title starts below U+2E00 — but some titles with emoji still get double-prefixed |

### Chart Palette (Still Open)

| # | File | Line | Issue |
|---|------|------|-------|
| D-071 | `chart.py` | 96 | `px.colors.qualitative.Set3` for pie charts — arbitrary colors, should use explicit palette |

### Fixes Since Round 6 ✅

| # | File | Line | Fix Applied |
|---|------|------|-------------|
| D-012 | `peer_comparison.py` | 51 | `@st.cache_data` removed from view layer |
| D-016 | `etf_browser.py` | 12, 18 | `@st.cache_data` replaced with module-level cache |
| D-059 | `_router_base.py` | 145 | `_info_card()` border changed from `#F39C12` to `#3498DB` |

### Page Grades (Round 7)

| Page | Grade | Change | Notes |
|------|-------|--------|-------|
| business_card.py | B | ← No change | 6 minor color violations (D-79, D-83) |
| chart.py | B+ | ← No change | D-071 Set3 palette remains |
| _router_base.py | B | ← Upgraded from B+ | D-073 affects all pages via shared components |
| event_dashboard.py | A- | ← No change | Best-graded page |
| financial_health.py | C+ | ← No change | |
| etf_detail.py | C | ← Downgraded from C+ | D-76, D-77 new violations |
| group_structure.py | D | ← No change | D-078, D-084 |
| category_browser.py | D | ← No change | |
| etf_browser.py | C | ← No change | |
| watchlist_page.py | C | ← No change | |
| operation_checkup.py | C | ← No change | |
| peer_comparison.py | C | ← No change | |
| main.py | C- | ← Downgraded from C | D-81, D-82, D-83 new violations |

### Cumulative Issue Count

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 | 26 | 26 | 2 |
| Round 3 | 3 | 29 | 0 |
| Round 4 | 25 | 54 | 0 |
| Round 5 | 17 | 71 | 2 |
| Round 6 | 10 | 81 | 1 |
| Round 7 | 11 | 92 | 0 |
| **Total** | **92** | **92** | **5** |

**Overall design grade: C+** (unchanged from Round 6)

### Top 5 Recommended Fixes (Round 7)

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 1 | D-073: Fix `#5D6D7E` → `#7F8C8D` in `_info_card()` | 5 min | Affects all pages globally |
| 2 | D-071: Replace Set3 palette in pie charts | 30 min | Affects all pie charts |
| 3 | D-084: Replace `st.bar_chart` with Plotly | 30 min | Single page, architecture compliance |
| 4 | D-005: Fix `_section_title()` emoji logic | 15 min | Affects all section titles |
| 5 | D-074: Standardize `#F8F9FA` background usage | 10 min | Affects `_白话_card()` globally |


## QA Verification (Cron Job 2026-06-16)
- Fixed failing unit test in i18n formatting (rounding behavior).
- Removed duplicate entries in tone QA test exclusions.
- All tests pass.

---

*Last updated: 2026-06-13 by PM after Round 7 design review.*
