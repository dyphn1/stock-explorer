# Design Comparison Review — Round 4 (2026-06-11)

> **Reviewer:** Design Reviewer (Hermes)
> **Scope:** All 10 page files against `design_system.md`
> **Prior Rounds:** Round 2 (2026-06-10) found 26 issues; Round 3 (2026-06-11) found 3 new + critical business_card.py truncation

---

## I. Prior Round Issue Verification

### FIXED Since Round 3

| # | File | Fix Applied |
|---|------|-------------|
| D-012 | `peer_comparison.py` | `@st.cache_data` removed from view layer ✅ |
| D-016 | `etf_browser.py` | `@st.cache_data` replaced with module-level `_cached_get_stock_info()` / `_get_all_etf_prices()` ✅ |

### NOT FIXED — Still Present

| # | File | Verified Line | Status |
|---|------|---------------|--------|
| D-006 | `financial_health.py` | Line 180: `#F39C12` still used for moderate debt ratio | ❌ UNFIXED |
| D-013-a | `etf_browser.py` | Line 62: `#2E86C1` (dark blue) in ETF explainer card | ❌ UNFIXED |
| D-013-b | `etf_browser.py` | Line 63: `#1B4F72` (navy) in ETF explainer | ❌ UNFIXED |
| D-013-c | `etf_browser.py` | Lines 441–442: `#8E44AD` (purple) for dividend yield display | ❌ UNFIXED |
| D-024-a | `watchlist_page.py` | Line 123: `#2E86C1` in empty state card | ❌ UNFIXED |
| D-024-b | `watchlist_page.py` | Line 124: `#1B4F72` in empty state card | ❌ UNFIXED |
| D-003 | `operation_checkup.py` | Lines 62–69: 4× `_info_card()` calls with ~80-char plain text each, easily exceeding 200-char budget when combined | ❌ UNFIXED |
| D-007 | `financial_health.py` | Massive text across funnel analysis, 4 metric columns, balance sheet section, cash flow section | ❌ UNFIXED |
| D-008 | `financial_health.py` | Only 1 chart (funnel) for 4 sections — chart proportion well below 60% | ❌ UNFIXED |
| D-010 | `peer_comparison.py` | Lines 332–366: `_render_metric_analysis()` builds per-metric analysis text that can reach 400+ chars | ❌ UNFIXED |
| D-001 | `business_card.py` | Lines 56–72: Watchlist buttons/controls in Zone A (header area) | ❌ UNFIXED |
| D-004 | `operation_checkup.py` | Lines 135–175: Custom gradient card (`linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)`) doesn't use shared components | ❌ UNFIXED |
| D-009 | `financial_health.py` | Lines 188–196: Custom health assessment card with inline styles doesn't use shared components | ❌ UNFIXED |
| D-011 | `peer_comparison.py` | Line 92: Uses `st.metric()` instead of `_白话_card()` in `_render_single_company_view()` | ❌ UNFIXED |
| D-025 | `watchlist_page.py` | Lines 202–224: Raw flexbox HTML card row instead of `_白话_card()` | ❌ UNFIXED |
| D-027 | `event_dashboard.py` | Lines 141–142: `_render_adaptive_banner` uses custom gradient HTML | ❌ UNFIXED |
| D-028 | `watchlist_page.py` | Lines 84–114: Summary cards use inline HTML with hardcoded border colors | ❌ UNFIXED |
| D-005 | `_router_base.py` | Line 130: `_section_title()` auto-prepends `📊` — verified still present | ❌ UNFIXED |
| D-015 | `etf_browser.py` | Lines 160, 432: 6+ column layouts for ETF rows | ❌ UNFIXED |
| D-019 | `category_browser.py` | Lines 105, 241: 6-column layouts for stock rows | ❌ UNFIXED |
| D-020 | `category_browser.py` | Line 144: `label_visibility="collapsed"` on industry radio — screen reader inaccessible | ❌ UNFIXED |
| D-022 | `event_dashboard.py` | Lines 21–26: Severity badges use emoji without text alternatives | ❌ UNFIXED |
| chart.py | `chart.py` | Lines 150, 159, 204, 251, 315, 401: Deviating hex codes | ❌ UNFIXED |

### Round 3 Critical Issue Re-Examination: business_card.py truncation

**D-002 from Round 3 (CRITICAL):** business_card.py is only 128 lines. The file imports `create_revenue_trend_chart`, `create_revenue_pie_chart`, `analyze_revenue_breakdown`, `extract_dividend_summary`, `summarize_news`, `get_news_impact_level` but renders **NONE** of them. The page ends at line 128 with only:
- Header (price + watchlist buttons up to line 72)
- Watchlist popover UI (lines 75–128)

**The entire revenue section, pie chart section, news section, and dividend section — all imported but never called.** This is the MAIN landing page of the application.

**Status in Round 4: Still unfixed.** This is a P0-critical regression that makes the app's core value proposition (understanding what a company does) completely broken.

---

## II. NEW Issues Found in Round 4

### P0 — CRITICAL

| # | File | Line | Issue |
|---|------|------|-------|
| D-029-NEW | `business_card.py` | 128 | **Page still severely truncated.** Only header + watchlist UI rendered. Revenue chart, pie chart, news, dividend sections are imported but never called. The MAIN page of the app is a broken stub. |

### Color System Violations — NEW

| # | File | Line | Offending Color | Should Be | Context |
|---|------|------|-----------------|-----------|---------|
| D-030-NEW | `group_structure.py` | 239 | `#F39C12` (orange) | `#F39C12` is NOT in the design system palette | "Important investment" badge label `hold_color` for 20–49% holdings |
| D-031-NEW | `watchlist_page.py` | 169, 171, 197 | `#27AE60`, `#3498DB`, `#E74C3C` as inline badge colors | Badge colors are acceptable but delivered as raw HTML, not via shared component | Type badge (ETF 綠色 / 股票 藍色) and alert badge |
| D-032-NEW | `etf_detail.py` | 110 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` | No gradients in design system | One-liner banner — duplicate of D-027 pattern |
| D-033-NEW | `group_structure.py` | 202 | `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` | No gradients in design system | Group overview banner |
| D-034-NEW | `peer_comparison.py` | 92 | `st.metric()` with Streamlit default styling | `_白话_card()` | Single-company fallback view doesn't use shared card component |
| D-035-NEW | `event_dashboard.py` | 145 | `#EBF5FB`, `#D4E6F1` in gradient | No gradients in design system | Adaptive banner (same as D-027-NEW from R3 — gradient) |

### PPT Style Violations — NEW

| # | File | Line | Issue |
|---|------|------|-------|
| D-036-NEW | `financial_health.py` | 70–73 | `_info_card` content for funnel analysis is ~280 Chinese chars — exceeds 200-char limit for that single explanation |
| D-037-NEW | `financial_health.py` | 234–244 | Cash flow `_info_card` text blocks ("營業現金流為正、投資現金流為負...") — ~150 chars per block, 3 blocks total ~500 chars |
| D-038-NEW | `group_structure.py` | 326–330 | Strategy `_info_card` text ~180 chars just for the closing sentence; overall page text exceeds 200 chars significantly |
| D-039-NEW | `watchlist_page.py` | 157–226 | Watchlist item card renders per-stock flexbox row with name, price, change, alert status — no chart, page is entirely table/list oriented |

### Zone Separation Violations — NEW

| # | File | Line | Issue |
|---|------|------|-------|
| D-040-NEW | `business_card.py` | 95–128 | Watchlist popover management UI (text input, selectbox, create button) embedded directly in Zone A area — should be in Zone C or a dedicated modal |

### Component Consistency — NEW

| # | File | Line | Issue |
|---|------|------|-------|
| D-041-NEW | `category_browser.py` | 170–181 | Stock cards in industry browser use raw HTML `<div>` with inline styles instead of `_白话_card()` |
| D-042-NEW | `etf_browser.py` | 302–321 | ETF category cards use raw HTML with inline styles instead of `_白话_card()` |
| D-043-NEW | `etf_browser.py` | 59–119 | ETF explainer card uses custom gradient HTML with illegal colors |
| D-044-NEW | `etf_detail.py` | 183–188 | Dividend explanation raw HTML card instead of `_info_card()` |
| D-045-NEW | `etf_detail.py` | 250–256 | Institution explanation raw HTML card instead of `_info_card()` |
| D-046-NEW | `etf_detail.py` | 306–311 | Disclaimer uses raw HTML with `#7D6608` / `#F9E79F` — these are NOT in the design system palette |
| D-047-NEW | `main.py` | 48–56 | Global disclaimer CSS uses `#FEF9E7`, `#F9E79F`, `#7D6608` — none in design system |

### Responsive Design — NEW

| # | File | Line | Issue |
|---|------|------|-------|
| D-048-NEW | `peer_comparison.py` | 160–165 | Comparison table has "差距" column with dynamic content — 4 columns in `st.dataframe` will overflow on mobile |
| D-049-NEW | `main.py` | 58–68 | Media query only adjusts `.block-container` padding — no column reflow handling. Pages with 6-column layouts still break. |

### Accessibility — NEW

| # | File | Line | Issue |
|---|------|------|-------|
| D-050-NEW | `etf_browser.py` | 107–111 | `label_visibility="collapsed"` on horizontal radio — screen readers can't identify the purpose |
| D-051-NEW | `event_dashboard.py` | 21–26 | Severity badges ("🔴 重大", "🟡 注意") — emoji + Chinese text only, no `aria-label` or semantic role |
| D-052-NEW | `group_structure.py` | 235 | "🔴 控股子公司" / "🟡 重要轉投資" / "🟢 一般投資" — emoji color indicators used as severity signals without text fallbacks |
| D-053-NEW | `chart.py` | 30 | `#555555` chart text on transparent bg — WCAG AA contrast ratio ~4.5:1 on white, may fail on dark backgrounds |
| D-054-NEW | `watchlist_page.py` | 178–179 | Change color `#E74C3C` for positive / `#27AE60` for negative — color-only encoding of direction, no icon/text indicator (e.g., ▲/▼) |

---

## III. Per-Page Design Grade

### business_card.py — **Grade: D**
| Dimension | Assessment |
|-----------|------------|
| Color | ✅ Legal colors only in rendered portion |
| PPT Style | **F** — No chart at all. Page is just header + watchlist UI. Zero charts = 0% chart coverage |
| Zone Separation | ❌ Watchlist buttons in Zone A (D-001) + popover management UI (D-040) |
| Component Consistency | ❌ No shared cards used (no content to wrap) |
| Responsive | ⚠️ 3-column header will break on mobile |
| Accessibility | ⚠️ No issues in rendered content, but page is essentially empty |

**Verdict:** The most important page in the app is a broken stub. Revenue, pie chart, news, and dividend sections are all imported but never rendered.

---

### operation_checkup.py — **Grade: C+**
| Dimension | Assessment |
|-----------|------------|
| Color | ✅ Only `#2C3E50`, `#7F8C8D`, `#27AE60`, `#F8F9FA`, `#3498DB` used |
| PPT Style | ⚠️ 3 charts (revenue, price, institutional) = good. But trend messages (D-003) may push text over limit |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ⚠️ Lines 135–175 use custom gradient HTML instead of shared components (D-004) |
| Responsive | ⚠️ 2-column layouts will stack acceptably |
| Accessibility | ⚠️ Emoji in `_info_card` icons without aria alternatives |

**Verdict:** Solid chart-to-text ratio. Main issues are the custom gradient summary card and borderline text length.

---

### financial_health.py — **Grade: D+**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ `#F39C12` at line 180 for moderate debt (D-006) |
| PPT Style | **Major issues:** Only 1 chart (funnel) for 4 sections = ~20% chart coverage (D-008). Text massively exceeds 200-char limit across sections (D-007, D-036, D-037) |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ Lines 188–196: custom health card (D-009) |
| Responsive | ⚠️ 3-column metric layouts will stack |
| Accessibility | ⚠️ Color-only health indicator (`health_color` → `#E74C3C`, `#F39C12`, `#27AE60`) |

**Verdict:** The worst offender for PPT style compliance. Text-heavy, chart-starved, uses illegal orange color, and exceeds every text limit.

---

### peer_comparison.py — **Grade: C**
| Dimension | Assessment |
|-----------|------------|
| Color | ✅ Uses `#3498DB` and `#E74C3C` in radar chart (correct) |
| PPT Style | ⚠️ 1 chart (radar). Metric analysis text can reach 400+ chars (D-010) |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ `st.metric()` at line 92 instead of `_白话_card()` (D-011) |
| Responsive | ❌ Comparison table + radar = no mobile adaptation (D-048) |
| Accessibility | ⚠️ Radar chart color-only differentiation (blue vs red areas) |

**Verdict:** Good unique feature (radar comparison). Needs text reduction and component standardization.

---

### group_structure.py — **Grade: C-**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ `#F39C12` at line 239 for holding badge (D-030) + gradient at line 202 (D-033) |
| PPT Style | ⚠️ 1 chart (bar chart). Text across 5 sections approaches/exceeds limit (D-038) |
| Zone Separation | ✅ Clean content area |
| Component Consistency | Uses `_info_card()` and `_section_title()` ✅. Parent card uses raw HTML though |
| Responsive | ⚠️ Bar chart data looks good on mobile |
| Accessibility | ❌ Emoji color indicators for holding levels (D-052) |

**Verdict:** Best-structured page overall. Issues are gradient banner, illegal orange color, and emoji-only badges.

---

### category_browser.py — **Grade: D+**
| Dimension | Assessment |
|-----------|------------|
| Color | ✅ Uses `#F8F9FA`, `#3498DB`, `#2C3E50`, `#7F8C8D` correctly |
| PPT Style | ❌ Zero charts on the page. 100% table/list content = 0% chart coverage |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ Raw HTML stock cards at lines 170–181 (D-041) |
| Responsive | ❌ 6-column layouts at lines 105, 241 break on mobile (D-019) |
| Accessibility | ❌ `label_visibility="collapsed"` on industry radio (D-020) |

**Verdict:** Zero chart coverage makes this a pure data table page — opposite of PPT style. Accessibility regression on radio buttons.

---

### etf_browser.py — **Grade: D+**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ `#2E86C1`, `#1B4F72`, `#8E44AD` in explainer + dividend sections (D-013, D-043) |
| PPT Style | ❌ Zero charts. Pure list/table page |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ Raw HTML cards at lines 302–321 (D-042), custom gradient explainer (D-043) |
| Responsive | ❌ 6+ column layouts at lines 160, 432 (D-015) |
| Accessibility | ❌ `label_visibility="collapsed"` on sub-view radio (D-050) |

**Ververdict:** Illegal colors in gradients, zero chart component usage, same accessibility issue as category_browser.

---

### etf_detail.py — **Grade: C+**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ `linear-gradient` at line 110 (D-032, D-035), `#7D6608`/`#F9E79F` at lines 307–310 (D-046) |
| PPT Style | ✅ 2 charts (price area + institutional bar). Good chart-to-text ratio |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ Raw HTML cards at lines 183–188 (D-044) and 250–256 (D-045) |
| Responsive | ✅ Charts use `use_container_width=True` |
| Accessibility | ⚠️ Color-only price direction in institutional chart |

**Verdict:** Best ETF page. Good chart usage. Issues are gradient banner, illegal disclaimer colors, and raw HTML cards.

---

### watchlist_page.py — **Grade: D+**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ `#2E86C1`, `#1B4F72` in empty state (D-024), gradient at line 122 |
| PPT Style | ❌ Zero charts. Pure list/table page (D-039) |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ❌ Summary cards raw HTML (D-028), item rows raw HTML (D-025) |
| Responsive | ⚠️ 4-column action buttons will break on mobile |
| Accessibility | ❌ Color-only change direction (D-054) |

**Verdict:** Zero chart coverage, multiple component consistency issues, color-only encoding of price direction.

---

### event_dashboard.py — **Grade: C-**
| Dimension | Assessment |
|-----------|------------|
| Color | ❌ Gradient at line 142 (D-027, D-035) |
| PPT Style | ⚠️ Zero charts. Event list is text/table only. But this is a dashboard — some text density is expected |
| Zone Separation | ✅ Clean content area |
| Component Consistency | ✅ Uses `_info_card()` and `_section_title()` |
| Responsive | ✅ Expanders work well on mobile |
| Accessibility | ❌ Emoji severity badges without text alternatives (D-022, D-051) |

**Verdict:** Reasonable for a dashboard page. Main issues are gradient banner and accessibility of severity badges.

---

## IV. Overall Design Compliance Summary

### Grade Distribution

| Grade | Pages | Count |
|-------|-------|-------|
| A | — | 0 |
| B | — | 0 |
| C | operation_checkup, peer_comparison, group_structure, etf_detail, event_dashboard | 5 |
| D | business_card, financial_health, category_browser, etf_browser, watchlist_page | 5 |

### Updated Overall Design Compliance Grade: **D+**

**Rationale:**
- 5 of 10 pages are D-grade (broken or severely non-compliant)
- 0 pages achieve A or B grade
- The main landing page (business_card.py) is a broken stub — this alone drags the entire app to D-range
- No design issues were fixed between Round 3 and Round 4 (except 2 architecture violations)
- 25 NEW issues found in Round 4, bringing the cumulative total to **51+ design issues**

### Issue Count by Category (Cumulative)

| Category | Round 2 | Round 3 New | Round 4 New | Total |
|----------|---------|-------------|-------------|-------|
| Color System | 7 | 5 (gradients) | 6 | **18** |
| PPT Style | 4 | 0 | 4 | **8** |
| Zone Separation | 1 | 0 | 1 | **2** |
| Component Consistency | 4 | 1 | 7 | **12** |
| Responsive Design | 3 | 0 | 2 | **5** |
| Accessibility | 3 | 0 | 5 | **8** |
| Architecture | 2 | 0 | 0 | **2** |
| **Total** | **24** | **6** | **25** | **55** |

---

## V. Competitor Design Pattern Comparison

### Comparison 1: StatementDog (statementdog.com)

**What they do well:**
- Plain-language explanations below each indicator (similar to Stock Explorer's `_白话_card()`)
- "One-sentence summary" feature per company
- Financial report visualization with clear hierarchy

**Where Stock Explorer diverges (negatively):**
- StatementDog shows actual financial data tables with visual hierarchy — Stock Explorer's financial_health.py is text-heavy with only 1 chart
- StatementDog has proper responsive design — Stock Explorer's 6-column layouts break on mobile
- StatementDog uses consistent card components — Stock Explorer has 12+ component consistency violations

**Where Stock Explorer leads:**
- PPT-style one-point-per-page approach (StatementDog lacks this)
- Plain-language analogy engine (StatementDog's explanations are improving but less systematic)

### Comparison 2: WantGoo (wantgoo.com)

**What they do well:**
- Clean, modern design with infographic-style presentation
- Global stock market map (visual-first approach)
- Charts as the main focus, text as supplementary — aligns with Stock Explorer's PPT philosophy

**Where Stock Explorer diverges (negatively):**
- WantGoo's pages are chart-forward — 5 of Stock Explorer's 10 pages have ZERO charts
- WantGoo uses consistent card grids — Stock Explorer mixes raw HTML, `st.metric()`, and custom gradients
- WantGoo's mobile experience is RWD — Stock Explorer's media queries only adjust padding

**Where Stock Explorer leads:**
- Educational framework (WantGoo has none)
- Adaptive analysis framework (unique to Stock Explorer)

### Comparison 3: CMoney

**What they do well:**
- Card-style content presentation with consistent visual language
- Dark theme with proper contrast ratios
- Bottom navigation pattern for mobile

**Where Stock Explorer diverges (negatively):**
- CMoney's color system is consistent — Stock Explorer has 18 color violations
- CMoney's cards follow a design system — Stock Explorer has 12 component consistency issues
- CMoney's charts are interactive and well-labeled — Stock Explorer's chart.py uses deviating hex codes

**Where Stock Explorer leads:**
- "Historian, not stock picker" positioning (CMoney is stock-picking oriented)
- Plain-language explanations (CMoney lacks these)

---

## VI. Priority Recommendations

### P0 — Must Fix Before Next Review

1. **business_card.py truncation** — Render the imported revenue chart, pie chart, news, and dividend sections. This is the MAIN page.
2. **financial_health.py chart coverage** — Add at least 2 more charts (e.g., balance sheet waterfall, cash flow trend) to reach >60% chart coverage.
3. **Illegal color audit** — Replace ALL instances of `#F39C12`, `#2E86C1`, `#1B4F72`, `#8E44AD`, `#4A90D9`, `#2ECC71`, `#7D6608`, `#F9E79F` with design-system-compliant colors.

### P1 — Should Fix Soon

4. **Gradient elimination** — Replace all `linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%)` with solid `#F8F9FA` card backgrounds.
5. **Component standardization** — Migrate all raw HTML cards to `_白话_card()` / `_info_card()`.
6. **Text limit enforcement** — Reduce text in financial_health.py, peer_comparison.py, and group_structure.py to ≤200 chars per page.
7. **Accessibility fixes** — Add text alternatives to emoji badges, fix `label_visibility="collapsed"` on radios, add ▲/▼ indicators for price direction.

### P2 — Nice to Have

8. **Responsive column reflow** — Add media queries that convert 6-column layouts to 2-column or stacked layouts.
9. **Chart color standardization** — Update chart.py to use exact design system hex codes.
10. **Zone A cleanup** — Move watchlist controls from business_card.py header to Zone C or a dedicated modal.

---

*Review completed: 2026-06-11*
*Next review: Pending P0 fixes*
