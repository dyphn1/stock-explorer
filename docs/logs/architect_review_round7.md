# Technical Debt Review — Round 7 (2026-06-12)

> **Reviewer**: PM (coordinating Architect analysis)
> **Date**: 2026-06-12
> **Scope**: Full codebase review (31 Python source files, ~6,500+ LOC)
> **Previous rounds**: R1–R6 found 19+ items, nearly all still open

---

## Executive Summary

This is the **seventh** technical debt review. The codebase has seen significant feature development (C01, C16, DR-01, DR-03) but **zero** tech debt items have been resolved in the last 5 review rounds. This round re-verifies all items and searches for new debt.

**Round 7 Result**: **Zero** previously identified items were resolved since Round 6. **3 new items** identified.

---

## Verification of Previous Items

| # | Item | Description | R6 Status | R7 Verification |
|---|------|-------------|-----------|-----------------|
| A01 | Timeline constants duplicated | `_TIMELINE_DAYS` / `_TIMELINE_OPTIONS` | ❌ Open | ❌ **STILL OPEN** — `_router_base.py:154` and `timeline_controls.py:12` |
| G01 | `_atomic_write` duplicated | `adaptive_engine.py` (str) vs `watchlist.py` (Path) | ❌ Open | ❌ **STILL OPEN** — `adaptive_engine.py:135` and `watchlist.py:21` |
| G02 | `models.py` dead code | 6 dataclasses, 86 lines, 0 imports | ❌ Open | ❌ **STILL OPEN** — confirmed 0 imports across `src/` |
| G04 | Rate limit flag disconnected | `_rate_limited` set but never read | ❌ Open | ❌ **STILL OPEN** — set at `_router_base.py:46`, read at 0 places |
| G05 | `ETF_CATEGORY_KEYWORDS` inline | Implicit first-match-wins priority | ❌ Open | ❌ **STILL OPEN** — `etf_browser.py:179` |
| G06 | Bare `FinMindClient()` in peer_comparison | No cache_dir | ❌ Open | ❌ **STILL OPEN** — `peer_comparison.py:54` |
| C01 | Category browser N+1 queries | 200 sequential calls per section | ❌ Open | ❌ **STILL OPEN** — `category_browser.py:68-89,205-226` |
| C02 | `max_workers=5` hardcoded | `_router_base.py:51` | ❌ Open | ❌ **STILL OPEN** |
| C03 | ETF dividend ranking sequential | ~500 calls, no dividend cache | ❌ Open | ❌ **STILL OPEN** — `etf_browser.py:346-407` |
| D01 | YAML storage doesn't scale | No storage abstraction | ❌ Open | ❌ **STILL OPEN** |
| D02 | Module-level global state | `finmind_client.py:32-34` | ❌ Open | ❌ **STILL OPEN** |
| D03 | Static data scattered | 5+ modules with inline dicts | ❌ Open | ❌ **STILL OPEN** |
| E02 | No integration tests | Only unit tests | ❌ Open | ❌ **STILL OPEN** — `tests/` has 1 file |
| F02 | No "last known good" fallback | FinMind sole source | ❌ Open | ❌ **STILL OPEN** |
| G10 | `get_list_entries()` dead code | Never called | ❌ Open | ❌ **STILL OPEN** — `watchlist.py:342` |
| G11 | `INDUSTRY_REVENUE_MAP` dead code | Never referenced | ❌ Open | ❌ **STILL OPEN** — `revenue_analyzer.py:11` |
| G12 | `_section_card` unused | `operation_checkup.py:135` | ❌ Open | ❌ **STILL OPEN** |
| G13 | `_MISSING_COL_WARNED` unbounded | Module-level set grows | ❌ Open | ⚠️ **ACCEPT FOR MVP** |
| G14 | `_is_etf()` logic duplicated | `watchlist.py` vs `adaptive_engine.py` | ❌ Open | ❌ **STILL OPEN** — `adaptive_engine.py:437-460` has inline 2-tier logic that doesn't call `watchlist._is_etf()` |

**Summary**: Zero items resolved since Round 6. All 19 previously identified items remain open.

---

## NEW Items Found in Round 7

### 🟢 NEW-G15: `FinMindClient()` bare instantiation in `peer_comparison.py` creates second cache directory

**File**: `src/pages/peer_comparison.py:54`

**Problem**: Already tracked as G06, but the impact is worse than documented. The bare `FinMindClient()` creates a **second** `.cache/` directory at the project root level, separate from the one created by the router's client. This means:
1. Cache entries are duplicated across two directories
2. The second cache has no TTL cleanup (only the router's client calls `_cleanup_cache()` on init)
3. Rate limit tracking is per-process but cache is split, reducing cache hit rate

**Severity**: Medium — wastes disk space and reduces cache effectiveness.

**Effort**: 20 minutes — pass `cache_dir` parameter or use singleton pattern.

---

### 🟡 NEW-G16: `detect_company_type()` in `adaptive_engine.py` has inverted ETF detection logic

**File**: `src/services/adaptive_engine.py:447`

**Problem**: The condition `if "etf" in industry.lower() or industry == "":` returns `"etf"` when `industry` is **empty string**. This means any stock with a missing/empty `industry_category` is classified as ETF. The correct logic should be `and industry != ""` — only classify as ETF when industry explicitly contains "etf".

**Impact**: Stocks with missing industry data are routed to the ETF analysis framework, showing wrong content.

**Severity**: High — causes incorrect analysis framework for any stock with missing industry data.

**Effort**: 5 minutes — change `or industry == ""` to `and industry != ""`.

---

### 🟢 NEW-G17: `revenue_analyzer.py` has 39-line dead dict + 186-line file with only 2 functions

**File**: `src/services/revenue_analyzer.py`

**Problem**: The file is 186 lines. `INDUSTRY_REVENUE_MAP` (lines 11-49, 39 lines) is dead code. The remaining `analyze_revenue_breakdown()` and `_parse_financial_for_segments()` functions are only used by `business_card.py`. The file could be significantly simplified.

**Severity**: Low — code clarity issue.

**Effort**: 1 minute to remove dead dict.

---

## Updated Summary Table

| Category | Items | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Code Duplication | 4 | — | — | 1 | 3 |
| Error Handling | 1 | — | — | 1 | — |
| Performance | 3 | — | 1 | 2 | — |
| Scalability | 2 | — | 1 | 1 | — |
| Missing Tests | 1 | — | — | 1 | — |
| Dependencies | 1 | — | — | 1 | — |
| Dead/Unused Code | 5 | — | — | — | 5 |
| Logic Bugs | 1 | — | 1 | — | — |
| **Total** | **18** | **—** | **3** | **8** | **7** |

**Total estimated effort**: ~19 hours for original items + ~0.5 hours for NEW items = **~19.5 hours**

---

## Architecture Observations

### Strengths
1. **Comprehensive test suite**: 50+ test methods in `test_business_logic.py` covering core algorithms
2. **Rate limit defense**: Session-state flag + module-level counter (though disconnected — G04)
3. **Atomic writes**: Both YAML storage modules use atomic write patterns (though duplicated — G01)
4. **Column alias system**: `COLUMN_ALIASES` in `adaptive_engine.py` provides graceful degradation
5. **Business card fully restored**: 462 lines with all rendering sections
6. **Design system compliance improved**: DR-01 color violations fully resolved, gradients eliminated
7. **File locking**: Both `watchlist.py` and `adaptive_engine.py` use `filelock.FileLock` for concurrent access

### Weaknesses
1. **Zero tech debt velocity**: 7 consecutive review rounds with zero items resolved
2. **Dead code proliferation**: `models.py` (86 lines), `get_list_entries()` (4 lines), `INDUSTRY_REVENUE_MAP` (39 lines), `_section_card` (3 lines) = 132+ lines of dead code
3. **ETF detection bug**: `detect_company_type()` inverts empty-industry logic (NEW-G16)
4. **No integration tests**: Unit tests cover algorithms but not the data pipeline end-to-end
5. **Scattered static data**: 5+ modules with inline dicts
6. **Disconnected rate limit mechanisms**: Session-state flag vs module-level counter

---

## Prioritized Action Plan

### Immediate (This Week) — ~1 hour

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 1 | Fix `detect_company_type()` ETF logic (NEW-G16) | 5 min | **BUG** | ❌ |
| 2 | Extract shared timeline constants (A01) | 10 min | DRY | ❌ |
| 3 | Consolidate `_atomic_write` (G01) | 15 min | DRY | ❌ |
| 4 | Fix disconnected rate limit flags (G04) | 10 min | Reliability | ❌ |
| 5 | Remove dead `models.py` (G02) | 5 min | Clarity | ❌ |
| 6 | Fix bare `FinMindClient()` in peer_comparison (G06) | 20 min | Testability | ❌ |
| 7 | Remove dead `get_list_entries()` (G10) | 2 min | Clarity | ❌ |
| 8 | Remove dead `INDUSTRY_REVENUE_MAP` (G11) | 1 min | Clarity | ❌ |
| 9 | Remove dead `_section_card` (G12) | 1 min | Clarity | ❌ |
| 10 | Deduplicate `_is_etf()` (G14) | 5 min | Consistency | ❌ |

### Short-Term (Next 2 Weeks) — ~6 hours

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 11 | Optimize category browser N+1 queries (C01) | 2 hours | Performance | ❌ |
| 12 | Cache ETF dividend data (C03) | 1.5 hours | Performance | ❌ |
| 13 | Consolidate static company data (D03) | 2 hours | Maintainability | ❌ |
| 14 | Make `max_workers` configurable (C02) | 20 min | Performance | ❌ |
| 15 | Fix ETF category classification (G05) | 30 min | UX | ❌ |

### Medium-Term (Post-MVP) — ~10 hours

| # | Item | Effort | Priority | Status |
|---|------|--------|----------|--------|
| 16 | Abstract storage + SQLite backend (D01) | 4 hours | Scalability | ❌ |
| 17 | Fix rate limit global state (D02) | 1 hour | Scalability | ❌ |
| 18 | Integration tests (E02) | 3 hours | Quality | ❌ |
| 19 | "Last known good" fallback (F02) | 2 hours | Reliability | ❌ |

---

*This is the seventh technical debt review. Zero items resolved since Round 6. Three new items identified (1 logic bug, 1 cache issue, 1 dead code). Total debt: 18 items (~19.5 hours). The team has not addressed any tech debt in 7 review rounds — a dedicated cleanup sprint is strongly recommended.*
