# Stock Explorer — Round 14 Review Report
## PM Consolidation | 2026-06-19

---

## 1. Competitor Research (QA Engineer)

### New Competitors Analyzed: 8
Groww (India), Dhan (India), Sensibull (India), Spiking (Singapore), Cake Finance (Thailand), SoFi (US), Finshots (India), Trading 212 (UK)

### Key Findings
1. **India leads beginner financial education innovation** — Groww (140M+ downloads), Dhan ("Read More, Trade Less" — closest to our historian positioning)
2. **Gamification drives 3x retention** — SoFi's Learn & Earn proven data
3. **TL;DR-first is emerging UX standard** across multiple markets
4. **Simulation/practice is the missing link** between education and action
5. **No TW competitor offers** paper trading, learning streaks, or institutional investor thesis explanations
6. **Dhan's "Why This Matters" conclusion sections** directly validate our synthesis layer direction

### New Features Identified (C69-C74)

| ID | Title | Effort | Priority | Source Competitors |
|----|-------|--------|----------|-------------------|
| C69 | Paper Trading Simulator | 16-24h | P2 | Groww, Trading 212 |
| C70 | "Why This Matters" Conclusion | 6-10h | P1 | Dhan, Finshots |
| C71 | Learning Streak | 8-12h | P2 | SoFi, Cake Finance |
| C72 | TL;DR First | 4-8h | P1 | Finshots, Dhan |
| C73 | Super Investor Thesis | 12-16h | P1 | Dhan, Spiking |
| C74 | Interactive What-If Scenarios | 14-20h | P1 | Sensibull, Groww |

---

## 2. Architecture Review (Architect)

### Codebase State
- Total: ~8,572 LOC across src/
- 13 service modules, 12 page modules
- business_card.py: **561 lines** (critical — approaching 600-line threshold)
- analogy_engine.py: **850 lines** (still unsplit)
- risk_analyzer.py: **567 lines** (clean, monitor only)

### New Architecture Debt
| ID | Issue | Severity | Effort |
|----|-------|----------|--------|
| D31 | risk_analyzer.py size monitoring (567 lines) | Medium | 0h (monitor) |
| D32 | Presentation helpers in business_card.py | Medium | 1-2h (with D24) |
| D33 | C41 API call in view layer | Low | 0.5-1h |

### Critical Updates
- **D24 urgency escalated to CRITICAL**: business_card.py already 561 lines; must be FIRST task in Sprint 4
- **D30 realized**: C44 is complete, growth it predicted has occurred
- **D29 superseded by D24**: C41 inline HTML will move during sub-directory extraction

### Revised Sprint 4 Sequence (Architect Recommended)
1. **D24** — Extract business_card.py (2-3h) — **FIRST, non-negotiable**
2. **D16** — Split analogy_engine.py (2-3h) — before C48
3. **R3** — Batch API minimal (1-2h) — unlocks C51
4. **C38** — Compare Stories Phase 1 (10-12h) — remaining Sprint 3 item
5. **C51** — Sector Heatmap (12-16h) — with R3 prerequisite
6. **C48** — Company Story Card (10-14h) — with D16 + D24 prerequisites
7. **C53-1** — Social Sharing URL (2-3h) — quick win

---

## 3. Design Review (Design Reviewer)

### Design Grade: A (Maintained)

### Verified Fixes
- **D-024 ✅**: _info_card background correctly changed to #F8F9FA
- **D-025 ✅**: C39 empty state properly shows "近期無顯著變化"

### New Design Issues (4)
| ID | Issue | Severity | Effort |
|----|-------|----------|--------|
| D-035 | C41 peer cards use inline HTML (D-003 regression) | P2 | 0.5-1h |
| D-036 | C44 risk cards use #FFF8F0 instead of #F8F9FA | P2 | <0.5h |
| D-037 | _白话_card uses #F5F5F5 instead of #F8F9FA | P2 | <0.5h |
| D-038 | C41 calls API in view layer | P2 | 1-2h |

### Priority Changes
- **D-007 → P2** (from P1): C41 partially addresses discovery with peer recommendations
- **D-032 → P2** (from P1): C44 proves progressive disclosure works with st.expander
- **D-013 → Resolved**: C44 implements risk analysis

### Updated Statistics
- 0 P0, **6 P1** (down from 7), **13 P2** (up from 10), **13 resolved** (up from 12)
- Total: 25 issues tracked

### Risk Assessment
Grade could slip to A- if:
- D-003 (card inconsistency) worsens with more features
- D-005 (page overload) worsens as C48, C56 are added
- D-021 (missing metric values) remains unfixed

---

## 4. Developer Estimates

### Design Fixes (4 items): 3.5-6h total
- D-035 + D-038 batch: 2.5-4h (refactor C41 peer cards + move API call)
- D-036 + D-037 batch: 0.5-1h (two color string changes)

### Architecture Debt (3 actionable): 5-8h total
- D24: 2-3h (MUST be first)
- D16: 2-3h (before C48)
- D32: 1-2h (during D24, marginal cost 0.5-1h)
- D31: 0h (monitor only)
- D33: same as D-038 (single fix addresses both)

### New Features (6 items): 60-90h total
| ID | Low | High | Midpoint | Priority | Dependencies |
|----|-----|------|----------|----------|--------------|
| C72 | 4h | 8h | 6h | P1 | None |
| C70 | 6h | 10h | 8h | P1 | D24 |
| C71 | 8h | 12h | 10h | P2 | None |
| C73 | 10h | 15.5h | 13h | P1 | D24 + content |
| C74 | 13h | 21h | 17h | P1 | D24 |
| C69 | 14h | 21h | 17.5h | P2 | D24 |

### Top Recommendations for Immediate Implementation
1. **C72 (TL;DR First)**: Best first new feature — lowest complexity, no dependencies, high value
2. **C70 + C72 share a narrative synthesis engine**: Can be batched
3. **C73 content creation**: Start content in Sprint 4 for development in Sprint 5
4. **C69 deferred to Sprint 7+**: Historian positioning risk, highest complexity

---

## 5. Effort Summary

### Round 14 Immediate Work (Next 2 Sprints)
| Category | Low | High | Midpoint |
|----------|-----|------|----------|
| Design Fixes | 3.5h | 6h | 4.8h |
| Architecture Debt | 5h | 8h | 6.5h |
| New Features (C70-C74) | 41h | 66.5h | 53.8h |
| **Total** | **49.5h** | **80.5h** | **65.1h** |

### Cumulative Backlog (All Sprints)
- Remaining Sprint 3: C38 (10-12h) + D16 (2-3h) = 12-15h
- Sprint 4 planned: D24 + D16 + R3 + C38 + C51 + C48 + C53-1 = 41-53h
- Round 14 new features: 41-66.5h
- Round 14 fixes: 3.5-6h
- **Total remaining: ~97.5-140.5h**

---

## 6. Pending Daniel Decisions (Updated)
1. C34 vs C46 priority for Sprint 5 → **No change, still pending**
2. C47 Phase 1 scope: 5 vs 10 lessons → **No change, still pending**
3. Business Card Page IA: "above the fold" definition → **No change, still pending**
4. C42 vs C46 priority if Sprint 4 slips → **No change, still pending**
5. **NEW**: C69 (Paper Trading) positioning risk — needs Daniel's input on whether simulation conflicts with historian positioning
6. **NEW**: C73 (Super Investor Thesis) content scope — 10 vs 30 stocks for MVP

---

## 7. Challenger 3-Round Summary (Round 14)

### Round 1 (Gap Authenticity): ❌ REQUIRES REVISION
- **C69 (Paper Trading) REJECTED** — Contradicts historian positioning; broker feature, not historian tool
- **C70 ("Why This Matters") DECLASSIFIED** — Not a new feature; fold into C37 redesign as P2 tweak
- **C72 (TL;DR First) DECLASSIFIED** — Merge into C48 UX work; layout change, not a feature
- **C73 (Super Investor) PIVOT** — From investor holdings tracking to fundamental analysis synthesis
- **C74 (What-If) PIVOT** — From forward-looking prediction to historical scenario exploration (past tense, factual)
- **C71 (Learning Streak) REFRAME** — From login streak to study log (historian's record-keeping)
- **Key gap**: Zero competitor-blind-spot analysis done; all 6 features are me-too

### Round 2 (Priority): ⚠️ PARTIALLY RESOLVED
- Core Sprint 4 sequence (D24→D16→C38) confirmed sound
- New feature integration needs recalculation after declassifications
- "Fix one, build one" policy recommended for P1 fixes vs new features
- Audit business_card.py line count on Sprint 4 day 1

### Round 3 (Goal Alignment): ❌ REQUIRES REVISION
- **0 of 6 new features** directly serve "Story first, data second" in original form
- Collective direction risks diluting historian positioning → becoming me-too broker app
- Gamification features (C71) conflict with historian brand
- Feature creep velocity: backlog growing faster than resolution
- Beginner path is already built; new features serve advanced users/engagement metrics

### Challenger's 10 Required Changes
1. Remove C69 from queue entirely
2. Declassify C70, C72 to D-series design tweaks
3. Pivot C73 to fundamental analysis synthesis
4. Pivot C74 to historical scenario exploration
5. Reframe C71 as study log (not gamification)
6. Recalculate Sprint 5 estimates (3 net new features, not 6)
7. Adopt Positioning Impact Score (1-5) for future features
8. Adopt feature budget rule: +1 feature = -1 feature
9. Label all features as "Beginner Path" or "Advanced Path"
10. Audit business_card.py line count on Sprint 4 day 1

### Final Challenger Decision: ❌ REQUIRES REVISION

---

## 8. PM Final Decision

**Sprint 4 core sequence APPROVED** (D24 → D16 → R3 → C38 → C51 → C48 → C53-1) — proceed as planned.

**Round 14 new features REVISED per Challenger:**
| ID | Original | Revised Action |
|----|----------|---------------|
| C69 | Paper Trading Simulator | **REMOVED** — positioning conflict |
| C70 | "Why This Matters" | **Folded into C37** — P2 design tweak, not standalone feature |
| C71 | Learning Streak | **Reframed as "Study Log"** — historian's record-keeping, not gamification |
| C72 | TL;DR First | **Merged into C48** — layout/design tweak, not C-series feature |
| C73 | Super Investor Thesis | **Pivoted to "Expert Analysis Synthesis"** — fundamental analysis, not holdings tracking |
| C74 | What-If Scenarios | **Pivoted to "Historical Scenario Explorer"** — past tense, factual, pre-built scenarios |

**New structural policies adopted:**
1. **Positioning Impact Score** (1-5) for all future features — auto-reject scores ≤2
2. **Feature Budget Rule** — every new feature added requires one removed/descoped
3. **Beginner/Advanced Path labels** — complete Beginner Path before Advanced features
4. **Fix one, build one** — for every new feature started, one P1 fix must be completed

**Revised Round 14 deliverables: 3 new features (not 6)**
- C71 (Study Log, reframed): 8-12h → Sprint 5
- C73 (Expert Analysis Synthesis, pivoted): 8-12h → Sprint 5
- C74 (Historical Scenario Explorer, pivoted): 10-15h → Sprint 6

**Revised total new feature effort: 26-39h** (down from 60-90h)

### Sprint 5 Plan (Revised)
1. Apply Challenger's structural policies to feature evaluation
2. Complete remaining P1 design fixes (D-021, D-034, D-035+D-038 batch)
3. Implement C71 (Study Log) — 8-12h
4. Implement C73 (Expert Analysis Synthesis) — 8-12h (content for 10 pilot stocks)
5. Begin C74 (Historical Scenario Explorer) — 10-15h

*Consolidated by PM on 2026-06-19 after 3-round Challenger review. Sub-agent reports: QA (competitor_research.md R14), Architect (architecture.md R14, tech_debt.md R14), Designer (design_review.md R14, current_problems.md R14), Developer (developer_estimates_round14.md), Challenger (challenge_log.md R14).*
