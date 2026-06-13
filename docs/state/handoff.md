# Handoff – Development
## Summary
- **Topic**: Development (🔧) — Sprint 13a
- **Date**: 2026-06-13 (Sprint 13a Dev completed)
- **Sprint Status**: Sprint 13a ✅ COMPLETE → Sprint 13b planned

## Key Metrics
- Design grade: A (17th consecutive A/A-)
- L0: 101/101 ✅ | L1: 20/20 ✅ | Tests: 149/149 ✅
- Sprint 13a: 3 commits, ~10-16h
- Features delivered: C33 Glossary (99 terms, tooltips in key metrics) + C48 Story Card (expander removed, always visible)
- Architecture: 🟢 HEALTHY — 30 service modules, 0 god modules, 100% Streamlit-free
- Sprint 13b: C36 Revenue Tree + C46 Moat Analysis (26-38h)

## Sprint Plans (Summary)
| Sprint | Items | Status |
|--------|-------|--------|
| Sprint 3-12 | Various | ✅ Complete |
| Sprint 13a | C33 Glossary + C48 Story Card | ✅ Complete |
| Sprint 13b | C46 Moat Analysis + C36 Revenue Tree | 📋 Planned (26-38h) |
| Sprint 14+ | C47 Education Academy + C40 Mode Toggle + User Validation + C113-C115/C118 | 📋 Deferred |

## Key Rules
- Content cap: 100 items max across all features
- Mandatory historian tone QA gate before each content feature ships
- Card-count limit: max 5 cards per page section (Direction A)
- Community features (C64, C67, C89) deprioritized — not feasible in Streamlit
- Content creation must be budgeted at 40% of effort for education features
- Priority resolution: vision alignment > retention impact > technical risk

## 🔧 Development Section (Sprint 13a — 2026-06-13)

Sprint 13a dev completed. 3 commits delivered.

**D-070 Fix — C48 Story Card expander removed (commit `...`):**
- Removed `st.expander("📌 30 秒認識這家公司", expanded=True)` wrapper from `_render_story_card()` in `_summary.py`
- Story card now renders directly on the page — always visible, no click required
- Also fixed D-068: replaced inline HTML health score `<div>` with `_summary_card("整體健康度", ...)` call
- This was the #1 P1 Sprint 13a prerequisite from Review Round 26

**C33 Glossary Service (3 commits):**
- `glossary_service.py` — new service module with `get_glossary_term()`, `get_all_terms()`, `search_terms()`
- `glossary.yaml` — 99 financial terms across 24 categories (獲利能力, 估值, 股利, 成長, 財務健康, 現金流, 市場, 市場趨勢, 市場參與者, 股東權益, 公司財務, 公司結構, 公司資訊, 分析方法, 技術分析, 選擇權/期貨, 風險指標, 投資工具, 投資策略, 投資行為, 總經, 財務報表, 財報項目)
- Each term has: `name`, `plain`, `example`, `analogy`, `category`
- `_glossary_tooltip()` component added to `_router_base.py` — renders ℹ️ popover with term definition
- Integrated into `_financial.py` key metrics: tooltips on 本益比, 毛利率, 營收年增率, ROE, 殖利率, 淨值比

**Key Findings:**
- Architecture: 🟢 HEALTHY — 0 god modules, 100% Streamlit-free, 30 service modules (was 29)
- L0: 101/101 ✅ | L1: 20/20 ✅ | Tests: 149/149 ✅
- D-074 (filelock) verified as already resolved — all 149 tests pass
- C48 Story Card is now always visible above-fold (no expander), directly supporting ten-second test principle

**New debt identified during Sprint 13a:** None.

## 🔧 Development Section (Sprint 12 — 2026-06-15) [ARCHIVED]

Sprint 12 dev completed. 3 commits delivered.

**Quick debt fixes (8 items, commit `658bd3f`):**
- D-035 ✅ Already done (peer cards use `_info_card()`)
- D-036 ✅ Fixed — `background:#FFF8F0` → `background:#F8F9FA` in risk dimension cards
- D-038 ✅ Fixed — moved `client.get_stock_info()` out of view layer to router
- D-044 ✅ Already done (uses `_section_title()`)
- D-047 ✅ Already done (uses `_section_title()`)
- D-064 ✅ Already done (uses `st.caption()`)
- D-065 ✅ Already done (uses `st.caption()`)
- D-066 ✅ Already done (uses `_info_card()`)

**Info Hierarchy (commit `fc4bafd`):**
- Above-fold: C48 (Story Card) → C37 → C39 → C43
- All other sections wrapped in `st.expander(expanded=False)` with Chinese labels
- C36 Revenue Tree relocated to standalone page (`src/pages/revenue_tree.py`)
- C38 Compare Stories relocated to standalone page (`src/pages/compare_stories.py`)
- Router and URL sync updated for new pages
- L0: 99/99 ✅ | L1: 20/20 ✅

**User Feedback (commit `1495c7e`):**
- Binary 👍/👎 buttons at bottom of Business Card page
- JSONL storage at `data/feedback.jsonl` with session-state dedup
- `feedback_service.py` — zero Streamlit dependency in service layer
- L0: 100/100 ✅ | L1: 20/20 ✅

**Key Findings:**
- Architecture: 🟢 HEALTHY — 0 god modules, 100% Streamlit-free, 100 L0 checks
- Design: A (16th consecutive) — Info Hierarchy directly supports PPT-style principle
- C36/C38 relocation reduces Business Card page from ~18 sections to 10 above-fold + expanders
- All verifications pass: L0 100/100, L1 20/20

**C40 Mode Toggle:** Deferred to Sprint 14 (per Challenger R21 revision)
**D02 Architecture Spike:** Deferred — requires separate investigation cycle

**New debt identified during Sprint 12:** None.

## 🔧 Development Section (Sprint 11 — 2026-06-15) [ARCHIVED]

Sprint 11 dev completed. 5 commits delivered: C117 + C116 + R3 + D-067 + D-071.
All verifications pass: L0 95/95, L1 18/18, Tests 149/149.
Architecture: 🟢 HEALTHY — 0 god modules, 100% Streamlit-free.

## 💡 Discussion Section (Round 27 — 2026-06-18)
**Topic**: Sprint 13b Scope Validation — C46 Moat Analysis + C36 Revenue Tree
**Challenger**: ✅ CONFIRMED with 2 revisions
**Key Decisions**: Full scope both features; C36 first then C46; Day 2 go/no-go gate; scoring rubric required before curation; pie chart default for C36
**Full details**: docs/state/handoff_discuss_r27.md

## 💡 Discussion Section (Round 21 — 2026-06-16) [ARCHIVED]
**Topic**: Sprint 12 Scope Validation + Post-Sprint 12 Roadmap
**Challenger**: ✅ CONFIRMED with 4 revisions
**Key Changes**: C40 deferred to Sprint 14; C48 Story Card added to Sprint 13a; C36/C38 relocation prerequisite; D02 architecture spike in Sprint 12
**Full details**: docs/state/handoff_discuss_r21.md

## 💡 Discussion Section (Round 20 — 2026-06-15)
**Topic**: C36-C47 Feature Candidates
**Finding**: 9 of 12 competitor-inspired features already shipped. Only 4 need work.
**Challenger**: ✅ CONFIRMED with 9 revisions
**Full details**: docs/state/handoff_discuss_r20.md

## 🔍 Review Section (Round 26 — 2026-06-17)

**Theme**: Review Round 26 — Sprint 12 Post-Mortem + Sprint 13a Prerequisites
**Participants**: PM, Architect, Designer, QA (timed out)

### Key Findings

**Sprint 12 Verification**: All 8 debt fix claims confirmed resolved. Info Hierarchy and User Feedback are well-architected.

**Architecture** (Architect review):
- Health: 🟢 HEALTHY — 0 god modules, 100% Streamlit-free, 29 service modules
- New debt: 5 items (D-072 through D-076)
- 🔴 D-074: Test infrastructure regression — 131/149 tests broken (filelock dependency)
- Top recommendation: Fix D-074 (0.25h) as Sprint 13a prerequisite

**Design** (Designer review):
- Grade: A (17th consecutive)
- New issues: 3 items
  - D-068 (P2): Story card health indicator inline HTML
  - D-069 (P2): _helpers.py card components bypass _router_base.py
  - **D-070 (P1)**: C48 Story Card hidden behind expander — most important Sprint 13a fix
- Sprint 13a design specs delivered: C33 tooltip pattern, C48 enhancement plan

**QA**: Subagent timed out on web research. Designer covered competitor analysis.

### Sprint 13a Prerequisites
1. Fix D-074 (filelock dependency, 0.25h) — restore test infrastructure
2. Remove C48 expander wrapper (D-070, 1h) — make story card always visible
3. Define glossary YAML schema (0.5h)

### New Debt Summary
- Total: 71 items | High: 1 | Medium: ~47 | Low: ~23
- Resolved in Sprint 12: 8 | Pending Sprint 13a: D-074, D-073, D-072 + existing backlog

### Competitor Insights (from Designer)
1. Glossary tooltips are table stakes — Stash/Investopedia/Finimize all have them
2. C48 Story Card is competitive but should be always visible (not in expander)
3. PPT-style + progressive disclosure is now a stronger differentiator

### Design System Updates Needed
- C33: Add `_glossary_tooltip()` component spec
- C48: Add `_hero_card()` or enhanced `_summary_card()` spec
- D-069: Document or consolidate `_helpers.py` card components

## 🔍 Review Section (Round 28 — 2026-06-18)

**Theme**: Review Round 28 — Sprint 13a Post-Mortem + Sprint 13b Prerequisites
**Participants**: PM, Architect, Designer, QA, Challenger

### Key Findings

**Sprint 13a Verification**: Both C33 Glossary and C48 Story Card verified clean.
- C33: `glossary_service.py` (73 lines), `glossary.yaml` (99 terms), `_glossary_tooltip()` — no debt
- C48: Always visible, zero inline HTML, pure component construction — D-068/D-070 resolved

**Architecture** (Architect review):
- Health: 🟢 HEALTHY — 30 service modules, 0 god modules, 100% Streamlit-free
- New debt: 2 items (D-077, D-078) — both 🟢 Low, deferrable
- C36 Revenue Tree: 🟢 READY — all infrastructure exists (73-line page + service layer)
- C46 Moat Analysis: 🟡 CONDITIONALLY READY — needs data model pre-work

**Design** (Designer review):
- Grade: A (18th consecutive A/A-)
- New issues: 2 items
  - D-079 (P2): Dual tooltip pattern on key metrics — merge into single interaction
  - D-080 (P2): Story card health score border should be color-coded by health level
- C36 design: Add glossary tooltips, concentration warning, trend mini-chart
- C46 design: Radar chart + card-based layout, standalone page, YAML data source

**QA** (Competitor research):
- 4 new feature gaps: C123 (Revenue Geography), C124 (Moat Types), C125 (Segment Profitability), C126 (Moat Comparison)
- Regression check: 10 of 12 previous gaps still fully relevant
- Cumulative: 126 feature candidates (C01-C126)

**Challenger**: ✅ CONFIRMED with 6 conditions
1. C46 must be evidence-first (not rating-first) to avoid stock-picking drift
2. C124 (Moat Type Classification) must be merged into C46's Sprint 13b scope — not deferred
3. C46 scoring rubric must be comparison-ready for C126 in Sprint 14
4. C123 needs TW-competitor validation before Sprint 14 commitment
5. Content creation must be explicitly budgeted at 40% for C46 (education feature)
6. D-079 must be a Day 0 prerequisite before any Sprint 13b tooltip work

### Sprint 13b Adjusted Plan (per Challenger conditions)
1. **Day 0**: Fix D-079 (merge dual tooltips, 1-2h) + begin C46 content pre-work
2. **C36 Revenue Tree polish**: Glossary tooltips, concentration warning, trend mini-chart
3. **C46 Moat Analysis**: Include moat type classification (C124 merged), evidence-first design, comparison-ready scoring
4. **Content budget**: 40% of C46 effort for moat.yaml + scoring rubric + explanations

### New Debt Summary
- Total: 73 items | High: 1 | Medium: ~47 | Low: ~25
- Resolved in Sprint 13a: 0 new (all from Sprint 12, already counted)
- New in Round 28: D-077, D-078 (architect), D-079, D-080 (designer)

### Competitor Insights
1. Revenue geography (C123) is proven by Koyfin/Simply Wall St but data availability for TW stocks uncertain
2. Moat type classification (C124) is Morningstar's gold standard — no TW competitor has it
3. Segment profitability (C125) is Simply Wall St's differentiator — no TW competitor shows it
4. Moat comparison (C126) directly serves core value #5 (benchmark-oriented)

### Design System Updates Needed
- Add `_glossary_tooltip()` component spec
- Add "health card" variant with dynamic border color
- Document "one help icon per metric" rule
- Add moat analysis page spec

## Next Cycle
✅ Round 28 Review COMPLETE → Sprint 13b (C36 Revenue Tree + C46 Moat Analysis with C124 merged) → 🔧 Development
OR → 💡 Discussion Round 29 (Sprint 14 scope: C47 Education Academy + C40 Mode Toggle + C123/C125/C126)

## Archive (Previous Rounds)
- Round 24 Review: docs/state/review_report_r24.md | Sprint 10 verified, Sprint 11 planned
- R19/R20 Discussion: docs/state/handoff_discuss.md | docs/state/handoff_discuss_r20.md
- Sprint 11 Execution: C117 + C116 + R3 + D-067 + D-071 (5 commits)
