# Handoff – Discussion (Round 18)

## Summary
- **Topic**: Discussion (💡) — Round 18: Sprint 9 Feature Directions (C98 + C101 + C103)
- **Date**: 2026-06-13
- **Participants**: Product Manager, System Architect, Designer, Developer, Challenger
- **Sprint Context**: Sprint 8 complete → Sprint 9 (C98 + C101 + C103) → Sprint 10+

## Critical Discovery: Estimate Gap
The developer's estimates (44.5-51.5h) significantly exceed the PM's original estimates (34-46h). The gap comes from:
- C98: No existing LLM client in codebase (+3h infrastructure)
- C101: Stock-specific scope requires dynamic question selection (+5-6h)
- Contingency buffers (+4h)

**Resolution**: Developer's estimates adopted as working plan. PM estimates are lower bound.

## Idea Proposals
| ID | Feature | Effort | Direction | Sprint |
|----|---------|--------|-----------|--------|
| C98 | Event Interpretation Engine (Hybrid) | 16-23.5h + 2h spike | P1 CONDITIONAL | Sprint 9 |
| C101 | Comprehension Check Quiz (Scoped) | ~11h | P2 CONFIRMED | Sprint 9 |
| C103 Lite | First Visit Guide (2-card primer) | 8-11.5h | P2 CONDITIONAL | Sprint 9 |

## Decisions Made
1. **C98 Hybrid approach**: Templates for dashboard (replacing summaries, not supplementing), LLM for individual event drill-down. 2h spike first to validate LLM approach.
2. **C101 Scoped to 5-8 generic questions**: Not stock-specific in Sprint 9. Reuses C85 quiz pattern. Can be enhanced to adaptive in Sprint 10.
3. **C103 Lite (2-card primer)**: "What you'll learn" + historian disclaimer. Dismissible with single click. Mobile-optimized.
4. **Implementation order**: C103 → C101 → C98 (lowest to highest risk)
5. **Mid-sprint checkpoint**: End of week 1. If behind: C103 Lite reduced to 1 card (-4h). If significantly behind: C103 Lite dropped.
6. **Historian filter QA gate**: PM writes templates → designer reviews → both sign off before coding begins.
7. **Interpretation replaces summary**: C98 interpretation card replaces event summary on dashboard (summary in expander) for ten-second test compliance.

## Challenger 3-Round Summary
- **Round 1** (Feature Direction): ⚠️ PARTIALLY REVISED — Template-only dashboard vs AI competitors; C101 generic vs contextual; C103 Lite value; C34 deprioritization concern
- **Round 2** (Priority): ⚠️ REVISED — Implementation order vs priority mismatch; estimate gap; C103 session-state unreliability; C98/C101 integration opportunity
- **Round 3** (Goal Alignment): ⚠️ REVISED — Historian filter QA process; ten-second test compliance; M5 milestone non-advancement; estimate gap contingency; C103 under-investment
- **Final Verdict**: ✅ CONFIRMED after 4 required revisions adopted

## Required Revisions Adopted
1. Interpretation card REPLACES event summary on dashboard (not supplements)
2. Historian filter QA gate established (PM writes → designer reviews → both sign off)
3. Mid-sprint checkpoint with explicit cut criteria added
4. Developer's estimates (44.5-51.5h) adopted as working plan

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| C98 spike | Validate LLM approach for event interpretation | Dev | Sprint 9, Day 1 |
| C98 dev | Hybrid interpretation engine (templates + LLM drill-down) | Dev | Sprint 9 |
| C101 | Comprehension Check Quiz (5-8 generic questions) | Dev + PM content | Sprint 9 |
| C103 Lite | First Visit Guide (2-card primer) | Dev | Sprint 9 |
| Historian QA | Write + review C98 interpretation templates | PM + Designer | Before C98 coding |
| Mid-sprint check | Week 1 checkpoint with cut criteria | PM | Sprint 9, Week 1 |

## Total Effort Estimate
- **PM estimate**: 35-42.5h
- **Developer estimate (adopted)**: 44.5-51.5h
- **Mid-sprint checkpoint**: End of week 1
- **Cut candidate**: C103 Lite (if behind schedule)

## Strategic Notes
- Sprint 9 does NOT address the 10 pre-existing L1 event-alert failures. Recommend Sprint 10 explicitly address M5 milestone remediation.
- C98's hybrid template+LLM approach is a bridge — plan for full LLM integration in Sprint 10 to maintain competitive differentiation (TW platforms adding AI narratives now).
- C34 (Company Story Timeline) remains the #1 priority for Sprint 10+ as the "purest historian differentiator."

## Next Cycle Handoff
🔧 Development → Sprint 9 (C98 + C101 + C103 Lite) → 🔍 Review Round 21 → Sprint 10 (C34 + M5 remediation)
