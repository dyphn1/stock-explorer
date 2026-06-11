# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Round 10
- **Date**: 2026-06-16
- **Participants**: PM, Architect, Developer, Designer, Challenger
- **Theme**: Round 9 Feature Proposals (C42, C44, C46, C47) from Competitor Research

## Idea Proposals
| ID | Feature | Owner | Status |
|----|---------|-------|--------|
| C42 | Stock Screener / Discovery Engine | Dev | ✅ Approved — Sprint 4 |
| C44 | "What Could Go Wrong" Risk Analysis | Dev | ✅ Approved — Sprint 3 (MVP) |
| C46 | Moat Analysis | Dev | ✅ Approved — Sprint 5 |
| C47 | Education Academy Phase 1 | Dev | ✅ Approved — Sprint 5 (5 lessons) |
| C34 | Company Story Timeline | Dev | ✅ Scheduled — Sprint 5 (with C46) |

## Decisions Made
1. **Direction A (C42 + C44) confirmed with revisions** — C42 is the P1 enabler feature (gets users to companies), C44 is the unique historian differentiator (risk analysis with historical evidence).
2. **C42 is P1 enabler, not P1 vision** — C34 (Company Story Timeline) remains the true P1 vision feature. C42 is an enabler that transforms the product from lookup to discovery.
3. **Sprint plan confirmed**: Sprint 3 = C41 + C38 + C44-MVP + R5 + R1; Sprint 4 = C36 + C42; Sprint 5 = C34 + C46 OR C47 Phase 1.
4. **R1 upgraded to P0** — financial_metrics extraction (2.5-4h) must be done before/alongside C44 in Sprint 3. Without it, C44 adds a 5th copy of duplicated financial logic.
5. **C44 must use progressive disclosure** — collapsible `st.expander()` on the business card page, not a full card section. The page already has 13 sections; adding a 14th without collapse violates the ten-second test.
6. **C44 tone risk elevated to HIGH** — must use "過去發生" / "歷史證據" / "觀察指標" language, never "可能發生" / "預測" / "建議". Tone review checkpoint required before shipping.
7. **C34 explicitly scheduled for Sprint 5** — C34 is the purest expression of "historian" positioning (Round 7 identified it as "#1 thing competitors DON'T have"). C38 (Sprint 3) creates prerequisite data structures.
8. **C47 split into two phases** — Phase 1 (Sprint 5, ~12h) = 5 pilot lessons. Phase 2 (post-plan) = remaining lessons + progress tracking.
9. **Sprint 3 contingency defined** — if C44-MVP exceeds 14h, reduce to 2 risk dimensions. C41 is next candidate for reduction.
10. **R3 must be verified before Sprint 4** — C42 depends on batch API pattern. If R3 wasn't done in Sprint 2, do it first in Sprint 4.

## Challenger's 3-Round Summary
| Round | Focus | Resolution |
|-------|-------|------------|
| 1 | Feature Direction | PARTIALLY RESOLVED — C42 is P1 enabler (not P1 vision). C34 is the true P1 vision feature. Revision: explicitly acknowledge C34 as vision P1. |
| 2 | Priority | REQUIRES REVISION — Architect/developer sprint plan contradiction resolved (C44 in Sprint 3, C42 in Sprint 4 per handoff). R1 upgraded to P0. |
| 3 | Goal Alignment | REQUIRES REVISION — C44 must use progressive disclosure. C44 tone risk elevated to HIGH. C34 scheduled for Sprint 5. |

## Final PM Decision (Challenger ✅ Confirmed after revisions)

| Sprint | Features | Base Hours | With Buffer | Core Value |
|--------|----------|------------|-------------|------------|
| 3 | R1 + C44-MVP + C41 + C38 + R5 | 33-41h | 50h | #1 Story, #3 Adaptive |
| 4 | C36 + C42 | 27-34h | 41h | #4 Knowledge, #1 Story |
| 5 | C34 + C46 or C47 P1 | 32-42h | 48h | #1 Story, #4 Knowledge |

**Note**: Sprint 3 includes R1 (financial_metrics extraction) as P0. C44 scoped to MVP (3 risk dimensions, top 20 stocks). Sprint 5 priority between C34 and C46/C47 Phase 1 pending Daniel's input.

## New Tech Debt
- R1 (financial_metrics extraction) — P0, must do before/alongside C44 in Sprint 3
- R3 (batch API verification) — must verify before C42 in Sprint 4
- Business card page architecture doc needed — define "above the fold" boundary

## Pending Daniel's Decision
1. **C34 vs C46 priority for Sprint 5** — C34 is the historian vision feature; C46 is unique differentiator. Which is more important?
2. **C47 Phase 1 scope** — 5 pilot lessons (12h) or 10 lessons (20h)? Recommendation: 5 lessons to validate quality.
3. **Business card page "above the fold" definition** — C37 + C43 are the ten-second answer; everything else below fold or in tabs. Approve?

## Next Cycle Handoff
Next: 🔧 Development → Sprint 3 (R1 + C44-MVP + C41 + C38 + R5)
Read `docs/state/handoff.md` for Sprint 3 entry point.

## Full Discussion Docs
- Architect: `docs/design/architect_discussion_r10.md`
- Designer: `docs/design/designer_discussion_r10.md`
- Developer: `docs/design/developer_discussion_r10.md`
- Challenger: `docs/design/challenger_discussion_r10.md`
