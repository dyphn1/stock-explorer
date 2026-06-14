# Architecture Review — Round 46 (2026-06-15)

> **Author**: System Architect
> **Context**: Sprint 20 COMPLETE (C167 AI Screener + D-123 tone fix). Sprint 21 planned: C170 Tappable Glossary + C188 Why Did This Move? + D-125/D-126/D-127.
> **Scope**: Full architecture health assessment, debt trend analysis (Rounds 20–46), Sprint 21 readiness, new feature architecture implications.

---

## Current Architecture Health

- **Overall Grade**: **B+ HEALTHY** (down from A- in Round 37 due to first god module emergence)
- **Key Metrics**:
  - 47 service modules (flat directory, only `llm/` is a sub-package)
  - ~50 page modules (largest: `etf_browser.py` at 437 lines)
  - 1 god module: `chart_stock.py` at 818 lines (exceeded 800-line threshold)
  - 2 modules >600 lines: `chart_stock.py` (818), `adaptive_engine.py` (622)
  - 42 of 47 services (89%) under 300 lines
  - 47 of 47 services (100%) Streamlit-free
  - 319+ tests passing (up from 165+ at Round 37)
  - 0 high-severity debt items
  - 15 `unsafe_allow_html=True` instances (CI-enforced, stable)

### Architecture Health by Layer

| Layer | Status | Notes |
|-------|--------|-------|
| **Data** (`src/data/`) | ✅ Clean | `finmind_client.py`, `batch_api.py`. YAML data under `src/data/`. |
| **Service** (`src/services/`) | ⚠️ Scaling | 47 modules in flat directory. Only `llm/` is a sub-package. 100% Streamlit-free. No circular imports. Directory navigation is becoming unwieldy. |
| **Page** (`src/pages/`) | ✅ Clean | ~50 modules, largest is 437 lines. `business_card/` properly sub-modularized. |
| **Presentation** (inline) | ⚠️ Stable | 15 `unsafe_allow_html=True` instances. CI enforcement prevents new instances. |

---

## Debt Trend Analysis (Rounds 20–46)

### Debt Resolution Velocity

| Round | Sprint | Key Resolutions | New Debt Added | Net Change |
|-------|--------|----------------|----------------|------------|
| 20 | Sprint 7 | D6 (partial), D-044, D7, D3 | D-048, D-049 | +2 |
| 21–30 | Sprints 8–14 | D5 (LLM layer), D-101, D-100, D-099 | D-051 through D-060 | +8 |
| 31–37 | Sprints 15–16b | D5 fully resolved (last high-sev item) | D-091, D-094, D-098 | +3 |
| 38–45 | Sprints 17–19 | D-121 (YAML screener), D-123 (tone QA) | D-122, D-124 | +2 |
| 46 | Sprint 20 | D-121 ✅, D-123 ✅ | D-125, D-126, D-127, D-130 | +4 |

**Total debt items**: 91 (up from 43 at Round 20). However, the *high-severity* count dropped from 1 to 0 (D5 resolved in Sprint 16b). Medium severity grew from ~36 to ~50, low from ~7 to ~41.

### Recurring Patterns

1. **God module re-emergence**: The codebase has a recurring pattern where a module grows past 800 lines. `analogy_engine.py` (850 lines) was split in Sprint 4 (D16). Now `chart_stock.py` has crossed the same threshold at 818 lines. The 800-line threshold is a reliable leading indicator — without proactive splitting, modules tend to grow 40-60 lines per sprint.

2. **DRY violations in shared constants**: `INDUSTRY_BENCHMARKS` (D-126) is the latest instance of a pattern seen repeatedly: data duplicated across page files. Earlier instances include `_find_financial_value` (D1/D2, resolved in Sprint 3) and EPS extraction logic (D17, resolved in Sprint 3). The pattern is: a constant or function is needed in two places → copied → diverges over time.

3. **Inline HTML proliferation**: D3 (inline HTML duplication) was partially resolved with `_router_base.py` helpers, but new instances keep appearing: `sector_heatmap.py` (D-044), `watchlist_page.py` (D-123), `etf_browser.py` (D-124). The CI enforcement on `unsafe_allow_html=True` has capped the growth but hasn't eliminated the pattern.

4. **Service layer flat directory scaling**: At 47 modules in a single flat directory (only `llm/` is a sub-package), finding and categorizing services requires scrolling through a long file list. This is a discoverability problem, not a correctness problem — but it slows onboarding and increases the risk of creating duplicate services.

5. **Test count growth is healthy**: Tests grew from 0 (Round 13) to 165+ (Round 37) to 319+ (Round 46). This is the strongest positive trend — the test infrastructure is now mature and catching regressions.

### Debt Aging

- **Stale medium items** (unresolved for 10+ rounds): D6 (YAML remaining — 3 hardcoded blocks), D11 (error boundary standardization), D14 (sidebar extraction), D-049 (notification tests)
- **Stale low items** (unresolved for 10+ rounds): D15 (async FinMind), D33 (page-level data access)
- **New items needing attention**: D-125 (chart_stock.py), D-126 (INDUSTRY_BENCHMARKS), D-127 (_summary.py)

---

## Top 5 Architecture Recommendations

### Rec 1: Split `chart_stock.py` into Domain-Submodules — D-125

- **Problem**: `chart_stock.py` is 818 lines — the first god module since D16 was resolved in Sprint 4. It contains ~12 chart functions spanning 3 distinct domains (financial charts, health/radar charts, valuation charts). C170 (Tappable Glossary) and C194 (Explain Why Good/Bad) will add glossary-related chart annotations, pushing it past 900 lines.
- **Recommendation**: Split into 3 focused sub-modules:
  - `chart_stock_financial.py` — revenue trend, revenue pie, institutional holdings, price history
  - `chart_stock_health.py` — health snowflake, radar chart, health timeline
  - `chart_stock_valuation.py` — valuation band chart, PER/PB interpretation
  - Keep `chart.py` as a re-export shim (already exists) for backward compatibility.
  - Extract shared chart utilities (color palettes, layout defaults, annotation helpers) into `_chart_theme.py` (already exists — verify it's used consistently).
- **Effort**: 2-3h (mechanical split, no logic changes)
- **Priority**: 🟡 **HIGH** — Must be done Day 1 of Sprint 21, before C170 chart work begins. This is the #1 prerequisite for Sprint 21.
- **Risk if deferred**: C170/C194 will push the file past 900 lines, making it harder to split later. New chart functions will be added to an already-overloaded module.

### Rec 2: Introduce Service Layer Sub-Package Organization

- **Problem**: 47 service modules live in a flat `src/services/` directory. Only `llm/` is a sub-package. Finding a specific service requires scrolling through a 50-item file list. As the service layer grows (potentially 60+ modules by Sprint 25), this becomes a significant discoverability and organization problem. New developers may accidentally create duplicate services because they can't find existing ones.
- **Recommendation**: Organize `src/services/` into domain sub-packages:
  ```
  src/services/
  ├── charts/          # chart_stock_*.py, chart_market.py, _chart_theme.py
  ├── analysis/        # risk_analyzer.py, adaptive_engine.py, pattern_detector.py
  ├── explanation/     # analogy_engine.py, delta_*.py, metric_*.py, glossary_service.py
  ├── education/       # lesson_service.py, quiz_*.py, metric_education.py
  ├── market/          # market_data.py, story_feed.py, case_study_library.py
  ├── portfolio/       # watchlist.py, investment_memo_service.py
  ├── screening/       # stock_screener_service.py, screener_explanation_provider.py
  ├── llm/             # (already exists) base.py, template_provider.py, factory.py
  ├── data/            # financial_metrics.py, company_facts.py, batch_api.py
  └── shared/          # validation.py, settings_service.py, feedback_service.py
  ```
  - Update all imports (mechanical, find-and-replace).
  - Add `__init__.py` files with explicit exports for each sub-package.
  - This is a pure refactoring — no logic changes.
- **Effort**: 3-4h (import updates across ~100 files)
- **Priority**: 🟡 **MEDIUM** — Do in Sprint 22 as a dedicated refactoring task. Not blocking for Sprint 21 since imports can be updated incrementally.
- **Risk if deferred**: Service layer continues to grow flat. By 60+ modules, the organizational debt becomes harder to pay. Risk of duplicate service creation increases.

### Rec 3: Extract `INDUSTRY_BENCHMARKS` to Shared Location — D-126

- **Problem**: The identical 25-entry `INDUSTRY_BENCHMARKS` dict is defined in both `_summary.py` (line 38) and `_health.py` (line 14). This is a DRY violation — adding a new industry benchmark requires updating two files, with risk of divergence.
- **Recommendation**: Move `INDUSTRY_BENCHMARKS` to a shared location. Two options:
  - **Option A**: Add to `_router_base.py` as a shared constant (both files already import from `_router_base`).
  - **Option B**: Create `src/services/benchmarks.py` as a dedicated shared constants module (cleaner separation of concerns).
  - Option B is preferred because `_router_base.py` is already 10+ `unsafe_allow_html=True` instances and mixing data constants with UI routing utilities violates single responsibility.
- **Effort**: 0.5h
- **Priority**: 🟡 **HIGH** — Quick fix, do Day 1 of Sprint 21 alongside D-125.
- **Risk if deferred**: Low immediate risk, but every new industry benchmark requires a two-file update. This will become more painful as the benchmark list grows beyond 25 entries.

### Rec 4: Establish a Shared UI Component Library

- **Problem**: Inline HTML duplication persists across pages (D-122 sector heatmap, D-123 watchlist, D-124 ETF browser). The `_router_base.py` provides some shared components (`_白话_card()`, `_info_card()`, `_subsidiary_card()`), but pages continue to bypass them with inline HTML. The design system documents components (`_mini_score_card`, `_glossary_tooltip`, `_so_what_box`, `_health_score_card` per D-121) but these aren't centralized.
- **Recommendation**: Create `src/services/ui_components.py` as a centralized UI component library:
  - Migrate all reusable HTML components from `_router_base.py` to `ui_components.py`
  - Add missing components: `_mini_score_card()`, `_glossary_tooltip()`, `_so_what_box()`, `_health_score_card()`
  - Standardize card styling (padding, border-radius, background) to match design system
  - Pages import from `ui_components.py` instead of `_router_base.py` for UI helpers
  - `_router_base.py` retains only data-loading functions (`get_stock_data()`, etc.)
- **Effort**: 4-6h (component migration + standardization)
- **Priority**: 🟢 **LOW** — Defer to Sprint 22. The CI enforcement on `unsafe_allow_html=True` prevents new instances. This is a cleanup task, not a blocking issue.
- **Architectural Note**: This aligns with the competitor research finding that Simply Wall St's visual-first approach (snowflake diagrams, infographic-style layouts) is the gold standard for beginner-friendly stock analysis. A shared UI component library would make it easier to implement visual features like C199 (Bear vs Bull debate cards) and C202 (Story Arc timeline labels) in future sprints.

### Rec 5: Proactive `_summary.py` Split Before C-170 — D-127

- **Problem**: `_summary.py` is 464 lines (93% of the 500-line threshold). C170 (Tappable Glossary) will add ~30-40 lines of glossary wrapper functions, pushing it past 500. The `_render_story_card()` function alone is 240 lines — half the file.
- **Recommendation**: Split proactively before C170 implementation:
  - `_summary_hero.py` — `_render_story_card()` (240 lines) + `_render_header()` — the "above the fold" content
  - `_summary_secondary.py` — `_render_takeaways()`, `_render_one_liner()`, `_render_news()` — supporting content
  - Update `_main.py` or the parent page to import from both files
- **Effort**: 1-2h (mechanical split)
- **Priority**: 🟢 **LOW** — Monitor during C170 implementation. Split only if C170 pushes past 500 lines. However, proactive splitting is recommended to avoid mid-sprint refactoring.
- **Risk if deferred**: If C170 pushes the file to 500+ lines mid-sprint, the split becomes a sprint disruption rather than a planned task.

---

## Sprint 21 Architecture Readiness

### Verdict: ✅ READY with Prerequisites

Sprint 21 (C170 + C188 + D-125/D-126/D-127) can proceed, but two prerequisites must be addressed:

| Prerequisite | Effort | When | Blocking? |
|-------------|--------|------|-----------|
| **D-126** (INDUSTRY_BENCHMARKS dedup) | 0.5h | Day 1 | No — can be done in parallel with C170 |
| **D-125** (chart_stock.py split) | 2-3h | Day 1, before C170 chart work | **Yes** — if C170 adds chart annotations |

### C170 (Tappable Glossary) — Architecture Impact

- **Service Layer**: `glossary_service.py` already exists. C170 will add tap/hover interaction logic — likely new functions for inline definition rendering. No new service module needed.
- **Page Layer**: Glossary wrappers will be added to section files in `business_card/_sections/`. This will increase `_summary.py` by ~30-40 lines (D-127 concern).
- **Chart Layer**: If C170 adds glossary annotations to charts (e.g., hover definitions on chart elements), this will add to `chart_stock.py` — making D-125 a hard prerequisite.
- **Presentation Layer**: Glossary tooltips will use `st.markdown()` with `unsafe_allow_html=True` or `st.tooltip()`. Must go through CI enforcement.
- **Risk**: Low. The feature is presentation-heavy with minimal service layer changes. The main risk is `_summary.py` growth (D-127).

### C188 (Why Did This Move?) — Architecture Impact

- **Service Layer**: `event_interpretation_service.py` already exists. C188 will add event-to-narrative mapping for single-stock price movements. May require new functions in the existing service.
- **Page Layer**: A new section file `_why_moved.py` in `business_card/_sections/` — estimated 80-120 lines. This is a clean addition that doesn't bloat existing files.
- **Data Layer**: Uses existing FinMind price data + `adaptive_engine.py` event detection. No new data sources.
- **LLM Layer**: Uses existing `TemplateExplanationProvider` via the `ExplanationProvider` protocol. No LLM changes needed.
- **Risk**: Low-medium. The feature is architecturally clean but the narrative quality depends on template coverage. If templates don't cover enough event types, the feature will feel incomplete.

### Overall Sprint 21 Risk Assessment

- **Low risk**: Both C170 and C188 fit cleanly into the 4-layer architecture
- **Medium risk**: `_summary.py` growth from C170 glossary wrappers (D-127)
- **Mitigation**: Do D-125 (chart split) and D-126 (benchmark dedup) on Day 1. Monitor `_summary.py` size during C170 implementation.

---

## New Feature Architecture Implications

### C170 Tappable Glossary

- **Architecture Fit**: ✅ Clean 4-layer fit
- **Service**: `glossary_service.py` (exists) — add `get_inline_definition(term, context)` for context-aware definitions
- **Page**: New glossary wrapper functions in section files — ~30-40 lines added to `_summary.py`
- **Presentation**: `_glossary_tooltip()` component (D-121) — needs design system documentation
- **Chart Impact**: If glossary annotations are added to chart elements, `chart_stock.py` will grow — making D-125 a prerequisite
- **Competitor Alignment**: Investopedia's glossary is the gold standard for financial education. C170 directly addresses this gap. Simply Wall St's progressive disclosure (summary first, details on click) is the interaction model to emulate.
- **Recommendation**: Implement as pure presentation layer first (tap → tooltip). Add chart annotations in a follow-up sprint after D-125 is resolved.

### C188 Why Did This Move?

- **Architecture Fit**: ✅ Clean 4-layer fit
- **Service**: `event_interpretation_service.py` (exists) — add `explain_price_movement(stock_id, date, direction)` for single-stock event narratives
- **Page**: New `_why_moved.py` section file in `business_card/_sections/` — ~80-120 lines
- **Data**: Uses existing `adaptive_engine.py` event detection + FinMind price data
- **LLM**: Uses `TemplateExplanationProvider` — no LLM changes
- **Competitor Alignment**: Public.com and Spiking both have this feature. It's the #1 most-requested feature in competitor research (appears as C98, C107, C188 across multiple rounds). No TW competitor has it.
- **Recommendation**: Start with template-based explanations for top 5 event types (earnings, dividend, sector movement, institutional activity, news). Expand template coverage in follow-up sprints. The `ExplanationProvider` protocol makes it easy to swap in a more sophisticated provider later.

### C201 Daily Market Story (Sprint 22+)

- **Architecture Fit**: 🟡 Requires new operational pattern
- **Service**: New `daily_briefing.py` service — fetches market data, selects top movers, generates narrative from templates
- **Page**: New `_daily_briefing.py` section for homepage integration
- **Operational**: First feature requiring daily content updates — introduces a cron/caching dimension the current architecture doesn't have
- **Recommendation**: Start with on-demand generation (user opens homepage → fetch today's data → generate story). Add daily caching in a follow-up sprint if performance requires it.

### C199 Bear vs Bull Debate Cards (Sprint 23+)

- **Architecture Fit**: 🟡 Requires new data curation
- **Service**: Would need `bull_case_generator.py` + integration with existing `risk_analyzer.py` (bear case)
- **Data**: Half the inputs exist (risks, events, metrics) but bull case needs manual curation
- **Recommendation**: Defer to Sprint 23+ when narrative infrastructure (C152/C188) is mature. The `ExplanationProvider` protocol will make it easy to add debate-style explanations later.

---

## Summary

The Stock Explorer architecture remains **B+ HEALTHY** with zero high-severity debt items. The 4-layer architecture is solid, the service layer is 100% Streamlit-free, and test coverage has grown 3x since Round 13. The primary concerns are:

1. **`chart_stock.py` god module** (818 lines) — first since D16 was resolved, needs immediate splitting
2. **Service layer flat directory** (47 modules) — discoverability declining, needs sub-package organization
3. **`_summary.py` approaching threshold** (464 lines) — C170 will push it past 500

Sprint 21 is architecturally ready with two quick prerequisites (D-125, D-126). C170 and C188 both fit cleanly into the 4-layer architecture. The biggest architectural risk is not the upcoming features — it's the organizational debt in the flat service directory, which will become a significant bottleneck by Sprint 25.

---

*Created: 2026-06-15*
*Maintainer: System Architect*
*Next review: Sprint 21 mid-point or Sprint 22 kickoff*
*Architecture Health: B+ HEALTHY (with structural concerns)*
