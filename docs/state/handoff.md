# Handoff – Development
## Summary
- **Topic**: Development (🔧) — Sprint 3
- **Date**: 2026-06-18
- **Sprint Status**: Sprint 3 in progress → C38 + D16 remaining

## Completed Items (Sprint 2-3)
| Item | Result |
|------|--------|
| C37: Key Takeaways Summary Card | ✅ Implemented (8651430) |
| C39: What Changed Delta Card | ✅ Implemented (8651430) |
| C45: Valuation Band Chart | ✅ Implemented (8d585c7) |
| C43: Snowflake Health Visualization | ✅ Implemented (b1624af) |
| R1: Extract financial_metrics.py | ✅ Implemented (f751110) |
| C41: Read Next Recommendations | ✅ Implemented (1f98d73) |
| C44: Risk Analysis MVP | ✅ Implemented (567239b) |

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

## 🔍 Review Results (Round 14 — 2026-06-19)

### Competitor Research
- 8 new competitors analyzed (Groww, Dhan, Sensibull, Spiking, Cake Finance, SoFi, Finshots, Trading 212)
- India identified as global leader in beginner financial education innovation
- Dhan's "Read More, Trade Less" positioning directly validates our historian approach
- 6 new features identified (C69-C74), revised to 3 after Challenger review

### Architecture
- business_card.py at 561 lines — D24 extraction is CRITICAL Sprint 4 first task
- 3 new debt items (D31, D32, D33) — all low/medium urgency
- Revised Sprint 4 sequence: D24 → D16 → R3 → C38 → C51 → C48 → C53-1

### Design
- Design grade A maintained (0 P0, 6 P1, 13 P2)
- 4 new P2 issues (D-035 through D-038)
- D-007, D-032 downgraded to P2; D-013 resolved

### New Features (Revised after Challenger)
- C69 (Paper Trading) — REMOVED (positioning conflict)
- C70 ("Why This Matters") — Folded into C37 redesign
- C71 (Study Log, reframed from Streak) — Sprint 5
- C72 (TL;DR) — Merged into C48
- C73 (Expert Analysis Synthesis, pivoted) — Sprint 5
- C74 (Historical Scenario Explorer, pivoted) — Sprint 6

### New Structural Policies
1. Positioning Impact Score (1-5) for future features
2. Feature Budget Rule: +1 = -1
3. Beginner/Advanced Path labels
4. Fix one, build one policy

### Revised Sprint 5
- P1 fixes + C71 (Study Log) + C73 (Expert Analysis) + C74 start
- Full details: docs/state/handoff_review.md
- Challenge details: docs/workflow/challenge_log.md

## 🔍 Review Results (Round 13 — 2026-06-19)
- 8 new competitors → 6 new feature gaps (C63-C68)
- 3 new architecture debt items (D29, D30, D-034)
- Design grade A maintained, 0 P0, 7 P1, 10 P2
- New P1: D-032 (progressive disclosure), D-034 (metric value tooltips)
- Key finding: C65 (Company Filing Explorer) — no TW competitor has AI-parsed annual reports
- Architecture urgency: D24 moved before C44 in Sprint 4 sequence
- Full details: docs/state/handoff_review.md, docs/design/design_review.md

## 🔍 Review Results (Round 11 — 2026-06-17)
- 9 new competitors → 7 new feature gaps (C48-C54)
- 6 new architecture debt items (D16-D21)
- Design grade B+ → A-, 0 P0, 7 P1, 10 P2
- Full details: docs/state/handoff_review.md (Round 12 version)

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

## 🔧 Development Results (Sprint 3 — 2026-06-19, Cycle 2)

### Completed This Cycle
| Item | Commit | Result |
|------|--------|--------|
| C44: Risk Analysis MVP | 567239b | ✅ New risk_analyzer.py service (3 dimensions: customer concentration, financial health, event-based) + business_card.py integration with st.expander progressive disclosure |
| docs/design/risk_analysis_design.md | 567239b | ✅ Architect design doc: 624 lines, historian tone guardrails, threshold specs |

### Verification
- L0: 56/56 ✅ (new file: risk_analyzer.py, +1 from baseline)
- L1: 8 passed + 10 pre-existing event_dashboard failures (unchanged, not regressions) ✅
- Architecture: risk_analyzer.py has NO streamlit import, NO API calls — clean service layer ✅

### Remaining Sprint 3 Items
| Item | Effort | Status |
|------|--------|--------|
| C38: Compare Stories Phase 1 | 10-12h | ⏳ Next |
| D16: Split analogy_engine.py | 2-3h | ⏳ After C38 |

## Next Cycle Handoff
Next theme: 🔧 Development → Sprint 3 continued (C38 Compare Stories Phase 1)

For full Round 13 review context: docs/state/handoff_review.md
For pending Daniel decisions: docs/state/pending_review.md
For Round 13 design review: docs/design/design_review.md

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

## 💡 Discussion Results (Round 14 — 2026-06-19)

### New Feature Directions Evaluated (Round 13 Discussion)

**Sprint 4 Spike Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C34-spike | Company Story Timeline Prototype | 4-6h | — |

**Sprint 6 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C34 | Company Story Timeline (full) | 18-26h | D16, D24, C34-spike |
| B | Notification System for Learning Engagement | 8-14h | — |

**Deferred:**
| ID | Feature | Effort | Reason |
|----|---------|--------|--------|
| C3 | AI-Augmented Historical Narrator | 14-22h | Fatal overlap with C34, C56, C59 — revisit Sprint 8+ |

**Confirmed from Round 12 (Sprint 5 unchanged):**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C58 | Beginner Onboarding Flow | 14-22h | — |
| C62 | Pre-Investment Checklist | 8-14h | D24 |
| C56 | Explain This Metric | 12-18h | D24 (contingent) |
| C60 | Concept Mastery Badges | 8-14h | — |
| C55 | Investment Diary | 10-16h | D24 |

**Key Decisions:**
1. **C3 (AI Narrator) indefinitely deferred** — Overlap risk with C34, C56, and C59 too high; saves 14-22h
2. **Notification System moved to Sprint 6** — Limited value in Sprint 5 (only Quick Wins to notify about); frees 8-14h in Sprint 5 for C56 content creation
3. **C34 spike in Sprint 4 (4-6h)** — Prototype using Streamlit native components to de-risk Sprint 6
4. **C56 contingent on D24** — If D24 slips, C56 moves to Sprint 6
5. **Content creation starts Sprint 4** — 19-30h content creation as parallel workstream
6. **Session state audit in Sprint 5** — Before adding more keys, audit and consider session state manager (D25)

**Revised Total Effort:** 154-260h remaining (all sprints, with Round 13 additions)

**New Architecture Debt:**
- D27: C34 timeline UI complexity — Streamlit has no native timeline; prototype spike needed — P2
- D28: Notification system session state tracking — 6+ new keys; monitor for D25 escalation — P2

**Challenger's 3-Round Summary:**
- Round 1 (Feature Direction): ✅ PARTIALLY RESOLVED — C34 M3-before-M2 acknowledged; C3 overlap confirmed
- Round 2 (Priority): ✅ RESOLVED with revision — C34 spike Sprint 4; Notifications moved to Sprint 6
- Round 3 (Goal Alignment): ✅ RESOLVED with conditions — C3 deferred; C56 contingent on D24; content Sprint 4

**Final PM Decision:** "Education Core Expansion" adopted with 4 conditions from Challenger.

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

## 💡 Discussion Results (Round 15 — 2026-06-19)

### New Feature Directions Evaluated (Round 13 Discussion)

**Sprint 4 Additions (Approved):**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C66 | Risk Profile Quiz | 6-10h | — |
| D-032 | Progressive Disclosure Pattern | 2-3h | D24 (Sprint 4) |
| D-038 | Non-Stock Landing Page IA | 1-2h | — |

**Sprint 5 Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C64 | Daily Market Quiz | 8-12h | D-038 IA |
| C68 | Weekly Market Digest (replaces C49) | 8-12h | — |
| C63 | Sector Stories | 10-14h | D-038 IA |

**Sprint 6+ Approved:**
| ID | Feature | Effort | Depends On |
|----|---------|--------|------------|
| C65-spike | Company Filing Explorer Data Source Spike | 4-6h | — |
| C65 | Company Filing Explorer (full) | 16-24h | C65-spike |

**Deferred (Sprint 8+):**
| ID | Feature | Effort | Reason |
|----|---------|--------|--------|
| C67 | Community Sentiment Indicator | 12-16h | Historian positioning conflict (herd-following risk); defer until real user traffic exists |

**Cancelled/Deferred Features:**
| ID | Feature | Reason |
|----|---------|--------|
| C49 | Daily Market Pulse | Replaced by C68 (weekly > daily for beginners; saves 6-8h) |

**Key Decisions:**
1. **C68 replaces C49** — Designer and Developer both confirmed weekly is superior to daily for beginners (Syfe, Smart FOLIO validate). Saves 6-8h in Sprint 5.
2. **C67 deferred to Sprint 8+** — Challenger identified fatal historian positioning conflict: social proof ("others added this to watchlist") contradicts "historian, not stock picker." Technical spike doesn't resolve positioning issue. Defer until real user traffic exists.
3. **D-032 moved to Sprint 4** — P1 progressive disclosure issue is actively worsening as C44 and C48 add sections. Must be in place before page overload increases.
4. **D-038 IA decision in Sprint 4** — 4 of 6 Round 13 features need a non-stock landing surface. The IA decision (1-2h) must be made in Sprint 4 before C64/C63/C68 implementation.
5. **C65 requires data source spike** — FinMind has no annual report API. 4-6h spike in Sprint 6 to resolve (MOPS scraping, manual curation, or FinMind financial statements as proxy).
6. **Content creation owner must be identified** — C63 (10 sector stories), C64 (30 quiz questions), C68 (digest templates) require ~20-30h content creation starting Sprint 4. Owner and QA process must be defined before work begins.
7. **C64 and C52 share quiz_engine.py** — Shared service, separate question pools. Content pipeline must be coordinated.

**Revised Total Effort:** 174-289h remaining (all sprints, with Round 13 additions and C49 removal)

**New Architecture Debt:**
- D-035: Quiz UI pattern not in design spec — P1
- D-036: Community data tone guidelines (for C67 if revived) — P2
- D-037: Contextual Zone B pattern for C65 — P2
- D-038: Non-stock landing page architecture — P2 (Sprint 4 IA decision)

**Challenger's 3-Round Summary:**
- Round 1 (Feature Direction): ✅ RESOLVED with revision — C67 deferred; C68 replaces C49; D-032 moved to Sprint 4
- Round 2 (Priority): ✅ RESOLVED with revision — Sprint 4 overflow risk acknowledged; C66 evaluated as potential Sprint 5 deferral if C38 causes overflow; D-038 IA elevated to Sprint 4
- Round 3 (Goal Alignment): ✅ RESOLVED with conditions — Content creation owner must be identified; C65 fallback plan must be explicit; D-032 before page overload worsens

**Final PM Decision:** "Engagement + Education Expansion" adopted with 5 conditions from Challenger:
1. C68 replaces C49 (not complements)
2. C67 deferred to Sprint 8+ pending positioning review
3. D-032 moved to Sprint 4
4. D-038 IA decision in Sprint 4
5. Content creation owner identified before Sprint 4 workstream begins

**Next Cycle Handoff**
Next: 🔧 Development → Sprint 3 continued (C38 Compare Stories Phase 1)