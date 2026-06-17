# Zone Separation Review

## Overview
This document reviews the zone separation compliance of key files in the Stock Explorer codebase, based on the design system specified in `docs/design/design_system.md`.

## Design System Zone Rules
From `docs/design/design_system.md`:

### Zone A: Top Navigation Bar (Navbar)
- **Left**: Company name + stock ticker + industry tag
- **Right**: Current price + change
- **Below**: Tabs (Business Card / Operational Checkup / Financial Health / Peer Comparison / Group Structure / Category Browse / ETF Zone / My Watchlist / Event Dashboard)
- Active tab shown in bold `**▎Tab Name**`, others as `st.button`
- **Must NOT contain**: search box, filters, or any interactive controls

### Zone B: Sidebar
- **Function**: Global navigation (search, hot stocks, hot ETFs, my watchlist, event dashboard)
- **Behavior**:
  - Default expanded (`initial_sidebar_state=\"expanded\"`)
  - Must be re-expandable after collapsing (must not disappear)
  - On stock click: set `session_state[\"stock_id\"]` + `session_state[\"page\"] = \"Business Card\"` + `st.rerun()`
- **Must NOT contain**: charts, data tables, or page content

### Zone C: Main Content Area
- **Function**: Pure data display + charts
- **Principles**:
  - One core message per page
  - Charts take more space than text
  - Interactive controls (time range, metric toggles) placed at the top of the content area, clearly separated from data
  - Controls remain stable when data refreshes

## Files Reviewed

### 1. src/pages/router.py
- **Navbar Rendering** (`_render_navbar` function, lines 312-355):
  - Zone A: Correctly renders company name, stock ticker, industry (left) and price/change (right) using `st.columns`.
  - Tabs: Uses `st.radio` for horizontal tab selection. While the design system specifies inactive tabs as `st.button` and active as bold text, the use of `st.radio` is an interactive control but is acceptable as the tab control itself. No other interactive controls (search, filters) are present in the navbar.
  - **Verdict**: Zone A compliant. No prohibited interactive controls found.

- **Sidebar Handling**:
  - The router does not render the sidebar; it is handled in `main.py`.
  - The router does render standalone pages (like event_dashboard, watchlist, etc.) in the main content area (Zone C) after the navbar.
  - **Verdict**: No zone mixing observed in the router.

### 2. src/main.py
- **Sidebar Rendering** (`_render_sidebar` function, lines 199-258):
  - Zone B: Contains:
    - Stock Explorer title and tagline (non-interactive)
    - Search box (text_input) - allowed as global navigation
    - Rate limit banner (warning) - status message, allowed
    - Primary navigation buttons (icon + label) - allowed as global navigation
    - Hot stocks and hot ETFs in expanders with buttons - allowed as global navigation
    - Disclaimer - static text, allowed
  - **No charts, data tables, or page content** found in the sidebar.
  - **Verdict**: Zone B compliant.

### 3. src/pages/event_dashboard.py
- This page is rendered in the main content area (Zone C) for the `event_dashboard` page key.
- **Content Analysis**:
  - The page contains markdown headers, expanders with event details, and buttons inside expanders.
  - Interactive controls (buttons) are located inside expanders, which are part of the data display section. The design system recommends placing interactive controls at the top of the content area, clearly separated from data.
  - No charts are present; the page is text and expander-based.
  - **Verdict**: Potential zone separation improvement: Consider moving any global interactive controls (if any) to the top of Zone C. However, the page does not appear to have global interactive controls like time range selectors. The current placement of controls inside expanders may be acceptable for this specific page type.

### 4. Sprint 23 Features (C202, C199, C200)
- **Files Reviewed**:
  - `src/pages/story_timeline.py` (C202)
  - `src/pages/debate_cards.py` (C199)
  - `src/pages/business_card/_historical_scenarios.py` (C200)
- **Zone Compliance**:
  - All three files are rendered in the main content area (Zone C) when accessed via the navbar.
  - They contain interactive controls (buttons, selectboxes, etc.) but these are typically placed appropriately within the content flow.
  - No prohibited elements (charts in sidebar, interactive controls in navbar) were observed.
  - **Verdict**: Zone separation compliant.

## Conclusion
Based on the review of the navbar (Zone A), sidebar (Zone B), and main content area (Zone C) in the key files:
- **Zone A**: Compliant - no prohibited interactive controls (search box, filters) found.
- **Zone B**: Compliant - no charts, data tables, or page content found.
- **Zone C**: Generally compliant, with a note for `event_dashboard.py` to consider the placement of interactive controls per the design system's recommendation for global controls to be at the top of the content area.

## Recommendations
1. Continue to enforce zone separation during development:
   - Zone A: Only company info, price, and tab controls. No search, filters, or extra interactive controls.
   - Zone B: Only navigation and global widgets (search, hot stocks, etc.). No charts, data tables, or page content.
   - Zone C: Place global interactive controls (time range, metric toggles) at the top, clearly separated from data displays. Ensure charts dominate over text where applicable.
2. When reviewing new features or changes, verify zone separation as part of the design review process.
3. Consider updating the navbar to match the design system's exact specification for tabs (inactive as `st.button`, active as bold text) if desired, though the current `st.radio` implementation is functional and not a zone violation.
