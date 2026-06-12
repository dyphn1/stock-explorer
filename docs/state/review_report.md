# Review Report
## Theme: Review (🔍) — Round 16
## Date: 2026-06-20

---

## 1. Key Findings Summary

### Architecture
- **D16 RESOLVED**: `analogy_engine.py` (850 lines) was already split in commit `f128fb0` into 4 focused modules: `analogy_engine.py` (193), `key_takeaways.py` (232), `delta_engine.py` (164), `health_scoring.py` (269). Total: 858 lines across 4 files.
- **D24 RESOLVED**: `business_card.py` extracted to sub-directory (commit `e12c103`).
- **D26 UNBLOCKED**: `story_composer.py` can now import from stable, focused modules.
- **New debt D39**: Duplicate import headers in `_main.py` and `_sections.py` — maintenance coupling risk.
- **Codebase grew by 3 files but SHRANK by 260 LOC** — structural improvement.

### Design
- **Grade A maintained** (5th consecutive round) — no new P1 issues.
- **3 new P2 issues**: D-042 (health mini-card styling), D-043 (dividend table HTML), D-044 (read next header).
- Sprint 5 prerequisites (D-039, D-040, D-041) are **NOT STARTED** — must complete before Sprint 5 feature coding.
- Sprint 4 design risk: C38 HIGH, C48 MEDIUM, C51 MEDIUM, C53-1 LOW.

### Competitor Research
- 6 new competitors analyzed: Bloom, Cleo, 長投學堂, Visual Capitalist, MoneySmart, Plum.
- 5 new feature suggestions (C81-C85): Historical Decision Scenarios, Animated Data Story, Investment Memo Template, Market Event Case Studies, Financial Wellness Check.
- **Key insight**: Competitive landscape is mature — most major feature categories already covered by C01-C80. Remaining white space is in execution quality and interactive depth.

### Cost Estimates
- Sprint 4: **43.5h** (R3 + C38 + C51 + C48 + C53-1 + debt)
- Sprint 5: **44.8h** (prerequisites + C71 + C73 + C74 + D-038)
- C81-C85 new features: **51h** total
- Design debt cleanup: **3.1h**
- **Grand total remaining: ~142h**

---

## 2. Feature Gaps (New from Round 16)

| ID | Title | Priority | Effort | Source | Alignment |
|----|-------|----------|--------|--------|-----------|
| C83 | Investment Memo Template | P2 | 6-10h | 長投學堂, Tykr | Story first + Point-to-point + Historian |
| C85 | Financial Wellness Check | P2 | 8-12h | Cleo, Plum, Bloom | Point-to-point + Beginner-friendly |
| C84 | Market Event Case Study | P2 | 10-14h | 長投學堂, Bloom | Story first + Adaptive + Historian |
| C82 | Animated Data Story | P2 | 12-16h | Visual Capitalist | Story first + PPT-style |
| C81 | Historical Decision Scenarios | P2 | 14-20h | Bloom, 長投學堂 | Story first + Historian |

**Recommendation**: C83 (Investment Memo Template) is the highest ROI — lowest effort, proven demand, directly extends C55.

---

## 3. Design Improvements

### New Issues
| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-042 | Health mini-cards use non-standard padding/border-radius | P2 | 0.5h |
| D-043 | Dividend table uses inline HTML instead of st.dataframe | P2 | 1.5h |
| D-044 | C41 Read Next header doesn't use _section_title() | P2 | 0.3h |

### Design System Updates Needed (6 items)
1. Mini Score Card variant spec
2. Story Card specification (for C48)
3. Comparison Layout Rules (for C38)
4. Heatmap Color Rules (for C51)
5. Section Header Standard (D-039)
6. Disclaimer Component spec (D-040)

---

## 4. Technical Debt Updates

### Newly Resolved This Round
- **D16**: `analogy_engine.py` split into 4 modules (commit `f128fb0`)
- **D26**: Unblocked — `story_composer.py` can now proceed

### New Architecture Debt
- **D39**: Duplicate import headers in `_main.py` and `_sections.py` (Medium, 1-2h)

### Still Open (High Priority)
- **D5**: No LLM integration layer (2-3h)
- **D23**: Market-level tone guidelines (1h) — needed before C51
- **D25**: Market data service module (2h) — needed for C51

### Sprint 5 Prerequisites (NOT STARTED — CRITICAL)
| ID | Description | Effort | Risk if Skipped |
|----|-------------|--------|-----------------|
| D-039 | Section header standardization | 1-2h | Header inconsistency worsens |
| D-040 | Historian disclaimer component | 0.5h | Regulatory risk |
| D-041 | Sprint 5 card components | 1h | D-003 regression to B- |

---

## 5. Challenger 3-Round Challenge

### Round 1: Gap Authenticity Challenge
**Challenger questions**: Are C81-C85 really gaps? The competitive landscape is mature — do we need more features or better execution of existing ones?

**Team response**: 
- C83 (Investment Memo) and C85 (Wellness Check) are genuine gaps — no TW competitor has structured reflection tools or behavioral self-assessment.
- C81 (Decision Scenarios) and C84 (Case Studies) are the purest "historian" features — they teach through historical exploration, not prediction.
- C82 (Animated Data Story) is a visual differentiation opportunity but carries high JS risk in Streamlit.
- **Verdict**: C83 and C85 are validated. C81, C82, C84 are medium-term opportunities. No features rejected this round.

### Round 2: Priority Challenge
**Challenger questions**: Should C81-C85 take priority over Sprint 4/5 planned work? What's the right sequence?

**Team response**:
- Sprint 4 (D16-unblocked features) and Sprint 5 (prerequisites + features) remain the priority.
- C83 and C85 should be considered for Sprint 5+ after prerequisites are done.
- C81, C82, C84 are post-Sprint 5 work.
- **Verdict**: No priority changes to Sprint 4/5. C83/C85 added to Sprint 6+ consideration.

### Round 3: Goal Alignment Challenge
**Challenger questions**: Does the overall direction still align with "historian, not stock picker"? Are there any contradictions?

**Team response**:
- All 5 new features pass the historian test — they teach through historical exploration, self-reflection, or behavioral awareness.
- The Sprint 5 prerequisites (D-039, D-040, D-041) are critical for maintaining design quality as the feature set grows.
- **Risk**: D-003 (card inconsistency) will worsen if D-041 is not completed before Sprint 5.
- **Verdict**: ✅ CONFIRMED — direction is sound. A grade conditional on D-041 completion before Sprint 5.

**Final Challenger Decision**: ✅ CONFIRMED with conditions:
1. D-041 must be completed before Sprint 5 feature coding
2. C83 should be prioritized as the first post-Sprint 5 feature
3. C82 should start as MVP (static fade-in) to de-risk JS integration
4. Design system updates (6 items) should be done alongside feature implementation

---

## 6. PM Decisions

### Sprint 4 CONFIRMED
**Sequence**: R3 (1.5h) → C48 (12h) + C38 (11h) parallel → C51 (14h) → C53-1 (2.5h)
**Parallel**: D23 tone guidelines (1h), D37 sections split (1.5h) alongside features
**Total**: 43.5h

### Sprint 5 CONFIRMED
**Prerequisites first**: D-039 (1.5h) + D-040 (0.5h) + D-041 (1h) + D-037 fix (0.3h) = 3.3h
**Then features**: C71 (10h) → C74 (13h) → C73 (17h)
**Total**: 44.8h

### New Features (Sprint 6+)
**Priority order**: C83 (8h) → C85 (10h) → C84 (12h) → C82 (14h) → C81 (17h)

### Design Debt Quick Wins (Anytime)
- D-036: Fix risk card background (0.3h)
- D-037: Fix 白话 card background (0.3h)
- D-044: Fix read next header (0.3h)
- D-042: Create mini score card component (0.5h)
- D-035: Replace peer card inline HTML (0.5h)
- **Total quick wins: ~2h**

---

## 7. Files Created/Modified This Round
- Created: `docs/research/competitor_research_r16.md`
- Created: `docs/design/architect_review_r16.md`
- Created: `docs/design/designer_review_r16.md`
- Created: `docs/design/developer_estimates_r16.md`
- Created: `docs/state/review_report.md` (this file)
- Modified: `docs/status/tech_debt.md` (D16 → RESOLVED, D26 → UNBLOCKED)
- Modified: `docs/status/current_problems.md` (D-042, D-043, D-044 added)
- Modified: `docs/status/issues.md` (C81-C85 added)
- Modified: `docs/state/handoff.md` (Review section updated)
- Modified: `docs/state/handoff_review.md` (Round 16 results)
- Modified: `docs/workflow/challenge_log.md` (Round 16 challenge)

---

*Next cycle: 🔧 Development → Sprint 4 execution (R3 + C48 + C38 + C51 + C53-1)*
*Next review: Sprint 4 mid-point (after R3 + one major feature complete)*
