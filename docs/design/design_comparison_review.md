# Stock Explorer Design Review Report — Design Comparison

> Reviewer: Design Reviewer sub-agent
> Date: 2026-06-11 (Round 3)
> Scope: Design system compliance re-audit, verification of Round 2 findings, competitor comparison
> Previous reviews: docs/design/design_review.md (Round 1, 2026-06-08), docs/design/design_comparison_review.md (Round 2, 2026-06-10)

---

## I. Competitor Design Comparison

### Methodology
Reviewed the design patterns, UX choices, and visual hierarchy of major stock information platforms including Simply Wall St and Investopedia (new in Round 3) alongside the previous five competitors.

### 1. Simply Wall St (simplywall.st)
**Design Approach**: Visual-first stock analysis with "Snowflake" infographic scoring.
- **Strengths**:
  - The "Snowflake" visualization is iconic — 6-axis radial chart that instantly communicates company health
  - Exceptional use of color: each axis has its own color, making the snowflake intuitive
  - Large, readable typography with clear hierarchy
  - "Story" concept: every stock has a narrative summary above the data
  - Responsive design works flawlessly on mobile
- **What they do better**:
  - Visual summary is superior — the snowflake gives instant context that tables can't
  - Color system is richer but still consistent (6 pastel colors for 6 axes)
  - Story-driven approach makes data memorable
- **What Stock Explorer does better**:
  - Stock Explorer's text analogies are more accessible for absolute beginners
  - Focus on Taiwanese market data with local context
  - Event dashboard is a unique feature Simply Wall St doesn't offer

### 2. Investopedia (investopedia.com)
**Design Approach**: Educational-first financial reference for beginners.
- **Strengths**:
  - Every financial concept has a "plain English" definition alongside technical jargon
  - Progressive complexity: simple summary → detailed article → expert analysis
  - Consistent visual language: green/red for gains/losses, blue for interactive elements
  - Excellent use of "Did You Know" callout boxes — similar to Stock Explorer's 白話_card pattern
  - Consistent font scale (14/16/20/28px system) — Stock Explorer's sizes are ad-hoc
- **What they do better**:
  - Content hierarchy is crystal clear: title → one-line summary → visual → details
  - Every chart has a takeaway sentence, not just data
- **What Stock Explorer does better**:
  - Stock Explorer is stock-specific (real data), Investopedia is concept-specific
  - Watchlist integration with alerts is more practical

### 3–7. statementdog / goodinfo / cmoney / wantgoo / Yahoo Finance
(See Round 2 report for full analysis — findings unchanged.)

### Key Takeaways for Stock Explorer

| Area | Best Practice (from competitors) | Stock Explorer Gap | Priority |
|------|----------------------------------|--------------------|----------|
| **Page completeness** | All competitors have fully-rendered pages | business_card.py is truncated (128 lines) — missing main content | **P0** |
| **Card consistency** | statementdog/cmoney use identical card templates everywhere | Cards vary across pages (inline HTML vs `_白话_card` vs custom) | **P1** |
| **Visual summary** | Simply Wall St's snowflake gives instant context | Financial Health page has only 1 chart — no visual summary | **P1** |
| **Empty states** | cmoney uses illustrations + CTAs | Stock Explorer uses plain `st.info()` — functional but bland | **P2** |
| **Comparison UI** | goodinfo's heatmaps are very effective | Stock Explorer's radar chart is novel but less intuitive | **P1** |
| **Mobile responsive** | All competitors handle mobile well | Stock Explorer has basic media queries but column layouts break | **P1** |
| **Color consistency** | All competitors use consistent semantic colors | Stock Explorer has color violations across 4+ UI files | **P1** |
| **Typography scale** | Yahoo/Investopedia use clear type scale | Stock Explorer's type sizes are inconsistent across pages | **P2** |

---

## II. Design System Compliance Audit — Per Page (Round 3)

### Grading Scale
- **A**: Fully compliant — PPT style, zone separation, color system, text limits
- **B**: Minor issues — mostly compliant, small deviations
- **C**: Moderate issues — several violations that affect UX
- **D**: Major issues — fundamental design system violations
- **F**: Critical — page is broken or unusable

---

### 2.1 business_card.py — Company Business Card

**PPT Style Grade: D+ (DOWNGRADED from B+)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ❌ Violation | Watchlist buttons in header mix Zone A with interactive controls |
| Color system | ✅ Compliant | Uses standard colors correctly |
| Text limits | ❌ Cannot Assess | File truncated at line 128 — revenue/news/dividend sections are imported but NEVER rendered |
| Chart proportion | ❌ Missing | NO charts are rendered despite importing `create_revenue_trend_chart` and `create_revenue_pie_chart` |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | Router handles `data is None` case |
| Button keys | ✅ Yes | Unique key format |
| Responsive | ❌ Partial | `st.columns([3, 1, 1])` — no responsive fallback |
| Page completeness | 🔴 CRITICAL | File imports revenue/news/dividend services but never calls them |

**Issues**:
- **D-001**: Watchlist buttons in navbar violate Zone A purity (lines 56-72)
- **D-002-NEW (P0)**: Page is severely incomplete — only 128 lines. Revenue chart, pie chart, news, dividend sections are imported but never rendered. This is the MAIN page of the app.

---

### 2.2 operation_checkup.py — Operational Checkup

**PPT Style Grade: B- (DOWNGRADED from B)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean separation |
| Color system | ⚠️ Partial | Standard colors OK, but gradient card is non-standard |
| Text limits | ⚠️ Exceeds | Trend messages (lines 62-69) + info cards add substantial text |
| Chart proportion | ✅ Good | 3 charts dominate the page |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | `st.info()` for missing data |
| Button keys | N/A | No buttons |
| Responsive | ⚠️ Partial | No responsive fallback |
| Section titles | ⚠️ Issue | `_section_title()` always prepends `📊` emoji — causes double-emoji on some sections |

**Issues**:
- **D-003**: Text volume likely exceeds 200-char limit
- **D-004**: Custom gradient card (lines 135-175) uses non-standard `linear-gradient`
- **D-005-NEW**: `_section_title()` auto-prepends `📊` causing redundancy with 🩺 營運摘要

---

### 2.3 financial_health.py — Financial Health

**PPT Style Grade: C+ (UNCHANGED — still worst page)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ❌ Violation | `#F39C12` (orange) at line 180 — NOT in design system |
| Text limits | ❌ Exceeds | Well over 200 chars across 4 sections |
| Chart proportion | ❌ Low | Only 1 funnel chart for 4 sections — below 60% |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | `st.info()` for all missing data cases |
| Button keys | N/A | No buttons |
| Responsive | ⚠️ Partial | `st.columns(3)` — no responsive fallback |
| Component consistency | ⚠️ Issue | Custom HTML card at lines 188-196 doesn't use shared components |

**Issues**:
- **D-006**: Color violation — `#F39C12` (orange) at line 180
- **D-007**: Text volume significantly exceeds 200-char limit
- **D-008**: Chart proportion below 60%
- **D-009**: Custom health card (lines 188-196) breaks component consistency

---

### 2.4 peer_comparison.py — Peer Comparison

**PPT Style Grade: B+ (UNCHANGED — D-012 fixed)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Uses standard colors |
| Text limits | ⚠️ Borderline | Analysis text could be lengthy with all metrics |
| Chart proportion | ✅ Good | Table + radar chart balance |
| Loading states | ✅ Yes | Multiple spinners |
| Error handling | ✅ Yes | Graceful fallback to single view |
| Architecture | ✅ Fixed | `@st.cache_data` removed from view layer |
| Responsive | ⚠️ Partial | Table may overflow |

**Issues**:
- **D-010**: Analysis text could reach 400+ chars with all metrics
- **D-011**: Uses `st.metric()` instead of `_白话_card()`
- **D-012**: ✅ **FIXED** — `@st.cache_data` removed

---

### 2.5 etf_browser.py — ETF Browser

**PPT Style Grade: B- (DOWNGRADED from B)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ❌ Violation | `#2E86C1`, `#1B4F72`, `#8E44AD` — none in design system |
| Text limits | ✅ Good | Concise |
| Chart proportion | N/A | List-based page |
| Loading states | ✅ Yes | Multiple spinners |
| Error handling | ✅ Yes | Try/except throughout |
| Architecture | ✅ Fixed | `@st.cache_data` removed |
| Responsive | ❌ Issue | 6-column layout breaks on narrow screens |

**Issues**:
- **D-013**: Color violations at lines 67, 68, 442
- **D-014**: Button key collision risk across sections
- **D-015**: 6-column layout (lines 160, 432) breaks on narrow screens
- **D-016**: ✅ **FIXED** — `@st.cache_data` removed, replaced with module-level cache functions

---

### 2.6 etf_detail.py — ETF Detail

**PPT Style Grade: B+ (UNCHANGED)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Acceptable | `#7D6608` judged acceptable for disclaimer |
| Text limits | ✅ Good | Concise sections |
| Chart proportion | ✅ Good | Price + institutional charts |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | Try/except throughout |
| Responsive | ✅ Acceptable | `st.columns(2)` — acceptable |

**Issues**:
- **D-017**: ✅ Acceptable — `#7D6608` on `#FEF9E7` background for disclaimer
- **D-018**: Hardcoded fee values should be labeled as estimates

---

### 2.7 event_dashboard.py — Event Dashboard

**PPT Style Grade: B+ (DOWNGRADED from A-)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Standard colors |
| Text limits | ✅ Good | Concise |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | Handles empty events |
| Button keys | ✅ Fixed | `f"evt_{evt_idx}"` pattern |
| Responsive | ✅ Good | Simple list layout |
| Component consistency | ⚠️ Issue | Custom gradient banner (lines 141-152) not in design system |

**Issues**:
- **D-022**: Emoji-only severity badges without text alternatives
- **D-023**: Static markdown table takes space
- **D-027-NEW**: `_render_adaptive_banner` uses `linear-gradient` inline HTML (lines 141-152) — not in design system

---

### 2.8 watchlist_page.py — Watchlist

**PPT Style Grade: B- (DOWNGRADED from B)**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ❌ Violation | `#2E86C1`, `#1B4F72` in empty state card |
| Text limits | ✅ Good | Concise |
| Loading states | ✅ Yes | Spinner for price loading |
| Error handling | ✅ Yes | Try/except throughout |
| Button keys | ✅ Good | Unique key format |
| Responsive | ⚠️ Partial | Flexbox cards may break on narrow screens |
| Component consistency | ⚠️ Issue | Raw flexbox HTML + inline HTML summary cards |

**Issues**:
- **D-024**: Color violations at lines 123-124
- **D-025**: Raw flexbox HTML instead of shared components
- **D-026**: Alert popover takes up significant screen space
- **D-028-NEW**: Summary cards (lines 84-114) use inline HTML with hardcoded colors

---

## III. Color System Violation Summary

### UI-Level Violations (page files)

| File | Line | Illegal Color | Should Be | Notes |
|------|------|---------------|-----------|-------|
| `financial_health.py` | 180 | `#F39C12` (orange) | `#3498DB` (blue for neutral) | D-006 — unchanged |
| `etf_browser.py` | 67 | `#2E86C1` (dark blue) | `#3498DB` (primary blue) | D-013a — unchanged |
| `etf_browser.py` | 68 | `#1B4F72` (navy) | `#2C3E50` (primary text) | D-013b — unchanged |
| `etf_browser.py` | 442 | `#8E44AD` (purple) | `#2C3E50` or `#3498DB` | D-013c — unchanged |
| `watchlist_page.py` | 123 | `#2E86C1` (dark blue) | `#3498DB` (primary blue) | D-024a — unchanged |
| `watchlist_page.py` | 124 | `#1B4F72` (navy) | `#2C3E50` (primary text) | D-024b — unchanged |
| `etf_detail.py` | 307 | `#7D6608` (dark gold) | Acceptable | Judged acceptable for disclaimer on `#FEF9E7` bg |

### Chart-Level Violations (chart.py)

| Line | Illegal Color | Should Be | Notes |
|------|---------------|-----------|-------|
| 150 | `#4A90D9` | `#3498DB` | Revenue bar chart — close but not exact |
| 159 | `#2ECC71` | `#27AE60` | YoY positive color |
| 204 | `#F39C12`, `#2ECC71` | `#3498DB`, `#27AE60` | OHLC colors — non-standard |
| 251 | `#2ECC71` | `#27AE60` | Candlestick decreasing color |
| 315 | `#2ECC71`, `#F39C12` | `#27AE60`, `#3498DB` | Funnel chart colors |

### Gradient/Background Violations (not in design system)

| File | Lines | Issue |
|------|-------|-------|
| `operation_checkup.py` | 136, 169 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — custom gradient |
| `etf_browser.py` | 61 | `linear-gradient(135deg,#EBF5FB,#EAF2F8)` — custom gradient |
| `event_dashboard.py` | 141 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — custom gradient |
| `watchlist_page.py` | 122 | `linear-gradient(135deg,#EBF5FB,#EAF2F8)` — custom gradient |
| `etf_detail.py` | 110 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — custom gradient |

---

## IV. Responsive Design Audit

**Status**: P2-2 was marked as "Implemented" in pending_review.md (2026-06-09).

**What was done**:
- Navbar changed from 9-button row to `st.radio(horizontal=True)` — wraps to dropdown on narrow screens ✅
- CSS media queries added in `main.py` (lines 58-68) for padding adjustments at 768px and 600px ✅

**What's still missing**:
- **Column layouts**: Many pages use `st.columns([0.5, 0.8, 1.5, 1.2, 1.2, 0.8])` (6-column) with no responsive fallback. Streamlit's columns don't auto-wrap.
- **Card grids**: Various pages use `st.columns(cols_per_row)` with `cols_per_row = 2-3` — no responsive adjustment.
- **Table overflow**: `st.dataframe()` will overflow on narrow screens.
- **No testing evidence**: No screenshots or test results at 375/768/1024/1440px breakpoints.

**Grade**: P2-2 is **partially fixed**. The navbar issue is resolved, but column-based layouts throughout the app still break on narrow screens.

---

## V. Accessibility Audit

| Issue | Location | Severity | WCAG Guideline |
|-------|----------|----------|----------------|
| Color-only severity indicators | `event_dashboard.py` lines 21-26 | Medium | 1.4.1 Use of Color |
| Emoji-only badges without text | `event_dashboard.py` lines 21-26, 31-38 | Medium | 1.1.1 Non-text Content |
| Hidden label on industry radio | `category_browser.py` line 141 | High | 1.3.1 Info and Relationships |
| Low contrast on `#7F8C8D` text on `#F8F9FA` bg | All `_白话_card` labels | Low | 1.4.3 Contrast — ratio 4.6:1, passes AA |
| No focus indicators on custom HTML cards | All pages | Low | 2.4.7 Focus Visible |

---

## VI. Round 2 → Round 3 Issue Verification Summary

| ID | Issue | Status | Notes |
|----|-------|--------|-------|
| D-001 | business_card.py Zone A violation | ❌ STILL PRESENT | Watchlist buttons in navbar |
| D-002 | business_card.py truncated | 🔴 WORSENED | Only 128 lines, revenue/news/dividend never rendered |
| D-003 | operation_checkup.py text exceeds limit | ❌ STILL PRESENT | Trend messages + info cards |
| D-004 | operation_checkup.py gradient card | ❌ STILL PRESENT | Non-standard linear-gradient |
| D-006 | financial_health.py `#F39C12` | ❌ STILL PRESENT | Orange not in design system |
| D-007 | financial_health.py text-heavy | ❌ STILL PRESENT | Significantly exceeds 200 chars |
| D-008 | financial_health.py low chart ratio | ❌ STILL PRESENT | Only 1 chart for 4 sections |
| D-009 | financial_health.py custom card | ❌ STILL PRESENT | Lines 188-196 |
| D-010 | peer_comparison.py text borderline | ❌ STILL PRESENT | Could reach 400+ chars |
| D-011 | peer_comparison.py `st.metric()` usage | ❌ STILL PRESENT | Line 92 |
| **D-012** | **peer_comparison.py `@st.cache_data`** | ✅ **FIXED** | **Removed from view layer** |
| D-013 | etf_browser.py color violations | ❌ STILL PRESENT | Lines 67, 68, 442 |
| D-014 | etf_browser.py button key risk | ❌ STILL PRESENT | Cross-section collision risk |
| D-015 | etf_browser.py 6-column layout | ❌ STILL PRESENT | Lines 160, 432 |
| **D-016** | **etf_browser.py `@st.cache_data`** | ✅ **FIXED** | **Replaced with module-level functions** |
| D-017 | etf_detail.py disclaimer color | ✅ ACCEPTABLE | Judged acceptable in Round 2 |
| D-018 | etf_detail.py hardcoded fees | ❌ STILL PRESENT | Lines 270-281 |
| D-022 | event_dashboard.py emoji badges | ❌ STILL PRESENT | No text alternatives |
| D-024 | watchlist_page.py color violations | ❌ STILL PRESENT | Lines 123-124 |
| D-025 | watchlist_page.py custom flexbox | ❌ STILL PRESENT | Lines 204-224 |

**Fixes since Round 2**: 2 fixed (D-012, D-016 — architecture violations). 19 still present. 0 improved.

**New findings in Round 3**:
- D-002-NEW (P0): business_card.py severely incomplete
- D-005-NEW: `_section_title()` emoji prefix conflict
- D-027-NEW: event_dashboard.py custom gradient banner
- D-028-NEW: watchlist_page.py inline HTML summary cards

---

## VII. Design Improvement Suggestions

### P0 — Critical (Blocks MVP quality)

1. **Complete business_card.py** — The page is truncated at 128 lines. Revenue chart, revenue pie chart, news, and dividend sections are imported but never rendered. This is the MAIN page of the app. Need to restore/render the full page content.

### P1 — Important (Affects UX quality)

2. **Fix color system violations** — Replace all illegal colors with design system palette. Affects 4 UI files + chart.py:
   - `financial_health.py:180` — `#F39C12` → `#3498DB`
   - `etf_browser.py:67,68,442` — `#2E86C1,#1B4F72,#8E44AD` → `#3498DB,#2C3E50,#2C3E50`
   - `watchlist_page.py:123,124` — `#2E86C1,#1B4F72` → `#3498DB,#2C3E50`
   - `chart.py` — `#4A90D9` → `#3498DB`, `#2ECC71` → `#27AE60`

3. **Remove custom gradients** — Replace all `linear-gradient(135deg,#EBF5FB,#D4E6F1)` cards with standard `#F8F9FA` background. Affects 5 files.

4. **Standardize card components** → All pages should use `_白话_card()` and `_info_card()` from `_router_base.py`. Custom cards should be extracted to shared components.

5. **Reduce text on financial_health.py** — Consolidate to 2-3 sections or make explanations collapsible. Target: < 200 chars of body text.

6. **Fix `_section_title()` emoji prefix** — The function auto-prepends `📊` which conflicts with pages that already have custom emoji prefixes. Either remove the auto-prefix or make it optional.

### P2 — Nice to Have (Polish)

7. **Improve empty states** — Add more helpful CTAs to empty watchlist, empty events, etc.

8. **Standardize typography scale** — Define a global type scale instead of ad-hoc sizes.

9. **Add text alternatives to severity badges** — `event_dashboard.py` should include text labels alongside emoji.

10. **Responsive column layouts** — Replace fixed `st.columns()` with responsive patterns.

---

## VIII. Overall PPT Style Adherence Grades

| Page | Grade | Change | Primary Issues |
|------|-------|--------|----------------|
| Business Card | D+ | ⬇️ B+ → D+ | Page truncated/incomplete |
| Operation Checkup | B- | ⬇️ B → B- | Text exceeds limit, gradient card, section title emoji |
| Financial Health | C+ | → unchanged | Color violation, text-heavy, low chart ratio |
| Peer Comparison | B+ | → unchanged | Text borderline, `st.metric()` usage |
| ETF Browser | B- | ⬇️ B → B- | Color violations, wide columns |
| ETF Detail | B+ | → unchanged | Minor color issue, hardcoded fees |
| Event Dashboard | B+ | ⬇️ A- → B+ | Accessibility, new gradient banner issue |
| Watchlist | B- | ⬇️ B → B- | Color violations, custom card HTML |

**Overall Design System Compliance: D+ (DOWNGRADED from B-)**

The app has good foundations in loading states, error handling, and zone separation. However:
1. **business_card.py is critically incomplete** (downgraded from B+ to D+)
2. **No design issues were fixed** between Round 2 and Round 3 (except 2 architecture violations)
3. **3 NEW issues** were found: section title emoji conflict, gradient banner on event dashboard, gradient banner on ETF detail page
4. **5 gradient violations** were found across the codebase (none in the design system)
5. **Chart colors still don't match** the design system palette

---

## IX. Specific CSS/Component Recommendations

### 9.1 Global Card Component (to replace inline HTML)

Create `src/pages/components.py`:
```python
def info_card(label: str, value: str, analogy: str = "", card_type: str = "info"):
    """Standardized card component.
    
    card_type: 'info' (blue), 'tip' (orange), 'warning' (yellow), 'success' (green)
    """
    styles = {
        "info":    {"bg": "#F8F9FA", "border": "#3498DB", "analogy_color": "#27AE60"},
        "tip":     {"bg": "#FFF8F0", "border": "#F39C12", "analogy_color": "#5D6D7E"},
        "warning": {"bg": "#FEF9E7", "border": "#F1C40F", "analogy_color": "#7D6608"},
        "success": {"bg": "#EAFAF1", "border": "#27AE60", "analogy_color": "#1E8449"},
    }
    s = styles.get(card_type, styles["info"])
    return f"""<div style="background:{s['bg']};border-radius:12px;padding:1.2rem;
        border-left:4px solid {s['border']};margin:0.5rem 0;">
        <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
        <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
        <div style="font-size:0.85rem;color:{s['analogy_color']};font-style:italic;margin-top:0.3rem;">{analogy}</div>
    </div>"""
```

### 9.2 Chart Color Standardization

In `src/services/chart.py`, replace all hardcoded colors:
```python
# Design system colors for charts
DS_BLUE = "#3498DB"
DS_GREEN = "#27AE60"
DS_RED = "#E74C3C"

# Replace:
# - "#4A90D9" → DS_BLUE
# - "#2ECC71" → DS_GREEN
# - "#F39C12" → DS_BLUE (for neutral/structural elements)
```

### 9.3 Remove Custom Gradients

Replace all `linear-gradient(135deg,#EBF5FB,#D4E6F1)` with standard `#F8F9FA` background in:
- `operation_checkup.py` (lines 136, 169)
- `etf_browser.py` (line 61)
- `event_dashboard.py` (line 141)
- `watchlist_page.py` (line 122)
- `etf_detail.py` (line 110)

---

*End of Design Review Report — Round 3*
