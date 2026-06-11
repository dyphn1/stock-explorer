# Stock Explorer — Technical Debt Register

> **Last Updated**: 2026-06-18
> **Source**: Review Cycle Round 12 (Architect's findings)
> **Maintainer**: System Architect

This file tracks all known architecture and technical debt in Stock Explorer, organized by severity.

## Severity Levels

- **High**: Impacts multiple components, causes duplication or inconsistency, high effort to fix if delayed.
- **Medium**: Causes moderate duplication or inconsistency, fixable with moderate effort.
- **Low**: Minor issues, fixable with low effort.

## High Severity Debt

### D5: No LLM integration layer
- **Effort**: 2-3h
- **Description**: The product vision specifies "LLM (plain-language translation only) + templates" but the codebase uses zero LLM. The `analogy_engine.py` and `news_summarizer.py` are purely template-based. Sprint 1's C28 Spike is meant to address this, but no abstraction exists yet.
- **Recommended Action**: Define an `src/services/llm/` abstraction layer with a protocol/interface. Current template engines become the "fallback" implementation.

### D16: `analogy_engine.py` god module (850 lines, 6 responsibilities)
- **Effort**: 2-3h
- **Description**: `analogy_engine.py` contains 6 distinct responsibilities:
  1. Analogy/revenue explanations (original purpose, lines 1–136)
  2. Curated key takeaways data `_KEY_TAKEAWAYS` (120 lines of hardcoded dict)
  3. `generate_key_takeaways()` — rule-based synthesis (100 lines)
  4. `compute_recent_deltas()` + `explain_delta()` — delta detection (180 lines)
  5. Health scoring: 6 `_score_*` functions + `compute_health_scores()` + `get_health_summary()` (270 lines)
  6. EPS extraction logic (now delegated to `financial_metrics.py` via R1)
- **Impact**: The module is doing the work of 3–4 separate services. The health scoring functions (`_score_roe`, `_score_gross_margin`, etc.) are pure functions that could be independently tested but are buried in a module dominated by string templates.
- **Recommended Action**: Split into focused modules:
  - `src/services/analogy_engine.py` — keep only analogy functions (lines 1–136)
  - `src/services/key_takeaways.py` — `generate_key_takeaways()` + `_KEY_TAKEAWAYS` data
  - `src/services/delta_engine.py` — `compute_recent_deltas()` + `explain_delta()`
  - `src/services/health_scoring.py` — all `_score_*` + `compute_health_scores()` + `get_health_summary()`

## Medium Severity Debt

### D1: Duplicate financial metric calculation
- **Effort**: RESOLVED (2-3h)
- **Description**: `_calc_extra_metrics()` in `_router_base.py` and `_get_benchmark_data()` in `peer_comparison.py` both computed gross_margin, net_margin, ROE, debt_ratio, revenue_yoy using identical logic. `_find_financial_value()` was defined in both `_router_base.py` and imported in `peer_comparison.py`, `roe_calculator.py`, and `financial_health.py`.
- **Resolution**: Extracted shared financial calculation into `src/services/financial_metrics.py` service. All consumers import from one place.
- **Note**: R1 completed during Sprint 3. RESOLVED.

### D2: `_find_financial_value` semantic duplication
- **Effort**: RESOLVED (2-3h)
- **Description**: The function `_find_financial_value()` existed in `_router_base.py` and was also imported/used in `peer_comparison.py`, `roe_calculator.py`, and `financial_health.py`. It was a business logic function living in a routing utility file.
- **Resolution**: Moved to `financial_metrics.py` (same refactoring as D1).
- **Note**: R1 completed during Sprint 3. RESOLVED.

### D3: Inline HTML duplication across pages
- **Effort**: 3-4h
- **Description**: `business_card.py`, `group_structure.py`, `etf_detail.py`, `etf_browser.py`, `watchlist_page.py` all contain large inline HTML strings with repeated CSS patterns (card styles, badge styles, color values). The `_router_base.py` provides `_白话_card()` and `_info_card()` but pages bypass them for complex layouts.
- **Recommended Action**: Create reusable HTML component functions in a new `src/services/ui_components.py` (or extend `_router_base.py`). Standardize card/badge patterns.

### D4: Service layer `__init__.py` wildcard imports
- **Effort**: 0.5h
- **Description**: `src/services/__init__.py` uses `from X import *` for 4 of 11 service modules. This creates implicit dependencies and makes it unclear which services are "public API" vs internal.
- **Recommended Action**: Replace wildcard imports with explicit imports. Document which services are stable public API.

### D6: Hardcoded data in Python modules
- **Effort**: 3-4h
- **Description**: `revenue_analyzer.py` has `KNOWN_COMPANY_REVENUE` dict (8 stocks, ~50 lines), `group_structure.py` has `KNOWN_GROUP_STRUCTURES` (5 groups, ~160 lines), `analogy_engine.py` has `one_liners` dict (20 stocks) and `industry_templates` (10 industries), `peer_comparison.py` has `INDUSTRY_BENCHMARKS` (22 entries).
- **Recommended Action**: Migrate all hardcoded data to YAML files under `src/data/`. Only keep the loading/parsing logic in Python.

### D7: `category_browser.py` N+1 API call pattern
- **Effort**: 2-3h
- **Description**: `_render_top_stocks_by_value()` and `_render_hot_stocks_by_volume()` each call `client.get_daily_price()` in a loop for 200 stocks (lines 68-89, 205-223). This is sequential, not parallel, and blocks the UI with a progress bar.
- **Recommended Action**: Use the same `ThreadPoolExecutor` pattern from `_router_base.get_stock_data()`. Batch-fetch with concurrency.

### D8: `etf_browser.py` sequential price fetching
- **Effort**: 2-3h
- **Description**: `_get_all_etf_prices()` iterates ETFs sequentially (lines 21-48). For ~100 ETFs, this is slow. The dividend ranking section also fetches dividends sequentially.
- **Recommended Action**: Same as D7 — use ThreadPoolExecutor for batch fetching.

### D9: Watchlist reads YAML on every operation
- **Effort**: 1-2h
- **Description**: `watchlist.py` calls `_load_data()` (file read + YAML parse) for every single operation (`add`, `remove`, `is_in`, `get_summary`). No in-memory caching.
- **Recommended Action**: Add a session-level cache or in-memory store that's invalidated on writes.

### D10: `events.yaml` read on every event query
- **Effort**: 1-2h
- **Description**: `adaptive_engine.py` calls `_load_events()` (file read + YAML parse + file lock) for every `get_events_for_stock()` and `get_all_recent_events()` call.
- **Recommended Action**: Cache events in memory with TTL or session_state.

### D11: No error boundary standardization
- **Effort**: 2-3h
- **Description**: Error handling is inconsistent. Some services return `None`, others return empty dicts `{}`, others return empty DataFrames. The architecture doc specifies "Return None or empty DataFrame" but enforcement is ad-hoc.
- **Recommended Action**: Create a standardized result type (e.g., `Result[T]` with `.is_ok`, `.value`, `.error`) or at minimum document the convention per service.

### D12: `_router_base.py` mixes routing and UI
- **Effort**: 1h
- **Description**: `_router_base.py` contains `_section_title()`, `_白话_card()`, `_info_card()` (lines 133-169) — these are UI rendering functions in a routing utility file. They use `st.markdown()` directly.
- **Recommended Action**: Move UI helper functions to a shared presentation utility module. Keep `_router_base.py` for data loading only.

### D13: No test infrastructure
- **Effort**: 3-4h initial setup
- **Description**: Zero test files exist. The architecture has good layer separation which would make unit testing natural, but no tests have been written.
- **Recommended Action**: Add pytest + a `tests/` directory. Start with service layer tests (pure functions, no Streamlit dependency).

### D14: Sidebar architecture not extracted
- **Effort**: 1-2h
- **Description**: `main.py` contains ~85 lines of sidebar rendering code (lines 161-245) with hardcoded stock/ETF lists. The `sidebar_architecture.md` doc proposes extracting this but it hasn't been implemented.
- **Recommended Action**: Extract sidebar to `src/services/sidebar_render.py` as proposed in the sidebar architecture doc.

### D15: FinMind client is not async-compatible
- **Effort**: 1-2h
- **Description**: `FinMindClient` uses synchronous API calls. The ThreadPoolExecutor in `_router_base.py` mitigates this for the main data load, but standalone page operations (category browser, ETF browser) don't benefit from this.
- **Recommended Action**: Consider an async FinMind client wrapper for future-proofing. Low priority since ThreadPoolExecutor works.

### D17: EPS extraction logic triplicated across 3 files
- **Effort**: RESOLVED (1-2h with R1)
- **Description**: The identical pattern of extracting EPS from financial statements using keyword matching appeared in 3 files:
  - `chart.py:640-682` — `create_valuation_band_chart()` TTM EPS calculation
  - `analogy_engine.py:747-759` — `compute_health_scores()` EPS growth calculation
  - `business_card.py:420-437` — inline PER percentile calculation in `_render_business_card()`
  All three use the same `eps_keywords = ["eps", "每股盈餘", "earnings per share"]` pattern, the same `str.contains()` filtering, the same `groupby("date").max()` dedup, and the same `tail(4).sum()` TTM calculation.
- **Resolution**: Extracted a shared `extract_ttm_eps(financial_df, as_of_date=None) -> float` function in `src/services/financial_metrics.py` (same as R1). All 3 consumers call this function.
- **Note**: R1 completed during Sprint 3. RESOLVED.

### D18: `_KEY_TAKEAWAYS` hardcoded dict (120 lines) violates D6
- **Effort**: 1h (with R5)
- **Description**: C37 added a 120-line hardcoded `_KEY_TAKEAWAYS` dict (20 stocks, 4–5 bullets each) directly in `analogy_engine.py`. This is the same anti-pattern as D6 (hardcoded data in Python). The handoff explicitly notes "C37 uses curated takeaways for top 20 stocks as PRIMARY approach" — this data will grow.
- **Recommended Action**: Move to `src/data/key_takeaways.yaml` as part of R5 (YAML migration). The loading function stays in the service module.

### D19: `business_card.py` inline HTML table generation (30+ lines)
- **Effort**: 1-2h (with R9)
- **Description**: `business_card.py` lines 340–360 contain inline HTML table generation for the dividend history table with badge columns. This is raw HTML string concatenation in a page file, bypassing the `_info_card()` / `_白话_card()` pattern. The health score dimension cards (lines 242–248) also use inline HTML with hardcoded styles.
- **Recommended Action**: Create a `render_badge_table(df, badge_col, badge_styles)` helper in `ui_components.py` (R2/R9). Move health dimension cards to a reusable `render_score_cards(scores, columns=5)` component.

### D20: `business_card.py` valuation interpretation duplicates `chart.py` logic
- **Effort**: RESOLVED (0.5-1h)
- **Description**: `business_card.py` lines 410–455 re-implemented the PER percentile calculation that already exists in `chart.py:create_valuation_band_chart()`. The page calls `create_valuation_band_chart()` for the chart, then re-computes p25/p75 and the "偏高/偏低/中間" interpretation inline. This is wasted computation (the chart function already calculated these values but didn't return them).
- **Resolution**: Refactored `create_valuation_band_chart()` to return a `(fig, interpretation_dict)` tuple, where `interpretation_dict` contains `{p25, p75, current_per, text}`. The page uses the returned dict instead of re-computing.
- **Note**: D-020 fix completed during Sprint 3. RESOLVED.

### D21: No new service modules — feature code concentrated in existing files
- **Effort**: Included in D16
- **Description**: All Sprint 2 features were added to existing files (`analogy_engine.py`, `chart.py`, `business_card.py`) rather than creating new service modules. The Round 9 analysis recommended creating `summary_engine.py` (C37) and `delta_engine.py` (C39) as separate modules. Instead, everything went into `analogy_engine.py`.
- **Impact**: Contributes to D16 (god module). Makes it harder to locate feature logic. The `analogy_engine.py` import in `business_card.py` now pulls in 850 lines when only ~136 lines of analogies are needed.
- **Recommended Action**: Address as part of D16 refactoring. No immediate action needed if D16 is planned for Sprint 3.

## New Architecture Debt Identified in Round 12

### D22: `financial_metrics.py` is a leaf service with no consumers in service layer
- **Effort**: No immediate action
- **Description**: `financial_metrics.py` is imported by page files (`_router_base.py`, `business_card.py`) and service files (`chart.py`, `analogy_engine.py`), but no other service imports it. This means the service-layer boundary is blurred — pages import directly from `financial_metrics.py` rather than going through a service facade.
- **Impact**: Low. The 4-layer architecture is slightly bent but not broken. `financial_metrics.py` is a pure utility module (pure functions, no state), so the layer violation is minimal.
- **Recommended Action**: No immediate action. If more shared utility modules are extracted, consider a `src/services/shared/` sub-directory for pure utility functions.

### D23: Tone guidelines for market-level features (from Round 11 discussion)
- **Effort**: Content task (1h)
- **Description**: C51 (Sector Heatmap) and C49 (Market Pulse) will display market-level data. The current tone guidelines (from `company_facts.yaml` and analogy functions) are designed for single-stock explanations. Market-level features need "過去發生" language — factual, not predictive.
- **Impact**: Without tone guidelines, market features may accidentally sound like investment advice.
- **Recommended Action**: Add tone guidelines to `docs/design/tone_guidelines.md` before C51 implementation. This is a content task, not a code task.

### D24/D27: `business_card.py` approaching architectural limit
- **Effort**: 2-3h (extract + update imports)
- **Description**: `business_card.py` is 447 lines after R1/D-020 cleanup (down from 479). Adding C44 risk section (~40 lines), C41 read-next (~30 lines), and C48 story card (~70 lines) will push it to ~590+ lines.
- **Impact**: The page file becomes hard to navigate. Multiple features competing for space.
- **Recommended Action**: Extract to `src/pages/business_card/` sub-directory before C48 implementation. Proposed structure:
  - `src/pages/business_card/__init__.py`
  - `src/pages/business_card/base.py` (shared layout, imports)
  - `src/pages/business_card/sections/summary.py` (C37)
  - `src/pages/business_card/sections/delta.py` (C39)
  - `src/pages/business_card/sections/health.py` (C43)
  - `src/pages/business_card/sections/risk.py` (C44)
  - `src/pages/business_card/sections/read_next.py` (C41)
  - `src/pages/business_card/sections/story.py` (C48)
  - `src/pages/business_card/sections/details.py` (metrics, events, etc.)

### D25: Market-level data flow is architecturally distinct from single-stock flow
- **Effort**: Part of C51 implementation
- **Description**: The current architecture is built around a single `stock_id → data dict` pattern. C51 (Sector Heatmap) and C49 (Market Pulse) require market-wide → aggregate → visualize flow.
- **Impact**: Without a clear abstraction, market-level features will ad-hoc the data flow.
- **Recommended Action**: Create `src/services/market_data.py` as part of C51 implementation.

### D26: `story_composer.py` will import from multiple unstable services
- **Effort**: Blocker for C48
- **Description**: C48's `story_composer.py` will import from `analogy_engine.py` (being split via D16), `company_facts.py`, `chart.py`, and `financial_metrics.py`.
- **Impact**: C48 development may be blocked or coupled to unstable interfaces if D16 slips.
- **Recommended Action**: Complete D16 before starting C48.

## Low Severity Debt
- None (all items classified as Medium or higher impact)

## Summary
- **Total Debt Items**: 27
- **High Severity**: 2 items (D5, D16)
- **Medium Severity**: 23 items (D1-D4, D6-D15, D17-D21, D22-D26)
- **Low Severity**: 0 items
- **Resolved Items**: D1, D2, D17, D20 (4 items)

## Next Review
This register should be updated after each review cycle. Next update: After Sprint 3 feature implementation.

-- 
*Created: 2026-06-11*
*Maintainer: System Architect*