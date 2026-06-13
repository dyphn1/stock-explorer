# Handoff – Discussion (Round 29)

## Summary
- **Topic**: Discussion (💡) — Sprint 14 Scope Validation (C40 + C126 + C47 + C125 stretch)
- **Date**: 2026-06-18 (Round 29 Discussion completed)
- **Sprint Status**: Sprint 13b ✅ COMPLETE → Sprint 14 CONFIRMED

## Team Proposals

### Architect Recommendation
- **Option C (preferred):** C126 Moat Comparison + C40 Mode Toggle Propagation + C47 Education Academy Spike
- C126: 10-14h, all infrastructure exists (C46 complete, moat_data.yaml has 20 stocks)
- C40: 4-6h, C105 already built — needs propagation to all pages
- C47: 10-12h, 3-5 lesson MVP prototype
- C123 deferred (no FinMind data source), C125 deferred (lower priority)

### Designer Recommendation
- **C40 Mode Toggle first priority** — lowest-risk, highest-leverage, enables all others
- C125 Segment Profitability #2 priority (2-3h enhancement to C36)
- C126 Moat Comparison #3 — grouped horizontal bar chart (not radar)
- C47 Education Academy #5 — Phase 0 approach (skeleton + 2 lessons)
- Key concern: D-005 Business Card overload must be addressed

### Developer Estimate
- **C47 Education Academy:** 33-42h total (service: 12-18h, view: 8-12h, content: 8-12h, integration: 5h)
- **C40 Mode Toggle:** 0h base (already built) + 4-6h propagation
- **C123 Revenue Geography:** 20-32h — NOT FEASIBLE (no FinMind data)
- **C125 Segment Profitability:** 12-22h — conditionally feasible
- **C126 Moat Comparison:** 14-24h — HIGHLY FEASIBLE (all infrastructure exists)

## Challenger Verdict: ✅ CONFIRMED with 7 revisions

### Revisions Required

| # | Revision | Impact |
|---|----------|--------|
| 1 | **Execution order: C40 → C126 → C47** | C40 first unblocks beginner-friendly views for all features |
| 2 | **C47 scope: 5 complete lessons** (min 3), all passing ten-second test | Reduces scope creep risk |
| 3 | **C125 added as stretch goal** if C40 + C126 complete under budget | Analysis depth ↑ |
| 4 | **C47 quality gate**: Every lesson must pass ten-second test before deployment | Content quality ↑ |
| 5 | **C40 + D-005 alignment**: Business Card ≤ 5 sections in Beginner Mode | Page overload resolved |
| 6 | **Session state disclaimer** in C47 + Sprint 15 persistence commitment | User expectation managed |
| 7 | **C47 done criteria**: 7-point checklist before feature marked complete | Completion clarity ↑ |

### Round Summaries
- **Round 1 (Feature Direction):** ✅ Passed — C126 estimate discrepancy resolved, C47 scope defined as 5 complete lessons, C125 vs C126 content burden clarified, C40 propagation complexity accepted, C47 vision alignment conditioned on example-first lessons
- **Round 2 (Priority):** ✅ Passed — Execution order revised to C40→C126→C47, C47 timing accepted as strategic investment, budget buffer analysis (realistic 28h), strategic tradeoff made explicit, C126 confirmed as TW market white space
- **Round 3 (Goal Alignment):** ✅ Passed — Designer override justified (sprint coherence > individual priority), quality gate established, session_state accepted with Sprint 15 commitment, D-005 remediation via C40, C47 done criteria defined

## Final Sprint 14 Plan (Post-Challenger)

### Sprint 14 — Education + Comparison + Accessibility (28-40h expected)

| Item | Hours | Order | Notes |
|------|-------|-------|-------|
| C40 Mode Toggle Propagation | 4-6h | 1st | Move C105 to navbar, propagate to all 6 pages, remove old C105 toggle |
| C126 Moat Comparison | 10-14h | 2nd | Grouped horizontal bar chart on Peer Comparison page, reuse C46 scoring |
| C47 Education Academy | 10-12h | 3rd | 5 complete lessons (min 3), all passing ten-second test, session_state progress |
| C125 Segment Profitability | 2-3h | Stretch | Margin overlay toggle on C36, only if budget allows |
| **TOTAL (core)** | **24-32h** | | Realistic 28h, fits 26-38h budget |
| **TOTAL (with stretch)** | **26-35h** | | Still within budget |

### Go/No-Go Gates
- **After C40 + C126 (~17h):** If on track, proceed with C47. If over budget, reduce C47 to 3 lessons.
- **C47 quality gate:** Each lesson must pass ten-second test before deployment. Launch with min 3 lessons.

### Fallback
- C47: Reduce to 3 lessons (from 5), still deployable
- C125: Defer to Sprint 15 if budget tight

## Key Risks
1. **C47 content creation bottleneck** (10h for 5 lessons): Mitigated by quality gate — launch with fewer lessons rather than subpar content
2. **C40 propagation complexity** (6 pages × content decisions): Mitigated by designer's detailed spec already completed
3. **Session state fragility** (C40 mode + C47 progress lost on reload): Mitigated by Sprint 15 persistence commitment + user-facing disclaimer
4. **D-005 overload persists if C40 incomplete:** C40 IS the D-005 remediation — ≤ 5 sections in Beginner Mode

## Action Items

| Item ID | Description | Owner | Due |
|---------|-------------|-------|-----|
| R29-01 | C40 Mode Toggle propagation to all pages | Dev | Sprint 14 Day 1-2 |
| R29-02 | C126 Moat Comparison grouped bar chart | Dev | Sprint 14 Day 2-4 |
| R29-03 | C47 lessons.yaml 5 lessons with ten-second test | Dev + Designer | Sprint 14 Day 3-6 |
| R29-04 | C47 education_academy.py page with progress sidebar | Dev | Sprint 14 Day 5-7 |
| R29-05 | C125 margin overlay toggle (stretch) | Dev | Sprint 14 (if budget) |
| R29-06 | Go/No-Go gate after C40+C126 | PM | Sprint 14 Day 4 |
| R29-07 | C47 quality gate: ten-second test per lesson | Designer | Sprint 14 Day 6 |
| R29-08 | Session state disclaimer banner in C47 | Dev | Sprint 14 Day 5 |

## Next Cycle
✅ Sprint 14 planned (C40 + C126 + C47 + C125 stretch) → 🔧 Development Sprint 14 → 🔍 Review Round 30

## Analysis Files
- **Architect analysis:** docs/design/architect_discussion_r29.md
- **Designer analysis:** docs/design/designer_discussion_r29.md
- **Developer estimate:** docs/design/developer_discussion_r29.md
- **Challenge log:** docs/design/challenge_r29.md
