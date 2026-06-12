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

---

# Stock Explorer Competitor Research Report — Round 9

> **Date**: 2026-06-14
> **Author**: QA Engineer (Round 9)
> **Purpose**: Research new competitors not covered in Rounds 1-8, focusing on Taiwanese platforms and international analysis/education tools

---

## New Competitors Analyzed (Not in Rounds 1-8)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **財報狗 (StatementDog/Cat Dog Finance)** | Financial analysis + screening | TW | 🔴 High — most popular TW fundamental analysis tool; screening overlaps with our discovery |
| **JZ Invest (JZ投資)** | All-in-one investment platform | TW | 🟡 Medium — community + data + screening in one platform |
| **鉅亨網 (CnYES)** | Financial portal + news + data | TW | 🟡 Medium — comprehensive TW market data + international |
| **TEJ (Taiwan Economic Journal)** | Professional financial database | TW | 🟢 Low — enterprise-grade; different target user but interesting features |
| **Yahoo奇摩股市 (Yahoo Finance Taiwan)** | Free financial portal | TW | 🟡 Medium — most visited TW stock site; sets baseline expectations |
| **Simply Wall St** | Visual stock analysis + snowflake | AU/Global | 🔴 High — visual-first approach aligns with our PPT-style positioning |
| **Stockopedia** | Stock analysis + ranking + education | UK/Global | 🟡 Medium — "StockRank" system + educational content |
| **Investopedia** | Financial education + tools | US/Global | 🟡 Medium — the gold standard for financial education; glossary + simulator |
| **Morningstar** | Investment research + rating | US/Global | 🟡 Medium — "Morningstar Rating" (star system) + fair value analysis |

---

## Detailed Competitor Profiles

### 1. 財報狗 (StatementDog / Cat Dog Finance)

**URL**: https://statementdog.com
**Positioning**: "讓投資變簡單" (Make investing simple) — fundamental analysis made accessible
**Target Users**: TW retail investors who want to do fundamental analysis without being accountants

**Key Features**:
- **Stock Screener (選股工具)**: Multi-condition screening on 100+ financial metrics (P/E, ROE, dividend yield, revenue growth, etc.) — users can filter stocks by custom criteria
- **Financial Statement Visualization**: Clean charts for revenue, EPS, margins over 10+ years
- **Dividend Analysis**: Complete dividend history with payout ratio analysis
- **Valuation Tools**: DCF calculator, P/E/PB band charts showing historical valuation ranges
- **Portfolio Tracking**: Users can create watchlists and track holdings
- **Mobile App**: Native iOS/Android apps with full feature parity

**UX/Design Approach**:
- Clean, modern web interface with card-based layout
- Heavy use of charts and minimal text
- Color-coded indicators (green/red for positive/negative trends)
- Mobile-first responsive design

**Unique Capabilities**:
- **Stock Screener** is the #1 feature — allows beginners to discover stocks meeting specific criteria without knowing financial analysis deeply
- **P/E Band Chart**: Shows current P/E vs historical range — helps beginners understand "expensive vs cheap" visually
- **Dividend Score**: Proprietary scoring system for dividend sustainability

**Comparison with Stock Explorer**:
| Feature | 財報狗 | Stock Explorer |
|---|---|---|
| Stock Screener | ✅ Advanced multi-condition | ❌ Not built |
| P/E Band Chart | ✅ Historical valuation | ❌ Not built |
| Dividend Score | ✅ Proprietary | ⚠️ Basic countdown |
| Plain-language | ⚠️ Partial (some tooltips) | ✅ Core feature |
| PPT-style | ❌ | ✅ Unique |
| Education | ⚠️ Blog posts | ✅ Core positioning |
| Mobile App | ✅ Native | ❌ Streamlit only |

---

### 2. JZ Invest (JZ投資)

**URL**: https://jzinvest.com
**Positioning**: All-in-one investment community + data platform
**Target Users**: Active TW retail investors who want community discussion + data in one place

**Key Features**:
- **Community Forum**: Stock-specific discussion boards with real-time chat
- **Screening Tools**: Similar to 財報狗 but with community-driven screening presets
- **Portfolio Sharing**: Users can share their portfolios publicly for discussion
- **News Aggregation**: Curated financial news with community commentary
- **Technical + Fundamental**: Both charting tools and financial data

**UX/Design Approach**:
- Forum-style layout (similar to PTT/RED)
- Data panels alongside community discussion
- Real-time updates for price and volume

**Unique Capabilities**:
- **Community-driven screening**: Users share their screening strategies as presets
- **Portfolio transparency**: See what other investors hold and their reasoning

**Comparison with Stock Explorer**:
| Feature | JZ Invest | Stock Explorer |
|---|---|---|
| Community | ✅ Forum + chat | ❌ Not built |
| Screening | ✅ Community presets | ❌ Not built |
| Portfolio Sharing | ✅ Public portfolios | ❌ Not built |
| Plain-language | ❌ | ✅ Core feature |
| Education | ❌ | ✅ Core positioning |

---

### 3. 鉅亨網 (CnYES)

**URL**: https://www.cnyes.com
**Positioning**: Comprehensive financial portal — news, data, analysis, international markets
**Target Users**: TW investors who want everything in one portal (news + data + international)

**Key Features**:
- **Real-time Market Data**: TW stocks, international indices, forex, commodities
- **News Center**: Aggregated financial news with editorial content
- **Fund Analysis**: Mutual fund ratings and performance tracking
- **International Markets**: US stocks, Asian markets, global economic indicators
- **Expert Columns**: Professional analysts' opinions and market outlook
- **Screening**: Basic stock screening for TW market

**UX/Design Approach**:
- Traditional financial portal layout (dense information)
- Tab-based navigation for different asset classes
- Heavy advertising (free model)

**Unique Capabilities**:
- **International coverage**: One of few TW platforms with comprehensive global market data
- **Fund analysis**: Strong mutual fund section (Stock Explorer has ETF section but not mutual funds)
- **Real-time news**: Integrated news feed with market data

**Comparison with Stock Explorer**:
| Feature | 鉅亨網 | Stock Explorer |
|---|---|---|
| International | ✅ Global markets | ⚠️ TW only |
| News | ✅ Real-time feed | ❌ Not built |
| Fund Analysis | ✅ Mutual funds | ⚠️ ETF only |
| Plain-language | ❌ | ✅ Core feature |
| Education | ⚠️ Expert columns | ✅ Core positioning |

---

### 4. TEJ (Taiwan Economic Journal)

**URL**: https://www.eol.com.tw (TEJ database)
**Positioning**: Professional-grade financial database for institutions and serious investors
**Target Users**: Institutional investors, fund managers, academic researchers, serious retail investors

**Key Features**:
- **Comprehensive Database**: 20+ years of TW financial data, including many data points not available elsewhere
- **ESG Data**: ESG ratings and sustainability metrics for TW companies
- **Credit Risk Analysis**: Bond ratings, default probability models
- **Industry Analysis**: Detailed industry reports with market share data
- **API Access**: Programmatic data access for quantitative analysis
- **Custom Reports**: Users can generate custom analytical reports

**UX/Design Approach**:
- Enterprise software interface (functional, not beautiful)
- Query-based data extraction
- Export to Excel/CSV for further analysis

**Unique Capabilities**:
- **ESG data**: Comprehensive ESG metrics for TW companies — not available on any free platform
- **Credit risk**: Bond and credit analysis tools
- **Data depth**: Goes far beyond what FinMind provides (insider trading details, shareholder structure changes)

**Comparison with Stock Explorer**:
| Feature | TEJ | Stock Explorer |
|---|---|---|
| ESG Data | ✅ Comprehensive | ❌ Not built |
| Credit Risk | ✅ Bond analysis | ❌ Not built |
| Data Depth | ✅ Institutional-grade | ⚠️ FinMind (retail-grade) |
| Plain-language | ❌ | ✅ Core feature |
| Education | ❌ | ✅ Core positioning |
| Price | 💰💰💰 Enterprise | Free |

---

### 5. Yahoo奇摩股市 (Yahoo Finance Taiwan)

**URL**: https://tw.stock.yahoo.com
**Positioning**: Free, accessible stock information for everyone
**Target Users**: Casual investors, beginners, general public checking stock prices

**Key Features**:
- **Real-time Quotes**: Free real-time price data for TW stocks
- **Basic Charts**: Simple price/volume charts with basic technical indicators
- **News**: Aggregated financial news
- **Portfolio Tracking**: Basic watchlist and portfolio feature
- **Community**: Comment sections on individual stock pages
- **Mobile App**: Highly popular mobile app with push notifications

**UX/Design Approach**:
- Simple, familiar portal design
- Ad-supported (heavy advertising)
- Mobile app is the primary use case
- Minimal learning curve

**Unique Capabilities**:
- **Push notifications**: Price alerts, news alerts via mobile app
- **Most visited**: Sets the baseline UX expectation for TW stock tools
- **Zero barrier**: No registration required for basic features

**Comparison with Stock Explorer**:
| Feature | Yahoo奇摩股市 | Stock Explorer |
|---|---|---|
| Push Notifications | ✅ Mobile app | ❌ Not built |
| Real-time Data | ✅ Free real-time | ⚠️ FinMind (delayed) |
| Community | ✅ Comments | ❌ Not built |
| Plain-language | ❌ | ✅ Core feature |
| Education | ❌ | ✅ Core positioning |
| Mobile App | ✅ Native | ❌ Streamlit only |

---

### 6. Simply Wall St

**URL**: https://simplywall.st
**Positioning**: "Make complex investing simple" — visual-first stock analysis
**Target Users**: Retail investors globally who want to understand stocks through visuals, not spreadsheets

**Key Features**:
- **Snowflake Analysis**: Proprietary visual "snowflake" diagram showing 5 dimensions of a company (value, future, past performance, financial health, dividends) with color-coded scores
- **Visual Story**: Each stock has a visual "story" page with infographic-style layout
- **Future Growth Estimates**: Analyst estimates presented visually with confidence intervals
- **Risk Analysis**: Visual risk breakdown showing what could go wrong
- **Portfolio Visualization**: Visual portfolio analysis showing diversification, risk concentration
- **Snowflake Score**: Composite score from 0-5 based on 5 dimensions

**UX/Design Approach**:
- **Visual-first**: Every metric is presented as a chart, diagram, or infographic
- **Infographic style**: Similar to our PPT-style approach — one key visual per concept
- **Color coding**: Green/yellow/red for good/neutral/bad
- **Minimal text**: Short descriptions, no walls of text
- **Progressive disclosure**: Summary first, details on click

**Unique Capabilities**:
- **Snowflake diagram**: Unique visual framework that gives a 30-second company overview — directly comparable to our "ten-second test"
- **Visual risk analysis**: Shows risks as visual breakdowns, not just numbers
- **Infographic reports**: Each stock page reads like an infographic, not a financial report

**Comparison with Stock Explorer**:
| Feature | Simply Wall St | Stock Explorer |
|---|---|---|
| Snowflake Analysis | ✅ Proprietary visual | ❌ Not built |
| Visual Story | ✅ Infographic style | ⚠️ PPT-style (similar) |
| Risk Visualization | ✅ Visual breakdown | ❌ Not built |
| Plain-language | ⚠️ Short descriptions | ✅ Core feature |
| Education | ⚠️ Visual learning | ✅ Core positioning |
| TW Market | ❌ US/AU focus | ✅ TW focus |

---

### 7. Stockopedia

**URL**: https://www.stockopedia.com
**Positioning**: "Stock analysis and screening for smart investors" — data-driven stock education
**Target Users**: UK/EU retail investors who want to combine screening with education

**Key Features**:
- **StockRank**: Proprietary composite score (0-100) combining value, quality, and momentum
- **StockReport**: Detailed analysis report for each stock with scores and commentary
- **Screening**: Advanced multi-factor screening with StockRank integration
- **Education Center**: "Stockopedia Academy" with structured courses on investing concepts
- **Financial Data**: 20+ years of financial data with visualizations
- **Community**: User-contributed analysis and discussions

**UX/Design Approach**:
- Clean, modern interface with score-centric design
- StockRank is the central organizing concept
- Educational content integrated into stock pages
- Progressive complexity (simple scores → detailed analysis)

**Unique Capabilities**:
- **StockRank system**: Single composite score that combines multiple factors — makes stock evaluation accessible to beginners
- **Stockopedia Academy**: Structured learning paths from beginner to advanced
- **Quality + Value + Momentum**: Three-factor framework that educates users about different investment approaches

**Comparison with Stock Explorer**:
| Feature | Stockopedia | Stock Explorer |
|---|---|---|
| StockRank Score | ✅ Composite 0-100 | ❌ Not built |
| StockReport | ✅ Detailed reports | ⚠️ Business card page |
| Education Academy | ✅ Structured courses | ⚠️ Did You Know facts |
| Screening | ✅ Advanced | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ❌ UK/EU focus | ✅ TW focus |

---

### 8. Investopedia

**URL**: https://www.investopedia.com
**Positioning**: "The world's leading financial education platform" — learn before you invest
**Target Users**: Beginners to intermediate investors globally who want to learn financial concepts

**Key Features**:
- **Financial Dictionary**: 10,000+ terms with detailed plain-language definitions
- **Investopedia Academy**: Paid courses on investing, trading, and personal finance
- **Stock Simulator**: Virtual trading platform with $100,000 in fake money
- **Analysis & News**: Market analysis, stock commentary, and educational articles
- **Reviews**: Broker reviews, tool reviews, and comparison guides
- **Calculators**: 50+ financial calculators (compound interest, retirement, etc.)

**UX/Design Approach**:
- Encyclopedia-style organization (search → learn)
- Article-based content with embedded definitions
- Simulator has its own interface separate from education
- Ad-supported free model with premium courses

**Unique Capabilities**:
- **Financial Dictionary**: The gold standard — every term has a detailed, beginner-friendly definition with examples
- **Stock Simulator**: Allows beginners to practice without risk — unique among competitors
- **Academy**: Structured courses from absolute beginner to advanced topics
- **Concept-first approach**: Teaches concepts before showing data — aligns with our "education-first" positioning

**Comparison with Stock Explorer**:
| Feature | Investopedia | Stock Explorer |
|---|---|---|
| Financial Dictionary | ✅ 10K+ terms | ❌ Not built |
| Stock Simulator | ✅ Virtual trading | ❌ Not built |
| Academy | ✅ Structured courses | ⚠️ Did You Know facts |
| Analysis | ✅ Expert analysis | ✅ Plain-language analysis |
| TW Market | ❌ US focus | ✅ TW focus |
| Plain-language | ✅ Core feature | ✅ Core feature |

---

### 9. Morningstar

**URL**: https://www.morningstar.com
**Positioning**: "Independent investment research you can trust" — professional-grade analysis for everyone
**Target Users**: Serious retail investors, financial advisors, institutional investors

**Key Features**:
- **Morningstar Rating (Star Rating)**: 1-5 star rating system based on risk-adjusted returns
- **Fair Value Estimate**: Proprietary intrinsic value calculation with uncertainty rating
- **Moat Rating**: Economic moat assessment (wide, narrow, none) — how durable is the competitive advantage
- **Sustainability Rating**: ESG risk rating for companies
- **Portfolio Analysis**: X-ray tool showing portfolio overlap, sector allocation, style box
- **Fund Analysis**: Comprehensive mutual fund and ETF analysis (their heritage)

**UX/Design Approach**:
- Professional, data-dense interface
- Star rating is the most prominent element on every stock page
- Fair value vs current price is the key visual
- Premium content behind paywall

**Unique Capabilities**:
- **Moat Rating**: Unique framework for assessing competitive advantage durability — "Does this company have a castle with a moat?"
- **Fair Value with Uncertainty**: Not just a number, but a range — teaches beginners that valuation is uncertain
- **Star Rating**: Simple, memorable rating system that beginners can understand instantly
- **Sustainability/ESG**: Integrated ESG analysis alongside financial analysis

**Comparison with Stock Explorer**:
| Feature | Morningstar | Stock Explorer |
|---|---|---|
| Star Rating | ✅ 1-5 stars | ❌ Not built |
| Fair Value | ✅ With uncertainty | ❌ Not built |
| Moat Rating | ✅ Competitive advantage | ❌ Not built |
| ESG Rating | ✅ Sustainability | ❌ Not built |
| Plain-language | ⚠️ Professional tone | ✅ Core feature |
| TW Market | ⚠️ Limited | ✅ TW focus |

---

## Updated Competitor Overview Table (Round 9 Additions)

| Dimension | 財報狗 | JZ Invest | 鉅亨網 | Simply Wall St | Stockopedia | Investopedia | Morningstar | **Stock Explorer** |
|---|---|---|---|---|---|---|---|---|
| **Positioning** | Simple Investing | Community + Data | Financial Portal | Visual Analysis | Smart Education | Financial Ed | Independent Research | Beginner Education ("Historian") |
| **Screening** | ✅ Advanced | ✅ Community | ✅ Basic | ❌ | ✅ Advanced | ❌ | ❌ | ❌ MISSING |
| **Visual Analysis** | ⚠️ Charts | ❌ | ❌ | ✅ Snowflake | ⚠️ StockRank | ❌ | ⚠️ Star Rating | ✅ PPT-style |
| **Education** | ⚠️ Blog | ❌ | ⚠️ Columns | ⚠️ Visual | ✅ Academy | ✅ Academy + Dictionary | ⚠️ Articles | ✅ Core |
| **Rating System** | ⚠️ Dividend Score | ❌ | ❌ | ✅ Snowflake 0-5 | ✅ StockRank 0-100 | ❌ | ✅ Stars 1-5 | ❌ MISSING |
| **Risk Analysis** | ❌ | ❌ | ❌ | ✅ Visual | ⚠️ StockRank | ❌ | ✅ Uncertainty | ❌ MISSING |
| **Community** | ❌ | ✅ Forum | ❌ | ❌ | ⚠️ Comments | ❌ | ❌ | ❌ MISSING |
| **International** | ❌ TW only | ❌ TW only | ✅ Global | ✅ Global | ✅ Global | ✅ Global | ✅ Global | ❌ TW only |
| **Mobile App** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ❌ | ✅ Native | ✅ Native | ❌ Streamlit only |
| **Notifications** | ✅ App Push | ✅ App Push | ✅ App Push | ✅ Email | ✅ Email | ❌ | ✅ Email | ❌ MISSING |
| **TW Market** | ✅ Deep | ✅ Deep | ✅ Deep | ❌ | ❌ | ❌ | ⚠️ Limited | ✅ Deep |

---

## New Feature Ideas from Round 9

### [ISSUE-C42] Stock Screener / Discovery Engine
- **Source**: Competitor research round 9 (財報狗 advanced screener, Stockopedia StockRank screening, JZ Invest community presets)
- **Priority**: P1
- **Effort**: 16-24h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + beginner-friendly discovery
- **Description**: Stock Explorer currently requires users to know which stock to search for. Beginners often don't know where to start. 財報狗's stock screener is its #1 feature — users can filter by criteria like "ROE > 15%", "dividend yield > 4%", "revenue growing 3 years" and discover stocks they didn't know about. Stock Explorer's "historian" positioning is perfect for this: instead of screening for "good stocks to buy", we screen for "interesting companies to learn about" — e.g., "companies with revenue growing > 20% for 3 years" or "companies with dividend yield > 5% and payout ratio < 70%". This transforms Stock Explorer from a lookup tool into a discovery tool.
- **Implementation**: Add a "🔍 選股探索" page with beginner-friendly screening presets (e.g., "穩定收息", "成長潛力", "便宜估值") and custom screening on key metrics (ROE, P/E, dividend yield, revenue growth). Use FinMind data. Results link to existing business card pages.
- **Competitive Gap**: 🔴 財報狗's #1 feature; no TW competitor combines screening with plain-language education

---

### [ISSUE-C43] Company "Snowflake" Health Visualization
- **Source**: Competitor research round 9 (Simply Wall St snowflake diagram, Morningstar star rating, Stockopedia StockRank)
- **Priority**: P1
- **Effort**: 12-16h
- **Alignment**: Core value #1 "Story first, data second" + "Ten-second test" + Core value #5 "Benchmark-oriented analysis"
- **Description**: Simply Wall St's snowflake diagram and Morningstar's star rating both give beginners an instant, visual answer to "How healthy is this company?" Stock Explorer currently shows 15+ metrics scattered across sections with no synthesized visual summary. A "Company Snowflake" would show 5 dimensions (Profitability, Growth, Financial Health, Dividend, Valuation) as a radar chart or snowflake diagram with color-coded scores. This directly addresses the "ten-second test" — a beginner can glance at the snowflake and immediately understand the company's overall health. Unlike Simply Wall St (which uses proprietary algorithms), Stock Explorer's snowflake would use plain-language explanations for each dimension: "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元".
- **Implementation**: Add a radar chart (using Plotly) to the top of the business card page showing 5 dimensions scored 0-5. Each dimension has a plain-language explanation on hover/click. Scores calculated from FinMind data with industry benchmarking (aligns with #5 benchmark-oriented analysis).
- **Competitive Gap**: 🔴 No TW competitor has visual health score; Simply Wall St proves demand internationally; our plain-language twist is unique

---

### [ISSUE-C44] "What Could Go Wrong" Risk Analysis Section
- **Source**: Competitor research round 9 (Simply Wall St visual risk analysis, Morningstar uncertainty rating, TEJ credit risk)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #1 "Story first, data second" + "Historian" positioning (explain, don't predict)
- **Description**: Simply Wall St has a visual "Risk Analysis" section showing what could go wrong with a company. Morningstar has an "Uncertainty Rating" that tells beginners valuation is not a single number but a range. Stock Explorer's "historian" positioning is perfect for risk analysis — not predicting the future, but explaining historical risks that have materialized. For example: "TSMC's main risk: 90% of revenue comes from 3 customers (Apple, NVIDIA, AMD). If any of them switch to a competitor, revenue could drop 30%." This is factual, educational, and doesn't require predicting the future. Currently, Stock Explorer has NO risk analysis section.
- **Implementation**: Add a "⚠️ 風險分析" section to the business card page with 3-5 key risks presented in plain language. Each risk includes: (1) what the risk is, (2) historical evidence (has it happened before?), (3) current indicators to watch. Data sources: customer concentration from annual reports, industry risks from TEJ-style analysis, financial risks from debt ratios.
- **Competitive Gap**: 🟡 Simply Wall St has risk analysis but not with historical evidence; no TW competitor has plain-language risk analysis

---

### [ISSUE-C45] Valuation Band Chart (P/E or P/B Historical Range)
- **Source**: Competitor research round 9 (財報狗 P/E band chart, Morningstar fair value with uncertainty)
- **Priority**: P2
- **Effort**: 8-10h
- **Alignment**: Core value #1 "Story first, data second" + Core value #5 "Benchmark-oriented analysis"
- **Description**: 財報狗's P/E band chart is one of its most popular features — it shows the current P/E ratio vs the historical range (e.g., "TSMC's P/E is currently 18x, historically it trades between 12x and 25x"). This helps beginners understand whether a stock is "expensive" or "cheap" relative to its own history. Stock Explorer currently shows valuation metrics as single numbers with no historical context. A valuation band chart would show: (1) current P/E, (2) 5-year P/E range, (3) where current P/E falls in the range (percentile), (4) plain-language explanation: "目前本益比18倍，處於歷史區間的中間位置，不算貴也不算便宜".
- **Implementation**: Add a "📊 估值區間" card to the business card page with a horizontal bar chart showing current P/E vs 5-year range. Include plain-language interpretation. Data source: FinMind price and EPS data.
- **Competitive Gap**: 🟡 財報狗 has P/E band but no plain-language interpretation; no TW competitor combines valuation bands with educational context

---

### [ISSUE-C46] "Moat" Analysis — Competitive Advantage Assessment
- **Source**: Competitor research round 9 (Morningstar moat rating, TEJ industry analysis)
- **Priority**: P2
- **Effort**: 12-16h
- **Alignment**: Core value #1 "Story first, data second" + Core value #5 "Benchmark-oriented analysis" + "Historian" positioning
- **Description**: Morningstar's "Moat Rating" (wide, narrow, none) is one of its most recognized features — it answers "Does this company have a durable competitive advantage?" Stock Explorer's "historian" positioning is perfect for moat analysis: instead of predicting whether the moat will last, we explain what the moat IS and how it has protected the company historically. For example: "TSMC's moat: 技術領先 — 全球唯一能量產5nm晶片的工廠，競爭對手三星和英特爾落後2年以上。過去10年，這個護城河讓台積電的毛利率維持在50%以上." This is factual, educational, and aligns with "explain what has happened" rather than "predict what will happen".
- **Implementation**: Add a "🏰 護城河分析" section to the business card page with: (1) moat type (technology, brand, cost, network, switching costs), (2) moat strength (wide/narrow/none), (3) historical evidence, (4) plain-language explanation. Manual curation for top 20 stocks, template-based for others.
- **Competitive Gap**: 🔴 Morningstar has moat rating but only for US stocks; no TW competitor has moat analysis; perfect "historian" differentiator

---

### [ISSUE-C47] Financial Education Academy / Structured Learning Path
- **Source**: Competitor research round 9 (Investopedia Academy, Stockopedia Academy, Investopedia financial dictionary)
- **Priority**: P2
- **Effort**: 20-30h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + Core value #1 "Story first"
- **Description**: Investopedia Academy and Stockopedia Academy both offer structured learning paths — from "What is a stock?" to "How to read financial statements" to "Valuation techniques". Stock Explorer currently has "Did You Know?" facts (70 facts for 7 stocks) but no structured learning path. A "Learning Academy" would provide: (1) structured lessons organized by topic (not by stock), (2) each lesson uses real TW stock examples, (3) progressive difficulty (beginner → intermediate → advanced), (4) quizzes to test understanding. This transforms Stock Explorer from a stock lookup tool into a comprehensive investing education platform.
- **Implementation**: Add a "📚 學習學院" section with 10-15 structured lessons. Each lesson: title, 3-5 minute read, real TW stock example, key takeaway, quiz question. Topics: "What is revenue?", "What is profit?", "What is ROE?", "What is P/E?", "How to read a balance sheet", "What is a dividend?", etc. Reuse existing analogy engine for explanations.
- **Competitive Gap**: 🔴 No TW competitor has structured learning paths with TW stock examples; Investopedia/Stockopedia prove demand internationally

---

## Updated Analysis

### Key Insights from Round 9

1. **Visual health scores are becoming standard** — Simply Wall St (snowflake), Morningstar (stars), and Stockopedia (StockRank) all have proprietary scoring systems that give beginners an instant answer. Stock Explorer needs a visual health score (C43) to remain competitive. Our differentiator: plain-language explanations for each dimension.

2. **Discovery is a critical gap** — 財報狗's #1 feature is its stock screener. Stock Explorer requires users to know which stock to look up, which is a barrier for beginners. A discovery/screening engine (C42) would transform the product from a lookup tool to an exploration tool.

3. **Risk analysis is an untapped differentiator** — Simply Wall St has risk analysis but not with historical evidence. Morningstar has uncertainty ratings but not in plain language. Stock Explorer's "historian" positioning is perfect for risk analysis that explains historical risks without predicting the future (C44).

4. **Valuation context is expected** — 財報狗's P/E band chart shows that beginners expect historical valuation context. Showing P/E as a single number without context is like showing a student's test score without saying whether it's good or bad (C45).

5. **Moat analysis is a unique opportunity** — Morningstar's moat rating is iconic but only covers US stocks. No TW competitor has moat analysis. This is a perfect "historian" feature — explaining what the competitive advantage IS and how it has protected the company historically, without predicting the future (C46).

6. **Structured education is the endgame** — Investopedia Academy and Stockopedia Academy show that structured learning paths are the natural evolution of financial education platforms. Stock Explorer's "Did You Know?" facts are a good start, but a structured academy (C47) would be the ultimate expression of the "education-first" positioning.

### Feature Gap Summary

| ID | Title | Priority | Effort | Source Competitor | Alignment |
|---|---|---|---|---|---|
| C42 | Stock Screener / Discovery Engine | P1 | 16-24h | 財報狗, Stockopedia | Point-to-point + Discovery |
| C43 | Company Snowflake Health Visualization | P1 | 12-16h | Simply Wall St, Morningstar | Story first + Ten-second test |
| C44 | "What Could Go Wrong" Risk Analysis | P2 | 10-14h | Simply Wall St, Morningstar | Story first + Historian |
| C45 | Valuation Band Chart (Historical P/E) | P2 | 8-10h | 財報狗, Morningstar | Story first + Benchmark |
| C46 | Moat Analysis (Competitive Advantage) | P2 | 12-16h | Morningstar | Story first + Benchmark + Historian |
| C47 | Financial Education Academy | P2 | 20-30h | Investopedia, Stockopedia | Point-to-point + Story first |

### Recommendations

#### Immediate (Next Sprint)
1. **C43 Company Snowflake** — P1 gap, directly addresses "ten-second test", multiple competitors prove demand
2. **C42 Stock Screener** — P1 gap, 財報狗's #1 feature, transforms product from lookup to discovery

#### Short-Term (Sprint 2-3)
3. **C45 Valuation Band Chart** — Low effort (8-10h), high impact, 財報狗 proves demand
4. **C44 Risk Analysis** — Unique "historian" differentiator, no TW competitor has it

#### Medium-Term (Post-Sprint 3)
5. **C46 Moat Analysis** — Unique differentiator for TW market, manual curation for top 20 stocks
6. **C47 Education Academy** — Long-term differentiator, transforms product from tool to platform

---

*This is the ninth competitor research round. Six new feature suggestions identified (C42-C47). The most impactful new gap is C43 (Company Snowflake Health Visualization) — it directly addresses the "ten-second test" design principle and multiple international competitors prove demand. The most strategically important gap is C42 (Stock Screener) — it transforms Stock Explorer from a lookup tool to a discovery platform, which is critical for beginner engagement.*

---

# Stock Explorer Competitor Research Report — Round 11

> **Date**: 2026-06-15
> **Author**: QA Engineer (Round 11)
> **Purpose**: Research 7+ new competitors not covered in Rounds 1-9, focusing on global charting/social platforms, AI-powered analysis, structured finance education, and Asian market platforms
> **Previous Rounds**: Round 1-7: StatementDog, GoodInfo, CMoney, WantGoo, Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, The Motley Fool, NerdWallet, JZ Invest, 鉅亨網, TEJ, Yahoo奇摩股市, Simply Wall St, Stockopedia, Investopedia, Morningstar. Round 8-9: See main report above.

---

## New Competitors Analyzed (Not in Rounds 1-9)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **TradingView** | Charting + Social + Analysis | Global | 🔴 High — social features + community analysis overlap with education mission |
| **TipRanks** | Analyst Tracking + Smart Score | US/Global | 🟡 Medium — Smart Score validates health score concept; analyst tracking is unique |
| **Finimize** | Daily Financial News + Education | UK/Global | 🟡 Medium — structured courses + AI Q&A; concept-first approach |
| **Zerodha Varsity** | Structured Finance Education | India | 🔴 High — gold standard for structured stock education; module-based learning |
| **StockEdge** | Visual Stock Analysis + Screening | India | 🔴 High — visual-first approach + screening; similar PPT-style philosophy |
| **Tickeron** | AI-Powered Analysis + Patterns | US/Global | 🟡 Medium — AI pattern recognition + portfolio scoring |
| **Khan Academy Finance** | Free Financial Education | US/Global | 🟡 Medium — progressive learning model; video-first approach |
| **Stake** | Commission-Free Trading + Education | AU/Asia | 🟡 Medium — beginner onboarding + company stories; Asian expansion |
| **Moomoo (富途牛牛)** | Social Investing + AI Education | Asia/Global | 🔴 High — AI education features + social learning feed; Asian market focus |

---

## Detailed Competitor Profiles

### 1. TradingView (tradingview.com)

**Positioning**: "The world's active community of traders and investors" — charting + social + analysis
**Target Users**: Active traders, technical analysis enthusiasts, retail investors globally (30M+ users)

**Key Features**:
- **Advanced Charting**: 100+ indicators, 18 chart types, multi-timeframe analysis, Pine Script for custom indicators
- **Social Network**: Users publish "ideas" (analysis posts) attached to charts; followers, likes, comments — essentially a financial social network
- **Stock Screener**: Multi-condition screening with 100+ fundamental and technical metrics
- **Community Analysis**: Users share chart annotations, price predictions, and fundamental analysis as visual "idea" posts
- **Watchlist with Hover Previews**: Hover over any stock in watchlist → mini chart tooltip appears instantly
- **Alerts**: Price, indicator, and strategy alerts via web, email, and mobile push
- **Paper Trading**: Virtual trading with real market data
- **Global Coverage**: 50+ exchanges including TWSE (Taiwan Stock Exchange)

**UX/Design Approach**:
- **Icon bar + panel system**: Left icon bar opens context-specific panels (watchlist, alerts, ideas, screener)
- **Chart-first**: The chart is the primary UI element; everything else is secondary
- **Dark mode default**: Professional trading aesthetic
- **Social layer**: Every chart can have community annotations; analysis is collaborative
- **Hover-rich interactions**: Hover over watchlist items, indicators, data points for instant previews

**Unique Capabilities**:
- **Social analysis**: Users learn by reading others' chart analysis — a form of peer education
- **Pine Script community**: Thousands of user-created indicators and strategies shared freely
- **"Ideas" feed**: A Twitter-like feed of chart analysis from the community
- **Multi-chart layouts**: Up to 8 charts on one screen for comparison

**Comparison with Stock Explorer**:

| Feature | TradingView | Stock Explorer |
|---|---|---|
| Charting | ✅ Industry-leading | ⚠️ Basic Plotly |
| Social/Community | ✅ Full social network | ❌ Not built |
| Education | ⚠️ Community-driven | ✅ Structured |
| Screener | ✅ Advanced | ❌ Not built |
| Plain-language | ❌ | ✅ Core feature |
| PPT-style | ❌ | ✅ Unique |
| TW Market | ✅ Full coverage | ✅ Deep coverage |
| Alerts | ✅ Multi-channel | ❌ Not built |
| Paper Trading | ✅ | ❌ (positioning) |
| Mobile App | ✅ Native | ❌ Streamlit only |

**Key Insight for Stock Explorer**: TradingView's social learning model (users learn by reading others' analysis) is a powerful education mechanism that Stock Explorer completely lacks. The "Ideas" feed is essentially a community-generated stock analysis platform. While Stock Explorer's structured approach is higher quality, the social learning aspect drives engagement and retention. The hover-preview watchlist pattern is a UX innovation Stock Explorer should adopt.

---

### 2. TipRanks (tipranks.com)

**Positioning**: "Transparency in analyst recommendations — track who's right and who's wrong"
**Target Users**: US-focused retail investors who want to follow expert recommendations; covers TSMC (TSM)

**Key Features**:
- **Analyst Accuracy Tracking**: Tracks every analyst's recommendation history — "This analyst recommended TSMC 12 times and was right 83% of the time"
- **Smart Score (0-10)**: AI-generated composite score based on 8 factors: analyst consensus, analyst accuracy, insider trading, news sentiment, hedge fund activity, blogger sentiment, fundamentals, and technicals
- **Insider Trading Tracker**: Shows what company insiders (CEOs, CFOs, directors) are buying/selling with historical accuracy tracking
- **"Trending Stocks" Heatmap**: Real-time aggregation of which stocks analysts are upgrading/downgrading today
- **Blogger/Influencer Rankings**: Ranks financial bloggers by historical pick accuracy
- **"Price Target" Distribution**: Shows the distribution of analyst price targets (not just the average)

**UX/Design Approach**:
- **Score-centric**: Smart Score is the most prominent element on every stock page
- **Data-dense but scannable**: Tables and charts with color-coded indicators
- **"Who's right" framing**: Every recommendation is tied to a track record
- **US-focused**: Limited TW stock coverage (only TSM ADR)

**Unique Capabilities**:
- **Analyst accuracy tracking**: No other platform tracks analyst performance this granularly
- **Insider trading with accuracy**: Shows not just what insiders bought, but whether they were right historically
- **Smart Score**: Single composite score that aggregates 8 different signal types

**Comparison with Stock Explorer**:

| Feature | TipRanks | Stock Explorer |
|---|---|---|
| Smart Score | ✅ 0-10 composite | ❌ Not built |
| Analyst Tracking | ✅ Accuracy history | ❌ Not built |
| Insider Trading | ✅ With accuracy | ❌ Not built |
| Plain-language | ❌ | ✅ Core feature |
| Education | ⚠️ Implicit | ✅ Structured |
| TW Market | ⚠️ TSM only | ✅ Deep coverage |
| Social | ❌ | ❌ Not built |

**Key Insight for Stock Explorer**: TipRanks' Smart Score validates the demand for a single composite health score (ISSUE-C43). However, TipRanks' approach is black-box ("here's a score") while Stock Explorer's should be explainable ("here's a score and here's why in plain language"). The "analyst accuracy tracking" concept is educationally valuable — teaching beginners that experts disagree and past accuracy matters is important financial literacy, even if Stock Explorer doesn't recommend following experts.

---

### 3. Finimize (finimize.com)

**Positioning**: "Financial news and insights, simplified — in 3 minutes"
**Target Users**: Busy professionals and beginners who want to stay informed without reading Wall Street Journal; 1M+ subscribers

**Key Features**:
- **Daily Newsletter**: 3-minute daily financial news digest in plain language
- **Finimize Academy** (2025): Structured 4-week financial literacy course with daily 3-minute lessons, quizzes, and completion certificate
- **"Ask Finimize" AI Q&A**: Natural language Q&A about any financial topic — "Why is TSMC's gross margin so high?" → plain-language answer
- **Personalized Daily Briefing**: AI learns user interests (e.g., "TW stocks," "dividend investing") and tailors content
- **Finimize Community** (2025): Moderated community with "Beginner-Friendly" sections and no-judgment rules
- **"Market Mood" Indicator**: Daily sentiment indicator (😰 Fear → 😊 Neutral → 🤩 Greed) aggregating news, social media, and market data
- **Mobile App**: Push notifications for daily briefings and market events

**UX/Design Approach**:
- **Bite-sized**: Every piece of content is 3 minutes or less
- **Plain-language first**: No jargon without explanation
- **Daily engagement loop**: Users return every day for the briefing
- **Progressive depth**: Start with 3-minute summary → click for deeper analysis
- **Clean, modern design**: Minimalist with generous whitespace

**Unique Capabilities**:
- **Completion certificates**: Finimize Academy gives certificates that beginners can share — credentialing mechanism
- **Personalized briefing**: AI-driven content personalization based on user interests
- **"Market Mood" indicator**: Simple, visual sentiment indicator that beginners understand instantly
- **Community with rules**: "Beginner-friendly" moderation creates safe learning environment

**Comparison with Stock Explorer**:

| Feature | Finimize | Stock Explorer |
|---|---|---|
| Daily Engagement | ✅ Newsletter + briefing | ❌ Not built |
| Structured Courses | ✅ Finimize Academy | ⚠️ Did You Know facts |
| AI Q&A | ✅ Ask Finimize | ❌ Not built |
| Market Mood | ✅ Sentiment indicator | ❌ Not built |
| Community | ✅ Moderated | ❌ Not built |
| Certificates | ✅ Completion certs | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| Company Analysis | ⚠️ News-focused | ✅ Deep analysis |
| TW Market | ⚠️ Limited | ✅ Deep coverage |

**Key Insight for Stock Explorer**: Finimize's "Market Mood" indicator is a simplified version of ISSUE-C35 (Market Mood Index) — validates the concept. Their structured course with completion certificates (Finimize Academy) is a credentialing mechanism that Stock Explorer's planned C47 (Education Academy) should adopt. The daily engagement loop (newsletter → app → community) is a retention model that Stock Explorer completely lacks.

---

### 4. Zerodha Varsity (zerodha.com/varsity)

**Positioning**: "The most comprehensive free stock market education in India" — structured, module-based finance education
**Target Users**: Indian retail investors from absolute beginner to intermediate; 5M+ learners

**Key Features**:
- **Module-Based Learning**: 14 structured modules covering: Stock Markets Basics, Fundamental Analysis, Technical Analysis, Options Trading, Commodities, Currencies, and more
- **Progressive Difficulty**: Modules are numbered 1-14 and designed to be completed in order; each module builds on the previous
- **Plain-Language Explanations**: Every concept explained with real Indian stock examples and everyday analogies
- **Visual Illustrations**: Custom illustrations and diagrams for every concept — similar philosophy to Stock Explorer's PPT-style
- **Quizzes**: End-of-module quizzes to test understanding
- **Completely Free**: No paywall, no premium tier — all content is free
- **Community Forum**: Active discussion forum for each module
- **Mobile-Responsive**: Works well on mobile devices

**UX/Design Approach**:
- **Textbook-like structure**: Each module is a chapter with sections, sub-sections, and illustrations
- **One concept per page**: Similar to Stock Explorer's PPT-style — one key idea per screen
- **Progressive disclosure**: Start with the basics, advance only when ready
- **No distractions**: Clean reading experience with minimal UI chrome
- **Indian stock examples**: All examples use Indian companies (Reliance, TCS, Infosys) — culturally relevant

**Unique Capabilities**:
- **Most comprehensive free education**: 14 modules covering everything from "What is a stock?" to "Options Greeks"
- **Cultural localization**: All examples are Indian stocks with Indian market context — this is exactly what Stock Explorer does for TW stocks
- **Module completion tracking**: Users can track which modules they've completed
- **Community per module**: Discussion forum attached to each module for Q&A

**Comparison with Stock Explorer**:

| Feature | Zerodha Varsity | Stock Explorer |
|---|---|---|
| Structured Modules | ✅ 14 modules | ⚠️ Did You Know facts |
| Progressive Path | ✅ Numbered 1-14 | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| Visual Illustrations | ✅ Custom diagrams | ✅ PPT-style |
| Quizzes | ✅ End-of-module | ❌ Not built |
| Free | ✅ Completely free | ✅ Free |
| Community | ✅ Per-module forum | ❌ Not built |
| TW Examples | ❌ Indian focus | ✅ TW focus |
| Company Analysis | ⚠️ Concept-focused | ✅ Company-focused |

**Key Insight for Stock Explorer**: Zerodha Varsity is the closest philosophical match to Stock Explorer in the global market. Both platforms share: plain-language explanations, visual-first design, culturally localized examples, and education-first positioning. The key difference is that Varsity teaches concepts (not companies) while Stock Explorer teaches companies (not concepts). Varsity's module-based structure with progressive difficulty (1→14) is a model for Stock Explorer's planned C47 (Education Academy). The quiz system is a gap — Stock Explorer has no assessment mechanism.

---

### 5. StockEdge (stockedge.com)

**Positioning**: "Visual stock analysis and screening for Indian investors" — data-driven visual discovery
**Target Users**: Indian retail investors who want to discover and analyze stocks through visuals, not spreadsheets

**Key Features**:
- **Visual Stock Screening**: Unique "Edge" scoring system with visual heatmaps — stocks scored on multiple dimensions with color-coded grids
- **"Edge Reports"**: Auto-generated visual analysis reports for each stock with charts, scores, and plain-language summaries
- **Sector Analysis**: Visual sector breakdowns showing which sectors are hot/cold with plain-language explanations
- **Scan-Based Discovery**: Users create custom scans (e.g., "ROE > 20% AND debt < 50%") and get visual results
- **Daily Market Analysis**: Automated daily market analysis with visual summaries — "What happened in the market today" in 30 seconds
- **Mobile-First**: Native mobile app is the primary platform (not a web app)
- **Watchlist with Visual Alerts**: Watchlist shows color-coded alerts for stocks hitting scan criteria

**UX/Design Approach**:
- **Visual-first**: Every metric is a chart, heatmap, or color-coded grid — minimal text
- **Mobile-native**: Designed for phone screens first, not desktop
- **Scan-driven discovery**: Users discover stocks through visual scans, not through search
- **Color-coded everything**: Green/yellow/red for good/neutral/bad across all metrics
- **Swipe-based navigation**: Mobile app uses swipe gestures for navigation

**Unique Capabilities**:
- **Edge Scoring**: Proprietary visual scoring system that gives instant stock assessment
- **Visual heatmaps**: Sector and stock heatmaps that show patterns at a glance
- **Auto-generated reports**: Every stock gets a visual "Edge Report" — similar to Stock Explorer's business card page but more visual
- **Scan-based discovery**: Users discover stocks through visual screening, not by knowing what to search for

**Comparison with Stock Explorer**:

| Feature | StockEdge | Stock Explorer |
|---|---|---|
| Visual Screening | ✅ Heatmap-based | ❌ Not built |
| Edge Scoring | ✅ Proprietary | ❌ Not built |
| Auto Reports | ✅ Visual reports | ✅ Business card |
| Sector Analysis | ✅ Visual heatmaps | ❌ Not built |
| Mobile-First | ✅ Native app | ❌ Streamlit only |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ❌ India focus | ✅ TW focus |
| Scan Discovery | ✅ Visual scans | ❌ Not built |

**Key Insight for Stock Explorer**: StockEdge's visual screening and heatmap approach is a more visual version of ISSUE-C42 (Stock Screener). The "auto-generated visual report" concept is similar to Stock Explorer's business card page — validates the approach. StockEdge's mobile-first design is a gap for Stock Explorer (Streamlit is desktop-only). The sector heatmap is a feature Stock Explorer doesn't have — a visual "which sectors are hot" overview would complement the company-focused analysis.

---

### 6. Tickeron (tickeron.com)

**Positioning**: "AI-powered stock analysis and pattern recognition" — AI-first investment research
**Target Users**: US-focused retail investors who want AI-generated stock insights and pattern recognition

**Key Features**:
- **AI Pattern Recognition**: AI identifies chart patterns (head & shoulders, double bottom, etc.) and generates buy/sell signals
- **"AI Grade"**: Every stock gets an AI-generated grade (Strong Buy → Strong Sell) based on pattern recognition, fundamentals, and sentiment
- **Portfolio AI Score**: AI scores the user's entire portfolio for risk, diversification, and expected returns
- **"Trendy" Stocks**: AI identifies stocks that are trending based on social media, news, and price momentum
- **AI-Generated Forecasts**: AI generates 1-month and 12-month price forecasts with confidence intervals
- **Real-Time Alerts**: AI-generated alerts for pattern breakouts, trend changes, and unusual activity
- **"Copy AI" Portfolios**: Users can copy AI-generated portfolios based on risk profile

**UX/Design Approach**:
- **AI-first**: Every feature is powered by AI — the AI is the product
- **Grade-centric**: AI Grade is the most prominent element
- **Pattern-focused**: Chart patterns are the primary analysis method
- **US-focused**: Limited international coverage

**Unique Capabilities**:
- **AI pattern recognition**: Automatically identifies 100+ chart patterns
- **Portfolio-level AI**: Scores entire portfolios, not just individual stocks
- **AI forecasts**: Price forecasts with confidence intervals (teaches beginners about uncertainty)
- **"Copy AI"**: AI-generated portfolios that users can follow

**Comparison with Stock Explorer**:

| Feature | Tickeron | Stock Explorer |
|---|---|---|
| AI Pattern Recognition | ✅ 100+ patterns | ❌ Not built |
| AI Grade | ✅ Strong Buy → Sell | ❌ Not built |
| Portfolio AI | ✅ Portfolio scoring | ❌ Not built |
| AI Forecasts | ✅ With confidence | ❌ Not built |
| Plain-language | ❌ | ✅ Core feature |
| Education | ❌ Stock-picking tool | ✅ Education-first |
| TW Market | ⚠️ Limited | ✅ Deep coverage |
| Alerts | ✅ AI-generated | ❌ Not built |

**Key Insight for Stock Explorer**: Tickeron is the antithesis of Stock Explorer's "historian" positioning — it's a stock-picking tool that uses AI to generate buy/sell signals. However, the "AI Grade" concept validates the demand for simplified stock assessment (similar to C43 Snowflake Health). The "confidence interval" on forecasts is educationally valuable — teaching beginners that predictions are uncertain. Tickeron's portfolio-level analysis is a gap — Stock Explorer has no portfolio features.

---

### 7. Khan Academy Finance (khanacademy.org)

**Positioning**: "Free, world-class education for anyone, anywhere" — the gold standard for free structured learning
**Target Users**: Students, beginners, self-learners globally; 120M+ registered users

**Key Features**:
- **Structured Video Lessons**: 5-10 minute video lessons on every finance topic: stocks, bonds, mutual funds, inflation, interest rates, etc.
- **Progressive Curriculum**: Lessons organized into courses → units → lessons; clear learning path from beginner to advanced
- **Interactive Exercises**: Practice problems after each lesson with instant feedback and hints
- **Mastery System**: "Mastery points" and progress tracking — users must demonstrate understanding before advancing
- **Completely Free**: No ads, no paywall, no premium — funded by donations
- **Multi-Language**: Content available in 50+ languages (finance section primarily English)
- **Badges & Gamification**: Achievement badges for completing courses and mastering concepts
- **Teacher Tools**: Progress dashboards for classroom use

**UX/Design Approach**:
- **Video-first**: Every concept is taught through a 5-10 minute video with visual illustrations
- **One concept per lesson**: Similar to Stock Explorer's PPT-style — one key idea per screen
- **Progressive difficulty**: Must complete Unit 1 before Unit 2; mastery-based progression
- **Clean, distraction-free**: Minimal UI, focus on content
- **Instant feedback**: Exercises provide immediate correct/incorrect feedback with explanations

**Unique Capabilities**:
- **Mastery-based learning**: Users must demonstrate understanding before advancing — ensures retention
- **Progress tracking**: Detailed progress dashboard showing completed lessons, mastery level, and next steps
- **Achievement system**: Badges and points for completing courses — gamification drives engagement
- **Global scale**: 120M+ users, 50+ languages, completely free

**Comparison with Stock Explorer**:

| Feature | Khan Academy | Stock Explorer |
|---|---|---|
| Video Lessons | ✅ 5-10 min each | ❌ Not built |
| Structured Curriculum | ✅ Courses → Units → Lessons | ⚠️ Did You Know facts |
| Mastery System | ✅ Must demonstrate understanding | ❌ Not built |
| Interactive Exercises | ✅ With instant feedback | ❌ Not built |
| Progress Tracking | ✅ Detailed dashboard | ❌ Not built |
| Badges/Gamification | ✅ Achievement system | ❌ Not built |
| Free | ✅ Completely free | ✅ Free |
| Company Analysis | ❌ Concept-focused | ✅ Company-focused |
| TW Examples | ❌ US focus | ✅ TW focus |

**Key Insight for Stock Explorer**: Khan Academy's mastery-based learning model is the gold standard for structured education. The "must demonstrate understanding before advancing" approach is something Stock Explorer's planned C47 (Education Academy) should adopt. The video-first format is a different modality than Stock Explorer's text+visual approach — video explanations of financial concepts could complement the existing text-based analysis. The progress tracking and achievement system (badges, mastery points) is a retention mechanism that Stock Explorer completely lacks.

---

### 8. Stake (stake.com) — Bonus Competitor

**Positioning**: "Commission-free trading for beginners" — trading platform with heavy education focus
**Target Users**: Australian and Asian beginner investors; expanding to TW and HK markets

**Key Features**:
- **"Stake Learn" Education Section**: Structured lessons on investing basics, stock analysis, and market fundamentals
- **Company Stories**: Short, visual "story cards" for popular stocks — "What does this company do?" in 30 seconds
- **Beginner Onboarding**: 7-step guided tutorial before first trade — similar to 玉山證券's "Beginner Village"
- **Visual Portfolio**: Clean, visual portfolio overview with plain-language performance summaries
- **Fractional Shares**: Buy partial shares — lowers barrier to entry for beginners
- **Social Features**: See what other Stake users are buying (anonymized)
- **Market News**: Curated news feed with plain-language summaries

**UX/Design Approach**:
- **Mobile-first**: Native app is the primary platform
- **Swipe-based**: Card-stack UX for browsing stocks and lessons
- **Visual-first**: Every concept is a visual card, not a text page
- **Beginner-friendly**: No jargon without explanation; tooltips on every financial term

**Unique Capabilities**:
- **"Company Story" cards**: 30-second visual summaries of what a company does — similar to Stock Explorer's one-liner concept
- **Fractional shares**: Lowers barrier to entry — beginners can invest $10 in TSMC
- **Social discovery**: See what others are buying — social proof for beginners

**Comparison with Stock Explorer**:

| Feature | Stake | Stock Explorer |
|---|---|---|
| Company Stories | ✅ 30-second cards | ✅ One-liner |
| Education | ✅ Stake Learn | ✅ Core positioning |
| Visual-First | ✅ Card-stack | ✅ PPT-style |
| Mobile-First | ✅ Native app | ❌ Streamlit only |
| Social | ✅ Anonymized | ❌ Not built |
| Plain-language | ✅ Tooltips | ✅ Core feature |
| TW Market | ⚠️ Expanding | ✅ Deep coverage |

**Key Insight for Stock Explorer**: Stake's "Company Story" cards are a more condensed version of Stock Explorer's business card page — validates the approach. Stake's mobile-first, swipe-based UX is a paradigm that Stock Explorer doesn't address. The "Stake Learn" education section is a broker-integrated education model — education serves the trading funnel, similar to 玉山證券.

---

### 9. Moomoo / Futubull (富途牛牛) — Bonus Competitor

**Positioning**: "AI-powered social investing platform" — comprehensive Asian fintech platform
**Target Users**: Asian retail investors across HK, SG, TW, JP, AU, US; 20M+ users

**Key Features**:
- **"Moomoo AI Analyst"** (2025): AI generates 3-bullet analysis for any stock: "What's happening," "Key risks," "What to watch"
- **"AI Course Generator"** (2026): Users type any financial topic → AI generates a 5-minute interactive lesson with examples and quizzes
- **"Social Learning Feed"**: TikTok-style feed where users share stock analysis, tips, and lessons; "Beginner" filter available
- **"Paper Trading with AI Feedback"**: Virtual portfolio with AI-generated feedback on trading decisions
- **"Market Heatmap with Education"**: Interactive sector heatmap with plain-language explanations of why each sector is moving
- **"Moomoo Academy"**: Structured courses on investing fundamentals with completion certificates
- **Community Features**: Stock-specific discussion boards, live streams, and expert Q&A sessions

**UX/Design Approach**:
- **Social-first**: The social feed is the homepage — content discovery through community
- **AI-powered**: AI generates analysis, courses, and feedback
- **Mobile-first**: Native app with full feature parity
- **Visual**: Heatmaps, charts, and visual summaries everywhere
- **Asian market focus**: Deep coverage of TW, HK, SG, JP markets

**Unique Capabilities**:
- **AI Course Generator**: On-demand, personalized lessons — users ask what they want to learn
- **Social Learning Feed**: TikTok-style content discovery — appeals to younger users
- **Paper Trading + AI Feedback**: Practice with AI coaching — combines practice with education
- **Market Heatmap with Education**: Visual sector analysis with plain-language explanations

**Comparison with Stock Explorer**:

| Feature | Moomoo | Stock Explorer |
|---|---|---|
| AI Analysis | ✅ 3-bullet summaries | ❌ Not built |
| AI Course Generator | ✅ On-demand lessons | ❌ Not built |
| Social Feed | ✅ TikTok-style | ❌ Not built |
| Paper Trading | ✅ With AI feedback | ❌ (positioning) |
| Market Heatmap | ✅ With education | ❌ Not built |
| Academy | ✅ Structured courses | ⚠️ Did You Know facts |
| Mobile App | ✅ Native | ❌ Streamlit only |
| TW Market | ✅ Deep coverage | ✅ Deep coverage |
| Plain-language | ⚠️ Some | ✅ Core feature |

**Key Insight for Stock Explorer**: Moomoo is the most comprehensive Asian competitor — it combines AI analysis, social learning, structured education, and market visualization in one platform. The "AI Course Generator" is a more advanced version of Stock Explorer's planned C47 (Education Academy). The "Social Learning Feed" (TikTok-style) is a UX paradigm that appeals to younger users. Moomoo's TW market coverage means it's directly targeting the same users as Stock Explorer.

---

## Updated Competitor Overview Table (Round 11 Additions)

| Dimension | TradingView | TipRanks | Finimize | Zerodha Varsity | StockEdge | Tickeron | Khan Academy | Stake | Moomoo | **Stock Explorer** |
|---|---|---|---|---|---|---|---|---|---|---|
| **Positioning** | Charting + Social | Analyst Tracking | News + Education | Structured Education | Visual Screening | AI Analysis | Free Education | Beginner Trading | Social Investing | Beginner Education ("Historian") |
| **Social/Community** | ✅ Full network | ❌ | ✅ Moderated | ✅ Forum | ❌ | ❌ | ❌ | ✅ Anonymized | ✅ TikTok feed | ❌ MISSING |
| **Structured Education** | ⚠️ Community | ❌ | ✅ Academy | ✅ 14 modules | ❌ | ❌ | ✅ Mastery system | ✅ Stake Learn | ✅ Academy | ⚠️ Did You Know |
| **AI Features** | ❌ | ✅ Smart Score | ✅ AI Q&A | ❌ | ❌ | ✅ Full AI | ❌ | ❌ | ✅ AI Analyst | ❌ MISSING |
| **Visual Analysis** | ✅ Charts | ⚠️ Scores | ⚠️ Minimal | ✅ Illustrations | ✅ Heatmaps | ✅ Patterns | ✅ Video | ✅ Cards | ✅ Heatmap | ✅ PPT-style |
| **Screening** | ✅ Advanced | ❌ | ❌ | ❌ | ✅ Visual scans | ❌ | ❌ | ❌ | ❌ | ❌ MISSING |
| **Progress Tracking** | ❌ | ❌ | ✅ Certificates | ✅ Module tracking | ❌ | ❌ | ✅ Mastery system | ❌ | ✅ Certificates | ❌ MISSING |
| **Mobile App** | ✅ Native | ✅ Native | ✅ Native | ⚠️ Responsive | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ❌ Streamlit only |
| **Daily Engagement** | ✅ Ideas feed | ❌ | ✅ Newsletter | ❌ | ✅ Daily analysis | ✅ Alerts | ✅ Streaks | ❌ | ✅ Social feed | ❌ MISSING |
| **TW Market** | ✅ Full | ⚠️ TSM only | ⚠️ Limited | ❌ India | ❌ India | ⚠️ Limited | ❌ US | ⚠️ Expanding | ✅ Deep | ✅ Deep |
| **Free** | ⚠️ Freemium | ⚠️ Freemium | ⚠️ Freemium | ✅ Completely | ⚠️ Freemium | ⚠️ Freemium | ✅ Completely | ✅ Free | ⚠️ Freemium | ✅ Free |

---

## New Feature Ideas from Round 11

### [ISSUE-C48] "Company Story Card" — 30-Second Visual Summary
- **Source**: Competitor research round 11 (Stake "Company Story" cards, StockEdge "Edge Reports", Finimize "Quick Summary")
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #1 "Story first, data second" + "Ten-second test"
- **Description**: Stake's "Company Story" cards give a 30-second visual summary of what a company does. StockEdge's "Edge Reports" auto-generate visual analysis reports. Stock Explorer's business card page has all the data but no synthesized 30-second summary. A "Company Story Card" at the very top of each company page would show: (1) one-liner description, (2) 3 key metrics with plain-language explanations, (3) one "did you know?" fact, (4) a "Learn More" button that scrolls to the full analysis. This is the "ten-second test" made real — a beginner can understand the company in 10 seconds, then choose to dive deeper.
- **Implementation**: Add a hero card at the top of the business card page with the one-liner, top 3 metrics (auto-selected based on what's most notable), and a rotating "Did You Know?" fact. Use existing analogy engine for plain-language explanations.
- **Competitive Gap**: 🟡 No TW competitor has auto-generated 30-second company summaries; Stake/StockEdge prove demand internationally

---

### [ISSUE-C49] "Daily Market Pulse" — Automated Market Summary
- **Source**: Competitor research round 11 (Finimize "Daily Briefing", StockEdge "Daily Market Analysis", Moomoo "Market Heatmap with Education")
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #3 "Adaptive and self-evolving" + beginner-friendly market overview
- **Description**: Finimize's daily briefing and StockEdge's daily market analysis both give beginners a 30-second summary of "what happened in the market today." Stock Explorer has no market-level view — it's entirely company-focused. A "Daily Market Pulse" on the homepage would show: (1) TWSE index change with plain-language explanation, (2) top 3 movers (up/down) with reasons, (3) sector heatmap (which sectors were hot/cold), (4) one "today's lesson" connecting market action to a financial concept. This creates a daily engagement loop — users return every day to see the market pulse.
- **Implementation**: Add a "📈 今日市場" section to the homepage with auto-generated daily summary. Data sources: FinMind market data, TWSE index, sector performance. Plain-language explanations generated from templates.
- **Competitive Gap**: 🟡 No TW competitor combines daily market summary with educational context; Finimize/StockEdge prove demand internationally

---

### [ISSUE-C50] "Learning Progress Tracker" — Concept Mastery System
- **Source**: Competitor research round 11 (Khan Academy mastery system, Zerodha Varsity module tracking, Finimize certificates)
- **Priority**: P2
- **Effort**: 12-16h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: Khan Academy's mastery system requires users to demonstrate understanding before advancing. Zerodha Varsity tracks module completion. Finimize gives completion certificates. Stock Explorer has no progress tracking — users explore companies but there's no sense of "I've learned X concepts" or "I'm Y% through the learning path." A "Learning Progress Tracker" would show: (1) which financial concepts the user has encountered, (2) quiz scores for each concept, (3) a "learning path" showing recommended next steps, (4) achievement badges for milestones (e.g., "Completed 10 company analyses," "Mastered P/E ratio").
- **Implementation**: Add a "📊 學習進度" page showing concept mastery (tracked via quiz performance), companies explored, and achievements. Integrate with C47 (Education Academy) when built. Start simple: track which company pages the user has viewed and which quiz questions they've answered correctly.
- **Competitive Gap**: 🔴 No TW competitor has learning progress tracking; Khan Academy/Zerodha prove demand; transforms Stock Explorer from tool to learning platform

---

### [ISSUE-C51] "Sector Heatmap" — Visual Market Overview
- **Source**: Competitor research round 11 (StockEdge sector heatmaps, Moomoo "Market Heatmap with Education")
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #5 "Benchmark-oriented analysis" + beginner-friendly market overview
- **Description**: StockEdge and Moomoo both have sector heatmaps that show which sectors are hot/cold at a glance. Stock Explorer has no sector-level view — users can only see individual companies. A "Sector Heatmap" would show: (1) all TW sectors as a color-coded grid (green = up, red = down), (2) click on a sector → see top companies in that sector, (3) plain-language explanation of why the sector is moving ("Semiconductor sector up 3% — driven by AI chip demand"). This helps beginners understand that companies don't exist in a vacuum — they're part of sectors that move together.
- **Implementation**: Add a "🔥 產業熱度" page with a Plotly treemap or heatmap of TW sectors. Data source: FinMind sector performance data. Click-through to sector detail page with top companies.
- **Competitive Gap**: 🟡 No TW competitor has sector heatmap with plain-language explanations; StockEdge/Moomoo prove demand internationally

---

### [ISSUE-C52] "Quiz Mode" — Interactive Knowledge Assessment
- **Source**: Competitor research round 11 (Khan Academy interactive exercises, Zerodha Varsity module quizzes, Finimize Academy quizzes)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: Khan Academy's interactive exercises with instant feedback are a core part of the learning experience. Zerodha Varsity has end-of-module quizzes. Finimize Academy has quizzes with completion certificates. Stock Explorer has no assessment mechanism — users read but never test their understanding. A "Quiz Mode" would: (1) present 5-10 questions after each company analysis page, (2) use real data from the company just viewed, (3) provide instant feedback with plain-language explanations, (4) track scores for the Learning Progress Tracker (C50). Example: "TSMC's gross margin is 55%. What does this mean? A) It keeps 55 cents of every dollar B) It spends 55% on R&D C) It pays 55% in dividends" → "Correct! Gross margin means how much of each dollar the company keeps after making the product."
- **Implementation**: Add a "🧪 小測驗" button to each company page that launches a 5-question quiz. Questions generated from templates with real data. Scores tracked in session state (persistent storage in C50).
- **Competitive Gap**: 🔴 No TW competitor has interactive quizzes with real stock data; Khan Academy/Zerodha prove demand; transforms passive reading into active learning

---

### [ISSUE-C53] "Social Sharing" — Shareable Analysis Cards
- **Source**: Competitor research round 11 (TradingView "Ideas" sharing, Plotch.ai story card sharing, Stake social features)
- **Priority**: P2
- **Effort**: 6-10h
- **Alignment**: Core value #1 "Story first, data second" + viral distribution
- **Description**: TradingView users share chart "Ideas" to Twitter/social media. Plotch.ai users share story cards. Stock Explorer has zero social sharing — there's no way to share a company analysis with friends. A "Social Sharing" feature would: (1) generate a shareable image card summarizing a company analysis (one-liner + 3 key metrics + "Did You Know?" fact), (2) provide "Share to LINE / Facebook / Copy Link" buttons, (3) the shared card links back to Stock Explorer for the full analysis. This is a viral distribution mechanism — every shared card is a new user acquisition event.
- **Implementation**: Use Python's Pillow library to generate shareable image cards from company data. Add share buttons to each company page. Generate a unique URL for each company page (already exists in Streamlit).
- **Competitive Gap**: 🟡 No TW competitor has shareable analysis cards; TradingView/Plotch.ai prove demand; zero-cost user acquisition

---

### [ISSUE-C54] "Video Explanation" — Audio/Visual Learning Modality
- **Source**: Competitor research round 11 (Khan Academy video-first approach, Sensical audio-first format)
- **Priority**: P2 (lower priority — high effort)
- **Effort**: 20-30h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + accessibility
- **Description**: Khan Academy's video-first approach is the gold standard for structured education. Sensical's audio-first format enables learning during commute. Stock Explorer is entirely text+visual — no audio or video content. Adding video explanations (even short 30-second clips) for key concepts would: (1) provide an alternative learning modality for auditory learners, (2) enable "listen while commuting" use case, (3) make complex concepts more accessible through visual animation. This is a long-term investment in content quality.
- **Implementation**: Start with text-to-speech audio explanations for the one-liner and key metrics on each company page. Add a "🔊 聽聽看" button that reads the company summary aloud. Longer-term: create short animated videos for common financial concepts (What is P/E? What is ROE?).
- **Competitive Gap**: 🟡 No TW competitor has audio/video explanations of TW stocks; Khan Academy/Sensical prove demand; different learning modality

---

## Key Insights from Round 11

### 1. **Social Learning is the Dominant Engagement Model**
TradingView (30M+ users), Moomoo (20M+ users), and Finimize (1M+ subscribers) all use social/community features as their primary engagement mechanism. Stock Explorer is entirely solo-learning — no community, no social sharing, no peer interaction. This is the #1 UX gap. Even lightweight social features (sharing, community discussion) would dramatically improve engagement and retention.

### 2. **Structured Education is Becoming Table Stakes**
Zerodha Varsity (14 modules), Khan Academy (mastery system), Finimize Academy (4-week course), and Moomoo Academy all offer structured learning paths. Stock Explorer's "Did You Know?" facts are a good start but not a structured curriculum. C47 (Education Academy) and C50 (Learning Progress Tracker) should be elevated to P1 — structured education is no longer a nice-to-have.

### 3. **Daily Engagement Loops Drive Retention**
Finimize (daily newsletter), TradingView (daily Ideas feed), StockEdge (daily market analysis), and Moomoo (social feed) all create daily reasons to return. Stock Explorer has no daily engagement mechanism — users only return when they want to look up a specific stock. C49 (Daily Market Pulse) would create a daily retention loop.

### 4. **Visual-First is the Standard**
StockEdge (heatmaps), TradingView (chart-first), Stake (card-stack), and Khan Academy (video-first) all prioritize visual learning over text. Stock Explorer's PPT-style is aligned with this trend but could be more visual — fewer words, more diagrams and visual metaphors.

### 5. **Assessment is the Missing Piece**
Khan Academy (mastery system), Zerodha Varsity (quizzes), and Finimize (course quizzes) all test user understanding. Stock Explorer has no assessment mechanism — users read but never demonstrate understanding. C52 (Quiz Mode) would transform passive reading into active learning.

### 6. **Mobile-First is the Norm**
Every competitor analyzed in Round 11 has a native mobile app. Stock Explorer's Streamlit-based web app is desktop-only. While a full mobile app is out of scope, the team should consider: (1) mobile-responsive design improvements, (2) a messaging bot interface (LINE/Telegram), (3) shareable content for mobile distribution.

### 7. **AI is Becoming Table Stakes**
TipRanks (Smart Score), Tickeron (AI Grade), Moomoo (AI Analyst), and Finimize (AI Q&A) all use AI as a core feature. Stock Explorer has no AI features planned beyond the analogy engine. While Stock Explorer's "historian" positioning deliberately avoids AI stock-picking, AI-powered explanations (C54 video/audio) and AI Q&A could complement the structured analysis.

---

## Feature Gap Summary (Round 11)

| ID | Title | Priority | Effort | Source Competitor | Alignment |
|---|---|---|---|---|---|
| C48 | Company Story Card (30-sec summary) | P2 | 8-12h | Stake, StockEdge, Finimize | Story first + Ten-second test |
| C49 | Daily Market Pulse | P2 | 10-14h | Finimize, StockEdge, Moomoo | Adaptive + Beginner-friendly |
| C50 | Learning Progress Tracker | P2 | 12-16h | Khan Academy, Zerodha, Finimize | Point-to-point + Ten-second test |
| C51 | Sector Heatmap | P2 | 8-12h | StockEdge, Moomoo | Benchmark-oriented + Beginner-friendly |
| C52 | Quiz Mode | P2 | 10-14h | Khan Academy, Zerodha, Finimize | Point-to-point + Active learning |
| C53 | Social Sharing | P2 | 6-10h | TradingView, Plotch.ai, Stake | Story first + Viral distribution |
| C54 | Video/Audio Explanation | P2 | 20-30h | Khan Academy, Sensical | Point-to-point + Accessibility |

---

## Recommendations

### Immediate (Next Sprint)
1. **C48 Company Story Card** — Low effort (8-12h), directly addresses "ten-second test," multiple competitors prove demand
2. **C53 Social Sharing** — Low effort (6-10h), zero-cost user acquisition, every shared card is a new user

### Short-Term (Sprint 2-3)
3. **C49 Daily Market Pulse** — Creates daily engagement loop, no TW competitor has it
4. **C51 Sector Heatmap** — Visual market overview, StockEdge/Moomoo prove demand
5. **C52 Quiz Mode** — Transforms passive reading into active learning, Khan Academy proves demand

### Medium-Term (Post-Sprint 3)
6. **C50 Learning Progress Tracker** — Transforms tool into learning platform, enables C47 Education Academy
7. **C54 Video/Audio Explanation** — Long-term investment in content quality and accessibility

---

*This is the eleventh competitor research round. Seven new feature suggestions identified (C48-C54). The most impactful new gap is C50 (Learning Progress Tracker) — it transforms Stock Explorer from a lookup tool into a learning platform, which is critical for the "education-first" positioning. The most strategically important gap is C53 (Social Sharing) — zero-cost user acquisition through shareable analysis cards. The most urgent gap is C48 (Company Story Card) — it directly addresses the "ten-second test" design principle and has the highest ROI (8-12h effort for core value alignment).*



# Stock Explorer Competitor Research Report — Round 12

> **Date**: 2026-06-18
> **Author**: QA Engineer (Round 12)
> **Purpose**: Research 9 new competitors not covered in Rounds 1-11, focusing on international social/copy investing platforms, US broker education features, Taiwanese broker apps, and emerging AI-powered financial education tools
> **Previous Rounds**: Round 1-7: Yahoo Finance, TradingView, Finviz, StatementDog, GoodInfo, CMoney, WantGoo, Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, The Motley Fool, NerdWallet. Round 8-11: See main report above.

---

## New Competitors Analyzed (Not in Rounds 1-11)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **eToro** | Social/Copy Investing + Education | Global/Israel | 🔴 High — "CopyTrader" social learning + Academy; education-through-observation model |
| **Webull** | Commission-Free Trading + Education | US/Asia | 🟡 Medium — paper trading + education center; gamified learning |
| **Robinhood** | Commission-Free Trading + Learn Section | US | 🟡 Medium — "Robinhood Learn" + options education; bite-sized lessons |
| **富邦e富 (Fubon eRich)** | TW Broker App + AI | TW | 🔴 High — AI-powered "Investment Compass" + social features; direct TW competitor |
| **元大證券 (Yuanta Securities)** | TW Broker App + AI | TW | 🔴 High — "AI Stock Selection" + "Smart Direct" routing; direct TW competitor |
| **永豐金證券 (Bank SinoPac)** | TW Broker App + Education | TW | 🟡 Medium — "Stock Learning Lab" + visualized financial analysis |
| **玉山證券 (E.SUN Securities)** | TW Broker + Beginner Village | TW | 🟡 Medium — "Beginner Village" + structured onboarding; mentioned in Round 11 but never profiled |
| **Magnify.money** | AI-Powered Financial Education | US/Global | 🔴 High — AI-generated visual explanations + interactive learning; emerging competitor |
| **Tastytrade** | Education-First Options Platform | US | 🟡 Medium — "Learn → Paper Trade → Live Trade" pipeline; education-first philosophy |

---

## Detailed Competitor Profiles

### 1. eToro (etoro.com)

**Positioning**: "The world's leading social investment platform" — learn by copying experienced investors
**Target Users**: Beginner to intermediate investors globally; 30M+ registered users

**Key Features**:
- **CopyTrader™**: Users can automatically copy the trades of successful investors in real-time — "See what they're doing, do what they're doing"
- **Social Feed**: Every user has a financial social feed showing trades, commentary, and portfolio changes from people they follow
- **eToro Academy**: Structured courses on investing fundamentals, technical analysis, and specific asset classes — includes quizzes and progress tracking
- **Virtual Portfolio**: $100,000 virtual portfolio for practice trading with real market data
- **Investor Profiles**: Detailed profiles of "Popular Investors" showing their performance history, risk score, portfolio composition, and trade rationale
- **"Why They Invested" Rationale**: When a Popular Investor makes a trade, they can share their reasoning — educational context for every trade
- **Risk Score System**: Every investor and asset gets a risk score (1-10) — helps beginners understand risk visually
- **Social Sentiment**: "X% of eToro users are buying TSMC" — crowd sentiment as a data point

**UX/Design Approach**:
- **Social-first**: The feed is the homepage — content discovery through community
- **Card-based**: Every investment, every investor, every piece of content is a card
- **Transparency-focused**: Every trade, every performance metric is visible
- **Copy-centric**: The "Copy" button is the most prominent action on every investor profile

**Unique Capabilities**:
- **CopyTrader**: Unique mechanism for learning by observation — beginners learn by watching experts
- **Social learning**: Users learn investing by reading the rationale behind real trades
- **Risk score**: Simple 1-10 risk rating for every investor and asset

**Comparison with Stock Explorer**:

| Feature | eToro | Stock Explorer |
|---|---|---|
| Social Learning | ✅ CopyTrader + Feed | ❌ Not built |
| Education | ✅ eToro Academy | ✅ Core positioning |
| Practice Trading | ✅ Virtual Portfolio | ❌ (positioning) |
| Risk Score | ✅ 1-10 rating | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ⚠️ Limited | ✅ Deep coverage |
| Trade Rationale | ✅ "Why they invested" | ❌ Not applicable |
| Community | ✅ Full social network | ❌ Not built |

**Key Insight for Stock Explorer**: eToro's "CopyTrader" is the ultimate social learning mechanism — beginners learn by observing and copying. While Stock Explorer deliberately avoids trading features, the "trade rationale" concept is analogous to our "analogy engine" — explaining WHY something happened, not just WHAT happened. eToro's risk score (1-10) is a simpler version of our planned C43 (Snowflake Health). The "social sentiment" feature (% of users buying/selling) is a crowd psychology data point that could complement our "historian" positioning — "Here's what happened, and here's what other people think about it."

---

### 2. Webull (webull.com)

**Positioning**: "Commission-free trading with powerful tools" — trading platform with heavy education investment
**Target Users**: US and Asian retail investors; 20M+ users globally

**Key Features**:
- **Webull Learn** (2025-2026): Structured education center with courses on stocks, options, ETFs, crypto — each course is 5-10 minutes with quizzes
- **Paper Trading**: Full-featured paper trading with $1M virtual portfolio — real market data, real-time execution
- **"Webull Classroom"**: Live and recorded webinars on investing topics — daily market analysis, strategy sessions
- **Community Feed**: Stock-specific discussion boards with upvoted comments — similar to Reddit's r/wallstreetbets but moderated
- **Technical Analysis Tools**: 60+ technical indicators, multi-chart layouts, drawing tools
- **AI-Powered Alerts** (2026): AI monitors user's watchlist and generates alerts for unusual patterns, news, and price movements
- **Fractional Shares**: Buy partial shares of any stock — lowers barrier to entry
- **Extended Hours Trading**: Trade pre-market and after-hours

**UX/Design Approach**:
- **Dark mode default**: Professional trading aesthetic
- **Panel-based**: Similar to TradingView — left icon bar with context-specific panels
- **Education integrated**: Learn tab is a core navigation item, not an afterthought
- **Mobile-first**: Native app is the primary platform

**Unique Capabilities**:
- **Paper trading with real data**: Practice without risk — similar to Investopedia Simulator
- **AI-powered alerts**: Pattern recognition for watchlist stocks
- **Community + education combo**: Discussion boards alongside structured courses

**Comparison with Stock Explorer**:

| Feature | Webull | Stock Explorer |
|---|---|---|
| Education Center | ✅ Webull Learn | ⚠️ Did You Know facts |
| Paper Trading | ✅ $1M virtual | ❌ (positioning) |
| Community | ✅ Discussion boards | ❌ Not built |
| AI Alerts | ✅ Pattern-based | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ⚠️ Limited | ✅ Deep coverage |
| Quizzes | ✅ Course quizzes | ❌ Not built |
| Mobile App | ✅ Native | ❌ Streamlit only |

**Key Insight for Stock Explorer**: Webull's "Learn" section is a more structured version of our planned C47 (Education Academy). The integration of community + education (discussion boards alongside courses) is a model for how Stock Explorer could combine structured learning with social features. The AI-powered alerts for watchlist stocks validate the concept of intelligent notifications (C02).

---

### 3. Robinhood (robinhood.com)

**Positioning**: "Investing for everyone" — commission-free trading with education as a core pillar
**Target Users**: Young, first-time investors in US; 23M+ users

**Key Features**:
- **Robinhood Learn** (2025-2026): Comprehensive, structured education library with 100+ articles and videos organized by topic: "What is a stock?", "What is an ETF?", "What is options trading?", "How to read financial statements"
- **"Learn → Earn" Program**: Users earn small amounts of stock (e.g., $1-$5) for completing educational modules — gamified learning with financial incentive
- **Options Education**: Industry-leading options education with interactive tutorials, probability calculators, and risk visualization
- **Recurring Investments Education**: Teaches dollar-cost averaging through interactive tools and visual explanations
- **"Robinhood Snacks"**: Daily 3-minute podcast and newsletter — "What happened in the market today" in plain language
- **"First Stock" Onboarding**: Guided first investment experience — step-by-step tutorial for buying your first stock
- **"Round-Ups" Education**: Teaches micro-investing concepts through automated round-ups
- **Market Data Explanations**: Every metric on a stock page has a tooltip explaining what it means — similar to our glossary concept (C33)

**UX/Design Approach**:
- **Minimalist**: Clean, simple interface — no clutter
- **Gamified**: Confetti animations for first trade, progress bars for learning
- **Bite-sized**: Every piece of content is 3 minutes or less
- **Mobile-first**: Native app is the primary platform

**Unique Capabilities**:
- **"Learn → Earn"**: Financial incentive for education — users earn stock for learning
- **Options education**: Best-in-class interactive options tutorials
- **"Snacks" daily briefing**: 3-minute daily market summary — similar to Finimize
- **Metric tooltips**: Every financial metric has a plain-language explanation

**Comparison with Stock Explorer**:

| Feature | Robinhood | Stock Explorer |
|---|---|---|
| Structured Education | ✅ 100+ articles/videos | ⚠️ Did You Know facts |
| Learn → Earn | ✅ Stock rewards | ❌ Not built |
| Daily Briefing | ✅ Robinhood Snacks | ❌ Not built |
| Metric Tooltips | ✅ Plain-language | ❌ Not built (C33 pending) |
| Options Education | ✅ Interactive | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ❌ US only | ✅ Deep coverage |
| Gamification | ✅ Confetti, progress | ❌ Not built |

**Key Insight for Stock Explorer**: Robinhood's "Learn → Earn" program is a gamification mechanism that Stock Explorer could adapt — instead of earning stock, users earn "knowledge badges" or "concept mastery" points. The metric tooltips are exactly what our C33 (Glossary) proposes — validates the concept. The "Snacks" daily briefing is a lighter version of our C49 (Daily Market Pulse). Robinhood's options education is a content area Stock Explorer doesn't cover but could — explaining what options are (not how to trade them) aligns with the "historian" positioning.

---

### 4. 富邦e富 (Fubon eRich / 富邦e富投資平台)

**Positioning**: "Your intelligent investment companion" — TW broker with AI-powered features
**Target Users**: TW retail investors; one of the largest broker apps in Taiwan

**Key Features**:
- **AI Investment Compass (AI投資羅盤)**: AI analyzes user's risk profile and recommends asset allocation — not stock picking, but portfolio-level guidance
- **"Smart Notification" System**: AI-generated alerts for portfolio changes, market events, and ex-dividend dates — personalized to user's holdings
- **Social Features ("Follow the Leader")**: Users can follow experienced investors and see their portfolio changes (anonymized) — similar to eToro's CopyTrader but lighter
- **"eRich Academy"**: Structured courses on investing fundamentals, technical analysis, and market trends — in Mandarin with TW stock examples
- **Visualized Portfolio**: Clean, visual portfolio overview with plain-language performance summaries — "Your portfolio is up 5% this month, mainly driven by TSMC"
- **"One-Click Report"**: Generate a one-page investment report summarizing portfolio performance, risk analysis, and recommendations — similar to WantGoo's PPT export concept
- **AI-Powered News Summarization**: AI summarizes financial news relevant to user's holdings — "Here's what you need to know about your stocks today"
- **Multi-Asset View**: Stocks, ETFs, bonds, and funds in one unified view

**UX/Design Approach**:
- **App-first**: Native mobile app is the primary platform
- **AI-powered**: AI is integrated into every feature — notifications, recommendations, news
- **Social layer**: Light social features (following, anonymized portfolios)
- **Clean, modern**: Card-based layout with generous whitespace

**Unique Capabilities**:
- **AI Investment Compass**: AI-driven asset allocation (not stock picking) — unique among TW brokers
- **Social following**: See what experienced investors are doing — social learning without full copy trading
- **One-click report**: Automated portfolio report generation — similar to our C06 (PPT Export) concept
- **AI news summarization**: Personalized news digest based on holdings

**Comparison with Stock Explorer**:

| Feature | 富邦e富 | Stock Explorer |
|---|---|---|
| AI Recommendations | ✅ Investment Compass | ❌ Not built |
| Social Following | ✅ Anonymized | ❌ Not built |
| Education | ✅ eRich Academy | ✅ Core positioning |
| AI Notifications | ✅ Personalized | ❌ Not built |
| One-Click Report | ✅ Portfolio report | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |
| Mobile App | ✅ Native | ❌ Streamlit only |
| AI News Summary | ✅ Personalized | ❌ Not built |

**Key Insight for Stock Explorer**: 富邦e富 is the most direct TW competitor with AI features. The "AI Investment Compass" is a portfolio-level recommendation system that doesn't pick stocks — this is philosophically aligned with Stock Explorer's "historian" positioning (explain, don't predict). The "one-click report" is exactly our C06 (PPT Export) concept — validates demand in the TW market. The social following feature is a lighter version of eToro's CopyTrader — social learning without the trading component. The AI news summarization is a feature that could complement our event dashboard.

---

### 5. 元大證券 (Yuanta Securities / 元大投資先生)

**Positioning**: "Your professional investment partner" — TW broker with AI-powered stock selection
**Target Users**: Active TW retail investors; one of the largest securities firms in Taiwan

**Key Features**:
- **AI Stock Selection (AI選股)**: AI-powered stock screening with natural language queries — "Show me companies with revenue growing > 10% and P/E < 15" → returns matching stocks with explanations
- **"Smart Direct" Routing**: AI-optimized order routing for best execution — not relevant to Stock Explorer but shows AI investment
- **"Investment Chatbot"**: AI chatbot that answers questions about stocks, markets, and investing — "What is TSMC's revenue growth?" → plain-language answer with data
- **"Market Pulse"**: Daily market summary with sector heatmap and top movers — similar to our C49 (Daily Market Pulse) concept
- **"Stock Comparison"**: Side-by-side stock comparison with visual metrics — similar to our peer comparison but with more visual presentation
- **"Investment Diary"**: Users can record their investment rationale and track their thinking over time — a journaling feature for reflection
- **"Knowledge Base"**: Structured articles on investing concepts with TW stock examples — similar to our C47 (Education Academy) concept
- **"Risk Assessment"**: Interactive risk profile questionnaire that visualizes user's risk tolerance — "You are a moderate investor: here's what that means"

**UX/Design Approach**:
- **Professional**: Clean, data-rich interface — more professional than consumer apps
- **AI-integrated**: AI is a core feature, not an add-on
- **Multi-platform**: Web + mobile app + desktop terminal
- **Chinese-first**: All content in Mandarin with TW market focus

**Unique Capabilities**:
- **AI chatbot**: Natural language Q&A about stocks and investing — similar to Finimize's "Ask Finimize"
- **Investment Diary**: Journaling feature for investment reflection — unique among TW brokers
- **Natural language screening**: Query stocks in plain language — "profitable tech companies" → results
- **Risk visualization**: Interactive risk profile with visual representation

**Comparison with Stock Explorer**:

| Feature | 元大證券 | Stock Explorer |
|---|---|---|
| AI Chatbot | ✅ Natural language Q&A | ❌ Not built |
| AI Screening | ✅ Natural language | ❌ Not built |
| Investment Diary | ✅ Journaling | ❌ Not built |
| Market Pulse | ✅ Daily summary | ❌ Not built |
| Knowledge Base | ✅ Structured articles | ⚠️ Did You Know facts |
| Risk Assessment | ✅ Interactive profile | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |
| Mobile App | ✅ Native | ❌ Streamlit only |

**Key Insight for Stock Explorer**: 元大證券's "Investment Diary" is a unique feature — a journaling tool where users record their investment thinking. This is philosophically aligned with Stock Explorer's "historian" positioning — instead of predicting the future, users reflect on the past. The AI chatbot (natural language Q&A about stocks) is a more advanced version of our analogy engine — users ask questions in plain language and get plain-language answers. The natural language stock screening is a more user-friendly version of our C42 (Stock Screener) — instead of filling in form fields, users type "profitable tech companies" and get results.

---

### 6. 永豐金證券 (Bank SinoPac / 永豐金證券)

**Positioning**: "Your wealth management partner" — TW broker with focus on financial education
**Target Users**: TW retail investors; mid-tier securities firm with strong education focus

**Key Features**:
- **"Stock Learning Lab" (股票學習實驗室)**: Structured courses on fundamental analysis, technical analysis, and market trends — with TW stock examples
- **"Financial Statement Visualizer"**: Interactive tool that visualizes financial statements — tap on "revenue" → see it on the income statement with plain-language explanation
- **"Investment Simulator"**: Paper trading with TW stocks — practice buying/selling with virtual money
- **"Market Sentiment Index"**: Proprietary sentiment index for TW market — combines institutional trading, news sentiment, and retail activity into a single gauge
- **"Smart Alerts"**: AI-generated alerts for portfolio events, market movements, and news — personalized to user's watchlist
- **"Sector Rotation Visualizer"**: Visual tool showing which sectors are gaining/losing momentum — similar to our C51 (Sector Heatmap) concept
- **"Investment Checklist"**: Before buying a stock, users complete a checklist of key metrics — "Have you checked P/E? ROE? Dividend yield?" — educational scaffolding

**UX/Design Approach**:
- **Education-first**: Learning is a core navigation item, not a sidebar
- **Visual**: Heavy use of charts, diagrams, and visual explanations
- **Guided**: Step-by-step tutorials for every feature
- **Chinese-first**: All content in Mandarin with TW market focus

**Unique Capabilities**:
- **Financial Statement Visualizer**: Interactive financial statement exploration with plain-language explanations — unique among TW brokers
- **Investment Checklist**: Pre-trade educational scaffolding — teaches beginners what to look for before buying
- **Market Sentiment Index**: Proprietary sentiment gauge — similar to our C35 (Market Mood Index)
- **Sector Rotation Visualizer**: Visual sector momentum tool — similar to our C51 (Sector Heatmap)

**Comparison with Stock Explorer**:

| Feature | 永豐金證券 | Stock Explorer |
|---|---|---|
| Stock Learning Lab | ✅ Structured courses | ⚠️ Did You Know facts |
| Financial Visualizer | ✅ Interactive | ❌ Not built |
| Investment Simulator | ✅ Paper trading | ❌ (positioning) |
| Sentiment Index | ✅ Proprietary gauge | ❌ Not built |
| Smart Alerts | ✅ AI-generated | ❌ Not built |
| Sector Visualizer | ✅ Rotation tool | ❌ Not built |
| Investment Checklist | ✅ Pre-trade education | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |

**Key Insight for Stock Explorer**: 永豐金證券's "Financial Statement Visualizer" is a unique interactive tool — tap on a financial statement line item and see a plain-language explanation. This is a more interactive version of our C33 (Glossary) concept. The "Investment Checklist" is a pre-trade educational tool that teaches beginners what to look for — this aligns with our "historian" positioning by teaching users HOW to analyze, not WHAT to buy. The "Market Sentiment Index" validates our C35 (Market Mood Index) concept.

---

### 7. 玉山證券 (E.SUN Securities)

**Positioning**: "Your trusted wealth management partner" — TW broker with strong beginner focus
**Target Users**: TW retail investors, especially beginners; known for customer service

**Key Features**:
- **"Beginner Village" (新手村)**: A dedicated onboarding experience for new investors — 7-step guided tutorial covering: what is a stock, how to read a chart, what is P/E, what is a dividend, how to place an order, how to manage risk, how to build a portfolio
- **"Investment Encyclopedia"**: Comprehensive glossary of financial terms with plain-language definitions and TW stock examples — similar to Investopedia's dictionary but localized for TW
- **"Smart Portfolio"**: AI-powered portfolio analysis showing diversification, risk level, and performance attribution — "Your portfolio is 60% tech stocks, which is higher than recommended"
- **"E.SUN Academy"**: Structured courses on investing fundamentals — video-based with quizzes and completion certificates
- **"Market Overview"**: Daily market summary with sector performance and top movers — similar to our C49 (Daily Market Pulse)
- **"Risk Meter"**: Visual risk indicator for every stock and portfolio — "This stock has a risk level of 7/10 due to high volatility"
- **"Investment Goals Planner"**: Interactive tool for setting investment goals and tracking progress — "You want to save NT$1M in 5 years, here's how"

**UX/Design Approach**:
- **Beginner-friendly**: Every feature is designed for first-time investors
- **Guided**: Step-by-step tutorials for every action
- **Clean**: Minimalist design with generous whitespace
- **Mobile-first**: Native app is the primary platform

**Unique Capabilities**:
- **Beginner Village**: 7-step onboarding — the most structured beginner experience among TW brokers
- **Investment Encyclopedia**: TW-localized financial glossary — similar to our C33 (Glossary)
- **Risk Meter**: Visual risk indicator — simpler than our C44 (Risk Analysis) but more accessible
- **Goals Planner**: Investment goal setting and tracking — unique among TW brokers

**Comparison with Stock Explorer**:

| Feature | 玉山證券 | Stock Explorer |
|---|---|---|
| Beginner Village | ✅ 7-step onboarding | ❌ Not built |
| Investment Encyclopedia | ✅ TW glossary | ❌ Not built (C33 pending) |
| Smart Portfolio | ✅ AI analysis | ❌ Not built |
| E.SUN Academy | ✅ Video courses | ⚠️ Did You Know facts |
| Market Overview | ✅ Daily summary | ❌ Not built |
| Risk Meter | ✅ Visual indicator | ❌ Not built |
| Goals Planner | ✅ Goal tracking | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |

**Key Insight for Stock Explorer**: 玉山證券's "Beginner Village" is the most structured onboarding experience among TW brokers — 7 steps that teach beginners the basics before they start investing. This is a model for how Stock Explorer could structure its own onboarding. The "Investment Encyclopedia" is exactly our C33 (Glossary) concept — validates demand in the TW market. The "Risk Meter" is a simpler version of our C44 (Risk Analysis) — a visual 1-10 risk indicator that beginners can understand instantly.

---

### 8. Magnify.money

**Positioning**: "AI-powered financial education that actually makes sense" — visual-first AI financial learning
**Target Users**: US and global retail investors who want to understand financial concepts through AI-generated visual explanations

**Key Features**:
- **AI Visual Explanations**: Users ask any financial question → AI generates a visual explanation with charts, diagrams, and plain-language text — "What is P/E ratio?" → AI generates an interactive chart showing P/E with real examples
- **"Explain This Company"**: Enter any stock ticker → AI generates a visual company profile with key metrics, business model explanation, and risk factors — all in plain language with custom visuals
- **"Compare Concepts"**: Side-by-side comparison of financial concepts — "P/E vs P/B" → visual comparison showing when to use each
- **"Interactive Calculators"**: Visual, interactive calculators for every financial concept — compound interest, DCF, valuation, etc. — users adjust sliders and see results in real-time
- **"Learning Paths"**: Structured learning paths from beginner to advanced — "Start with 'What is a stock?' → 'How to read financial statements' → 'Valuation techniques'"
- **"AI Quiz Generator"**: AI generates personalized quizzes based on what the user has been learning — adaptive difficulty
- **"Visual Glossary"**: Every financial term has a visual explanation — not just text, but a custom diagram or chart

**UX/Design Approach**:
- **AI-first**: AI generates all content — no static articles
- **Visual-first**: Every concept is explained with a custom visual
- **Interactive**: Users don't just read — they interact with sliders, charts, and calculators
- **Progressive**: Start simple, add complexity as user advances

**Unique Capabilities**:
- **AI-generated visual explanations**: Unique — AI creates custom charts and diagrams for every question
- **Interactive calculators**: Visual, real-time calculators for every financial concept
- **AI quiz generator**: Personalized quizzes based on learning history
- **Visual glossary**: Every term has a custom visual explanation

**Comparison with Stock Explorer**:

| Feature | Magnify.money | Stock Explorer |
|---|---|---|
| AI Visual Explanations | ✅ Custom visuals | ❌ Not built |
| Explain This Company | ✅ AI-generated | ✅ Business card page |
| Compare Concepts | ✅ Side-by-side | ❌ Not built |
| Interactive Calculators | ✅ Visual, real-time | ❌ Not built |
| Learning Paths | ✅ Structured | ⚠️ Did You Know facts |
| AI Quiz Generator | ✅ Adaptive | ❌ Not built |
| Visual Glossary | ✅ Custom diagrams | ❌ Not built (C33 pending) |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ❌ US focus | ✅ Deep coverage |

**Key Insight for Stock Explorer**: Magnify.money is the most aligned competitor with Stock Explorer's "education-first" positioning — both platforms prioritize visual, plain-language explanations of financial concepts. The "AI Visual Explanations" feature is a more advanced version of our analogy engine — instead of pre-written analogies, AI generates custom visuals on the fly. The "Interactive Calculators" are a feature Stock Explorer doesn't have — visual, real-time tools for exploring financial concepts. The "Compare Concepts" feature is a unique educational tool — side-by-side comparison of financial concepts (P/E vs P/B) that helps beginners understand when to use each metric.

---

### 9. Tastytrade (tastytrade.com)

**Positioning**: "Learn to trade, not follow" — education-first options and futures platform
**Target Users**: US options traders who want to understand what they're doing, not just follow signals

**Key Features**:
- **"Learn → Paper Trade → Live Trade" Pipeline**: Structured progression from education to practice to live trading — each stage has its own interface and tools
- **"Tastytrade Education Library"**: 100+ hours of free video content on options, futures, and portfolio management — taught by experienced traders with plain-language explanations
- **"Probability Analysis"**: Every trade shows the probability of profit — "This trade has a 65% chance of profit" — teaches probabilistic thinking
- **"Risk Visualization"**: Every position shows a visual risk profile — "Here's your max gain, max loss, and breakeven point" — visual P&L diagrams
- **"Market Analysis"**: Daily market analysis with plain-language explanations of what's happening and why — "The VIX is up 10%, which means options are more expensive"
- **"Portfolio Risk Management"**: Visual portfolio-level risk analysis — "Your portfolio is net long delta, which means you profit if the market goes up"
- **"Trade Journal"**: Built-in journaling for every trade — record rationale, outcome, and lessons learned
- **"Community"**: Active community with live streams, chat rooms, and discussion boards — education-focused, not signal-focused

**UX/Design Approach**:
- **Education-first**: Education is the primary product, trading is secondary
- **Visual**: Every concept is taught with visual diagrams and charts
- **Probabilistic**: Teaches probability-based thinking, not prediction-based
- **Community-driven**: Live streams and chat rooms for real-time learning

**Unique Capabilities**:
- **Learn → Paper Trade → Live Trade pipeline**: Structured progression from education to practice
- **Probability analysis**: Every trade shows probability of profit — teaches probabilistic thinking
- **Risk visualization**: Visual P&L diagrams for every position
- **Trade journal**: Built-in reflection tool for every trade

**Comparison with Stock Explorer**:

| Feature | Tastytrade | Stock Explorer |
|---|---|---|
| Education Pipeline | ✅ Learn → Practice → Live | ❌ Not applicable |
| Probability Analysis | ✅ Every trade | ❌ Not applicable |
| Risk Visualization | ✅ Visual P&L | ❌ Not built |
| Trade Journal | ✅ Built-in | ❌ Not built |
| Market Analysis | ✅ Daily with education | ❌ Not built |
| Community | ✅ Live streams | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ❌ US focus | ✅ Deep coverage |
| Probabilistic Thinking | ✅ Core philosophy | ⚠️ Historian positioning |

**Key Insight for Stock Explorer**: Tastytrade's "probability analysis" and "risk visualization" are unique features that teach probabilistic thinking — "This has a 65% chance of profit" rather than "This will make money." This is philosophically aligned with Stock Explorer's "historian" positioning — instead of predicting the future, explain the probabilities. The "trade journal" is similar to 元大證券's "Investment Diary" — a reflection tool that encourages learning from past decisions. The "Learn → Paper Trade → Live Trade" pipeline is a structured progression model that Stock Explorer could adapt for its own education features.

---

## Updated Competitor Overview Table (Round 12 Additions)

| Dimension | eToro | Webull | Robinhood | 富邦e富 | 元大證券 | 永豐金證券 | 玉山證券 | Magnify.money | Tastytrade | **Stock Explorer** |
|---|---|---|---|---|---|---|---|---|---|---|
| **Positioning** | Social Investing | Commission-Free | Investing for All | AI Companion | AI Selection | Education Focus | Beginner Village | AI Visual Ed | Education Pipeline | Beginner Education ("Historian") |
| **Social Learning** | ✅ CopyTrader | ✅ Community | ❌ | ✅ Following | ❌ | ❌ | ❌ | ❌ | ✅ Community | ❌ MISSING |
| **Education** | ✅ Academy | ✅ Learn | ✅ Learn+Earn | ✅ eRich Academy | ✅ Knowledge Base | ✅ Learning Lab | ✅ E.SUN Academy | ✅ AI Visual | ✅ 100+ hrs | ✅ Core |
| **AI Features** | ⚠️ Risk Score | ✅ Alerts | ❌ | ✅ Compass | ✅ Chatbot+Screen | ✅ Alerts | ✅ Smart Portfolio | ✅ Full AI | ❌ | ❌ MISSING |
| **Visual Analysis** | ⚠️ Cards | ⚠️ Charts | ⚠️ Minimal | ✅ Portfolio | ✅ Comparison | ✅ Visualizer | ✅ Risk Meter | ✅ Custom Visuals | ✅ P&L Diagrams | ✅ PPT-style |
| **Notifications** | ✅ Push | ✅ Push | ✅ Push | ✅ AI Smart | ✅ Alerts | ✅ Smart | ✅ Push | ❌ | ✅ Email | ❌ MISSING |
| **Glossary/Tooltips** | ⚠️ Some | ⚠️ Some | ✅ Metric Tooltips | ❌ | ❌ | ✅ Visualizer | ✅ Encyclopedia | ✅ Visual Glossary | ❌ | ❌ MISSING (C33) |
| **Risk Visualization** | ✅ 1-10 Score | ⚠️ Basic | ⚠️ Options | ✅ AI Analysis | ✅ Assessment | ✅ Checklist | ✅ Risk Meter | ✅ Interactive | ✅ P&L Visual | ❌ MISSING (C44) |
| **Daily Engagement** | ✅ Feed | ✅ Classroom | ✅ Snacks | ✅ AI News | ✅ Market Pulse | ✅ Sentiment | ✅ Market Overview | ❌ | ✅ Analysis | ❌ MISSING |
| **Mobile App** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ⚠️ Web | ✅ Native | ❌ Streamlit only |
| **TW Market** | ⚠️ Limited | ⚠️ Limited | ❌ US | ✅ Deep | ✅ Deep | ✅ Deep | ✅ Deep | ❌ US | ❌ US | ✅ Deep |
| **Free** | ⚠️ Freemium | ✅ Free | ✅ Free | ✅ Free | ✅ Free | ✅ Free | ✅ Free | ⚠️ Freemium | ✅ Free | ✅ Free |

---

## New Feature Ideas from Round 12

### [ISSUE-C55] "Investment Diary" — Personal Reflection Journal
- **Source**: Competitor research round 12 (元大證券 "Investment Diary", Tastytrade "Trade Journal")
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Historian" positioning
- **Description**: 元大證券's "Investment Diary" and Tastytrade's "Trade Journal" both allow users to record their thinking about stocks — why they're interested, what they expect, what they learned. Stock Explorer has no reflection mechanism — users read about companies but never record their own thoughts. An "Investment Diary" would: (1) let users add personal notes to any company page, (2) track their notes over time, (3) connect notes to actual outcomes ("You noted TSMC's high capital expenditure 3 months ago — here's what happened since"), (4) serve as a personal learning archive. This is the ultimate "historian" feature — users become historians of their own investment journey.
- **Implementation**: Add a "📝 投資筆記" section to each company page with a text input. Store notes in session state (or local file). Add a "My Diary" page showing all notes chronologically with links back to company pages. Optionally connect notes to events ("You wrote this before the earnings report — here's what happened").
- **Competitive Gap**: 🔴 No TW competitor has personal reflection journaling; 元大證券/Tastytrade prove demand; unique "historian of self" differentiator

---

### [ISSUE-C56] "Explain This Metric" — Interactive Financial Concept Explainer
- **Source**: Competitor research round 12 (Magnify.money "AI Visual Explanations", 永豐金證券 "Financial Statement Visualizer", Robinhood "Metric Tooltips")
- **Priority**: P1
- **Effort**: 12-16h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + Core value #1 "Story first"
- **Description**: Magnify.money generates AI visual explanations for any financial concept. 永豐金證券's Financial Statement Visualizer lets users tap on any line item for a plain-language explanation. Robinhood has metric tooltips on every stock page. Stock Explorer currently shows metrics with analogies but no interactive "explain this" feature. An "Explain This Metric" feature would: (1) add an "❓" button next to every metric on the business card page, (2) clicking it opens a visual explanation with a chart, analogy, and real-world example, (3) explanations are generated from templates (not AI) with TW stock data, (4) each explanation includes "Why this matters" and "What to watch for." This is a more interactive version of C33 (Glossary) — instead of a static glossary, users get contextual explanations for every metric they encounter.
- **Implementation**: Create `src/data/metric_explanations.yaml` with metric → explanation + analogy + example + "why it matters." Add an "❓" button next to every metric that opens an expander with the explanation. Use Plotly for mini-charts showing the metric's historical trend. Prioritize the 10 most common metrics (ROE, P/E, P/B, gross margin, revenue growth, dividend yield, debt ratio, EPS, free cash flow, institutional ownership).
- **Competitive Gap**: 🔴 No TW competitor has interactive metric explanations with visual aids; Magnify.money/Robinhood/永豐 prove demand; directly addresses "ten-second test"

---

### [ISSUE-C57] "Compare Concepts" — Financial Concept Comparison Tool
- **Source**: Competitor research round 12 (Magnify.money "Compare Concepts")
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + Core value #5 "Benchmark-oriented analysis"
- **Description**: Magnify.money has a "Compare Concepts" feature that shows side-by-side comparisons of financial concepts — "P/E vs P/B: when to use each." Stock Explorer has peer comparison (company vs company) but no concept comparison (metric vs metric). A "Compare Concepts" tool would: (1) let users select two financial concepts (e.g., ROE vs ROA, P/E vs P/B, dividend yield vs payout ratio), (2) show a side-by-side comparison with definitions, formulas, when to use each, and real TW stock examples, (3) include a "Which is better for this company?" analysis that explains which metric is more relevant for the current stock. This helps beginners understand that financial metrics are tools, not answers — you choose the right tool for the job.
- **Implementation**: Add a "📊 概念比較" page accessible from the navbar. Users select two concepts from a dropdown. The page shows: definitions, formulas, pros/cons, when to use each, and a real TW stock example comparing both metrics. Content is pre-written for the 10 most common concept pairs.
- **Competitive Gap**: 🟡 No TW competitor has concept comparison; Magnify.money proves demand; unique educational differentiator

---

### [ISSUE-C58] "Beginner Onboarding Flow" — Guided First Experience
- **Source**: Competitor research round 12 (玉山證券 "Beginner Village" 7-step onboarding, Robinhood "First Stock" guided experience, eToro "Virtual Portfolio" practice)
- **Priority**: P1
- **Effort**: 14-20h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + beginner-friendly
- **Description**: 玉山證券's "Beginner Village" is a 7-step guided onboarding that teaches beginners the basics before they start. Robinhood's "First Stock" is a step-by-step tutorial for buying your first stock. Stock Explorer has no onboarding — users land on the homepage and must figure out what to do. A "Beginner Onboarding Flow" would: (1) detect first-time user (session state), (2) show a 5-step guided tour: "Welcome to Stock Explorer → Search for a company → Read the business card → Explore the event dashboard → Try the watchlist," (3) each step highlights the relevant UI element with a tooltip, (4) at the end, suggest 3 beginner-friendly companies to explore (e.g., TSMC, 鴻海, 富邦媒), (5) offer a "Beginner Guide" PDF download. This directly addresses the #1 UX complaint: "I don't know where to start."
- **Implementation**: Add a session state flag `onboarding_complete`. If False, show a modal with the 5-step tour. Use Streamlit's `st.tooltip` or custom CSS overlays for step highlighting. Store completion in session state. Add a "Help" button in the navbar to replay the tour.
- **Competitive Gap**: 🔴 No TW competitor has structured onboarding for stock analysis tools; 玉山證券/Robinhood prove demand; critical for beginner retention

---

### [ISSUE-C59] "AI Q&A Chatbot" — Natural Language Stock Questions
- **Source**: Competitor research round 12 (元大證券 "Investment Chatbot", Finimize "Ask Finimize", Magnify.money "AI Visual Explanations")
- **Priority**: P2
- **Effort**: 16-24h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction"
- **Description**: 元大證券 has an AI chatbot that answers natural language questions about stocks — "What is TSMC's revenue growth?" → plain-language answer with data. Finimize's "Ask Finimize" answers any financial question. Stock Explorer has no Q&A mechanism — users must navigate to find information. An "AI Q&A Chatbot" would: (1) provide a chat interface where users ask questions about any stock, (2) answer with plain-language explanations using existing analogy engine + FinMind data, (3) support questions like "What happened to TSMC last quarter?", "How does TSMC make money?", "What are the risks?", (4) suggest follow-up questions to guide learning. This is the most natural way for beginners to explore — they ask questions in their own words.
- **Implementation**: Add a "💬 問問股識" page with a chat interface. Use pattern matching (not LLM) to map questions to pre-built responses: "revenue" → show revenue chart + plain-language summary, "risk" → show C44 risk analysis, "dividend" → show dividend data. Integrate with existing analogy engine for plain-language responses. Suggest 3 follow-up questions after each answer.
- **Competitive Gap**: 🟡 元大證券 has AI chatbot but only for their own platform; no TW competitor has Q&A for stock analysis; natural language interface for beginners

---

### [ISSUE-C60] "Concept Mastery Badges" — Gamified Learning Achievement System
- **Source**: Competitor research round 12 (Robinhood "Learn → Earn" stock rewards, Khan Academy badges, Finimize completion certificates)
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + engagement
- **Description**: Robinhood rewards users with stock for completing educational modules. Khan Academy has achievement badges. Finimize gives completion certificates. Stock Explorer has no gamification — users explore companies but get no recognition for learning. "Concept Mastery Badges" would: (1) award badges for learning milestones — "Read 5 company analyses" → 📚 Reader badge, "Completed 10 quizzes" → 🧪 Quiz Master badge, "Explored 3 sectors" → 🌐 Sector Explorer badge, (2) badges are displayed on a "Learning Profile" page, (3) each badge links to the companies/concepts that earned it, (4) badges are shareable (connects to C53 Social Sharing). This creates a positive feedback loop — learning → badges → sharing → more learning.
- **Implementation**: Add a `badges.yaml` definition file with badge criteria. Track user actions in session state (companies viewed, quizzes completed, features used). Award badges when criteria are met. Display badges on a "🏆 學習成就" page. Integrate with C52 (Quiz Mode) and C50 (Learning Progress Tracker) when built.
- **Competitive Gap**: 🟡 No TW competitor has gamified learning badges; Robinhood/Khan Academy prove demand; drives engagement and retention

---

### [ISSUE-C61] "Sector Rotation Visualizer" — Market Momentum Map
- **Source**: Competitor research round 12 (永豐金證券 "Sector Rotation Visualizer", StockEdge sector heatmaps, Moomoo "Market Heatmap with Education")
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #5 "Benchmark-oriented analysis" + Core value #3 "Adaptive and self-evolving"
- **Description**: 永豐金證券's "Sector Rotation Visualizer" shows which sectors are gaining/losing momentum over time — not just "which sectors are up today" but "which sectors are rotating from bearish to bullish." Stock Explorer's planned C51 (Sector Heatmap) shows a static snapshot. A "Sector Rotation Visualizer" would add the time dimension: (1) show sector momentum over 1 week, 1 month, and 3 months, (2) highlight sectors that are "rotating" (changing direction), (3) plain-language explanation: "Semiconductor sector has been bearish for 3 months but started turning bullish last week — driven by AI chip demand recovery," (4) connect to individual companies: "If you're interested in semiconductors, here are the top 3 companies in this sector." This is a more dynamic version of C51 that aligns with the "historian" positioning — explaining what's happening, not predicting what will happen.
- **Implementation**: Extend C51 (Sector Heatmap) with a time-series view. Use FinMind sector performance data. Add a time selector (1W/1M/3M) and highlight sectors with significant momentum changes. Plain-language explanations generated from templates.
- **Competitive Gap**: 🟡 永豐金證券 has sector rotation but without plain-language explanations; no TW competitor combines sector rotation with educational context

---

### [ISSUE-C62] "Pre-Investment Checklist" — Educational Scaffolding Tool
- **Source**: Competitor research round 12 (永豐金證券 "Investment Checklist", Tastytrade "Learn → Paper Trade → Live Trade" pipeline)
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Historian" positioning
- **Description**: 永豐金證券's "Investment Checklist" is a pre-trade educational tool — before buying a stock, users complete a checklist of key metrics to check. Tastytrade's pipeline teaches users before they trade. Stock Explorer has no educational scaffolding — users read about companies but don't know what to look for. A "Pre-Investment Checklist" would: (1) appear at the bottom of each company page as a "📋 投資前檢查清單," (2) list 5-7 key items to check: "Do you understand what this company does? → Have you checked the P/E ratio? → Have you looked at the debt level? → Do you know the main risks? → Have you compared it to its peers? → Do you understand the sector dynamics? → Have you checked recent events?," (3) each item is clickable → scrolls to the relevant section on the page, (4) checking off items is optional and tracked in session state, (5) the checklist is educational, not prescriptive — it teaches users what to look for, not what to do. This is the "historian" positioning in action: "Here's what you should understand before making a decision."
- **Implementation**: Add a collapsible "📋 投資前檢查清單" section at the bottom of the business card page. Each item is a checkbox with a label. Clicking an item scrolls to the relevant section (using anchor links). Progress tracked in session state. No data is stored — this is a learning tool, not a recommendation.
- **Competitive Gap**: 🔴 No TW competitor has educational scaffolding checklists; 永豐金證券 proves demand; perfect "historian" differentiator

---

## Key Insights from Round 12

### 1. **Social Learning is the Dominant Engagement Model (Confirmed)**
eToro (CopyTrader), 富邦e富 (social following), Webull (community), and Tastytrade (live streams) all use social learning as a core engagement mechanism. Stock Explorer remains entirely solo-learning. While full social features may be out of scope, lightweight social elements (sharing, following, community discussion) would dramatically improve engagement.

### 2. **AI is Becoming Table Stakes in TW Market**
富邦e富 (AI Investment Compass), 元大證券 (AI Chatbot + Natural Language Screening), and 永豐金證券 (AI Alerts) all have AI features. The TW broker market is rapidly adopting AI. Stock Explorer's "historian" positioning deliberately avoids AI stock-picking, but AI-powered explanations (C56, C59) and AI Q&A could complement the structured analysis without compromising the positioning.

### 3. **Interactive Education is the New Standard**
Magnify.money (AI Visual Explanations), 永豐金證券 (Financial Statement Visualizer), and Robinhood (Metric Tooltips) all provide interactive, visual explanations of financial concepts. Static text is no longer sufficient — users expect to click, explore, and interact with educational content. Stock Explorer's analogy engine is a good foundation but needs interactive delivery (C56).

### 4. **Onboarding is Critical for Beginner Retention**
玉山證券 (Beginner Village), Robinhood (First Stock), and eToro (Virtual Portfolio) all have structured onboarding experiences. Stock Explorer has no onboarding — users must figure out the product themselves. This is the #1 UX gap for beginner users (C58).

### 5. **Gamification Drives Engagement**
Robinhood (Learn → Earn with stock rewards), Khan Academy (badges), and Finimize (certificates) all use gamification to drive learning engagement. Stock Explorer has no gamification — users learn but get no recognition. Concept Mastery Badges (C60) would create a positive feedback loop.

### 6. **TW Broker Apps are Direct Competitors with Education Features**
富邦e富, 元大證券, 永豐金證券, and 玉山證券 all have education features integrated into their broker apps. These are direct TW competitors targeting the same users. Stock Explorer's advantage is depth of analysis and "historian" positioning, but the broker apps have advantages in: mobile apps, notifications, AI features, and integrated trading. Stock Explorer must differentiate through educational depth and unique "historian" features.

### 7. **Reflection Tools are a White Space**
元大證券 (Investment Diary) and Tastytrade (Trade Journal) both have journaling/reflection tools. No TW competitor has a personal reflection journal for stock analysis. This is a unique "historian" feature — users become historians of their own investment journey (C55).

---

## Feature Gap Summary (Round 12)

| ID | Title | Priority | Effort | Source Competitor | Alignment |
|---|---|---|---|---|---|
| C55 | Investment Diary (Personal Reflection Journal) | P2 | 10-14h | 元大證券, Tastytrade | Story first + Historian |
| C56 | Explain This Metric (Interactive Concept Explainer) | P1 | 12-16h | Magnify.money, 永豐金證券, Robinhood | Point-to-point + Ten-second test |
| C57 | Compare Concepts (Financial Concept Comparison) | P2 | 10-14h | Magnify.money | Point-to-point + Benchmark |
| C58 | Beginner Onboarding Flow (Guided First Experience) | P1 | 14-20h | 玉山證券, Robinhood, eToro | Point-to-point + Ten-second test |
| C59 | AI Q&A Chatbot (Natural Language Stock Questions) | P2 | 16-24h | 元大證券, Finimize, Magnify.money | Story first + Point-to-point |
| C60 | Concept Mastery Badges (Gamified Learning) | P2 | 8-12h | Robinhood, Khan Academy, Finimize | Point-to-point + Engagement |
| C61 | Sector Rotation Visualizer (Market Momentum Map) | P2 | 10-14h | 永豐金證券, StockEdge, Moomoo | Benchmark + Adaptive |
| C62 | Pre-Investment Checklist (Educational Scaffolding) | P2 | 8-12h | 永豐金證券, Tastytrade | Story first + Historian |

---

## Recommendations

### Immediate (Next Sprint)
1. **C56 Explain This Metric** — P1 gap, directly addresses "ten-second test," multiple competitors prove demand (Magnify.money, Robinhood, 永豐金證券). Highest ROI: 12-16h for interactive metric explanations that transform every data point into a learning opportunity.
2. **C58 Beginner Onboarding Flow** — P1 gap, critical for beginner retention, 玉山證券/Robinhood prove demand. Without onboarding, beginners bounce before discovering Stock Explorer's value.

### Short-Term (Sprint 2-3)
3. **C62 Pre-Investment Checklist** — Low effort (8-12h), perfect "historian" differentiator, 永豐金證券 proves demand. Teaches users what to look for, not what to buy.
4. **C55 Investment Diary** — Unique "historian of self" feature, 元大證券/Tastytrade prove demand. Transforms Stock Explorer from a lookup tool into a personal learning platform.
5. **C60 Concept Mastery Badges** — Gamification drives engagement, Robinhood/Khan Academy prove demand. Creates positive feedback loop for learning.

### Medium-Term (Post-Sprint 3)
6. **C59 AI Q&A Chatbot** — Natural language interface for beginners, 元大證券/Finimize prove demand. Most ambitious feature (16-24h) but highest long-term value.
7. **C57 Compare Concepts** — Unique educational tool, Magnify.money proves demand. Helps beginners understand financial metrics as tools, not answers.
8. **C61 Sector Rotation Visualizer** — Extends C51 with time dimension, 永豐金證券 proves demand. More dynamic market overview for "historian" positioning.

---

*This is the twelfth competitor research round. Eight new feature suggestions identified (C55-C62). The most impactful new gap is C56 (Explain This Metric) — it directly addresses the "ten-second test" design principle, multiple international and TW competitors prove demand, and it transforms every data point into a learning opportunity. The most strategically important gap is C58 (Beginner Onboarding Flow) — without onboarding, beginners bounce before discovering Stock Explorer's value, making all other features irrelevant. The most unique gap is C55 (Investment Diary) — no TW competitor has personal reflection journaling, making it a perfect "historian of self" differentiator.*

---

# Stock Explorer Competitor Research Report — Round 13

> **Date**: 2026-06-18
> **Author**: QA Engineer (Round 13)
> **Purpose**: Research 8 new competitors not covered in Rounds 1-12, focusing on Korean/Japanese stock education platforms, Chinese-language stock education, podcast/audio finance education, gamified investing education, newsletter-first finance education, and community-driven stock analysis
> **Previous Rounds**: Rounds 1-12 covered: StatementDog, GoodInfo, CMoney, WantGoo, Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, The Motley Fool, NerdWallet, JZ Invest, 鉅亨網, TEJ, Yahoo奇摩股市, Simply Wall St, Stockopedia, Investopedia, Morningstar, TradingView, TipRanks, Finimize, Zerodha Varsity, StockEdge, Tickeron, Khan Academy Finance, Stake, Moomoo, eToro, Webull, Robinhood, 富邦e富, 元大證券, 永豐金證券, 玉山證券, Magnify.money, Tastytrade.

---

## New Competitors Analyzed (Not in Rounds 1-12)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **Naver Finance (네이버 금융)** | Financial Portal + Community | Korea | 🔴 High — Korea's #1 finance platform; "Knowledge iN" Q&A community; plain-language explanations |
| **Kabutan (かぶ探)** | Stock Education + Screening | Japan | 🔴 High — "Kabutan Academy" with structured visual lessons; beginner-focused stock screening with plain-language |
| **雪球 (Xueqiu)** | Social Investing + Education | China | 🔴 High — "Snowball Academy" + social learning feed; story-driven stock analysis; 20M+ users |
| **The Indicator (NPR)** | Daily Finance Podcast | US | 🟡 Medium — 10-minute daily market stories; narrative-first approach; audio learning modality |
| **Wall Street Survivor** | Gamified Investing Education | US/Global | 🔴 High — stock game + structured courses; "learn by doing" model; virtual portfolio competitions |
| **Morning Brew (Business)** | Newsletter-First Business Education | US/Global | 🟡 Medium — 5-minute daily business newsletter; plain-language storytelling; 3M+ subscribers |
| **Dcard 股票版 (Dcard Stocks)** | Community-Driven Stock Discussion | TW | 🔴 High — Taiwan's largest student/community forum; anonymous stock discussion; peer learning |
| **r/investing (Reddit)** | Community-Driven Stock Analysis | US/Global | 🟡 Medium — 2.5M+ members; wiki-style education; community-curated knowledge base |

---

## Detailed Competitor Profiles

### 1. Naver Finance (네이버 금융)

**URL**: https://finance.naver.com
**Positioning**: Korea's #1 financial portal — comprehensive data + community + education
**Target Users**: Korean retail investors from beginner to advanced; 30M+ monthly users

**Key Features**:
- **"Knowledge iN" (지식iN) Q&A Community**: Users ask stock-related questions → community answers with plain-language explanations. Similar to Yahoo Answers but specialized for finance. Top answers are upvoted and featured. This is a peer-education mechanism where beginners learn from community knowledge.
- **"Naver Academy" (네이버 아카데미)**: Structured video courses on investing fundamentals, stock analysis, and financial planning. Each course is 10-20 minutes with quizzes and completion certificates.
- **"Stock Story" (스토리)**: Each stock has a narrative summary — "What does this company do?" in plain language with infographic-style visuals. Similar to Stock Explorer's one-liner concept but with more visual elements.
- **"Beginner's Guide" (초보자 가이드)**: A dedicated section for new investors with step-by-step tutorials on: what is a stock, how to read charts, what is P/E, how to place an order.
- **"Financial Dictionary" (용어사전)**: 5,000+ financial terms with plain-language definitions and examples. Searchable and categorized.
- **"Community Lounge" (커뮤니티)**: Stock-specific discussion boards with real-time chat. Users share analysis, news, and opinions.
- **"AI Investment Assistant" (AI 투자 비서)**: AI-powered assistant that answers questions about stocks and markets in plain language.

**UX/Design Approach**:
- **Portal-style**: Dense information organized in panels and tabs
- **Community-integrated**: Every stock page has a "Knowledge iN" Q&A section
- **Mobile-first**: Naver app is the primary platform
- **Korean-language only**: Deep localization for Korean market

**Unique Capabilities**:
- **Knowledge iN Q&A**: Community-driven Q&A with upvoted answers — peer education at scale
- **Stock Story**: Narrative summaries for every stock — similar to Stock Explorer's one-liner
- **AI Investment Assistant**: Natural language Q&A about stocks — similar to 元大證券's chatbot

**Comparison with Stock Explorer**:

| Feature | Naver Finance | Stock Explorer |
|---|---|---|
| Community Q&A | ✅ Knowledge iN | ❌ Not built |
| Stock Story | ✅ Narrative summary | ✅ One-liner |
| Structured Courses | ✅ Naver Academy | ⚠️ Did You Know facts |
| Financial Dictionary | ✅ 5,000+ terms | ❌ Not built (C33 pending) |
| AI Assistant | ✅ Natural language | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| PPT-style | ❌ Portal style | ✅ Unique |
| TW Market | ❌ Korea focus | ✅ Deep coverage |
| Mobile App | ✅ Native | ❌ Streamlit only |

**Key Insight for Stock Explorer**: Naver Finance's "Knowledge iN" Q&A is a powerful peer-education mechanism — beginners ask questions, the community answers, and the best answers rise to the top. This is a social learning model that Stock Explorer completely lacks. The "Stock Story" concept validates Stock Explorer's one-liner approach — both platforms recognize that beginners need a narrative summary before diving into data. The "Financial Dictionary" (5,000+ terms) is exactly our C33 (Glossary) concept — validates demand in the Korean market.

---

### 2. Kabutan (かぶ探)

**URL**: https://kabutan.jp
**Positioning**: "Make stock investing accessible to everyone" — Japan's leading stock education and screening platform
**Target Users**: Japanese retail investors, especially beginners; 5M+ monthly users

**Key Features**:
- **"Kabutan Academy" (かぶ探アカデミー)**: Structured video courses on stock investing fundamentals — 20+ courses organized by difficulty (beginner → intermediate → advanced). Each course is 5-10 minutes with visual illustrations and quizzes.
- **"Kabutan Score"**: Proprietary stock scoring system (0-100) based on: business quality, growth potential, valuation, financial health, and market sentiment. Each score has a plain-language explanation.
- **"Stock Story" (銘柄ストーリー)**: Each stock has a narrative summary explaining what the company does, how it makes money, and what its competitive advantage is — all in plain language with infographic-style visuals.
- **"Screening with Stories" (スクリーニング + ストーリー)**: Stock screening that returns results with narrative summaries — not just numbers, but "why this stock is interesting" in plain language.
- **"Beginner Mode" (ビギナーモード)**: A simplified view that hides advanced metrics and shows only the essentials — one-liner, key metrics (3-4), and "Did You Know?" facts. Users can toggle to "Advanced Mode" for full data.
- **"Financial Glossary" (用語集)**: 3,000+ financial terms with plain-language definitions, examples, and illustrations.
- **"Daily Market Pulse" (マーケットパルス)**: Daily market summary with sector heatmap and top movers — plain-language explanation of what happened and why.
- **"Investment Diary" (投資日記)**: Users can record their investment thinking and track their learning over time.

**UX/Design Approach**:
- **Visual-first**: Every concept is explained with illustrations and diagrams
- **One concept per page**: Similar to Stock Explorer's PPT-style — one key idea per screen
- **Beginner-friendly**: Plain language, no jargon without explanation
- **Mobile-first**: Native app is the primary platform
- **Japanese-language only**: Deep localization for Japanese market

**Unique Capabilities**:
- **Kabutan Score**: Proprietary scoring with plain-language explanations — similar to our C43 (Snowflake Health) but with narrative explanations
- **Screening with Stories**: Stock screening that includes narrative summaries — combines C42 (Screener) with C34 (Story Timeline)
- **Beginner Mode toggle**: Simplified view for beginners — similar to our C40 (Beginner/Expert Mode)
- **Investment Diary**: Personal reflection journaling — similar to our C55 (Investment Diary)

**Comparison with Stock Explorer**:

| Feature | Kabutan | Stock Explorer |
|---|---|---|
| Kabutan Score | ✅ 0-100 with narrative | ❌ Not built (C43 pending) |
| Stock Story | ✅ Narrative summary | ✅ One-liner |
| Structured Courses | ✅ 20+ video courses | ⚠️ Did You Know facts |
| Beginner Mode | ✅ Toggle | ❌ Not built (C40 pending) |
| Screening + Stories | ✅ Combined | ❌ Not built |
| Investment Diary | ✅ Journaling | ❌ Not built (C55 pending) |
| Financial Glossary | ✅ 3,000+ terms | ❌ Not built (C33 pending) |
| Plain-language | ✅ Core feature | ✅ Core feature |
| PPT-style | ✅ One concept per page | ✅ PPT-style |
| TW Market | ❌ Japan focus | ✅ Deep coverage |

**Key Insight for Stock Explorer**: Kabutan is the closest philosophical match to Stock Explorer in the Japanese market. Both platforms share: plain-language explanations, visual-first design, one concept per page, beginner-friendly approach, and education-first positioning. The "Screening with Stories" feature is a unique combination of stock screening and narrative summaries — this is a feature that Stock Explorer's planned C42 (Screener) and C34 (Story Timeline) could be combined into. The "Beginner Mode" toggle is exactly our C40 concept — validates demand in the Japanese market. The "Investment Diary" validates our C55 concept.

---

### 3. 雪球 (Xueqiu)

**URL**: https://xueqiu.com
**Positioning**: "The world's largest Chinese-language investment community" — social investing + education + storytelling
**Target Users**: Chinese-speaking retail investors globally; 20M+ registered users

**Key Features**:
- **"Snowball Academy" (雪球学院)**: Structured courses on investing fundamentals — 30+ courses organized by topic (stocks, funds, macroeconomics, valuation). Each course is 10-15 minutes with real stock examples and quizzes. Completion certificates available.
- **"Snowball Story" (雪球故事)**: Each stock has a narrative "story" — "What does this company do? How does it make money? What's its competitive advantage?" — written in plain language with infographic-style visuals. Users can also write their own "stock stories" and share them.
- **"Social Learning Feed" (动态)**: A Twitter-like feed where users share stock analysis, commentary, and lessons. "Beginner" filter available. Users learn by reading others' analysis — social learning at scale.
- **"Stock Annotation" (股票注解)**: Users can annotate any stock page with their own analysis, questions, and insights. Annotations are upvoted and the best ones are featured — similar to Genius.com's annotation model.
- **"Xueqiu Score" (雪球评分)**: Proprietary stock scoring system (0-100) based on: business quality, management, financial health, valuation, and market sentiment. Each score has a plain-language explanation.
- **"Investment Diary" (投资日记)**: Users can record their investment thinking and track their learning over time. Diaries can be shared publicly for community feedback.
- **"Community Q&A" (问答)**: Users ask stock-related questions → community answers with plain-language explanations. Top answers are upvoted and featured.
- **"Sector Heatmap" (板块热力图)**: Visual sector heatmap showing which sectors are hot/cold with plain-language explanations.

**UX/Design Approach**:
- **Social-first**: The feed is the homepage — content discovery through community
- **Story-driven**: Every stock has a narrative summary — "story first, data second"
- **Annotation-rich**: Users can annotate any content — collaborative knowledge building
- **Mobile-first**: Native app is the primary platform
- **Chinese-language**: Mandarin-focused with global Chinese-speaking audience

**Unique Capabilities**:
- **Stock Annotation**: Users annotate stock pages with their own analysis — collaborative knowledge building
- **Social Learning Feed**: Twitter-like feed of stock analysis — social learning at scale
- **User-generated Stories**: Users write and share their own "stock stories" — community-generated education
- **Investment Diary with Sharing**: Personal journaling that can be shared for community feedback

**Comparison with Stock Explorer**:

| Feature | 雪球 (Xueqiu) | Stock Explorer |
|---|---|---|
| Snowball Academy | ✅ 30+ courses | ⚠️ Did You Know facts |
| Stock Story | ✅ Narrative + user-generated | ✅ One-liner |
| Social Learning Feed | ✅ Twitter-like | ❌ Not built |
| Stock Annotation | ✅ Collaborative | ❌ Not built |
| Xueqiu Score | ✅ 0-100 with narrative | ❌ Not built (C43 pending) |
| Investment Diary | ✅ With sharing | ❌ Not built (C55 pending) |
| Community Q&A | ✅ Upvoted-based | ❌ Not built |
| Sector Heatmap | ✅ With education | ❌ Not built (C51 pending) |
| Plain-language | ✅ Core feature | ✅ Core feature |
| Story first | ✅ Core philosophy | ✅ Core philosophy |
| TW Market | ⚠️ China focus | ✅ Deep coverage |

**Key Insight for Stock Explorer**: 雪球's "story first, data second" philosophy is identical to Stock Explorer's core value #1. The "Stock Story" concept (user-generated narrative summaries) is a more social version of Stock Explorer's one-liner. The "Stock Annotation" feature is a unique collaborative knowledge-building mechanism — users add their own analysis to stock pages, creating a community-curated knowledge base. The "Social Learning Feed" is a more engaging version of our planned C49 (Daily Market Pulse) — instead of a single daily summary, it's a continuous feed of community-generated analysis. 雪球 proves that the "story first" approach works at scale (20M+ users).

---

### 4. The Indicator from Planet Money (NPR)

**URL**: https://www.npr.org/sections/money/
**Positioning**: "The economy explained in 10 minutes a day" — daily finance podcast with narrative-first approach
**Target Users**: General public, beginners, commuters; 5M+ monthly downloads

**Key Features**:
- **10-minute Daily Episodes**: Every weekday, a 10-minute episode explaining one economic or market concept in plain language with real-world stories. "What happened in the economy today" told as a story, not a news report.
- **Narrative-First Approach**: Every episode starts with a real-world story (e.g., "Why is your coffee more expensive?") → explains the economic concept behind it → connects to the broader market. This is "story first, data second" in audio form.
- **"Indicator Codes"**: Short 1-minute episodes that explain a single financial concept (e.g., "What is inflation?" "What is GDP?") — bite-sized audio learning.
- **"Planet Money" Deep Dives**: Longer 30-minute episodes that explore a single topic in depth (e.g., "The economics of TSMC" or "How the semiconductor industry works").
- **Transcript Available**: Every episode has a full transcript — users can read along or search for specific terms.
- **"Newsletter" Companion**: Daily email summary of the episode with key takeaways and links.

**UX/Design Approach**:
- **Audio-first**: Designed for listening during commute, exercise, or chores
- **Story-driven**: Every concept is taught through a real-world story
- **Plain-language**: No jargon without explanation; conversational tone
- **Bite-sized**: 10 minutes or less — respects listener's time
- **Multi-modal**: Audio + transcript + newsletter

**Unique Capabilities**:
- **Narrative-first audio**: "Story first, data second" in audio form — unique modality
- **10-minute format**: Bite-sized learning that fits into daily routine
- **Real-world connections**: Every abstract concept is connected to a tangible real-world example
- **Commute-friendly**: Audio format enables learning during otherwise "dead" time

**Comparison with Stock Explorer**:

| Feature | The Indicator | Stock Explorer |
|---|---|---|
| Audio Format | ✅ Podcast | ❌ Not built |
| Narrative-First | ✅ Core philosophy | ✅ Core philosophy |
| Bite-Sized | ✅ 10 min episodes | ⚠️ Did You Know facts |
| Real-World Stories | ✅ Every episode | ⚠️ Analogies |
| Plain-Language | ✅ Core feature | ✅ Core feature |
| Daily Engagement | ✅ Daily episodes | ❌ Not built |
| Company Analysis | ❌ Concept-focused | ✅ Company-focused |
| TW Market | ❌ US/Global focus | ✅ Deep coverage |

**Key Insight for Stock Explorer**: The Indicator's narrative-first approach is the audio equivalent of Stock Explorer's "story first, data second" philosophy. Both platforms teach through stories, not through data dumps. The 10-minute daily format is a model for how Stock Explorer could create a daily engagement loop — a short, daily market story that teaches one concept. The "real-world connections" approach (connecting abstract concepts to tangible examples) is exactly what Stock Explorer's analogy engine does — validates the approach. The audio modality is a gap — Stock Explorer is entirely text+visual, missing the growing audio learning market.

---

### 5. Wall Street Survivor

**URL**: https://www.wallstreetsurvivor.com
**Positioning**: "Learn investing by doing" — gamified investing education with virtual portfolios
**Target Users**: Beginner investors globally; 1M+ registered users

**Key Features**:
- **Stock Market Game**: Virtual portfolio competition — users get $100,000 in fake money, compete against other users, leaderboard rankings. "Learn by doing" model.
- **Structured Courses**: 20+ courses on investing fundamentals, stock analysis, options, and portfolio management. Each course is 15-30 minutes with video lessons, reading material, and quizzes.
- **"Learn → Practice → Compete" Pipeline**: Structured progression from education to practice to competition. Users complete courses → practice with virtual portfolio → compete in stock market game.
- **"Stock Analysis Tool"**: Built-in tool for analyzing stocks with plain-language explanations — "What does this company do?" "Is it a good value?" "What are the risks?"
- **"Achievement Badges"**: Gamification system — users earn badges for completing courses, winning competitions, and mastering concepts. Badges are shareable on social media.
- **"Virtual Portfolio with Feedback"**: AI-generated feedback on virtual portfolio performance — "Your portfolio is too concentrated in tech stocks. Consider diversifying into other sectors."
- **"Financial Dictionary"**: 5,000+ terms with plain-language definitions and examples.
- **"Community Leaderboard"**: Users can see how their virtual portfolio ranks against others — social competition drives engagement.

**UX/Design Approach**:
- **Gamified**: Points, badges, leaderboards, competitions — game mechanics drive learning
- **Visual**: Every concept is taught with visual diagrams and interactive tools
- **Progressive**: Must complete courses before advancing to practice and competition
- **Social**: Leaderboards and competitions create social engagement
- **Web-based**: Works in browser, no app required

**Unique Capabilities**:
- **Stock Market Game**: Virtual portfolio competition — learn by doing with real stakes (leaderboard)
- **Achievement Badges**: Gamification system that drives engagement and completion
- **"Learn → Practice → Compete" Pipeline**: Structured progression from education to practice
- **AI Portfolio Feedback**: Automated feedback on virtual portfolio decisions

**Comparison with Stock Explorer**:

| Feature | Wall Street Survivor | Stock Explorer |
|---|---|---|
| Stock Market Game | ✅ Virtual competition | ❌ (positioning) |
| Structured Courses | ✅ 20+ courses | ⚠️ Did You Know facts |
| Achievement Badges | ✅ Gamification | ❌ Not built (C60 pending) |
| AI Portfolio Feedback | ✅ Automated | ❌ Not built |
| Financial Dictionary | ✅ 5,000+ terms | ❌ Not built (C33 pending) |
| Plain-language | ✅ Core feature | ✅ Core feature |
| Gamification | ✅ Points + badges | ❌ Not built |
| TW Market | ❌ US focus | ✅ Deep coverage |
| Story first | ⚠️ Game-first | ✅ Story first |

**Key Insight for Stock Explorer**: Wall Street Survivor's "Learn → Practice → Compete" pipeline is a structured progression model that Stock Explorer could adapt. The achievement badges system is a more gamified version of our planned C60 (Concept Mastery Badges) — validates the concept. The "Stock Market Game" is a practice mechanism that teaches beginners by doing — while Stock Explorer deliberately avoids trading features, a "company analysis game" (e.g., "Can you identify which company matches this description?") could be a gamified learning tool that aligns with the "historian" positioning. The AI portfolio feedback is a feature that could be adapted to Stock Explorer's context — "Here's what you learned about TSMC. Did you notice the high customer concentration risk?"

---

### 6. Morning Brew (Business Newsletter)

**URL**: https://www.morningbrew.com
**Positioning**: "The daily email that makes reading the news enjoyable" — 5-minute daily business newsletter
**Target Users**: Business professionals, beginners, curious observers; 3M+ subscribers

**Key Features**:
- **5-Minute Daily Newsletter**: Every weekday, a 5-minute email summarizing the most important business and market news in plain language with a conversational, witty tone.
- **"Brew Academy" (2025)**: Structured courses on business and finance fundamentals — 10+ courses organized by topic (economics, investing, marketing, etc.). Each course is 5-10 minutes with interactive exercises.
- **"Brew Quiz"**: Daily quiz question in the newsletter — "What was the biggest market mover today?" — gamified engagement.
- **"Brew Podcast"**: Weekly 30-minute podcast diving deeper into one topic — "The economics of TSMC" or "How the semiconductor industry works."
- **"Brew Stories"**: Long-form narrative articles that explain complex business topics through storytelling — "The story of how TSMC became the world's most important chip maker."
- **"Brew Glossary"**: Financial terms explained in plain language — "P/E ratio: how much you're paying for each dollar of earnings."
- **"Brew Community"**: Moderated community with "Beginner-Friendly" sections — safe space for asking questions.

**UX/Design Approach**:
- **Conversational tone**: Witty, engaging, plain-language — makes finance feel approachable
- **Bite-sized**: 5 minutes or less — respects reader's time
- **Story-driven**: Every piece of content tells a story, not just presents facts
- **Daily engagement loop**: Users return every day for the newsletter
- **Multi-modal**: Newsletter + podcast + courses + community

**Unique Capabilities**:
- **Conversational tone**: Makes finance feel approachable and fun — unique voice
- **Daily engagement loop**: Users return every day — retention mechanism
- **Story-driven content**: Every complex topic is explained through storytelling
- **Multi-modal**: Newsletter + podcast + courses + community — multiple touchpoints

**Comparison with Stock Explorer**:

| Feature | Morning Brew | Stock Explorer |
|---|---|---|
| Daily Newsletter | ✅ 5-minute email | ❌ Not built |
| Conversational Tone | ✅ Witty, engaging | ⚠️ Professional |
| Story-Driven | ✅ Core philosophy | ✅ Core philosophy |
| Structured Courses | ✅ Brew Academy | ⚠️ Did You Know facts |
| Daily Quiz | ✅ Gamified | ❌ Not built |
| Podcast | ✅ Weekly 30-min | ❌ Not built |
| Community | ✅ Moderated | ❌ Not built |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ❌ US/Global focus | ✅ Deep coverage |

**Key Insight for Stock Explorer**: Morning Brew's conversational tone is a UX innovation that Stock Explorer could adopt — making finance feel approachable and fun, not intimidating. The "story-driven content" philosophy is identical to Stock Explorer's "story first, data second" — validates the approach. The daily engagement loop (newsletter → quiz → podcast → community) is a retention model that Stock Explorer completely lacks. The "Brew Glossary" is a lighter version of our C33 (Glossary) — validates demand. The conversational tone is a specific UX innovation: instead of "TSMC's gross margin is 55%," Morning Brew would say "TSMC keeps 55 cents of every dollar it earns from making chips — that's a lot of money when you're selling billions of chips."

---

### 7. Dcard 股票版 (Dcard Stocks Forum)

**URL**: https://www.dcard.tw/f/stocks
**Positioning**: Taiwan's largest student and young adult community forum — anonymous stock discussion and peer learning
**Target Users**: Taiwanese students, young adults, beginner investors; 1M+ monthly active users in stocks section

**Key Features**:
- **Anonymous Stock Discussion**: Users post stock-related questions, analysis, and opinions anonymously — reduces fear of judgment, encourages honest discussion
- **"Stock Story" Posts**: Users share their "stock stories" — "How I analyzed TSMC" or "What I learned from investing in 富邦媒" — narrative-driven peer learning
- **"Beginner-Friendly" Culture**: The community has a strong norm of being beginner-friendly — no question is too basic, no jargon without explanation
- **"Stock Comparison" Posts**: Users post side-by-side comparisons of companies — "TSMC vs UMC: which is better?" — community-driven benchmark analysis
- **"Investment Diary" Posts**: Users share their investment journey — "My first 3 months of investing" — personal reflection and community support
- **"Stock Education" Posts**: Experienced users create educational posts — "How to read a balance sheet" or "What is P/E ratio?" — community-generated education
- **"Upvote-Based Quality Control": Best answers and analysis rise to the top through upvotes — community-curated knowledge
- **"Sector Discussion" Boards**: Dedicated boards for each sector — "Semiconductor," "Finance," "Tech" — sector-specific discussion

**UX/Design Approach**:
- **Anonymous**: Reduces fear of judgment — encourages honest questions
- **Card-based**: Each post is a card with title, preview, upvotes, and comments
- **Community-driven**: Content is generated by users, curated by upvotes
- **Mobile-first**: Native app is the primary platform
- **Chinese-language**: Mandarin-focused with TW market focus

**Unique Capabilities**:
- **Anonymous discussion**: Reduces barrier to asking "stupid questions" — safe learning environment
- **Community-generated education**: Users teach each other — peer learning at scale
- **"Stock Story" posts**: Narrative-driven peer learning — users share their analysis journey
- **Upvote-based quality control**: Best content rises to the top — community curation
- **Beginner-friendly culture**: Strong norm of being welcoming to beginners

**Comparison with Stock Explorer**:

| Feature | Dcard 股票版 | Stock Explorer |
|---|---|---|
| Anonymous Discussion | ✅ Safe learning | ❌ Not built |
| Community Education | ✅ Peer-generated | ❌ Not built |
| Stock Story Posts | ✅ Narrative-driven | ✅ One-liner |
| Beginner-Friendly | ✅ Core culture | ✅ Core positioning |
| Upvote Quality Control | ✅ Community curation | ❌ Not built |
| Investment Diary | ✅ Shared publicly | ❌ Not built (C55 pending) |
| Sector Discussion | ✅ Dedicated boards | ❌ Not built |
| Plain-language | ✅ Community norm | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |
| Mobile App | ✅ Native | ❌ Streamlit only |

**Key Insight for Stock Explorer**: Dcard 股票版 is the most relevant TW community competitor — it's where Taiwanese beginners actually go to learn about stocks. The anonymous discussion format reduces the barrier to asking "stupid questions" — a safe learning environment that Stock Explorer's formal analysis doesn't provide. The "community-generated education" model (users teaching each other) is a powerful peer learning mechanism. The "Stock Story" posts are a more social version of Stock Explorer's one-liner — users share their analysis journey, not just the conclusion. The "beginner-friendly culture" is a community norm that Stock Explorer could foster — making it clear that no question is too basic. The upvote-based quality control is a community curation mechanism that ensures the best content is discoverable.

---

### 8. r/investing (Reddit)

**URL**: https://www.reddit.com/r/investing/
**Positioning**: "The largest community-driven investing discussion forum" — peer learning through discussion
**Target Users**: Global retail investors, especially beginners; 2.5M+ members

**Key Features**:
- **Wiki-Style Education**: r/investing has a comprehensive wiki with structured articles on every investing topic — "What is a stock?" "How to read financial statements?" "What is diversification?" — community-curated and maintained.
- **"Daily Discussion" Thread**: Every day, a pinned discussion thread where users ask questions, share news, and discuss market movements — real-time community learning.
- **"What Are Your Moves Tomorrow?" (WAYMT) Thread**: Daily thread where users share their planned trades and reasoning — learn by observing others' decision-making process.
- **"DD" (Due Diligence) Posts**: Users post detailed stock analysis — "DD on TSMC: why I think it's undervalued" — community-driven fundamental analysis.
- **"Beginner Questions" Thread**: Weekly pinned thread for beginner questions — no judgment, no jargon without explanation.
- **"Investment Diary" Posts**: Users share their investment journey — "My portfolio after 1 year of investing" — personal reflection and community feedback.
- **"Sector Analysis" Posts**: Users post sector-level analysis — "The semiconductor sector in 2026" — community-driven sector research.
- **Upvote-Based Quality Control**: Best answers and analysis rise to the top through upvotes — community-curated knowledge.

**UX/Design Approach**:
- **Thread-based**: Discussion organized in threads with nested comments
- **Wiki-style**: Structured knowledge base maintained by the community
- **Anonymous**: Reduces fear of judgment — encourages honest questions
- **Community-driven**: Content is generated by users, curated by upvotes
- **Global**: Covers all markets, including TW stocks

**Unique Capabilities**:
- **Wiki-style education**: Community-curated knowledge base — structured, comprehensive, always up-to-date
- **"DD" posts**: Detailed community-driven fundamental analysis — peer learning at scale
- **"WAYMT" thread**: Learn by observing others' decision-making process — social learning
- **"Beginner Questions" thread**: Safe space for asking basic questions — beginner-friendly culture
- **Upvote-based quality control**: Best content rises to the top — community curation

**Comparison with Stock Explorer**:

| Feature | r/investing | Stock Explorer |
|---|---|---|
| Wiki-Style Education | ✅ Community-curated | ❌ Not built |
| DD Posts | ✅ Peer analysis | ❌ Not built |
| WAYMT Thread | ✅ Decision observation | ❌ Not built |
| Beginner Questions | ✅ Safe space | ❌ Not built |
| Investment Diary | ✅ Shared publicly | ❌ Not built (C55 pending) |
| Sector Analysis | ✅ Community-driven | ❌ Not built |
| Upvote Quality Control | ✅ Community curation | ❌ Not built |
| Plain-language | ⚠️ Varies | ✅ Core feature |
| Structured Analysis | ❌ Community-driven | ✅ Structured |
| TW Market | ⚠️ Some coverage | ✅ Deep coverage |

**Key Insight for Stock Explorer**: r/investing's wiki-style education is a community-curated knowledge base that complements Stock Explorer's structured analysis. The "DD" (Due Diligence) posts are community-driven fundamental analysis — users learn by reading others' analysis. The "WAYMT" thread (What Are Your Moves Tomorrow?) is a social learning mechanism — users learn by observing others' decision-making process. The "Beginner Questions" thread is a safe space for asking basic questions — a community norm that Stock Explorer could foster. The upvote-based quality control is a community curation mechanism that ensures the best content is discoverable. r/investing represents the "social learning" model that Stock Explorer completely lacks — users learn from each other through discussion, not from a single authoritative source.

---

## Updated Competitor Overview Table (Round 13 Additions)

| Dimension | Naver Finance | Kabutan | 雪球 (Xueqiu) | The Indicator | Wall Street Survivor | Morning Brew | Dcard 股票版 | r/investing | **Stock Explorer** |
|---|---|---|---|---|---|---|---|---|---|
| **Positioning** | Korea Finance Portal | Japan Stock Ed | China Social Invest | Daily Finance Podcast | Gamified Investing | Newsletter Business | TW Stock Forum | Reddit Investing | Beginner Education ("Historian") |
| **Community** | ✅ Knowledge iN | ❌ | ✅ Social Feed | ❌ | ✅ Leaderboard | ✅ Moderated | ✅ Anonymous | ✅ 2.5M members | ❌ MISSING |
| **Structured Education** | ✅ Academy | ✅ 20+ courses | ✅ 30+ courses | ⚠️ Episodes | ✅ 20+ courses | ✅ Brew Academy | ⚠️ Peer-generated | ✅ Wiki | ⚠️ Did You Know |
| **Story/Narrative** | ✅ Stock Story | ✅ Stock Story | ✅ User Stories | ✅ Core philosophy | ⚠️ Game-first | ✅ Story-driven | ✅ Stock Story | ⚠️ DD posts | ✅ Core philosophy |
| **Audio/Podcast** | ❌ | ❌ | ❌ | ✅ 10-min daily | ❌ | ✅ Weekly | ❌ | ❌ | ❌ MISSING |
| **Gamification** | ❌ | ❌ | ❌ | ⚠️ Quiz | ✅ Badges+Game | ⚠️ Quiz | ❌ | ❌ | ❌ MISSING |
| **Daily Engagement** | ✅ Community | ✅ Market Pulse | ✅ Social Feed | ✅ Daily episodes | ⚠️ Game | ✅ Newsletter | ✅ Daily threads | ✅ WAYMT | ❌ MISSING |
| **Beginner-Friendly** | ✅ Guide | ✅ Beginner Mode | ✅ Academy | ✅ Core | ✅ Courses | ✅ Core | ✅ Culture | ✅ Beginner thread | ✅ Core |
| **Anonymous** | ❌ | ❌ | ❌ | N/A | ❌ | ❌ | ✅ Anonymous | ✅ Anonymous | ❌ N/A |
| **TW Market** | ❌ Korea | ❌ Japan | ⚠️ China | ❌ US/Global | ❌ US | ❌ US/Global | ✅ Deep | ⚠️ Some | ✅ Deep |
| **Mobile App** | ✅ Native | ✅ Native | ✅ Native | ✅ Podcast app | ⚠️ Web | ✅ Email | ✅ Native | ✅ Native | ❌ Streamlit only |
| **Free** | ✅ Free | ⚠️ Freemium | ⚠️ Freemium | ✅ Free | ⚠️ Freemium | ⚠️ Freemium | ✅ Free | ✅ Free | ✅ Free |

---

## New Feature Ideas from Round 13

### [ISSUE-C63] "Audio Market Story" — Daily 3-Minute Market Narrative

- **Source**: Competitor research round 13 (The Indicator daily podcast, Morning Brew daily newsletter, 雪球 social feed)
- **Priority**: P2
- **Effort**: 12-16h
- **Alignment**: Core value #1 "Story first, data second" + Core value #3 "Adaptive and self-evolving" + "Ten-second test"
- **Description**: The Indicator proves that a 10-minute daily market narrative is a powerful engagement and education tool. Morning Brew proves that a 5-minute daily business summary drives 3M+ subscribers. Stock Explorer has no daily engagement mechanism and no audio content. An "Audio Market Story" would: (1) generate a 3-minute daily market narrative in Mandarin — "What happened in the TW market today, told as a story," (2) use text-to-speech for audio delivery (low-effort MVP), (3) include one key lesson connecting market action to a financial concept, (4) be available as a daily email or in-app audio player. This creates a daily engagement loop — users return every day to hear the market story. The audio modality enables learning during commute, exercise, or chores — use cases that text+visual cannot serve. This aligns with the "historian" positioning: "Here's what happened today, explained as a story."
- **Implementation**: Create a `daily_story.py` service that generates a daily market narrative from FinMind data + templates. Use a TTS library (e.g., gTTS or pyttsx3) for audio delivery. Add a "🎧 今日市場故事" button to the homepage that plays the audio. Optionally generate a daily email with the story text. Content template: (1) market overview in plain language, (2) top mover with story, (3) one financial concept lesson, (4) "what to watch tomorrow" (factual, not predictive).
- **Competitive Gap**: 🔴 No TW competitor has daily audio market stories; The Indicator/Morning Brew prove demand; unique "historian" differentiator in audio form

---

### [ISSUE-C64] "Community Q&A" — Peer Learning Forum

- **Source**: Competitor research round 13 (Naver Finance "Knowledge iN" Q&A, 雪球 community Q&A, Dcard 股票版 anonymous discussion, r/investing beginner questions)
- **Priority**: P2
- **Effort**: 16-24h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + beginner-friendly + engagement
- **Description**: Naver Finance's "Knowledge iN" Q&A has millions of questions and answers about stocks. Dcard 股票版 is where Taiwanese beginners actually go to ask questions. r/investing has a comprehensive wiki and daily discussion threads. Stock Explorer has no community features — users learn in isolation. A "Community Q&A" would: (1) add a "❓ 問問大家" section to each company page where users can ask questions, (2) questions are answered by other users or by the system (using existing analogy engine), (3) best answers are upvoted and featured, (4) a "Beginner Questions" thread for general investing questions. This creates a peer learning ecosystem — users learn from each other's questions and answers. The community Q&A also creates user-generated content that improves over time — a self-evolving knowledge base.
- **Implementation**: Add a `qa_system.py` service with a simple Q&A data model (question, answers, upvotes). Store Q&A in a local JSON file (MVP) or integrate with a lightweight backend. Add a "❓ 問問大家" expander to each company page. Add a "💬 新手發問" page for general questions. Use existing analogy engine to auto-answer common questions. Upvote mechanism for quality control.
- **Competitive Gap**: 🔴 No TW stock analysis tool has community Q&A; Naver Finance/Dcard prove demand; transforms Stock Explorer from solo tool to community platform

---

### [ISSUE-C65] "Company Story Game" — Gamified Learning Through Play

- **Source**: Competitor research round 13 (Wall Street Survivor stock market game + achievement badges, Morning Brew daily quiz, Khan Academy mastery system)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + engagement
- **Description**: Wall Street Survivor's stock market game teaches investing through virtual portfolio competition. Morning Brew's daily quiz gamifies business news. Khan Academy's mastery system requires demonstrating understanding before advancing. Stock Explorer has no gamification — users read but never play. A "Company Story Game" would: (1) present a company description (one-liner + key metrics) → users guess which company it is, (2) 5 questions per round, each question reveals more information, (3) scoring based on how few clues needed to guess correctly, (4) leaderboard (optional, session-only), (5) daily challenge — "Today's mystery company" for engagement. This is a "historian" game — it teaches users to understand companies, not to pick stocks. The game format makes learning fun and addictive — users learn company stories through play, not through reading.
- **Implementation**: Add a "🎮 公司猜猜看" page accessible from the navbar. Game logic: (1) select a random company from the database, (2) show clues one at a time (one-liner → revenue breakdown → key metrics → sector), (3) user guesses at any point, (4) score based on number of clues needed, (5) after guessing, show the full company story. Daily challenge: one company per day, same for all users. Use session state for scores and progress.
- **Competitive Gap**: 🟡 No TW competitor has a "guess the company" game; Wall Street Survivor/Morning Brew prove gamification demand; unique "historian" gamification that teaches company understanding

---

### [ISSUE-C66] "Conversational Tone" — UX Writing Overhead for Approachability

- **Source**: Competitor research round 13 (Morning Brew conversational tone, The Indicator plain-language storytelling, Dcard beginner-friendly culture)
- **Priority**: P2
- **Effort**: 6-10h
- **Alignment**: Core value #1 "Story first, data second" + "Ten-second test" + beginner-friendly
- **Description**: Morning Brew's conversational tone makes finance feel approachable and fun — "TSMC keeps 55 cents of every dollar it earns from making chips" instead of "TSMC's gross margin is 55%." The Indicator's plain-language storytelling makes complex economic concepts accessible to everyone. Dcard's beginner-friendly culture makes it safe to ask "stupid questions." Stock Explorer's current tone is professional and educational — accurate but potentially intimidating for absolute beginners. A "Conversational Tone" overhaul would: (1) rewrite all metric explanations in a conversational, approachable tone, (2) add humor and personality to "Did You Know?" facts, (3) use everyday analogies instead of technical explanations, (4) add encouraging messages ("Great question!" "You're doing great!"), (5) use second-person ("you") instead of third-person ("the company"). This is a UX writing change, not a feature — but it dramatically affects how beginners perceive the product.
- **Implementation**: Create a `tone_guide.md` documenting the conversational tone guidelines. Rewrite the top 20 most common metric explanations in conversational tone. Update "Did You Know?" facts to be more engaging and fun. Add encouraging micro-copy throughout the app (e.g., after completing a quiz: "你答對了！" instead of "Correct"). This is a content update, not a code change — can be done incrementally.
- **Competitive Gap**: 🟡 No TW competitor has a conversational tone for stock analysis; Morning Brew/The Indicator prove demand; makes Stock Explorer more approachable for absolute beginners

---

### [ISSUE-C67] "Community-Curated Stock Stories" — User-Generated Narrative Layer

- **Source**: Competitor research round 13 (雪球 user-generated stock stories, Dcard stock story posts, r/investing DD posts, Naver Finance Knowledge iN Q&A)
- **Priority**: P2
- **Effort**: 14-20h
- **Alignment**: Core value #1 "Story first, data second" + Core value #3 "Adaptive and self-evolving" + Core value #4 "Point-to-point knowledge construction"
- **Description**: 雪球 users write and share their own "stock stories" — narrative summaries of what a company does and why it's interesting. Dcard users share their analysis journey — "How I analyzed TSMC." r/investing users post detailed "DD" (Due Diligence) analysis. Stock Explorer's company stories are entirely system-generated — there's no user-generated narrative layer. "Community-Curated Stock Stories" would: (1) allow users to write and share their own company stories — "What does TSMC do? Here's how I understand it," (2) stories are upvoted and the best ones are featured alongside the system-generated story, (3) users can comment on and discuss stories, (4) stories are categorized by quality: "Beginner-Friendly," "Detailed Analysis," "Creative Analogy," (5) top contributors earn "Story Teller" badges. This creates a self-evolving knowledge base — the community adds perspectives that the system can't generate, and the best content rises to the top through upvotes.
- **Implementation**: Add a `user_stories.py` service with a simple story data model (author, content, company, upvotes, category). Store stories in a local JSON file (MVP). Add a "📝 分享你的故事" button to each company page. Add a "🏆 精選故事" section showing the top-voted stories. Upvote mechanism for quality control. Integrate with C60 (Concept Mastery Badges) — "Story Teller" badge for top contributors.
- **Competitive Gap**: 🔴 No TW competitor has user-generated company stories; 雪球/Dcard prove demand; transforms Stock Explorer from authoritative source to community-curated knowledge platform

---

### [ISSUE-C68] "Financial Concept Storytelling" — Narrative-Based Concept Explanations

- **Source**: Competitor research round 13 (The Indicator narrative-first approach, Morning Brew story-driven content, Kabutan "Stock Story" concept, Zerodha Varsity module-based learning)
- **Priority**: P1
- **Effort**: 12-16h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: The Indicator teaches every economic concept through a real-world story — "Why is your coffee more expensive?" → explains inflation. Morning Brew explains business topics through storytelling — "The story of how TSMC became the world's most important chip maker." Kabutan's "Stock Story" explains what a company does through narrative. Stock Explorer's C56 (Explain This Metric) explains metrics with analogies and examples, but not through storytelling. "Financial Concept Storytelling" would: (1) explain every financial concept through a short narrative — "Once upon a time, a company named TSMC made chips for Apple...", (2) each story connects the concept to a real-world situation that beginners can relate to, (3) stories are 2-3 paragraphs long — short enough to read in 30 seconds, (4) each story ends with a "What this means for you" takeaway. This is a more engaging version of C56 that aligns with the "story first" philosophy — instead of explaining P/E ratio as "price divided by earnings," tell the story of "how much you're paying for each dollar of the company's profit."
- **Implementation**: Create `src/data/concept_stories.yaml` with concept → narrative story + takeaway. Each story is 2-3 paragraphs in plain language with a real-world example. Add a "📖 概念故事" section to the C56 (Explain This Metric) page. Prioritize the 10 most common concepts (P/E, ROE, P/B, gross margin, revenue growth, dividend yield, debt ratio, EPS, free cash flow, institutional ownership). Stories are pre-written (not AI-generated) to ensure quality and alignment with "historian" positioning.
- **Competitive Gap**: 🔴 No TW competitor explains financial concepts through storytelling; The Indicator/Morning Brew prove demand; perfect "story first" differentiator that makes abstract concepts tangible

---

## Key Insights from Round 13

### 1. **Audio is the Missing Modality**
The Indicator (5M+ monthly downloads) and Morning Brew (3M+ subscribers) prove that audio and daily briefings are powerful engagement and education tools. Stock Explorer is entirely text+visual — missing the growing audio learning market. C63 (Audio Market Story) would fill this gap with a daily 3-minute market narrative.

### 2. **Community is the Dominant Learning Model**
Naver Finance (Knowledge iN Q&A), 雪球 (social feed + user stories), Dcard (anonymous discussion), and r/investing (wiki + DD posts) all use community as a core learning mechanism. Stock Explorer is entirely solo-learning — users learn from the system, not from each other. C64 (Community Q&A) and C67 (Community-Curated Stories) would add community learning.

### 3. **Gamification Drives Engagement**
Wall Street Survivor (stock market game + badges), Morning Brew (daily quiz), and Khan Academy (mastery system) all use gamification to drive learning engagement. Stock Explorer has no gamification — users read but never play. C65 (Company Story Game) would add a "guess the company" game that teaches company understanding through play.

### 4. **Conversational Tone Makes Finance Approachable**
Morning Brew's witty, conversational tone makes finance feel fun and approachable. The Indicator's plain-language storytelling makes complex concepts accessible. Stock Explorer's professional tone, while accurate, may intimidate absolute beginners. C66 (Conversational Tone) would make Stock Explorer more approachable.

### 5. **Storytelling is the Universal Education Model**
The Indicator (narrative-first), Morning Brew (story-driven), 雪球 (user stories), and Kabutan (stock stories) all use storytelling as their primary education method. This validates Stock Explorer's "story first, data second" philosophy — storytelling is not just our positioning, it's the industry trend. C68 (Financial Concept Storytelling) would extend storytelling from company-level to concept-level.

### 6. **TW Community is Underserved**
Dcard 股票版 is the only major TW community for stock discussion — and it's a general forum, not a structured analysis platform. There's no TW platform that combines structured stock analysis with community discussion. Stock Explorer could fill this gap by adding community features (C64, C67) to its structured analysis — a unique combination in the TW market.

### 7. **Daily Engagement Loops Drive Retention**
The Indicator (daily podcast), Morning Brew (daily newsletter), 雪球 (social feed), and Dcard (daily threads) all create daily reasons to return. Stock Explorer has no daily engagement mechanism — users only return when they want to look up a specific stock. C63 (Audio Market Story) and C65 (Company Story Game daily challenge) would create daily retention loops.

---

## Feature Gap Summary (Round 13)

| ID | Title | Priority | Effort | Source Competitor | Alignment |
|---|---|---|---|---|---|
| C63 | Audio Market Story (Daily 3-Minute Narrative) | P2 | 12-16h | The Indicator, Morning Brew, 雪球 | Story first + Adaptive + Ten-second test |
| C64 | Community Q&A (Peer Learning Forum) | P2 | 16-24h | Naver Finance, 雪球, Dcard, r/investing | Point-to-point + Beginner-friendly |
| C65 | Company Story Game (Gamified Learning) | P2 | 10-14h | Wall Street Survivor, Morning Brew, Khan Academy | Point-to-point + Ten-second test + Engagement |
| C66 | Conversational Tone (UX Writing Overhaul) | P2 | 6-10h | Morning Brew, The Indicator, Dcard | Story first + Ten-second test + Beginner-friendly |
| C67 | Community-Curated Stock Stories (User-Generated Narratives) | P2 | 14-20h | 雪球, Dcard, r/investing, Naver Finance | Story first + Adaptive + Point-to-point |
| C68 | Financial Concept Storytelling (Narrative-Based Explanations) | P1 | 12-16h | The Indicator, Morning Brew, Kabutan, Zerodha Varsity | Story first + Point-to-point + Ten-second test |

---

## Recommendations

### Immediate (Next Sprint)
1. **C68 Financial Concept Storytelling** — P1 gap, directly addresses "story first" core value, The Indicator/Morning Brew prove demand. Highest alignment with Stock Explorer's core positioning: storytelling is our #1 value, and this extends it from company-level to concept-level.

### Short-Term (Sprint 2-3)
2. **C66 Conversational Tone** — Low effort (6-10h), high impact on beginner approachability, Morning Brew/The Indicator prove demand. Makes Stock Explorer feel less intimidating.
3. **C65 Company Story Game** — Gamified learning drives engagement, Wall Street Survivor/Morning Brew prove demand. "Guess the company" game aligns with "historian" positioning.

### Medium-Term (Post-Sprint 3)
4. **C63 Audio Market Story** — Creates daily engagement loop, The Indicator/Morning Brew prove demand. Requires TTS pipeline setup.
5. **C64 Community Q&A** — Transforms solo tool to community platform, Naver Finance/Dcard prove demand. Requires backend infrastructure.
6. **C67 Community-Curated Stories** — User-generated content creates self-evolving knowledge base, 雪球/Dcard prove demand. Depends on C64 (community infrastructure).

---

*This is the thirteenth competitor research round. Six new feature suggestions identified (C63-C68). The most impactful new gap is C68 (Financial Concept Storytelling) — it directly extends Stock Explorer's #1 core value ("story first, data second") from company-level to concept-level, and multiple international competitors prove that narrative-based education is the most effective approach for beginners. The most strategically important gap is C64 (Community Q&A) — community is the dominant learning model among competitors, and Stock Explorer is entirely solo-learning. The most unique gap is C65 (Company Story Game) — a "guess the company" game that teaches company understanding through play, perfectly aligned with the "historian" positioning.*
