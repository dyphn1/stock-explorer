# Sprint 7 Cost Estimates — Round 18

**Date:** 2026-06-12
**Developer:** Sprint 7 Planning
**Sprint Scope:** C84 + C82/D28/D-045 spikes + debt cleanup

---

## Item-by-Item Effort Table

| Item ID | Description | Dev Hours | Verification (20%) | Total Hours |
|---------|-------------|-----------|--------------------|-------------|
| **C84** | Market Event Case Study — spike + implementation | 10.0 | 2.0 | **12.0** |
| **D28** | Spike: Animated Data Story feasibility in Streamlit | 3.0 | 0.6 | **3.6** |
| **D-045** | Spike: card-count limit compliance on sector_heatmap.py | 1.0 | 0.2 | **1.2** |
| **D-044** | Extract market_data.py service from sector_heatmap.py | 2.5 | 0.5 | **3.0** |
| **D3** | Consolidate inline HTML into shared UI components | 3.5 | 0.7 | **4.2** |
| **D6** | Migrate hardcoded data dicts to YAML files | 3.5 | 0.7 | **4.2** |
| **D13** | Initial test infrastructure (pytest + service tests) | 3.5 | 0.7 | **4.2** |
| **D11** | Standardize error boundary conventions (Result pattern) | 2.5 | 0.5 | **3.0** |
| **D7** | Fix N+1 API calls in category_browser.py | 2.5 | 0.5 | **3.0** |
| | **TOTAL** | **32.0** | **6.4** | **38.4** |

---

## Notes on Estimates

### C84 — Market Event Case Study (10h dev)
Spike (2h): Identify which historical market events to cover, data availability check, UI approach (timeline vs. card-based). Implementation (8h): New standalone page or section in business card, event data model, template rendering, navigation from event alerts. Depends on C02 Notification Center data (Sprint 6 ✅).

### D28 Spike — Animated Data Story Feasibility (3h dev)
Research Streamlit animation options: `st.empty()` polling, `streamlit-folium`, Plotly animated charts, or pure CSS/JS injection. C82 is conditional on this spike's outcome. If animation is infeasible, C82 scope reduces to static data story (no animation). Low risk, quick spike.

### D-045 Spike — Card-Count Limit Compliance (1h dev)
Audit `sector_heatmap.py` against the 5-card-per-section limit (Direction A from handoff). Count all card renders in each section. If over limit, propose consolidation strategy. Quick read-only analysis.

### Debt Items Selected (Top 5 by Impact)
1. **D-044** — Sector heatmap has no service layer. This is the #1 architectural gap identified in Round 17. Adds `market_data.py`, unblocks future market-level features.
2. **D3** — Inline HTML duplication across 5+ pages. Highest design-consolidation impact. Creates `ui_components.py` with reusable card/badge/table helpers.
3. **D6** — Hardcoded data in Python modules. Prevents content scaling. YAML migration is mechanical but touches many files.
4. **D13** — Zero test infrastructure. High long-term ROI. Start with pure service-layer functions (no Streamlit dependency). Initial setup + 5-6 service tests.
5. **D7** — N+1 API calls in category_blocks UI. Direct user-facing performance win. Uses existing `ThreadPoolExecutor` pattern from `_router_base.py`.

### Debt Items Deferred
- **D5** (LLM layer): Low priority — template engine works fine for current scope.
- **D11** (error boundaries): Deferred to Sprint 8 — Result pattern refactoring touches every service.
- **D8** (ETF browser sequential fetch): Lower user impact than D7.
- **D-046** (share section JS): Already addressed in Sprint 6 (st.html replaced per code review).
- **D-047** (inverted logic): Already fixed in Sprint 6.
- **D-045 code smell** (dead import): 0.1h — include in D3 cleanup, not separate line item.

---

## Recommended Sequence

```
Phase 1 — Spikes & Prerequisites (parallel)
├── D-045 spike (card-count audit) — 1.2h
├── D28 spike (animation feasibility) — 3.6h
└── C84 spike (event study approach) — included in C84 total

Phase 2 — Features
└── C84 implementation — 10h dev (after spike)
    Note: C82 (Animated Data Story) is DEFERRED to Sprint 8,
    conditional on D28 spike outcome. Not in Sprint 7 dev budget.

Phase 3 — Debt Cleanup (parallel after C84 dev)
├── D-044: market_data.py extraction — 3.0h
├── D3: ui_components.py consolidation — 4.2h
├── D6: YAML migration — 4.2h
├── D7: N+1 fix — 3.0h
└── D13: test infrastructure — 4.2h

Phase 4 — Verification
└── L0/L1 regression + per-item verification — 6.4h (budgeted)
```

### Dependencies
- **D-044 before D3**: `ui_components.py` (D3) should import from `market_data.py` (D-044) rather than duplicating sector logic.
- **D7 uses ThreadPoolExecutor from `_router_base.py`**: No new dependencies, just apply existing pattern.
- **D13 tests target services modified by D6/D-044**: Write tests after those services stabilize.
- **C84 depends on C02 (Sprint 6 ✅)**: Event notification data structures already exist.

---

## Risk Assessment

### High Risks (Could Blow Up Estimate)

1. **C84 scope creep**: If "Market Event Case Study" requires pulling historical event data from new APIs or building a timeline UI from scratch, dev hours could double (10h → 20h). **Mitigation**: Spike first. Cap at 3 pre-built case studies with static data.

2. **D3 (inline HTML) is larger than estimated**: 5+ pages with inline HTML, each with unique layouts. Could hit 6-8h instead of 3.5h. **Mitigation**: Prioritize the 2 worst offenders (business_card.py, sector_heatmap.py). Defer etf_detail.py and watchlist_page.py.

3. **D6 (YAML migration) import chain breaks**: Hardcoded dicts are imported by multiple consumers. YAML loading could introduce parsing errors or type mismatches. **Mitigation**: Add YAML schema validation. Keep fallback to hardcoded data during migration.

4. **D13 (tests) reveals service layer coupling**: Writing tests for tightly coupled services may require refactoring before tests can be written, adding 2-4h unplanned work. **Mitigation**: Start with the most isolated modules (`financial_metrics.py`, `health_scoring.py`).

### Medium Risks

5. **D-044 touches sector_heatmap.py which has 150+ lines of inline HTML**: Extracting the service layer could accidentally break the UI. Need visual regression check. **Mitigation**: D3 should follow D-044 to consolidate the HTML after extraction.

6. **D28 spike could be inconclusive**: If Streamlit animation feasibility is "maybe" rather than yes/no, could require a second spike or prototype. **Mitigation**: Set clear go/no-go criteria before spike begins.

### Low Risks

7. **D7 (N+1 fix)**: Low risk — ThreadPoolExecutor pattern already proven in `_router_base.py`. Just need to wrap existing sequential calls.
8. **D-045 audit**: Read-only analysis. Zero implementation risk.

---

## Sprint 7 Total Budget

| Category | Hours |
|----------|-------|
| Features (C84) | 12.0 |
| Spikes (D28, D-045) | 4.8 |
| Debt Cleanup (5 items) | 17.6 |
| Verification Overhead | 4.0 |
| **TOTAL** | **38.4** |

**Estimated range:** 34-44h (accounting for risk contingencies)
**Prior handoff estimate:** 30-45h ✅ Consistent
