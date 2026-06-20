# ADR-009: Layout Restructure — Two-Layer Navigation Architecture

## Status
Planned

## Date
2026-06-14

## Background

Currently all page navigation is placed in the sidebar, causing:
1. Too many sidebar items (16+ buttons), lacking hierarchy
2. Search box in the sidebar, which doesn't follow industry conventions
3. Page functions (business card, operation checkup, etc.) mixed with global functions (category browser, ETF)

## Decision

Adopt a **two-layer navigation architecture**, referencing the design patterns of VS Code and modern SaaS apps.

## New Layout Structure

```
┌─────────────────────────────────────────────────────┐
│  🔍 [Global Search Box]                            │  ← Top Bar (persistent)
├────┬────────────────────────────────────────────────┤
│ 📊 │                                                │
│ 📈 │         Main Content Area                      │
│ │ │         Pure data + charts                      │
│ 🔔 │                                                │
│ ⚙️ │                                                │
│    │    ┌─────────────────────────────┐             │
│    │    │ + Business Card             │  ← FAB     │
│    │    │   Operation Checkup         │   (floating)│
│    │    │   Financial Health          │             │
│    │    │   Peer Comparison           │             │
│    │    │   Group Structure           │             │
│    │    └─────────────────────────────┘             │
└────┴────────────────────────────────────────────────┘
 ↑
 Activity Bar (icon + text, collapsible)
```

### Top Search Bar
- Global search bar persists at the top
- Regardless of which page you're on, you can switch the stock being observed
- Replaces the current sidebar search box

### Left Activity Bar
- Only contains **top-level global navigation**: Overview, Category Browser, ETF Section, My Watchlist, Event Dashboard
- Icon + text design
- When collapsed, only icons are shown
- Settings button independently placed at the bottom

### Floating Action Button (FAB)
- Floating button in the bottom-right corner
- **Context-aware**: Based on the currently displayed stock, expands all analysis functions for that stock
- Clicking updates the main content area in-place, the top search bar remains unchanged

## Rationale

1. **Industry convention**: Search bar at the top is the standard for modern software
2. **Clear hierarchy**: Global navigation vs. page functions separated
3. **PPT style**: Main content area is more spacious, fitting the "one key point per page" principle
4. **Extensible**: Adding global functions only requires adding an icon to the Activity Bar

## Alternatives

| Option | Reason for Rejection |
|--------|---------------------|
| Keep current sidebar | Too many items, lacks hierarchy, search bar position doesn't follow convention |
| Top nav + sidebar | Limited native Streamlit support, high implementation cost |
| Hamburger menu | Hides commonly used functions, not suitable for data-intensive applications |

## Consequences

- ✅ Search bar position matches user expectations
- ✅ Clear navigation hierarchy
- ✅ More spacious main content area
- ⚠️ Need to refactor the layout logic in main.py
- ⚠️ FAB requires custom Streamlit components
