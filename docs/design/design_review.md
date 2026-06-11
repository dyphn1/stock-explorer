# Stock Explorer Design Review

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
