# Stock Explorer Design Review

## 2026-06-14 Design Review — Review Round 9

> **Author**: Design Reviewer
> **Date**: 2026-06-14
> **Context**: Round 9 review — comparing competitor designs, assessing current UI, and proposing design improvements for approved features (C37, C39, C41, C36, C38) plus new Round 9 features (C42-C47).
> **Current Design Grade**: B+ (improved from B in Round 8, C+ in Sprint 0)

---

## Table of Contents

1. [Competitor Design Analysis](#competitor-design-analysis)
2. [Current UI Assessment](#current-ui-assessment)
3. [Design Recommendations for Approved Features](#design-recommendations-for-approved-features)
4. [Design Recommendations for New Round 9 Features](#design-recommendations-for-new-round-9-features)
5. [Design Gaps → current_problems.md Items](#design-gaps--current_problemsmd-items)
6. [Design System Recommendations](#design-system-recommendations)

---

## Competitor Design Analysis

### International Competitors (Rounds 7-8)

#### Simply Wall St — Visual-First Pioneer
- **Snowflake Diagram**: 5-dimensional visual summary (Value, Future, Past Performance, Financial Health, Dividends) with color-coded scores. Each dimension is a "petal" on the snowflake. Green = good, yellow = neutral, red = bad.
- **Key insight for Stock Explorer**: The snowflake IS the ten-second test. A beginner glances at it and instantly understands the company's health. Our current business card page has no equivalent synthesized visual.
- **Infographic-style layout**: Each stock page reads like an infographic, not a financial report. One key visual per concept, minimal text.
- **Progressive disclosure**: Summary first, details on click. This aligns perfectly with our "progressive drill-down" principle.
- **Design gap**: Simply Wall St has no TW market coverage. Our opportunity: apply their visual-first approach to TW stocks with plain-language explanations.

#### Public.com — Story Cards
- **Story Cards**: Each stock has a "Quick Summary" card at the top with 3-5 bullet points synthesizing the most important information. Below the card: detailed sections.
- **Key insight for Stock Explorer**: This is exactly what C37 (Key Takeaways) should look like. Public.com proves that synthesis cards work for beginners.
- **Social layer**: Users can see what other investors think. Stock Explorer doesn't need social features, but the "story first" approach is directly applicable.
- **Design gap**: Public.com's story cards are manually curated. Our C37 will be auto-generated, which is more scalable but risks feeling generic.

#### Seeking Alpha — Key Takeaways + Quant Rating
- **Key Takeaways**: 3-5 bullet points at the top of each stock page. "Bull vs Bear" debate format.
- **Quant Rating**: Proprietary rating system (Buy/Hold/Sell) with clear visual indicators.
- **Key insight for Stock Explorer**: Seeking Alpha's key takeaways are expert-written, not auto-generated. Our C37 needs curated templates for top 20 stocks to match this quality.
- **Design gap**: Seeking Alpha is expert-oriented. Our beginner-friendly positioning means we need MORE plain-language explanation, not less.

#### Koyfin — Modern Dashboard
- **"Recent Changes" section**: Highlights metrics that moved significantly compared to the previous period. This is exactly what C39 (What Changed Recently) should be.
- **Plain-language metric descriptions**: Every metric has a short description. "ROE: Return on Equity measures how efficiently a company generates profits from shareholders' equity."
- **Key insight for Stock Explorer**: Koyfin proves that highlighting recent changes is valuable for beginners. Our C39 should use the same pattern: metric name + direction arrow + percentage + plain-language explanation.
- **Design gap**: Koyfin is data-dense. Our PPT-style approach means we should show FEWER metrics but explain them BETTER.

### Taiwanese Competitors (Round 9)

#### 財報狗 (StatementDog) — The Local Benchmark
- **Stock Screener**: Multi-condition screening on 100+ financial metrics. This is their #1 feature and the biggest gap in Stock Explorer (C42).
- **P/E Band Chart**: Shows current P/E vs historical range. One of the most popular features. Directly maps to C45.
- **Card-based layout**: Clean, modern web interface with card-based layout. Similar to our approach.
- **Color-coded indicators**: Green/red for positive/negative trends. We use the same pattern.
- **Key insight**: 財報狗 proves that TW investors want screening and valuation context. Our "historian" positioning means we should frame screening as "discover interesting companies" not "find stocks to buy."
- **Design gap**: 財報狗 has minimal plain-language explanation. Our advantage is the analogy engine — we can make screening results educational.

#### Yahoo奇摩股市 — The Baseline
- **Most visited TW stock site**: Sets baseline UX expectations for TW users.
- **Push notifications**: Price alerts via mobile app. Stock Explorer has no notification system.
- **Simple, familiar portal design**: Minimal learning curve. Our PPT-style approach is more innovative but also more unfamiliar.
- **Key insight**: Yahoo Finance Taiwan is the "default" that users compare everything to. Our design must be AT LEAST as easy to use, even if the presentation style is different.
- **Design gap**: Yahoo is ad-supported and cluttered. Our clean PPT-style is a differentiator, but we must ensure it doesn't feel "empty" by comparison.

#### Simply Wall St (Round 9 Deep Dive) — The Visual Standard
- **Snowflake Analysis**: Proprietary visual framework that gives a 30-second company overview. Directly comparable to our "ten-second test."
- **Visual risk analysis**: Shows risks as visual breakdowns, not just numbers.
- **Infographic reports**: Each stock page reads like an infographic.
- **Key insight**: Simply Wall St is the CLEAREST model for what Stock Explorer should become. Their visual-first, plain-language, beginner-friendly approach is exactly our positioning. The main difference: they cover US/AU markets, we cover TW.
- **Design gap**: Simply Wall St has no narrative timeline (C34), no relationship-based recommendations (C41), and no moat analysis (C46). These are our unique differentiators.

#### Morningstar — The Rating Standard
- **Star Rating (1-5)**: Simple, memorable rating system. Beginners understand stars instantly.
- **Moat Rating**: "Does this company have a castle with a moat?" — Wide, Narrow, None. This is the model for C46.
- **Fair Value with Uncertainty**: Not just a number, but a range. Teaches beginners that valuation is uncertain.
- **Key insight**: Morningstar's rating systems are the gold standard for making complex analysis accessible. Our C43 (Snowflake) should follow the same principle: reduce complex data to a simple, visual score.
- **Design gap**: Morningstar is professional-toned. Our plain-language, analogy-driven approach is more beginner-friendly.

#### Investopedia — The Education Standard
- **Financial Dictionary**: 10,000+ terms with detailed plain-language definitions. The model for C33 (Glossary).
- **Academy**: Structured courses from absolute beginner to advanced. The model for C47.
- **Concept-first approach**: Teaches concepts before showing data. Aligns with our "education-first" positioning.
- **Key insight**: Investopedia proves that structured education is the natural evolution of financial platforms. Stock Explorer's "Did You Know?" facts are a good start, but a structured academy would be transformative.
- **Design gap**: Investopedia is US-focused and not stock-specific. Our advantage is combining education with real TW stock data.

### Design Trends Across All Competitors

| Trend | Competitors | Stock Explorer Status |
|-------|-------------|----------------------|
| **Visual health scores** | Simply Wall St (snowflake), Morningstar (stars), Stockopedia (StockRank) | ❌ MISSING — C43 addresses this |
| **Synthesis/summary cards** | Public.com (story cards), Seeking Alpha (key takeaways) | ❌ MISSING — C37 addresses this |
| **Discovery/screening** | 財報狗 (screener), Stockopedia (screening) | ❌ MISSING — C42 addresses this |
| **Valuation context** | 財報狗 (P/E band), Morningstar (fair value) | ❌ MISSING — C45 addresses this |
| **Risk visualization** | Simply Wall St (visual risk), Morningstar (uncertainty) | ❌ MISSING — C44 addresses this |
| **Structured education** | Investopedia (academy), Stockopedia (academy) | ⚠️ Partial (Did You Know facts) — C47 addresses this |
| **Plain-language** | Koyfin (metric descriptions), Investopedia (dictionary) | ✅ Core feature (analogy engine) |
| **Narrative/story** | Public.com (story cards), Stocksera (story tab) | ⚠️ PPT-style (no story tab) — C34 addresses this |
| **Mobile-first** | 財報狗, Yahoo, Simply Wall St (all have apps) | ❌ Streamlit limitations |
| **Notifications** | 財報狗, Yahoo, Simply Wall St, Morningstar | ❌ MISSING — C02 addresses this |

### Key Design Insights for Stock Explorer

1. **Visual health scores are table stakes** — Every major competitor has a proprietary scoring system. C43 (Snowflake) is not optional; it's required to remain competitive.
2. **Synthesis > Data** — The trend is toward synthesizing data into key takeaways, not just displaying metrics. C37 is the highest-ROI feature.
3. **Discovery is critical** — 財報狗's #1 feature is screening. Stock Explorer requires users to know which stock to look up, which is a barrier for beginners. C42 transforms the product.
4. **Education is the endgame** — Investopedia and Stockopedia both have academies. C47 is the long-term differentiator.
5. **Our unique advantage is plain-language + TW focus** — No competitor combines plain-language explanations with TW market data. This is our moat.

---

## Current UI Assessment

### What's Working

#### 1. PPT-Style Presentation (Zone C)
- The business card page follows the PPT-style principle: one key point per section, charts leading text.
- Revenue pie chart + analogy descriptions is a strong pattern.
- The dividend story section with countdown is unique and well-designed.
- **Grade: B+** — Good adherence to PPT style, but could be more visual.

#### 2. Zone A/B/C Layering
- **Zone A (Navbar)**: Clean horizontal radio navigation. No interactive controls in Zone A. ✅
- **Zone B (Sidebar)**: Search, navigation, hot stocks, ETFs, disclaimer. Well-organized. ✅
- **Zone C (Main)**: All content and charts. No zone violations. ✅
- **Grade: A-** — Proper zone separation. Minor issue: the business card page header (company name + price) duplicates the navbar header.

#### 3. Plain-Language System
- Analogy engine provides consistent plain-language explanations across all pages.
- `_白话_card()` and `_info_card()` provide consistent card styling.
- "Did You Know?" facts add educational value.
- **Grade: B+** — Strong foundation, but inconsistent application (some pages use inline HTML instead of shared components).

#### 4. Color System
- Primary: `#3498DB` (blue) — clickable, primary actions
- Success: `#27AE60` (green) — positive, growth
- Danger: `#E74C3C` (red) — negative, warnings (used sparingly)
- Neutral: `#7F8C8D` (gray) — secondary text
- Background: `#F8F9FA` (light gray) — card backgrounds
- **Grade: B** — Consistent in `_router_base.py` but pages bypass it with inline HTML.

### What's Not Working

#### 1. Inconsistent Card Styling (P1)
- `_router_base.py` provides `_白话_card()` and `_info_card()` but pages frequently bypass these with inline HTML.
- `group_structure.py` uses completely different card styling (white background, different border colors).
- `watchlist_page.py` uses inline HTML for card rows instead of `_info_card()`.
- `etf_detail.py` uses inline HTML for the one-liner, header, and dividend sections.
- **Impact**: Visual inconsistency across pages. Users see different card styles on different pages, which feels unprofessional.

#### 2. No Visual Health Score (P0)
- The business card page shows 15+ metrics scattered across sections with no synthesized visual summary.
- Every major competitor (Simply Wall St, Morningstar, Stockopedia) has a visual health score.
- This directly violates the "ten-second test" — a beginner cannot glance at the page and understand the company's health.
- **Impact**: Core design principle violation. Highest-priority gap.

#### 3. No Synthesis Layer (P0)
- The business card page shows data but doesn't synthesize it. A beginner sees numbers but doesn't know what matters.
- C37 (Key Takeaways) addresses this but hasn't been implemented yet.
- **Impact**: Beginners leave the page without understanding the company.

#### 4. Business Card Page Overload Risk (P1)
- The business card page already has: header, one-liner, "Did You Know?", 3 key metrics, dividend story, revenue pie chart, revenue trend, news, disclaimer.
- Adding C37 + C39 + C41 + C36 to this page risks violating the "one key point per page" principle.
- **Impact**: The page may become too long, pushing content below the fold.

#### 5. Mobile Responsiveness (P1)
- CSS media queries exist for 768px and 600px breakpoints, but they only adjust padding and font sizes.
- Multi-column layouts (`st.columns`) don't stack gracefully on mobile.
- Charts may be too small to read on mobile.
- **Impact**: Poor mobile experience. Competitors have native apps; we're limited by Streamlit.

#### 6. Loading State Inconsistency (P2)
- Some pages show `st.spinner()` while loading data, others don't.
- No skeleton loading or progressive rendering.
- The router shows "載入股票資料..." then each page shows "載入 XX 頁..." — two sequential spinners.
- **Impact**: Perceived slowness. Users see multiple loading states for a single page transition.

#### 7. Error State Inconsistency (P2)
- Some pages show `st.info("暫無資料")` for empty data, others show `st.error()`.
- No standardized empty state design.
- **Impact**: Inconsistent user experience when data is unavailable.

#### 8. No Design System Documentation (P1)
- `docs/design/design_system.md` does NOT exist (confirmed gap).
- Color values, card styles, and spacing are defined inline across multiple files.
- New features (C37, C39, C41, C36, C38) have no design system to follow.
- **Impact**: Design inconsistencies will multiply as new features are added.

#### 9. Watchlist Page Uses Non-PPT Layout (P2)
- The watchlist page uses a table-like layout with columns for rank, ID, name, industry, value, button.
- This is the ONLY page that uses a dense table layout — all other pages use card-based PPT style.
- **Impact**: Visual inconsistency. The watchlist feels like a different product.

#### 10. Category Browser Uses Dense Tables (P2)
- The category browser uses multi-column layouts with small text for stock lists.
- This is data-dense rather than PPT-style.
- **Impact**: Beginners may find this overwhelming. The "historian" positioning suggests a more narrative approach.

### Zone A/B/C Compliance Check

| Page | Zone A | Zone B | Zone C | Compliance |
|------|--------|--------|--------|------------|
| Business Card | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Operation Checkup | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Financial Health | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Peer Comparison | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Group Structure | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Event Dashboard | ✅ Minimal navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Watchlist | ✅ Minimal navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| Category Browser | ✅ Minimal navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| ETF Browser | ✅ Minimal navbar | ✅ Sidebar | ✅ Content | ✅ Full |
| ETF Detail | ✅ Navbar | ✅ Sidebar | ✅ Content | ✅ Full |

**Overall Zone Compliance: A-** — All pages properly separate Zone A/B/C. The only issue is that some pages use `_render_navbar_minimal()` (radio-only) while others use `_render_navbar()` (full header with price), creating slight visual inconsistency.

---

## Design Recommendations for Approved Features

### C37: Key Takeaways Summary Card

**Status**: Approved for Sprint 2. Highest design priority.

**Design Direction**:
- **Placement**: FIRST element on the business card page, below the company name/price header but above ALL other content. This is the "slide title" — the first thing the user sees.
- **Card design**: Use a **distinctive card style** that signals "this is a summary, not raw data." Recommendation: orange/amber border (`#F39C12`) with warm background (`#FFF8F0`). This is the ONLY card that uses orange — it's the "hero card" of the page.
- **Icon**: `📋` (clipboard) — universally understood as "summary."
- **Typography**: Each bullet as a separate line with `① ② ③` numbering. Each bullet ≤ 40 Chinese characters. Total card text ≤ 200 characters.
- **Content template**:
  ```
  📋 重點摘要
  ① [One-liner: what this company does]
  ② [Most impressive metric with analogy]
  ③ [Trend observation: growing/stable/declining]
  ```
- **Ten-second test**: The user should be able to read the 3 bullets in 10 seconds and restate the company's story.
- **Auto-generation**: Rule-based for most stocks, curated templates for top 20 stocks. Show a small "🕐 更新於 YYYY-MM-DD" timestamp.

**Design Risks**:
- Generic auto-generated bullets → Mitigation: curated templates for top 20
- Too many bullets pushing content down → Mitigation: hard cap at 3 bullets
- Stale content → Mitigation: regenerate on each data refresh

---

### C39: What Changed Recently Delta Card

**Status**: Approved for Sprint 3.

**Design Direction**:
- **Placement**: Business Card page, BELOW C37 (Key Takeaways) and ABOVE the revenue chart. This is the "what's new" section — it comes after the summary but before the detailed data.
- **Card design**: Standard info card (blue border) with `🔄` icon.
- **Content**: Maximum 2 deltas — the two most significant changes. Each delta: metric name + direction arrow + percentage + plain-language explanation.
- **Color coding**: Green (`#27AE60`) with ↑ for positive, Red (`#E74C3C`) with ↓ for negative. This is one of the approved uses of red/green (direction indication, not buy/sell).
- **Threshold**: Only show deltas > 10% change. Small fluctuations are noise.
- **Example**:
  ```
  🔄 最近有什麼變化
  📈 營收成長15% — 過去3個月增速是一年來最快
  📉 毛利率下降3% — 因為晶片價格競爭加劇
  ```

**Design Risks**:
- Too many deltas → Mitigation: hard cap at 2
- Negative-only deltas → Mitigation: add context message
- Stale "recent" data → Mitigation: hide card if data > 60 days old

---

### C41: Read Next Recommendations

**Status**: Approved for Sprint 3.

**Design Direction**:
- **Placement**: BOTTOM of the Business Card page, after all charts and metrics. This is the "next slide" prompt — the user has finished reading and is ready for the next thing.
- **Card design**: Tip card (orange border, same style as C37) with `📖` icon. Using the same orange as C37 creates visual consistency between "summary" and "next steps."
- **Content**: 2-3 recommendations maximum. Each: company name + ticker + one-line relationship description.
- **Example**:
  ```
  📖 接著看
  → 蘋果 (AAPL) — 台積電最大的客戶，佔營收25%
  → 聯華電子 (UMC) — 台積電的主要競爭對手
  → 輝達 (NVDA) — 台積電5奈米晶片的大客戶
  ```
- **Interaction**: Each recommendation is a clickable button that navigates to that company's Business Card page.

**Design Risks**:
- Manual curation bottleneck → Mitigation: fallback to same-industry recommendations
- Circular recommendations → Mitigation: exclude last 3 visited stocks
- Too many recommendations → Mitigation: hard cap at 3

---

### C36: Visual Revenue Tree

**Status**: Approved for Sprint 4.

**Design Direction**:
- **Placement**: New tab ("收入樹狀圖") next to the existing pie chart on the Business Card page. Default to the pie chart; let users discover the tree.
- **Chart type**: **Treemap** (not sunburst). Treemaps use space more efficiently, labels are easier to read, and the rectangular format fits the card-based layout better.
- **Color**: Use the existing color system. Primary segments in `#3498DB` (blue), with sub-segments in lighter tints. Avoid introducing new colors.
- **Labels**: Each rectangle must show the segment name + percentage. If too small, show only the name with tooltip for percentage.
- **Card wrapper**: Standard info card with plain-language explanation below.
- **Hierarchy cap**: Maximum 2 levels. No drilling down. Keep it simple.

**Design Risks**:
- Over-complexity for small companies → Mitigation: cap at top 5 segments, group rest as "其他"
- Data availability → Mitigation: graceful fallback to pie chart
- Chart density → Mitigation: max 2 levels, no drill-down

---

### C38: Compare Stories Side-by-Side

**Status**: Deferred (Phase 1 in Sprint 3 per Challenger recommendation).

**Design Direction**:
- **Placement**: New tab ("故事比較") on the Peer Comparison page, AFTER the existing metric comparison tab. Default to metric comparison.
- **Layout**: Two-column (50/50). Left: Company A. Right: Company B.
- **Color coding**: Blue (`#3498DB`) for Company A, Green (`#27AE60`) for Company B.
- **Content per column**: One-liner + revenue milestones + key events + business model summary. ≤ 100 characters per column.
- **Sub-toggle**: Show ONE dimension at a time: "商業模式" / "關鍵事件" / "收入里程碑". Default to "商業模式" (simplest).
- **Highlight differences**: Bold text where stories diverge.
- **One-line explanation at top**: "比較兩家公司的商業模式，了解它們的策略差異。"

**Design Risks**:
- PPT style violation → Mitigation: frame as ONE key point ("These two companies have different strategies")
- Clutter → Mitigation: one dimension at a time
- Beginner confusion → Mitigation: one-line explanation at top

---

## Design Recommendations for New Round 9 Features

### C43: Company Snowflake Health Visualization (NEW — P1)

**Design Direction**:
- **Placement**: TOP of the Business Card page, below C37 (Key Takeaways) or as a replacement for the "關鍵數字三連卡" section. This is the MOST IMPORTANT new visual element.
- **Chart type**: Radar chart (Plotly `go.Scatterpolar`) with 5 dimensions: 獲利能力、成長性、財務健康、股利、估值.
- **Scoring**: Each dimension scored 0-5, normalized against industry benchmarks.
- **Color coding**: Green (`#27AE60`) for score ≥ 4, Yellow (`#F39C12`) for 2-4, Red (`#E74C3C`) for < 2.
- **Plain-language**: Each dimension has a one-line explanation on hover/click. Example: "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元"
- **Ten-second test**: The snowflake IS the ten-second test. A beginner glances at it and instantly understands the company's health.

**Priority**: CRITICAL — This is the single most important design addition. Every competitor has a visual health score. We need one too.

---

### C42: Stock Screener / Discovery Engine (NEW — P1)

**Design Direction**:
- **Placement**: New page accessible from sidebar navigation ("🔍 選股探索").
- **Beginner-friendly presets**: Instead of raw filter controls, start with preset screens:
  - "穩定收息" — dividend yield > 4%, payout ratio < 70%
  - "成長潛力" — revenue growth > 20% for 3 years
  - "便宜估值" — P/E < 15, P/B < 2
- **Results**: Card-based layout (PPT style), not dense tables. Each result shows: company name, one-liner, key metric, "查看名片" button.
- **Framing**: "發現有趣的公司" not "篩選好股票". The historian positioning means we frame screening as discovery, not stock-picking.

**Priority**: HIGH — Transforms the product from lookup to discovery.

---

### C44: "What Could Go Wrong" Risk Analysis (NEW — P2)

**Design Direction**:
- **Placement**: New section on the Business Card page, below the snowflake (C43) and key takeaways (C37).
- **Card design**: Warning-style card (red border `#E74C3C`, light red background `#FDEDEC`) with `⚠️` icon.
- **Content**: 3-5 key risks, each with: (1) what the risk is, (2) historical evidence, (3) current indicators to watch.
- **Tone**: Factual, not predictive. "Here's what has happened before" not "Here's what might happen."
- **Example**:
  ```
  ⚠️ 風險分析
  ① 客戶集中度高：90%營收來自3大客戶（蘋果、輝達、AMD）
     歷史證據：2020年華為禁令導致營收下降15%
     觀察指標：客戶訂單變化、地緣政治風險
  ```

**Priority**: MEDIUM — Unique differentiator, no TW competitor has this.

---

### C45: Valuation Band Chart (NEW — P2)

**Design Direction**:
- **Placement**: Business Card page, in the "關鍵數字" section alongside PER/PBR.
- **Chart type**: Horizontal bar chart showing current P/E vs 5-year range (min/max). A vertical line marks the current position.
- **Plain-language interpretation**: "目前本益比18倍，處於歷史區間（12x-25x）的中間位置，不算貴也不算便宜"
- **Data source**: FinMind price + EPS data.

**Priority**: MEDIUM — Low effort, high impact. 財報狗 proves demand.

---

### C46: Moat Analysis (NEW — P2)

**Design Direction**:
- **Placement**: New section on the Business Card page, below the revenue tree (C36).
- **Card design**: Castle-themed card (border `#2C3E50`, icon `🏰`).
- **Content**: (1) moat type (technology/brand/cost/network/switching costs), (2) moat strength (wide/narrow/none), (3) historical evidence, (4) plain-language explanation.
- **Scoring**: Wide moat = 🟢, Narrow moat = 🟡, No moat = 🔴.
- **Manual curation**: Top 20 stocks only. Template-based for others.

**Priority**: MEDIUM — Unique differentiator for TW market.

---

### C47: Financial Education Academy (NEW — P2)

**Design Direction**:
- **Placement**: New top-level page ("📚 學習學院") accessible from sidebar.
- **Structure**: 10-15 structured lessons, organized by difficulty (beginner → intermediate → advanced).
- **Lesson format**: Title, 3-5 minute read, real TW stock example, key takeaway, quiz question.
- **Topics**: "What is revenue?", "What is profit?", "What is ROE?", "What is P/E?", "How to read a balance sheet", "What is a dividend?", etc.
- **Reuse**: Existing analogy engine for explanations.

**Priority**: LOW (long-term) — 20-30h effort. Transforms product from tool to platform.

---

## Design Gaps → current_problems.md Items

The following design issues should be added to `docs/status/current_problems.md`:

### P0 — Blocking Issues

1. **No visual health score** — Business Card page shows 15+ metrics with no synthesized visual summary. Every major competitor has one. Directly violates the "ten-second test." (C43 addresses this)

2. **No synthesis layer** — Business Card page shows data but doesn't synthesize it. Beginners see numbers but don't know what matters. (C37 addresses this)

### P1 — Important Issues

3. **Inconsistent card styling** — Pages use inline HTML instead of shared `_白话_card()` / `_info_card()` components. `group_structure.py`, `watchlist_page.py`, and `etf_detail.py` have completely different card styles.

4. **No design system documentation** — `docs/design/design_system.md` does not exist. Colors, card styles, and spacing are defined inline across multiple files. New features have no design system to follow.

5. **Business Card page overload risk** — Adding C37 + C39 + C41 + C36 to the existing page risks violating "one key point per page." Need a strategy for progressive disclosure.

6. **Mobile responsiveness gaps** — Multi-column layouts don't stack gracefully on mobile. Charts may be too small. Only basic padding/font-size adjustments exist.

7. **No discovery mechanism** — Users must know which stock to search for. No screening, no guided discovery, no "beginner path." (C42 addresses this)

### P2 — Optimization Issues

8. **Loading state inconsistency** — Multiple sequential spinners (router + page). No skeleton loading or progressive rendering.

9. **Error state inconsistency** — Empty data shows different messages on different pages. No standardized empty state design.

10. **Watchlist page uses non-PPT layout** — Only page with dense table layout. Feels like a different product.

11. **Category browser uses dense tables** — Data-dense rather than PPT-style. Overwhelming for beginners.

12. **No glossary/tooltip system** — Financial terms (ROE, P/B, PER) have no inline help. Beginners must already know the terms. (C33 addresses this)

13. **No risk analysis section** — Stock Explorer has NO risk analysis. Simply Wall St and Morningstar both have it. (C44 addresses this)

14. **No valuation context** — P/E and P/B shown as single numbers without historical context. 財報狗's P/E band chart proves this is expected. (C45 addresses this)

15. **No structured learning path** — "Did You Know?" facts are scattered. No progressive education. (C47 addresses this)

---

## Design System Recommendations

### Immediate Actions (Before Sprint 2)

1. **Create `docs/design/design_system.md`** — Document:
   - Color palette (primary, success, danger, neutral, background)
   - Card styles (info card, tip card, warning card, success card)
   - Typography (font family, sizes, weights)
   - Spacing system (padding, margins)
   - Zone A/B/C rules
   - PPT-style principles (one key point per page, charts > 60% area, text ≤ 200 chars)

2. **Standardize card components** — Ensure ALL pages use `_白话_card()` and `_info_card()` from `_router_base.py`. Replace inline HTML in `group_structure.py`, `watchlist_page.py`, `etf_detail.py`.

3. **Add new card types** for upcoming features:
   - **Summary card** (orange border, for C37 Key Takeaways)
   - **Delta card** (blue border with arrows, for C39 What Changed)
   - **Recommendation card** (orange border, for C41 Read Next)
   - **Warning card** (red border, for C44 Risk Analysis)
   - **Snowflake card** (multi-color, for C43 Health Visualization)

### Sprint 2 Actions

4. **Implement C37 (Key Takeaways)** with the summary card design. This sets the pattern for all future cards.

5. **Run the ten-second test** after C37 implementation. Show the page to someone unfamiliar with the stock. If they can't summarize the core concept in 10 seconds, redesign.

### Sprint 3-4 Actions

6. **Implement C43 (Snowflake)** as the second "hero" element on the Business Card page. This is the visual anchor that every competitor has.

7. **Implement C42 (Stock Screener)** with card-based results (not tables). Frame as "discovery" not "screening."

8. **Standardize loading states** — Single spinner per page transition, with progress indication.

9. **Standardize error states** — Consistent empty state design across all pages.

### Long-Term Actions

10. **Mobile-first redesign** — Consider a mobile-specific layout that stacks columns vertically and uses larger touch targets.

11. **Accessibility audit** — Check color contrast ratios (target ≥ 4.5:1), add alt text to charts, ensure keyboard navigation works.

12. **Design system evolution** — As new features are added, update `design_system.md` with new patterns and components.

---

## Summary

### Design Grade: B+

**Strengths**:
- Proper Zone A/B/C separation
- Strong plain-language foundation (analogy engine)
- PPT-style presentation on most pages
- Consistent color system (when shared components are used)
- Unique "historian" positioning with no direct competitor

**Weaknesses**:
- No visual health score (critical gap)
- No synthesis layer (critical gap)
- Inconsistent card styling across pages
- No design system documentation
- Mobile responsiveness gaps
- No discovery mechanism

### Top 5 Design Priorities

1. **Create `docs/design/design_system.md`** — Foundation for all future design work
2. **Implement C37 (Key Takeaways)** — Directly addresses the ten-second test
3. **Implement C43 (Snowflake)** — Visual health score that every competitor has
4. **Standardize card components** — Replace inline HTML with shared components
5. **Implement C42 (Stock Screener)** — Transforms product from lookup to discovery

### Competitor Benchmark

| Feature | Simply Wall St | Morningstar | 財報狗 | Public.com | Stock Explorer |
|---------|---------------|-------------|--------|------------|----------------|
| Visual health score | ✅ Snowflake | ✅ Stars | ⚠️ Dividend Score | ❌ | ❌ MISSING |
| Key takeaways | ⚠️ Visual | ⚠️ Fair Value | ❌ | ✅ Story Cards | ❌ MISSING |
| Discovery/screening | ❌ | ❌ | ✅ Advanced | ❌ | ❌ MISSING |
| Risk analysis | ✅ Visual | ✅ Uncertainty | ❌ | ❌ | ❌ MISSING |
| Valuation context | ❌ | ✅ Fair Value | ✅ P/E Band | ❌ | ❌ MISSING |
| Plain-language | ⚠️ Short desc | ⚠️ Professional | ⚠️ Partial | ✅ | ✅ Core |
| TW market | ❌ | ⚠️ Limited | ✅ Deep | ❌ | ✅ Deep |

**Stock Explorer's unique position**: We are the ONLY platform that combines plain-language explanations with TW market data. Our "historian" positioning (explain, don't predict) is unique. Our PPT-style presentation is unique. But we're missing the visual health score and synthesis layer that competitors consider table stakes.

---

*Design Review completed. Recommendations aligned with PPT-style design system, ten-second test principle, and "beginner education" mission. Next review: After Sprint 2 feature implementation (C37 + C43).*

---

## 2026-06-17 Design Review — Review Round 11

> **Author**: Design Reviewer
> **Date**: 2026-06-17
> **Context**: Round 11 review — assessing Sprint 2 feature implementation (C37, C39, C43, C45) and checking for new design issues.
> **Current Design Grade**: A- (upgraded from B+ in Round 9)

---

## Table of Contents

1. [Sprint 2 Feature Assessment](#sprint-2-feature-assessment)
2. [New Design Issues](#new-design-issues)
3. [Resolved Issues](#resolved-issues)
4. [Grade Justification](#grade-justification)
5. [Recommendations for Sprint 3](#recommendations-for-sprint-3)

---

## Sprint 2 Feature Assessment

### C37: Key Takeaways Summary Card ✅ IMPLEMENTED

**What was specified (Round 9)**:
- First element on business card page, below header
- Orange/amber "hero card" style (`#F39C12` border, `#FFF8F0` background)
- 📋 icon, ① ② ③ numbering, ≤ 40 chars per bullet, ≤ 200 total chars
- Ten-second test: user can restate company story from 3 bullets

**What was implemented**:
- Placed as first content element after header divider (line 140-152 of `business_card.py`) ✅ Correct placement
- Uses `_info_card("重點摘要", takeaways_text, "📋")` — the shared component ✅
- Curated templates for top 20 stocks in `_KEY_TAKEAWAYS` dict ✅ High-quality content
- Auto-generated fallback for non-top-20 stocks using `generate_key_takeaways()` ✅
- Hard cap at 5 bullets (takeaways[:5]) — design spec said 3, implementation allows up to 5

**Design deviations**:
1. **Missing orange/amber hero card style**: The spec called for a distinctive orange/amber border (`#F39C12`) with warm background (`#FFF8F0`) — the ONLY card using orange on the page. Instead, C37 uses the standard `_info_card()` which has a **blue** border (`#3498DB`). This is a significant deviation from the design direction. The whole point was for C37 to visually stand out as the "hero card." Using the same blue border as every other card defeats this purpose. → **New issue: D-016**

2. **No timestamp**: The spec called for a small "🕐 更新於 YYYY-MM-DD" timestamp. Not implemented. Minor issue.

3. **Bullet count**: Spec said max 3, implementation caps at 5. The auto-generator can produce up to 5 bullets (one per metric). This risks pushing content down. → **New issue: D-017**

**Verdict**: Functionally complete and well-executed. The curated top-20 templates are excellent. The fallback auto-generation is solid. The main gap is the missing distinctive visual treatment.

---

### C39: What Changed Delta Card ✅ IMPLEMENTED

**What was specified (Round 9)**:
- Below C37, max 2 deltas, > 10% threshold
- Standard info card (blue border) with 🔄 icon
- Green ↑ for positive, Red ↓ for negative
- Each delta: metric name + direction arrow + percentage + plain-language explanation

**What was implemented**:
- Placed after "關鍵數字三連卡" section (line 200-217) — **NOT directly below C37** ⚠️
- Uses `_info_card("最近有什麼變化", delta_text, "🔄")` ✅ Correct icon
- Shows 📈/📉 emojis with direction ✅
- Includes metric name, current/previous values, percentage, and plain-language explanation ✅
- > 10% threshold enforced ✅
- **No hard cap at 2 deltas** — all deltas > 10% are shown ⚠️

**Design deviations**:
1. **Placement too low**: C39 appears AFTER the "關鍵數字三連卡" (key metrics cards), not directly below C37 as specified. The design intent was: summary → what changed → detailed data. Current order is: summary → detailed data → what changed. This reduces the "what's new" prominence. → **New issue: D-018**

2. **No delta count cap**: Spec said max 2 deltas. Implementation shows ALL deltas exceeding 10% threshold. With revenue, price, and YoY all potentially > 10%, this could show 3 deltas. → **New issue: D-019**

3. **Color coding missing**: Spec called for green (`#27AE60`) text for positive and red (`#E74C3C`) text for negative deltas. Implementation uses default card text color for all deltas regardless of direction. The 📈/📉 emojis provide some visual cue, but the text itself isn't color-coded. → **New issue: D-020**

**Verdict**: Core logic is solid. The `explain_delta()` function produces excellent plain-language explanations. Main issues are placement, missing cap, and lack of directional color coding.

---

### C43: Snowflake Health Visualization ✅ IMPLEMENTED

**What was specified (Round 9)**:
- Radar chart with 5 dimensions: 獲利能力、成長性、財務健康、股利、估值
- Scored 0-5 (normalized), color-coded: Green ≥ 4, Yellow 2-4, Red < 2
- Plain-language explanations on hover/click
- Ten-second test: the snowflake IS the ten-second test

**What was implemented**:
- Radar chart using `go.Scatterpolar` with 5 dimensions ✅
- Dimensions: 獲利能力、成長性、財務健康、股利品質、估值合理性 ✅ (5 dimensions, names match intent)
- Scored 0-100 (not 0-5 as spec'd, but equivalent scale) ✅
- Color coding: Green ≥ 70, Yellow 40-70, Red < 40 (using emoji indicators 🟢🟡🔴) ✅
- Reference lines at 40 (及格線) and 70 (良好線) ✅ Excellent addition
- Dimension score cards below chart in 5 columns ✅
- Plain-language health summary via `get_health_summary()` ✅
- Hover tooltips showing dimension name + score ✅
- Detailed scoring functions for each dimension (_score_roe, _score_gross_margin, etc.) ✅

**Design deviations**:
1. **Score scale mismatch**: Spec said 0-5, implementation uses 0-100. This is actually a minor improvement (finer granularity), but the spec should be updated to match.

2. **No plain-language per-dimension explanation on hover**: The spec asked for one-line explanations like "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元" on hover/click. Current hover only shows "獲利能力: 85分". The dimension cards below show scores but not the underlying metric values or plain-language explanations. → **New issue: D-021**

3. **Chart placed after key metrics**: The snowflake appears after "關鍵數字三連卡" and C39, not near the top of the page. Per Round 9, it should be "below C37 (Key Takeaways) or as a replacement for the 關鍵數字三連卡 section." → **New issue: D-022**

**Verdict**: This is the strongest Sprint 2 implementation. The scoring system is sophisticated, the chart is well-designed with reference lines, and the health summary is genuinely useful. The main gap is missing per-dimension plain-language explanations.

---

### C45: Valuation Band Chart ✅ IMPLEMENTED

**What was specified (Round 9)**:
- Horizontal bar chart showing current P/E vs 5-year range (min/max)
- Vertical line marking current position
- Plain-language interpretation

**What was implemented**:
- Line chart showing historical PER over 2 years with 25th-75th percentile band ✅
- Current PER marked with red dashed horizontal line ✅
- Plain-language interpretation via `_info_card("估值解讀", ...)` showing whether valuation is low/mid/high ✅
- TTM EPS calculation from quarterly financial data ✅
- Robust error handling with multiple fallback states ✅

**Design deviations**:
1. **Chart type differs from spec**: Spec said "horizontal bar chart showing current P/E vs 5-year range (min/max)" — a simpler bar/thermometer-style chart. Implementation uses a full time-series line chart with percentile band. This is actually **more informative** than the spec, but it's a different visual metaphor. The implementation is superior to the spec.

2. **Data window**: Spec said 5-year range, implementation uses 2-year range (730 days). This is likely due to data availability constraints. → **New issue: D-023**

3. **Placement**: The valuation chart is at the bottom of the page (after revenue trend, before news), in a separate "估值區間" section. This is reasonable placement but could be closer to the PER metric in "關鍵數字" section for better context. Minor issue.

**Verdict**: Excellent implementation that exceeds the spec. The percentile band approach is more sophisticated than a simple min/max bar. The plain-language interpretation is a nice touch.

---

## New Design Issues

### D-016: C37 Missing Orange/Amber Hero Card Style
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: C37 (Key Takeaways) uses the standard `_info_card()` with blue border (`#3498DB`) instead of the specified orange/amber hero card style (`#F39C12` border, `#FFF8F0` background). The design intent was for C37 to be the ONLY card using orange — the "hero card" of the page. Using the same blue border as every other card defeats this purpose.
- **Affected Files**: `business_card.py` (line 152), `_router_base.py`
- **Proposed Fix**: Create a new `_summary_card()` component in `_router_base.py` with orange/amber styling (`border-left:4px solid #F39C12`, `background:#FFF8F0`), and use it for C37.
- **Effort**: 30 min

### D-017: C37 Bullet Count Exceeds Spec
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Design spec said max 3 bullets for C37. Implementation caps at 5. For stocks with many available metrics, this can produce 5 bullets, pushing content down and violating the "≤ 200 characters" text limit.
- **Affected Files**: `analogy_engine.py` (line 422: `return takeaways[:5]`)
- **Proposed Fix**: Change cap to 3 (`return takeaways[:3]`) to match spec and enforce brevity.
- **Effort**: 5 min

### D-018: C39 Placement Too Low on Page
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: C39 (What Changed) appears AFTER the "關鍵數字三連卡" section, not directly below C37 as specified. The intended flow was: summary → what changed → detailed data. Current order is: summary → detailed data → what changed.
- **Affected Files**: `business_card.py` (lines 170-217)
- **Proposed Fix**: Move C39 block (lines 200-217) to immediately after C37 block (lines 140-152), before the "關鍵數字三連卡" section.
- **Effort**: 15 min

### D-019: C39 Missing Delta Count Cap
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec said max 2 deltas. Implementation shows ALL deltas exceeding 10% threshold. Revenue, price, and YoY could all exceed 10%, showing 3 deltas.
- **Affected Files**: `analogy_engine.py` (`compute_recent_deltas` function)
- **Proposed Fix**: Add `return deltas[:2]` at the end of `compute_recent_deltas()` to enforce the 2-delta cap.
- **Effort**: 5 min

### D-020: C39 Missing Directional Color Coding
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec called for green (`#27AE60`) text for positive deltas and red (`#E74C3C`) text for negative deltas. Implementation uses default card text color for all deltas. The 📈/📉 emojis provide some visual cue, but the text itself isn't color-coded.
- **Affected Files**: `business_card.py` (lines 208-216)
- **Proposed Fix**: Apply inline color styling to delta text based on direction. Use `<span style="color:#27AE60">` for positive and `<span style="color:#E74C3C">` for negative.
- **Effort**: 30 min

### D-021: C43 Missing Per-Dimension Plain-Language Explanations
- **Severity**: P1
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec asked for one-line plain-language explanations on hover/click for each dimension (e.g., "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元"). Current hover only shows "獲利能力: 85分". The dimension cards below show scores but not the underlying metric values or explanations.
- **Affected Files**: `chart.py` (create_health_snowflake), `business_card.py` (lines 232-249)
- **Proposed Fix**: Pass the underlying metric values (ROE, gross margin, etc.) into the hover template for each dimension. Add a plain-language explanation below each dimension card.
- **Effort**: 1-2h

### D-022: C43 Placement Not Near Top of Page
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: The snowflake chart appears after "關鍵數字三連卡" and C39, not near the top of the page. Per Round 9, it should be "below C37 (Key Takeaways) or as a replacement for the 關鍵數字三連卡 section."
- **Affected Files**: `business_card.py` (lines 219-253)
- **Proposed Fix**: Move C43 block to immediately after C37, before C39 and key metrics. This makes the snowflake the second thing users see (after the summary), which aligns with the "ten-second test" principle.
- **Effort**: 15 min

### D-023: C45 Uses 2-Year Window Instead of 5-Year
- **Severity**: P2
- **Added**: 2026-06-17
- **Source**: Design Review Round 11
- **Description**: Spec said "current P/E vs 5-year range." Implementation uses 2-year window (730 days). This may be due to data availability, but it reduces the chart's usefulness for long-term valuation context.
- **Affected Files**: `chart.py` (line 626: `cutoff_2y = pd.Timestamp.now() - pd.Timedelta(days=730)`)
- **Proposed Fix**: Extend to 5 years (1825 days) if data is available. Add a fallback: if < 2 years of data available, show what's available with a note.
- **Effort**: 30 min

---

## Resolved Issues

| ID | Title | Severity | Resolution |
|----|-------|----------|------------|
| D-001 | No Visual Health Score | P0 | **RESOLVED** — C43 (Snowflake Health Visualization) fully implemented with 5-dimension radar chart, color-coded scores, reference lines, and plain-language health summary. |
| D-002 | No Synthesis Layer | P0 | **RESOLVED** — C37 (Key Takeaways) implemented with curated templates for top 20 stocks and auto-generated fallback for others. |
| D-014 | No Valuation Context | P2 | **RESOLVED** — C45 (Valuation Band Chart) implemented with historical PER percentile band, current PER marker, and plain-language interpretation. |

---

## Grade Justification

**Previous Grade**: B+ (Round 9)
**New Grade**: A-

**Reasoning for upgrade**:

The Sprint 2 implementation delivers three of the four highest-priority design gaps identified in Round 9:
1. **D-001 (P0) resolved**: Visual health score (C43) is now the strongest feature of the product
2. **D-002 (P0) resolved**: Synthesis layer (C37) provides the "ten-second test" summary
3. **D-014 (P2) resolved**: Valuation context (C45) exceeds the spec with percentile bands

The implementation quality is generally high:
- Curated content for top 20 stocks shows attention to quality
- Sophisticated scoring algorithms for health dimensions
- Robust error handling throughout
- Good use of shared components (`_info_card`)

**Reasons grade is A- not A**:
- C37 missing the distinctive orange/amber hero card style (D-016) — this was a key design differentiator
- C39 placement and color coding issues (D-018, D-020) reduce effectiveness
- C43 missing per-dimension plain-language explanations (D-021)
- Page layout order doesn't follow the "summary → what changed → detailed data" flow
- Several P2 issues (D-017, D-019, D-022, D-023) indicate spec compliance gaps

---

## Recommendations for Sprint 3

### Priority 1 (Quick Wins — < 2h total)
1. **Fix D-016**: Create `_summary_card()` with orange/amber styling for C37
2. **Fix D-017**: Change C37 cap from 5 to 3 bullets
3. **Fix D-018**: Move C39 directly below C37
4. **Fix D-019**: Add `deltas[:2]` cap in C39
5. **Fix D-022**: Move C43 directly below C37 (after C39)

### Priority 2 (Important — 2-4h total)
6. **Fix D-020**: Add directional color coding to C39 deltas
7. **Fix D-021**: Add per-dimension plain-language explanations to C43
8. **Fix D-023**: Extend C45 to 5-year window with graceful fallback

### Priority 3 (New Features — Sprint 3 backlog)
9. **C41**: Read Next Recommendations (approved for Sprint 3)
10. **C38**: Compare Stories Side-by-Side (deferred to Phase 1)
11. **D-004**: Note — design system now exists at `docs/domain/design_system.md` but should be copied/linked to the expected `docs/design/design_system.md` path

### Page Layout Target for Sprint 3
The ideal Business Card page order should be:
1. Header (company name + price)
2. **C37** — Key Takeaways (orange hero card)
3. **C43** — Snowflake Health (visual anchor)
4. **C39** — What Changed (delta card, max 2)
5. 一句話定位 (one-liner)
6. 你知道嗎？ (Did You Know)
7. 關鍵數字三連卡 (key metrics)
8. 配息故事 (dividend story)
9. 營收組成 (revenue pie)
10. 營收趨勢 (revenue trend)
11. 估值區間 (valuation band)
12. 近期動態 (news)
13. C41 — Read Next (recommendations)
14. 免責聲明 (disclaimer)
