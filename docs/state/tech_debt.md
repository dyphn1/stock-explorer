# Stock Explorer Technical Debt Report

> **Date**: 2026-06-12
> **Reviewer**: System Architect (Subagent)
> **Scope**: Full codebase review (31 Python source files, ~6,200 LOC excluding tests)
> **Context**: Previous reviews: R1 2026-06-09 (19 items), R2 2026-06-10 (13 items), R3 2026-06-10 (14 items, 6 new), R4 2026-06-11 (14 items verified — ALL still open, 2 NEW found+fixed). This is Round 5.

---

## Executive Summary

This is the **fifth** technical debt review. Round 4 confirmed all 14 items were still open with zero progress and found NEW-G08 and NEW-G09 (both fixed the same day). This round re-verifies all items and searches for new debt.

**Round 5 Result**: **Zero** Round 4 items were resolved. However, **5 new items** were identified through deeper analysis of dead code, unused functions, and patterns not caught in previous rounds.

---

## Verification of Round 4 Items

| # | Item | Description | Round 4 Status | Round 5 Verification |
|---|------|-------------|---------------|---------------------|
| A01 | LOW-A01 | Timeline constants duplicated (`_TIMELINE_DAYS` / `_TIMELINE_OPTIONS`) | ❌ Not done | ❌ **STILL OPEN** — `_router_base.py:154` and `timeline_controls.py:12` both define the same mapping |
| G01 | NEW-G01 | `_atomic_write` duplicated in `adaptive_engine.py` (str) and `watchlist.py` (Path) | ❌ Not done | ❌ **STILL OPEN** — Identical logic at `adaptive_engine.py:135` and `watchlist.py:21` |
| G02 | NEW-G02 | `models.py` dead code — 6 dataclasses, 86 lines, 0 imports | ❌ Not done | ❌ **STILL OPEN** — `rg "from src.data.models|from src.data import models"` returns 0 results |
| G04 | NEW-G04 | Rate limit flag `_rate_limited` session state set but never read | ❌ Not done | ❌ **STILL OPEN** — Set at `_router_base.py:46`; read at 0 places; `main.py:182` uses `get_rate_limit_status()` (module counter) |
| G05 | NEW-G05 | `ETF_CATEGORY_KEYWORDS` inline with implicit first-match-wins priority | ❌ Not done | ❌ **STILL OPEN** — `etf_browser.py:179`, dict ordering determines classification |
| G06 | NEW-G06 | `FinMindClient()` bare instantiation in `peer_comparison.py` without cache_dir | ❌ Not done | ❌ **STILL OPEN** — `peer_comparison.py:54` creates `FinMindClient()` directly |
| C01 | HIGH-C01 | Category browser N+1 queries (200 sequential calls per section) | ❌ Not done | ❌ **STILL OPEN** — `category_browser.py:68-89,205-226` loops over stocks sequentially |
| C02 | MEDIUM-C02 | `max_workers=5` hardcoded in `_router_base.py:51` | ❌ Not done | ❌ **STILL OPEN** — No configurable parameter |
| C03 | MEDIUM-C03 | ETF dividend ranking sequential (~500 calls, no dividend cache) | ❌ Not done | ❌ **STILL OPEN** — `etf_browser.py:346-407` loops over ETFs calling `client.get_dividend(sid)` |
| D01 | HIGH-D01 | YAML storage doesn't scale beyond single-user | ❌ Not done | ❌ **STILL OPEN** — No storage abstraction layer |
| D02 | MEDIUM-D02 | Module-level global state for rate limiting (`finmind_client.py:32-34`) | ❌ Not done | ❌ **STILL OPEN** — `_consecutive_failures` is module-level global |
| D03 | MEDIUM-D03 | Static data scattered across 5 modules | ❌ Not done | ❌ **STILL OPEN** — `analogy_engine`, `revenue_analyzer`, `group_structure`, `peer_comparison`, `etf_browser` all have inline dicts |
| E02 | MEDIUM-E02 | No integration tests for data pipeline | ❌ Not done | ❌ **STILL OPEN** — `tests/` has 1 file (`test_business_logic.py`), 0 integration tests |
| F02 | MEDIUM-F02 | FinMind sole data source, no "last known good" fallback | ❌ Not done | ❌ **STILL OPEN** — No fallback mechanism |
| — | Challenger | `business_card.py` truncation (NEW-G08, NEW-G09) | ✅ Fixed | ✅ **CONFIRMED** — `business_card.py` is 370 lines, all imports used, `list_names` imported |

**Summary**: Zero items resolved since Round 4. All 14 previously identified items remain open.

---

## NEW Items Found in Round 5

### 🟢 NEW-G10: `get_list_entries()` is dead code — never called outside its definition

**File**: `src/services/watchlist.py` (line 342)

**Problem**: The function `get_list_entries()` is defined at line 342 as `return load_watchlist(list_name)` — a trivial alias for `load_watchlist()`. It is never imported or called by any other file. `load_watchlist()` is used directly everywhere.

**Impact**: Unnecessary function definition. Confusing for developers — two names for the same operation.

**Recommendation**: Remove `get_list_entries()` and its type signature. Or, if the intent was to provide a public API alias, add a comment explaining why it exists. Estimated effort: 2 minutes.

---

### 🟢 NEW-G11: `INDUSTRY_REVENUE_MAP` in `revenue_analyzer.py` is dead code — never referenced

**File**: `src/services/revenue_analyzer.py` (lines 11-49)

**Problem**: The dict `INDUSTRY_REVENUE_MAP` (39 lines of industry-to-business-line keyword mappings) is defined at module level but never referenced in any function body. The `analyze_revenue_breakdown()` function checks `KNOWN_COMPANY_REVENUE` and `_parse_financial_for_segments()` but never uses `INDUSTRY_REVENUE_MAP`.

**Impact**: 39 lines of dead dict data increases module size by ~50%. Confusing for developers who may think this data is being used.

**Recommendation**: Either (a) refactor `_parse_financial_for_segments()` to use this mapping for the keyword scoring logic, or (b) remove it. Estimated effort: option (a) 1 hour, option (b) 1 minute.

---

### 🟢 NEW-G12: `_section_card` assigned but never used in `operation_checkup.py`

**File**: `src/pages/operation_checkup.py` (line 135)

**Problem**: The variable `_section_card` is assigned a CSS HTML template string at line 135 but is never referenced again in the function or module. The actual rendering at line 168-175 uses an inline `st.markdown(f"""...""")` with the same gradient pattern but different content. The dead assignment appears to be a leftover from refactoring.

**Impact**: 1 line of dead code. Minor clarity issue.

**Recommendation**: Remove lines 135-137. Estimated effort: 1 minute.

---

### 🟡 NEW-G13: `_MISSING_COL_WARNED` set grows unboundedly per process

**File**: `src/services/adaptive_engine.py` (line 62)

**Problem**: The module-level `_MISSING_COL_WARNED: set[str] = set()` prevents repeated log warnings for missing columns. While it prevents log spam, the set grows monotonically for the lifetime of the process. In a long-running Streamlit session with many different stocks, if different stocks trigger different missing columns, this set will keep growing.

**Impact**: Minor memory issue in long-running sessions. Not a real problem for typical usage (the set will be small), but an architectural smell — module-level mutable state that persists across user interactions.

**Recommendation**: Acceptable for current single-user scope. If multi-user deployment is planned (D01), consider using `st.session_state` or an LRU-bounded cache. Estimated effort: defer with D01.

**Priority**: 🟡 LOW — Acceptable for MVP.

---

### 🟡 NEW-G14: `_is_etf()` logic duplicated between `watchlist.py` and `detect_company_type()` in `adaptive_engine.py`

**Files**:
- `src/services/watchlist.py` (line 91) — `_is_etf(stock_id, name, industry_category)` with 3-tier detection
- `src/services/adaptive_engine.py` (line 398-405) — `detect_company_type()` has inline ETF detection

**Problem**: The ETF detection logic exists in two places with different implementations:
- `watchlist.py`: 3-tier detection (industry_category → name keywords → stock_id pattern)
- `adaptive_engine.py`: 2-tier detection (industry_category → stock_id "00" prefix pattern only)

The `detect_company_type()` function (line 398) doesn't call `_is_etf()` from `watchlist.py` — it has its own simplified inline logic that would miss ETFs whose only distinguishing feature is name-based (e.g., a "高股息" stock with industry_category that doesn't contain "etf").

**Impact**: Inconsistent ETF detection. `detect_company_type()` may fail to detect name-based ETFs that `_is_etf()` would catch. This matters for the adaptive analysis framework banner on `business_card.py`.

**Recommendation**: Have `detect_company_type()` call `watchlist._is_etf()` instead of duplicating logic. Estimated effort: 5 minutes.

---

## Updated Summary Table

| Category | R3 Items | R4 Items | R5 Items | Critical | High | Medium | Low |
|----------|----------|----------|----------|----------|------|--------|-----|
| Code Duplication | 2 | 2 | 3 (+1 new) | — | — | 1 | 2 |
| Error Handling | 1 | 1 | 1 | — | — | 1 | — |
| Performance | 3 | 3 | 3 | — | 1 | 2 | — |
| Scalability | 2 | 2 | 2 | — | 1 | 1 | — |
| Missing Tests | 1 | 1 | 1 | — | — | 1 | — |
| Dependencies | 1 | 1 | 1 | — | — | 1 | — |
| Dead/Unused Code | — | — | **4** (3 new) | — | — | — | 4 |
| **Total** | **10** | **10\*** | **15** (+5 new) | **—** | **2** | **8** | **5** |

\* R4 and R3 had 10 active items each (the R3 table undercounted due to Challenger additions).

**Total estimated effort**: ~17 hours for original items + ~2 hours for NEW items = **~19 hours**
(Immediate quick wins: 15 min, Short-term: 6h, Medium-term: 10h, NEW items: ~2h)

---

## Updated Prioritized Action Plan

### Immediate (This Week) — ~1 hour

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 1 | Extract shared timeline constants (A01) | 10 min | DRY | ❌ Not done |
| 2 | Consolidate `_atomic_write` (NEW-G01) | 15 min | DRY | ❌ Not done |
| 3 | Fix disconnected rate limit flags (NEW-G04) | 10 min | Reliability | ❌ Not done |
| 4 | Remove dead `models.py` or adopt it (NEW-G02) | 5 min / 3h | Clarity | ❌ Not done |
| 5 | Remove bare `FinMindClient()` in peer_comparison (NEW-G06) | 20 min | Testability | ❌ Not done |
| 6 | Remove dead `get_list_entries()` (NEW-G10) | 2 min | Clarity | ❌ Not done |
| 7 | Remove dead `INDUSTRY_REVENUE_MAP` (NEW-G11) | 1 min | Clarity | ❌ Not done |
| 8 | Remove dead `_section_card` (NEW-G12) | 1 min | Clarity | ❌ Not done |
| 9 | Deduplicate `_is_etf()` into `detect_company_type()` (NEW-G14) | 5 min | Consistency | ❌ Not done |

### Short-Term (Next 2 Weeks) — ~6 hours

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 10 | Optimize category browser N+1 queries (C01) | 2 hours | Performance | ❌ Not done |
| 11 | Cache ETF dividend data (C03) | 1.5 hours | Performance | ❌ Not done |
| 12 | Consolidate static company data (D03) | 2 hours | Maintainability | ❌ Not done |
| 13 | Make `max_workers` configurable (C02) | 20 min | Performance tuning | ❌ Not done |
| 14 | Fix ETF category classification priority (G05) | 30 min | UX correctness | ❌ Not done |

### Medium-Term (Post-MVP) — ~10 hours

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 15 | Abstract storage + SQLite backend (D01) | 4 hours | Scalability | ❌ Not done |
| 16 | Fix rate limit global state (D02) | 1 hour | Scalability | ❌ Not done |
| 17 | Integration tests with saved API responses (E02) | 3 hours | Quality | ❌ Not done |
| 18 | "Last known good" data fallback (F02) | 2 hours | Reliability | ❌ Not done |

### Monitoring / Defer

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 19 | Bound `_MISSING_COL_WARNED` set (NEW-G13) | Defer with D01 | Low | ❌ Accept for MVP |

---

## Architecture Observations

### Strengths (unchanged since Round 4)
1. **Comprehensive test suite**: 800-line `test_business_logic.py` with 10 test classes — covers all core algorithms
2. **Rate limit defense in depth**: Session-state flag + module-level counter (though disconnected — NEW-G04)
3. **Atomic writes**: Both YAML storage modules use atomic write patterns (though duplicated — NEW-G01)
4. **Column aliases**: `COLUMN_ALIASES` system in `adaptive_engine.py` provides graceful degradation
5. **Business card fully restored**: 370 lines with all 7 rendering sections (R4 Challenger fix)
6. **URL sync**: Robust `sync_url_to_session()`/`navigate_to()` pattern for browser back/forward

### Weaknesses (new or remaining)
1. **Dead code proliferation**: `models.py` (86 lines), `get_list_entries()` (4 lines), `INDUSTRY_REVENUE_MAP` (39 lines), `_section_card` (3 lines) = 132+ lines of dead code
2. **No ETF detection unification**: `watchlist._is_etf()` and `adaptive_engine.detect_company_type()` have diverged
3. **Scattered static data**: 5+ modules with inline dicts adding up to hundreds of lines of duplicated/unstructured data
4. **Zero tech debt velocity**: 5 consecutive review rounds with zero items resolved. The team is focused on features, not maintenance.
5. **No integration tests**: The 800-line test file covers unit logic but not the data pipeline end-to-end

---

## Verification Notes

All claims verified by reading source code:
- **`_TIMELINE_DAYS` / `_TIMELINE_OPTIONS`**: Confirmed at `_router_base.py:154` and `timeline_controls.py:12` — identical `{"1Y": 365, "3Y": 1095, "5Y": 1825, "ALL": None}` mapping
- **`_atomic_write` duplication**: Confirmed at `adaptive_engine.py:135` (accepts `str`) and `watchlist.py:21` (accepts `Path`)
- **`models.py` unused**: `rg "from src.data.models|from src.data import models"` returns 0 results across entire `src/` tree
- **`_rate_limited` set but never read**: Set at `_router_base.py:46`; `rg "_rate_limited"` returns only that 1 match; `main.py:182` uses `get_rate_limit_status()`
- **`FinMindClient()` bare instantiation**: Confirmed at `peer_comparison.py:54` — `client = FinMindClient()` without `cache_dir`
- **`get_list_entries` unused**: Defined at `watchlist.py:342`; `rg "get_list_entries"` returns only the definition (1 match)
- **`INDUSTRY_REVENUE_MAP` unused**: Defined at `revenue_analyzer.py:11`; `rg "INDUSTRY_REVENUE_MAP"` returns only the definition (1 match)
- **`_section_card` unused**: Assigned at `operation_checkup.py:135`; never referenced again in the file
- **`_is_etf` divergence**: `watchlist.py:91` has 3-tier detection; `adaptive_engine.py:398-405` has 2-tier inline logic that doesn't call `watchlist._is_etf()`
- **Test count**: `test_business_logic.py` is 800 lines, 10 test classes, ~59 test methods — no integration tests
- **No new files**: Same 31 Python files as Round 4 (excluding `__pycache__`)

---

*This is the fifth technical debt review. Zero items have been resolved since Round 4. Five new items were identified (3 dead code, 1 unbounded set, 1 logic duplication). The total debt stands at 19 items (~19 hours). The most impactful remaining investments are: (1) optimizing the category browser's N+1 query pattern, (2) consolidating static company data, (3) cleaning up dead code (132+ lines), and (4) fixing the disconnected rate limit mechanisms. The team has not addressed any tech debt in 5 review rounds — a dedicated cleanup sprint is recommended.*
