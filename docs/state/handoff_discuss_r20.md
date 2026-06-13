# Handoff – Discussion (Round 20)

## Summary
- **Topic**: Discussion (💡) — C36-C47 Feature Candidates: What needs building vs. what's already done?
- **Date**: 2026-06-15 (Round 20 Discussion completed)
- **Sprint Status**: Sprint 10 ✅ COMPLETE → Sprint 11 planned → Sprint 12-14 revised

## Key Finding: 9 of 12 Features Already Built

Architect, Designer, and Developer all confirmed through code review that **9 of 12 competitor-inspired features (C37-C45) are already implemented** in both service and page layers:

| Status | Features |
|--------|----------|
| ✅ Shipped | C37 Key Takeaways, C38 Compare Stories, C39 Delta Card, C41 Read Next, C42 Stock Screener, C43 Snowflake Health, C44 Risk Analysis, C45 Valuation Band |
| 🟡 Partial | C40 Beginner/Expert Mode (simple mode exists, no navbar toggle) |
| 🔴 New Build | C36 Revenue Tree, C46 Moat Analysis, C47 Education Academy |

## Idea Proposals

| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| Sprint 12 | Polish shipped features + C40 + user feedback | Dev + Designer | 📋 Planned |
| Sprint 13 | C36 Revenue Tree + C46 Moat + C47 content start | Dev + Architect | 📋 Planned |
| Sprint 14 | C47 Part 2 + C40 polish + user validation | Dev + Designer | 📋 Pending |

## Decisions Made

### Challenger Verdict: ✅ CONFIRMED (with 9 revisions)

**Direction A: "Ten-Second Company Page" (Sprint 12) — REVISED**
- QA/polish C37/C39/C43/C45 with "story first" QA gate
- Add Business Card page information hierarchy redesign (4-6h)
- C40 navbar toggle revised to 10-16h (was 6-10h)
- Add user feedback collection mechanism (2-4h)
- Architecture debt gate: D16/D24 must be complete before C40 starts
- **Revised effort: 26-38h** (was 20-30h)

**Direction B: "Historian's Deep Dive" (Sprint 13) — REVISED**
- C36 Revenue Tree (12-16h) with fallback to pie chart if data unavailable
- C46 Moat Analysis (14-18h) with template-based fallback for non-top-20
- C47 content creation starts in parallel (8-12h content)
- Data source validation gate in Week 1 for C36
- **Revised effort: 30-40h** (was 26-34h)

**Direction C: "Education Platform" (Sprint 14) — REVISED**
- Split C47: Part 2 only (remaining lessons + quiz integration)
- C40 polish and edge case handling
- User validation (5 beginner testers per sprint)
- **Revised effort: 20-28h** (was 22-32h)

### 9 Challenger Revisions

1. Sprint 12 hours increased to 26-38h (information hierarchy + C40 correction + user feedback)
2. C40 hours revised 6-10h → 10-16h (cross-section coupling)
3. Architecture debt gate added: D16/D24 must complete before C40
4. Sprint 13 scope includes C47 content creation kickoff
5. Sprint 14 scope includes user validation
6. User validation added: 5 beginner testers per sprint
7. Content creation needs: clear owner + timeline + review process
8. C36 fallback: degrade to existing pie chart if data unavailable
9. Beginner mode architecture: define C36/C46 presentation in Sprint 12

### Revised Sprint Plans

| Sprint | Items | Hours | Key Gate |
|--------|-------|-------|----------|
| Sprint 12 | C37/C39/C43/C45 QA + info hierarchy + C40 + user feedback | 26-38h | D16/D24 complete |
| Sprint 13 | C36 + C46 + C47 content kickoff | 30-40h | C36 data Week 1 |
| Sprint 14 | C47 Part 2 + C40 polish + user validation | 20-28h | Content review pass |

**Revised total: ~76-106h across 3 sprints** (was 68-96h)

### Key Risks Identified

1. **Content creation bottleneck**: 19-27h pure content creation across C36/C46/C47 — needs dedicated owner
2. **C36 data source**: FinMind lacks hierarchical segment data — manual curation for top-20, fallback required
3. **C40 cross-section coupling**: Affects all pages — D24 must complete first
4. **Feature fatigue**: 9 features shipped but never tested with real beginners — user validation critical
5. **Beginner mode architecture**: C36/C46 must have defined presentation in beginner mode

## Action Items

| Item ID | Description | Owner | Due |
|---------|-------------|-------|-----|
| R20-01 | Sprint 12 architecture debt gate check (D16/D24) | Architect | Sprint 12 Day 1 |
| R20-02 | C36 data source validation (Week 1 Sprint 13) | Developer | Sprint 13 Week 1 |
| R20-03 | C36/C46 template-based fallback content | Designer | Sprint 13 |
| R20-04 | User feedback collection UI (Sprint 12) | Designer + Dev | Sprint 12 |
| R20-05 | Content creation owner + timeline assignment | PM | Sprint 13 planning |
| R20-06 | Beginner mode architecture definition | Architect + Designer | Sprint 12 |
| R20-07 | 5 beginner user testers recruited per sprint | QA | Each sprint |

## Analysis Files

- **Architect analysis**: docs/analysis/feasibility_c36_c47.md
- **Designer analysis**: docs/design/design_review_c36_c47.md
- **Developer analysis**: docs/design/developer_c36_c47_analysis.md
- **Challenge log**: docs/design/challenge_log_c36_c47.md

## Next Cycle

🔍 Review Round 24 → Sprint 12 (Polish + C40 + User Feedback)
