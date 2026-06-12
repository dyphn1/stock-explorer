# Architect Review Round 17 — Sprint 4 Post-Implementation Audit

> **Date**: 2026-06-12
> **Reviewer**: System Architect
> **Scope**: Sprint 4 implementation audit (R3, C48, C38, C51, C53-1) + Sprint 5 readiness
> **Sprint Status**: L0: 65/65 ✅ | L1: 8/8 ✅ | Sprint 4 COMPLETE

---

## 1. New Architecture Debt from Sprint 4

### D-042: `_sections.py` grew to 918 lines — exceeds D37 threshold

- **Severity**: Medium-High
- **Effort**: 1-2h (split into sub-modules)
- **Status**: ⏳ NEW — PENDING
- **Description**: `_sections.py` was 612 lines after D24 extraction. Sprint 4 added:
  - `_render_story_card()` (C48): ~115 lines (lines 44-159)
  - `_render_compare_stories()` (C38): ~99 lines (lines 660-758)
  - `_render_share_section()` (C53-1): ~101 lines (lines 818-910)
  - Import block grew from ~35 to ~41 lines (added `compare_stories`, `_get_health_metric_values`)
  - **Total: 918 lines** — far exceeding the D37 threshold of ~730 lines that was supposed to trigger a split.
- **Impact**: `_sections.py` is now the largest file in the business_card/ sub-directory and approaching monolith territory. Finding a specific section function requires scrolling through 918 lines. The file will grow further in Sprint 5.
- **Recommended Action**: Split `_sections.py` into 3-4 sub-modules as proposed in D37:
  - `_sections_core.py` — header, one-liner, key metrics, footer (stable)
  - `_sections_analysis.py` — takeaways, deltas, health, risk (analysis)
  - `_sections_detail.py` — dividend, revenue breakdown, revenue trend, valuation, news (detail)
  - `_sections_discovery.py` — read next, compare stories, story card, share (discovery)
- **Priority for Sprint 5**: 🟡 Do as FIRST task of Sprint 5, before D-039/040/041.

---

### D-043: `_render_key_metrics()` calls non-existent `get_roe_analyzer()` and `get_pbr_analyzer()`

- **Severity**: **HIGH** — Runtime crash (NameError)
- **Effort**: 0.25h (fix function names)
- **Status**: ⏳ NEW — BUG
- **Description**: `_sections.py` lines 437 and 445 call `get_roe_analyzer(roe)` and `get_pbr_analyzer(pbr)` respectively. These functions do not exist anywhere in the codebase. The correct functions are `get_roe_analogy()` and `get_pbr_analogy()` from `analogy_engine.py` (which ARE imported at line 14-15 but not used in these two calls).
- **Impact**: When `_render_key_metrics()` renders the third column (PBR path) or the second column (ROE fallback path), it will raise `NameError: name 'get_roe_analyzer' is not defined`. This is a **runtime crash** that will break the business card page for any stock that hits these code paths.
- **Recommended Action**: Rename `get_roe_analyzer` → `get_roe_analogy` and `get_pbr_analyzer` → `get_pbr_analogy` on lines 437 and 445.
- **Priority for Sprint 5**: 🔴 CRITICAL — Fix immediately. This is a P0 bug.

---

### D-044: `sector_heatmap.py` (444 lines) is a standalone page with no service-layer abstraction

- **Severity**: Medium
- **Effort**: 2-3h (extract market data service)
- **Status**: ⏳ NEW — PENDING
- **Description**: `sector_heatmap.py` is 444 lines containing:
  - 3 rendering functions (`_render_sector_heatmap`, `_render_treemap`, `_render_sector_grid`, `_render_top_movers`)
  - Inline sector metric computation (lines 134-165: avg change, up/down/flat counts)
  - Inline batch fetching with progress bar (lines 104-125)
  - Direct `BatchAPI` usage (data layer access from presentation layer)
  - Heavy inline HTML (lines 196-201, 342-362, 392-413, 423-443)
- **Impact**: The page works but violates the 4-layer architecture. Sector metric computation should be in a service module. The inline HTML duplicates patterns from `_router_base.py` (`_白话_card` is imported but only used for the top KPIs; the rest is raw HTML).
- **Recommended Action**: Create `src/services/market_data.py` (as proposed in D25) with:
  - `compute_sector_metrics(summary_map, sector_stocks)` → sector_metrics dict
  - `fetch_sector_data(client, all_stock_info)` → summaries + sector mapping
  - Move `_render_treemap` and `_render_sector_grid` chart logic to `chart.py` or a new `chart_sector.py`
- **Priority for Sprint 5**: 🟡 Do alongside D37 split. Not blocking for Sprint 5 features.

---

### D-045: `compare_stories.py` imports `generate_key_takeaways` but never uses it

- **Severity**: Low
- **Effort**: 0.1h (remove dead import)
- **Status**: ⏳ NEW — CODE SMELL
- **Description**: `compare_stories.py` line 25 imports `generate_key_takeaways` from `key_takeaways.py`, but the function is never called anywhere in the module. The import is dead code.
- **Impact**: Minimal — adds a module load at import time and creates a false dependency. Could confuse future developers into thinking the function is used.
- **Recommended Action**: Remove the dead import on line 25.
- **Priority for Sprint 5**: 🟢 Quick fix, do alongside D-043.

---

### D-046: `_render_share_section()` uses `st.html()` with fragile JS element IDs

- **Severity**: Medium
- **Effort**: 1h (add proper Streamlit components or test thoroughly)
- **Status**: ⏳ NEW — FRAGILE
- **Description**: `_render_share_section()` (C53-1) uses `st.html()` to inject JavaScript that references `document.getElementById('share-url-input')` and `document.getElementById('share-copy-icon')`. However, Streamlit's `st.text_input()` does NOT render an element with `id="share-url-input"` — Streamlit generates its own internal IDs. The JS will silently fail to find the elements.
- **Impact**: The copy-to-clipboard button and URL auto-update will not work. The share section will render but the interactive features (copy button, URL population) will be broken. Users will see a non-functional share UI.
- **Recommended Action**: Either:
  - (a) Use `st.text_input()` with `disabled=True` and `st.button()` with a callback that uses `st.session_state` + `st.toast()` for clipboard feedback (pure Streamlit, no JS)
  - (b) Use `st.code()` for the URL display + `st.button("📋 複製")` with `pyperclip` or `st.write()` with `javascript` parameter
  - (c) If JS is required, use `streamlit.components.v1.html()` with proper HTML that doesn't rely on element IDs from other Streamlit widgets
- **Priority for Sprint 5**: 🟡 Should be fixed before Sprint 5 user testing. The feature is "complete" but non-functional.

---

### D-047: `_section_title()` in `_router_base.py` has inverted logic (dead code)

- **Severity**: Low
- **Effort**: 0.1h
- **Status**: ⏳ NEW — PRE-EXISTING BUG (not introduced in Sprint 4)
- **Description**: `_router_base.py` line 70: `if not title:` should be `if title:` — the condition is inverted. When `title` is falsy (empty/None), it tries to render `f"### 📊 {title}"` which just shows `### 📊 ` with no text. When `title` is truthy, it falls through to the emoji detection logic. The guard clause is meant to handle empty titles but does the opposite.
- **Impact**: Low — the function still renders something for all inputs. But empty titles produce a header with no text, and the emoji detection path is only reached for truthy titles (which is the opposite of the intended behavior).
- **Recommended Action**: Change `if not title:` to `if title:` and swap the return/mardown logic.
- **Priority for Sprint 5**: 🟢 Quick fix, do alongside D-039 (section header standardization).

---

## 2. Status of Existing Debt Items

### D37: `_sections.py` split
- **Previous Status**: ⏳ PENDING — 612 lines after D24
- **Current Status**: 🔴 **OVERDUE** — Now 918 lines (+306 lines from Sprint 4)
- **Change**: Sprint 4 added 3 new section functions without splitting. The D37 threshold of ~730 lines was crossed. Split is now more urgent.
- **Action**: Must be FIRST task of Sprint 5.

### D38: `chart.py` growth
- **Previous Status**: ⏳ MONITOR — 787 lines
- **Current Status**: ⏳ MONITOR — Still 787 lines (no change)
- **Change**: No new chart functions were added in Sprint 4. C51's treemap is in `sector_heatmap.py` (inline), not in `chart.py`. D38 remains at monitor level.
- **Action**: If Sprint 5 adds more charts, consider splitting to `chart_sector.py`.

### D39: Duplicate import headers
- **Previous Status**: ⏳ PENDING — `_main.py` and `_sections.py` have near-identical import blocks
- **Current Status**: ⏳ PENDING — **Worsened**
- **Change**: `_main.py` has 29 lines of imports (lines 6-36). `_sections.py` has 41 lines of imports (lines 2-41). Both import the same 10+ services. The duplication is now 70 lines total across 2 files. Adding a new service requires updating both files.
- **Action**: Consider a shared import module or consolidate imports into `_main.py` and re-export from there.

### D25: Market data abstraction gap
- **Previous Status**: Part of C51 implementation
- **Current Status**: ⏳ **NOT ADDRESSED** — C51 implemented without `market_data.py`
- **Change**: `sector_heatmap.py` was implemented as a standalone page with inline data fetching and metric computation. No `market_data.py` service was created.
- **Action**: Create `src/services/market_data.py` as proposed in D25. Extract from `sector_heatmap.py`.

### D23: Tone guidelines for market-level features
- **Previous Status**: ⏳ PENDING — No `docs/design/tone_guidelines.md` exists
- **Current Status**: ⏳ **NOT ADDRESSED** — Still no tone guidelines file
- **Change**: C51 (Sector Heatmap) was implemented without tone guidelines. The sector descriptions use neutral language ("平均漲跌", "上漲/下跌") which is acceptable but not guided by documented guidelines.
- **Action**: Create `docs/design/tone_guidelines.md` before Sprint 5 market features.

### D12: `_router_base.py` mixes routing and UI
- **Previous Status**: ⏳ PENDING — 1h effort
- **Current Status**: ⏳ **UNCHANGED** — `_section_title()`, `_白话_card()`, `_info_card()`, `_summary_card()` still in `_router_base.py`
- **Change**: No refactoring done. `_router_base.py` is 177 lines. The UI functions (lines 69-114) are ~46 lines that should be in a shared UI module.
- **Action**: Move UI helper functions to `src/services/ui_components.py` (also addresses D3).

### D3: Inline HTML duplication across pages
- **Previous Status**: ⏳ PENDING — 3-4h effort
- **Current Status**: ⏳ **WORSENED** — `sector_heatmap.py` added ~150 lines of inline HTML. `_sections.py` dividend table HTML (~55 lines) and share section JS (~80 lines) add more inline HTML.
- **Change**: Total inline HTML in the codebase has grown significantly. `sector_heatmap.py` alone has 6 blocks of inline HTML with hardcoded styles.
- **Action**: Create `src/services/ui_components.py` with reusable card/badge components.

### D4: Service layer `__init__.py` wildcard imports
- **Previous Status**: ⏳ PENDING — 0.5h effort
- **Current Status**: ⏳ **UNCHANGED** — Still 7 wildcard imports, no new services added to `__init__.py`
- **Change**: `compare_stories.py` was added to `src/services/` but NOT exported in `__init__.py`. This is actually correct behavior (it's used internally by `_sections.py`, not as a public API), but the wildcard pattern remains.
- **Action**: Replace wildcard imports with explicit imports.

### D6: Hardcoded data in Python modules
- **Previous Status**: ⏳ PENDING — 3-4h effort
- **Current Status**: ⏳ **UNCHANGED** — No new hardcoded data added in Sprint 4
- **Change**: `sector_heatmap.py` has `_SECTOR_COLORS` (16 colors, line 18-23) — a small hardcoded data item. Not significant enough to warrant a YAML migration on its own.
- **Action**: Include in next YAML migration pass.

### D13: No test infrastructure
- **Previous Status**: ⏳ PENDING — 3-4h initial setup
- **Current Status**: ⏳ **UNCHANGED** — Zero test files exist
- **Change**: No tests added. The codebase is now ~4,327 lines across 16 service modules with zero test coverage.
- **Action**: Add pytest + `tests/` directory. Start with service layer tests.

### D14: Sidebar architecture not extracted
- **Previous Status**: ⏳ PENDING — 1-2h effort
- **Current Status**: ⏳ **UNCHANGED** — `main.py` still has ~85 lines of sidebar code
- **Change**: No extraction done. `main.py` is 297 lines.
- **Action**: Extract to `src/services/sidebar_render.py` as proposed.

### Summary Table

| Debt | Severity | Previous | Current | Trend |
|------|----------|----------|---------|-------|
| D37 | Medium | 612 lines | **918 lines** | 🔴 Worsened |
| D38 | Low | 787 lines | 787 lines | ➡️ Stable |
| D39 | Low | Duplicate imports | **More duplication** | 🔴 Worsened |
| D25 | Medium | Pending | **Not addressed** | 🔴 Worsened |
| D23 | Medium | Pending | **Not addressed** | ➡️ Stable |
| D12 | Low | Pending | Unchanged | ➡️ Stable |
| D3 | Medium | Pending | **More inline HTML** | 🔴 Worsened |
| D4 | Low | Pending | Unchanged | ➡️ Stable |
| D6 | Medium | Pending | Unchanged | ➡️ Stable |
| D13 | Medium | Pending | Unchanged | ➡️ Stable |
| D14 | Low | Pending | Unchanged | ➡️ Stable |

---

## 3. Performance Bottlenecks and Structural Issues

### 3.1 `sector_heatmap.py` — Sequential batch fetching with progress bar

- **Issue**: Lines 114-125 fetch prices in batches of 50 sequentially. For ~1,000 stocks, this is 20 sequential batch calls. Each call goes through `BatchAPI.get_watchlist_summaries()` which calls `get_stock_infos()` (one API call for all stocks via cache) + `get_latest_prices()` (one API call per stock). The progress bar is good UX but the underlying fetching is still sequential per-stock for prices.
- **Impact**: First load of the sector heatmap page will be slow (~30-60s for 1,000 stocks). Subsequent loads within the same session are fast (FinMindClient cache).
- **Severity**: Medium — acceptable for a market overview page that loads once per session.
- **Recommendation**: Consider using `ThreadPoolExecutor` (like `_router_base.py` does) for the price fetching. The current batch approach with progress bar is good UX but could be 5-10x faster with concurrency.

### 3.2 `_render_compare_stories()` — Double peer lookup

- **Issue**: `_render_compare_stories()` (lines 676-691) calls `client.get_stock_info()` to find peers, then calls `generate_compare_stories()` which internally calls `_find_peers()` that does the same filtering again. The peer lookup logic is duplicated between the section function and the service module.
- **Impact**: Minimal — `get_stock_info()` is cached. But the code duplication means two identical filtering operations.
- **Severity**: Low
- **Recommendation**: Move the peer lookup entirely into `generate_compare_stories()` and pass only the necessary data to the section function.

### 3.3 `_render_read_next()` — Same peer lookup as `_render_compare_stories()`

- **Issue**: `_render_read_next()` (lines 771-778) also calls `client.get_stock_info()` and filters by industry to find peers. This is the same operation as `_render_compare_stories()`. Both sections independently fetch and filter the full stock universe.
- **Impact**: Minimal — cached. But architecturally inconsistent. Two sections doing the same data access.
- **Severity**: Low
- **Recommendation**: Pre-compute peer data in `_main.py` and pass it as part of the `data` dict or as a separate parameter.

### 3.4 `_main.py` and `_sections.py` import duplication

- **Issue**: `_main.py` imports 10 services (29 lines). `_sections.py` imports the same 10 services plus `compare_stories` (41 lines). When a new service is added, both files must be updated.
- **Impact**: Maintenance burden. Risk of import drift between the two files.
- **Severity**: Low-Medium
- **Recommendation**: Consider having `_sections.py` import from `_main.py` (reverse direction) or create a shared `_business_card_imports.py` module.

---

## 4. Sprint 5 Architecture Readiness Assessment

### Prerequisites Status

| Prerequisite | Status | Effort | Notes |
|-------------|--------|--------|-------|
| **D-039**: Section header standardization | ⏳ NOT STARTED | 1-2h | Needed for consistent section headers across all pages. Low risk. |
| **D-040**: Historian disclaimer component | ⏳ NOT STARTED | 0.5h | Quick win. Create a reusable disclaimer component. |
| **D-041**: Sprint 5 card components | ⏳ NOT STARTED | 1h | New reusable card components for Sprint 5 features. |
| **D37**: `_sections.py` split | ⏳ NOT STARTED | 1-2h | **CRITICAL** — At 918 lines, this is overdue. Must be done first. |

### Readiness Verdict: 🟡 **CONDITIONAL GO**

**Blockers**: None of the prerequisites are true blockers — Sprint 5 features can be implemented without them. However:

1. **D-043 (P0 bug)** must be fixed before any user testing. The `get_roe_analyzer` / `get_pbr_analyzer` NameError will crash the business card page for certain stocks.
2. **D37 (sections.py split)** should be done before adding more sections to `_sections.py`. At 918 lines, adding Sprint 5 sections will push it past 1,000 lines.
3. **D-046 (share section JS)** should be fixed if C53-1 is considered "complete" — the current implementation is non-functional.

### Recommended Sprint 5 Sequence

1. **D-043** — Fix `get_roe_analyzer`/`get_pbr_analyzer` bug (0.25h) — 🔴 IMMEDIATE
2. **D37** — Split `_sections.py` into sub-modules (1-2h) — 🟡 FIRST
3. **D-039** — Section header standardization (1-2h)
4. **D-040** — Historian disclaimer component (0.5h)
5. **D-041** — Sprint 5 card components (1h)
6. Sprint 5 feature development

### Architecture Risks for Sprint 5

1. **`_sections.py` at 918 lines**: Adding more sections without splitting will create a 1,000+ line file. This is the #1 structural risk.
2. **No test infrastructure**: With 4,327 lines of service code and zero tests, regressions are likely. Each Sprint 5 feature increases the risk.
3. **Inline HTML growth**: `sector_heatmap.py` added 150+ lines of inline HTML. Sprint 5 features will likely add more unless `ui_components.py` is created.
4. **Session state proliferation**: C53-1 added JS-based session state manipulation. Sprint 5 features will add more session state keys. No session state manager exists.

---

## 5. Top 3 Recommendations

### 1. 🔴 Fix D-043 Immediately (P0 Bug)

**What**: Rename `get_roe_analyzer` → `get_roe_analogy` and `get_pbr_analyzer` → `get_pbr_analogy` in `_sections.py` lines 437 and 445.

**Why**: This is a runtime crash (NameError) that will break the business card page for stocks that hit the ROE/PBR code paths in `_render_key_metrics()`. The correct functions are already imported but not used.

**Effort**: 0.25h (2 lines changed)

---

### 2. 🟡 Split `_sections.py` Before Sprint 5 Development (D37)

**What**: Split `_sections.py` (918 lines) into 3-4 sub-modules as proposed in D37:
- `_sections_core.py` — header, one-liner, key metrics, footer
- `_sections_analysis.py` — takeaways, deltas, health, risk
- `_sections_detail.py` — dividend, revenue breakdown, revenue trend, valuation, news
- `_sections_discovery.py` — read next, compare stories, story card, share

**Why**: At 918 lines, `_sections.py` is the largest file in the business card sub-directory and is growing with every feature. Sprint 5 will add more sections. Without the split, the file will exceed 1,000 lines and become the new monolith.

**Effort**: 1-2h (reorganization only, no logic changes)

---

### 3. 🟡 Create `ui_components.py` to Stop Inline HTML Proliferation (D3)

**What**: Create `src/services/ui_components.py` with reusable components:
- `render_badge_table(df, badge_col, badge_styles)` — replaces dividend history table HTML
- `render_score_cards(scores, columns=5)` — replaces health dimension cards HTML
- `render_sector_card(sector, metrics)` — replaces sector grid HTML
- Move `_RISK_BADGES`, `_RISK_COLORS` here from `_helpers.py`
- Move `_section_title()`, `_白话_card()`, `_info_card()`, `_summary_card()` here from `_router_base.py`

**Why**: Inline HTML is the #1 source of code duplication and maintenance burden. `sector_heatmap.py` added 150+ lines of inline HTML. `_sections.py` has ~100 lines of inline HTML for the dividend table. Each new feature adds more. A shared component library will reduce total code and ensure visual consistency.

**Effort**: 2-3h initial setup, saves 1-2h per future feature

---

## Appendix: File Size Summary

### Service Layer (src/services/)

| File | Lines | Status |
|------|-------|--------|
| `chart.py` | 787 | Monitor (D38) |
| `adaptive_engine.py` | 590 | Stable |
| `risk_analyzer.py` | 567 | Stable |
| `compare_stories.py` | 328 | New (Sprint 4) — has dead import |
| `watchlist.py` | 323 | Stable |
| `health_scoring.py` | 269 | Stable (split from analogy_engine) |
| `key_takeaways.py` | 232 | Stable (split from analogy_engine) |
| `dividend_analyzer.py` | 201 | Stable |
| `analogy_engine.py` | 193 | Stable (split from 850-line god module) |
| `financial_metrics.py` | 188 | Stable |
| `delta_engine.py` | 164 | Stable (split from analogy_engine) |
| `news_summarizer.py` | 158 | Stable |
| `revenue_analyzer.py` | 145 | Stable |
| `roe_calculator.py` | 97 | Stable |
| `company_facts.py` | 46 | Stable |
| `validation.py` | 32 | Stable |
| **Total** | **4,327** | **16 modules** |

### Presentation Layer (src/pages/)

| File | Lines | Notes |
|------|-------|-------|
| `sector_heatmap.py` | 444 | New (Sprint 4) — inline HTML, no service layer |
| `business_card/_sections.py` | 918 | Grew +306 from Sprint 4 — needs split |
| `business_card/_main.py` | 89 | Orchestrator |
| `business_card/_helpers.py` | 95 | Shared helpers |
| `_router_base.py` | 177 | Routing + UI mix (D12) |
| `router.py` | 181 | Page router |
| `main.py` | 297 | Entry + sidebar (D14) |
| Other pages | ~1,200 | category_browser, etf_browser, etc. |
| **Total** | **~3,400** | **17 page files + business_card sub-dir** |

---

*Created: 2026-06-12*
*Maintainer: System Architect*
*Next Review: Sprint 5 mid-point*
