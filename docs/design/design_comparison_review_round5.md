# Design Comparison Review — Round 5

**Date:** 2026-06-12
**Reviewer:** Design Reviewer (automated)
**Scope:** Post-restoration review of business_card.py + design trend research + compliance audit

---

## I. Executive Summary

Round 5 was triggered by the P0 fix to `business_card.py` (restored from 128→370 lines). This round verifies that restoration, checks all pages against the design system, and brings in 2025-2026 design trend research to identify forward-looking improvements.

**Key Findings:**
- `business_card.py` is now fully restored (370 lines) — P0 issue D-002-NEW/D-029 is RESOLVED
- 17 new design issues found (D-046 through D-062)
- Overall grade improved from D+ to C- (business_card jumped from F to B)
- Chart color violations remain the most pervasive cross-cutting problem

---

## II. 2025-2026 Design Trend Research

### A. Mobile-First Financial Education UX

**What leading apps are doing in 2025-2026:**

1. **Progressive Disclosure** — Apps like Figma's financial templates, Revolut Junior, and Binance Academy use "layers" of information. Default view = one number + one sentence. Tap to expand. Stock Explorer's PPT-style One Key Point Per Page aligns well with this trend, BUT fails to implement progressive disclosure — most pages dump all content at once.

2. **Bottom-Sheet Detail Panels** — Mobile-first financial apps (Robinhood, eToro, Webull) use bottom sheets for secondary info instead of inline expansion. Stock Explorer's `st.expander` pattern is the Streamlit equivalent and is correctly used in several places.

3. **Micro-Animations & Skeleton Screens** 2025 trend: skeleton loading instead of spinners. Streamlit doesn't support skeleton screens natively, but `st.spinner` with descriptive text is the acceptable fallback. ✅ Stock Explorer does this well.

4. **Thumb-Friendly Tap Targets** — Minimum 44×44px touch targets. Streamlit `st.button` meets this. However, 6-column layouts in category_browser.py and etf_browser.py create tap targets that are too narrow on mobile (< 120px wide).

5. **Dark Mode Typography** — 2025 trend: using `rgba(255,255,255,0.87)` for primary text on dark backgrounds (Material Design 3). Stock Explorer uses `#555555` chart text which fails WCAG AA on dark backgrounds (~3.2:1 contrast ratio vs required 4.5:1).

### B. PPT-Style / Card-Based Dashboard Designs

**What's working in 2025:**

1. **"Snowflake" Layout** — One hero metric per card, max 4 cards per row on desktop, 1 on mobile. Stock Explorer's `_白话_card()` component is well-designed for this. The problem is INCONSISTENT usage across pages.

2. **Visual Hierarchy via Typography Scale** — Best-in-class dashboards use: 32-40px hero numbers, 16-18px labels, 12-14px secondary text. Stock Explorer uses `1.6rem` (~25.6px) for values — slightly small for PPT-style. Recommendation: increase to `2rem` (~32px).

3. **Generous Whitespace** — Top financial apps use 1.5-2rem padding inside cards. Stock Explorer uses `1.2rem` — acceptable but could be more spacious.

4. **Consistent Card Anatomy** — Every card should have: label (gray), value (bold dark), plain-language (green italic). Stock Explorer's `_白话_card()` in `_router_base.py` defines this correctly. The problem is pages that bypass it with raw HTML.

### C. Data Visualization Best Practices for Beginners (2025)

1. **Annotated Charts > Standalone Charts** — Best practice: annotate the "so what" directly on the chart, not below it. Stock Explorer uses separate `_info_card()` below charts for interpretation. Better approach: add annotation text directly on the Plotly figure.

2. **Color-Blind Safe Palettes** — 2025 standard: never rely on red/green alone. Add shape/pattern/icon differentiation. Stock Explorer uses red/green for up/down which is problematic for ~8% of males with deuteranopia.

3. **Limiting Chart Types for Beginners** — Beginners comprehend: bar > line > pie > radar > funnel. Stock Explorer uses funnel charts (hard) and radar charts (very hard) early. Consider simplifying.

4. **Horizontal Bar > Vertical Bar** for category comparison (easier label reading). Stock Explorer's group_structure.py uses vertical `st.bar_chart`.

### D. Color Systems for Financial Data (2025)

1. **Semantic Color Tokens** — 2025 trend: use `color-positive`, `color-negative`, `color-neutral`, `color-info` as tokens, NOT hardcoded hex. Stock Explorer's design system defines tokens but chart.py uses raw hex values.

2. **Accessible Red/Green** — Standard accessible red: `#D32F2F` (not `#E74C3C`). Accessible green: `#2E7D32` (not `#27AE60`). Stock Explorer's red/green choices are slightly too bright for WCAG AA.

3. **Neutral Grays** — Card backgrounds should use pure neutral grays, not blue-tinted grays. `#F8F9FA` is slightly blue-tinted. True neutral: `#F5F5F5`.

---

## III. Page-by-Page Compliance Check

### A. `business_card.py` (370 lines) — RESTORED ✅

**Grade: B** (up from F)

| System Area | Status | Notes |
|-------------|--------|-------|
| Zone Separation | ⚠️ Partial | Watchlist UI (lines 57-129) still in Zone A area (header row). D-001 and D-040 remain. |
| Color System | ✅ Pass | Uses `#F8F9FA`, `#3498DB`, `#27AE60`, `#2C3E50`, `#7F8C8D` — all in spec. |
| PPT Style | ⚠️ Partial | One-liner banner at line 136 uses `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — NOT in design system (NEW D-046). |
| Chart Proportion | ✅ Pass | Revenue pie chart + revenue trend chart = 2 charts, both Plotly, well-sized. |
| Typography | ✅ Pass | Uses `1.8rem` values (slightly overspec), `0.85rem` labels, `0.85rem` green italic. |
| Component Consistency | ⚠️ Partial | Lines 242-272: dividend mini-cards use raw HTML with `text-align:center` instead of `_白话_card()`. Lines 317-324: revenue breakdown items use custom HTML with `box-shadow` not in design system (NEW D-047). |
| Cards | ✅ Pass | Info cards at line 149+ use correct `#F8F9FA` + `border-left:4px solid #3498DB` pattern. |
| Error Handling | ✅ Pass | Has fallbacks for all metrics (`else` branches with `extra_metrics.get(...)` fallback chain). |
| Loading State | N/A | Handled by router. |

**Issues Resolved from Round 4:**
- ✅ D-002-NEW: Page truncation — RESOLVED (370 lines, all sections rendered)
- ✅ D-029: STILL severely truncated — RESOLVED

**New Issues Found:**
- D-046: One-liner banner uses illegal gradient background
- D-047: Revenue breakdown cards use `box-shadow` not in design system

---

### B. `financial_health.py` (248 lines)

**Grade: C+** (unchanged)

| System Area | Status | Notes |
|-------------|--------|-------|
| Color System | ❌ Fail | Line 180: `#F39C12` (orange) for moderate debt ratio — NOT in palette (D-006). Line 177: `health_color` uses 4 arbitrary colors inline. |
| PPT Style | ❌ Fail | Text exceeds 200 chars significantly. _info_card at lines 69-75 has ~280 chars. Cash flow section has 3 _info_card blocks totaling ~500 chars (D-036, D-037). |
| Chart Proportion | ❌ Fail | Only 1 chart (funnel) for 4 sections (D-008). |
| Component Consistency | ⚠️ Pass | Uses `_白话_card()` and `_info_card()` from shared components. ✅ |
| Zone Separation | ✅ Pass | Timeline selector at top of Zone C, clearly separated. |
| Typography | ⚠️ Partial | Debt ratio health card at lines 188-196 uses raw HTML with dynamic `health_color` instead of standardized `_info_card()` pattern (D-009). |

**Issues: D-006, D-008, D-009, D-036, D-037** (all previously identified, unchanged)

---

### C. `category_browser.py` (270 lines)

**Grade: D+** (up from D)

| System Area | Status | Notes |
|-------------|--------|-------|
| Color System | ✅ Pass | Industry stock cards use `#F8F9FA`, `#3498DB`, `#7F8C8D`, `#2C3E50` — in spec. Value column uses `#3498DB`. ✅ |
| Component Consistency | ❌ Fail | Lines 170-181: Stock cards in industry browser use raw HTML `<div>` with inline styles (NEW D-048). ETF category cards in etf_browser.py lines 302-321 (D-042, pre-existing). |
| Responsive Design | ❌ Fail | Lines 105, 241: 6-column layout `[0.6, 1, 1.2, 1.5, 1.2, 0.8]` — too narrow on mobile (D-019). |
| Accessibility | ❌ Fail | Line 141: `label_visibility="collapsed"` on industry radio — screen reader inaccessible (D-020). |
| PPT Style | ❌ Fail | Page has 3 sections (top stocks, industry browser, hot stocks) — no single core message. Violates "one key point per page" principle. |
| Card Pattern | ⚠️ Partial | Industry stock cards at lines 170-180 have correct colors but wrong anatomy: no green italic plain-language line (just stock_id + name + button). Missing the "plain-language translation" required by design system. |

**New Issues Found:**
- D-048: Industry stock cards use raw HTML instead of `_白话_card()`
- D-049: Page has 3 unrelated sections — violates PPT-style "one key point per page"

---

### D. `group_structure.py` (330 lines)

**Grade: D** (unchanged)

| System Area | Status | Notes |
|-------------|--------|-------|
| Color System | ❌ Fail | Line 239: `#F39C12` (orange) for "重要轉投資" badge (D-030). Line 202: `linear-gradient` not in design system (D-033). |
| PPT Style | ⚠️ Partial | Lines 326-330: Strategy `_info_card` text ~180 chars for closing sentence — borderline (D-038). Overall page text likely exceeds 200 chars when all sections render. |
| Component Consistency | ❌ Fail | 5 out of 6 cards are raw HTML. Zero usage of `_白话_card()` or `_info_card()`. Only the empty state uses `_info_card()`. |
| Zone Separation | ✅ Pass | Clean section separation with `_section_title()`. |
| Cards | ⚠️ Partial | Subsidiary cards at lines 244-265 have `background:white;border:1px solid #ECF0F1` — deviates from `#F8F9FA` card background in design system. NEW: `#ECF0F1` border color not in design system (NEW D-050). |
| Badges | ❌ Fail | Badge colors (lines 234-242): uses `#F39C12` for medium, emoji circles (🔴🟡🟢) without text alternatives. Missing aria-labels. |

**New Issues Found:**
- D-050: Subsidiary cards use `#ECF0F1` border color not in design system
- D-051: Group overview card uses `border-radius:16px` — design system specifies `12px`
- D-052: Page uses `st.bar_chart` (Streamlit native) instead of Plotly chart — violates design system chart rules

---

### E. `event_dashboard.py` (172 lines)

**Grade: A-** (unchanged — best page)

| System Area | Status | Notes |
|-------------|--------|-------|
| Color System | ⚠️ Minor | Line 142: `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — not in design system (D-035/D-27). |
| PPT Style | ✅ Pass | Clean separation with expandable event list. One core message per section. |
| Component Consistency | ⚠️ Partial | Severity badges use emoji without text alternatives (D-022). Missing aria-labels. |
| Zone Separation | ✅ Pass | Well-structured with clear section headers. |
| Typography | ✅ Pass | Good hierarchy. |
| Error Handling | ✅ Pass | Graceful empty state with informative message. |

**Issues: D-022, D-035** (pre-existing, minor)

---

### F. Additional Pages Reviewed

#### `operation_checkup.py` (175 lines) — Grade: C

| Issue | Details |
|-------|---------|
| Colors | Lines 136, 169: `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` (D-027 pattern) |
| PPT Style | Lines 62-70: Trend messages ~100 chars each — acceptable |
| Components | ✅ Uses `_白话_card()` and `_info_card()` consistently |
| Charts | 3 charts (revenue, price, institutional) — good proportion |

#### `peer_comparison.py` (420 lines) — Grade: C+

| Issue | Details |
|-------|---------|
| Colors | ✅ No violations found |
| PPT Style | Lines 333-367: Metric analysis text could reach 400+ chars (D-010) |
| Components | Line 92: Uses `st.metric()` in single-company view instead of `_白话_card()` (D-034) |
| Charts | 2 charts (comparison table + radar) — acceptable |

#### `watchlist_page.py` (333 lines) — Grade: C

| Issue | Details |
|-------|---------|
| Colors | Lines 123-124: `#2E86C1` (dark blue), `#1B4F72` (navy) in empty state (D-024). Lines 97, 108: hardcoded border colors in summary cards (D-028). |
| PPT Style | Lines 157-226: Page is entirely list-oriented, no chart (D-039) |
| Components | Lines 84-114: Summary cards use raw HTML with hardcoded colors (D-028). Lines 204-224: Watchlist item cards use raw flexbox HTML (D-025). |

#### `etf_browser.py` (458 lines) — Grade: D+

| Issue | Details |
|-------|---------|
| Colors | Line 61: `linear-gradient(135deg,#EBF5FB,#EAF2F8)` with `#2E86C1` border (D-013). Line 442: `#8E44AD` (purple) for dividend yield (D-013). |
| Components | Lines 302-321: ETF category cards use raw HTML (D-042). Lines 59-119: ETF explainer card uses custom gradient (D-043). |
| Responsive | Lines 160, 432: 5-6 column layouts break on narrow screens. |

---

## IV. NEW Design Issues (D-046 through D-062)

### D-046 — business_card.py One-Liner Banner Uses Illegal Gradient
- **File:** `business_card.py`
- **Line:** 136
- **Issue:** `background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — gradients are NOT allowed in the design system (Section 3.1 specifies flat colors only)
- **Should be:** `background:#EBF5FB` (flat background matching the "light gray" palette) OR simply omit the background since `#F8F9FA` is the standard card background
- **Severity:** Medium
- **Fix:** Replace the gradient with a flat `#EBF5FA` or the standard `#F8F9FA` card background

### D-047 — business_card.py Revenue Breakdown Cards Use Non-Standard Styling
- **File:** `business_card.py`
- **Lines:** 317-324
- **Issue:** Revenue breakdown item cards use `background:white`, `border-radius:10px`, `border-left:4px solid #3498DB`, `box-shadow:0 1px 3px rgba(0,0,0,0.05)` — `box-shadow` is NOT in the design system component spec (Section 3.3)
- **Should be:** Match the `_info_card()` or `_白话_card()` pattern exactly
- **Severity:** Low

### D-048 — category_browser.py Industry Stock Cards Use Raw HTML
- **File:** `category_browser.py`
- **Lines:** 170-181
- **Issue:** Stock cards in the industry browser section use raw HTML `<div>` with inline styles instead of the shared `_白话_card()` component
- **Should be:** Use `_白话_card()` for consistency, or at minimum match the design system card anatomy exactly
- **Severity:** Medium

### D-049 — category_browser.py Violates PPT-Style "One Key Point Per Page"
- **File:** `category_browser.py`
- **Lines:** 38-49 (3 unrelated sections)
- **Issue:** Page contains 3 distinct sections (top stocks by value, industry browser, hot stocks by volume) — each answering a different question. Violates design system Section 5.1: "Each page answers only one question"
- **Should be:** Either split into 3 separate pages, or restructure around a single core question like "Which stocks are popular today?"
- **Severity:** High

### D-050 — group_structure.py Subsidiary Cards Use Non-Standard Border Color
- **File:** `group_structure.py`
- **Lines:** 244-265
- **Issue:** Subsidiary cards use `border:1px solid #ECF0F1` — `#ECF0F1` is NOT in the design system color palette (Section 3.1)
- **Should be:** Use `border-left:4px solid #3498DB` with `background:#F8F9FA` to match the standard card pattern
- **Severity:** Low

### D-051 — group_structure.py Group Overview Card Uses Wrong Border Radius
- **File:** `group_structure.py`
- **Line:** 202
- **Issue:** `border-radius:16px` — design system Section 3.3 specifies `border-radius:12px` for all cards
- **Should be:** `border-radius:12px`
- **Severity:** Low

### D-052 — group_structure.py Uses Streamlit Native Chart Instead of Plotly
- **File:** `group_structure.py`
- **Line:** 283
- **Issue:** `st.bar_chart(chart_data.set_index("公司"), use_container_width=True)` — design system Section 3.4 states "Use Plotly (do not embed matplotlib directly)" and all charts should use the theme-aware `_apply_theme_layout()`. `st.bar_chart` is Streamlit's native chart which doesn't support the design system's color tokens or theme adaptation.
- **Should be:** Use Plotly `go.Bar` with design system colors and `_apply_theme_layout()`
- **Severity:** Medium

### D-053 — chart.py Funnel Chart Uses Non-Palette Colors
- **File:** `chart.py`
- **Line:** 315
- **Issue:** Funnel chart marker colors `["#3498DB", "#2ECC71", "#F39C12", "#E74C3C"]` — `#2ECC71` and `#F39C12` are NOT in the design system palette. Should be `#27AE60` and `#3498DB` (blue for info, not orange).
- **Should be:** `["#3498DB", "#27AE60", "#27AE60", "#E74C3C"]` or use blue tones only for non-directional data
- **Severity:** Medium

### D-054 — chart.py Revenue Trend Chart Uses Wrong Blue
- **File:** `chart.py`
- **Line:** 150
- **Issue:** `marker_color="#4A90D9"` — should be `#3498DB` per design system
- **Should be:** `marker_color="#3498DB"`
- **Severity:** Low (pre-existing, documented in Round 3 chart color table)

### D-055 — chart.py Revenue Trend YoY Uses Wrong Green
- **File:** `chart.py`
- **Line:** 159
- **Issue:** `"#2ECC71"` for positive YoY — should be `#27AE60`
- **Should be:** `"#27AE60"`
- **Severity:** Low (pre-existing, documented in Round 3 chart color table)

### D-056 — chart.py OHLC Single-Day Fallback Uses Non-Palette Colors
- **File:** `chart.py`
- **Line:** 204
- **Issue:** `ohlc_colors = ["#F39C12", "#2ECC71", "#E74C3C", "#3498DB"]` — `#F39C12` and `#2ECC71` are wrong
- **Should be:** `["#3498DB", "#27AE60", "#E74C3C", "#3498DB"]` (use blue for neutral OHLC, green for high, red for low)
- **Severity:** Medium

### D-057 — chart.py Candlestick Colors Are Reversed for Taiwanese Convention
- **File:** `chart.py`
- **Lines:** 250-251
- **Issue:** `increasing_line_color="#E74C3C"` (red=up), `decreasing_line_color="#2ECC71"` (green=down). While this follows Taiwanese market convention (red=up), the design system Section 3.1 states "Red/green only for price direction (up/down)" without specifying which is which. However, the institutional chart at line 257 uses the SAME convention (`#E74C3C` if close >= open), creating inconsistency with the revenue trend chart at line 159 where green = positive = good.
- **Recommendation:** Document the Taiwanese convention (紅漲綠跌) explicitly in the design system to resolve ambiguity
- **Severity:** Low (consistency/documentation issue)

### D-058 — chart.py Institutional Chart Uses Wrong Green
- **File:** `chart.py`
- **Line:** 401
- **Issue:** `"#2ECC71"` — should be `#27AE60`
- **Severity:** Low (pre-existing)

### D-059 — _router_base.py _info_card Uses Non-Palette Orange Border
- **File:** `_router_base.py`
- **Line:** 145
- **Issue:** `_info_card()` uses `border-left:4px solid #F39C12` — `#F39C12` (orange) is NOT in the design system color palette. Section 3.1 only defines: Blue `#3498DB`, Green `#27AE60`, Red `#E74C3C`, and background colors.
- **Should be:** `border-left:4px solid #3498DB` (use blue for info/tip cards, matching the info card spec in Section 3.3 which already shows `#3498DB` for info cards and `#F39C12` for tip cards — but `#F39C12` isn't in the palette)
- **Severity:** High (this is a SHARED component used by ALL pages)

### D-060 — main.py Welcome Page Uses Non-Standard Styling
- **File:** `main.py`
- **Lines:** 262-270
- **Issue:** Welcome page uses raw HTML with `text-align:center;padding:4rem 2rem` — no card structure, no design system colors for the container. Uses `#7F8C8D` and `#95A5A6` text colors (the latter is NOT in the design system palette).
- **Should be:** Use a centered card with `#F8F9FA` background and design system typography
- **Severity:** Low

### D-061 — main.py CSS Uses Non-Standard Colors
- **File:** `main.py`
- **Lines:** 49-56
- **Issue:** `.disclaimer` class uses `#FEF9E7` background (in palette ✅) but `#7D6608` text color — NOT in design system palette. Also `#F9E79F` border color — NOT in palette.
- **Should be:** Use `#2C3E50` for text (primary text color) and `#F1C40F` → replace with `#3498DB` border or remove border
- **Severity:** Low

### D-062 — Global: No CSS Custom Properties (Design Tokens)
- **File:** `main.py` (CSS section)
- **Lines:** 27-98
- **Issue:** All CSS values are hardcoded hex/rgba. Modern 2025 best practice is CSS custom properties (`:root { --color-primary: #3498DB; }`) for design tokens. This makes it impossible to implement dark mode switching or theme consistency.
- **Should be:** Define CSS custom properties in `:root` for all design system colors, then reference `var(--color-primary)` throughout
- **Severity:** Medium (architectural improvement)

---

## V. Design Improvement Recommendations

### Priority 1: Fix Shared Component Color Violations (affects ALL pages)

**D-059 — `_info_card()` orange border:**
```python
# _router_base.py line 145 — CHANGE:
# FROM:
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;...">
# TO:
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;...">
```

### Priority 2: Fix Chart Color Palette (chart.py)

Create a centralized color constant:
```python
# chart.py — ADD at top:
DS_BLUE = "#3498DB"
DS_GREEN = "#27AE60"
DS_RED = "#E74C3C"
DS_BG_CARD = "#F8F9FA"
DS_TEXT_PRIMARY = "#2C3E50"
DS_TEXT_SECONDARY = "#7F8C8D"
```

Then replace all instances of `#4A90D9` → `DS_BLUE`, `#2ECC71` → `DS_GREEN`, `#F39C12` → `DS_BLUE` (for non-directional).

### Priority 3: Eliminate All Gradients (8 occurrences across 6 files)

Replace every `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` with flat `#EBF5FB`:
```html
<!-- FROM: -->
background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);
<!-- TO: -->
background:#EBF5FB;
```

Files to fix: `business_card.py`, `group_structure.py`, `event_dashboard.py`, `operation_checkup.py`, `etf_browser.py`, `watchlist_page.py`, `etf_detail.py`

### Priority 4: Standardize Card Components

**For pages using raw HTML cards, migrate to `_白话_card()`:**

```python
# category_browser.py lines 170-181 — REPLACE raw HTML with:
from src.pages._router_base import _白话_card
# In the loop:
with cols[j]:
    _白话_card(
        f"{row['stock_id']} {row.get('stock_name', '')}",
        "",
        "點擊查看公司名片"
    )
    if st.button("查看名片", key=f"ind_{row['stock_id']}", use_container_width=True):
        navigate_to(page="名片", stock_id=row["stock_id"])
```

### Priority 5: Responsive Design Fix

**Replace 6-column layouts with responsive alternatives:**

```python
# category_browser.py / etf_browser.py — FROM:
cols = st.columns([0.6, 1, 1.2, 1.5, 1.2, 0.8])
# TO (use 3 columns + button):
col1, col2, col3 = st.columns([2, 2, 1])
col1.markdown(f"**#{rank}** `{sid}` {name}")
col2.markdown(industry)
if col3.button("查看", key=f"val_{sid}", use_container_width=True):
    navigate_to(page="名片", stock_id=sid)
```

### Priority 6: Typography Scale Adjustment

**Increase hero value size for PPT-style impact:**

```python
# _router_base.py _白话_card — CHANGE:
# FROM: font-size:1.6rem
# TO:   font-size:2rem
<div style="font-size:2rem;font-weight:700;color:#2C3E50;">{value}</div>
```

### Priority 7: Add CSS Custom Properties

```css
/* main.py — REPLACE the <style> block with: */
:root {
  --color-primary: #3498DB;
  --color-positive: #27AE60;
  --color-negative: #E74C3C;
  --color-bg-card: #F8F9FA;
  --color-bg-warning: #FEF9E7;
  --color-bg-tip: #FFF8F0;
  --color-text-primary: #2C3E50;
  --color-text-secondary: #7F8C8D;
  --radius-card: 12px;
  --padding-card: 1.2rem;
}
```

---

## VI. Updated Page Grades

| Page | Round 4 Grade | Round 5 Grade | Change | Key Factor |
|------|--------------|---------------|--------|------------|
| business_card.py | F → D | **B** | ⬆⬆ | P0 fix restored all content |
| event_dashboard.py | A- | **A-** | — | Still the best page |
| operation_checkup.py | C | **C** | — | Minor gradient issue |
| peer_comparison.py | C+ | **C+** | — | Text volume issue remains |
| financial_health.py | C+ | **C+** | — | Multiple pre-existing issues |
| watchlist_page.py | C | **C** | — | Raw HTML cards, no chart |
| etf_browser.py | D+ | **D+** | — | Gradient + raw HTML cards |
| group_structure.py | D | **D** | — | Raw HTML, wrong colors, native chart |
| category_browser.py | D | **D+** | ⬆ | Slightly better on color compliance |
| etf_detail.py | C | **C** | — | Gradient + raw HTML cards |

**Overall Grade: C-** (up from D+)

**Grade Distribution:**
- A: 1 page (event_dashboard.py)
- B: 1 page (business_card.py)
- C: 5 pages (financial_health, peer_comparison, operation_checkup, watchlist_page, etf_detail)
- D: 3 pages (group_structure, category_browser, etf_browser)

---

## VII. Cumulative Issue Count

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 (2026-06-10) | 26 | 26 | 2 (D-012, D-016) |
| Round 3 (2026-06-11) | 3 new | 29 | 0 |
| Round 4 (2026-06-12) | 25 new | 54 | 0 |
| Round 5 (2026-06-12) | 17 new | 71 | 2 (D-002-NEW, D-029) |
| **Total** | **71** | **71** | **2** |

---

## VIII. Recommended Fix Priority

### Immediate (this week):
1. **D-059** — Fix `_info_card()` orange border in shared component (1 line, affects all pages)
2. **D-053-D-058** — Fix chart.py color constants (6 lines, affects all charts)
3. **D-046** — Remove gradient from business_card.py one-liner (1 line)

### Short-term (next 2 weeks):
4. **D-049** — Restructure category_browser.py into single-focus page
5. **D-052** — Replace `st.bar_chart` with Plotly in group_structure.py
6. **D-048** — Migrate raw HTML cards to `_白话_card()` in category_browser.py
7. **D-019** — Fix responsive 6-column layouts

### Medium-term (next month):
8. **D-062** — Implement CSS custom properties
9. **D-036/D-037** — Reduce text volume in financial_health.py
10. **D-010** — Reduce text volume in peer_comparison.py
11. **D-008** — Add charts to financial_health.py sections

---

*Review completed: 2026-06-12*
*Next review: Round 6 (scheduled after fixes are applied)*
