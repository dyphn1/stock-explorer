# Review Report
## Theme: Review (🔍) — Round 22
## Date: 2026-06-13

---

## 1. Key Findings Summary

### Verification
- **L0**: 89/89 ✅ (66 syntax, 21 imports, key uniqueness, architecture — all pass)
- **L1**: 8/18 (10 pre-existing M5 event-alert failures — **zero new regressions** from Sprint 9)

### Architecture
- **Sprint 9 verified clean**: C98 template-only approach correct, C101 has D-062 quiz duplication, C103 Lite exemplary, D-057 consolidation complete
- **4 new debt items**: D-062 (quiz engine dup, Medium), D-063 (unused import, Low), D-064 (inline HTML, Low), D-065 (session state proliferation, Medium)
- **Architecture health**: 🟢 HEALTHY — 24 service modules (87.5% under 300 lines), 35 page modules, 0 god modules, 4-layer architecture holding
- **Sprint 10 feasibility**: C34 Option B approved (with designer's card-based approach), C105 low risk, M5 root cause identified, D-061 partially exists

### Design
- **Design Grade: A** (12th consecutive A/A-) — CONDITIONAL on fixing all 4 inline HTML items in Sprint 10
- **5 new P2 issues**: D-062 (quiz result cards inline HTML), D-063 (score logic in view), D-064 (key concept inline HTML), D-065 (disclaimer inline HTML), D-066 (adaptive banner inline HTML, pre-existing)
- **4 new components needed**: `_quiz_result_card()`, `_timeline_event_card()`, `_content_toggle()`, `_key_concept()`

### Competitor Research
- **10 new competitors**: Acorns, Betterment, Wealthfront, Cake, Tiger Brokers, Spiking, Busyu, Swifty, Plum, Wombat
- **6 new feature gaps** (C107-C112): 3 are resurrected from prior rounds, 1 is premature (requires D5), 1 is compound (C38+C34), 1 is genuinely new but data availability unverified
- **Tiger Brokers** is the most direct competitive threat — expanding into TW with "Stock Stories" and "Tiger Academy"
- **Spiking** validates C98's event interpretation approach with "Why Stock Moved" AI
- **Cumulative totals**: 100 competitors analyzed, 112 feature gaps identified (C01-C112)

---

## 2. Feature Gaps (New from Round 22)

| ID | Feature | Status | Priority | Effort | Source |
|----|---------|--------|----------|--------|--------|
| C107 | "Why Is This Stock Moving?" Inline AI Explanations | NEW (directional) | P1 | 12-16h | Spiking, Busyu |
| C108 | Insider Trading Context Layer | NEW (data feasibility TBD) | P2 | 10-14h | Spiking, TipRanks |
| C109 | Compare Timelines Side-by-Side | NEW (compound C38+C34) | P2 | 14-18h | Cake, Chartr |
| C110 | Earnings Story (same as C94 from R17) | P1 | 14-18h | Tiger, Busyu |
| C111 | Badge & Achievement System (same as C60 from R12) | P2 | 8-12h | Acorns, Cake |
| C112 | Investment Diary (same as C55 from R12) | P2 | 10-14h | Tiger |

**Note**: C107-C112 are explicitly NOT Sprint 10 scope. They are directional inputs for Sprint 11+.

---

## 3. Design Improvements

### Immediate (Before Sprint 10 Feature Coding)
1. **D-061**: Add conftest.py with shared fixtures — enables D-062 refactoring
2. **D-063**: Remove unused FinMindClient import from first_visit_guide.py — <0.1h

### During Sprint 10
3. **D-062**: Extract shared quiz_engine.py (after D-061 provides test coverage)
4. **D-064 + D-065 + D-066**: Fix all inline HTML instances (quiz result cards, key concept, disclaimer, adaptive banner) — 1-2h total
5. **C34 design**: Use designer's `_timeline_event_card()` based on `_summary_card()` pattern, not raw CSS
6. **C105 design**: Default to simple mode, business card page only

### Design Grade
**A** (maintained). Condition: All 4 inline HTML items (D-062, D-064, D-065, D-066) must be fixed in Sprint 10 or grade drops to A-.

---

## 4. Technical Debt Updates

### Newly Identified This Round
- **D-062**: comprehension_quiz_service.py duplicates financial_wellness_service.py quiz pattern — Medium, 1-2h
- **D-063**: first_visit_guide.py unused FinMindClient import — Low, <0.1h
- **D-064**: comprehension_check.py inline HTML for result cards — Low, 0.5h
- **D-065**: Session state key proliferation (15+ keys, no namespacing) — Medium, document in Sprint 11

### Confirmed Resolved (Sprint 9)
- **D-057**: `_section_title()` consolidation ✅ (21 call sites updated)

### Still Open (High Priority)
- **M5** (HIGH): 10 L1 event-alert failures — Sprint 10 remediation (8-12h)
- **D-061** (Medium): Test infrastructure — Sprint 10 (3-4h)
- **D-062** (Medium): Quiz engine extraction — Sprint 10 (1-2h)

---

## 5. Challenger 3-Round Challenge

### Round 1: Gap Authenticity Challenge — ⚠️ PARTIALLY VALIDATED
**Key findings:**
- C107-C112 overstated: 3 of 6 are resurrected gaps, 1 premature (requires D5), 1 compound
- Tiger Brokers threat is real but urgency was overstated
- M5 delay (5+ sprints of broken core feature) needs explicit acknowledgment
- C34 Option B approved but designer's card-based approach preferred over raw CSS

### Round 2: Priority Challenge — ⚠️ REVISED
**Key findings:**
- M5 fix must precede C34 live data integration (sequencing constraint)
- D-061 (test infrastructure) must precede D-062 (refactoring untested code)
- D-062 justification weakened (C105 doesn't add quiz features) but still valuable
- Zero capacity for C107-C112 in Sprint 10

### Round 3: Goal Alignment Challenge — ⚠️ CONDITIONALLY ALIGNED
**Key findings:**
- Sprint 10 core (C34+C105+M5+D-061) strongly aligns with "historian, not stock picker"
- Some C107-C112 items (C111 badges, C108 insider data) need historian-positioning review
- C105 toggle is a band-aid for page overload (D-005) — acceptable short-term
- Design grade A condition must include D-066 (pre-existing)

### Final Challenger Verdict: ⚠️ REVISED with 4 conditions
1. M5 remediation before C34 live data integration
2. D-061 before D-062 (tests before refactoring)
3. C107-C112 explicitly excluded from Sprint 10 scope
4. Design grade A condition strengthened to include all 4 inline HTML items

---

## 6. PM Decisions

### Sprint 10 Scope (CONFIRMED with revisions)

| Order | Item | Hours | Type | Dependency |
|-------|------|-------|------|------------|
| 1 | D-061: Test infrastructure (conftest.py, pytest config, service tests) | 3-4h | Debt | None |
| 2 | D-062: Quiz engine extraction | 1-2h | Debt | D-061 |
| 3 | D-063: Remove unused import | <0.1h | Debt | None |
| 4 | M5 remediation: Fix try/except + test injection | 8-12h | Debt | D-061 |
| 5 | C34: Company Story Timeline (card-based approach) | 14-18h | Feature | M5 fix for live data |
| 6 | C105: Simple/Detailed Toggle (business card only) | 10-14h | Feature | None |
| 7 | D-064+D-065+D-066: Fix inline HTML | 1-2h | Debt | None |
| **TOTAL** | | **37-52h** | | |

### Sprint 11+ (Directional)
- C107: Inline AI Explanations (requires D5 LLM abstraction first)
- C108: Insider Trading Context (requires data feasibility verification)
- C110: Earnings Story (P1, same as C94 from Round 17)
- C109: Compare Timelines (compound C38+C34)

### Design Grade
**A** (maintained, 12th consecutive A/A-). Condition: Fix D-062, D-064, D-065, D-066 in Sprint 10.

### Structural Changes Required
1. M5 fix before C34 live data integration (sequencing constraint)
2. D-061 before D-062 (test coverage before refactoring)
3. C107-C112 explicitly marked as Sprint 11+ scope in issues.md
4. Design grade A condition includes all 4 inline HTML items (D-062, D-064, D-065, D-066)
5. Document all session state keys in main.py comment block (D-065 mitigation)

---
*Effort: 37-52h Sprint 10*
*Cumulative remaining (Sprint 10+): ~37-52h committed + 53-79h future*
*Next cycle: 🔧 Development → Sprint 10 → 🔍 Review Round 23 → Sprint 11*
