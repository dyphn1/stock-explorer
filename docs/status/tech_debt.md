# Stock Explorer — Technical Debt Register

> **Last Updated**: 2026-06-19
> **Source**: Review Cycle Round 15 (Architect's findings)
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
- **Status**: ⏳ **PENDING** — Still 850 lines, un-split. Was deferred to end of Sprint 3 after C44 and C38. C48 (Sprint 4) is blocked on this.
- **Description**: `analogy_engine.py` contains 6 distinct responsibilities:
  1. Analogy/revenue explanations (original purpose, lines 1–136)
  2. Curated key takeaways data `_KEY_TAKEAWAYS` (120 lines of hardcoded dict)
  3. `generate_key_takeaways()` — rule-based synthesis (100 lines)
  4. `compute_recent_deltas()` + `explain_delta()` — delta detection (180 lines)
  5. Health scoring: 6 `_score_*` functions + `compute_health_scores()` + `get_health_summary()` (270 lines)
  6. EPS extraction logic (now delegated to `financial_metrics.py` via R1)
- **Impact**: The module is doing the work of 3–4 separate services. The health scoring functions (`_score_roe`, `_score_gross_margin`, etc.) are pure functions that could be independently tested but are buried in a module dominated by string templates. **Critical path for C48.**
- **Recommended Action**: Split into focused modules:
  - `src/services/analogy_engine.py` — keep only analogy functions (lines 1–136)
  - `src/services/key_takeaways.py` — `generate_key_takeaways()` + `_KEY_TAKEAWAYS` data
  - `src/services/delta_engine.py` — `compute_recent_deltas()` + `explain_delta()`
  - `src/services/health_scoring.py` — all `_score_*` + `compute_health_scores()` + `get_health_summary()`
- **Priority for Sprint 4**: 🔴 HIGH — Must be completed before C48 starts. D26 explicitly flags D16 as a blocker for `story_composer.py`.

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
- **Description**: `src/services/__init__.py` uses `from X import *` for 4 of 11 service modules. This creates implicit dependencies and makes it unclear which services are "public API" vs internal. Only 4 modules are exported (`analogy_engine`, `news_summarizer`, `revenue_analyzer`, `financial_metrics`), leaving 7 "hidden" — this actually makes the hidden modules good candidates for internal-only status.
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
- **Note**: This item will be resolved as part of D16 split — the data moves to `key_takeaways.py` module.

### D19: `business_card.py` inline HTML table generation (30+ lines)
- **Effort**: 1-2h (with R9)
- **Description**: `business_card.py` lines 340–360 contain inline HTML table generation for the dividend history table with badge columns. This is raw HTML string concatenation in a page file, bypassing the `_info_card()` / `_白话_card()` pattern. The health score dimension cards (lines 242–248) also use inline HTML with hardcoded styles.
- **Recommended Action**: Create a `render_badge_table(df, badge_col, badge_styles)` helper in `ui_components.py` (R2/R9). Move health dimension cards to a reusable `render_score_cards(scores, columns=5)` component.
- **Note**: Will be easier to address after D24 (sub-directory extraction) separates these into individual section files.

### D20: `business_card.py` valuation interpretation duplicates `chart.py` logic
- **Effort**: RESOLVED (0.5-1h)
- **Description**: `business_card.py` lines 410–455 re-implemented the PER percentile calculation that already exists in `chart.py:create_valuation_band_chart()`. The page calls `create_valuation_band_chart()` for the chart, then re-computes p25/p75 and the "偏高/偏低/中間" interpretation inline. This is wasted computation (the chart function already calculated these values but didn't return them).
- **Resolution**: Refactored `create_valuation_band_chart()` to return a `(fig, interpretation_dict)` tuple, where `interpretation_dict` contains `{p25, p75, current_per, text}`. The page uses the returned dict instead of re-computing.
- **Note**: D-020 fix completed during Sprint 3. RESOLVED.

### D21: No new service modules — feature code concentrated in existing files
- **Effort**: Included in D16
- **Description**: All Sprint 2 features were added to existing files (`analogy_engine.py`, `chart.py`, `business_card.py`) rather than creating new service modules. The Round 9 analysis recommended creating `summary_engine.py` (C37) and `delta_engine.py` (C39) as separate modules. Instead, everything went into `analogy_engine.py`.
- **Impact**: Contributes to D16 (god module). Makes it harder to locate feature logic. The `analogy_engine.py` import in `business_card.py` now pulls in 850 lines when only ~136 lines of analogies are needed.
- **Recommended Action**: Address as part of D16 refactoring. No immediate action needed if D16 is planned for Sprint 3/4.

## New Architecture Debt Identified in Round 12

### D22: `financial_metrics.py` is a leaf service with no consumers in service layer
- **Effort**: No immediate action
- **Description**: `financial_metrics.py` is imported by page files (`_router_base.py`, `business_card.py`) and service files (`chart.py`, `analogy_engine.py`), but no other service imports it. This means the service-layer boundary is blurred — pages import directly from `financial_metrics.py` rather than going through a service facade.
- **Impact**: Low. The 4-layer architecture is slightly bent but not broken. `financial_metrics.py` is a pure utility module (pure functions, no state), so the layer violation is minimal.
- **Recommended Action**: No immediate action. If more shared utility modules are extracted, consider a `src/services/shared/` sub-directory for pure utility functions.

### D23: Tone guidelines for market-level features
- **Effort**: Content task (1h)
- **Status**: ⏳ **PENDING** — No `docs/design/tone_guidelines.md` file exists yet.
- **Description**: C51 (Sector Heatmap) and C49 (Market Pulse) will display market-level data. The current tone guidelines (from `company_facts.yaml` and analogy functions) are designed for single-stock explanations. Market-level features need "過去發生" language — factual, not predictive.
- **Impact**: Without tone guidelines, market features may accidentally sound like investment advice.
- **Recommended Action**: Add tone guidelines to `docs/design/tone_guidelines.md` before C51 implementation. This is a content task, not a code task. **Should be done in Sprint 4 before C51 starts.**

### D24/D27: `business_card.py` approaching architectural limit
- **Effort**: RESOLVED (2-3h)
- **Status**: ✅ **RESOLVED** — Commit e12c103. Extracted to `src/pages/business_card/` sub-directory with 4 files: `__init__.py` (4 lines), `_main.py` (84 lines), `_sections.py` (612 lines), `_helpers.py` (95 lines). Total: 795 lines across 4 files (vs. 561 monolith). Net structural improvement despite +234 lines from duplicated import headers.
- **Description**: `business_card.py` was 561 lines after C41 Read Next (~60 lines) and C44 Risk Analysis (~114 lines). Adding C38 compare stories section (~50 lines) and C48 story card (~70 lines) would have pushed it to ~681 lines.
- **Impact**: Resolved. The page file is now properly modularized. Section functions are isolated and can be tested/split further.
- **Priority for Sprint 4**: ✅ COMPLETE — Was the FIRST task of Sprint 4.
- **New concern**: `_sections.py` is 612 lines and will grow with C38 + C48. See D37.

### D25: Market-level data flow is architecturally distinct from single-stock flow
- **Effort**: Part of C51 implementation
- **Description**: The current architecture is built around a single `stock_id → data dict` pattern. C51 (Sector Heatmap) and C49 (Market Pulse) require market-wide → aggregate → visualize flow.
- **Impact**: Without a clear abstraction, market-level features will ad-hoc the data flow.
- **Recommended Action**: Create `src/services/market_data.py` as part of C51 implementation.

### D26: `story_composer.py` will import from multiple unstable services
- **Effort**: Blocker for C48
- **Status**: ⏳ **PENDING** — Blocked on D16.
- **Description**: C48's `story_composer.py` will import from `analogy_engine.py` (being split via D16), `company_facts.py`, `chart.py`, and `financial_metrics.py`.
- **Impact**: C48 development may be blocked or coupled to unstable interfaces if D16 slips.
- **Recommended Action**: Complete D16 before starting C48.

## New Architecture Debt Identified in Round 13

### D27: C34 timeline UI complexity
- **Effort**: Requires spike (4-6h approved for Sprint 4)
- **Description**: C34 (Company Story Timeline) requires a timeline UI but Streamlit has no native timeline component. The approved approach is a C34-spike in Sprint 4 to prototype using Streamlit native components.
- **Impact**: If the spike reveals Streamlit cannot adequately render a timeline, C34 (18-26h) may need significant rework or a different tech approach.
- **Recommended Action**: Run C34-spike in Sprint 4 to de-risk. Evaluate `streamlit-timeline` or custom HTML/CSS approaches.

### D28: Notification system session state tracking
- **Effort**: Monitor (escalate to D25 session state manager if needed)
- **Description**: The Notification System (Sprint 6) will add 6+ new session_state keys. The current ad-hoc session_state pattern (already 8+ keys in `business_card.py` alone) does not scale.
- **Impact**: Session state proliferation across features will make debugging and testing difficult. Risk of key collisions.
- **Recommended Action**: Add session state audit to Sprint 5 plan (already in handoff). Consider a session state manager pattern.

## New Architecture Debt Identified in Round 14 (Sprint 3 Review)

### D29: C41 Read Next inline HTML in business_card.py
- **Effort**: 1h (with D24)
- **Status**: ⚠️ **SUPERSEDED BY D24** — C41 is complete. The inline HTML (lines 449-490 in Round 12, now lines 504-544) will be moved to `read_next.py` section file when D24 extracts the sub-directory.
- **Description**: C41 added ~60 lines of inline HTML directly in `_render_business_card()` in `business_card.py`, including raw HTML string concatenation for peer stock cards. This bypasses the `_info_card()` / `_白话_card()` pattern and adds to the file's growth.
- **Impact**: Contributes to D24 (business_card.py bloat). The inline HTML is not reusable.
- **Recommended Action**: Extract peer stock card rendering to a `render_peer_cards(peers_df, navigate_fn)` helper in `ui_components.py` (D3). Move to `read_next.py` section file when D24 extracts the sub-directory.
- **New**: Identified during Round 14 review of C41 commit (1f98d73).

### D30: C44 Risk Analysis will compound business_card.py growth
- **Effort**: Included in D24
- **Status**: ✅ **REALIZED** — C44 is complete (commit 567239b). It added ~114 lines to `business_card.py` (447→561 lines). The file now has risk analysis via `st.expander` progressive disclosure. D24 extraction is now more urgent since the file is already 561 lines.
- **Description**: C44 added risk analysis to `business_card.py` with 3 dimensions (customer concentration, financial health, event-based) using `st.expander` progressive disclosure. New helper functions `_render_risk_dimension()` and `get_health_dimension_explanation()` were added to the page file.
- **Impact**: Risk section added ~114 lines. Combined with C41's ~60 lines, the file grew from 447→561 lines. Without D24, C38 and C48 will push it to ~681 lines.
- **Recommended Action**: D24 must be the FIRST task in Sprint 4. Extract before adding C38 or C48 sections.
- **New**: Identified during Round 14 review. Urgency increased because C44 is complete and the file is already 561 lines.

## New Architecture Debt Identified in Round 14 (Sprint 3 Review)

### D31: `risk_analyzer.py` is a 567-line service with mixed responsibilities
- **Effort**: Monitor (split only if it grows beyond ~700 lines)
- **Description**: `risk_analyzer.py` (567 lines) contains 3 distinct risk assessment functions plus 7 helper functions:
  1. `assess_customer_concentration()` (lines 151-289) — ~139 lines
  2. `assess_financial_health()` (lines 290-430) — ~141 lines
  3. `assess_event_risk()` (lines 431-517) — ~87 lines
  4. `assess_risk()` (lines 518-567) — orchestrator, ~50 lines
  5. 7 private helper functions (lines 35-135) — threshold classification, cash flow trend, etc.
- **Positive**: The module has **zero Streamlit imports** and **zero API calls** — clean service layer boundary. It imports only from `financial_metrics.py` and `news_summarizer.py`. This is a model service module.
- **Concern**: At 567 lines, it's already approaching the size where `analogy_engine.py` became a god module (850 lines). The 3 assessment functions are independent.
- **Impact**: Low for now. Well-structured internally with clear function boundaries. The orchestrator pattern is clean.
- **Recommended Action**: No immediate action needed. Monitor if additional risk dimensions (volatility, cyclicality) are added — that would be the time to split into `customer_risk.py`, `financial_risk.py`, `event_risk.py`.
- **New**: Identified during Round 14 review of C44 commit (567239b).

### D32: `business_card.py` now contains presentation helper functions that should live in a shared UI module
- **Effort**: 1-2h (with D24)
- **Description**: `business_card.py` defines 3 presentation-helper functions at the top of the file (lines 43-83):
  1. `get_health_dimension_explanation()` (lines 43-48) — returns plain-language score explanation
  2. `_render_risk_dimension()` (lines 66-83) — renders a risk dimension card with inline HTML
  3. `_RISK_BADGES` and `_RISK_COLORS` dicts (lines 51-61) — style constants
- **Impact**: These are presentation functions living in a page file. If another page needs to render risk dimensions or health explanations, this code cannot be reused. Same anti-pattern as D3 (inline HTML duplication) and D12 (_router_base.py mixing routing and UI).
- **Recommended Action**: Move to `ui_components.py` (D3/R9) when D24 extracts the sub-directory. The health explanation function is a pure function that belongs in a shared module. The risk dimension renderer should be a reusable component.
- **New**: Identified during Round 14 review of C44 commit (567239b).

### D33: C41 Read Next creates a new data access pattern in the presentation layer
- **Effort**: 0.5-1h (low priority)
- **Description**: C41's Read Next section (lines 504-544 in `business_card.py`) calls `client.get_stock_info()` directly inside the page render function to get peer stocks. This is a **data access call in the presentation layer** — the page is calling the FinMind client directly instead of receiving pre-computed peer data through the `data` dict from `_router_base.py`.
- **Impact**: Low. The `get_stock_info()` call is cached by FinMindClient, so there's no performance penalty. But it breaks the 4-layer architecture pattern where pages should only consume data from the `data` dict.
- **Recommended Action**: Pre-compute peer stock recommendations in `_router_base.py`'s `get_stock_data()` and include them in the `data` dict. This keeps the presentation layer clean. Low priority — the current approach works and the cache makes it fast.
- **New**: Identified during Round 14 review of C41 commit (1f98d73).

## New Architecture Debt Identified in Round 15 (Sprint 4 Kickoff)

### D37: `_sections.py` is 612 lines and will grow with C38 + C48
- **Effort**: 1-2h (split alongside feature implementation)
- **Status**: ⏳ **PENDING** — `_sections.py` is 612 lines after D24 extraction. C38 and C48 will each add ~50-70 lines.
- **Description**: The D24 extraction created `_sections.py` as the single file containing all 14 section rendering functions (header, takeaways, deltas, health, risk, one-liner, key metrics, dividend, revenue breakdown, revenue trend, valuation, news, read next, footer). C38 (Compare Stories) and C48 (Company Story Card) will push it to ~730+ lines.
- **Impact**: `_sections.py` is becoming the new monolith — the same problem D24 solved for `business_card.py` is re-emerging at the section level.
- **Recommended Action**: When C38 and C48 are implemented, split `_sections.py` into:
  - `_sections_core.py` — header, one-liner, key metrics, footer (stable sections)
  - `_sections_analysis.py` — takeaways, deltas, health, risk (analysis sections)
  - `_sections_detail.py` — dividend, revenue breakdown, revenue trend, valuation, news (detail sections)
  - `_sections_discovery.py` — read next, compare stories, story card (discovery sections)
- **Priority for Sprint 4**: 🟡 Do alongside C38/C48 implementation, not as a separate task.
- **New**: Identified during Round 15 review of D24 extraction (e12c103).

### D38: `chart.py` grew to 787 lines with chart functions added incrementally
- **Effort**: 1h (if needed — split only if market charts are added)
- **Status**: ⏳ **MONITOR** — `chart.py` is 787 lines. Single responsibility (chart rendering) but growing.
- **Description**: `chart.py` grew from 779→787 lines since Round 14. Contains all chart types: revenue trend, revenue pie, valuation band, health snowflake. If C51 (Sector Heatmap) adds treemap/sunburst charts to this file, it will cross 850+ lines.
- **Impact**: Low for now. The module is coherent — all functions are chart rendering. But finding a specific chart function requires scrolling through 787 lines.
- **Recommended Action**: If C51 adds sector/market charts, create `chart_sector.py` for market-level visualizations. Keep `chart.py` for single-stock charts.
- **Priority for Sprint 4**: 🟢 Monitor. Act only if market charts push it beyond 850 lines.
- **New**: Identified during Round 15 review.

## Low Severity Debt
- D33: C41 Read Next page-level data access pattern (see above)

## Summary
- **Total Debt Items**: 35
- **High Severity**: 2 items (D5, D16)
- **Medium Severity**: 29 items (D3-D4, D6-D15, D18-D21, D22-D32, D37-D38)
- **Low Severity**: 1 item (D33)
- **Resolved Items**: D1, D2, D17, D20, D24 (5 items)
- **Pending Sprint 4**: D5, D6, D16, D18, D19, D23, D25, D26, D27, D28, D29, D30, D31, D32, D37, D38

## Sprint 4 Readiness Assessment

### Prerequisites (Hard Blockers)
1. **D16** (Split analogy_engine.py) — Blocks C48's `story_composer.py` (D26)
2. ~~D24~~ (business_card.py sub-directory) — ✅ COMPLETE
3. **R3** (Batch API minimal) — Blocks C51 Sector Heatmap

### Recommended Sprint 4 Sequence
1. ~~**D24**~~ — ✅ COMPLETE (e12c103)
2. **D16** — Split analogy_engine.py (2-3h) — Must complete before C48
3. **R3** — Batch API minimal (1-2h) — Unlocks C51
4. **C38** — Compare Stories Phase 1 (10-12h) — Can parallelize with R3
5. **C51** — Sector Heatmap (12-16h) — With R3 prerequisite
6. **C48** — Company Story Card (10-14h) — With D16 + D24 prerequisites
7. **C53-1** — Social Sharing URL (2-3h) — Quick win

### Architecture Risks for Sprint 4
- **analogy_engine.py uncontrolled growth**: File is still 850 lines. C38 and C48 need functions from it. **D16 must be FIRST or second task.**
- **_sections.py emerging monolith** (D37): At 612 lines, C38 and C48 will push it to ~730+. Split alongside feature implementation.
- **C48 coupling to unstable interfaces**: story_composer.py needs analogy_engine.py split first (D16). If D16 slips, C48 slips.
- **Market data abstraction gap**: C51 needs `market_data.py` (D25). Without it, sector heatmap will ad-hoc the market-wide data flow.
- **Tone guidelines gap**: C51 displays market-level data. Without tone guidelines (D23), market features risk sounding like investment advice.
- **risk_analyzer.py size creep**: At 567 lines, monitor for future split if risk dimensions grow beyond 3.
- **chart.py growth** (D38): At 787 lines, monitor. Split to `chart_sector.py` if market charts are added.

## Next Review
This register should be updated after each review cycle. Next update: After D16 + R3 complete (Sprint 4 mid-point).

---
*Created: 2026-06-11*
*Maintainer: System Architect*
*Last Updated: 2026-06-19 (Round 15)*
