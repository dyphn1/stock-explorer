# ⚔️ Challenger Round 15 — Team Response & Revised Plan

> **Author**: Product Manager
> **Date**: 2026-06-21
> **Cycle**: Discussion Round 15
> **Context**: Responding to Challenger's 3-round challenge on the post-Sprint 5 feature plan.

---

## Challenger Issues & Team Resolutions

### Issue 1: C42 Stock Screener Buried in Sprint 7
**Challenger finding**: C42 (biggest competitive gap — 財報狗 #1 feature) deferred to Sprint 7 behind C83, C85, C84, and C82 spike. Both Architect and Developer recommended earlier.

**Resolution**: ✅ **ACCEPTED.** C42 moves to Sprint 6. Revised Sprint 6: C83(8h) + C85(10h) + C42(16h) = 34h (within proven 35-43h velocity). D-042/043/D-044 debt batch moves to Sprint 7.

### Issue 2: C45 Valuation Band Enhancement Deferred to Sprint 8
**Challenger finding**: C45 (easiest Option A feature, 8-10h, enhances existing chart) paired with highest-risk C63 in Sprint 8. Should be with C43 in Sprint 6.

**Resolution**: ✅ **ACCEPTED.** C45 moves to Sprint 6. Revised Sprint 6: C83(8h) + C85(10h) + C42(16h) + C45(9h) = 43h (at velocity ceiling but manageable since C45 is low-risk enhancement). Alternatively, C45 can slip to Sprint 7 if Sprint 6 runs long — it's not on the critical path.

### Issue 3: D28 Audio Spike in Sprint 8 (Same Sprint as C63 Build)
**Challenger finding**: D28 spike should be BEFORE committing C63 to a sprint, not concurrent.

**Resolution**: ✅ **ACCEPTED.** D28 spike moves to Sprint 7 alongside C82 spike. Sprint 7 becomes: C84(12h) + C82 spike(6h) + D28 spike(4h) = 22h — comfortable capacity.

### Issue 4: Direction B (Dual-Mode Disclosure) Contradicts Historian Vision
**Challenger finding**: Beginner/Expert toggle creates tiered information architecture contradicting "historian IS the complete perspective." No competitor uses this pattern. Direction A's card-count limit (max 5 cards/page) already solves page bloat.

**Resolution**: ✅ **ACCEPTED.** Direction B is **REJECTED** for now. Rely on Direction A's card-count discipline (max 5 cards/page). Re-evaluate Direction A after Sprint 5 features ship — if page bloat is empirically observed, revisit.

### Issue 5: Round 14 Decisions Silently Dropped
**Challenger finding**: C65 (Company Story Game, Sprint 7), C68 (Financial Concept Storytelling, Sprint 6-7), D22 (Persistence Layer, Sprint 6 P0) from Round 14 are absent from Round 15 plan.

**Resolution**: ✅ **RECONCILED.** Status of each:
- **C66 (Conversational Tone)**: ✅ COMPLETED in Sprint 4 (per handoff.md). No action needed.
- **C65 (Company Story Game)**: 🔄 **DEFERRED to Sprint 9+.** Content-heavy (requires company_facts.yaml expansion to 15+ companies). Lower priority than C81-C85 from Round 16 which address competitive gaps more directly.
- **C68 (Financial Concept Storytelling, 5+5 concepts)**: 🔄 **DEFERRED to Sprint 9+.** Content-heavy (10 lessons). C83 (Investment Memo) and C84 (Case Studies) from Round 16 are lighter-weight education features that should be validated first.
- **D22 (Persistence Layer, P0)**: ⚠️ **REMAINS P0 for C64.** C64 is Sprint 9+, so D22 is scheduled for Sprint 8 (before C64). This is consistent with the Round 14 decision.

### Issue 6: M5 Milestone Gap (No Event-Triggered Content Update)
**Challenger finding**: M5 requires content updated within 24h of major events. No mechanism in the plan.

**Resolution**: ✅ **ACCEPTED.** Add **D-045 spike** (event-triggered content regeneration) in Sprint 7. Scope: 3-4h investigation of whether existing event dashboard data can trigger content regeneration flags. This is a pre-requisite for M5 and should be investigated before C63/C81/C64 consume all sprint capacity.

### Issue 7: D37 _sections.py Split Timing
**Challenger finding**: D37 must be a hard Sprint 5 prerequisite, not a maybe, before C43 adds business card sections in Sprint 6.

**Resolution**: ✅ **ACCEPTED.** D37 is confirmed as a **HARD PREREQUISITE** for Sprint 6. C43 cannot start until D37 is complete.

---

## Revised Post-Sprint 5 Feature Plan (Post-Challenger)

### Sprint 5 (Current — Unchanged)
| Item | Effort | Type |
|------|--------|------|
| D-039 + D-040 + D-041 prerequisites | 3.3h | Debt |
| D-037 fix | 0.3h | Debt |
| C71 Study Log | 8-12h | Feature |
| C74 Historical Scenarios | 10-16h | Feature |
| C73 Expert Analysis | 14-20h | Feature |
| D-038 fix | 1.5h | Debt |
| **D37 _sections.py split** | **2-3h** | **Debt (HARD PREREQ)** |
| **Total** | **44.8-55.8h** | |

### Sprint 6 (Revised)
| Item | Effort | Type | Content Items |
|------|--------|------|---------------|
| C83 Investment Memo Template | 6-10h | Feature | 0 |
| C85 Financial Wellness Check | 8-12h | Feature | 1 |
| C42 Stock Screener | 16-24h | Feature | 0 |
| C43 Company Snowflake | 12-16h | Feature | 0 |
| C45 Valuation Band Enhancement | 8-10h | Feature | 0 |
| **Total** | **50-72h** | | **1** |

**Note**: Sprint 6 is at the high end of capacity. C45 is the "flex" item — if the sprint runs long, C45 slips to Sprint 7.

### Sprint 7 (Revised)
| Item | Effort | Type | Content Items |
|------|--------|------|---------------|
| C84 Market Event Case Studies | 10-14h | Feature | 5-10 |
| C82 Animated Data Story spike | 5-8h | Spike | 0 |
| D28 Audio Infrastructure spike | 3-4h | Spike | 0 |
| D-045 Event-Triggered Content spike | 3-4h | Spike | 0 |
| D-042/043/D-044 debt cleanup | 2.3h | Debt | 0 |
| C45 Valuation Band (if not done Sprint 6) | 8-10h | Feature | 0 |
| **Total** | **31-40h** | | **5-10** |

### Sprint 8 (Revised)
| Item | Effort | Type | Content Items |
|------|--------|------|---------------|
| C63 Audio Market Story | 18-24h | Feature | 12 (quarterly start) |
| D22 Persistence Layer | 8-12h | Debt (P0) | 0 |
| **Total** | **26-36h** | | **12** |

**Note**: C63 is conditional on D28 spike success. If D28 fails, C63 is replaced with C65 (Company Story Game) or C68 (Concept Storytelling).

### Sprint 9+ (Revised)
| Item | Effort | Type | Content Items |
|------|--------|------|---------------|
| C81 Historical Decision Scenarios | 14-22h | Feature | 20 (scoped down) |
| C64 Community Q&A | 26-38h | Feature | UGC (exempt) |
| C65 Company Story Game | 22-32h | Feature | 15 |
| C68 Financial Concept Storytelling | 30-44h | Feature | 10 |
| **Total** | **92-136h** | | **45** |

---

## Content Cap Ledger (Post-Revision)

| Sprint | Feature | Content Items | Running Total |
|--------|---------|---------------|---------------|
| 5 | C73 Expert Analysis | 10 | 10 |
| 5 | C74 Historical Scenarios | 0 | 10 |
| 6 | C85 Wellness Check | 1 | 11 |
| 7 | C84 Case Studies | 5-10 | 16-21 |
| 8 | C63 Audio (quarterly start) | 12 | 28-33 |
| 9+ | C81 Scenarios (scoped) | 20 | 48-53 |
| 9+ | C65 Game | 15 | 63-68 |
| 9+ | C68 Concepts | 10 | 73-78 |
| **Remaining for future features** | | | **22-27** |

✅ Content cap (100 items) is respected with 22-27 items of headroom.

---

## Design Directions (Post-Challenger)

### Direction A: "PPT-Style 2.0" — Progressive Card Stack ✅ ADOPTED
- Hero card → Story cards (max 5) → Action card
- Max 5 cards per page section (hard rule)
- New card types: `_story_card()` (green border), `_expert_card()` (purple — pending Daniel), `_scenario_card()`, `_study_card()`

### Direction B: "Dual-Mode Disclosure" ❌ REJECTED
- Contradicts historian vision (all content should be beginner-grade)
- No competitor uses this pattern
- Direction A's card-count limit solves page bloat more simply
- **Re-evaluate after Sprint 5** if empirical page bloat is observed

### Direction C: "Color-Coded Narrative" ⏸️ PHASE 2
- Deferred pending Daniel approval of expanded color palette
- Current RGB + orange palette sufficient for Sprint 5-6

---

## Pending Daniel Decisions (Updated)

1. **C34 vs C46 priority for Sprint 5** — Still pending. Recommendation: defer both to Sprint 9+ given content cap pressure.
2. **C47 Phase 1 scope: 5 vs 10 lessons** — Still pending. Recommendation: 5 lessons (C68 deferred).
3. **Business Card Page IA: "above the fold" definition** — Still pending. Recommendation: C37 + C43 only (snowflake + key takeaways).
4. **NEW: Color palette expansion** — Direction C proposes purple (expert) + teal (community) border colors. Does this violate the "RGB only" design principle?

---

## Final PM Assessment

The Challenger's 3-round process identified 7 substantive issues. All 7 have been resolved:
- 3 sequencing fixes (C42→Sprint 6, C45→Sprint 6, D28→Sprint 7)
- 1 design direction rejection (Direction B)
- 1 reconciliation of Round 14 vs Round 15 features (C65/C68 deferred, D22 maintained)
- 1 new spike for M5 (D-045)
- 1 hard prerequisite confirmation (D37)

The revised plan is now ready for Challenger confirmation.

---

*Team response written by PM. Awaiting Challenger final confirmation.*
