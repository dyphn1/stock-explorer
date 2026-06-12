# Review Report
## Theme: Review (🔍) — Round 17
## Date: 2026-06-21

---

## 1. Key Findings Summary

### Architecture
- **D-043 (P0 BUG)**: `_sections.py` calls non-existent `get_roe_analyzer()`/`get_pbr_analyzer()` — runtime NameError crash on business card page. Fix: 0.25h.
- **D-042**: `_sections.py` grew to 918 lines (was 612 after D24) — exceeds D37 threshold by 53%. Split needed: 1-2h.
- **D-044**: `sector_heatmap.py` (444 lines) has no service-layer abstraction, inline data fetching. Extract: 2-3h.
- **D-045**: `compare_stories.py` imports `generate_key_takeaways` but never uses it. Dead import: 0.1h.
- **D-046**: `_render_share_section()` JS references non-existent element IDs — copy button non-functional. Fix: 1h.
- **D-047**: `_section_title()` has inverted `if not title:` logic (pre-existing). Fix: 0.1h.
- D37 (sections split): 🔴 OVERDUE — 918 lines
- D39 (duplicate imports): Worsened — 70 lines of duplication across `_main.py` + `_sections.py`
- D25 (market data abstraction): NOT addressed — C51 built without `market_data.py`
- D3 (inline HTML): Worsened — `sector_heatmap.py` added 150+ lines inline HTML

### Design
- **Grade A maintained** (7th consecutive round) — but increasingly fragile
- **4 new P2 issues**: D-045 (C51 inline HTML), D-046 (C51 KPI card), D-047 (C53-1 header), D-048 (C53-1 st.html)
- **3 unfixed issues from Round 16**: D-042 (mini-cards), D-043 (dividend table), D-044 (read next header)
- Sprint 5 prerequisites (D-039, D-040, D-041) still NOT STARTED — 3 rounds now
- Sprint 5 design readiness: 6/10 — MODERATE RISK

### Competitor Research
- 5 new features identified (C93-C97): Dividend Income Calendar, Earnings Story, Watchlist Health Dashboard, Sector Ecosystem Map, First 30 Days
- 81 total competitors analyzed, 74 total features identified (C01-C97)
- Key insight: Cross-competitor synthesis creates category-of-one features
- White space focus: execution gaps + TW market-specific opportunities

### Cost Estimates
- P0 Bugs: 0.25h
- Sprint 5 Prerequisites: 5.6h
- Sprint 5 Features (C71, C73, C74): 42h
- Design Debt (D-042-D-048): 5.75h
- Architecture Debt: 3.5h
- **Grand Total: 57.1h** (vs 46.4h in Round 16, +10.7h)

---

## 2. Feature Gaps (New from Round 17)

| ID | Title | Priority | Effort | Source | Alignment |
|----|-------|----------|--------|--------|-----------|
| C93 | Dividend Income Calendar (Market-Wide + Income Projection) | P1 | 12-16h | 口袋股利 + C1 + MoneySmart synthesis | Story first + Point-to-point + Historian |
| C94 | Earnings Story (Post-Earnings Plain-Language Narrative) | P1 | 14-18h | M5 gap + Finshots + The Indicator synthesis | Story first + Adaptive + Ten-second test + Historian |
| C95 | Watchlist Health Dashboard (Aggregate Portfolio Health) | P2 | 10-14h | watchlist.py gap + Simply Wall St + Tykr synthesis | Story first + PPT-style + Ten-second test + Historian |
| C96 | Sector Ecosystem Map (Visual Supply Chain Relationships) | P2 | 16-22h | group_structure.py gap + Visual Capitalist + TW market | Story first + PPT-style + Point-to-point + Historian |
| C97 | First 30 Days (Structured Beginner Curriculum / C58 Implementation) | P1 | 18-24h | Beginner journey mapping + Bloom + Zerodha Varsity | Point-to-point + Ten-second test + Historian + Beginner-friendly |

**Challenger Revision**: C93 CONDITIONAL (position as intermediate), C94 CONDITIONAL (historical framing + disclaimers), C95 REJECTED for current sprint (Sprint 7+), C96 REJECTED for current sprint (Sprint 7+), C97 CONDITIONAL (content-only, no new feature dev).

**Feature Budget**: C52 (Quiz Mode) and C55 (Investment Diary) deferred to Sprint 8+.

---

## 3. Design Improvements

### New Issues
| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-045 | C51 sector grid/top movers use inline HTML with non-standard padding/border-radius | P2 | 1-2h |
| D-046 | C51 4th KPI card uses inline HTML instead of _白话_card() | P2 | 0.5h |
| D-047 | C53-1 share section header doesn't use _section_title() | P2 | 0.5h |
| D-048 | C53-1 share button uses st.html() with non-functional JS | P2 | 1-2h |

### Design System Updates Needed (8 items)
1. Mini Score Card variant spec (D-042)
2. Compact Card variant for grid layouts (D-045)
3. Study Log Card specification (C71)
4. Expert Analysis Card specification (C73)
5. Historical Scenario Card specification (C74)
6. Section Header Standard (D-039)
7. Disclaimer Component spec (D-040)
8. JavaScript Escape Hatch pattern documentation (D-048)

---

## 4. Technical Debt Updates

### Newly Identified This Round
| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-043 | P0 NameError: `get_roe_analyzer()`/`get_pbr_analyzer()` don't exist | HIGH | 0.25h |
| D-042 | `_sections.py` at 918 lines — exceeds D37 threshold | Medium-High | 1-2h |
| D-044 | `sector_heatmap.py` no service-layer abstraction | Medium | 2-3h |
| D-045 | Dead import in `compare_stories.py` | Low | 0.1h |
| D-046 | Share section JS references non-existent element IDs | Medium | 1h |
| D-047 | `_section_title()` inverted logic | Low | 0.1h |

### Still Open (High Priority)
- **D-043**: P0 bug — runtime crash (0.25h)
- **D37**: `_sections.py` split — 918 lines (1-2h)
- **D-044 (architect)**: `market_data.py` extraction (2-3h)
- **D-039/040/041**: Sprint 5 prerequisites — NOT STARTED (2.5h)

---

## 5. Challenger 3-Round Challenge

### Round 1: Gap Authenticity Challenge
**Challenger questions**: Are C93-C97 really gaps? Is C97 too ambitious? Is C96 too complex? Are we falling into the "feature smoothie" trap?

**Team response**: All features pass historian filter. C93 serves TW dividend investors. C94 is historical, not predictive. C97 IS C58 implementation. Cross-competitor synthesis is validated approach.

**Verdict**: ⚠️ PARTIALLY REVISED — C93 conditional (intermediate positioning), C94 conditional (historical framing), C95 rejected (Sprint 7+), C96 rejected (Sprint 7+), C97 conditional (content-only).

### Round 2: Priority Challenge
**Challenger questions**: Should new features take priority over Sprint 5? Is D-043 being given enough urgency? Should D37 be elevated?

**Team response**: Sprint 5 planned work takes priority. D-043 must be fixed immediately. D37 elevated to P1.

**Verdict**: ⚠️ REVISED — Priority sequence: D-043 → prerequisites → C71/C73/C74 with D37 split → debt → new features. Sprint 5 scope locked.

### Round 3: Goal Alignment Challenge
**Challenger questions**: Does direction still align with "historian"? Are there contradictions? What are the risks of 97 features? Feature Budget Rule?

**Team response**: All features pass historian filter with proper framing. C97 replaces C58. Backlog is a menu, not a mandate. Effort is realistic.

**Verdict**: ⚠️ REVISED — Historian alignment conditional on framing. Feature Triage process established. Feature Budget: for every 5 new features, 1 existing P2 deferred. C52 and C55 deferred to Sprint 8+.

**Final Challenger Decision**: ⚠️ REVISED with conditions:
1. D-043 fixed before any new development
2. Sprint 5 scope locked (C71 + C73 + C74 + prerequisites)
3. D37 elevated to P1
4. Feature Triage every 3 rounds
5. C94 must use _historian_disclaimer() and "歷史統計" framing
6. C93 positioned as intermediate feature

---

## 6. PM Decisions

### Sprint 5 LOCKED (Challenger Confirmed)
**Prerequisites first**: D-043 (0.25h) + D-039 (1.5h) + D-040 (0.5h) + D-041 (1.5h) + D-047 (0.1h) = 4.35h
**Then features**: C71 (10h) → C73 (18h) → C74 (14h) = 42h
**Alongside**: D37 sections split (2h) + D-044 architect market_data.py (2.5h)
**Total Sprint 5**: ~50.85h

### New Features (Sprint 6+)
**Priority order**: C93 (14h) → C94 (16h) → C97 (21h) = 51h (midpoint of ranges)

### Deferred Features
- C52 (Quiz Mode) → Sprint 8+
- C55 (Investment Diary) → Sprint 8+
- C95 (Watchlist Health Dashboard) → Sprint 7+
- C96 (Sector Ecosystem Map) → Sprint 7+

### Design Debt Quick Wins (Anytime)
- D-037: Fix 白话 card background (0.3h)
- D-036: Fix risk card background (0.3h)
- D-044: Fix read next header (0.3h)
- D-046: Fix 4th KPI card (0.3h)
- D-047: Fix share header (0.3h)
- **Total quick wins: ~1.5h**

---

## 7. Files Created/Modified This Round
- Created: `docs/research/competitor_research_r17.md`
- Created: `docs/design/architect_review_r17.md`
- Created: `docs/design/designer_review_r17.md`
- Created: `docs/design/developer_estimates_r17.md`
- Created: `docs/state/review_report.md` (this file)
- Modified: `docs/workflow/challenge_log.md` (Round 17 challenge)
- Modified: `docs/status/issues.md` (C93-C97 added)
- Modified: `docs/status/current_problems.md` (D-045-D-048 added)
- Modified: `docs/status/tech_debt.md` (D-042-D-047 added)
- Modified: `docs/state/handoff.md` (Review section updated)
- Modified: `docs/state/handoff_review.md` (Round 17 results)

---

*Next cycle: 🔧 Development → Sprint 5 execution (D-043 fix → prerequisites → C71 → C73 → C74)*
*Next review: Sprint 5 mid-point (after D-043 + prerequisites + one feature complete)*
