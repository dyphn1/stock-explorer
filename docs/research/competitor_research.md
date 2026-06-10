# Stock Explorer Competitor Research Report — Round 7

> **Date**: 2026-06-12
> **Author**: PM (coordinating QA research)
> **Purpose**: Update competitor analysis with latest findings and identify new feature gaps

---

## Competitor Overview Table

| Dimension | StatementDog | GoodInfo | CMoney | WantGoo | **Stock Explorer** |
|-----------|-------------|----------|--------|---------|-------------------|
| **Positioning** | Financial Analysis Expert | All-in-One TW Stock Portal | Investment Decision Platform | Stock Community + Data | Beginner Education ("Historian") |
| **Target Users** | Mid-Career Investors | All Investors | Heavy Investors | Mid/Short-Term Traders | **Beginner Investors** |
| **UI Style** | Data-Dense Tables | Traditional Portal | App Style | Forum + Minimal | **PPT Style** |
| **Plain-Language** | Partial | None | Yes (Key Summaries) | None | **Core Feature** |
| **Event Detection** | ⚠️ Fundamental Alerts | ⚠️ Price Alerts | ✅ Full Alerts | ⚠️ Sporadic News | ✅ Adaptive Engine (M5) |
| **Peer Comparison** | ✅ Complete | ⚠️ Basic | ✅ Complete | ❌ | ✅ Benchmark-Oriented |
| **Group Structure** | ⚠️ Simplified | ❌ | ⚠️ Partial | ❌ | ✅ Point-to-Point |
| **Mobile** | ✅ RWD | ✅ RWD | ✅ Native App | ✅ RWD + App | ⚠️ Streamlit Limitations |
| **Educational** | ⚠️ Medium | ❌ Low | ⚠️ Medium | ❌ Low | **Core: Education-Oriented** |
| **Notifications** | ✅ Line Notify | ✅ Email | ✅ App Push | ❌ | ❌ **MISSING** |
| **PPT/Report Export** | ❌ | ❌ | ❌ | ✅ One-click | ❌ **MISSING** |
| **Health Score** | ✅ Reverse DCF | ❌ | ✅ AI Score | ❌ | ❌ **MISSING** |
| **Glossary/Tooltips** | ❌ | ❌ | ⚠️ Basic | ❌ | ❌ **MISSING** |
| **Learning Path** | ❌ | ❌ | ⚠️ Courses | ❌ | ❌ **MISSING** |

---

## Feature Gap Analysis

### Gaps That Competitors Have (We Don't)

| Feature | Competitors | Our Status | Priority | Alignment |
|---------|-------------|------------|----------|-----------|
| **Notifications** | StatementDog (Line), CMoney (Push), GoodInfo (Email) | ❌ Not built | P0 | M5 event detection is wasted without notifications |
| **Health Score** | Simply Wall St (snowflake), Stockopedia (rank) | ❌ Not built | P1 | Aligns with "benchmark-oriented" value |
| **Glossary/Tooltips** | Investopedia (10K+ terms) | ❌ Not built | P2 | Aligns with "beginner-friendly" positioning |
| **PPT Export** | WantGoo (one-click report) | ❌ Not built | P1 | Leverages our unique PPT-style CSS |
| **Learning Path** | CMoney (courses), Investopedia Academy | ❌ Not built | P2 | Aligns with "Story first" value |
| **Market Thermometer** | WantGoo, CMoney | ❌ Not built | P1 | Beginner-friendly market overview |
| **Company Timeline Narrative** | None (unique opportunity) | ❌ Not built | P2 | Perfect "historian" differentiator |

### Features We Have (Competitors Don't)

| Feature | Our Implementation | Competitive Advantage |
|---------|-------------------|----------------------|
| **Plain-language explanations** | Core feature, all metrics have analogies | Unique in TW market |
| **PPT-style presentation** | Custom CSS, one key point per page | Unique design approach |
| **Point-to-point group structure** | Parent-subsidiary mapping with ownership % | More detailed than competitors |
| **Adaptive event detection** | M5 engine with false positive filtering | More sophisticated than competitors |
| **Ex-dividend countdown** | Real-time countdown + badge | GoodInfo has data but no countdown |
| **"Did You Know?" facts** | 70 facts for 7 stocks, rotating tips | No competitor has contextual facts |
| **Benchmark-oriented comparison** | Always compare to industry #1 | Most competitors compare to average |

---

## New Feature Suggestions

### [ISSUE-C33] Beginner Glossary / Term Tooltip System
- **Source**: Competitor research (Investopedia 10K+ term glossary)
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: The design system requires "All professional terms must have plain-language translations" but there's no systematic glossary. Beginners encounter terms like "ROE," "P/B ratio," "institutional investors" with no inline help.
- **Implementation**: Create `src/data/glossary.yaml` with term → plain-language definition. Add hover tooltips or click-to-expand definitions on all financial terms across all pages.
- **Competitive Gap**: 🟡 No TW competitor has systematic glossary tooltips

### [ISSUE-C34] Company Story Timeline (Narrative Thread)
- **Source**: Challenger review (Round 1) + competitor gap analysis
- **Priority**: P2
- **Effort**: 16-24h
- **Alignment**: Core value #1 "Story first, data second" + "Historian" positioning
- **Description**: The event dashboard is a disconnected list. What's missing is a narrative timeline — "Here's what happened to TSMC in the last 3 years, told as a story." The team has all the data (events, revenue, price) but no narrative thread connecting them. This is the #1 thing competitors DON'T have.
- **Implementation**: Add a "Story" tab to each company page that weaves events, revenue milestones, and price movements into a chronological narrative with plain-language explanations.
- **Competitive Gap**: 🔴 No competitor has narrative timeline — unique differentiator

### [ISSUE-C35] Market Mood Index
- **Source**: Competitor research (WantGoo market temperature, CMoney sentiment)
- **Priority**: P1 (conditional on data validation)
- **Effort**: 10-12h
- **Alignment**: Core value #3 "Adaptive and self-evolving" + beginner-friendly
- **Description**: Beginners want to know "Is the market hot or cold right now?" A simple market mood index on the homepage using institutional buy/sell surplus + trading volume + advance/decline ratio.
- **Data Feasibility**: FinMind has `TaiwanStockInstitutionalInvestorsBuySell` — validated
- **Competitive Gap**: 🟡 WantGoo has temperature but not explainable mood index

---

## Recommendations

### Immediate (Next Sprint)
1. **C02 Notifications** — P0 gap, all competitors have it, M5 engine is wasted without it
2. **C06 PPT Export** — Leverages unique PPT-style CSS, WantGoo proves demand

### Short-Term (Sprint 2-3)
3. **C34 Company Story Timeline** — Unique differentiator, no competitor has it
4. **C07 Custom Event Thresholds** — Unlocks C02, already approved
5. **C35 Market Mood** — Conditional on data validation

### Medium-Term (Post-Sprint 2)
6. **C33 Glossary** — Systematic educational infrastructure
7. **C14 Health Score** — Depends on Daniel's scope decision

---

*This is the seventh competitor research round. Three new feature suggestions identified. The most impactful gap remains notifications (C02) — all competitors have it and our M5 engine is built for it.*

---

# Stock Explorer Competitor Research Report — Round 8

> **Date**: 2026-06-13
> **Author**: QA Engineer (Round 8)
> **Purpose**: Identify new competitors and feature gaps not covered in Rounds 1-7

---

## New Competitors Analyzed (Not in Rounds 1-7)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **Public.com** | Social investing + story cards | US | 🔴 High — story cards overlap with PPT-style positioning |
| **Seeking Alpha** | Crowdsourced analysis + Quant Rating | US/Global | 🟡 Medium — "Story" focus + "Smart Comment" summaries |
| **Koyfin** | Modern financial data + plain-language | US/Global | 🟡 Medium — metric descriptions + dashboard narratives |
| **Finary** | Portfolio tracking + education | EU | 🟡 Medium — "Learn" section with bite-sized lessons |
| **Sharesies** | Micro-investing + heavy education | NZ | 🟡 Medium — "Discover" section with company stories |
| **Stocksera** | AI-powered stock analysis + narrative | US | 🔴 High — "Story" tab per stock + narrative summaries |
| **The Motley Fool** | Long-form narrative stock analysis | US | 🟡 Medium — "Bull vs Bear" debates + storytelling |
| **NerdWallet** | Comparison + education model | US | 🟢 Low — "How it works" explainers for every concept |

---

## New Feature Ideas from Round 8

### [ISSUE-C36] "How This Company Makes Money" Visual Revenue Tree
- **Source**: Competitor research round 8 (Public.com revenue tree, Koyfin revenue breakdown)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #1 "Story first, data second" + Core value #2 "PPT-style presentation"
- **Description**: Stock Explorer currently shows a revenue pie chart (what percentage each segment contributes). What's missing is a visual revenue tree that shows HOW money flows through the business — e.g., "TSMC → 5nm chips (40%) → Apple (25%), NVIDIA (15%), AMD (10%)". Public.com and Koyfin both have hierarchical revenue breakdowns that help beginners understand the business model visually. This is a natural extension of our existing pie chart that aligns with the "historian" positioning — explaining how the company works, not whether to buy it.
- **Implementation**: Extend `create_revenue_pie_chart()` in `chart.py` with a hierarchical treemap or sunburst chart. Add a "Revenue Tree" tab next to the pie chart on the business card page. Data source: FinMind revenue breakdown + manual curation for top 20 stocks.
- **Competitive Gap**: 🟡 No TW competitor has visual revenue tree; Public.com/Koyfin prove demand internationally

---

### [ISSUE-C37] "Key Takeaways" Summary Card
- **Source**: Competitor research round 8 (Seeking Alpha "Key Takeaways", Public.com "Quick Summary")
- **Priority**: P2
- **Effort**: 6-8h
- **Alignment**: Core value #1 "Story first, data second" + "Ten-second test"
- **Description**: Seeking Alpha and Public.com both have a "Key Takeaways" or "Quick Summary" card at the top of each stock page — 3-5 bullet points that synthesize the most important information. Stock Explorer's business card page has metrics scattered across sections but no synthesized summary. A beginner opening TSMC's page sees 15+ metrics but doesn't know which 3 matter most. This directly violates the "ten-second test" — a beginner should be able to restate the core concept within 10 seconds.
- **Implementation**: Add a "📋 重點摘要" card at the top of the business card page with 3-5 auto-generated key takeaways. Use existing analogy_engine.py patterns to generate plain-language summaries. Example: "① 台積電是全球90%先進晶片的製造商 ② 毛利率55%代表每賣100元賺55元 ③ 過去3年營收穩定成長，但資本支出很高"
- **Competitive Gap**: 🟡 No TW competitor has auto-generated key takeaways; aligns with "ten-second test" design principle

---

### [ISSUE-C38] "Compare Stories" Side-by-Side Narrative Mode
- **Source**: Competitor research round 8 (Stocksera "Compare Stories", Seeking Alpha side-by-side)
- **Priority**: P2
- **Effort**: 12-16h
- **Alignment**: Core value #5 "Benchmark-oriented analysis" + Core value #1 "Story first"
- **Description**: Stocksera and Seeking Alpha allow comparing two companies' narratives side-by-side. Stock Explorer has peer comparison (metrics comparison) but no narrative comparison — "How is TSMC's story different from UMC's story?" This is a natural extension of the peer comparison page that adds a narrative layer to the existing metric comparison. Perfect for the "historian" positioning: instead of "which stock is better?", the question becomes "how are these companies' stories different?"
- **Implementation**: Add a "故事比較" tab to the existing peer comparison page. Show two companies' key events, revenue milestones, and business models side-by-side with plain-language narrative. Reuse existing event data and analogy engine.
- **Competitive Gap**: 🟡 No TW competitor has narrative comparison; extends existing peer comparison advantage

---

### [ISSUE-C39] "What Changed Recently" Delta Card
- **Source**: Competitor research round 8 (Koyfin "Recent Changes", Finary "What's New")
- **Priority**: P2
- **Effort**: 8-10h
- **Alignment**: Core value #3 "Adaptive and self-evolving" + Core value #1 "Story first"
- **Description**: Koyfin and Finary both highlight what changed recently — metrics that moved significantly compared to the previous period. Stock Explorer shows historical data in charts but doesn't explicitly highlight recent changes. Beginners don't know what to look for in a 3-year revenue chart. A "What Changed Recently" card would say: "📈 最近3個月營收成長15%，是過去一年最快的增速" or "📉 毛利率從55%下降到52%，因為晶片價格競爭加劇". This makes the data feel alive and relevant.
- **Implementation**: Add a "🔄 最近有什麼變化" card to the business card page. Compare current metrics (last 30 days) vs previous period (30-60 days ago). Highlight significant changes (>10%) with plain-language explanations. Reuse existing data pipeline.
- **Competitive Gap**: 🟡 No TW competitor highlights recent changes with plain-language explanations

---

### [ISSUE-C40] "Beginner Mode" / "Expert Mode" Complexity Toggle
- **Source**: Competitor research round 8 (Sharesies complexity levels, NerdWallet "Simple View")
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: Sharesies and NerdWallet both have complexity toggles — a "simple view" that hides advanced metrics and shows only the essentials, and an "advanced view" that shows everything. Stock Explorer currently shows all metrics to all users, which can overwhelm absolute beginners. A "Beginner Mode" would show only: one-liner, revenue pie, key metrics (3-4), and "Did You Know?" facts. "Expert Mode" would show everything. This aligns with the "progressive drill-down" principle in the product vision.
- **Implementation**: Add a session_state toggle ("🌱 新手模式" / "🔬 進階模式") in the navbar. In Beginner Mode, hide advanced sections (institutional investor charts, detailed financial ratios, debt analysis). Show only the 3-4 most important metrics per section. In Expert Mode, show everything (current behavior).
- **Competitive Gap**: 🟢 No TW competitor has complexity toggle; aligns with "progressive drill-down" design principle

---

### [ISSUE-C41] "Read Next" Company Recommendation Engine
- **Source**: Competitor research round 8 (The Motley Fool "Related Stocks", Seeking Alpha "You May Also Like")
- **Priority**: P2
- **Effort**: 6-8h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + beginner-friendly discovery
- **Description**: The Motley Fool and Seeking Alpha both suggest related companies to research after viewing a stock. Stock Explorer has no discovery mechanism — users must know which stock to search for. A "Read Next" section would say: "After learning about TSMC, you might want to understand its biggest customer: Apple (AAPL)" or "TSMC's main competitor: 聯華電子 (UMC)". This creates a learning path that connects companies through business relationships, not just industry categories.
- **Implementation**: Add a "📖 接著看" section to the business card page with 2-3 recommended companies. Recommendations based on: (1) same industry (industry #2 player), (2) parent-subsidiary relationships (group structure data), (3) customer-supplier relationships (manual curation for top 20 stocks). Reuse existing group_structure.py data.
- **Competitive Gap**: 🟡 No TW competitor has relationship-based recommendations; extends existing group structure advantage

---

## Updated Competitor Overview Table (Round 8 Additions)

| Dimension | Public.com | Seeking Alpha | Koyfin | Stocksera | **Stock Explorer** |
|---|---|---|---|---|---|
| **Positioning** | Social Investing | Crowdsourced Analysis | Modern Financial Data | AI Stock Narratives | Beginner Education ("Historian") |
| **Story Cards** | ✅ Built-in | ✅ "Story" focus | ⚠️ Dashboard narratives | ✅ "Story" tab | ⚠️ PPT-style (no story tab) |
| **Key Takeaways** | ✅ Quick Summary | ✅ Key Takeaways | ⚠️ Auto-generated | ⚠️ AI summary | ❌ MISSING |
| **Revenue Tree** | ✅ Hierarchical | ⚠️ Basic | ✅ Visual breakdown | ❌ | ⚠️ Pie chart only |
| **Compare Stories** | ❌ | ✅ Side-by-side | ❌ | ✅ Compare mode | ❌ MISSING |
| **Recent Changes** | ❌ | ⚠️ Price alerts | ✅ Highlighted | ❌ | ❌ MISSING |
| **Complexity Toggle** | ❌ | ❌ | ❌ | ❌ | ❌ MISSING |
| **Recommendations** | ⚠️ Social | ✅ "You May Also Like" | ❌ | ❌ | ❌ MISSING |

---

## Summary

### New Competitors Researched: 8
(Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, The Motley Fool, NerdWallet)

### New Feature Gaps Identified: 6

| ID | Title | Priority | Alignment |
|---|---|---|---|
| C36 | Visual Revenue Tree | P2 | Story first + PPT-style |
| C37 | Key Takeaways Summary Card | P2 | Story first + Ten-second test |
| C38 | Compare Stories Side-by-Side | P2 | Benchmark-oriented + Story first |
| C39 | What Changed Recently Delta Card | P2 | Adaptive + Story first |
| C40 | Beginner/Expert Mode Toggle | P2 | Point-to-point + Ten-second test |
| C41 | Read Next Recommendations | P2 | Point-to-point + Discovery |

### Key Insights
1. **Narrative features are becoming table stakes** — Stocksera, Public.com, and Seeking Alpha all have story/narrative features. Stock Explorer's "historian" positioning is validated but needs execution (C34 Story Timeline is critical).
2. **Synthesis > Data** — The trend is toward synthesizing data into key takeaways, not just displaying metrics. Stock Explorer's analogy engine is a strong foundation but needs a synthesis layer.
3. **Progressive disclosure is standard** — Complexity toggles and beginner modes are common in international platforms. Stock Explorer's "progressive drill-down" principle needs explicit UI support.
4. **Relationship-based discovery is a white space** — No competitor connects companies through business relationships (customer-supplier, parent-subsidiary). Stock Explorer's group structure data is a unique asset.

---

*This is the eighth competitor research round. Six new feature suggestions identified. The most impactful new gap is C37 (Key Takeaways) — it directly addresses the "ten-second test" design principle and has the highest ROI (6-8h effort for core value alignment).*
