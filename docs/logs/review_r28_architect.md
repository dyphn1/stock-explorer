# Round 28 — Architecture Review (2026-06-18)

## Sprint 13a Architecture Assessment

### C33 Glossary

**Files reviewed**: `src/services/glossary_service.py` (73 lines), `src/data/glossary.yaml` (695 lines, 99 terms), `src/pages/_router_base.py:166-187` (`_glossary_tooltip()`)

**Architecture evaluation**: 🟢 **CLEAN** — No architectural debt introduced.

- **Service layer**: `glossary_service.py` is 73 lines, zero Streamlit imports, uses module-level `_cache` for lazy YAML loading, clean public API (`get_glossary_term()`, `get_all_terms()`, `search_terms()`). Follows the established pattern of `company_facts.py` and `dividend_analyzer.py`. Service count increases from 29 → 30 — all 30 remain 100% Streamlit-free.
- **Data layer**: `glossary.yaml` uses the established YAML schema pattern (`company_facts.yaml`, `case_studies.yaml`). Each term has `name`, `plain`, `example`, `analogy`, `category`. 99 terms across 24 categories. Well-structured.
- **Presentation layer**: `_glossary_tooltip()` added to `_router_base.py:166-187`. This is architecturally appropriate — `_router_base.py` is the page-layer shared component module (8 card/utility functions). The function uses `st.popover()` and `st.markdown()` — it belongs in the presentation layer, not the service layer. It injects `glossary_service` as a parameter (dependency injection), keeping the service reference clean. **Minor note**: this is the first `_router_base.py` component that takes a service module as a parameter. The pattern is acceptable (avoids circular imports) but worth monitoring if more service-aware components are added.
- **Integration**: 6 glossary tooltips integrated into `_financial.py` key metrics (本益比, 毛利率, 營收年增率, ROE, 殖利率, 淨值比). Each call is `_glossary_tooltip("term_key", glossary_service)` — minimal footprint, co-located with the metric it explains.
- **Risk assessment**: None. This is the cleanest feature addition since `feedback_service.py` in Sprint 12.

### C48 Story Card

**Files reviewed**: `src/pages/business_card/_sections/_summary.py:38-146` (`_render_story_card()`)

**Architecture evaluation**: 🟢 **CLEAN** — D-070 (expander wrapper) properly resolved; D-068 (inline HTML health indicator) confirmed fixed.

- **Expander removal**: Confirmed — zero `st.expander` references in `_render_story_card()`. The function builds output using shared components only: `_info_card()`, `_白话_card()`, `_summary_card()` (all from `_router_base.py:88-146`).
- **Component story card uses** (all from `_router_base.py`):
  - `_info_card("一句話定位", one_liner, "💡")` — line 131
  - `_白话_card(label, value, analogy)` — line 138 (×3 in columns)
  - `_summary_card("整體健康度", ...)` — line 142
  - `_info_card("你知道嗎？", fact_text, "🤔")` — line 146
- **No inline HTML**: `unsafe_allow_html` count in `_summary.py` = 0. The Sprint 13a fix replaced the inline HTML `<div>` for health scores with `_summary_card()` (D-068 fix confirmed).
- **Above-fold placement**: Story card renders directly on the page — supports the 10-second test principle established in Sprint 12's Info Hierarchy reorganization.
- **Risk assessment**: None. The story card is now a model example of component-based page construction.

---

## New Debt Identified

### D-077: `_glossary_tooltip()` passes service module as parameter — first service-aware presentation component

- **Severity**: 🟢 **Low**
- **Description**: `_router_base.py:166` — `_glossary_tooltip(term_key, glossary_service)` is the first presentation-layer component in `_router_base.py` that takes a service module as a parameter. The other 7 functions (`_section_title`, `_白话_card`, `_summary_card`, `_info_card`, `_subsidiary_card`, `_count_label`, `get_stock_data`, `filter_by_timeline`) are purely presentational. Introducing service-awareness into `_router_base.py` creates a minor architectural inconsistency.
- **Impact**: Low. The dependency injection pattern avoids circular imports (which would occur if `_router_base.py` imported `glossary_service` directly). The pragmatic benefit outweighs the purity concern.
- **Recommended Action**: **Keep as-is** for now. If a 3rd or 4th service-aware tooltip component is added to `_router_base.py`, extract them into a separate `src/pages/_tooltips.py` module. Document this boundary: `_router_base.py` = pure presentation helpers; `src/pages/_tooltips.py` = service-aware tooltip components.
- **Effort**: 0.5h (if/when needed)
- **Priority**: 🟢 Defer until additional tooltip components are needed.

### D-078: `_render_metric_popover()` now has dual tooltip sources (metric education + glossary) — pattern deserves review

- **Severity**: 🟢 **Low**
- **Description**: `_financial.py:22-55` — `_render_metric_popover()` renders its own inline HTML card (D-073, 8 lines of CSS), AND is now preceded by `_glossary_tooltip()` calls in each metric column (6 invocations in `_render_key_metrics`). The popover card uses `unsafe_allow_html` with hardcoded `#F8F9FA`/`#3498DB` (identical to `_白话_card()` from `_router_base.py:88-95`). The function also uses `st.session_state` for expander toggle — a state-management pattern not used elsewhere in page components.
- **Impact**: Low. Works correctly, but the metric card rendering is a candidate for the D-073 refactor (`_白话_card()` replacement). The dual tooltip situation (glossary ℹ️ + education ❓) is a UX concern, not an architectural one.
- **Recommended Action**: Refactor via existing D-073 (replace inline HTML with `_白话_card()`). No new debt action needed — fold into D-073.
- **Effort**: 0.5h (same as D-073)
- **Priority**: 🟢 Fix alongside D-073.

---

## Architecture Health Metrics

### Service Layer (`src/services/`)

| Metric | Value | Change since Round 26 |
|--------|-------|----------------------|
| **Total service modules** | 30 (excl. `__init__.py`) | +1 (`glossary_service.py`) |
| **Largest service** | `chart.py` — 787 lines | No change |
| **2nd largest** | `adaptive_engine.py` — 622 lines | No change |
| **3rd largest** | `risk_analyzer.py` — 567 lines | No change |
| **Services under 300 lines** | 27 of 30 (90%) | Maintained |
| **Services with zero Streamlit imports** | 30 of 30 (100%) | ✅ Maintained |
| **New services in Sprint 13a** | `glossary_service.py` (73 lines) | Clean addition |
| **Total service functions** | 190 | +4 (`_load_data`, `get_glossary_term`, `get_all_terms`, `search_terms`) |

### Page Layer (`src/pages/`)

| Metric | Value | Change since Round 26 |
|--------|-------|----------------------|
| **Total page modules** | 37 | +0 (no new page files) |
| **Largest page** | `etf_browser.py` — 437 lines | No change |
| **`unsafe_allow_html` instances** | 26 (down from 27) | -1 (D-068 fix removed one instance from `_summary.py`) |
| **Expander-free story card** | ✅ | D-070 resolved |
| **`_router_base.py` functions** | 9 (was 8) | +1 (`_glossary_tooltip`) |

### Overall Codebase

| Metric | Value | Change since Round 26 |
|--------|-------|----------------------|
| **Largest file overall** | `chart.py` — 787 lines | No change |
| **God modules (>800 lines)** | 0 ✅ | No change |
| **Modules >600 lines** | 2 (`chart.py`, `adaptive_engine.py`) | No change |
| **YAML data/config files** | 8 | +1 (`glossary.yaml`) |
| **YAML total entries** | ~200+ | +99 (`glossary.yaml`) |
| **L0 checks** | 101/101 ✅ | +1 (glossary-related check added) |
| **L1 checks** | 20/20 ✅ | No change |
| **Tests** | 149/149 ✅ | D-074 resolved (filelock fix confirmed in handoff) |
| **Design grade** | A (17th consecutive) | Maintained |

### 4-Layer Architecture Assessment

| Layer | Status | Notes |
|-------|--------|-------|
| **Data** (`src/data/`) | ✅ Clean | `glossary.yaml` follows established schema pattern. 8 YAML files total. |
| **Service** (`src/services/`) | ✅ Clean | 30 modules, 90% under 300 lines, 100% Streamlit-free. `glossary_service.py` sets a good example of a small, focused service. |
| **Page** (`src/pages/`) | ✅ Clean | 37 modules. `_summary.py` now fully uses shared components (zero inline HTML in story card). `_glossary_tooltip` in `_router_base.py` is a reasonable placement. |
| **Presentation** (inline) | ⚠️ STABLE | 26 `unsafe_allow_html` instances (down from 27). `_render_metric_popover()` remains the most notable inline HTML offender (D-073). `_helpers.py` card components (4 instances) still duplicate `_router_base.py` card patterns (D-069). |

**Architecture Health Grade**: 🟢 **HEALTHY** — Sprint 13a delivered two features without compromising architecture. The service layer grew cleanly. The page layer improved (story card fully component-based, one fewer `unsafe_allow_html` instance). Two new low-severity items identified (D-077, D-078) but both are deferrable.

---

## Sprint 13b Readiness

### C36 Revenue Tree

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| **Service: `revenue_analyzer.py`** | ✅ EXISTS | 4 public functions already available (`analyze_revenue_breakdown`, `_parse_financial_for_segments`, `_auto_describe_segment`, `_create_generic_breakdown`). Already used by `revenue_tree.py:37`. |
| **Page: `revenue_tree.py`** | ✅ EXISTS (73 lines) | Standalone page already created (Sprint 12 Info Hierarchy relocation). Already uses `_section_title`, `_info_card`, `_白话_card` from `_router_base.py`. |
| **Chart service** | ✅ EXISTS | `chart.py:create_revenue_pie_chart()` already used at `revenue_tree.py:43`. |
| **Analogy engine** | ✅ EXISTS | `get_revenue_analogy()`, `get_yoy_analogy()` already imported at `revenue_tree.py:12`. |
| **Glossary integration** | 🟡 **MISSING** | No glossary tooltips in `revenue_tree.py` yet. Can be added using `_glossary_tooltip()` (e.g., for "營收年增率", "營業收入"). |
| **D-072** (delta inline HTML) | 🟢 **DEFERRABLE** | Not blocking C36. `_render_deltas()` delta HTML is in `_story.py`, not C36. |
| **D-073** (popover card HTML) | 🟢 **DEFERRABLE** | `_render_metric_popover()` is in `_financial.py`, not directly in `revenue_tree.py`. |

**C36 Readiness Verdict**: 🟢 **READY** — `revenue_tree.py` is already implemented as a 73-line standalone page with all required services wired in. Sprint 13b work is primarily **content/polish**: expanding `revenue_analyzer.py` data coverage, adding glossary tooltips, and potentially enhancing the chart. The architecture is already in place.

### C46 Moat Analysis

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| **Service: `moat_analyzer.py`** | ❌ **DOES NOT EXIST** | Must be created from scratch for Sprint 13b. |
| **Page: `moat_analysis.py`** | ❌ **DOES NOT EXIST** | Must be created from scratch for Sprint 13b. |
| **Foundation services** | ✅ AVAILABLE | `risk_analyzer.py` (567 lines, 11 functions including `assess_risk()`, `assess_financial_health()`) provides risk dimension analysis that can inform moat assessment. `analogy_engine.py` provides analogy generation for moat strength descriptions. |
| **Data layer** | 🟡 **TBD** | May need `moat.yaml` for moat factor definitions (brand, network effects, switching costs, cost advantages, etc.), following the `glossary.yaml` schema pattern. |
| **Scoring model** | 🟡 **TBD** | Need to define: what 5-7 moat dimensions to assess, scoring rubric (0-100 per dimension), data sources per dimension. |
| **Component reuse** | ✅ AVAILABLE | `_info_card()`, `_白话_card()`, `_summary_card()`, `_glossary_tooltip()`, `_historian_disclaimer()` all available for page construction. |

**C46 Readiness Verdict**: 🟡 **CONDITIONALLY READY** — No existing moat code exists. Both the service module and page module must be created from scratch. However:
1. The architecture is well-prepared: `risk_analyzer.py` and `analogy_engine.py` provide reusable foundations.
2. The component library (`_router_base.py`) provides all needed UI building blocks.
3. The pattern is proven: `glossary_service.py` (Sprint 13a) + `revenue_tree.py` (Sprint 12) provide a complete reference for "new service + new page" creation.

**Recommended pre-work** (2-3h, before Sprint 13b Day 1):
- Define moat analysis data model: 5 dimensions (brand, network effects, switching costs, cost advantages, intangible assets), scoring scale, data sources.
- Design `moat.yaml` schema following `glossary.yaml` pattern.
- Scaffold `moat_analyzer.py` with `assess_moat(data: dict) -> dict` entry point.

---

## Top 3 Recommendations

#### 1. 🟢 Pre-scaffold C46 Moat Analysis before Sprint 13b coding begins (2-3h)
- **Effort**: 2-3h (data model design + scaffold)
- **Why**: C46 has zero existing code (no service, no page, no data file). Unlike C36 (which already has 73 lines of page + service), C46 requires ground-up creation. Defining the data model and scoring rubric upfront prevents ad-hoc structures.
- **What**: (a) Define `moat.yaml` schema (dimensions, weights, scoring criteria), (b) scaffold `moat_analyzer.py` with `assess_moat()` and 5 dimension assessors, (c) scaffold `moat_analysis.py` page using `_router_base.py` components.
- **When**: **Before Sprint 13b Day 1** development begins.
- **Risk if deferred**: Moat dimensions may be hardcoded in Python (violating D6), scoring may be inconsistent, or the feature may require significant rework.

#### 2. 🟢 Add glossary tooltips to `revenue_tree.py` (0.5h) — C36 polish
- **Effort**: 0.5h
- **Why**: C36 already has the page and service infrastructure. Adding 2-3 glossary tooltips (營收年增率, 營業收入, 自由現金流 if applicable) brings it in line with the tooltip pattern established in `_financial.py`. This is a quick win.
- **What**: Import `_glossary_tooltip` and `glossary_service` in `revenue_tree.py`. Add `_glossary_tooltip()` calls for revenue-related terms.
- **When**: **C36 content/polish day** in Sprint 13b.
- **Risk if deferred**: Inconsistent tooltip coverage between pages.

#### 3. 🟢 Monitor `_router_base.py` service-aware component count (ongoing)
- **Effort**: N/A (monitor)
- **Why**: `_glossary_tooltip()` is the first service-aware component in `_router_base.py` (D-077). If C36/C46/C47 add more service-aware tooltips or badges to `_router_base.py`, the module becomes a mixed-concern file. Set a threshold: if 3+ service-aware components are added, extract them to `src/pages/_tooltips.py`.
- **What**: Track service-aware component count in future architecture reviews.
- **When**: **Round 29+** — raised as awareness item, no immediate action.
- **Risk if deferred**: Minor — `_router_base.py` is 250 lines and can accommodate several more functions without becoming a god module.

---

## Verdict

🟢 **HEALTHY — Sprint 13a passed with flying colors.** No architectural debt was introduced by C33 Glossary or C48 Story Card. The service layer grew cleanly (30 modules, 100% Streamlit-free), the page layer improved (story card fully component-based), and D-068/D-070 design debt was properly resolved. Architecture health metrics are all green.

**Sprint 13b readiness**: C36 Revenue Tree is architecturally ready (all infrastructure exists). C46 Moat Analysis needs ground-up creation but the service layer foundations (`risk_analyzer.py`, `analogy_engine.py`) and component library (`_router_base.py`) are well-prepared. The key pre-work is data model design for moat scoring.

**Two new debt items** (D-077, D-078) are both 🟢 Low severity and deferrable. The existing backlog (D-072, D-073, D-076, D5, D6) remains unchanged — none are blocking Sprint 13b.

**Key metric**: 30 services, 0 god modules, 100% Streamlit-free, 101/101 L0, 20/20 L1, 149/149 tests, 🟢 HEALTHY.

---

*Section added: 2026-06-18 (Round 28)*
*Reviewer: System Architecture*
*Next review: Sprint 13b mid-point or Sprint 14 kickoff*
*Architecture Health: 🟢 HEALTHY*
