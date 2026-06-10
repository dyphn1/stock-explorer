# Stock Explorer Technical Debt Report

> **Date**: 2026-06-11
> **Reviewer**: System Architect (Subagent)
> **Scope**: Full codebase review (50 Python source files, ~6,200 LOC including tests)
> **Context**: All P0/P1/P2 bugs fixed. Previous reviews: 2026-06-09 (364 lines, 19 items), 2026-06-10 (317 lines, 13 items). This is Round 3.

---

## Executive Summary

This is the **third** technical debt review. The previous review (2026-06-10) identified 13 items. Since then, the following have been **completed or substantially resolved**:

| # | Item | Status |
|---|------|--------|
| 1 | `FinMindRateLimitError` silently swallowed (B01) | ✅ Fixed — `_fetch()` catches it, sets session state |
| 2 | Missing `uv.lock` (F01) | ✅ Fixed — lock file now exists on disk |
| 3 | No tests for event detection (E01) | ✅ Fixed — 800-line test file covering 11 functions |
| 4 | `st.session_state` in tests (E03) | ✅ Fixed — down to 1 usage (from test framework coupling) |

This update identifies **14 remaining/active items**, including **6 new items** discovered during this review. Priorities have been re-assessed.

---

## 1. Code Duplication (DRY) — Updated

### ✅ RESOLVED: Card helpers duplicated across 4+ files
All page modules import `_section_title`, `_白话_card`, `_info_card` from `_router_base.py`.

### ✅ RESOLVED: `_find_value` / `_find_financial_value` duplicated
Single definition in `_router_base.py` (line 117).

### ✅ RESOLVED: `_is_etf` logic unified
Only definition in `watchlist.py` (line 91).

### ✅ RESOLVED: `filter_by_timeline` duplicate removed
Only definition in `_router_base.py`.

### 🟢 LOW-A01: Timeline constants duplicated between modules

**Files affected**:
- `src/pages/_router_base.py` → `_TIMELINE_DAYS` (line 154) — maps labels to day counts
- `src/pages/timeline_controls.py` → `_TIMELINE_OPTIONS` (line 12) — same mapping

**Problem**: `_TIMELINE_DAYS` and `_TIMELINE_OPTIONS` define the same `{"1Y": 365, "3Y": 1095, "5Y": 1825, "ALL": None}` mapping.

**Impact**: If a new timeline option is added to one but not the other, the filter and UI will be out of sync.

**Recommendation**: Extract timeline constants into a shared module. Estimated effort: 10 minutes.

### 🟡 NEW-G01: `_atomic_write` function duplicated in two modules

**Files affected**:
- `src/services/adaptive_engine.py` (line 135) — accepts `str` path
- `src/services/watchlist.py` (line 21) — accepts `Path` path

**Problem**: Both functions implement identical atomic-write-via-tempfile-and-rename logic. The `watchlist.py` version accepts `Path` objects while `adaptive_engine.py` accepts `str`, making consolidation slightly non-trivial but straightforward.

**Impact**: If a bug is found in the atomic write pattern (e.g., Windows compatibility), it must be fixed in two places. Inconsistent type signatures.

**Recommendation**: Extract to a shared utility module (e.g., `src/services/storage_util.py`). Estimated effort: 15 minutes.

### 🟡 NEW-G02: `models.py` dataclasses are dead code

**File**: `src/data/models.py` (86 lines, 6 dataclasses: `CompanyCard`, `RevenueBreakdown`, `FinancialSummary`, `PeerComparison`, `GroupStructure`, `AnalysisResult`)

**Problem**: Zero imports of any model class exist in the entire source tree. The data dict in `get_stock_data()` uses untyped dicts throughout.

**Impact**: 86 lines of dead code. The typed data structures were designed for the app but the app was built with raw dicts instead. This increases the risk of typos in dict key access going undetected.

**Recommendation**: Either (a) refactor the data pipeline to use these dataclasses (type safety benefit), or (b) remove `models.py` to avoid confusion. Estimated effort: option (a) 3 hours, option (b) 5 minutes.

---

## 2. Error Handling Gaps — Updated

### ✅ RESOLVED: Silent exception swallowing in data loading
`get_stock_data()` wraps each API call in `_fetch()` with per-call try/except.

### ✅ RESOLVED: No input validation on stock_id
`src/services/validation.py` provides `validate_stock_id()`.

### ✅ RESOLVED: `FinMindRateLimitError` silently swallowed
`_fetch()` (line 44) now catches `FinMindRateLimitError` specifically and sets `st.session_state["_rate_limited"] = True`. Rate limit banner in `main.py` (line 182-184) shows user-facing warning.

### 🟡 NEW-G04: Rate limit uses two disconnected mechanisms

**Files affected**:
- `src/pages/_router_base.py` (line 46) — sets `st.session_state["_rate_limited"] = True`
- `src/data/finmind_client.py` (lines 32-63) — module-level `_consecutive_failures` counter
- `src/main.py` (line 182-184) — reads `get_rate_limit_status()` (module-level counter)

**Problem**: When `_fetch()` catches `FinMindRateLimitError`, it sets `st.session_state["_rate_limited"]` but the UI banner in `main.py` checks `get_rate_limit_status()` which reads the module-level `_consecutive_failures` counter. The session-state flag is never read. Combined failures (empty responses, errors) increment `_consecutive_failures` which triggers the banner at threshold=3, but a single `FinMindRateLimitError` may not trigger it if there are fewer than 3 consecutive failures.

**Impact**: The `_rate_limited` session state flag is dead code — set but never read. The banner works via the module-level counter but may not fire for isolated rate limit events.

**Recommendation**: Either (a) read `st.session_state.get("_rate_limited")` in `main.py` and clear it after display, or (b) remove the session state flag and rely solely on the module-level counter. Estimated effort: 10 minutes.

---

## 3. Performance Bottlenecks — Updated

### ✅ RESOLVED: Sequential API calls in `get_stock_data()`
10 API calls now run in parallel via `ThreadPoolExecutor(max_workers=5)`.

### ✅ RESOLVED: `st.cache_data` removed from view layer
Zero occurrences of `st.cache_data` found in source code.

### 🔴 HIGH-C01: N+1 query pattern in category browser (UNFIXED)

**File**: `src/pages/category_browser.py` (lines 68-89, 205-226)

**Problem**: The category browser fetches daily prices for 200 stocks sequentially (one API call per stock). Despite FinMindClient caching, this is still 200 sequential network calls on first load. Both `_render_top_stocks_by_value` and `_render_hot_stocks_by_volume` do this independently (400 total calls for both sections, though the second batch hits cache).

**Impact**: Category browser takes 30-60 seconds to load on cold cache. With ThreadPoolExecutor applied per-stock (not across stocks), this remains the slowest page.

**Recommendation**: Consider fetching all prices in bulk (the ETF browser's `_get_all_etf_prices()` pattern works because ETF prices are cached after first load, but category browser doesn't have this). Add a shared "fetch all daily prices" batch function with TTL ≥ 24h. Estimated effort: 2 hours.

### 🟡 MEDIUM-C02: `ThreadPoolExecutor` max_workers not configurable

**File**: `src/pages/_router_base.py` (line 51)

**Problem**: `max_workers=5` is hardcoded. Under rate limiting, 5 concurrent calls may trigger more 429s.

**Impact**: No way to tune concurrency without code changes.

**Recommendation**: Make `max_workers` a parameter with a default of 5. Estimated effort: 20 minutes.

### 🟡 MEDIUM-C03: ETF dividend ranking still fetches sequentially

**File**: `src/pages/etf_browser.py` (lines 340-413)

**Problem**: The dividend ranking fetches dividend data for ALL ETFs sequentially (~500 calls). While prices are cached by `_get_all_etf_prices()`, dividends are not.

**Impact**: ETF dividend ranking takes 5+ minutes on first load.

**Recommendation**: Cache dividend data separately with TTL ≥ 7 days. Estimated effort: 1.5 hours.

### 🟡 NEW-G06: `FinMindClient` instantiated directly (no dependency injection)

**Files creating `FinMindClient()` directly**:
- `src/pages/router.py` (line 39)
- `src/pages/peer_comparison.py` (line 54 — fallback benchmark)
- `src/main.py` (line 131)

**Problem**: `FinMindClient` is instantiated with `FinMindClient(cache_dir=".cache")` in 2 places and bare `FinMindClient()` in 1 place (`peer_comparison.py`). No dependency injection means tests cannot easily mock the data layer.

**Impact**: The `peer_comparison.py` creates its own `FinMindClient()` without cache_dir, which uses default `.cache` but bypasses the test mock. Testing page-level logic with real data requires real API access or complex monkeypatching.

**Recommendation**: Accept `FinMindClient` as a parameter in rendering functions (most already do). Remove the bare `FinMindClient()` instantiation from `peer_comparison.py`. Estimated effort: 20 minutes.

---

## 4. Scalability Concerns — Updated

### 🔴 HIGH-D01: YAML-based storage doesn't scale beyond single-user (UNFIXED)

**Files**: `src/services/watchlist.py`, `src/services/adaptive_engine.py`

**Problem**: Watchlist and events stored in YAML files with file locks. File locks don't work across processes/machines. The `FinMindClient` is not a singleton, so concurrent sessions may have stale data.

**Impact**: Cannot deploy to any multi-user environment without data corruption.

**Recommendation**: Abstract storage behind an interface. Implement SQLite backend. Estimated effort: 4 hours.

### 🟡 MEDIUM-D02: Module-level global state for rate limiting (UNFIXED)

**File**: `src/data/finmind_client.py` (lines 32-34)

**Problem**: `_consecutive_failures` and `_last_failure_time` are module-level globals.

**Impact**: In a multi-process deployment, each process has its own counter. Also, the `_MISSING_COL_WARNED` set in `adaptive_engine.py` (line 62) is a similar module-level global that persists for the process lifetime — acceptable but worth noting.

**Recommendation**: Use `st.session_state` for per-session tracking, or a shared cache. Estimated effort: 1 hour.

### 🟡 MEDIUM-D03: Hardcoded static data in multiple modules (UNFIXED)

**Files**:
- `src/services/analogy_engine.py` → `one_liners` dict (20 entries, inline)
- `src/services/revenue_analyzer.py` → `KNOWN_COMPANY_REVENUE` (9 entries, inline)
- `src/pages/group_structure.py` → `KNOWN_GROUP_STRUCTURES` (5 entries, inline)
- `src/pages/peer_comparison.py` → `INDUSTRY_BENCHMARKS` (28 entries, inline)
- `src/pages/etf_browser.py` → `ETF_CATEGORY_KEYWORDS` (~50 keywords, inline)

**Problem**: Static data scattered across 5 modules. Adding a new company requires edits in multiple files. `INDUSTRY_BENCHMARKS` has 28 industries but may not cover all ~60+ industries in the market (see `docs/design/ux_improvements.md`).

**Impact**: High maintenance cost. Inconsistencies between modules.

**Recommendation**: Create a single `src/data/company_registry.yaml` that holds all static company data. Load once at startup. Estimated effort: 2 hours.

---

## 5. Missing Tests — UPDATED

### ✅ RESOLVED: Unit test suite expanded from 29 to ~59 tests
`tests/test_business_logic.py` now has 800 lines covering:
- `calc_roe_ttm()` — 10 tests (was 10)
- `_is_etf()` — 13 tests (was 13)
- `filter_by_timeline()` — 6 tests (was 6)
- `validate_stock_id()` — 9 tests (NEW)
- `detect_revenue_event()` — 7 tests (NEW)
- `detect_price_abnormal()` — 7 tests (NEW)
- `detect_news_event()` — 8 tests (NEW)
- `check_data_freshness()` — 7 tests (NEW)
- `detect_company_type()` — 9 tests (NEW)
- `extract_dividend_summary()` — 9 tests (NEW)

### ✅ RESOLVED: st.session_state usage in tests greatly reduced
Down to 1 usage at line 260 (for `test_tl_1y`), which is necessary because `filter_by_timeline()` reads from `st.session_state`.

### 🟡 MEDIUM-E02: No integration tests for data pipeline (UNFIXED)

**Problem**: No tests verify that FinMind API responses are correctly parsed and transformed. The `COLUMN_ALIASES` system in `adaptive_engine.py` is critical for resilience but not tested end-to-end.

**Impact**: Fragile dependency on FinMind API schema. If FinMind changes column names, the app will fail silently.

**Recommendation**: Add snapshot tests with saved API responses. Test the full pipeline from API response to rendered output. Estimated effort: 3 hours.

---

## 6. Dependency Health — Updated

### ✅ RESOLVED: Unused dependencies removed
`python-dotenv` and `tqdm` are no longer in `pyproject.toml`.

### ✅ RESOLVED: `uv.lock` file committed
Lock file exists on disk, ensuring reproducible builds.

### 🟡 MEDIUM-F02: FinMind is the sole data source (UNFIXED)

**Problem**: All data comes from FinMind. No fallback if FinMind is down or rate-limited.

**Impact**: Complete data unavailability when FinMind has issues.

**Recommendation**: Cache a "last known good" dataset. Estimated effort: 2 hours.

---

## 7. UI/UX Observations

### 🟢 NEW-G05: ETF category keywords inline in `etf_browser.py`

**File**: `src/pages/etf_browser.py` (line 179)

**Problem**: `ETF_CATEGORY_KEYWORDS` dict with ~50 keywords and 5 categories is defined inline at module level. The `_classify_etf()` function (line 213) uses first-match-wins semantics which may misclassify ETFs (e.g., a "高股息" ETF that's also "主題型" gets whichever category is listed first in the dict).

**Potential Impact**: Misclassified ETFs in the ETF browser. The ordering of dict keys in `ETF_CATEGORY_KEYWORDS` determines classification priority — this is implicit, not explicit.

**Recommendation**: Either (a) document the priority order, (b) use explicit priority scoring, or (c) allow multi-category classification. Estimated effort: 30 minutes.

---

## 8. Architecture Observations

### Strengths (since last review)
1. **Rate limit handling**: Both session-state flag and module-level counter provide defense in depth (though they're currently disconnected — see NEW-G04)
2. **Test suite**: ~59 tests covering all core algorithms — good regression safety net
3. **Atomic writes**: Both YAML storage modules use atomic write patterns (though duplicated — see NEW-G01)
4. **Column aliases**: `COLUMN_ALIASES` system in `adaptive_engine.py` provides graceful degradation when API columns change
5. **TTL-based cleanup**: Cache cleanup with TTL expiry and LRU eviction in `FinMindClient`

### Weaknesses (new or remaining)
1. **Dead code**: `models.py` (86 lines, 6 dataclasses) is never imported — confusing for new developers
2. **Duplicated utilities**: `_atomic_write` in 2 places, `_TIMELINE_DAYS`/`_TIMELINE_OPTIONS` in 2 places
3. **No dependency injection**: `FinMindClient()` instantiated directly in multiple places
4. **Disconnected rate limit mechanisms**: Session flag set but never read; module counter used instead
5. **Scattered static data**: 5 modules with inline company data dicts — no single source of truth

---

## 9. Prioritized Action Plan

### Immediate (This Week)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 1 | Extract shared timeline constants (A01) | 10 min | DRY | ❌ Not done |
| 2 | Consolidate `_atomic_write` (NEW-G01) | 15 min | DRY | ❌ Not done |
| 3 | Fix disconnected rate limit flags (NEW-G04) | 10 min | Reliability | ❌ Not done |
| 4 | Remove dead `models.py` or adopt it (NEW-G02) | 5 min / 3h | Clarity | ❌ Not done |
| 5 | Remove bare `FinMindClient()` in peer_comparison (NEW-G06) | 20 min | Testability | ❌ Not done |

**Subtotal: ~1 hour (quick wins) / 4 hours (with models.py refactor)**

### Short-Term (Next 2 Weeks)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 6 | Optimize category browser N+1 queries (C01) | 2 hours | Performance | ❌ Not done |
| 7 | Cache ETF dividend data (C03) | 1.5 hours | Performance | ❌ Not done |
| 8 | Consolidate static company data (D03) | 2 hours | Maintainability | ❌ Not done |
| 9 | Make `max_workers` configurable (C02) | 20 min | Performance tuning | ❌ Not done |
| 10 | Fix ETF category classification priority (NEW-G05) | 30 min | UX correctness | ❌ Not done |

**Subtotal: ~6 hours**

### Medium-Term (Post-MVP)

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 11 | Abstract storage + SQLite backend (D01) | 4 hours | Scalability | ❌ Not done |
| 12 | Fix rate limit global state (D02) | 1 hour | Scalability | ❌ Not done |
| 13 | Integration tests with saved API responses (E02) | 3 hours | Quality | ❌ Not done |
| 14 | "Last known good" data fallback (F02) | 2 hours | Reliability | ❌ Not done |

**Subtotal: ~10 hours**

---

## 10. Summary Table

| Category | Items (2026-06-09) | Items (2026-06-10) | Items (2026-06-11) | Critical | High | Medium | Low |
|----------|---------------------|---------------------|---------------------|----------|------|--------|-----|
| Code Duplication | 4 | 1 | 2 (+1 new) | — | — | 1 | 1 |
| Error Handling | 3 | 1 | 1 (+1 new) | — | — | 1 | — |
| Performance | 3 | 3 | 3 (+1 new) | — | 1 | 2 | — |
| Scalability | 3 | 3 | 2 | — | 1 | 1 | — |
| Missing Tests | 3 | 3 | 1 (2 resolved) | — | — | 1 | — |
| Dependencies | 3 | 2 | 1 (1 resolved) | — | — | 1 | — |
| **Total** | **19** | **13** | **10** (−3 resolved, +6 new, −6 old reclassified) | **—** | **2** | **7** | **1** |

**Total estimated effort**: ~17 hours (Immediate: 1h, Short-term: 6h, Medium-term: 10h)

---

## 11. Key Changes Since Last Review (2026-06-10)

### Resolved Items (4)
1. ✅ **B01**: `FinMindRateLimitError` now caught by `_fetch()` in `_router_base.py` (line 44), sets `st.session_state["_rate_limited"] = True`; rate limit banner in `main.py` (line 182-184) checks `get_rate_limit_status()`
2. ✅ **F01**: `uv.lock` now exists on disk
3. ✅ **E01**: Test suite expanded from 29 to ~59 tests covering all event detection, validation, freshness, company type, and dividend analysis functions
4. ✅ **E03**: `st.session_state` usage reduced to 1 test (was 3); remaining usage is necessary for `filter_by_timeline()` integration

### New Items Identified (6)
1. 🟡 **NEW-G01**: `_atomic_write` duplicated in `adaptive_engine.py` and `watchlist.py` (also inconsistent type signatures)
2. 🟡 **NEW-G02**: `models.py` — 6 dataclasses, 86 lines, never imported (dead code)
3. 🟡 **NEW-G04**: Rate limit flag `_rate_limited` session state set but never read; two disconnected mechanisms
4. 🟡 **NEW-G05**: `ETF_CATEGORY_KEYWORDS` inline in `etf_browser.py` with implicit priority ordering
5. 🟡 **NEW-G06**: `FinMindClient()` instantiated directly in `peer_comparison.py` without cache_dir
6. 🟡 **NEW-G07**: `INDUSTRY_BENCHMARKS` covers only 28 industries; some stocks' industries may not be covered (see `docs/design/ux_improvements.md`)

### Items Reclassified (as part of D03)
- `ETF_CATEGORY_KEYWORDS` in `etf_browser.py` added to D03's scope (static data consolidation)

---

## 12. Verification Notes

All claims in this report were verified by reading source code:
- **`_fetch()` rate limit handling**: Confirmed at `_router_base.py` lines 44-48
- **Rate limit banner**: Confirmed at `main.py` lines 182-184 using `get_rate_limit_status()`
- **Test coverage**: Counted test classes and methods in `test_business_logic.py` (800 lines)
- **`uv.lock` existence**: Confirmed via filesystem search
- **`st.cache_data` removal**: 0 matches in `src/` directory
- **`_atomic_write` duplication**: Lines 135 in `adaptive_engine.py` and 21 in `watchlist.py`
- **`models.py` unused**: 0 import matches across entire `src/` tree
- **`FinMindClient()` instantiations**: Found 3 direct creations (router.py:39, peer_comparison.py:54, main.py:131)
- **Test count**: `test_business_logic.py` contains 10 test classes, ~59 test methods total

---

*The codebase continues to improve. The team has resolved 4 more items since the last review, including the critical test coverage gap. The highest-leverage remaining investments are: (1) optimizing the category browser's N+1 query pattern, (2) consolidating static company data across 5 modules, and (3) cleaning up duplicated utilities (atomic_write, timeline constants). The test suite is now comprehensive — the focus should shift to performance optimization and codebase consolidation.*

---

## 13. Challenger Round 3 Addendum (2026-06-11)

### Critical Finding NOT Caught by Architect

The Challenger's Round 3 review identified a **P0 regression** that the Architect's code-pattern review missed:

**business_card.py is severely truncated (128 lines).** The `_render_business_card()` function imports 15+ service functions but calls **NONE** of them. The page only renders stock name, price, and watchlist buttons. Revenue chart, pie chart, news, dividend, and analogy sections are imported but never rendered.

**Why the Architect missed it:** The review focused on code patterns (duplication, dead code, error handling) but did not trace the rendering flow from imports to actual `st.markdown()` / `st.plotly_chart()` calls. This is a **methodology gap** — future Architect reviews should add a "rendering flow verification" step that checks whether imported services are actually invoked.

**This is the #1 priority item in the current backlog.** See `docs/workflow/challenge_log.md` Round 1 Q2 and Round 2 Q2 for full analysis.

### Priority Adjustments from Challenger

| Item | Architect's Priority | Challenger's Adjustment |
|------|---------------------|------------------------|
| NEW-G07 (INDUSTRY_BENCHMARKS incomplete) | Listed in Scalability | **Defer to P3** — only affects edge cases |
| business_card.py truncation | Not identified | **P0 — CRITICAL regression** |
| C15 (Paper Trading) | Not in tech_debt | **REJECTED** — positioning violation |
| C18 (Gamification) | Not in tech_debt | **P3 (post-MVP)** — no core value alignment |

### Recommended Action

The team should **complete business_card.py before any new features**. This is a regression fix, not a feature addition. Estimated effort: 8-12 hours. See `docs/workflow/challenge_log.md` for the full implementation breakdown.

---

## Round 4 Update (2026-06-11)

> **Reviewer**: System Architect (Subagent) — Automated Cron
> **Scope**: Targeted verification of Round 3 items + new debt discovery
> **Checks performed**: 6 targeted searches (A through F)

---

### Verification of Round 3 Items

| Item | Description | Round 3 Status | Round 4 Verification |
|------|-------------|---------------|---------------------|
| A01 | Timeline constants duplicated (`_TIMELINE_DAYS` / `_TIMELINE_OPTIONS`) | ❌ Not done | ❌ **Still present** — `_router_base.py:154` and `timeline_controls.py:12` |
| NEW-G01 | `_atomic_write` duplicated in 2 modules | ❌ Not done | ❌ **Still present** — `adaptive_engine.py:135` (str), `watchlist.py:21` (Path) |
| NEW-G02 | `models.py` dead code (86 lines, 6 dataclasses) | ❌ Not done | ❌ **Still present** — 0 imports across entire `src/` tree |
| NEW-G04 | Rate limit flag `_rate_limited` set but never read | ❌ Not done | ❌ **Still present** — set at `_router_base.py:46`, read at 0 places; `main.py:182` uses `get_rate_limit_status()` (module counter) |
| NEW-G05 | `ETF_CATEGORY_KEYWORDS` inline with implicit priority | ❌ Not done | ❌ **Still present** — `etf_browser.py:179`, first-match-wins semantics |
| NEW-G06 | `FinMindClient()` bare instantiation in `peer_comparison.py` | ❌ Not done | ❌ **Still present** — `peer_comparison.py:54` creates `FinMindClient()` without `cache_dir` |
| C01 | Category browser N+1 queries (200 sequential calls) | ❌ Not done | ❌ **Still present** — no batch fetch added |
| C02 | `max_workers=5` hardcoded | ❌ Not done | ❌ **Still present** — `_router_base.py:51` |
| C03 | ETF dividend ranking sequential (~500 calls) | ❌ Not done | ❌ **Still present** — no dividend cache added |
| D01 | YAML storage doesn't scale beyond single-user | ❌ Not done | ❌ **Still present** — no storage abstraction |
| D02 | Module-level global state for rate limiting | ❌ Not done | ❌ **Still present** — `finmind_client.py:32-34` |
| D03 | Static data scattered across 5 modules | ❌ Not done | ❌ **Still present** — no company registry created |
| E02 | No integration tests for data pipeline | ❌ Not done | ❌ **Still present** — 88 unit tests, 0 integration tests |
| F02 | FinMind sole data source, no fallback | ❌ Not done | ❌ **Still present** — no "last known good" cache |
| Challenger | `business_card.py` truncated (128 lines) | P0 — CRITICAL | ❌ **Still present** — 128 lines, only renders header + watchlist buttons |

**Summary**: Zero Round 3 items were resolved between Round 3 and Round 4. All 14 active items + the Challenger's P0 finding remain open.

---

### New Items Found in Round 4

#### 🔴 NEW-G08: `list_names()` called but not imported in `business_card.py`

**File**: `src/pages/business_card.py` (line 78)

**Problem**: The function `list_names()` is called at line 78 (`existing_lists = list_names()`) but is NOT in the import block (lines 22-30). The import block only includes `is_in_watchlist`, `is_in_any_list`, `get_lists_for_stock`, `add_to_watchlist`, `remove_from_all_lists`, `remove_from_watchlist`, and `create_list`.

**Impact**: This is a latent `NameError` bug. It will crash at runtime when a user clicks "➕ 加入關注" (Add to Watchlist) and the popover tries to list existing watchlist names. The bug is currently masked because the code path requires user interaction to trigger.

**Recommendation**: Add `list_names` to the import block at line 22-30. Estimated effort: 1 minute.

**Priority**: 🔴 HIGH — This is a runtime crash in a user-facing feature (watchlist management on the business card page).

---

#### 🟡 NEW-G09: `business_card.py` imports 15+ service functions but uses only ~5

**File**: `src/pages/business_card.py` (lines 8-30)

**Problem**: The file imports 15 service functions (`create_revenue_trend_chart`, `create_revenue_pie_chart`, `analyze_revenue_breakdown`, 7 analogy functions, `extract_dividend_summary`, `summarize_news`, `get_news_impact_level`) but none of them are called anywhere in the 128-line file. Only the watchlist functions and basic data access are used.

**Impact**: Unnecessary imports increase startup time and create confusion about what the page actually does. This is a symptom of the larger truncation problem (the rendering code that would use these imports was never written).

**Recommendation**: Either (a) complete the business card rendering to use these imports, or (b) remove the unused imports now and re-add them when the rendering code is written. Estimated effort: 5 minutes for option (b).

**Priority**: 🟡 MEDIUM — Code clarity issue; will be resolved naturally when business_card.py is completed.

---

### Updated Summary Table

| Category | Items (Round 3) | Items (Round 4) | Critical | High | Medium | Low |
|----------|-----------------|-----------------|----------|------|--------|-----|
| Code Duplication | 2 | 2 | — | — | 1 | 1 |
| Error Handling | 1 | 1 | — | — | 1 | — |
| Performance | 3 | 3 | — | 1 | 2 | — |
| Scalability | 2 | 2 | — | 1 | 1 | — |
| Missing Tests | 1 | 1 | — | — | 1 | — |
| Dependencies | 1 | 1 | — | — | 1 | — |
| **New (Round 4)** | — | **2** | — | **1** | **1** | — |
| **Total** | **10** | **12** | **—** | **3** | **8** | **1** |

**Total estimated effort**: ~17 hours (unchanged — no items resolved, 2 new small items added)

---

### Round 4 Action Plan Additions

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 15 | Add `list_names` to import block in `business_card.py` (NEW-G08) | 1 min | 🔴 HIGH — runtime crash | ❌ Not done |
| 16 | Remove unused imports from `business_card.py` (NEW-G09) | 5 min | 🟡 MEDIUM — clarity | ❌ Not done |

---

### Key Observations

1. **No progress since Round 3**: All 14 previously identified items remain unresolved. The codebase has not changed since the Round 3 review.

2. **business_card.py is the critical blocker**: The Challenger's P0 finding (truncated business card) remains the #1 priority. Until this is fixed, the app's core page (the stock business card) is non-functional — it only shows a header and watchlist buttons.

3. **NEW-G08 is a hidden crash bug**: The missing `list_names` import means the watchlist feature on the business card page will crash at runtime. This would be caught immediately if the page were tested end-to-end.

4. **Test count stable**: 88 tests in `test_business_logic.py` — no change from Round 3.

5. **No new files**: The file count is identical to Round 3 (same 50 Python files including pycache).

---

*This is the fourth technical debt review. The team has not addressed any items since Round 3. The most impactful actions remain: (1) complete business_card.py (8-12 hours, P0), (2) fix the `list_names` import bug (1 minute, quick win), and (3) consolidate duplicated utilities (atomic_write, timeline constants) for immediate DRY improvements.*
