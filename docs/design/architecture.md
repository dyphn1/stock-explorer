# Stock Explorer — Architecture Analysis

## 2026-06-14 Technical Analysis — Review Round 9

---

### Architecture Overview

**Current State**: Sprint 1 (Development theme, active). The project has completed Sprint 0 (foundation) and is now in Sprint 1 working on C28 Spike + LLM Architecture. The codebase follows a 4-layer architecture defined in `docs/architecture/architecture.md`:

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer (View) — src/pages/*.py         │
│  11 page files, pure rendering + service calls       │
├─────────────────────────────────────────────────────┤
│  Routing Layer — src/pages/router.py                │
│  Session state management, page selection            │
├─────────────────────────────────────────────────────┤
│  Business Logic Layer — src/services/*.py           │
│  10 service modules (chart, analogy, adaptive, etc.) │
├─────────────────────────────────────────────────────┤
│ Data Layer — src/data/finmind_client.py             │
│  FinMind API wrapper with file-based caching         │
└─────────────────────────────────────────────────────┘
```

**Key Metrics**:
- 31 Python source files (excluding `__pycache__`)
- ~5,200 lines of application code across src/
- 11 presentation pages, 10 service modules, 1 data client
- Data sources: FinMind API (11 endpoints), 2 YAML data files, 1 events YAML
- Zero external LLM dependency (template-based explanations)

**Verified Status** (from STATUS.md):
- L0 (Import): 54/54 ✅
- L1 (Render): 15/18 ⚠️ (3 pre-existing failures from Sprint 0/1)
- L2 (Smoke): Not yet run

---

### Identified Architecture Debt

| # | Item | Severity | Description | Recommended Action |
|---|------|----------|-------------|-------------------|
| D1 | **Duplicate financial metric calculation** | 🔴 High | `_calc_extra_metrics()` in `_router_base.py` (lines 68-118) and `_get_benchmark_data()` in `peer_comparison.py` (lines 213-252) both compute gross_margin, net_margin, ROE, debt_ratio, revenue_yoy using identical logic. `_find_financial_value()` is defined in both `_router_base.py` and imported in `peer_comparison.py` and `roe_calculator.py` and `financial_health.py`. | Extract shared financial calculation into a new `src/services/financial_metrics.py` service. All consumers import from one place. |
| D2 | **`_find_financial_value` semantic duplication** | 🔴 High | The function `_find_financial_value()` exists in `_router_base.py` (lines 121-130) and is also imported/used in `peer_comparison.py`, `roe_calculator.py`, and `financial_health.py`. It's a business logic function living in a routing utility file. | Move to `financial_metrics.py` (same refactoring as D1). |
| D3 | **Inline HTML duplication across pages** | 🟡 Medium | `business_card.py`, `group_structure.py`, `etf_detail.py`, `etf_browser.py`, `watchlist_page.py` all contain large inline HTML strings with repeated CSS patterns (card styles, badge styles, color values). The `_router_base.py` provides `_白话_card()` and `_info_card()` but pages bypass them for complex layouts. | Create reusable HTML component functions in a new `src/services/ui_components.py` (or extend `_router_base.py`). Standardize card/badge patterns. |
| D4 | **Service layer `__init__.py` wildcard imports** | 🟡 Medium | `src/services/__init__.py` uses `from X import *` for only 3 of 10 service modules. This creates implicit dependencies and makes it unclear which services are "public API" vs internal. | Replace wildcard imports with explicit imports. Document which services are stable public API. |
| D5 | **No LLM integration layer** | 🟡 Medium | The product vision specifies "LLM (plain-language translation only) + templates" but the codebase uses zero LLM. The `analogy_engine.py` and `news_summarizer.py` are purely template-based. Sprint 1's C28 Spike is meant to address this, but no abstraction exists yet. | Define an `src/services/llm/` abstraction layer with a protocol/interface. Current template engines become the "fallback" implementation. |
| D6 | **Hardcoded data in Python modules** | 🟡 Medium | `revenue_analyzer.py` has `KNOWN_COMPANY_REVENUE` dict (8 stocks, ~50 lines), `group_structure.py` has `KNOWN_GROUP_STRUCTURES` (5 groups, ~160 lines), `analogy_engine.py` has `one_liners` dict (20 stocks) and `industry_templates` (10 industries), `peer_comparison.py` has `INDUSTRY_BENCHMARKS` (22 entries). | Migrate all hardcoded data to YAML files under `src/data/`. Only keep the loading/parsing logic in Python. |
| D7 | **`category_browser.py` N+1 API call pattern** | 🟡 Medium | `_render_top_stocks_by_value()` and `_render_hot_stocks_by_volume()` each call `client.get_daily_price()` in a loop for 200 stocks (lines 68-89, 205-223). This is sequential, not parallel, and blocks the UI with a progress bar. | Use the same `ThreadPoolExecutor` pattern from `_router_base.get_stock_data()`. Batch-fetch with concurrency. |
| D8 | **`etf_browser.py` sequential price fetching** | 🟡 Medium | `_get_all_etf_prices()` iterates ETFs sequentially (lines 21-48). For ~100 ETFs, this is slow. The dividend ranking section also fetches dividends sequentially. | Same as D7 — use ThreadPoolExecutor for batch fetching. |
| D9 | **Watchlist reads YAML on every operation** | 🟡 Low | `watchlist.py` calls `_load_data()` (file read + YAML parse) for every single operation (`add`, `remove`, `is_in`, `get_summary`). No in-memory caching. | Add a session-level cache or in-memory store that's invalidated on writes. |
| D10 | **`events.yaml` read on every event query** | 🟡 Low | `adaptive_engine.py` calls `_load_events()` (file read + YAML parse + file lock) for every `get_events_for_stock()` and `get_all_recent_events()` call. | Cache events in memory with TTL or session_state. |
| D11 | **No error boundary standardization** | 🟡 Medium | Error handling is inconsistent. Some services return `None`, others return empty dicts `{}`, others return empty DataFrames. The architecture doc specifies "Return None or empty DataFrame" but enforcement is ad-hoc. | Create a standardized result type (e.g., `Result[T]` with `.is_ok`, `.value`, `.error`) or at minimum document the convention per service. |
| D12 | **`_router_base.py` mixes routing and UI** | 🟡 Medium | `_router_base.py` contains `_section_title()`, `_白话_card()`, `_info_card()` (lines 133-169) — these are UI rendering functions in a routing utility file. They use `st.markdown()` directly. | Move UI helper functions to a shared presentation utility module. Keep `_router_base.py` for data loading only. |
| D13 | **No test infrastructure** | 🟡 Medium | Zero test files exist. The architecture has good layer separation which would make unit testing natural, but no tests have been written. | Add pytest + a `tests/` directory. Start with service layer tests (pure functions, no Streamlit dependency). |
| D14 | **Sidebar architecture not extracted** | 🟡 Low | `main.py` contains ~85 lines of sidebar rendering code (lines 161-245) with hardcoded stock/ETF lists. The `sidebar_architecture.md` doc proposes extracting this but it hasn't been implemented. | Extract sidebar to `src/services/sidebar_render.py` as proposed in the sidebar architecture doc. |
| D15 | **FinMind client is not async-compatible** | 🟡 Low | `FinMindClient` uses synchronous API calls. The ThreadPoolExecutor in `_router_base.py` mitigates this for the main data load, but standalone page operations (category browser, ETF browser) don't benefit from this. | Consider an async FinMind client wrapper for future-proofing. Low priority since ThreadPoolExecutor works. |

---

### Performance Bottlenecks

| # | Item | Impact | Recommendation |
|---|------|--------|----------------|
| P1 | **Sequential API calls in category_browser** | 🔴 High | 200 sequential `get_daily_price()` calls for the value ranking section. Each call triggers a cache check (file I/O) or API call. Can take 30-60 seconds. | Use `ThreadPoolExecutor(max_workers=10)` batch pattern from `_router_base.py`. Expected improvement: 5-10x faster. |
| P2 | **Sequential API calls in etf_browser** | 🔴 High | Same pattern as P1 but for ETF prices and dividend data. The dividend ranking fetches dividends for ALL ETFs sequentially. | Batch fetch with ThreadPoolExecutor. Pre-cache dividend data. |
| P3 | **No cross-request cache warming** | 🟡 Medium | Cache is only populated on first user request. Cold start for a new stock requires 10+ API calls. | Implement a cache warming strategy for hot stocks (the 9 sidebar stocks). Pre-fetch on app startup. |
| P4 | **YAML parsing on every watchlist operation** | 🟡 Medium | `watchlist.yaml` is read and parsed on every add/remove/check operation. File lock adds overhead. | Cache in session_state. Invalidate on write. |
| P5 | **YAML parsing on every events query** | 🟡 Medium | `events.yaml` is read and parsed on every event dashboard render and every stock page's event check. | Cache in session_state with TTL. |
| P6 | **Full stock info loaded for category browser** | 🟡 Medium | `client.get_stock_info()` loads the entire universe (~1,800 stocks) into memory for the category browser. This is cached by FinMindClient, but the initial load is slow. | Already mitigated by FinMindClient's all_stock_info cache. No action needed. |
| P7 | **Page-level spinners create perceived slowness** | 🟡 Low | Every page transition shows `st.spinner("載入股票資料...")` then `st.spinner("載入 XX 頁...")` — two sequential spinners. | Combine into a single spinner. Show progress for parallel data loading. |

---

### Feasibility Assessment for Approved Features

#### C37: Key Takeaways Summary Card (Sprint 2, ~6.5h)

- **Feasibility**: ✅ **High**. Pure presentation + thin service layer.
- **Dependencies**: `analogy_engine.py` (exists), `company_facts.py` (exists), `_info_card()` (exists), `data` dict from router (exists).
- **Risks**: 
  - Rule-based summaries may feel generic for stocks with sparse data. Mitigate with graceful degradation (fewer bullets).
  - No new data sources needed — all data already in the `data` dict.
- **Architecture Fit**: Clean. New `summary_engine.py` service module + thin addition to `business_card.py`. Follows existing patterns exactly.
- **Recommendation**: Proceed as planned. Lowest risk feature. Consider making the summary data-driven (top 3 metrics by absolute value) rather than purely rule-based for better variety.

#### C39: What Changed Recently Delta Card (Sprint 3, ~5.5h)

- **Feasibility**: ✅ **High**. Data already exists; this is a presentation-layer repackaging.
- **Dependencies**: `data` dict fields (monthly_revenue, financial, daily_price, extra_metrics), `adaptive_engine.py` event detection, `analogy_engine.py` for descriptions.
- **Risks**:
  - Delta calculations may be noisy for volatile stocks. Mitigate with >10% threshold.
  - Overlaps conceptually with the event dashboard. Position as "stock-specific recent changes" vs "portfolio-wide historical events."
  - **Architecture debt interaction**: D1 (duplicate metric calculation) means delta calculations may diverge if computed differently. Fix D1 before or alongside C39.
- **Architecture Fit**: New `delta_engine.py` service module. Thin addition to `business_card.py`. Clean separation.
- **Recommendation**: Proceed as planned. Consider combining with C37 into a single "smart summary" service to avoid two separate service modules that do similar data analysis.

#### C41: Read Next Recommendations (Sprint 3, ~6.5h)

- **Feasibility**: ✅ **High**. Data-driven with existing data sources.
- **Dependencies**: `group_structure.py` `KNOWN_GROUP_STRUCTURES` (exists), `peer_comparison.py` `INDUSTRY_BENCHMARKS` (exists), `navigate_to()` (exists).
- **Risks**:
  - Manual relationship data doesn't scale. Start with top 10 stocks, not 20.
  - **Architecture debt interaction**: D6 (hardcoded data in Python) — the relationship data should go in a YAML file, not in a new Python module.
  - Recommendations may be obvious (TSMC → UMC). The value is in surfacing non-obvious relationships (customer-supplier).
- **Architecture Fit**: New `recommendation_engine.py` service + YAML data file. Bottom section of `business_card.py`. Clean.
- **Recommendation**: Proceed as planned. Use a new `src/data/relationships.yaml` file rather than hardcoding in Python. This aligns with D6 remediation.

#### C36: Visual Revenue Tree (Sprint 4, ~8-9h)

- **Feasibility**: 🟡 **Medium**. Charting capability exists; data curation is the bottleneck.
- **Dependencies**: `chart.py` theme system (exists), `revenue_analyzer.py` pattern (exists), `business_card.py` revenue section (exists).
- **Risks**:
  - Manual curation doesn't scale beyond top 10-20 stocks. Acceptable for P2.
  - **Architecture debt interaction**: D6 (hardcoded data) — revenue tree data should go in a new `src/data/revenue_tree.yaml` file.
  - Sunburst/treemap readability on small screens. Test with real data.
- **Architecture Fit**: New `create_revenue_treemap()` in `chart.py` + YAML data file + tab in `business_card.py`. Clean extension.
- **Recommendation**: Proceed as planned for Sprint 4. Use `plotly.express.treemap` for simpler implementation (fewer lines than `go.Sunburst`). Start with top 10 stocks.

#### C38: Compare Stories Phase 1 (Sprint 3, deferred, 8-10h)

- **Feasibility**: 🟡 **Medium** (Phase 1 without LLM). **Low** (Phase 2 with LLM).
- **Dependencies**: `analogy_engine.py` (exists), `revenue_analyzer.py` (exists), `adaptive_engine.py` (exists), `peer_comparison.py` (exists). Phase 2 depends on C28 LLM architecture decision.
- **Risks**:
  - Phase 1 (structured data only) may feel shallow — "reading two business cards side by side" rather than a true narrative comparison.
  - Loading two companies' data adds API calls. Use the same `_get_benchmark_data()` pattern.
  - **Architecture debt interaction**: D1 (duplicate metrics) — the narrative comparison will need financial metrics. Use the shared `financial_metrics.py` once D1 is fixed.
  - Scope creep: narrative comparison could become a full product feature. Strictly limit Phase 1 to 4 narrative dimensions.
- **Architecture Fit**: New `narrative_comparator.py` service + tab in `peer_comparison.py`. Clean extension.
- **Recommendation**: Defer to Sprint 3 as planned. Phase 1 is independently valuable. The phased approach (structured first, LLM later) is the right risk management strategy. Ensure the `narrative_comparator.py` service has a clean interface that can accept an LLM provider in Phase 2.

---

### Recommendations

#### Priority 1: Fix Critical Architecture Debt (Before Sprint 2 Features)

**R1: Extract shared financial metrics service** (addresses D1, D2)
- Create `src/services/financial_metrics.py` with:
  - `calc_financial_metrics(financial_df, balance_sheet_df, monthly_revenue_df) -> dict`
  - `find_financial_value(df, keywords) -> float`
- Migrate all consumers: `_router_base.py`, `peer_comparison.py`, `roe_calculator.py`, `financial_health.py`
- **Effort**: 2-3h. **Impact**: Eliminates ~100 lines of duplication, ensures consistent calculations across all pages and features.

**R2: Move UI helpers out of `_router_base.py`** (addresses D12)
- Create `src/services/ui_components.py` with `_section_title()`, `_白话_card()`, `_info_card()`
- Update all imports across pages
- **Effort**: 1h. **Impact**: Proper layer separation, routing layer stays focused on data loading.

#### Priority 2: Performance Improvements (Before Sprint 2 Features)

**R3: Batch API calls in category_browser and etf_browser** (addresses P1, P2, D7, D8)
- Extract a shared `batch_fetch_prices(client, stock_ids, max_workers=10)` utility
- Replace sequential loops in `category_browser.py` and `etf_browser.py`
- **Effort**: 2-3h. **Impact**: 5-10x speedup for category browser and ETF browser pages.

**R4: Add session-level caching for watchlist and events** (addresses P4, P5, D9, D10)
- Cache watchlist data in `st.session_state["_watchlist_cache"]` with invalidation on write
- Cache events in `st.session_state["_events_cache"]` with TTL
- **Effort**: 1-2h. **Impact**: Eliminates redundant YAML parsing on every operation.

#### Priority 3: Data Architecture (During Sprint 2-3)

**R5: Migrate hardcoded data to YAML files** (addresses D6)
- Move `KNOWN_COMPANY_REVENUE` from `revenue_analyzer.py` → `src/data/revenue_breakdown.yaml`
- Move `KNOWN_GROUP_STRUCTURES` from `group_structure.py` → `src/data/group_structures.yaml`
- Move `one_liners` from `analogy_engine.py` → `src/data/one_liners.yaml`
- Move `INDUSTRY_BENCHMARKS` from `peer_comparison.py` → `src/data/industry_benchmarks.yaml`
- **Effort**: 3-4h. **Impact**: All curated data is in YAML files, not Python code. Easier to maintain and extend.

**R6: Standardize service `__init__.py`** (addresses D4)
- Replace wildcard imports with explicit imports
- Document public API surface
- **Effort**: 0.5h. **Impact**: Clearer module boundaries.

#### Priority 4: LLM Abstraction (During Sprint 1-2)

**R7: Define LLM provider interface** (addresses D5)
- Create `src/services/llm/base.py` with `ExplanationProvider` protocol
- Current template engines become `TemplateExplanationProvider` implementation
- Future LLM integration becomes `LLMExplanationProvider` implementation
- **Effort**: 2-3h. **Impact**: Clean separation between template and LLM explanation. C28 Spike can plug into this interface.

#### Priority 5: Testing Infrastructure (During Sprint 3-4)

**R8: Add pytest + initial service tests** (addresses D13)
- Create `tests/` directory with `tests/services/` and `tests/data/`
- Start with pure service functions: `financial_metrics.py`, `analogy_engine.py`, `validation.py`
- **Effort**: 3-4h initial setup. **Impact**: Prevents regressions as features are added.

#### Priority 6: UI Component Standardization (During Sprint 3-4)

**R9: Create reusable UI component library** (addresses D3)
- Standardize card/badge/color patterns in `ui_components.py`
- Replace inline HTML in `group_structure.py`, `etf_detail.py`, `etf_browser.py`, `watchlist_page.py`
- **Effort**: 3-4h. **Impact**: Consistent look-and-feel, easier maintenance.

---

### Summary

The Stock Explorer architecture is **well-structured** with clear layer separation and good adherence to the architecture definition document. The primary concerns are:

1. **Financial metric duplication** (D1, D2) — the most impactful debt item, affecting 4+ files
2. **Sequential API calls** (P1, P2, D7, D8) — the most impactful performance issue
3. **Hardcoded data in Python** (D6) — will become a maintenance burden as curated data grows

The approved features (C37, C39, C41, C36, C38) are all **feasible** with the current architecture. C37 and C39 are lowest risk and should be built first. C38 is highest risk and correctly deferred. The main architecture gaps for these features are:
- No shared financial metrics service (needed for C39, C38)
- No LLM abstraction (needed for C38 Phase 2)
- No relationship data in YAML (needed for C41)

**Recommended immediate actions** (before Sprint 2): R1 (extract financial metrics), R3 (batch API calls), R4 (session caching). These 3 items total ~5-8h and will make all subsequent feature development faster and more consistent.

---

*Created: 2026-06-14*
*Maintainer: System Architect*
*Next review: After Sprint 2 feature implementation*
