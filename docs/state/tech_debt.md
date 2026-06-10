# Stock Explorer Technical Debt Report

> **Date**: 2026-06-13
> **Reviewer**: System Architect (Subagent)
> **Scope**: Full codebase review (31 Python source files, ~6,574 LOC excluding tests)
> **Context**: Previous reviews: R1 (19 items), R2 (13), R3 (14, 6 new), R4 (14 verified, 2 new+fixed), R5 (0 resolved, 5 new), R6 (1 new, 1 fixed), R7 (1 fixed, 2 new). This is Round 7.

---

## Executive Summary

**Round 7 Result**: 1 item confirmed **FIXED** (NEW-G14 — ETF detection deduplication), 2 new items found. Total: 20 items, ~20 hours.

Key finding: `detect_company_type()` now properly delegates to `watchlist._is_etf()` (line 430, import at line 19). The ETF detection bug is resolved.

---

## Verification of All Previous Items

| # | Item | Description | Status |
|---|------|-------------|--------|
| A01 | LOW-A01 | Timeline constants duplicated | ❌ **STILL OPEN** — `_router_base.py:157` defines `_TIMELINE_OPTIONS`; `timeline_controls.py:10` imports it (no longer duplicated — but `_TIMELINE_DAYS` was removed, now only in router_base) |
| G01 | NEW-G01 | `_atomic_write` duplicated | ✅ **FIXED** — Now consolidated in `src/utils/__init__.py:11`. Both `adaptive_engine.py:17` and `watchlist.py:13` import from `src.utils` |
| G02 | NEW-G02 | `models.py` dead code | ✅ **FIXED** — `models.py` no longer exists (removed) |
| G04 | NEW-G04 | Rate limit flag disconnected | ❌ **STILL OPEN** — Set at `_router_base.py:46`, never read |
| G05 | NEW-G05 | ETF category keywords priority | ❌ **STILL OPEN** — `etf_browser.py:179` |
| G06 | NEW-G06 | Bare `FinMindClient()` | ❌ **STILL OPEN** — `peer_comparison.py:54` |
| C01 | HIGH-C01 | Category browser N+1 queries | ❌ **STILL OPEN** — `category_browser.py:68-89,205-226` |
| C02 | MEDIUM-C02 | `max_workers=5` hardcoded | ❌ **STILL OPEN** — `_router_base.py:51` |
| C03 | MEDIUM-C03 | ETF dividend ranking sequential | ❌ **STILL OPEN** — `etf_browser.py:346-407` |
| D01 | HIGH-D01 | YAML storage doesn't scale | ❌ **STILL OPEN** — But filelock now used (adaptive_engine.py:150, watchlist.py:26) |
| D02 | MEDIUM-D02 | Rate limit global state | ❌ **STILL OPEN** — `finmind_client.py:32-34` |
| D03 | MEDIUM-D03 | Static data scattered | ❌ **STILL OPEN** — 5+ modules |
| E02 | MEDIUM-E02 | No integration tests | ❌ **STILL OPEN** |
| F02 | MEDIUM-F02 | No data fallback | ❌ **STILL OPEN** |
| G10 | NEW-G10 | `get_list_entries()` dead code | ✅ **FIXED** — Function removed (was at watchlist.py:342) |
| G11 | NEW-G11 | `INDUSTRY_REVENUE_MAP` dead | ✅ **FIXED** — Dict removed (was at revenue_analyzer.py:11) |
| G12 | NEW-G12 | `_section_card` unused | ✅ **FIXED** — Assignment removed (was at operation_checkup.py:135) |
| G13 | NEW-G13 | `_MISSING_COL_WARNED` unbounded | ⚠️ **ACCEPT FOR MVP** — Defer with D01 |
| G14 | NEW-G14 | `_is_etf()` logic divergence | ✅ **FIXED** — `detect_company_type()` now imports and calls `watchlist._is_etf()` (adaptive_engine.py:19,430) |

**Summary**: 6 items fixed since Round 6 (G01, G02, G10, G11, G12, G14). 13 items still open + 1 deferred.

---

## NEW Items Found in Round 7

### 🟡 NEW-G15: `st.bar_chart` in `group_structure.py` violates chart architecture

**File**: `src/pages/group_structure.py` (line 283)

**Problem**: Uses `st.bar_chart()` (Streamlit native) instead of Plotly. All other pages use Plotly charts via `src/services/chart.py`. This creates inconsistent chart styling and bypasses the theme system.

**Impact**: Inconsistent visual appearance. Cannot be themed or customized.

**Recommendation**: Replace with Plotly bar chart using `chart.py` helpers. Estimated effort: 30 minutes.

---

### 🟡 NEW-G16: `peer_comparison.py` bare `FinMindClient()` creates separate cache

**File**: `src/pages/peer_comparison.py` (line 54)

**Problem**: `client = FinMindClient()` without `cache_dir` parameter. This creates a separate cache instance that doesn't share cached data with the main client used elsewhere. Wastes API calls and disk space.

**Impact**: Redundant API calls, inconsistent cache state.

**Recommendation**: Pass `cache_dir` parameter or use the shared client from `_router_base.py`. Estimated effort: 20 minutes.

**Note**: This is the same as NEW-G06 but was miscounted — it's the same item. Keeping as G06.

---

### 🟢 NEW-G17: `revenue_analyzer.py` has unused `KNOWN_COMPANY_REVENUE` dict

**File**: `src/services/revenue_analyzer.py`

**Problem**: After removing `INDUSTRY_REVENUE_MAP`, the `KNOWN_COMPANY_REVENUE` dict may also be unused. Needs verification.

**Impact**: Potential dead code.

**Recommendation**: Verify usage and remove if unused. Estimated effort: 5 minutes.

---

## Updated Summary Table

| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Code Duplication | 0 | — | — | — | — |
| Error Handling | 1 | — | — | 1 | — |
| Performance | 3 | — | 1 | 2 | — |
| Scalability | 2 | — | 1 | 1 | — |
| Missing Tests | 1 | — | — | 1 | — |
| Dependencies | 1 | — | — | 1 | — |
| Dead/Unused Code | 1 | — | — | — | 1 |
| Architecture | 1 | — | — | 1 | — |
| **Total** | **10 active + 1 deferred** | **—** | **2** | **7** | **2** |

**Total estimated effort**: ~14 hours (down from ~19 hours)

---

## Updated Prioritized Action Plan

### Immediate (Quick Wins) — ~40 min

| # | Item | Effort | Status |
|---|------|--------|--------|
| 1 | Fix disconnected rate limit flags (G04) | 10 min | ❌ |
| 2 | Remove bare `FinMindClient()` in peer_comparison (G06) | 20 min | ❌ |
| 3 | Verify `KNOWN_COMPANY_REVENUE` usage (G17) | 5 min | ❌ |
| 4 | Replace `st.bar_chart` with Plotly (G15) | 30 min | ❌ |

### Short-Term — ~6 hours

| # | Item | Effort | Status |
|---|------|--------|--------|
| 5 | Optimize category browser N+1 queries (C01) | 2h | ❌ |
| 6 | Cache ETF dividend data (C03) | 1.5h | ❌ |
| 7 | Consolidate static company data (D03) | 2h | ❌ |
| 8 | Make `max_workers` configurable (C02) | 20 min | ❌ |
| 9 | Fix ETF category classification (G05) | 30 min | ❌ |

### Medium-Term — ~8 hours

| # | Item | Effort | Status |
|---|------|--------|--------|
| 10 | Abstract storage + SQLite backend (D01) | 4h | ❌ |
| 11 | Fix rate limit global state (D02) | 1h | ❌ |
| 12 | Integration tests (E02) | 3h | ❌ |
| 13 | "Last known good" data fallback (F02) | 2h | ❌ |

### Deferred

| # | Item | Status |
|---|------|--------|
| 14 | Bound `_MISSING_COL_WARNED` (G13) | Accept for MVP |

---

## Architecture Observations

### Strengths
1. **File locking implemented**: Both YAML storage modules use `filelock.FileLock` (adaptive_engine.py:150, watchlist.py:26)
2. **ETF detection unified**: `detect_company_type()` delegates to `watchlist._is_etf()` with full 3-tier detection
3. **Atomic writes consolidated**: `_atomic_write` now in `src/utils/__init__.py`
4. **Dead code cleaned up**: `models.py`, `get_list_entries()`, `INDUSTRY_REVENUE_MAP`, `_section_card` all removed
5. **Theme-aware charts**: `chart.py` has proper `_get_chart_colors()` with dark/light mode support

### Weaknesses
1. **Tech debt velocity improving but slow**: 6 items fixed in Round 7, but 13 remain open
2. **No integration tests**: Still only unit tests
3. **Scattered static data**: 5+ modules with inline dicts
4. **Rate limit mechanisms still disconnected**: Session flag vs module counter

---

## Verification Notes (Round 7)

- **`_atomic_write` consolidation**: Confirmed at `src/utils/__init__.py:11` — both services import from `src.utils`
- **`models.py` removed**: File no longer exists
- **`get_list_entries` removed**: `rg "get_list_entries"` returns 0 results
- **`INDUSTRY_REVENUE_MAP` removed**: `rg "INDUSTRY_REVENUE_MAP"` returns 0 results
- **`_section_card` removed**: `rg "_section_card"` returns 0 results
- **ETF detection unified**: `adaptive_engine.py:19` imports `_is_etf` from watchlist; line 430 calls it
- **File locking**: `from filelock import FileLock` at `adaptive_engine.py:15` and `watchlist.py:11`
- **`st.bar_chart`**: Confirmed at `group_structure.py:283`
- **Bare `FinMindClient()`**: Confirmed at `peer_comparison.py:54`

---

*This is the seventh technical debt review. Six items fixed since Round 6 (G01, G02, G10, G11, G12, G14). Three new items found (G15, G16/G06 duplicate, G17). Total: 14 active items (~14 hours). Tech debt velocity is improving — first meaningful cleanup in 7 rounds.*
