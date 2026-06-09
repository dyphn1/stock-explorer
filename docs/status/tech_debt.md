# Stock Explorer Technical Debt Report

> **Date**: 2026-06-10
> **Reviewer**: System Architect (Subagent)
> **Scope**: Full codebase review (54 Python files, ~5,300 LOC)
> **Context**: All P0/P1/P2 bugs fixed. Previous review was 2026-06-09 (364 lines). This is an updated review reflecting changes made since then.

---

## Executive Summary

This is an **updated** technical debt review. The previous review (2026-06-09) identified 19 items. Since then, the following have been **completed**:

| # | Item | Status |
|---|------|--------|
| 1 | Consolidate `_find_value` / `_find_financial_value` | ✅ Done — single `_find_financial_value` in `_router_base.py`; `roe_calculator.py` now imports it |
| 2 | Remove duplicate card helpers from page modules | ✅ Done — all pages import `_section_title`, `_白话_card`, `_info_card` from `_router_base.py` |
| 3 | Remove duplicate `filter_by_timeline` from `timeline_controls.py` | ✅ Done — only definition is in `_router_base.py` |
| 4 | Unify `_is_etf` logic | ✅ Done — only definition is in `watchlist.py`; `router.py` imports it |
| 5 | Remove unused dependencies (`dotenv`, `tqdm`) | ✅ Done — `pyproject.toml` is clean |
| 6 | Input validation for `stock_id` | ✅ Done — `src/services/validation.py` with `validate_stock_id()` |
| 7 | Partial data loading in `get_stock_data()` | ✅ Done — each API call wrapped in independent try/except; returns partial data |
| 8 | Parallel API calls with `ThreadPoolExecutor` | ✅ Done — `get_stock_data()` uses `max_workers=5` |
| 9 | Unit tests for core business logic | ✅ Done — `tests/test_business_logic.py` (29 tests) covering `calc_roe_ttm`, `_is_etf`, `filter_by_timeline` |

This update identifies **12 remaining items** (down from 19), including **3 new items** that emerged from the recent changes. Priorities have been re-assessed.

---

## 1. Code Duplication (DRY) — Updated

### ✅ RESOLVED: Card helpers duplicated across 4+ files
All page modules now import `_section_title`, `_白话_card`, `_info_card` from `_router_base.py`. No local re-definitions remain.

### ✅ RESOLVED: `_find_value` / `_find_financial_value` duplicated
Single definition `_find_financial_value` in `_router_base.py` (line 113). `roe_calculator.py` imports it. No other copies exist.

### ✅ RESOLVED: `_is_etf` logic duplicated between `router.py` and `watchlist.py`
Only definition is in `watchlist.py` (line 91). `router.py` imports it as `_is_etf_check`. Note: `adaptive_engine.py` `detect_company_type()` (line 389) has **inline** ETF detection logic that is simpler (only checks industry and `00xx` pattern), but this is a separate, purpose-specific check (company type classification, not ETF routing), so it's not a DRY violation per se — see NEW-A01 below.

### ✅ RESOLVED: `filter_by_timeline` duplicate removed
Only definition is in `_router_base.py`. `timeline_controls.py` keeps only the UI selector `render_timeline_selector()`.

### 🟢 NEW-A01: Timeline constants duplicated between modules

**Files affected**:
- `src/pages/_router_base.py` → `_TIMELINE_DAYS` (line 149) — maps labels to day counts
- `src/pages/timeline_controls.py` → `_TIMELINE_OPTIONS` (line 12) — same mapping

**Problem**: `_TIMELINE_DAYS` and `_TIMELINE_OPTIONS` define the same `{"1Y": 365, "3Y": 1095, "5Y": 1825, "ALL": None}` mapping. The values will inevitably diverge.

**Impact**: If a new timeline option is added to one but not the other, the filter and the UI will be out of sync.

**Recommendation**: Extract timeline constants into a shared module (e.g., `src/services/timeline.py` or `_router_base.py`) and have `timeline_controls.py` import from it. Estimated effort: 10 minutes.

---

## 2. Error Handling Gaps — Updated

### ✅ RESOLVED: Silent exception swallowing in data loading
`get_stock_data()` now wraps each API call in `_fetch()` (line 41–45) with per-call try/except. Failed calls return `None` for that data source; the rendering functions already handle `None` gracefully.

### ✅ RESOLVED: No input validation on stock_id
`src/services/validation.py` provides `validate_stock_id()` with proper format checking (4-digit numeric, empty/special char handling).

### 🟡 MEDIUM-B01: `FinMindRateLimitError` is raised but never caught

**File**: `src/data/finmind_client.py` (lines 126–128)

**Problem**: When a 429 rate limit is detected, `FinMindRateLimitError` is raised. However, in `get_stock_data()` (line 44), the `_fetch()` inner function catches **all** exceptions with a bare `except Exception` and returns `None`. The rate limit error is silently swallowed — the user never sees a rate limit warning.

**Impact**: Rate limit detection exists but provides no user-facing feedback. Users see "暫無資料" instead of "API rate limited, try again later."

**Recommendation**: Either (a) handle `FinMindRateLimitError` specially in `_fetch()` to propagate it, or (b) set a session state flag that the UI can check. At minimum, log a warning. Estimated effort: 15 minutes.

---

## 3. Performance Bottlenecks — Updated

### ✅ RESOLVED: Sequential API calls in `get_stock_data()`
10 API calls now run in parallel via `ThreadPoolExecutor(max_workers=5)`.

### 🔴 HIGH-C01: N+1 query pattern in category browser (UNFIXED)

**File**: `src/pages/category_browser.py` (lines 68–89, 205–226)

**Problem**: The category browser fetches daily prices for 200 stocks sequentially (one API call per stock). Despite `@st.cache_data` on `FinMindClient`, this is still 200 sequential network calls on first load. The ETF browser has partially addressed this with `_get_all_etf_prices()` and caching, but the category browser has not.

**Impact**: Category browser takes 30–60 seconds to load on cold cache. This is the slowest page in the app.

**Recommendation**:
1. Pre-compute top 200 by trading money using a batch approach or reduce to top 50.
2. Consider showing only top 20 by default with "Load more" pagination.
3. Add aggressive caching (TTL ≥ 24h) for the stock info + daily price combo.
Estimated effort: 2 hours.

### 🟡 MEDIUM-C02: `ThreadPoolExecutor` max_workers not configurable

**File**: `src/pages/_router_base.py` (line 47)

**Problem**: `max_workers=5` is hardcoded. Under rate limiting, 5 concurrent calls may trigger more 429s. Under normal conditions, higher concurrency could be faster.

**Impact**: No way to tune concurrency without code changes. The FinMind API may rate-limit aggressive concurrent requests.

**Recommendation**: Make `max_workers` a parameter with a default of 5. Consider adaptive concurrency that backs off on rate limit errors. Estimated effort: 20 minutes.

### 🟡 MEDIUM-C3: ETF dividend ranking still fetches sequentially

**File**: `src/pages/etf_browser.py` (lines 340–413)

**Problem**: While `_get_all_etf_prices()` caches prices efficiently, the dividend ranking still fetches dividend data for ALL ETFs sequentially (one API call per ETF). This is ~500 sequential calls.

**Impact**: ETF dividend ranking is the second-slowest feature. First load can take 5+ minutes.

**Recommendation**: Add dividend caching with TTL ≥ 7 days (dividends don't change daily). Batch the fetches or use a separate background cache warm-up. Estimated effort: 1.5 hours.

---

## 4. Scalability Concerns — Updated

### 🔴 HIGH-D01: YAML-based storage doesn't scale beyond single-user (UNFIXED)

**Files**: `src/services/watchlist.py`, `src/services/adaptive_engine.py`

**Problem**: Watchlist and events are stored in YAML files with file locking. File locks don't work across processes/machines. The multi-watchlist system (ISSUE-C03) is now implemented, increasing the write frequency.

**Impact**: Cannot deploy to any multi-user environment without data corruption. The new multi-watchlist CRUD operations (create_list, delete_list, rename_list) all write to the same file, increasing contention.

**Recommendation**: Abstract storage behind an interface. Implement SQLite backend for multi-user support. Keep YAML as default for local development. Estimated effort: 4 hours.

### 🟡 MEDIUM-D02: Module-level global state for rate limiting (UNFIXED)

**File**: `src/data/finmind_client.py` (lines 32–34)

**Problem**: `_consecutive_failures` and `_last_failure_time` are module-level globals. In a multi-process deployment, each process has its own counter.

**Impact**: Rate limit warnings may not appear when they should, or may appear incorrectly.

**Recommendation**: Use `st.session_state` for per-session tracking, or a shared cache for multi-process. Estimated effort: 1 hour.

### 🟡 MEDIUM-D03: Hardcoded static data in multiple modules (UNFIXED)

**Files**: `src/services/analogy_engine.py` (one_liners dict, 20 entries), `src/services/revenue_analyzer.py` (KNOWN_COMPANY_REVENUE, 9 entries), `src/pages/group_structure.py` (KNOWN_GROUP_STRUCTURES, 5 entries), `src/pages/peer_comparison.py` (INDUSTRY_BENCHMARKS, 28 entries)

**Problem**: Static company data is scattered across 4 modules. Adding a new company requires edits in multiple files. No single source of truth.

**Impact**: High maintenance cost as company coverage grows. Inconsistencies between modules.

**Recommendation**: Create a single `src/data/company_registry.yaml` (or JSON) that holds all static company data. Load it once at startup. Estimated effort: 2 hours.

---

## 5. Missing Tests — UPDATED

### ✅ NEW COVERAGE: Unit tests added
`tests/test_business_logic.py` now has 29 tests covering:
- `calc_roe_ttm()` — 10 tests (full TTM, single quarter, 2 quarters, empty, None, zero equity, negative ROE, English columns)
- `_is_etf()` — 13 tests (regular stock, by industry, case-insensitive, by name heuristic, by ID pattern, priority, None/empty industry)
- `filter_by_timeline()` — 6 tests (empty, None, ALL, 1Y, 3Y, default)

### 🔴 HIGH-E01: No tests for event detection algorithms (NEW)

**Problem**: The core business logic tests cover `_is_etf`, `calc_roe_ttm`, and `filter_by_timeline`. But there are **zero** tests for:
- `detect_revenue_event()` — YoY threshold behavior
- `detect_price_abnormal()` — single-day threshold behavior
- `detect_news_event()` — keyword matching
- `check_data_freshness()` — date staleness logic
- `detect_company_type()` — ETF/group/default classification
- `extract_dividend_summary()` — frequency classification, annual estimation
- `validate_stock_id()` — the newly added validation function

**Impact**: These are the core "value-add" algorithms of the app. A regression in event detection would go unnoticed.

**Recommendation**: Add pytest-based unit tests for all pure functions with known inputs/outputs. Start with `validate_stock_id()` and `detect_revenue_event()`. Estimated effort: 3 hours.

### 🟡 MEDIUM-E02: No integration tests for data pipeline (UNFIXED)

**Problem**: No tests verify that FinMind API responses are correctly parsed and transformed. The `COLUMN_ALIASES` system in `adaptive_engine.py` is a good start but not tested.

**Impact**: Fragile dependency on FinMind API schema. If FinMind changes column names, the app will fail silently.

**Recommendation**: Add snapshot tests with saved API responses. Test the full data pipeline from API response to rendered output. Estimated effort: 3 hours.

### 🟡 MEDIUM-E03: Test uses `st.session_state` outside Streamlit context

**File**: `tests/test_business_logic.py` (lines 236, 243, 255)

**Problem**: `filter_by_timeline()` tests set `st.session_state["test_tl_1y"] = "1Y"` etc. This requires a Streamlit runtime context. The tests may fail when run with plain `pytest` outside Streamlit.

**Impact**: Tests may be fragile or fail in CI without Streamlit mocking.

**Recommendation**: Either use `pytest-mock` to mock `st.session_state`, or refactor `filter_by_timeline()` to accept an optional `timeline_value` parameter that bypasses `st.session_state`. Estimated effort: 30 minutes.

---

## 6. Dependency Health — Updated

### ✅ RESOLVED: Unused dependencies removed
`python-dotenv` and `tqdm` are no longer in `pyproject.toml`.

### 🟡 MEDIUM-F01: Missing `uv.lock` file

**Problem**: The project uses `uv` but has no `uv.lock` file committed. A `uv sync` on a different day could install incompatible versions. No upper bounds are specified.

**Impact**: Non-reproducible builds. The `st.query_params` API requires Streamlit >=1.30 — a future Streamlit 2.x could break it.

**Recommendation**: Run `uv lock` and commit `uv.lock`. Estimated effort: 5 minutes.

### 🟡 MEDIUM-F02: FinMind is the sole data source (UNFIXED)

**Problem**: All data comes from FinMind. No fallback if FinMind is down or rate-limited.

**Impact**: Complete data unavailability when FinMind has issues.

**Recommendation**: Cache a "last known good" dataset that can be served when the API is unavailable. The disk cache in `FinMindClient` helps but doesn't handle the initial load case. Estimated effort: 2 hours.

---

## 7. New Architecture Observations

### Strengths (since last review)
1. **Parallel data loading**: `ThreadPoolExecutor` in `get_stock_data()` is a clean implementation
2. **Input validation**: `validation.py` is a good addition
3. **Test suite**: 29 unit tests provide a foundation for regression safety
4. **Multi-watchlist**: `watchlist.py` now supports multiple named lists with full CRUD
5. **DRY cleanup**: Card helpers, `_find_value`, and `_is_etf` are properly consolidated

### Weaknesses (new or remaining)
1. **No abstraction layers**: Business logic is tightly coupled to Streamlit. The `data` dict in `get_stock_data()` is untyped — `models.py` dataclasses are defined but unused
2. **Rate limit detection silently swallowed**: `FinMindRateLimitError` is raised but caught by the generic `except Exception` in `_fetch()`
3. **No dependency injection**: `FinMindClient` is instantiated directly in multiple places
4. **No `uv.lock`**: Despite claiming it's done in the previous review's action plan, no lock file exists on disk
5. **Inner function `_fetch` swallows debugging info**: Line 44 `except Exception: return name, None` — no logging, making troubleshooting API failures difficult

---

## 8. Prioritized Action Plan

### Immediate (This Week)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 1 | Commit `uv.lock` | 5 min | Reproducibility | ❌ Not done |
| 2 | Extract shared timeline constants (NEW-A01) | 10 min | DRY | ❌ Not done |
| 3 | Add logging to `_fetch()` inner function | 10 min | Debuggability | ❌ Not done |
| 4 | Handle `FinMindRateLimitError` visibility (B01) | 15 min | UX | ❌ Not done |
| 5 | Fix `st.session_state` in tests (E03) | 30 min | Test reliability | ❌ Not done |

**Subtotal: ~1 hour**

### Short-Term (Next 2 Weeks)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 6 | Add tests for event detection & validation (E01) | 3 hours | Quality | ❌ Not done |
| 7 | Make `max_workers` configurable (C02) | 20 min | Performance tuning | ❌ Not done |
| 8 | Optimize category browser N+1 queries (C01) | 2 hours | Performance | ❌ Not done |
| 9 | Cache ETF dividend data (C03) | 1.5 hours | Performance | ❌ Not done |
| 10 | Consolidate static company data (D03) | 2 hours | Maintainability | ❌ Not done |
| 11 | Add type checking configuration | 2 hours | Quality | ❌ Not done |

**Subtotal: ~11 hours**

### Medium-Term (Post-MVP)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 12 | Abstract storage + SQLite backend (D01) | 4 hours | Scalability | ❌ Not done |
| 13 | Fix rate limit global state (D02) | 1 hour | Scalability | ❌ Not done |
| 14 | Integration tests with saved API responses (E02) | 3 hours | Quality | ❌ Not done |
| 15 | Pagination for large lists | 1 hour | UX | ❌ Not done |
| 16 | "Last known good" data fallback (F02) | 2 hours | Reliability | ❌ Not done |

**Subtotal: ~11 hours**

---

## 9. Summary Table

| Category | Items (2026-06-09) | Items (2026-06-10) | Critical | High | Medium | Low |
|----------|---------------------|---------------------|----------|------|--------|-----|
| Code Duplication | 4 | 1 (3 resolved) | — | — | — | 1 |
| Error Handling | 3 | 1 (1 resolved, 1 new) | — | — | 1 | — |
| Performance | 3 | 3 (1 resolved) | — | 1 | 2 | — |
| Scalability | 3 | 3 | — | 1 | 2 | — |
| Missing Tests | 3 | 3 (1 resolved) | — | 1 | 2 | — |
| Dependencies | 3 | 2 (1 resolved) | — | — | 2 | — |
| **Total** | **19** | **13** | **—** | **3** | **9** | **1** |

**Total estimated effort**: ~23 hours (Immediate: 1h, Short-term: 11h, Medium-term: 11h)

---

## 10. Key Changes Since Last Review

### Resolved Items (9)
1. ✅ `_find_value` / `_find_financial_value` consolidated into single `_find_financial_value` in `_router_base.py`
2. ✅ Card helpers (`_section_title`, `_白话_card`, `_info_card`) no longer duplicated in page modules
3. ✅ `filter_by_timeline` duplicate removed from `timeline_controls.py`
4. ✅ `_is_etf` unified — only in `watchlist.py`
5. ✅ Unused deps (`dotenv`, `tqdm`) removed
6. ✅ Input validation added (`src/services/validation.py`)
7. ✅ Partial data loading in `get_stock_data()` (per-call try/except)
8. ✅ Parallel API calls (`ThreadPoolExecutor`)
9. ✅ Unit tests added (29 tests)

### New Items Identified (3)
1. 🟢 NEW-A01: Timeline constants duplicated (`_TIMELINE_DAYS` vs `_TIMELINE_OPTIONS`)
2. 🟡 B01 (moved from resolved to active): `FinMindRateLimitError` silently swallowed by `_fetch()`
3. 🔴 E01: No tests for event detection, company type, dividend analysis, and validation

### Previously Claimed "Done" But Not Actually Done (1)
1. ❌ `uv.lock`: Marked as done in previous action plan, but no lock file exists

---

*The codebase is in good shape. The team has addressed 9 of 19 items from the first review. The highest-leverage remaining investments are: (1) adding tests for event detection algorithms, (2) optimizing the category browser's N+1 query pattern, and (3) consolidating static company data. These three actions will reduce bugs, speed up the slowest pages, and make the codebase easier to maintain.*
