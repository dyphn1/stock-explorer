# Stock Explorer — Current Problems

> **Last Updated**: 2026-06-14
> **Source**: Design Review Round 9 (2026-06-14)
> **Maintainer**: Design Reviewer

This file tracks all known design/UX problems in Stock Explorer, organized by severity.

---

## Severity Levels

- **P0 (Blocking)**: Violates core design principles (ten-second test, PPT style). Must fix before next release.
- **P1 (Important)**: Significant UX friction or inconsistency. Should fix in next sprint.
- **P2 (Optimization)**: Minor issues or nice-to-have improvements. Fix when capacity allows.

---

## P0 — Blocking Issues

### D-001: No Visual Health Score
- **Severity**: P0
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Business Card page shows 15+ metrics scattered across sections with no synthesized visual summary. Every major competitor (Simply Wall St snowflake, Morningstar stars, Stockopedia StockRank) has a visual health score. This directly violates the "ten-second test" — a beginner cannot glance at the page and understand the company's health.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Implement C43 (Company Snowflake Health Visualization) — a radar chart with 5 dimensions (獲利能力、成長性、財務健康、股利、估值) scored 0-5 with color coding and plain-language explanations.
- **Related Features**: C43
- **Competitor Benchmark**: Simply Wall St (snowflake), Morningstar (stars), Stockopedia (StockRank)

### D-002: No Synthesis Layer
- **Severity**: P0
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Business Card page shows data but doesn't synthesize it. A beginner sees 15+ metrics but doesn't know which 3 matter most. This violates the "ten-second test" and "story first, data second" core value.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Implement C37 (Key Takeaways Summary Card) — 3-5 auto-generated bullet points synthesizing the most important information, placed at the TOP of the page.
- **Related Features**: C37
- **Competitor Benchmark**: Public.com (story cards), Seeking Alpha (key takeaways)

---

## P1 — Important Issues

### D-003: Inconsistent Card Styling
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `_router_base.py` provides `_白话_card()` and `_info_card()` but pages frequently bypass these with inline HTML. `group_structure.py` uses completely different card styling (white background, different border colors). `watchlist_page.py` uses inline HTML for card rows. `etf_detail.py` uses inline HTML for the one-liner, header, and dividend sections. This creates visual inconsistency across pages.
- **Affected Pages**: `group_structure.py`, `watchlist_page.py`, `etf_detail.py`, `etf_browser.py`
- **Proposed Fix**: Replace all inline HTML cards with shared components from `_router_base.py`. Create additional card types (summary card, warning card) as needed.
- **Effort**: 2-3h

### D-004: No Design System Documentation
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `docs/design/design_system.md` does NOT exist. Color values, card styles, spacing, and typography are defined inline across multiple files. New features (C37, C39, C41, C36, C38, C42-C47) have no design system to follow, leading to inconsistencies.
- **Affected Files**: All pages and services
- **Proposed Fix**: Create `docs/design/design_system.md` documenting: color palette, card styles, typography, spacing system, Zone A/B/C rules, PPT-style principles.
- **Effort**: 2-3h

### D-005: Business Card Page Overload Risk
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The Business Card page already has 9 sections (header, one-liner, "Did You Know?", 3 key metrics, dividend story, revenue pie chart, revenue trend, news, disclaimer). Adding C37 + C39 + C41 + C36 to this page risks violating the "one key point per page" PPT-style principle.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Follow the "one new card per page per sprint" principle. Add features incrementally. Use progressive disclosure (expandable sections) for less critical content. Consider a "beginner mode by default" approach instead of showing everything.
- **Related Features**: C37, C39, C41, C36, C43

### D-006: Mobile Responsiveness Gaps
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: CSS media queries exist for 768px and 600px breakpoints, but they only adjust padding and font sizes. Multi-column layouts (`st.columns`) don't stack gracefully on mobile. Charts may be too small to read. Competitors have native apps; we're limited by Streamlit.
- **Affected Pages**: All pages
- **Proposed Fix**: Add mobile-specific CSS that stacks columns vertically, increases touch target sizes, and adjusts chart heights. Consider a mobile-first redesign for the Business Card page.
- **Effort**: 4-6h

### D-007: No Discovery Mechanism
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Users must know which stock to search for. No screening, no guided discovery, no "beginner path." 財報狗's #1 feature is its stock screener. Stock Explorer requires prior knowledge of TW stock tickers, which is a barrier for beginners.
- **Affected Pages**: `main.py` (welcome page), `category_browser.py`
- **Proposed Fix**: Implement C42 (Stock Screener / Discovery Engine) with beginner-friendly presets ("穩定收息", "成長潛力", "便宜估值") and card-based results.
- **Related Features**: C42
- **Competitor Benchmark**: 財報狗 (advanced screener), Stockopedia (StockRank screening)

---

## P2 — Optimization Issues

### D-008: Loading State Inconsistency
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Some pages show `st.spinner()` while loading data, others don't. The router shows "載入股票資料..." then each page shows "載入 XX 頁..." — two sequential spinners. No skeleton loading or progressive rendering.
- **Affected Pages**: `router.py`, all page files
- **Proposed Fix**: Standardize on a single spinner per page transition. Consider skeleton loading for chart areas.
- **Effort**: 1-2h

### D-009: Error State Inconsistency
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Empty data shows different messages on different pages (`st.info("暫無資料")`, `st.error()`, `st.warning()`). No standardized empty state design.
- **Affected Pages**: All pages
- **Proposed Fix**: Create a standardized empty state component with consistent messaging and styling.
- **Effort**: 1h

### D-010: Watchlist Page Uses Non-PPT Layout
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The watchlist page uses a table-like layout with columns for rank, ID, name, industry, value, button. This is the ONLY page that uses a dense table layout — all other pages use card-based PPT style. It feels like a different product.
- **Affected Pages**: `watchlist_page.py`
- **Proposed Fix**: Redesign watchlist using card-based layout consistent with other pages. Each watchlist item as a card with key info and actions.
- **Effort**: 2-3h

### D-011: Category Browser Uses Dense Tables
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The category browser uses multi-column layouts with small text for stock lists. This is data-dense rather than PPT-style. Beginners may find this overwhelming.
- **Affected Pages**: `category_browser.py`
- **Proposed Fix**: Redesign with larger cards, fewer items per row, and more visual hierarchy. Consider a "featured stock" card at the top of each category.
- **Effort**: 2-3h

### D-012: No Glossary/Tooltip System
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Financial terms (ROE, P/B, PER) have no inline help. Beginners must already know the terms. Investopedia has 10,000+ term glossary. Stock Explorer's analogy engine provides explanations but only in card format, not as hover tooltips.
- **Affected Pages**: All pages with financial metrics
- **Proposed Fix**: Implement C33 (Beginner Glossary / Term Tooltip System) with hover tooltips or click-to-expand definitions on all financial terms.
- **Related Features**: C33
- **Competitor Benchmark**: Investopedia (10K+ term glossary)

### D-013: No Risk Analysis Section
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Stock Explorer has NO risk analysis section. Simply Wall St has visual risk analysis. Morningstar has uncertainty ratings. Stock Explorer's "historian" positioning is perfect for risk analysis that explains historical risks without predicting the future.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Implement C44 ("What Could Go Wrong" Risk Analysis) with 3-5 key risks presented in plain language with historical evidence.
- **Related Features**: C44
- **Competitor Benchmark**: Simply Wall St (visual risk), Morningstar (uncertainty rating)

### D-014: No Valuation Context
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: P/E and P/B are shown as single numbers without historical context. 財報狗's P/E band chart (showing current P/E vs historical range) is one of its most popular features. Beginners don't know whether a P/E of 18 is "expensive" or "cheap" without context.
- **Affected Pages**: `business_card.py`, `financial_health.py`
- **Proposed Fix**: Implement C45 (Valuation Band Chart) showing current P/E vs 5-year range with plain-language interpretation.
- **Related Features**: C45
- **Competitor Benchmark**: 財報狗 (P/E band chart), Morningstar (fair value with uncertainty)

### D-015: No Structured Learning Path
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: "Did You Know?" facts are scattered across stock pages. No progressive education, no structured curriculum, no "beginner to advanced" learning path. Investopedia Academy and Stockopedia Academy both offer structured courses.
- **Affected Pages**: `business_card.py` (Did You Know section)
- **Proposed Fix**: Implement C47 (Financial Education Academy) with 10-15 structured lessons organized by difficulty, each using real TW stock examples.
- **Related Features**: C47
- **Competitor Benchmark**: Investopedia (Academy), Stockopedia (Academy)

---

## Resolved Issues

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| — | — | — | — | — |

---

## Statistics

- **Total Issues**: 15
- **P0 (Blocking)**: 2
- **P1 (Important)**: 5
- **P2 (Optimization)**: 8
- **Resolved**: 0

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 2 feature implementation.*
