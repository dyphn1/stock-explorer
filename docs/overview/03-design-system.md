# Design System — Stock Explorer

> **Status**: Baseline specification | **Last Updated**: 2026-06-17

---

## 1. Design Philosophy

### Core Principles
1. **Historian, not stock picker** — Only say "what happened to this company," never give buy/sell advice
2. **PPT style** — One key point per page, image-driven, text-assisted
3. **10-second test** — Beginners can restate the core concept within 10 seconds
4. **Beginner-friendly** — All professional terms must have plain-language translations

### Design Decision Priority
```
Correctness > Clarity > Completeness > Aesthetics
```

---

## 2. Layout Zones

Pages are strictly divided into three zones that must not be mixed:

```
┌─────────────────────────────────────────────────┐
│  Zone A: Top Navigation Bar (Navbar)             │
│  Company name + stock price + page tabs          │
├──────────┬──────────────────────────────────────┤
│          │                                      │
│  Zone B  │  Zone C: Main Content Area            │
│  Sidebar │  Pure data + charts                   │
│  Navigation │  No interactive controls          │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

### Zone A: Top Navigation Bar
- **Left**: Company name + stock ID + industry tag
- **Right**: Current price + change
- **Bottom**: Page tabs (Business Card / Operations Checkup / Financial Health / Peer Comparison / Group Structure / Category Browser / ETF Section / My Watchlist / Event Dashboard)
- Must NOT contain: search box, filters, any interactive controls

### Zone B: Sidebar
- **Function**: Global navigation (search, hot stocks, hot ETFs, my watchlist, event dashboard)
- **Behavior**: Default expanded, can be collapsed and re-expanded
- Must NOT contain: charts, data tables, page content

### Zone C: Main Content Area
- **Function**: Pure data display + charts
- **Principle**: One core message per page, chart space greater than text
- Interactive controls (time range, metric toggles) placed at top of content area, clearly separated from data

---

## 3. Color System

| Usage | Color | Hex Code |
|-------|-------|----------|
| Primary accent | Blue | `#3498DB` |
| Positive / Up | Green | `#27AE60` |
| Negative / Down | Red | `#E74C3C` |
| Card background | Light gray | `#F8F9FA` |
| Warning background | Light yellow | `#FEF9E7` |
| Tip background | Light orange | `#FFF8F0` |
| Primary text | Dark gray | `#2C3E50` |
| Secondary text | Gray | `#7F8C8D` |

### Extended Color Tokens

| Token | Hex | Usage |
|-------|-----|-------|
| `medium` | `#E67E22` | Amber/orange for medium-priority items |
| `border_light` | `#E1E4E8` | Structural borders/dividers |
| `accent_purple` | `#9B59B6` | Sector heatmap accent |
| `white` | `#FFFFFF` | Pure white |
| `positive_bg` | `#E8F8F0` | Light positive bg tint |
| `negative_bg` | `#FDEDEC` | Light negative bg tint |
| `teal` | `#16A085` | Sector heatmap accent |
| `card_bg_alt` | `#ECF0F1` | Alternate card bg |

**Rules**:
- Red/green only used for price change context, never for decoration
- All text-to-background contrast must meet WCAG AA standards
- Chart colors use Plotly default palette for consistency

---

## 4. Typography

| Level | Usage | Size |
|-------|-------|------|
| H1 | Page title | 24px |
| H2 | Section title | 20px |
| H3 | Card title | 16px |
| Body | Body text | 14px |
| Caption | Supporting text | 12px |

**Chinese font**: System default (PingFang / Microsoft JhengHei)
**English font**: System default (San Francisco / Segoe UI)
**Numeric font**: Monospace (for data alignment)

---

## 5. Component Specifications

### 5.1 Metric Card
```
┌────────────────────────────┐
│  📊 Revenue Growth Rate     │
│  ────────────────────────  │
│  +12.5%                    │
│  12.5% growth vs same month last year │
│  "For every 100 dollars of revenue, 12.5 dollars more" │
└────────────────────────────┘
```
- Title + icon
- Large number
- Plain-language explanation
- Real-world analogy (optional)

### 5.2 Chart Container
- Use Plotly interactive charts
- Every chart must have a title above it
- Data source annotation below
- Hover tooltip shows exact value + plain-language explanation

### 5.3 Navigation Components
- Sidebar buttons: `st.button` + `use_container_width=True`
- Page tabs: Active tab uses `**▎Tab Name**`, others use `st.button`
- After navigation, must update both `st.session_state` and `st.query_params`

---

## 6. State Handling

### 6.1 Loading State
- Show `st.spinner` during page transitions
- Chart area shows skeleton placeholder during data loading

### 6.2 Error State
- API failure: Show friendly error message + retry button
- No data: Show "No data available" empty state + guidance text
- Single section failure does not affect other sections

### 6.3 Empty State
- Empty watchlist: Show guidance text + "Explore Stocks" button
- No search results: Show "No matching stocks found" + suggestions

---

## 7. HTML Prototypes

> 📁 HTML prototypes for all pages are in `design/prototypes/`, maintained by the UX Designer.

### Prototype Directory
```
design/
├── index.html                 # Design entry: preview index of all pages
├── prototypes/                # HTML prototypes for each page
│   ├── business_card.html     # Business card page ✅
│   ├── operation_checkup.html # Operations checkup
│   ├── financial_health.html  # Financial health
│   ├── peer_comparison.html   # Peer comparison
│   ├── group_structure.html   # Group structure
│   ├── category_browser.html  # Category browser
│   ├── etf_browser.html       # ETF browser
│   ├── watchlist.html         # My watchlist
│   ├── event_dashboard.html   # Event dashboard
│   └── daily_market.html      # Daily market overview
├── components/                # Reusable components
│   ├── _navbar.html           # Top navigation bar
│   ├── _sidebar.html          # Sidebar
│   └── _card.html             # Data card
├── assets/                    # CSS, design variables
│   ├── design-tokens.css      # Design system variables
│   └── base.css               # Global base styles
├── specs/                     # Design specifications
└── reviews/                   # Design review reports
```

### Prototype Usage
1. **Daniel reviews**: Open `design/index.html` → click page card → preview in browser
2. **Developer implements**: Reference layout, spacing, colors from prototype files
3. **Design Reviewer reviews**: Compare Streamlit implementation side-by-side with prototype

## 8. Accessibility

- All images must have alt text
- Color is not the only way to convey information (use icons, text)
- Interactive elements must have clear labels
- All interactive elements must be keyboard-navigable
