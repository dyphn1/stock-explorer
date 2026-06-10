# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Round 8
- **Date**: 2026-06-13
- **Participants**: PM, Architect, Developer, Designer, Challenger
- **Theme**: Round 8 Feature Proposals (C36-C41) from Competitor Research

## Idea Proposals
| ID | Feature | Owner | Status |
|----|---------|-------|--------|
| C37 | Key Takeaways Summary Card | Dev | ✅ Approved — Sprint 2 |
| C39 | What Changed Recently Delta Card | Dev | ✅ Approved — Sprint 3 |
| C41 | Read Next Recommendations | Dev | ✅ Approved — Sprint 3 |
| C38 | Compare Stories Side-by-Side (Phase 1) | Dev+Arch | ✅ Approved — Sprint 3 |
| C36 | Visual Revenue Tree (top 10 stocks) | Dev | ✅ Approved — Sprint 4 |
| C40 | Beginner/Expert Mode Toggle | — | ❌ CUT — replaced with "beginner by default" design principle |

## Decisions Made
1. **C37 (Key Takeaways) is the #1 priority** — directly addresses the ten-second test. Uses curated templates for top 20 stocks as PRIMARY approach, rule-based as fallback. 6.5h.
2. **C40 (Mode Toggle) is CUT** — replaced with "beginner mode by default" design principle. Saves 10-15h, avoids Zone A violation, eliminates maintenance burden.
3. **C38 (Compare Stories) moved to Sprint 3** — Phase 1 structured comparison only (no LLM dependency). Most historian-aligned feature; can't risk Sprint 5 deferral. 8-10h.
4. **C39 (What Changed) deferred to Sprint 3** — reduces Sprint 2 overload. 5.5h.
5. **C36 (Revenue Tree) ships with top 10 stocks only** — reduces data curation from 4-5h to 2-3h. ~8-9h total.
6. **C41 (Read Next) confirmed for Sprint 3** — reuses existing group_structure and peer_comparison data. 6.5h.
7. **Total new feature scope: ~40h base (with C40 cut, ~30h net new)** — still requires careful sprint capacity management.
8. **Core values gap identified**: #3 (Adaptive) and #5 (Benchmark) are underrepresented. C39 covers adaptation; C38 covers benchmarking. No additional features needed but awareness is important.
9. **Business card page overload risk**: C37 (Sprint 2) → C39+C41 (Sprint 3) → C36 (Sprint 4). One new card per sprint to preserve ten-second test.
10. **Ten-second test verification time**: 2-3h per feature must be added to sprint estimates (not yet included).

## Challenger's 3-Round Summary
| Round | Focus | Resolution |
|-------|-------|------------|
| 1 | Feature Direction | C40 cut, C37 curated-first approach, C38 most historian-aligned |
| 2 | Priority | C38 moved to Sprint 3, C39 deferred to Sprint 3, C36 top 10 only |
| 3 | Goal Alignment | Core values #3/#5 underrepresented; business card page overload risk; no verification time in estimates |

## Final PM Decision (Challenger ✅ Confirmed after revisions)

| Sprint | Features | Base Hours | With 50% Buffer | Core Value |
|--------|----------|------------|-----------------|------------|
| 0 | Design + Quick wins | 2.7h | 4h | #2 PPT |
| 1 | C28 Spike + LLM | 5h | 7.5h | #1 Story |
| 2 | D02 + C31 + C37 | 24.5h | 37h | #1 Story, #3 Adaptive |
| 3 | C28 Full + C38 P1 + C39 + C41 | 43h | 64.5h | #1 Story, #4 Knowledge |
| 4 | C14 + C36 | 15.5h | 23h | #5 Benchmark, #1 Story |
| 5 | C29 + Buffer | 10h | 15h | #4 Knowledge |
| **Total** | | **~101h** | **~151h** | |

**Note**: Sprint 3 is heavily loaded (43h base). C28 is primary; C38/C39/C41 are smaller additions. If capacity is exceeded, C39 or C41 can shift to Sprint 4.

## New Tech Debt (carried from previous)
- NEW-G18: events.yaml schema extension (2-3h) — before C28 Sprint 3
- NEW-G19: User prefs abstraction (2-3h) — before Sprint 3
- NEW-G20: analogy_engine coverage gap (4-6h) — before C29 Sprint 5

## Pending Daniel's Decision
- #8: Roadmap approval — 5-sprint plan, ~109h (existing) + ~40h (new) = ~151h buffered
- #10: C31 content strategy — manual vs template vs LLM
- #14: Sprint 3 capacity concern — 43h base is very high. Options: extend to Sprint 6, or defer C39/C41 to Sprint 4.

## Next Cycle Handoff
Next: 🔧 Development → Sprint 1 (C28 Spike + LLM Architecture)
Read `docs/state/handoff.md` for Sprint 1 entry point.
