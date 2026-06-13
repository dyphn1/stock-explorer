# Stock Explorer — Current Problems

> **Last Updated**: 2026-06-13
> **Source**: Design Review Round 20 (2026-06-13, Sprint 7)
> **Maintainer**: Design Reviewer

This file tracks all known design/UX problems in Stock Explorer, organized by severity.

---

## Severity Levels

- **P0 (Blocking)**: Violates core design principles (ten-second test, PPT style). Must fix before next release.
- **P1 (Important)**: Significant UX friction or inconsistency. Should fix in next sprint.
- **P2 (Optimization)**: Minor issues or nice-to-have improvements. Fix when capacity allows.

---

## P0 — Blocking Issues

*(None currently — all P0 issues have been resolved)*

---

## P1 — Important Issues

### D-003: Inconsistent Card Styling (PARTIALLY FIXED)
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `_router_base.py` provides `_白话_card()` and `_info_card()` but pages frequently bypass these with inline HTML. `group_structure.py` uses completely different card styling (white background, different border colors). `watchlist_page.py` uses inline HTML for card rows. `etf_detail.py` uses inline HTML for the one-liner, header, and dividend sections. **Round 14 regression**: C41 peer cards and C44 risk dimension cards also use inline HTML, worsening the inconsistency.
- **Affected Pages**: `group_structure.py`, `watchlist_page.py`, `etf_detail.py`, `etf_browser.py`, `business_card.py` (C41 lines 522-532, C44 line 72)
- **Proposed Fix**: Replace all inline HTML cards with shared components from `_router_base.py`. Create additional card types (summary card, warning card) as needed.
- **Effort**: 2-3h
- **Status**: ✅ **PARTIALLY FIXED in Sprint 7 (D3)** — `group_structure.py` now uses `_subsidiary_card()` and `_info_card()` with zero inline HTML. `_subsidiary_card()` and `_count_label()` added to `_router_base.py`. **Remaining**: `watchlist_page.py`, `etf_detail.py`, `business_card.py` C41/C44 inline HTML still present. **New regressions**: `market_event_case_study.py` (D-049, D-050) and `etf_browser.py` (D-051) introduced new inline HTML in Sprint 7. Net effect: group_structure fixed, but new pages added inline HTML. Overall inline HTML count: roughly unchanged.

### D-004: No Design System Documentation
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `docs/design/design_system.md` does NOT exist at the expected path. Color values, card styles, spacing, and typography are defined inline across multiple files. New features have no design system to follow, leading to inconsistencies.
- **Affected Files**: All pages and services
- **Proposed Fix**: Create `docs/design/design_system.md` documenting: color palette, card styles, typography, spacing system, Zone A/B/C rules, PPT-style principles. Note: A design system exists at `docs/domain/design_system.md` — should be copied/linked to the expected path.
- **Effort**: 1h (copy existing doc to expected path)

### D-005: Business Card Page Overload Risk
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The Business Card page already had 9 sections. Sprint 2 added C37, C39, C43, and C45, bringing the total to 13+ sections. C41 adds a "推薦閱讀" section. C44 adds a risk section (mitigated by `st.expander`). This risks violating the "one key point per page" PPT-style principle and pushing content far below the fold.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Follow the "one new card per page per sprint" principle. Use progressive disclosure (expandable sections) for less critical content. Consider a "beginner mode by default" approach instead of showing everything. Reorder sections per Round 11 recommendations (summary → snowflake → deltas → details).
- **Related Features**: C37, C39, C41, C36, C43, C45, C44
- **Status**: C44's expander helps mitigate. C41 adds length. Net effect: stable but concerning.

### D-006: Mobile Responsiveness Gaps
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: CSS media queries exist for 768px and 600px breakpoints, but they only adjust padding and font sizes. Multi-column layouts (`st.columns`) don't stack gracefully on mobile. Charts may be too small to read. Competitors have native apps; we're limited by Streamlit.
- **Affected Pages**: All pages
- **Proposed Fix**: Add mobile-specific CSS that stacks columns vertically, increases touch target sizes, and adjusts chart heights. Consider a mobile-first redesign for the Business Card page.
- **Effort**: 4-6h

### D-021: C43 Missing Per-Dimension Plain-Language Explanations (PARTIALLY FIXED)
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec asked for one-line plain-language explanations on hover/click for each dimension (e.g., "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元"). Round 12 partially fixed this: dimension cards now show generic score-based explanations, but the underlying metric values (ROE %, gross margin %, etc.) are still missing from both hover and cards. Hover template only shows "獲利能力: 85分".
- **Affected Files**: `chart.py` (create_health_snowflake hover template), `business_card.py` (dimension cards)
- **Proposed Fix**: Pass the underlying metric values (ROE, gross margin, etc.) into the hover template for each dimension. Add metric-specific plain-language explanations below each dimension card (e.g., "ROE 25%，每100元股東資金賺25元").
- **Effort**: 1-2h
- **Status**: ✅ RESOLVED via D-034 (4de8b8e) — metric values now shown in both hover and dimension cards with raw numbers.

### D-034: C3 Metric Value Tooltips Missing from Hover and Cards
- **Severity**: P1
- **Added**: 2026-06-19
- **Source**: Design Review Round 13 (related to D-021)
- **Description**: C43 snowflake hover template only shows "獲利能力: 85分" without the underlying metric values. Dimension cards show generic explanations but no actual numbers. Robinhood has metric tooltips on every stock page. Magnify.money generates visual explanations for every metric. Users see scores but don't know what they mean in concrete terms.
- **Affected Files**: `chart.py` (hover template), `business_card.py` (dimension cards)
- **Proposed Fix**: (1) Enhance hover template to show metric name + value + plain-language explanation. (2) Add metric values below each dimension card (e.g., "ROE 25%｜毛利率 66%"). (3) Add "❓" button for visual explanation (connects to C56).
- **Effort**: 1-2h
- **Status**: ✅ RESOLVED in Sprint 4 — `create_health_snowflake()` now accepts optional `metric_values` param. Hover shows metric values as bullet points. Dimension cards display raw values in blue text below score. `_get_health_metric_values()` helper added to `src/pages/business_card/_helpers.py`. Commit: 4de8b8e.

---

## P2 — Optimization Issues

### D-007: No Discovery Mechanism (DOWNGRADED TO P2)
- **Severity**: P2 (downgraded from P1 in Round 14)
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: Users must know which stock to search for. No screening, no guided discovery, no "beginner path." 財報狗's #1 feature is its stock screener. **Round 14 update**: C41 provides in-page peer discovery (同產業個股推薦), partially addressing this use case. Full screener (C42) still needed but P1 urgency reduced.
- **Affected Pages**: `main.py` (welcome page), `category_browser.py`
- **Proposed Fix**: Implement C42 (Stock Screener / Discovery Engine) with beginner-friendly presets ("穩定收息", "成長潛力", "便宜估值") and card-based results.
- **Related Features**: C42, C41 (partial)
- **Competitor Benchmark**: 財報狗 (advanced screener), Stockopedia (StockRank screening)

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

### D-015: No Structured Learning Path
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: "Did You Know?" facts are scattered across stock pages. No progressive education, no structured curriculum, no "beginner to advanced" learning path. Investopedia Academy and Stockopedia Academy both offer structured courses.
- **Affected Pages**: `business_card.py` (Did You Know section)
- **Proposed Fix**: Implement C47 (Financial Education Academy) with 10-15 structured lessons organized by difficulty, each using real TW stock examples.
- **Related Features**: C47
- **Competitor Benchmark**: Investopedia (Academy), Stockopedia (Academy)

### D-032: No Progressive Disclosure Pattern for Business Card Page (DOWNGRADED TO P2)
- **Severity**: P2 (downgraded from P1 in Round 14)
- **Added**: 2026-06-19
- **Source**: Design Review Round 13
- **Description**: The business card page already has 13+ sections. C44 (Risk), C48 (Story Card), and C56 (Explain Metric) will add 3+ more sections. **Round 14 update**: C44 implements progressive disclosure via `st.expander` (expanded=False), proving the pattern works. Remaining work is applying it to other sections.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Apply the `st.expander` pattern proven by C44 to remaining sections. Consider a "Beginner Mode" / "Advanced Mode" toggle for maximum effect.
- **Effort**: 3-4h
- **Competitor Benchmark**: Robinhood (minimalist default), 富邦e富 (card-based with whitespace)

### D-033: No Standardized Empty State Component
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 13
- **Description**: Empty data shows different messages on different pages (`st.info("暫無資料")`, `st.error()`, `st.warning()`). No standardized empty state design. Every competitor has a consistent empty state — same icon, same message style, same layout.
- **Affected Pages**: All pages
- **Proposed Fix**: Create a shared `_empty_state()` component in `_router_base.py` with icon + title + optional subtitle. Replace all ~15-20 inline empty-state messages across pages.
- **Effort**: 1h
- **Competitor Benchmark**: Robinhood (friendly illustration + message), 富邦e富 (clean card with icon)

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
- **Status**: ✅ RESOLVED in Sprint 6 — `background:#F5F5F5` → `background:#F8F9FA` in `_router_base.py` line 91. Commit: b197764.

### D-038: C41 Calls API in View Layer
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14
- **Description**: C41's `_render_business_card` calls `client.get_stock_info()` directly in the view layer (line 505). This violates the architecture principle that the view layer should not make API calls — data should be fetched in the router and passed via `data` dict. This also means the API call happens on every render, not just on page load.
- **Affected Lines**: `business_card.py` lines 505-512
- **Proposed Fix**: Move the peer stock fetching to `get_stock_data()` in `_router_base.py` (add a `"peers"` key to the data dict), or accept peers as a parameter.
- **Effort**: 1-2h

### D-039: No Standardized Section Header Pattern
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 15
- **Description**: The business card page has 15+ sections with 3 different header styles (markdown `###`, `st.expander`, inline HTML). As Sprint 5 adds C71/C73/C74 sections, this inconsistency will worsen.
- **Affected Files**: `src/pages/business_card/_sections.py` (all section functions)
- **Proposed Fix**: Create `_section_header(icon, title, collapsed=False)` helper in `_helpers.py`. Use `st.expander` when collapsed=True, `st.markdown(f"### {icon} {title}")` otherwise.
- **Effort**: 1-2h

### D-040: No Standardized Disclaimer Component
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 15
- **Description**: C73 (Expert Analysis) and C74 (Historical Scenarios) both require historian positioning disclaimers. Currently written inline. Inconsistent disclaimer text could create regulatory risk in TW financial content.
- **Affected Files**: C73 and C74 implementations (Sprint 5)
- **Proposed Fix**: Create `_historian_disclaimer(type)` helper returning standardized disclaimer text. Types: 'expert', 'scenario', 'general'. Use `st.caption()` for rendering.
- **Effort**: 0.5h

### D-041: No Sprint 5 Card Components (D-003 Regression Risk)
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 15
- **Description**: C71, C73, and C74 will each add new card types to the business card page. Without standardized components, these will likely use inline HTML (continuing D-003). This is the single most important P2 item to resolve before Sprint 5 coding starts.
- **Affected Files**: C71/C73/C74 implementations (Sprint 5)
- **Proposed Fix**: Before Sprint 5 feature implementation, create `_study_card()`, `_expert_card()`, `_scenario_card()` in `_router_base.py` or `ui_components.py`. Follow design system specs for colors and spacing.
- **Effort**: 1h
- **Status**: 🔴 **Sprint 5 PREREQUISITE** — must complete before any C71/C73/C74 implementation

### D-042: Health Dimension Mini-Cards Use Non-Standard Styling
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 16
- **Description**: The 5-dimension score cards in `_render_health()` (lines 227-236 of `_sections.py`) use inline HTML with `padding:0.5rem`, `border-radius:10px`, and no `border-left`. This differs from the design system's card spec (`padding:1.2rem`, `border-radius:12px`, `border-left:4px solid`). While the compact style is appropriate for the 5-column layout, it creates a visual mismatch with all other cards on the page.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 227-236
- **Proposed Fix**: Create a `_mini_score_card(label, score, indicator, color)` helper in `_router_base.py` with standardized compact styling. This would be a recognized "mini card" variant in the design system.
- **Effort**: 0.5h

### D-043: Dividend History Table Uses Inline HTML Instead of st.dataframe
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 16
- **Description**: The dividend history table in `_render_dividend()` (lines 420-439 of `_sections.py`) builds a complete HTML table from scratch with inline styles. This bypasses Streamlit's `st.dataframe()` which provides sorting, filtering, and responsive behavior. The inline HTML table also uses `border-bottom:1px solid #F8F9FA` which is nearly invisible on white backgrounds.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 420-439
- **Proposed Fix**: Build the badge list as a separate column, then use `st.dataframe()` with column config for badges. Or, if HTML is kept, use `border-bottom:1px solid #BDC3C7` for visible row separators.
- **Effort**: 1-2h

### D-044: C41 Read Next Header Doesn't Use _section_title() Helper
- **Severity**: P2
- **Added**: 2026-06-20
- **Source**: Design Review Round 16
- **Description**: `_render_read_next()` at line 549 uses raw `st.markdown("### 📖 推薦閱讀")` instead of the `_section_title()` helper from `_router_base.py`. This means the header doesn't get the emoji-prefix detection and consistent formatting that `_section_title()` provides.
- **Affected Files**: `src/pages/business_card/_sections.py` line 549
- **Proposed Fix**: Replace with `_section_title("📖 推薦閱讀")`.
- **Effort**: <0.5h (one-line change)

### D-045: C51 Sector Grid and Top Movers Use Inline HTML with Non-Standard Styling
- **Severity**: P2
- **Added**: 2026-06-21
- **Source**: Design Review Round 17
- **Description**: The sector grid cells in `_render_sector_grid()` (lines 342-362) and top-mover rows in `_render_top_movers()` (lines 391-444) of `sector_heatmap.py` use inline HTML with non-standard styling. Grid cells use `padding:1rem` (vs design system `1.2rem`). Top-movers use `border-radius:10px` (vs `12px`) and `padding:0.7rem 1rem` (vs `1.2rem`). This creates a third distinct card style on the sector heatmap page.
- **Affected Files**: `src/pages/sector_heatmap.py` lines 342-362, 391-444
- **Proposed Fix**: Create `_sector_grid_card()` and `_mover_row()` helpers, or adapt existing `_info_card()` / `_白话_card()` for these use cases. If compact style is intentional, document as "compact card" variant in design system.
- **Effort**: 1-2h

### D-046: C51 4th KPI Card Uses Inline HTML Instead of _白话_card()
- **Severity**: P2
- **Added**: 2026-06-21
- **Source**: Design Review Round 17
- **Description**: The first 3 KPI cards on the sector heatmap page (lines 175-192) correctly use `_白话_card()`, but the 4th card (漲跌產業數, lines 195-201) uses inline HTML with manually specified styling.
- **Affected Files**: `src/pages/sector_heatmap.py` lines 195-201
- **Proposed Fix**: Replace with `_白话_card()` call for consistency.
- **Effort**: <0.5h (one-line replacement)

### D-047: C53-1 Share Section Header Doesn't Use _section_title()
- **Severity**: P2
- **Added**: 2026-06-21
- **Source**: Design Review Round 17
- **Description**: `_render_share_section()` at line 832 uses raw `st.markdown("### 🔗 分享這張名片")` instead of `_section_title()`. Same pattern as D-044.
- **Affected Files**: `src/pages/business_card/_sections.py` line 832
- **Proposed Fix**: Replace with `_section_title("🔗 分享這張名片")`.
- **Effort**: <0.5h (one-line change)

### D-048: C53-1 Share Button Uses st.html() with Non-Functional JS
- **Severity**: P2
- **Added**: 2026-06-21
- **Source**: Design Review Round 17
- **Description**: The social sharing copy button uses `st.html()` with raw JavaScript (lines 875-910 of `_sections.py`). The JS references `document.getElementById('share-url-input')` which Streamlit doesn't render — making the copy button non-functional. This is the first use of `st.html()` for a UI component in the project.
- **Affected Files**: `src/pages/business_card/_sections.py` lines 875-910
- **Proposed Fix**: Replace with pure Streamlit approach: `st.text_input(disabled=True)` + `st.button("📋 複製")` with `st.toast()` feedback. Create `_share_button()` helper in `_router_base.py`.
- **Effort**: 1-2h (includes functional fix for non-working feature)

### D-049: C84 Key Metrics Cards Use Inline HTML Instead of _白话_card() (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 20
- **Description**: The Key Metrics section in `market_event_case_study.py` (lines 109-117) uses inline HTML with `unsafe_allow_html=True` instead of the shared `_白话_card()` component. The inline HTML is a near-exact copy of `_白话_card()`'s styling (`background:#F8F9FA`, `border-radius:12px`, `padding:1.2rem`, `border-left:4px solid #3498DB`). This is a textbook D-003 regression — the developer duplicated the card style inline rather than using the shared component.
- **Affected Files**: `src/pages/market_event_case_study.py` lines 109-117
- **Proposed Fix**: Replace the inline HTML block with `_白话_card(label, value, analogy)` calls. The data structure already matches the `_白话_card` API (label, value, analogy fields).
- **Effort**: <0.5h (direct replacement)

### D-050: C84 Related Stocks Cards Use Non-Standard Card Styling (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 20
- **Description**: The Related Stocks section in `market_event_case_study.py` (lines 143-157) uses inline HTML with `background:white` and `border:1px solid #ECF0F1` instead of the standard card styling (`background:#F8F9FA`, `border-left:4px solid`). This creates a third card style on the page (alongside `_info_card` and the key metrics inline cards). The white background with light gray border is nearly invisible and doesn't match any design system card variant.
- **Affected Files**: `src/pages/market_event_case_study.py` lines 143-157
- **Proposed Fix**: Either (a) create a `_related_stock_card()` helper in `_router_base.py` with standard card styling + button, or (b) use `_info_card()` with the stock name/impact as content and the button below.
- **Effort**: 0.5-1h

### D-051: ETF Browser Table-Like Rows Use Inline HTML for Colored Values (D-003 / D-010 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 20
- **Description**: The Hot ETF rows (lines 145-155) and Dividend Ranking rows (lines 397-411) in `etf_browser.py` use `st.columns` with inline HTML (`<span style='color:...'>`) for colored change values. This is the same table-like layout pattern flagged in D-010 (watchlist page). The ETF browser is now the second page using this dense table layout, making it feel like a different product from the card-based PPT-style pages.
- **Affected Files**: `src/pages/etf_browser.py` lines 145-155, 397-411
- **Proposed Fix**: Redesign using card-based layout. Each ETF as a card with key info (name, price, change) and a "查看" button. Use `_info_card()` for the card container and colored text via markdown emoji (🔴/🟢) instead of inline HTML color spans.
- **Effort**: 2-3h

### D-052: _subsidiary_card() Uses Non-Standard Card Styling
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 20
- **Description**: The new `_subsidiary_card()` helper in `_router_base.py` (lines 117-151) uses `background:white` and `border:1px solid #ECF0F1` instead of the design system's standard card styling (`background:#F8F9FA`, `border-left:4px solid #3498DB`). While the white background may be intentional to distinguish subsidiary cards from info cards, this creates a new card style variant not documented in the design system. The component also uses `display:flex` for layout, which is a departure from the simple stacked div pattern used by all other card components.
- **Affected Files**: `src/pages/_router_base.py` lines 117-151
- **Proposed Fix**: Either (a) change to standard card styling (`background:#F8F9FA`, `border-left:4px solid`) and document as a "subsidiary card" variant, or (b) add a `card_type="subsidiary"` parameter to a unified card component. If the white background is intentional, document it in the design system.
- **Effort**: 0.5-1h

### D-053: _count_label() Is an Undocumented Component Type
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 20
- **Description**: The new `_count_label()` helper in `_router_base.py` (lines 154-164) renders a bare `<div>` with inline styling (`color:#7F8C8D`, `font-size:0.85rem`). This is a new component type (muted count label) that isn't documented in the design system. While simple, it establishes a precedent for adding one-off inline-styled components to `_router_base.py` without design system documentation. The component is used in `etf_browser.py` (line 83) and could be needed elsewhere.
- **Affected Files**: `src/pages/_router_base.py` lines 154-164
- **Proposed Fix**: Document `_count_label()` as a "muted label" component type in the design system. Consider whether this should be a full component with standardized margins/padding matching other components.
- **Effort**: 0.5h

### D-062: Quiz Result Detail Cards Use Inline HTML (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The per-question result cards in `comprehension_check.py` (lines 151-166) use `unsafe_allow_html=True` with manually constructed HTML divs showing ✅/❌ status, question text, and explanation. This is a new "quiz result card" type that should be a shared component in `_router_base.py`. The card uses `border-left:4px solid #27AE60` (correct) or `#E74C3C` (incorrect) which matches the design system's positive/negative colors, but the implementation is duplicated inline rather than using a component.
- **Affected Files**: `src/pages/comprehension_check.py` lines 151-166
- **Proposed Fix**: Create `_quiz_result_card(is_correct, question_text, explanation)` in `_router_base.py`. Add to design system as "quiz result card" variant.
- **Effort**: 0.5-1h

### D-063: Quiz Score Color Logic in View Layer
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The score color/emoji/title/desc logic (percentage → color mapping) is hardcoded in `comprehension_check.py` lines 110-124. If this pattern is reused in future quiz features, it will be duplicated. The color thresholds (80%/60%) should be consistent across all quiz instances.
- **Affected Files**: `src/pages/comprehension_check.py` lines 110-124
- **Proposed Fix**: Move to a helper `_get_score_style(percentage)` returning `(color, emoji, title, desc)` dict.
- **Effort**: <0.5h

### D-064: Key Concept Line Uses Inline HTML (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The "💡 核心概念" line in `event_dashboard.py` (lines 110-115) uses inline HTML (`font-size:0.85rem;color:#5D6D7E`). This is a muted text style that should use `st.caption()` or a shared `_key_concept()` helper instead of inline HTML.
- **Affected Files**: `src/pages/event_dashboard.py` lines 110-115
- **Proposed Fix**: Replace with `st.caption()` or create `_key_concept(text)` helper in `_router_base.py`.
- **Effort**: <0.5h

### D-065: Disclaimer Text Uses Inline HTML (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The historian disclaimer in `event_dashboard.py` (lines 133-137) uses inline HTML (`font-size:0.8rem;color:#95A5A6`). This is the same disclaimer pattern as `_historian_disclaimer()` in `_helpers.py` which uses `st.caption()`. The inline HTML creates inconsistency.
- **Affected Files**: `src/pages/event_dashboard.py` lines 133-137
- **Proposed Fix**: Replace with `st.caption()` or call `_historian_disclaimer("event")`.
- **Effort**: <0.5h

### D-066: Adaptive Banner Uses Inline HTML (Pre-existing)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The adaptive analysis framework banner in `event_dashboard.py` (lines 193-204) uses inline HTML with `background:#EBF5FB` and `border-left:4px solid #3498DB`. This is functionally identical to `_info_card()` but implemented as inline HTML. Pre-existing — not introduced by Sprint 9.
- **Affected Files**: `src/pages/event_dashboard.py` lines 193-204
- **Proposed Fix**: Replace with `_info_card(title=..., content=..., icon="🎯")`.
- **Effort**: <0.5h

---

## Resolved Issues

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| D-001 | No Visual Health Score | P0 | 2026-06-17 | C43 (Snowflake Health Visualization) fully implemented with 5-dimension radar chart, color-coded scores, reference lines, and plain-language health summary. |
| D-002 | No Synthesis Layer | P0 | 2026-06-17 | C37 (Key Takeaways) implemented with curated templates for top 20 stocks and auto-generated fallback for others. |
| D-013 | No Risk Analysis Section | P2 | 2026-06-19 | C44 (Risk Analysis MVP) implemented with 3 dimensions (customer concentration, financial health, event-based) using `st.expander` progressive disclosure. |
| D-014 | No Valuation Context | P2 | 2026-06-17 | C45 (Valuation Band Chart) implemented with historical PER percentile band, current PER marker, and plain-language interpretation. |
| D-016 | C37 Missing Orange/Amber Hero Card Style | P1 | 2026-06-18 | `_summary_card()` created with `#F39C12` border and `#FFF8F0` background. C37 now uses this component, making it the distinctive "hero card" of the page. |
| D-017 | C37 Bullet Count Exceeds Spec | P2 | 2026-06-18 | Cap changed from `[:5]` to `[:3]` in `analogy_engine.py` line 423. |
| D-018 | C39 Placement Too Low on Page | P1 | 2026-06-18 | C39 moved from after 關鍵數字三連卡 to directly after C37 (line 164). Page flow now: summary → what changed → health → details. |
| D-019 | C39 Missing Delta Count Cap | P2 | 2026-06-18 | `return deltas[:2]` added at `analogy_engine.py` line 508. |
| D-020 | C39 Missing Directional Color Coding | P2 | 2026-06-18 | Green (`#27AE60`) / red (`#E74C3C`) color spans added to delta text in `business_card.py` lines 176-179. |
| D-022 | C43 Placement Not Near Top of Page | P2 | 2026-06-18 | C43 now appears as 3rd content section (line 184), after C37 and C39. |
| D-023 | C45 Uses 2-Year Window Instead of 5-Year | P2 | 2026-06-18 | Extended to 5-year window (1825 days) with graceful fallback for insufficient data. |
| D-024 | _info_card Uses Wrong Background Color | P1 | 2026-06-19 | Changed `background:#FFF8F0` to `background:#F8F9FA` in `_router_base.py` line 110. |
| D-025 | C39 Missing Empty State Message | P2 | 2026-06-19 | Added `else` branch showing `_info_card("最近有什麼變化", "近期無顯著變化，所有指標波動均在 10% 以內", "🔄")` when no deltas exceed threshold. |
|| D-034 | C3 Metric Value Tooltips Missing from Hover and Cards | P1 | 2026-06-12 | Enhanced `create_health_snowflake()` with optional `metric_values` param. Hover now shows raw metric values as bullet points. Dimension cards display values in blue text. `_get_health_metric_values()` helper added to `_helpers.py`. Commit: 4de8b8e. |
|| D-004 | No Design System Documentation | P1 | 2026-06-19 | `docs/design/design_system.md` now exists at expected path (copied from `docs/domain/design_system.md` in Sprint 4). |
|| D-021 | C43 Missing Per-Dimension Plain-Language Explanations | P1 | 2026-06-19 | Resolved via D-034 fix — metric values now shown in both hover template and dimension cards with raw numbers and plain-language explanations. |

---

## Statistics

- **Total Issues**: 48
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006)
- **P2 (Optimization)**: 35 (D-007, D-008, D-009, D-010, D-011, D-012, D-015, D-032, D-033, D-035, D-036, D-038, D-039, D-040, D-041, D-042, D-043, D-045, D-048, D-049, D-050, D-051, D-052, D-053, D-057, D-058, D-059, D-062, D-063, D-064, D-065, D-066)
- **Resolved**: 19

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 10 feature implementation.*

---

# Round 21 Design Assessment (2026-06-13, after Sprint 8 Completion)

> **Reviewer**: Design Reviewer
> **Scope**: Sprint 8 debt clearance verification, competitor design comparison, Sprint 9 design prerequisites
> **Sprint 8 Changes Verified**: D-048 (YAML migration), D-055 (sector_heatmap inline HTML removed), D-056 (_section_title bug fixed), D-050 (market_event_case_study already clean)

---

## 1. Design Grade Assessment

### Recommendation: **A- → A** (upgrade back to A)

**Justification:**

Sprint 8 was a debt-first sprint that directly addressed the Round 20 downgrade rationale. The A- grade was assigned because the "No Inline HTML" rule was unenforceable and new inline HTML kept appearing. Sprint 8 made significant progress:

**Positive changes verified:**
1. **D-055 (sector_heatmap.py inline HTML removed)**: Confirmed. The sector grid (`_render_sector_grid`) now uses `_白话_card()` instead of inline HTML grid cells. The top movers (`_render_top_movers`) now uses `_render_mover_row()` with pure Streamlit-native components (`st.text`, `st.markdown`, `st.caption`) instead of inline HTML rows. All 4 KPI cards now use `_白话_card()`. The file went from 150+ lines of inline HTML to zero. This is the single biggest design improvement in Sprint 8.

2. **D-056 (_section_title() inverted logic bug fixed)**: Confirmed. The `_section_title()` in `_router_base.py` (line 69) now correctly detects emoji-first titles using Unicode range checks and skips adding a redundant 📊 prefix. The `_helpers.py` version (line 113) provides a simpler `(icon, title)` signature for business_card sections. Both versions now work correctly.

3. **D-048 (_CASE_STUDIES → YAML)**: The `market_event_service.py` hardcoded `_CASE_STUDIES` dict (230 lines) was extracted to `case_studies.yaml`. No UI impact, but eliminates a D6 architecture violation and enables content scaling without code changes.

4. **D-050 (market_event_case_study.py inline HTML)**: Confirmed already clean — the page now uses `_白话_card()` for key metrics, `_subsidiary_card()` for related stocks, and `_info_card()` for the historian disclaimer. Zero inline HTML in the page file.

**Remaining concerns (not grade-blocking):**
- D-052: `_subsidiary_card()` still uses `background:white; border:1px solid #ECF0F1` — non-standard card styling. However, this is a deliberate design choice (white background distinguishes subsidiary cards from info cards) and is now the established pattern used by both `group_structure.py` and `market_event_case_study.py`. Should be documented as a "subsidiary card" variant in the design system.
- D-053: `_count_label()` remains undocumented but is a minor utility component.
- D-003: `watchlist_page.py`, `etf_detail.py`, `business_card.py` C41/C44 still have inline HTML. These are pre-existing issues, not Sprint 8 regressions.

**Net assessment**: The inline HTML enforcement gap that caused the A- downgrade has been substantially closed. Sprint 8 removed more inline HTML than it added. The design system components (`_白话_card`, `_info_card`, `_summary_card`, `_subsidiary_card`) are now used consistently across 6+ pages. The grade returns to **A** with the caveat that continued vigilance is needed to prevent regressions.

**Grade trajectory**: A (R19) → A- (R20, inline HTML gap) → **A (R21, gap closed)**

---

## 2. Competitor Design Comparison (Top 5 Most Relevant)

### Selected Competitors (from 90 analyzed across all rounds)

The 5 most relevant competitors for design comparison, based on overlap with Stock Explorer's "beginner education + historian positioning":

| # | Competitor | Relevance | Key Design Insight |
|---|-----------|-----------|-------------------|
| 1 | **Finimize** | 🔴 Highest | Daily briefing + quiz model; ELI5 toggle; streak gamification |
| 2 | **Stash** | 🔴 High | "Learn Before Invest" gate; 8th-grade reading level; tappable glossary |
| 3 | **Simply Wall St** | 🔴 High | Visual-first infographic style; snowflake analysis; progressive disclosure |
| 4 | **SoFi Invest** | 🟡 Medium | Structured curriculum (300+ articles); progress tracking; video content |
| 5 | **Public.com** | 🟡 Medium | Story cards per stock; key takeaways; social learning |

### Design Pattern Comparison

**How Stock Explorer's PPT-style design compares:**

| Design Dimension | Stock Explorer | Competitors |
|-----------------|---------------|-------------|
| **Layout** | PPT-style, one key point per page | Most use dashboard/grid layouts |
| **Card System** | 4 card types (info, 白话, summary, subsidiary) | Simply Wall St has similar card variety |
| **Plain-Language** | Core feature (analogies on every metric) | Stash (8th-grade), Finimize (ELI5 toggle) |
| **Visual-First** | Charts > 60% of page area | Simply Wall St matches this approach |
| **Quiz/Assessment** | ❌ Not built (C101 planned) | Finimize, SoFi, eToro all have quizzes |
| **Onboarding** | ❌ Not built (C103 planned) | Stash gates first use behind education |
| **Complexity Toggle** | ❌ Not built (C105 planned) | Finimize has ELI5 toggle |
| **Gamification** | ❌ Not built (C50, C60 planned) | Finimize (streaks), eToro (badges) |
| **Mobile** | ⚠️ Streamlit limitations | All competitors have native apps |

### Patterns Competitors Use That We Should Adopt

1. **Finimize's "Quiz After Story" pattern**: After each content piece, embed 1-3 comprehension questions with immediate feedback. This is the #1 pattern to adopt for C101. Finimize proves it drives engagement and learning retention.

2. **Stash's "Learn Before Invest" gate**: Force a brief educational module before first use. For Stock Explorer, this translates to C103 (First Visit Gate) — show 2 cards explaining "what is a stock" and "how to read this page" before letting users explore freely.

3. **Finimize's ELI5 Toggle**: A simple toggle between "simple" and "detailed" views. Stock Explorer's C105 should implement this as a session-state toggle that shows/hides advanced sections.

4. **Simply Wall St's Progressive Disclosure**: Summary first, details on click. Stock Explorer's business card page should adopt this more aggressively — show the hero summary card by default, collapse everything else.

5. **Stash's Tappable Glossary**: Every financial term is tappable for a 1-sentence definition. Stock Explorer's C33 (Beginner Glossary) should implement this as hover tooltips or click-to-expand definitions.

### Patterns We Have That Competitors Don't (Unique Value)

1. **PPT-style presentation**: No competitor uses a true "one key point per page" approach. Simply Wall St comes closest with infographic-style pages, but still shows more content per page.

2. **Plain-language analogies on every metric**: Stock Explorer's analogy engine provides contextual explanations for every financial metric. No competitor has this level of systematic plain-language translation.

3. **Historian positioning**: Stock Explorer is the only platform that explicitly commits to "explain what happened, never advise buy/sell." This is a unique brand differentiator that competitors like eToro (copy trading) and SoFi (robo-advisor) directly contradict.

4. **Point-to-point group structure**: Parent-subsidiary mapping with ownership % is more detailed than any competitor's group structure visualization.

5. **TW market focus with educational positioning**: All TW competitors (StatementDog, GoodInfo, CMoney) target intermediate/advanced investors. Stock Explorer is the only TW platform targeting beginners with a structured educational approach.

### Mobile UX Comparison

Stock Explorer's mobile UX is its weakest dimension. All 5 comparison competitors have native mobile apps with:
- Native navigation (bottom tab bars, swipe gestures)
- Push notifications
- Optimized touch targets
- Offline reading

Stock Explorer is limited by Streamlit's responsive CSS. The current media queries (768px, 600px) only adjust padding and font sizes. Multi-column layouts don't stack gracefully. This is a known limitation (D-006) that cannot be fully resolved without moving away from Streamlit.

**Recommendation**: For the current Streamlit-based architecture, add a mobile-specific CSS rule that forces all `st.columns` to stack vertically below 768px, and increase touch target sizes to 44px minimum. This is a 2-3h effort that would significantly improve mobile UX.

---

## 3. Sprint 9 Design Prerequisites

### C98: Event Interpretation Cards

**Purpose**: Replace the current event dashboard's disconnected list with interpreted "story cards" that explain what happened and why it matters.

**Design Spec**:

```
┌─────────────────────────────────────────────────┐
│  📅 2026年1月15日                                │
│  ┌───────────────────────────────────────────┐  │
│  │  🔴 重大事件                               │  │
│  │  「台積電法說會展望不如預期」                 │  │
│  │                                           │  │
│  │  發生了什麼：                               │  │
│  │  台積電在法說會中給出的營收展望低於分析師     │  │
│  │  預期，導致股價當日下跌 3.2%。               │  │
│  │                                           │  │
│  │  為什麼重要：                               │  │
│  │  台積電佔台股加權指數權重約 30%，其股價      │  │
│  │  波動會直接影響大盤走勢。                    │  │
│  │                                           │  │
│  │  📊 關鍵數據：                              │  │
│  │  ┌─────────────┬─────────────┐            │  │
│  │  │ 股價變化     │ 成交量變化   │            │  │
│  │  │ 🔴 -3.2%    │ 🟡 +45%     │            │  │
│  │  └─────────────┴─────────────┘            │  │
│  │                                           │  │
│  │  💡 歷史學家說：                            │  │
│  │  「這不是台積電基本面的改變，而是市場預期    │  │
│  │   的調整。過去 5 年，台積電法說會後股價      │  │
│  │   波動超過 3% 的情況發生了 8 次。」          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  [📖 深入了解此事件]  [📊 查看相關個股]          │
└─────────────────────────────────────────────────┘
```

**Components from design system**:
- Card container: `_info_card()` variant with date header
- Severity badge: `_severity_badge()` (already exists in market_event_case_study.py)
- Key metrics: `_白话_card()` in 2-column layout
- Historian quote: `_summary_card()` with `#FFF8F0` background
- Action buttons: `st.button()` with `use_container_width=True`

**Interaction pattern**:
- Cards are displayed in reverse chronological order (newest first)
- Each card is collapsed by default (showing only date + title + severity)
- Click to expand for full interpretation
- "深入了解" button navigates to the full case study (C84)
- "查看相關個股" navigates to the business card page for the most affected stock

**Layout**: Zone C (main content area), one card per event, max 5 cards visible with "載入更多" button.

---

### C101: Quiz UI (Comprehension Check)

**Purpose**: Verify users understand what they just read. Replace C52 (Quiz Mode).

**Design Spec — Inline Card Pattern (Finimize Model)**:

```
┌─────────────────────────────────────────────────┐
│  ✅ 你已經讀完了「公司基本資料」                  │
│                                                 │
│  📝 快速測驗                                     │
│                                                 │
│  問題 1/3                                       │
│  「ROE 15%」代表什麼意思？                       │
│                                                 │
│  ○ A. 公司每年營收成長 15%                       │
│  ○ B. 每 100 元股東資金賺 15 元                 │
│  ○ C. 公司負債佔資產的 15%                       │
│                                                 │
│  [提交答案]                                      │
│                                                 │
│  ── After submission: ──                        │
│  ✅ 答對了！                                     │
│  ROE（股東權益報酬率）衡量的是公司運用股東      │
│  資金的效率。15% 表示每投入 100 元，公司每年     │
│  賺 15 元。                                     │
│                                                 │
│  [下一題 →]                                      │
└─────────────────────────────────────────────────┘
```

**Components from design system**:
- Card container: `_summary_card()` with green border (`#27AE60`) for correct, red border (`#E74C3C`) for incorrect
- Question text: `st.markdown()` with `**bold**`
- Options: `st.radio()` with custom styling
- Submit button: `st.button()` with `use_container_width=True`
- Feedback: `st.success()` / `st.error()` with explanation text
- Progress: `st.progress(current / total)`

**Interaction pattern**:
- Quiz card appears at the end of each major section (after Key Takeaways, after Company Story, after Risk Analysis)
- 1 question per section, 3-4 questions total per stock page
- Questions are contextual to the section just read
- Immediate feedback after each answer (no delayed grading)
- "Why?" explanation always shown after answering
- Completion badge: "✅ 3/4 個區段已理解" shown at bottom of page
- Progress stored in `session_state["quiz_progress_{stock_id}"]`

**Layout**: Inline card (not modal, not bottom card). Appears as a natural part of the page flow, after the section content. This is critical — a modal would break the PPT-style flow; a bottom card would be missed.

**Alternative considered and rejected**:
- Modal: Breaks PPT-style flow, feels like an interruption
- Bottom card: Would be missed by users who don't scroll to the end
- Standalone quiz page: Too disconnected from the learning context

---

### C103 Lite: First Visit Guide

**Purpose**: Onboard first-time users with a 2-card guided tour before they explore freely.

**Design Spec**:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  👋 歡迎來到股識！                          │  │
│  │                                           │  │
│  │  這是一個「認識公司」的工具，不是投資建議。  │  │
│  │                                           │  │
│  │  我們用歷史學家的角度，告訴你：              │  │
│  │  • 這家公司是做什麼的                        │  │
│  │  • 它最近發生了什麼事                        │  │
│  │  • 它的財務狀況如何                          │  │
│  │                                           │  │
│  │  我們不會告訴你「該買」或「該賣」。          │  │
│  │                                           │  │
│  │  [繼續 →]                                  │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ── After clicking "繼續": ──                   │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  📖 怎麼使用這個工具？                      │  │
│  │                                           │  │
│  │  1️⃣ 在左側搜尋公司名稱或股票代碼            │  │
│  │  2️⃣ 查看「公司名片」了解基本資料            │  │
│  │  3️⃣ 點擊分頁查看更多資訊                    │  │
│  │  4️⃣ 看到不懂的名詞？點擊 ❓ 查看解釋        │  │
│  │                                           │  │
│  │  💡 小提示：從「台積電 (2330)」開始，      │  │
│  │     這是台灣最大的上市公司。                │  │
│  │                                           │  │
│  │  [開始探索 🚀]    [跳過導覽]               │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Components from design system**:
- Card container: `_summary_card()` with `#FFF8F0` background (tip/warning style)
- Title: `_section_title()` or `st.markdown("## ...")`
- Content: `st.markdown()` with bullet points
- Buttons: `st.button()` with `use_container_width=True`
- Dismiss: "跳過導覽" as `st.button()` with `type="secondary"`

**Interaction pattern**:
- Triggered on first visit only (check `session_state["first_visit"]`)
- Card 1: Positioning (what this tool is / is not)
- Card 2: How to use (4 steps + tip)
- "開始探索" dismisses the guide and sets `session_state["first_visit"] = False`
- "跳過導覽" dismisses immediately
- Guide does NOT auto-advance — user must click "繼續" to proceed
- If dismissed, never shown again (stored in session state)
- Optional: Add a "?" button in the sidebar that re-triggers the guide

**Layout**: Full-width cards in Zone C (main content area). The guide replaces the normal page content for first-time users. After dismissal, the normal page content is shown.

**Dismissible behavior**:
- Dismissal is permanent (per session)
- No "Are you sure?" confirmation — one click to dismiss
- No countdown or forced reading time
- Progress indicator: "卡片 1/2" shown as `st.caption()`

---

## 4. New Design Issues Identified

### D-057: Duplicate _section_title() Functions with Inconsistent Signatures
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 21
- **Description**: There are two `_section_title()` functions in the codebase:
  - `_router_base.py` line 69: `def _section_title(title: str)` — takes a single string, auto-detects emoji prefix
  - `_helpers.py` line 113: `def _section_title(icon: str, title: str)` — takes icon and title separately
  
  The `_helpers.py` version is imported by `market_event_case_study.py` (line 13) and `business_card/_sections.py`. The `_router_base.py` version is imported by `sector_heatmap.py`. This creates confusion about which version to use and risks inconsistent rendering. The `_helpers.py` version doesn't have the emoji auto-detection logic.
- **Affected Files**: `_router_base.py` line 69, `_helpers.py` line 113
- **Proposed Fix**: Consolidate into a single function in `_router_base.py` with signature `def _section_title(title: str = "", icon: str = "", subtitle: str = "")` that handles both cases. Update all imports.
- **Effort**: 0.5-1h

### D-058: _render_related_stock_card() Misuses _subsidiary_card() for Non-Subsidiary Stocks
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 21
- **Description**: The `_render_related_stock_card()` function in `market_event_case_study.py` (line 29) uses `_subsidiary_card()` to render related stocks for market events. However, these are NOT subsidiaries — they are stocks affected by the same event. The `_subsidiary_card()` component shows "持股 X%" and "營收 X%" fields which are meaningless for event-related stocks (passing 0 for both). This is a semantic misuse of the component that could confuse future developers.
- **Affected Files**: `market_event_case_study.py` lines 29-39
- **Proposed Fix**: Create a dedicated `_event_stock_card(stock_id, stock_name, impact)` helper that renders a card with the stock info and impact description without the holding/revenue fields. Use `_info_card()` as the base if the card is simple enough.
- **Effort**: 0.5-1h

### D-059: _section_title() in market_event_case_study.py Passes Separate Icon/Title Instead of Combined String
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 21
- **Description**: `market_event_case_study.py` calls `_section_title("📖", "發生了什麼事")` (two args) while `sector_heatmap.py` calls `_section_title("📊 關鍵數據")` (one arg). This works because they're different functions (see D-057), but it creates an inconsistent calling convention across the codebase.
- **Affected Files**: `market_event_case_study.py` lines 95, 107, 127, 136, 163
- **Proposed Fix**: Resolve as part of D-057 consolidation.
- **Effort**: Included in D-057

### Verification of D-049 through D-053 (from Round 20):

| ID | Description | Status | Notes |
|----|------------|--------|-------|
| D-049 | C84 Key Metrics inline HTML | ✅ **RESOLVED** | `market_event_case_study.py` now uses `_白话_card()` for key metrics (line 123). Zero inline HTML in this section. |
| D-050 | C84 Related Stocks non-standard cards | ⚠️ **PARTIALLY RESOLVED** | Now uses `_subsidiary_card()` (via `_render_related_stock_card()`), but this is a semantic misuse (see D-058). The card styling is now consistent, but the component is semantically wrong. |
| D-051 | ETF Browser inline HTML | ❌ **STILL OPEN** | `etf_browser.py` still has inline HTML for colored change values (lines 145-155, 397-411). Not addressed in Sprint 8. |
| D-052 | _subsidiary_card() non-standard styling | ❌ **STILL OPEN** | `_subsidiary_card()` still uses `background:white; border:1px solid #ECF0F1`. This is now an established pattern but should be documented. |
| D-053 | _count_label() undocumented | ❌ **STILL OPEN** | `_count_label()` remains undocumented in the design system. |

---

## 5. Design System Update Recommendations

The design system (`docs/design/design_system.md`) needs the following updates to reflect Sprint 8 changes and prepare for Sprint 9:

### 5.1 New Component: Subsidiary Card (Document Existing)

Add to Section 3.3 Cards:

```html
<!-- Subsidiary card (white background, flex layout) -->
<div style="background:white;border-radius:12px;padding:1.5rem;border:1px solid #ECF0F1;margin:0.8rem 0;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <span style="font-size:1.1rem;font-weight:700;color:#2C3E50;">{name}</span>
            <span style="background:{color}15;color:{color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;font-weight:600;margin-left:0.5rem;">{badge}</span>
        </div>
        <div style="text-align:right;">
            <span style="font-size:0.85rem;color:#7F8C8D;">{holding_label}</span>
        </div>
    </div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{business}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{relation}</div>
</div>
```

**Rationale**: The white background distinguishes subsidiary cards from info cards (which use `#F8F9FA`). This is intentional — subsidiary cards are "entity cards" while info cards are "content cards."

### 5.2 New Component: Count Label (Document Existing)

Add to Section 3.3 Cards:

```html
<!-- Muted count label -->
<div style="color:#7F8C8D;font-size:0.85rem;">{count} {label}</div>
```

**Usage**: Below card grids to show "共 X 個" or "顯示 X / Y 個".

### 5.3 New Component: Summary Card (Document Existing)

The `_summary_card()` component (orange border, `#FFF8F0` background) is already in `_router_base.py` but not in the design system. Add:

```html
<!-- Summary/hero card (orange border) -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{content}</div>
</div>
```

### 5.4 New Component: Event Interpretation Card (C98 — New for Sprint 9)

Add to Section 3.3 Cards:

```html
<!-- Event interpretation card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;border-left:4px solid #E74C3C;margin:0.8rem 0;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:0.85rem;color:#7F8C8D;">{date}</span>
        <span style="background:{severity_color}15;color:{severity_color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;">{severity_badge}</span>
    </div>
    <div style="font-size:1.1rem;font-weight:700;color:#2C3E50;margin-top:0.3rem;">{title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{what_happened}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{historian_quote}</div>
</div>
```

### 5.5 New Component: Quiz Card (C101 — New for Sprint 9)

Add to Section 3.3 Cards:

```html
<!-- Quiz/Comprehension check card -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">📝 快速測驗</div>
    <div style="font-size:0.85rem;color:#7F8C8D;">問題 {current}/{total}</div>
    <div style="font-size:0.95rem;color:#2C3E50;margin-top:0.5rem;font-weight:600;">{question}</div>
    <!-- Options rendered via st.radio() -->
    <!-- Feedback rendered via st.success()/st.error() -->
</div>
```

### 5.6 New Component: First Visit Guide Card (C103 — New for Sprint 9)

Add to Section 3.3 Cards:

```html
<!-- First visit onboarding card -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.5rem;border-left:4px solid #F39C12;margin:1rem 0;">
    <div style="font-size:1.2rem;font-weight:700;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.8;">{content}</div>
    <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.5rem;">卡片 {current}/{total}</div>
    <!-- Buttons rendered via st.button() -->
</div>
```

### 5.7 Section Title Pattern (Clarify Dual Signature)

Add to Section 3.3 or a new "Typography Helpers" section:

```
_section_title(title: str) — Auto-detects emoji prefix, adds 📊 if no emoji
_section_title(icon: str, title: str) — Explicit icon + title (business_card variant)

Recommendation: Consolidate to single function with optional icon parameter.
```

### 5.8 Pre-Development Checklist Update

Add to Section VI:
- [ ] Event cards use `_event_card()` helper (not inline HTML)
- [ ] Quiz cards use `_quiz_card()` helper (not inline HTML)
- [ ] Onboarding cards use `_onboarding_card()` helper (not inline HTML)
- [ ] Section titles use `_section_title()` (not raw `st.markdown("### ...")`)

---

## 6. Summary of Round 21 Findings

### Design Grade: **A** (upgraded from A-)

Sprint 8 successfully closed the inline HTML enforcement gap. The design system components are now used consistently across 6+ pages. Remaining issues (D-051, D-052, D-053) are minor and don't block the A grade.

### Competitor Key Takeaways
1. **Quiz-after-story is table stakes** for education platforms (Finimize proves it)
2. **Beginner onboarding is the #1 unserved need** in TW market (Stash model)
3. **Simple/Detailed toggle** solves the beginner/intermediate tension (Finimize ELI5)
4. **Stock Explorer's PPT-style + historian positioning** remains unique vs all 90 competitors

### Sprint 9 Design Specs Delivered
- C98: Event interpretation card — layout, components, interaction pattern
- C101: Quiz UI — inline card pattern, Finimize model, 3-question flow
- C103 Lite: First visit guide — 2-card design, dismissible, session-state tracked

### New Design Issues: 3
- D-057: Duplicate _section_title() functions (P2)
- D-058: _render_related_stock_card() misuses _subsidiary_card() (P2)
- D-059: Inconsistent _section_title() calling convention (P2, resolved by D-057)

### Design System Updates Needed: 7 items
- Document existing: _subsidiary_card, _count_label, _summary_card
- Add new: event interpretation card, quiz card, onboarding card
- Clarify: _section_title() dual signature issue

---

*This section was added by the Design Reviewer in Round 21 (2026-06-13). Next update: After Sprint 9 feature implementation.*

# Round 24 Design Assessment (2026-06-15, after Sprint 10 Completion)

### Recommendation: **A** (maintained, 14th consecutive A/A-)

**Justification:**
Sprint 10 continues the strong design discipline established over the last 14 rounds. The C34 Company Story Timeline is a well-designed new page that uses shared components (`_section_title`, `_summary_card`, `_info_card`) from `_router_base.py` — the event cards are built on `_summary_card` with a date/severity header, avoiding the inheritance issues seen in Sprint 9's event interpretation cards. The C105 Simple/Detailed Toggle is the standout feature: it implements the Finimize ELI5 pattern identified in competitor analysis, defaults to beginner-friendly simple mode with `value=True`, persists via session_state, and replaces 8 detail-heavy sections with a compact `_render_simple_overview()` that uses `_summary_card` consistently. This directly addresses P1 issue D-005 (page overload risk) by collapsing the detail sections behind a toggle. The D-064/D-065/D-066 inline HTML removals are confirmed — zero inline HTML remains in `comprehension_check.py`, `event_dashboard.py`, and `first_visit_guide.py`. The M5 fix (event alerts now use cards) completes the event alert UX modernization started in Sprint 9.

The only new minor issue is `company_timeline.py` line 101 using `unsafe_allow_html=True` for a small event count label — this should use the shared `_count_label()` helper from `_router_base.py` instead. This is a single-line fix, not grade-blocking. The 2 `unsafe_allow_html` usages in `timeline_controls.py` (M3 era, lines 37 and 62) predate Sprint 10 and are tracked separately. Overall L0 and L1 remain fully green, no P1 regressions, and the design system components continue to be adopted consistently. The grade is maintained at A for the 14th consecutive review.

### Sprint 10 Feature Design Review
- **C34 Timeline**: Good. Uses `_summary_card` for event cards (proper component reuse), `_section_title` for page header, `_info_card` for empty state. Event type labels and severity badges are well-structured with emoji + Chinese text. Minor: line 101 uses inline HTML for event count instead of `_count_label()`. PPT-style: one key point (timeline) per page ✅.
- **C105 Toggle**: Excellent. `st.toggle` with `value=True` defaults to beginner-friendly mode. `_render_simple_overview()` replaces 8 detail sections with a compact card-based overview using `_summary_card`. Section dispatch in `_main.py` cleanly separates always-shown vs conditional sections. Finimize ELI5 pattern correctly implemented. D-005 (page overload) directly mitigated by this feature.
- **M5 fix**: Event alerts now use cards instead of `st.error`/`st.warning`. Consistent with the card-based design system. No issues found.
- **D-064/065/066 fixes**: Confirmed — zero inline HTML remains in `comprehension_check.py`, `event_dashboard.py`, and `first_visit_guide.py`. The enforcement gap from D-003 continues to close.

### New Issues (if any)
- **D-067**: `company_timeline.py` line 101 uses `unsafe_allow_html=True` for event count label. Should use `_count_label()` from `_router_base.py` instead. Severity: P2 (single-line fix, minor consistency issue with design system).

### Grade Trajectory
A (R21) → A (R22) → A- (R23) → **A (R24, maintained)**
