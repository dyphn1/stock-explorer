# Round 28 — QA Competitor Research Report

> **Date**: 2026-06-18
> **Author**: QA Engineer (Round 28)
> **Sprint Focus**: Sprint 13b — C36 Revenue Tree + C46 Moat Analysis
> **Prior Research**: 26 rounds (Rounds 1-26), 122 feature candidates (C01-C122)

---

## Competitor Feature Analysis (Sprint 13b Focus)

### Revenue Tree / Business Model Visualization

| Competitor | Approach | Our Gap |
|-----------|----------|---------|
| **Simply Wall St** | Sunburst chart: revenue by segment (inner ring) → sub-segment (outer ring). Color-coded by growth rate. Shows both revenue AND margin per segment. Includes "Revenue by geography" toggle for multi-region companies. | C36 only plans treemap/sunburst for segment breakdown. Missing: margin-per-segment layer, geography toggle, and growth-rate color coding. |
| **Public.com** | "How They Make Money" card: hierarchical revenue tree with plain-language explanations. Top-level: 3-5 revenue streams with % contribution. Each stream has a 1-sentence "what this means" explanation. Includes customer concentration callouts (e.g., "25% of revenue from Apple"). | C36 plans visual chart but Public.com proves beginners need narrative explanations attached to each segment. Customer concentration callouts are missing from C36 scope. |
| **Koyfin** | Segment-level revenue breakdown with geographic split. Interactive treemap with drill-down. Side-by-side comparison mode for comparing revenue trees of 2 companies. Includes "Revenue Quality" metric (recognition of recurring vs one-time revenue). | C36 plans single-company view. Missing: geographic dimension, side-by-side comparison mode, and revenue quality distinction. |
| **Seeking Alpha** | Segment revenue bar charts with YoY growth overlays. "Segment Analysis" tab with analyst commentary on each business unit's trajectory. | C36 plans static visualization. Missing: analyst-style narrative commentary on segment trajectory. |
| **Morningstar** | Revenue breakdown within "Business Overview" section: qualitative description of revenue drivers + segment pie chart. Emphasizes "what drives revenue growth" rather than just percentages. | C36 focuses on visual tree. Missing: qualitative "revenue driver narrative" that Morningstar provides. |

### Moat Analysis / Competitive Advantage

| Competitor | Approach | Our Gap |
|-----------|----------|---------|
| **Morningstar** | Iconic "Moat Rating": Wide / Narrow / None. Sub-classified by moat type: Network Effect, Cost Advantage, Switching Costs, Intangible Assets, Efficient Scale. Each type has a plain-language explanation + historical evidence. Updated quarterly. Moat Trend (Improving/Stable/Declining). | C46 plans moat analysis section but only for TW stocks (Morningstar doesn't cover TW). Gap: missing moat type classification (5 types), moat trend indicator, and the systematic review cadence. |
| **Stockopedia** | "Competitive Position" in StockReports: qualitative assessment of market position, brand strength, and barriers to entry. Integrated with StockRank (Quality factor includes moat proxies like ROE stability, margin consistency). Shows "competitive landscape" positioning vs sector peers. | C46 plans single-company moat view. Missing: peer competitive landscape comparison and quantitative moat proxies (margin stability, ROE consistency). |
| **Simply Wall St** | Visual risk analysis is the inverse of moat: shows "what could weaken the competitive advantage" visually. Risk breakdown includes competition risk, customer concentration risk, and regulatory risk. | C46 scope focuses on moat strengths. Missing: inverse risk analysis showing moat vulnerabilities (Simply Wall St's approach). |
| **Investopedia** | Educational articles on "Types of Economic Moats" — teaches users HOW to evaluate moat, not just showing a rating. "Moat Scorecard" template for DIY analysis. | C46 provides analyst-curated moat assessment. Missing: educational scaffolding that teaches users to evaluate moats themselves. |
| **TEJ (TW only)** | Industry analysis reports with market share data, competitive landscape mapping, and entry barrier assessment. Most detailed competitive data available for TW stocks but enterprise-only. | C46 has no access to TEJ-level market share data. Gap: quantitative competitive positioning (market share %, competitor count, entry barriers). |

---

## New Feature Gaps Identified

### [ISSUE-C123]: Revenue Geography Breakdown — Where Customers Are
- **Source**: Competitor research Round 28 (Koyfin geographic revenue split, Simply Wall St geography toggle)
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #1 "Story first, data second" + "Historian" positioning
- **Description**: Koyfin and Simply Wall St both show revenue by geography (e.g., "TSMC: 65% Americas, 15% China, 10% Europe, 10% Others"). C36 Revenue Tree plans segment breakdown but the geographic dimension is missing. Geography tells a critical story: "TSMC makes chips in Taiwan but 65% of its customers are American companies like Apple and NVIDIA." This is a natural extension of C36 that adds geopolitical context — highly relevant for TW stocks.
- **Implementation**: Add a "🗺️ 營收地區" toggle to the Revenue Tree page. Use FinMind revenue-by-region data (if available) or manual curation for top 20 stocks. Overlay with color-coded world map or horizontal stacked bar.
- **Competitive Gap**: 🟡 Koyfin has geographic revenue but no TW stocks. No TW competitor shows revenue geography with plain-language context. Combined with C36's segment tree, this would be world-class.

### [ISSUE-C124]: Moat Type Classification System
- **Source**: Competitor research Round 28 (Morningstar moat type taxonomy)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: Morningstar's moat analysis is not just "Wide/Narrow/None" — it classifies moat type: (1) Network Effect, (2) Cost Advantage, (3) Switching Costs, (4) Intangible Assets, (5) Efficient Scale. C46 Moat Analysis currently plans strength assessment but no type classification. Beginners need to understand NOT JUST "this company has a moat" BUT "this company's moat is [type] because [reason]." The type classification turns a rating into an educational moment.
- **Implementation**: Add moat type taxonomy to C46's "🏰 護城河分析" section. For each company, identify primary moat type from the 5 categories with a 2-sentence explanation: "🏰 護城河類型：技術領先（無形資產）。台積電擁有超過5萬項專利，競爭對手需要數年才能追趕。" Create a `moat_types.yaml` with type definitions and examples.
- **Competitive Gap**: 🔴 Morningstar has moat types for US stocks only. No TW competitor classifies moat types. This would be a unique educational feature that teaches beginners the 5 types of competitive advantage through real TW examples.

### [ISSUE-C125]: Segment-Level Profitability View
- **Source**: Competitor research Round 28 (Simply Wall St margin-per-segment, Koyfin segment earnings)
- **Priority**: P2
- **Effort**: 6-10h
- **Alignment**: Core value #5 "Benchmark-oriented analysis" + "Story first"
- **Description**: Simply Wall St shows not just revenue by segment but PROFIT MARGIN by segment. A revenue tree showing "Semiconductors (80%) + Real Estate (15%) + Other (5%)" is incomplete without showing "Semiconductors margin: 60%, Real Estate margin: 10%." This tells the REAL story: the small real estate segment contributes far less to actual profits. C36 Revenue Tree focuses on revenue breakdown only. Adding margin context transforms the tree from a "what they sell" chart to a "where the money actually comes from" chart.
- **Implementation**: Add margin overlay to C36's sunburst/treemap. Each segment slice shows both % of revenue AND segment margin %. Color coding: green for high-margin segments, yellow for medium, red for low. Plain-language summary: "晶圓代工佔營收78%，毛利率60% — 這是台積電真正的金雞母."
- **Competitive Gap**: 🟡 Simply Wall St has margin-per-segment but no TW stocks. No TW competitor shows segment-level profitability. This would significantly enhance C36's educational value.

### [ISSUE-C126]: Competitor Moat Comparison View
- **Source**: Competitor research Round 28 (Stockopedia competitive landscape positioning, Seeking Alpha side-by-side)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #5 "Benchmark-oriented analysis" + "Story first"
- **Description**: Stockopedia shows competitive positioning vs sector peers. Morningstar's moat rating is standalone — but Stockopedia shows "Company X has a WIDE moat vs competitors' NARROW moats in the same sector." C46 Moat Analysis provides single-company assessment. A "Moat Comparison" view would show: "TSMC: Wide moat (technology leadership). UMC: Narrow moat (cost efficiency). Samsung Foundry: No moat (behind in technology)." This transforms moat from a standalone feature into a benchmark-comparison feature, directly supporting Stock Explorer's #5 core value.
- **Implementation**: Add a "🏰 護城河比較" tab to the existing peer comparison page. Show moat strength + moat type for 3-5 peer companies side-by-side. Include plain-language explanation: "台積電的護城河比聯電寬，因為台積電在先進製程領先2年以上。"
- **Competitive Gap**: 🟡 Stockopedia shows competitive positioning for UK stocks. No TW competitor offers moat comparison. Combined with C46's single-company moat analysis, this would create the most comprehensive competitive advantage analysis for TW stocks.

---

## Regression Check

| Previous Feature Gap | Status | Notes |
|---------------------|--------|-------|
| **C42: Stock Screener** | 🟡 Partially addressed | 財報狗's #1 feature. Still a P1 gap — no screening capability exists. Not in Sprint 13b scope. Remains critical for discovery. |
| **C43: Snowflake Health Visualization** | 🟡 Partially addressed | C48 Story Card (Sprint 13a) provides a summary card but not a true multi-dimensional snowflake. Still relevant as P1. Not in Sprint 13b scope. |
| **C44: Risk Analysis Section** | ❌ Still relevant | Simply Wall St visual risk analysis is not built. C46 Moat Analysis focuses on strengths, not vulnerabilities. "What could go wrong" section still missing. |
| **C45: Valuation Band Chart** | ❌ Still relevant | 財報狗's P/E band chart is popular. Not in Sprint 13b scope. Still a P2 gap that beginners expect. |
| **C47: Education Academy** | ❌ Still relevant | Investopedia/Stockopedia academies prove demand. C33 Glossary (Sprint 13a) is infrastructure but not structured curriculum. Deferred to Sprint 14+. |
| **C119: Glossary-First Onboarding** | ❌ Still relevant | C33 Glossary is built (99 terms) but no onboarding flow teaches terms before data. Planting.tw/Groww model not yet implemented. P1 gap. |
| **C120: Story Card Export** | ❌ Still relevant | C48 Story Card is always visible (Sprint 13a) but no export/sharing capability. Viral distribution mechanism still missing. |
| **C121: Concept Progress Bar** | ❌ Still relevant | No progress tracking exists. Users browse without sense of accomplishment. Zerodha Varsity/Khan Academy model not implemented. |
| **C122: Beginner Confidence Score** | ❌ Still relevant | No adaptive content recommendation. All users see same complexity regardless of readiness. |
| **C37: Key Takeaways Summary** | 🟡 Partially addressed | C48 Story Card provides a summary but not structured "3-5 key takeaways" format from Seeking Alpha/Public.com. Partially covered by C48 but not fully. |
| **C39: What Changed Recently** | ❌ Still relevant | Koyfin's "Recent Changes" section not implemented. Beginners don't know what to look for in historical charts. |
| **C41: Read Next Recommendations** | ❌ Still relevant | No discovery mechanism. Users must know which stock to search for. Relationship-based recommendations (customer-supplier, parent-subsidiary) not built. |

---

## Summary

- **New competitors analyzed**: 0 (deepened analysis of existing competitors from Rounds 8-9)
- **Existing competitors re-analyzed for Sprint 13b**: Simply Wall St, Public.com, Koyfin, Morningstar, Stockopedia (5 competitors, deeper feature analysis)
- **New feature gaps identified**: 4 (C123, C124, C125, C126)
- **Cumulative feature candidates**: 126 (C01-C126)
- **Most impactful new gap**: **C124 (Moat Type Classification)** — It transforms C46 from a simple rating into an educational framework. Morningstar's 5-type taxonomy (network effect, cost advantage, switching costs, intangible assets, efficient scale) is the global gold standard, and no TW competitor has it. Paired with C46 (which has the historian-evidential approach), this creates the definitive moat analysis for TW stocks.
- **Sprint 13b competitive position**: C36 Revenue Tree and C46 Moat Analysis are both well-validated by international competitors. C36 fills a gap that Koyfin and Simply Wall St prove is valued for global stocks. C46 fills a gap that Morningstar proves is iconic for US stocks — with the added differentiator of TW stock focus and historian-style evidence. The 4 new gaps (C123-C126) are natural extensions that should be considered for Sprint 14+ if C36/C46 succeed.
- **Regression health**: 10 of 12 previously-identified gaps remain fully relevant. C43 and C37 are partially addressed by C48 Story Card. No gaps were fully resolved. The Sprint 13a (C33 + C48) delivery was high-value but narrow — the backlog of education and discovery features continues to grow while the competitor landscape advances.
- **Strategic note**: Simply Wall St has added "Revenue by geography" for TW-listed stocks (e.g., 2330.TW). This opens a direct competitive vector for C124. Morningstar has not added moat ratings for individual TW stocks — C46 remains a white space opportunity. The window for differentiation in TW moat analysis is still open.
