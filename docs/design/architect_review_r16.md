# Architecture Review — Round 16

> **Date**: 2026-06-20
> **Reviewer**: System Architect
> **Scope**: Sprint 3 → Sprint 4 transition — D16 resolution verification, new debt from Sprint 3 features, Sprint 4 readiness, Sprint 5 risk assessment
> **Previous Review**: Round 15 (2026-06-19)

---

## 1. Executive Summary

**D16 (analogy_engine.py god module) is RESOLVED** — commit `f128fb0` split the 850-line monolith into 4 focused modules totaling 858 lines. This was the critical path item blocking C48 and the highest-priority architecture debt. The split is clean: `analogy_engine.py` (193 lines, analogy functions only), `key_takeaways.py` (232 lines), `delta_engine.py` (164 lines), `health_scoring.py` (269 lines).

**D24 (business_card.py sub-directory) remains RESOLVED** — 4 files totaling 795 lines.

**Both D16 and D24 were completed in the same commit** (`f128fb0`), along with a partial D-003 fix (replacing C41's inline peer card HTML with `_info_card()`). This is a significant architecture milestone.

**Sprint 4 is ready to begin feature development.** No hard blockers remain. C38, C48, C51, C53-1, and R3 are all unblocked.

**One new_medium-severity item identified**: D39 (`_sections.py` import coupling — `_main.py` and `_sections.py` have duplicate import headers that must be kept in sync).

---

## 2. Sprint 3 Completion Assessment

### ✅ Completed Sprint 3 Items

| Item | Status | Commit | Notes |
|------|--------|--------|-------|
| **C44** (Risk Analysis MVP) | ✅ Complete | `567239b` | 3 risk dimensions (customer concentration, financial health, event-based) via `st.expander` progressive disclosure. `risk_analyzer.py` is 567 lines, well-structured. |
| **C41** (Read Next) | ✅ Complete | `1f98d73` | Peer stock recommendations section. Inline HTML cards replaced with `_info_card()` in `f12c103`. |
| **D24** (business_card.py extraction) | ✅ Complete | `e12c103` | 561-line monolith → 4 files. |
| **D16** (analogy_engine.py split) | ✅ Complete | `f128fb0` | 850-line god module → 4 focused modules. |
| **D-034** (C3 metric values) | ✅ Complete | `4de8b8e` | Snowflake hover shows raw metric values. Dimension cards display values in blue text. |
| **D-004** (Design system doc) | ✅ Complete | `0af5383` | `docs/design/design_system.md` now exists at expected path. |
| **D-024** (info_card background) | ✅ Complete | `c46ec8e` | Changed from `#FFF8F0` to `#F8F9FA`. |

### ⏳ Still Pending from Sprint 3 Plan

| Item | Status | Notes |
|------|--------|-------|
| **C38** (Compare Stories Phase 1) | ⏳ Moved to Sprint 4 | Deferred from Sprint 3. Now unblocked (D16 complete). 10-12h effort. |
| **D-025** (C39 empty state) | ✅ Completed | Already resolved in earlier commit. |

### Sprint 3 Grade: A

All planned Sprint 3 architecture debt items are resolved. C38 was deferred but is now unblocked. The Sprint 3 feature set (C44, C41) is complete and well-architected.

---

## 3. Codebase Growth Summary

| Metric | R14 | R15 | R16 | Δ R15→R16 |
|--------|-----|-----|-----|-----------|
| Total .py files | 32 | 36 | **39** | **+3** |
| Total app LOC | ~8,572 | ~8,969 | **~8,709** | **−260** |
| `analogy_engine.py` | 850 | 850 | **193** | **−657** (split) |
| `key_takeaways.py` | — | — | **232** | new |
| `delta_engine.py` | — | — | **164** | new |
| `health_scoring.py` | — | — | **269** | new |
| `business_card/_sections.py` | — | 612 | **604** | −8 (D-003 fix removed inline HTML) |
| `business_card/_main.py` | — | 84 | **83** | −1 |
| `risk_analyzer.py` | 567 | 567 | **567** | 0 |
| `chart.py` | 787 | 787 | **787** | 0 |
| L0 (Import) | 56/56 | 59/59 | **59/59 ✅** | stable |
| L1 (Render) | 18/18 | 18/18 | **18/18 ✅** | stable |

**Key insight**: Despite adding 3 new files, total LOC *decreased* by 260 lines. This is because the D16 split eliminated duplicated function bodies, and the D-003 fix in `f128fb0` replaced verbose inline HTML with compact `_info_card()` calls. The codebase is both larger in file count and smaller in total lines — a clear structural improvement.

---

## 4. Sprint 4 Readiness

### Prerequisites (All Clear ✅)

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| ~~D24~~ | ✅ Complete | `e12c103` |
| ~~D16~~ | ✅ Complete | `f128fb0` |
| **R3** (Batch API minimal) | 📋 Ready to implement | 1-2h, no dependencies |

### Sprint 4 Feature Readiness

| Feature | Effort | Dependencies | Arch Risk | Verdict |
|---------|--------|-------------|-----------|---------|
| **R3** (Batch API minimal) | 1-2h | None | Low — isolated utility | ✅ Start immediately |
| **C38** (Compare Stories P1) | 10-12h | None (now unblocked) | Medium — narrative comparison is new pattern | ✅ Start after or parallel with R3 |
| **C51** (Sector Heatmap) | 12-16h | R3 + needs `market_data.py` (D25) | Medium — needs new service module | ✅ Start after R3 |
| **C48** (Company Story Card) | 10-14h | None (D16 + D24 complete) | Medium — `story_composer.py` is new | ✅ Start immediately |
| **C53-1** (Social Sharing URL) | 2-3h | None | Low — isolated feature | ✅ Quick win |

**Recommended Sprint 4 sequence:**
1. **R3** (1-2h) + **C48** start (10-14h) — parallel tracks
2. **C38** (10-12h) — after R3 or parallel
3. **C51** (12-16h) — with `market_data.py` (D25) as sub-task
4. **C53-1** (2-3h) — quick win at end

**Critical path**: R3 → C51. C48 is independent and can proceed in parallel.

### Total estimated effort: 35-47h (excluding D-items below)

### Sprint 4 Architecture Debt Items to Address Alongside Features

| Item | Effort | When | Notes |
|------|--------|------|-------|
| **D25** (`market_data.py`) | 1-2h | As part of C51 | Do not ad-hoc market data flow |
| **D23** (Tone guidelines for market data) | 1h | Before C51 ships | Content task, not code |
| **D37** (`_sections.py` split) | 1-2h | Alongside C38 + C48 | Prevents re-emerging monolith |
| **D-041** (C71/C73/C74 card components) | 1h | Before Sprint 5 | Prevents D-003 regression |
| **D-039** (Section header pattern) | 1-2h | Before Sprint 5 | Standardizes section headers |
| **D-040** (Disclaimer component) | 0.5h | Before Sprint 5 | Regulatory compliance |
| **D-037** (`_白话_card` background) | <0.5h | Anytime | One-line fix: `#F5F5F5` → `#F8F9FA` |
| **D-038** (C41 API in view layer) | 1-2h | Low priority | Move peer fetching to router |

---

## 5. New Architecture Debt Identified

### D39: Duplicate import headers in `_main.py` and `_sections.py` (NEW)

- **Severity**: 🟡 Medium
- **Description**: `_main.py` (lines 1-34) and `_sections.py` (lines 1-40) have nearly identical import blocks — both import from `analogy_engine`, `key_takeaways`, `delta_engine`, `health_scoring`, `risk_analyzer`, `dividend_analyzer`, `news_summarizer`, `company_facts`, `watchlist`, and `_router_base`. When a new service is added, both files must be updated in sync.
- **Impact**: Maintenance burden. Risk of one file getting out of sync with the other.
- **Recommended Action**: Create `src/pages/business_card/_imports.py` with shared imports, or move all imports to `_main.py` and have `_sections.py` import from `_main.py` for its dependencies. Alternatively, accept this as a reasonable trade-off since both files are in the same sub-directory and the imports are stable.

### D-037: `_白话_card` background color still wrong

- **Severity**: 🟢 Low (one-line fix)
- **Status**: ⚠️ Still pending despite D-024 fix. D-024 fixed `_info_card()` but `_白话_card()` at `_router_base.py:91` still uses `background:#F5F5F5` instead of the design system's `#F8F9FA`.
- **Effort**: <0.5h (one-line change)
- **Recommended Action**: Change `background:#F5F5F5` to `background:#F8F9FA` in `_router_base.py:91`.

### D-038: C41 API call in view layer (architecturally, now in `_sections.py`)

- **Severity**: 🟢 Low
- **Description**: `_render_read_next()` in `_sections.py` (line ~542-560) still calls `client.get_stock_info()` directly in the view layer. This was identified as D-038/D33. The D24 extraction moved it from `business_card.py` to `_sections.py` but didn't fix the architectural issue.
- **Impact**: Low — FinMindClient caches responses.
- **Recommended Action**: Pre-compute peer data in `_router_base.py`'s `get_stock_data()` and pass via `data` dict.

---

## 6. Refactoring Recommendations (with priority and effort)

### 1. 🔴 D16 — RESOLVED ✅ (was critical path)

**Status**: Complete at `f128fb0`. The 850-line `analogy_engine.py` has been split into:
- `analogy_engine.py` (193 lines) — 10 analogy functions (`get_revenue_analogy`, `get_gross_margin_analogy`, etc.) + `get_one_liner()` with `one_liners` dict (20 stocks) and `industry_templates` (10 industries)
- `key_takeaways.py` (232 lines) — `_KEY_TAKEAWAYS` dict (20 stocks, ~120 lines of data) + `generate_key_takeaways()` (~100 lines)
- `delta_engine.py` (164 lines) — `compute_recent_deltas()` + `explain_delta()`
- `health_scoring.py` (269 lines) — 6 `_score_*` functions + `compute_health_scores()` + `get_health_summary()`

**Remaining concern**: `key_takeaways.py` still has hardcoded data (D18/D6). The `_KEY_TAKEAWAYS` dict (120 lines) should be migrated to `src/data/key_takeaways.yaml` when capacity allows. `analogy_engine.py` also has `one_liners` and `industry_templates` dicts that should be YAML-migrated (D6).

### 2. 🟡 D37 — Plan `_sections.py` split alongside C38/C44

**Priority**: Do alongside C38 + C48 implementation, not as a separate task.
**Effort**: 1-2h

**Recommended split** (when C38 and C48 are added):
```
src/pages/business_card/
  _main.py              (83 lines — orchestrator, stable)
  _helpers.py           (95 lines — shared helpers, stable)
  _sections_core.py     (~150 lines) — header, one-liner, key metrics, footer
  _sections_analysis.py (~200 lines) — takeaways, deltas, health, risk
  _sections_detail.py   (~250 lines) — dividend, revenue breakdown, revenue trend, valuation, news
  _sections_discovery.py (~100 lines) — read next, compare stories, story card
```

**Trigger for split**: When `_sections.py` exceeds 650 lines (currently 604). C38 and C48 will push it to ~730+.

### 3. 🟡 D-041 — Create Sprint 5 card components BEFORE feature implementation

**Priority**: 🔴 **Sprint 5 PREREQUISITE** — must complete before any C71/C73/C74 implementation.
**Effort**: 1h

**Action**: Before Sprint 5 coding starts, create shared card components in `_router_base.py` or a new `ui_components.py`:
- `_study_card()` — for C71 Study Log entries
- `_expert_card()` — for C73 Expert Analysis synthesis
- `_scenario_card()` — for C74 Historical Scenarios

**Rationale**: The designer's own worst-case forecast is "A- — D-003 not addressed; C71/C73/C74 add more inline HTML; card inconsistency worsens." Each Sprint 5 feature will add ~50-70 lines. If each uses inline HTML, D-003 becomes exponentially harder to fix.

### 4. 🟡 D-039 + D-040 — Standardize section headers and disclaimers

**Priority**: Before Sprint 5
**Effort**: 1.5-2.5h combined

**D-039 Action**: Create `_section_header(icon: str, title: str, collapsed: bool = False)` helper:
```python
def _section_header(icon: str, title: str, collapsed: bool = False):
    if collapsed:
        return st.expander(f"{icon} {title}", expanded=False)
    else:
        st.markdown(f"### {icon} {title}")
```
Currently, sections use 7 different `st.markdown(f"### ...")` calls with inconsistent icon placement (see `_sections.py` lines 208, 300, 455, 478, 496, 525, 549). This doesn't matter yet, but when C71/C73/C74 add 3+ more sections, inconsistency will be visible.

**D-040 Action**: Create `_historian_disclaimer(type: str)` returning standardized text. Types: `'expert'`, `'scenario'`, `'general'`. Use `st.caption()` for rendering. This is a regulatory compliance item — inconsistent disclaimer text across C73/C74 could create risk.

### 5. 🟢 D6 — Hardcoded data migration to YAML (ongoing)

**Priority**: Low — do when capacity allows during Sprint 4-5
**Effort**: 3-4h total

**Files with hardcoded data remaining**:
| File | Data | Lines |
|------|------|-------|
| `analogy_engine.py` | `one_liners` (20 stocks), `industry_templates` (10) | ~40 lines |
| `key_takeaways.py` | `_KEY_TAKEAWAYS` (20 stocks) | ~120 lines |
| `revenue_analyzer.py` | `KNOWN_COMPANY_REVENUE` (8 stocks) | ~50 lines |
| `group_structure.py` | `KNOWN_GROUP_STRUCTURES` (5 groups) | ~160 lines |
| `peer_comparison.py` | `INDUSTRY_BENCHMARKS` (22 entries) | ~40 lines |

**Note**: This debt is partially addressed by the D16 split — at least the data is now in the correct module. YAML migration is "make it nice" not "fix a bug."

### 6. 🟢 D31 — Monitor `risk_analyzer.py` growth

**Status**: Monitoring. At 567 lines, it's approaching the threshold where `analogy_engine.py` became a god module (850 lines). Currently well-structured with clean orchestration pattern.

**Risk from Sprint 5**: C73 (Expert Analysis) may add functions to `risk_analyzer.py`. If it does, consider creating a separate `expert_analysis.py` module.

**Trigger for split**: If `risk_analyzer.py` exceeds 700 lines after any Sprint 5 additions.

---

## 7. Sprint 5 Risk Assessment

### Planned Sprint 5 Features (from design reviews)

| Feature | Effort | Architecture Risk | Notes |
|---------|--------|------------------|-------|
| **C71** (Study Log) | 8-12h | 🟡 Medium | Adds new section to business card. Needs `_study_card()` component (D-041). Needs persistence (YAML or D22). |
| **C73** (Expert Analysis 10 stocks) | 14-20h | 🔴 High | Most complex Sprint 5 feature. May need new service module. Requires disclaimer component (D-040). May overlap with `risk_analyzer.py` — risk of scope creep into that module. |
| **C74** (Historical Scenarios) | 10-16h | 🟡 Medium | Needs `src/data/historical_scenarios.yaml`. Requires disclaimer component (D-040). Selectbox-only interaction (no free-form inputs) to maintain historian positioning. |

### Key Risks

#### 🔴 Risk 1: C73 Expert Analysis scope creep into risk_analyzer.py

C73 may naturally extend `risk_analyzer.py` with "expert consensus" risk assessment. If 3-4 new functions are added to `risk_analyzer.py`, it will cross 700 lines and need splitting. **Mitigation**: Create `expert_analysis.py` as a separate module. Keep `risk_analyzer.py` focused on the 3 existing risk dimensions.

#### 🔴 Risk 2: D-003 regression — Sprint 5 features add inline HTML

Without D-041 (card components created BEFORE implementation), each Sprint 5 feature will likely add inline HTML cards, worsening D-003. The designer explicitly forecasts this as the worst-case scenario. **Mitigation**: D-041 is a Sprint 5 prerequisite. Create `_study_card()`, `_expert_card()`, `_scenario_card()` before any Sprint 5 coding.

#### 🟡 Risk 3: `_sections.py` exceeding 700 lines

Currently 604 lines. C71 + C73 + C74 will each add a section function (~50-70 lines), pushing it to ~800+ lines. **Mitigation**: Apply D37 split (into 4 section sub-modules) when implementing the first Sprint 5 section. Update `_main.py` imports accordingly.

#### 🟡 Risk 4: C73 disclaimer compliance

C73 ships expert analysis synthesis. If disclaimers are inconsistent or missing, regulatory risk in TW financial content. **Mitigation**: D-040 is a Sprint 5 prerequisite. `_historian_disclaimer('expert')` must exist before C73 implementation starts.

#### 🟢 Risk 5: C71 persistence

Study Log needs to persist user entries. The watchlist pattern (YAML + `_load_data()`) is the precedent. **Mitigation**: Follow `watchlist.py` pattern. Create `src/data/study_log.yaml` + loading functions. Low risk since the pattern is proven.

#### 🟢 Risk 6: D22 persistence layer promotion

D22 was promoted to Sprint 6 P0 (persistence layer for community features). Sprint 5 doesn't need it — C71 can use the watchlist YAML pattern. D22 remains a Sprint 6 concern.

### Total Sprint 5 Effort Estimate: 32-48h (features only) + 3-5h (preventive architecture items)

### Recommended Sprint 5 Sequence

1. **Pre-work** (2.5h, BEFORE feature coding):
   - D-041: Create `_study_card()`, `_expert_card()`, `_scenario_card()` (1h)
   - D-039: Create `_section_header()` helper (1h)
   - D-040: Create `_historian_disclaimer()` helper (0.5h)
   - D-037: Fix `_白话_card` background color (<0.5h, can defer)

2. **Feature implementation**:
   - C71 (Study Log) — 8-12h — simplest, start first
   - C74 (Historical Scenarios) — 10-16h — medium complexity
   - C73 (Expert Analysis) — 14-20h — most complex, needs D-040 prerequisite

3. **Alongside features**:
   - D37: Split `_sections.py` when it exceeds 650 lines (triggered by first section addition)

---

## 8. Updated Debt Register Summary

| Priority | Count | Items |
|----------|-------|-------|
| 🔴 Resolved in this round | 1 | **D16** (analogy_engine.py split) — was the critical blocker |
| 🟡 P1 (High) | 3 | D-003, D-005, D-006 (from project issue tracker, design-side) |
| 🟢 P2 (Medium) | 15+ | D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, D18, D21, D22, D23, D25, D26, D27, D28, D29, D30, D31, D32, D33, D37, D38, D39 (new) |
| ✅ Total Resolved | 7 | D1, D2, D16, D17, D20, D24, D-004 (design system doc) |
| **Total tracked** | **36** | (+1 new: D39, +1 resolved: D16 vs Round 15) |

### Net Change Since Round 15
- **+1 resolved**: D16 (analogy_engine.py split) — the #1 critical path item
- **+1 new**: D39 (duplicate import headers in business_card sub-directory)
- **D26 unblocked**: `story_composer.py` can now import from stable, focused modules

---

## 9. Key Recommendations Summary

| # | Recommendation | Priority | Effort | Impact |
|---|---------------|----------|--------|--------|
| 1 | ✅ **D16 complete** — analogy_engine.py split into 4 modules | DONE | — | Unblocks C48, eliminates god module |
| 2 | **Start C48 immediately** — no blockers remain | 🔴 High | 10-14h | Sprint 4 critical feature |
| 3 | **D-041 before Sprint 5** — create C71/C73/C74 card components | 🔴 High | 1h | Prevents D-003 regression |
| 4 | **D-040 before C73** — create disclaimer component | 🔴 High | 0.5h | Regulatory compliance |
| 5 | **D37 alongside C38/C48** — split `_sections.py` when it exceeds 650 lines | 🟡 Medium | 1-2h | Prevents re-emerging monolith |
| 6 | **D23 before C51** — write tone guidelines for market-level data | 🟡 Medium | 1h | Prevents historian tone violation |
| 7 | **D-037 anytime** — fix `_白话_card` background color | 🟢 Low | <0.5h | Design system compliance |

---

## 10. Next Review

Next review should occur at **Sprint 4 mid-point** (after R3 + one major feature complete). Key assessment criteria:
- C48 `story_composer.py` structure and imports from the new D16-split modules
- `_sections.py` size after first feature addition (trigger for D37 split)
- `market_data.py` design for C51 (D25)
- Sprint 5 prerequisite items (D-039, D-040, D-041) completion status

---

*Created: 2026-06-20*
*Maintainer: System Architect*
*Next review: Sprint 4 mid-point (after R3 + one major feature)*
