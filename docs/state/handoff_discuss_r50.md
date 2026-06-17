# Handoff – Discussion Round 50

## Summary
- **Topic**: 💡 Discussion (Round 50 — 2026-06-17)
- **Participants**: Product Manager, System Architect, Design Reviewer, Challenger
- **Sprint Status**: Sprint 24 ✅ C201 COMPLETE + design cleanup → Sprint 25 Planning
- **Challenger Verdict**: ⚠️ CONDITIONAL — 4 systemic risks identified, 5 blocking questions for Daniel

---

## Sprint 24 — FINAL VERIFICATION ✅

| Feature | Status | Evidence |
|---------|--------|----------|
| C201 Daily Market Dashboard | ✅ COMPLETE | Commit `ad5b46c`, 300 lines + 591 test lines |
| Design system color cleanup | ✅ COMPLETE | Commit `2fc60d3`, 30+ violations fixed across 4 files |
| All tests green | ✅ 662/662 | 3.84s execution |

---

## Sprint 25 — FINAL PLAN (Post-Challenge)

### MUST (Core)

| Feature | Effort | Risk | Go/No-Go Gate |
|---------|--------|------|----------------|
| **Pre-sprint fixes** (8 color fixes + 3 tech debt + API abuse fix) | 3-4h | Low | All fixes applied, 662+ tests green |
| **C209** Collapsible Source Transparency (3 pages v1) | 4-6h | Low | Source section renders on business_card, daily_market, event_dashboard |

### SHOULD (High value, if time permits)

| Feature | Effort | Risk | Go/No-Go Gate |
|---------|--------|------|----------------|
| **C203** Company Ecosystem Cards v1 (8 companies) | 10-12h | Medium | Daniel approval required; cap at 8 companies |
| **C206** Recurring Investment Education (1 lesson) | 6-8h | Low | Single DCA lesson, hypothetical data only |

### COULD (Nice to have)

| Feature | Effort | Notes |
|---------|--------|-------|
| Remaining Round 7 design fixes (D-075 to D-083) | 2-3h | Page-specific, lower priority |
| Dark/Light Theme (D-126) | 8-12h | Pending Daniel decision |
| `_infocard` component (D-127) | 6-9h | Pending Daniel decision |

### Fallback Plan (if Daniel doesn't approve C203)
- C209 expands to all pages (7-9h) → MUST
- C206 elevates to MUST (6-8h)
- API abuse fix still done in Week 1

---

## Implementation Order

| Week | Focus | Deliverable |
|------|-------|-------------|
| Week 1 Day 1-2 | Pre-sprint fixes | 8 color fixes (10 min) + 3 tech debt (20 min) + API abuse fix (1-2h) |
| Week 1-2 | C209 implementation | `_source_section()` component + 3 pages integrated |
| Week 2-3 | C203 implementation (if approved) | `ecosystem_service.py` + `ecosystem_cards.py` + data expansion to 8 companies |
| Week 3-4 | C206 implementation | Single DCA lesson in academy, hypothetical data only |
| Week 4 | Buffer + remaining fixes | Regression testing, remaining design fixes |

---

## Key Architectural Decisions (Updated)

1. **C209 uses `st.expander()` pattern** — collapsed by default, zero clutter, additive change
2. **C203 caps at 8 companies** — existing 5 from `group_structures.yaml` + 3 new. NOT 15-20.
3. **C203 reuses `_subsidiary_card()`** — no new component needed. Card-based, not network graph.
4. **C206 is single lesson only** — hypothetical data only, NO calculator, NO real stock examples
5. **API abuse fix is prerequisite** — `get_stock_info` must be fixed before C203 fetches 8+ stock prices
6. **Pre-sprint fixes are mandatory** — 8 non-palette colors + 3 tech debt items in Week 1 Day 1-2
7. **Design audit needed** — 92 issues reported but 3 of top 5 were already fixed. Fresh audit required.

---

## 5 Blocking Questions for Daniel

| # | Question | Blocker For | Default if No Response |
|---|----------|-------------|----------------------|
| Q1 | Approve "ecosystem cards" approach for C203? (8 companies, parent-subsidiary + limited customer-supplier, card-based) | C203 (SHOULD) | Defer C203 to Sprint 26 |
| Q2 | C206 scope: Single DCA lesson OK? Hypothetical data only? | C206 (SHOULD) | Default: single DCA lesson, hypothetical only |
| Q3 | Apply 8 non-palette color fixes before Sprint 25? (10 min, brings grade to B-) | Design debt | PM decides: YES |
| Q4 | Fix API abuse in `get_stock_info` before C203? | C203 data layer | PM decides: YES (prerequisite) |
| Q5 | Fix 3 Sprint 23 tech debt items in Sprint 25 Week 1? (20 min) | Tech debt | PM decides: YES |

---

## Role Opinions Summary

### Architect
- **Top pick**: C209 (cleanest, lowest risk) → C203 (if Daniel approves) → C206 (pure content, low risk)
- **Key insight**: 3 of 5 "top priority" Round 7 fixes were already done in Sprint 24 cleanup. Fresh audit needed.
- **Recommendation**: Fix API abuse before C203. Cap C203 at 8 companies.

### Designer
- **Top pick**: C209 (progressive disclosure, clean pattern) → C206 (uses existing `_lesson_card()`) → C203 (reuses `_subsidiary_card()`)
- **Key insight**: `_subsidiary_card()` is the perfect fit for C203. No new component needed.
- **Recommendation**: Apply 8 color fixes (10 min) before Sprint 25. Brings grade from C+ to B-.

### Challenger
- **Verdict**: ⚠️ CONDITIONAL — 4 systemic risks
- **Key concerns**: (1) C203 data source problem renamed not solved, (2) C206 scope ambiguity (education vs advice), (3) API abuse will be triggered by C203, (4) 92 design issues at 5.4% fix rate
- **Recommendation**: Pre-sprint fixes are mandatory. Cap all features at conservative scope. Define fallback plan.

---

## Action Items

| Item ID | Description | Owner | Sprint | Status |
|---------|-------------|-------|--------|--------|
| A50-01 | Apply 8 non-palette color fixes to shared components | Developer | Sprint 25 W1D1 | ⏳ Pending |
| A50-02 | Fix 3 Sprint 23 tech debt items (naming, namespace, dead import) | Developer | Sprint 25 W1D1 | ⏳ Pending |
| A50-03 | Fix API abuse in `get_stock_info` | Developer | Sprint 25 W1D2 | ⏳ Pending |
| A50-04 | Create `_source_section()` component in `_router_base.py` | Developer | Sprint 25 W1-2 | ⏳ Pending |
| A50-05 | Integrate C209 into 3 pages (business_card, daily_market, event_dashboard) | Developer | Sprint 25 W1-2 | ⏳ Pending |
| A50-06 | Expand `group_structures.yaml` to 8 companies | Developer | Sprint 25 W2-3 | ⏳ Pending (needs Daniel) |
| A50-07 | Create `ecosystem_service.py` + `ecosystem_cards.py` | Developer | Sprint 25 W2-3 | ⏳ Pending (needs Daniel) |
| A50-08 | Create single DCA lesson (hypothetical data only) | Developer | Sprint 25 W3-4 | ⏳ Pending (needs Daniel) |
| A50-09 | Run fresh design audit (verify 92 issues against current code) | QA | Sprint 25 W1 | ⏳ Pending |
| A50-10 | Evaluate dark theme (D-126) and _infocard (D-127) for Sprint 26 | PM + Designer | Sprint 26 | ⏳ Pending Daniel |

---

## Documentation Created
- `docs/architecture/discuss_r50_architect.md` — Full architecture analysis
- `docs/design/discuss_r50_designer.md` — Design assessment + Round 7 fix verification
- `docs/state/challenge_r50.md` — 3-round challenge with 10 questions
- `docs/state/handoff_discuss_r50.md` — This document

---

*Created: 2026-06-17 by PM*
*Source: docs/architecture/discuss_r50_architect.md, docs/design/discuss_r50_designer.md, docs/state/challenge_r50.md*
