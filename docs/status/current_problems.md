# Stock Explorer — Current Problems

> **Last Updated**: 2026-06-17
> **Source**: Design Review Round 11 (2026-06-17)
> **Maintainer**: Design Reviewer

This file tracks all known design/UX problems in Stock Explorer, organized by severity.

---

## Severity Levels

- **P0 (Blocking)**: Violates core design principles (ten-second test, PPT style). Must fix before next release.
- **P1 (Important)**: Significant UX friction or inconsistency. Should fix in next sprint.
- **P2 (Optimization)**: Minor issues or nice-to-have improvements. Fix when capacity allows.

---

## P0 — Blocking Issues

*(None currently — all P0 issues from Round 9 have been resolved)*

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
- **Description**: `docs/design/design_system.md` does NOT exist at the expected path. Color values, card styles, spacing, and typography are defined inline across multiple files. New features (C37, C39, C41, C36, C38, C42-C47) have no design system to follow, leading to inconsistencies.
- **Affected Files**: All pages and services
- **Proposed Fix**: Create `docs/design/design_system.md` documenting: color palette, card styles, typography, spacing system, Zone A/B/C rules, PPT-style principles. Note: A design system exists at `docs/domain/design_system.md` — should be copied/linked to the expected path.
- **Effort**: 1h (copy existing doc to expected path)

### D-005: Business Card Page Overload Risk
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The Business Card page already had 9 sections. Sprint 2 added C37, C39, C43, and C45, bringing the total to 13+ sections. This risks violating the "one key point per page" PPT-style principle and pushing content far below the fold.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Follow the "one new card per page per sprint" principle. Use progressive disclosure (expandable sections) for less critical content. Consider a "beginner mode by default" approach instead of showing everything. Reorder sections per Round 11 recommendations (summary → snowflake → deltas → details).
- **Related Features**: C37, C39, C41, C36, C43, C45

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

### D-016: C37 Missing Orange/Amber Hero Card Style
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: C37 (Key Takeaways) uses the standard `_info_card()` with blue border (`#3498DB`) instead of the specified orange/amber hero card style (`#F39C12` border, `#FFF8F0` background). The design intent was for C37 to be the ONLY card using orange — the "hero card" of the page. Using the same blue border as every other card defeats this purpose.
- **Affected Files**: `business_card.py` (line 152), `_router_base.py`
- **Proposed Fix**: Create a new `_summary_card()` component in `_router_base.py` with orange/amber styling (`border-left:4px solid #F39C12`, `background:#FFF8F0`), and use it for C37.
- **Effort**: 30 min

### D-018: C39 Placement Too Low on Page
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: C39 (What Changed) appears AFTER the "關鍵數字三連卡" section, not directly below C37 as specified. The intended flow was: summary → what changed → detailed data. Current order is: summary → detailed data → what changed. This reduces the "what's new" prominence.
- **Affected Files**: `business_card.py` (lines 170-217)
- **Proposed Fix**: Move C39 block (lines 200-217) to immediately after C37 block (lines 140-152), before the "關鍵數字三連卡" section.
- **Effort**: 15 min

### D-021: C43 Missing Per-Dimension Plain-Language Explanations
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec asked for one-line plain-language explanations on hover/click for each dimension (e.g., "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元"). Current hover only shows "獲利能力: 85分". The dimension cards below show scores but not the underlying metric values or explanations.
- **Affected Files**: `chart.py` (create_health_snowflake), `business_card.py` (lines 232-249)
- **Proposed Fix**: Pass the underlying metric values (ROE, gross margin, etc.) into the hover template for each dimension. Add a plain-language explanation below each dimension card.
- **Effort**: 1-2h

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

### D-015: No Structured Learning Path
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: "Did You Know?" facts are scattered across stock pages. No progressive education, no structured curriculum, no "beginner to advanced" learning path. Investopedia Academy and Stockopedia Academy both offer structured courses.
- **Affected Pages**: `business_card.py` (Did You Know section)
- **Proposed Fix**: Implement C47 (Financial Education Academy) with 10-15 structured lessons organized by difficulty, each using real TW stock examples.
- **Related Features**: C47
- **Competitor Benchmark**: Investopedia (Academy), Stockopedia (Academy)

### D-017: C37 Bullet Count Exceeds Spec
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Design spec said max 3 bullets for C37. Implementation caps at 5. For stocks with many available metrics, this can produce 5 bullets, pushing content down and violating the "≤ 200 characters" text limit.
- **Affected Files**: `analogy_engine.py` (line 422: `return takeaways[:5]`)
- **Proposed Fix**: Change cap to 3 (`return takeaways[:3]`) to match spec and enforce brevity.
- **Effort**: 5 min

### D-019: C39 Missing Delta Count Cap
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec said max 2 deltas. Implementation shows ALL deltas exceeding 10% threshold. Revenue, price, and YoY could all exceed 10%, showing 3 deltas.
- **Affected Files**: `analogy_engine.py` (`compute_recent_deltas` function)
- **Proposed Fix**: Add `return deltas[:2]` at the end of `compute_recent_deltas()` to enforce the 2-delta cap.
- **Effort**: 5 min

### D-020: C39 Missing Directional Color Coding
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec called for green (`#27AE60`) text for positive deltas and red (`#E74C3C`) text for negative deltas. Implementation uses default card text color for all deltas. The 📈/📉 emojis provide some visual cue, but the text itself isn't color-coded.
- **Affected Files**: `business_card.py` (lines 208-216)
- **Proposed Fix**: Apply inline color styling to delta text based on direction. Use `<span style="color:#27AE60">` for positive and `<span style="color:#E74C3C">` for negative.
- **Effort**: 30 min

### D-022: C43 Placement Not Near Top of Page
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: The snowflake chart appears after "關鍵數字三連卡" and C39, not near the top of the page. Per Round 9, it should be "below C37 (Key Takeaways) or as a replacement for the 關鍵數字三連卡 section."
- **Affected Files**: `business_card.py` (lines 219-253)
- **Proposed Fix**: Move C43 block to immediately after C37, before C39 and key metrics. This makes the snowflake the second thing users see (after the summary), which aligns with the "ten-second test" principle.
- **Effort**: 15 min

### D-023: C45 Uses 2-Year Window Instead of 5-Year
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec said "current P/E vs 5-year range." Implementation uses 2-year window (730 days). This may be due to data availability, but it reduces the chart's usefulness for long-term valuation context.
- **Affected Files**: `chart.py` (line 626: `cutoff_2y = pd.Timestamp.now() - pd.Timedelta(days=730)`)
- **Proposed Fix**: Extend to 5 years (1825 days) if data is available. Add a fallback: if < 2 years of data available, show what's available with a note.
- **Effort**: 30 min

---

## Resolved Issues

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| D-001 | No Visual Health Score | P0 | 2026-06-17 | C43 (Snowflake Health Visualization) fully implemented with 5-dimension radar chart, color-coded scores, reference lines, and plain-language health summary. |
| D-002 | No Synthesis Layer | P0 | 2026-06-17 | C37 (Key Takeaways) implemented with curated templates for top 20 stocks and auto-generated fallback for others. |
| D-014 | No Valuation Context | P2 | 2026-06-17 | C45 (Valuation Band Chart) implemented with historical PER percentile band, current PER marker, and plain-language interpretation. |

---

## Statistics

- **Total Issues**: 20
- **P0 (Blocking)**: 0
- **P1 (Important)**: 7 (D-003, D-004, D-005, D-006, D-007, D-016, D-018, D-021)
- **P2 (Optimization)**: 10 (D-008, D-009, D-010, D-011, D-012, D-013, D-015, D-017, D-019, D-020, D-022, D-023)
- **Resolved**: 3 (D-001, D-002, D-014)

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 3 feature implementation.*
