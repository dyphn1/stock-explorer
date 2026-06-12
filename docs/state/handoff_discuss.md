# Handoff – Discussion (Round 15)

## Summary
- **Topic**: Discussion (💡) — Round 15
- **Date**: 2026-06-21
- **Participants**: Product Manager, System Architect, Designer, Developer, Challenger
- **Sprint Context**: Sprint 4 complete → Sprint 5 prerequisites → Sprint 5 features → Post-Sprint 5 planning

## Features Evaluated (Post-Sprint 5 Direction)

### Idea Proposals
| ID | Feature | Effort | Direction | Sprint |
|----|---------|--------|-----------|--------|
| C42 | Stock Screener (Discovery Engine) | 16-24h | Discovery & Health | Sprint 6 |
| C43 | Company Snowflake Health Viz | 12-16h | Discovery & Health | Sprint 6 |
| C45 | Valuation Band Enhancement | 8-10h | Discovery & Health | Sprint 6 (flex to 7) |
| C83 | Investment Memo Template | 6-10h | Quick Win | Sprint 6 |
| C85 | Financial Wellness Check | 8-12h | Quick Win | Sprint 6 |
| C84 | Market Event Case Studies | 10-14h | Education | Sprint 7 |
| C82 | Animated Data Story (spike) | 5-8h | Engagement | Sprint 7 |
| D28 | Audio Infrastructure (spike) | 3-4h | Infrastructure | Sprint 7 |
| D-045 | Event-Triggered Content (spike) | 3-4h | Infrastructure (M5) | Sprint 7 |
| C63 | Audio Market Story (weekly) | 18-24h | Content | Sprint 8 (conditional) |
| D22 | Persistence Layer (P0) | 8-12h | Infrastructure | Sprint 8 |
| C81 | Historical Decision Scenarios | 14-22h | Education | Sprint 9+ |
| C64 | Community Q&A | 26-38h | Community | Sprint 9+ |
| C65 | Company Story Game | 22-32h | Engagement | Sprint 9+ |
| C68 | Financial Concept Storytelling | 30-44h | Education | Sprint 9+ |

### Deferred / Reconciled from Round 14
| ID | Feature | Status | Rationale |
|----|---------|--------|-----------|
| C66 | Conversational Tone | ✅ COMPLETE | Delivered in Sprint 4 |
| C65 | Company Story Game | 🔄 DEFERRED to Sprint 9+ | Content-heavy; C81-C85 validated first |
| C68 | Concept Storytelling (5+5) | 🔄 DEFERRED to Sprint 9+ | Content-heavy; C83/C84 validated first |
| D22 | Persistence Layer | ⚠️ P0 for C64 | Scheduled Sprint 8 (before C64) |

## Decisions Made
1. **Primary post-Sprint 5 direction: "Discovery & Health" (Option A)** — C42 Stock Screener + C43 Company Snowflake + C45 Valuation Band Enhancement as the Sprint 6 core
2. **Quick wins first in Sprint 6** — C83 (Investment Memo) and C85 (Wellness Check) are standalone pages with zero dependencies, providing immediate value while C42/C43/C45 are built
3. **Direction B (Dual-Mode Disclosure) REJECTED** — Contradicts historian vision; Direction A's card-count limit (max 5 cards/page) solves page bloat more simply
4. **Direction C (Color-Coded Narrative) deferred to Phase 2** — Pending Daniel approval of expanded color palette (purple/teal)
5. **Sprint 7 is the "de-risk" sprint** — Three spikes (C82 animation, D28 audio, D-045 event-triggered content) run in parallel with C84 case studies
6. **C63 Audio is conditional** — Only builds in Sprint 8 if D28 spike succeeds. Fallback: C65 or C68
7. **Content cap budget: 22-27 items remaining** after all planned features through Sprint 9+
8. **D37 _sections.py split is a HARD PREREQUISITE** for Sprint 6 — C43 cannot start until D37 is complete
9. **D-045 spike added for M5 milestone** — Event-triggered content regeneration investigation in Sprint 7
10. **C45 is the Sprint 6 flex item** — If capacity runs low, C45 slips to Sprint 7

## Design Directions Adopted
- **Direction A: "PPT-Style 2.0"** — Progressive Card Stack (hero → story → action cards, max 5 cards/page)
- **New card types needed**: `_story_card()` (green border), `_scenario_card()`, `_study_card()`, `_expert_card()`
- **Design system updates needed**: Section 3.3 (new card types), Section 5.1 (clarify "one key point = one narrative arc"), Section VI (add card count rule)

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| D-039/040/041 | Complete Sprint 5 prerequisites | Dev | Before Sprint 5 features |
| D37 | Split _sections.py monolith | Dev | Before Sprint 6 C43 |
| C83 | Build Investment Memo Template page | Dev | Sprint 6 |
| C85 | Build Financial Wellness Check page | Dev | Sprint 6 |
| C42 | Build Stock Screener page + service | Dev | Sprint 6 |
| C43 | Build Company Snowflake visualization | Dev | Sprint 6 (after D37) |
| C45 | Enhance Valuation Band chart | Dev | Sprint 6 (flex to 7) |
| C84 | Build Market Event Case Studies page | Dev + PM/Designer content | Sprint 7 |
| C82 spike | Test Streamlit + CSS animation feasibility | Dev | Sprint 7 |
| D28 spike | Test audio infrastructure feasibility | Dev | Sprint 7 |
| D-045 spike | Investigate event-triggered content regeneration | Dev/Architect | Sprint 7 |
| D-042/043/044 | Batch debt cleanup | Dev | Sprint 7 |
| Design system update | Add new card type specs to design_system.md | Designer | Before Sprint 6 |

## Challenger 3-Round Summary
- **Round 1 (Feature Direction)**: 7 challenges raised — C42/C45 sequencing, Direction B contradiction, content cap math, D28 spike timing, Round 14 reconciliation, M5 gap, D37 timing
- **Round 2 (Priority)**: Re-challenges on page bloat pretext, conservative C83/C85 sequencing, C82 spike scope, Sprint 9+ parking lot, Round 14 silent drops
- **Round 3 (Goal Alignment)**: M5 milestone gap confirmed, role recommendation contradictions identified, 5 overlooked risks flagged
- **PM Response**: All 7 contradictions accepted and resolved in revised plan
- **Final Verdict**: ✅ CONFIRMED — All contradictions resolved, plan ready for implementation

## Watch Flags (Non-Blocking)
1. **C42 scope creep** — Monitor for scope beyond 16h in Sprint 6
2. **D37 critical path** — If D37 slips, C43 slips, cascading to Sprint 7
3. **Sprint 5 capacity** — 44.8-55.8h exceeds proven velocity (35-43h)
4. **C82 content impact** — If spike greenlights full build, re-evaluate content cap (20-50 items not in ledger)

## New Architecture Debt
- D-045: Event-triggered content regeneration — Medium (spike in Sprint 7)
- D-046: Audio service layer — Medium (spike in Sprint 7, full build Sprint 8)
- D-047: Animation framework for C82 — Medium (spike in Sprint 7)

## Competitor Insights Addressed
- Stock Screener (C42) — 財報狗 #1 feature, biggest competitive gap
- Company Snowflake (C43) — Simply Wall St/Morningstar/Stockopedia visual health scores
- Valuation Band (C45) — 財報狗 most popular chart, historical context
- Investment Memo (C83) — 長投學堂 proves demand for structured reflection
- Wellness Check (C85) — Cleo/Plum/Bloom prove behavioral finance demand
- Case Studies (C84) — No TW competitor has interactive case studies

## Next Cycle Handoff
Next: 🔧 Development → Sprint 5 prerequisites (D-039 + D-040 + D-041 + D37) → Sprint 5 features (C71 + C74 + C73) → Sprint 6 (C83 + C85 + C42 + C43 + C45)
