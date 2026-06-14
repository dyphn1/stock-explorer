# Stock Explorer — Current Problems

> **Last Updated**: 2026-06-14
> **Source**: Design Review Round 40 (2026-06-14, after C147/C140/D-113/D-114 feature review)
> **Maintainer**: Design Reviewer

This file tracks all known design/UX problems in Stock Explorer, organized by severity.

### D-108: Settings Page Visual Feedback Boxes Use Inline HTML (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 38
- **Description**: The settings page (`settings.py`) has 2 visual feedback boxes (lines 101-108, 168-176) that use `unsafe_allow_html=True` with inline-styled divs (`background-color:#f0f2f6; border-radius:8px; padding:12px 16px; font-size:14px`). These are functionally identical to `_info_card()` but implemented as inline HTML. This is a D-003 regression — the developer duplicated the card style inline rather than using a shared component.
- **Affected Files**: `src/pages/settings.py` lines 101-108, 168-176
- **Proposed Fix**: Replace with `_info_card()` calls or create a `_feedback_box(message, icon="✅")` helper in `_router_base.py`. Alternatively, use `st.success()` / `st.info()` which Streamlit renders with consistent styling.
- **Effort**: 0.5-1h

### D-109: C14 Benchmark Logic Duplicated in _summary.py (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 38
- **Description**: `_render_story_card()` in `_summary.py` (lines 183-288) contains ~100 lines of inline benchmark data fetching and metric computation that is structurally identical to `_fetch_benchmark_health_scores()` in `_health.py` (lines 46-163). Both functions: (1) look up `INDUSTRY_BENCHMARKS` by industry, (2) fetch benchmark financial data via `client.get_*()`, (3) compute gross_margin, net_margin, revenue_yoy, debt_ratio, current_ratio, roe, (4) call `compute_health_scores()`. This is a D-003 regression (duplicated logic across files). The architect's review (D-107) identified the same issue from an architecture perspective.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` lines 183-288, `src/pages/business_card/_sections/_health.py` lines 46-163
- **Proposed Fix**: Extract benchmark health score fetching into a shared service function (e.g., `health_scoring.get_benchmark_scores(client, industry, stock_id)`). Both `_health.py` and `_summary.py` call this function. This also resolves D-106 (architecture debt).
- **Effort**: 1-2h

### D-117: `_health.py` Uses Raw `st.markdown("### 🏥 公司健康狀況")` Instead of `_section_title()`
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: `_render_health()` at line 184 uses `st.markdown("### 🏥 公司健康狀況")` instead of `_section_title("🏥 公司健康狀況")`. This is the only section header in `_health.py` and it bypasses the `_section_title()` helper's emoji auto-detection and consistent formatting. While the result looks identical, it creates an inconsistency with the rest of the codebase.
- **Affected Files**: `src/pages/business_card/_sections/_health.py` line 184
- **Proposed Fix**: Replace with `_section_title("🏥 公司健康狀況")`.
- **Effort**: <0.25h

### D-118: `_historical_pattern.py` Uses `_info_card()` with Empty Title
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: The event match cards in `_render_historical_pattern()` (line 54) call `_info_card("", card_content, direction_emoji)` with an empty title string. This renders the card with an empty title div. While visually acceptable, it's a semantic misuse of `_info_card()` which expects a non-empty title.
- **Affected Files**: `src/pages/business_card/_sections/_historical_pattern.py` line 54
- **Proposed Fix**: Either (a) pass the match date as the title, or (b) create a dedicated `_event_match_card()` helper.
- **Effort**: 0.25-0.5h

### D-119: `_so_what_box()` Component Not Documented in Design System
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: The `_so_what_box()` component in `_router_base.py` (lines 184-216) is a new "So What?" implication callout box introduced in Sprint 18 (C149). It uses a distinct visual style (`background:#F0F7FF`, `border-left:4px solid #2980B9`) that differs from all other card types. It is not documented in the design system.
- **Affected Files**: `src/pages/_router_base.py` lines 184-216
- **Proposed Fix**: Document in `docs/design/design_system.md` as a new "Implication Callout" card variant.
- **Effort**: 0.25h

### D-120: Benchmark Logic Duplication Escalation (from D-109)
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 40
- **Description**: D-109 identified benchmark duplication. Round 40 confirms the duplication has grown — `_summary.py` now has 107 lines of benchmark logic (lines 188-294) vs `_health.py`'s 117 lines (46-163). Additionally, `INDUSTRY_BENCHMARKS` dict is triplicated across `_summary.py`, `_health.py`, and `peer_comparison.py`. Extraction to a shared service + YAML is now the recommended fix.
- **Affected Files**: `_summary.py` lines 188-294, `_health.py` lines 46-163, `peer_comparison.py`
- **Proposed Fix**: (1) Extract `INDUSTRY_BENCHMARKS` to `src/data/industry_benchmarks.yaml`. (2) Extract benchmark health score fetching to `health_scoring.get_benchmark_scores()`. Do as Day 1 Sprint 20 infrastructure.
- **Effort**: 1.5-2.5h

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

### D-004: Design System Documentation Not Maintained (DOWNGRADED TO P2)
- **Severity**: P2 (downgraded from P1 in Round 34)
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: `docs/design/design_system.md` exists at the expected path but is not maintained alongside actual components. New components (`_mini_score_card`, `_glossary_tooltip`, `_health_score_card`) are added to `_router_base.py` without design system updates. The doc needs a maintenance pass to reflect the current component library.
- **Affected Files**: `docs/design/design_system.md`, all pages and services
- **Proposed Fix**: Update `docs/design/design_system.md` to include: `_mini_score_card` (compact score card variant), `_glossary_tooltip` (popover tooltip component), `_health_score_card` (planned), "entity card" variant (`_subsidiary_card` with white background), "muted label" variant (`_count_label`). Add a maintenance note: "Update this doc when adding new components to `_router_base.py`."
- **Effort**: 1h (update existing doc)
- **Status**: ✅ PARTIALLY RESOLVED — doc exists at expected path. Remaining: needs maintenance update for new components.

### D-005: Business Card Page Overload Risk (MITIGATED)
- **Severity**: P1 (mitigated to P2 in Round 34 — kept as P1 for tracking)
- **Added**: 2026-06-14
- **Source**: Design Review Round 9
- **Description**: The Business Card page already had 9 sections. Sprint 2 added C37, C39, C43, and C45, bringing the total to 13+ sections. C41 adds a "推薦閱讀" section. C44 adds a risk section (mitigated by `st.expander`). **Round 34 update**: C105 toggle + Sprint 12 expander pattern significantly mitigated this. The page shows 4 above-fold sections by default. Users who disable the toggle still see all sections, but the default experience is now clean.
- **Affected Pages**: `business_card.py`
- **Proposed Fix**: Follow the "one new card per page per sprint" principle. Use progressive disclosure (expandable sections) for less critical content. Consider a "beginner mode by default" approach instead of showing everything. Reorder sections per Round 11 recommendations (summary → snowflake → deltas → details).
- **Related Features**: C37, C39, C41, C36, C43, C45, C44, C105
- **Status**: ✅ MITIGATED in Sprint 12 — C105 toggle + expander pattern reduces above-fold sections from 18+ to 4. Severity reduced to P2 in practice.

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
- **Status**: ✅ RESOLVED in Sprint 12 — peer cards already use `_info_card()`. Commit: 658bd3f.

### D-036: C44 Risk Dimension Cards Use Non-Standard Background
- **Severity**: P2
- **Added**: 2026-06-19
- **Source**: Design Review Round 14
- **Description**: C44 risk dimension cards use `background:#FFF8F0` (tip/warning background) instead of the standard card background `#F8F9FA`. While defensible for risk context (warning = orange tint), this creates visual inconsistency. The design system specifies `#F8F9FA` for info cards and `#FFF8F0` for tip cards — risk dimensions are informational, not tips.
- **Affected Lines**: `business_card.py` line 72
- **Proposed Fix**: Change to `background:#F8F9FA` and rely on the `border-left:4px solid {color}` for risk level indication. The color-coded border already communicates risk level effectively.
- **Effort**: <0.5h (one-line change)
- **Status**: ✅ RESOLVED in Sprint 12 — `background:#FFF8F0` → `background:#F8F9FA` in `_render_risk_dimension()` in `_helpers.py` line 86. Commit: 658bd3f.

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
- **Status**: ✅ RESOLVED in Sprint 12 — `_render_compare_stories()` and `_render_read_next()` now accept `all_info=None` parameter instead of calling `client.get_stock_info()` internally. `_render_business_card()` fetches `all_info` once and passes it. Commit: 658bd3f.

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
- **Status**: ✅ RESOLVED in Sprint 12 — already uses `_section_title("📖 推薦閱讀")`. Commit: 658bd3f.

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
- **Status**: ✅ RESOLVED in Sprint 12 — already uses `_section_title("🔗 分享這張名片")`. Commit: 658bd3f.

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
- **Status**: ✅ RESOLVED in Sprint 12 — already uses `st.caption()`. Commit: 658bd3f.

### D-065: Disclaimer Text Uses Inline HTML (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The historian disclaimer in `event_dashboard.py` (lines 133-137) uses inline HTML (`font-size:0.8rem;color:#95A5A6`). This is the same disclaimer pattern as `_historian_disclaimer()` in `_helpers.py` which uses `st.caption()`. The inline HTML creates inconsistency.
- **Affected Files**: `src/pages/event_dashboard.py` lines 133-137
- **Proposed Fix**: Replace with `st.caption()` or call `_historian_disclaimer("event")`.
- **Effort**: <0.5h
- **Status**: ✅ RESOLVED in Sprint 12 — already uses `st.caption()`. Commit: 658bd3f.

### D-066: Adaptive Banner Uses Inline HTML (Pre-existing)
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 22
- **Description**: The adaptive analysis framework banner in `event_dashboard.py` (lines 193-204) uses inline HTML with `background:#EBF5FB` and `border-left:4px solid #3498DB`. This is functionally identical to `_info_card()` but implemented as inline HTML. Pre-existing — not introduced by Sprint 9.
- **Affected Files**: `src/pages/event_dashboard.py` lines 193-204
- **Proposed Fix**: Replace with `_info_card(title=..., content=..., icon="🎯")`.
- **Effort**: <0.5h
- **Status**: ✅ RESOLVED in Sprint 12 — already uses `_info_card()`. Commit: 658bd3f.

### D-081: Metric Popover Card Uses Inline HTML Instead of _白话_card() (D-003 Regression)
- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30
- **Description**: `_render_metric_popover()` in `_financial.py` (lines 41-47) renders the metric card using `unsafe_allow_html=True` with inline HTML instead of calling `_白话_card()`. The inline HTML is a near-exact copy of `_白话_card()`'s styling (`background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB`). This was introduced as part of the D-079 fix — the card needs to be rendered inline to share a row with the ❓ help button via `st.columns([5, 1])`.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py` lines 41-47
- **Proposed Fix**: Create a `_白话_card_with_help(label, value, analogy, help_key)` helper in `_router_base.py` that renders the card + button in a two-column layout using shared component styling. Alternatively, modify `_白话_card()` to accept an optional `help_icon` parameter.
- **Effort**: 0.5-1h
- **Note**: This is a D-003 regression, but the trade-off is architecturally justified (two-column layout requirement). Still should be consolidated into a shared component.
- **Status**: ✅ **RESOLVED in Sprint 14** — `_render_metric_popover()` now calls `_白话_card()` within the column layout. The two-column requirement is preserved by wrapping the `_白话_card()` call in `st.columns([5, 1])`. Commit: `724921c`.

### D-082: Moat Dimension Mini-Cards Use _summary_card() with Empty Icon
- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30
- **Description**: The 5 moat dimension mini-cards in `_moat.py` (line 49) use `_summary_card(f"{color_emoji} {dim_name}", f"{score_val:.0f} 分", "")`. The `_summary_card()` renders with orange `border-left:4px solid #F39C12` and `#FFF8F0` background — a "hero card" style that's inappropriate for dimension score cards that should be neutral information display. The empty icon parameter `""` also renders an empty icon slot in the card header.
- **Affected Files**: `src/pages/business_card/_sections/_moat.py` line 49
- **Proposed Fix**: Create a `_mini_score_card(label, score)` helper in `_router_base.py` with compact styling: `background:#F8F9FA;border-radius:8px;padding:0.5rem;border-left:4px solid {score_color}`. Use score-based border color (green/amber/red).
- **Effort**: 0.5h
- **Status**: ✅ **RESOLVED in Sprint 14** — `_mini_score_card()` created in `_router_base.py` with score-based border colors (green ≥70, amber ≥40, red <40). Moat dimension cards now use this component. Commit: `724921c`.

### D-083: Story Card Health Score Border Not Color-Coded by Health Level (D-080 Continuation)
- **Severity**: P2
- **Added**: 2026-06-18
- **Source**: Design Review Round 30 (continuation of D-080 from Round 28)
- **Description**: The health score in the story card (line 142 `_summary_card("整體健康度", ...)`) always renders with orange border (#F39C12). D-080 identified this in Round 28 but was not resolved in Sprint 13b. The health label shows 🟢/🟡/🔴 emoji but the card border doesn't match. This creates a visual disconnect between the emoji indicator and the card styling.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` line 142
- **Proposed Fix**: Add optional `border_color` parameter to `_summary_card()` in `_router_base.py`. Pass health-score-based color: `#27AE60` (≥70), `#F39C12` (≥40), `#E74C3C` (<40).
- **Effort**: 0.25h
- **Note**: Continuation of D-080. Now tracked as D-083 for Sprint 14 resolution.
- **Status**: ✅ **RESOLVED in Sprint 14** — `border_color` parameter added to `_summary_card()`. Health score now passes score-based color. Commit: `724921c`.

### D-084: Moat Comparison Page Section Headers Use Raw st.markdown Instead of _section_title()
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 32
- **Description**: The moat_comparison.py page has 5 section headers (lines 65, 113, 127, 145, 156) that use raw `st.markdown("### ...")` instead of `_section_title()`. This means they don't get the emoji-prefix detection and consistent formatting that `_section_title()` provides.
- **Affected Files**: `src/pages/moat_comparison.py` lines 65, 113, 127, 145, 156
- **Proposed Fix**: Replace with `_section_title()` calls for consistency.
- **Effort**: 0.25h

### D-085: Moat Comparison Page Fetches Data in View Layer
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 32
- **Description**: `moat_comparison.py` calls `client.get_stock_info()` (line 35) and `get_stock_data()` (line 96) directly in the page renderer. This is a view-layer data fetch (same pattern as D-038). Lower severity since it's a standalone page with its own data loading, but still architecturally inconsistent.
- **Affected Files**: `src/pages/moat_comparison.py` lines 35, 96
- **Proposed Fix**: Move peer data fetching to the router layer.
- **Effort**: 1-2h

### D-086: Academy Quiz Score Color/Emoji Logic in View Layer
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 32
- **Description**: The score color/emoji/title/desc logic (percentage → color mapping) is hardcoded in `academy.py` lines 170-181. Same pattern as D-063. If this pattern is reused in future quiz features, it will be duplicated.
- **Affected Files**: `src/pages/academy.py` lines 170-181
- **Proposed Fix**: Move to a helper `_get_score_style(percentage)` returning `(color, emoji, title, desc)` dict.
- **Effort**: <0.5h

### D-087: Academy Content Block Headings Don't Use _section_title()
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 32
- **Description**: `_render_content_block()` heading type uses `st.markdown(f"#### {block.get('text', '')}")` instead of `_section_title()`. Since these are content-level headings within a lesson (below the `##` lesson title), `####` is appropriate, but it's inconsistent with the section-file convention.
- **Affected Files**: `src/pages/academy.py` line 31
- **Proposed Fix**: Acceptable as-is for content-level headings. Document the convention.
- **Effort**: <0.1h

### D-088: _financial.py Metric Education Passes Inline HTML Through _info_card()
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Design Review Round 32
- **Description**: `_financial.py` line 150 passes `<span style='color:...'>` HTML fragments as content to `_info_card()`. Since `_info_card()` already uses `unsafe_allow_html=True` internally, the HTML renders, but it bypasses the semantic contract of the card component.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py` line 150
- **Proposed Fix**: Replace with emoji-only indicators (🟢/🔴) or add a `direction_indicator` parameter to `_info_card()`.
- **Effort**: 0.5h

### D-089: _financial.py Growing Multi-Responsibility Section File
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Challenger Round 32
- **Description**: `_financial.py` (343 lines) contains 6 distinct render functions: `_render_metric_popover()`, `_render_key_metrics()`, `_render_dividend()`, `_render_revenue_breakdown()`, `_render_revenue_trend()`, `_render_valuation()`. The dividend function alone is 113 lines with inline HTML table generation. If it grows beyond 400 lines, splitting should be considered.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py`
- **Proposed Fix**: Monitor. Split into `_financial_metrics.py`, `_financial_dividend.py`, `_financial_revenue.py` if it exceeds 400 lines.
- **Effort**: 1-2h (when needed)

### D-090: Metric Popover session_state Accumulation Anti-Pattern
- **Severity**: P2
- **Added**: 2026-06-13
- **Source**: Challenger Round 32
- **Description**: `_render_metric_popover()` in `_financial.py` uses `st.session_state[f"_open_popover_{popover_key}"] = True` to track popover state. These dynamic keys are never cleaned up, causing session_state accumulation over long sessions. The D-081 fix moved to `_白话_card()` but the underlying session_state toggle remains.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py` line 45
- **Proposed Fix**: Replace with `st.popover()` built-in toggle if Streamlit version supports it. Eliminates the stale key accumulation.
- **Effort**: 0.5h

---
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
|| D-035 | C41 Peer Cards Use Inline HTML | P2 | 2026-06-15 | Already resolved — peer cards use `_info_card()`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-036 | C44 Risk Dimension Cards Non-Standard Background | P2 | 2026-06-15 | `background:#FFF8F0` → `background:#F8F9FA` in `_render_risk_dimension()`. Commit: 658bd3f. |
|| D-038 | C41 Calls API in View Layer | P2 | 2026-06-15 | Moved `client.get_stock_info()` out of view layer to router. Commit: 658bd3f. |
|| D-044 | C41 Read Next Header Doesn't Use _section_title() | P2 | 2026-06-15 | Already resolved — uses `_section_title("📖 推薦閱讀")`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-047 | C53-1 Share Section Header Doesn't Use _section_title() | P2 | 2026-06-15 | Already resolved — uses `_section_title("🔗 分享這張名片")`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-064 | Key Concept Line Uses Inline HTML | P2 | 2026-06-15 | Already resolved — uses `st.caption()`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-065 | Disclaimer Text Uses Inline HTML | P2 | 2026-06-15 | Already resolved — uses `st.caption()`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-066 | Adaptive Banner Uses Inline HTML | P2 | 2026-06-15 | Already resolved — uses `_info_card()`. Verified in Sprint 12. Commit: 658bd3f. |
|| D-079 | Dual Tooltip Pattern on Key Metrics | P2 | 2026-06-18 | Merged into single `_render_metric_popover()` with glossary + metric education. Commit: b51c13b. |
|| D-080 | Story Card Health Score Border Color | P2 | — | **DEFERRED to Sprint 14** — tracked as D-083. Low priority, emoji indicator already communicates health level. |
||| D-081 | Metric Popover Card Uses Inline HTML | P2 | 2026-06-13 | RESOLVED in Sprint 14 — `_render_metric_popover()` now calls `_白话_card()`. Commit: `724921c`. |
||| D-082 | Moat Dimension Mini-Cards Use _summary_card() | P2 | 2026-06-13 | RESOLVED in Sprint 14 — `_mini_score_card()` created with score-based border colors. Commit: `724921c`. |
||| D-083 | Story Card Health Score Border Not Color-Coded | P2 | 2026-06-13 | RESOLVED in Sprint 14 — `border_color` param added to `_summary_card()`. Commit: `724921c`. |

---

## Statistics

- **Total Issues**: 92
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006)
- **P2 (Optimization)**: 44 (D-004, D-007, D-008, D-009, D-010, D-011, D-012, D-015, D-032, D-033, D-039, D-040, D-041, D-042, D-045, D-048, D-049, D-051, D-052, D-053, D-062, D-063, D-067, D-068, D-069, D-070, D-084, D-085, D-086, D-087, D-088, D-089, D-090, D-091, D-092, D-093, D-094, D-095, D-108, D-109)
- **Resolved/Consolidated**: 33

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 15 feature implementation.*

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

# Round 26 Design Assessment (2026-06-17, after Sprint 12 Completion)

> **Reviewer**: Design Reviewer
> **Scope**: Sprint 12 verification (Info Hierarchy, User Feedback, 8 debt fixes), competitor comparison, Sprint 13a design prerequisites
> **Sprint 12 Changes Verified**: Info Hierarchy (expander pattern, C36/C38 relocation), User Feedback (binary 👍/👎), 8 quick debt fixes (D-035/036/038/044/047/064/065/066)

---

## 1. Design Grade Assessment

### Recommendation: **A** (maintained, 17th consecutive A/A-)

**Justification:**

Sprint 12 delivered three high-quality changes that directly strengthen the PPT-style design philosophy:

**Positive changes verified:**

1. **Info Hierarchy (commit `fc4bafd`)**: The above-fold / progressive disclosure model is now fully realized. Business Card page shows only C48 Story Card → C37 Takeaways → C39 Deltas → C43 Health (or simple overview) above the fold. All other sections (one-liner, news, key metrics, dividend, revenue, valuation, risk, expert, historical) are wrapped in `st.expander(expanded=False)`. C36 Revenue Tree and C38 Compare Stories relocated to standalone pages (`revenue_tree.py` 73 lines, `compare_stories.py` 137 lines). This is the single biggest UX improvement since C105 — the page went from 18+ visible sections to 4 above-fold + clean expanders. D-005 (page overload risk) is now fully resolved.

2. **User Feedback (commit `1495c7e`)**: Binary 👍/👎 buttons at page bottom. Clean implementation: `st.columns([1, 1, 6])` layout, session-state dedup, `st.toast()` confirmation, JSONL storage via `feedback_service.py`. Zero Streamlit dependency in service layer. The 👍/👎 pattern is minimalist and non-intrusive — doesn't disrupt the PPT-style flow. After feedback is given, shows "✅ 感謝你的回饋！" caption. Good UX.

3. **8 Quick Debt Fixes (commit `658bd3f`)**: All verified — D-035 (peer cards → `_info_card()`), D-036 (risk dimension background → `#F8F9FA`), D-038 (API call moved out of view layer), D-044/047 (section headers use `_section_title()`), D-064/065/066 (inline HTML → `st.caption()` / `_info_card()`). Zero inline HTML in `event_dashboard.py` and `comprehension_check.py`.

**Remaining concerns (not grade-blocking):**

- **D-068 (NEW)**: `_render_story_card()` line 152 uses `unsafe_allow_html=True` for the health score indicator — a 7-line inline HTML block that should use a shared component. This is the only remaining inline HTML in the `_summary.py` section file.
- **D-069 (NEW)**: `_helpers.py` has 4 `unsafe_allow_html=True` usages in `_render_risk_dimension()` (line 94), `_study_card()` (line 145), `_expert_card()` (line 158), `_scenario_card()` (line 171). These are pre-existing from Sprint 5 (D-041) and are consistent card-style inline HTML, but they bypass `_router_base.py` shared components.
- **D-051**: `etf_browser.py` still has inline HTML for colored change values (lines 167, 427, 431). Pre-existing, not a Sprint 12 regression.
- **D-052**: `_subsidiary_card()` still uses non-standard `background:white` styling. Established pattern, documented in Round 21.

**Net assessment**: Sprint 12 significantly improved the Business Card page's information architecture. The expander pattern is now the standard for secondary content. The feedback feature is well-designed and non-intrusive. The 8 debt fixes continue the trend of eliminating inline HTML regressions. The grade is maintained at **A** for the 17th consecutive review.

**Grade trajectory**: A (R21) → A (R22) → A- (R23) → A (R24) → A (R25) → **A (R26, maintained)**

---

## 2. Competitor Design Comparison (Focus: C33 Glossary & C48 Story Card)

### Selected Competitors for C33/C48 Comparison

| # | Competitor | Relevance | Key Design Insight |
|---|-----------|-----------|-------------------|
| 1 | **Stash** | 🔴 Highest | Tappable glossary — every financial term has a 1-sentence tooltip; "Learn Before Invest" gate |
| 2 | **Investopedia** | 🔴 Highest | 10,000+ term glossary; each term has definition + related terms + article link |
| 3 | **Simply Wall St** | 🔴 High | Snowflake analysis with hover tooltips; progressive disclosure via "Read More" |
| 4 | **Finimize** | 🟡 Medium | ELI5 toggle; glossary terms highlighted inline with dotted underline |
| 5 | **Public.com** | 🟡 Medium | Story cards per stock; key takeaways with emoji icons; social learning |

### Glossary/Tooltip UI Patterns (for C33)

| Pattern | Stock Explorer Current | Competitor Best Practice | Recommendation |
|---------|----------------------|------------------------|----------------|
| **Inline term highlighting** | ❌ None — terms are shown as-is | Finimize: dotted underline on terms, tap to see tooltip | Implement C33 as `st.tooltip()` on metric labels or hover-triggered `st.caption()` |
| **Dedicated glossary panel** | ❌ None | Stash: bottom sheet with search | Consider a sidebar "辭典" panel for C33 Phase 2 |
| **Metric value tooltips** | ✅ Partial — hover on snowflake shows values | Simply Wall St: hover on any metric shows definition + formula | Extend to all `_白话_card()` labels — add `❓` icon with tooltip |
| **Contextual help** | ✅ Analogy text serves as explanation | Investopedia: "What does this mean?" expand on every metric | Already partially solved by analogy engine. C33 adds formal definitions |

### Story Card / Summary Card Designs (for C48)

Stock Explorer's C48 Story Card (implemented in `_summary.py`) compares well:

| Dimension | Stock Explorer C48 | Competitors |
|-----------|-------------------|-------------|
| **Hero card at top** | ✅ `st.expander("📌 30 秒認識這家公司", expanded=True)` with metrics | Atom Finance: hero card with key metrics; Dhan: company header card |
| **Key metrics row** | ✅ 3 `_白话_card()` in `st.columns(3)` | Simply Wall St: 4-metric grid with icons |
| **Health indicator** | ✅ Color-coded health score (🟢/🟡/🔴) | Simply Wall St: snowflake (similar to C43) |
| **Did You Know fact** | ✅ Rotating fact via `get_company_facts()` | Finimize: rotating "Did you know?" in daily briefing |
| **One-liner** | ✅ `_info_card("一句話定位", ...)` | Public.com: company tagline |

**Key insight**: C48 is well-positioned vs competitors. The main gap is that the story card is inside an `st.expander` — it should be the most prominent element on the page, not hidden behind an expandable container. Consider making it always expanded (no expander wrapper) or using a larger visual treatment.

### PPT-Style vs Competitor Approaches

Stock Explorer's PPT-style (one key point per page, charts > 60% of area, max 200 chars text) remains **unique** among all 90+ competitors analyzed. The closest competitor is Simply Wall St's infographic approach, but they still show more content per page. The expander pattern from Sprint 12 strengthens this differentiation by hiding secondary content behind progressive disclosure.

---

## 3. Sprint 13a Design Prerequisites

### C33: Beginner Glossary / Term Tooltip System

**Design Spec — Inline Tooltip Pattern (Stash/Investimize Model)**:

```
┌─────────────────────────────────────────────────┐
│  📊 關鍵數字與配息                                │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ 本益比 (PER)  │  │ 毛利率        │            │
│  │ 15.3         │  │ 66.2%        │            │
│  │ ❓ 每1股...   │  │ ❓ 每100元... │            │
│  └──────────────┘  └──────────────┘            │
│                                                 │
│  ── On hover/click ──                           │
│  ┌───────────────────────────────────────────┐  │
│  │ 📖 本益比 (PER)                            │  │
│  │ 股價 ÷ 每股盈餘。衡量你願意為每1元獲利     │  │
│  │ 付多少價格。PER 15 = 你願意付15元買1元     │  │
│  │ 的獲利。                                   │  │
│  │ [了解更多 →]                               │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Components needed**:
1. `_glossary_tooltip(term: str, definition: str, icon: str = "❓")` — renders a term label with a small ❓ icon that shows a tooltip on hover. Use `st.markdown()` with HTML `<span title="...">` or a custom tooltip component.
2. `_glossary_panel()` — optional sidebar panel showing all terms for the current page. Triggered by a "📖 辭典" button in the sidebar.
3. Glossary data source: `data/glossary.yaml` — structured term definitions with term, definition, related_terms, analogy.

**UI Pattern Decision**: For Streamlit, the best approach is:
- **Phase 1**: Add `st.tooltip()` or HTML `title` attribute to metric labels in `_白话_card()`. Show term name + 1-sentence definition on hover.
- **Phase 2**: Add a "📖 辭典" expandable section at the bottom of each page with all terms used on that page.

**Interaction**: Hover (desktop) or tap (mobile) on a term shows a tooltip with the definition. No page navigation required. Tooltip disappears after 2 seconds or on mouse leave.

**Layout**: Inline with existing card components. The ❓ icon appears next to the metric label in `_白话_card()`. No new card type needed — this is an enhancement to existing `_白话_card()`.

### C48: Company Story Card (Enhancement)

C48 is already implemented in `_render_story_card()` (lines 38-157 of `_summary.py`). Sprint 13a should focus on **enhancement** rather than new implementation:

**Current state**: Story card is inside `st.expander("📌 30 秒認識這家公司", expanded=True)` — this is a PPT-style violation (hiding the most important content behind an expander).

**Design Spec for Enhancement**:

```
┌─────────────────────────────────────────────────┐
│  📌 30 秒認識這家公司                            │
│  ┌───────────────────────────────────────────┐  │
│  │  TSMC `2330`                              │  │
│  │  半導體製造業                                │  │
│  │                                           │  │
│  │  💡 一句話定位                             │  │
│  │  全球最大的晶圓代工製造商，為蘋果、        │  │
│  │  輝達等客戶生產晶片。                      │  │
│  │                                           │  │
│  │  ┌──────────┬──────────┬──────────┐      │  │
│  │  │ 最近月營收 │ 本益比    │ 毛利率    │      │  │
│  │  │ 2,832 億  │ 15.3     │ 66.2%    │      │  │
│  │  │ 每100元.. │ 每1股..  │ 每100元.. │      │  │
│  │  └──────────┴──────────┴──────────┘      │  │
│  │                                           │  │
│  │  🏥 整體健康度: 85/100 🟢 健康             │  │
│  │                                           │  │
│  │  🤔 你知道嗎？                            │  │
│  │  台積電佔台股加權指數權重約 30%...         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Key changes for Sprint 13a**:
1. **Remove the `st.expander` wrapper** — the story card should be always visible as the first content element (after the toggle). This is the single most important C48 design fix.
2. **Replace inline HTML health indicator** (line 152) with a shared `_health_score_card()` component in `_router_base.py`.
3. **Add C33 tooltips** to the 3 key metrics in the story card — each metric label should have a ❓ icon with glossary definition.

**Information hierarchy** (C48 card internal):
1. Company name + industry (largest text)
2. One-liner positioning (`_info_card`)
3. 3 key metrics (`_白话_card` in 3 columns) — with C33 tooltips
4. Health score indicator (compact, centered)
5. "Did You Know?" fact (`_info_card`)

---

## 4. New Design Issues

### D-068: Story Card Health Indicator Uses Inline HTML (P2)
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 26
- **Description**: `_render_story_card()` in `_summary.py` (lines 144-153) uses `unsafe_allow_html=True` for the health score indicator — a 7-line inline HTML block with `background:#F8F9FA;border-radius:10px`. This is the only remaining inline HTML in the `_summary.py` section file. It should use a shared component from `_router_base.py`.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` lines 144-153
- **Proposed Fix**: Create `_health_score_card(score, label)` in `_router_base.py` with standardized card styling. Replace the inline HTML block.
- **Effort**: 0.5h

### D-069: _helpers.py Card Components Bypass _router_base.py (P2)
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 26
- **Description**: `_helpers.py` has 4 card-rendering functions (`_render_risk_dimension`, `_study_card`, `_expert_card`, `_scenario_card`) that use inline HTML with `unsafe_allow_html=True` instead of calling shared components from `_router_base.py`. While these are consistent in style (all use `#F8F9FA` background, `border-radius:12px`, `border-left:4px solid`), they create a parallel set of card components that aren't documented in the design system. `_render_risk_dimension()` is particularly notable since it's used in the business card page's risk section.
- **Affected Files**: `src/pages/business_card/_helpers.py` lines 85-95, 136-172
- **Proposed Fix**: Either (a) replace these with calls to `_info_card()` / `_summary_card()` from `_router_base.py`, or (b) move them to `_router_base.py` and document in the design system as specialized card variants.
- **Effort**: 1-2h

### D-070: C48 Story Card Hidden Behind Expander (P1)
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 26
- **Description**: The C48 Story Card is wrapped in `st.expander("📌 30 秒認識這家公司", expanded=True)` (line 127 of `_summary.py`). While `expanded=True` means it's visible by default, the expander UI adds visual chrome (the ▼ arrow, the collapsible frame) that contradicts the PPT-style principle. The story card is the most important content element on the Business Card page — it should be rendered as a prominent, always-visible hero section, not hidden inside a collapsible container. This also affects the ten-second test: a novice seeing an expander might not realize they should click it.
- **Affected Files**: `src/pages/business_card/_sections/_summary.py` line 127
- **Proposed Fix**: Remove the `st.expander` wrapper. Render the story card content directly as a prominent section with a `_section_title("📌 30 秒認識這家公司")` header. Use a `_summary_card()` or a new `_hero_card()` component for the container.
- **Effort**: 1h
- **Related**: This is the most important C48 design fix for Sprint 13a.

### Verification of Sprint 12 Debt Fixes:

| ID | Description | Status | Notes |
|----|------------|--------|-------|
| D-035 | C41 Peer Cards inline HTML | ✅ RESOLVED | Already uses `_info_card()`. Verified. |
| D-036 | C44 Risk Dimension non-standard bg | ✅ RESOLVED | `background:#F8F9FA` confirmed. |
| D-038 | C41 API in view layer | ✅ RESOLVED | `all_info` param pattern confirmed. |
| D-044 | Read Next header | ✅ RESOLVED | Uses `_section_title()`. |
| D-047 | Share section header | ✅ RESOLVED | Uses `_section_title()`. |
| D-064 | Key Concept inline HTML | ✅ RESOLVED | Uses `st.caption()`. |
| D-065 | Disclaimer inline HTML | ✅ RESOLVED | Uses `st.caption()`. |
| D-066 | Adaptive Banner inline HTML | ✅ RESOLVED | Uses `_info_card()`. |

---

## 5. Summary of Round 26 Findings

### Design Grade: **A** (maintained, 17th consecutive)

Sprint 12's Info Hierarchy is a landmark UX improvement — the Business Card page now truly follows the PPT-style "one key point per page" principle with 4 above-fold sections and clean progressive disclosure. The feedback feature is well-designed. 8 debt fixes continue the inline HTML elimination trend.

### Competitor Key Takeaways
1. **Glossary tooltips are table stakes** — Stash, Investopedia, Finimize all have them. C33 is overdue.
2. **C48 Story Card is competitive** but should be always visible (not in expander).
3. **PPT-style + progressive disclosure** is now a stronger differentiator than ever — competitors show more content per page.

### Sprint 13a Design Specs Delivered
- C33 Glossary: Inline tooltip pattern, `_glossary_tooltip()` component, `data/glossary.yaml` data source
- C48 Enhancement: Remove expander wrapper, replace inline HTML health indicator, add C33 tooltips to metrics

### New Design Issues: 3
- D-068: Story card health indicator inline HTML (P2)
- D-069: _helpers.py card components bypass _router_base.py (P2)
- D-070: C48 story card hidden behind expander (P1) — **most important fix for Sprint 13a**

---

*This section was added by the Design Reviewer in Round 26 (2026-06-17). Next update: After Sprint 13a feature implementation.*

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

# Round 34 Design Assessment (2026-06-14, Design Review)

> **Reviewer**: Design Reviewer
> **Scope**: Competitor UX pattern audit, recent feature design debt (C126 moat comparison, C47 academy, C101 quiz), P1/P2 consolidation
> **Current Design Grade**: A-

---

## 1. Design Grade Assessment

### Recommendation: **A- → A** (upgrade)

**Justification:**

Round 34 reviews the design debt from three recent features (C126 moat comparison, C47 academy, C101 quiz) and finds that all three use shared components from `_router_base.py` correctly. The moat comparison page (`moat_comparison.py`) is a model citizen — it uses `_section_title()`, `_info_card()`, `_summary_card()`, and `_mini_score_card()` with zero inline HTML. The academy page (`academy.py`) uses `_info_card()`, `_section_title()`, and `_白话_card()` consistently. The quiz score logic was already centralized in `_get_score_style()` (D-086 resolved).

**Positive findings:**
1. **C126 Moat Comparison** (commit `724921c`): Clean component usage. All 5 section headers use `_section_title()`. Peer overview uses `_info_card()`. Score comparison uses `_summary_card()`. Dimension comparison uses `_mini_score_card()`. Moat type and evidence use `_info_card()`. Zero inline HTML. This is the best-designed new page since C105.
2. **C47 Academy**: Uses `_info_card()` for callouts, `_section_title()` for section headers, `_白话_card()` for quiz score display. The `_get_score_style()` helper centralizes the color/emoji logic. Zero inline HTML in the page file.
3. **D-084/D-086/D-088 resolved**: Confirmed — moat comparison headers use `_section_title()`, academy quiz score uses centralized helper, financial.py inline HTML eliminated.

**Remaining P1 issues (4):**
- D-003: Inconsistent card styling — `_helpers.py` still has 4 card functions with inline HTML (`_study_card`, `_expert_card`, `_scenario_card`, `_render_risk_dimension`). These are consistent in style but bypass `_router_base.py`.
- D-004: No design system documentation — `docs/design/design_system.md` exists but is not maintained alongside the actual components.
- D-005: Business Card page overload — mitigated by C105 toggle and Sprint 12 expander pattern, but still a concern for users who disable the toggle.
- D-006: Mobile responsiveness — unchanged, Streamlit limitation.

**Net assessment**: The recent features (C126, C47, C101) demonstrate strong design discipline — all use shared components, zero inline HTML regressions. The grade upgrades from A- to **A** based on consistent component adoption in recent features.

**Grade trajectory**: A (R21) → A (R22) → A- (R23) → A (R24) → A (R26) → **A (R34, upgraded)**

---

## 2. Competitor UX Pattern Audit (Round 34 Focus)

### Key Competitor Patterns Not Yet Implemented

| Pattern | Competitors | Our Status | Priority |
|---------|-------------|------------|----------|
| **Quiz after story** | Finimize, SoFi | ✅ C101 implemented | — |
| **Key takeaways card** | Seeking Alpha, Public.com | ✅ C37 implemented | — |
| **Beginner/Expert toggle** | Finimize, Sharesies | ✅ C105 implemented | — |
| **Glossary tooltips** | Stash, Investopedia | ⚠️ `_glossary_tooltip()` exists in `_router_base.py` but not wired to any page | P2 |
| **Company story timeline** | Stocksera, Public.com | ⚠️ C34 implemented as event list, not narrative | P2 |
| **Revenue tree** | Public.com, Koyfin | ⚠️ C36 pie chart only, no hierarchical tree | P2 |
| **What changed recently** | Koyfin, Finary | ✅ C39 implemented | — |
| **Read next recommendations** | Motley Fool, Seeking Alpha | ✅ C41 implemented | — |
| **First visit guide** | Stash, Finimize | ✅ C103 implemented | — |
| **Progress bar on learning** | Duolingo, SoFi | ⚠️ Academy has `st.progress()` but no streak/gamification | P2 |

### Most Impactful Missing Pattern: Glossary Tooltips

The `_glossary_tooltip()` component already exists in `_router_base.py` (lines 189-210) but is **not wired to any page**. This is the single biggest gap between our implementation and competitor best practices. Stash and Investopedia both have tappable glossary terms on every financial metric. Our `_glossary_tooltip()` component is built but unused — it needs to be integrated into `_白话_card()` as an optional parameter.

**Recommendation**: Wire `_glossary_tooltip()` into `_白话_card()` as an optional `glossary_key` parameter. When provided, a small ℹ️ icon appears next to the metric label. Clicking it shows a popover with the term definition. This is a 1-2h effort that directly addresses the "beginner-friendly" positioning.

---

## 3. P2 Consolidation Opportunities

### 3.1 D-052 + D-053: _subsidiary_card and _count_label → Document in Design System

Both components are stable and widely used. Rather than "fixing" them, they should be documented in the design system as approved variants:
- `_subsidiary_card()`: "Entity card" variant — white background, flex layout, used for subsidiary/group structure display
- `_count_label()`: "Muted label" variant — used below card grids for "共 X 個" display

**Action**: Mark as ✅ DOCUMENTED (not resolved — they're working as intended, just need design system documentation).

### 3.2 D-062 + D-063: Quiz Result Cards → Consolidated by D-086

D-062 (quiz result cards use inline HTML) and D-063 (quiz score color logic in view layer) are both addressed:
- D-062: The `comprehension_check.py` quiz result cards use `st.success()`/`st.error()` + `st.info()` instead of inline HTML cards. This is acceptable for feedback display.
- D-063: The academy quiz now uses `_get_score_style()` helper (D-086 resolved).

**Action**: Mark D-062 and D-063 as ✅ CONSOLIDATED — the pattern is now consistent between `comprehension_check.py` and `academy.py`.

### 3.3 D-089: _financial.py Growing → Monitor

`_financial.py` is 343 lines with 6 render functions. The dividend function (113 lines with inline HTML table) is the biggest concern. The threshold for splitting (400 lines) hasn't been reached yet.

**Action**: Keep as P2, update threshold to 350 lines for proactive splitting.

---

## 4. New Design Issues (Round 34)

### D-091: _glossary_tooltip() Component Built But Not Wired to Any Page
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 34
- **Description**: `_glossary_tooltip()` in `_router_base.py` (lines 189-210) is a fully-built component that renders a clickable ℹ️ icon with a popover containing term definition, example, and analogy. However, it is **not imported or called by any page**. The glossary data source (`glossary.yaml`) exists but is unused. This is a significant gap vs competitors (Investopedia 10K+ terms, Stash tappable glossary). The component was built in anticipation of C33 but never integrated.
- **Affected Files**: `src/pages/_router_base.py` (component exists), no pages import it
- **Proposed Fix**: Wire `_glossary_tooltip()` into `_白话_card()` as an optional `glossary_key` parameter. When provided, render the ℹ️ icon next to the label. Also add a `glossary_service` parameter to `_render_key_metrics()` and `_render_story_card()` to pass through.
- **Effort**: 1-2h
- **Competitor Benchmark**: Investopedia (10K+ term glossary), Stash (tappable glossary on every term)

### D-092: Academy Lesson List Uses Raw st.markdown Instead of Card Components
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 34
- **Description**: The lesson list in `_render_academy()` (lines 281-320 of `academy.py`) renders each lesson as raw `st.markdown()` with `###` headers, `st.caption()`, and `st.markdown("- ...")` for objectives. This creates a flat, text-heavy list that doesn't match the card-based PPT-style design. Each lesson should be a card with the title, metadata, objectives, and action button — consistent with how other list views work in the app (e.g., watchlist cards, ETF cards).
- **Affected Files**: `src/pages/academy.py` lines 281-320
- **Proposed Fix**: Create a `_lesson_card(lesson, progress)` helper in `_router_base.py` or `academy.py` that renders each lesson as a card with: icon + title + metadata row + objectives list + action button. Use `_info_card()` as the container and add the button below.
- **Effort**: 1-2h
- **Competitor Benchmark**: Duolingo (card-based lesson list), Coursera (course cards with metadata)

### D-093: Moat Comparison Page Fetches Data for All Peers Sequentially
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 34
- **Description**: `_render_moat_comparison_page()` in `moat_comparison.py` (lines 94-110) fetches `get_stock_data()` for each peer sequentially in a `for` loop. With 3 peers, this means 3 sequential API calls (each with 10 sub-tasks). Combined with the primary stock's data already loaded, this creates a total of 40 API calls. The page should use `ThreadPoolExecutor` (like `get_stock_data()` does internally) to parallelize peer data fetching. This is both a performance issue and a design issue — users see a long loading spinner while peers are fetched one by one.
- **Affected Files**: `src/pages/moat_comparison.py` lines 94-110
- **Proposed Fix**: Use `ThreadPoolExecutor` to fetch peer data in parallel. Show skeleton placeholders (`_info_card("...", "載入中...")`) for peers while loading. This matches the pattern already used in `get_stock_data()`.
- **Effort**: 1-2h
- **Note**: This is primarily a performance issue but affects perceived UX quality.

### D-094: _financial.py Dividend Table Inline HTML Exceeds D-043 Scope
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 34 (escalation of D-043)
- **Description**: D-043 flagged the dividend history table in `_financial.py` (lines 220-256) as using inline HTML instead of `st.dataframe()`. In Round 34, this is re-escalated because the table has grown to 36 lines of HTML generation code (building `<table>`, `<tr>`, `<td>` tags manually with inline styles). The table includes badge rendering (🟢/🟡/🔴 for dividend quality) which is difficult to replicate in `st.dataframe()`. However, the current approach is fragile and hard to maintain.
- **Affected Files**: `src/pages/business_card/_sections/_financial.py` lines 220-256
- **Proposed Fix**: Two options: (a) Use `st.dataframe()` with a custom column config for badges (render emoji in a separate column), or (b) Extract the table to a `_dividend_table()` helper in `_router_base.py` with documented "data table" variant styling. Option (b) is preferred since the badge rendering is core to the UX.
- **Effort**: 1-2h
- **Status**: Escalated from D-043 (Round 16) — the table has grown more complex since then

### D-095: Academy Quiz Results Use st.success/st.error Instead of Card Components
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 34
- **Description**: The quiz result display in `_render_quiz()` (lines 204-214 of `academy.py`) uses `st.success()` / `st.error()` for per-question results and `st.info()` for explanations. While functional, this creates a visual mismatch with the rest of the page which uses card-based components. The `st.success()` / `st.error()` boxes use Streamlit's default green/red background which doesn't match the design system's `#27AE60` / `#E74C3C` colors with `border-left` pattern. The per-question results also lack the question number and status icon (✅/❌) that would make them scannable.
- **Affected Files**: `src/pages/academy.py` lines 204-214
- **Proposed Fix**: Create a `_quiz_result_card(is_correct, question_text, explanation)` helper that renders a compact result card with: status icon (✅/❌) + question number + question text + explanation. Use `border-left:4px solid #27AE60` (correct) or `#E74C3C` (incorrect) for visual consistency with the design system.
- **Effort**: 0.5-1h
- **Note**: This is a lower priority than D-092 (lesson list cards) but both should be done together for consistency.

---

## 5. Existing Issue Status Updates

### D-003: Inconsistent Card Styling → PARTIALLY FIXED (updated)
- **Update**: Recent features (C126, C47) use shared components correctly. Remaining inline HTML is in `_helpers.py` (4 functions: `_study_card`, `_expert_card`, `_scenario_card`, `_render_risk_dimension`). These are consistent in style but bypass `_router_base.py`. Severity remains P1 but scope is narrowing.

### D-004: No Design System Documentation → PARTIALLY FIXED (updated)
- **Update**: `docs/design/design_system.md` exists but is not maintained alongside actual components. The design system needs updates for `_mini_score_card`, `_glossary_tooltip`, and the "entity card" variant (`_subsidiary_card`). Severity reduced to P2 — the doc exists but needs maintenance.

### D-005: Business Card Page Overload → MITIGATED (updated)
- **Update**: C105 toggle + Sprint 12 expander pattern significantly mitigated this. The page shows 4 above-fold sections by default. Severity reduced to P2 — the risk is managed by the toggle.

### D-006: Mobile Responsiveness → UNCHANGED
- **Update**: No change. Still a P1 due to Streamlit limitations.

### D-043: Dividend History Table Inline HTML → ESCALATED (updated)
- **Update**: Escalated to D-094 in Round 34. The table has grown more complex (36 lines of HTML generation). Needs a dedicated `_dividend_table()` helper.

### D-062/D-063: Quiz Result Cards → CONSOLIDATED (updated)
- **Update**: Both issues are addressed by the `_get_score_style()` helper (D-086) and the use of `st.success()`/`st.error()` for feedback. The pattern is now consistent. Mark as ✅ CONSOLIDATED.

### D-089: _financial.py Growing → MONITOR (updated)
- **Update**: File is 343 lines. Threshold for splitting lowered to 350 lines. Monitor for next review.

---

## 6. Summary of Round 34 Findings

### Design Grade: **A** (upgraded from A-)

Recent features (C126 moat comparison, C47 academy, C101 quiz) demonstrate strong design discipline — all use shared components from `_router_base.py` with zero inline HTML regressions. The moat comparison page is the best-designed new page since C105.

### Competitor Key Takeaways
1. **Glossary tooltips are the #1 missing pattern** — `_glossary_tooltip()` is built but not wired to any page (D-091)
2. **Card-based lesson lists are standard** — Duolingo, Coursera all use cards for lesson lists (D-092)
3. **Parallel data loading is expected** — moat comparison fetches peers sequentially (D-093)

### New Design Issues: 5
| ID | Title | Severity | Effort |
|----|-------|----------|--------|
| D-091 | _glossary_tooltip() built but not wired | P2 | 1-2h |
| D-092 | Academy lesson list uses raw markdown | P2 | 1-2h |
| D-093 | Moat comparison sequential peer fetch | P2 | 1-2h |
| D-094 | Dividend table inline HTML escalated | P2 | 1-2h |
| D-095 | Quiz results use st.success instead of cards | P2 | 0.5-1h |

### Consolidated Issues: 3
- D-052 + D-053: _subsidiary_card and _count_label → ✅ DOCUMENTED
- D-062 + D-063: Quiz result cards → ✅ CONSOLIDATED
- D-043: Dividend table → ESCALATED to D-094

### Updated Statistics
- **Total Issues**: 90
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006 — D-004 downgraded to P2)
- **P2 (Optimization)**: 42 (net +5 new, -3 consolidated, +1 escalated, -1 downgraded)
- **Resolved/Consolidated**: 33

---

*This section was added by the Design Reviewer in Round 34 (2026-06-14). Next update: After Sprint 17 feature implementation.*

---

# Round 37 Design Assessment (2026-06-14, Post-Sprint 16b)

> **Reviewer**: Design Reviewer
> **Scope**: Sprint 16b design verification, competitor design comparison, Sprint 17 design prerequisites

## 1. Design Grade Assessment

### Recommendation: **A** (maintained)

**Justification:**

Sprint 16b delivered 6 features that overall maintain the A grade. The design quality is solid, with two standout features (C28 Story Timeline, D5 LLM Abstraction) that demonstrate good design discipline, and two features (C07 Settings, C132 Risk Simplifier) that are architecturally sound but raise minor design concerns.

**Positive findings:**

1. **C28 Story Timeline (commit `ca49d2c`)**: Excellent design discipline. Uses `_section_title()`, `_summary_card()`, and `_info_card()` from `_router_base.py` — zero inline HTML. Severity coding (`_SEVERITY_COLORS` dict mapping high→`#E74C3C`, medium→`#F39C12`, low→`#27AE68`) is consistent with the design system's existing color palette. Timeline entries use `_summary_card(border_color=...)` which leverages the D-083 fix from Sprint 14. The severity legend at the bottom is a nice touch. The empty state uses `_info_card()` correctly. This is the best-designed new page since C126 moat comparison.

2. **D5 LLM Abstraction (commit `5e7fde8`)**: Protocol-based design (`ExplanationProvider` with `@runtime_checkable`) is architecturally sound. The `ExplanationRequest`/`ExplanationResponse` dataclasses are clean. The `TemplateExplanationProvider` covers 10 metric templates with direction-aware explanations (increase/decrease/neutral). The factory pattern (`get_explanation_provider()`) enables future LLM integration without changing callers. The templates pass the "ten-second test" — e.g., "月營收成長15%，表現優於預期，可能是需求回溫或新產品貢獻" is immediately understandable by a beginner. **Design concern**: The template explanations are somewhat generic ("可能是需求回溫或新產品貢獻") — they attribute changes to common causes without stock-specific context. This is acceptable for a template fallback but should be noted as a UX limitation when C134 wires it in.

3. **C132 Risk Simplifier (Sprint 16a, commit `8051cb8`)**: The 1-5 scale with emoji mapping (1-2→🟢, 3→🟡, 4→🟠, 5→🔴) largely aligns with existing color patterns, though the addition of 🟠 (level 4) introduces a fourth severity color not previously used in the design system (which uses green/amber/red). The emoji progression is logical and intuitive. Descriptions are plain-language and pass the ten-second test.

**Remaining concerns (not grade-blocking):**

- **C07 Settings**: Uses raw `st.markdown("## ...")` for the page header instead of `_section_title()`. The section label uses `### 📈 📊 💰` markdown headers which are functional but don't use the `_section_title()` helper. However, this is a settings_infrastructure page where PPT-style is less critical — users expect form-like layouts on settings pages. The sliders with `key=` parameter properly sync to session_state, and the reset button with `st.rerun()` is the correct Streamlit pattern. The value labels (`_value_label_pricerange`, `_value_label_volume`) that show 🔴/🟡/🟢 sensitivity indicators are a **nice design touch** — this is exactly the kind of progressive disclosure that makes settings beginner-friendly.

- **C07 missing feedback**: Settings sliders don't show live preview of what events would change. This is deferred to Sprint 17 (wiring), but it's worth noting as a design gap — users adjust sliders without knowing the impact until Sprint 17 wires them.

- **D5 unused**: The `ExplanationProvider` has zero callers. This is expected (Sprint 17 C134 will wire it), but it means the "ten-second test" quality of LLM-generated explanations is unverified in production. The template explanations work, but the real test will come when C134 generates delta-specific explanations.

**Net assessment**: Sprint 16b maintained design discipline. C28 Story Timeline is exemplary. C07 is functional infrastructure. D5 is architecturally sound but untested in production. The grade remains **A** — no regressions, no new inline HTML, and C28 demonstrates that the design system components are being used consistently.

**Grade trajectory**: A (R21) → A (R22) → A- (R23) → A (R24) → A (R26) → A (R34) → **A (R37, maintained)**

---

## 2. Sprint 16b Design Verification

| Feature | Shared Components Used? | Consistent Severity Colors? | Ten-Second Test? | Inline HTML? | Overall Assessment |
|---------|------------------------|---------------------------|-----------------|--------------|-------------------|
| **C28 Story Timeline** | ✅ `_section_title`, `_summary_card`, `_info_card` | ✅ high→`#E74C3C`, medium→`#F39C12`, low→`#27AE68` (matches design system) | ✅ Cards are scannable; legend explains severity | ✅ Zero inline HTML | ✅ **Excellent** |
| **D5 LLM Abstraction** | N/A (backend service) | N/A | ✅ Template explanations pass (e.g., "月營收成長15%...") | ✅ Pure Python | ✅ **Sound** (awaiting C134 wiring) |
| **C07 Settings Skeleton** | ⚠️ Raw `st.markdown("## ⚙️ 設定")` instead of `_section_title()` | N/A | ✅ Slider labels are clear; value indicators show sensitivity | ✅ Zero inline HTML | ✅ **Functional** (settings page, PPT-style less critical) |
| **C132 Risk Simplifier** | N/A (backend service) | ⚠️ Introduces 🟠 for level 4 (new color, but fits the pattern) | ✅ "非常低風險" through "非常高的風險" is clear | ✅ Pure Python | ✅ **Good** |
| **C14 Health Narrative** | N/A (backend enhancement) | N/A | ✅ `get_health_summary()` produces plain-language text | ✅ Pure Python | ✅ **Good** |
| **C41 Read Next Phase A** | ✅ Uses existing `_render_read_next()` | N/A | ✅ "推薦閱讀" card is clear | ✅ Uses `_info_card` | ✅ **Good** |

**Summary**: Zero inline HTML regressions. C28 is the design star. All backend services (D5, C132, C14) produce beginner-friendly output. C07 minor issue with non-standard headers but acceptable for infrastructure.

---

## 3. Competitor Design Patterns to Adopt

### Sprint 17+ Opportunities

Based on the current 4 competitors from the original briefing plus patterns observed in C07/C134/C14 design context:

### 1. Finimize's "Confidence Meter" for Explanations
- **What**: Finimize shows a small confidence indicator next to each AI explanation ("We're 85% sure this is due to..."). Beginners don't know whether to trust explanations.
- **Stock Explorer context**: When C134 wires `TemplateExplanationProvider` to `explain delta()`, each explanation should include a subtle confidence indicator. The `ExplanationResponse.confidence` field (0.0-1.0) already exists in D5 but is always set to 1.0. 
- **Adoption**: For Sprint 17 C134, render template-sourced explanations with a subtle "📊 系統估算" caption below the explanation text. When future LLM-sourced explanations arrive, show "🤖 AI 分析" instead. This builds trust transparency from day one.

### 2. Simply Wall St's "Benchmark Ghost Layer" on Snowflake
- **What**: Simply Wall St overlays a semi-transparent "industry average" polygon behind the stock's snowflake, so users see both their stock AND the benchmark in one glance. No tab switching.
- **Stock Explorer context**: C14 Full Radar needs an industry #1 benchmark overlay. The current snowflake (`create_health_snowflake`) doesn't support overlay layers.
- **Adoption**: For Sprint 17 C14, add a second trace to the Plotly snowflake figure with `fill='tonextx'` and opacity 0.15 in gray. Label it "🏭 產業標竿" with a legend entry. This should be toggleable (default: on) via a `st.toggle("顯示產業比較")`.

### 3. Stash's "Glossary Gate" Before Technical Content
- **What**: Stash shows a brief definition popover automatically the first time a user encounters a financial term, without requiring them to click. It's proactive education.
- **Stock Explorer context**: `_glossary_tooltip()` exists but isn't wired to any page (D-091). The `TemplateExplanationProvider` templates explain changes but don't define the underlying terms.
- **Adoption**: For Sprint 17 C134, when rendering delta explanations, auto-detect financial terms (PER, ROE, 毛利率, etc.) in the explanation text and wrap them with `_glossary_tooltip()` popovers. This is a light integration — the glossary component exists, it just needs to be called from the C134 rendering layer.

### 4. Public.com's "What This Means for You" Callout
- **What**: After each stock story or data point, Public.com adds a small "💡 What this means for you" box that translates data into personal relevance. Not investment advice — just context.
- **Stock Explorer context**: The `explain_delta()` function produces factual explanations ("月營收成長15%") but doesn't add the "what this means" layer. The C132 risk descriptions ("這家公司風險很低，財務健康狀況良好") are a good start but could be more actionable.
- **Adoption**: For Sprint 17 C134, add an optional `implication` field to `ExplanationResponse`. For template-based explanations, add a stock sentence: e.g., "如果你正在觀察這家公司，穩定的營收成長是一個正面的訊號。" (framed as observability, not advice). This passes the historian tone test.

### 5. Finimize's "Progressive Disclosure for Settings"
- **What**: Finimize's settings use accordion-style grouping: "Basic" thresholds are visible by default, "Advanced" thresholds are behind a "Show more" button. This prevents settings overwhelm.
- **Stock Explorer context**: C07 currently shows 3 sliders flat. Sprint 17 will wire them. When more settings are added (industry thresholds, volume detection, notification frequency), the settings page will grow.
- **Adoption**: For Sprint 17 C07 wiring, wrap the 3 existing sliders in a `st.expander("基本門檻設定", expanded=True)` and add a placeholder `st.expander("進階門檻設定", expanded=False)` for the planned Sprint 18+ additions. This provides a growth path without cluttering.

---

## 4. Sprint 17 Design Prerequisites

### 4.1 C14 Full Radar — Benchmark Overlay Design Spec

**Context**: C14 adds industry #1 benchmark data to the existing health snowflake and integrates the radar into the story card above-fold.

**Benchmark Overlay on Snowflake**:
```
┌─────────────────────────────────────────────────┐
│  🏥 健康評分 — 台積電 (2330)                      │
│                                                 │
│    獲利能力  ●━━━━━━━━━━●                       │
│    ╱    ╲   ╱  ╲   ╱  ╲                        │
│  財務結構 ●──── ──── ● 償債能力                   │
│    ╲    ╱   ╲  ╱   ╲  ╱                        │
│    營運效率  ●━━━━━━━━━━●                       │
│         ╲    ╱                                  │
│          成長潛力                              │
│                                                 │
│  ● 台積電 (85分)   ░░░ 產業標竿 — 日月光 (78分) │
│                                                 │
│  [顯示產業比較 ▼]  [產業排名: #2/15]              │
└─────────────────────────────────────────────────┘
```

**Implementation notes**:
- Use Plotly's `scatterpolar` with a second trace for benchmark (gray, `opacity=0.15`)
- Industry #1 name should come from `data/industry_benchmarks.yaml` — hardcode for MVP
- Toggle via `st.toggle("顯示產業比較", value=True)` — defaults to on so users see the benchmark immediately
- Industry rank badge: `#2/15` shown as `st.caption()` below the snowflake, using the 🟢/🟡/🔴 color from C132 risk level
- Use `_mini_score_card()` for the 5 dimension scores (already exists, D-082 resolved)

**Story Card Integration**:
- Move the health score from the story card's inline display to the snowflake chart
- Story card should show: `_section_title("📌 30 秒認識這家公司")` → snowflake chart → key metrics → Did You Know
- The snowflake replaces the current `_render_story_card()` health indicator section

### 4.2 C134 Change Explanations — UX Pattern for `explain_delta()` Narratives

**Context**: `explain_delta()` in `delta_engine.py` produces plain-language explanations like "月營收成長15%，表現優於預期，可能是需求回溫或新產品貢獻". C134 will refactor this to use `TemplateExplanationProvider` from D5.

**UX Pattern — "Delta Card with Explanation"**:
```
┌─────────────────────────────────────────────────┐
│  📈 最近有什麼變化                                │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  📊 月營收                                  │  │
│  │  2,832 億 → 2,456 億 (+15.3%)             │  │
│  │                                           │  │
│  │  💬 台積電月營收成長 15%，表現優於預期，    │  │
│  │     可能是需求回溫或新產品貢獻              │  │
│  │                                           │  │
│  │  📊 系統估算 · 基於近 30 日資料             │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  📊 股價（近 30 日均價）                    │  │
│  │  850 元 → 780 元 (-8.2%)                  │  │
│  │                                           │  │
│  │  💬 台積電股價近 30 日小跌 8%，略有回檔     │  │
│  │                                           │  │
│  │  📊 系統估算 · 基於近 30 日資料             │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Design spec**:
1. **Container**: Each delta is a card using `_info_card()` with the metric name as title
2. **Layout**: `st.columns([2, 1])` — left: metric value + change %, right: explanation text
3. **Change indicator**: Use colored emoji (🔴/🟢) + bold percentage, consistent with C39's existing color coding
4. **Explanation text**: Rendered below the metric value in `st.caption()` style (smaller, muted)
5. **Source badge**: "📊 系統估算" for template-sourced, "🤖 AI 分析" for future LLM-sourced — builds trust transparency
6. **Glossary integration**: Auto-detect financial terms in explanations and wrap with `_glossary_tooltip()` (see Pattern #3 above)
7. **Implication sentence**: Optional one-line "如果你正在觀察..." context (see Pattern #4 above)
8. **Empty state**: When no deltas exceed threshold, show `_info_card("最近有什麼變化", "近期無顯著變化，所有指標波動均在 10% 以內", "🔄")` — this already exists from D-025

**Refactoring requirements** (from `handoff_discuss_r36.md`):
- Write C39 regression tests BEFORE refactoring `explain_delta()` (Action Item A3)
- `explain_delta()` should delegate to `TemplateExplanationProvider.explain()` via `ExplanationRequest(metric_name, current_value, delta=change_pct)`
- Keep `explain_delta()` as a convenience wrapper for backward compatibility

### 4.3 C07 Wire Thresholds — Visual Feedback Design Spec

**Context**: C07 settings page has 3 sliders (price/volume/revenue). Sprint 17 wires them to `adaptive_engine.py` parameters.

**Design spec for wiring**:
1. **Session state accessibility spike** (Action Item A2): Verify that `st.session_state["settings_price_threshold"]` is accessible from `adaptive_engine.py`. The engine runs in the service layer (no Streamlit imports), so values must be passed as parameters, not read from session_state directly.

2. **Visual feedback when wired**:
   - Add a `st.success("✅ 門檻設定已生效")` toast when the user changes a slider AND the value is successfully wired to the engine
   - Show a small indicator next to each slider: "目前使用中" (green dot) when the setting is active, "未連線" (gray dot) when not yet wired
   - This gives users confidence that their settings actually do something

3. **Progressive disclosure** (see Pattern #5 above):
   - Wrap 3 existing sliders in `st.expander("基本門檻設定", expanded=True)`
   - Add placeholder `st.expander("進階門檻設定", expanded=False)` with `st.info("即將推出：產業別閾值、法人動向敏感度...")`

4. **Reset button**: Already exists and works correctly. When wired, reset should also re-initialize the adaptive_engine's internal thresholds.

---

## 5. New Design Debt from Sprint 16b

### D-096: C07 Settings Page Uses Raw st.markdown Headers Instead of _section_title()
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 37
- **Description**: `settings.py` uses `st.markdown("## 風險閾值設定")` (line 65) and `st.markdown("### 📈 股價變動閾值")` (line 74) instead of `_section_title()`. While this is a settings/infrastructure page where PPT-style is less critical, it creates inconsistency with the rest of the app. The `_section_title()` helper provides emoji auto-detection and consistent formatting.
- **Affected Files**: `src/pages/settings.py` lines 65, 74, 100, 123
- **Proposed Fix**: Replace with `_section_title("⚙️ 設定")` and `_section_title("📈 股價變動閾值")` calls.
- **Effort**: 0.25h
- **Note**: Low priority — settings page is infrastructure, not user-facing content. But should be fixed when C07 is wired in Sprint 17.

### D-097: D5 TemplateExplanationProvider Explanations Are Generic (No Stock-Specific Context)
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 37
- **Description**: The `TemplateExplanationProvider` in `template_provider.py` produces explanations like "月營收成長15%，表現優於預期，可能是需求回溫或新產品貢獻". These are factually correct but generic — they don't reference the specific stock's industry, recent news, or unique situation. The `ExplanationRequest` has a `context` dict field that could carry stock-specific data, but `TemplateExplanationProvider.explain()` ignores it entirely. When C134 wires this to `explain_delta()`, users will see the same generic explanations for TSMC and a small-cap stock.
- **Affected Files**: `src/services/llm/template_provider.py` line 101
- **Proposed Fix**: Enhance `TemplateExplanationProvider.explain()` to use `request.context` when available. At minimum, use `context.get("industry")` to add industry-specific flavor: e.g., "月營收成長15%，在半導體產業中表現優於同業平均". This is a Sprint 17 prerequisite for C134.
- **Effort**: 1-2h
- **Competitor Benchmark**: Spiking's "Why Stock Moved" uses stock-specific context (recent news, sector performance) in every explanation.

### D-098: C132 Risk Level 4 Uses 🟠 Not in Design System Color Palette
- **Severity**: P2
- **Added**: 2026-06-14
- **Source**: Design Review Round 37
- **Description**: The `risk_simplifier.py` uses 5 emoji/color levels: 🟢🟢🟡🟠🔴. The design system's established color palette uses only 3 severity colors: green (`#27AE60`), amber (`#F39C12`), red (`#E74C3C`). The addition of 🟠 (orange) for level 4 is logical in the progression but introduces a fourth color that doesn't appear anywhere else in the design system. This creates a minor inconsistency — users who've learned "green = good, amber = caution, red = danger" must now learn "orange = elevated risk" as a new category.
- **Affected Files**: `src/services/risk_simplifier.py` line 77
- **Proposed Fix**: Either (a) keep 🟠 but document it in the design system as the "elevated risk" color, or (b) simplify to 4 levels (🟢🟡🟡🔴) to stay within the existing 3-color palette. Option (a) is recommended since the 5-level granularity is more informative for users.
- **Effort**: 0.5h (documentation update)

---

## Statistics

- **Total Issues**: 93 (+3 new: D-096, D-097, D-098)
- **P0 (Blocking)**: 0
- **P1 (Important)**: 3 (D-003, D-005, D-006 — unchanged)
- **P2 (Optimization)**: 45 (net +3 from Round 37)
- **Resolved/Consolidated**: 33 (unchanged)
- **New Issues This Round**: 3 (D-096, D-097, D-098 — all P2)
- **Design Grade**: **A** (maintained, 4th consecutive A since R34)

---

*This section was added by the Design Reviewer in Round 37 (2026-06-14). Next update: After Sprint 17 feature implementation.*
