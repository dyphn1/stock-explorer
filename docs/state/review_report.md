# Review Report
## Theme: Review (🔍) — Round 20
## Date: 2026-06-13

---

## 1. Key Findings Summary

### Architecture
- **D6 (YAML migration)**: Partially resolved — only 1 of 6 data blocks migrated. `market_event_service.py`'s `_CASE_STUDIES` (230 lines) is a NEW D6 violation introduced by C84.
- **D-044 (market_data.py)**: ✅ Confirmed resolved — clean 283-line service with 8 well-designed functions.
- **D7 (N+1 fix)**: ✅ Confirmed resolved — `ThreadPoolExecutor(max_workers=10)` in `category_browser.py`.
- **D3 (card consolidation)**: ✅ Confirmed resolved — `_subsidiary_card()` and `_count_label()` helpers added.
- **8 new debt items**: D-048 through D-056 (see Technical Debt section).
- **Top 3 architecture recommendations**:
  1. Complete D6 YAML migration (3-4h) — highest impact, unblocks content scaling
  2. Extract inline HTML from `sector_heatmap.py` and `market_event_case_study.py` (2-3h)
  3. Fix D8/D9/D10 performance debt (3-4h)

### Design
- **Design Grade: A-** (downgraded from A due to inline HTML enforcement gap)
- **D3 card consolidation**: Partially effective — `group_structure.py` fully consolidated, but C84 introduced 116 lines of new inline HTML.
- **5 new P2 issues**: D-049 through D-053 (C84 inline HTML, non-standard card styling, undocumented components).
- **"No Inline HTML" rule**: NOT enforceable without automated CI checking. Every sprint adds more inline HTML.
- **Top 3 design recommendations**:
  1. Add CI check for `unsafe_allow_html=True` before Sprint 8
  2. Standardize `_subsidiary_card()` styling to match design system
  3. Create card component gallery in design system doc

### Competitor Research
- **10 new competitors analyzed**: Luca AI, ticker.ai, Chartr, Alopexx, StonkGrid, Tapp.finance, 群益金融資訊網, PChome股市頻道, etc.
- **6 new feature gaps identified** (C98-C103):
  - C98: Event Interpretation Engine — P1, 14-18h — CONDITIONAL
  - C99: Scrollytelling — P3 (downgraded), 16-22h — DEFERRED to Sprint 10+
  - C100: Natural Language Screener — **REJECTED** (contradicts historian positioning)
  - C101: Comprehension Check Quiz — P2, 8-12h — CONFIRMED (replaces C52)
  - C102: Market Narrative Feed — **REJECTED** (market news, not historian)
  - C103: Learn First Gate — P2, 10-14h — CONDITIONAL (rename to "First Visit Guide")
- **Cumulative totals**: 86 competitors analyzed, 103 feature gaps identified (C01-C103)

### Cost Estimates
- **Sprint 8 (Debt-First)**: 10-17h debt clearance before any new features
- **Sprint 9**: C98 spike (2h) + C98 dev (14-18h) + C101 (8-12h) + C103 (10-14h) = 34-46h
- **Sprint 10+**: C99 (16-22h) + remaining backlog

---

## 2. Feature Gaps (New from Round 20)

| ID | Feature | Status | Priority | Effort |
|----|---------|--------|----------|--------|
| C98 | Event Interpretation Engine | CONDITIONAL | P1 | 14-18h |
| C99 | Scrollytelling Visual History | DEFERRED to Sprint 10+ | P3 | 16-22h |
| C100 | Natural Language Screener | **REJECTED** | — | — |
| C101 | Comprehension Check Quiz | CONFIRMED (replaces C52) | P2 | 8-12h |
| C102 | Market Narrative Feed | **REJECTED** | — | — |
| C103 | First Visit Guide (renamed) | CONDITIONAL | P2 | 10-14h |

---

## 3. Design Improvements

### Immediate (Before Sprint 8)
1. **Add CI check for inline HTML** — automated enforcement of "No Inline HTML" rule
2. **Standardize `_subsidiary_card()` styling** — change to `background:#F8F9FA` + `border-left:4px solid`

### During Sprint 8
3. **D-049**: Refactor C84 key metrics to use `_白话_card()` — <0.5h
4. **D-050**: Refactor C84 related stocks to use `_subsidiary_card()` — 0.5-1h
5. **D-052**: Standardize `_subsidiary_card()` styling — 0.5-1h
6. **D-053**: Document `_count_label()` in design system — 0.5h

### Design Grade
**A-** (downgraded from A) — Design system quality is A, but adoption is B+ due to persistent inline HTML. Grade returns to A once automated enforcement is implemented.

---

## 4. Technical Debt Updates

### Newly Identified This Round
- **D-048**: `market_event_service.py` `_CASE_STUDIES` hardcoded (230 lines) — P1, 1-2h
- **D-049**: `get_events_for_stock()` name collision — Medium, 0.25h
- **D-050**: `market_event_case_study.py` 116 lines inline HTML — Medium, 1-2h
- **D-051**: O(n) linear scan for case study lookups — Low, 0.5h
- **D-052**: `etf_browser.py` still sequential (D8) — Medium, 1-2h
- **D-053**: `adaptive_engine.py` no cache (D10) — Medium, 1-2h
- **D-054**: `watchlist.py` no cache (D9) — Medium, 1-2h
- **D-055**: `sector_heatmap.py` 150+ lines inline HTML — Medium, 2-3h
- **D-056**: `_section_title()` naming clarity — Low, 0.1h

### Confirmed Resolved
- **D-044**: market_data.py extraction — clean service layer
- **D7**: N+1 fix in category_browser.py — ThreadPoolExecutor
- **D3**: Card consolidation — new helpers in _router_base.py

### Still Open (High Priority for Sprint 8)
- **D-048** (P1): _CASE_STUDIES YAML migration — first task of Sprint 8
- **D6** (P1): Complete remaining 5 YAML migrations
- **D-055** (Medium): sector_heatmap.py inline HTML
- **D-050** (Medium): market_event_case_study.py inline HTML
- **D8/D9/D10** (Medium): Performance debt (parallelize ETF, cache watchlist/engine)

---

## 5. Challenger 3-Round Challenge

### Round 1: Gap Authenticity Challenge — ⚠️ PARTIALLY REVISED
**Challenger Finding**: C100 (Natural Language Screener) contradicts "historian, not stock picker" — a screener is stock-picking behavior regardless of framing. C102 (Market Narrative Feed) is a market news feature, not a historian feature. C99 (Scrollytelling) is too expensive (16-22h) for P2 priority.

**Verdict**: 2 features REJECTED (C100, C102), 1 DOWNGRADED to P3 (C99), 3 CONDITIONAL (C98, C101, C103).

### Round 2: Priority Challenge — ⚠️ REVISED
**Challenger Finding**: D6 was claimed "resolved" in Sprint 7 but only 1/6 blocks migrated. D-048 (_CASE_STUDIES) should be P1, not Medium. "No Inline HTML" rule is unenforceable without automated CI checking. Sprint 8 should be debt-first.

**Verdict**: D6 reclassified as "partially resolved." D-048 elevated to P1. Sprint 8 confirmed as debt-first. CI enforcement recommended.

### Round 3: Goal Alignment Challenge — ⚠️ REVISED
**Challenger Finding**: The two rejected features (C100, C102) failed the "ten-second test" — validates the filtering approach. Design Grade A downgraded to A- until automated inline HTML enforcement. M5 milestone (Adaptive updates within 24h) is NOT achieved. Competitor research needs restructuring to start from product vision pain points, not competitor features.

**Verdict**: 6 structural changes required (historian filter, feature triage, CI enforcement, milestone verification, competitor research restructuring, product vision update).

### Final Challenger Verdict: ⚠️ REQUIRES REVISION
- 2 features rejected, 1 cancelled, 1 deferred, 3 conditional
- Sprint 8 is debt-first (10-17h debt before features)
- 6 structural changes required

---

## 6. PM Decisions

### Sprint 8 Scope (REVISED — Debt-First, No New Features)
| Item | Hours | Type |
|------|-------|------|
| D-048: _CASE_STUDIES → YAML | 1-2h | Debt (P1) |
| D6: Remaining 5 YAML migrations | 3-4h | Debt (P1) |
| D-055: sector_heatmap.py inline HTML | 2-3h | Debt |
| D-050: market_event_case_study.py inline HTML | 1-2h | Debt |
| D8: Parallelize etf_browser.py | 1-2h | Debt |
| D9: Cache watchlist.py | 1-2h | Debt |
| D10: Cache adaptive_engine.py | 1-2h | Debt |
| D-056: _section_title() docstring | 0.1h | Debt |
| **TOTAL** | **10.2-17.1h** | |

### Sprint 9 (Post-Debt Features)
- C98 spike (2h) → C98 dev (14-18h) + C101 (8-12h) + C103 (10-14h) = 34-46h

### Sprint 10+ (Deferred)
- C99 (Scrollytelling) — P3, 16-22h

### Explicitly Rejected
- C100 (Natural Language Screener) — contradicts historian positioning
- C102 (Market Narrative Feed) — market news, not historian

### Explicitly Cancelled
- C52 (Quiz Mode) — replaced by C101

### Structural Changes Required
1. Add "historian filter" and "ten-second test" to competitor research template
2. Implement Feature Triage process (every 3 rounds, review entire backlog)
3. Add automated inline HTML enforcement (CI check)
4. Add milestone verification to sprint review checklist
5. Restructure competitor research to start from product vision pain points
6. Update product vision to expand LLM scope (translation → interpretation with data citation)

### Design Grade
**A-** (downgraded from A) — returns to A once CI enforcement is implemented.

---

*Effort: 10.2-17.1h Sprint 8 (debt), 34-46h Sprint 9 (features), 16-22h Sprint 10+*
*Cumulative remaining: ~60-85h (reduced from 82-112h by rejecting 2 features)*
