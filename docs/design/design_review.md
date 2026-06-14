# Stock Explorer Design Review

## 2026-06-13 Design Review — Review Round 20 (Sprint 7)

> **Author**: Design Reviewer
> **Date**: 2026-06-13
> **Context**: Round 20 review — Sprint 7 deliverables: C84 (Market Event Case Study page), D3 (card consolidation with `_subsidiary_card` and `_count_label` helpers). Reviewing design compliance of new page and card consolidation results.
> **Current Design Grade**: A (maintained for 10th consecutive round)

---

## Table of Contents

1. [Design Grade Assessment](#design-grade-assessment-round-20)
2. [C84 Market Event Case Study — Design Compliance Review](#c84-market-event-case-study--design-compliance-review)
3. [D3 Card Consolidation — Verification](#d3-card-consolidation--verification)
4. [New Design Issues Identified](#new-design-issues-identified-round-20)
5. [D3 Effectiveness Assessment](#d3-effectiveness-assessment)
6. [Updated Issue Checklist](#updated-issue-checklist-round-20)
7. [Recommendations Summary](#recommendations-summary-round-20)

---

## Design Grade Assessment (Round 20)

### Overall Grade: A (Maintained — 10th Consecutive)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | C84 is a standalone page (no stock_id) — correctly uses Zone C only. No zone mixing. |
| **PPT-Style Adherence** | A- | C84 follows one-key-point-per-page (each case study answers "what happened?"). Lessons use `st.expander` for progressive disclosure. Minor: text volume in "What Happened" section exceeds 200-char guideline. |
| **Card Component Consistency** | B+ | **Mixed results**: D3 fixed `group_structure.py` (0 inline HTML). But C84 introduces 2 new inline HTML blocks (D-049, D-050). `etf_browser.py` still has 3 inline HTML usages (D-051). Net effect: inline HTML count roughly unchanged. |
| **Color System** | A | C84 uses correct colors: `#3498DB` (info), `#27AE60` (positive), `#E74C3C` (negative), `#F8F9FA` (card bg). `_subsidiary_card` uses non-standard white bg (D-052). |
| **Plain-Language System** | A | C84 historian tone is excellent. Disclaimer at top and bottom. Lessons use beginner-friendly language. |
| **Loading/Error States** | B | C84 has no loading spinner (data is local JSON). Error state for missing case study uses `st.error()`. No standardized empty state component used. |
| **Mobile Responsiveness** | B- | D-006 still unresolved. C84 key metrics use 2-col layout that won't stack gracefully. |
| **Design System Documentation** | B | D-004 resolved (doc exists at `docs/design/design_system.md`). But new components (`_subsidiary_card`, `_count_label`) not yet added to design system doc. |

### Grade Justification

The grade is maintained at **A** for the 10th consecutive round because:
- All P0 issues remain resolved
- C84 is a well-designed standalone page with strong historian positioning
- D3 card consolidation successfully standardized `group_structure.py`
- `_subsidiary_card()` and `_count_label()` are valuable additions to the shared component library
- No new P0 or P1 issues introduced
- New P2 issues (D-049 through D-053) are minor and fixable within 0.5-2h each

**Risk**: The grade could slip to A- in Round 21 if:
- Inline HTML continues to be added in new pages faster than old pages are fixed (D-003 net-negative trend)
- `_subsidiary_card` non-standard styling (D-052) is copied as a pattern by future developers
- ETF browser table-like layout (D-051) is extended to more pages

---

## C84 Market Event Case Study — Design Compliance Review

### What Was Implemented
- **Page**: `src/pages/market_event_case_study.py` (183 lines)
- **Data**: Local JSON via `market_event_service` (no API calls for case study content)
- **Sections**: Historian disclaimer → Case study selector → Hero → What Happened → Key Metrics → Lessons Learned → Related Stocks → All Case Studies overview → Historian disclaimer
- **Components used**: `_info_card()`, `_section_title()`, `_historian_disclaimer()` — all shared components

### Design Compliance Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Zone layering** | ✅ Pass | Standalone page, no navbar/sidebar mixing. All content in Zone C. |
| **PPT-style** | ✅ Pass | One key point per case study ("what happened and why"). Clear hero section. |
| **Progressive disclosure** | ✅ Pass | Lessons use `st.expander(expanded=False)`. All case studies in expandable list. |
| **Historian tone** | ✅ **Excellent** | Disclaimer at top and bottom. Factual language throughout. No buy/sell advice. |
| **Card usage** | ⚠️ **Mixed** | Historian disclaimer correctly uses `_info_card()`. But Key Metrics (lines 109-117) and Related Stocks (lines 143-157) use inline HTML. |
| **Color system** | ✅ Pass | All colors match design system. Severity badges use correct emoji + color mapping. |
| **Plain-language** | ✅ Pass | "以歷史學家的角度，回顧台灣與全球金融市場的重大事件" — clear purpose. |
| **Ten-second test** | ✅ Pass | Page purpose is immediately clear from hero section. |
| **Button keys** | ✅ Pass | Uses `f"related_{study['id']}_{stock['stock_id']}"` and `f"goto_{cs['id']}"` — unique. |
| **Error handling** | ⚠️ Partial | Uses `st.error()` for missing case study. No standardized empty state component. |
| **Text volume** | ⚠️ Concern | "What Happened" section may exceed 200-char guideline for long case studies. |

### Verdict
**Well-designed page with strong historian positioning.** The overall structure, tone, and progressive disclosure are excellent. The main issues are the two inline HTML card blocks (D-049, D-050) that duplicate existing shared component styling.

---

## D3 Card Consolidation — Verification

### What D3 Delivered
1. **`_subsidiary_card()`** added to `_router_base.py` (lines 117-151) — renders subsidiary info with holding badge, business description, and relation
2. **`_count_label()`** added to `_router_base.py` (lines 154-164) — renders muted count label
3. **`group_structure.py`** refactored to use `_subsidiary_card()` and `_info_card()` — **zero inline HTML** (verified: 0 `unsafe_allow_html` occurrences)
4. **`etf_browser.py`** uses `_count_label()` for the ETF count display (line 83)

### Verification Results

| File | Before D3 | After D3 | Status |
|------|-----------|----------|--------|
| `group_structure.py` | Inline HTML cards with non-standard styling | Uses `_subsidiary_card()`, `_info_card()`, `_summary_card()`, `_section_title()` | ✅ **Fully consolidated** |
| `etf_browser.py` | No count label component | Uses `_count_label()` for count display | ✅ **Partially consolidated** (3 inline HTML usages remain in table rows) |
| `_router_base.py` | 3 card components (`_白话_card`, `_summary_card`, `_info_card`) | 5 components (+ `_subsidiary_card`, `_count_label`) | ✅ **Extended** |

### D3 Effectiveness Assessment

**Strengths**:
- `group_structure.py` is now a model page — all shared components, zero inline HTML
- `_subsidiary_card()` is a well-designed component with clear API (name, hold_label, hold_color, holding, revenue, business, relation)
- `_count_label()` is simple and effective
- The pattern of adding page-specific card types to `_router_base.py` is a good extensibility approach

**Weaknesses**:
- `_subsidiary_card()` uses non-standard card styling (D-052) — `background:white` + `border:1px solid #ECF0F1` instead of standard `background:#F8F9FA` + `border-left:4px solid`
- `_count_label()` is undocumented in the design system (D-053)
- D3 did not address existing inline HTML in `watchlist_page.py`, `etf_detail.py`, `business_card.py` (C41/C44)
- New page `market_event_case_study.py` was created during the same sprint but did NOT use shared components for all cards — suggesting the D3 consolidation message didn't fully propagate

**Net Assessment**: D3 was **partially effective**. It successfully consolidated `group_structure.py` and added useful new components. However, the overall inline HTML problem (D-003) remains unresolved because:
1. New pages still use inline HTML (C84 added 2 new blocks)
2. Old pages were not cleaned up (`watchlist_page.py`, `etf_detail.py`, `business_card.py`)
3. The new `_subsidiary_card` itself uses non-standard styling

---

## New Design Issues Identified (Round 20)

### D-049: C84 Key Metrics Cards Use Inline HTML Instead of _白话_card()
- **Severity**: P2 | **Effort**: <0.5h
- **Issue**: Lines 109-117 use inline HTML that is a near-exact copy of `_白话_card()` styling
- **Fix**: Replace with `_白话_card(label, value, analogy)` — data structure already matches

### D-050: C84 Related Stocks Cards Use Non-Standard Card Styling
- **Severity**: P2 | **Effort**: 0.5-1h
- **Issue**: Lines 143-157 use `background:white` + `border:1px solid #ECF0F1` instead of standard card styling
- **Fix**: Create `_related_stock_card()` or use `_info_card()` + button

### D-051: ETF Browser Table-Like Rows Use Inline HTML for Colored Values
- **Severity**: P2 | **Effort**: 2-3h
- **Issue**: Hot ETF and Dividend Ranking rows use `st.columns` with inline HTML color spans — same pattern as D-010 watchlist
- **Fix**: Redesign using card-based layout with `_info_card()`

### D-052: _subsidiary_card() Uses Non-Standard Card Styling
- **Severity**: P2 | **Effort**: 0.5-1h
- **Issue**: Uses `background:white` + `border:1px solid #ECF0F1` instead of design system standard
- **Fix**: Change to standard styling or document as "subsidiary card" variant in design system

### D-053: _count_label() Is an Undocumented Component Type
- **Severity**: P2 | **Effort**: 0.5h
- **Issue**: New component type not documented in design system
- **Fix**: Add to design system doc as "muted label" component type

---

## Updated Issue Checklist (Round 20)

### P0 — Blocking Issues
*(None)*

### P1 — Important Issues (3 items)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| D-003 | Inconsistent Card Styling | ⚠️ Partially Fixed (D3) | 2-3h remaining |
| D-005 | Business Card Page Overload | ⚠️ Stable | 3-4h |
| D-006 | Mobile Responsiveness Gaps | ❌ Unresolved | 4-6h |

### P2 — Optimization Issues (22 items)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| D-007 | No Discovery Mechanism | ❌ Unresolved | 12-16h |
| D-008 | Loading State Inconsistency | ❌ Unresolved | 1-2h |
| D-009 | Error State Inconsistency | ❌ Unresolved | 1h |
| D-010 | Watchlist Uses Non-PPT Layout | ❌ Unresolved | 2-3h |
| D-011 | Category Browser Uses Dense Tables | ❌ Unresolved | 2-3h |
| D-012 | No Glossary/Tooltip System | ❌ Unresolved | 8-12h |
| D-015 | No Structured Learning Path | ❌ Unresolved | 20-30h |
| D-032 | No Progressive Disclosure Pattern | ❌ Unresolved | 3-4h |
| D-033 | No Standardized Empty State | ❌ Unresolved | 1h |
| D-035 | C41 Peer Cards Use Inline HTML | ❌ Unresolved | 0.5-1h |
| D-036 | C44 Risk Cards Non-Standard Bg | ❌ Unresolved | <0.5h |
| D-038 | C41 Calls API in View Layer | ❌ Unresolved | 1-2h |
| D-039 | No Standardized Section Header | ❌ Unresolved | 1-2h |
| D-040 | No Standardized Disclaimer | ❌ Unresolved | 0.5h |
| D-041 | No Sprint 5 Card Components | ❌ Unresolved | 1h |
| D-042 | Health Mini-Cards Non-Standard | ❌ Unresolved | 0.5h |
| D-043 | Dividend Table Uses Inline HTML | ❌ Unresolved | 1-2h |
| D-044 | C41 Header Doesn't Use _section_title | ❌ Unresolved | <0.5h |
| D-045 | Sector Grid Uses Inline HTML | ❌ Unresolved | 1-2h |
| D-046 | 4th KPI Card Uses Inline HTML | ❌ Unresolved | <0.5h |
| D-047 | Share Section Header Not Standard | ❌ Unresolved | <0.5h |
| D-048 | Share Button Uses Non-Functional JS | ❌ Unresolved | 1-2h |
| D-049 | C84 Key Metrics Inline HTML | 🆕 New | <0.5h |
| D-050 | C84 Related Stocks Non-Standard | 🆕 New | 0.5-1h |
| D-051 | ETF Browser Table-Like Rows | 🆕 New | 2-3h |
| D-052 | _subsidiary_card Non-Standard | 🆕 New | 0.5-1h |
| D-053 | _count_label Undocumented | 🆕 New | 0.5h |

---

## Recommendations Summary (Round 20)

### Top 3 Design Recommendations

1. **🔴 Enforce "No Inline HTML" Rule Before Sprint 8**
   - The D3 consolidation added new components but didn't prevent new inline HTML in C84
   - **Action**: Add a pre-commit or pre-review checklist item: "All new cards must use shared components from `_router_base.py`"
   - **Impact**: Prevents D-003 from worsening. Estimated 5-10h to fix all existing inline HTML across pages.

2. **🟡 Standardize _subsidiary_card Styling**
   - The new `_subsidiary_card` uses non-standard styling that could be copied as a pattern
   - **Action**: Change to `background:#F8F9FA` + `border-left:4px solid` to match design system, OR document as a recognized "subsidiary card" variant
   - **Impact**: Prevents D-052 from becoming a pattern for future components. <0.5h.

3. **🟢 Create Card Component Gallery in Design System Doc**
   - New components (`_subsidiary_card`, `_count_label`) are not documented in the design system
   - **Action**: Add a "Component Gallery" section to `docs/design/design_system.md` with all 5 card components, their APIs, and usage examples
   - **Impact**: Prevents future developers from reinventing card styles. 1-2h.

### Quick Wins (Can be done in <1h each)
- D-049: Replace C84 key metrics inline HTML with `_白话_card()` (<0.5h)
- D-052: Fix `_subsidiary_card` background to `#F8F9FA` (<0.5h)
- D-053: Document `_count_label` in design system (0.5h)

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | D-003 fully resolved (all inline HTML replaced), D-005 addressed with progressive disclosure |
| **Expected case** | A | D-049-D-053 fixed in Sprint 8, D-003 net unchanged |
| **Worst case** | A- | Inline HTML continues to grow, D-003 becomes unmanageable |

---

## 2026-06-19 Design Review — Review Round 13

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: Round 13 review — comparing competitor designs from Round 12 research, assessing current UI state, and proposing design improvements. This review covers the period since the Round 12 review (2026-06-18).
> **Current Design Grade**: A (maintained from Round 12)

---

## Table of Contents

1. [Design Grade Assessment](#design-grade-assessment)
2. [Competitor Design Trends (Round 12 Research)](#competitor-design-trends-round-12-research)
3. [Current Unresolved Problems Analysis](#current-unresolved-problems-analysis)
4. [New Design Improvement Proposals](#new-design-improvement-proposals)
5. [Updated Issue Checklist](#updated-issue-checklist)
6. [Recommendations Summary](#recommendations-summary)

---

## Design Grade Assessment

### Overall Grade: A (Maintained)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | All pages properly separate zones. Consistent navbar implementation. |
| **PPT-Style Adherence** | A- | Business card page follows one-key-point-per-page. C37/C39/C43/C45 well integrated. Minor: page length growing with new sections. |
| **Card Component Consistency** | B+ | D-024 fixed `_info_card` background. But D-003 (inconsistent card styling) remains — `group_structure.py`, `watchlist_page.py`, `etf_detail.py` still use inline HTML. |
| **Color System** | A- | Design system at `docs/domain/design_system.md` is well-defined. D-004 (missing from `docs/design/`) still unresolved but the canonical doc exists. |
| **Plain-Language System** | A | Analogy engine + C37/C39 provide strong plain-language explanations. D-021 partially fixed (generic explanations added, metric values still missing). |
| **Visual Health Score** | A | C43 (Snowflake) implemented with 5-dimension radar chart, color-coded scores, reference lines. |
| **Synthesis/Summary Layer** | A | C37 (Key Takeaways) implemented with curated templates + auto-generated fallback. |
| **Valuation Context** | A | C45 (Valuation Band Chart) implemented with 5-year window. |
| **Mobile Responsiveness** | B- | D-006 unresolved. Basic media queries exist but multi-column layouts don't stack gracefully. |
| **Discovery Mechanism** | C+ | D-007 unresolved. No stock screener or guided discovery. Users must know which stock to search. |
| **Design System Documentation** | B | D-004 unresolved. Exists at `docs/domain/design_system.md` but NOT at `docs/design/design_system.md`. |
| **Page Load Performance** | B+ | D-008 (loading state inconsistency) unresolved but C41/C44 spinners added. |

### Grade Justification

The grade is maintained at **A** because:
- All P0 issues resolved (D-001, D-002)
- 12 issues resolved total (D-001, D-002, D-014, D-016-D-025)
- Core design principles (PPT style, ten-second test, Zone A/B/C) are well-implemented
- C37/C39/C43/C45 are well-designed and integrated
- The remaining P1/P2 issues are all "important but not blocking" — none violate core design principles

**Risk**: The grade could slip to A- in Round 14 if:
- D-003 (card inconsistency) is not addressed before more features are added
- D-005 (page overload) worsens as C44, C48, C56 are added to the business card page
- D-021 (missing metric values in explanations) remains unfixed

---

## Competitor Design Trends (Round 12 Research)

### Competitors Analyzed in Round 12

| # | Competitor | Type | Key Design Innovation |
|---|-----------|------|----------------------|
| 1 | **eToro** | Social trading | CopyTrader social learning, Virtual Portfolio practice |
| 2 | **Webull** | Commission-free broker | Webull Learn, paper trading, community + education combo |
| 3 | **Robinhood** | Consumer broker | Learn→Earn gamification, metric tooltips, Snacks daily briefing |
| 4 | **富邦e富** (Fubon eRich) | TW broker | AI Investment Compass, one-click report, social following |
| 5 | **元大證券** (Yuanta) | TW broker | AI chatbot, natural language screening, Investment Diary |
| 6 | **永豐金證券** (Bank SinoPac) | TW broker | Financial Statement Visualizer, Investment Checklist, Sector Rotation |
| 7 | **玉山證券** (E.SUN) | TW broker | Beginner Village (7-step onboarding), Investment Encyclopedia, Risk Meter |
| 8 | **Magnify.money** | AI visual education | AI Visual Explanations, Interactive Calculators, Compare Concepts |
| 9 | **Tastytrade** | Options education | Probability analysis, risk visualization, trade journal |

### 7 Key Design Trends from Round 12

#### Trend 1: Social Learning is the Dominant Engagement Model
- **Evidence**: eToro (CopyTrader), 富邦e富 (social following), Webull (community), Tastytrade (live streams)
- **Implication for Stock Explorer**: Full social features may be out of scope, but lightweight social elements (sharing via C53, following, community discussion) would improve engagement. C53-1 (Social Sharing URL) approved for Sprint 4.

#### Trend 2: AI is Becoming Table Stakes in TW Market
- **Evidence**: 富邦e富 (AI Investment Compass), 元大證券 (AI Chatbot + Natural Language Screening), 永豐金證券 (AI Alerts)
- **Implication for Stock Explorer**: The "historian" positioning deliberately avoids AI stock-picking, but AI-powered explanations (C56, C59) and AI Q&A could complement structured analysis. C56 (Explain This Metric) approved for Sprint 5.

#### Trend 3: Interactive Education is the New Standard
- **Evidence**: Magnify.money (AI Visual Explanations), 永豐金證券 (Financial Statement Visualizer), Robinhood (Metric Tooltips)
- **Implication for Stock Explorer**: Static text is no longer sufficient. Users expect to click, explore, and interact with educational content. C56 (Explain This Metric) directly addresses this. D-021 (missing metric values) undermines our interactive education — should be fixed.

#### Trend 4: Onboarding is Critical for Beginner Retention
- **Evidence**: 玉山證券 (Beginner Village 7-step onboarding), Robinhood (First Stock guided experience), eToro (Virtual Portfolio practice)
- **Implication for Stock Explorer**: No onboarding exists — users land on the homepage and must figure out what to do. This is the #1 UX gap for beginners. C58 (Beginner Onboarding Flow) approved for Sprint 5 as P1.

#### Trend 5: Gamification Drives Engagement
- **Evidence**: Robinhood (Learn→Earn with stock rewards), Khan Academy (badges), Finimize (certificates)
- **Implication for Stock Explorer**: No gamification exists. C60 (Concept Mastery Badges) approved for Sprint 5 as session-only MVP.

#### Trend 6: TW Broker Apps are Direct Competitors with Education Features
- **Evidence**: 富邦e富, 元大證券, 永豐金證券, 玉山證券 all have education features
- **Implication for Stock Explorer**: These target the same users. Our advantage is depth of analysis and "historian" positioning. But they have mobile apps, notifications, AI features. We must differentiate through educational depth.

#### Trend 7: Reflection Tools are a White Space
- **Evidence**: 元大證券 (Investment Diary), Tastytrade (Trade Journal)
- **Implication for Stock Explorer**: No TW competitor has a personal reflection journal for stock analysis. C55 (Investment Diary) approved for Sprint 6 — unique "historian of self" differentiator.

### Competitive Gap Analysis (Updated)

| Feature | Best-in-Class | Stock Explorer Status | Gap |
|---------|--------------|----------------------|-----|
| Visual Health Score | Simply Wall St (snowflake) | ✅ C43 implemented | 🟢 Closed |
| Synthesis/Summary | Public.com (story cards) | ✅ C37 implemented | 🟢 Closed |
| Valuation Context | 財報狗 (P/E band) | ✅ C45 implemented | 🟢 Closed |
| Risk Analysis | Simply Wall St (visual risk) | ⏳ C44 in progress | 🟡 In Progress |
| Discovery/Screening | 財報狗 (screener) | ❌ Not built (C42) | 🔴 Gap |
| Onboarding | 玉山證券 (Beginner Village) | ❌ Not built (C58) | 🔴 Gap |
| Interactive Education | Magnify.money (visual explainer) | ❌ Not built (C56) | 🔴 Gap |
| Glossary/Tooltips | Robinhood (metric tooltips) | ❌ Not built (C33) | 🔴 Gap |
| Social Learning | eToro (CopyTrader) | ⚠️ C53-1 (URL sharing) | 🟡 Partial |
| Gamification | Robinhood (Learn→Earn) | ❌ Not built (C60) | 🟡 Gap (P2) |
| Reflection Tools | 元大證券 (Investment Diary) | ❌ Not built (C55) | 🟡 Gap (P2) |
| AI Q&A | 元大證券 (chatbot) | ❌ Not built (C59) | 🟡 Gap (P2) |
| Mobile App | All competitors | ❌ Streamlit only | 🔴 Structural |
| Notifications | 財報狗, Yahoo | ❌ Not built (C02) | 🟡 Gap |

---

## Current Unresolved Problems Analysis

### P1 — Important Issues (6 items)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| **D-003** | Inconsistent Card Styling | ❌ Unresolved | 2-3h | `group_structure.py`, `watchlist_page.py`, `etf_detail.py` still use inline HTML. New card types (`_diary_card`, `_checklist_card`, `_badge_card`) planned but not yet created. Risk: more features = more inconsistency. |
| **D-004** | No Design System Documentation | ⚠️ Partial | 1h | Exists at `docs/domain/design_system.md` (235 lines, comprehensive). NOT at `docs/design/design_system.md`. Easy fix: copy or symlink. |
| **D-005** | Business Card Page Overload | ⚠️ Worsening | 4-6h | C44 (Risk), C48 (Story Card), C56 (Explain Metric) all planned for business card page. Current page already has 13+ sections. Without progressive disclosure, this will violate PPT style. |
| **D-006** | Mobile Responsiveness Gaps | ❌ Unresolved | 4-6h | Basic media queries exist. Multi-column layouts don't stack. Charts too small on mobile. |
| **D-007** | No Discovery Mechanism | ❌ Unresolved | 12-16h | Users must know which stock to search. No screening, no guided discovery. C42 planned but not started. |
| **D-021** | C43 Missing Metric Values in Explanations | ⚠️ Partially Fixed | 1-2h | Generic score-based explanations added. But underlying metric values (ROE %, gross margin %) still missing from hover template and dimension cards. |

### P2 — Optimization Issues (8 items)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| **D-008** | Loading State Inconsistency | ❌ Unresolved | 1-2h | Multiple sequential spinners. No skeleton loading. |
| **D-009** | Error State Inconsistency | ❌ Unresolved | 1h | Different empty-state messages across pages. |
| **D-010** | Watchlist Uses Non-PPT Layout | ❌ Unresolved | 2-3h | Only page with dense table layout. Feels like a different product. |
| **D-011** | Category Browser Uses Dense Tables | ❌ Unresolved | 2-3h | Data-dense rather than PPT-style. |
| **D-012** | No Glossary/Tooltip System | ❌ Unresolved | 8-12h | Financial terms have no inline help. C33 planned. |
| **D-013** | No Risk Analysis Section | ⏳ In Progress | 12-14h | C44 is next in Sprint 3. 3 risk dimensions planned. |
| **D-015** | No Structured Learning Path | ❌ Unresolved | 20-30h | C47 planned for long-term. C52 (Quiz Mode) in Sprint 5. |

### New Issues from Round 12 Research

| ID | Title | Priority | Effort | Source |
|----|-------|----------|--------|--------|
| **D-026** | No Beginner Onboarding | P1 | 14-20h | C58 approved Sprint 5. 玉山證券 Beginner Village model. |
| **D-027** | No Interactive Metric Explanations | P1 | 12-16h | C56 approved Sprint 5. Magnify.money/Robinhood model. |
| **D-028** | No Pre-Investment Checklist | P2 | 8-12h | C62 approved Sprint 5. 永豐金證券 model. |
| **D-029** | No Concept Comparison Tool | P2 | 10-14h | C57 approved Sprint 6. Magnify.money model. |
| **D-030** | No Investment Diary | P2 | 10-16h | C55 approved Sprint 6. 元大證券/Tastytrade model. |
| **D-031** | No Gamified Learning Badges | P2 | 8-12h | C60 approved Sprint 5. Robinhood/Khan Academy model. |

---

## New Design Improvement Proposals

### Proposal 1: D-032 — Progressive Disclosure Pattern for Business Card Page

**Priority**: P1
**Effort**: 3-4h
**Source**: D-005 (page overload) + competitor analysis (Robinhood minimalist, 富邦e富 card-based)

**Problem**: The business card page currently has 13+ sections. C44 (Risk), C48 (Story Card), and C56 (Explain Metric) will add 3+ more sections. This violates the "one key point per page" PPT-style principle and pushes content far below the fold.

**Competitor Pattern**: Robinhood uses a minimalist approach — only show what's needed, hide the rest behind "Learn more" expanders. 富邦e富 uses card-based layout with generous whitespace — each card is self-contained and doesn't overwhelm.

**Proposal**: Implement a **"Beginner Mode" / "Advanced Mode"** toggle on the business card page:
- **Beginner Mode** (default): Show only C37 (Key Takeaways) + C43 (Snowflake) + C39 (What Changed). Everything else is hidden behind expandable sections.
- **Advanced Mode**: Show all sections (current behavior).
- Store preference in session state.
- Add a "🎓 初學者模式" toggle at the top of Zone C.

**Design Rationale**: This directly addresses D-005 without removing any content. Beginners see a clean, focused page (PPT style). Advanced users see everything. This is the same pattern Robinhood uses (simple by default, detailed on demand).

**New card component needed**: `_expandable_card()` — a card with a click-to-expand section. The collapsed state shows the card title + one-line summary. The expanded state shows full content.

### Proposal 2: D-033 — Standardized Empty State Component

**Priority**: P2
**Effort**: 1h
**Source**: D-009 (error state inconsistency) + competitor analysis (all competitors have consistent empty states)

**Problem**: Empty data shows different messages on different pages (`st.info("暫無資料")`, `st.error()`, `st.warning()`). No standardized empty state design.

**Competitor Pattern**: Every competitor has a consistent empty state — same icon, same message style, same layout. Robinhood uses a friendly illustration + "No data available" message. 富邦e富 uses a clean card with an icon.

**Proposal**: Create a shared `_empty_state()` component in `_router_base.py`:
```python
def _empty_state(icon="📭", title="暫無資料", subtitle=""):
    st.markdown(f"""
    <div style="text-align:center;padding:2rem;color:#7F8C8D;">
        <div style="font-size:2rem;">{icon}</div>
        <div style="font-size:1rem;margin-top:0.5rem;">{title}</div>
        {"<div style='font-size:0.85rem;margin-top:0.3rem;'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)
```

Replace all inline empty-state messages with this component. Estimated 15-20 occurrences across all pages.

### Proposal 3: D-034 — Metric Value Tooltip Enhancement for C43 Snowflake

**Priority**: P1
**Effort**: 1-2h
**Source**: D-021 (partially fixed) + competitor analysis (Robinhood metric tooltips, Magnify.money visual explanations)

**Problem**: C43 dimension cards show generic score-based explanations ("獲利能力: 85分") but the underlying metric values (ROE %, gross margin %, etc.) are missing. This undermines the "ten-second test" — users see a score but don't know what it means in concrete terms.

**Competitor Pattern**: Robinhood has metric tooltips on every stock page — click on "ROE" and see "Return on Equity: 25% — this means the company earns 25 cents for every dollar of shareholder equity." Magnify.money generates visual explanations for every metric.

**Proposal**: Enhance the C43 hover template and dimension cards to include:
1. **Hover template**: Show metric name + value + plain-language explanation (e.g., "ROE: 25% — 每100元股東資金賺25元")
2. **Dimension cards**: Below the score, add a small line with the actual metric value (e.g., "ROE 25%｜毛利率 66%｜營收成長 15%")
3. **"❓" button**: Next to each dimension, add a small "❓" button that opens an expander with a visual explanation (connects to C56 when built)

This is a lightweight enhancement that leverages existing data. The metric values are already computed by the snowflake engine — they just need to be passed to the display layer.

---

## Updated Issue Checklist

### P0 — Blocking Issues
*(None)*

### P1 — Important Issues (7 items)

| ID | Title | Status | Effort | Proposed Sprint |
|----|-------|--------|--------|-----------------|
| D-003 | Inconsistent Card Styling | ❌ Unresolved | 2-3h | Sprint 4 (with D24 extraction) |
| D-004 | No Design System Documentation | ⚠️ Partial | 1h | Sprint 4 (quick win) |
| D-005 | Business Card Page Overload | ⚠️ Worsening | 3-4h | Sprint 5 (D-032 progressive disclosure) |
| D-006 | Mobile Responsiveness Gaps | ❌ Unresolved | 4-6h | Sprint 6+ |
| D-007 | No Discovery Mechanism | ❌ Unresolved | 12-16h | Sprint 5+ (C42) |
| D-021 | C43 Missing Metric Values | ⚠️ Partially Fixed | 1-2h | Sprint 4 (D-034) |
| D-032 | No Progressive Disclosure Pattern | 🆕 New | 3-4h | Sprint 5 |

### P2 — Optimization Issues (13 items)

| ID | Title | Status | Effort | Proposed Sprint |
|----|-------|--------|--------|-----------------|
| D-008 | Loading State Inconsistency | ❌ Unresolved | 1-2h | Sprint 4 |
| D-009 | Error State Inconsistency | ❌ Unresolved | 1h | Sprint 4 (D-033) |
| D-010 | Watchlist Uses Non-PPT Layout | ❌ Unresolved | 2-3h | Sprint 6 |
| D-011 | Category Browser Uses Dense Tables | ❌ Unresolved | 2-3h | Sprint 6 |
| D-012 | No Glossary/Tooltip System | ❌ Unresolved | 8-12h | Sprint 5+ (C33) |
| D-013 | No Risk Analysis Section | ⏳ In Progress | 12-14h | Sprint 3 (C44) |
| D-015 | No Structured Learning Path | ❌ Unresolved | 20-30h | Sprint 5+ (C47) |
| D-026 | No Beginner Onboarding | 🆕 New (C58) | 14-20h | Sprint 5 |
| D-027 | No Interactive Metric Explanations | 🆕 New (C56) | 12-16h | Sprint 5 |
| D-028 | No Pre-Investment Checklist | 🆕 New (C62) | 8-12h | Sprint 5 |
| D-029 | No Concept Comparison Tool | 🆕 New (C57) | 10-14h | Sprint 6 |
| D-030 | No Investment Diary | 🆕 New (C55) | 10-16h | Sprint 6 |
| D-031 | No Gamified Learning Badges | 🆕 New (C60) | 8-12h | Sprint 5 |
| D-033 | No Standardized Empty State | 🆕 New | 1h | Sprint 4 |
| D-034 | C3 Metric Value Tooltips | 🆕 New | 1-2h | Sprint 4 |

### Resolved Issues (12 items)

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| D-001 | No Visual Health Score | P0 | 2026-06-17 | C43 (Snowflake) implemented |
| D-002 | No Synthesis Layer | P0 | 2026-06-17 | C37 (Key Takeaways) implemented |
| D-014 | No Valuation Context | P2 | 2026-06-17 | C45 (Valuation Band) implemented |
| D-016 | C37 Missing Orange/Amber Hero Card | P1 | 2026-06-18 | `_summary_card()` created |
| D-017 | C37 Bullet Count Exceeds Spec | P2 | 2026-06-18 | Cap changed to 3 bullets |
| D-018 | C39 Placement Too Low | P1 | 2026-06-18 | Moved directly after C37 |
| D-019 | C39 Missing Delta Count Cap | P2 | 2026-06-18 | `return deltas[:2]` added |
| D-020 | C39 Missing Directional Color Coding | P2 | 2026-06-18 | Green/red color spans added |
| D-022 | C43 Placement Not Near Top | P2 | 2026-06-18 | Now 3rd content section |
| D-023 | C45 Uses 2-Year Window | P2 | 2026-06-18 | Extended to 5-year window |
| D-024 | _info_card Wrong Background | P1 | 2026-06-19 | Changed to #F8F9FA |
| D-025 | C39 Missing Empty State | P2 | 2026-06-19 | Added "近期無顯著變化" fallback |

---

## Recommendations Summary

### Immediate Actions (Sprint 4)

1. **D-004**: Copy `docs/domain/design_system.md` → `docs/design/design_system.md` (1h quick win)
2. **D-033**: Create `_empty_state()` component, replace all inline empty states (1h)
3. **D-034**: Enhance C43 hover template with metric values (1-2h)
4. **D-008**: Standardize loading states across pages (1-2h)

### Sprint 5 Actions

5. **D-032**: Implement progressive disclosure for business card page (3-4h) — **critical before C44/C48/C56 are added**
6. **D-003**: Standardize card components as part of D24 extraction (2-3h)
7. **D-021**: Complete the fix — add metric values to dimension cards (1-2h, overlaps with D-034)

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | D-003, D-004, D-005, D-021 all resolved in Sprint 4-5 |
| **Expected case** | A | D-004, D-021, D-032 resolved; D-003 addressed with D24 |
| **Worst case** | A- | D-005 worsens as C44/C48/C56 are added without progressive disclosure |

### Key Competitor Design Trends to Watch

1. **Interactive education** (Magnify.money, Robinhood) — C56 is the right response
2. **Onboarding** (玉山證券, Robinhood) — C58 is critical for beginner retention
3. **AI Q&A** (元大證券, Finimize) — C59 is a long-term differentiator
4. **Social learning** (eToro, 富邦e富) — C53 is a lightweight start
5. **Reflection tools** (元大證券, Tastytrade) — C55 is a unique white-space opportunity

---

---

## 2026-06-19 Design Review — Review Round 14

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: Round 14 review — verifying C41 (Read Next), C44 (Risk Analysis MVP), D-024 (info_card color fix), D-025 (C39 empty state). Assessing design compliance of new features and fixes.
> **Current Design Grade**: A (maintained from Round 13)

---

## Table of Contents

1. [Design Grade Assessment](#design-grade-assessment-round-14)
2. [C41 Read Next — Design Compliance Review](#c41-read-next--design-compliance-review)
3. [C44 Risk Analysis — Design Compliance Review](#c44-risk-analysis--design-compliance-review)
4. [D-024 / D-025 — Fix Verification](#d-024--d-025--fix-verification)
5. [Competitor Design Trends (Round 14 Update)](#competitor-design-trends-round-14-update)
6. [New Design Issues Identified](#new-design-issues-identified)
7. [P1 Priority Assessment](#p1-priority-assessment)
8. [Updated Issue Checklist](#updated-issue-checklist-round-14)
9. [Recommendations Summary](#recommendations-summary-round-14)

---

## Design Grade Assessment (Round 14)

### Overall Grade: A (Maintained)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | No changes to layout structure. C41 and C44 both render within Zone C. |
| **PPT-Style Adherence** | A- | C44 uses `st.expander` (expanded=False) — good progressive disclosure. C41 adds a new section at page bottom — acceptable placement but adds to page length. Page now has ~15 sections. |
| **Card Component Consistency** | B+ | **Regression found**: C41 peer cards use inline HTML (no border-left, no border-radius, no background). C44 risk dimension cards use inline HTML with `#FFF8F0` background (should be `#F8F9FA` per design system). D-003 still unresolved. |
| **Color System** | A- | D-024 fix verified — `_info_card` now uses `#F8F9FA`. C44 risk cards use `#FFF8F0` (tip/warning background) which is acceptable for risk context but inconsistent with design system card spec. |
| **Plain-Language System** | A | C44 risk descriptions are well-written in historian tone. C41 uses plain-language CTA ("一起認識這家公司"). |
| **Visual Health Score** | A | No changes to C43. |
| **Synthesis/Summary Layer** | A | No changes to C37. |
| **Valuation Context** | A | No changes to C45. |
| **Mobile Responsiveness** | B- | D-006 unresolved. C41 peer cards will stack poorly on mobile (no padding/background). |
| **Discovery Mechanism** | C+ | D-007 unresolved. C41 partially addresses this by providing peer navigation within the same industry. |
| **Design System Documentation** | B | D-004 unresolved. |
| **Page Load Performance** | B+ | C41 calls `client.get_stock_info()` synchronously within the render path — potential performance concern. |

### Grade Justification

The grade is maintained at **A** because:
- D-024 and D-025 fixes are verified correct
- C44 Risk Analysis is well-architected (clean service layer, progressive disclosure via `st.expander`)
- C41 Read Next provides genuine UX value (discovery mechanism within the page)
- No P0 issues introduced
- Remaining issues are all P1/P2 — important but not blocking

**Risk**: The grade could slip to A- in Round 15 if:
- C41 inline HTML cards are not standardized (D-003 regression)
- C44 risk card background color inconsistency is not addressed
- Page length continues to grow without D-032 progressive disclosure

---

## C41 Read Next — Design Compliance Review

### What Was Implemented
- **Section**: `### 📖 推薦閱讀` at the bottom of the business card page (lines 501-557)
- **Peer stocks**: Queries `client.get_stock_info()` for same-industry stocks, displays up to 5 peers
- **Fun facts**: Shows up to 2 remaining company facts (rotating, skipping the one already shown)
- **Navigation**: Each peer has a "查看 XX 名片" button using `navigate_to()`

### Design Compliance Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Placement** | ✅ Pass | At the bottom of the page, after all primary content. Logical flow: learn about this company → discover peers. |
| **Section title** | ✅ Pass | Uses `### 📖 推薦閱讀` with emoji, consistent with other section titles. |
| **Empty state** | ✅ Pass | Uses `_info_card("推薦閱讀", "目前沒有找到相關的同產業個股推薦", "📖")` — reuses shared component. |
| **Button keys** | ✅ Pass | Uses `f"read_next_{stock_id}_peer_{_peer_id}"` — unique, follows naming convention. |
| **Card styling** | ❌ **FAIL** | Peer cards use **inline HTML** without card styling: no `border-radius`, no `border-left`, no background color, no padding. This violates the design system card spec (Section 3.3) and D-003. |
| **Typography** | ⚠️ Partial | Uses `font-size:1rem` for name (should be `1.6rem` for values per design system). Missing label/value hierarchy. |
| **Plain-language** | ✅ Pass | "🔗 同產業同業，一起認識這家公司" is friendly and clear. |
| **Ten-second test** | ✅ Pass | Section purpose is immediately clear. |
| **Performance** | ⚠️ Concern | Calls `client.get_stock_info()` synchronously on every render. This is an API call in the view layer. |

### Verdict
**Functional but visually inconsistent.** The peer cards look like raw text links rather than cards. They don't match the `_info_card` or `_白话_card` styling used everywhere else on the page. This is a **D-003 regression** — new inline HTML where shared components should be used.

**Recommended Fix**: Create a `_peer_card()` component or reuse `_info_card()` with a "查看名片" button inside. Minimum: add `background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB` to the peer card HTML.

---

## C44 Risk Analysis — Design Compliance Review

### What Was Implemented
- **Service**: `src/services/risk_analyzer.py` (567 lines, pure functions, no Streamlit/API imports)
- **Dimensions**: Customer concentration, financial health, event-based risk
- **Integration**: `st.expander("⚠️ 風險分析 — 什麼可能出問題？", expanded=False)` at line 263
- **Rendering**: `_render_risk_dimension()` helper with color-coded risk badges

### Design Compliance Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Progressive disclosure** | ✅ **Excellent** | Uses `st.expander` with `expanded=False`. This is exactly what D-032 calls for. Risk section is hidden by default, reducing page overload. |
| **Service layer separation** | ✅ **Excellent** | `risk_analyzer.py` has zero Streamlit imports, zero API calls. Clean architecture. |
| **Historian tone** | ✅ **Excellent** | All descriptions use past-tense, factual language. No buy/sell recommendations. |
| **Risk badges** | ✅ Pass | `🔴 高風險`, `🟡 中風險`, `🟢 低風險` — clear, color-coded, with emoji. |
| **Color coding** | ✅ Pass | Uses `#E74C3C` (red), `#F39C12` (amber), `#27AE60` (green) — matches design system. |
| **Card background** | ⚠️ **Inconsistent** | Risk dimension cards use `background:#FFF8F0` (tip/warning background per design system). The design system spec at `risk_analysis_design.md` also specifies `#FFF8F0`. However, the standard `_info_card` uses `#F8F9FA`. The `#FFF8F0` choice is defensible for risk (warning context) but creates visual inconsistency. |
| **Card structure** | ⚠️ Partial | Uses inline HTML instead of `_info_card()` or `_summary_card()`. Missing `border-left:4px solid {color}` is present but the card structure diverges from the standard pattern (no consistent padding/radius with other cards). |
| **Missing data handling** | ✅ Pass | Gracefully skips `None` dimensions. No placeholder shown when no risk data exists. |
| **Summary text** | ✅ Pass | Contextual summary: "分析顯示 客戶集中、財務健康 面向存在較高風險" for high-risk, "以下為各風險維度分析" for low-risk. |
| **Plain-language** | ✅ **Excellent** | Descriptions like "最近一期負債比為 65%，高於一般認為的警戒線 65%" are concrete and beginner-friendly. |
| **Ten-second test** | ✅ Pass | Expander title "⚠️ 風險分析 — 什麼可能出問題？" is immediately clear. |

### Verdict
**Well-designed and architecturally sound.** The progressive disclosure via `st.expander` is the standout feature — it directly addresses D-005 (page overload) and partially fulfills D-032 (progressive disclosure pattern). The service layer is clean. The historian tone is consistent.

**Issues found**:
1. **Card background inconsistency** (P2): `#FFF8F0` vs `#F8F9FA` — minor but adds to D-003
2. **Inline HTML** (P2): Risk dimension cards bypass shared components — D-003 regression

---

## D-024 / D-025 — Fix Verification

### D-024: `_info_card` Background Color

| Check | Status | Evidence |
|-------|--------|----------|
| Background changed from `#FFF8F0` to `#F8F9FA` | ✅ **Verified** | `_router_base.py` line 110: `background:#F8F9FA` |
| Matches design system spec | ✅ **Verified** | Design system Section 3.3: card background = `#F8F9FA` |
| `_summary_card` unchanged | ✅ **Verified** | `_router_base.py` line 100: `background:#FFF8F0` (correct — tip card) |
| `_白话_card` background | ⚠️ **Note** | Uses `#F5F5F5` instead of `#F8F9FA` — pre-existing inconsistency, not part of D-024 |

**Verdict**: D-024 fix is **correct and complete**.

### D-025: C39 Empty State

| Check | Status | Evidence |
|-------|--------|----------|
| Empty state added | ✅ **Verified** | `business_card.py` line 217: `_info_card("最近有什麼變化", "近期無顯著變化，所有指標波動均在 10% 以內", "🔄")` |
| Uses shared component | ✅ **Verified** | Uses `_info_card()` — consistent with design system |
| Message is plain-language | ✅ **Verified** | "近期無顯著變化，所有指標波動均在 10% 以內" — clear, factual, beginner-friendly |
| Trigger condition | ✅ **Verified** | `else` branch when `deltas` is empty (no metrics exceed threshold) |

**Verdict**: D-025 fix is **correct and complete**.

---

## Competitor Design Trends (Round 14 Update)

### Risk Analysis Patterns from Competitors

| Competitor | Risk UI Pattern | Stock Explorer C44 Comparison |
|-----------|----------------|-------------------------------|
| **Simply Wall St** | Visual risk meter (0-100), color-coded zones, expandable detail | C44 uses 3-level badge system (🔴🟡🟢) — simpler but equally clear |
| **Morningstar** | Uncertainty rating (low/medium/high/very high) with narrative | C44 mirrors this with 3-level + plain-language narrative |
| **玉山證券** | Risk Meter in beginner onboarding | C44 is more detailed (3 dimensions vs single meter) — better for education |
| **Tastytrade** | Probability analysis with visual risk/reward | C44 deliberately avoids probability (historian positioning) — correct choice |
| **永豐金證券** | Investment Checklist with risk items | C44's expander pattern is similar — collapsible, scannable |

### Recommendation/Discovery Patterns from Competitors

| Competitor | Discovery Pattern | Stock Explorer C41 Comparison |
|-----------|------------------|------------------------------|
| **財報狗** | Stock screener with card-based results | C41 is simpler (peer list only) — appropriate for MVP |
| **eToro** | "Popular Investors" + copy-trader suggestions | C41's "同產業個股推薦" is analogous but without social proof |
| **Robinhood** | "People Also Watch" section on stock pages | C41 directly mirrors this pattern — good competitive alignment |
| **Webull** | "Trending Lists" + sector-based discovery | C41's industry-based filtering matches this approach |
| **富邦e富** | AI Investment Compass with recommendations | C41 is manual (industry match) vs AI — simpler but more transparent |

### Key Insight
C41's "同產業個股推薦" is directly comparable to Robinhood's "People Also Watch" — a proven pattern. The main gap is **visual polish** (card styling) and **breadth** (competitors also show "trending" and "most watched" beyond just industry peers).

---

## New Design Issues Identified

### D-035: C41 Peer Cards Use Inline HTML (D-003 Regression)

- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14
- **Description**: C41 Read Next peer stock cards use raw inline HTML (`<div>` with text styling) instead of the shared `_info_card()` / `_白话_card()` components. The peer cards lack `border-radius`, `border-left`, background color, and consistent padding. This is a regression of D-003 (inconsistent card styling).
- **Affected Lines**: `business_card.py` lines 522-532
- **Proposed Fix**: Either (a) create a `_peer_card()` component in `_router_base.py` with standard card styling + button, or (b) use `_info_card()` with the peer name/industry as content and the button below.
- **Effort**: 0.5-1h

### D-036: C44 Risk Dimension Cards Use Non-Standard Background

- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14
- **Description**: C44 risk dimension cards use `background:#FFF8F0` (tip/warning background) instead of the standard card background `#F8F9FA`. While defensible for risk context (warning = orange tint), this creates visual inconsistency. The design system specifies `#F8F9FA` for info cards and `#FFF8F0` for tip cards — risk dimensions are informational, not tips.
- **Affected Lines**: `business_card.py` line 72
- **Proposed Fix**: Change to `background:#F8F9FA` and rely on the `border-left:4px solid {color}` for risk level indication. The color-coded border already communicates risk level effectively.
- **Effort**: <0.5h (one-line change)

### D-037: `_白话_card` Uses Non-Standard Background Color

- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14 (discovered during D-024 verification)
- **Description**: `_白话_card()` in `_router_base.py` uses `background:#F5F5F5` while the design system specifies card background as `#F8F9FA`. This affects all 白話 cards across the entire app (key metrics, dividend cards, etc.). Pre-existing issue, not a regression.
- **Affected Files**: `_router_base.py` line 91
- **Proposed Fix**: Change `background:#F5F5F5` to `background:#F8F9FA` to match design system.
- **Effort**: <0.5h (one-line change)

### D-038: C41 Calls API in View Layer

- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14
- **Description**: C41's `_render_business_card` calls `client.get_stock_info()` directly in the view layer (line 505). This violates the architecture principle that the view layer should not make API calls — data should be fetched in the router and passed via `data` dict. This also means the API call happens on every render, not just on page load.
- **Affected Lines**: `business_card.py` lines 505-512
- **Proposed Fix**: Move the peer stock fetching to `get_stock_data()` in `_router_base.py` (add a `"peers"` key to the data dict), or accept peers as a parameter.
- **Effort**: 1-2h

---

## P1 Priority Assessment

### Current P1 Issues (7 items) — Priority Review

| ID | Title | Current Priority | Recommended Change | Rationale |
|----|-------|-----------------|-------------------|-----------|
| D-003 | Inconsistent Card Styling | P1 | **Keep P1** | Worsened by C41 (new inline HTML). Affects every page. |
| D-004 | No Design System Documentation | P1 | **Keep P1** | Quick win (1h). Still blocks new feature consistency. |
| D-005 | Business Card Page Overload | P1 | **Keep P1** | C44 partially mitigates (expander). C41 adds to page length. Net effect: neutral. |
| D-006 | Mobile Responsiveness Gaps | P1 | **Keep P1** | Unchanged. |
| D-007 | No Discovery Mechanism | P1 | **Downgrade to P2** | C41 provides in-page peer discovery. Not a full screener but addresses the core use case (discovering related stocks). |
| D-021 | C43 Missing Metric Values | P1 | **Keep P1** | Still unfixed. D-034 (metric tooltips) is the proposed fix. |
| D-032 | No Progressive Disclosure | P1 | **Downgrade to P2** | C44 implements progressive disclosure via `st.expander`. The pattern is proven. Remaining work is applying it to other sections. |
| D-034 | C3 Metric Value Tooltips | P1 | **Keep P1** | Unfixed. Directly impacts ten-second test for C43. |

### Recommended Priority Changes
- **D-007 → P2**: C41's peer recommendations partially address discovery. Full screener (C42) is still needed but the P1 urgency is reduced.
- **D-032 → P2**: C44 proves the `st.expander` pattern works. The remaining work is applying it to other sections — important but no longer urgent.

---

## Updated Issue Checklist (Round 14)

### P0 — Blocking Issues
*(None)*

### P1 — Important Issues (6 items, reduced from 8)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| D-003 | Inconsistent Card Styling | ❌ Unresolved | 2-3h | Worsened by C41 inline HTML. Now affects C41, C44, plus previously flagged files. |
| D-004 | No Design System Documentation | ⚠️ Partial | 1h | Quick win. Copy `docs/domain/design_system.md` → `docs/design/design_system.md`. |
| D-005 | Business Card Page Overload | ⚠️ Stable | 3-4h | C44 expander helps. C41 adds length. Net neutral. D-032 (now P2) will address remaining. |
| D-006 | Mobile Responsiveness Gaps | ❌ Unresolved | 4-6h | Unchanged. |
| D-021 | C43 Missing Metric Values | ⚠️ Partially Fixed | 1-2h | D-034 is the proposed fix. |
| D-034 | C3 Metric Value Tooltips | ❌ Unresolved | 1-2h | Enhance hover template + dimension cards with actual metric values. |

### P2 — Optimization Issues (13 items, increased from 10)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| D-007 | No Discovery Mechanism | ⏳ Partial | 12-16h | Downgraded to P2 — C41 provides partial peer discovery. |
| D-008 | Loading State Inconsistency | ❌ Unresolved | 1-2h | Unchanged. |
| D-009 | Error State Inconsistency | ❌ Unresolved | 1h | Unchanged. |
| D-010 | Watchlist Uses Non-PPT Layout | ❌ Unresolved | 2-3h | Unchanged. |
| D-011 | Category Browser Uses Dense Tables | ❌ Unresolved | 2-3h | Unchanged. |
| D-012 | No Glossary/Tooltip System | ❌ Unresolved | 8-12h | Unchanged. |
| D-013 | No Risk Analysis Section | ✅ **Resolved** | — | C44 implemented. Mark resolved. |
| D-015 | No Structured Learning Path | ❌ Unresolved | 20-30h | Unchanged. |
| D-032 | No Progressive Disclosure | ⏳ Partial | 3-4h | Downgraded to P2 — C44 proves the pattern. Apply to remaining sections. |
| D-033 | No Standardized Empty State | ❌ Unresolved | 1h | Unchanged. |
| D-035 | C41 Peer Cards Use Inline HTML | 🆕 New | 0.5-1h | D-003 regression. |
| D-036 | C44 Risk Cards Non-Standard BG | 🆕 New | <0.5h | `#FFF8F0` → `#F8F9FA`. |
| D-037 | `_白话_card` Wrong Background | 🆕 New | <0.5h | `#F5F5F5` → `#F8F9FA`. |
| D-038 | C41 API Call in View Layer | 🆕 New | 1-2h | Move `get_stock_info()` to router layer. |

### Resolved Issues (13 items, increased from 12)

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| D-001 | No Visual Health Score | P0 | 2026-06-17 | C43 (Snowflake) implemented |
| D-002 | No Synthesis Layer | P0 | 2026-06-17 | C37 (Key Takeaways) implemented |
| D-013 | No Risk Analysis Section | P2 | 2026-06-19 | C44 (Risk Analysis MVP) implemented with 3 dimensions + expander |
| D-014 | No Valuation Context | P2 | 2026-06-17 | C45 (Valuation Band) implemented |
| D-016 | C37 Missing Orange/Amber Hero Card | P1 | 2026-06-18 | `_summary_card()` created |
| D-017 | C37 Bullet Count Exceeds Spec | P2 | 2026-06-18 | Cap changed to 3 bullets |
| D-018 | C39 Placement Too Low | P1 | 2026-06-18 | Moved directly after C37 |
| D-019 | C39 Missing Delta Count Cap | P2 | 2026-06-18 | `return deltas[:2]` added |
| D-020 | C39 Missing Directional Color Coding | P2 | 2026-06-18 | Green/red color spans added |
| D-022 | C43 Placement Not Near Top | P2 | 2026-06-18 | Now 3rd content section |
| D-023 | C45 Uses 2-Year Window | P2 | 2026-06-18 | Extended to 5-year window |
| D-024 | _info_card Wrong Background | P1 | 2026-06-19 | Changed to `#F8F9FA` |
| D-025 | C39 Missing Empty State | P2 | 2026-06-19 | Added "近期無顯著變化" fallback |

---

## Recommendations Summary (Round 14)

### Immediate Actions (Sprint 4 — with C38, D16 remaining)

1. **D-036**: Change C44 risk card background from `#FFF8F0` to `#F8F9FA` (<0.5h — one line)
2. **D-037**: Change `_白话_card` background from `#F5F5F5` to `#F8F9FA` (<0.5h — one line)
3. **D-035**: Standardize C41 peer cards with shared card component (0.5-1h)
4. **D-038**: Move `client.get_stock_info()` call from view to router layer (1-2h)
5. **D-004**: Copy design system doc to expected path (1h quick win)

### Sprint 5 Actions

6. **D-003**: Comprehensive card standardization across all pages (2-3h) — should include D-035, D-036, D-037 fixes if not done in Sprint 4
7. **D-032**: Apply progressive disclosure to remaining business card sections (3-4h)
8. **D-021/D-034**: Add metric values to C43 hover template and dimension cards (1-2h)

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | D-003, D-004, D-021 all resolved; card consistency achieved |
| **Expected case** | A | D-035/036/037/038 fixed in Sprint 4; D-003 addressed in Sprint 5 |
| **Worst case** | A- | D-003 not addressed; more inline HTML added with new features |

### Key Competitor Design Trends to Watch

1. **Risk visualization** (Simply Wall St, Morningstar) — C44 is competitive; consider adding a visual risk meter in future iterations
2. **Peer discovery** (Robinhood "People Also Watch") — C41 matches this pattern; consider adding "trending" and "most watched" in future
3. **Interactive education** (Magnify.money, Robinhood) — C56 is the right response
4. **Onboarding** (玉山證券, Robinhood) — C58 is critical for beginner retention
5. **Progressive disclosure** (all competitors) — C44 sets the pattern; apply universally

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 4 feature implementation.*

---

## Sprint 21 Design Direction

> **Author**: Design Reviewer
> **Date**: 2026-06-14
> **Context**: Sprint 21 Planning — design-level evaluation of 6 candidate features (C152, C170, C171, C172, C173, C174) before sprint commitment.
> **Current Design Grade**: A (6th consecutive A since R34)
> **Candidates**: C152 (Multi-Factor Event Narratives, P1, 16-20h), C170 (Tappable Glossary, P1, 6-10h), C171 (Valuation Band Chart, P2, 8-10h), C172 (Concept Comparison Tool, P2, 10-14h), C173 (Visual Financial Calculators, P2, 12-16h), C174 (Sector-Level Storytelling, P2, 14-20h)

---

## Table of Contents

1. [UX Impact Assessment](#ux-impact-assessment)
2. [Priority Ranking](#priority-ranking)
3. [Design Direction: Top 3 Candidates](#design-direction-top-3-candidates)
4. [Component Reuse Recommendations](#component-reuse-recommendations)
5. [New Component Proposals](#new-component-proposals)
6. [Design Risks](#design-risks)
7. [Recommendations Summary](#recommendations-summary)

---

## UX Impact Assessment

### By Candidate

| Candidate | UX Impact | Effort | Impact/Effort | Aligns With | Risk |
|-----------|-----------|--------|---------------|-------------|------|
| **C152** Multi-Factor Event Narratives | 🔴 **Highest** — Transforms event dashboard from disconnected list into coherent story. Directly addresses "ten-second test" for events. No TW competitor has this. | 16-20h | High | Story first + Historian | Medium — narrative quality depends on template coverage; beginners may still feel overwhelmed if too many factors shown |
| **C170** Tappable Glossary | 🔴 **Highest** — Closes D-012 (No Glossary/Tooltip System), the oldest P2 gap. Directly enables "beginner-friendly" design principle. Every metric becomes educational. Reuses existing C139 popover pattern. | 6-10h | **Very High** | Ten-second test + Beginner-friendly | Low — pattern already proven by `_explain_button` and `_glossary_tooltip` in `_router_base.py` |
| **C171** Valuation Band Chart | 🟡 **High** — 財報狗's P/E band is one of its most popular features. Beginners currently see P/E as a single number without context ("Is 18x expensive?"). Adds historical context visually. | 8-10h | High | Benchmark-oriented + Story first | Low — well-defined chart type; parallels C45 (Valuation Band) but adds plain-language interpretation layer |
| **C172** Concept Comparison Tool | 🟡 **Medium-High** — Magnify.money's "Compare Concepts" is educationally powerful. Helps beginners distinguish similar metrics (ROE vs ROA, P/E vs P/B). Currently no concept-level education exists. | 10-14h | Medium | Point-to-point knowledge | Medium — needs curated content per concept pair; risks becoming a data dump without careful information architecture |
| **C173** Visual Financial Calculators | 🟡 **Medium** — Interactive calculators (compound interest, dividend reinvestment) make abstract concepts tangible. High engagement potential. Magnify.money proves demand. | 1-16h | Medium | Point-to-point + Ten-second test | Medium — interactive widgets risk violating "Zone C: no interactive controls" if placed incorrectly; also increases page complexity |
| **C174** Sector-Level Storytelling | 🟠 **Medium (Strategic)** — Smallcase's "thematic stories" validate sector-level narrative. Connects company-level stories into industry-wide arcs. Unique differentiator. But requires significant content curation. | 14-20h | Medium-Long term | Story first + Historian | High — most complex candidate; needs multi-company data synthesis; risks information overload for beginners |

### Key Insight from Round 8 & 9 Competitor Research

Simply Wall St's snowflake gives a **30-second company overview** — our C152 serves the same role for events: a 30-second event overview. Stockopedia's StockRank combines multiple factors into one score — C152 combines multiple events into one narrative. The pattern is clear: **synthesis is the dominant UX trend.** Beginners don't want data points; they want the story that connects them.

---

## Priority Ranking

### Tier 1: Must-High-Impact (Recommend for Sprint 21)

| Rank | Candidate | Reasoning |
|------|-----------|-----------|
| **1** | **C170** Tappable Glossary | Lowest effort (6-10h), highest impact/effort ratio, reuses proven popover patterns, closes the oldest P2 gap (D-012). Unblocks beginner-friendly design principle for ALL future features. **This is the highest-leverage feature in the sprint.** |
| **2** | **C152** Multi-Factor Event Narratives | Highest absolute UX impact. Transforms event dashboard from raw data to coherent story. P1 priority. No TW competitor has this. Natural extension of existing `_so_what_box` and C98 event interpretation engine. |

### Tier 2: High Value (Recommend if capacity allows)

| Rank | Candidate | Reasoning |
|------|-----------|-----------|
| **3** | **C171** Valuation Band Chart | 財報狗 proves demand. Relatively low effort (8-10h). Closes a long-standing gap (valuation context). Pure chart + text — no new interaction patterns needed. |
| **4** | **C172** Concept Comparison Tool | Educationally powerful but needs curated content per concept pair. Could be phased: Phase A = top 5 concept pairs, Phase B = expand. |

### Tier 3: Future Sprints

| Candidate | Reasoning |
|-----------|-----------|
| **C173** Visual Financial Calculators | Valuable but risks Zone C violation (interactive controls in content area). Needs careful placement design. Consider for Sprint 22 after glossary (C170) establishes the interactive education pattern. |
| **C174** Sector-Level Storytelling | Strategic long-term differentiator but highest risk. Requires multi-company narrative synthesis. Recommend spike/proof-of-concept before committing to full implementation. |

### Recommended Sprint 21 Commitment

**C170 + C152 + C171** — total effort: 30-38h. This is aggressive but justified:
- C170 (6-10h) sets the educational infrastructure for all other features
- C152 (16-20h) is the highest-impact narrative feature
- C171 (8-10h) is a low-risk, high-value chart feature

If capacity is tight: **C170 + C152** only (22-30h).

---

## Design Direction: Top 3 Candidates

### C170: Tappable Glossary

**Problem it solves**: D-012 (No Glossary/Tooltip System) — Beginners encounter terms like "ROE," "P/B ratio," "institutional investors" with no inline help. Investopedia has 10,000+ terms; Stock Explorer has zero.

**Can C170 reuse C139's popover pattern? YES.** The `_glossary_tooltip()` component in `_router_base.py` (lines 269-290) already implements exactly the st.popover pattern needed. It:
1. Takes a `term_key` and `glossary_service` as parameters
2. Looks up the term via `glossary_service.get_glossary_term(term_key)`
3. Renders a clickable `ℹ️ {name}` label that opens `st.popover`
4. Shows plain-language definition + example + analogy inside the popover

**Recommendation**: C170 should be a **systematic application** of the existing `_glossary_tooltip()` pattern across all financial metrics, not a new component. The design work is:
1. Create `src/data/glossary.yaml` with 30-50 core financial terms (ROE, P/B, PER, gross margin, net margin, revenue YoY, dividend yield, payout ratio, debt ratio, current ratio, EPS, free cash flow, institutional ownership, etc.)
2. Each term has: `name` (繁體中文), `plain` (plain-language definition, ≤2 sentences), `example` (real TW stock example), `analogy` (everyday analogy)
3. Wire `_glossary_tooltip()` into every metric display across all pages

**Where to place glossary tooltips**:
- Next to section titles containing financial terms (e.g., `_section_title("ROE 股東報酬率")` → add `_glossary_tooltip("ROE", glossary_service)` inline)
- Inside metric card labels (e.g., `_白话_card("ROE", "25%", "每100元股東資金賺25元")` → make "ROE" a glossary-linked label)
- Next to chart axis labels and legend items where space permits

**Beginner experience flow**:
1. User sees "ROE 25%" on the business card page
2. Notices the ℹ️ icon next to "ROE"
3. Clicks → popover shows: "ROE（股東報酬率）— 公司用股東的錢賺錢的能力。ROE 25% 代表每100元股東資金，公司一年賺25元。巴菲特最重視這個指標。"
4. User understands the concept in <10 seconds

**Design risk**: Too many ℹ️ icons create visual noise. **Mitigation**: Only show glossary links for terms that a genuine beginner wouldn't know. Skip obvious ones like "營收" (revenue). Prioritize ratios and technical terms.

---

### C152: Multi-Factor Event Narratives

**Problem it solves**: M5 events currently display as disconnected cards. When TSMC has 4 events in a week (revenue miss + insider selling + institutional outflow + sector downturn), users see 4 separate cards. Humans want the STORY, not the raw ingredients. Public.com and Spiking both combine multiple factors into one narrative.

**How to display multi-factor narratives without overwhelming beginners:**

Use a **progressive disclosure card with two layers**:

**Layer 1 — "事件總覽" Summary Card** (always visible):
- A single `_summary_card()` with a synthesized one-paragraph narrative
- This is the "30-second version" — a beginner can read this alone and understand what happened
- Example: "台積電本週面臨多重壓力：營收不如預期(-3%)、外資連續賣超、半導體板塊因蘋果訂單下修而走弱。綜合來看，短期展望趨向保守."
- Uses `_summary_card(icon="📰", title="本週事件總覽", content=synthesized_narrative)`

**Layer 2 — Individual Event Details** (collapsible):
- Below the summary card, show individual event cards in a `st.expander("查看個別事件 (4)")`
- Each event card uses existing `_info_card()` with the event's plain-language explanation
- This satisfies advanced users who want the details

**Visual hierarchy**:
```
┌─────────────────────────────────────────────────────┐
│  📰 本週事件總覽                                      │
│  台積電本週面臨多重壓力：營收不如預期(-3%)、外資連續     │
│  賣超、半導體板塊因蘋果訂單下修而走弱...                │
│                                           [展開 ▼]   │
├─────────────────────────────────────────────────────┤
│  ▼ 查看個別事件 (4)                                   │
│  ┌─────────────────────────────────────────────┐     │
│  │ 📉 營收不如預期                               │     │
│  │ 6月營收較上月衰退3%，低於分析師預期...         │     │
│  └─────────────────────────────────────────────┘     │
│  ┌─────────────────────────────────────────────┐     │
│  │ 🏦 外資連續賣超                               │     │
│  │ 外資本週淨賣超15,000張，為近月最大...          │     │
│  └─────────────────────────────────────────────┘     │
│  ...                                                │
└─────────────────────────────────────────────────────┘
```

**Synthesized narrative construction** (design rules):
1. **Lead with the highest-impact factor** (revenue > earnings > insider > institutional > sector)
2. **Use connecting language** ("同時," "此外," "綜合來看") — mirrors how humans tell stories
3. **End with a historian-framed conclusion** — not a prediction, but a summary of what the combined factors suggest ("市場對短期展望趨向保守" NOT "建議賣出")
4. **Maximum 3-4 sentences** in the summary paragraph — respects the 200-char guideline (with some flexibility for Chinese)
5. **Include data points** — don't just say "營收不如預期," say "營收不如預期(-3%)" so the narrative is grounded

**Interaction design**:
- Default: Show summary card only (collapsed)
- User clicks expander → see individual events
- If only 1 event in the window → skip the summary, show the single event card directly (no synthesis needed for a single factor)
- If 2+ events → show summary + collapsible details

**Component reuse**:
- `_summary_card()` for the synthesized narrative (change border color to `#3498DB` to distinguish from "hero card" usage)
- `_info_card()` for individual event details inside the expander
- `_so_what_box()` is NOT appropriate here (it's for metric deltas, not event narratives)
- **New component needed**: `_event_narrative_card()` — a specialized card that renders the summary + expander pattern

**Design risk**: If synthesis quality is poor (template-generated, feels robotic), beginners will just expand to read individual events and the summary card becomes wasted space. **Mitigation**: Invest in high-quality templates for the top 10 event type combinations. Use C98 event interpretation engine for individual event text quality.

---

### C171: Valuation Band Chart

**Problem it solves**: Beginners see "P/E = 18x" and don't know if that's expensive. 財報狗's P/E band chart is one of its most popular features — it shows current P/E vs historical range. Morningstar's "Fair Value with Uncertainty" teaches beginners that valuation is a range, not a single number.

**Design pattern**: Horizontal band chart with three visual elements:

```
  P/E 區間圖
  ─────────────────────────────────────
  5年前        現在        5年後
  10x    ═══════●════════════    30x
         ↑                    ↑
     歷史最低12x           歷史最高25x
  ─────────────────────────────────────
  目前本益比 18x，處於歷史的 45% 分位
  "不算貴也不算便宜，跟歷史平均差不多"
```

**Layout**: One `_白话_card()` for the current P/E value + analogy, then a Plotly horizontal bar chart below showing the band. Total height: ~200px. This keeps it as a single "card-width" element that doesn't dominate the page.

**Color coding**:
- Blue dot/line for current value
- Light blue band for historical range (10th-90th percentile)
- Gray band for extreme range (min-max)
- Green zone below 25th percentile ("相對便宜")
- Red zone above 75th percentile ("相對昂貴")

**Plain-language interpretation** (in `_白话_card` analogy field):
- Below 25th percentile: "目前本益比處於歷史偏低區間，相對便宜"
- 25th-75th percentile: "目前本益比處於歷史中間區間，不算貴也不算便宜"
- Above 75th percentile: "目前本益比處於歷史偏高區間，相對貴"

**Component reuse**:
- `_白话_card()` for the current value + interpretation text (reuse existing component, no changes needed)
- Plotly horizontal bar chart (new chart function: `create_valuation_band_chart()`)
- For the percentile calculation: reuse existing price/EPS data pipeline

**Design risk**: P/E band charts can inadvertently suggest "buy when cheap, sell when expensive" — violating the "historian, not stock picker" principle. **Mitigation**: Frame all interpretations historically ("過去这一段區間的表現是...") rather than predictively ("現在便宜，應該買"). Include a `st.caption()` disclaimer: "歷史估值區間僅供參考，不構成投資建議。"

---

## Component Reuse Recommendations

### Existing Components Available in `_router_base.py`

| Component | Used By | Reuse For |
|-----------|---------|-----------|
| `_section_title(title)` | All pages | C152 section headers, C171 chart section, C172 comparison section, C174 story section |
| `_explain_button(...)` | C139 metric explainer | C170 could extend this pattern for glossary terms with explanations |
| `_白话_card(label, value, analogy)` | Key metrics throughout | C171 valuation display card; C173 calculator result cards |
| `_summary_card(title, content, icon, border_color)` | Story card, read-next | **C152 multi-factor narrative summary card** (primary reuse target) |
| `_mini_score_card(label, score)` | Moat dimension cards | C172 concept comparison score display |
| `_info_card(title, content, icon)` | Event cards, tips | C152 individual event detail cards inside expander; C172 concept definition cards |
| `_so_what_box(deltas)` | Metric change implications | NOT recommended for C152 (different use case — metric deltas vs event narratives) |
| `_subsidiary_card(...)` | Group structure | NOT needed for Sprint 21 candidates |
| `_count_label(count, label)` | ETF browser counts | C174 sector story (stock counts per sector) |
| `_glossary_tooltip(term_key, glossary_service)` | C139 popover tooltips | **C170 primary pattern** — systematic application across all metrics |
| `filter_by_timeline(df, ...)` | Historical data pages | C171 P/E band historical range filtering |

### Key Reuse Insight: C170 + C139 Synergy

The `_glossary_tooltip()` component in `_router_base.py` (lines 269-290) already implements the popover pattern needed for C170. C139 uses a st.popover with the ℹ️ icon for metric explanations. C170 should **extend and systematize** this pattern:

1. `_glossary_tooltip(term_key, glossary_service)` → for standalone glossary definitions (what C170 needs most)
2. `_explain_button(metric_name, metric_value, ...)` → for metric-specific explanations with data context (existing C139 pattern)
3. C170 can combine both: a glossary tooltip for the term definition + an explain button for the specific metric value

**Do NOT create a new popover component.** The existing `_glossary_tooltip()` is sufficient for C170's core use case.

### Key Reuse Insight: C152 + `_so_what_box` Relationship

C152 and `_so_what_box(C149)` serve different purposes and should NOT be merged:
- `_so_what_box()` synthesizes **metric deltas** (e.g., "ROE dropped 5%, revenue grew 10%")
- C152 synthesizes **events** (e.g., "revenue miss + insider selling + sector downturn")
- Both answer "So what?" but for different data types
- Both can coexist on the same page (C152 in the events section, `_so_what_box` in the metrics section)

---

## New Component Proposals

### 1. `_event_narrative_card(synthesized_narrative: str, events: list[dict])` (for C152)

**Purpose**: Renders the two-layer progressive disclosure card for multi-factor event narratives.

**API**:
```python
def _event_narrative_card(
    synthesized_narrative: str,
    events: list[dict],  # Each dict: {date, title, content, icon}
    window_label: str = "本週",
) -> None:
```

**Behavior**:
- If `len(events) < 2`: render a single `_info_card()` with the narrative (no expander needed)
- If `len(events) >= 2`: render `_summary_card()` + `st.expander()` containing individual `_info_card()` for each event
- Card border: `#3498DB` (info blue) with `📰` icon

**Why new**: Combines `_summary_card` + expander + multiple `_info_card` into a single reusable pattern. This pattern doesn't exist yet — it's not just a card, it's a card-with-collapsible-details component.

### 2. `_concept_comparison_card(concept_a: dict, concept_b: dict)` (for C172)

**Purpose**: Renders a side-by-side comparison of two financial concepts.

**API**:
```python
def _concept_comparison_card(
    concept_a: dict,  # {name, definition, formula, when_to_use, example, analogy}
    concept_b: dict,  # Same structure
) -> None:
```

**Layout**: Two-column layout. Left column = Concept A, Right column = Concept B. Key differences highlighted with 🟢/🔴 indicators. "When to use" callout at bottom.

**Why new**: No existing component handles side-by-side comparison. `_info_card()` is single-concept only.

### 3. `_calculator_card(title: str, inputs: dict, compute_fn: callable)` (for C173)

**Purpose**: Renders an interactive financial calculator with input fields and real-time results.

**API**:
```python
def _calculator_card(
    title: str,
    inputs: dict,  # {label: {type: "number"|"percent", default: 0, min: 0, max: 100}}
    compute_fn: callable,  # Takes input dict, returns {result: str, analogy: str}
    formula_label: str = "",  # e.g. "複利 = 本金 × (1 + 利率)^年數"
) -> None:
```

**Why new**: Interactive calculator pattern doesn't exist. Must be carefully placed to avoid Zone C violation — recommend placing in a dedicated "Calculators" tab or modal, NOT inline on the business card page.

**Zone C compliance**: Interactive sliders/inputs violate the "no interactive controls in Zone C" design principle. **Recommendation**: C173 calculators should live in a **dedicated page** (e.g., `/calculators`) accessed from the sidebar, NOT embedded in existing stock pages.

---

## Design Risks

### Risk 1: C152 Narrative Quality (Severity: Medium)

**Risk**: Template-generated multi-factor narratives may feel robotic. If synthesis quality is low, beginners won't read the summary card.

**Mitigation**:
- Hire/test templates with native Chinese speakers — Chinese narrative flow is very different from English
- Start with 10-15 high-quality manual templates for the most common event type combinations
- A/B test: show some users the summary + details, others just details. Measure collapsed-vs-expanded rate.
- **Fallback**: If synthesis confidence is low, skip the summary card and show individual events only (graceful degradation)

### Risk 2: C170 Glossary Maintenance Burden (Severity: Low)

**Risk**: Glossary YAML needs to stay in sync with actual metrics displayed. New metrics get added; old ones get renamed.

**Mitigation**:
- Add a pre-commit check: if a metric key is used in code but missing in glossary.yaml, warn (not error)
- Glossary maintenance is a content task, not an engineering task — assign to PM/educational content role
- Prioritize glossary entries by usage frequency: top 20 metrics cover 80% of beginner confusion

### Risk 3: C171 "Valuation Equals Recommendation" Misinterpretation (Severity: Medium)

**Risk**: Showing "目前本益比處於歷史偏低區間，相對便宜" could be interpreted as a buy recommendation, violating the "historian, not stock picker" principle.

**Mitigation**:
- Use historical framing only: "過去十年中，台積電本益比有25%的時間比現在更低"
- Add disclaimer caption: "歷史估值區間僅供參考，不構成投資建議。"
- Avoid the words "便宜" / "貴" — use "處於歷史較低區間" / "處於歷史較高區間" instead
- This aligns with 財報狗's P/E band chart approach (factual, not prescriptive)

### Risk 4: D-003 Regression in New Features (Severity: High)

**Risk**: Sprint 21 adds 3-6 new features, each likely to introduce inline HTML for cards. D-003 (inconsistent card styling) has been the persistent P1 problem for 10+ review rounds.

**Mitigation — Sprint 21 Design Pre-Checklist**:
- [ ] C170 glossary: MUST use `_glossary_tooltip()` from `_router_base.py` — no inline HTML
- [ ] C152 narrative card: MUST use new `_event_narrative_card()` — no inline HTML
- [ ] C171 valuation card: MUST use `_白话_card()` for the value display — no inline HTML
- [ ] C172 comparison: MUST use new `_concept_comparison_card()` — no inline HTML
- [ ] ALL new pages: Must pass `grep -r "unsafe_allow_html" src/pages/` returning zero new occurrences
- [ ] ALL new components: Must be added to `_router_base.py` and documented in `design_system.md`

### Risk 5: C174 Sector Story Complexity (Severity: High)

**Risk**: Sector-level storytelling requires synthesizing data from multiple companies, events, and time periods. This is 3x more complex than company-level storytelling. Beginners may be overwhelmed by cross-company comparisons.

**Mitigation**: Do NOT implement C174 in Sprint 21. Recommend a **spike** (3-5h) to:
1. Identify 3 candidate sectors (semiconductor, finance, ETF)
2. Draft one sector narrative manually
3. Test with 2-3 beginners for comprehension
4. If the spike validates: schedule for Sprint 22

### Risk 6: PPT-Style Violation from C173 Calculators (Severity: Medium)

**Risk**: Interactive calculators with sliders and input fields directly violate the "Zone C: no interactive controls" design principle.

**Mitigation**: C173 must live on a **dedicated page** (sidebar link: "🧮 財務計算機"), NOT embedded in existing stock pages. The calculator page itself should follow PPT-style: one calculator per view, large input/output areas, minimal text.

---

## Recommendations Summary

### Top 3 Recommendations

1. **🔴 Commit C170 (Tappable Glossary) as Sprint 21's foundation feature**
   - 6-10h effort, closes D-012 (oldest P2 gap)
   - Reuses existing `_glossary_tooltip()` — no new component needed
   - Enables beginner-friendly design for ALL concurrent features
   - **Suggested**: Build `glossary.yaml` with 30 terms in Sprint 20 (as pre-work)

2. **🟡 Commit C152 (Multi-Factor Event Narratives) as Sprint 21's headline feature**
   - 16-20h effort, P1 priority
   - Needs one new component: `_event_narrative_card()` in `_router_base.py`
   - Transforms event dashboard from data list to story
   - Design the progressive disclosure pattern carefully: summary first, details on demand

3. **🟢 Commit C171 (Valuation Band Chart) as Sprint 21's chart feature**
   - 8-10h effort, reuses `_白话_card()` + new Plotly chart function
   - Fill the "valuation context" gap that 財報告 users expect
   - Strict historian framing to avoid "buy/sell" misinterpretation

### Sprint 21 Pre-Design Checklist (Before Coding Starts)

- [ ] Create `src/data/glossary.yaml` with 30 core terms (C170 content requirement)
- [ ] Design C152 narrative templates for top 10 event type combinations (C152 content requirement)
- [ ] Define C171 plain-language interpretation thresholds (25th/75th percentile breakpoints)
- [ ] Add `_event_narrative_card()` to `_router_base.py` and document in `design_system.md`
- [ ] Add `create_valuation_band_chart()` to `chart.py`
- [ ] Run D-003 regression check: `grep -r "unsafe_allow_html" src/pages/` baseline
- [ ] Address D-119: Document `_so_what_box()` in `design_system.md` (0.25h quick win)
- [ ] Address D-120: Extract `INDUSTRY_BENCHMARKS` to YAML if not done in Sprint 20

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | All 3 candidates ship with zero inline HTML, `_event_narrative_card()` adds to shared component library, overall inline HTML count decreases |
| **Expected case** | A | C170 + C152 ship, D-003 net unchanged, new components properly documented at `_router_base.py` |
| **Worst case** | A- | Features ship with inline HTML regressions (D-003 worsens), glossary not maintained post-launch |

---

*This section was added by the Design Reviewer for Sprint 21 planning. Next update: After Sprint 21 feature review.*
