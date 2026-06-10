# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡)
- **Date**: 2026-06-12
- **Participants**: Product Manager, System Architect, Developer, Design Reviewer, Challenger
- **Theme**: Feature Direction + Roadmap Round 6

## Idea Proposals
| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C01 | Ex-Dividend Countdown + Badge | Dev | ✅ Done |
| C31 | Daily Financial Challenge | Dev | Approved — 8h, Challenger Round 5 "best new feature" |
| C16 | "Did You Know?" Company Facts | Dev | ✅ Done |
| C07 | Custom Event Thresholds | Dev + Architect | Approved — 12h, Sprint 1, "force multiplier" |
| C14 | Health Score (Badge or Radar) | Dev | Deferred — needs Daniel decision on scope |
| C28 | Company Story Timeline | Dev | Approved — next priority after Sprint 2 (25h) |
| C02 | Notification / Push System | Dev + Architect | Partially approved — D02 Pull Model in Sprint 2 |
| D02 | Background Worker Architecture | Architect | Approved — 7h Pull Model in Sprint 2 |
| C04 | Market Thermometer | Dev | Deferred — lower priority than engagement |
| C06 | Auto-Generate PPT | Dev | Phase 3 — 18-24h, needs all pages B+ |
| C32 | Market Mood | Dev | Conditional — go/no-go by Day 3 of Sprint 1 |
| DR-04 | Component inconsistency (inline HTML) | Dev | Approved — 2h, Sprint 1 |
| DR-05 | Responsive column layouts | Dev | Approved — 1.5h, Sprint 1 |

## Decisions Made
1. **Sprint 1 — Foundation + Force Multiplier (15.5h)**: DR-04 (component consistency, 2h) → DR-05 (responsive columns, 1.5h) → C07 (Custom Event Thresholds, 12h). C07 is the Architect's "force multiplier" — it transforms event detection from demo to personalized tool.
2. **Sprint 2 — Competitive Parity + Engagement (15h)**: D02 (Pull Model notification, 7h) → C31 (Daily Financial Challenge, 8h). D02 addresses the P0 notification gap. C31 is the Challenger-approved retention mechanism.
3. **C32 (Market Mood) is conditional**: Data source must be validated by Day 3 of Sprint 1. If no data source exists, replace with C28 MVP (basic Company Story Timeline, 10h).
4. **C28 (Company Story Timeline) is the next priority after Sprint 2** — no further deferral. This is the direct counter to StockStory/Stockopedia AI threats.
5. **C14 (Health Score) scope decision still pending from Daniel** — Badge (4-6h) vs Radar (14-20h). Not in current sprint.
6. **C06 (PPT Generation) remains Phase 3** — needs all pages at B+ first.
7. **Challenger required 2 rounds of revision** before approving. Key changes: replaced C14-B with C07, added D02, made C32 conditional, committed to C28 as next priority.

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| DR-04 | Migrate raw HTML cards to `_白话_card()` in Category Browser and Group Structure | Dev | Sprint 1 |
| DR-05 | Fix 6-column responsive layouts in Category Browser and ETF Browser | Dev | Sprint 1 |
| C07 | Custom Event Thresholds — UI + adaptive_engine.py refactoring | Dev + Architect | Sprint 1 |
| D02 | Pull Model notification — architecture doc + implementation | Architect + Dev | Sprint 2 |
| C31 | Daily Financial Challenge — question bank, streak tracking, UI | Dev | Sprint 2 |
| C32 | Market Mood — data source validation by Day 3 Sprint 1 | Dev | Sprint 1 Day 3 |
| C28 | Company Story Timeline — next priority after Sprint 2 | Dev | Sprint 3 |

## Team Opinions Summary

### Architect (nemotron-120b)
- **Recommended order**: D02+C02 Pull Model (7-11h) → C31+C07 (17-24h) → C28 (20-30h)
- **Highest ROI**: C07 (force multiplier for all event-dependent features)
- **Key insight**: C07 transforms event detection from demo to real tool. Every event-dependent feature benefits.
- **Critical gaps flagged**: N+1 query in category_browser.py, disconnected rate limit handling, YAML storage doesn't scale, no integration tests, dead code proliferation
- **Competitive threat**: StockStory and Stockopedia AI both have sophisticated event/alert systems; hardcoded thresholds make Stock Explorer feel rigid.

### Design Reviewer (gemma-31b)
- **Recommended order**: DR-04 (2h) → DR-05 (1.5h) → C14 Badge (4-6h) → C31 (7-10h)
- **Key insight**: The gap between A- (Event Dashboard) and D (Category Browser/Group Structure) is almost entirely about shared component usage, color compliance, and PPT-style discipline
- **C14 recommendation**: Build simple Badge (4-6h), NOT Radar Chart (14-20h). Badge communicates in <1 second, radar requires 15-30s to interpret.
- **Pattern to replicate**: Event Dashboard's badge system, expandable detail, empty state handling, progressive disclosure
- **C32 concern**: Did NOT include C32 in recommendations. Market Mood may contradict "historian" positioning.

### Developer (owl-alpha)
- **Recommended order**: DR-05+DR-04+C14-B (Sprint 1, 8.5h) → C31+C32 (Sprint 2, 18h)
- **ROI ranking**: DR-05 (⭐⭐⭐⭐⭐) > DR-04 (⭐⭐⭐⭐⭐) > C14-B (⭐⭐⭐⭐⭐) > C31 (⭐⭐⭐⭐) > C32 (⭐⭐⭐⭐) > C07 (⭐⭐⭐½)
- **Key insight**: C07 touches 612-line adaptive_engine.py — high regression risk. Must run full M5 test suite after changes.
- **Technical risks**: D02 (Streamlit is wrong tool for background workers), C06 (kaleido + Chinese fonts), C28 (25h, highest risk)
- **Optimal sequence**: DR-04 → DR-05 → C07 → D02 → C31 → C29 → C28

### Challenger (gpt-oss-120b)
- **Round 1 verdict**: ❌ REJECTED — Plan fails "Story first" core value, defends against zero competitive threats, includes contradictory C32, avoids highest-ROI work
- **Round 2 verdict**: ⚠️ NEEDS REVISION — Prerequisite argument weak, C14-B too small, C07 deferral is strategic mistake, estimates optimistic
- **Round 3 verdict**: ✅ ACCEPTED (with conditions) — Revised plan addresses core gaps, includes C07 and D02, makes C32 conditional, commits to C28
- **Key conditions**: C28 must be next priority after Sprint 2, C32 data validation deadline Day 3 Sprint 1, Architect must document D02 approach before Sprint 2, N+1 query fix bundled with D02

## Final PM Decision (Post-Challenger Confirmed)

| Order | Sprint | Item | Hours | Core Value | Risk |
|-------|--------|------|-------|------------|------|
| 1 | Sprint 1 | DR-04: Component consistency | 2h | #2 PPT-style | Trivial |
| 2 | Sprint 1 | DR-05: Responsive columns | 1.5h | #2 PPT-style | Trivial |
| 3 | Sprint 1 | C07: Custom Event Thresholds | 12h | #3 Adaptive | Medium |
| 4 | Sprint 2 | D02: Pull Model notification | 7h | #3 Adaptive | Medium |
| 5 | Sprint 2 | C31: Daily Financial Challenge | 8h | #1 Story first | Medium |
| **Total** | | | **30.5h** | | |

**Conditional**: C32 Market Mood (10h) — only if data source validated by Day 3 Sprint 1. Otherwise replace with C28 MVP (10h).

**Mandatory follow-up**: C28 Company Story Timeline (25h) is the first priority after Sprint 2. No further deferral.

**Rationale**: This plan fixes the visual foundation (DR-04, DR-05), builds the force multiplier that makes event detection personal (C07), addresses the P0 notification gap (D02), and delivers the Challenger-approved retention mechanism (C31). C32 is conditional on data availability. C28 is committed as the next sprint's top priority to counter StockStory/Stockopedia AI threats.

## Pending Daniel's Decision
See `docs/state/pending_review.md` for items requiring human input:
- #7: C14 Health Score scope — Badge (4-6h) or Full Radar (14-20h)?
- #8: Revised roadmap approval (this 2-sprint plan, 30.5h + conditional 10h)
- #9: Category Browser + Group Structure structural redesign — include now or defer?

## Next Cycle Handoff
Next theme: 🔧 Development → read `docs/state/handoff.md`
Next dev cycle should tackle: Sprint 1 (DR-04 → DR-05 → C07), then Sprint 2 (D02 → C31)
