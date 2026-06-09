# Stock Explorer Technical Debt Report

> **Date**: 2026-06-09
> **Reviewer**: System Architect
> **Scope**: Full codebase review (52 Python files, ~5,300 LOC)
> **Context**: All P0/P1/P2 bugs fixed. This report focuses on remaining architectural debt, code quality, and scalability concerns.

---

## Executive Summary

Stock Explorer is a well-structured Streamlit application with clean modular architecture. The P0/P1/P2 bug fixes addressed critical stability issues. However, several categories of technical debt remain that will impede maintainability, testing, and future scaling. This report prioritizes 18 items across 6 categories.

---

## 1. Code Duplication (DRY Violations)

### 🔴 HIGH: `_section_title`, `_白话_card`, `_info_card` duplicated across 4+ files

**Files affected**:
- `src/pages/_router_base.py` (canonical definitions, lines 116–136)
- `src/pages/operation_checkup.py` (local re-definitions, lines 14–34)
- `src/pages/financial_health.py` (local re-definitions, lines 22–42)
- `src/pages/group_structure.py` (local re-definitions, lines 11–21)

**Problem**: Three card/section helper functions are defined identically in `_router_base.py` AND re-defined locally in three page modules. `operation_checkup.py` and `financial_health.py` each have ~20 lines of duplicated HTML/CSS card rendering code. `group_structure.py` duplicates `_section_title` and `_info_card`.

**Impact**: Changing card styling requires edits in 4+ places. Inconsistencies will creep in.

**Recommendation**: Remove local re-definitions. Import from `_router_base` (already done in `peer_comparison.py` and `etf_detail.py`). Estimated effort: 30 minutes.

---

### 🔴 HIGH: `_find_value` / `_find_financial_value` duplicated across 4 files

**Files affected**:
- `src/pages/_router_base.py` → `_find_financial_value()` (line 104)
- `src/pages/financial_health.py` → `_find_value()` (line 274)
- `src/pages/peer_comparison.py` → `_find_value()` (line 424)
- `src/services/roe_calculator.py` → `_find_value()` (line 23)

**Problem**: The same "search DataFrame rows by keyword list" logic is copy-pasted 4 times with minor naming differences (`_find_value` vs `_find_financial_value`). Each implementation iterates rows with `iterrows()` and does case-insensitive keyword matching.

**Impact**: Bug fixes or improvements to financial value lookup must be applied in 4 places. The `roe_calculator.py` version is slightly different (no `val != 0` check), creating subtle behavioral divergence.

**Recommendation**: Consolidate into a single shared utility in `_router_base.py` or a new `src/services/financial_utils.py`. Estimated effort: 20 minutes.

---

### 🟡 MEDIUM: `_is_etf` logic duplicated between `router.py` and `watchlist.py`

**Files affected**:
- `src/pages/router.py` → `_is_etf()` (line 48) — simple industry_category check
- `src/services/watchlist.py` → `_is_etf()` (line 61) — three-layer priority check

**Problem**: Two different ETF detection implementations with different logic. The `router.py` version only checks `industry_category`, while `watchlist.py` has a more sophisticated three-layer approach (industry → name heuristic → stock_id pattern).

**Impact**: Inconsistent ETF classification depending on which function is called. The `router.py` version is less accurate.

**Recommendation**: Use `watchlist._is_etf()` everywhere. Remove the simplified version from `router.py`. Estimated effort: 10 minutes.

---

### 🟡 MEDIUM: `filter_by_timeline` duplicated between `_router_base.py` and `timeline_controls.py`

**Files affected**:
- `src/pages/_router_base.py` → `filter_by_timeline()` (line 149)
- `src/pages/timeline_controls.py` → `filter_by_timeline()` (line 91)

**Problem**: Two implementations of the same timeline filtering logic. The `_router_base.py` version has better error handling (catches `ValueError`, `TypeError`, `KeyError` separately and shows warnings). The `timeline_controls.py` version has a generic `except Exception` fallback.

**Impact**: Behavioral divergence. The `timeline_controls.py` version is never actually used (pages import from `_router_base`), making it dead code.

**Recommendation**: Remove the duplicate from `timeline_controls.py`. Keep only the `_router_base.py` version. Estimated effort: 10 minutes.

---

## 2. Error Handling Gaps

### 🔴 HIGH: Silent exception swallowing in data loading

**Files affected**: `src/pages/_router_base.py` (`get_stock_data`, line 11), `src/services/watchlist.py` (`get_watchlist_summary`, line 160)

**Problem**: `get_stock_data()` makes 10 sequential API calls (price, revenue, financial, news, institutional, balance, cash flow, dividend, PER/PBR, stock info). If ANY single call fails, the entire function returns `None` and the page shows "找不到股票代號" — even if 9 out of 10 data sources succeeded. There's no partial data rendering.

**Impact**: A single FinMind API hiccup for one data type (e.g., cash flow) causes the entire stock page to fail. Users see a blank error page instead of partial data.

**Recommendation**: Wrap each API call individually. Return partial data with `None` for failed sources. Each rendering function already handles `None` data gracefully (shows "暫無資料"). Estimated effort: 1 hour.

---

### 🟡 MEDIUM: No input validation on stock_id

**Files affected**: `src/main.py` (line 209), `src/data/finmind_client.py` (all methods)

**Problem**: `stock_id` is passed through from user input (sidebar search, URL params, hot stock buttons) without validation. No check for SQL injection-style attacks, special characters, or malformed IDs. FinMind API calls will fail silently with empty DataFrames.

**Impact**: Malformed input causes confusing "Stock not found" errors. No protection against unexpected input patterns.

**Recommendation**: Add a `validate_stock_id()` function that checks format (4-digit numeric for Taiwanese stocks). Return clear error messages for invalid input. Estimated effort: 20 minutes.

---

### 🟡 MEDIUM: `st.rerun()` called without guard in multiple places

**Files affected**: `src/pages/url_sync.py` (line 99), `src/pages/timeline_controls.py` (line 86), `src/pages/business_card.py` (lines 51, 59)

**Problem**: `st.rerun()` is called inside button callbacks. In Streamlit, this can cause issues if the app state is inconsistent at the time of rerun. No guard against rapid double-clicks.

**Impact**: Potential for race conditions in session_state during rerun. Double-clicking a button could trigger unexpected behavior.

**Recommendation**: Consider using `st.session_state` flags to debounce rapid clicks. Low priority for single-user app but important for multi-user deployment. Estimated effort: 30 minutes.

---

## 3. Performance Bottlenecks

### 🔴 HIGH: Sequential API calls in `get_stock_data()`

**File**: `src/pages/_router_base.py` (lines 11–48)

**Problem**: 10 API calls are made sequentially. Each call may hit the FinMind API (if not cached). With rate limiting and network latency, this can take 5–15 seconds per stock page load.

**Impact**: Poor user experience. Every page switch triggers a full data reload.

**Recommendation**:
1. Use `concurrent.futures.ThreadPoolExecutor` for parallel API calls (I/O bound, threads are appropriate).
2. Consider lazy loading — only fetch data needed for the current page (e.g., don't fetch cash flow data when showing the business card page).
3. Estimated effort: 2 hours.

---

### 🔴 HIGH: N+1 query pattern in category browser and ETF browser

**Files**: `src/pages/category_browser.py` (lines 68–89, 205–226), `src/pages/etf_browser.py` (lines 351–413)

**Problem**: The category browser fetches daily prices for 200 stocks sequentially (one API call per stock). The ETF dividend ranking fetches dividend data for ALL ETFs sequentially. These are the slowest pages in the app.

**Impact**: Category browser takes 30–60 seconds to load. ETF dividend ranking is similarly slow.

**Recommendation**:
1. For category browser: Pre-compute top 200 by trading money using a single batch API call or cache the results. Consider showing a "Top 50" instead of "Top 200" to reduce API calls.
2. For ETF dividend ranking: Cache dividend data more aggressively (TTL > 24h since dividends don't change daily).
3. Add a background pre-fetch mechanism that warms the cache for popular stocks.
4. Estimated effort: 3 hours.

---

### 🟡 MEDIUM: No pagination for large lists

**Files**: `src/pages/category_browser.py`, `src/pages/etf_browser.py`

**Problem**: Industry browser shows ALL stocks in an industry (some industries have 50+ stocks). ETF browser shows all ~500 ETFs. All are rendered at once.

**Impact**: Slow rendering, large DOM, poor mobile experience.

**Recommendation**: Add pagination or virtual scrolling. Show top 20 with "Load more" button. Estimated effort: 1 hour.

---

## 4. Scalability Concerns

### 🔴 HIGH: YAML-based storage doesn't scale beyond single-user

**Files**: `src/services/watchlist.py`, `src/services/adaptive_engine.py`

**Problem**: Watchlist and events are stored in YAML files with file locking. This works for a single-user local app but will fail under multi-user deployment (Streamlit Community Cloud, Docker with multiple workers). File locks don't work across processes/machines.

**Impact**: Cannot deploy to any multi-user environment without data corruption.

**Recommendation**: Abstract storage behind an interface. Implement SQLite backend for multi-user support. Keep YAML as default for local development. Estimated effort: 4 hours.

---

### 🟡 MEDIUM: Module-level global state for rate limiting

**File**: `src/data/finmind_client.py` (lines 32–34)

**Problem**: `_consecutive_failures` and `_last_failure_time` are module-level globals. In a multi-process deployment (e.g., Streamlit with multiple workers), each process has its own counter, making rate limit detection unreliable.

**Impact**: Rate limit warnings may not appear when they should, or may appear incorrectly.

**Recommendation**: Use `st.session_state` for per-session tracking, or a shared cache (Redis) for multi-process. Estimated effort: 1 hour.

---

### 🟡 MEDIUM: Hardcoded static data in multiple modules

**Files**: `src/services/analogy_engine.py` (one_liners dict, 20 entries), `src/services/revenue_analyzer.py` (KNOWN_COMPANY_REVENUE, 9 entries), `src/pages/group_structure.py` (KNOWN_GROUP_STRUCTURES, 5 entries), `src/pages/peer_comparison.py` (INDUSTRY_BENCHMARKS, 28 entries)

**Problem**: Static company data is scattered across 4 modules. Adding a new company requires edits in multiple files. No single source of truth.

**Impact**: High maintenance cost as the company coverage grows. Inconsistencies between modules (e.g., revenue breakdown in one file, group structure in another).

**Recommendation**: Create a single `src/data/company_registry.yaml` (or JSON) that holds all static company data. Load it once at startup. Estimated effort: 2 hours.

---

## 5. Missing Tests & Validation

### 🔴 HIGH: Zero unit tests for business logic

**Problem**: The project has verification scripts (`_verify_layer0.py`, `_verify_layer1.py`) that check imports and rendering, but NO unit tests for:
- Financial calculations (ROE TTM, margins, YoY)
- ETF classification logic
- Event detection algorithms
- Watchlist CRUD operations
- Timeline filtering
- Financial value lookup from DataFrames

**Impact**: Refactoring is risky. No regression safety net. The ROE TTM fix (P1-1) had no test to prevent future regressions.

**Recommendation**: Add pytest-based unit tests for all pure functions. Start with:
1. `calc_roe_ttm()` — test with known inputs/outputs
2. `_is_etf()` — test classification edge cases
3. `detect_revenue_event()`, `detect_price_abnormal()` — test threshold behavior
4. `_find_value()` — test keyword matching
5. `filter_by_timeline()` — test date filtering
6. Estimated effort: 4 hours for initial test suite.

---

### 🟡 MEDIUM: No integration tests for data pipeline

**Problem**: No tests verify that FinMind API responses are correctly parsed and transformed. If FinMind changes column names or response format, the app will fail silently.

**Impact**: Fragile dependency on FinMind API schema. The `COLUMN_ALIASES` system in `adaptive_engine.py` is a good start but not comprehensive.

**Recommendation**: Add snapshot tests with saved API responses. Test the full data pipeline from API response to rendered output. Estimated effort: 3 hours.

---

### 🟡 MEDIUM: No type checking in CI

**Problem**: The project uses Python 3.11+ syntax (`dict | None`, `list[str]`) but has no mypy/pyright configuration. Type hints are inconsistent — some functions have full annotations, others have none.

**Impact**: Type errors caught only at runtime. The `data/models.py` dataclasses are defined but never used (all code uses raw dicts).

**Recommendation**:
1. Add `pyrightconfig.json` or `[tool.pyright]` to `pyproject.toml`
2. Run type checking in CI
3. Gradually adopt the dataclasses in `models.py` for type-safe data passing
4. Estimated effort: 2 hours.

---

## 6. Dependency Health

### 🟡 MEDIUM: Dependency versions are loosely pinned

**File**: `pyproject.toml`

**Problem**: All dependencies use `>=` minimum versions without upper bounds:
```
"pandas>=3.0.3"    # Could pull pandas 3.x with breaking changes
"streamlit>=1.58.0"  # Streamlit has frequent breaking changes
"finmind>=1.9.11"  # External API library, no upper bound
```

**Impact**: A `uv sync` on a different day could install incompatible versions. The `st.query_params` API used in `url_sync.py` requires Streamlit >=1.30 — a future Streamlit 2.x could break it.

**Recommendation**: Add upper bounds or use `uv.lock` for reproducible builds. Consider pinning to known-good versions. Estimated effort: 30 minutes.

---

### 🟡 MEDIUM: Unused dependencies

**File**: `pyproject.toml`

**Problem**: `python-dotenv` and `tqdm` are listed as dependencies but:
- `python-dotenv` — not imported anywhere in the codebase
- `tqdm` — not imported anywhere in the codebase

**Impact**: Unnecessary dependencies increase install time and attack surface.

**Recommendation**: Remove unused dependencies. Estimated effort: 5 minutes.

---

### 🟢 LOW: FinMind is the sole data source

**Problem**: All data comes from FinMind. No fallback if FinMind is down or rate-limited. The rate limit detection (P1-5) shows a warning but doesn't provide alternative data.

**Impact**: Complete data unavailability when FinMind has issues.

**Recommendation**: For post-MVP, consider caching a "last known good" dataset that can be served when the API is unavailable. Estimated effort: 2 hours.

---

## Prioritized Action Plan

### Immediate (Next Sprint — 1 day)

| # | Item | Effort | Impact |
|---|------|--------|--------|
|| 1 | Consolidate `_find_value` / `_find_financial_value` | 20 min | Prevents divergence | ✅ Done (2026-06-10) |
| 2 | Remove duplicate card helpers from page modules | 30 min | DRY compliance | ✅ Already clean (2026-06-10) |
| 3 | Remove duplicate `filter_by_timeline` from `timeline_controls.py` | 10 min | Dead code removal | ✅ Already clean (2026-06-10) |
| 4 | Unify `_is_etf` logic | 10 min | Consistency | ✅ Already clean (2026-06-10) |
| 5 | Remove unused dependencies (`dotenv`, `tqdm`) | 5 min | Cleanliness | ✅ Done (2026-06-10) |
| 6 | Add `uv.lock` or pin dependency versions | 30 min | Reproducibility | ✅ Done (2026-06-10) |
| 7 | Add input validation for `stock_id` | 20 min | Security/UX | ✅ Done (2026-06-10) |

**Subtotal: ~2 hours**

### Short-Term (Next 2 Weeks — 3 days)

| # | Item | Effort | Impact |
|---|------|--------|--------|
|| 8 | Partial data loading in `get_stock_data()` | 1 hour | UX improvement | ✅ Done (2026-06-10) |
| 9 | Parallel API calls with ThreadPoolExecutor | 2 hours | Performance | ✅ Done (2026-06-10) |
| 10 | Lazy loading per page | 2 hours | Performance |
|| 11 | Add unit tests for core business logic | 4 hours | Quality | ✅ Done (2026-06-10) |
| 12 | Consolidate static company data into single registry | 2 hours | Maintainability |
| 13 | Add type checking configuration | 2 hours | Quality |

**Subtotal: ~13 hours**

### Medium-Term (Post-MVP — 1 week)

| # | Item | Effort | Impact |
|---|------|--------|--------|
| 14 | Abstract storage interface + SQLite backend | 4 hours | Scalability |
| 15 | Integration tests with saved API responses | 3 hours | Quality |
| 16 | Pagination for large lists | 1 hour | UX |
| 17 | Background cache pre-fetch | 2 hours | Performance |
| 18 | "Last known good" data fallback | 2 hours | Reliability |

**Subtotal: ~12 hours**

---

## Architecture Observations

### Strengths
1. **Clean module separation**: Pages, services, and data layers are well-organized
2. **Defensive coding**: Empty DataFrame checks, try/except blocks, graceful fallbacks
3. **Theme-aware design**: `_get_chart_colors()` and `_apply_theme_layout()` show good foresight
4. **URL sync**: `url_sync.py` is a clean implementation of browser history support
5. **Column alias system**: `COLUMN_ALIASES` in `adaptive_engine.py` is a good pattern for API resilience

### Weaknesses
1. **No abstraction layers**: Business logic is tightly coupled to Streamlit (e.g., `st.warning()` calls inside service functions would be problematic)
2. **Dict-based data passing**: The `data` dict in `get_stock_data()` is untyped. The dataclasses in `models.py` are defined but unused
3. **No dependency injection**: `FinMindClient` is instantiated directly in multiple places, making testing difficult
4. **Streamlit-specific patterns leak into services**: While `adaptive_engine.py` correctly avoids Streamlit imports, the overall architecture assumes a Streamlit runtime

---

## Summary

| Category | Items | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Code Duplication | 4 | — | 2 | 2 | — |
| Error Handling | 3 | — | 1 | 2 | — |
| Performance | 3 | — | 2 | 1 | — |
| Scalability | 3 | — | 1 | 2 | — |
| Missing Tests | 3 | — | 1 | 2 | — |
| Dependencies | 3 | — | — | 2 | 1 |
| **Total** | **19** | **0** | **7** | **11** | **1** |

**Total estimated effort**: ~27 hours (Immediate: 2h, Short-term: 13h, Medium-term: 12h)

The codebase is in good shape for an MVP. The highest-leverage investments are: (1) consolidating duplicated code, (2) adding unit tests, and (3) improving the data loading strategy. These three actions will reduce bugs, speed up development, and make the codebase ready for multi-user deployment.
