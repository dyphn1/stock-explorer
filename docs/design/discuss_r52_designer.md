# Sprint 26 Design Assessment

> **Prepared by**: Design Reviewer (automated cron)
> **Date**: 2026-06-17
> **Sprint Context**: Sprint 25 complete → Sprint 26 planning
> **Sources**: `current_problems.md` (Round 7), `design_system.md`, `pending_review.md`

---

## 1. Current Design System Compliance Status

### Overall Grade: **C+** (unchanged from Round 6)

**Cumulative issue count: 92 issues across 7 rounds, 5 fixed**

| Round | Date | New | Total | Fixed |
|-------|------|-----|-------|-------|
| Round 2 | 2026-06-10 | 26 | 26 | 2 (D-012, D-016) |
| Round 3 | 2026-06-11 | 3 | 29 | 0 |
| Round 4 | 2026-06-12 | 25 | 54 | 0 |
| Round 5 | 2026-06-12 | 17 | 71 | 2 (D-002, D-029) |
| Round 6 | 2026-06-12 | 10 | 81 | 1 (D-059) |
| Round 7 | 2026-06-13 | 11 | 92 | 0 |

### Page Grades (Round 7)

| Page | Grade | Notes |
|------|-------|-------|
| event_dashboard.py | **A-** | Best-graded page |
| chart.py | **B+** | D-071 Set3 palette remains |
| _router_base.py | **B** | D-073 affects all pages via shared components |
| business_card.py | **B** | 6 minor color violations |
| financial_health.py | **C+** | Stable |
| etf_browser.py | **C** | Stable |
| watchlist_page.py | **C** | Stable |
| operation_checkup.py | **C** | Stable |
| peer_comparison.py | **C** | Stable |
| etf_detail.py | **C** | Downgraded from C+ (D-76, D-77) |
| main.py | **C-** | Downgraded from C (D-81, D-82, D-83) |
| group_structure.py | **D** | D-078, D-084 |
| category_browser.py | **D** | Structural issues remain |

### Key Observations
- **Grade progression**: D+ → C- → C → C+ over 5 rounds. The trajectory is positive but slowing.
- **3 pages at D grade** (group_structure, category_browser) are the biggest drag on the overall score.
- **event_dashboard.py at A-** proves the team can produce high-quality pages — this should be the reference standard.
- **Zero new illegal palette colors** found in Round 7 (all F39C12, 2E86C1, 1A4F72, 8E44AD, 2ECC71, 4A90D9 instances cleaned). All linear-gradient instances eliminated. This is a major structural win.
- Round 7's 11 new issues are all **minor color deviations** (#5D6D7E vs #7F8C8D, #95A5A6, #BDC3C7) — not new categories of problems.

---

## 2. Impact Analysis: Top 5 Recommended Fixes

From Round 7, the recommended priority order (reordered by impact):

| Priority | Issue | Effort | Impact | Scope |
|----------|-------|--------|--------|-------|
| 1 | **D-073**: Fix `#5D6D7E` → `#7F8C8D` in `_info_card()` | 5 min | **Global** — every page using `_info_card()` | Shared component |
| 2 | **D-071**: Replace Set3 palette in pie charts | 30 min | **Global** — all pie charts | chart.py |
| 3 | **D-084**: Replace `st.bar_chart` with Plotly | 30 min | **Single page** — group_structure.py | Architecture compliance |
| 4 | **D-005**: Fix `_section_title()` emoji logic | 15 min | **Global** — all section titles | Shared component |
| 5 | **D-074**: Standardize `#F8F9FA` background | 10 min | **Global** — all `_白话_card()` | Shared component |

### Combined Impact Assessment
- **Total effort**: 90 minutes (1.5 hours)
- **Global reach**: 4 of 5 fixes touch shared components (`_router_base.py`, `chart.py`), meaning a single change propagates across all 13+ pages.
- **Expected grade impact**: Fixing D-073 alone could upgrade `_router_base.py` from B to B+, and since `_info_card()` is used on most pages, the ripple effect could push the overall grade toward **B-**.
- **D-071 (Set3 palette)**: This is the last remaining chart-level color violation. Fixing it would bring `chart.py` from B+ to A-, making it the second A-grade file.
- **D-084 (st.bar_chart)**: This is the last architecture violation in the chart layer. Fixing it means **zero architecture violations** remain — a significant milestone.
- **D-005 (emoji conflict)**: A persistent issue across 3 rounds. Low effort, affects all section titles. Should not be deferred further.
- **D-074 (#F8F9FA)**: The design system specifies `#F8F9FA` as the card background color, so this may actually be a design system documentation issue rather than a code issue. Needs clarification before fixing.

### Recommendation: Execute all 5 in Sprint 26
The combined 1.5-hour effort for global improvements across shared components is an exceptional ROI. These should be batch-fixed in the first day of Sprint 26.

---

## 3. Design Feasibility: C203 Ecosystem Cards

### Proposal Summary (from pending_review.md)
- **Scope**: Card-based layout for 8 companies (5 existing + 3 new)
- **Content**: Parent-subsidiary + 2-3 well-known customer-supplier pairs
- **Component reuse**: `_subsidiary_card()` — no new component needed
- **Estimate**: 10-12 hours (down from 36-50h for original "Supply Chain Visual Map")
- **Default if no response**: Defer to Sprint 26

### Design Feasibility Assessment

**✅ Strengths:**
1. **Component reuse**: `_subsidiary_card()` already exists in `group_structure.py` and follows the design system card spec (border-radius: 12px, padding: 1.2rem, border-left accent). Zero new component development needed.
2. **Data availability**: Uses existing data — no paid API dependency. This eliminates the original proposal's biggest risk.
3. **Alignment with design system**: Card-based layout directly conforms to the component spec in Section 3.3 of `design_system.md`. Each card would use the standard info card pattern (label + value + plain-language explanation).
4. **PPT style compliance**: A card grid naturally follows "one key point per page" — each card is one company in the ecosystem. Text per card would be minimal (company name, relationship type, key metric).
5. **Precedent**: `group_structure.py` already renders subsidiary cards. The rendering pattern is proven.

**⚠️ Risks & Concerns:**
1. **group_structure.py is graded D**: The host page has known issues (D-078 color violations, D-084 st.bar_chart). Adding new content to a D-grade page without fixing its existing issues could increase technical debt.
2. **Customer-supplier data quality**: "Well-known" pairs may not have clean data in FinMind. Need to verify data availability for at least 2-3 pairs before committing.
3. **Layout density**: 8 cards in a grid could exceed the 200-char text limit if each card has a description. Need to enforce strict text constraints.
4. **Scope creep risk**: "2-3 well-known customer-supplier pairs" is vague. Should be scoped to exactly which pairs and verified against available data.

**📋 Design Requirements for C203:**
- Must use `_subsidiary_card()` or `_info_card()` — no raw HTML cards
- Card colors must use design system palette only (#3498DB border for info cards)
- Text per card ≤ 2 sentences (plain-language explanation)
- Chart proportion on page must be > 60% (cards should supplement, not replace, data visualization)
- Must pass the "ten-second test": a beginner understands the ecosystem in 10 seconds

**Verdict**: **Feasible for Sprint 26** with the condition that D-078 and D-084 on `group_structure.py` are fixed first (or in parallel). The 10-12h estimate is realistic given component reuse.

---

## 4. Sprint 26 Design Prioritization Recommendations

### Tier 1: Quick Wins (Day 1, ~2 hours)
These are global-impact, low-effort fixes that should be done immediately:

| Task | Issue | Effort | Expected Impact |
|------|-------|--------|-----------------|
| Fix `_info_card()` text color | D-073 | 5 min | All pages |
| Fix `_section_title()` emoji | D-005 | 15 min | All section titles |
| Replace Set3 in pie charts | D-071 | 30 min | All pie charts |
| Replace st.bar_chart with Plotly | D-084 | 30 min | group_structure.py |
| Standardize `#F8F9FA` | D-074 | 10 min | All `_白话_card()` |
| Fix main.py disclaimer colors | D-81 | 10 min | main.py upgrade to C |
| Fix main.py sidebar/welcome colors | D-82, D-83 | 15 min | main.py upgrade to C+ |

**Subtotal: ~2 hours. Expected grade impact: C+ → B-**

### Tier 2: D-Grade Page Remediation (Days 2-3, ~4-6 hours)
Focus on the two D-grade pages to eliminate the lowest performers:

| Task | Target | Effort | Expected Impact |
|------|--------|--------|-----------------|
| Fix group_structure.py colors (D-078) | group_structure.py | 30 min | D → C+ |
| Fix category_browser.py structural issues | category_browser.py | 2-3 h | D → C+ |
| Migrate raw HTML cards to `_白话_card()` (D-41, D-42, D-48) | category_browser.py, etf_browser.py | 1-2 h | Component consistency |

**Subtotal: ~4-6 hours. Expected grade impact: B- → B**

### Tier 3: New Feature — C203 Ecosystem Cards (Days 3-5, ~10-12 hours)
- Implement card-based ecosystem layout
- Reuse `_subsidiary_card()` component
- Verify customer-supplier data availability first

### Tier 4: Future Sprint Candidates
- **D-126 Dark/Light Theme**: 8-12h effort. Low priority — current dark theme works, this is a nice-to-have.
- **D-127 _infocard() component**: 6-9h effort. Medium priority — would improve visual-first metrics but requires new component design.

---

## 5. D-126 (Dark/Light Theme) vs D-127 (_infocard): Priority Recommendation

### D-126: Dark/Light Theme Implementation
- **Effort**: 8-12 hours
- **Impact**: Cosmetic preference, no functional improvement
- **Risk**: High — CSS variable refactoring touches every file, could introduce regressions across all 13+ pages
- **Current state**: The app works in dark mode. Users have not reported theme-switching as a need.
- **Design system status**: Not mentioned in `design_system.md` at all. Would require design system amendment first.

### D-127: _infocard() Component
- **Effort**: 6-9 hours
- **Impact**: Enables infographic-style visual cards — directly supports the "PPT style" and "image-first" design principles
- **Risk**: Medium — new component, but follows existing `_info_card()` patterns
- **Current state**: Multiple pages (financial_health, etf_detail, category_browser) use raw HTML cards that should be using a standardized component. An `_infocard()` would give them a proper home.
- **Design system status**: Would extend Section 3.3 (Cards) — a natural evolution of the existing spec.

### Recommendation: **Prioritize D-127 (_infocard) over D-126 (Theme)**

**Rationale:**
1. **D-127 directly supports the design philosophy** of "PPT style" and "image-first" — it's not cosmetic, it's functional.
2. **Lower risk**: 6-9h vs 8-12h, and doesn't touch every file in the project.
3. **Immediate use case**: The raw HTML cards identified in D-41, D-42, D-44, D-45, D-47, D-48 could all be migrated to `_infocard()` once it exists, compounding the design grade improvement.
4. **D-126 should wait**: Theme switching is a significant architectural change (CSS variables, every color reference becomes dynamic). It should be planned as a dedicated sprint item, not squeezed into a sprint with other priorities.
5. **D-126 prerequisite**: The color system should be fully compliant (all 92 issues resolved or acknowledged) before introducing theme switching, otherwise you're multiplying the maintenance surface.

**Suggested Sprint 26 ordering**: Tier 1 quick wins → Tier 2 D-grade remediation → C203 Ecosystem Cards → D-127 _infocard (if time permits). Defer D-126 to Sprint 27+.

---

## 6. Summary

| Metric | Value |
|--------|-------|
| Current grade | C+ |
| Total issues | 92 (5 fixed) |
| Top 5 fix effort | 1.5 hours combined |
| Projected grade after Tier 1+2 | B |
| C203 feasibility | ✅ Feasible (10-12h, reuses existing component) |
| D-126 vs D-127 | Prioritize D-127 (_infocard) |
| Recommended Sprint 26 focus | Quick wins → D-grade pages → C203 → D-127 |

**Bottom line**: Sprint 26 is positioned to be a high-impact design sprint. The low-hanging fruit (1.5 hours of fixes) can move the overall grade from C+ to B-, and the C203 feature is well-scoped with proven component reuse. The team should resist the temptation to start D-126 (theme switching) until color compliance is fully resolved.
