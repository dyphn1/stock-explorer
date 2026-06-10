# Sidebar UX Research - Stock & Financial Dashboards

**Date:** 2026-06-09
**Author:** UX Research Agent (Hermes)
**Purpose:** Inform the sidebar design for Stock Explorer

---

## Table of Contents

1. [Platform Breakdowns](#platform-breakdowns)
2. [Comparative Analysis](#comparative-analysis)
3. [General Sidebar UX Best Practices](#general-sidebar-ux-best-practices)
4. [Recommendations for Stock Explorer](#recommendations-for-stock-explorer)

---

## Platform Breakdowns

### 1. Yahoo Finance (finance.yahoo.com)

**What's in the sidebar:**
- **Navigation links:** Home, News, Markets, Watchlists, Portfolios, Videos, Screeners
- **Watchlists section:** User-created watchlists with inline stock tickers, prices, and change %
- **Market indices:** S&P 500, Dow, Nasdaq with mini sparkline charts
- **Trending tickers:** Auto-populated list of most-active stocks
- **Calendar events:** Earnings and economic calendar snippets

**Organization:**
- Top-level nav items with icons (Home, Markets, News, etc.)
- Collapsible "My Watchlists" section with each watchlist as a named group
- Each watchlist shows a compact table (symbol → price → change)
- Fixed left sidebar (~240px), always visible on desktop

**Interaction patterns:**
- Hover on watchlist items highlights the row; click navigates to quote page
- Watchlists can be expanded/collapsed individually
- Drag-to-reorder watchlists (limited)
- "+" button to create new watchlist always visible at section header
- Active page indicated with bold text + left accent bar

**Effectiveness:**
- ✅ Watchlists are front and center — the most user-valuable feature
- ✅ Inline price data means users don't need to navigate away
- ✅ Clean icon + label pattern is scannable
- ❌ Sidebar can feel cramped on smaller screens
- ❌ No search in sidebar — search is top-center, creating a split focus

---

### 2. TradingView (tradingview.com)

**What's in the sidebar:**
- **Symbol search** (prominent at top)
- **Watchlist panel:** Symbols with price, change %, mini charts
- **Alerts panel:** Active price/indicator alerts
- **News panel:** Headlines with timestamps
- **Ideas/Community panel:** Social trading ideas
- **Screeners:** Stock, forex, crypto screeners
- **Chart layout controls**
- **Drawing tools** (when in chart mode)
- **Indicator panel**

**Organization:**
- Multi-panel sidebar — users can switch between panels via icon tabs on the left edge
- Left edge has a **vertical icon bar** (~56px) with icons for each panel
- Clicking an icon opens that panel as a **slide-out drawer** (~280px) next to the icon bar
- Panels: Watchlist, Alerts, News, Screeners, Ideas, Pine Editor, etc.

**Interaction patterns:**
- Icon bar is always visible; panels overlay content when opened
- Panels can be **popped out** into separate windows (multi-monitor support)
- Drag-to-reorder watchlist items
- Right-click context menu on watchlist items (add alert, remove, chart)
- Hover on symbols shows a **mini chart preview** (tooltip)
- Panels remember their open/closed state per session
- Resizable panel width (drag the inner edge)

**Effectiveness:**
- ✅ Icon bar + panel system scales to many features without clutter
- ✅ Pop-out panels are excellent for power users / multi-monitor
- ✅ Mini chart previews on hover are a killer feature
- ✅ Drag-to-reorder gives users control
- ❌ Icon-only bar requires learning — not all icons are intuitive
- ❌ Too many panels can overwhelm new users
- ❌ Panel management (which are open, closing all) can be fiddly

---

### 3. Finviz (finviz.com)

**What's in the sidebar:**
- **Screener filters:** The primary sidebar feature — extensive filter controls
- **Filter categories:** Exchange, Index, Sector, Industry, Country, Market Cap, Dividend Yield, P/E, Price, Change, Volume, etc.
- **Watchlist (Elite):** Saved watchlists (paid feature)
- **Ticker search** (top of page, not sidebar)
- **Heatmap toggle**

**Organization:**
- Left sidebar is **dedicated to the screener** — it's a filter panel, not nav
- Filters are organized as a **vertical list of dropdown selectors**
- Each filter shows the currently selected value
- "Reset" and "Apply" actions at the bottom
- Very dense, information-rich layout

**Interaction patterns:**
- Click a filter → dropdown with checkboxes, ranges, or text input
- Filters apply immediately (no "Apply" button needed)
- Active filters shown as tags/chips that can be individually removed
- Hover on filter labels shows tooltip descriptions
- Sidebar is **always visible** on desktop; hidden behind hamburger on mobile

**Effectiveness:**
- ✅ Immediate filter feedback — no page reload
- ✅ Filter chips make active state clear
- ✅ Extremely powerful for the target user (stock screeners)
- ❌ Very dense — intimidating for casual users
- ❌ No visual hierarchy within filters — all filters look equal
- ❌ No grouping/collapsing of filter categories

---

### 4. Stock Rover

**What's in the sidebar:**
- **Navigation:** Dashboard, Markets, Watchlists, Portfolios, Screeners, Tools
- **Watchlist tree:** Hierarchical watchlist folders → individual watchlists
- **Portfolio tree:** Portfolio accounts → holdings
- **Quick links:** Recent views, saved screeners
- **Market summary:** Indices and movers

**Organization:**
- **Tree-view navigation** with expandable/collapsible folders
- Each top-level section (Watchlists, Portfolios) is a collapsible group
- Nested items indented with connecting lines
- Icons differentiate item types (folder vs. watchlist vs. portfolio)
- Sidebar is **resizable** and can be collapsed to icons-only

**Interaction patterns:**
- Click arrow to expand/collapse folders
- Drag-and-drop to reorganize watchlists into folders
- Right-click for context menu (rename, delete, export, share)
- Hover shows item count (e.g., "Watchlist (12)")
- Collapsed state shows icons only — preserves screen real estate
- Active item highlighted with accent color

**Effectiveness:**
- ✅ Tree view handles large numbers of watchlists/portfolios elegantly
- ✅ Collapsible sections reduce cognitive load
- ✅ Drag-and-drop organization is intuitive
- ✅ Icons-only collapsed mode is great for focusing on data
- ❌ Right-click actions are undiscoverable for new users
- ❌ Deep nesting can get confusing (folders in folders)

---

### 5. Simply Wall St

**What's in the sidebar:**
- **Primary nav:** Home, Discover, Portfolios, Markets, Community, Reports
- **User portfolios:** List of portfolio names with total value
- **Saved stocks:** "My Stocks" collection
- **Discovery categories:** Growth, Value, Dividend, etc.
- **Snowflake summaries:** Visual "snowflake" scores for saved stocks

**Organization:**
- Clean, minimal sidebar with clear section dividers
- Nav items use **icon + label** consistently
- Portfolios section shows portfolio name + current value + change
- Discovery section uses **color-coded category pills**
- Generous whitespace — less dense than Finviz or TradingView

**Interaction patterns:**
- Hover on nav items shows subtle background highlight
- Active nav item uses bold + accent color
- Portfolios expand to show holdings on click
- Snowflake visuals update in real-time in sidebar
- Smooth expand/collapse animations

**Effectiveness:**
- ✅ Clean, approachable design — good for retail investors
- ✅ Visual snowflakes in sidebar provide at-a-glance insight
- ✅ Color-coded categories aid scanning
- ✅ Generous spacing reduces cognitive load
- ❌ Limited sidebar functionality compared to TradingView
- ❌ No inline price data for individual stocks in sidebar

---

### 6. Google Finance (google.com/finance)

**What's in the sidebar:**
- **Navigation:** Home, Watchlists, Portfolios, Markets, News
- **Watchlists:** Simple list of watchlist names
- **Market indices:** Major indices with price and change
- **Trending:** Most active, top gainers, top losers
- **Search** (top of page, not sidebar)

**Organization:**
- Minimal sidebar — Google's signature simplicity
- Watchlists are just text links (no inline data)
- Market data in a compact, table-like format
- Trending section uses tabs (Most Active / Gainers / Losers)
- Very narrow sidebar (~200px)

**Interaction patterns:**
- Click watchlist name → navigates to watchlist page
- Click trending stock → navigates to quote page
- Tabs switch trending category
- No expand/collapse — everything visible at once
- Hover states are subtle (underline on text links)

**Effectiveness:**
- ✅ Extremely clean and uncluttered
- ✅ Fast to scan — minimal visual noise
- ✅ Google's design language is familiar to billions
- ❌ No inline data — must navigate to see prices
- ❌ Limited functionality — more of a nav menu than a dashboard
- ❌ No customization or personalization in sidebar

---

## Comparative Analysis

| Feature | Yahoo Finance | TradingView | Finviz | Stock Rover | Simply Wall St | Google Finance |
|---|---|---|---|---|---|---|
| **Primary purpose** | Nav + data | Multi-tool panel | Screener filters | Data organization | Nav + discovery | Simple nav |
| **Inline price data** | ✅ | ✅ | ❌ | ✅ | Partial | ❌ |
| **Collapsible sections** | ✅ | ✅ (panels) | ❌ | ✅ | ✅ | ❌ |
| **Drag-to-reorder** | Limited | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Context menus** | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Icon + label nav** | ✅ | Icons only | ❌ | ✅ | ✅ | ✅ |
| **Resizable** | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Collapsed to icons** | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Mini charts** | Sparklines | Hover preview | ❌ | ❌ | Snowflakes | ❌ |
| **Density** | Medium | High | Very High | Medium | Low | Low |

### Key Patterns Across Platforms

1. **Watchlists are the #1 sidebar feature** — every platform puts them front and center
2. **Icon + label** is the dominant nav pattern (5/6 platforms)
3. **Inline data** (prices, changes) in the sidebar is a major differentiator for power users
4. **Collapsible sections** are essential when there's more than ~8 items
5. **Active state indication** (accent color, bold, left bar) is universal
6. **Search is typically NOT in the sidebar** — it's top-center or top-left

---

## General Sidebar UX Best Practices

### When to Use Sidebar vs. Top Nav vs. Hamburger

| Pattern | Best For | Avoid When |
|---|---|---|
| **Persistent sidebar** | 5-15 nav items, dashboard apps, data-heavy tools | Content-heavy pages, marketing sites |
| **Top nav** | 3-7 nav items, content sites, simple apps | Complex apps with many sections |
| **Hamburger menu** | Mobile, secondary navigation, infrequently used items | Primary navigation on desktop |
| **Icon bar + panels** | Many tools/features, power-user apps | Casual/simple apps |

**For Stock Explorer:** A **persistent sidebar** is appropriate because:
- It's a data/dashboard application
- Users need constant access to watchlists and navigation
- The sidebar can display live data (prices, changes)
- Desktop is the primary use case for stock analysis

### How Many Items Before Clutter?

- **5-7 items:** Comfortable without sections
- **8-12 items:** Use section headers or grouping
- **12-20 items:** Use collapsible sections
- **20+ items:** Use icon bar + panel system (TradingView model) or hierarchical tree

**Rule of thumb:** If a user can't see all sidebar items without scrolling, it needs better organization.

### Mobile / Responsive Behavior

| Breakpoint | Recommended Behavior |
|---|---|
| **> 1024px** | Persistent sidebar, full width |
| **768px – 1024px** | Collapsible sidebar, defaults to open |
| **< 768px** | Sidebar hidden behind hamburger/menu button, slides in as overlay |

**Key mobile considerations:**
- Sidebar should **overlay** content on mobile (not push content)
- Swipe-from-left gesture to open is expected
- Tap outside to close
- Ensure touch targets are ≥ 44px height
- Auto-close sidebar after selecting an item on mobile

### Accessibility Considerations

1. **Keyboard navigation:**
   - Tab through sidebar items sequentially
   - Enter/Space to activate
   - Arrow keys for tree navigation (up/down) and expand/collapse (left/right)
   - Escape to close sidebar on mobile

2. **Screen readers:**
   - Use `<nav>` with `aria-label="Main navigation"`
   - Collapsible sections: `aria-expanded="true/false"` on the toggle
   - Current page: `aria-current="page"` on active item
   - Tree items: `role="tree"`, `role="treeitem"`, `aria-level`, `aria-setsize`, `aria-posinset`

3. **Visual:**
   - Minimum contrast ratio 4.5:1 for text
   - Don't rely solely on color to indicate active state (use icon, weight, or border)
   - Focus indicators must be visible (outline or background change)
   - Icon-only items must have `aria-label` or visible text on focus/hover

4. **Motion:**
   - Respect `prefers-reduced-motion` for expand/collapse animations
   - Avoid auto-expanding on hover (triggers for users with motor impairments)

---

## Recommendations for Stock Explorer

### Recommended Sidebar Structure

```
┌─────────────────────────┐
│ 🔍 Search stocks...     │  ← Optional: quick search in sidebar
├─────────────────────────┤
│ 📊 Dashboard            │  ← Primary nav (icon + label)
│ 📈 Markets              │
│ 📰 News                 │
├─────────────────────────┤
│ ⭐ Watchlists      [+]  │  ← Collapsible section
│   ├─ Tech Stocks   12   │     Each shows name + count
│   ├─ Dividends      8   │     Active: accent color + bold
│   └─ Watchlist 3    5   │
├─────────────────────────┤
│ 💼 Portfolios      [+]  │  ← Collapsible section
│   ├─ Retirement  $142K  │     Shows name + total value
│   └─ Growth       $23K  │
├─────────────────────────┤
│ 🔧 Screeners       [+]  │  ← Collapsible section
│   ├─ High Growth        │     Saved screeners
│   └─ Under $10          │
├─────────────────────────┤
│ 📉 Market Overview      │  ← Compact market indices
│   S&P 500  5,421  +0.3% │     Always visible, minimal
│   NASDAQ   17,200 +0.5% │
└─────────────────────────┘
```

### Specific Recommendations

#### 1. Layout & Width
- **Default width: 240-280px** — enough for labels + inline data
- **Minimum width: 200px** — don't let it get too narrow
- **Collapsible to 56px icon-only mode** — for users who want maximum chart/data space
- **Resizable** — let power users drag to their preferred width (remember in localStorage)

#### 2. Navigation Items (Top Section)
- Use **icon + label** for all primary nav items
- Limit to **3-5 primary items** (Dashboard, Markets, News, etc.)
- Active item: **left accent bar (3px) + bold text + subtle background tint**
- Hover: **background color change** (subtle, ~5% opacity)

#### 3. Watchlists Section (Priority #1)
- **Collapsible** with section header showing count
- **"+" button** always visible in section header for creating new watchlists
- Each watchlist shows: **name + item count** (e.g., "Tech Stocks (12)")
- **Inline price/price change** for the first 3-5 stocks in expanded mode (Yahoo Finance model)
- **Drag-to-reorder** watchlists
- **Right-click context menu:** Rename, Delete, Export, Add Stock
- **Star/favorite** watchlists to pin them to the top

#### 4. Portfolios Section
- Similar to watchlists but shows **total value + daily change** instead of stock count
- Color-code: green for positive, red for negative change
- Expand to see top holdings (optional, keep it compact)

#### 5. Screeners Section
- List saved screeners as simple links
- Show **result count** next to each screener name (e.g., "High Growth (47)")
- Click opens screener results in main content area

#### 6. Market Overview (Bottom)
- **Always visible** at the bottom of the sidebar
- Show 3-5 major indices with **mini sparklines**
- Compact format: `Index Name  Price  Change%  [sparkline]`
- Click to navigate to that index/market page

#### 7. Interaction Patterns
- **Expand/collapse:** Click section header arrow; animate smoothly (150-200ms)
- **Hover on watchlist items:** Show mini chart tooltip (TradingView model — this is a differentiator)
- **Active states:** Left accent bar + bold + background tint
- **Empty states:** Show helpful prompts ("Create your first watchlist →")
- **Badge/notification dot:** Show on News if there are breaking stories

#### 8. Responsive Behavior
- **Desktop (> 1024px):** Persistent sidebar, full functionality
- **Tablet (768-1024px):** Collapsible, defaults to open, can collapse to icons
- **Mobile (< 768px):** Hidden by default, hamburger menu to open, overlay mode, auto-close on selection

#### 9. Accessibility
- Full keyboard navigation (Tab, Enter, Arrow keys)
- `aria-current="page"` on active nav item
- `aria-expanded` on collapsible section headers
- `aria-label` on icon-only buttons
- Minimum 44px touch targets on mobile
- Focus indicators visible on all interactive elements
- Respect `prefers-reduced-motion`

#### 10. Data Freshness
- Show a **last-updated timestamp** or live indicator
- Subtle animation on price changes (flash green/red for 500ms)
- Consider a **manual refresh** button in the sidebar footer

### Anti-Patterns to Avoid

1. ❌ Don't put search in the sidebar — it belongs at the top center/top left of the main content area
2. ❌ Don't show more than 15 items without collapsible sections
3. ❌ Don't use icon-only navigation without labels (except in collapsed mode)
4. ❌ Don't auto-expand sections on hover — it's disorienting and inaccessible
5. ❌ Don't hide watchlists behind a click — they should be visible by default
6. ❌ Don't use the sidebar for advertising or promotional content
7. ❌ Don't make the sidebar wider than 320px — it steals too much content space

### Inspiration Ranking (Most → Least Applicable)

1. **TradingView** — Best overall sidebar system (icon bar + panels, pop-out, hover previews)
2. **Yahoo Finance** — Best for inline watchlist data display
3. **Stock Rover** — Best for hierarchical organization (tree view)
4. **Simply Wall St** — Best for clean, approachable design
5. **Finviz** — Best for filter/screener sidebar (niche use case)
6. **Google Finance** — Best for minimalism (but too simple for Stock Explorer)

---

## Summary

The ideal Stock Explorer sidebar should:
- Be a **persistent, collapsible sidebar** (240-280px default, 56px collapsed)
- Prioritize **watchlists** as the primary sidebar content with inline price data
- Use **icon + label** navigation with clear active states
- Support **drag-to-reorder, context menus, and hover previews** for power users
- Include a compact **market overview** at the bottom
- Be fully **responsive** with overlay mode on mobile
- Meet **WCAG 2.1 AA** accessibility standards
- Take the most inspiration from **TradingView's panel system** and **Yahoo Finance's inline data approach**

---

*Research compiled for Stock Explorer. For questions or updates, refer to the project's design docs.*
