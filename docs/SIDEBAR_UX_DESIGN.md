# Stock Explorer — Sidebar UX Design Specification

**Date:** 2026-06-09
**Author:** UX Research Agent (Hermes)
**Sources:** SIDEBAR_RESEARCH.md, SIDEBAR_GAP_ANALYSIS.md, DESIGN_SYSTEM.md
**Status:** Design recommendation — ready for Daniel's review

---

## Table of Contents

1. [Design System Compliance Summary](#1-design-system-compliance-summary)
2. [Gap Analysis Conflict Resolution](#2-gap-analysis-conflict-resolution)
3. [Final Sidebar Structure](#3-final-sidebar-structure)
4. [ASCII Mockups](#4-ascii-mockups)
5. [Component Hierarchy](#5-component-hierarchy)
6. [Detailed Specifications](#6-detailed-specifications)
7. [Collapsible Behavior & Animation](#7-collapsible-behavior--animation)
8. [Responsive Behavior](#8-responsive-behavior)
9. [Accessibility](#9-accessibility)
10. [What Was Rejected & Why](#10-what-was-rejected--why)

---

## 1. Design System Compliance Summary

The DESIGN_SYSTEM.md defines three strict zones:

| Zone | Purpose | Allowed | Forbidden |
|------|---------|---------|-----------|
| **A** — Top Navbar | Company name, price, tabs | Display-only info, tab buttons | Search box, filters, interactive controls |
| **B** — Sidebar | Global navigation only | Nav links, search, hot stocks/ETFs, watchlist links | **Charts, data tables, page content** |
| **C** — Main Content | Pure data + charts | Charts, data, interactive controls | — |

**The sidebar is a navigation surface, not a data surface.** This is the single most important rule governing all decisions in this document.

---

## 2. Gap Analysis Conflict Resolution

The gap analysis (SIDEBAR_GAP_ANALYSIS.md) proposed several features that conflict with the design system. Here is the resolution for each:

### Conflict 1: Inline Price Data in Sidebar

**Gap analysis proposed:** Show `2330 台積電 270 ▲` (stock name + price + change) for each stock in the sidebar watchlist section.

**Conflict:** DESIGN_SYSTEM Zone B rule: "Must NOT contain: charts, data tables, or page content." Individual stock prices with change indicators constitute data content that belongs in Zone C.

**Resolution:** ❌ **Rejected.** Stock prices, changes, and sparkline charts must NOT appear in the sidebar. The sidebar shows watchlist *names* (navigational links), not watchlist *contents* (data). Clicking a watchlist name navigates to the watchlist page in Zone C where data is displayed.

### Conflict 2: Market Overview with Sparklines

**Gap analysis proposed:** Show market indices with mini sparklines at the bottom of the sidebar (e.g., `加權指數 22,341 ▲ [sparkline]`).

**Conflict:** Sparklines are charts. Zone B forbids charts. Live index prices are data content.

**Resolution:** ❌ **Rejected.** Market overview with prices and sparklines belongs in Zone C (e.g., a "Markets" page or dashboard widget), not in the sidebar. The sidebar may contain a **nav link** to the Markets page.

### Conflict 3: Search Box Placement

**Gap analysis proposed:** Move search box out of sidebar to top-center.

**Conflict:** None. DESIGN_SYSTEM Section 3.5 explicitly says "Search box" is part of the sidebar. Zone A forbids search. The gap analysis recommendation to remove search from sidebar actually contradicts the design system.

**Resolution:** ⚠️ **Partial resolution.** The search box **stays in the sidebar** per DESIGN_SYSTEM Section 3.5. However, it should be the **first item** at the top of the sidebar (not buried), matching the industry pattern where search is prominent. This is consistent with the design system — no conflict.

### Conflict 4: Collapsible Sections

**Gap analysis proposed:** Make watchlist, hot stocks, and hot ETFs sections collapsible.

**Conflict:** None. Collapsible nav sections are a navigation pattern, not data content. This is fully compatible with Zone B's "global navigation" purpose.

**Resolution:** ✅ **Accepted.** All stock/ETF sections should be collapsible with section headers.

### Conflict 5: Icon + Label Navigation

**Gap analysis proposed:** Add icons to nav items for visual hierarchy.

**Conflict:** None. Icons in nav items are a navigation enhancement, not data content.

**Resolution:** ✅ **Accepted.** All primary nav items use icon + label.

### Conflict 6: Badge on Event Dashboard

**Gap analysis proposed:** Show a notification badge `(3)` on the Event Dashboard link.

**Conflict:** None. A badge on a nav item is a navigation indicator (like "3 unread messages"), not page content.

**Resolution:** ✅ **Accepted.** Badge shows unread event count.

### Conflict 7: Resizable Sidebar Width

**Gap analysis proposed:** Let users drag to resize sidebar width.

**Conflict:** None. This is a layout behavior, not content.

**Resolution:** ✅ **Accepted** (P1 priority). Resizable with min/max constraints.

### Conflict 8: Hover Mini Chart Preview

**Gap analysis proposed:** Hovering a stock in the sidebar shows a mini chart tooltip.

**Conflict:** A mini chart is a chart. Zone B forbids charts. Even as a tooltip, this would display data content in the sidebar.

**Resolution:** ❌ **Rejected.** Hover previews with charts belong in Zone C. The sidebar is nav-only.

### Conflict 9: Drag-to-Reorder

**Gap analysis proposed:** Drag to reorder watchlist items.

**Conflict:** None. Reordering nav items is a navigation organization feature.

**Resolution:** ✅ **Accepted** (P2 priority). Nice-to-have for power users.

### Conflict 10: Right-Click Context Menu

**Gap analysis proposed:** Right-click on stock items for actions (add alert, remove, etc.).

**Conflict:** None. Context menus on nav items are navigation controls.

**Resolution:** ✅ **Accepted** (P2 priority). But must also have visible alternative (accessibility).

---

## 3. Final Sidebar Structure

The sidebar contains **only navigation elements**, organized top-to-bottom in this exact order:

```
┌──────────────────────────────┐
│ 🔍 股識                       │  ← Brand header (always visible)
│ 認識一家公司，從這裡開始         │
├──────────────────────────────┤
│ 🔎 搜尋股票...                │  ← Search box (always visible, top)
├──────────────────────────────┤
│ 📊 總覽                       │  ← Primary nav (icon + label)
│ 📈 分類瀏覽                    │
│ 📰 新聞                       │
│ 📉 市場總覽                    │
├──────────────────────────────┤
│ ⭐ 我的關注            [+][▾] │  ← Collapsible section
│   ├─ 關注清單 1          (5) │     Nav links only — no prices
│   ├─ 關注清單 2          (3) │     Count = number of stocks
│   └─ 關注清單 3          (8) │
├──────────────────────────────┤
│ 🔥 熱門股票               [▾] │  ← Collapsible section
│   ├─ 2330 台積電              │     Stock buttons (nav only)
│   ├─ 2317 鴻海                │     No price data
│   ├─ 2454 聯發科              │
│   └─ ... (9 total)           │
├──────────────────────────────┤
│ 🏷️ 熱門 ETF               [▾] │  ← Collapsible section
│   ├─ 0050 元大台灣50          │
│   ├─ 0056 元大高股息          │
│   └─ ... (5 total)           │
├──────────────────────────────┤
│ 🔔 事件儀表板           (3)   │  ← Nav link with badge
│ ⚙️ 設定                       │  ← Settings nav link
├──────────────────────────────┤
│ ── 免責宣告 ──                │  ← Legal disclaimer (footer)
│ 本工具不提供投資建議...         │
└──────────────────────────────┘
```

### Priority-to-Section Mapping

| Priority | Feature | Section | Design System Status |
|----------|---------|---------|---------------------|
| P0 | Sidebar re-expandable after collapse | Global behavior | ✅ Required by DS |
| P0 | Search box | Top of sidebar | ✅ Required by DS 3.5 |
| P0 | Multiple watchlist management | 我的關注 section | ✅ Nav feature |
| P0 | Market overview access | 📉 市場總覽 nav link | ✅ Nav link (not data) |
| P1 | Category browse shortcut | 📈 分類瀏覽 nav link | ✅ Nav feature |
| P1 | Icon + label nav | All nav items | ✅ Nav enhancement |
| P1 | Resizable width | Global behavior | ✅ Layout feature |
| P2 | Notification badge | 事件儀表板 | ✅ Nav indicator |
| P2 | Drag-to-reorder | Watchlist section | ✅ Nav organization |
| P2 | Right-click context menu | Stock items | ✅ Nav control |

---

## 4. ASCII Mockups

### 4.1 Expanded State (Default) — 260px

```
┌──────────────────────────────┐
│ 🔍 股識                       │
│ 認識一家公司，從這裡開始         │
├──────────────────────────────┤
│ 🔎 搜尋股票...                │
├──────────────────────────────┤
│ 📊 總覽                       │
│ 📈 分類瀏覽                    │
│ 📰 新聞                       │
│ 📉 市場總覽                    │
├──────────────────────────────┤
│ ⭐ 我的關注            [+][▾] │
│   ▸ 關注清單 1          (5)   │
│   ▸ 關注清單 2          (3)   │
│   ▸ 關注清單 3          (8)   │
├──────────────────────────────┤
│ 🔥 熱門股票               [▾] │
│   ▸ 2330 台積電               │
│   ▸ 2317 鴻海                 │
│   ▸ 2454 聯發科               │
│   ▸ 2382 廣達                 │
│   ▸ 2303 聯電                 │
│   ▸ 2308 台達電               │
│   ▸ 2412 中華電               │
│   ▸ 3008 大立光               │
│   ▸ 1301 台塑                 │
├──────────────────────────────┤
│ 🏷️ 熱門 ETF               [▾] │
│   ▸ 0050 元大台灣50           │
│   ▸ 0056 元大高股息           │
│   ▸ 00878 國泰高股息          │
│   ▸ 00929 中信台泥            │
│   ▸ 0051 元大中型100          │
├──────────────────────────────┤
│ 🔔 事件儀表板           (3)   │
│ ⚙️ 設定                       │
├──────────────────────────────┤
│ ── 免責宣告 ──                │
│ 本工具不提供投資建議...         │
└──────────────────────────────┘
```

### 4.2 Collapsed State — 56px icon-only

```
┌──────┐
│  🔍  │  ← Brand icon only
├──────┤
│  🔎  │  ← Search icon (opens search overlay on click)
├──────┤
│  📊  │  ← Nav icons only (tooltips on hover)
│  📈  │
│  📰  │
│  📉  │
├──────┤
│  ⭐  │  ← Section icons (click to expand that section)
├──────┤
│  🔥  │
├──────┤
│  🏷️  │
├──────┤
│  🔔  │  ← Badge preserved on collapsed icon
│  ⚙️  │
└──────┘
```

### 4.3 Partial Collapse — Sections Collapsed, Nav Visible

```
┌──────────────────────────────┐
│ 🔍 股識                       │
│ 認識一家公司，從這裡開始         │
├──────────────────────────────┤
│ 🔎 搜尋股票...                │
├──────────────────────────────┤
│ 📊 總覽                       │
│ 📈 分類瀏覽                    │
│ 📰 新聞                       │
│ 📉 市場總覽                    │
├──────────────────────────────┤
│ ⭐ 我的關注            [+][▸] │  ← Collapsed: items hidden
├──────────────────────────────┤
│ 🔥 熱門股票               [▸] │  ← Collapsed: items hidden
├──────────────────────────────┤
│ 🏷️ 熱門 ETF               [▸] │  ← Collapsed: items hidden
├──────────────────────────────┤
│ 🔔 事件儀表板           (3)   │
│ ⚙️ 設定                       │
├──────────────────────────────┤
│ ── 免責宣告 ──                │
└──────────────────────────────┘
```

---

## 5. Component Hierarchy

```
Sidebar (Zone B)
├── BrandHeader
│   ├── LogoIcon ("🔍")
│   ├── BrandName ("股識")
│   └── Tagline ("認識一家公司，從這裡開始")
│
├── SearchBox
│   ├── Input (placeholder: "例如：2330 或 台積電")
│   └── SearchIcon
│
├── PrimaryNav
│   ├── NavItem (icon: "📊", label: "總覽", active: boolean)
│   ├── NavItem (icon: "📈", label: "分類瀏覽")
│   ├── NavItem (icon: "📰", label: "新聞")
│   └── NavItem (icon: "📉", label: "市場總覽")
│
├── WatchlistSection (collapsible)
│   ├── SectionHeader
│   │   ├── Icon ("⭐")
│   │   ├── Title ("我的關注")
│   │   ├── AddButton ("+") — always visible
│   │   └── CollapseToggle ("▾"/"▸")
│   └── WatchlistList
│       ├── WatchlistItem (name: "關注清單 1", count: 5)
│       ├── WatchlistItem (name: "關注清單 2", count: 3)
│       └── WatchlistItem (name: "關注清單 3", count: 8)
│
├── HotStocksSection (collapsible)
│   ├── SectionHeader
│   │   ├── Icon ("🔥")
│   │   ├── Title ("熱門股票")
│   │   └── CollapseToggle ("▾"/"▸")
│   └── StockList
│       ├── StockButton (label: "2330 台積電", key: "hot_2330")
│       ├── StockButton (label: "2317 鴻海", key: "hot_2317")
│       └── ... (9 items total)
│
├── HotETFSection (collapsible)
│   ├── SectionHeader
│   │   ├── Icon ("🏷️")
│   │   ├── Title ("熱門 ETF")
│   │   └── CollapseToggle ("▾"/"▸")
│   └── ETFList
│       ├── ETFButton (label: "0050 元大台灣50", key: "etf_0050")
│       └── ... (5 items total)
│
├── EventDashboardLink
│   ├── Icon ("🔔")
│   ├── Label ("事件儀表板")
│   └── Badge (count: 3) — hidden when 0
│
├── SettingsLink
│   ├── Icon ("⚙️")
│   └── Label ("設定")
│
└── DisclaimerFooter
    └── Text ("本工具不提供投資建議，請諮詢專業人士")
```

---

## 6. Detailed Specifications

### 6.1 Dimensions

| Property | Value | Notes |
|----------|-------|-------|
| **Default expanded width** | 260px | Between Yahoo Finance (240px) and TradingView (280px) |
| **Minimum expanded width** | 220px | When user resizes narrower |
| **Maximum expanded width** | 320px | When user resizes wider |
| **Collapsed width** | 56px | Icon-only mode |
| **Section header height** | 40px | Includes icon + label + toggle |
| **Nav item height** | 40px | Minimum touch target |
| **Stock/ETF button height** | 36px | Slightly compact for dense lists |
| **Search box height** | 40px | Standard input height |
| **Brand header height** | 60px | Logo + tagline |
| **Disclaimer footer** | Auto | Wraps text, min 40px padding-bottom: 16px |

### 6.2 Typography

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Brand name | Noto Sans TC | 1.2rem | 700 | `#2C3E50` |
| Tagline | Noto Sans TC | 0.75rem | 400 | `#7F8C8D` |
| Nav item label | Noto Sans TC | 0.9rem | 500 | `#2C3E50` |
| Nav item active | Noto Sans TC | 0.9rem | 700 | `#2C3E50` |
| Section header | Noto Sans TC | 0.85rem | 600 | `#7F8C8D` |
| Stock/ETF label | Noto Sans TC | 0.85rem | 400 | `#2C3E50` |
| Count badge | Noto Sans TC | 0.7rem | 500 | `#7F8C8D` |
| Disclaimer | Noto Sans TC | 0.7rem | 400 | `#7F8C8D` |

### 6.3 Colors

| Element | State | Background | Text | Border/Left Accent |
|---------|-------|------------|------|--------------------|
| Sidebar | Default | `#FFFFFF` (or inherit Streamlit dark) | — | — |
| Nav item | Default | Transparent | `#2C3E50` | — |
| Nav item | Hover | `rgba(52, 152, 219, 0.08)` | `#2C3E50` | — |
| Nav item | Active | `rgba(52, 152, 219, 0.12)` | `#2C3E50` | Left: 3px solid `#3498DB` |
| Section header | Default | Transparent | `#7F8C8D` | — |
| Section header | Hover | `rgba(0, 0, 0, 0.04)` | `#2C3E50` | — |
| Stock button | Default | Transparent | `#2C3E50` | — |
| Stock button | Hover | `rgba(52, 152, 219, 0.08)` | `#2C3E50` | — |
| Stock button | Active | `rgba(52, 152, 219, 0.12)` | `#2C3E50` | Left: 3px solid `#3498DB` |
| Badge | — | `#E74C3C` | `#FFFFFF` | — |
| Collapse toggle | Default | Transparent | `#7F8C8D` | — |
| Collapse toggle | Hover | `rgba(0, 0, 0, 0.08)` | `#2C3E50` | — |

### 6.4 Spacing

| Element | Padding | Margin |
|---------|---------|--------|
| Sidebar container | 0 | 0 |
| Brand header | 16px 16px 12px 16px | 0 |
| Search box | 8px 16px | 0 |
| Nav items | 0 16px | 0 |
| Section header | 8px 16px | 0 |
| Section content | 0 0 8px 0 | 0 |
| Stock/ETF buttons | 0 16px 0 24px | 0 |
| Disclaimer | 12px 16px | 0 |
| Between sections | — | 4px (via `st.markdown("---")` or divider) |

---

## 7. Collapsible Behavior & Animation

### 7.1 Two-Level Collapse System

The sidebar supports **two independent collapse mechanisms**:

1. **Full sidebar collapse** (Streamlit native): The entire sidebar collapses to 56px icon-only mode. Streamlit provides the expand button (`[>]`) by default — **do NOT hide this with CSS** (per DESIGN_SYSTEM Section 3.5).

2. **Section-level collapse** (custom): Individual sections (我的關注, 熱門股票, 熱門 ETF) can be collapsed/expanded independently via section header toggle buttons.

### 7.2 Full Sidebar Collapse

| Property | Value |
|----------|-------|
| Trigger | Streamlit's built-in collapse button OR a custom collapse toggle in the brand header |
| Collapsed width | 56px |
| Expand mechanism | Streamlit's built-in `[>]` button (always visible, never hidden with CSS) |
| Animation | Handled by Streamlit (no custom animation needed) |
| State persistence | `session_state["sidebar_collapsed"]` |

**Critical rule (P0 bug fix):** The sidebar MUST be re-expandable after collapsing. This is the #1 bug reported by Daniel. Streamlit's default behavior already supports this — the issue is likely caused by custom CSS hiding the expand button. **Audit all CSS for `[data-testid="collapsedControl"]` hiding rules and remove them.**

### 7.3 Section-Level Collapse

| Property | Value |
|----------|-------|
| Trigger | Click section header collapse toggle (▾ / ▸) |
| Default state | All sections expanded |
| Animation | Smooth height transition, 150ms ease-in-out |
| State persistence | `session_state["section_watchlist_expanded"]`, etc. |
| Icon | ▾ = expanded, ▸ = collapsed |

**Animation spec:**
```css
.section-content {
  transition: max-height 150ms ease-in-out, opacity 150ms ease-in-out;
  overflow: hidden;
}
.section-content.collapsed {
  max-height: 0;
  opacity: 0;
}
.section-content.expanded {
  max-height: 500px;  /* enough for max items */
  opacity: 1;
}
```

### 7.4 Collapse State Matrix

| Full Sidebar | Section State | What User Sees |
|-------------|---------------|----------------|
| Expanded (260px) | All expanded | Full sidebar with all items |
| Expanded (260px) | Some collapsed | Sidebar with collapsed sections showing only headers |
| Expanded (260px) | All collapsed | Sidebar showing only headers + nav + search |
| Collapsed (56px) | N/A (ignored) | Icon-only bar with tooltips |

---

## 8. Responsive Behavior

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| **> 1024px** | 260px default | Persistent sidebar, full functionality, resizable |
| **768px – 1024px** | 240px default | Persistent sidebar, can collapse to icons |
| **< 768px** | Full-width overlay | Hidden behind hamburger, slides in as overlay, auto-close on selection |

**Mobile-specific:**
- Sidebar overlays content (does not push)
- Swipe-from-left gesture to open
- Tap outside to close
- Touch targets ≥ 44px height
- Auto-close after selecting a nav item

---

## 9. Accessibility

### 9.1 Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Move to next interactive element |
| `Shift + Tab` | Move to previous interactive element |
| `Enter` / `Space` | Activate focused element |
| `↑` / `↓` | Navigate within a section's items |
| `←` / `→` | Collapse/expand section (when section header focused) |
| `Escape` | Close sidebar on mobile |

### 9.2 ARIA Attributes

```html
<nav aria-label="Main navigation">
  <!-- Brand -->
  <div role="banner">...</div>

  <!-- Search -->
  <div role="search">
    <input aria-label="搜尋股票" placeholder="例如：2330 或 台積電" />
  </div>

  <!-- Nav items -->
  <a href="..." aria-current="page">📊 總覽</a>

  <!-- Collapsible section -->
  <div role="group" aria-labelledby="watchlist-header">
    <button id="watchlist-header"
            aria-expanded="true"
            aria-controls="watchlist-content">
      ⭐ 我的關注
    </button>
    <ul id="watchlist-content" role="list">
      <li><a href="...">關注清單 1 <span aria-label="5 支股票">(5)</span></a></li>
    </ul>
  </div>

  <!-- Badge -->
  <a href="...">
    🔔 事件儀表板
    <span aria-label="3 個未讀事件" class="badge">3</span>
  </a>
</nav>
```

### 9.3 Focus Management

- All interactive elements have visible focus indicators (outline: 2px solid `#3498DB`)
- Focus trap within sidebar when open on mobile
- Focus returns to trigger element when sidebar closes

### 9.4 Screen Reader Considerations

- Icon-only items in collapsed mode have `aria-label` with full text
- Badge counts are announced as "X 個未讀事件" not just "3"
- Section collapse state is announced via `aria-expanded`
- Active nav item uses `aria-current="page"`

### 9.5 Motion

- Respect `prefers-reduced-motion`: disable all collapse/expand animations
- No auto-expand on hover (motor impairment concern)

---

## 10. What Was Rejected & Why

These features from the gap analysis were **rejected** because they violate the DESIGN_SYSTEM Zone B rule ("Must NOT contain: charts, data tables, or page content"):

| # | Rejected Feature | Gap Priority | Reason |
|---|-----------------|-------------|--------|
| 1 | **Inline stock prices in sidebar** (e.g., `2330 台積電 270 ▲`) | P0 | Price data is content, not navigation. Belongs in Zone C. |
| 2 | **Market overview with sparklines** at sidebar bottom | P0 | Sparklines are charts. Charts are forbidden in Zone B. |
| 3 | **Mini chart tooltip on hover** | P2 | Charts in tooltips are still charts. Forbidden in Zone B. |
| 4 | **Real-time price change indicators** (flash green/red) | P2 | Price data display. Forbidden in Zone B. |

### Recommended Alternative Placements

| Rejected Sidebar Feature | Proper Zone C Placement |
|--------------------------|------------------------|
| Inline stock prices | Watchlist page in Zone C with full data table |
| Market overview + sparklines | "市場總覽" page in Zone C, or dashboard widget |
| Mini chart hover preview | Chart page in Zone C with full interactive chart |
| Price change flash | Stock detail page in Zone C |

### What Was Accepted

These gap analysis features were **accepted** because they are navigation features, not data content:

| # | Accepted Feature | Gap Priority | Section |
|---|-----------------|-------------|---------|
| 1 | Multiple watchlist management | P0 | 我的關注 section |
| 2 | Sidebar re-expandable (bug fix) | P0 | Global behavior |
| 3 | Category browse shortcut | P1 | 📈 分類瀏覽 nav link |
| 4 | Icon + label nav pattern | P1 | All nav items |
| 5 | Resizable sidebar width | P1 | Global behavior |
| 6 | Notification badge on events | P2 | 事件儀表板 link |
| 7 | Drag-to-reorder watchlists | P2 | Watchlist section |
| 8 | Right-click context menu | P2 | Stock items |

---

## Appendix A: Streamlit Implementation Notes

### A.1 Key Constraints

- Streamlit's `st.sidebar` is the container — all items go inside it
- `st.session_state` persists collapse states across reruns
- `st.rerun()` triggers page navigation on item click
- Button keys must follow format: `{function}_{stock_id}` (e.g., `hot_2330`, `etf_0050`)
- **Never hide Streamlit's built-in sidebar expand button with CSS**

### A.2 State Variables

```python
# Sidebar collapse state (managed by Streamlit natively)
# Do NOT override with custom CSS

# Section collapse states (custom)
session_state["section_watchlist_expanded"] = True   # default: expanded
session_state["section_hotstocks_expanded"] = True    # default: expanded
session_state["section_hotetf_expanded"] = True       # default: expanded

# Watchlist data
session_state["watchlists"] = [
    {"id": "wl_1", "name": "關注清單 1", "count": 5},
    {"id": "wl_2", "name": "關注清單 2", "count": 3},
    {"id": "wl_3", "name": "關注清單 3", "count": 8},
]

# Event badge
session_state["event_unread_count"] = 3
```

### A.3 Navigation Pattern

```python
# On sidebar item click:
def on_stock_click(stock_id: str):
    session_state["stock_id"] = stock_id
    session_state["page"] = "Business Card"
    st.rerun()

# On watchlist click:
def on_watchlist_click(watchlist_id: str):
    session_state["watchlist_id"] = watchlist_id
    session_state["page"] = "My Watchlist"
    st.rerun()
```

---

## Appendix B: Design System Pre-Development Checklist

Before implementing any sidebar changes, confirm:

- [ ] Sidebar contains ONLY navigation elements (no prices, charts, or data tables)
- [ ] Search box is in sidebar (Zone B), not in navbar (Zone A)
- [ ] Sidebar is collapsible AND re-expandable (Streamlit expand button visible)
- [ ] All buttons have unique keys following `{function}_{id}` format
- [ ] Section collapse states persist in `session_state`
- [ ] Active nav item has left accent bar (3px solid `#3498DB`)
- [ ] Badge on Event Dashboard hides when count is 0
- [ ] Disclaimer footer is always visible at bottom
- [ ] No CSS hides Streamlit's built-in sidebar expand control
- [ ] Touch targets ≥ 44px on mobile
- [ ] `aria-label` on all icon-only elements
- [ ] `prefers-reduced-motion` respected for collapse animations

---

*This document resolves all conflicts between the gap analysis recommendations and the design system. Features that would violate Zone B's "no charts/data/page content" rule have been rejected and redirected to Zone C placements. All accepted features are navigation-only enhancements.*

*For questions or updates, refer to DESIGN_SYSTEM.md and SIDEBAR_RESEARCH.md.*
