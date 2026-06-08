# 股識 Stock Explorer — Design System Specification

> This is a "must-follow before development" design baseline. All new features, new pages, and new components must be confirmed against this document before writing a single line of code.

---

## I. Design Philosophy

### Core Principles
1. **Historian, not stock picker** — Only say "what happened to this company," never give buy/sell advice
2. **PPT style** — One key point per page, image-first with text as supplement
3. **Ten-second test** — A novice can summarize the core concept after ten seconds
4. **Beginner-friendly** — All professional terms must have plain-language translations

### Design Decision Priority
```
Correctness > Clarity > Completeness > Aesthetics
```
It is better to show less than to show incorrect or confusing content.

---

## II. Layout Zone Division

Pages must strictly separate three zones — no mixing:

```
┌─────────────────────────────────────────────────┐
│  Zone A: Top Navigation Bar (Navbar)             │
│  Company name + price + tabs                     │
├──────────┬──────────────────────────────────────┤
│          │                                      │
│  Zone B  │  Zone C: Main Content Area           │
│  Sidebar │  Pure data + charts                  │
│  Nav     │  No interactive controls             │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

### Zone A: Top Navigation Bar
- **Left**: Company name + stock ticker + industry tag
- **Right**: Current price + change
- **Below**: Tabs (Business Card / Operational Checkup / Financial Health / Peer Comparison / Group Structure / Category Browse / ETF Zone / My Watchlist / Event Dashboard)
- Active tab shown in bold `**▎Tab Name**`, others as `st.button`
- **Must NOT contain**: search box, filters, or any interactive controls

### Zone B: Sidebar
- **Function**: Global navigation (search, hot stocks, hot ETFs, my watchlist, event dashboard)
- **Behavior**:
  - Default expanded (`initial_sidebar_state="expanded"`)
  - Must be re-expandable after collapsing (must not disappear)
  - On stock click: set `session_state["stock_id"]` + `session_state["page"] = "Business Card"` + `st.rerun()`
- **Must NOT contain**: charts, data tables, or page content

### Zone C: Main Content Area
- **Function**: Pure data display + charts
- **Principles**:
  - One core message per page
  - Charts take more space than text
  - Interactive controls (time range, metric toggles) placed at the top of the content area, clearly separated from data
  - Controls remain stable when data refreshes

---

## III. Component Specifications

### 3.1 Color System

| Purpose | Color | Hex Code |
|---------|-------|----------|
| Primary accent | Blue | `#3498DB` |
| Positive / Up | Green | `#27AE60` |
| Negative / Down | Red | `#E74C3C` |
| Card background | Light gray | `#F8F9FA` |
| Warning background | Light yellow | `#FEF9E7` |
| Tip background | Light orange | `#FFF8F0` |
| Primary text | Dark gray | `#2C3E50` |
| Secondary text | Gray | `#7F8C8D` |

**Rules**:
- Red/green only for price direction (up/down) and buy/sell signals
- Blue only for "clickable selections"
- No colors other than red, green, or blue may be used for status indication

### 3.2 Buttons

| Type | Style | Usage |
|------|-------|-------|
| Primary action | `use_container_width=True`, default color | View, search |
| Tab | `use_container_width=True`, default color | Navigation bar tabs |
| Sidebar item | `use_container_width=True`, default color | Hot stocks, ETFs |

**Rules**:
- All buttons must have a unique `key`
- Key format: `{function}_{stock_id}` or `{function}_{page}_{stock_id}`
- No duplicate keys (causes `StreamlitDuplicateElementKey` crash)

### 3.3 Cards

```html
<!-- Info card (blue border) -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
    <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{plain_language}</div>
</div>

<!-- Tip card (orange border) -->
<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.3rem;line-height:1.6;">{content}</div>
</div>
```

### 3.4 Charts

**General Rules**:
- Use Plotly (do not embed matplotlib directly)
- Transparent or dark background (to match the overall dark theme)
- All charts must have titles
- Scales must auto-adjust (fixed scales that clip data are not allowed)
- Chart height adapts to data volume

**Bar Charts**:
- Baseline fixed (y-axis starts at 0)
- On zoom, adjust y-axis height — do not scale the entire chart in a way that causes clipping

**Gantt / Timeline Charts**:
- x-axis is time, horizontally scrollable
- y-axis is items, fixed spacing
- On zoom, adjust axis spacing — do not clip content

**Comparison Charts**:
- When two companies are side by side, scales must be identical
- Must clearly indicate which specific items are leading/trailing
- Do not display multiple types of axes simultaneously (e.g., price + deviation rate) unless the chart has a toggle

**Chart Interactions**:
- Do not display "multiple coordinate systems" simultaneously (red/green buy/sell + arrows + negative-value axes)
- If different types of metrics need to be displayed, provide a toggle mechanism
- Negative-value axes are only reasonable for specific metrics (e.g., deviation rate)

### 3.5 Sidebar

- Search box: `label_visibility="collapsed"`, placeholder is "e.g.: 2330 or TSMC"
- Hot stocks/ETFs: one `st.button` per item, key is `hot_{sid}` / `etf_{sid}`
- On click, set `session_state["stock_id"]` and `session_state["page"]`, then `st.rerun()`
- After sidebar collapse, Streamlit shows the expand button by default (do not hide this button with CSS)

---

## IV. Interaction Pattern Specifications

### 4.1 Page Switching

**Must have a loading state**:
- Any page switch (sidebar click, tab click) must show `st.spinner` or `st.progress`
- The screen must not "freeze" for more than 0.5 seconds without any feedback
- Interactive controls remain available during data loading

**Switching flow**:
```
User click → show spinner → load data → render page → hide spinner
```

### 4.2 Data Update vs. UI Refresh

- **Data update**: handled in the service layer, does not directly manipulate the UI
- **UI refresh**: only triggered via `st.rerun()` at the router layer
- **Must NOT** call any Streamlit API in the data layer (`src/data/`)
- **Must NOT** call any Streamlit API in the service layer (`src/services/`)

### 4.3 Time Range Selection

- After selecting a time range, data must be reloaded
- If data does not change, it indicates a caching issue or the API was not called correctly
- Time range selector is placed at the top of the content area, clearly separated from charts

### 4.4 Error Handling

- Stock not found: show `st.error("Stock ID {stock_id} not found")`, do not crash
- API failure: show `st.warning("Data temporarily unavailable, please try again later")`, do not crash
- Empty data: show `st.info("No data available to display at this time")`, do not crash
- **Under no circumstances should Streamlit throw an uncaught exception**

---

## V. PPT Style Detailed Specifications

### 5.1 One Key Point Per Page
- Each page answers only one question:
  - Business Card: How does this company make money?
  - Operational Checkup: How does it make money? How stable is it?
  - Financial Health: How much is earned? How much is spent? How much is left?
  - Peer Comparison: How does it differ from the industry leader?
  - Group Structure: What is the relationship between parent and subsidiaries?

### 5.2 Text Limits
- Total text per page must not exceed 200 characters (excluding chart titles)
- Each plain-language explanation must not exceed 2 sentences
- Taglines must not exceed 15 characters

### 5.3 Chart Proportion
- Charts must occupy > 60% of the page area
- Maximum 3 charts per page
- Charts must be clearly separated (`st.markdown("---")`)

### 5.4 Typography
- Global font: `Noto Sans TC`
- Headings: `font-weight: 700`
- Values: `font-size: 1.6rem, font-weight: 700`
- Labels: `font-size: 0.85rem, color: #7F8C8D`
- Plain-language: `font-size: 0.85rem, color: #27AE60, font-style: italic`

---

## VI. Pre-Development Checklist

Before writing any new page or feature, confirm the following:

- [ ] Complies with layout zone division (Zone A navbar, Zone B sidebar, Zone C content)
- [ ] Color usage conforms to the color system
- [ ] Button keys are unique and follow naming conventions
- [ ] Page switching has a loading state
- [ ] Data layer does not depend on Streamlit
- [ ] Error handling is complete (not found, API failure, empty data)
- [ ] Chart scales auto-adjust
- [ ] Text volume conforms to PPT style limits
- [ ] Sidebar behavior is correct (collapsible and expandable)
- [ ] Passes the ten-second test (a beginner can understand the core message)

---

*Created: 2026-06-08*
*Maintainer: Main agent (PM)*
