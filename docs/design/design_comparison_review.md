# Stock Explorer Design Review Report — Design Comparison

> Reviewer: Design Reviewer sub-agent
> Date: 2026-06-10 (Round 2)
> Scope: Design system compliance audit, competitor comparison, per-page PPT-style grading
> Previous review: docs/design/design_review.md (2026-06-08, Round 1)

---

## I. Competitor Design Comparison

### Methodology
Reviewed the design patterns, UX choices, and visual hierarchy of five major stock information platforms. Since these are external websites, observations are based on publicly known design patterns and general UX analysis.

### 1. statementdog.com (記帳狗 / Statement Dog)
**Design approach**: Clean, card-based dashboard focused on financial statements.
- **Strengths**:
  - Excellent use of whitespace — each metric gets its own card with clear visual separation
  - Consistent color coding: green for positive, red for negative throughout
  - Progressive disclosure: summary cards first, drill-down tables on click
  - Mobile-first responsive design with collapsible sections
- **What they do better than Stock Explorer**:
  - More consistent card component system (every metric follows the same card template)
  - Better mobile experience — cards stack cleanly, no horizontal overflow
  - Sticky header with search always accessible
- **What Stock Explorer does better**:
  - PPT-style one-concept-per-page is more beginner-friendly than statementdog's data-dense approach
  - Plain-language analogies (白話文) — statementdog has no equivalent
  - Watchlist with multi-list support is more flexible

### 2. goodinfo.tw
**Design approach**: Information-dense tables, power-user oriented.
- **Strengths**:
  - Extremely comprehensive data coverage — everything visible at a glance
  - Fast loading with server-side rendering
  - Excellent comparison tools (side-by-side tables)
  - Color-coded heatmaps for quick visual scanning
- **What they do better**:
  - Comparison tables are more feature-rich (sortable columns, inline charts)
  - Heatmap visualization for peer comparison is very effective
  - Breadcrumb navigation is clearer
- **What Stock Explorer does better**:
  - Goodinfo is overwhelming for beginners — Stock Explorer's PPT style is the right call
  - Stock Explorer's plain-language explanations have no equivalent on goodinfo
  - Better visual hierarchy — goodinfo shows everything equally, nothing stands out

### 3. cmoney.tw
**Design approach**: Community-driven with social features, modern card UI.
- **Strengths**:
  - Beautiful card-based layouts with rounded corners and subtle shadows
  - Excellent use of icons and visual metaphors
  - Strong community features (comments, ratings, shared watchlists)
  - Smooth animations and transitions
- **What they do better**:
  - More polished visual design — better use of gradients, shadows, micro-interactions
  - Social proof elements (how many people follow a stock)
  - Better empty states with illustrations and clear CTAs
- **What Stock Explorer does better**:
  - Stock Explorer's educational focus (analogies, plain-language) is unique
  - Cleaner information architecture — cmoney has feature creep
  - No social media noise — focused on learning

### 4. wantgoo.tradingview.com
**Design approach**: Professional charting with community overlays.
- **Strengths**:
  - Best-in-class charting (TradingView widgets)
  - Excellent technical indicator overlays
  - Strong community sentiment indicators
  - Professional-grade screening tools
- **What they do better**:
  - Chart quality is far superior — interactive, zoomable, with drawing tools
  - Screening/filtering is more powerful
  - Real-time data updates
- **What Stock Explorer does better**:
  - Not competing on charting — Stock Explorer's educational mission is different
  - Plain-language explanations for beginners
  - No information overload

### 5. finance.yahoo.com
**Design approach**: Balanced information architecture, mainstream audience.
- **Strengths**:
  - Excellent tab-based navigation (Summary, Chart, Conversations, Statistics)
  - Strong use of data visualization (interactive charts, key statistics cards)
  - Good balance between depth and accessibility
  - Consistent design language across all pages
  - Excellent responsive design — works well on all screen sizes
- **What they do better**:
  - More polished tab navigation with icons
  - Better use of summary statistics cards (key metrics at a glance)
  - More consistent spacing and typography scale
  - Better loading states with skeleton screens
- **What Stock Explorer does better**:
  - Yahoo Finance assumes financial literacy — Stock Explorer teaches it
  - Plain-language analogies are unique to Stock Explorer
  - PPT-style one-concept-per-page is more focused

### Key Takeaways for Stock Explorer

| Area | Best Practice (from competitors) | Stock Explorer Gap | Priority |
|------|----------------------------------|-------------------|----------|
| **Card consistency** | statementdog/cmoney use identical card templates everywhere | Cards vary across pages (inline HTML vs `_白话_card` vs custom) | **P1** |
| **Empty states** | cmoney uses illustrations + CTAs | Stock Explorer uses plain `st.info()` — functional but bland | **P2** |
| **Loading states** | Yahoo uses skeleton screens | Stock Explorer uses `st.spinner` — adequate but basic | **P2** |
| **Comparison UI** | goodinfo's heatmaps are very effective | Stock Explorer's radar chart is novel but less intuitive | **P1** |
| **Mobile responsive** | All competitors handle mobile well | Stock Explorer has basic media queries but untested edge cases | **P1** |
| **Color consistency** | All competitors use consistent semantic colors | Stock Explorer has color violations (see Section III) | **P1** |
| **Typography scale** | Yahoo uses a clear type scale (12/14/16/20/24/32px) | Stock Explorer's type sizes are inconsistent across pages | **P2** |

---

## II. Design System Compliance Audit — Per Page

### Grading Scale
- **A**: Fully compliant — PPT style, zone separation, color system, text limits
- **B**: Minor issues — mostly compliant, small deviations
- **C**: Moderate issues — several violations that affect UX
- **D**: Major issues — fundamental design system violations
- **F**: Critical — page is broken or unusable

---

### 2.1 business_card.py — Company Business Card

**PPT Style Grade: B+**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ⚠️ Partial | Watchlist buttons in header (col3) mix Zone A with interactive controls. Design system says Zone A "Must NOT contain interactive controls" (Section II, Zone A) |
| Color system | ✅ Compliant | Uses standard colors correctly |
| Text limits | ⚠️ Unknown | File truncated at line 128 — cannot verify full text count. Header section looks clean. |
| Chart proportion | ⚠️ Unknown | File truncated — cannot verify chart-to-text ratio |
| Loading states | ✅ Yes | Router wraps with `st.spinner("載入名片頁...")` |
| Error handling | ✅ Yes | Router handles `data is None` case |
| Button keys | ✅ Yes | Uses `f"watch_{stock_id}"`, `f"unwatch_{stock_id}"` — unique |
| Responsive | ⚠️ Partial | Uses `st.columns([3, 1, 1])` — no responsive fallback for narrow screens |

**Issues found**:
- **D-001**: Watchlist buttons in navbar violate Zone A purity (line 56-72). Interactive controls should be in Zone C, not Zone A.
- **D-002**: File is truncated — the full page content (revenue chart, news, dividend sections) could not be reviewed. Need to verify text limits and chart proportions.

---

### 2.2 operation_checkup.py — Operational Checkup

**PPT Style Grade: B**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean separation — controls at top of Zone C, data below |
| Color system | ✅ Compliant | Uses `#3498DB`, `#27AE60`, `#E74C3C` correctly |
| Text limits | ⚠️ Exceeds | Trend messages (lines 62-69) are ~80 chars each × 4 variants = potential 320 chars of text. Info cards add more. Total likely exceeds 200-char limit. |
| Chart proportion | ✅ Good | 3 charts with good spacing, charts dominate the page |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | `st.info()` for missing data in each section |
| Button keys | N/A | No buttons on this page |
| Responsive | ⚠️ Partial | Uses `st.columns(2)` and `st.columns(3)` — no responsive fallback |

**Issues found**:
- **D-003**: Text volume likely exceeds 200-char limit (Design System Section 5.2). The trend interpretation messages (lines 62-69) plus info cards (lines 70, 122-128) add substantial text. Recommend condensing to one summary sentence.
- **D-004**: Custom gradient card (lines 135-175) uses `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` — not in design system. Should use standard `#F8F9FA` card background.
- **D-005**: Section title "🩺 營運摘要" uses emoji in heading — inconsistent with `_section_title()` pattern used elsewhere.

---

### 2.3 financial_health.py — Financial Health

**PPT Style Grade: C+**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ⚠️ Violation | Line 180: `health_color = "#F39C12"` — orange is NOT in the design system color palette (Section 3.1). Only blue, green, red are allowed for status indication. |
| Text limits | ❌ Exceeds | Heavy text content: info cards (lines 69-75, 235-244), balance sheet explanations (lines 164-171), cash flow explanations (lines 222-231). Well over 200 chars. |
| Chart proportion | ⚠️ Low | Only 1 chart (funnel) + many text-heavy card sections. Charts likely < 60% of page. |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | `st.info()` for all missing data cases |
| Button keys | N/A | No buttons |
| Responsive | ⚠️ Partial | Uses `st.columns(3)` for ratio cards — no responsive fallback |

**Issues found**:
- **D-006**: Color violation — `#F39C12` (orange) used for "moderate" debt ratio warning (line 180). Design system Section 3.1 states: "No colors other than red, green, or blue may be used for status indication." Should use `#3498DB` (blue) for moderate/neutral status.
- **D-007**: Text volume significantly exceeds 200-char limit. The page has 4 major sections each with detailed explanations. This is the most text-heavy page in the app.
- **D-008**: Chart proportion below 60%. Only 1 funnel chart for a page with 4 sections. Needs more visual content or fewer text sections.
- **D-009**: Custom inline HTML card (lines 188-196) doesn't use `_info_card()` or `_白话_card()` — breaks component consistency.

---

### 2.4 peer_comparison.py — Peer Comparison

**PPT Style Grade: B+**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Uses `#3498DB` (target) and `#E74C3C` (benchmark) correctly |
| Text limits | ⚠️ Borderline | Analysis text (lines 333-367) could exceed 200 chars when all metrics present |
| Chart proportion | ✅ Good | Table + radar chart — good balance |
| Loading states | ✅ Yes | Multiple spinners for benchmark loading |
| Error handling | ✅ Yes | Graceful fallback to single-company view |
| Button keys | N/A | No buttons on this page |
| Responsive | ⚠️ Partial | Comparison table may overflow on narrow screens |

**Issues found**:
- **D-010**: Text volume in `_render_metric_analysis` (lines 333-367) generates analysis for each metric — with 4 metrics, total text could reach 400+ chars. Should limit to top 2-3 most significant differences.
- **D-011**: `_render_single_company_view` (lines 74-96) uses `st.metric()` — inconsistent with the `_白话_card()` pattern used everywhere else.
- **D-012**: Uses `@st.cache_data(ttl=3600)` on line 51 — architecture doc Section 3.3 says "Must not use `st.cache_data` in the View layer." This is in `src/pages/`, so it violates the architecture.

---

### 2.5 etf_browser.py — ETF Browser

**PPT Style Grade: B**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ⚠️ Violation | Line 447: `#8E44AD` (purple) for dividend yield — NOT in design system. Lines 67-68: `#2E86C1` and `#1B4F72` — darker blues not in palette. |
| Text limits | ✅ Good | ETF explanation card is concise |
| Chart proportion | N/A | List-based page, no charts — acceptable for browser |
| Loading states | ✅ Yes | Multiple spinners for data loading |
| Error handling | ✅ Yes | Try/except throughout |
| Button keys | ⚠️ Risk | Uses `f"hot_{row['stock_id']}"` (line 174), `f"cat_{row['stock_id']}"` (line 330), `f"div_{row['stock_id']}"` (line 450) — unique within section but could collide if same stock appears in multiple sections |
| Responsive | ⚠️ Partial | Uses `st.columns([0.5, 0.8, 1.5, 1.2, 1.2, 0.8])` — 6-column layout will break on narrow screens |

**Issues found**:
- **D-013**: Color violations — `#8E44AD` (purple, line 447), `#2E86C1` (dark blue, line 67), `#1B4F72` (navy, line 68). None are in the design system palette.
- **D-014**: Button key collision risk — if a stock appears in both "Hot ETFs" and "Dividend Ranking", the `f"hot_{sid}"` and `f"div_{sid}"` keys are different, but the "View" button text is identical which may confuse users.
- **D-015**: 6-column layout (line 165, 437) is too wide for narrow screens. No responsive fallback.
- **D-016**: Uses `@st.cache_data(ttl=3600)` on lines 12 and 18 — same architecture violation as peer_comparison.py.

---

### 2.6 etf_detail.py — ETF Detail

**PPT Style Grade: B+**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Uses standard colors |
| Text limits | ✅ Good | Concise sections with clear headings |
| Chart proportion | ✅ Good | Price chart + institutional chart — good ratio |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | Try/except throughout |
| Button keys | N/A | No buttons |
| Responsive | ⚠️ Partial | Uses `st.columns(2)` for fee cards — acceptable |

**Issues found**:
- **D-017**: Custom disclaimer card (lines 306-311) uses `#7D6608` (dark gold) — not in design system. Should use `#FEF9E7` background with `#F1C40F` border (warning style from design system).
- **D-018**: Fee card values are hardcoded (lines 273-281) — "約 0.3% / 年" and "約 0.04% / 年" are approximations. Should either fetch actual data or label clearly as "常見範圍".

---

### 2.7 category_browser.py — Category Browser

**PPT Style Grade: B**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Uses standard colors |
| Text limits | ✅ Good | Minimal text |
| Chart proportion | N/A | List-based page, no charts — acceptable |
| Loading states | ✅ Yes | Spinner for data loading |
| Error handling | ✅ Yes | Try/except throughout |
| Button keys | ⚠️ Risk | Uses `f"val_{row['stock_id']}"` (line 111), `f"ind_{row['stock_id']}"` (line 185), `f"vol_{row['stock_id']}"` (line 247) — unique within section |
| Responsive | ⚠️ Partial | 6-column layout (line 105) and 3-column card grid (line 158) — no responsive fallback |

**Issues found**:
- **D-019**: 6-column layout (line 105) will break on narrow screens.
- **D-020**: Industry browser uses `st.radio` with `label_visibility="collapsed"` (line 141) — the label "產業" is hidden, making it inaccessible for screen readers. Accessibility issue.
- **D-021**: No loading state for individual stock price fetches — the progress bar (line 65) is good but the page shows nothing until all 200 stocks are processed.

---

### 2.8 event_dashboard.py — Event Dashboard

**PPT Style Grade: A-**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ✅ Compliant | Uses standard colors |
| Text limits | ✅ Good | Concise event display |
| Chart proportion | N/A | Event list page — no charts needed |
| Loading states | ✅ Yes | Router wraps with spinner |
| Error handling | ✅ Yes | Handles empty events gracefully |
| Button keys | ✅ Fixed | Uses `f"evt_{evt_idx}"` (line 91) — P0 fix from Round 1 was applied |
| Responsive | ✅ Good | Simple list layout, works on all screens |

**Issues found**:
- **D-022**: Severity badges use emoji (🔴🟡🟢) without text alternatives — accessibility concern for color-blind users. Should include text labels alongside colors.
- **D-023**: "關於事件儀表板" section (lines 100-112) is a static markdown table — takes up space without adding dynamic value. Consider making it collapsible.

---

### 2.9 watchlist_page.py — Watchlist

**PPT Style Grade: B**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Zone separation | ✅ Yes | Clean content area |
| Color system | ⚠️ Violation | Lines 123-124: `#2E86C1` and `#1B4F72` — darker blues not in palette |
| Text limits | ✅ Good | Concise |
| Chart proportion | N/A | List-based page — acceptable |
| Loading states | ✅ Yes | Spinner for price loading |
| Error handling | ✅ Yes | Try/except throughout |
| button keys | ✅ Good | Uses `f"wl_card_{stock_id}_{selected_list}"` — unique and descriptive |
| Responsive | ⚠️ Partial | Card layout uses flexbox (lines 204-224) — may break on narrow screens |

**Issues found**:
- **D-024**: Color violations — `#2E86C1` (line 123) and `#1B4F72` (line 124) in empty state card. Should use `#3498DB` (primary blue from design system).
- **D-025**: Card layout uses raw flexbox HTML (lines 204-224) instead of `_白话_card()` — breaks component consistency.
- **D-026**: Alert popover (lines 241-284) is very tall — takes up significant screen real estate. Consider a simpler inline edit pattern.

---

## III. Color System Violation Summary

The design system (Section 3.1) defines a strict palette:
- Blue: `#3498DB` (primary accent)
- Green: `#27AE60` (positive/up)
- Red: `#E74C3C` (negative/down)
- Light gray: `#F8F9FA` (card background)
- Light yellow: `#FEF9E7` (warning background)
- Light orange: `#FFF8F0` (tip background)
- Dark gray: `#2C3E50` (primary text)
- Gray: `#7F8C8D` (secondary text)

**Violations found across the codebase**:

| File | Line | Illegal Color | Should Be |
|------|------|---------------|-----------|
| `financial_health.py` | 180 | `#F39C12` (orange) | `#3498DB` (blue for neutral) |
| `etf_browser.py` | 67 | `#2E86C1` (dark blue) | `#3498DB` (primary blue) |
| `etf_browser.py` | 68 | `#1B4F72` (navy) | `#2C3E50` (primary text) |
| `etf_browser.py` | 447 | `#8E44AD` (purple) | `#2C3E50` (primary text) or `#3498DB` |
| `watchlist_page.py` | 123 | `#2E86C1` (dark blue) | `#3498DB` (primary blue) |
| `watchlist_page.py` | 124 | `#1B4F72` (navy) | `#2C3E50` (primary text) |
| `etf_detail.py` | 307 | `#7D6608` (dark gold) | `#7D6608` is acceptable for disclaimer text on `#FEF9E7` bg |
| `chart.py` | 30-31 | `#555555`, `#333333` | These are chart-specific — acceptable as they're for axis labels, not UI |
| `chart.py` | 150 | `#4A90D9` | Close to `#3498DB` but not exact — should standardize |
| `chart.py` | 204 | `#F39C12`, `#2ECC71`, `#E74C3C`, `#3498DB` | OHLC colors — `#F39C12` and `#2ECC71` are not in design system. `#2ECC71` is close to `#27AE60` but not exact. |

---

## IV. Responsive Design Audit (P2-2 Verification)

**Status**: P2-2 was marked as "Implemented" in pending_review.md (2026-06-09).

**What was done**:
- Navbar changed from 9-button row to `st.radio(horizontal=True)` — this wraps to a dropdown on narrow screens ✅
- CSS media queries added in `main.py` (lines 58-68) for padding adjustments at 768px and 600px ✅

**What's still missing**:
- **Column layouts**: Many pages use `st.columns([0.5, 0.8, 1.5, 1.2, 1.2, 0.8])` (6-column) or `st.columns(3)` (3-column) with no responsive fallback. Streamlit's columns don't auto-wrap — they overflow horizontally.
- **Card grids**: `category_browser.py` uses `st.columns(cols_per_row)` with `cols_per_row = 3` — no responsive adjustment.
- **Table overflow**: `st.dataframe()` in peer_comparison.py and etf_browser.py will overflow on narrow screens.
- **No testing evidence**: No screenshots or test results at 375/768/1024/1440px breakpoints.

**Grade**: P2-2 is **partially fixed**. The navbar issue is resolved, but column-based layouts throughout the app still break on narrow screens.

---

## V. Accessibility Audit

| Issue | Location | Severity | WCAG Guideline |
|-------|----------|----------|----------------|
| Color-only severity indicators | `event_dashboard.py` lines 21-26 | Medium | 1.4.1 Use of Color |
| Emoji-only badges without text | `event_dashboard.py` lines 21-26, 31-38 | Medium | 1.1.1 Non-text Content |
| Hidden label on industry radio | `category_browser.py` line 141 | High | 1.3.1 Info and Relationships |
| Low contrast on `#7F8C8D` text on `#F8F9FA` bg | All `_白话_card` labels | Low | 1.4.3 Contrast (Minimum) — ratio is 4.6:1, passes AA for normal text |
| `#5D6D7E` on `#FFF8F0` bg | `_info_card` content | Low | Ratio is 4.8:1, passes AA |
| `#555555` chart text on transparent bg | `chart.py` line 30 | Medium | May fail on dark backgrounds — ratio against dark bg is 3.9:1, fails AA |
| No focus indicators on custom HTML cards | All pages | Low | 2.4.7 Focus Visible |
| `label_visibility="collapsed"` on search | `main.py` line 177 | Low | Acceptable if placeholder provides context |

---

## VI. Loading States Audit

| Page | Has Spinner | Location | Quality |
|------|-------------|----------|---------|
| Business Card | ✅ | `router.py:120` | Good |
| Operation Checkup | ✅ | `router.py:123` | Good |
| Financial Health | ✅ | `router.py:126` | Good |
| Peer Comparison | ✅ | `router.py:129` | Good |
| ETF Browser | ✅ | `router.py:74`, `etf_browser.py:83,107` | Good — multiple spinners |
| ETF Detail | ✅ | `router.py:111` | Good |
| Category Browser | ✅ | `router.py:69`, `category_browser.py:20` | Good |
| Event Dashboard | ✅ | `router.py:84` | Good |
| Watchlist | ✅ | `router.py:79`, `watchlist_page.py:143` | Good |

**Verdict**: All pages have loading states. This was a P1 fix from Round 1 and is now fully implemented. ✅

---

## VII. Error State Design Quality

| Page | Error Type | Handling | Quality |
|------|------------|----------|---------|
| All pages | Stock not found | `st.error()` in router | ✅ Good |
| All pages | API failure | Try/except → `st.info()` | ✅ Good |
| All pages | Empty data | `st.info()` per section | ✅ Good |
| ETF Browser | API failure | `st.error()` + early return | ✅ Good |
| Category Browser | Missing columns | `st.error()` + early return | ✅ Good |
| Watchlist | Price fetch failure | `st.warning()` | ✅ Good |
| Peer Comparison | Benchmark not found | Fallback to single-company view | ✅ Good |

**Verdict**: Error handling is comprehensive and follows design system Section 4.4. ✅

---

## VIII. NEW Design Improvement Suggestions

### P0 — Critical (Blocks MVP quality)

1. **Fix color system violations** — Replace all illegal colors with design system palette. Affects 6 files. This is a branding/consistency issue.
   - `financial_health.py:180` — `#F39C12` → `#3498DB`
   - `etf_browser.py:67,68,447` — `#2E86C1,#1B4F72,#8E44AD` → `#3498DB,#2C3E50,#2C3E50`
   - `watchlist_page.py:123,124` — `#2E86C1,#1B4F72` → `#3498DB,#2C3E50`

2. **Remove `st.cache_data` from View layer** — `peer_comparison.py:51` and `etf_browser.py:12,18` violate architecture Section 3.3. Move caching to the data layer.

3. **Fix Zone A violation in business_card.py** — Move watchlist buttons from navbar (Zone A) to content area (Zone C).

### P1 — Important (Affects UX quality)

4. **Standardize card components** — Create a shared card component library:
   - `business_card.py` has inline HTML cards that don't use `_白话_card()` / `_info_card()`
   - `financial_health.py` has custom gradient card (line 169) and custom health card (line 188)
   - `watchlist_page.py` has raw flexbox card (line 204)
   - **Recommendation**: All pages should use `_白话_card()` and `_info_card()` from `_router_base.py`. Custom cards should be extracted to shared components.

5. **Reduce text on financial_health.py** — The page has 4 sections with detailed explanations. Consolidate to 2-3 sections or make explanations collapsible. Target: < 200 chars of body text.

6. **Improve responsive column layouts** — Replace fixed `st.columns()` with responsive patterns:
   ```python
   # Instead of fixed 6-column layout:
   if st.session_state.get("is_narrow", False):
       cols = st.columns(2)
   else:
       cols = st.columns(6)
   ```
   Or use CSS grid with `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))`.

7. **Add text alternatives to severity badges** — `event_dashboard.py` should include text labels alongside emoji: "🔴 重大 (High)" instead of just "🔴 重大".

8. **Standardize chart colors in chart.py** — Replace `#4A90D9` with `#3498DB`, `#2ECC71` with `#27AE60`, `#F39C12` with `#3498DB` (for neutral) or remove orange from charts entirely.

### P2 — Nice to Have (Polish)

9. **Improve empty states** — Add illustrations or more helpful CTAs to empty watchlist, empty events, etc. Currently just `st.info()` text.

10. **Add skeleton loading screens** — Replace `st.spinner` with skeleton placeholders for a more polished feel (like Yahoo Finance).

11. **Standardize typography scale** — Define a global type scale:
    - H1: 2rem / 32px
    - H2: 1.5rem / 24px
    - H3: 1.2rem / 19px
    - Body: 1rem / 16px
    - Caption: 0.85rem / 13.6px
    - Currently pages use inconsistent sizes (1.3rem, 1.1rem, 0.92rem, etc.)

12. **Add focus indicators to interactive elements** — Custom HTML cards should have `:focus` styles for keyboard navigation.

13. **Extract ETF fee data** — `etf_detail.py` hardcodes fee estimates. Either fetch actual expense ratios or label clearly as "常見範圍" with a data source note.

---

## IX. Overall PPT Style Adherence Grades

| Page | Grade | Primary Issues |
|------|-------|----------------|
| Business Card | B+ | Zone A violation, file truncated |
| Operation Checkup | B | Text exceeds limit, custom gradient card |
| Financial Health | C+ | Color violation, text-heavy, low chart ratio |
| Peer Comparison | B+ | Text borderline, `st.cache_data` in View |
| ETF Browser | B | Color violations, wide columns, `st.cache_data` |
| ETF Detail | B+ | Minor color issue, hardcoded fees |
| Category Browser | B | Wide columns, accessibility issue |
| Event Dashboard | A- | Minor accessibility concerns |
| Watchlist | B | Color violations, custom card HTML |

**Overall Design System Compliance: B-**

The app has a solid foundation with good loading states, error handling, and zone separation. The main areas for improvement are:
1. **Color system violations** (6 files, ~10 instances)
2. **Text volume control** (financial_health.py is the worst offender)
3. **Component consistency** (inline HTML cards vs shared components)
4. **Responsive design** (column layouts break on narrow screens)
5. **Chart color standardization** (chart.py uses colors outside the design system)

---

## X. Specific CSS/Component Recommendations

### 10.1 Global Card Component (to replace inline HTML)

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

### 10.2 Responsive Column Helper

```python
def responsive_columns(narrow_count=2, wide_count=6, breakpoint=768):
    """Return column layout based on screen width."""
    # Use session state set by JS detection
    is_narrow = st.session_state.get("screen_width", 1024) < breakpoint
    return st.columns(narrow_count if is_narrow else wide_count)
```

### 10.3 Chart Color Standardization

In `src/services/chart.py`, replace all hardcoded colors:
```python
# Design system colors for charts
DS_BLUE = "#3498DB"
DS_GREEN = "#27AE60"
DS_RED = "#E74C3C"
DS_TEXT = "#555555"
DS_GRID = "rgba(128,128,128,0.15)"

# Replace:
# - "#4A90D9" → DS_BLUE
# - "#2ECC71" → DS_GREEN
# - "#F39C12" → DS_BLUE (for neutral/structural elements)
```

### 10.4 CSS Media Query Enhancement

Add to `main.py`:
```css
/* Responsive column wrapping */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 1rem !important;
    }
    /* Make radio buttons stack vertically */
    div[role="radiogroup"] {
        flex-direction: column !important;
    }
    /* Reduce card padding */
    div[style*="border-radius:12px"] {
        padding: 0.8rem !important;
    }
}
```

---

*End of Design Review Report — Round 2*
