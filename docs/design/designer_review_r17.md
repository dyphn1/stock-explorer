# Design Review — Round 17

> **Author**: Design Reviewer
> **Date**: 2026-06-20
> **Context**: Round 17 review — Sprint 4 complete (C38 Compare Stories, C48 Story Card, C51 Sector Heatmap, C53-1 Social Sharing), Sprint 5 prerequisites re-assessed.
> **Current Design Grade**: A (under review — 7th consecutive round attempt)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Grade Assessment](#current-grade-assessment)
3. [Sprint 4 Design Impact](#sprint-4-design-impact)
4. [New Design Issues](#new-design-issues)
5. [Previously Identified Issues Status](#previously-identified-issues-status)
6. [Design System Gaps for Sprint 5](#design-system-gaps-for-sprint-5)
7. [Competitor & Trend Analysis](#competitor--trend-analysis)
8. [Sprint 5 Design Readiness](#sprint-5-design-readiness)
9. [Top 3 Design Recommendations](#top-3-design-recommendations)
10. [Summary](#summary)

---

## Executive Summary

Sprint 4 delivered four features (C38, C48, C51, C53-1) that significantly expanded Stock Explorer's scope. The business card page now has **18 sections** (up from 14 in R16), and a new standalone sector heatmap page was added. Overall design quality remains strong — the A grade is maintained for a **7th consecutive round** — but the cumulative weight of P2 issues is growing. Three previously identified issues (D-042, D-043, D-044) remain unfixed, and four new issues are identified in this review. Sprint 5 prerequisites (D-039, D-040, D-041) are still not started.

---

## Current Grade Assessment

### Overall Grade: A (Maintained — 7th consecutive round)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | All 18 business card sections render within Zone C. Sector heatmap page correctly uses full-width Zone C. No layout intrusions. |
| **PPT-Style Adherence** | A- | 18 sections on business card page. C44/C38/C48 use `st.expander` progressive disclosure. Page length is concerning but managed by expanders. C48's `expanded=True` expander is a smart choice — visible but collapsible. |
| **Card Component Consistency** | B+ | D-003 root cause persists. Sprint 4 features (C38, C48, C53-1) use shared components well. C51 sector heatmap uses inline HTML for grid cells and top-movers (new regression). `_白话_card` still uses `#F5F5F5` (D-037). |
| **Color System** | A- | D-036 (risk card `#FFF8F0`) and D-037 (`_白话_card` `#F5F5F5`) remain. C51 correctly uses Taiwan convention (red=up, green=down). C48 story card uses shared components with correct colors. |
| **Plain-Language System** | A | Historian tone consistent across all 18 sections + sector heatmap. C38 compare stories and C48 story card maintain the analogy engine pattern. |
| **Visual Health Score** | A | C43 + D-034 metric value tooltips unchanged. |
| **Synthesis/Summary Layer** | A | C37 + C48 provide two-tier summary (key takeaways → story card). |
| **Mobile Responsiveness** | B- | D-006 unchanged. C51 sector grid uses `cols_per_row = 4` which will break on mobile. |
| **Design System Documentation** | A | D-004 resolved. Both paths exist and are in sync. |
| **Component Architecture** | B+ | C48 uses `_info_card()` and `_summary_card()` (excellent). C38 uses `_info_card()` for narrative lines (good). C51 uses inline HTML for grid cells and top-movers (regression). C53-1 uses `st.html()` for share button (acceptable but non-standard). |

### Grade Justification

The grade is maintained at **A** for a 7th consecutive round because:

- **Zero P0 issues** — no blocking design problems
- **Core design principles intact** — PPT style, ten-second test, Zone A/B/C, historian tone
- **Sprint 4 features well-designed overall** — C48 uses shared components correctly; C38 uses progressive disclosure; C51 is a clean standalone page
- **No new P1 issues** introduced in Sprint 4
- **Progressive disclosure pattern strengthened** — C38 and C48 both use `st.expander`, bringing the total to 3 expandable sections (C44, C38, C48)

**Risk to grade**: The A could slip to A- in Round 18 if:
1. Sprint 5 features (C71, C73, C74) add more inline HTML without D-041 card components
2. D-003 is not addressed — the B+ in Card Component Consistency is the weakest dimension
3. Page overload (D-005) worsens — 18 sections is approaching the practical limit

---

## Sprint 4 Design Impact

Sprint 4 delivered four features that expanded both the business card page and the overall app scope.

### Positive Design Impacts

1. **C48 (Story Card)** — ✅ Excellent design. Uses `st.expander("📌 30 秒認識這家公司", expanded=True)` for progressive disclosure. Uses `_info_card()`, `_白话_card()`, and `_summary_card()` — all shared components. This is the model for how new sections should be built. The rotating "Did You Know?" fact with session_state index is a nice touch.

2. **C38 (Compare Stories)** — ✅ Good design. Uses `st.expander` with `expanded=False` for progressive disclosure. Uses `_info_card()` for narrative lines. The peer navigation button (`navigate_to`) is well-integrated. The emoji-prefix stripping logic for icons is clever.

3. **C53-1 (Social Sharing)** — ✅ Acceptable design. Uses `st.html()` for the copy button (non-standard but necessary for clipboard API). The share section header uses raw `st.markdown("### 🔗 分享這張名片")` instead of `_section_title()` — a minor inconsistency (see D-047).

4. **C51 (Sector Heatmap)** — ✅ Good overall page design. Correctly uses `_section_title()` and `_info_card()` for KPI cards. The treemap visualization is well-designed with Taiwan convention colors. Progress bar during batch loading is a nice UX touch.

### Negative Design Impacts (New Issues)

5. **D-045: C51 Sector Grid Uses Inline HTML** — The `_render_sector_grid()` function (lines 303-362) builds grid cells with inline HTML using `border-radius:12px` and `padding:1rem` — close to but not matching the design system's `padding:1.2rem`. The `_render_top_movers()` function (lines 365-444) uses inline HTML with `border-radius:10px` and `padding:0.7rem 1rem` — a third distinct card style.

6. **D-046: C51 KPI Card Uses Inline HTML** — The 4th KPI card (漲跌產業數, line 195-201) uses inline HTML instead of `_白话_card()`, breaking the pattern of the first 3 KPI cards which correctly use `_白话_card()`.

7. **D-047: C53-1 Share Section Header Doesn't Use _section_title()** — Line 832 uses raw `st.markdown("### 🔗 分享這張名片")` instead of `_section_title()`. Same pattern as D-044.

8. **D-048: C53-1 Uses st.html() for Share Button** — The copy-to-clipboard button uses `st.html()` with raw JavaScript (lines 875-910). This is a necessary evil for clipboard API access, but it's a non-standard UI component that can't be themed or styled consistently. The `background:#F0F0F0` on the button doesn't match any design system color.

### Net Assessment

Sprint 4 added significant value with **generally good design discipline**. C48 and C38 are model implementations. C51 is a strong standalone page with minor inline HTML issues. C53-1 is functional but introduces `st.html()` as a new pattern. **4 new P2 issues** were introduced, but none are severe enough to threaten the A grade.

---

## New Design Issues

### D-045: C51 Sector Grid and Top Movers Use Inline HTML
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 17
- **Description**: The sector grid cells in `_render_sector_grid()` (lines 342-362) and top-mover rows in `_render_top_movers()` (lines 391-444) use inline HTML with non-standard styling. Grid cells use `padding:1rem` (vs design system `1.2rem`) and top-movers use `border-radius:10px` (vs `12px`) and `padding:0.7rem 1rem` (vs `1.2rem`). This creates a third distinct card style on the sector heatmap page, alongside the correctly-styled `_白话_card()` KPIs and `_info_card()` treemap description.
- **Affected Files**: `src/pages/sector_heatmap.py` lines 342-362, 391-444
- **Proposed Fix**: Create `_sector_grid_card()` and `_mover_row()` helpers in a shared location, or adapt the existing `_info_card()` / `_白话_card()` for these use cases. If the compact style is intentional, document it as a "compact card" variant in the design system.
- **Effort**: 1-2h

### D-046: C51 4th KPI Card Uses Inline HTML Instead of _白话_card()
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 17
- **Description**: The first 3 KPI cards on the sector heatmap page (lines 175-192) correctly use `_shared_card()`, but the 4th card (漲跌產業數, lines 195-201) uses inline HTML with manually specified styling. The inline HTML uses `background:#F8F9FA` (correct) but the overall card structure doesn't match `_白话_card()`'s label/value/analogy pattern.
- **Affected Files**: `src/pages/sector_heatmap.py` lines 195-201
- **Proposed Fix**: Replace with `_白话_card(f"🔴 {up_sectors} / 🟢 {down_sectors}", "上漲 / 下跌", "漲跌產業數")` or similar. The current format with emoji in the value is slightly non-standard for `_白话_card()` but would be more consistent.
- **Effort**: <0.5h

### D-047: C53-1 Share Section Header Doesn't Use _section_title()
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 17
- **Description**: `_render_share_section()` at line 832 uses raw `st.markdown("### 🔗 分享這張名片")` instead of the `_section_title()` helper. This is the same pattern as D-044 (C41 Read Next header). The header doesn't get emoji-prefix detection and consistent formatting.
- **Affected Files**: `src/pages/business_card/_sections.py` line 832
- **Proposed Fix**: Replace with `_section_title("🔗 分享這張名片")`.
- **Effort**: <0.5h (one-line change)

### D-048: C53-1 Share Button Uses st.html() — Non-Standard Component
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 17
- **Description**: The social sharing copy button uses `st.html()` with raw JavaScript (lines 875-910 of `_sections.py`). This is the first use of `st.html()` in the project for a UI component. The button's inline styles (`background:#F0F0F0`, `border-radius:8px`) don't match any design system specification. While `st.html()` is necessary for clipboard API access, the component should be standardized.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 875-910
- **Proposed Fix**: Create a `_share_button(url, key)` helper in `_router_base.py` that encapsulates the JS + HTML. Document the `st.html()` pattern in the design system as an "escape hatch" for features requiring JavaScript.
- **Effort**: 0.5-1h

---

## Previously Identified Issues Status

### D-042: Health Dimension Mini-Cards Use Non-Standard Styling — ❌ NOT FIXED

**Status**: Unchanged since Round 16.

The 5-dimension score cards in `_render_health()` (lines 347-352 of `_sections.py`) still use inline HTML with `padding:0.5rem`, `border-radius:10px`, and no `border-left`. The design system specifies `padding:1.2rem`, `border-radius:12px`, `border-left:4px solid`.

**Current code** (line 347):
```html
<div style="text-align:center;padding:0.5rem;background:#F8F9FA;border-radius:10px;margin:0.2rem 0;">
```

**Recommended fix**: Create a `_mini_score_card()` helper in `_router_base.py` with standardized compact styling. This would be a recognized "mini card" variant in the design system.

### D-043: Dividend History Table Uses Inline HTML Instead of st.dataframe — ❌ NOT FIXED

**Status**: Unchanged since Round 16.

The dividend history table (lines 538-557 of `_sections.py`) still builds a complete HTML table from scratch. The `border-bottom:1px solid #F8F9FA` is nearly invisible on white backgrounds.

**Recommended fix**: Use `st.dataframe()` with column config for badges, or change to `border-bottom:1px solid #BDC3C7` for visible row separators.

### D-044: C41 Read Next Header Doesn't Use _section_title() — ❌ NOT FIXED

**Status**: Unchanged since Round 16.

Line 768 still uses raw `st.markdown("### 📖 推薦閱讀")` instead of `_section_title("📖 推薦閱讀")`.

**Recommended fix**: One-line change to `_section_title("📖 推薦閱讀")`.

### Other Previously Identified Issues

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| D-003 | Inconsistent Card Styling | 🔄 Ongoing | C48/C38 improve (use shared components). C51 worsens (inline HTML). Net: slight improvement. |
| D-005 | Business Card Page Overload | 🔄 Ongoing | 18 sections now. C48/C38 expanders help. Net: manageable but concerning. |
| D-006 | Mobile Responsiveness | ❌ Unchanged | C51's 4-column grid will break on mobile. |
| D-036 | Risk Card Background | ❌ Unchanged | `_helpers.py` line 86 still uses `#FFF8F0`. |
| D-037 | `_白话_card` Background | ❌ Unchanged | `_router_base.py` line 91 still uses `#F5F5F5`. |
| D-038 | C41 API in View Layer | ❌ Unchanged | Line 771 still calls `client.get_stock_info()` in view layer. |
| D-039 | No Standardized Section Headers | ❌ Not started | 8 raw `st.markdown("### ...")` calls in `_sections.py` + 5 in `sector_heatmap.py`. |
| D-040 | No Standardized Disclaimer | ❌ Not started | C73/C74 will need this. |
| D-041 | No Sprint 5 Card Components | ❌ Not started | C71/C73/C74 will need this. |

---

## Design System Gaps for Sprint 5

Sprint 5 will add three features: C71 (Study Log), C73 (Expert Analysis), C74 (Historical Scenarios). The following design system gaps must be addressed before implementation.

### Gap 1: No Study Log Card Component (C71)

**Current State**: No `_study_card()` component exists. C71 will add study log entries to the business card page — a new card type showing user's learning progress.

**Required Design**:
```html
<!-- Study log entry card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-size:0.8rem;color:#7F8C8D;">{date} · {topic}</div>
    <div style="font-weight:600;color:#2C3E50;margin-top:0.3rem;">{title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.3rem;line-height:1.6;">{summary}</div>
</div>
```

**Recommendation**: Create `_study_card(date, topic, title, summary)` in `_router_base.py`. Use `st.expander` for the section with `expanded=False` (following C44/C38 pattern).

### Gap 2: No Expert Analysis Card Component (C73)

**Current State**: No `_expert_card()` component exists. C73 will show expert analysis for 10 stocks — a new card type with consensus ratings and analyst commentary.

**Required Design**:
```html
<!-- Expert analysis card -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} 分析師共識</div>
    <div style="font-size:1.4rem;font-weight:700;color:{consensus_color};margin:0.3rem 0;">{consensus_label}</div>
    <div style="font-size:0.85rem;color:#7F8C8D;">基於 {analyst_count} 位分析師</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{key_points}</div>
</div>
```

**Recommendation**: Create `_expert_card(consensus, analyst_count, key_points)` in `_router_base.py`. Use orange border (`#F39C12`) to distinguish from info cards. Include `_historian_disclaimer("expert")` below the card.

### Gap 3: No Historical Scenario Card Component (C74)

**Current State**: No `_scenario_card()` component exists. C74 will show historical scenarios — "what happened to this stock during event X?"

**Required Design**:
```html
<!-- Historical scenario card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">📅 {event_name}（{event_date}）</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.7;">{narrative}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{historian_takeaway}</div>
</div>
```

**Recommendation**: Create `_scenario_card(event_name, event_date, narrative, historian_takeaway)` in `_router_base.py`. Use blue border (info style). Include `_historian_disclaimer("scenario")` below each scenario.

### Gap 4: No Mini Score Card Variant (D-042)

The health dimension cards have established a de facto "mini card" pattern that should be formalized:

```html
<!-- Mini score card (for compact grid layouts) -->
<div style="text-align:center;padding:0.5rem;background:#F8F9FA;border-radius:10px;margin:0.2rem 0;">
    <div style="font-size:0.8rem;color:#7F8C8D;">{indicator} {label}</div>
    <div style="font-size:1.4rem;font-weight:700;color:#2C3E50;">{value}</div>
    <div style="font-size:0.7rem;color:#7F8C8D;margin-top:0.2rem;">{description}</div>
</div>
```

### Gap 5: No Compact Card Variant for Grid Layouts (D-045)

The sector heatmap has established a "compact card" pattern for grid displays:

```html
<!-- Compact card (for grid/tile layouts) -->
<div style="background:{bg};border-radius:12px;padding:1rem;margin-bottom:0.5rem;border-left:4px solid {border_color};min-height:140px;">
    <div style="font-size:0.75rem;color:#7F8C8D;">{subtitle}</div>
    <div style="font-size:1.5rem;font-weight:700;color:{text_color};margin:0.3rem 0;">{value}</div>
    <div style="font-size:0.75rem;color:#7F8C8D;">{detail}</div>
</div>
```

### Gap 6: No Standardized st.html() Pattern (D-048)

C53-1 introduced `st.html()` for JavaScript-dependent UI. This should be documented as an "escape hatch" pattern:

**Design System Rule**: `st.html()` should only be used when no Streamlit native component provides the required functionality. All `st.html()` usage must:
1. Be encapsulated in a named helper function
2. Use design system colors (no hardcoded hex values)
3. Include a fallback for when JavaScript is unavailable
4. Be documented in the design system under "JavaScript Escape Hatches"

---

## Competitor & Trend Analysis

### Robinhood (2025-2026)
- **Clean minimalist cards**: Robinhood uses white cards with subtle shadows on a light gray background. Stock Explorer's `#F8F9FA` card background is consistent with this trend.
- **Progressive disclosure**: Robinhood shows a simple stock page by default, with "Show More" for detailed financials. Stock Explorer's `st.expander` pattern (C44, C38, C48) follows this trend well.
- **Metric tooltips**: Robinhood has hover tooltips on every metric. Stock Explorer's D-034 fix (metric values in hover + dimension cards) is competitive.
- **Dark mode**: Robinhood defaults to dark mode. Stock Explorer uses a light theme — this is acceptable for the Taiwan market where light themes dominate financial apps.

### Public.com (2025-2026)
- **Story-first approach**: Public.com leads with narrative ("Why people invest in this") before numbers. Stock Explorer's C48 (Story Card) + C37 (Key Takeaways) mirrors this approach.
- **Social features**: Public.com has comments and social sharing built in. Stock Explorer's C53-1 (Social Sharing URL) is a lighter but appropriate version.
- **Plain-language**: Public.com explains every metric in plain English. Stock Explorer's analogy engine is competitive.

### Coinbase (2025-2026)
- **Data visualization**: Coinbase uses clean, colorful charts with consistent color coding. Stock Explorer's Plotly charts with design system colors are on par.
- **Mobile-first**: Coinbase is mobile-native. Stock Explorer's mobile responsiveness (D-006, grade B-) is the weakest dimension compared to competitors.
- **Micro-interactions**: Coinbase has subtle animations on price changes. Streamlit limits this, but the `st.toast()` notifications for watchlist actions are a good substitute.

### Figma Finance UI Trends (2025-2026)
- **Glassmorphism**: Trending in consumer fintech but not yet in professional/analytical tools. Stock Explorer's flat card design is appropriate for its audience.
- **Bento grids**: Card-based grid layouts (like Apple's promotional pages). Stock Explorer's sector heatmap grid (C51) follows this trend.
- **Accessible color contrast**: WCAG 2.1 AA compliance is now standard. Stock Explorer's color palette (`#2C3E50` on `#F8F9FA`) provides good contrast. The `#7F8C8D` secondary text on `#F8F9FA` background should be verified for AA compliance (contrast ratio ~4.5:1 — borderline).
- **Large touch targets**: 44px minimum touch targets on mobile. Stock Explorer's buttons meet this, but the sector grid cells may not.

### Key Trends Stock Explorer Should Adopt

1. **Accessibility contrast check**: Verify `#7F8C8D` on `#F8F9FA` meets WCAG AA. If not, darken to `#5D6D7E` or similar.
2. **Mobile-first grid**: C51's 4-column grid should switch to 2-column on mobile (currently no mobile-specific CSS for the heatmap page).
3. **Skeleton loading**: Replace `st.spinner()` with skeleton placeholders for a more polished loading experience (Streamlit limitation — may not be feasible).
4. **Consistent empty states**: D-033 (standardized empty state component) remains unresolved. Every competitor has a consistent empty state design.

---

## Sprint 5 Design Readiness

### Readiness Score: 6/10 — ⚠️ MODERATE RISK

| Criterion | Status | Risk |
|-----------|--------|------|
| Card components for C71/C73/C74 | ❌ Not created | HIGH — will likely use inline HTML |
| Section header standardization (D-039) | ❌ Not started | MEDIUM — 8+ raw headers already exist |
| Disclaimer component (D-040) | ❌ Not started | MEDIUM — regulatory risk for C73/C74 |
| Design system doc updates | ❌ Not started | LOW — can be done in parallel |
| Mobile responsiveness for new features | ❌ Not assessed | MEDIUM — C73 may need multi-column layout |
| Accessibility audit | ❌ Not done | LOW — no new colors planned |

### Prerequisites That Must Be Completed Before Sprint 5 Coding

1. **D-041: Create card components** (1h) — `_study_card()`, `_expert_card()`, `_scenario_card()` in `_router_base.py`
2. **D-039: Standardize section headers** (1-2h) — Replace all raw `st.markdown("### ...")` with `_section_title()`
3. **D-040: Create disclaimer component** (0.5h) — `_historian_disclaimer(type)` in `_router_base.py`
4. **D-037: Fix `_白话_card` background** (<0.5h) — `#F5F5F5` → `#F8F9FA`
5. **D-036: Fix risk card background** (<0.5h) — `#FFF8F0` → `#F8F9FA`

**Total prerequisite effort**: 3-4.5h — should be completed as the first Sprint 5 task.

### Design System Updates Needed

1. Add "Mini Score Card" variant (for D-042)
2. Add "Compact Card" variant (for D-045)
3. Add "Study Log Card" specification (for C71)
4. Add "Expert Analysis Card" specification (for C73)
5. Add "Historical Scenario Card" specification (for C74)
6. Add "JavaScript Escape Hatch" pattern documentation (for D-048)
7. Add accessibility contrast requirements (WCAG AA)
8. Add mobile grid rules (2-column max on mobile)

---

## Top 3 Design Recommendation

### #1: Fix D-003 (Inconsistent Card Styling) — Consolidate All Inline HTML

**Priority**: HIGHEST
**Effort**: 2-3h
**Impact**: Would raise Card Component Consistency from B+ to A-

This is the single most impactful design improvement available. The pattern is proven (C48, C38 use shared components correctly), but 5+ sections still use inline HTML. Every new feature that uses inline HTML worsens the inconsistency. **Recommendation**: Dedicate 2-3h in early Sprint 5 to replace all remaining inline HTML cards with shared components. This includes:
- Health dimension mini-cards (D-042) → `_mini_score_card()`
- Dividend history table (D-043) → `st.dataframe()` or `_info_card()` per row
- Sector heatmap grid cells (D-045) → `_sector_grid_card()` or `_info_card()`
- Sector heatmap top movers (D-045) → `_mover_row()` or `_info_card()`
- Group structure subsidiary cards → `_info_card()` variant
- Share button (D-048) → `_share_button()` helper

### #2: Complete All Sprint 5 Prerequisites Before Feature Coding

**Priority**: HIGH
**Effort**: 3-4.5h
**Impact**: Prevents D-003 from worsening, ensures regulatory compliance for C73/C74

D-039 (section headers), D-040 (disclaimer component), and D-041 (card components) have been "not started" since Round 15. Each sprint that passes without addressing these makes the next sprint harder. **Recommendation**: Make these 3 prerequisites the first tasks of Sprint 5, before any C71/C73/C74 implementation begins.

### #3: Add Mobile-Specific CSS for C51 Sector Heatmap

**Priority**: MEDIUM
**Effort**: 1-2h
**Impact**: Raises Mobile Responsiveness from B- to B+

The sector heatmap page has a 4-column grid (`cols_per_row = 4`) that will break on mobile. The existing mobile CSS (768px and 600px breakpoints) only adjusts padding and font sizes. **Recommendation**: Add mobile-specific CSS that:
- Switches the sector grid to 2 columns on screens < 768px
- Increases touch target sizes for stock buttons
- Adjusts the treemap height for mobile (currently 500px — too tall for mobile)
- Stacks the top-movers columns vertically on mobile

---

## Summary

### What Changed Since Round 16

1. **Sprint 4 completed** — All 4 Sprint 4 features (C38, C48, C51, C53-1) are now live.
2. **Business card page grew to 18 sections** — C48 (story card) at top, C38 (compare stories) and C53-1 (sharing) at bottom.
3. **New standalone page** — C51 sector heatmap is the first non-business-card page with significant UI.
4. **No new P1 issues** — The 3 active P1 issues (D-003, D-005, D-006) remain unchanged.
5. **4 new P2 issues identified** — D-045 (C51 inline HTML), D-046 (C51 KPI card), D-047 (C53-1 header), D-048 (C53-1 st.html).
6. **3 previously identified P2 issues remain unfixed** — D-042, D-043, D-044.
7. **Sprint 5 prerequisites still not started** — D-039, D-040, D-041 remain at 0% progress.

### Design Issues Updated Counts

| Category | Previous (R16) | Current (R17) | Change |
|----------|----------------|----------------|--------|
| P0 (Blocking) | 0 | 0 | — |
| P1 (Important) | 3 | 3 | — |
| P2 (Optimization) | 16 | 19 | +3 (D-045, D-046, D-047, D-048; net +3 after counting) |
| Resolved | 15 | 15 | — |
| **Total** | **34** | **37** | **+3** |

*Note: D-042, D-043, D-044 were already counted in R16's total of 16 P2 issues. The 4 new issues (D-045-D-048) bring the net to 19 active P2 issues.*

### Grade Decision: A (Maintained — 7th consecutive round)

**Rationale**: Sprint 4 features were well-designed overall. C48 is a model implementation that uses shared components correctly. C38 and C51 are strong additions. The 4 new P2 issues are all low-severity optimizations. The B+ in Card Component Consistency remains the weakest dimension but is offset by strengths across all other dimensions. The A grade is maintained but is increasingly dependent on addressing D-003 before Sprint 5 adds more inline HTML.

### Top Priority Actions for Sprint 5

1. **Before any Sprint 5 coding**: Complete all 3 prerequisites (D-039, D-040, D-041) — 2.5-3.5h total.
2. **Quick wins** (can be done any time):
   - Fix D-037: `#F5F5F5` → `#F8F9FA` in `_router_base.py` line 91 (<0.5h)
   - Fix D-036: `#FFF8F0` → `#F8F9FA` in `_helpers.py` line 86 (<0.5h)
   - Fix D-044: Use `_section_title()` in `_render_read_next` (<0.5h)
   - Fix D-046: Use `_白话_card()` for 4th KPI in sector heatmap (<0.5h)
   - Fix D-047: Use `_section_title()` in `_render_share_section` (<0.5h)
3. **During Sprint 5**: Address D-003 comprehensively — replace all inline HTML cards with shared components (2-3h).
4. **During Sprint 5**: Add mobile-specific CSS for C51 sector heatmap (1-2h).

---

*Design Review maintained by Design Reviewer. Next update: After Sprint 5 feature implementation or Round 18, whichever comes first.*
