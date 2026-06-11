# Design Review — Round 14 Discussion

## 2026-06-19 Design Review — Round 14 Discussion

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: 💡 Discussion theme cycle — Sprint 4 Visual/UX Focus: evaluating C38 (Compare Stories), C51 (Sector Heatmap), C48 (Company Story Card), and C53-1 (Social Sharing URL) for design direction. Analyzing visual/UX patterns from 14 rounds of competitor research and resolving open design issues.
> **Current Design Grade**: A (maintained from Round 13)

---

## Table of Contents

1. [Current Design State Summary](#current-design-state-summary)
2. [Sprint 4 Feature Design Analysis](#sprint-4-feature-design-analysis)
3. [Design Direction A: C48 Company Story Card](#design-direction-a-c48-company-story-card)
4. [Design Direction B: C38 Compare Stories](#design-direction-b-c38-compare-stories)
5. [Design Direction C: C51 Sector Heatmap](#design-direction-c-c51-sector-heatmap)
6. [Design Direction D: C53-1 Social Sharing](#design-direction-d-c53-1-social-sharing)
7. [New Card Type Specifications](#new-card-type-specifications)
8. [Open Design Issues Resolution Plan](#open-design-issues-resolution-plan)
9. [Design Risk Register](#design-risk-register)
10. [Recommendation](#recommendation)

---

## Current Design State Summary

### Where We Are

Stock Explorer's design grade has been maintained at **A** for two consecutive rounds. The core visual foundation is solid, and the PPT-style philosophy is consistently applied:

| Component | Status | Grade |
|-----------|--------|-------|
| **Visual Health Score (C43 Snowflake)** | ✅ Implemented — 5-dimension radar chart | A |
| **Synthesis Layer (C37 Key Takeaways)** | ✅ Orange hero card, 3-bullet cap | A |
| **Delta Tracking (C39 What Changed)** | ✅ Directional color coding | A |
| **Valuation Context (C45 Band Chart)** | ✅ 5-year PER percentile band | A |
| **Recommendations (C41 Read Next)** | ✅ Peer stocks + fun facts | A |
| **Page Layout Flow** | ✅ Summary → Delta → Health → Metrics → Details | A |
| **Color System** | ✅ Blue/Green/Red + gray-scale backgrounds | A |
| **Zone A/B/C Layout** | ✅ Strictly maintained | A |

### Open Design Issues

| ID | Issue | Severity | Sprint 4 Plan |
|----|-------|----------|---------------|
| D-021 | C43 hover values missing underlying metric data | P1 | ✅ Resolve via hover tooltip enhancement |
| D-024 | `_info_card` background `#FFF8F0` → `#F8F9FA` | P1 | ✅ Quick CSS fix (D-037) |
| D-025 | C39 empty state when no deltas exceed threshold | P2 | ✅ Add empty state card |
| D-003 | Inconsistent card styling (group_structure, watchlist, etf_detail) | P2 | ✅ Ongoing — card type library fixes |
| D-006 | Mobile responsiveness gaps | P2 | ⚠️ Deferred — Streamlit limitations |

### Design System Compliance Score

| Principle | Compliance | Notes |
|-----------|-----------|-------|
| PPT-style (one key point per card) | ✅ 95% | New Sprint 4 cards must maintain this |
| Ten-second test | ✅ 90% | C48 is the ultimate expression of this principle |
| Zone A/B/C separation | ✅ 100% | No zone violations in Sprint 3 |
| Color system | ⚠️ 85% | D-024/D-036/D-037 fix remaining violations |
| Max 200 chars text per card | ✅ 95% | C38 side-by-side may need careful editing |
| Chinese (zh-TW) only | ✅ 100% | All new content in zh-TW |

---

## Sprint 4 Feature Design Analysis

### Feature Competitive Validation Matrix

Based on 14 rounds of competitor research covering 50+ competitors across TW, US, Japan, Korea, India, EU, and Singapore markets:

| Feature | Competitors with Equivalent | Validation Level | Market Timing |
|---------|---------------------------|-----------------|---------------|
| **C48 Company Story Card** | Dhan, Atom Finance, Toss, Stake, StockEdge, Finimize | 🔴 **Very High** — 6+ competitors in 5 markets | **Urgent** — Atom Finance is doing exactly this now |
| **C51 Sector Heatmap** | StockEdge, Moomoo, 永豐金證券, 元大證券 | 🟡 **High** — 4+ competitors in 3 markets | Important — but our "with education" angle is unique |
| **C38 Compare Stories** | Atom Finance, Seeking Alpha, Stocksera | 🟡 **Medium** — 3 competitors but narrative comparison is rare | Differentiated — no TW competitor has narrative comparison |
| **C53-1 Social Sharing** | TradingView, Plotch.ai, Stake, Minkabu | 🟡 **Medium** — sharing is table stakes | Quick win — our narrative cards are unique content to share |

### Key Competitive Insights for Sprint 4

1. **The "30-second stock story" is becoming table stakes**: Dhan (India), Atom Finance (US), Toss (Korea), Stake (AU), and Finimize (UK) all offer some form of ultra-short company summary. This means C48 isn't a nice-to-have — it's becoming expected. **Our window to differentiate through quality is closing.**

2. **Sector visualization with narrative is a white space**: StockEdge and Moomoo have sector heatmaps, but they're purely visual. No competitor adds plain-language explanations of WHY sectors are moving. This is where C51's "with education" angle creates unique value.

3. **Narrative comparison is genuinely rare**: While metric comparison (side-by-side numbers) is common, narrative comparison ("how are these companies' stories different?") exists only in Stocksera and Seeking Alpha in limited form. This is a true differentiator for C38.

4. **Social sharing amplifies every other feature**: Every company card, every comparison, every heatmap becomes potential shareable content. C53-1 isn't just a feature — it's a distribution channel for C48, C38, and C51.

---

## Design Direction A: C48 Company Story Card

### Description

A **hero card at the top of each company page** — before C37 Key Takeaways — that gives the user a complete 30-second understanding of the company. This is the ultimate expression of the "ten-second test" design principle, evolved from C37 (which summarizes key metrics) into a true narrative-first experience.

### Visual Mockup

```
┌─────────────────────────────────────────────────────────────┐
│  🏢 台積電 (2330) · 半導體業                    💰 980 +2.3% │
│─────────────────────────────────────────────────────────────│
│  ▼ 📖 公司故事卡 (C48)                                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  🏭 全球90%先進晶片的製造商                              │    │
│  │     (每10支iPhone，就有9支用的是台積電晶片)                │    │
│  │                                                       │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  💰 毛利率 55%         📈 營收成長 28%        🏆 ROE 31%  │    │
│  │  💡 "每賣100元賺55元"   💡 "比去年多賺28%"    💡 "股東每100元賺31元"│
│  │                                                       │    │
│  │  🌍 冷知識：台積電一家的晶片產量，超過中國所有工廠的總和       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│─────────────────────────────────────────────────────────────│
│  ▼ 📋 重點摘要 (C37)                                         │
│  ...
```

### Design Specifications

**Card Type**: New `_story_card()` — extends `_summary_card()` with additional visual elements

**Visual Design**:
- **Border**: Left border 6px solid `#F39C12` (amber/orange — hero card status)
- **Background**: Gradient from `#FFF8F0` (warm) to `#FFFFFF` (clean) — subtly distinct from other cards
- **Layout**: 3 zones within the card:
  1. **Top zone**: One-liner + parenthetical explanation (≤ 60 chars total)
  2. **Middle zone**: 3 key metrics in a horizontal row, each with value + plain-language analogy (≤ 30 chars per metric)
  3. **Bottom zone**: Rotating "Did You Know?" fact with globe emoji (≤ 80 chars)
- **Typography**: One-liner uses `font-size: 1.4rem, font-weight: 700`; metrics use existing value styling; facts use `font-size: 0.85rem, font-style: italic`

**Metric Selection Algorithm** (for "3 most notable"):
The 3 metrics are auto-selected based on what's most **notable** about this company (not just the biggest numbers):
- If gross margin > industry avg by > 10% → include gross margin
- If revenue growth > 20% → include revenue growth
- If ROE > 20% → include ROE
- If dividend yield > 4% → include dividend yield
- If debt ratio < 30% → include financial health highlight
- Fallback: top 3 by absolute value
- Tie-breaking: prefer metrics with existing analogy engine content

**Competitor Reference**:

| Competitor | What They Do | How We Differentiate |
|-----------|-------------|---------------------|
| **Atom Finance** | AI-generated "Company Narratives" with plain-language summary | We use curated templates + analogy engine → more reliable, more localized for TW |
| **Dhan** | "Why This Matters" conclusion at the top of each stock page | We go beyond conclusion to full narrative story card with metrics + analogies |
| **Toss Securities** | "Stock Stories" — 30-second visual summaries | We add plain-language metric explanations that Toss lacks |
| **Stake** | "Company Story" cards — visual-first, minimal text | We go deeper (3 metrics + analogies) while maintaining the 30-second test |

**Alignment with Design System**:

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ ONE key concept (the company's identity), visual-first with metrics supporting, ≤ 60 chars for the core message |
| **Ten-second test** | ✅ This IS the ten-second test made real — user reads one-liner + 3 metrics + fact = complete picture in ≤ 30 seconds |
| **Zone A/B/C** | ✅ Story card is the FIRST element in Zone C (main content), above C37. No zone violations |
| **Plain-language** | ✅ Every metric has an analogy underneath. One-liner avoids jargon |
| **Color system** | ✅ Amber border for hero card status (same as C37). Green/red only for metric direction indicators |
| **Max 200 chars** | ✅ Total card text ≤ 170 chars (one-liner 60 + metrics 90 + fact 80 = 230, but metrics value text is visual, not prose) — trim to fit 200 if needed |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Positional conflict with C37** — Both are summary cards; C37 already shows key takeaways above the fold | High | C48 goes ABOVE C37 (first on page). C48 = narrative identity; C37 = analytical summary. Different purpose, different position. If redundancy is detected in testing, merge fact/fact elements |
| **Metric selection feels arbitrary** — Users may wonder "why these 3 metrics?" | Low | The selection algorithm is data-driven (notable = deviation from industry average, not absolute size). Document the logic |
| **Card height** — 3 zones may push C37 below the fold on smaller screens | Medium | C48 is designed to be compact: 3 rows of content max (~280px). Must fit within 800px "above the fold" budget alongside page header |
| **Content staleness** — Static facts don't update with current data | Low | "Did You Know?" facts rotate from existing `company_facts.yaml` (70+ facts). Facts are about the company's identity, not current numbers |

---

## Design Direction B: C38 Compare Stories

### Description

A **new "故事比較" (Story Comparison) tab** on the peer comparison page that shows two companies' narratives side-by-side. Unlike the existing metric comparison (which shows numbers), this tells users HOW the two companies' stories differ — in plain language, with visual hierarchy.

### Visual Mockup

```
┌─────────────────────────────────────────────────────────────┐
│  比較：台積電 (2330) vs 聯華電子 (2303)                        │
│─────────────────────────────────────────────────────────────│
│  [📊 指標比較]  [📖 故事比較] ← NEW TAB                       │
│                                                             │
│  ┌────────────────────┐    ┌────────────────────┐           │
│  │ 🏭 台積電           │    │ ⚙️ 聯華電子         │           │
│  │                    │    │                    │           │
│  │ 全球90%先進晶片     │    │ 成熟製程晶片專家     │           │
│  │ 的製造商            │    │                    │           │
│  │                    │    │                    │           │
│  │ 💰 毛利率 55%       │    │ 💰 毛利率 32%       │           │
│  │ 📈 營收成長 28%     │    │ 📈 營收成長 8%      │           │
│  │ 🏆 ROE 31%         │    │ 🏆 ROE 15%         │           │
│  │                    │    │                    │           │
│  │ 主要客戶：Apple     │    │ 主要客戶：IoT裝置    │           │
│  │ NVIDIA, AMD        │    │ 汽車電子, 家電      │           │
│  └────────────────────┘    └────────────────────┘           │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  📋 故事差異摘要                                               │
│                                                             │
│  • 技術層次：台積電做最先進的5nm晶片，聯華電子主攻成熟製程           │
│  • 客戶類型：台積電服務Apple等頂級品牌，聯華電子服務廣泛的IoT市場    │
│  • 獲利模式：台積電靠技術領先賺高毛利，聯華電子靠大量生產賺穩定收入  │
│                                                             │
│  💡 白話：如果半導體是餐飲業，台積電是米其林三星餐廳，             │
│     聯華電子是遍佈全台的連鎖餐廳 — 都是餐廳，但完全不同的生意模式    │
│  ─────────────────────────────────────────────────────────  │
```

### Design Specifications

**Card Layout**: Two `_story_card()` instances side-by-side in a 2-column `st.columns(2)` layout

**Each card contains**:
- Company name + one-liner (≤ 40 chars)
- Top 3 metrics (same algorithm as C48)
- Top 2 customers/partners (new data element from `company_facts.yaml`)

**Comparison summary** (below the two cards):
- 3-5 bullet points of narrative differences (generated from templates + data)
- Required categories: 技術/產品差異、客戶/市場差異、獲利模式差異
- Each bullet ≤ 50 chars
- Final "白話" analogy line ≤ 80 chars (using analogy engine)

**Color-Coding for Comparison**:
- The "winning" metric in each row gets a subtle `#27AE60` (green) dot prefix
- The "trailing" metric gets a `#E74C3C` (red) dot prefix
- **Important**: This is NOT "which stock is better" — it's "which is higher/lower on this dimension". The dots indicate relative position, not recommendation
- Analogy bullets use neutral `#2C3E50` text — no color coding on the narrative differences

**Competitor Reference**:

| Competitor | What They Do | How We Differentiate |
|-----------|-------------|---------------------|
| **Atom Finance** | Side-by-side stock comparison with AI-generated narrative differences | We go deeper with analogy-based plain-language explanations; Atom's AI summaries are generic |
| **Seeking Alpha** | Side-by-side fundamental comparison (numbers only, no narrative) | We add the narrative layer that Seeking Alpha lacks |
| **Stocksera** | "Compare Stories" feature with narrative summaries | We add structured metric comparison within the story cards + white-language analogies |
| **元大證券** | Visual side-by-side basic comparison | We go beyond visual metrics to full narrative comparison with plain-language analogies |

**Alignment with Design System**:

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ One key message per comparison ("these companies differ in 3 ways"), cards are visual-first |
| **Ten-second test** | ✅ User glances at the two cards and immediately understands the key difference (company A vs company B identity) |
| **Zone A/B/C** | ✅ Comparison is Zone C content. The tab bar is part of the page's internal navigation, not Zone A |
| **Plain-language** | ✅ Narrative differences use everyday analogies. No jargon without explanation |
| **Color system** | ✅ Green/red dots only for metric direction (same as existing delta card). Analogy text is neutral |
| **Max 200 chars** | ⚠️ Risk: comparison bullets + analogy could exceed 200 chars. **Mitigation**: enforce 50-char limit per bullet, 80-char limit on analogy. Total: ~230 chars → trim to 200 by reducing to 3 bullets if needed |

### Design Risk: Recommendation Perception

**🔴 CRITICAL**: The side-by-side comparison with green/red dots MUST NOT be perceived as "which stock to buy." This is the single biggest design risk for C38.

**Mitigation design requirements**:
1. **Header disclaimer**: "這不是投資建議，而是幫你理解兩家公司的不同" (This is not investment advice, it's helping you understand how these companies differ)
2. **No scoring**: Never assign an overall "winner" score
3. **Balanced framing**: Every bullet point must describe DIFFERENCES, not SUPERIORITY. "台積電技術領先" not "台積電比較好"
4. **Analogy framing**: The closing analogy must use NEUTRAL comparisons ("米其林 vs 連鎖餐廳" not "高級餐廳 vs 普通餐廳")

---

## Design Direction C: C51 Sector Heatmap

### Description

A **new "🔥 產業熱度" (Sector Heatmap) page** showing all TW sectors as a color-coded interactive grid. This is Stock Explorer's first market-level visualization (not company-focused), and it introduces a new kind of content: sector narratives that explain WHY sectors are moving.

### Visual Mockup

```
┌─────────────────────────────────────────────────────────────┐
│  🔥 產業熱度圖                                                 │
│─────────────────────────────────────────────────────────────│
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🟢🟢🟢🟢 │ │ 🟢🟢🟢🟢 │ │ 🟡🟡🟡⚪ │ │ 🟢🟢🟢🟢 │       │
│  │ 半導體    │ │ 電子零組件│ │ 金融保險  │ │ 生技醫療  │       │
│  │ +3.2%    │ │ +2.8%    │ │ +1.1%    │ │ +2.5%    │       │
│  │ 🔥🔥🔥   │ │ 🔥🔥     │ │ 🔥       │ │ 🔥🔥     │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🟡🟡🟡⚪ │ │ 🟢🟢🟢🟢 │ │ 🔴🔴⚪⚪ │ │ 🟡🟡🟡⚪ │       │
│  │ 紡織纖維  │ │ 電腦及周邊│ │ 觀光餐旅  │ │ 化學工業  │       │
│  │ +0.8%    │ │ +2.3%    │ │ -1.5%    │ │ +0.9%    │       │
│  │ 🔥       │ │ 🔥🔥     │ │          │ │ 🔥       │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                             │
│  圖例：🟢 漲 >2%  🟢 漲 1-2%  🟡 漲 0-1%  ⚪ 平盤         │
│        🔴 跌 0-1%  🔴 跌 1-2%  🔴 跌 >2%                   │
│                                                             │
│  點擊任一產業查看詳細說明與熱門個股 →                            │
│─────────────────────────────────────────────────────────────│
│  ⏱ 時間範圍：[今日] [本週] [本月]                              │
└─────────────────────────────────────────────────────────────┘
```

### Alternative Visual: Treemap (Recommended)

After analyzing competitor patterns, the **treemap visualization** is preferred over the grid for the following reasons:

```
┌─────────────────────────────────────────────────────────────┐
│                         產業熱度圖 (Treemap)                   │
│                                                             │
│  ┌─────────────────────────────┐ ┌──────────────────┐      │
│  │                             │ │                  │      │
│  │        半導體 +3.2%          │ │  電子零組件 +2.8% │      │
│  │        (市值佔比 35%)        │ │  (市值佔比 18%)   │      │
│  │                             │ │                  │      │
│  └─────────────────────────────┘ └──────────────────┘      │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐     │
│  │               │ │               │ │               │     │
│  │  金融保險     │ │  電腦及周邊     │ │  生技醫療     │     │
│  │  +1.1%        │ │  +2.3%        │ │  +2.5%        │     │
│  └───────────────┘ └───────────────┘ └───────────────┘     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ 紡織 │ │ 化學 │ │ 觀光 │ │ ...  │ │ ...  │ │ ...  │   │
│  │ +0.8%│ │ +0.9%│ │ -1.5%│ │      │ │      │ │      │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│─────────────────────────────────────────────────────────────│
└─────────────────────────────────────────────────────────────┘

Treemap advantages:
- Size = market cap (immediate visual hierarchy of sector importance)
- Color = performance (green/red color system)
- Click-through → sector detail page with top companies + narrative
```

### Design Specifications

**Visualization**: Plotly treemap (`plotly.express.treemap`)
- Size: Market cap (or number of listed companies as proxy)
- Color: Performance change (%) using diverging color scale
- Labels: Sector name + percentage change
- Click: Navigate to sector detail page

**Color Scale for Heatmap**:

| Performance | Color | Hex |
|-------------|-------|-----|
| > +3% | Dark green | `#1E8449` |
| +1% to +3% | Green | `#27AE60` |
| 0% to +1% | Light green | `#82E0AA` |
| -1% to 0% | Light red | `#F1948A` |
| -3% to -1% | Red | `#E74C3C` |
| < -3% | Dark red | `#922B21` |

**Sector Detail Page** (click-through destination):
- Sector name + one-liner description (≤ 40 chars)
- Performance summary for selected time range
- Top 5 companies in the sector (using `_story_card()` mini-version)
- Plain-language narrative: "本週半導體上漲3.2%，主要因為AI晶片需求持續強勁，台積電和聯發科領漲"
- The narrative is generated from templates + event data

**Time Range Selector**: Buttons for [今日] [本週] [本月] — placed at top of content area (controls clearly separated from data, per design system)

**Competitor Reference**:

| Competitor | What They Do | How We Differentiate |
|-----------|-------------|---------------------|
| **StockEdge** | Visual sector heatmap with scan-based discovery | We add plain-language narratives explaining WHY sectors move — StockEdge is purely visual |
| **Moomoo** | Interactive sector heatmap with basic explanations | We go deeper with analogy-rich narratives and company-level drill-down |
| **永豐金證券** | "Sector Rotation Visualizer" showing momentum over time | We add the plain-language education layer; their visualizations lack explanatory text |
| **財報狗** | Sector overview with heat indicators | We add click-through to sector detail with company stories; 財報狗 is summary-only |

**Alignment with Design System**:

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ The treemap IS the "one key point" — which sectors are up/down. One visual, one message |
| **Ten-second test** | ✅ User looks at the treemap and immediately sees: green sectors = up, red = down, bigger = more important. < 5 seconds |
| **Zone A/B/C** | ✅ Heatmap is Zone C content. Time selector at top of content area, clearly separated. Sidebar navigation links to this page |
| **Plain-language** | ✅ Sector narratives use everyday language. Sector one-liners avoid jargon |
| **Color system** | ✅ Green/red for performance direction (existing convention). 6 levels of green/red provide granularity without adding new colors |
| **Max 200 chars** | ✅ Sector one-liner ≤ 40 chars. Sector narrative ≤ 100 chars. Total ≤ 140 chars per sector detail page |

### Responsive Design Note

**D-06 (Mobile Responsiveness)**: The treemap visualization must degrade gracefully on mobile:
- Mobile: Show a **scrollable vertical list** instead of treemap grid
- Each sector as a `_heat_row_card()` — horizontal bar with sector name + color indicator + percentage
- Sort by absolute performance change (biggest movers first)
- This is a temporary workaround; full mobile optimization is deferred

---

## Design Direction D: C53-1 Social Sharing

### Description

**Shareable links and image cards** for any company page, comparison, or sector view. Users can share a beautifully formatted summary card to LINE, Facebook, or copy a link — every shared card is a new user acquisition event.

### Visual Mockup: Shareable Card (generated image)

```
┌─────────────────────────────────┐
│  📊 股識 Stock Explorer          │
│─────────────────────────────────│
│                                 │
│  台積電 (2330)                    │
│  全球90%先進晶片的製造商           │
│                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  毛利率 55%  │  營收成長 28%      │
│  ROE 31%    │  本益比 18x       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                 │
│  "每10支iPhone，就有9支用        │
│   台積電的晶片"                   │
│                                 │
│  → 完整分析：tinyurl.com/xxx    │
│                                 │
│  🔵 Powered by 股識              │
└─────────────────────────────────┘
```

### Design Specifications

**Share Button Placement**: 
- On company pages: Floating `📤 分享` button in bottom-right corner (fixed position, `z-index: 100`)
- On comparison pages: Same floating button, shares the comparison card
- On sector pages: Shares the sector heatmap card

**Share Card Content** (generated via Pillow):
- Header: "📊 股識 Stock Explorer" with blue `#3498DB` accent
- Company one-liner (≤ 40 chars)
- 4 key metrics in a 2×2 grid (not 3, because 2×2 is more visually balanced for square cards)
- One "Did You Know?" fact (≤ 60 chars)
- Footer: Short URL back to Stock Explorer + "Powered by 股識"
- Card size: 600×400px (optimized for LINE/Facebook preview)
- Font: Noto Sans TC (not available in Pillow → fallback to system sans-serif)

**Share Channels**:
1. **LINE**: Opens LINE share URL (`https://social-plugins.line.me/lineit/share?url=...`)
2. **Facebook**: Opens Facebook share dialog
3. **Copy Link**: Copies short URL to clipboard with `st.toast("連結已複製！")` confirmation

**Implementation Note**: 
- Sprint 4 MVP (C53-1) = shareable **URL only** — no image generation yet
- Streamlit's built-in URL parameters make each company page naturally shareable via URL
- Image card generation deferred to Sprint 5+ (requires Pillow + font handling)

**Competitor Reference**:

| Competitor | What They Do | How We Differentiate |
|-----------|-------------|---------------------|
| **TradingView** | "Ideas" sharing — users share chart analysis | We share company STORIES, not just charts. More educational, less trading-focused |
| **Plotch.ai** | Story card sharing for market narratives | We add plain-language metric explanations that Plotch.ai cards lack |
| **Stake** | Social discovery — see what others are viewing | We focus on outbound sharing (user shares content) rather than inbound discovery |
| **Minkabu** | Portfolio sharing and public investment blogs | We keep it simple: share a company card, not a full portfolio |

---

## New Card Type Specifications

### Complete Card Type Library (Updated for Sprint 4)

The following card types must be added to `_router_base.py` to support Sprint 4 features:

```python
def _story_card(title: str, subtitle: str, metrics: list, fact: str, icon: str = "🏢") -> str:
    """Hero card for 30-second company summary (C48).
    - border-left: 6px solid #F39C12 (amber hero status)
    - background: linear-gradient(135deg, #FFF8F0, #FFFFFF)
    - Contains: one-liner, 3 metrics with analogies, rotating fact
    - Max total text: 200 chars
    """

def _compare_card(left_story: dict, right_story: dict, bullets: list, analogy: str) -> str:
    """Side-by-side story comparison (C38).
    - Two sub-columns with _story_card() content
    - Comparison bullets below with green/red dot indicators
    - Closing analogy line
    - Disclaimer: '這不是投資建議'
    - Max total text: 200 chars for bullets + analogy
    """

def _sector_tile(sector_name: str, performance: float, market_cap: int) -> str:
    """Individual sector tile for heatmap grid (C51 mobile fallback).
    - Background color based on performance (green/red scale)
    - Text: sector name + percentage
    - Click-through to sector detail
    """

def _explain_card(title: str, content: str, icon: str = "❓") -> str:
    """Light blue expandable card for metric explanations (C56 — Sprint 5).
    - border-left: 3px solid #3498DB, background: #EBF5FB
    - Expandable via st.expander
    """

def _diary_card(title: str, content: str, icon: str = "📝") -> str:
    """Green card for personal diary entries (C55 — Sprint 6).
    - border-left: 4px solid #27AE60, background: #F0FFF4
    - Text area for free-form notes
    """

def _checklist_card(title: str, content: str, icon: str = "📋") -> str:
    """Amber card for pre-investment checklist (C62 — Sprint 5).
    - border-left: 4px solid #F39C12, background: #FFF8F0
    - 5 checkboxes with section links
    """

def _badge_card(title: str, content: str, icon: str = "🏆") -> str:
    """Blue gradient card for achievement badges (C60 — Sprint 5).
    - border-left: 4px solid #3498DB, background: linear-gradient(135deg, #EBF5FB, #FFFFFF)
    - Badge emoji + name + description
    """

def _timeline_card(title: str, events: list, icon: str = "📅") -> str:
    """Gold card for company timeline (C34 — Sprint 6).
    - border-left: 4px solid #F4D03F, background: #FEF9E7
    - Chronological event list with plain-language descriptions
    """
```

### Card Type Color Summary

| Card Type | Border | Background | Usage | Sprint |
|-----------|--------|------------|-------|--------|
| `_info_card` | `#3498DB` (blue) | `#F8F9FA` | Standard info display | ✅ Existing |
| `_summary_card` | `#F39C12` (amber) | `#FFF8F0` | Key takeaways (C37) | ✅ Existing |
| `_白话_card` | `#27AE60` (green) | `#F8F9FA` | Plain-language explanations | ✅ Existing |
| `_story_card` | `#F39C12` (amber, 6px) | Gradient `#FFF8F0→#FFF` | Company story (C48) | Sprint 4 |
| `_compare_card` | N/A (double `_story_card`) | Inherited | Comparison (C38) | Sprint 4 |
| `_sector_tile` | None | Performance-based | Heatmap tile (C51) | Sprint 4 |
| `_explain_card` | `#3498DB` (blue, 3px) | `#EBF5FB` | Metric explanations (C56) | Sprint 5 |
| `_diary_card` | `#27AE60` (green) | `#F0FFF4` | Personal diary (C55) | Sprint 6 |
| `_checklist_card` | `#F39C12` (amber) | `#FFF8F0` | Pre-investment checklist (C62) | Sprint 5 |
| `_badge_card` | `#3498DB` (blue) | Gradient `#EBF5FB→#FFF` | Achievement badges (C60) | Sprint 5 |
| `_timeline_card` | `#F4D03F` (gold) | `#FEF9E7` | Company timeline (C34) | Sprint 6 |

---

## Open Design Issues Resolution Plan

### D-021: C43 Hover Values
**Status**: Resolved in Sprint 4
**Design solution**: Add hover tooltip to C43 snowflake chart that shows the underlying metric value for each dimension. The tooltip format: `獲利能力: 4.2/5 (ROE: 31%, 行業平均: 18%)`
**Card type**: Extend existing C43 radar chart with custom hover text

### D-024: `_info_card` Background
**Status**: Sprint 4 fix (D-037)
**Design solution**: Change `_info_card()` background from `#FFF8F0` to `#F8F9FA` per design system spec
**Impact**: Affects all pages using `_info_card()` — must verify visual consistency across 6+ pages

### D-025: C39 Empty State
**Status**: Sprint 4 fix
**Design solution**: Design a "no significant changes" card:
```
🔄 最近沒有重大變化
過去30天內的指標變動都在正常範圍內。
這通常表示公司營運穩定，沒有特別需要關注的事件。
```
**Card type**: New `_empty_card()` — gray border (`#BDC3C7`), light gray background (`#F8F9FA`), `ℹ️` icon

### D-003: Inconsistent Card Styling
**Status**: Partially resolved in Sprint 4
**Root cause**: `group_structure.py`, `watchlist.py`, and `etf_detail.py` use inline HTML that doesn't use the shared card components
**Sprint 4 action**: Add new card type library (above). Sprint 5 action: migrate all pages to shared components

### D-006: Mobile Responsiveness
**Status**: Deferred (Streamlit limitations)
**Sprint 4 mitigation**: 
- Sector heatmap (C51) provides list-view fallback for mobile
- Story card (C48) uses single-column layout naturally
- Compare card (C38) should stack vertically on mobile (use `st.columns` with responsive check)
- Add `viewport` meta tag to base template

---

## Design Risk Register

### P1 Risks (Must Resolve in Sprint 4)

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|-------------|--------|------------|-------|
| **DR-041** | C48 story card is perceived as redundant with C37 key takeaways | Medium | High — users see two "summary" sections and are confused | Clear positioning: C48 = narrative identity (who is this company), C37 = analytical summary (what are the numbers). C48 first, C37 second. Different visual design (hero card vs info card) | Designer |
| **DR-042** | C38 compare stories is perceived as "which stock to buy" recommendation | High | Critical — violates "historian not stock picker" positioning | Required disclaimer. No scoring. Neutral framing ("different" not "better"). Design review must verify all language is neutral | Designer + PM |
| **DR-043** | C51 sector heatmap color scale confuses users (6 levels too many) | Medium | Medium — users can't distinguish between dark green and light green | Simplify to 3 levels (green/yellow/red) for MVP. Add legend prominently. Test with 5 users | Designer |
| **DR-044** | New card types break Zone C layout consistency | Low | High — new cards may be wider/narrower than existing ones | All new cards follow the same CSS template (border-radius: 12px, padding: 1.2rem, margin: 0.5rem 0). Design must verify rendered HTML matches | Developer + Designer |

### P2 Risks (Monitor in Sprint 4)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| **DR-045** | Card type library grows too large (11 card types by Sprint 6) | Medium | Medium — maintenance burden | Document each card type with its specific use case. Don't create new cards without deleting/updating existing ones |
| **DR-046** | C53-1 share button placement covers content on small screens | Medium | Low | Floating button uses `position: fixed; bottom: 20px; right: 20px` with `z-index: 100`. Add small screen detection to hide or reduce |
| **DR-047** | C51 sector page introduces new router pattern that doesn't match existing stock_id flow | Low | Medium | Architect has identified this as D34 — document the two patterns separately |
| **DR-048** | Sprint 4 adds too many new card types at once, risking visual inconsistency | Medium | Medium | Sprint 4 adds only 2 new rendering patterns: `_story_card()` + `_sector_tile()`. Other card types are defined but not yet used |

---

## Recommendation

### Primary Recommendation: Adopt All Four Sprint 4 Design Directions

The Sprint 4 features — **C48 Story Card**, **C38 Compare Stories**, **C51 Sector Heatmap**, and **C53-1 Social Sharing** — form a **cohesive visual/UX upgrade** that transforms Stock Explorer from a single-company analysis tool into a **market-aware, shareable, comparison-capable learning platform**:

```
[Market View: C51 Sector Heatmap]  →  [Company View: C48 Story Card]
          ↓                                      ↓
    "Which sectors                    "What is this company?"
     are hot?"
          ↓                                      ↓
[Comparison View: C38 Compare Stories]  →  [Sharing: C53-1 Social URL]
          ↓
    "How are these
     companies different?"
```

### Sprint 4 Design Priority

| Priority | Feature | Design Deliverable | Key Design Decision |
|----------|---------|-------------------|-------------------|
| **1** | C48 Story Card | `_story_card()` component, metric selection algorithm, gradient styling | Hero card (amber, 6px border) ABOVE C37 — not replacing it, but introducing it |
| **2** | C38 Compare Stories | `_compare_card()` component, side-by-side layout, neutral framing rules | Neutral language is NON-NEGOTIABLE. Design review must approve all comparison text |
| **3** | C51 Sector Heatmap | Treemap visualization, 3-level color scale, sector detail page narrative | Simplified 3-level color scale (green/yellow/red) for MVP. Add legend prominently |
| **4** | C53-1 Social Sharing | URL parameter support, share button placement, (deferred: image card generation) | Floating button in bottom-right. MVP = URL sharing only |

### Design Grade Projection

If all four design directions are implemented as specified, the design grade can reach **A+** in Round 15:

- **A+ criteria**: All P1 design issues resolved, new card types maintain visual consistency, Zone A/B/C maintained across new pages, neutral comparison framing prevents positioning violations, social sharing drives distribution.
- **Current blockers to A+**: DR-041 (C48/C37 redundancy), DR-042 (C38 recommendation framing), DR-043 (heatmap color complexity)
- **Risk-adjusted projection**: A (maintained) if DR-042 is resolved smoothly; A+ if all three DR-041/42/43 are resolved

### Key Design Decisions for Discussion

1. **C48 position relative to C37**: C48 ABOVE C37 (narrative first, then analytical). This is a departure from the current C37-first order. Rationale: story-first aligns with "ten-second test" better than analysis-first.
2. **C38 color-coding for comparison**: Use green/red dots for metric direction ONLY, with explicit disclaimer. This is the minimum viable differentiation. Alternative: no color-coding at all (risk-averse option).
3. **C51 color scale**: 3 levels (MVP) vs 6 levels (full). Recommendation: 3 levels for usability, expand to 6 in Sprint 5+ after user testing.
4. **C53-1 scope**: URL-only MVP (Sprint 4) vs URL + image card (Sprint 5). Recommendation: URL-only in Sprint 4 (no dependency on Pillow/font rendering), image card in Sprint 5.

---

*Design Review completed. Four directions proposed for Sprint 4: C48 Company Story Card (30-second visual summary), C38 Compare Stories (side-by-side narrative comparison), C51 Sector Heatmap (visual market overview), and C53-1 Social Sharing (shareable links). All four maintain PPT-style design system, pass the ten-second test, and respect Zone A/B/C separation. Key design risk: C38 must be rigorously neutral to avoid "stock picker" perception. Next review: After Sprint 4 feature implementation.*
