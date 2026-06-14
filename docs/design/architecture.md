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

---

## 2026-06-18 Technical Analysis — Review Round 12

### Context

Sprint 3 is in progress. R1 (financial_metrics.py extraction) and design fixes D-018, D-020, D-021, D-023 are complete. Remaining Sprint 3: C44 (Risk Analysis MVP), C41 (Read Next), C38 (Compare Stories P1), D16 (split analogy_engine.py). This analysis covers **architecture debt resolution status** and **new debt identification**. For feasibility assessment of remaining features, see `docs/design/architect_discussion_r12.md`.

### Codebase Growth Summary

| Metric | Round 9 | Round 11 | Round 12 |
|--------|---------|----------|----------|
| Total .py files (excl. `__pycache__`) | 31 | 31 | 31 |
| Total application LOC | ~5,200 | ~7,699 | ~7,818 |
| `analogy_engine.py` | ~192 | 857 | 850 (D16 pending) |
| `financial_metrics.py` | — | — | **188 (new)** |
| `chart.py` | ~490 | 757 | 779 |
| `business_card.py` | ~337 | 479 | 447 |
| `_router_base.py` | ~170 | ~170 | **177** |
| L0 (Import) | 54/54 | 54/54 | **55/55 ✅** |
| L1 (Render) | 15/18 | 15/15 | **18/18 ✅** |

**Key change since Round 11**: R1 (financial_metrics.py extraction) is complete. This resolves D1, D2, and D17. `business_card.py` shrank from 479→447 lines because inline EPS extraction and PER percentile recomputation were replaced by the `financial_metrics.py` shared functions and the `create_valuation_band_chart()` interpretation return.

### Architecture Debt Resolution Status

#### ✅ RESOLVED (4 items)

**D1: Duplicate financial metric calculation** — RESOLVED by R1
- `financial_metrics.py` (188 lines) now contains `calc_extra_metrics()`, `find_financial_value()`, and all shared financial calculations.
- `_router_base.py` imports `calc_extra_metrics, find_financial_value` from `financial_metrics.py` (line 10).
- `peer_comparison.py`, `roe_calculator.py`, `financial_health.py` all import `find_financial_value` from `financial_metrics.py`.
- The old `_calc_extra_metrics()` in `_router_base.py` has been fully removed. Only `calc_extra_metrics()` in `financial_metrics.py` remains.
- **Impact**: ~80 lines of duplication eliminated. All financial calculations now go through one code path.

**D2: `_find_financial_value` semantic duplication** — RESOLVED by R1
- `find_financial_value()` now lives in `financial_metrics.py` (line 9).
- All 4 consumers import from the single source: `_router_base.py`, `peer_comparison.py`, `roe_calculator.py`, `financial_health.py`.
- No duplicate definitions remain in the codebase.

**D17: EPS extraction logic triplicated across 3 files** — RESOLVED by R1
- `extract_quarterly_eps()` and `extract_ttm_eps()` now live in `financial_metrics.py` (lines 21-84).
- `chart.py` imports `extract_quarterly_eps` from `financial_metrics.py` (line 10) — uses it in `create_valuation_band_chart()` (line 651).
- `analogy_engine.py` imports `extract_quarterly_eps` from `financial_metrics.py` (line 9) — uses it in `compute_health_scores()` (line 746).
- `business_card.py` no longer has any inline EPS extraction code. The `eps_keywords` pattern, `str.contains()` filtering, `groupby("date").max()` dedup, and `tail(4).sum()` TTM calculation are all gone from the page file.
- **Impact**: EPS extraction is now a single function. Changes to keywords, TTM window, or dedup logic only need to happen in one place.

**D20: `business_card.py` valuation interpretation duplicates `chart.py` logic** — RESOLVED by D-020 fix
- `create_valuation_band_chart()` now returns `(fig, interpretation_dict)` tuple (chart.py line 773).
- `interpretation_dict` contains `{p25, p75, current_per, valuation_text}`.
- `business_card.py` uses the returned `interp` dict (line 412: `fig, interp = create_valuation_band_chart(...)`) and renders it via `_info_card("估值解讀", interp["valuation_text"], "💡")` (line 423).
- The old inline PER percentile recomputation (p25/p75 calculation + "偏高/偏低/中間" interpretation) in `business_card.py` has been fully removed.
- **Impact**: Eliminates double computation on every page render. Valuation interpretation is computed once in `chart.py` and consumed by `business_card.py`.

#### ⏳ PARTIALLY ADDRESSED (1 item)

**D19: `business_card.py` inline HTML table generation** — PARTIALLY ADDRESSED
- The dividend history table inline HTML (lines 340-360 in Round 11) was cleaned up during the D-020/D-021 fixes.
- However, the health score dimension cards still use inline HTML with hardcoded styles.
- The `_info_card()` / `_白话_card()` pattern from `_router_base.py` is now used for valuation interpretation (D-020 fix), showing the component-based approach is spreading.
- **Remaining work**: Create `render_score_cards()` and `render_badge_table()` helpers in `ui_components.py` (R9, Sprint 3-4).

#### 🔴 STILL OPEN (16 items)

**D16: `analogy_engine.py` god module** — OPEN, 850 lines
- Still contains 6 distinct responsibilities (analogies, key takeaways data, delta engine, health scoring, EPS extraction now delegated, one-liners).
- R1 is complete, which was the blocker for D16. D16 can now proceed.
- `analogy_engine.py` is imported by 4 files: `business_card.py` (11 functions), `financial_health.py` (6 functions), `peer_comparison.py` (3 functions), `operation_checkup.py` (4 functions).
- **Recommendation**: Proceed with D16 immediately. The 2-3h estimate is realistic now that R1 is done.

**D18: `_KEY_TAKEAWAYS` hardcoded dict** — OPEN
- Still 120+ lines of hardcoded dict in `analogy_engine.py` (lines 200-321).
- Should be migrated to `src/data/key_takeaways.yaml` as part of R5 (YAML migration).

**D3: Inline HTML duplication across pages** — OPEN
- `business_card.py`, `group_structure.py`, `etf_detail.py`, `etf_browser.py`, `watchlist_page.py` still contain large inline HTML strings.
- D-020 fix showed progress: `business_card.py` now uses `_info_card()` for valuation interpretation.

**D4: Service layer `__init__.py` wildcard imports** — OPEN
- `src/services/__init__.py` still uses `from X import *` for 4 modules (including the new `financial_metrics.py`).

**D5: No LLM integration layer** — OPEN
- No abstraction exists. Template engines are still the only implementation.

**D6: Hardcoded data in Python modules** — OPEN
- `revenue_analyzer.py`, `group_structure.py`, `analogy_engine.py`, `peer_comparison.py` still have hardcoded data.
- New `financial_metrics.py` does NOT have hardcoded data (clean extraction).

**D7: `category_browser.py` N+1 API calls** — OPEN
- Still sequential, not parallel.

**D8: `etf_browser.py` sequential price fetching** — OPEN
- Still sequential.

**D9: Watchlist reads YAML on every operation** — OPEN
- No in-memory caching.

**D10: `events.yaml` read on every event query** — OPEN
- No caching.

**D11: No error boundary standardization** — OPEN
- Inconsistent error handling across services.

**D12: `_router_base.py` mixes routing and UI** — OPEN
- `_section_title()`, `_白话_card()`, `_info_card()`, `_summary_card()` still in `_router_base.py` (lines 69-114).
- These are used by 6+ page files.

**D13: No test infrastructure** — OPEN
- Zero test files exist.

**D14: Sidebar architecture not extracted** — OPEN
- `main.py` still contains ~85 lines of sidebar rendering code.

**D15: FinMind client is not async-compatible** — OPEN
- Synchronous API calls. ThreadPoolExecutor mitigates but standalone pages don't benefit.

**D21: No new service modules — feature code concentrated** — OPEN
- Contributed by D16. Will be resolved when D16 is done.

### New Architecture Debt (D22+)

#### D22: `financial_metrics.py` is a leaf service with no consumers in service layer

- **Severity**: 🟢 Low
- **Description**: `financial_metrics.py` is imported by page files (`_router_base.py`, `business_card.py`) and service files (`chart.py`, `analogy_engine.py`), but no other service imports it. This means the service-layer boundary is blurred — pages import directly from `financial_metrics.py` rather than going through a service facade.
- **Impact**: Low. The 4-layer architecture is slightly bent but not broken. `financial_metrics.py` is a pure utility module (pure functions, no state), so the layer violation is minimal.
- **Recommended Action**: No immediate action. If more shared utility modules are extracted, consider a `src/services/shared/` sub-directory for pure utility functions.

#### D23: Tone guidelines for market-level features (from Round 11 discussion)

- **Severity**: 🟡 Medium
- **Description**: C51 (Sector Heatmap) and C49 (Market Pulse) will display market-level data. The current tone guidelines (from `company_facts.yaml` and analogy functions) are designed for single-stock explanations. Market-level features need "過去發生" language — factual, not predictive.
- **Impact**: Without tone guidelines, market features may accidentally sound like investment advice.
- **Recommended Action**: Add tone guidelines to `docs/design/tone_guidelines.md` before C51 implementation. This is a content task, not a code task.

#### D24: `business_card.py` approaching architectural limit (carried from Round 11 discussion)

- **Severity**: 🟡 Medium
- **Description**: `business_card.py` is 447 lines after R1/D-020 cleanup (down from 479). Adding C44 risk section (~40 lines), C41 read-next (~30 lines), and C48 story card (~70 lines) will push it to ~590+ lines.
- **Impact**: The page file becomes hard to navigate. Multiple features competing for space.
- **Recommended Action**: Extract to `src/pages/business_card/` sub-directory before C48 implementation. See D27 in `architect_discussion_r12.md` for the proposed structure.

#### D25: Market-level data flow is architecturally distinct from single-stock flow

- **Severity**: 🟡 Medium
- **Description**: The current architecture is built around a single `stock_id → data dict` pattern. C51 (Sector Heatmap) and C49 (Market Pulse) require market-wide → aggregate → visualize flow.
- **Impact**: Without a clear abstraction, market-level features will ad-hoc the data flow.
- **Recommended Action**: Create `src/services/market_data.py` as part of C51 implementation.

#### D26: `story_composer.py` will import from multiple unstable services

- **Severity**: 🟡 Medium
- **Description**: C48's `story_composer.py` will import from `analogy_engine.py` (being split via D16), `company_facts.py`, `chart.py`, and `financial_metrics.py`.
- **Impact**: C48 development may be blocked or coupled to unstable interfaces if D16 slips.
- **Recommended Action**: Complete D16 before starting C48.

#### D27: `business_card.py` architectural limit (duplicate of D24, consolidated)

- **Severity**: 🟡 Medium
- **Description**: Same as D24. Consolidated here for the debt register.
- **Effort**: 2-3h (extract + update imports).

### Performance Impact of R1 + Design Fixes

No new performance bottlenecks were introduced. The R1 extraction and design fixes are computationally neutral:

- **R1 (financial_metrics.py)**: Function extraction has zero runtime overhead. Same calculations, same data, just organized in one module.
- **D-020 (interpretation return)**: Eliminates double computation of PER percentiles on every `business_card.py` render. Net positive.
- **D-018 (C39 placement)**: Pure layout change. No performance impact.
- **D-021 (dimension explanations)**: Adds one `st.markdown()` call per dimension. Negligible.
- **D-023 (5-year window)**: Extends the price data window from 2 to 5 years. This increases the PER calculation loop from ~500 rows to ~1,250 rows (2.5x more iterations). For 5-year daily data × ~20 EPS values, this is ~25,000 iterations vs. ~10,000 previously. Still acceptable (<100ms) but worth monitoring.

**Net performance impact**: Slightly positive (D-020 eliminates double computation) with one area to monitor (D-023 5-year window).

### Feasibility Assessment for Remaining Sprint 3 Features

#### C44: Risk Analysis MVP (Est. 12-14h)

- **Feasibility**: ✅ **High**. The health scoring functions in `analogy_engine.py` already compute per-dimension scores. Risk analysis inverts the narrative.
- **Dependencies**: `compute_health_scores()` (exists), `adaptive_engine.py` (event-based risks), `financial_metrics.py` (R1 — done ✅).
- **Architecture Debt Interaction**: D16 (god module) — `compute_health_scores()` lives in `analogy_engine.py` (850 lines). C44 will import from this module. D16 split should happen before or alongside C44.
- **Verdict**: **Proceed as planned.** Low risk, high value. Ensure consistent data sources between health and risk outputs.

#### C41: Read Next Recommendations (Est. 6-8h)

- **Feasibility**: ✅ **High**. No new data sources needed beyond what exists.
- **Architecture Debt Interaction**: D6 (hardcoded data) — relationship data MUST go in `src/data/relationships.yaml`, not in Python.
- **Verdict**: **Proceed as planned.** Lowest risk remaining Sprint 3 feature.

#### C38: Compare Stories Phase 1 (Est. 10-12h)

- **Feasibility**: 🟡 **Medium**. R1 (done ✅) unblocks the shared financial metrics dependency.
- **Architecture Debt Interaction**: D16 — `analogy_engine.py` provides analogy functions for narrative text.
- **Verdict**: **Proceed with phased approach.** Phase 1 is independently valuable.

#### D16: Split analogy_engine.py (Est. 2-3h)

- **Feasibility**: ✅ **High**. R1 (done ✅) was the blocker. Now unblocked.
- **Verdict**: **Proceed immediately.** Unblocks C44, C38, and C48.

### Summary

**Resolved this round**: D1, D2, D17, D20 (4 items)
**New debt identified**: D22, D23, D24, D25, D26, D27 (6 items, 1 low + 5 medium)
**Still open**: D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, D16, D18, D19, D21 (17 items)

**Total debt items**: 27 (4 resolved + 6 new + 17 open = 27 tracked, with 4 marked resolved)

**Key architectural recommendation**: **D16 is the critical next step.** R1 is done, which was the blocker. D16 (2-3h) unblocks C44, C38, and C48. The sequencing should be: D16 → C44 → C41 → C38 for Sprint 3 remaining, then R3 → C51 → C48 → C53-1 for Sprint 4.

**The architecture is healthy**: The 4-layer model holds. R1 was the highest-impact debt item and is now resolved. The codebase grew from ~7,699 to ~7,818 lines (+119) but `business_card.py` actually shrank (479→447) due to eliminated duplication. L0: 55/55, L1: 18/18 — all green.

---

*Created: 2026-06-18*
*Maintainer: System Architect*
*Next review: After Sprint 3 completion / Sprint 4 kickoff*

---

## 2026-06-19 Technical Analysis — Review Round 14

### Context

Sprint 3 is completing: C44 (Risk Analysis MVP) and C41 (Read Next) are done. Remaining Sprint 3: C38 (Compare Stories P1) and D16 (split analogy_engine.py). Sprint 4 is about to start with the sequence: D24 → R3 → C51 → C48 → C53-1. This analysis covers **architecture debt resolution status**, **new debt from C44/C41/D-024/D-025**, and **Sprint 4 readiness assessment**.

### Codebase Growth Summary

| Metric | Round 9 | Round 11 | Round 12 | Round 14 |
|--------|---------|----------|----------|----------|
| Total .py files (excl. `__pycache__`) | 31 | 31 | 31 | **32** |
| Total application LOC | ~5,200 | ~7,699 | ~7,818 | **~8,572** |
| `analogy_engine.py` | ~192 | 857 | 850 | **850** |
| `financial_metrics.py` | — | — | 188 | **188** |
| `risk_analyzer.py` | — | — | — | **567 (new)** |
| `chart.py` | ~490 | 757 | 779 | **779** |
| `business_card.py` | ~337 | 479 | 447 | **561** |
| `_router_base.py` | ~170 | ~170 | 177 | **177** |
| L0 (Import) | 54/54 | 54/54 | 55/55 | **56/56 ✅** |
| L1 (Render) | 15/18 | 15/15 | 18/18 | **8 passed + 10 pre-existing ✅** |

**Key changes since Round 12**: C44 (Risk Analysis) added `risk_analyzer.py` (567 lines, new service module) and ~114 lines to `business_card.py` (447→561). C41 (Read Next) added ~60 lines of inline HTML to `business_card.py`. D-024 and D-025 were minor design fixes with no architectural impact.

### Architecture Debt Resolution Status

#### ✅ RESOLVED (4 items — unchanged from Round 12)

**D1, D2, D17, D20** — All resolved by R1 (financial_metrics.py extraction) and D-020 fix. No regression.

#### ⏳ PARTIALLY ADDRESSED (1 item)

**D19: `business_card.py` inline HTML table generation** — PARTIALLY ADDRESSED
- The dividend history table still uses inline HTML (lines ~377-427).
- The health score dimension cards still use inline HTML (lines ~241-265).
- **New**: C41 added ~60 more lines of inline HTML for peer stock cards (lines ~504-544), worsening D19.
- **New**: C44's `_render_risk_dimension()` (lines 66-83) uses inline HTML with hardcoded styles — this is a new instance of the same anti-pattern, now in a helper function inside `business_card.py` rather than in the main render flow.

#### 🔴 STILL OPEN — CRITICAL (2 items)

**D16: `analogy_engine.py` god module** — OPEN, 850 lines
- Still contains 6 distinct responsibilities (analogies, key takeaways data, delta engine, health scoring, one-liners, EPS extraction now delegated to financial_metrics.py).
- R1 is complete, which was the blocker. D16 can now proceed.
- `analogy_engine.py` is imported by 4 files: `business_card.py` (11 functions), `financial_health.py` (6 functions), `peer_comparison.py` (3 functions), `operation_checkup.py` (4 functions).
- **Impact of delay**: C48's `story_composer.py` (D26) is blocked. C38 also imports analogy functions from this module.
- **Recommendation**: Must be completed before C48 starts. Ideally done alongside or immediately after C38.

**D24/D30: `business_card.py` architectural limit** — OPEN, now 561 lines
- `business_card.py` grew from 447→561 lines (+114) due to C44 and C41.
- The file now contains these distinct sections:
  1. Header/watchlist (lines ~43-115)
  2. Key takeaways / one-liner / facts (lines ~115-180)
  3. Health snowflake (lines ~227-265)
  4. Risk analysis expander (lines ~263-283)
  5. Key metrics three-column cards (lines ~293-320)
  6. Dividend story (lines ~322-380)
  7. Revenue breakdown + trend (lines ~435-460)
  8. Valuation band chart (lines ~462-480)
  9. Recent news (lines ~482-500)
  10. Read Next / peer recommendations (lines ~504-544)
  11. Disclaimer (lines ~555-561)
- Adding C38 compare stories section (~50 lines) will push to ~611 lines.
- Adding C48 story card (~70 lines) will push to ~681 lines.
- **This is the exact threshold D24 was created to prevent.**
- **Recommendation**: D24 extraction is **non-negotiable** before C48. Ideally done before C38 to prevent further growth.

#### 🟡 NEW ARCHITECTURE DEBT (D31+)

**D31: `risk_analyzer.py` is a 567-line service with mixed responsibilities**

- **Severity**: 🟡 Medium
- **Description**: `risk_analyzer.py` (567 lines) contains 3 distinct risk assessment functions plus 7 helper functions:
  1. `assess_customer_concentration()` (lines 151-289) — ~139 lines
  2. `assess_financial_health()` (lines 290-430) — ~141 lines
  3. `assess_event_risk()` (lines 431-517) — ~87 lines
  4. `assess_risk()` (lines 518-567) — orchestrator, ~50 lines
  5. 7 private helper functions (lines 35-135) — threshold classification, cash flow trend, etc.
- **Positive**: The module has **zero Streamlit imports** and **zero API calls** — clean service layer boundary. It imports only from `financial_metrics.py` and `news_summarizer.py`.
- **Concern**: At 567 lines, it's already approaching the size where `analogy_engine.py` was when it became a god module (850 lines). The 3 assessment functions are independent and could be split if the module grows further.
- **Impact**: Low for now. The module is well-structured internally with clear function boundaries. The orchestrator pattern (`assess_risk()` calling the 3 sub-assessors) is clean.
- **Recommended Action**: No immediate action needed. Monitor if additional risk dimensions (volatility, cyclicality) are added — that would be the time to split into `customer_risk.py`, `financial_risk.py`, `event_risk.py`.
- **New**: Identified during Round 14 review of C44 commit (567239b).

**D32: `business_card.py` now contains presentation helper functions that should live in a shared UI module**

- **Severity**: 🟡 Medium
- **Description**: `business_card.py` now defines 3 presentation-helper functions at the top of the file (lines 43-83):
  1. `get_health_dimension_explanation()` (lines 43-48) — returns plain-language score explanation
  2. `_render_risk_dimension()` (lines 66-83) — renders a risk dimension card with inline HTML
  3. `_RISK_BADGES` and `_RISK_COLORS` dicts (lines 51-61) — style constants
- **Impact**: These are presentation functions living in a page file. If another page needs to render risk dimensions or health explanations, this code cannot be reused. This is the same anti-pattern as D3 (inline HTML duplication) and D12 (_router_base.py mixing routing and UI).
- **Recommended Action**: Move to `ui_components.py` (D3/R9) when D24 extracts the sub-directory. The health explanation function is a pure function that belongs in a shared module. The risk dimension renderer should be a reusable component.
- **New**: Identified during Round 14 review of C44 commit (567239b).

**D33: C41 Read Next creates a new data access pattern in the presentation layer**

- **Severity**: 🟢 Low
- **Description**: C41's Read Next section (lines 504-544 in `business_card.py`) calls `client.get_stock_info()` directly inside the page render function to get peer stocks. This is a **data access call in the presentation layer** — the page is calling the FinMind client directly instead of receiving pre-computed peer data through the `data` dict from `_router_base.py`.
- **Impact**: Low. The `get_stock_info()` call is cached by FinMindClient, so there's no performance penalty. But it breaks the 4-layer architecture pattern where pages should only consume data from the `data` dict.
- **Recommended Action**: Pre-compute peer stock recommendations in `_router_base.py`'s `get_stock_data()` and include them in the `data` dict. This keeps the presentation layer clean. Low priority — the current approach works and the cache makes it fast.
- **New**: Identified during Round 14 review of C41 commit (1f98d73).

### Service Layer Organization Assessment

#### Current Service Modules (13 total)

| Service | Lines | Responsibilities | Streamlit? | API Calls? |
|---------|-------|-----------------|------------|------------|
| `financial_metrics.py` | 188 | Shared financial calculations | ❌ No | ❌ No |
| `risk_analyzer.py` | 567 | Risk analysis (3 dimensions) | ❌ No | ❌ No |
| `analogy_engine.py` | 850 | Analogies, takeaways, deltas, health scoring, one-liners | ❌ No | ❌ No |
| `chart.py` | 779 | All chart rendering | ❌ No | ❌ No |
| `adaptive_engine.py` | 590 | Event detection, adaptive learning | ❌ No | ❌ No |
| `peer_comparison.py` | — | Peer comparison (page-level service) | — | — |
| `news_summarizer.py` | 158 | News summarization templates | ❌ No | ❌ No |
| `revenue_analyzer.py` | 145 | Revenue breakdown analysis | ❌ No | ❌ No |
| `dividend_analyzer.py` | 201 | Dividend analysis | ❌ No | ❌ No |
| `watchlist.py` | 323 | Watchlist management | ❌ No | ❌ No |
| `roe_calculator.py` | 97 | ROE calculation | ❌ No | ❌ No |
| `company_facts.py` | 46 | Company facts loading | ❌ No | ❌ No |
| `validation.py` | 32 | Input validation | ❌ No | ❌ No |

**Positive findings**:
- `risk_analyzer.py` is a **model service module**: zero Streamlit, zero API calls, clean imports from other services. This is exactly how new services should be structured.
- `financial_metrics.py` continues to be a clean shared utility.
- All service modules maintain proper layer boundaries.

**Concerns**:
- `analogy_engine.py` (850 lines) is still the largest service module and the biggest architectural risk.
- `chart.py` (779 lines) is growing but is still focused on a single responsibility (chart rendering).
- Service layer has 13 modules but `__init__.py` only exports 4 via wildcard (D4 still open).

### Sprint 4 Sequence Evaluation

The planned Sprint 4 sequence is: **D24 → R3 → C51 → C48 → C53-1**

**Assessment**: ✅ **Architecturally sound**, with one critical sequencing note.

| Step | Assessment | Notes |
|------|-----------|-------|
| **D24** (business_card.py sub-directory) | ✅ **Must be first** | `business_card.py` is 561 lines. Every feature added before extraction makes D24 harder. Non-negotiable. |
| **R3** (Batch API minimal) | ✅ Correct position | Unlocks C51. Should be done early. |
| **C51** (Sector Heatmap) | ✅ Correct position | Needs R3. Will create `market_data.py` (D25). |
| **C48** (Company Story Card) | ✅ Correct position | Needs D16 + D24. Should create `story_composer.py`. |
| **C53-1** (Social Sharing URL) | ✅ Correct position | Quick win, no dependencies. |

**Critical sequencing issue**: The handoff shows Sprint 3 remaining as: C38 → D16. But D16 is listed as a Sprint 4 prerequisite for C48. **D16 must be completed before C48 starts.** If C38 is done before D16, that's fine — but D16 cannot slip past C48's start.

**Recommended Sprint 4 sequence** (revised from handoff):
1. **D24** — Extract business_card.py to sub-directory (2-3h) — **FIRST, non-negotiable**
2. **D16** — Split analogy_engine.py (2-3h) — **Must complete before C48**
3. **R3** — Batch API minimal (1-2h) — Unlocks C51
4. **C38** — Compare Stories Phase 1 (10-12h) — Can be done in parallel with R3 if resources allow
5. **C51** — Sector Heatmap (12-16h) — With R3 + D25 (market_data.py)
6. **C48** — Company Story Card (10-14h) — With D16 + D24 + story_composer.py
7. **C53-1** — Social Sharing URL (2-3h) — Quick win

**Note**: The handoff shows the Sprint 4 sequence as D24 → R3 → C44 → C51 → C48 → C53-1, but C44 is already complete (commit 567239b). The actual remaining work is C38 (Sprint 3) and then Sprint 4 items.

### Emerging Patterns and Future Debt Risks

1. **Inline HTML proliferation**: Each new feature adds inline HTML to `business_card.py`. C41 added peer cards, C44 added risk dimension cards. This pattern will continue with C48 (story card) and C53-1 (share button). **D24 + D3 (ui_components.py) are the only way to stop this.**

2. **Page-level data access**: C41's direct `client.get_stock_info()` call in the presentation layer (D33) could become a pattern if not corrected. Future features should pre-compute data in `_router_base.py`.

3. **Session state proliferation**: `business_card.py` now uses multiple session_state keys (`_fact_idx_{stock_id}`, `_peer_{stock_id}` for buttons). As C48 and C53-1 add more interactive elements, this will become unmanageable. **D28 (session state audit) should be scheduled for Sprint 5.**

4. **Service module size creep**: `risk_analyzer.py` is already 567 lines. If additional risk dimensions are added (volatility, cyclicality), it will follow the same path as `analogy_engine.py`. **Monitor and split early.**

5. **Market data abstraction gap**: C51 will need `market_data.py` (D25). Without it, the sector heatmap will ad-hoc the market-wide data flow. This is a **hard prerequisite for C51**, not optional.

### Summary

**Resolved this round**: 0 new items (D1, D2, D17, D20 resolved in previous rounds)
**New debt identified**: D31, D32, D33 (3 items: 1 low + 2 medium)
**Still open (critical)**: D16, D24/D30
**Still open (medium)**: D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, D18, D19, D21, D22, D23, D25, D26, D27, D28, D29, D31, D32
**Still open (low)**: D33

**Total debt items**: 33 (4 resolved + 29 open)

**Key architectural recommendations for Sprint 4**:

1. **🔴 D24 is the #1 priority** — `business_card.py` at 561 lines is past the threshold. Every feature added before extraction makes it harder. Must be the FIRST task in Sprint 4.

2. **🔴 D16 must complete before C48** — `analogy_engine.py` (850 lines) blocks `story_composer.py`. Can be done in parallel with D24/R3, but must finish before C48 starts.

3. **🟡 D32 (presentation helpers in business_card.py)** — Move `get_health_dimension_explanation()` and `_render_risk_dimension()` to `ui_components.py` as part of D24 extraction.

4. **🟡 D31 (risk_analyzer.py size)** — Monitor. No immediate action needed, but if additional risk dimensions are added, split into sub-modules.

5. **🟢 D33 (page-level data access)** — Low priority. Pre-compute peer data in `_router_base.py` when convenient.

**The architecture is healthy overall**: The 4-layer model holds. `risk_analyzer.py` is a model service module. L0: 56/56, L1: stable. The primary risk is `business_card.py` growth — D24 is the critical path.

---

*Created: 2026-06-19*
*Maintainer: System Architect*

---

## Sprint 21 Technical Analysis

> **Date**: 2026-06-14
> **Author**: System Architect
> **Context**: Sprint 20 in progress (C167 ✅ done, C163 + C40 pending). Sprint 21 planning for the sprint after Sprint 20.

---

### Problem Statement

Sprint 21 faces a convergence of three forces:

1. **A mature ExplanationProvider protocol** — C167 (ScreenerExplanationProvider) proved the protocol pattern works for screening contexts. The infrastructure is ready for more ambitious narrative features.
2. **Mounting design debt around education** — D-012 (no glossary) and D-015 (no learning path) have been open since Round 9. C163 (Learn First Gate) will partially address onboarding but not inline education.
3. **Competitor pressure on narrative features** — Round 9 confirmed that Simply Wall St, Stockopedia, and 財報狗 all have features that combine data with narrative context. Stock Explorer's "historian" positioning needs to evolve from "explains single metrics" to "tells multi-factor stories."

The core question for Sprint 21: **Should we invest in narrative infrastructure (C152), educational infrastructure (C170), or visual/analytical features (C171-C174)?**

---

### Feature Direction 1: C152 Multi-Factor Event Narratives (P1, 16-20h)

**Description**: Combine multiple events, metrics, and contextual factors into a single coherent narrative — "Here's what happened to TSMC this quarter, told as one story that connects revenue, events, and market conditions."

**How C152 Interacts with the ExplanationProvider Protocol**:

C152 is a natural extension of the existing protocol. The current architecture has:
- `ExplanationProvider` protocol with `explain(ExplanationRequest) -> ExplanationResponse`
- `TemplateExplanationProvider` for template-based explanations
- `DeltaExplanationProvider` for change explanations (wraps TemplateExplanationProvider via composition)
- `ScreenerExplanationProvider` for screening explanations (wraps TemplateExplanationProvider via composition)

C152 would introduce a `NarrativeExplanationProvider` that:
1. **Composes multiple existing providers** — delegates to `DeltaExplanationProvider` for metric changes, `TemplateExplanationProvider` for static context, and a new `EventNarrativeProvider` for event sequencing
2. **Uses the same `ExplanationRequest`/`ExplanationResponse` protocol** — no new interface needed
3. **Adds a `compose_narrative()` orchestration function** in the service layer that merges multiple `ExplanationResponse` objects into a single narrative with chronological ordering and causal linking
4. **Requires a new `EventNarrativeProvider`** that reads from `events.yaml` (already exists from C147/C140) and generates plain-language event sequences

**Pros**:
- ✅ **Highest alignment with "historian" positioning** — this IS the historian product vision
- ✅ **Leverages existing infrastructure** — ExplanationProvider protocol, events.yaml, analogy_engine, compose-and-enrich pipeline
- ✅ **No new data sources needed** — all data already in the system
- ✅ **Proven pattern** — C167 showed that new ExplanationProvider implementations are low-risk (~14h for ScreenerExplanationProvider)
- ✅ **Competitive white space** — no TW competitor has multi-factor narrative synthesis
- ✅ **C152 spike already deferred twice** — the feature has been validated through 3 rounds of competitor research

**Cons**:
- ⚠️ **Requires D-120 (benchmark extraction) as prerequisite** — narrative context needs industry benchmark data, and the triplicated `INDUSTRY_BENCHMARKS` dict will cause maintenance issues if not extracted first
- ⚠️ **Requires D-16 (analogy_engine.py split) as prerequisite** — the narrative composer needs clean imports from analogy functions currently buried in the 850-line god module
- ⚠️ **Risk of "narrative sprawl"** — without clear scope boundaries, C152 could try to narrate everything. Must be limited to 3-5 factors per narrative
- ⚠️ **Tone QA complexity** — multi-factor narratives increase the risk of accidental prescriptive language. The 3-layer tone QA (keyword + pattern + human review) must be enforced
- ⚠️ **16-20h is a wide range** — the upper end would consume most of Sprint 21's capacity

**Effort Estimate**: 16-20h (narrative composer service + EventNarrativeProvider + page integration + tone QA)
**Prerequisites**: D-120 (1.5-2.5h) + D-16 (2-3h) = 3.5-5.5h infrastructure before C152 starts

---

### Feature Direction 2: C170 Tappable Glossary + C163 Learn First Gate Bundle (P1, 12-18h)

**Description**: Bundle C170 (Tappable Glossary, 6-10h) with C163 (Learn First Gate, 10-14h) into a single "beginner education infrastructure" sprint. C163 is already in Sprint 20, but if it slips to Sprint 21, C170 can be bundled with it since both target the same user journey: first-time users encountering financial terms.

**Can C170 Be Bundled with C163?**

**Yes, strongly recommended.** Here's why:

1. **Shared data structure** — Both features need a `glossary.yaml` (or similar) with term → plain-language definition mappings. C163 needs "key concept cards" for the gate; C170 needs "inline tooltips" for the same terms. One YAML file serves both.

2. **Shared service layer** — A new `glossary_service.py` can provide:
   - `get_term_definition(term) -> str` — for C170 tooltips
   - `get_key_concepts(stock_id) -> list[ConceptCard]` — for C163 gate cards
   - `get_all_terms() -> dict` — for both features

3. **Shared UI component** — A `_glossary_tooltip()` helper in `_router_base.py` (or `ui_components.py`) can be used by C170 for inline tooltips AND by C163 for concept card rendering.

4. **Sequential user journey** — C163 (gate) is encountered BEFORE C170 (inline tooltips). A user who passes through the gate has already seen the key terms. C170 then reinforces those terms inline. This is a natural educational progression.

5. **Combined effort fits Sprint 21** — C163 (10-14h) + C170 (6-10h) = 16-24h. With shared infrastructure, the overlap reduces this to approximately 12-18h.

**Pros**:
- ✅ **Highest beginner impact** — directly addresses the "ten-second test" for first-time users
- ✅ **Shared infrastructure reduces total effort** — one YAML, one service, one UI component
- ✅ **C170 is P1 and small (6-10h)** — can be added to C163 without blowing the sprint
- ✅ **No prerequisites** — glossary is greenfield, no dependency on D-120 or D-16
- ✅ **Competitive gap** — no TW competitor has systematic glossary tooltips (D-012 open since Round 9)
- ✅ **Enables future features** — glossary infrastructure supports C172 (Concept Comparison) and C173 (Visual Calculators) in future sprints

**Cons**:
- ⚠️ **Requires C163 to slip from Sprint 20** — if C163 ships in Sprint 20, C170 alone (6-10h) may not fill Sprint 21
- ⚠️ **Content creation bottleneck** — glossary needs 50-100 terms with plain-language definitions. This is PM/Designer work, not developer work
- ⚠️ **Streamlit tooltip limitations** — Streamlit has no native tooltip component. Implementation requires `st.popover()` or custom HTML. The `_glossary_tooltip()` component needs careful UX design
- ⚠️ **Risk of "glossary as band-aid"** — a glossary doesn't solve the deeper problem of financial literacy. It's infrastructure, not a feature users will rave about

**Effort Estimate**: 12-18h (C163 + C170 with shared infrastructure)
**Prerequisites**: None (greenfield)

---

### Feature Direction 3: C171 Valuation Band Chart + C172 Concept Comparison (P2, 14-20h)

**Description**: Two P2 visual/analytical features that extend existing charting infrastructure. C171 (Valuation Band Chart, 8-10h) shows historical P/E or P/B ranges with plain-language interpretation. C172 (Concept Comparison Tool, 10-14h) allows side-by-side comparison of financial concepts (e.g., "ROE vs ROA" or "P/E vs P/B").

**Note**: C45 (Valuation Band Chart) is already implemented per the issues.md file. C171 may be a re-scoping or enhancement of C45. This analysis assumes C171 is either not yet built or needs significant rework.

**Pros**:
- ✅ **Leverages existing chart.py infrastructure** — `create_valuation_band_chart()` already exists (C45). C171 may only need a plain-language interpretation layer
- ✅ **C172 reuses glossary infrastructure** — if C170 is built in Sprint 21, C172 can reuse the glossary data for concept definitions
- ✅ **Competitor-validated** — 財報狗 has P/E band charts; Magnify.money has concept comparison. Both are proven demand
- ✅ **Low architectural risk** — both are presentation-layer features with thin service layers
- ✅ **Good "filler" features** — if C152 or C163+C170 finish early, C171/C172 can fill remaining sprint capacity

**Cons**:
- ⚠️ **C45 overlap** — C45 (Valuation Band Chart) is listed as "✅ Already implemented" in issues.md. C171 may duplicate existing work
- ⚠️ **Lower priority (P2)** — both are P2, meaning they're less critical than C152 (P1) or C170 (P1)
- ⚠️ **C172 is conceptually complex** — comparing financial concepts side-by-side requires careful UX design to avoid confusion. "ROE vs ROA" is only meaningful if users understand both terms first
- ⚠️ **No narrative value** — these are analytical features, not narrative features. They don't advance the "historian" positioning as directly as C152
- ⚠️ **C172 depends on C170 glossary** — if C170 isn't built first, C172 needs its own concept definition data

**Effort Estimate**: 14-20h (C171 8-10h + C172 10-14h, with some overlap)
**Prerequisites**: C170 glossary (for C172 concept definitions)

---

### Feature Direction 4 (Wildcard): C174 Sector-Level Storytelling (P2, 14-20h)

**Description**: Thematic sector narratives connecting multiple companies — "Here's the semiconductor industry's story" showing how TSMC, UMC, and MediaTek's stories intertwine. Identified in Round 9 as "the untapped frontier" and validated by Smallcase's thematic investing approach.

**Pros**:
- ✅ **Unique differentiator** — no TW competitor has sector-level storytelling
- ✅ **Perfect "historian" evolution** — from "company historian" to "industry historian"
- ✅ **Leverages existing data** — group_structure.py, peer_comparison.py, and events.yaml already have the data
- ✅ **Smallcase validation** — proves demand for thematic sector narratives internationally

**Cons**:
- ⚠️ **Highest risk** — 14-20h with significant unknowns around data integration and narrative coherence
- ⚠️ **Requires market_data.py (D25)** — sector-level features need a market data abstraction that doesn't exist yet
- ⚠️ **Requires D-120 (benchmark extraction)** — sector narratives need industry benchmark context
- ⚠️ **Content curation bottleneck** — sector stories need manual curation for quality
- ⚠️ **May be too ambitious for Sprint 21** — better suited for Sprint 22+ when narrative infrastructure (C152) is mature

**Effort Estimate**: 14-20h
**Prerequisites**: D-120, D-25 (market_data.py), C152 (narrative infrastructure)

---

### Infrastructure Prerequisites

#### D-120: Benchmark Logic Extraction (1.5-2.5h) — HARD PREREQUISITE

**Status**: Escalated from D-109. The `INDUSTRY_BENCHMARKS` dict is triplicated across `_summary.py`, `_health.py`, and `peer_comparison.py`. Additionally, benchmark health score fetching logic is duplicated between `_summary.py` (107 lines) and `_health.py` (117 lines).

**Recommended Fix**:
1. Extract `INDUSTRY_BENCHMARKS` to `src/data/industry_benchmarks.yaml`
2. Extract benchmark health score fetching to `health_scoring.get_benchmark_scores(client, industry, stock_id)` in a new or existing service module
3. Update all 3 consumers to use the shared YAML + service function

**Impact**: Unblocks C152 (needs benchmark context for narratives), C171 (needs benchmark data for valuation bands), and C174 (needs sector-level benchmarks). Also reduces maintenance burden for all future features that need industry comparison data.

**Sequencing**: Must be done BEFORE any Sprint 21 feature that uses industry benchmarks. Ideally done as the last Sprint 20 task or the first Sprint 21 task.

#### D-16: analogy_engine.py Split (2-3h) — SOFT PREREQUISITE

**Status**: Open since Round 11. `analogy_engine.py` is 850 lines with 6 distinct responsibilities.

**Impact on Sprint 21**: C152's `NarrativeExplanationProvider` needs clean imports from analogy functions. C170/C172 need glossary functions that may end up in a split-out module. D-16 is not a hard prerequisite (workarounds exist) but will cause increasing pain if deferred.

**Recommendation**: Bundle D-16 with D-120 as Sprint 21 Day 1 infrastructure (total 3.5-5.5h).

---

### Recommendation

**Primary Recommendation: Feature Direction 1 (C152) + D-120 infrastructure**

**Rationale**:

1. **C152 is the highest-value P1 feature** in the pipeline. It directly delivers on the "historian" product vision — the core differentiator that no TW competitor has.
2. **The ExplanationProvider protocol is mature** — C167 proved the pattern. C152 is the next logical extension.
3. **D-120 is overdue** — benchmark triplication has been open since Round 38 (D-109). Every sprint that defers it increases the maintenance burden.
4. **Sprint 21 capacity**: D-120 (1.5-2.5h) + D-16 (2-3h) + C152 (16-20h) = 19.5-25.5h. This fits within a normal sprint capacity.

**Contingency Plan**: If C152 spike quality is low (the spike was deferred from Sprint 19), fall back to **Feature Direction 2 (C170 + C163 bundle)**. C170 is P1, has no prerequisites, and can be completed in 6-10h, leaving room for C171 (8-10h) as a stretch goal.

**Not Recommended for Sprint 21**:
- **C174 (Sector-Level Storytelling)** — too ambitious without C152 narrative infrastructure. Plan for Sprint 22+.
- **C173 (Visual Financial Calculators)** — P2, high effort (12-16h), and overlaps with existing calculator features. Defer to Sprint 22+.
- **C172 (Concept Comparison)** — only if C170 is built first. Standalone C172 without glossary infrastructure is high-risk.

**Sprint 21 Recommended Plan**:

| Order | Task | Effort | Type |
|-------|------|--------|------|
| 1 | D-120 benchmark extraction | 1.5-2.5h | Infrastructure |
| 2 | D-16 analogy_engine.py split | 2-3h | Infrastructure |
| 3 | C152 Multi-Factor Event Narratives | 16-20h | Feature |
| **Total** | | **19.5-25.5h** | |

**Stretch Goal** (if C152 finishes early): C170 Tappable Glossary (6-10h) — greenfield, no prerequisites, high beginner impact.

---

*Created: 2026-06-14*
*Maintainer: System Architect*
*Next review: After Sprint 20 completion / Sprint 21 kickoff*
