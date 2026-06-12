# Developer Cost Estimates — Round 17

> **Date**: 2026-06-12
> **Author**: Developer
> **Context**: Sprint 4 complete (C38, C48, C51, C53-1). Estimates for Sprint 5 (prerequisites + features), Round 17 new design/architect issues (D-042 through D-048), P0 bug fix, and architecture debt.
> **References**: `architect_review_r17.md`, `designer_review_r17.md`, `developer_estimates_r16.md`

---

## 1. P0 Bugs (Fix Immediately)

### D-043: `_render_key_metrics()` calls non-existent `get_roe_analyzer()` / `get_pbr_analyzer()`

| Field | Value |
|-------|-------|
| **Item ID** | D-043 |
| **Description** | `_sections.py` lines 437 and 445 call `get_roe_analyzer(roe)` and `get_pbr_analyzer(pbr)`. These functions do not exist. The correct functions `get_roe_analogy()` and `get_pbr_analogy()` are already imported (lines 14-15) but not used in these calls. |
| **Estimated Hours** | 0.25h (2 lines changed) |
| **Dependencies** | None |
| **Risk Level** | **CRITICAL P0** — Runtime NameError crash when ROE/PBR fallback paths execute |
| **Affected Files** | `src/pages/business_card/_sections.py` lines 437, 445 |
| **Fix** | Rename `get_roe_analyzer` → `get_roe_analogy` and `get_pbr_analyzer` → `get_pbr_analogy` |
| **Notes** | Confirmed via code search: these function names appear ONLY in these two call sites, nowhere else in the codebase. The correct functions are imported from `analogy_engine`. This is a copy-paste error from Sprint 4. Will crash the business card page for any stock that hits the ROE fallback (col2) or PBR fallback (col3) in `_render_key_metrics()`. |

**P0 Total: 0.25h**

---

## 2. Sprint 5 Prerequisites

### D37: Split `_sections.py` (918 lines → 4 sub-modules)

| Field | Value |
|-------|-------|
| **Item ID** | D37 |
| **Description** | `_sections.py` is 918 lines — extraction D24 was supposed to prevent monolith re-growth. Sprint 4 added `_render_story_card` (~115 lines), `_render_compare_stories` (~99 lines), `_render_share_section` (~101 lines). Must split before Sprint 5 adds more sections. |
| **Estimated Hours** | 2.0h (range: 1.5-2.5h) |
| **Dependencies** | None — pure refactoring, no logic changes |
| **Risk Level** | Medium-High — mechanical split is simple but import ripple effects must be carefully managed. `_main.py` imports all 16 section functions from `_sections.py`. Any missed import will cause runtime errors. |
| **Affected Files** | `src/pages/business_card/_sections.py` (918 lines) → split into 4 files; `src/pages/business_card/_main.py` — update imports; `src/pages/business_card/__init__.py` — no change needed (only exports `_render_business_card`) |
| **Proposed Split** | `_sections_core.py` (~200 lines) — `_render_header`, `_render_one_liner`, `_render_key_metrics`, `_render_footer`; `_sections_analysis.py` (~250 lines) — `_render_takeaways`, `_render_deltas`, `_render_health`, `_render_risk`; `_sections_detail.py` (~280 lines) — `_render_dividend`, `_render_revenue_breakdown`, `_render_revenue_trend`, `_render_valuation`, `_render_news`; `_sections_discovery.py` (~250 lines) — `_render_compare_stories`, `_render_read_next`, `_render_story_card`, `_render_share_section` |
| **Notes** | Round 16 estimated 1.5h; now 918 lines (vs 612 at R16) so +0.5h for the larger file. Must be FIRST Sprint 5 task. Import management is the main risk — use IDE refactoring tools and test after each sub-module extraction. |

### D-039: Section Header Standardization

| Field | Value |
|-------|-------|
| **Item ID** | D-039 |
| **Description** | 12+ sections across `_sections.py` and `sector_heatmap.py` use raw `st.markdown("### ...")` instead of the `_section_title()` helper in `_router_base.py`. The helper already exists (lines 69-86) but has a bug (D-047) that must be fixed first. |
| **Estimated Hours** | 1.5h (range: 1-2h) |
| **Dependencies** | D-047 (fix `_section_title()` inverted logic bug) — must be done first; D37 (sections split) — should be done first so each sub-module imports `_section_title` |
| **Risk Level** | Low — straightforward find-and-replace, but D-047 bugfix is a prerequisite. |
| **Affected Files** | `_router_base.py` — enhance `_section_title()` with D-047 fix; each `_sections_*.py` sub-module — add `_section_title` import and replace raw headers (8+ call sites in `_sections.py`: lines 326, 418, 573, 596, 614, 643, 768, 832); `sector_heatmap.py` — lines 60, 221, 305, 367 |
| **Notes** | Designer investigation confirmed `_section_title` is NOT imported in `_sections.py` (line 34 import block lacks it). Each sub-module will need to add it. The `_sections_core.py` group is most critical since it renders every page load. |

### D-040: Historian Disclaimer Component

| Field | Value |
|-------|-------|
| **Item ID** | D-040 |
| **Description** | Create `_historian_disclaimer(disclaimer_type)` helper for regulatory/educational disclaimers. C73 (expert analysis) and C74 (historical scenarios) each need different disclaimer text. Currently only a single general disclaimer exists in `_render_footer()`. |
| **Estimated Hours** | 0.5h |
| **Dependencies** | None |
| **Risk Level** | Very Low — single function with 3 text variants |
| **Affected Files** | `_router_base.py` — add `_historian_disclaimer(disclaimer_type)` (~15 lines): `"general"` for footer, `"expert"` for C73, `"scenario"` for C74 |
| **Notes** | Quick win. Regulatory compliance item. Should use `st.caption()` or muted `_info_card()` styling. |

### D-041: Sprint 5 Card Components

| Field | Value |
|-------|-------|
| **Item ID** | D-041 |
| **Description** | Create `_study_card()`, `_expert_card()`, `_scenario_card()` reusable components before Sprint 5 feature coding begins. Without these, Sprint 5 features will use inline HTML, worsening D-003. |
| **Estimated Hours** | 1.5h (range: 1-2h) |
| **Dependencies** | None |
| **Risk Level** | Low — but HIGH risk if skipped. Designer forecasts D-003 regression to B grade if Sprint 5 features add inline HTML. |
| **Affected Files** | `_router_base.py` — add 3 components (~45 lines total); `docs/design/design_system.md` — add specs |
| **Component Specs** | `_study_card(date, topic, title, summary)` — blue border `#3498DB`, `#F8F9FA` bg; `_expert_card(consensus_label, analyst_count, key_points)` — orange border `#F39C12`, `#FFF8F0` bg; `_scenario_card(event_name, event_date, narrative, takeaway)` — blue border `#3498DB`, `#F8F9FA` bg |
| **Notes** | Round 16 estimated 1h; revised up to 1.5h because `_expert_card` has more complex internal layout (consensus badge + key points). Must be done before C71/C73/C74 coding. |

### D-047: Fix `_section_title()` Inverted Logic Bug

| Field | Value |
|-------|-------|
| **Item ID** | D-047 |
| **Description** | `_router_base.py` line 70: `if not title:` should be `if title:` — the condition is inverted. When title is falsy, it tries to render `### 📊 {title}` (empty). When title is truthy, it falls through to emoji detection. |
| **Estimated Hours** | 0.1h (<0.5h) |
| **Dependencies** | None |
| **Risk Level** | Very Low — single-line fix |
| **Affected Files** | `_router_base.py` line 70 |
| **Notes** | Pre-existing bug (not introduced in Sprint 4). Fix as part of D-039 prerequisite work. Function still renders something for all inputs, but behavior is inverted. |

**Prerequisites Subtotal: 5.6h**

---

## 3. Sprint 5 Features

### C71: Study Log

| Field | Value |
|-------|-------|
| **Item ID** | C71 |
| **Description** | User-facing study log showing learning progress for a stock. Persisted entries surviving page reloads. Uses YAML persistence following `watchlist.py` pattern. `_study_card()` component renders each entry. |
| **Estimated Hours** | 10h (range: 8-12h) |
| **Dependencies** | D-041 (`_study_card` component); D-039 (section header for the study log section); D37 (split — section goes into `_sections_discovery.py`) |
| **Risk Level** | Medium — YAML persistence pattern is proven from `watchlist.py`, but this is the first user-generated content feature. Need to handle empty states, entry creation, and session-based display. |
| **Affected Files** | `src/data/study_log.yaml` — initial data file; `src/services/study_log.py` — CRUD operations following `watchlist.py` pattern (~60 lines); `src/pages/business_card/_sections_discovery.py` — add `_render_study_log()` (~70 lines); `src/pages/business_card/_main.py` — wire in study log section |
| **Notes** | Simplest Sprint 5 feature. Start first to establish the pattern. Round 16 estimated 10h — confirmed. The `_study_card()` component (D-041) will be the visual building block. Need to decide: entries per-stock or per-user (single-user app = per-stock). |

### C73: Expert Analysis (10 stocks)

| Field | Value |
|-------|-------|
| **Item ID** | C73 |
| **Description** | Expert analysis section for 10 stocks showing consensus ratings and analyst commentary. Most complex Sprint 5 feature. `_expert_card()` component renders each analysis. |
| **Estimated Hours** | 18h (range: 15-22h) |
| **Dependencies** | D-040 (`_historian_disclaimer("expert")`); D-041 (`_expert_card` component); D-039 (section header) |
| **Risk Level** | **High** — Data source for expert consensus is unclear. FinMind provides institutional tracking but not analyst ratings. May need mock/curated data. Risk of scope creep into `risk_analyzer.py` (currently 567 lines, architect's threshold is 700). |
| **Affected Files** | `src/services/expert_analysis.py` — new service module (~200 lines), MUST be separate from `risk_analyzer.py`; `src/data/expert_consensus.yaml` — expert analysis data for 10 stocks (~100 lines); `src/pages/business_card/_sections_analysis.py` — add `_render_expert_analysis()` (~60 lines) |
| **Risk Mitigation** | Create `expert_analysis.py` as completely separate module. Do NOT extend `risk_analyzer.py`. Spike FinMind API endpoints first to find analyst data. If unavailable, curate mock data for 10 stocks with `_historian_disclaimer("expert")` framing. |
| **Notes** | Round 16 estimated 17h; revised to 18h because architect flagged the `risk_analyzer.py` boundary risk — need strict module separation. The 10-stock scope is fixed (not all stocks). Content writing for `expert_consensus.yaml` is ~4h of the estimate. |

### C74: Historical Scenarios

| Field | Value |
|-------|-------|
| **Item ID** | C74 |
| **Description** | Historical scenarios section showing "what happened to this stock during event X?" Selectbox-driven interaction. `_scenario_card()` component renders each scenario. |
| **Estimated Hours**  | 14h (range: 11-18h) |
| **Dependencies** | D-040 (`_historian_disclaimer("scenario")`); D-041 (`_scenario_card` component); D-039 (section header) |
| **Risk Level** | Medium — Historical price calculations use existing FinMind data. Content-heavy: `historical_scenarios.yaml` requires 5-10 decision points per stock for top stocks. Selectbox-only interaction (no free-form inputs). |
| **Affected Files** | `src/data/historical_scenarios.yaml` — scenario definitions (~200 lines of content); `src/services/scenario_engine.py` — historical outcome calculation (~80 lines), separate module to avoid bloating existing services; `src/pages/business_card/_sections_discovery.py` — add `_render_scenarios()` (~80 lines) |
| **Notes** | Round 16 estimated 13h; revised to 14h because `scenario_engine.py` needs more careful historical price lookup logic. Content writing for `historical_scenarios.yaml` is ~5h of the estimate. Stories must be framed as "this is what happened" not "this is what to do" — educational framing per Bloom's model. |

**Sprint 5 Features Subtotal: 42h**

---

## 4. Design Debt (D-042, D-043, D-044 from Round 16 + D-045 to D-048)

### D-042: Health Dimension Mini-Cards Use Non-Standard Styling

| Field | Value |
|-------|-------|
| **Item ID** | D-042 |
| **Description** | The 5-dimension score cards in `_render_health()` (lines 346-355 of `_sections.py`) use inline HTML with `padding:0.5rem`, `border-radius:10px`, and no `border-left`. Design system specifies `padding:1.2rem`, `border-radius:12px`, `border-left:4px solid`. |
| **Estimated Hours** | 0.5h |
| **Dependencies** | D37 (move to `_sections_analysis.py` first) |
| **Risk Level** | Low — create `_mini_score_card()` helper, replace inline HTML |
| **Affected Files** | `_router_base.py` — add `_mini_score_card(label, score, indicator, color, metric_html)` (~20 lines); `_sections_analysis.py` — replace inline HTML with component call |
| **Notes** | The compact style is appropriate for 5-column layout. Formalize it as a "Mini Score Card" design system variant. This is the lowest Round 16 carry-over issue. |

### D-043: Dividend History Table Uses Inline HTML

| Field | Value |
|-------|-------|
| **Item ID** | D-043 (design) |
| **Description** | The dividend history table (lines 538-557) builds a complete HTML table from scratch. `border-bottom:1px solid #F8F9FA` is nearly invisible on white. Badge rendering via HTML string concatenation is fragile. |
| **Estimated Hours** | 1.5h (range: 1-2h) |
| **Dependencies** | D37 (move to `_sections_detail.py` first) |
| **Risk Level** | Low — restructure table rendering |
| **Affected Files** | `_sections_detail.py` — replace HTML table construction with `st.dataframe()` + column config for badges, or fix border color to `#BDC3C7` |
| **Notes** | Design review separately flagged this as D-043 (debt). Architect review separately flagged the NameError bug as D-043 (P0). These are different issues in the same ID. Using D-043 (design) here for the inline HTML issue. `st.dataframe()` provides sorting and filtering "for free" — UX improvement beyond debt cleanup. |

### D-044: C41 Read Next Header Doesn't Use `_section_title()`

| Field | Value |
|-------|-------|
| **Item ID** | D-044 (design) |
| **Description** | Line 768 uses raw `st.markdown("### 📖 推薦閱讀")` instead of `_section_title("📖 推薦閱讀")`. Same pattern as D-047 (C53-1 header). |
| **Estimated Hours** | 0.25h (<0.5h) |
| **Dependencies** | D-039 (must have `_section_title` import in the sub-module); D37 (move to `_sections_discovery.py`) |
| **Risk Level** | Very Low — one-line change |
| **Affected Files** | `_sections_discovery.py` — replace raw markdown with `_section_title()` call |
| **Notes** | Quick win. Do alongside D-039. |

### D-045: C51 Sector Grid and Top Movers Use Inline HTML

| Field | Value |
|-------|-------|
| **Item ID** | D-045 |
| **Description** | `_render_sector_grid()` (lines 342-362) and `_render_top_movers()` (lines 391-444) in `sector_heatmap.py` use inline HTML with non-standard styling. Grid cells use `padding:1rem` (vs design system `1.2rem`). Top-movers use `border-radius:10px` (vs `12px`) and `padding:0.7rem 1rem` (vs `1.2rem`). Creates a third distinct card style. |
| **Estimated Hours** | 1.5h (range: 1-2h) |
| **Dependencies** | None |
| **Risk Level** | Low — create compact card helpers or adapt existing components |
| **Affected Files** | `sector_heatmap.py` — replace inline HTML; optionally `_router_base.py` — add `_compact_card()` and `_mover_row()` helpers if the compact style is intentional |
| **Notes** | Designer's effort estimate: 1-2h. The compact style may be intentional for grid layouts — if so, document it as a "Compact Card" design system variant. The top-mover rows could use `_info_card()` with reduced padding instead of raw HTML. |

### D-046: C51 4th KPI Card Uses Inline HTML Instead of `_白话_card()`

| Field | Value |
|-------|-------|
| **Item ID** | D-046 |
| **Description** | The first 3 KPI cards (lines 175-192) correctly use `_白话_card()`, but the 4th card (漲跌產業數, lines 195-201) uses inline HTML with manually specified styling. |
| **Estimated Hours** | 0.25h (<0.5h) |
| **Dependencies** | None |
| **Risk Level** | Very Low — one-line replacement |
| **Affected Files** | `sector_heatmap.py` lines 195-201 — replace with `_白话_card()` call |
| **Notes** | Quickest design debt fix. Designer's estimate: <0.5h. The emoji-in-value format is slightly non-standard for `_白话_card()` but more consistent than inline HTML. |

### D-047: C53-1 Share Section Header Doesn't Use `_section_title()`

| Field | Value |
|-------|-------|
| **Item ID** | D-047 (design) |
| **Description** | Line 832 uses raw `st.markdown("### 🔗 分享這張名片")` instead of `_section_title()`. Same pattern as D-044. |
| **Estimated Hours** | 0.25h (<0.5h) |
| **Dependencies** | D-039 (must have `_section_title` import); D37 (move to `_sections_discovery.py`) |
| **Risk Level** | Very Low — one-line change |
| **Affected Files** | `_sections_discovery.py` — replace raw markdown with `_section_title()` call |
| **Notes** | Quick win. Do alongside D-039. |

### D-048: C53-1 Share Button Uses `st.html()` — Non-Standard Component

| Field | Value |
|-------|-------|
| **Item ID** | D-048 |
| **Description** | The copy-to-clipboard button uses `st.html()` with raw JavaScript (lines 875-910). This is the first use of `st.html()` for a UI component. The button's inline styles (`background:#F0F0F0`, `border-radius:8px`) don't match any design system specification. Additionally, the JS references `document.getElementById('share-url-input')` which Streamlit doesn't render — making the feature non-functional (see D-046 architect). |
| **Estimated Hours** | 1.5h (range: 1-2h) |
| **Dependencies** | D-046 (architect) — the JS element ID issue must be fixed; this item standardizes the component |
| **Risk Level** | Medium — the feature is currently non-functional due to the JS element ID bug. Fix requires either: (a) pure Streamlit approach with `st.button()` + `st.toast()`, or (b) `streamlit.components.v1.html()` with self-contained HTML. |
| **Affected Files** | `_sections_discovery.py` — replace `st.html()` calls with standardized `_share_button()` helper; `_router_base.py` — add `_share_button(url, key)` encapsulating the JS + HTML |
| **Notes** | Designer's estimate: 0.5-1h. Revised to 1.5h because the feature is architecturally broken (D-046 architect) and needs a functional fix, not just standardization. The `_share_button()` helper should use design system colors and document the `st.html()` pattern as a "JavaScript Escape Hatch" in the design system. |

**Design Debt Subtotal: 5.75h**

---

## 5. Architecture Debt

### D-044 (architect): `sector_heatmap.py` Service Layer Extraction

| Field | Value |
|-------|-------|
| **Item ID** | D-044 (architect) |
| **Description** | `sector_heatmap.py` (444 lines) is a standalone page with no service-layer abstraction. Contains inline sector metric computation (lines 134-165), inline batch fetching with progress bar (lines 104-125), and direct `BatchAPI` usage from the presentation layer. Violates the 4-layer architecture. |
| **Estimated Hours** | 2.5h (range: 2-3h) |
| **Dependencies** | None |
| **Risk Level** | Medium — extracting a service layer from a working page risks breaking the page. Must maintain the progress bar UX. |
| **Affected Files** | `src/services/market_data.py` (NEW, ~120 lines) — `compute_sector_metrics(summary_map, sector_stocks)` + `fetch_sector_data(client, all_stock_info)`; `sector_heatmap.py` — reduce to ~280 lines by extracting computation and data fetching |
| **Notes** | Architect's estimate: 2-3h. Not blocking for Sprint 5 features. Do alongside D37 split. The `market_data.py` service was originally proposed in D25 and never created. This is the right time to create it. |

### D-046 (architect): Share Section JS Fix

| Field | Value |
|-------|-------|
| **Item ID** | D-046 (architect) |
| **Description** | `_render_share_section()` uses `st.html()` with JS that references `document.getElementById('share-url-input')` and `document.getElementById('share-copy-icon')`. Streamlit's `st.text_input()` does NOT render elements with these IDs. The copy-to-clipboard button and URL auto-update are non-functional. |
| **Estimated Hours** | 1.0h (range: 0.5-1.5h) |
| **Dependencies** | None |
| **Risk Level** | Medium — the feature is "complete" but non-functional. Users see a share section that doesn't work. |
| **Affected Files** | `_sections_discovery.py` — replace JS-dependent share section with functional implementation |
| **Fix Options** | (a) Pure Streamlit: `st.text_input(disabled=True)` + `st.button("📋 複製")` with `st.toast()` feedback — simplest, no JS; (b) `st.code()` for URL + `st.button()` with `pyperclip` — requires `pyperclip` dependency; (c) `streamlit.components.v1.html()` with self-contained HTML — most robust but most complex |
| **Notes** | Architect's estimate: 1h. Recommend option (a) for simplicity. The share URL can be built with `st.query_params` and displayed in a disabled text input. Copy feedback via `st.toast("✅ 已複製連結")`. This eliminates all JS from the share section. |

**Architecture Debt Subtotal: 3.5h**

---

## 6. Summary Tables

### Grand Totals by Category

| Category | Items | Total Hours | Complexity Range |
|----------|-------|-------------|-----------------|
| **P0 Bugs** | D-043 (P0 NameError) | 0.25h | Critical |
| **Sprint 5 Prerequisites** | D37, D-039, D-040, D-041, D-047 | 5.6h | Low |
| **Sprint 5 Features** | C71, C73, C74 | 42h | Medium–High |
| **Design Debt** | D-042, D-043(design), D-044(design), D-045, D-046(design), D-047(design), D-048 | 5.75h | Low–Medium |
| **Architecture Debt** | D-044(architect), D-046(architect) | 3.5h | Medium |
| **Grand Total** | | **57.1h** | |

### Sprint 5 Recommended Sequence

| Order | Item | Hours | Cumulative | Priority |
|-------|------|-------|------------|----------|
| 1 | D-043 (P0 bug fix) | 0.25h | 0.25h | 🔴 IMMEDIATE |
| 2 | D37 (sections split) | 2.0h | 2.25h | 🟡 FIRST |
| 3 | D-047 fix (`_section_title` bug) | 0.1h | 2.35h | 🟡 FIRST |
| 4 | D-039 (section headers) | 1.5h | 3.85h | 🟡 FIRST |
| 5 | D-040 (disclaimer component) | 0.5h | 4.35h | 🟡 FIRST |
| 6 | D-041 (card components) | 1.5h | 5.85h | 🟡 FIRST |
| 7 | D-046 architect (share JS fix) | 1.0h | 6.85h | 🟡 Quick fix |
| 8 | D-044 architect (market_data.py) | 2.5h | 9.35h | 🟡 Alongside features |
| 9 | C71 (Study Log) | 10h | 19.35h | 🟢 Feature |
| 10 | C73 (Expert Analysis) | 18h | 37.35h | 🟢 Feature |
| 11 | C74 (Historical Scenarios) | 14h | 51.35h | 🟢 Feature |
| 12 | D-042 (mini score cards) | 0.5h | 51.85h | 🟢 Debt cleanup |
| 13 | D-043 design (dividend table) | 1.5h | 53.35h | 🟢 Debt cleanup |
| 14 | D-044 design (read next header) | 0.25h | 53.6h | 🟢 Debt cleanup |
| 15 | D-045 (sector grid HTML) | 1.5h | 55.1h | 🟢 Debt cleanup |
| 16 | D-046 design (4th KPI card) | 0.25h | 55.35h | 🟢 Debt cleanup |
| 17 | D-047 design (share header) | 0.25h | 55.6h | 🟢 Debt cleanup |
| 18 | D-048 (share button standardize) | 1.5h | 57.1h | 🟢 Debt cleanup |

### Comparison with Round 16 Estimates

| Category | R16 Estimate | R17 Estimate | Delta | Reason |
|----------|-------------|-------------|-------|--------|
| Prerequisites | 3.3h | 5.6h | +2.3h | D37 split now 918 lines (was 612); added D-047 bugfix |
| Sprint 5 Features | 40h | 42h | +2h | C73 +1h (module boundary risk), C74 +1h (historical lookup complexity) |
| Design Debt (new) | 3.1h | 5.75h | +2.65h | 4 new issues D-045-D-048; D-048 includes functional fix |
| Architecture Debt | — | 3.5h | +3.5h | New: D-044(architect) + D-046(architect) |
| P0 Bug | — | 0.25h | +0.25h | New: D-043 NameError crash |
| **Total** | **46.4h** | **57.1h** | **+10.7h** | |

---

## 7. Risk Assessment

### Critical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **C73 Expert Analysis data source** | If FinMind doesn't provide analyst consensus, must curate mock data. +4-6h for data sourcing. | Medium | Spike FinMind API first; fall back to curated `expert_consensus.yaml` with disclaimer |
| **D37 split import errors** | 16 section functions imported across `_main.py`. Missed import = runtime crash. +0.5-1h. | Medium | Use IDE refactoring; test each sub-module extraction incrementally |
| **C74 historical data gaps** | FinMind's historical depth varies by stock. Some calculations need graceful degradation. +1-2h. | Medium | Add try/except with fallback messages per scenario |

### Medium Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **D-048 share button fix** | Current JS approach is non-functional. Pure Streamlit alternative may have limited UX. +0.5-1h. | High | Use `st.button()` + `st.toast()` approach; accept simpler UX |
| **C71 study log scope** | If multi-user support is needed later, YAML→SQLite migration adds 4-6h. | Low | Document as single-user limitation |
| **D-044 architect extraction** | Extracting `market_data.py` from working page risks breaking progress bar UX. +0.5h. | Medium | Extract incrementally; test after each function migration |

### Estimation Confidence

| Category | Confidence | Notes |
|----------|------------|-------|
| P0 Bug (D-043) | Very High (±5%) | 2 lines changed, well-understood |
| Prerequisites | High (±10%) | Simple, well-defined helpers; D37 is the largest uncertainty |
| Sprint 5 Features | Medium (±20%) | C73 is the uncertainty — data source unknown |
| Design Debt | High (±10%) | Simple, well-defined fixes |
| Architecture Debt | Medium (±15%) | D-044(architect) extraction scope depends on how much logic is inlined |

---

## 8. Key Files Summary

| File | Current Size | Changes By | Expected After |
|------|-------------|-----------|----------------|
| `src/pages/business_card/_sections.py` | 918 lines | D37 split | Deleted (split into 4 files) |
| `_sections_core.py` (NEW) | — | D37 | ~200 lines |
| `_sections_analysis.py` (NEW) | — | D37, D-042 | ~270 lines |
| `_sections_detail.py` (NEW) | — | D37, D-043 design | ~300 lines |
| `_sections_discovery.py` (NEW) | — | D37, D-044 design, D-047 design, D-048, C71, C74 | ~430 lines |
| `src/pages/business_card/_main.py` | 89 lines | D37 import updates, C71/C73/C74 wiring | ~130 lines |
| `_router_base.py` | 177 lines | D-039, D-040, D-041, D-042, D-047 fix, D-048 | ~260 lines |
| `src/services/market_data.py` (NEW) | — | D-044 architect | ~120 lines |
| `src/services/study_log.py` (NEW) | — | C71 | ~60 lines |
| `src/services/expert_analysis.py` (NEW) | — | C73 | ~200 lines |
| `src/services/scenario_engine.py` (NEW) | — | C74 | ~80 lines |
| `src/pages/sector_heatmap.py` | 444 lines | D-044 architect, D-045, D-046 design | ~280 lines |

---

*Created: 2026-06-12*
*Developer cost estimates for Round 17 review cycle.*
*Next review: Sprint 5 mid-point or Round 18.*
