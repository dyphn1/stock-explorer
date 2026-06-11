# Design Review — Discussion Round 10

> **Author**: Design Reviewer
> **Date**: 2026-06-15
> **Context**: Sprint 2 is complete (C37, C39, C43, C45 implemented). Sprint 3 is next. This review evaluates the UX impact and provides design direction for the remaining Round 9 features: C42 (Stock Screener), C44 (Risk Analysis), C46 (Moat Analysis), C47 (Education Academy).
> **Current Design Grade**: B+ (C37 + C43 now implemented, addressing the two P0 gaps)

---

## Table of Contents

1. [UX Impact Assessment](#ux-impact-assessment)
2. [Design Direction for C42 (Stock Screener)](#design-direction-for-c42-stock-screener)
3. [Design Direction for C44 (Risk Analysis)](#design-direction-for-c44-risk-analysis)
4. [Design Direction for C46 (Moat Analysis)](#design-direction-for-c46-moat-analysis)
5. [Design Direction for C47 (Education Academy)](#design-direction-for-c47-education-academy)
6. [Recommendations](#recommendations)

---

## UX Impact Assessment

### Current Business Card Page State (Post-Sprint 2)

The business card page now has the following sections after Sprint 2:

| # | Section | Source | Status |
|---|---------|--------|--------|
| 1 | Company name + price header | Pre-Sprint 2 | ✅ Existing |
| 2 | One-liner | Pre-Sprint 2 | ✅ Existing |
| 3 | "Did You Know?" fact | Pre-Sprint 2 | ✅ Existing |
| 4 | Key Takeaways Summary Card (C37) | Sprint 2 | ✅ New |
| 5 | Snowflake Health Visualization (C43) | Sprint 2 | ✅ New |
| 6 | What Changed Delta Card (C39) | Sprint 2 | ✅ New |
| 7 | 3 Key Metrics cards | Pre-Sprint 2 | ✅ Existing |
| 8 | Valuation Band Chart (C45) | Sprint 2 | ✅ New |
| 9 | Dividend Story + Countdown | Pre-Sprint 2 | ✅ Existing |
| 10 | Revenue Pie Chart | Pre-Sprint 2 | ✅ Existing |
| 11 | Revenue Trend Chart | Pre-Sprint 2 | ✅ Existing |
| 12 | News section | Pre-Sprint 2 | ✅ Existing |
| 13 | Disclaimer | Pre-Sprint 2 | ✅ Existing |

**That is 13 sections on a single page.** The page has grown significantly from the original ~9 sections. The two P0 gaps (no synthesis, no visual health score) are now addressed by C37 and C43, but the page is approaching critical mass.

### Overload Risk Matrix for C42-C47

| Feature | Placement | Overload Risk | PPT-Style Risk | Recommendation |
|---------|-----------|---------------|----------------|----------------|
| **C42** (Screener) | **New page** (sidebar nav) | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |
| **C44** (Risk) | Business Card page | 🔴 HIGH — adds 14th section | 🟡 MEDIUM — new card type, new color | Needs progressive disclosure strategy |
| **C46** (Moat) | Business Card page | 🔴 HIGH — adds 15th section | 🟡 MEDIUM — new card type, new icon | Needs progressive disclosure strategy |
| **C47** (Academy) | **New page** (sidebar nav) | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |

### Key Finding: The Business Card Page Cannot Absorb C44 and C46 As-Is

With 13 sections already, adding C44 (Risk Analysis) and C46 (Moat Analysis) as full card sections would push the page to 15 sections. This violates the PPT-style "one key point per page" principle and creates a scrolling wall of content that defeats the ten-second test.

**The business card page needs a tabbed or collapsible strategy for Sprint 4+ features.** C42 and C47 are safe since they live on separate pages.

---

## Design Direction for C42 (Stock Screener)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C42 is a new top-level page accessible from the sidebar navigation. It does not touch the business card page at all.

**Strategic impact**: HIGH — This transforms Stock Explorer from a "lookup tool" (users must know the stock name) to a "discovery platform" (users can find interesting companies). This is the single most important UX transformation in the remaining feature set. 財報狗's #1 feature is screening; its absence in Stock Explorer is the #1 beginner engagement barrier.

### 2. Design Consistency with PPT-Style Principle

**Placement**: New sidebar entry: `🔍 選股探索` (Stock Discovery). This is consistent with existing sidebar navigation patterns.

**Page layout** (PPT-style compliant):
- **Zone A**: Standard navbar (radio navigation)
- **Zone B**: Standard sidebar
- **Zone C**: Screener page content

**Page structure** (one key point per "slide"):
```
Slide 1: "發現有趣的公司" (hero text, ≤ 40 chars)
Slide 2: 3 preset screen cards (stable dividend / growth / value)
Slide 3: Results (card-based, NOT table)
```

**Card-based results** (critical): Each result must be a card, not a table row. Table layouts violate PPT-style and are the reason the watchlist page feels like a different product. Each result card shows:
- Company name + ticker
- One-liner (what they do)
- Key metric that matched the filter
- `查看名片` button (navigates to business card page)

**Preset screens** (beginner-friendly, not raw filters):
```
🟢 穩定收息    — 殖利率 > 4%，配息率 < 70%
📈 成長潛力    — 營收連續3年成長 > 20%
💰 便宜估值    — 本益比 < 15，股價淨值比 < 2
```

**Framing language** (historian positioning): "發現有趣的公司" not "篩選好股票". The CTA should be `開始探索` not `開始選股`. Results header: "找到 X 間值得了解的公司" not "找到 X 檔股票".

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **財報狗** | Multi-condition screening with 100+ metrics | Simplified to 3 presets + 5 key metrics (ROE, P/E, dividend yield, revenue growth, P/B) |
| **Stockopedia** | StockRank-integrated results | Results show a simple "分數" (0-100) alongside each card |
| **JZ Invest** | Community-driven presets | Presets are curated by the Stock Explorer team, not user-generated |
| **Simply Wall St** | Visual-first results | Each result card has a mini snowflake sparkline (5-bar visual) |

**Key differentiator**: No competitor combines screening with plain-language education. Every result card should include a one-line plain-language explanation of WHY this company matched. Example: "台積電符合『成長潛力』因為過去3年營收成長25%，主要來自5奈米晶片需求."

### 4. Mobile Responsiveness Considerations

- **Preset cards**: Stack vertically on mobile (already single-column on small screens)
- **Filter controls**: Use `st.selectbox` and `st.slider` (native Streamlit, mobile-friendly) instead of custom HTML
- **Result cards**: Single-column stack on mobile (same as desktop cards, just narrower)
- **Avoid**: Multi-column filter layouts that break on small screens. Use a single-column filter panel above results.
- **Touch targets**: Buttons must be ≥ 44px height on mobile (Streamlit default is adequate)

### 5. Ten-Second Test Implications

**The screener page IS a ten-second test for the product's value proposition.** A beginner should be able to:
1. See the 3 preset cards (3 seconds)
2. Tap one (1 second)
3. See 3-5 result cards with plain-language explanations (6 seconds)
4. Understand: "This tool helps me find interesting companies to learn about"

**If the user sees a dense table of numbers, the test fails.** Card-based results are non-negotiable.

### Design Spec Summary

```
Page: 🔍 選股探索
├── Hero: "發現有趣的公司" (one-line description)
├── Preset Cards (3 cards, horizontal on desktop, vertical on mobile)
│   ├── 🟢 穩定收息
│   ├── 📈 成長潛力
│   └── 💰 便宜估值
├── Custom Filters (collapsible, advanced)
│   ├── ROE slider
│   ├── P/E slider
│   ├── Dividend yield slider
│   └── Revenue growth slider
└── Results (card-based grid)
    └── Per card: name, ticker, one-liner, match reason, 查看名片 button
```

---

## Design Direction for C44 (Risk Analysis)

### 1. UX Impact on Business Card Page

**Risk: 🔴 HIGH** — The business card page already has 13 sections. Adding a full risk analysis card as the 14th section pushes the page past the "one key point per page" threshold.

**Mitigation strategy**: C44 must use **progressive disclosure**. The default view shows a compact risk summary (2-3 lines). The full risk analysis expands on click. This is consistent with Simply Wall St's approach (summary first, details on click).

**Placement**: Business Card page, BELOW the Snowflake (C43) and Key Takeaways (C37), but ABOVE the 3 key metrics. The logic: after seeing the company's health summary (C43), the user should see what could go wrong BEFORE diving into detailed metrics. This creates a natural narrative arc: "Here's how healthy it is → Here's what could go wrong → Here are the detailed numbers."

**Alternative placement**: If the page feels too long, C44 can be placed in a collapsible `st.expander()` section titled `⚠️ 風險分析`. This is the recommended approach for Sprint 4.

### 2. Design Consistency with PPT-Style Principle

**Card design**: Warning-style card (red border `#E74C3C`, light red background `#FDEDEC`) with `⚠️` icon. This is a NEW card type that needs to be added to the design system.

**Content structure** (PPT-style: one key point per risk):
```
⚠️ 風險分析
① 客戶集中度高
   90%營收來自3大客戶（蘋果、輝達、AMD）
   過去發生：2020年華為禁令導致營收下降15%
   📊 觀察指標：客戶訂單變化

② 匯率風險
   70%營收以美元計價，台幣升值會壓縮利潤
   過去發生：2022年台幣升值影響毛利率2%
   📊 觀察指標：USD/TWD匯率
```

**Character limits**: Each risk ≤ 120 Chinese characters total (including evidence and indicators). Maximum 3 risks shown. This keeps the card compact.

**Tone** (historian positioning): Factual, not predictive. Use "過去發生" (happened before) and "觀察指標" (indicators to watch) — never "可能發生" (might happen) or "預測" (predict).

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Simply Wall St** | Visual risk breakdown (color-coded bars) | Use a mini horizontal bar for each risk showing severity (low/medium/high) |
| **Morningstar** | Uncertainty rating (wide range) | Show a "風險等級" badge: 🟢低 / 🟡中 / 🔴高 |
| **TEJ** | Credit risk analysis | Simplified to 3 key risks max, plain-language descriptions |
| **財報狗** | No risk section | Stock Explorer's risk analysis is a differentiator |

**Key differentiator**: No TW competitor has plain-language risk analysis with historical evidence. Simply Wall St has visual risk but without the "here's what happened before" narrative. Our historian framing is unique.

### 4. Mobile Responsiveness Considerations

- **Risk cards**: Stack vertically (already the default for card-based layout)
- **Expand/collapse**: On mobile, risks should be collapsed by default (saves vertical space). Use `st.expander()` for each risk.
- **Severity badges**: Use emoji (🟡🔴) instead of color-only indicators (color-blind accessible, works on all screens)
- **Touch targets**: Expand/collapse toggle must be ≥ 44px

### 5. Ten-Second Test Implications

**Risk analysis should NOT be part of the ten-second test.** The ten-second test is answered by C37 (Key Takeaways) and C43 (Snowflake). Risk analysis is a "second-level" detail that users explore after the initial overview.

**However**: The compact risk summary (collapsed state) should be visible in the first viewport. A user scrolling through the page should see the `⚠️ 風險分析` header and understand "this section exists" even if they don't expand it. This sets expectations without overwhelming.

### Design Spec Summary

```
Section: ⚠️ 風險分析 (collapsible/expander)
├── Default (collapsed): "3個主要風險：客戶集中度、匯率、技術迭代"
├── Expanded:
│   ├── Risk 1: 客戶集中度高 [🔴高]
│   │   ├── Description (≤ 40 chars)
│   │   ├── Historical evidence (≤ 40 chars)
│   │   └── Watch indicator (≤ 30 chars)
│   ├── Risk 2: 匯率風險 [🟡中]
│   │   └── (same structure)
│   └── Risk 3: 技術迭代風險 [🟡中]
│       └── (same structure)
└── Footer: "風險分析基於歷史資料，不構成投資建議"
```

---

## Design Direction for C46 (Moat Analysis)

### 1. UX Impact on Business Card Page

**Risk: 🔴 HIGH** — Same overload concern as C44. Adding Moat as a 15th section is not viable as a full card.

**Mitigation strategy**: C46 should be placed in a **tab alongside C36 (Visual Revenue Tree)**. The revenue tree tab already exists as a sub-section. Adding a "護城河" tab creates a "Company Deep Dive" area that groups advanced analysis together, keeping the main page clean.

**Recommended placement**: New tab `🏰 護城河` in the same tab group as `收入樹狀圖` (C36). This keeps the main business card page at 13 sections and groups advanced features in a discoverable but non-intrusive location.

**Alternative**: If C36 is not yet implemented (Sprint 4), C46 can be a standalone collapsible section. But the tab approach is cleaner long-term.

### 2. Design Consistency with PPT-Principle

**Card design**: Castle-themed card (border `#2C3E50` dark navy, icon `🏰`). This is a NEW card type. The dark navy conveys "strength" and "durability" — appropriate for moat analysis.

**Content structure**:
```
🏰 護城河分析
類型：技術領先
強度：🟢 寬護城河

台積電是全球唯一能量產5奈米的工廠，
競爭對手三星和英特爾落後2年以上。

歷史證據：過去10年毛利率維持50%以上
```

**Moat types** (5 categories, matching Morningstar's framework):
- `技術領先` (Technology)
- `品牌價值` (Brand)
- `成本優勢` (Cost)
- `網路效應` (Network)
- `轉換成本` (Switching Costs)

**Moat strength** (3 levels, matching Morningstar):
- `🟢 寬護城河` (Wide) — durable competitive advantage, 10+ years
- `🟡 窄護城河` (Narrow) — some advantage, 5-10 years
- `🔴 無護城河` (None) — no durable advantage

**Character limits**: Total card text ≤ 150 Chinese characters. One moat type per company (the strongest one). Historical evidence ≤ 60 characters.

**Manual curation**: Top 20 stocks only. For other stocks, show a template-based fallback: "此公司的護城河分析仍在整理中" with a `🔔 通知我` button.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Morningstar** | Moat rating (wide/narrow/none) + narrative | Same 3-level system, but with plain-language narrative and historical evidence |
| **TEJ** | Industry analysis with market share | Simplified to moat type + one key metric (market share, margin, etc.) |
| **Simply Wall St** | No moat analysis | Stock Explorer's moat analysis is a unique differentiator |

**Key differentiator**: Morningstar's moat rating is iconic but only covers US stocks and uses professional language. Stock Explorer's plain-language moat analysis with historical evidence for TW stocks is unique. The "historian" framing (explain what the moat IS, not predict if it will last) is our angle.

### 4. Mobile Responsiveness Considerations

- **Tab layout**: Tabs work well on mobile (Streamlit's `st.tabs()` is responsive)
- **Moat card**: Single-column, full-width on mobile
- **Moat strength badge**: Use emoji (🟢🟡🔴) — works on all devices, color-blind accessible
- **Historical evidence**: Can be truncated on mobile with "查看更多" expansion

### 5. Ten-Second Test Implications

**Moat analysis is NOT part of the ten-second test.** It's a "deep dive" feature for users who want to understand the company's competitive position. The ten-second test is fully answered by C37 + C43.

**However**: The tab label `🏰 護城河` should be intuitive enough that users understand what it contains without clicking. The castle icon is universally understood as "defense" / "protection" / "strength."

### Design Spec Summary

```
Tab: 🏰 護城河 (grouped with 收入樹狀圖 tab)
├── Moat type badge: 技術領先
├── Moat strength: 🟢 寬護城河
├── Plain-language description (≤ 80 chars)
├── Historical evidence (≤ 60 chars)
└── Key metric: 毛利率 52% (10-year avg)
```

---

## Design Direction for C47 (Education Academy)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C47 is a new top-level page accessible from the sidebar. It does not touch the business card page.

**Strategic impact**: TRANSFORMATIVE — This is the feature that turns Stock Explorer from a "stock lookup tool" into an "investing education platform." It's the long-term differentiator that no TW competitor has. Investopedia and Stockopedia prove demand internationally; no one does this for TW stocks.

### 2. Design Consistency with PPT-Style Principle

**Placement**: New sidebar entry: `📚 學習學院` (Learning Academy). Positioned below the main navigation items, above the disclaimer. This signals "educational resource" not "core analysis tool."

**Page structure** (PPT-style: one key point per lesson):
```
Page header: "📚 學習學院 — 從零開始學投資"
├── Difficulty filter: 初級 | 中級 | 高級
├── Lesson cards (grid layout)
│   ├── 📖 什麼是營收？
│   │   ├── Difficulty: 初級
│   │   ├── Read time: 3 分鐘
│   │   └── TW example: 台積電
│   ├── 📖 什麼是獲利？
│   │   ├── Difficulty: 初級
│   │   ├── Read time: 4 分鐘
│   │   └── TW example: 鴻海
│   └── (more lessons...)
└── Progress tracker (optional, Phase 2)
```

**Lesson page structure** (one key point per lesson):
```
Lesson: 什麼是營收？
├── Hero: "營收就是一家公司賣東西賺到的錢" (≤ 40 chars)
├── Analogy: "就像一間雞排店，一天賣100塊雞排，每塊50元，營收就是5,000元"
├── Real example: 台積電 2024 年營收 2.89 兆元
├── Key takeaway: "營收愈大不代表愈賺錢，還要看成本"
├── Quiz: "以下哪個是營收？" (multiple choice)
└── Next lesson: 什麼是獲利？
```

**Card design**: Lesson cards use the standard info card style (blue border) with a `📖` icon. Difficulty badges: `🟢 初級` / `🟡 中級` / `🔴 高級`.

**Reuse analogy engine**: All lesson explanations should use the existing analogy engine (`_白话_card()`) for consistency. The academy is where the analogy engine shines — every concept gets a real-world analogy + TW stock example.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Investopedia** | Structured courses + dictionary | Structured lessons (10-15), each with real TW stock example |
| **Stockopedia** | StockRank-integrated education | Lessons linked to actual metrics shown on business card pages |
| **Investopedia** | Concept-first approach | Each lesson teaches the concept BEFORE showing the data |
| **Stockopedia** | Progressive difficulty (beginner → advanced) | 3 difficulty levels with clear prerequisites |

**Key differentiator**: Investopedia is US-focused and not stock-specific. Stockopedia is UK/EU-focused. Stock Explorer's academy uses REAL TW STOCK EXAMPLES for every concept. "什麼是ROE？" is explained using 台積電's actual ROE, not a hypothetical company. This is unique.

**Cross-linking opportunity**: Each lesson should link to relevant business card pages. "什麼是ROE？" → links to 台積電's business card page showing ROE. This creates a learning loop: learn concept → see real example → explore company → discover new concepts.

### 4. Mobile Responsiveness Considerations

- **Lesson grid**: 2-column on desktop, 1-column on mobile
- **Lesson pages**: Single-column, full-width (already PPT-style)
- **Quiz**: Use `st.radio()` for multiple choice (native Streamlit, mobile-friendly)
- **Progress tracking**: If implemented, use a simple progress bar (mobile-friendly)
- **Read time**: Display prominently — mobile users want to know "is this a 3-min or 30-min read?"

### 5. Ten-Second Test Implications

**The academy page IS a ten-second test for the product's educational value.** A beginner should be able to:
1. See the lesson grid (3 seconds)
2. Read 3-5 lesson titles (3 seconds)
3. Understand: "This platform teaches me investing concepts using real Taiwanese companies" (4 seconds)

**If the user sees a wall of text or a confusing lesson hierarchy, the test fails.** Card-based lesson grid with clear difficulty labels and read times is non-negotiable.

### Design Spec Summary

```
Page: 📚 學習學院
├── Header: "從零開始學投資" + difficulty filter
├── Lesson Grid (card-based, 2-col desktop / 1-col mobile)
│   └── Per card: title, difficulty badge, read time, TW example, 開始學習 button
└── Lesson Page (opened on card click)
    ├── Concept explanation (analogy + plain language)
    ├── Real TW stock example (with live data link)
    ├── Key takeaway (≤ 40 chars)
    ├── Quiz (1 question, multiple choice)
    └── Next lesson link
```

**Phase 1 scope** (pending Daniel decision): 5 pilot lessons covering the most fundamental concepts:
1. 什麼是營收？(Revenue)
2. 什麼是獲利？(Profit)
3. 什麼是ROE？(Return on Equity)
4. 什麼是P/E？(Price-to-Earnings)
5. 什麼是股利？(Dividend)

---

## Recommendations

### Immediate Actions (Before Sprint 3)

1. **Approve the "above the fold" definition for the business card page**: C37 (Key Takeaways) + C43 (Snowflake) are the ten-second answer. Everything else is below the fold or in tabs. This gives the team a clear boundary for what goes on the main page vs. what goes in tabs/expanders.

2. **Create the tabbed section strategy for Sprint 4**: The business card page needs a tab group for advanced analysis:
   - Tab 1: `📊 財務數據` (default — existing metrics)
   - Tab 2: `🌳 收入樹狀圖` (C36 — Sprint 4)
   - Tab 3: `🏰 護城河` (C46 — Sprint 4)
   
   C44 (Risk Analysis) should be a collapsible section ABOVE the tabs, not inside them. Risk is too important to hide behind a tab click.

3. **Add new card types to the design system** (`docs/design/design_system.md`):
   - Warning card (red border, for C44 Risk Analysis)
   - Castle card (dark navy border, for C46 Moat Analysis)
   - Lesson card (blue border + difficulty badge, for C47 Academy)

### Sprint 3 Priorities

4. **C42 (Stock Screener) should be the Sprint 4 priority, not C46**: The screener transforms the product from lookup to discovery. Moat analysis is a nice-to-have for existing users. If Sprint 4 has capacity issues, cut C46 before C42. (This aligns with the pending_review.md recommendation.)

5. **C44 (Risk Analysis) should use progressive disclosure**: Collapsible `st.expander()` with a compact summary visible by default. This keeps the business card page manageable.

### Sprint 4+ Priorities

6. **C47 (Education Academy) Phase 1**: 5 pilot lessons, validate quality before scaling. Each lesson must use real TW stock examples and the existing analogy engine. Cross-link lessons to business card pages.

7. **C46 (Moat Analysis) manual curation**: Start with top 20 stocks. Template-based fallback for others. The castle icon and 3-level strength system should be intuitive for beginners.

### Design System Updates Needed

8. **Document the "business card page architecture"**: With 13+ sections, the page needs a clear information architecture document that defines:
   - Above the fold: C37 + C43 (ten-second test)
   - Below the fold: metrics, charts, dividend, news
   - Tabs: C36 (Revenue Tree) + C46 (Moat)
   - Collapsible: C44 (Risk)

9. **Standardize the "historian" tone for risk and moat**: Both C44 and C46 must use factual, historical language. Create a style guide section that defines:
   - ✅ "過去發生" (happened before), "歷史證據" (historical evidence), "觀察指標" (watch indicators)
   - ❌ "可能發生" (might happen), "預測" (predict), "建議" (recommend)

### Mobile-First Considerations

10. **All new features must be designed mobile-first**: Streamlit's mobile rendering is limited. Design for the smallest screen first, then enhance for desktop. This is especially critical for:
    - C42 screener results (card-based, single-column)
    - C47 lesson grid (single-column on mobile)
    - C44 risk cards (collapsed by default on mobile)

### Design Grade Projection

| Scenario | Grade |
|----------|-------|
| C42 + C44 implemented well, C46 deferred | A- |
| C42 + C44 + C46 implemented with tab strategy | A |
| C42 + C44 + C46 + C47 Phase 1 implemented | A+ |
| All features added without tab/collapse strategy | B (overload) |

---

*Design Review completed. The key message: C42 and C47 are safe (separate pages). C44 and C46 need progressive disclosure (tabs/expanders) to avoid business card page overload. The "above the fold" definition (C37 + C43 = ten-second test) must be formally approved before Sprint 4 begins.*
