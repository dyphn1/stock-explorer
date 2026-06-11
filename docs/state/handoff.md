# Handoff – Development
## Summary
- **Topic**: Development (🔧) — Sprint 3
- **Date**: 2026-06-18
- **Sprint Status**: Sprint 3 in progress → C44 remaining

## Completed Items (Sprint 2)
| Item | Result |
|------|--------|
| C37: Key Takeaways Summary Card | ✅ Implemented (8651430) |
| C39: What Changed Delta Card | ✅ Implemented (8651430) |
| C45: Valuation Band Chart | ✅ Implemented (8d585c7) |
| C43: Snowflake Health Visualization | ✅ Implemented (b1624af) |

## Key Metrics
- Design grade: A- (Round 11)
- Total issues: 20 (0 P0, 7 P1, 10 P2), 3 resolved
- Codebase: +2,499 LOC in Sprint 2, 0 new service modules
- L0: 54/54 ✅ | L1: 15/15 ✅

## Sprint 3 Plan
| Item | Effort |
|------|--------|
| C44: Risk Analysis MVP | 12-14h |
| C41: Read Next Recommendations | 6-8h |
| C38: Compare Stories Phase 1 | 10-12h |
| R1: Extract financial_metrics.py | 2-3h |
| D16: Split analogy_engine.py | 2-3h |
| Design fixes (D-016-D-022) | <2h |

## 🔍 Review Results (Round 11 — 2026-06-17)
- 9 new competitors → 7 new feature gaps (C48-C54)
- 6 new architecture debt items (D16-D21)
- Design grade B+ → A-, 0 P0, 7 P1, 10 P2
- Full details: docs/state/handoff_review.md

## Pending Daniel Decisions
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope: 5 vs 10 lessons
3. Business Card Page IA: "above the fold" definition
4. C42 vs C46 priority if Sprint 4 slips

## 🔧 Development Results (Sprint 3 — 2026-06-18)

### Completed This Cycle
| Item | Commit | Result |
|------|--------|--------|
| R1: Extract financial_metrics.py | f751110 | ✅ New shared module, 3 consumers updated |
| D-018: Move C39 after C37 | a6deec3 | ✅ Page order fixed |
| D-020: Return interpretation from chart | a6deec3 | ✅ Eliminates duplicate computation |
| D-021: Dimension explanations | a6deec3 | ✅ Score-based plain-language |
| D-023: 5-year valuation window | a6deec3 | ✅ Extended from 2yr |
| Fix: get_revenue_analyzer typo | f751110 | ✅ Pre-existing bug fixed |
| Fix: get_dividend_analyzer typo | f751110 | ✅ Pre-existing bug fixed |

### Verification
- L0: 55/55 ✅
- L1: 18/18 ✅

## 🔧 Development Results (Sprint 3 — 2026-06-19)

### Completed This Cycle
| Item | Commit | Result |
|------|--------|--------|
| C41: Read Next Recommendations | 1f98d73 | ✅ Peer stocks + fun facts section added to business card |
| D-024: _info_card wrong background color | c46ec8e | ✅ Changed #FFF8F0 → #F8F9FA per design system |
| D-025: C39 missing empty state message | c46ec8e | ✅ Added "近期無顯著變化" fallback when no deltas |

### Verification
- L0: 55/55 ✅
- L1: 8/8 new + 10 pre-existing news failures (unchanged, not regressions) ✅

### Remaining Sprint 3 Items
| Item | Effort | Status |
|------|--------|--------|
| C44: Risk Analysis MVP | 12-14h | ⏳ Next |
| C38: Compare Stories Phase 1 | 10-12h | ⏳ After C44 |
| D16: Split analogy_engine.py | 2-3h | ⏳ After C44 |

## Next Cycle Handoff
Next theme: 🔧 Development → Sprint 3 continued (C44 Risk Analysis MVP)

For full Round 11 review context: docs/state/handoff_review.md
For pending Daniel decisions: docs/state/pending_review.md
For Round 11 discussion: docs/state/handoff_discuss.md

## 💡 Discussion Results (Round 11 — 2026-06-18)

### New Features Evaluated (C48-C54, from Round 11 Competitor Research)

**Sprint 4 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C51 | Sector Heatmap | 12-16h | R3 (batch API) |
| C48 | Company Story Card (replaces C37) | 10-14h | D16 (split analogy_engine) |
| C53-1 | Social Sharing Phase 1 (URL) | 2-3h | — |

**Sprint 5 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C49 | Daily Market Pulse | 14-20h | C51's market_data.py |
| C52 | Quiz Mode (20-question MVP) | 12-18h + 5h content | — |
| C53-2 | Social Sharing Phase 2 (Image) | 5-9h | export_service.py |

**Deferred (Sprint 5+):**
| ID | Feature | Effort | Blocker |
|----|---------|--------|---------|
| C50 | Learning Progress Tracker | 16-24h | D22 (persistence layer) + no user identity |
| C54 | Video/Audio Explanation | 30-45h | R7 (LLM) + TTS pipeline |

### Key Decisions
1. **C48 replaces C37** — not alongside (avoids page overload, fixes D-016)
2. **New `market_data.py` service** — shared infrastructure for C49 + C51
3. **New `story_composer.py` service** — composes company stories from existing data
4. **New `export_service.py` utility** — HTML-to-image for C48 + C53
5. **Tone guidelines for market features** — "過去發生" language, factual not predictive
6. **R3 and D16 are hard prerequisites for Sprint 4**

### New Architecture Debt
- D23: Tone guidelines for market-level features — P2
- D24: business_card.py growth from C48 — consider sub-directory extraction — P2

### Competitor Insights Addressed
- #4 Visual-first (C51 Sector Heatmap)
- #1 Social learning (C53 Social Sharing)
- #3 Daily engagement loop (C49 Daily Market Pulse)
- #5 Assessment (C52 Quiz Mode)
- #2 Structured education (C50 deferred, C52 partial)

## 💡 Discussion Results (Round 13 — 2026-06-18)

### Round 12 New Features Evaluated (C55-C62, from Round 12 Competitor Research)

**Sprint 5 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C58 | Beginner Onboarding Flow | 14-22h | — (P1, prerequisite) |
| C62 | Pre-Investment Checklist | 8-14h | — |
| C56 | Explain This Metric | 12-18h | D24 (Sprint 4) |
| C60 | Concept Mastery Badges | 8-14h | — (session-only MVP) |

**Sprint 6 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C57 | Compare Concepts | 10-14h | — |
| C55 | Investment Diary | 10-16h | — |
| C61 | Sector Rotation Visualizer | 10-16h | C51 (Sprint 4) |

**Sprint 7+ Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C59 | AI Q&A Chatbot | 18-28h | All education features stable |

**Key Decisions:**
1. **"Foundation + Education Core" direction** — Reframed from "Education-First" to accurately reflect that C58/C60/C59 are UX/engagement/interface features supporting the education core (C56+C57+C62)
2. **C58 moved to Sprint 5** — All roles agree onboarding is prerequisite for C56/C62 effectiveness
3. **C60 moved to Sprint 5** — Lowest-effort feature, session-only MVP acceptable
4. **Content creation starts Sprint 4** — C56/C57/C62 require ~15h content writing; begin as parallel workstream
5. **C59 deferred to Sprint 7+** — Highest risk, benefits from stable education foundation
6. **New data files** — `metric_explanations.yaml`, `concept_pairs.yaml`, `badges.yaml`, `checklist_items.yaml`
7. **New card types** — `_diary_card()` (green), `_checklist_card()` (amber), `_badge_card()` (blue)
8. **New architecture debt** — D25 (session state scalability), D26 (content creation bottleneck)

**Challenger's 3-Round Summary:**
- Round 1 (Feature Direction): ✅ RESOLVED — Direction reframed; 4/8 features are purely educational
- Round 2 (Priority): ✅ RESOLVED — C58 moved to Sprint 5; C60 moved to Sprint 5
- Round 3 (Goal Alignment): ✅ RESOLVED — M2 partially addressed; business_card.py risk mitigated; content creation starts Sprint 4

## 💡 Discussion Results (Round 12 — 2026-06-18)

### Sprint 3 Remaining + Sprint 4 Preparation Discussion

**Sprint 3 Remaining Sequence (Revised):**
1. **C41** (Read Next, 6-8h) — first, lowest risk, direct vision alignment
2. **C44** (Risk Analysis MVP, 12-14h) — 3 risk dimensions only (customer concentration, financial health, event-based)
3. **C38** (Compare Stories P1, 10-12h) — structured comparison, no LLM
4. **D16** (Split analogy_engine.py, 2-3h) — moved to end, before C48
5. **D-025** (Expandable card component, 2-3h) — NEW, for C44 progressive disclosure

**Sprint 4 Sequence (Revised):**
1. **R3** (Batch API minimal, 1-2h) — rate-limit-safe fetching for C51
2. **D24** (business_card.py sub-directory extraction, 2-3h) — NEW, before C48
3. **C51** (Sector Heatmap, 12-16h) — with minimal R3 prerequisite
4. **C48** (Company Story Card replaces C37, 10-14h) — hero card pattern
5. **C53-1** (Social Sharing URL, 2-3h) — quick win

**Total revised effort**: 60-80h (72-96h with 20% buffer)

**Key Decisions:**
1. **C44 scope**: Capped at 3 risk dimensions for MVP (customer concentration, financial health, event-based) — volatility and cyclicality deferred to preserve historian positioning
2. **C48 replaces C37** — not alongside (avoids page overload, fixes D-016)
3. **R3 prerequisite** — minimal batch fetching (1-2h) required for data correctness (rate limit safety)
4. **business_card.py limits** — D-025 (expandable card) added to Sprint 3, D24 (sub-directory extraction) added to Sprint 4 to prevent >600-line file
5. **C52 preparation** — content creation starts in Sprint 4 final week (parallel workstream) for Sprint 5 development
6. **Contingency plan** — if Sprint 3 overflows: defer D-025 first, then D16; if exceeds 48h, defer C38 to Sprint 4
7. **New backlog item** — C55: Recent Events Narrative (4-6h, Sprint 5) added to address M2 milestone gap

**Challenger's 3-Round Summary:**
- **Round 1 (Feature Direction)**: RESOLVED — Direction A maintained; C51 is both visual AND educational; C44 scoped to purely historical dimensions
- **Round 2 (Priority)**: RESOLVED — C41 moved first (lower risk/faster value); D16 moved to end of Sprint 3; R3 confirmed as hard prerequisite for data correctness; business_card.py growth addressed with D-025/D24
- **Round 3 (Goal Alignment)**: RESOLVED — M2 milestone accepted as "good enough"; all role contradictions resolved; explicit contingency plan defined; ten-second test analysis provided for C41/C38

**Final PM Decision (Challenger ✅ Confirmed with Conditions):**
**Direction A ("Stabilize + Visual Impact") adopted with revisions:**
- Sprint 3: C41 → C44 → C38 → D16 → D-025
- Sprint 4: R3 → D24 → C51 → C48 → C53-1
- C44 limited to 3 historical risk dimensions only
- C52 content creation begins in Sprint 4 final week
- D-025 and D24 are non-negotiable for architectural limits
- Contingency plan in place for Sprint 3 overflow
- C55 (Recent Events Narrative) added to Sprint 5 backlog

**Pending Daniel's Decision** (unchanged from previous):
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope: 5 vs 10 lessons
3. Business Card Page IA: "above the fold" definition

**Next Cycle Handoff**
Next: 🔧 Development → Sprint 3 continued (C41 + C44 + C38 + D16 + D-025)