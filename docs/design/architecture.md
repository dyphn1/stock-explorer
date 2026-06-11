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

---

## 2026-06-17 Technical Analysis — Review Round 11

### Context

Sprint 2 completed with 4 features shipped: C37 (Key Takeaways), C39 (What Changed Delta), C45 (Valuation Band), C43 (Snowflake Health). Sprint 3 is now in progress (C44, C41, C38, R1, R5). This analysis covers **only NEW architecture debt** introduced during Sprint 2. For debt items D1–D15, see the Round 9 analysis above.

### Codebase Growth Summary

| Metric | Round 9 | Round 11 | Change |
|--------|---------|----------|--------|
| Total .py files (excl. `__pycache__`) | 31 | 31 | 0 |
| Total application LOC | ~5,200 | ~7,699 | +2,499 |
| `analogy_engine.py` | ~192 lines | 857 lines | +665 |
| `chart.py` | ~490 lines | 757 lines | +267 |
| `business_card.py` | ~337 lines | 479 lines | +142 |

Growth is concentrated in two service files (+932 lines) and one page file (+142 lines). No new service modules were created.

### New Architecture Debt (D16+)

#### D16: `analogy_engine.py` has become a 857-line god module

- **Severity**: 🟟 High
- **Description**: `analogy_engine.py` grew from ~192 lines (pure analogy functions) to 857 lines. It now contains 6 distinct responsibilities:
  1. Analogy/revenue explanations (original purpose, lines 1–193)
  2. Curated key takeaways data `_KEY_TAKEAWAYS` (120 lines of hardcoded dict)
  3. `generate_key_takeaways()` — rule-based synthesis (100 lines)
  4. `compute_recent_deltas()` + `explain_delta()` — delta detection (180 lines)
  5. Health scoring: 6 `_score_*` functions + `compute_health_scores()` + `get_health_summary()` (270 lines)
  6. EPS extraction logic duplicated from `chart.py` (lines 743–761)
- **Impact**: The module is doing the work of 3–4 separate services. The health scoring functions (`_score_roe`, `_score_gross_margin`, etc.) are pure functions that could be independently tested but are buried in a module dominated by string templates.
- **Recommended Action**: Split into focused modules:
  - `src/services/analogy_engine.py` — keep only analogy functions (lines 1–193)
  - `src/services/key_takeaways.py` — `generate_key_takeaways()` + `_KEY_TAKEAWAYS` data
  - `src/services/delta_engine.py` — `compute_recent_deltas()` + `explain_delta()`
  - `src/services/health_scoring.py` — all `_score_*` + `compute_health_scores()` + `get_health_summary()`
- **Effort**: 2–3h (extract + update imports). **Note**: This is a stepping stone to R1 (financial_metrics extraction). Don't split until R1 is done — do them together.

#### D17: EPS extraction logic triplicated across 3 files

- **Severity**: 🟡 Medium
- **Description**: The identical pattern of extracting EPS from financial statements using keyword matching appears in 3 files:
  - `chart.py:640-682` — `create_valuation_band_chart()` TTM EPS calculation
  - `analogy_engine.py:747-759` — `compute_health_scores()` EPS growth calculation
  - `business_card.py:420-437` — inline PER percentile calculation in `_render_business_card()`
  
  All three use the same `eps_keywords = ["eps", "每股盈餘", "earnings per share"]` pattern, the same `str.contains()` filtering, the same `groupby("date").max()` dedup, and the same `tail(4).sum()` TTM calculation.
- **Impact**: If the EPS extraction logic needs to change (e.g., different keywords, different TTM window), it must be updated in 3 places. The `business_card.py` version is inline (not even a function).
- **Recommended Action**: Extract a shared `extract_ttm_eps(financial_df, as_of_date=None) -> float` function in a new `src/services/financial_metrics.py` (same as R1). All 3 consumers call this function.
- **Effort**: 1–2h as part of R1.

#### D18: `_KEY_TAKEAWAYS` hardcoded dict (120 lines) violates D6

- **Severity**: 🟡 Medium
- **Description**: C37 added a 120-line hardcoded `_KEY_TAKEAWAYS` dict (20 stocks, 4–5 bullets each) directly in `analogy_engine.py`. This is the same anti-pattern as D6 (hardcoded data in Python). The handoff explicitly notes "C37 uses curated takeaways for top 20 stocks as PRIMARY approach" — this data will grow.
- **Impact**: Curated takeaways are mixed with analogy logic. Adding a new stock requires editing a Python file, not a YAML file. Non-developers cannot contribute.
- **Recommended Action**: Move to `src/data/key_takeaways.yaml` as part of R5 (YAML migration). The loading function stays in the service module.
- **Effort**: 1h as part of R5.

#### D19: `business_card.py` inline HTML table generation (30+ lines)

- **Severity**: 🟡 Medium
- **Description**: `business_card.py` lines 340–360 contain inline HTML table generation for the dividend history table with badge columns. This is raw HTML string concatenation in a page file, bypassing the `_info_card()` / `_白话_card()` pattern. The health score dimension cards (lines 242–248) also use inline HTML with hardcoded styles.
- **Impact**: Inconsistent with the component-based approach. The dividend table HTML is 20+ lines of string formatting that's hard to maintain.
- **Recommended Action**: Create a `render_badge_table(df, badge_col, badge_styles)` helper in `ui_components.py` (R2/R9). Move health dimension cards to a reusable `render_score_cards(scores, columns=5)` component.
- **Effort**: 1–2h as part of R9.

#### D20: `business_card.py` valuation interpretation duplicates `chart.py` logic

- **Severity**: 🟡 Medium
- **Description**: `business_card.py` lines 410–455 re-implement the PER percentile calculation that already exists in `chart.py:create_valuation_band_chart()`. The page calls `create_valuation_band_chart()` for the chart, then re-computes p25/p75 and the "偏高/偏低/中間" interpretation inline. This is wasted computation (the chart function already calculated these values but didn't return them).
- **Impact**: Double computation on every page render. If the valuation interpretation logic changes, it must be updated in both places.
- **Recommended Action**: Refactor `create_valuation_band_chart()` to return a `(fig, interpretation_dict)` tuple, where `interpretation_dict` contains `{p25, p75, current_per, text}`. The page uses the returned dict instead of re-computing.
- **Effort**: 0.5–1h.

#### D21: No new service modules — feature code concentrated in existing files

- **Severity**: 🟡 Medium
- **Description**: All Sprint 2 features were added to existing files (`analogy_engine.py`, `chart.py`, `business_card.py`) rather than creating new service modules. The Round 9 analysis recommended creating `summary_engine.py` (C37) and `delta_engine.py` (C39) as separate modules. Instead, everything went into `analogy_engine.py`.
- **Impact**: Contributes to D16 (god module). Makes it harder to locate feature logic. The `analogy_engine.py` import in `business_card.py` now pulls in 857 lines when only ~200 lines of analogies are needed.
- **Recommended Action**: Address as part of D16 refactoring. No immediate action needed if D16 is planned for Sprint 3.
- **Effort**: Included in D16.

### Performance Impact of Sprint 2

No new performance bottlenecks were introduced. The Sprint 2 features are computationally lightweight:

- **C37 (Key Takeaways)**: Dict lookup + string formatting. Negligible.
- **C39 (Deltas)**: Simple arithmetic on already-loaded data. Negligible.
- **C43 (Health Snowflake)**: Scoring functions are pure arithmetic on `extra_metrics` dict values. Negligible. The radar chart adds one Plotly figure render.
- **C45 (Valuation Band)**: The TTM EPS calculation iterates over all price rows × available EPS rows. For 2 years of daily data (~500 rows) × ~8 quarterly EPS values, this is ~4,000 iterations — acceptable but could be slow for longer time ranges. The `business_card.py` inline PER calculation (D20) duplicates this work.

**Net performance impact**: Neutral to slightly negative (D20 double computation). No new N+1 API patterns.

### Feasibility Assessment for Sprint 3+ Features

#### C44: Risk Analysis MVP (Sprint 3, ~6h)

- **Feasibility**: ✅ **High**. The health scoring functions in `analogy_engine.py` (D16) already compute per-dimension scores. Risk analysis can reuse the same 5-dimension framework but invert the narrative ("what's weak" vs "what's strong").
- **Dependencies**: `compute_health_scores()` (exists), `adaptive_engine.py` (exists for event-based risks).
- **Architecture Fit**: New `risk_engine.py` service module + section in `business_card.py`. Clean extension.
- **Risk**: Risk analysis and health scoring may confuse users if they tell different stories. Ensure consistent data sources.
- **Recommendation**: Proceed. Consider combining with C43 into a single "company assessment" service that produces both health and risk outputs from the same scores.

#### C41: Read Next Recommendations (Sprint 3, ~6.5h)

- **Feasibility**: ✅ **High**. No new data sources needed beyond what's in `group_structure.py` and `peer_comparison.py`.
- **Architecture Fit**: New `recommendation_engine.py` service + YAML data file + bottom section of `business_card.py`.
- **Risk**: D6 (hardcoded data) — relationship data must go in `src/data/relationships.yaml`, not in a Python module.
- **Recommendation**: Proceed as planned. Use YAML for relationship data.

#### C38: Compare Stories Phase 1 (Sprint 3, deferred, 8–10h)

- **Feasibility**: 🟡 **Medium**. The current `peer_comparison.py` already loads two companies' data via `_get_benchmark_data()`. C38 adds narrative comparison on top.
- **Architecture Fit**: New `narrative_comparator.py` service + tab in `peer_comparison.py`.
- **Risk**: D1/D17 (duplicate financial metrics/EPS extraction) — the narrative comparison will need financial metrics. Use the shared `financial_metrics.py` once R1 is done.
- **Recommendation**: Defer to Sprint 3. Ensure `narrative_comparator.py` has a clean interface for future LLM integration (Phase 2).

#### C42: Stock Screener / Discovery Engine (Sprint 4, ~8h)

- **Feasibility**: 🟡 **Medium**. Requires filtering the full stock universe (~1,800 stocks) by criteria. The `category_browser.py` already does sequential filtering (D7/P1).
- **Architecture Fit**: New `screener_engine.py` service + new page `screener_page.py`.
- **Risk**: Performance — screening 1,800 stocks sequentially will be slow. Need batch API calls (R3) or pre-computed screening data.
- **Recommendation**: Defer to Sprint 4. Consider pre-computing screening metrics for the 200 most-traded stocks to avoid performance issues.

#### C46: Export / Share Card (Sprint 4, ~4h)

- **Feasibility**: ✅ **High**. Pure presentation layer. Export the business card as image/PDF.
- **Dependencies**: None beyond existing page rendering.
- **Architecture Fit**: New `export_service.py` utility + button in `business_card.py`.
- **Risk**: Streamlit's limited export capabilities. May need `plotly.io.write_image()` for charts + HTML-to-image for cards.
- **Recommendation**: Low risk. Proceed in Sprint 4.

#### C47: Financial Education Academy (Sprint 4, ~10h)

- **Feasibility**: 🟡 **Medium**. Content curation is the bottleneck, not architecture.
- **Dependencies**: `company_facts.yaml` (exists), analogy functions (exists).
- **Architecture Fit**: New `academy_engine.py` service + `src/data/academy_lessons.yaml` + new page.
- **Risk**: D6 (hardcoded data) — lesson content must go in YAML, not Python.
- **Recommendation**: Defer to Sprint 4. Use YAML for all lesson content.

### Summary

Sprint 2 shipped 4 features with **no new service modules** and **no new performance bottlenecks**. The primary new debt is:

1. **`analogy_engine.py` god module** (D16) — 857 lines, 6 responsibilities. Highest priority to split.
2. **EPS extraction triplication** (D17) — same logic in 3 files. Fix as part of R1.
3. **Curated takeaways hardcoded** (D18) — 120-line dict in Python. Fix as part of R5.
4. **Inline HTML in business_card.py** (D19) — dividend table and score cards. Fix as part of R9.
5. **Valuation double-computation** (D20) — `chart.py` and `business_card.py` both compute PER percentiles. Quick fix.

**All Sprint 3+ features are feasible** with the current architecture. The main blockers are:
- R1 (financial_metrics extraction) needed for C38
- R3 (batch API calls) needed for C42 performance
- R5 (YAML migration) needed for C41, C47 data maintainability

**Recommended immediate actions** (Sprint 3):
1. **R1**: Extract `financial_metrics.py` (addresses D1, D2, D17) — 2–3h
2. **D20**: Refactor `create_valuation_band_chart()` to return interpretation — 0.5h
3. **D16**: Split `analogy_engine.py` into focused modules — 2–3h (can batch with R1)

---

*Created: 2026-06-17*
*Maintainer: System Architect*
*Next review: After Sprint 3 feature implementation*
