# Handoff – Discussion Round 47

## Summary
- **Topic**: 💡 Discussion (Round 47 — 2026-06-15)
- **Date**: 2026-06-15
- **Participants**: Product Manager, System Architect, Design Reviewer, Developer, Challenger
- **Sprint Status**: Sprint 21 ✅ COMPLETE → Sprint 22 (C201) in progress
- **Challenger Verdict**: ✅ ALIGNED — 3 conditions (C199 Tone QA gate, C200 Week 1 go/no-go, C207-C214 evaluation in Round 48)

---

## Idea Proposals

| Idea ID | Description | Source | Priority | Status |
|---------|-------------|--------|----------|--------|
| C202 | Story Arc Timeline Labels — Auto-Detected Narrative Arcs on Company Event Timeline | Competitor R46 (StockStory) | P2 MUST | Sprint 23 |
| C199 | Bear vs Bull Visual Debate Cards — Side-by-Side Argument Cards with Icons and Key Stats | Competitor R46 (Simply Wall St) | P2 SHOULD | Sprint 23 (with Tone QA gate) |
| C200 | What If I Had Invested? Historical Scenario Calculator | Competitor R46 (Magnify.money, StockStory) | P2 COULD | Sprint 23 (with Week 1 go/no-go) |

---

## Decisions Made

### Sprint 23 Plan (Post-Challenge)

| Priority | Feature | Effort | Risk | Go/No-Go Gate |
|----------|---------|--------|------|----------------|
| MUST | C202 Story Arc Timeline Labels | 9-14h | Low | Quality check on 3 test stocks (TSMC, 鴻海, 緯穎) |
| SHOULD | C199 Bear vs Bull Debate Cards | 10-16h | Medium | Tone QA gate — 2 revision max, then defer |
| COULD | C200 What If Calculator | 12-17h | Medium-High | Week 1: FinMind API caching + historian framing |
| **Total** | | **31-47h** | | |

### Implementation Order
1. **Week 1**: C202 (Story Arc) — quick win, lowest risk
2. **Week 1-2**: C199 (Debate Cards) — parallel with C202 UI phase
3. **Week 2-3**: C200 (What If Calculator) — only if Week 1 gate passes

### Sprint 24 (Provisional)
- C200 (if deferred from Sprint 23)
- C201 follow-ups (daily caching pipeline)
- C206 Recurring Investment Education (pending regulatory review)
- C203 Supply Chain Visual Map
- C209 Source Transparency Layer (pending Round 48 evaluation)

---

## 3 Conditions (Pre-Sprint 23)

| Condition | Owner | Deadline |
|-----------|-------|----------|
| C199 Tone QA Gate: Content review must pass before C199 ships. Four-safeguard pattern (disclaimer, "自動產生" label, data-driven points, banned word list) is mandatory. | PM + Designer | Before C199 release |
| C200 Week 1 Go/No-Go: FinMind API caching must be validated. Historian framing must pass tone QA (no FOMO language). | Developer + PM | Sprint 23 Week 1 |
| C207-C214 Evaluation: Round 48 Discussion must evaluate C209 (Source Transparency) and C210 (Video Library) before Sprint 24 planning. | PM + QA | Round 48 |

---

## Key Architectural Decisions

1. **C202 uses rule-based arc detection** (not LLM) — YAML-configurable thresholds, minimum 8 quarters of data, non-overlapping 6-month windows
2. **C199 uses asymmetric evidence display** — not forced 3-vs-3; shows evidence balance indicator
3. **C200 extends existing C74** (`_historical_scenarios.py`, 320 lines) — curated scenarios remain as "Featured," calculator adds "Custom"
4. **All three features are presentation-layer heavy** — monitor `_router_base.py` growth, extract UI helpers if files exceed 400 lines
5. **All features are independent of Sprint 21/22 work** — no blocking dependencies

---

## Role Opinions Summary

### Architect
- **Top pick**: C200 (highest feasibility, existing C74 foundation) → C202 (rule-based viable now) → C199 (conditional on C188 quality)
- **Key insight**: C74 existing codebase (320 lines) significantly de-risks C200
- **Recommendation**: Proceed with all three, but C200 last in sequencing

### Designer
- **Top pick**: C202 (cleanest design fit, zero new colors) → C199 (highest UX impact, P1 advisor risk) → C200 (defer to Sprint 24 if P1 FOMO risk unresolved)
- **Key insight**: C199 needs four-safeguard advisor boundary pattern; C200 needs historian framing
- **P1 Issues**: C199 advisor boundary, C200 FOMO framing — both resolvable through copy/design

### Developer
- **Top pick**: C202 (lowest risk, 9-14h) → C199 (parallelizable, content quality risk) → C200 (highest technical risk, FinMind API)
- **Key insight**: All three features touch completely different files — parallel development is feasible
- **Total estimate**: 31-47h (realistic ~39h)

### Challenger
- **Round 1**: Scope justification, C202 quality bar, C199 safeguards, C200 sequencing — all addressed
- **Round 2**: C202 vs C199 priority (vision alignment > competitive differentiation), C200 go/no-go gate, sprint capacity, C207-C214 deferral — all addressed
- **Round 3**: Educational mission alignment, role contradiction resolution, go/no-go criteria — all addressed
- **Verdict**: ✅ ALIGNED with 3 conditions

---

## Action Items

| Item ID | Description | Owner | Sprint |
|---------|-------------|-------|--------|
| A47-01 | Create `story_arc_detector.py` service module | Developer | Sprint 23 |
| A47-02 | Create `story_arcs.yaml` content templates | Developer + PM | Sprint 23 |
| A47-03 | Create `debate_engine.py` service module | Developer | Sprint 23 |
| A47-04 | Create `debate_templates.yaml` content templates | Developer + PM | Sprint 23 |
| A47-05 | Implement four-safeguard advisor boundary pattern for C199 | Designer + PM | Sprint 23 |
| A47-06 | Create `scenario_calculator.py` service module | Developer | Sprint 23 |
| A47-07 | Validate FinMind API caching strategy (Week 1 gate) | Developer | Sprint 23 Week 1 |
| A47-08 | Evaluate C209 and C210 in Round 48 Discussion | PM + QA | Round 48 |

---

## Next Cycle Handoff

**Next cycle**: 🔧 Development Round 48 — Sprint 22 execution (C201 今日市場動態)
**Reference**: `docs/state/handoff.md` Development section for Sprint 22 plan
**Sprint 23 Plan**: This document (`docs/state/handoff_discuss_r47.md`)

---

*Created: 2026-06-15 by PM*
*Source: docs/architecture/discuss_r47_architect.md, docs/design/discuss_r47_designer.md, docs/status/discuss_r47_developer.md, docs/state/challenge_r47.md*
