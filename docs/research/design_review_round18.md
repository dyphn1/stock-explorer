# Design Review — Round 18

> **Date**: 2026-06-12
> **Reviewer**: Design Reviewer
> **Scope**: Sprint 6 delivered features — C83 Investment Memo, C85 Financial Wellness, C02 Notification Center
> **Previous Grade**: A (Round 17)
> **Recommended Grade**: A (9th consecutive)

---

## Executive Summary

Sprint 6 delivered three standalone pages (C83, C85, C02) that are **the cleanest new pages since the project began**. All three use shared card components (`_info_card()`, `_summary_card()`, `_study_card()`, `_expert_card()`), standardized section headers (`_section_title()`), and standardized disclaimers (`_historian_disclaimer()`). The D-037 fix (card background color) landed in Sprint 6. No new P0 or P1 issues were introduced. Two minor P2 issues were found (D-049, D-050). The overall design grade remains **A**.

---

## Sprint 6 Feature Reviews

### C83 — Investment Memo (`investment_memo.py` + `investment_memo_service.py`)

| Criterion | Score | Notes |
|-----------|-------|-------|
| PPT-style compliance | ✅ PASS | Tip card + form + saved memos. Each saved memo rendered as one `_summary_card()` — one key point per card. |
| Card consistency | ✅ PASS | Uses `_info_card()` for tip, `_summary_card()` for saved memos, `_section_title()` for headers. Zero inline HTML. |
| Zone A/B/C separation | ✅ PASS | Tip (Zone A context), form (Zone B interaction), saved list (Zone C reference). Clean flow. |
| Loading state | ✅ PASS | `st.spinner("搜尋中…")` for stock search. |
| Error state | ✅ PASS | `st.warning()` for no matches, `st.error()` for validation failures, `st.success()` for save confirmation. |
| Color system | ✅ PASS | All colors via shared components. No hardcoded colors in page code. |
| Service layer | ✅ PASS | Zero Streamlit imports. Pure business logic. |

**PPT-Style Compliance Score: A+**
This is the best-designed new page in the project. It follows the "one key point per card" principle perfectly — each saved memo is a single `_summary_card()` with structured content. The tip card at top sets context without clutter. The form is clean and well-organized.

**New issues found: NONE**

---

### C85 — Financial Wellness (`financial_wellness.py` + `financial_wellness_service.py`)

| Criterion | Score | Notes |
|-----------|-------|-------|
| PPT-style compliance | ⚠️ PARTIAL | Quiz results page has 3 score cards in a row + interpretation card + tips + category breakdown. The 3-column score cards use inline HTML (D-049). |
| Card consistency | ⚠️ PARTIAL | Uses `_summary_card()` and `_info_card()` correctly for interpretation and tips. BUT the 3 score cards and category breakdown cards use inline HTML. |
| Zone A/B/C separation | ✅ PASS | Intro (Zone A), quiz form (Zone B), results (Zone B), tips (Zone C). |
| Loading state | ✅ PASS | No explicit spinner needed (quiz is client-side), but results render immediately. |
| Error state | ✅ PASS | `st.warning()` for missing answers. Graceful handling of empty state. |
| Color system | ⚠️ PARTIAL | Hardcoded colors in inline HTML: `#27AE60`, `#F39C12`, `#E74C3C`, `#3498DB`, `#F8F9FA`, `#7F8C8D`. While these match the design system values, they're specified inline rather than via shared components. |
| Service layer | ✅ PASS | Zero Streamlit imports. Pure business logic with question bank, scoring, interpretation, and tips. |

**PPT-Style Compliance Score: B+**
The quiz flow is well-designed, but the results page has too many visual elements competing for attention. The 3-column score cards with inline HTML are a step backward from the card consistency standard. The category breakdown with 3-column grid of inline HTML cards also adds visual noise.

**New issues found: D-049** (see below)

---

### C02 — Notification Center (`notification_center.py` + `notification_service.py`)

| Criterion | Score | Notes |
|-----------|-------|-------|
| PPT-style compliance | ✅ PASS | Summary banner (one key point) + notification list (one card per event) + settings (collapsed). |
| Card consistency | ✅ PASS | Uses `_summary_card()` for summary, `_expert_card()` for high severity, `_study_card()` for medium/low, `_info_card()` for empty states, `_section_title()` for headers. Excellent. |
| Zone A/B/C separation | ✅ PASS | Summary (Zone A), notification list (Zone B), settings in expander (Zone C). |
| Loading state | ✅ PASS | `st.spinner("檢查通知...")` and `st.spinner("載入通知...")` for async operations. |
| Error state | ✅ PASS | Empty state handled with `_info_card()`. Graceful handling of no subscriptions. |
| Color system | ✅ PASS | Severity colors defined in `_severity_color()` helper using standard palette values. Notification settings use `st.expander` for progressive disclosure. |
| Service layer | ✅ PASS | Zero Streamlit imports. Clean separation of data access, settings management, and event processing. |

**PPT-Style Compliance Score: A**
The notification center is well-architected. The severity-based card selection (`_expert_card` for high, `_study_card` for medium/low) is a clever use of the card component system. The settings panel correctly uses `st.expander` for progressive disclosure.

**New issues found: D-050** (see below)

---

## New Design Issues

### D-049: C85 Score Cards and Category Breakdown Use Inline HTML
- **Severity**: P2
- **Added**: 2026-06-12
- **Source**: Design Review Round 18
- **Description**: The Financial Wellness results page uses inline HTML for the 3 score cards (total score, rating, category summary at lines 117-156) and the category breakdown grid (lines 202-212). These should use `_summary_card()` / `_info_card()` or a new `_score_card()` component. The inline HTML duplicates the card styling pattern (`background:#F8F9FA`, `border-radius:12px`, `border-left:4px solid`) that's already in `_info_card()`.
- **Affected Files**: `financial_wellness.py` lines 117-156, 202-212
- **Proposed Fix**: Create a `_score_card(title, value, subtitle, color)` helper in `_router_base.py` or `_helpers.py`. Replace all 4 inline HTML blocks.
- **Effort**: 1h

### D-050: C02 Notification Settings Uses st.expander Instead of _section_header()
- **Severity**: P2
- **Added**: 2026-06-12
- **Source**: Design Review Round 18
- **Description**: The notification settings panel at line 198 uses raw `st.expander("展開通知偏好設定", expanded=False)` instead of the `_section_header(icon, title, collapsed=True)` helper from `_helpers.py`. This means the expander label doesn't follow the standardized icon + title format used everywhere else.
- **Affected Files**: `notification_center.py` line 198
- **Proposed Fix**: Replace with `with _section_header("⚙️", "通知設定", collapsed=True):` (the `_section_title` call at line 194 should be removed since `_section_header` renders it).
- **Effort**: <0.5h

---

## Previously Identified Issues — Status Update

### Resolved in Sprint 6

| ID | Title | Resolution |
|----|-------|------------|
| **D-037** | `_白话_card` Uses Non-Standard Background Color | ✅ RESOLVED — `background:#F5F5F5` → `background:#F8F9FA` in `_router_base.py` line 91. Commit: b197764. |

### Still Open — P1 Issues

| ID | Title | Status |
|----|-------|--------|
| **D-003** | Inconsistent Card Styling | 🔴 Still open. Sprint 6 pages are clean, but `group_structure.py`, `watchlist_page.py`, `etf_detail.py`, `etf_browser.py`, `business_card.py` (C41, C44) still use inline HTML. Sprint 6 did not worsen this. |
| **D-005** | Business Card Page Overload | 🟡 Stable — see detailed assessment below. |
| **D-006** | Mobile Responsiveness Gaps | 🔴 Still open. No Sprint 6 changes affected mobile. |

### Still Open — P2 Issues (D-010 through D-048)

| ID | Title | Sprint 6 Impact |
|----|-------|-----------------|
| D-010 | Watchlist Page Uses Non-PPT Layout | No change |
| D-011 | Category Browser Uses Dense Tables | No change |
| D-012 | No Glossary/Tooltip System | No change |
| D-015 | No Structured Learning Path | No change |
| D-032 | No Progressive Disclosure for Business Card | No change |
| D-033 | No Standardized Empty State Component | No change |
| D-035 | C41 Peer Cards Use Inline HTML | No change |
| D-036 | C44 Risk Dimension Cards Use Non-Standard Background | No change |
| D-038 | C41 Calls API in View Layer | No change |
| D-039 | No Standardized Section Header Pattern | ✅ Partially mitigated — Sprint 6 pages all use `_section_title()` |
| D-040 | No Standardized Disclaimer Component | ✅ Partially mitigated — Sprint 6 pages all use `_historian_disclaimer()` |
| D-041 | No Sprint 5 Card Components | ✅ RESOLVED — `_study_card()`, `_expert_card()`, `_scenario_card()` now exist in `_helpers.py` and are used by C02 and C71/C73/C74 |
| D-042 | Health Dimension Mini-Cards Use Non-Standard Styling | No change |
| D-043 | Dividend History Table Uses Inline HTML | No change |
| D-044 | C41 Read Next Header Doesn't Use _section_title() | No change |
| D-045 | C51 Sector Grid Uses Inline HTML | No change |
| D-046 | C51 4th KPI Card Uses Inline HTML | No change |
| D-047 | C53-1 Share Section Header Doesn't Use _section_title() | No change |
| D-048 | C53-1 Share Button Uses st.html() with Non-Functional JS | No change |

---

## D-005 Assessment: Business Card Page Overload

### Current Section Count

The business card page (`_main.py` lines 76-95) now renders **19 sections**:

| # | Section | Collapsed? | Source |
|---|---------|------------|--------|
| 1 | Header (`_render_header`) | No | Core |
| 2 | Story Card (`_render_story_card`) | No | C48 |
| 3 | Key Takeaways (`_render_takeaways`) | No | C37 |
| 4 | Recent Deltas (`_render_deltas`) | No | C39 |
| 5 | Health Snowflake (`_render_health`) | No | C43 |
| 6 | Risk Analysis (`_render_risk`) | **Yes** (expander) | C44 |
| 7 | One-Liner (`_render_one_liner`) | No | Core |
| 8 | Key Metrics (`_render_key_metrics`) | No | Core |
| 9 | Dividend (`_render_dividend`) | No | Core |
| 10 | Revenue Breakdown (`_render_revenue_breakdown`) | No | Core |
| 11 | Revenue Trend (`_render_revenue_trend`) | No | Core |
| 12 | Valuation (`_render_valuation`) | No | C45 |
| 13 | Compare Stories (`_render_compare_stories`) | No | C38 |
| 14 | News (`_render_news`) | No | Core |
| 15 | Study Log (`_render_study_log`) | No | C71 |
| 16 | Expert Analysis (`_render_expert_analysis`) | No | C73 |
| 17 | Historical Scenarios (`_render_historical_scenarios`) | **Yes** (expander) | C74 |
| 18 | Read Next (`_render_read_next`) | No | C41 |
| 19 | Share Section (`_render_share_section`) | No | C53-1 |

### Progressive Disclosure Analysis

**Working well:**
- C44 Risk Analysis uses `st.expander` (collapsed by default) ✅
- C74 Historical Scenarios uses `_section_header(collapsed=True)` ✅

**Problem:**
- Only 2 of 19 sections are collapsed by default
- Sections 15-17 (Study Log, Expert Analysis, Historical Scenarios) are Sprint 5 additions that push content far below the fold
- Expert Analysis (C73) is NOT collapsed — it should be, since it only has content for 10 stocks
- Study Log (C71) is NOT collapsed — it's a personal tracking feature that most users don't need to see immediately

### Recommendation

Apply progressive disclosure to:
1. **C71 Study Log** → collapse by default (personal utility, not core analysis)
2. **C73 Expert Analysis** → collapse by default (only relevant for 10 stocks)
3. **C38 Compare Stories** → collapse by default (supplementary context)
4. **C41 Read Next** → collapse by default (discovery, not analysis)

This would leave 14 sections visible by default and 5 collapsed, which is still a lot but more manageable.

### D-005 Verdict: STABLE — Not worsened by Sprint 6

Sprint 6 did not add any sections to the business card page. The overload is from Sprints 2-5. The progressive disclosure pattern (proven by C44 and C74) needs to be extended to C71, C73, C38, and C41.

---

## Design Grade Recommendation

### Grade: A (maintained)

**Rationale:**
- Sprint 6 pages are the **cleanest new additions** in the project
- All three pages use shared card components and standardized helpers
- D-037 (card background color) was resolved
- D-041 (Sprint 5 card components) was resolved — `_study_card()`, `_exponent_card()`, `_scenario_card()` now exist
- Only 2 new P2 issues found (D-049, D-050), both minor
- No new P0 or P1 issues
- The overall design trajectory is positive

**Grade trajectory**: A for 9 consecutive rounds (Rounds 10-18).

---

## Priority Fixes Before Sprint 7

### Must Fix (P1)

1. **D-003**: Inconsistent Card Styling — Replace inline HTML cards in `group_structure.py`, `watchlist_page.py`, `etf_detail.py`, `etf_browser.py`, and `business_card.py` (C41, C44) with shared components. **Effort: 2-3h**

2. **D-005**: Business Card Page Overload — Apply progressive disclosure to C71, C73, C38, C41. **Effort: 1h**

### Should Fix (P2)

3. **D-049**: C85 Score Cards Use Inline HTML — Create `_score_card()` helper. **Effort: 1h**

4. **D-050**: C02 Settings Uses Raw st.expander — Replace with `_section_header()`. **Effort: <0.5h**

5. **D-033**: No Standardized Empty State Component — Create `_empty_state()` in `_router_base.py`. **Effort: 1h**

6. **D-039**: Standardize remaining raw `st.markdown("### ...")` calls in business card sections. **Effort: 1h**

---

## PPT-Style Compliance Summary

| Feature | PPT Score | Key Strength | Key Weakness |
|---------|-----------|--------------|--------------|
| C83 Investment Memo | **A+** | Perfect card-per-memo pattern. Zero inline HTML. | None. |
| C85 Financial Wellness | **B+** | Clean quiz flow. Good use of `_summary_card()` for interpretation. | Inline HTML for score cards and category breakdown. |
| C02 Notification Center | **A** | Severity-based card selection. Clean progressive disclosure. | Raw `st.expander` instead of `_section_header()`. |

---

## Statistics

- **Total Issues**: 37 (35 previous + 2 new: D-049, D-050)
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006)
- **P2 (Optimization)**: 24 (D-007, D-008, D-009, D-010, D-011, D-012, D-015, D-032, D-033, D-035, D-036, D-038, D-039, D-040, D-042, D-043, D-044, D-045, D-046, D-047, D-048, D-049, D-050)
- **Resolved**: 21 (19 previous + D-037 + D-041)

---

*This file is maintained by the Design Reviewer. Next update: After Sprint 7 feature implementation.*
