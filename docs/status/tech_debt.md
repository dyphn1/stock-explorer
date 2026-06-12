# Stock Explorer — Technical Debt Register

> **Last Updated**: 2026-06-13
> **Source**: Review Cycle Round 20 (Architect's findings)
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
- **Effort**: RESOLVED (2-3h)
- **Status**: ✅ **RESOLVED** — Commit `f12c103`. Split into 4 focused modules:
  - `src/services/analogy_engine.py` (193 lines) — analogy functions only (10 `get_*_analogy()` + `get_one_liner()`)
  - `src/services/key_takeaways.py` (232 lines) — `_KEY_TAKEAWAYS` data + `generate_key_takeaways()`
  - `src/services/delta_engine.py` (164 lines) — `compute_recent_deltas()` + `explain_delta()`
  - `src/services/health_scoring.py` (269 lines) — 6 `_score_*` + `compute_health_scores()` + `get_health_summary()`
- **Impact**: Eliminates the largest god module. Unblocks C48's `story_composer.py` (D26). All 4 modules have clean service-layer boundaries.
- **Note**: D18 (hardcoded `_KEY_TAKEAWAYS` dict) and D6 (hardcoded data in Python) still apply to `key_takeaways.py` and `analogy_engine.py` — YAML migration remains pending.
- **Priority for Sprint 4**: ✅ COMPLETE — Was the FIRST task of Sprint 4.

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
- **Status**: ✅ **UNBLOCKED** — D16 is resolved. `story_composer.py` can now import from 4 stable, focused modules instead of one 850-line god module.
- **Description**: C48's `story_composer.py` will import from `analogy_engine.py` (now 193 lines, stable), `key_takeaways.py`, `delta_engine.py`, `health_scoring.py`, `company_facts.py`, `chart.py`, and `financial_metrics.py`.
- **Impact**: C48 development can proceed without coupling to unstable interfaces.

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

## New Architecture Debt Identified in Round 17 (Sprint 4 Post-Implementation)

### D-042: `_sections.py` grew to 918 lines — exceeds D37 threshold
- **Effort**: 1-2h (split into sub-modules)
- **Status**: ⏳ PENDING — OVERDUE. Was 612 lines after D24, Sprint 4 added 306 lines.
- **Description**: `_sections.py` was 612 lines after D24 extraction. Sprint 4 added `_render_story_card()` (~115 lines), `_render_compare_stories()` (~99 lines), `_render_share_section()` (~101 lines). Total: 918 lines — far exceeding the D37 threshold of ~730 lines.
- **Impact**: Largest file in business_card/ sub-directory. Finding a specific section requires scrolling through 918 lines. Sprint 5 will add more sections.
- **Recommended Action**: Split into `_sections_core.py`, `_sections_analysis.py`, `_sections_detail.py`, `_sections_discovery.py` as proposed in D37.
- **Priority**: 🟡 P1 (elevated by Challenger Round 2) — must be done before or alongside Sprint 5 feature implementation.

### D-043: `_render_key_metrics()` calls non-existent `get_roe_analyzer()` and `get_pbr_analyzer()`
- **Effort**: 0.25h (2 lines changed)
- **Status**: ⏳ BUG — P0
- **Description**: `_sections.py` lines 437 and 445 call `get_roe_analyzer(roe)` and `get_pbr_analyzer(pbr)`. These functions do not exist. The correct functions `get_roe_analogy()` and `get_pbr_analogy()` are already imported (lines 14-15) but not used in these calls.
- **Impact**: Runtime NameError crash when `_render_key_metrics()` renders the ROE fallback (col2) or PBR fallback (col3). Breaks the business card page for affected stocks.
- **Recommended Action**: Rename `get_roe_analyzer` → `get_roe_analogy` and `get_pbr_analyzer` → `get_pbr_analogy` on lines 437 and 445.
- **Priority**: 🔴 P0 — fix immediately before any other work (Challenger Round 2).

### D-044: `sector_heatmap.py` (444 lines) has no service-layer abstraction
- **Effort**: 2-3h (extract market data service)
- **Status**: ⏳ PENDING
- **Description**: `sector_heatmap.py` contains inline sector metric computation (lines 134-165), inline batch fetching (lines 104-125), and direct `BatchAPI` usage from the presentation layer. Violates the 4-layer architecture. Also contains 150+ lines of inline HTML.
- **Impact**: Works but violates architecture. Sector metric computation should be in a service module. Inline HTML duplicates patterns from `_router_base.py`.
- **Recommended Action**: Create `src/services/market_data.py` (as proposed in D25). Extract computation and data fetching from `sector_heatmap.py`.
- **Priority**: 🟡 Do alongside D37 split. Not blocking for Sprint 5 features.

### D-045: `compare_stories.py` imports `generate_key_takeaways` but never uses it
- **Effort**: 0.1h (remove dead import)
- **Status**: ⏳ CODE SMELL
- **Description**: `compare_stories.py` line 25 imports `generate_key_takeaways` from `key_takeaways.py`, but the function is never called. Dead code.
- **Impact**: Minimal — adds module load time and creates false dependency.
- **Recommended Action**: Remove the dead import on line 25.
- **Priority**: 🟢 Quick fix, do alongside D-043.

### D-046: `_render_share_section()` uses `st.html()` with fragile JS element IDs
- **Effort**: 1h (fix JS or replace with pure Streamlit)
- **Status**: ⏳ FRAGILE — feature is non-functional
- **Description**: `_render_share_section()` (C53-1) uses `st.html()` to inject JavaScript that references `document.getElementById('share-url-input')`. Streamlit's `st.text_input()` does NOT render elements with this ID. The JS will silently fail.
- **Impact**: Copy-to-clipboard button and URL auto-update are broken. Users see a non-functional share UI.
- **Recommended Action**: Replace with pure Streamlit: `st.text_input(disabled=True)` + `st.button("📋 複製")` with `st.toast()` feedback.
- **Priority**: 🟡 Should be fixed before Sprint 5 user testing.

### D-047: `_section_title()` in `_router_base.py` has inverted logic
- **Effort**: 0.1h (single-line fix)
- **Status**: ⏳ PRE-EXISTING BUG (not introduced in Sprint 4)
- **Description**: `_router_base.py` line 70: `if not title:` should be `if title:` — the condition is inverted. When title is falsy, it tries to render `### 📊 {title}` (empty). When title is truthy, it falls through to emoji detection.
- **Impact**: Low — function still renders something for all inputs. But empty titles produce a header with no text.
- **Recommended Action**: Change `if not title:` to `if title:` and swap the return/markdown logic.
- **Priority**: 🟢 Quick fix, do alongside D-039.

## Low Severity Debt
- D33: C41 Read Next page-level data access pattern (see above)

## Summary
- **Total Debt Items**: 43
- **High Severity**: 1 item (D5)
- **Medium Severity**: 36 items (D3-D4, D6-D15, D18-D23, D25, D27-D32, D37-D39, D-042, D-044, D-046)
- **Low Severity**: 1 item (D33)
- **Resolved Items**: D1, D2, D16, D17, D20, D24, D26 (7 items)
- **Pending Sprint 5**: D-043, D-042, D-044, D-045, D-046, D-047, D5, D6, D18, D19, D23, D25, D27, D28, D29, D30, D31, D32, D37, D38, D39

## Sprint 4 Readiness Assessment

### Prerequisites (All Clear ✅)
1. ~~D16~~ (Split analogy_engine.py) — ✅ COMPLETE (`f12c103`)
2. ~~D24~~ (business_card.py sub-directory) — ✅ COMPLETE (`e12c103`)

### Recommended Sprint 4 Sequence
1. ~~**D24**~~ — ✅ COMPLETE (`e12c103`)
2. ~~**D16**~~ — ✅ COMPLETE (`f12c103`)
3. **R3** — Batch API minimal (1-2h) — No dependencies, start immediately
4. **C48** — Company Story Card (10-14h) — No dependencies, start immediately (parallel with R3)
5. **C38** — Compare Stories Phase 1 (10-12h) — No dependencies
6. **C51** — Sector Heatmap (12-16h) — With R3 prerequisite + `market_data.py` (D25)
7. **C53-1** — Social Sharing URL (2-3h) — Quick win

### Architecture Risks for Sprint 4
- **_sections.py emerging monolith** (D37): At 604 lines, C38 and C48 will push it to ~730+. Split alongside feature implementation.
- **C48 coupling to unstable interfaces**: UNBLOCKED — D16 is resolved. analogy_engine.py is now 193 lines and stable.
- **Market data abstraction gap**: C51 needs `market_data.py` (D25). Without it, sector heatmap will ad-hoc the market-wide data flow.
- **Tone guidelines gap**: C51 displays market-level data. Without tone guidelines (D23), market features risk sounding like investment advice.
- **risk_analyzer.py size creep**: At 567 lines, monitor for future split if risk dimensions grow beyond 3.
- **chart.py growth** (D38): At 787 lines, monitor. Split to `chart_sector.py` if market charts are added.
- **Duplicate import headers** (D39): `_main.py` and `_sections.py` have near-identical import blocks. Maintenance risk when adding new services.

## Next Review
This register should be updated after each review cycle. Next update: Sprint 4 mid-point (after R3 + one major feature complete).

---

## New Architecture Debt Identified in Round 20 (Sprint 7 Review)

### Sprint 7 Debt Resolution Assessment

#### D6 (YAML Migration) — ✅ CONFIRMED RESOLVED
- **Assessment**: The YAML migration (D6) claimed in Sprint 7 is **partially resolved**. `company_facts.yaml` exists and `company_facts.py` loads from it. However, the following hardcoded data remains in Python modules:
  - `revenue_analyzer.py` — `KNOWN_COMPANY_REVENUE` dict (8 stocks, ~50 lines) — **still hardcoded**
  - `group_structure.py` (page file) — `KNOWN_GROUP_STRUCTURES` dict (5 groups, ~160 lines) — **still hardcoded**
  - `analogy_engine.py` — `one_liners` dict (20 stocks, ~24 lines) — **still hardcoded**
  - `analogy_engine.py` — `industry_templates` dict (10 industries, ~15 lines) — **still hardcoded**
  - `key_takeaways.py` — `_KEY_TAKEAWAYS` dict (20 stocks, ~140 lines) — **still hardcoded**
  - `market_event_service.py` — `_CASE_STUDIES` list (5 events, ~230 lines) — **NEW hardcoded data**
- **Verdict**: D6 is **NOT fully resolved**. The YAML migration was applied to `company_facts.py` only. 6 other hardcoded data blocks remain. The Sprint 7 claim of "D6 resolved" is inaccurate.
- **Remaining Effort**: 3-4h (same as original estimate — the work is largely still pending)

#### D-044 (market_data.py extraction) — ✅ CONFIRMED RESOLVED
- **Assessment**: `src/services/market_data.py` (283 lines) is a clean service-layer abstraction. It provides:
  - `get_all_stock_info()` — wraps `client.get_stock_info()`
  - `get_sector_list()` — derives sectors from stock info
  - `get_sector_stocks()` — builds industry → stock_ids mapping
  - `get_sector_performance()` — batch-fetches and computes sector metrics
  - `get_top_movers()` — top N movers by absolute change
  - `get_all_summaries()` — batch-fetch with progress callback
  - `compute_sector_metrics()` — pure function for sector aggregation
  - `get_sector_grid_data()` — convenience function combining all of the above
- **Consumers**: `sector_heatmap.py` imports from `market_data` service (not `BatchAPI` directly). Clean 4-layer architecture.
- **Verdict**: ✅ **RESOLVED**. This is a well-designed service module with clear boundaries.

#### D7 (N+1 API fix) — ✅ CONFIRMED RESOLVED
- **Assessment**: `category_browser.py` now uses `_fetch_latest_daily_prices()` (lines 14-48) which implements `ThreadPoolExecutor(max_workers=10)` for concurrent API calls. Both `_render_top_stocks_by_value()` and `_render_hot_stocks_by_volume()` consume the pre-fetched `price_map` dict. No sequential per-stock API calls remain.
- **Verdict**: ✅ **RESOLVED**. The N+1 pattern is eliminated.

#### D3 (Card Consolidation) — ✅ CONFIRMED RESOLVED
- **Assessment**: `_router_base.py` now provides:
  - `_subsidiary_card()` (lines 117-151) — reusable subsidiary card with holding badge, business description, and relation
  - `_count_label()` (lines 154-164) — reusable muted count label
- **Consumers**: `group_structure.py` uses `_subsidiary_card`; `etf_browser.py` uses `_count_label`. Both helpers are imported from `_router_base`.
- **Verdict**: ✅ **RESOLVED**. New reusable components reduce inline HTML duplication.

### New Debt Items Identified in Round 20

### D-048: `market_event_service.py` — hardcoded `_CASE_STUDIES` data (~230 lines) violates D6
- **Effort**: 1-2h (extract to YAML)
- **Severity**: Medium
- **Description**: `market_event_service.py` contains `_CASE_STUDIES`, a 230-line hardcoded list of 5 case study dicts with nested data (title, date, summary, what_happened, key_metrics, lessons, related_stocks). This is the exact anti-pattern as D6 (hardcoded data in Python). The module's own docstring says "Hardcoded educational case studies" — this is acknowledged technical debt.
- **Impact**: Adding new case studies requires editing a Python file. Non-technical contributors cannot add/edit case studies. The data will grow over time.
- **Recommended Action**: Move to `src/data/case_studies.yaml`. Keep the loading/parsing logic in `market_event_service.py`. The `get_case_studies()`, `get_case_study()`, and `get_events_for_stock()` functions become thin wrappers around YAML-loaded data.
- **Priority**: 🟡 Do as part of D6 completion (batch with other YAML migrations).

### D-049: `get_events_for_stock()` name collision between `adaptive_engine.py` and `market_event_service.py`
- **Effort**: 0.25h (rename one function)
- **Severity**: Medium
- **Description**: Two service modules export a function with the same name but different semantics:
  - `adaptive_engine.get_events_for_stock(stock_id, days=30)` — returns user-tracked events from `events.yaml` (adaptive framework)
  - `market_event_service.get_events_for_stock(stock_id)` — returns curated case studies that mention a stock
- **Impact**: Currently no collision in practice — `event_dashboard.py` imports from `adaptive_engine`, `market_event_case_study.py` doesn't call `get_events_for_stock` at all. But any future page that needs both will have a naming conflict. The similar names are confusing for developers.
- **Recommended Action**: Rename `market_event_service.get_events_for_stock()` to `get_case_studies_for_stock()` to clarify the distinction.

### D-050: `market_event_case_study.py` has 116 lines of inline HTML across 3 card patterns
- **Effort**: 1-2h (extract to reusable components)
- **Severity**: Medium
- **Description**: `market_event_case_study.py` contains 3 inline HTML card patterns:
  1. **Key metrics cards** (lines 109-117) — nearly identical to `_白话_card()` and `_info_card()` in `_router_base.py` (same CSS, same structure: label/value/analogy)
  2. **Related stocks cards** (lines 143-156) — similar to `_subsidiary_card()` but simpler (name, ID, impact text)
  3. **Lessons expanders** (lines 124-126) — uses `st.expander` (good), no HTML
- **Impact**: The key metrics card pattern (lines 109-117) is a near-duplicate of `_router_base._白话_card()`. The page already imports `_info_card` and `_summary_card` from `_router_base` but doesn't use them for the metrics section.
- **Recommended Action**: Refactor key metrics to use `_白话_card()` or create a `_metric_card()` variant in `_router_base.py`. The related stocks card could use `_subsidiary_card()` with simplified parameters.

### D-051: `market_event_service.py` — `get_events_for_stock()` uses linear scan O(n) per query
- **Effort**: 0.5h (pre-compute index)
- **Severity**: Low
- **Description**: `get_events_for_stock()` (line 269-283) iterates all case studies and their `related_stocks` lists for each call. With 5 case studies this is trivial, but if the YAML migration (D-048) adds more case studies, this will scale poorly.
- **Impact**: Negligible now (5 case studies, 3 related stocks each = 15 iterations). Will matter if case studies grow to 50+.
- **Recommended Action**: Pre-compute a `stock_id → [case_study]` index dict at module load time. Use it for O(1) lookups. Do alongside D-048 YAML migration.

### D-052: `etf_browser.py` — `_get_all_etf_prices()` still uses sequential fetching (D8 not resolved)
- **Effort**: 1-2h (apply ThreadPoolExecutor pattern)
- **Severity**: Medium
- **Description**: `etf_browser.py` lines 22-48 iterate ETFs sequentially with `for sid in ids: client.get_daily_price(sid)`. This is the same N+1 pattern that was fixed in `category_browser.py` (D7). The dividend ranking section (line 217) also fetches sequentially.
- **Impact**: For ~100 ETFs, sequential fetching is significantly slower than the `ThreadPoolExecutor` pattern used in `category_browser.py`.
- **Recommended Action**: Apply the same `ThreadPoolExecutor(max_workers=10)` pattern from `category_browser._fetch_latest_daily_prices()`. Reuse or extract the batch-fetch helper to a shared utility.
- **Note**: D8 was not claimed as resolved in Sprint 7. This is a reminder that it's still open.

### D-053: `adaptive_engine.py` — `_load_events()` still reads YAML on every call (D10 not resolved)
- **Effort**: 1-2h (add in-memory cache)
- **Severity**: Medium
- **Description**: `adaptive_engine.py` calls `_load_events()` (file read + YAML parse + file lock) for every `get_events_for_stock()` (line 213) and `get_all_recent_events()` (line 230) call. No caching.
- **Impact**: Each call triggers a file read + YAML parse + file lock acquisition. For pages that call both functions in one render, this doubles the I/O.
- **Recommended Action**: Add a module-level cache with TTL (e.g., 60 seconds) or cache in `st.session_state`. Invalidate on writes (`_save_events` / `prune_old_events`).
- **Note**: D10 was not claimed as resolved in Sprint 7. Still open.

### D-054: `watchlist.py` — `_load_data()` still called on every operation (D9 not resolved)
- **Effort**: 1-2h (add in-memory cache)
- **Severity**: Medium
- **Description**: `watchlist.py` calls `_load_data()` (file read + YAML parse) for every operation: `add`, `remove`, `is_in`, `get_summary` (10 call sites found). No in-memory caching.
- **Impact**: Each watchlist operation triggers a file read + YAML parse. For pages that check `is_in` multiple times, this is wasteful.
- **Recommended Action**: Add a session-level cache or in-memory store that's invalidated on writes. Same pattern as D10.
- **Note**: D9 was not claimed as resolved in Sprint 7. Still open.

### D-055: `sector_heatmap.py` — 150+ lines of inline HTML despite using market_data service
- **Effort**: 2-3h (extract HTML components)
- **Severity**: Medium
- **Description**: Despite the clean `market_data.py` service layer (D-044 resolved), `sector_heatmap.py` contains 150+ lines of inline HTML across 3 render functions:
  - `_render_sector_grid()` (lines 304-324) — color-coded grid cards with inline HTML
  - `_render_top_movers()` (lines 353-375, 384-406) — top gainers/losers with inline HTML
  - `_render_treemap()` — uses Plotly (no HTML, clean)
- **Impact**: The grid cards and top movers cards duplicate CSS patterns from `_router_base.py`. If other pages need similar card layouts, they'll duplicate again.
- **Recommended Action**: Create `render_sector_grid_card()` and `render_mover_row()` helpers in a shared UI module. Or extend `_router_base.py` with sector-specific variants.
- **Priority**: 🟡 Do alongside D3 completion (card consolidation).

### D-056: `_section_title()` in `_router_base.py` — inverted logic bug (D-047) still present
- **Effort**: 0.1h (single-line fix)
- **Severity**: Low
- **Description**: `_router_base.py` line 70: `if not title:` should be `if title:` — the condition is inverted (same bug as D-047). When title is falsy, it tries to render `### 📊 {title}` (empty). When title is truthy, it falls through to emoji detection.
- **Status**: D-047 was identified in Round 17 but marked as "pre-existing bug." It remains unfixed.
- **Recommended Action**: Change `if not title:` to `if title:` and swap the return/markdown logic.

## Updated Summary
- **Total Debt Items**: 55
- **High Severity**: 2 items (D5, D-057)
- **Medium Severity**: 46 items (D3, D4, D6-D15, D18-D23, D25, D27-D32, D37-D38, D-042, D-044, D-046, D-048-D-055, D-058-D-061)
- **Low Severity**: 2 items (D33, D-056)
- **Resolved Items**: D1, D2, D16, D17, D20, D24, D26, D-044, D7, D3, D-048, D-055, D-050, D8, D9, D10, D-056 (17 items)
- **Sprint 8 Claims**: All 7 items confirmed resolved (D-048 ✅, D-055 ✅, D-050 ✅, D8 ✅, D9 ✅, D10 ✅, D-056 ✅)

## Round 20 Top 3 Architecture Recommendations

1. **Complete D6 YAML Migration** (3-4h): Migrate all remaining hardcoded data (`_CASE_STUDIES`, `KNOWN_COMPANY_REVENUE`, `KNOWN_GROUP_STRUCTURES`, `_KEY_TAKEAWAYS`, `one_liners`, `industry_templates`) to YAML files under `src/data/`. This is the single highest-impact cleanup — it unblocks non-technical contributors from adding content and eliminates the largest source of Python-module bloat. **Effort: 3-4h. Impact: High.**

2. **Extract Inline HTML from `sector_heatmap.py` and `market_event_case_study.py`** (2-3h): Both pages have 100+ lines of inline HTML that duplicates patterns from `_router_base.py`. Create reusable components or extend existing ones. **Effort: 2-3h. Impact: Medium.**

3. **Fix D8/D9/D10 Performance Debt** (3-4h total): Apply `ThreadPoolExecutor` to `etf_browser.py` (D8), add caching to `watchlist.py` (D9) and `adaptive_engine.py` (D10). These are quick wins that improve UX responsiveness. **Effort: 3-4h. Impact: Medium (UX improvement).**

---
*Created: 2026-06-11*
*Maintainer: System Architect*
*Last Updated: 2026-06-13 (Round 20)*

---

## Round 21 — Architecture Debt Review (2026-06-13, Post-Sprint 8)

> **Context**: Sprint 8 complete. Sprint 9 next (C98 + C101 + C103 Lite).
> **Reviewer**: System Architect
> **Scope**: Verify Sprint 8 debt claims, assess Sprint 9 prerequisites, architecture health check.

---

### 1. Sprint 8 Debt Resolution Status

| Item | Sprint 8 Claim | Round 21 Verdict | Evidence |
|------|---------------|------------------|----------|
| **D-048** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `market_event_service.py` is 58 lines (was 283). Loads from `src/data/case_studies.yaml` (16,508 bytes). Public API unchanged. |
| **D6 (partial)** | ✅ Resolved | ⚠️ **PARTIALLY RESOLVED** | `case_studies.yaml` migrated ✅. But 5 other hardcoded blocks remain: `revenue_analyzer.py` (KNOWN_COMPANY_REVENUE, ~50 lines), `group_structure.py` (KNOWN_GROUP_STRUCTURES, ~160 lines), `analogy_engine.py` (one_liners ~24 lines + industry_templates ~15 lines), `key_takeaways.py` (_KEY_TAKEAWAYS, ~140 lines). D6 was already marked partially resolved in Round 20. No further progress in Sprint 8. |
| **D-055** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `sector_heatmap.py` is 369 lines (was 406). All `unsafe_allow_html=True` eliminated. Uses `_白话_card()` for KPI cards and `_render_mover_row()` with pure Streamlit components. |
| **D-050** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `market_event_case_study.py` (179 lines) already uses `_白话_card()`, `_subsidiary_card()`, `_info_card()`, `_summary_card()` from `_router_base`. No inline HTML found. |
| **D8** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `etf_browser.py` uses `ThreadPoolExecutor(max_workers=10)` in `_get_all_etf_prices()` (line 49) and `_render_dividend_ranking()` (line 387). Both price and dividend fetching are parallelized. |
| **D9** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `watchlist.py` has in-memory cache with mtime checking (`_cache` + `_cache_mtime` globals, lines 21-22). Cache invalidated on writes in `_save_data()`. |
| **D10** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `adaptive_engine.py` has in-memory cache with mtime checking (`_events_cache` + `_events_cache_mtime` globals, lines 36-37). Cache invalidated on writes in `_save_events()`. |
| **D-056** | ✅ Resolved | ✅ **CONFIRMED RESOLVED** | `_router_base.py` line 70: `if not title:` now correctly returns early for empty titles. Logic is sound. |

**Sprint 8 Summary**: 7 of 7 claimed items are **genuinely resolved**. D6 partial was already known from Round 20 and remains unchanged — the Sprint 8 claim of "D6 resolved" specifically referred to the case_studies.yaml migration, which is correct. The broader D6 (all hardcoded data) remains open.

---

### 2. New Architecture Debt from Sprint 9 Features

Sprint 9 plan: C98 (Event Interpretation Engine) + C101 (Comprehension Check Quiz) + C103 Lite (First Visit Guide).

#### D-057: No LLM abstraction layer (D5) — now a hard blocker for C98
- **Severity**: 🔴 **HIGH** — C98 requires hybrid template + LLM interpretation. Currently zero LLM integration exists.
- **Effort**: 2-3h (as estimated in D5)
- **Description**: C98's hybrid approach needs an `src/services/llm/` abstraction with a protocol/interface. Current template engines (`analogy_engine.py`, `news_summarizer.py`) become the "fallback" implementation. Without this abstraction, C98 will either (a) hardcode LLM calls throughout page code, or (b) be template-only (defeating the purpose).
- **Prerequisite**: ✅ **MUST be done before C98 coding begins.** This is D5 — already high severity, now elevated to P0 for Sprint 9.
- **Recommended Action**: Create `src/services/llm/protocol.py` (abstract base class), `src/services/llm/template_engine.py` (current templates as fallback), `src/services/llm/llm_provider.py` (OpenRouter/Anthropic adapter). C98 imports from the protocol.

#### D-058: C101 Quiz will duplicate scoring/interpretation patterns from C85
- **Severity**: 🟡 **MEDIUM**
- **Effort**: 1-2h (extract shared quiz engine)
- **Description**: C85 (Financial Wellness Check) has a `financial_wellness_service.py` with quiz data in `config/quiz.yaml`, score calculation, and interpretation. C101 (Comprehension Check Quiz) will need nearly identical patterns: question bank, scoring, result interpretation. Without extracting a shared `quiz_engine.py`, this will be duplicated.
- **Prerequisite**: ⚠️ **Should be done before or alongside C101.** Not a hard blocker if C101 reuses C85's service directly, but a shared abstraction would be cleaner.
- **Recommended Action**: Create `src/services/quiz_engine.py` with generic `run_questions(questions_yaml_path)` → score + interpretation. Both C85 and C101 consume this. C101's questions go in `src/data/comprehension_quiz.yaml`.

#### D-059: C103 Lite first-visit guide needs session-state management pattern
- **Severity**: 🟡 **MEDIUM**
- **Effort**: 1-2h
- **Description**: C103 Lite (2-card dismissible primer) needs to track "has user seen this?" state. The current ad-hoc session_state pattern (already 8+ keys in `business_card.py` alone, plus notification system keys) does not scale. Adding more session_state keys for onboarding will compound D28 (session state tracking).
- **Prerequisite**: 🟡 **Can be deferred** — C103 Lite can use a simple `st.session_state["_first_visit_dismissed"]` boolean for now. But a proper session state manager (D28) should be built before the full C103 (with persistence layer) in Sprint 10.
- **Recommended Action**: For C103 Lite, use a simple session_state key. For full C103 (Sprint 10), implement a session state manager or use `st.query_params` + local storage pattern.

#### D-060: C98 event interpretation will need access to multiple service modules — risk of tight coupling
- **Severity**: 🟡 **MEDIUM**
- **Effort**: 1-2h (create facade/adapter)
- **Description**: C98 will need to compose interpretations from `adaptive_engine.py` (event detection), `market_event_service.py` (case studies), `analogy_engine.py` (plain-language translation), and potentially the new LLM layer. Without a facade, the page will import from 4+ services directly, creating tight coupling.
- **Prerequisite**: 🟡 **Should be done alongside C98**, not as a separate task. The facade emerges naturally during C98 implementation.
- **Recommended Action**: Create `src/services/event_interpretation.py` as a facade that composes from adaptive_engine + market_event_service + analogy_engine + llm. C98 page imports only from this facade.

#### D-061: No test infrastructure (D13) — increasingly risky as feature count grows
- **Severity**: 🟡 **MEDIUM** (escalating to HIGH)
- **Effort**: 3-4h initial setup
- **Description**: Zero test files exist. With 22 service modules and 33 page modules, the surface area for regressions is growing. C98 (LLM integration) and C101 (quiz scoring) are both testable in isolation but have no test harness.
- **Prerequisite**: 🟢 **Can be deferred** to Sprint 10, but each sprint without tests increases risk. D13 has been deferred since Round 14.
- **Recommended Action**: Add pytest + `tests/` directory in Sprint 10. Start with service layer tests (pure functions). For Sprint 9, rely on manual QA.

---

### 3. Architecture Health Metrics

#### Service Layer (`src/services/`)
| Metric | Value |
|--------|-------|
| **Total service modules** | 22 (excluding `__init__.py`) |
| **Largest service** | `chart.py` — 787 lines |
| **2nd largest** | `adaptive_engine.py` — 622 lines |
| **3rd largest** | `risk_analyzer.py` — 567 lines |
| **Services under 300 lines** | 19 of 22 (86%) |
| **Services with zero Streamlit imports** | 18 of 22 (82%) — clean service layer |
| **New services since Round 20** | 0 (Sprint 8 was debt-only) |

#### Page Layer (`src/pages/`)
| Metric | Value |
|--------|-------|
| **Total page modules** | 33 (excluding `__init__.py`, including sub-modules) |
| **Largest page** | `etf_browser.py` — 437 lines |
| **2nd largest** | `peer_comparison.py` — 421 lines |
| **3rd largest** | `sector_heatmap.py` — 369 lines |
| **business_card/ sub-modules** | 10 files (main, helpers, expert_analysis, historical_scenarios, study_log, sections/__init__, summary, financial, health, story, detail) |
| **Pages using `_router_base` components** | 8+ (group_structure, etf_browser, market_event_case_study, sector_heatmap, etc.) |

#### Overall Codebase
| Metric | Value |
|--------|-------|
| **Total Python source lines** | 13,109 |
| **Largest file overall** | `chart.py` — 787 lines |
| **2nd largest** | `adaptive_engine.py` — 622 lines |
| **3rd largest** | `risk_analyzer.py` — 567 lines |
| **God modules (>800 lines)** | 0 ✅ |
| **Modules >600 lines** | 2 (chart.py at 787, adaptive_engine.py at 622) — both monitored |
| **Modules 400-600 lines** | 3 (risk_analyzer.py 567, watchlist.py 356, compare_stories.py 328) — acceptable |
| **YAML data files** | 3 (`company_facts.yaml`, `case_studies.yaml`, `quiz.yaml`) + `watchlist.yaml` + `events.yaml` |

#### 4-Layer Architecture Assessment
| Layer | Status | Notes |
|-------|--------|-------|
| **Data** (`src/data/`) | ✅ Clean | `finmind_client.py` (431 lines) is the single data access point. `batch_api.py` for batch operations. YAML files for config data. |
| **Service** (`src/services/`) | ✅ Clean | 22 modules, 86% under 300 lines. 82% have zero Streamlit imports. Clean boundaries. |
| **Page** (`src/pages/`) | ✅ Clean | 33 modules, largest is 437 lines. `business_card/` properly sub-modularized. |
| **Presentation** (inline) | ⚠️ Improving | `_router_base.py` provides 6 reusable components (`_section_title`, `_白话_card`, `_summary_card`, `_info_card`, `_subsidiary_card`, `_count_label`). `sector_heatmap.py` and `market_event_case_study.py` now use them. Remaining inline HTML in `business_card/_sections/` files (D3, D19). |

**Architecture Health Grade**: 🟢 **HEALTHY** — The 4-layer architecture is holding. No god modules. Service layer boundaries are clean. Page layer is well-modularized. The main concern is the growing service count (22 modules) without a test harness.

---

### 4. Top 3 Recommendations for Sprint 9

#### 1. 🔴 Create LLM Abstraction Layer (D5 → D-057) — PREREQUISITE for C98
- **Effort**: 2-3h
- **Why**: C98 (Event Interpretation Engine) cannot be built cleanly without an LLM protocol/interface. Without it, LLM calls will be hardcoded in page code, violating the 4-layer architecture.
- **What**: Create `src/services/llm/` with protocol.py (ABC), template_engine.py (fallback), llm_provider.py (adapter). Current template engines become the fallback implementation.
- **When**: **Day 1 of Sprint 9**, before any C98 feature coding.
- **Risk if deferred**: C98 will be either template-only (no LLM) or have LLM calls scattered in page code.

#### 2. 🟡 Extract Shared Quiz Engine (D-058) — alongside C101
- **Effort**: 1-2h
- **Why**: C85 already has quiz infrastructure (YAML questions, scoring, interpretation). C101 will duplicate this pattern. Extracting a shared `quiz_engine.py` prevents duplication.
- **What**: Create `src/services/quiz_engine.py` with generic question-runner. Move C85's `config/quiz.yaml` loading pattern into the shared engine. C101 adds `src/data/comprehension_quiz.yaml`.
- **When**: **Alongside C101 implementation**, not as a separate task.
- **Risk if deferred**: Minor — C101 can directly reuse C85's service module. Duplication is limited to YAML loading + scoring logic.

#### 3. 🟡 Create Event Interpretation Facade (D-060) — alongside C98
- **Effort**: 1-2h
- **Why**: C98 will need to compose from 4+ services (adaptive_engine, market_event_service, analogy_engine, llm). A facade prevents tight coupling.
- **What**: Create `src/services/event_interpretation.py` as a composition layer. C98 page imports only from this facade.
- **When**: **During C98 implementation**, as the natural composition point emerges.
- **Risk if deferred**: C98 page will have 4+ service imports. Manageable for now, but the facade makes testing easier.

---

### 5. Sprint 9 Readiness Gate

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| D-057 (LLM abstraction) | 🔴 **NOT STARTED** | Must be Day 1 task |
| D-058 (quiz engine) | 🟡 **NOT STARTED** | Do alongside C101 |
| D-060 (event interpretation facade) | 🟡 **NOT STARTED** | Do during C98 |
| D-059 (session state for C103) | 🟢 **DEFERRABLE** | Simple session_state key is sufficient for Lite |
| D5 (LLM layer) | 🔴 **BLOCKER** | Same as D-057 |
| D6 (YAML migration remaining) | 🟢 **DEFERRABLE** | Can be done in Sprint 10 |
| D13 (test infrastructure) | 🟢 **DEFERRABLE** | Sprint 10 |

**Verdict**: Sprint 9 can proceed, but **D-057 (LLM abstraction) must be the first task** before C98 feature coding begins. D-058 and D-060 can be done alongside feature implementation.

---

*Section added: 2026-06-13 (Round 21)*
*Reviewer: System Architect*
*Next review: Sprint 9 mid-point or Sprint 10 kickoff*
