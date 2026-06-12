# Developer Cost Estimates — Round 16

> **Date**: 2026-06-20
> **Author**: Developer
> **Context**: Sprint 3 complete, Sprint 4 starting. Estimates for Sprint 4 execution, Sprint 5 (prerequisites + features), Round 16 new feature suggestions (C81-C85), and design debt cleanup (D-035 through D-044).
> **References**: `architect_review_r16.md`, `designer_review_r16.md`, `competitor_research_r16.md`, `tech_debt.md`, `current_problems.md`

---

## 1. Sprint 4 Execution Cost

### R3: Batch API Minimal
- **Time**: 1.5h
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Very Low — isolated utility addition to `FinMindClient` or `_router_base.py`
- **Files**: `src/services/finmind_client.py` (add batch method) or `_router_base.py` (add `_batch_get()` wrapper)
- **Notes**: Architect review confirms 1-2h, no dependencies. This is the gateway to C51's data needs.

### C38: Compare Stories Phase 1
- **Time**: 11h (range: 10-12h)
- **Complexity**: High
- **Dependencies**: R3 for batch data fetching; `_comparison_card()` component (design review requires this before implementation)
- **Risk**: Medium-High — first multi-company comparison layout in the app. No precedent for side-by-side rendering. `st.columns(2)` width allocation is untested. Chart scale enforcement is a new concern.
- **Files**:
  - `src/pages/business_card/_sections.py` — add `_render_compare_stories()` (~60-70 lines)
  - `src/pages/business_card/_helpers.py` — add `_comparison_card()` component (~20 lines)
  - `src/pages/business_card/_sections_discovery.py` (after D37 split) — move compare stories here
  - `src/services/market_data.py` (D25) — for peer company data
- **Design constraints**: Max 2 companies per comparison; identical card components per side; identical chart y-axis ranges. Must define `_comparison_card()` *before* implementation (designer's explicit recommendation). This is flagged as the highest design risk in Sprint 4.
- **Architect's estimate**: 10-12h ✅ aligns

### C51: Sector Heatmap
- **Time**: 14h (range: 12-16h)
- **Complexity**: Medium
- **Dependencies**: R3 + D25 (`market_data.py`) must exist first; D23 (tone guidelines) needed before shipping
- **Risk**: Medium — new visualization type (heatmap via `plotly.graph_objects.Heatmap`). Market-level data flow is architecturally distinct from single-stock pattern. Mobile readability concern.
- **Files**:
  - `src/services/market_data.py` (D25, ~2h included) — new service for market-wide data aggregation
  - `src/pages/sector_heatmap.py` — new page file (~200 lines)
  - `chart.py` or new `chart_sector.py` — heatmap rendering function (~80 lines)
  - `docs/design/tone_guidelines.md` (D23) — content task, 1h, must be done before C51 ships
  - `router.py` — register new page route
- **Design constraints**: Single-hue gradient only (`#EBF5FB` → `#2980B9`). No red→green. Hover template with value + plain-language explanation. `max-width` + horizontal scroll for mobile.
- **Architect's estimate**: 12-16h ✅ aligns

### C48: Company Story Card
- **Time**: 12h (range: 10-14h)
- **Complexity**: Medium
- **Dependencies**: D16 + D24 are complete (confirmed by architect). Can start immediately.
- **Risk**: Medium — `story_composer.py` is a new service module that imports from 4 D16-split modules + `company_facts.py` + `chart.py` + `financial_metrics.py`. Many integration points. Designer requires `_story_card()` component before implementation.
- **Files**:
  - `src/services/story_composer.py` — new service (~150-200 lines) — composes narrative from analogy_engine, key_takeaways, delta_engine, health_scoring
  - `src/pages/business_card/_sections.py` — add `_render_story_card()` (~50 lines)
  - `_router_base.py` or `src/pages/business_card/_helpers.py` — add `_story_card()` component (~20 lines)
  - `src/data/story_templates.yaml` (optional) — narrative templates for future scalability
- **Design constraints**: `#3498DB` border-left, `#F8F9FA` background, max 200 characters, max 3 sentences. Place directly after C37.
- **Architect's estimate**: 10-14h ✅ aligns

### C53-1: Social Sharing URL
- **Time**: 2.5h (range: 2-3h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Very Low — isolated feature. URL generation + copy-to-clipboard. No new visual components if kept simple.
- **Files**:
  - `src/pages/business_card/_sections.py` — add share URL button rendering (~20 lines)
  - `_router_base.py` or `ui_components.py` — `_share_url_button()` helper (~15 lines)
  - `src/utils/url_utils.py` — URL builder with stock_id + tab params (~10 lines)
- **Design constraints**: Button placement should not compete with watchlist button. Consider placing in header's col3 area. Shared URL should deep-link to `/stock/{stock_id}?tab=business-card`.
- **Architect's estimate**: 2-3h ✅ aligns

### Sprint 4 Architecture Debt (addressed alongside features)

#### D25: Market Data Service (`market_data.py`)
- **Time**: 2h
- **Complexity**: Low
- **Dependencies**: Part of C51 implementation
- **Risk**: Low — new service module following existing `financial_metrics.py` pattern
- **Files**: `src/services/market_data.py` — market-wide data aggregation

#### D23: Tone Guidelines for Market Data
- **Time**: 1h
- **Complexity**: Low
- **Dependencies**: None (content task)
- **Risk**: Low — must be done before C51 ships to prevent historian tone violation
- **Files**: `docs/design/tone_guidelines.md`

#### D37: `_sections.py` Split
- **Time**: 1.5h (range: 1-2h)
- **Complexity**: Low
- **Dependencies**: Do alongside C38 + C48 (when `_sections.py` exceeds 650 lines)
- **Risk**: Low — mechanical file split. Must update `_main.py` imports.
- **Files**:
  - `src/pages/business_card/_sections.py` (604 lines) → split into:
    - `_sections_core.py` (~150 lines) — header, one-liner, key metrics, footer
    - `_sections_analysis.py` (~200 lines) — takeaways, deltas, health, risk
    - `_sections_detail.py` (~250 lines) — dividend, revenue breakdown, revenue trend, valuation, news
    - `_sections_discovery.py` (~100 lines) — read next, compare stories, story card
  - `_main.py` — update imports

### Sprint 4 Total

| Item | Time | Complexity |
|------|------|------------|
| R3 (Batch API) | 1.5h | Low |
| C38 (Compare Stories) | 11h | High |
| C51 (Sector Heatmap) + D25 | 14h | Medium |
| C48 (Story Card) | 12h | Medium |
| C53-1 (Social Sharing URL) | 2.5h | Low |
| D23 (Tone Guidelines) | 1h | Low |
| D37 (Sections split) | 1.5h | Low |
| **Sprint 4 Total** | **43.5h** | |

---

## 2. Sprint 5 Total Cost

### Prerequisites (MUST complete before feature coding)

#### D-039: Standardized Section Header Pattern
- **Time**: 1.5h (range: 1-2h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Low — straightforward helper creation + find-and-replace across 8 raw `st.markdown("### ...")` calls
- **Files**:
  - `_router_base.py` — enhance existing `_section_title()` (lines 69-86) with collapsed/expander support, or create new `_section_header()`
  - `src/pages/business_card/_sections.py` — line 34: add `_section_title` to import from `_router_base` (it's NOT imported there currently — designer's critical finding). Replace raw headers at lines 208, 300, 455, 478, 496, 525, 549.
- **Note**: Designer investigation confirmed `_section_title` is NOT imported in `_sections.py` line 34. All 14 business card sections use raw markdown headers. This is the root cause of D-039.

#### D-040: Standardized Disclaimer Component
- **Time**: 0.5h
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Very Low — single function with 3 text variants + `st.caption()`
- **Files**:
  - `_router_base.py` — add `_historian_disclaimer(disclaimer_type)` (~15 lines)
  - `_sections.py` line 604 — replace footer disclaimer with `_historian_disclaimer("general")`
- **Note**: Regulatory compliance item. C73 and C74 each need different disclaimer text. Inconsistent text could create risk in TW financial content.

#### D-041: Sprint 5 Card Components
- **Time**: 1h
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Low — but HIGH risk if skipped. Designer forecasts D-003 regression to B- if Sprint 5 features add inline HTML without these components.
- **Files**:
  - `src/pages/business_card/_helpers.py` or new `src/services/ui_components.py` — add:
    - `_study_card(entry)` — blue border, `#F8F9FA` bg, for C71 study log entries
    - `_expert_card(consensus, source_count)` — orange border, `#FFF8F0` bg, for C73 expert analysis
    - `_scenario_card(scenario_name, result_text)` — blue border, `#F8F9FA` bg, for C74 historical scenarios
  - `docs/design/design_system.md` — add card component specs

#### D-037: Fix `_白话_card` Background Color
- **Time**: 0.3h (<0.5h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Very Low — one-line change
- **Files**: `_router_base.py` line 91 — change `background:#F5F5F5` → `background:#F8F9FA`

### Sprint 5 Prerequisites Subtotal: 3.3h

### Sprint 5 Features

#### C71: Study Log
- **Time**: 10h (range: 8-12h)
- **Complexity**: Medium
- **Dependencies**: D-041 (`_study_card` component)
- **Risk**: Medium — persistence needed (user's study entries must survive page reloads). Follows `watchlist.py` YAML pattern which is proven.
- **Files**:
  - `src/data/study_log.yaml` — initial data file
  - `src/services/study_log.py` — CRUD operations following `watchlist.py` pattern (~60 lines)
  - `src/pages/business_card/_sections_discovery.py` — add `_render_study_log()` (~70 lines)
  - `src/pages/business_card/_main.py` — wire in study log section
- **Notes**: Simplest Sprint 5 feature. Start first. YAML persistence pattern is proven from watchlist.

#### C73: Expert Analysis (10 stocks)
- **Time**: 17h (range: 14-20h)
- **Complexity**: High
- **Dependencies**: D-040 (`_historian_disclaimer`), D-041 (`_expert_card` component)
- **Risk**: High — most complex Sprint 5 feature. Risk of scope creep into `risk_analyzer.py`. May need new `expert_analysis.py` service module. Data source for expert consensus is unclear (FinMind provides institutional tracking but not analyst ratings).
- **Files**:
  - `src/services/expert_analysis.py` — new service module (~200 lines) — keep separate from `risk_analyzer.py` (architect's explicit recommendation to prevent that module crossing 700 lines)
  - `src/data/expert_consensus.yaml` — expert analysis data for 10 stocks (~100 lines)
  - `src/pages/business_card/_sections_analysis.py` — add `_render_expert_analysis()` (~60 lines)
  - `_router_base.py` — add disclaimer component call
- **Risk mitigation**: Create `expert_analysis.py` as separate module. Do NOT extend `risk_analyzer.py`. Monitor `risk_analyzer.py` — currently 567 lines, architect triggers split at 700.

#### C74: Historical Scenarios
- **Time**: 13h (range: 10-16h)
- **Complexity**: Medium
- **Dependencies**: D-040 (`_historian_disclaimer`), D-041 (`_scenario_card` component)
- **Risk**: Medium — needs `historical_scenarios.yaml` data file. Historical price calculations must use existing FinMind data. Selectbox-only interaction (no free-form inputs).
- **Files**:
  - `src/data/historical_scenarios.yaml` — 5-10 decision points per top stock (~200 lines)
  - `src/pages/business_card/_sections_discovery.py` — add `_render_scenarios()` (~80 lines)
  - `src/services/scenario_engine.py` — historical outcome calculation (~80 lines)
- **Notes**: Stories must be framed as "this is what happened" not "this is what to do". Selectbox interaction for decision points, not free text.

### Sprint 5 Features Subtotal: 40h

### Sprint 5 Alongside-Feature Work

#### D-038: C41 API in View Layer (moved to _sections.py)
- **Time**: 1.5h (range: 1-2h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Low — pre-compute peer data in router, pass via data dict
- **Files**:
  - `_router_base.py` — add peer stock pre-computation to `get_stock_data()`
  - `src/pages/business_card/_sections.py` — remove `client.get_stock_info()` call at line ~552, use `data["peers"]` instead

### Sprint 5 Total

| Category | Time | Notes |
|----------|------|-------|
| Prerequisites (D-039, D-040, D-041, D-037) | 3.3h | MUST complete before feature coding |
| C71 (Study Log) | 10h | Simplest, start first |
| C73 (Expert Analysis) | 17h | Most complex, highest risk |
| C74 (Historical Scenarios) | 13h | Medium complexity |
| D-038 fix (alongside features) | 1.5h | Pre-compute peers in router |
| **Sprint 5 Total** | **44.8h** | |

---

## 3. Round 16 New Feature Cost (C81-C85)

### C81: Historical Decision Scenario Explorer ("What Would Have Happened")
- **Time**: 17h (range: 14-20h)
- **Complexity**: High
- **Dependencies**: Historical price data from FinMind (existing); D-040 disclaimer component
- **Risk**: High — branching logic is new for Stock Explorer. Must start with hardcoded historical data. Educational framing is critical (Bloom's model). 5-10 scenarios per stock × 10 stocks = 50-100 scenario definitions.
- **Files**:
  - `src/data/historical_scenarios.yaml` — 5-10 decision points per top 10 stock (~300 lines)
  - `src/services/scenario_engine.py` — outcome calculation logic (~100 lines)
  - `src/pages/scenario_page.py` — new page for scenario exploration (~200 lines)
  - `router.py` — register route
  - `navbar.py` — add navigation link
- **Recommendation**: Medium-term priority. Highest innovation but highest effort. Use C74's `historical_scenarios.yaml` as data foundation if both are built.

### C82: Animated Data Story (Scrollable Visual Company History)
- **Time**: 14h (range: 12-16h)
- **Complexity**: High
- **Dependencies**: Plotly animation framework or JavaScript scroll-driven animation library
- **Risk**: High — Streamlit + JavaScript animation is untested. The developer survey would need to prototype: (1) scroll-driven Plotly frame updates, or (2) CSS scroll-snap + static image swap. True animation may require `streamlit.components.v1` custom component.
- **Files**:
  - `src/pages/data_story.py` — new page for scrollable visual story (~250 lines)
  - `src/templates/step_card.html` — HTML template for each scroll step
  - `static/data_story.js` — scroll-driven animation logic (if JS approach chosen)
  - `chart.py` — add animated/step-wise chart functions (~100 lines)
  - `router.py` — register route
- **Recommendation**: Start with MVP (5 scroll steps, static fade-in images) to de-risk. Full animation as enhancement. Risk is high because Streamlit's JS integration is not well-tested in this codebase.

### C83: Investment Memo Template (Structured Reflection Tool)
- **Time**: 8h (range: 6-10h)
- **Complexity**: Medium
- **Dependencies**: None (standalone feature). Future: C50 (Learning Progress Tracker) for integration.
- **Risk**: Low — templated form with 5-7 prompts. Pre-fill logic must access business card data via existing services. C55 (Investment Diary) partially overlaps — this is the structured version.
- **Files**:
  - `src/pages/memo_page.py` — new page for memo template (~150 lines)
  - `src/data/memo_templates.yaml` — template prompts and structure (~50 lines)
  - `src/services/memo_engine.py` — pre-fill logic using existing analysis results (~80 lines)
  - `router.py` — register route
  - `src/pages/business_card/_sections.py` — add "📝 投資備忘錄" button linking to memo page (~5 lines)
- **Recommendation**: Lowest effort (6-10h), highest ROI per QA research. 長投學堂 proves demand. Directly extends C55. Perfect "historian of self" feature. **Should be prioritized first among C81-C85.**

### C84: Market Event Case Study (Interactive Historical Market Event Explorer)
- **Time**: 12h (range: 10-14h)
- **Complexity**: Medium
- **Dependencies**: Historical market data from FinMind (existing). D-040 disclaimer for educational framing.
- **Risk**: Medium — primarily content-heavy. Content writing for 5-10 case studies is the bulk of effort. "How does this relate to today?" comparison logic needs design.
- **Files**:
  - `src/data/market_case_studies.yaml` — 5-10 case studies (~400 lines of content)
  - `src/pages/case_study_page.py` — new page for case study exploration (~200 lines)
  - `src/services/case_engine.py` — current market comparison logic (~60 lines)
  - `router.py` — register route
  - `navbar.py` — add navigation link
- **Recommendation**: Medium priority. No TW competitor has interactive case studies. Content writing is the bottleneck, not code complexity.

### C85: Financial Wellness Check (Behavioral Finance Self-Assessment)
- **Time**: 10h (range: 8-12h)
- **Complexity**: Medium
- **Dependencies**: None (standalone). Future: company recommendation engine (not built yet).
- **Risk**: Low-Medium — 10-question quiz is straightforward. Company recommendation matching logic is basic (filter by risk profile). Must frame as self-awareness, not investment advice (legal).
- **Files**:
  - `src/pages/wellness_check.py` — new page for self-assessment (~200 lines)
  - `src/data/wellness_questions.yaml` — 10 questions + scoring rubric (~100 lines)
  - `src/services/wellness_engine.py` — profile generation + company recommendation (~100 lines)
  - `router.py` — register route
  - `navbar.py` — add navigation link
- **Recommendation**: Enables personalization for all other content. Cleo/Plum/Bloom prove demand. Medium effort with high strategic value.

### C81-C85 Total

| ID | Title | Time | Complexity | Priority | Rec. Order |
|----|-------|------|------------|----------|------------|
| C83 | Investment Memo Template | 8h | Medium | P2 | **1st** |
| C85 | Financial Wellness Check | 10h | Medium | P2 | 2nd |
| C84 | Market Event Case Study | 12h | Medium | P2 | 3rd |
| C82 | Animated Data Story | 14h | High | P2 | 4th |
| C81 | Historical Decision Scenarios | 17h | High | P2 | 5th |
| **Total** | | **51h** | | | |

---

## 4. Design Debt Cleanup Cost (D-035 through D-044)

### Carry-Over P2 Issues from Previous Rounds

#### D-035: C41 Peer Cards Use Inline HTML
- **Time**: 0.5h
- **Complexity**: Low
- **Dependencies**: None (D24 extraction is done; this is in `_sections.py` now)
- **Risk**: Very Low — replace inline HTML with `_info_card()` or `_peer_card()` component
- **Files**: `src/pages/business_card/_sections.py` lines 569-area — replace raw HTML at lines 522-532 (original numbering, now shifted after D24)

#### D-036: C44 Risk Dimension Cards Use Non-Standard Background
- **Time**: 0.3h (<0.5h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Very Low — one-line change
- **Files**: `src/pages/business_card/_helpers.py` line 86 — change `background:#FFF8F0` → `background:#F8F9FA`

#### D-037: `_白话_card` Background Color
- **Time**: 0.3h (<0.5h)
- **Complexity**: Low
- **Dependencies**: None (already counted in Sprint 5 prerequisites)
- **Risk**: Very Low — one-line change in `_router_base.py` line 91

#### D-038: C41 API Call in View Layer
- **Time**: 1.5h (already counted in Sprint 5)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Low — pre-compute peers in router

### New P2 Issues from Round 16

#### D-039: No Standardized Section Header Pattern ✅ (Sprint 5 prerequisite)
- **Already accounted in Sprint 5 Total above**

#### D-040: No Standardized Disclaimer Component ✅ (Sprint 5 prerequisite)
- **Already accounted in Sprint 5 Total above**

#### D-041: No Sprint 5 Card Components ✅ (Sprint 5 prerequisite)
- **Already accounted in Sprint 5 Total above**

#### D-042: Health Dimension Mini-Cards Use Non-Standard Styling
- **Time**: 0.5h
- **Complexity**: Low
- **Dependencies**: None (can be done anytime)
- **Risk**: Low — create `_mini_score_card()` helper, replace inline HTML in `_sections.py` lines 227-236
- **Files**:
  - `_router_base.py` — add `_mini_score_card(label, score, indicator, color)` (~15 lines)
  - `src/pages/business_card/_sections.py` — replace inline HTML at lines 227-236 with component call
  - `docs/design/design_system.md` — add "Mini Score Card" variant spec
- **Note**: This is the lowest Round 16 issue. The compact style is appropriate for 5-column layout, but needs formalization as a design system variant.

#### D-043: Dividend History Table Uses Inline HTML Instead of `st.dataframe`
- **Time**: 1.5h (range: 1-2h)
- **Complexity**: Low
- **Dependencies**: None
- **Risk**: Low — restructure table rendering. Must decide: (a) convert to `st.dataframe()` with badge column config, or (b) keep HTML but fix `border-bottom:1px solid #F8F9FA` → `#BDC3C7` for visible row separators. Option (a) is preferred but requires restructuring the badge data into a DataFrame-friendly format.
- **Files**: `src/pages/business_card/_sections.py` lines 420-439 — replace HTML table construction
- **Note**: `st.dataframe()` provides sorting and free filtering "for free" — this is a UX improvement beyond just debt cleanup.

#### D-044: C41 Read Next Header Doesn't Use `_section_title()` Helper
- **Time**: 0.3h (<0.5h)
- **Complexity**: Low
- **Dependencies**: D-039 (must be done first — need `_section_title()` import in `_sections.py`)
- **Risk**: Very Low — one-line change after D-039
- **Files**: `src/pages/business_card/_sections.py` line 549 — replace `st.markdown("### 📖 推薦閱讀")` with `_section_title("📖 推薦閱讀")`

### Design Debt Cleanup Total (excluding items already counted in Sprint 5)

| ID | Time | Complexity | Notes |
|----|------|------------|-------|
| D-035 | 0.5h | Low | Replace peer card inline HTML |
| D-036 | 0.3h | Low | One-line bg color fix |
| D-037 | (in Sprint 5) | Low | Already counted in Sprint 5 prerequisites |
| D-038 | (in Sprint 5) | Low | Already counted in Sprint 5 features |
| D-039 | (in Sprint 5) | Low | Already counted in Sprint 5 prerequisites |
| D-040 | (in Sprint 5) | Low | Already counted in Sprint 5 prerequisites |
| D-041 | (in Sprint 5) | Low | Already counted in Sprint 5 prerequisites |
| D-042 | 0.5h | Low | `_mini_score_card()` component |
| D-043 | 1.5h | Low | Dividend table → `st.dataframe` |
| D-044 | 0.3h | Low | One-line header fix (after D-039) |
| **New items total** | **3.1h** | | D-035 through D-044 excluding duplicates |

---

## 5. Summary Table

### Grand Totals by Category

| Category | Items | Total Hours | Complexity Range |
|----------|-------|-------------|-----------------|
| **Sprint 4 Execution** | R3, C38, C51, C48, C53-1 | 39h | Low–High |
| **Sprint 4 Debt** | D25, D23, D37 | 4.5h | Low |
| **Total Sprint 4** | | **43.5h** | |
| **Sprint 5 Prerequisites** | D-039, D-040, D-041, D-037 | 3.3h | Low |
| **Sprint 5 Features** | C71, C73, C74 | 40h | Medium–High |
| **Sprint 5 Debt** | D-038 | 1.5h | Low |
| **Total Sprint 5** | | **44.8h** | |
| **New Features (C81-C85)** | C83, C85, C84, C82, C81 | 51h | Medium–High |
| **Design Debt Cleanup** | D-035, D-036, D-042, D-043, D-044 | 3.1h | Low |
| **All Categories Grand Total** | | **142.4h** | |

### Sprint-by-Sprint Breakdown

| Sprint | Features | Debt | Total | Weeks (1 dev) |
|--------|----------|------|-------|---------------|
| Sprint 4 | 39h | 4.5h | 43.5h | ~1.1 weeks |
| Sprint 5 | 40h | 4.8h (prereqs + D-038) | 44.8h | ~1.1 weeks |

### Recommended Priority Order for C81-C85

| Order | ID | Title | Time | Rationale |
|-------|----|-------|------|-----------|
| 1 | C83 | Investment Memo Template | 8h | Lowest effort, highest ROI, extends C55 directly |
| 2 | C85 | Financial Wellness Check | 10h | Enables personalization, proven by Cleo/Plum/Bloom |
| 3 | C84 | Market Event Case Study | 12h | Unique "historian" differentiator, no TW competitor |
| 4 | C82 | Animated Data Story | 14h | Visual differentiation, but high JS risk |
| 5 | C81 | Historical Decision Scenarios | 17h | Highest innovation, highest effort, overlaps with C74 data |

---

## 6. Risk Assessment

### Critical Risks (could impact estimates by >20%)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **C73 Expert Analysis data source** | If FinMind doesn't provide analyst consensus data, must find alternative or mock data. Could add 4-6h for data sourcing. | Medium | Spike FinMind's API endpoints first; fall back to mock data with `_historian_disclaimer()` |
| **C82 Animated Data Story JS integration** | Streamlit + custom JavaScript animation is untested. Could require `streamlit.components.v1` custom component (adds 6-8h). | High | Start with MVP (static fade-in), defer full animation |
| **C38 Compare Stories layout** | `st.columns(2)` may not render well with existing card components. May need full-width stacked layout (+2-4h). | Medium | Prototype layout before building full feature |
| **C71 Study Log persistence** | YAML persistence works for single-user. If multi-user is needed later, SQLite migration adds 4-6h. | Low | Document as single-user limitation; revisit in Sprint 6 |

### Medium Risks (could impact estimates by 10-20%)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **C51 mobile heatmap** | Heatmaps with many cells may be unreadable on mobile despite horizontal scroll. May need simplified mobile view (+2-3h). | Medium | Design mobile-specific cell count limit |
| **C74 historical data gaps** | FinMind's historical depth varies by stock. Some calculations may need graceful degradation (+1-2h). | Medium | Add try/except with fallback messages |
| **D37 sections split import tracking** | Splitting `_sections.py` into 4 files requires updating all imports in `_main.py` and potentially other files. Mechanical but error-prone (+0.5-1h). | Medium | Use IDE refactoring tools; test each split incrementally |
| **C48 story_composer complexity** | Importing from 6+ services (4 from D16 split + company_facts + chart + financial_metrics) may surface interface mismatches (+2-3h). | Medium | Write a composition test early |

### Low Risks (minimal estimate impact)

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **D-039 section header edge cases** | 7 different raw `st.markdown("### ...")` patterns may not all be trivially replaceable | Low | Test each replacement visually |
| **C53-1 OG preview cards** | If social sharing preview cards are needed later, that's a separate feature | Low | Keep C53-1 as URL-only for now |
| **Tone guidelines (D23)** | Content task, not code. May have iteration cycles with stakeholders | Low | Write initial draft, async review |

### Estimation Confidence

| Category | Confidence | Notes |
|----------|------------|-------|
| Sprint 4 (R3, C38, C51, C48, C53-1) | High (±10%) | Architect has reviewed and confirmed ranges. Patterns established from Sprint 3. |
| Sprint 4 Debt (D25, D23, D37) | High (±10%) | Mechanical work with clear scope. |
| Sprint 5 Prerequisites | Very High (±5%) | Simple, well-defined helpers. |
| Sprint 5 Features | Medium (±20%) | C73 is the uncertainty. Data source for expert analysis not confirmed. |
| C81-C85 New Features | Medium (±25%) | Based on QA research competitor data. No spikes run. C82 and C81 are the most uncertain. |
| Design Debt Cleanup D-035/D-036/D-042/D-043/D-044 | High (±10%) | Simple, well-defined fixes. |

### Key Files That Would Need Changes

| File | Changes By | Current Size | Expected Growth |
|------|-----------|--------------|-----------------|
| `src/pages/business_card/_sections.py` | C38, C48, D37, C71, C73, C74 | 604 lines | Split into 4 files (~600 total) |
| `src/pages/business_card/_helpers.py` | D-042, C38 `_comparison_card()`, C48 `_story_card()` | 95 lines | ~150 lines |
| `src/pages/business_card/_main.py` | D37 import updates, C71/C73/C74 wiring | 83 lines | ~120 lines |
| `_router_base.py` | D-039, D-040, D-041, D-037, D-038, D-042 | ~169 lines | ~220 lines |
| `src/services/market_data.py` (NEW) | C51, D25 | — | ~200 lines |
| `src/services/story_composer.py` (NEW) | C48 | — | ~180 lines |
| `src/services/expert_analysis.py` (NEW) | C73 | — | ~200 lines |
| `src/services/scenario_engine.py` (NEW) | C74 | — | ~80 lines |
| `src/services/study_log.py` (NEW) | C71 | — | ~60 lines |

### Design System Doc Updates Needed (from designer_review_r16.md)

These are content/ spec tasks that affect developer implementation:

| Update | Affected Features | Effort |
|--------|------------------|--------|
| Add "Mini Score Card" variant | D-042 | 0.5h |
| Add Story Card specification | C48 | 0.5h |
| Add Comparison Layout Rules (Section 5.5) | C38 | 0.5h |
| Add Heatmap Color Rules | C51 | 0.5h |
| Add Section Header Standard | D-039 | 0.5h |
| Add Disclaimer Component Specification | D-040 | 0.5h |
| **Total design system updates** | | **3h** |

---

*Created: 2026-06-20*
*Developer cost estimates for Round 16 review cycle.*
*Next review: Sprint 4 mid-point (after R3 + one major feature complete).*
