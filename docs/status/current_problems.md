# Stock Explorer — Current Problems

> **Last Updated**: 2026-06-20
> **Source**: Design Review Round 16 (2026-06-20)
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

### D-003: Inconsistent Card Styling
- **Severity**: P1
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `_router_base.py` provides `_白话_card()` and `_info_card()` but pages frequently bypass these with inline HTML. `group_structure.py` uses completely different card styling (white background, different border colors). `watchlist_page.py` uses inline HTML for card rows. `etf_detail.py` uses inline HTML for the one-liner, header, and dividend sections. **Round 14 regression**: C41 peer cards and C44 risk dimension cards also use inline HTML, worsening the inconsistency.
- **Affected Pages**: `group_structure.py`, `watchlist_page.py`, `etf_detail.py`, `etf_browser.py`, `business_card.py` (C41 lines 522-532, C44 line 72)
- **Proposed Fix**: Replace all inline HTML cards with shared components from `_router_base.py`. Create additional card types (summary card, warning card) as needed.
- **Effort**: 2-3h

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

- **Total Issues**: 35
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006)
- **P2 (Optimization)**: 22 (D-007, D-008, D-009, D-010, D-011, D-012, D-015, D-032, D-033, D-035, D-036, D-038, D-039, D-040, D-041, D-042, D-043, D-045, D-048)
- **Resolved**: 19

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 4 feature implementation.*
