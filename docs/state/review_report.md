# Review Report
## Theme: Review (🔍) — Round 21
## Date: 2026-06-13

---

## 1. Key Findings Summary

### Architecture
- **Sprint 8 debt claims verified**: All 7 claimed items (D-048, D-055, D-050, D8, D9, D10, D-056) are **genuinely resolved**. Code evidence confirmed for each.
- **D6 (YAML migration)**: Still partially resolved — only 1 of 6 data blocks migrated (`case_studies.yaml`). 5 hardcoded blocks remain.
- **5 new debt items for Sprint 9**: D-057 (LLM abstraction — HIGH, blocker), D-058 (quiz engine duplication), D-059 (session state for C103), D-060 (event interpretation facade), D-061 (test infrastructure — escalating)
- **Architecture health**: 🟢 HEALTHY — 0 god modules, 4-layer architecture holding, 22 service modules (86% under 300 lines), largest file is `chart.py` at 787 lines
- **Top 3 architecture recommendations**:
  1. Create LLM abstraction layer (D-057, 2-3h) — Day 1 prerequisite for C98
  2. Extract shared quiz engine (D-058, 1-2h) — alongside C101
  3. Create event interpretation facade (D-060, 1-2h) — during C98

### Design
- **Design Grade: A** (upgraded from A-) — Sprint 8 closed the inline HTML enforcement gap. `sector_heatmap.py` went from 150+ lines of inline HTML to zero. `_section_title()` bug fixed. `market_event_case_study.py` confirmed clean.
- **3 new P2 issues**: D-057 (duplicate `_section_title()` functions), D-058 (`_render_related_stock_card()` misuses `_subsidiary_card()`), D-059 (inconsistent calling convention)
- **7 design system updates needed**: Document existing (`_subsidiary_card`, `_count_label`, `_summary_card`), add new (event interpretation card, quiz card, onboarding card), clarify `_section_title()` dual signature
- **Sprint 9 design specs delivered**: C98 (event interpretation card layout), C101 (inline quiz card pattern), C103 Lite (2-card onboarding design)

### Competitor Research
- **4 new competitors analyzed**: Finimize, Stash, SoFi Invest, eToro
- **3 new feature gaps identified** (C104-C106):
  - C104: Post-Narrative Comprehension Check — P2, 8-12h — Finimize model
  - C105: Simple/Detailed Content Depth Toggle — P2, 10-14h — Finimize + Stash
  - C106: First 7 Days Beginner Onboarding — P2, 16-22h — Stash + SoFi
- **Cumulative totals**: 90 competitors analyzed, 106 feature gaps identified (C01-C106)
- **Key insight**: "Quiz after story" is becoming table stakes for education platforms. Beginner onboarding is the #1 unserved need in TW market.

### Cost Estimates
- **Sprint 9 (Features)**: C98 spike (2h) + C98 dev (16-23.5h) + C101 (8-12h) + C103 Lite (8-11.5h) = 34-46h (PM) / 44.5-51.5h (dev, adopted as plan)
- **Sprint 9 Prerequisites**: D-057 (2-3h) must be Day 1 before C98
- **Sprint 10+**: C34 (Company Story Timeline) + M5 remediation + C105 + C106

---

## 2. Feature Gaps (New from Round 21)

| ID | Feature | Status | Priority | Effort | Source |
|----|---------|--------|----------|--------|--------|
| C104 | Post-Narrative Comprehension Check | NEW | P2 | 8-12h | Finimize |
| C105 | Simple/Detailed Content Depth Toggle | NEW | P2 | 10-14h | Finimize + Stash |
| C106 | First 7 Days Beginner Onboarding | NEW | P2 | 16-22h | Stash + SoFi |

---

## 3. Design Improvements

### Immediate (Before Sprint 9)
1. **D-057**: Consolidate duplicate `_section_title()` functions — 0.5-1h
2. **D-058**: Create dedicated `_event_stock_card()` helper — 0.5-1h
3. **Design system updates**: Document 7 new/updated components — 2-3h

### During Sprint 9
4. **C98 design spec**: Event interpretation cards replace summaries (ten-second test compliance)
5. **C101 design spec**: Inline quiz card pattern (Finimize model), 1 question per section
6. **C103 Lite design spec**: 2-card onboarding, session-state tracked, permanently dismissible

### Design Grade
**A** (upgraded from A-) — Sprint 8 closed the inline HTML enforcement gap. Grade trajectory: A (R19) → A- (R20) → **A (R21)**.

---

## 4. Technical Debt Updates

### Newly Identified This Round
- **D-057**: No LLM abstraction layer (D5 → now blocker for C98) — HIGH, 2-3h, **Day 1 prerequisite**
- **D-058**: C101 Quiz will duplicate C85 scoring patterns — Medium, 1-2h
- **D-059**: C103 Lite needs session-state management — Medium, 1-2h, deferrable
- **D-060**: C98 will couple to 4+ services without facade — Medium, 1-2h
- **D-061**: No test infrastructure (D13) — Medium (escalating), 3-4h, deferrable to Sprint 10

### Confirmed Resolved (Sprint 8)
- **D-048**: `_CASE_STUDIES` → YAML ✅
- **D-055**: `sector_heatmap.py` inline HTML removed ✅
- **D-050**: `market_event_case_study.py` already clean ✅
- **D8**: `etf_browser.py` ThreadPoolExecutor ✅
- **D9**: `watchlist.py` mtime cache ✅
- **D10**: `adaptive_engine.py` mtime cache ✅
- **D-056**: `_section_title()` inverted logic bug fixed ✅

### Still Open (High Priority)
- **D-057/D5** (HIGH): LLM abstraction layer — Sprint 9 Day 1 prerequisite
- **D6** (Medium): 5 remaining YAML migrations — Sprint 10
- **D-051** (Low): O(n) linear scan for case study lookups — deferrable
- **D13** (Medium): Test infrastructure — Sprint 10

---

## 5. Challenger 3-Round Challenge

### Round 1: Gap Authenticity Challenge — ⚠️ PARTIALLY REVISED
**Challenger Finding**: C104 (Post-Narrative Comprehension Check) overlaps significantly with C101 (Comprehension Check Quiz). Both are quiz features. C104 is described as "the implementation specification for C101" — this suggests they should be merged, not treated as separate features. C105 (Simple/Detailed Toggle) is the most strategically valuable new feature — no TW competitor has it, and it solves the beginner/intermediate tension that has existed since Sprint 1. C106 (First 7 Days) is large (16-22h) and may not fit in Sprint 9 alongside C98+C101+C103.

**Verdict**: C104 should be merged into C101 (they're the same feature at different specificity levels). C105 is the highest-value new feature. C106 should be deferred to Sprint 10.

### Round 2: Priority Challenge — ⚠️ REVISED
**Challenger Finding**: D-057 (LLM abstraction) is correctly identified as a Day 1 prerequisite, but the 2-3h estimate may be optimistic. Creating a protocol ABC + template fallback + LLM provider adapter + testing the integration could take 3-4h. The Sprint 9 plan should account for this. D-061 (test infrastructure) has been deferred since Round 14 — at what point does it become a blocker? With 22 service modules and growing, the risk surface is expanding.

**Verdict**: D-057 estimate revised to 3-4h. D-061 should be scheduled for Sprint 10 as a hard commitment, not "deferrable."

### Round 3: Goal Alignment Challenge — ✅ CONFIRMED
**Challenger Finding**: The three new features (C104/C101 merge, C105, C106) all align with "historian, not stock picker" — they're education features, not stock-picking tools. C105 (Simple/Detailed Toggle) directly serves the beginner persona. C106 (First 7 Days) creates the structured onboarding that's standard in US fintech but absent in TW. The design grade upgrade to A is justified — Sprint 8 genuinely closed the inline HTML gap. The architecture health assessment is accurate — 0 god modules, clean 4-layer separation.

**Verdict**: ✅ CONFIRMED with 3 required revisions: (1) merge C104 into C101, (2) D-057 estimate revised to 3-4h, (3) D-061 scheduled as hard Sprint 10 commitment.

### Final Challenger Verdict: ✅ CONFIRMED with revisions
- C104 merged into C101 (same feature, C104 is the implementation spec)
- C105 (Simple/Detailed Toggle) — highest-value new feature, recommend Sprint 10
- C106 (First 7 Days) — defer to Sprint 10 (too large for Sprint 9)
- D-057 estimate: 3-4h (not 2-3h)
- D-061: Hard commitment for Sprint 10

---

## 6. PM Decisions

### Sprint 9 Scope (CONFIRMED with revisions)
| Item | Hours | Type | Order |
|------|-------|------|-------|
| D-057: LLM abstraction layer | 3-4h | Prerequisite | **Day 1** |
| C103 Lite: First Visit Guide | 8-11.5h | Feature | 1st |
| C101: Comprehension Check (includes C104) | 8-12h | Feature | 2nd |
| C98: Event Interpretation Engine | 2h spike + 16-23.5h dev | Feature | 3rd |
| **TOTAL** | **37-51h** | | |

### Sprint 10 (Planned)
| Item | Hours | Type |
|------|-------|------|
| C34: Company Story Timeline | 16-24h | Feature |
| C105: Simple/Detailed Toggle | 10-14h | Feature |
| C106: First 7 Days Onboarding | 16-22h | Feature |
| M5 remediation: Fix 10 L1 event-alert failures | 8-12h | Debt |
| D-061: Test infrastructure | 3-4h | Debt |
| D6: Remaining YAML migrations | 3-4h | Debt |
| **TOTAL** | **56-80h** | |

### Design Grade
**A** (upgraded from A-)

### Structural Changes Required
1. Merge C104 into C101 (same feature, different specificity)
2. Schedule D-061 (test infrastructure) as hard Sprint 10 commitment
3. Update design system with 7 new/updated components before Sprint 9 coding

---

*Effort: 37-51h Sprint 9 (features + prerequisite), 56-80h Sprint 10*
*Cumulative remaining: ~93-131h*
*Next cycle: 🔧 Development → Sprint 9 → 🔍 Review Round 22 → Sprint 10*
