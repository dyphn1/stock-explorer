# Stock Explorer — Architect Review Round 15

> **Date**: 2026-06-19
> **Reviewer**: System Architect
> **Scope**: Sprint 4 kickoff — debt resolution status, new debt identification, feasibility reassessment
> **Previous Review**: Round 14 (2026-06-19)

---

## 1. Executive Summary

Round 15 confirms that **D24 (business_card.py sub-directory extraction) is complete** — the single most critical architecture debt item from Round 14. The 561-line monolith is now 4 files totaling 795 lines across a sub-directory. This is a net structural improvement.

**D16 (analogy_engine.py split) remains the critical open item** at 850 lines. It is the hard blocker for C48 (Company Story Card) and should be the first development task in Sprint 4.

**No new P0 debt items** were identified. One new medium-severity item (D37) is proposed: `_sections.py` at 612 lines is already approaching the size threshold that triggered D24.

---

## 2. Codebase Growth Summary

| Metric | R11 | R12 | R14 | R15 | Δ R14→R15 |
|--------|-----|-----|-----|-----|-----------|
| Total .py files | 31 | 31 | 32 | **36** | **+4** |
| Total app LOC | ~7,699 | ~7,818 | ~8,572 | **~8,969** | **+397** |
| `analogy_engine.py` | 857 | 850 | 850 | **850** | 0 |
| `financial_metrics.py` | — | 188 | 188 | **188** | 0 |
| `risk_analyzer.py` | — | — | 567 | **567** | 0 |
| `chart.py` | 757 | 779 | 779 | **787** | **+8** |
| `business_card.py` (monolith) | 479 | 447 | 561 | **— (extracted)** | — |
| `business_card/_main.py` | — | — | — | **84** | new |
| `business_card/_sections.py` | — | — | — | **612** | new |
| `business_card/_helpers.py` | — | — | — | **95** | new |
| `business_card/__init__.py` | — | — | — | **4** | new |
| L0 (Import) | 54/54 | 55/55 | 56/56 | **59/59 ✅** | +3 |
| L1 (Render) | 15/15 | 18/18 | 8+10 pre-exist | **stable** | — |

**Key change since Round 14**: D24 extraction split `business_card.py` (561 lines) into 4 files. Net LOC increased by ~200 due to duplicated import headers across the 4 files. L0 improved from 56→59 (3 new import targets).

---

## 3. Debt Resolution Status

### ✅ RESOLVED (5 items)

| Item | Resolution | Notes |
|------|-----------|-------|
| **D1** (Duplicate financial metrics) | ✅ R1 complete | `financial_metrics.py` (188 lines) is the single source of truth |
| **D2** (`_find_financial_value` duplication) | ✅ R1 complete | All 4 consumers import from `financial_metrics.py` |
| **D17** (EPS extraction triplication) | ✅ R1 complete | `extract_ttm_eps()` in `financial_metrics.py` |
| **D20** (Valuation double-computation) | ✅ D-020 fix | `create_valuation_band_chart()` returns `(fig, interp_dict)` |
| **D24** (business_card.py sub-directory) | ✅ **NEW** — Commit e12c103 | 561-line monolith → 4 files: `_main.py` (84), `_sections.py` (612), `_helpers.py` (95), `__init__.py` (4) |

### ⏳ PARTIALLY ADDRESSED (2 items)

| Item | Status | Notes |
|------|--------|-------|
| **D19** (Inline HTML in business_card) | 🟡 Partial | Dividend table inline HTML still exists but is now in `_sections.py` rather than a monolithic file. Health score dimension cards also remain. Easier to address now that sections are separated. |
| **D32** (Presentation helpers in page file) | 🟡 Partial | `get_health_dimension_explanation()` and `_render_risk_dimension()` moved to `_helpers.py` (95 lines) — better than inline in the monolith, but still not in a shared `ui_components.py`. D32 is now "presentation helpers in a page sub-module" rather than "presentation helpers in a page file." |

### 🔴 STILL OPEN — CRITICAL (1 item)

**D16: `analogy_engine.py` god module** — 850 lines, 6 responsibilities
- **Status**: Unblocked (R1 complete since Round 12). No progress since Round 14.
- **Impact**: Blocks C48's `story_composer.py` (D26). C38 also imports analogy functions.
- **Urgency**: 🔴 **Must be completed before C48 starts.** Should be the first or second task in Sprint 4 (after or parallel with any remaining Sprint 3 items).
- **Effort**: 2-3h. Well-defined split plan exists in tech_debt.md.

### 🟡 STILL OPEN — MEDIUM (27 items)

D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, D18, D19, D21, D22, D23, D25, D26, D27, D28, D29 (superseded by D24), D30 (realized, now resolved by D24), D31, D32

### 🟢 STILL OPEN — LOW (1 item)

D33 (C41 page-level data access)

---

## 4. New Architecture Debt Identified in Round 15

### D37: `_sections.py` is 612 lines and will grow with C38 + C48

- **Severity**: 🟡 Medium
- **Description**: The D24 extraction created `_sections.py` as the single file containing all section rendering functions. At 612 lines, it already contains 14 section functions (header, takeaways, deltas, health, risk, one-liner, key metrics, dividend, revenue breakdown, revenue trend, valuation, news, read next, footer). C38 (Compare Stories) and C48 (Company Story Card) will each add a section function (~50-70 lines), pushing it to ~730+ lines.
- **Impact**: `_sections.py` is becoming the new monolith — the same problem D24 solved for `business_card.py` is re-emerging at the section level.
- **Recommended Action**: When C38 and C48 are implemented, split `_sections.py` into:
  - `_sections_core.py` — header, one-liner, key metrics, footer (stable sections)
  - `_sections_analysis.py` — takeaways, deltas, health, risk (analysis sections)
  - `_sections_detail.py` — dividend, revenue breakdown, revenue trend, valuation, news (detail sections)
  - `_sections_discovery.py` — read next, compare stories, story card (discovery sections)
- **Effort**: 1-2h (split + update imports in `_main.py`)
- **Priority**: Do alongside C38/C48 implementation, not as a separate task.

### D38: `chart.py` grew to 787 lines with chart functions added incrementally

- **Severity**: 🟡 Medium (monitor)
- **Description**: `chart.py` grew from 779→787 lines since Round 14. The module now contains all chart types: revenue trend, revenue pie, valuation band, health snowflake, and potentially others. Unlike `analogy_engine.py`, chart.py has a **single responsibility** (chart rendering), so the size is less concerning. However, if C51 (Sector Heatmap) adds treemap/sunburst charts to this file, it will cross 850+ lines.
- **Impact**: Low for now. The module is coherent — all functions are chart rendering. But the lack of sub-organization means finding a specific chart function requires scrolling through 787 lines.
- **Recommended Action**: If C51 adds sector/market charts, create `chart_sector.py` for market-level visualizations. Keep `chart.py` for single-stock charts.
- **Effort**: 1h (if needed)
- **Priority**: Monitor. Act only if market charts are added.

---

## 5. Debt That Has Worsened Since Round 14

### D16 urgency increased
- **Why**: Sprint 4 is now active. C48 (Company Story Card, 10-14h) is a Sprint 4 deliverable that is blocked on D16. Every day D16 is deferred is a day C48 cannot start.
- **Status change**: From "should be done soon" to "active blocker for Sprint 4 work."

### D32 partially improved
- **Why**: The D24 extraction moved `get_health_dimension_explanation()` and `_render_risk_dimension()` from inline in the monolith to `_helpers.py`. This is structurally better but still not the ideal home (`ui_components.py`).
- **Status change**: From "presentation helpers in page file" to "presentation helpers in page sub-module." Slightly better, but the reuse problem remains.

---

## 6. Sprint 4 Feasibility Assessment

### Current Sprint 4 Plan (from handoff)
D24 ✅ → D16 → R3 → C38 → C51 → C48 → C53-1

### Updated Feasibility Assessment

| Step | Effort | Dependencies | Risk | Verdict |
|------|--------|-------------|------|---------|
| **D24** (Extract business_card.py) | 2-3h | None | ✅ **DONE** | ✅ Complete |
| **D16** (Split analogy_engine.py) | 2-3h | None (R1 done) | Low — well-defined split | ✅ **Proceed immediately** |
| **R3** (Batch API minimal) | 1-2h | None | Low — isolated utility | ✅ Proceed in parallel with D16 |
| **C38** (Compare Stories P1) | 10-12h | D16 (for analogy functions) | Medium — narrative comparison is new pattern | ✅ Proceed after D16 |
| **C51** (Sector Heatmap) | 12-16h | R3 + D25 (market_data.py) | Medium — needs new `market_data.py` service | ✅ Proceed after R3 |
| **C48** (Company Story Card) | 10-14h | D16 + D24 | Medium — `story_composer.py` is new | ✅ Proceed after D16 |
| **C53-1** (Social Sharing URL) | 2-3h | None | Low — isolated feature | ✅ Quick win, do last |

### Total remaining effort: 37-50h
### Critical path: D16 → C38 → C51 (or D16 → C48 in parallel with C38/C51)

### Architecture Risks for Sprint 4

1. **🔴 D16 is the critical path**: If D16 slips, C48 slips. C38 also needs analogy functions from the split. **D16 must be the first development task in Sprint 4.**

2. **🟡 _sections.py growth (D37)**: C38 and C48 will each add ~50-70 lines to `_sections.py`. At 612 lines now, it will reach ~730+ lines. This is manageable but should be monitored. Split alongside feature implementation.

3. **🟡 Market data abstraction gap (D25)**: C51 needs `market_data.py`. Without it, sector heatmap will ad-hoc the market-wide data flow. This is a hard prerequisite for C51.

4. **🟡 Tone guidelines gap (D23)**: C51 displays market-level data. Without tone guidelines, market features risk sounding like investment advice. Content task, not code task, but should be done before C51 ships.

5. **🟢 chart.py growth (D38)**: Monitor. Only act if market charts push it beyond 850 lines.

---

## 7. Top 3 Recommendations

### 1. 🔴 Complete D16 immediately — it is the Sprint 4 critical path

**Action**: Split `analogy_engine.py` (850 lines) into 4 focused modules:
- `src/services/analogy_engine.py` — analogy functions only (~136 lines)
- `src/services/key_takeaways.py` — `generate_key_takeaways()` + data
- `src/services/delta_engine.py` — `compute_recent_deltas()` + `explain_delta()`
- `src/services/health_scoring.py` — all `_score_*` + `compute_health_scores()`

**Effort**: 2-3h. **Impact**: Unblocks C48 and C38. Eliminates the largest remaining god module.

### 2. 🟡 Plan _sections.py split alongside C38/C48 implementation

**Action**: When implementing C38 and C48, split `_sections.py` into 2-3 sub-modules (`_sections_core.py`, `_sections_analysis.py`, `_sections_detail.py`) rather than appending to the 612-line file.

**Effort**: 1-2h (do alongside feature work). **Impact**: Prevents the same monolith problem D24 solved from re-emerging at the section level.

### 3. 🟡 Create `market_data.py` as part of C51 — do not ad-hoc market data flow

**Action**: Before implementing C51's visualization, create `src/services/market_data.py` with a clean interface for market-wide data aggregation. This is D25 from the debt register.

**Effort**: 1-2h (as part of C51). **Impact**: Establishes the market-level data flow pattern. Prevents C51 from bypassing the 4-layer architecture.

---

## 8. Debt Register Summary

| Priority | Count | Items |
|----------|-------|-------|
| 🔴 P0 (Critical) | 0 | — |
| 🟡 P1 (High) | 3 | D-003, D-005, D-006 (from project issue tracker) |
| 🟢 P2 (Medium/Low) | 13+ | D3-D16, D18-D38 (architecture debt register) |
| ✅ Resolved | 5 | D1, D2, D17, D20, D24 |

**Total tracked debt items**: 34 (5 resolved + 29 open)
**Net change since Round 14**: +1 new item (D37), +1 resolved (D24), +1 partially improved (D32)

---

## 9. Next Review

This register should be updated after D16 and R3 are complete (Sprint 4 mid-point). The next architect review should assess:
- D16 completion and its effect on C48 feasibility
- `_sections.py` size after C38 implementation
- `market_data.py` design for C51

---

*Created: 2026-06-19*
*Maintainer: System Architect*
*Next review: After D16 + R3 complete (Sprint 4 mid-point)*
