## 2026-06-18 Design Review — Sprint 13b Feature Candidates

> **Author**: Design Reviewer
> **Context**: Sprint 13a complete (C33 Glossary + C48 Story Card), Design Grade A (17th consecutive A/A-)
> **Scope**: Sprint 13b candidates — C46 Moat Analysis + C36 Revenue Tree — UX evaluation and design direction

---

### C46 Moat Analysis — UX Evaluation

- **Placement recommendation**: New **"🏰 護城河分析"** section on the **Business Card page**, positioned **below the fold** (after C37 Summary + C39 What Changed + C43 Snowflake). Recommend `st.expander(expanded=False)` to avoid overwhelming beginners. This is a "deep dive" feature — interested users will expand it, beginners won't be confronted with it. Do NOT place it above the fold; the Business Card page already has 3 cards at the top (C37/C39/C43) and adding a 4th would violate the "3 cards above fold" rule established in Round 21.

- **Visual approach**: **5-dimension moat scoring** presented as a **horizontal row of 5 mini-cards** (matching the C43 Snowflake dimension-card pattern already established). Each card shows:
  - Moat dimension name (e.g., "技術壁壘", "品牌價值", "成本優勢", "網路效應", "轉換成本")
  - Strength indicator: **寬護城河** (green `#27AE60`), **窄護城河** (yellow `#F39C12`), or **無護城河** (red `#E74C3C`)
  - One-line plain-language explanation below each indicator
  - Example: "技術壁壘 🟢 寬護城河 — 全球唯一能量產5nm晶片的工廠，競爭對手落後2年以上"

  Below the 5 mini-cards, a **"歷史證據"** section with 2-3 bullet points of historical evidence (e.g., "過去10年毛利率維持50%以上"、"市佔率從30%提升到55%"). This is what makes it "historian" — not predicting the moat will last, but showing how it has protected the company historically.

  **Alternative considered**: Radar chart overlay on C43 Snowflake. **Rejected** — the Snowflake already has 5 dimensions; adding moat as a 6th would clutter it. Moat Analysis is a separate concept (competitive advantage durability) from financial health. Keep them separate.

- **Alignment with design system**: **Strong** (⭐⭐⭐ on 9 of 10 criteria per Round 27 scoring matrix).
  - **PPT-style**: ✅ One key point per moat dimension (5 mini-cards = 5 key points, each with one color + one line)
  - **Ten-second test**: ✅ A beginner can glance at the 5 color-coded indicators and within 10 seconds know "TSMC has wide moats in technology and cost, narrow in brand"
  - **Beginner-friendly**: ✅ Castle/moat metaphor is universally understood (Morningstar proved this). Plain-language explanations mandatory for each dimension.
  - **Historian positioning**: ✅ Explains historical competitive advantage, doesn't predict future durability
  - **Text limit concern**: 5 dimensions × ~30 chars each = ~150 chars, plus evidence bullets × ~40 chars = ~120 chars. Total ~270 chars — **exceeds the 200-char static text limit**. Recommendation: Use `st.expander` to hide evidence bullets by default. Visible text (5 dimension cards) = ~150 chars, within limit.

- **Competitor reference**: **Morningstar Moat Rating** (Wide/Narrow/None) is the gold standard. Morningstar uses a simple 3-level rating with analyst commentary. Our improvement: (1) decompose into 5 specific dimensions (Morningstar gives only overall rating), (2) add historical evidence (Morningstar is forward-looking), (3) plain-language explanations (Morningstar is professional tone). **Simply Wall St** also has moat-like analysis within its snowflake but doesn't break it out separately. **No TW competitor** has moat analysis — this is a unique differentiator.

- **Data sourcing concern**: Moat analysis requires **qualitative judgment**. Recommend manual curation for top 20 stocks (same approach as C36 Revenue Tree). For non-top-20 stocks, use a **template-based fallback**: score each dimension using quantitative proxies (R&D spend → technology moat, gross margin → cost moat, customer concentration → switching cost moat, etc.) with a disclaimer: "此為量化估算，非專業分析". This avoids the "LLM hallucination" risk of auto-generating moat assessments.

---

### C36 Revenue Tree — UX Evaluation

- **Placement recommendation**: **New "商業模式" tab** on the Business Card page, **NOT a replacement for the existing pie chart**. The existing pie chart shows "what percentage each segment contributes" (composition). The Revenue Tree shows "how money flows through the business" (hierarchy). They answer different questions and both should exist. The new tab should be placed **after the existing "營收組成" section** or as a **toggle between "圓餅圖" and "樹狀圖"** within the same section. Recommend the toggle approach (simpler, no new tab needed): a small `st.radio` or `st.segmented_control` at the top of the revenue section that switches between pie chart and tree map.

- **Visual approach**: **Plotly Treemap** (not sunburst — treemap is better for hierarchical data with size encoding). Structure:
  - **Level 1**: Company name (root)
  - **Level 2**: Business segments (e.g., "5nm晶片", "7nm晶片", "封裝服務")
  - **Level 3**: Key customers (e.g., "Apple", "NVIDIA", "AMD") — only for top 20 stocks with curated data
  - Color coding: Use existing blue/green palette. Each segment gets a different shade of blue (`#3498DB` family). Do NOT use red/green for revenue segments — red/green is reserved for price direction.
  - Size = revenue contribution. Label = segment name + percentage.
  - Hover tooltip: segment name, revenue amount, percentage of total, plain-language description (e.g., "5nm晶片：台積電最先進的製程，佔營收40%，主要賣給Apple和NVIDIA")

  **Fallback for non-top-20 stocks**: If hierarchical revenue data is not available, show the existing pie chart with a small `st.info()` note: "此公司暫無詳細營收樹狀圖，顯示圓餅圖作為替代". This graceful degradation is critical — don't show an empty chart.

- **Alignment with design system**: **Strong** (⭐⭐⭐ on 8 of 10 criteria).
  - **PPT-style**: ✅ Treemap is inherently visual-first — one glance shows the business structure
  - **Ten-second test**: ⚠️ Moderate — treemaps can confuse beginners if too many segments. **Mitigation**: Limit to max 8 segments at Level 2, max 3 customers per segment. If data has more, group smaller ones into "其他".
  - **Beginner-friendly**: ⚠️ Needs plain-language labels. "5nm晶片" → "5nm晶片（最先進的晶片製造技術）". Use the glossary tooltip system (C33, just completed) to explain technical terms.
  - **Progressive drill-down**: ✅ Click a segment → drill into sub-segments. Natural interaction.
  - **Historian positioning**: ✅ Explains how the company makes money, not whether to buy
  - **Chart proportion**: ✅ Treemap occupies >60% of the section area (design system Section V.3)
  - **Max 3 charts per page**: ✅ Replaces or toggles with existing pie chart, doesn't add a new chart

- **Competitor reference**: **Public.com** has a revenue tree showing "how companies make money" with hierarchical breakdowns. **Koyfin** has revenue breakdowns with visual hierarchy. Both use treemap-style visualizations. **Stocksera** has "auto-generated visual reports" that include revenue structure. Our improvement: (1) plain-language labels and tooltips (Public.com/Koyfin are English-only), (2) customer-level breakdown (most competitors stop at segment level), (3) integration with existing glossary system (C33) for term explanations.

- **Data sourcing concern**: This is the **#1 risk** for C36. FinMind provides revenue breakdown by segment but NOT by customer. Customer-level data requires manual curation or annual report scraping. **Recommendation**: Start with segment-level treemap (FinMind data, available for all stocks). Add customer-level breakdown for top 20 stocks only (manual curation, ~4-6h of content work). This reduces the data risk significantly.

---

### Sprint 13b Design Direction

- **Priority recommendation**: **C46 Moat Analysis first, C36 Revenue Tree second** — but both can fit in Sprint 13b if C36 uses the segment-level-only approach (no customer-level breakdown in v1).

  **Rationale**:
  1. **C46 has higher strategic value**: No TW competitor has moat analysis. It's a unique differentiator that directly strengthens the "historian" positioning. C36 is beautiful but less unique (Public.com/Koyfin have similar features).
  2. **C46 has lower data risk**: Template-based quantitative scoring works for all stocks from day 1. C36 requires manual curation for customer-level data.
  3. **C46 has higher beginner impact**: "Does this company have a competitive advantage?" is a fundamental question beginners ask. "How does revenue break down?" is more analytical and appeals to intermediate users.
  4. **C36 is a strong complement**: Together, C36 + C46 form a "business understanding duo" — how the company makes money (C36) + why it's hard to compete with (C46). They tell a complete business story.

  **Effort estimate**: C46 (12-16h) + C36 segment-level only (8-10h) = 20-26h. This fits a standard Sprint.

- **Design specifications**:

  **C46 Moat Analysis — Design Spec**:
  ```
  Section: 🏰 護城河分析 (st.expander, expanded=False)
  ├── 5 dimension mini-cards (horizontal row):
  │   ├── 技術壁壘: [寬/窄/無] + plain-language explanation
  │   ├── 品牌價值: [寬/窄/無] + plain-language explanation
  │   ├── 成本優勢: [寬/窄/無] + plain-language explanation
  │   ├── 網路效應: [寬/窄/無] + plain-language explanation
  │   └── 轉換成本: [寬/窄/無] + plain-language explanation
  ├── 歷史證據 (2-3 bullets, plain-language)
  └── 整體評估: [寬護城河/窄護城河/無護城河] + 1-sentence summary
  ```
  - Colors: Green `#27AE60` (寬), Yellow `#F39C12` (窄), Red `#E74C3C` (無)
  - Card style: Use existing `_info_card()` pattern with colored left border
  - Text: ≤ 200 chars visible (5 cards × ~30 chars), evidence hidden in expander
  - Data: Template-based quantitative scoring for all stocks; manual curation for top 20

  **C36 Revenue Tree — Design Spec**:
  ```
  Section: 營收組成 (existing section, enhanced)
  ├── View toggle: [圓餅圖 ▎樹狀圖] (st.segmented_control)
  ├── Pie chart view: (existing, unchanged)
  └── Tree map view (NEW):
      ├── Level 1: Company (root)
      ├── Level 2: Business segments (max 8, from FinMind)
      ├── Level 3: Key customers (top 20 stocks only, manual curation)
      ├── Color: Blue palette (#3498DB family)
      ├── Hover: Segment name, revenue, %, plain-language description
      └── Fallback: st.info() for non-top-20 stocks
  ```
  - Chart height: 400px (treemap needs more vertical space than pie)
  - Max segments: 8 at Level 2 (group smaller ones into "其他")
  - Customer-level data: Manual curation for top 20 stocks (~4-6h content work)
  - Glossary integration: Technical terms in labels get tooltip from C33 glossary

- **Ten-second test compliance**:

  **C46 Moat Analysis**: ✅ **Passes** — A beginner sees 5 color-coded indicators and within 10 seconds can say "TSMC has wide moats in technology and cost, narrow in brand." The color coding is universally understood (green = good, yellow = okay, red = bad). The castle metaphor is intuitive.

  **C36 Revenue Tree**: ⚠️ **Conditionally passes** — A beginner sees the treemap and within 10 seconds can say "TSMC makes most money from 5nm chips." BUT only if: (1) segments are limited to 8 max, (2) labels are plain-language (not just "5nm" but "5nm晶片（最先進技術）"), (3) the toggle defaults to pie chart (familiar) with treemap as opt-in. **Recommendation**: Default to pie chart view; treemap is opt-in via toggle. This ensures beginners aren't confronted with an unfamiliar visualization on first visit.

- **Design system impact**:
  - **New components**: `_moat_dimension_card()` (5 mini-cards with color-coded border), `_revenue_tree_toggle()` (segmented control + treemap)
  - **No new colors needed**: Uses existing green/yellow/red for moat strength, existing blue palette for treemap
  - **No new typography**: Uses existing card styles and type scales
  - **Layout**: Both features are below-the-fold sections on the Business Card page — no impact on above-the-fold layout
  - **Text limit**: C46 uses expander to stay within 200-char limit. C36 treemap has minimal text (labels only, ~100 chars total)

- **Risks and mitigations**:

  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | C46: Template-based moat scoring is inaccurate for some stocks | P2 | Add disclaimer "量化估算" + manual curation for top 20 |
  | C36: FinMind revenue breakdown has limited segment detail for some stocks | P2 | Fallback to pie chart + st.info() note |
  | C36: Customer-level data requires manual curation (4-6h) | P3 | Segment-level treemap works for all stocks; customer-level is enhancement |
  | C46: 5 dimension cards may overlap on mobile | P2 | Use `st.columns(5)` with wrapping; on mobile, stack vertically |
  | Both: Business Card page getting too long | P2 | Both below fold in expanders; existing content already scrolls |

---

### Summary

**Sprint 13b should prioritize C46 Moat Analysis as the lead feature** with C36 Revenue Tree (segment-level only) as a complementary second feature. Together they form a "business understanding" duo that strengthens the "historian" positioning with zero overlap with existing features. Both pass the ten-second test (C46 directly, C36 conditionally with pie-chart-default toggle). Both use existing design system components and colors. Combined effort (20-26h) fits a standard Sprint. The unique TW-market differentiator (no competitor has either feature) justifies the investment.

---

*This design discussion was prepared by the Design Reviewer for the Sprint 13b planning cycle. All recommendations align with the PPT-style design system, the ten-second test principle, and the "historian, not stock picker" product positioning.*
