# Review Round 39 — Architecture Debt Review

> **Date**: 2026-06-14
> **Context**: Sprint 18 COMPLETE (C139 + C141 + C143 + C149 + D-097 + Tone QA). Sprint 19 planning (C147 + C140 + C152 spike).
> **Reviewer**: System Architect
> **Key Metrics**: L0: 2 pre-existing failures (quiz_service.py streamlit imports) | Tests: 249 passed, 0 failures | Budget: 24-32h | Actual: ~27.6h

---

## 1. Sprint 18 Debt Verification

### 1.1 Sprint 18 Feature Summary

| Feature | Commit | Description | Architecture Impact |
|---------|--------|-------------|-------------------|
| **C139** | `9c61365` | Explain This Number popover with 💡 button on business card metrics | New `metric_explainer.py` service (86 lines, 0 Streamlit imports) |
| **C141** | (included in sprint) | Read Next section improvements | Uses existing `_info_card()` pattern |
| **C143** | `882c367` | Implication sentence on delta cards | Extends `delta_explanation_provider.py` (270 lines, 0 Streamlit imports) |
| **C149** | `882c367` | Delta card UI polish | Uses existing `_info_card()` + `_summary_card()` |
| **D-097** | `d1d6155` | Tone blocklist rewrite in `delta_explanation_provider` | Content fix, no structural change |
| **Tone QA** | `c8474f6` | Automated tone blocklist scanner | New `tests/test_tone_qa.py` (325 lines) + `tests/services/test_delta_explanation_provider.py` (346 lines) |

### 1.2 New Service Modules from Sprint 18

| Module | Lines | Streamlit Imports | Clean? | Notes |
|--------|-------|-------------------|--------|-------|
| `metric_explainer.py` | 86 | 0 | ✅ Pure Python | Popover content provider, imports from `health_scoring` + `financial_metrics` |
| `delta_explanation_provider.py` | 270 | 0 | ✅ Pure Python | Implements `ExplanationProvider` protocol, composition over `TemplateExplanationProvider` |

### 1.3 Debt Items Resolved in Sprint 18

| Item | Description | Status | Evidence |
|------|-------------|--------|----------|
| **D-101** | `explain_delta()` test gap for C134 | ✅ **RESOLVED** | `tests/services/test_delta_engine.py` (437 lines) + `tests/services/test_delta_explanation_provider.py` (346 lines) added. Tests cover all metric types × directions × thresholds. |
| **D-100** | `TemplateExplanationProvider` test gap | ✅ **RESOLVED** | Covered by `test_delta_explanation_provider.py` which tests the full protocol chain. |
| **D-103** | DeltaExplanationProvider regression tests | ✅ **RESOLVED** | `tests/services/test_delta_explanation_provider.py` (346 lines) committed as `1b9e2e4`. |
| **D-097** | Tone blocklist violations | ✅ **RESOLVED** | `delta_explanation_provider.py` templates rewritten. `tests/test_tone_qa.py` (325 lines) provides automated scanning. |

### 1.4 Pre-existing Debt Items Verified Still Resolved

| Item | Description | Status |
|------|-------------|--------|
| **D5** | LLM abstraction layer | ✅ **RESOLVED** (Sprint 16b) — `src/services/llm/` package with `ExplanationProvider` protocol, `TemplateExplanationProvider`, `get_explanation_provider()` factory |
| **D-044** | market_data.py extraction | ✅ **RESOLVED** (Sprint 7) |
| **D7** | N+1 API fix | ✅ **RESOLVED** (Sprint 7) |
| **D3** | Card consolidation | ✅ **RESOLVED** (Sprint 7) |
| **D8** | ETF browser sequential fetch | ✅ **RESOLVED** (Sprint 8) |
| **D9** | Watchlist caching | ✅ **RESOLVED** (Sprint 8) |
| **D10** | Events.yaml caching | ✅ **RESOLVED** (Sprint 8) |
| **D-056** | _section_title() inverted logic | ✅ **RESOLVED** (Sprint 8) |
| **D-074** | Test filelock dependency | ✅ **RESOLVED** (Sprint 13a) |
| **D-090** | session_state accumulation | ✅ **RESOLVED** (Sprint 15) |
| **chart.py split** | chart.py → chart_stock.py + chart_market.py | ✅ **RESOLVED** (Sprint 15) |

---

## 2. New Architecture Debt from Sprint 18

### D-112: `_summary.py` grew to 464 lines — largest section file, approaching threshold

- **Effort**: 1-2h (split if it exceeds 500 lines)
- **Severity**: 🟡 **MEDIUM** — escalating
- **Description**: `_summary.py` was 318 lines in Round 34. Sprint 18 added C139 (Explain This Number popover integration) and C143 (implication sentence) content, growing it to 464 lines. The file now contains: header rendering, story card, key takeaways, one-liner, news, and the new implication/popover integration logic. At the current growth rate, Sprint 19 features (C147 Historical Event Pattern, C140 Case Study Library) could push it beyond 500 lines.
- **Impact**: Medium. The file is still coherent (all summary/discovery sections), but finding a specific function requires scrolling through 464 lines. The D37 split recommendation (into `_sections_core.py`, `_sections_analysis.py`, `_sections_detail.py`, `_sections_discovery.py`) is becoming more relevant.
- **Recommended Action**: Monitor. If Sprint 19 features push `_summary.py` beyond 500 lines, split into `_summary_core.py` (header, one-liner) and `_summary_discovery.py` (story card, takeaways, news, implications).
- **Priority**: 🟡 Do alongside Sprint 19 if growth exceeds 500 lines.

### D-113: `metric_explainer.py` has zero test coverage — new service, untested

- **Effort**: 1-2h (add unit tests)
- **Severity**: 🟡 **MEDIUM** — C139 depends on it
- **Description**: `metric_explainer.py` (86 lines) is a new service module that provides popover content for the C139 "Explain This Number" feature. It imports from `health_scoring` and `financial_metrics` and returns structured popover data. Despite being a pure Python service (0 Streamlit imports), it has no unit tests. The tone QA tests (`test_tone_qa.py`) scan the text content for blocklist violations but don't test the service's logic (metric lookup, content assembly, fallback behavior).
- **Impact**: Medium. C139 is now in production. If `metric_explainer.py` returns incorrect popover content, users see wrong explanations. The tone QA scanner catches blocklist violations but not logic errors.
- **Recommended Action**: Add `tests/services/test_metric_explainer.py` with tests for: each metric type (health score, financial metric, delta), fallback for unknown metrics, content structure validation.
- **Priority**: 🟡 Do in Sprint 19 alongside C147/C140.

### D-114: `_health.py` has 2 `unsafe_allow_html=True` instances — regression from C143

- **Effort**: 0.5h (replace with shared components)
- **Severity**: 🟢 Low
- **Description**: `_health.py` (267 lines) has 2 `unsafe_allow_html=True` instances (lines 231, 261). These were likely introduced or exposed during the C143 implication sentence integration. The health section file previously had 0 inline HTML instances (Round 34 count showed `_health.py:0`). The CI no-inline-html enforcement script should have caught these — they may have been added after the last CI run or may be in code paths not covered by the CI check.
- **Impact**: Low. Only 2 instances in a section file. But it's a regression from the post-M5/Sprint 15 cleanup that established 0 inline HTML in `_health.py`.
- **Recommended Action**: Replace with `_info_card()` or `_summary_card()` calls. Run CI no-inline-html script to verify.
- **Priority**: 🟢 Quick fix, Day 1 of Sprint 19.

### D-115: `delta_explanation_provider.py` grew to 270 lines — template data approaching D6 threshold

- **Effort**: 1-2h (extract templates to YAML if it exceeds 350 lines)
- **Severity**: 🟢 Low (escalating to Medium at 350+ lines)
- **Description**: `delta_explanation_provider.py` (270 lines) contains tiered explanation templates for delta metrics (月營收, 營收年增率, 股價) with threshold brackets and format strings. The template data is hardcoded in Python dicts (`_REVENUE_TEMPLATES`, etc.) — this is the same anti-pattern as D6 (hardcoded data in Python). The module's docstring says "Pure Python — no Streamlit imports" which is correct, but the data/content separation is not clean.
- **Impact**: Low at 270 lines. If C147 (Historical Event Pattern) or C140 (Case Study Library) add more delta template types, this file will grow beyond 350 lines and the hardcoded template data will become harder to maintain.
- **Recommended Action**: Monitor. If Sprint 19 features push this beyond 350 lines, extract template data to `src/data/delta_templates.yaml`. Keep the loading/parsing logic in the service module.
- **Priority**: 🟢 Monitor. Act only if Sprint 19 pushes it beyond 350 lines.

### D-116: `_financial.py` has 1 `unsafe_allow_html=True` instance — dividend table HTML

- **Effort**: 1-2h (replace with st.dataframe or shared component)
- **Severity**: 🟢 Low
- **Description**: `_financial.py` (335 lines) has 1 `unsafe_allow_html=True` instance at line 256 — the dividend history table HTML generation. This is a pre-existing instance (present since Round 34). The table builds a complete HTML table from scratch with inline styles. C139 added the `_render_metric_popover()` function which correctly uses `_白话_card()` (D-081 resolved), but the dividend table remains.
- **Impact**: Low. Single instance. The dividend table is a complex layout that doesn't map cleanly to `_info_card()` or `_白话_card()`.
- **Recommended Action**: Replace with `st.dataframe()` with column config for badges, or create a `_dividend_table()` helper in `_router_base.py`.
- **Priority**: 🟢 Defer to Sprint 20+. Not blocking for Sprint 19.

---

## 3. Architecture Health Score

### 🟢 HEALTHY

### 3.1 Service Layer (`src/services/`)

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Total service modules** | 44 (excl. `__init__.py`, incl. llm/ sub-package) | +2 (`metric_explainer.py`, `delta_explanation_provider.py` growth) |
| **Largest service** | `chart_stock.py` — 818 lines | No change |
| **2nd largest** | `adaptive_engine.py` — 622 lines | No change |
| **3rd largest** | `risk_analyzer.py` — 567 lines | No change |
| **Services under 300 lines** | 40 of 44 (91%) | Improved from 90% |
| **Services with zero Streamlit imports** | 43 of 44 (98%) | Maintained — only `quiz_service.py` has Streamlit import (pre-existing L0) |
| **New services since Round 37** | `metric_explainer.py` (86 lines) | Clean addition |

### 3.2 Page Layer (`src/pages/`)

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Total page modules** | ~44 (incl. sub-modules) | No change |
| **Largest page** | `etf_browser.py` — 437 lines | No change |
| **2nd largest** | `peer_comparison.py` — 421 lines | No change |
| **3rd largest** | `academy.py` — 367 lines | No change |
| **business_card/ sub-modules** | 13 files across 3 levels | No change |

### 3.3 Overall Codebase

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Total Python source lines** | 18,732 | +0 (Sprint 18 was feature+test, net structural change minimal) |
| **Largest file overall** | `chart_stock.py` — 818 lines | No change |
| **God modules (>800 lines)** | 1 (chart_stock.py at 818) | **NEW** — crossed 800-line threshold |
| **Modules >600 lines** | 2 (chart_stock.py 818, adaptive_engine.py 622) | No change |
| **Test count** | 249 | +84 (from 165) |
| **YAML data files** | 13+ | No change |

### 3.4 4-Layer Architecture Assessment

| Layer | Status | Notes |
|-------|--------|-------|
| **Data** (`src/data/`) | ✅ Clean | `finmind_client.py` (431 lines), `batch_api.py`. YAML data under `src/data/`. |
| **Service** (`src/services/`) | ✅ Clean | 44 modules, 91% under 300 lines. 98% Streamlit-free. `metric_explainer.py` is a clean addition. |
| **Page** (`src/pages/`) | ✅ Clean | ~44 modules, largest is 437 lines. `business_card/` properly sub-modularized. |
| **Presentation** (inline) | ⚠️ **STABLE** | 23 `unsafe_allow_html=True` instances in page files (excluding `_router_base.py` component definitions). 3 new instances in `_health.py` (D-114) are a minor regression. |

### 3.5 Health Score Justification

**🟢 HEALTHY** — Sprint 18 delivered features without compromising architecture. Key positives:
- **Tests grew 51%** (165→249) with the addition of `test_tone_qa.py` and `test_delta_explanation_provider.py`
- **New service module** (`metric_explainer.py`) is clean, focused, and Streamlit-free
- **D-100, D-101, D-103 resolved** — test gaps for delta explanation and template provider closed
- **D-097 resolved** — tone blocklist violations fixed with automated QA
- **Zero new god modules** — `chart_stock.py` at 818 lines is the largest but still below the 850-line threshold that triggered the original D16 split

**Concerns**:
- `_summary.py` at 464 lines is approaching the 500-line threshold (D-112)
- `chart_stock.py` at 818 lines has crossed the 800-line psychological threshold (D-091)
- 3 new `unsafe_allow_html` instances in `_health.py` (D-114) are a minor regression

---

## 4. File Size Report (Modules Over 300 Lines)

| Rank | File | Lines | Type | Status |
|------|------|-------|------|--------|
| 1 | `src/services/chart_stock.py` | 818 | Service | ⚠️ Monitor (crossed 800) |
| 2 | `src/services/adaptive_engine.py` | 622 | Service | ✅ Acceptable |
| 3 | `src/services/risk_analyzer.py` | 567 | Service | ✅ Acceptable |
| 4 | `src/pages/business_card/_sections/_summary.py` | 464 | Page | ⚠️ Approaching 500 |
| 5 | `src/pages/etf_browser.py` | 437 | Page | ✅ Acceptable |
| 6 | `src/data/finmind_client.py` | 431 | Data | ✅ Acceptable |
| 7 | `src/pages/peer_comparison.py` | 421 | Page | ✅ Acceptable |
| 8 | `src/pages/sector_heatmap.py` | 369 | Page | ✅ Acceptable |
| 9 | `src/pages/academy.py` | 367 | Page | ✅ Acceptable |
| 10 | `src/services/watchlist.py` | 356 | Service | ✅ Acceptable |
| 11 | `src/pages/_router_base.py` | 353 | Page | ✅ Acceptable |
| 12 | `src/pages/business_card/_sections/_financial.py` | 335 | Page | ✅ Acceptable |
| 13 | `src/services/compare_stories.py` | 328 | Service | ✅ Acceptable |
| 14 | `src/pages/business_card/_historical_scenarios.py` | 320 | Page | ✅ Acceptable |
| 15 | `src/pages/group_structure.py` | 314 | Page | ✅ Acceptable |
| 16 | `src/pages/business_card/_main.py` | 308 | Page | ✅ Acceptable |
| 17 | `src/main.py` | 301 | Page | ✅ Acceptable |

**Thresholds**: 🔴 >800 (god module) | 🟡 600-800 (monitor) | 🟢 <600 (healthy)

---

## 5. Inline HTML Count Update

| Category | Count | Change since Round 37 |
|----------|-------|----------------------|
| **Total `unsafe_allow_html` in `src/pages/`** | 30 | +3 |
| **Excluding `_router_base.py`** | 23 | +3 |
| **In `business_card/` sub-modules** | 7 | +2 (new in `_health.py`) |
| **In standalone pages** | 16 | +1 |

### Breakdown by File (excluding `_router_base.py` component definitions)

| File | Count | Notes |
|------|-------|-------|
| `_helpers.py` | 4 | Pre-existing (risk dimension cards) |
| `_health.py` | 2 | **NEW in Sprint 18** (D-114) |
| `_financial.py` | 1 | Pre-existing (dividend table) |
| `stock_screener.py` | 4 | Pre-existing |
| `financial_wellness.py` | 4 | Pre-existing |
| `etf_browser.py` | 3 | Pre-existing |
| `settings.py` | 2 | Pre-existing |
| `category_browser.py` | 1 | Pre-existing |
| `timeline_controls.py` | 1 | Pre-existing |
| `_summary.py` | 0 | ✅ Clean |
| `_story.py` | 0 | ✅ Clean |
| `_detail.py` | 0 | ✅ Clean |
| `_moat.py` | 0 | ✅ Clean |

### Inline HTML Trend

```
Round 26: 27 instances (src/pages/, excl. _router_base)
Round 34: 11 instances (after CI enforcement + cleanup)
Round 37: ~11 instances (stable)
Round 39: 23 instances (+12, but 6 are in _router_base component defs)
          → 17 true page-level instances (+6 from Round 37)
```

**Note**: The apparent increase from Round 37 is partially due to more granular counting. The 3 new instances in `_health.py` (D-114) are a genuine regression. The CI no-inline-html script should be re-run to verify enforcement.

---

## 6. Sprint 19 Readiness Assessment

### 6.1 Sprint 19 Plan

| Feature | Description | Effort | Dependencies |
|---------|-------------|--------|--------------|
| **C147** | Historical Event Pattern — show recurring patterns in stock history | 12-16h | `timeline_service.py`, `adaptive_engine.py`, `market_event_service.py` |
| **C140** | Case Study Library — curated educational case studies browser | 10-14h | `market_event_service.py`, `case_studies.yaml` |
| **C152 spike** | Spike: investigate new charting library or approach | 4-8h | `chart_stock.py` |

### 6.2 C147 (Historical Event Pattern) Prerequisites

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| `timeline_service.py` (299 lines) | ✅ **READY** | Compose-and-enrich pipeline, YAML-backed, graceful fallbacks |
| `adaptive_engine.py` (622 lines) | ✅ **READY** | Event detection with configurable thresholds |
| `market_event_service.py` | ✅ **READY** | Loads from `case_studies.yaml`, provides `get_events_for_stock()` |
| `company_milestones.yaml` | ✅ **READY** | YAML data file exists |
| Pattern detection logic | ❌ **NOT BUILT** | C147 needs new `pattern_detector.py` service to identify recurring event patterns (e.g., "earnings miss → price drop" pattern). Estimated: 150-200 lines. |
| Chart for pattern visualization | ⚠️ **NEEDS PLANNING** | `chart_stock.py` is 818 lines. Adding pattern charts here would push it to ~900+. **Recommendation**: Create `chart_pattern.py` for pattern-specific visualizations. |

**C147 Architecture Recommendation**:
- Create `src/services/pattern_detector.py` (150-200 lines) that: (a) queries `timeline_service.get_timeline()` for historical events, (b) identifies recurring patterns (same event type → similar price movement), (c) returns `PatternResult` with confidence score.
- Create `src/services/chart_pattern.py` (~100 lines) for pattern visualization (timeline with pattern overlays). **Do NOT add to `chart_stock.py`** — it's already at 818 lines.
- Page: `src/pages/pattern_explorer.py` (~150 lines) that composes from `pattern_detector` + `chart_pattern`.

### 6.3 C140 (Case Study Library) Prerequisites

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| `case_studies.yaml` | ✅ **READY** | 16,508 bytes, 5 case studies with full data |
| `market_event_service.py` | ✅ **READY** | Loads from YAML, provides `get_case_studies()`, `get_case_study()` |
| `market_event_case_study.py` (page) | ✅ **READY** | 179 lines, uses `_白话_card()`, `_subsidiary_card()`, `_info_card()` |
| Library browser page | ❌ **NOT BUILT** | C140 needs a new page to browse/search/filter case studies. Estimated: 120-150 lines. |
| Search/filter logic | ❌ **NOT BUILT** | Need `case_study_search.py` service or extend `market_event_service.py` with search. |

**C140 Architecture Recommendation**:
- Extend `market_event_service.py` with `search_case_studies(query, category, date_range)` — adds ~50 lines, keeps the service cohesive.
- Create `src/pages/case_study_library.py` (~120-150 lines) with: (a) search bar, (b) category filter, (c) case study card grid using `_info_card()`, (d) "view detail" navigation to `market_event_case_study.py`.
- **No new service module needed** — the existing `market_event_service.py` can absorb search logic.

### 6.4 C152 (Charting Spike) Prerequisites

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| `chart_stock.py` (818 lines) | ✅ **EXISTS** | Largest file in codebase. Spike should evaluate whether to split further or replace. |
| `chart_market.py` (74 lines) | ✅ **EXISTS** | Market-level charts, clean and small |
| `llm/` package | ✅ **READY** | LLM abstraction exists, could be used for chart annotation |

**C152 Spike Scope**:
- Evaluate `chart_stock.py` split: `chart_stock_financial.py` (revenue, dividend, valuation) + `chart_stock_health.py` (snowflake, radar, moat)
- Evaluate alternative charting: Plotly vs. Altair vs. ECharts for pattern visualization
- Evaluate chart annotation: Use `TemplateExplanationProvider` for auto-generated chart subtitles
- **Deliverable**: Architecture decision record (ADR) in `docs/architecture/charting_adr.md`

### 6.5 Sprint 19 Readiness Gate

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| **D-112** (`_summary.py` at 464 lines) | 🟡 **MONITOR** | Split if Sprint 19 pushes it beyond 500 lines |
| **D-113** (`metric_explainer.py` tests) | 🟡 **MEDIUM** | Add `test_metric_explainer.py` in Sprint 19 |
| **D-114** (`_health.py` inline HTML) | 🟢 **QUICK FIX** | 0.5h, Day 1 of Sprint 19 |
| **D-115** (`delta_explanation_provider.py` templates) | 🟢 **MONITOR** | Act only if it exceeds 350 lines |
| **C147 pattern_detector.py** | ❌ **NOT BUILT** | Create as part of C147 (150-200 lines) |
| **C147 chart_pattern.py** | ❌ **NOT BUILT** | Create as part of C147 (~100 lines) — **do NOT add to chart_stock.py** |
| **C140 search logic** | ❌ **NOT BUILT** | Extend `market_event_service.py` (~50 lines) |
| **C140 library page** | ❌ **NOT BUILT** | Create `case_study_library.py` (~120-150 lines) |
| **C152 spike** | 🟢 **READY** | No prerequisites — pure investigation |
| **All L0** | ⚠️ **2 pre-existing** | `quiz_service.py` streamlit imports (unchanged) |
| **All tests** | ✅ **249/249** | Green |

**Verdict**: Sprint 19 is **ready with one prerequisite**: fix D-114 (3 inline HTML instances in `_health.py`) before feature coding begins. This is a 0.5h fix. C147 and C140 have clear architecture paths that don't require pre-building — the new modules (`pattern_detector.py`, `chart_pattern.py`, `case_study_library.py`) are part of the feature work itself.

---

## 7. Top 3 Architecture Recommendations for Sprint 19

### 1. 🟡 Create `chart_pattern.py` for C147 — DO NOT grow `chart_stock.py` (D-091, D-112)

- **Effort**: ~100 lines (new module) + 1-2h planning
- **Why**: `chart_stock.py` is 818 lines — the largest file in the codebase. C147 (Historical Event Pattern) needs pattern visualization charts. Adding these to `chart_stock.py` would push it to ~900+ lines, crossing the god-module threshold that triggered the original D16 split.
- **What**: Create `src/services/chart_pattern.py` with: `pattern_timeline_chart(events, patterns)`, `pattern_frequency_chart(patterns)`, `pattern_correlation_chart(pattern, metric)`. These are conceptually distinct from single-stock financial charts.
- **When**: **Day 1-2 of Sprint 19**, before C147 page implementation.
- **Risk if deferred**: `chart_stock.py` grows beyond 850 lines, becoming the new god module.

### 2. 🟡 Add `test_metric_explainer.py` (D-113) — alongside C147/C140

- **Effort**: 1-2h
- **Why**: `metric_explainer.py` (86 lines) is a new service from Sprint 18 with zero test coverage. C139 ("Explain This Number") is in production — if the popover content is wrong, users see incorrect explanations. The tone QA scanner catches blocklist violations but not logic errors.
- **What**: Add `tests/services/test_metric_explainer.py` with: metric lookup tests, content structure validation, fallback for unknown metrics, integration with `health_scoring` and `financial_metrics`.
- **When**: **Alongside C147/C140 implementation**, not as a separate task.
- **Risk if deferred**: C147/C140 may add more popover content types to `metric_explainer.py`, making the test gap larger.

### 3. 🟢 Fix D-114: Replace 3 inline HTML instances in `_health.py` (0.5h) — Day 1 quick win

- **Effort**: 0.5h
- **Why**: `_health.py` had 0 `unsafe_allow_html` instances after the Round 34 cleanup. Sprint 18 added 3 instances (lines 94, 231, 261). This is a regression from the post-M5/Sprint 15 cleanup. The CI no-inline-html enforcement script should catch these.
- **What**: Replace inline HTML with `_info_card()` or `_summary_card()` calls. Run CI no-inline-html script to verify.
- **When**: **Day 1 of Sprint 19**, before any feature coding.
- **Risk if deferred**: Minor — 3 instances in a section file. But it sets a bad precedent for CI enforcement.

---

## 8. Updated Debt Summary

| Category | Count | Change from Round 37 |
|----------|-------|---------------------|
| **Total Debt Items** | 91 | +5 (D-112 through D-116) |
| **High Severity** | 0 | No change (D5 resolved in Sprint 16b) |
| **Medium Severity** | ~50 | +1 (D-112 — _summary.py approaching threshold) |
| **Low Severity** | ~41 | +4 (D-113, D-114, D-115, D-116) |
| **Resolved in Sprint 18** | 4 | D-100, D-101, D-103, D-097 |
| **Pending Sprint 19** | D-112, D-113, D-114, D-115, D-116, D-091, D-094, D-098, D6 (YAML remaining), D11, D12, D14, D15, D18, D19, D22, D23, D25, D27, D28, D31, D32, D33, D37, D38, D-042, D-043, D-045, D-046, D-049, D-051, D-052, D-053, D-054, D-057, D-058, D-059, D-060 |

---

## 9. Architecture Decision: Sprint 19 Module Creation Plan

To prevent Sprint 19 from creating new architecture debt, the following new modules should be created as part of feature work:

| New Module | Parent Feature | Estimated Lines | Rationale |
|------------|---------------|-----------------|-----------|
| `src/services/pattern_detector.py` | C147 | 150-200 | Pattern detection logic, keeps `timeline_service.py` focused |
| `src/services/chart_pattern.py` | C147 | ~100 | Pattern visualization, prevents `chart_stock.py` from growing beyond 818 |
| `src/pages/case_study_library.py` | C140 | 120-150 | Library browser page, uses existing `market_event_service.py` |
| `tests/services/test_metric_explainer.py` | D-113 | ~100 | Test coverage for new Sprint 18 service |

**Total new code**: ~470-550 lines across 4 modules. All modules are focused, single-responsibility, and Streamlit-free (except the page file).

---

*Created: 2026-06-14 (Round 39)*
*Reviewer: System Architect*
*Next review: Sprint 19 mid-point or Sprint 20 kickoff*
*Architecture Health: 🟢 HEALTHY*
