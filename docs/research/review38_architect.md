## Architecture Debt Review — Round 38

> **Context**: Sprint 17 COMPLETE (C14 + C134 + C07 + D-101). Sprint 18 next (C139 + C141 + C143 + D-097 + Tone QA).
> **Reviewer**: System Architect
> **Scope**: Verify Sprint 17 debt items (D-103–D-106), assess new Sprint 17 debt, architecture health check.
> **Key Metrics**: L0: 118/118 ✅ | L1: 20/20 ✅ | Tests: 72 collected (2 collection errors from `filelock` — D-074 regression persists)

---

### Sprint 17 Debt Verification

| ID | Description | Status | Notes |
|----|-------------|--------|-------|
| D-103 | `delta_explanation_provider.py` untested | ⏳ **STILL PENDING** | 179-line service module created in Sprint 17 (C134). Zero test files reference it. `tests/services/test_delta_engine.py` exists (54 tests for `delta_engine.py`) but does NOT import `delta_explanation_provider`. The `DeltaExplanationProvider` class and `_pick_template()` function are completely untested. |
| D-104 | `settings_service.py` untested | ⏳ **STILL PENDING** | 16-line service module created in Sprint 17 (C07). Zero test files reference it. The `get_threshold()` function is used by `router.py` (line 169–172) but has no unit tests. Trivial module (16 lines) but still should have basic coverage. |
| D-105 | `INDUSTRY_BENCHMARKS` hardcoded in 2 files | ⏳ **STILL PENDING** | Confirmed: identical 30-entry `INDUSTRY_BENCHMARKS` dict exists in both `_health.py` (line 14–43) and `_summary.py` (line 38–67). Both are page files, not service modules. The dict maps industry name → (benchmark_stock_id, benchmark_name). This is hardcoded data in Python (D6 anti-pattern). |
| D-106 | `_fetch_benchmark_health_scores` duplicated | ⚠️ **PARTIALLY ADDRESSED** | `_fetch_benchmark_health_scores()` exists only in `_health.py` (line 46–163). However, `_summary.py` contains equivalent inline benchmark-fetching logic inside `_render_stories_card()` (lines 183–288) — ~100 lines of duplicated financial metric extraction (gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe). The logic is structurally identical but NOT extracted into a shared function. D-106 is partially addressed: the `_health.py` function exists, but `_summary.py` duplicates the logic inline rather than calling it. |

**Sprint 17 Debt Summary**: All 4 pending items (D-103, D-104, D-105, D-106) remain open. D-106 is partially addressed — `_health.py` has the function, but `_summary.py` duplicates the logic inline.

---

### New Debt Items (Sprint 17)

| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-107 | `_summary.py` inline benchmark logic duplicates `_fetch_benchmark_health_scores()` | 🟡 Medium | 1–2h |
| **Description** | `_render_story_card()` in `_summary.py` (lines 183–288) contains ~100 lines of inline benchmark data fetching and metric computation that is structurally identical to `_fetch_benchmark_health_scores()` in `_health.py`. Both functions: (1) look up `INDUSTRY_BENCHMARKS` by industry, (2) fetch benchmark financial data via `client.get_*()`, (3) compute gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe, (4) call `compute_health_scores()`. The logic should be extracted into a shared service function. | | |
| **Impact** | If benchmark logic changes (e.g., new metrics, different thresholds), both locations must be updated in sync. Risk of divergence. | | |
| **Recommended Action** | Extract benchmark health score fetching into a shared service function (e.g., `health_scoring.get_benchmark_scores(client, industry, stock_id)`). Both `_health.py` and `_summary.py` call this function. | | |
| **Priority** | 🟡 Do alongside D-105 (YAML migration of `INDUSTRY_BENCHMARKS`) in Sprint 18 or 19. | | |

| D-108 | `adaptive_engine.py` does NOT import `settings_service` — threshold wiring is incomplete | 🟡 Medium | 0.5h |
| **Description** | Sprint 17 created `settings_service.py` with `get_threshold()`. The `router.py` (line 169–172) imports `get_threshold` and passes thresholds to `run_auto_detection()`. However, `adaptive_engine.py` itself does NOT import `settings_service` — it still uses hardcoded default parameter values (`price_threshold=7.0`, `revenue_threshold=30.0`). The wiring is: `router.py` reads session_state via `get_threshold()` → passes as kwargs to `run_auto_detection()`. This means the settings bridge works via kwargs, but `adaptive_engine.py` has no awareness of `settings_service.py`. If a developer calls `run_auto_detection()` directly (e.g., from a test or another page), the settings are ignored. | | |
| **Impact** | The current kwargs-based wiring works for the router→adaptive_engine path. But the design is fragile: `adaptive_engine.py` should be the authoritative consumer of threshold settings, not the router. | | |
| **Recommended Action** | Add a thin wrapper in `adaptive_engine.py` that calls `settings_service.get_threshold()` as fallback when kwargs are not provided. Or document that `run_auto_detection()` is router-only. | | |
| **Priority** | 🟡 Do in Sprint 18 alongside C139/C141. Not blocking. | | |

| D-109 | `chart_stock.py` grew to 818 lines (was 778 in Round 37) | 🟢 Low | Monitor |
| **Description** | `chart_stock.py` added the `benchmark_scores` / `benchmark_label` parameters to `create_health_snowflake()` (C14). The function now renders a dashed ghost overlay for benchmark comparison. This added ~40 lines to the function. The file is now 818 lines — approaching the 850-line god-module threshold. | | |
| **Impact** | Low. The module is coherent (all single-stock chart rendering). But at 818 lines, finding a specific function requires scrolling. | | |
| **Recommended Action**: Monitor. If Sprint 18 or 19 adds more chart types, split into `chart_stock_financial.py` and `chart_stock_health.py`. | | |
| **Priority** | 🟢 Monitor only. | | |

| D-110 | `_health.py` has 2 `unsafe_allow_html=True` instances (health score cards) | 🟢 Low | 0.5h |
| **Description** | `_health.py` lines 222–232 render health dimension cards with inline HTML (`<div style="text-align:center;padding:0.5rem;background:#F8F9FA;...">`). This is the same card pattern as `_白话_card()` from `_router_base.py`. The 5-dimension score cards could use a shared `render_score_card()` component. | | |
| **Impact** | Low. The inline HTML works and is contained within one function. But it duplicates the card pattern from `_router_base.py`. | | |
| **Recommended Action** | Replace inline HTML with a shared `render_score_card()` component or use `_info_card()` with emoji indicators. | | |
| **Priority** | 🟢 Do alongside D-105 in Sprint 18. | | |

| D-111 | `delta_explanation_provider.py` has dead code — `self._template_provider.is_available()` call on line 169 | 🟢 Low | 0.1h |
| **Description** | Line 169 calls `self._template_provider.is_available()` but discards the return value. The comment says "call it to verify it's available (protocol compliance)" but this is not a meaningful check — `is_available()` always returns `True` for `TemplateExplanationProvider`. This is dead code that adds confusion about the composition pattern. | | |
| **Impact** | Negligible runtime impact. But it's misleading — suggests the template provider might not be available, which is never the case. | | |
| **Recommended Action** | Remove line 169 or replace with a comment explaining the composition relationship. | | |
| **Priority** | 🟢 Quick fix alongside D-103 tests. | | |

---

### Architecture Health

#### Service Layer (`src/services/`)

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Total service modules** | 44 (excl. `__init__.py`, incl. llm/ sub-package) | +2 (`delta_explanation_provider.py`, `settings_service.py`) |
| **Largest service** | `chart_stock.py` — 818 lines | +40 (was 778) |
| **2nd largest** | `adaptive_engine.py` — 622 lines | No change |
| **3rd largest** | `risk_analyzer.py` — 567 lines | No change |
| **Services under 300 lines** | 40 of 44 (91%) | Improved from 90% |
| **Services with zero Streamlit imports** | 43 of 44 (98%) | Maintained — only `quiz_service.py` has Streamlit (pre-existing) |
| **New services since Round 37** | `delta_explanation_provider.py` (179 lines), `settings_service.py` (16 lines) | Both clean, focused modules |

#### Page Layer (`src/pages/`)

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Total page modules** | ~44 (incl. sub-modules) | No change |
| **Largest page** | `_summary.py` — 458 lines | +140 (benchmark overlay in `_render_story_card`) |
| **2nd largest** | `etf_browser.py` — 437 lines | No change |
| **3rd largest** | `peer_comparison.py` — 421 lines | No change |
| **business_card/ sub-modules** | 13+ files across 3 levels | No change |

#### Overall Codebase

| Metric | Value | Change since Round 37 |
|--------|-------|----------------------|
| **Largest file overall** | `chart_stock.py` — 818 lines | +40 (was 778) |
| **God modules (>800 lines)** | 0 ✅ | No change (chart_stock.py at 818 is below threshold) |
| **Modules >600 lines** | 2 (`chart_stock.py` 818, `adaptive_engine.py` 622) | No change |
| **Test count** | 72 collected (2 collection errors) | Regression — D-074 `filelock` error persists |
| **YAML data files** | 13+ | No change |

#### 4-Layer Architecture Assessment

| Layer | Status | Notes |
|-------|--------|-------|
| **Data** (`src/data/`) | ✅ Clean | `finmind_client.py`, `batch_api.py`. YAML data under `src/data/`. |
| **Service** (`src/services/`) | ✅ Clean | 44 modules, 91% under 300 lines. 98% Streamlit-free. New `delta_explanation_provider.py` properly implements `ExplanationProvider` protocol. `settings_service.py` is a clean 16-line accessor. |
| **Page** (`src/pages/`) | ✅ Clean | ~44 modules, largest is 458 lines. `_summary.py` grew 140 lines from benchmark overlay but remains well-structured. |
| **Presentation** (inline) | ⚠️ **STABLE** | `_health.py` has 2 `unsafe_allow_html=True` instances (health score cards). `_summary.py` has 0 (uses `_info_card()`/`_白话_card()`/`_summary_card()`). CI enforcement prevents new instances. |

**Architecture Health Grade**: 🟢 **HEALTHY** — Sprint 17 delivered features without compromising architecture. The LLM abstraction (D5) and delta explanation provider are well-designed. The benchmark overlay adds inline complexity but is contained. Zero god modules. Service layer boundaries are clean.

---

### Sprint 18 Readiness Assessment

Sprint 18 plan: **C139 Explain This Number** + **C141 Source Badge** + **C143 Implication Sentence** + **D-097** + **Tone QA**

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| **D-103** (delta_explanation_provider tests) | 🟡 **NOT STARTED** | Should be done before C139/C143 — both features build on the ExplanationProvider protocol. 1–2h. |
| **D-104** (settings_service tests) | 🟢 **DEFERRABLE** | 16-line module, trivial. Can be done in Sprint 18 but not blocking. |
| **D-105** (INDUSTRY_BENCHMARKS YAML migration) | 🟡 **NOT STARTED** | D-107 depends on this. If D-105 is deferred, D-107 (deduplication) must also defer. Not blocking for Sprint 18 features. |
| **D-107** (benchmark logic deduplication) | 🟡 **NOT STARTED** | Not blocking for Sprint 18. Can be deferred to Sprint 19. |
| **D-108** (adaptive_engine settings wiring) | 🟡 **NOT STARTED** | Not blocking for Sprint 18. C139/C141/C143 don't depend on threshold settings. |
| **D-074** (test filelock regression) | 🔴 **PERSISTENT** | 2 test files still fail at collection time. This has persisted since Round 26. **Must fix before Sprint 18 development.** 0.25h. |
| **D-097** (industry context for C139) | 🟡 **NOT STARTED** | D-097 is a Sprint 18 task itself. It provides industry context that C139 may use. |
| **All L0/L1** | ✅ **PASSING** | L0: 118/118, L1: 20/20 |
| **All tests** | ⚠️ **72 collected, 2 errors** | D-074 filelock regression persists. Fix before Sprint 18. |

**Verdict**: Sprint 18 is **ready with one prerequisite**: fix D-074 (filelock dependency) before feature coding begins. This is a 0.25h fix that restores test collection. D-103 (delta_explanation_provider tests) should also be done early in Sprint 18 since C139 and C143 both build on the ExplanationProvider protocol. D-105/D-107/D-108 are not blocking for Sprint 18.

---

### Top 3 Architecture Recommendations

#### 1. 🔴 Fix D-074: Restore test infrastructure (0.25h) — PREREQUISITE
- **Effort**: 0.25h
- **Why**: 2 test files (`test_adaptive_engine.py`, `test_business_logic.py`) fail at collection time due to missing `filelock` dependency. This regression has persisted since Round 26 (3+ sprints). Without full test coverage, Sprint 18 changes are untested.
- **What**: Add `filelock>=3.0.0` to `pyproject.toml` dependencies, or add a `conftest.py` mock for `filelock.FileLock`.
- **When**: **Day 1 of Sprint 18**, before any feature coding.
- **Risk if deferred**: Service-layer changes in Sprint 18 will be untested. Regression risk increases with each sprint.

#### 2. 🟡 Add tests for `DeltaExplanationProvider` (D-103, 1–2h) — alongside C139/C143
- **Effort**: 1–2h
- **Why**: C139 (Explain This Number) and C143 (Implication Sentence) both build on the `ExplanationProvider` protocol. The `DeltaExplanationProvider` (179 lines) has 3 metric template dicts (_REVENUE_TEMPLATES, _PRICE_TEMPLATES, _YOY_TEMPLATES) × 2 directions × 3 thresholds + generic fallback. Without tests, template changes during C139/C143 could silently break explanations.
- **What**: Add `tests/services/test_delta_explanation_provider.py` with tests for: each metric template (up/down at each threshold), generic fallback for unknown metrics, stock_name prefix handling, edge cases (zero pct, exactly at threshold).
- **When**: **Alongside C139/C143 implementation**, before modifying templates.
- **Risk if deferred**: Template changes during C139/C143 will be untested. Behavior changes in delta explanations could confuse users.

#### 3. 🟡 Extract shared benchmark function (D-107, 1–2h) — alongside D-105
- **Effort**: 1–2h
- **Why**: `_summary.py` has ~100 lines of inline benchmark-fetching logic that duplicates `_fetch_benchmark_health_scores()` from `_health.py`. Both compute identical metrics (gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe) from identical API calls. If benchmark logic changes, both locations must be updated in sync.
- **What**: Extract benchmark health score fetching into a shared service function (e.g., `health_scoring.get_benchmark_scores(client, industry, stock_id)`). Migrate `INDUSTRY_BENCHMARKS` to YAML (D-105). Both `_health.py` and `_summary.py` call the shared function.
- **When**: **Sprint 19**, alongside D-105 YAML migration. Not blocking for Sprint 18.
- **Risk if deferred**: Benchmark logic may diverge between the two locations. New metrics require updates in two places.

---

### Updated Debt Summary

| Category | Count | Change |
|----------|-------|--------|
| **Total Debt Items** | 91 | +5 (D-107 through D-111) |
| **High Severity** | 0 | No change (D5 resolved in Sprint 16b) |
| **Medium Severity** | ~50 | +2 (D-107, D-108) |
| **Low Severity** | ~41 | +3 (D-109, D-110, D-111) |
| **Resolved in Sprint 17** | 1 | D-101 (delta_engine tests — 54 tests added) |
| **Pending Sprint 18** | D-103 (delta_explanation_provider tests), D-074 (filelock fix), D-104 (settings tests) | +3 |
| **Deferred to Sprint 19+** | D-105 (YAML migration), D-106 (benchmark dedup), D-107 (benchmark dedup), D-108 (settings wiring), D-109 (chart size), D-110 (health inline HTML), D-111 (dead code) | +7 |

---

*Created: 2026-06-14 (Round 38)*
*Reviewer: System Architect*
*Next review: Sprint 18 mid-point or Sprint 19 kickoff*
*Architecture Health: 🟢 HEALTHY*
