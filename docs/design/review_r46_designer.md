# Design Review — Round 46 (2026-06-15)

> **Author**: Design Reviewer
> **Date**: 2026-06-15
> **Context**: Round 46 review — design improvements and competitor design comparison. Analyzing D-121 through D-124, 15 remaining `unsafe_allow_html=True` instances, and competitor design patterns from Rounds 8 & 9.
> **Current Design Grade**: A (maintained)

---

## Table of Contents

1. [Current Design Health Assessment](#current-design-health-assessment)
2. [Inline HTML Status Audit](#inline-html-status-audit)
3. [Competitor Design Comparison](#competitor-design-comparison)
4. [Top 5 Design Improvement Recommendations](#top-5-design-improvement-recommendations)
5. [Design System Updates Needed](#design-system-updates-needed)
6. [Upcoming Feature Design Considerations](#upcoming-feature-design-considerations)
7. [Updated Issue Checklist](#updated-issue-checklist)

---

## Current Design Health Assessment

### Design System Coverage: B+

The design system at `docs/design/design_system.md` (236 lines) covers the foundational elements well:
- **Zone A/B/C layout** — clearly defined with rules for each zone
- **Color system** — 9 colors with specific usage rules
- **Button specifications** — 3 types with key naming conventions
- **Card components** — 2 card types (info card, tip card) with HTML templates
- **Chart rules** — general rules plus bar, gantt, and comparison specifics
- **Interaction patterns** — page switching, data updates, time range, error handling
- **PPT-style specs** — text limits, chart proportions, typography

**Gaps identified:**
- Only 2 card types documented (info card, tip card), but `_router_base.py` has 5+ components (`_info_card`, `_summary_card`, `_白话_card`, `_subsidiary_card`, `_count_label`)
- No documentation for `_mini_score_card`, `_glossary_tooltip`, `_so_what_box`, `_health_score_card` (planned components for C170, C204)
- No "Component Gallery" section showing all components with APIs and usage examples
- No empty state component specification
- No loading state component specification
- No tooltip/glossary component specification

### Inline HTML Status: 15 Instances Remaining

| File | Count | Context |
|------|-------|---------|
| `_router_base.py` | 10 | Component definitions (card rendering functions) |
| `_helpers.py` | 4 | Helper formatting functions |
| `_financial.py` | 1 | Financial metric display |

**Assessment**: The 10 instances in `_router_base.py` are *by design* — these are the shared component definitions that use `unsafe_allow_html=True` to render styled cards. This is an acceptable pattern since it centralizes HTML in one file. The 4 in `_helpers.py` and 1 in `_financial.py` should be migrated to use Streamlit-native components or consolidated into `_router_base.py`.

**CI enforcement** prevents new inline HTML instances, which is the correct control mechanism.

### Consistency Score: B+

| Dimension | Score | Notes |
|-----------|-------|-------|
| Zone A/B/C Compliance | A | All pages properly separate zones |
| PPT-Style Adherence | A- | Core principle followed; watchlist page (D-123) is the exception |
| Card Component Consistency | B | D-122 (sector heatmap), D-124 (ETF browser) create visual inconsistency |
| Color System | A | Well-defined and followed |
| Plain-Language System | A | Core feature, well-implemented |
| Loading/Error States | B | Inconsistent across pages |
| Mobile Responsiveness | B- | D-006 unresolved |
| Design System Documentation | B | Exists but incomplete (D-121) |

---

## Competitor Design Comparison

### Public.com (Round 8)

**What they do well:**
- **Story cards**: Every stock has a narrative-first "story card" that explains the company in plain language — directly aligned with Stock Explorer's "historian" positioning
- **Quick Summary**: 3-5 bullet point synthesis at the top of each stock page — addresses the "ten-second test"
- **Hierarchical revenue tree**: Shows how money flows through the business (TSMC → 5nm chips → Apple/NVIDIA/AMD)
- **Clean, card-based layout**: Generous whitespace, minimal text, visual-first

**What we can learn:**
- The "story card" concept is exactly what Stock Explorer's business card page should be — but Public.com executes it more cleanly with better visual hierarchy
- Their quick summary directly addresses the "ten-second test" — our C37 (Key Takeaways) was approved but implementation quality needs to match
- Revenue tree visualization is more informative than our pie chart alone

**Gap:** Public.com's story cards are more visually polished. Our PPT-style approach has the right philosophy but the execution (card styling, spacing, typography) needs refinement to match their clean aesthetic.

---

### Simply Wall St (Round 9)

**What they do well:**
- **Snowflake diagram**: Proprietary 5-dimension visual health score — gives beginners an instant, intuitive answer to "how healthy is this company?"
- **Infographic-style layout**: Every stock page reads like an infographic, not a financial report — directly comparable to our PPT-style approach
- **Visual risk breakdown**: Shows what could go wrong with visual indicators, not just numbers
- **Progressive disclosure**: Summary first, details on click — aligns with our "progressive drill-down" principle
- **Color-coded scoring**: Green/yellow/red for good/neutral/bad — instantly understandable

**What we can learn:**
- Simply Wall St is the closest international competitor to Stock Explorer's design philosophy (visual-first, one key concept per screen, minimal text)
- Their snowflake diagram proves that a visual health score is expected by beginners — our C43 (Snowflake) was approved and should be prioritized
- Their infographic-style layout is the gold standard for what we're trying to achieve with PPT-style
- The risk visualization approach (visual breakdown, not just numbers) is something we should adopt for C44

**Gap:** Simply Wall St's snowflake is proprietary and polished. Our C43 implementation needs to match their visual quality. Their infographic reports are more visually sophisticated than our current card-based layout.

---

### Investopedia (Round 9)

**What they do well:**
- **Financial Dictionary**: 10,000+ terms with detailed, beginner-friendly definitions — the gold standard for financial glossary
- **Concept-first approach**: Teaches concepts before showing data — aligns with our "education-first" positioning
- **Structured learning paths**: Academy courses from absolute beginner to advanced
- **Embedded definitions**: Terms within articles link to definitions — contextual learning

**What we can learn:**
- Investopedia's financial dictionary is exactly what C170 (Tappable Glossary) should become — but integrated into stock pages, not a separate section
- Their concept-first approach validates our "historian" positioning — we explain what happened, not what to buy
- The embedded definition pattern (tap a term → see definition) is the right UX for C170

**Gap:** Investopedia has a comprehensive glossary system that Stock Explorer completely lacks. C170 (Tappable Glossary) is critical to close this gap. Their structured learning paths (Academy) are also something we should model for C47.

---

### Stockopedia (Round 9)

**What they do well:**
- **StockRank system**: Single composite score (0-100) combining value, quality, and momentum — makes stock evaluation accessible
- **StockReport**: Detailed analysis report with scores and commentary
- **Stockopedia Academy**: Structured learning paths from beginner to advanced
- **Progressive complexity**: Simple scores → detailed analysis

**What we can learn:**
- StockRank validates the demand for a composite health score — our C204 (Confidence Indicator) should provide a similar at-a-glance assessment
- Their "Quality + Value + Momentum" three-factor framework educates users about different investment approaches — we could adopt a similar multi-dimension approach
- The progressive complexity model (simple → detailed) aligns with our "progressive drill-down" principle

**Gap:** Stockopedia's StockRank is a polished scoring system. Our C204 (Confidence Indicator) needs to provide similar clarity but with our "historian" twist — explaining confidence in plain language, not just showing a number.

---

### Zerodha Varsity (Round 11)

**What they do well:**
- **Module-based learning**: 14 structured modules with progressive difficulty (1→14)
- **One concept per page**: Directly aligned with our PPT-style "one key point per page"
- **Culturally localized examples**: All examples use Indian stocks — exactly what we do for TW stocks
- **Quizzes**: End-of-module assessment to test understanding
- **Clean reading experience**: Minimal UI chrome, focused on content

**What we can learn:**
- Zerodha Varsity is the closest philosophical match to Stock Explorer globally
- Their module-based structure with numbered progression (1→14) is the right model for our planned C47 (Education Academy)
- The quiz system is a gap — Stock Explorer has no assessment mechanism
- Their "one concept per page" approach validates our PPT-style principle

**Gap:** Zerodha Varsity teaches concepts (not companies) while we teach companies (not concepts). Their quiz system is something we should adopt. Their module completion tracking would improve engagement.

---

### Finimize (Round 11)

**What they do well:**
- **Bite-sized content**: Every piece is 3 minutes or less — respects user attention
- **"Market Mood" indicator**: Simple visual sentiment indicator (😰→😊→🤩) — beginners understand instantly
- **Completion certificates**: Finimize Academy gives credentials that beginners can share
- **Daily engagement loop**: Newsletter → app → community drives retention
- **Clean, modern design**: Minimalist with generous whitespace

**What we can learn:**
- Finimize's "Market Mood" indicator validates our C35 (Market Mood Index) concept
- Their completion certificates are a credentialing mechanism that C47 (Education Academy) should adopt
- The bite-sized approach (3 minutes or less) aligns with our "ten-second test" — if users can't understand in 10 seconds, the content is too complex
- Their clean, modern design with generous whitespace is the aesthetic standard we should target

**Gap:** Finimize's daily engagement loop (newsletter → app → community) is a retention model Stock Explorer completely lacks. Their "Market Mood" indicator is a simplified version of what we're building.

---

## Top 5 Design Improvement Recommendations

### Rec 1: Create Component Gallery in Design System Doc

**Problem (D-121):** The design system documents only 2 card types but `_router_base.py` has 5+ components. New components (`_mini_score_card`, `_glossary_tooltip`, `_so_what_box`, `_health_score_card`) are planned but undocumented. Developers creating new pages don't have a single reference for available components, leading to inline HTML reinvention.

**Recommendation:** Add a "Component Gallery" section to `docs/design/design_system.md` documenting ALL shared components:
- `_info_card(label, value, plain_language)` — blue-border info card
- `_summary_card(title, bullets)` — summary card with bullet points
- `_白话_card(label, value, analogy)` — plain-language explanation card
- `_subsidiary_card(name, hold_label, hold_color, holding, revenue, business, relation)` — subsidiary info card
- `_count_label(text)` — muted count label
- `_mini_score_card()` — planned for C204
- `_glossary_tooltip()` — planned for C170
- `_so_what_box()` — planned for C188
- `_health_score_card()` — planned for C204
- `_empty_state(icon, title, subtitle)` — standardized empty state (new)
- `_section_title(title, icon)` — standardized section header
- `_historian_disclaimer()` — historian positioning disclaimer

Each entry should include: purpose, API signature, HTML template, usage example, and design rules.

**Affected Files:** `docs/design/design_system.md`
**Effort:** 2-3h
**Priority:** P1 — directly addresses D-121 and prevents future inline HTML proliferation

---

### Rec 2: Standardize Card Styling Across All Pages

**Problem (D-122, D-124):** Sector heatmap uses non-standard padding/border-radius/background. ETF browser uses inline HTML for colored values and table-like rows. These create visual inconsistency that makes the product feel like it was built by different teams.

**Recommendation:** 
1. Refactor `sector_heatmap.py` (lines 342-362, 391-444) to use shared card components from `_router_base.py` instead of inline HTML grid cells
2. Refactor `etf_browser.py` (lines 145-155, 397-411) to replace inline HTML colored values with `_info_card()` or a new `_metric_value_card()` component
3. Create a new `_data_row()` component in `_router_base.py` for table-like rows that need colored values — this replaces the inline HTML pattern with a standardized component

**Affected Files:** `src/pages/sector_heatmap.py`, `src/pages/etf_browser.py`, `src/ui/_router_base.py`
**Effort:** 3-5h
**Priority:** P1 — directly addresses D-122 and D-124, improves consistency score

---

### Rec 3: Redesign Watchlist Page to PPT-Style Card Layout

**Problem (D-123):** Watchlist page uses dense table layout (columns) instead of card-based PPT style. This is the only page that feels like a different product — violating the core design principle of "one key point per page."

**Recommendation:** Redesign the watchlist page using a card-based layout:
- Each watchlist item becomes a card showing: company name, ticker, current price, change %, and a one-line plain-language summary
- Cards use the standard `_info_card()` or a new `_watchlist_card()` component
- Add a "remove" action button on each card (key: `remove_{stock_id}`)
- Show 6-8 cards per page with pagination or infinite scroll
- Empty watchlist shows `_empty_state(icon="📭", title="尚未加入任何股票", subtitle="搜尋股票後點擊「加入觀察清單」")`

**Affected Files:** `src/pages/watchlist_page.py`
**Effort:** 4-6h
**Priority:** P1 — directly addresses D-123, critical for visual consistency

---

### Rec 4: Design C170 Tappable Glossary Component System

**Problem:** No glossary/tooltip system exists (D-121, D-012). Financial terms have no inline help. Investopedia's 10,000+ term dictionary and Zerodha Varsity's embedded definitions prove this is expected by beginners.

**Recommendation:** Design the `_glossary_tooltip()` component for C170:
- **Inline pattern**: Wrap financial terms in a styled span with a subtle underline (color: `#3498DB`, dotted)
- **Tap/click interaction**: Clicking the term opens a small overlay card (not a popup) with:
  - Term name (bold, `#2C3E50`)
  - One-sentence plain-language definition (`#27AE60`, italic)
  - "Why it matters" one-liner (optional)
  - Example with a TW stock (optional)
- **Visual style**: Use the standard card template (background: `#F8F9FA`, border-left: 4px solid `#3498DB`)
- **Data source**: Start with a curated glossary of 50 key terms (P/E, ROE, EPS, dividend yield, market cap, etc.)
- **Progressive enhancement**: Phase 1 = curated terms only; Phase 2 = LLM-generated definitions for any term

**Affected Files:** `src/ui/_router_base.py` (new `_glossary_tooltip()` component), `docs/design/design_system.md` (documentation)
**Effort:** Component design: 2-3h; Full implementation: 8-12h (C170)
**Priority:** P1 — C170 is an upcoming feature; designing the component now ensures consistency

---

### Rec 5: Design C188 "Why Did This Move?" Explanation Card

**Problem:** Beginners see stock price movements but don't understand why. Koyfin's "Recent Changes" and Finary's "What's New" prove that explaining price movements is expected. Stock Explorer's "historian" positioning is perfect for this — explaining what happened, not predicting what will happen.

**Recommendation:** Design the `_so_what_box()` component for C188:
- **Trigger**: Appears when a stock has a significant daily move (>3% or >5%)
- **Layout**: A single tip card (orange border, `#FFF8F0` background) with:
  - Icon: 📈 (up) or 📉 (down)
  - Headline: One-line plain-language explanation (e.g., "台積電今日上漲4.2%，因為蘋果新iPhone訂單超乎預期")
  - Context: 1-2 sentences of historical context (e.g., "過去一年，台積電因蘋果消息平均波動2.1%")
  - Source: Data source citation (e.g., "資料來源: FinMind, 2026-06-15")
- **Position**: Below the price in Zone A or at the top of Zone C
- **Design**: Use the existing tip card pattern from the design system (orange border, `#FFF8F0` background)

**Affected Files:** `src/ui/_router_base.py` (new `_so_what_box()` component), `docs/design/design_system.md` (documentation)
**Effort:** Component design: 1-2h; Full implementation: 8-10h (C188)
**Priority:** P1 — C188 is an upcoming feature; the component should be designed now

---

## Design System Updates Needed

The following additions/changes to `docs/design/design_system.md` are needed:

### 1. New Section: Component Gallery (after Section III)

Add a comprehensive "Component Gallery" section documenting all shared components:

```markdown
## III-A. Component Gallery

### Card Components

| Component | Purpose | Border Color | Background |
|-----------|---------|-------------|------------|
| `_info_card()` | Key metric display | Blue `#3498DB` | `#F8F9FA` |
| `_summary_card()` | Bullet-point summary | Blue `#3498DB` | `#F8F9FA` |
| `_白话_card()` | Plain-language explanation | Green `#27AE60` | `#F8F9FA` |
| `_tip_card()` | Tip / insight | Orange `#F39C12` | `#FFF8F0` |
| `_subsidiary_card()` | Subsidiary info | Blue `#3498DB` | `#F8F9FA` |
| `_mini_score_card()` | Mini score display | Varies by score | `#F8F9FA` |
| `_health_score_card()` | Health score summary | Varies | `#F8F9FA` |
| `_so_what_box()` | Price movement explanation | Orange `#F39C12` | `#FFF8F0` |
| `_glossary_tooltip()` | Term definition overlay | Blue `#3498DB` | `#F8F9FA` |
| `_empty_state()` | Empty data state | None | Transparent |
| `_data_row()` | Table-like row with colored values | None | Transparent |

### Label Components
| Component | Purpose | Style |
|-----------|---------|-------|
| `_count_label()` | Muted count display | `font-size:0.85rem, color:#7F8C8D` |
| `_section_title()` | Section header | `font-weight:700, color:#2C3E50` |
| `_historian_disclaimer()` | Historian positioning | Orange border, `#FFF8F0` background |
```

### 2. New Section: Glossary/Tooltip Pattern

Add a section under "Interaction Pattern Specifications" for the glossary tooltip pattern:
- Trigger: tap/click on underlined term
- Display: overlay card (not popup)
- Dismiss: tap outside or close button
- Animation: fade-in, 200ms

### 3. New Section: Read Time Indicator

Add a specification for C205 (Read Time):
- Display: "⏱️ 約X分鐘閱讀" in muted text (`#7F8C8D`, `0.85rem`)
- Position: Below section title or at top of content area
- Calculation: Based on word count (Chinese: ~300 chars/min)

### 4. New Section: Confidence Indicator

Add a specification for C204 (Confidence Indicator):
- Display: Visual indicator (🟢🟡🔴 or progress bar) with percentage
- Position: Near data displays or health scores
- Color coding: Green (>70%), Yellow (40-70%), Red (<40%)
- Plain-language: Always include a one-line explanation

### 5. Update Card Styling Rules

Update the card styling section to standardize:
- ALL cards must use `border-radius: 12px` and `padding: 1.2rem`
- ALL cards must use `border-left: 4px solid {color}` (no full borders)
- ALL cards must use `background: #F8F9FA` (no white backgrounds)
- Exception: `_subsidiary_card()` should be refactored to match standard styling

### 6. Add "No Inline HTML" Rule

Add to the Pre-Development Checklist:
- [ ] No `unsafe_allow_html=True` in new page files — all cards must use shared components from `_router_base.py`
- [ ] If a new card type is needed, add it to `_router_base.py` and document in design system first

---

## Upcoming Feature Design Considerations

### C170 Tappable Glossary

**Design Implications:**
- Requires a curated glossary data source (start with 50 key terms, expand over time)
- The `_glossary_tooltip()` component must be designed before implementation begins
- Terms need to be automatically detected and wrapped in page text — this requires a text processing layer
- Mobile consideration: tap targets must be at least 44x44px for accessibility
- The glossary should be consistent with the "historian" tone — definitions should explain what the term means in the context of understanding a company, not in the context of trading
- **Competitor reference**: Investopedia's embedded definitions are the gold standard; Zerodha Varsity's contextual explanations are the model for plain-language

### C188 Why Did This Move?

**Design Implications:**
- Requires a "significant move" threshold definition (suggest >3% daily change)
- The `_so_what_box()` component must be designed before implementation
- Explanation generation can be template-based initially (e.g., "{stock}今日{change}，因為{reason}")
- The "reason" data source needs to be identified — could be news sentiment, earnings announcements, or sector movement
- Must maintain "historian" tone — explain what happened, don't predict what will happen
- **Competitor reference**: Koyfin's "Recent Changes" and Finary's "What's New" are the models; Simply Wall St's risk visualization provides the visual pattern

### C204 Confidence Indicator

**Design Implications:**
- Requires a confidence scoring algorithm (data freshness, data completeness, sample size)
- The `_mini_score_card()` and `_health_score_card()` components must be designed before implementation
- Visual design should use the standard color system (green/yellow/red) but with a distinct visual pattern (e.g., progress bar or gauge) to distinguish from other scores
- Must include plain-language explanation of what the confidence level means
- Position: near data displays, not as a standalone section
- **Competitor reference**: TipRanks' Smart Score (0-10) and Stockopedia's StockRank (0-100) are the models; Morningstar's uncertainty rating provides the "range" concept

### C205 Read Time

**Design Implications:**
- Simple calculation based on Chinese character count (~300 chars/min reading speed)
- Display: "⏱️ 約X分鐘閱讀" in muted text (`#7F8C8D`, `0.85rem`)
- Position: at the top of the content area, below the section title
- Should update dynamically if the page has expandable sections (show read time for expanded content)
- Low design impact — primarily a text label with a calculation
- **Competitor reference**: Finimize's "3-minute read" badge is the model; Medium's read time indicator is the UX pattern

---

## Updated Issue Checklist

### P0 — Blocking Issues
*(None)*

### P1 — Important Issues (4 items)

| ID | Title | Status | Effort | Proposed Sprint |
|----|-------|--------|--------|-----------------|
| D-121 | Design System Missing Documentation for New Components | ❌ Unresolved | 2-3h | Sprint 21 |
| D-122 | Inconsistent Card Styling in Sector Heatmap | ❌ Unresolved | 3-5h | Sprint 21 |
| D-123 | Watchlist Page Uses Non-PPT Layout | ❌ Unresolved | 4-6h | Sprint 21 |
| D-124 | ETF Browser Uses Inline HTML | ❌ Unresolved | 2-3h | Sprint 21 |

### P2 — Optimization Issues (New from this review)

| ID | Title | Status | Effort | Proposed Sprint |
|----|-------|--------|--------|-----------------|
| D-125 | No Glossary/Tooltip Component Designed | 🆕 New | 2-3h (design) | Sprint 21 |
| D-126 | No "Why Did This Move" Component Designed | 🆕 New | 1-2h (design) | Sprint 21 |
| D-127 | No Confidence Indicator Component Designed | 🆕 New | 2-3h (design) | Sprint 22 |
| D-128 | No Read Time Component Designed | 🆕 New | 0.5h (design) | Sprint 22 |

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | D-121 through D-124 resolved in Sprint 21; component gallery complete; all upcoming feature components designed before implementation |
| **Expected case** | A | D-121 and D-122 resolved; D-123 and D-124 deferred to Sprint 22; component gallery started |
| **Worst case** | A- | D-121 through D-124 deferred; new features implemented without component design; inline HTML count grows |

---

## Summary

### Key Findings

1. **Design system documentation is the #1 priority (D-121):** The design system exists but is incomplete. Without a comprehensive component gallery, developers will continue to reinvent card styles with inline HTML. This is the root cause of D-122 and D-124.

2. **Visual consistency is achievable in Sprint 21:** D-122 (sector heatmap) and D-124 (ETF browser) can be resolved by refactoring to use shared components. D-123 (watchlist) requires a full redesign but is scoped at 4-6h.

3. **Competitor designs validate our direction:** Simply Wall St's infographic approach, Public.com's story cards, and Zerodha Varsity's module-based learning all validate Stock Explorer's PPT-style, education-first positioning. The gap is in execution quality, not direction.

4. **Upcoming features need component design NOW:** C170, C188, C204, and C205 should have their components designed before implementation begins. This prevents the pattern of "implement first, design later" that created the current inline HTML problem.

5. **The "historian" positioning is a unique differentiator:** No competitor combines plain-language explanations with historical analysis for TW stocks. Simply Wall St comes closest but focuses on US/AU markets. This is our moat.

### Recommended Sprint 21 Design Priorities

1. **Component Gallery documentation** (D-121) — 2-3h — unblocks all other design work
2. **Sector heatmap card standardization** (D-122) — 3-5h — quick win for visual consistency
3. **ETF browser inline HTML removal** (D-124) — 2-3h — quick win for visual consistency
4. **C170 Glossary component design** (D-125) — 2-3h — prepares for upcoming feature
5. **C188 "Why Did This Move" component design** (D-126) — 1-2h — prepares for upcoming feature

**Total estimated effort: 10-16h** — achievable within Sprint 21.

---

*This is the Round 46 design review. 4 active issues (D-121 through D-124) and 4 new component design needs (D-125 through D-128) identified. The most impactful action is creating the Component Gallery documentation — it addresses the root cause of visual inconsistency and prepares the design system for upcoming features.*
