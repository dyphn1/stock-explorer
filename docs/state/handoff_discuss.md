# Handoff – Discussion (Round 17)

## Summary
- **Topic**: Discussion (💡) — Round 17: Sprint 8+ Feature Directions
- **Date**: 2026-06-13
- **Participants**: Product Manager, System Architect, Designer, Developer, Challenger
- **Sprint Context**: Sprint 7 complete → Sprint 8 (D22 + D28 + C63 conditional) → Sprint 9+ planning

## Critical Discovery: Backlog Stale
During analysis, the Architect, Designer, and Developer all independently confirmed:
- ✅ **C37 (Key Takeaways)** — Already implemented (`key_takeaways.py` + `_render_takeaways()`)
- ✅ **C39 (What Changed Recently)** — Already implemented (`delta_engine.py` + `_render_deltas()`)
- ✅ **C41 (Read Next Recommendations)** — Already implemented (`_render_read_next()` in `_story.py`)
- ✅ **C42 (Stock Screener)** — Already implemented (`stock_screener.py` + `stock_screener_service.py`)
- ❌ **C40 (Beginner/Expert Mode)** — Previously cut in favor of "beginner mode by default"

**Net new features remaining: 6** (C34, C81, C63, C65, C64, C68), not 10+ as backlog suggested.

## Idea Proposals
| ID | Feature | Effort | Direction | Sprint |
|----|---------|--------|-----------|--------|
| C34 | Company Story Timeline (top 15 stocks) | 20-28h | Core Differentiator | Sprint 9 |
| C81 | Interactive Historical Scenarios | 12-16h | Enhancement | Sprint 9 |
| D22 | Persistence Layer + C64 feasibility | 8-12h | Infrastructure P0 | Sprint 8 |
| D28 | Audio Infrastructure spike | 3-4h | Infrastructure | Sprint 8 |
| C63 | Audio Market Story (conditional) | 20-28h | Conditional | Sprint 8 |
| C68 | Financial Concept Storytelling | 32-44h | Education | Sprint 10 |
| C65 | Company Story Game | 24-32h | Engagement | Sprint 11+ |
| C64 | Community Q&A (if D22 ✓) | 30-40h | Community | Sprint 11+ |

## Decisions Made
1. **C34 is the #1 priority** after Sprint 8 infrastructure — the purest "historian" differentiator, no TW competitor has it
2. **C81 moves to Sprint 9** alongside C34 — leverages narrative patterns from C34's `narrative_engine.py`
3. **C68 before C64** — education before community (Challenger Round 1 correction)
4. **C63 remains conditional** — if D28 spike fails, D-049/D-050 debt cleanup fills Sprint 8
5. **C34 scoped to top 15 stocks** — content cap compliance (100 items max)
6. **D22 includes C64 feasibility test** — can't plan 30-40h feature on unproven infrastructure (Challenger Round 3)
7. **Content creation effort explicit** — 20-30h PM/Designer time for C34 narratives + C68 stories was excluded from dev estimates

## Challenger 3-Round Summary
- **Round 1** (Feature Direction): ⚠️ PARTIALLY REVISED — C42 missing (already built), C64/C68 sequence inverted, C63 needs fallback
- **Round 2** (Priority): ⚠️ REVISED — C34 content scope unbounded, Sprint 8 too thin without fallback
- **Round 3** (Goal Alignment): ⚠️ REVISED — content creation effort excluded, D22 must test C64 feasibility
- **Final Verdict**: ✅ CONFIRMED after all 6 required revisions adopted

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| D22 | Persistence Layer + C64 feasibility test | Dev | Sprint 8 |
| D28 | Audio Infrastructure spike | Dev | Sprint 8 |
| C63 | Audio Market Story (if D28 ✓) | Dev + PM content | Sprint 8 |
| C34 | Company Story Timeline (top 15 stocks) | Dev + PM content | Sprint 9 |
| C81 | Interactive Historical Scenarios | Dev | Sprint 9 |
| C68 | Financial Concept Storytelling | Dev + PM/Designer content | Sprint 10 |
| C65 | Company Story Game | Dev + Designer | Sprint 11+ |
| C64 | Community Q&A (if D22 ✓) | Dev | Sprint 11+ |
| Backlog cleanup | Mark C37/C39/C41/C42 as Done in issues.md | PM | This cycle |

## Total Effort Estimate
- **Dev effort**: 156-234h (Sprints 8-11+)
- **Content creation**: 20-30h (parallel, C34 + C68 + C63 scripts)
- **PM/Designer review**: 8-12h (narrative QA gate)
- **Total**: 184-276h at 20-30h/sprint = 7-10 sprints = 6-12 months

## Next Cycle Handoff
🔧 Development → Sprint 8 (D22 + D28 + C63 conditional) → 💡 Discussion Round 18 → Sprint 9 (C34 + C81)
