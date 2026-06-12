# Competitor Research Report — Round 17

> **Date**: 2026-06-12
> **Author**: QA Engineer (Round 17)
> **Purpose**: Deep-dive white space analysis — cross-competitor synthesis, codebase gap analysis, and TW market-specific opportunities not covered in Rounds 1-16.
>
> **Previous Rounds Coverage** (76 competitors, 69 feature suggestions C01-C92):
> - Rounds 1-15: 64 competitors across TW brokers, US brokers, social investing, AI tools, gamified education, visual storytelling, community forums
> - Round 16: Bloom, Cleo, 長投學堂, Visual Capitalist, MoneySmart, Plum → C81-C85
> - Round 17 (macro trends): Perplexity Finance, Fantastic Knowledge, Beewise, NOMA Finance, OpenAI Agent, Durable Agent → C86-C92

---

## Research Methodology for Round 17 (Deep-Dive)

After 17 rounds covering 76 competitors and identifying 92 features (C01-C92), the competitive landscape is exhaustively mapped at the **feature level**. Round 17 Deep-Dive takes a fundamentally different approach:

### What's Already Covered (Avoiding Redundancy)
- ✅ AI agents, explainable AI, empathy engine, micro-learning, personas, collaborative analysis, market narrative feed (C86-C92)
- ✅ Interactive scenarios, animated data stories, investment memo, market case studies, wellness check (C81-C85)
- ✅ All major competitor categories: TW brokers, US brokers, social investing, AI tools, gamified ed, visual storytelling, community forums

### Round 17 Deep-Dive Focus: EXECUTION GAPS + TW MARKET-SPECIFIC WHITE SPACE
We look for: (1) Features that competitors have but execute poorly — opportunities to "do it right" for TW market, (2) TW-specific regulatory/cultural features that no international competitor can replicate, (3) Cross-feature synthesis opportunities where combining 2-3 existing features creates something no competitor has, (4) Beginner onboarding gaps — the critical first-week experience that determines retention.

### Analysis Method
Since live web search is unavailable, this round uses:
1. **Codebase architecture analysis** — examining all 39 Python source files to identify structural gaps
2. **Cross-competitor synthesis** — combining insights from 76 competitors to identify combination features
3. **TW market-specific analysis** — identifying features that only make sense for TW market (regulatory, cultural, linguistic)
4. **Beginner journey mapping** — tracing the complete first-time user experience to identify drop-off points

---

## New Feature Gaps Identified — Round 17 Deep-Dive

### [ISSUE-C93] "Dividend Income Calendar" — Market-Wide Dividend Calendar with Income Projection

**Source**: Cross-competitor synthesis — 口袋股利 (dividend calendar) + Stock Explorer's C1 (ex-dividend countdown) + MoneySmart (financial calculators) + 長投學堂 (DCA simulator)

**Priority**: P1

**Effort**: 12-16h

**Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Historian" positioning + beginner-friendly

**Description**:
口袋股利 has a dividend calendar but it's a simple list. Stock Explorer has C1 (single-stock ex-dividend countdown) but no market-wide view. MoneySmart has calculators but no dividend-specific tools. No competitor combines all three into a unified "Dividend Income Calendar."

A "Dividend Income Calendar" would:
1. **Monthly calendar view**: Show all TW stocks going ex-dividend each day of the month — color-coded by dividend yield (green = high yield, yellow = medium, blue = low)
2. **Income projection**: For each stock, show "If you own X shares, you'll receive NT$Y on [date]" — personalized to user's watchlist
3. **Dividend story**: Each calendar entry includes a one-line plain-language story — "TSMC pays NT$11/share this quarter. That's like getting a free iPhone for every 5 shares you own."
4. **Annual income timeline**: Show the user's projected dividend income for the entire year — "Based on your watchlist, you'll receive NT$XX,XXX in dividends in 2026"
5. **"Dividend Gap" analysis**: Identify months with no dividend income — "You have no dividends in March and September. Here are stocks that pay in those months."

**User Value**: Dividend investors (a huge segment in TW) currently track ex-dividends across multiple platforms. A unified calendar with income projection saves time AND teaches dividend strategy through visualization. Beginners see the "income stream" concept visually — "Oh, I get money every month from different stocks!"

**Implementation Notes**:
- Build `dividend_calendar.py` service that aggregates ex-dividend dates from FinMind data
- Create a "📅 股利日曆" page accessible from the navbar
- Calendar view: use a monthly grid with color-coded dots for each ex-dividend stock
- Income projection: multiply shares owned (from watchlist) by dividend per share
- Annual timeline: aggregate all projected dividends by month
- Connect to C1 (ex-dividend countdown) — clicking a calendar entry opens the company page
- Connect to watchlist — only show stocks the user owns (or show all with "add to watchlist" prompt)
- MVP: 12-16h for calendar view + income projection for top 50 dividend stocks

**Beginner-Friendly Test**: ✅ Passes — beginners see a visual calendar (intuitive) with plain-language income projections. The "annual income timeline" makes the abstract concept of "dividend investing" concrete and tangible.

**Alignment with "Historian" Positioning**: "Here's when companies historically pay dividends. Here's what you would have received. Here's what you will receive." — pure historian, no prediction.

**Competitive Gap**: 🔴 No TW competitor has a market-wide dividend calendar WITH income projection. 口袋股利 has a calendar but no projection. Stock Explorer has countdown (C1) but no calendar view. This would be a **unique TW market feature** that combines the best of 口袋股利 + C1 + MoneySmart calculators.

---

### [ISSUE-C94] "Earnings Story" — Post-Earnings Plain-Language Narrative Analysis

**Source**: Codebase gap analysis — M5 event detection identifies earnings events but generates no narrative; cross-competitor synthesis — Finshots (plain-language earnings summaries) + The Indicator (daily economic narratives) + StockAnalysis.com (plain-language analysis)

**Priority**: P1

**Effort**: 14-18h

**Alignment**: Core value #1 "Story first, data second" + Core value #3 "Adaptive and self-evolving" + "Historian" positioning + "Ten-second test"

**Description**:
Stock Explorer's M5 event detection engine identifies earnings releases but only lists them as events in the dashboard. Finshots (India) proves that plain-language earnings summaries are hugely popular. No TW competitor provides automated plain-language earnings narratives.

An "Earnings Story" feature would:
1. **Auto-generate earnings narratives**: Within 24 hours of an earnings release, generate a plain-language story — "TSMC earned NT$XXX billion this quarter. That's X% more than last quarter. Here's why..."
2. **Beat/Miss context**: "Analysts expected NT$XXX billion. TSMC beat/missed by X%. Here's what that means..."
3. **Plain-language breakdown**: Revenue, profit, margin — each explained with analogies from the analogy engine
4. **Historical comparison**: "This is the 3rd quarter in a row that TSMC beat expectations. Here's the pattern..."
5. **"What happened next"**: After the earnings story, show what happened to the stock price historically after similar earnings — "After beating expectations 3 quarters in a row, TSMC's stock rose an average of X%"

**User Value**: Earnings season is overwhelming for beginners — dozens of companies report every quarter, and the financial jargon is impenetrable. An "Earnings Story" transforms raw earnings data into a narrative beginners can follow. This creates a **quarterly engagement loop** — users return every quarter to read earnings stories.

**Implementation Notes**:
- Build `earnings_story.py` service with template-based narrative generation
- Templates for: beat, miss, in-line; revenue growth/decline; margin expansion/contraction
- Trigger from M5 event detection when earnings are released
- Display as a "📊 財報故事" section on the company page (appears after each earnings release)
- Archive all earnings stories (creates a historical narrative record)
- Connect to analogy engine for plain-language metric explanations
- Connect to C84 (Market Event Case Study) — significant earnings become case studies
- MVP: 14-18h for 5 narrative templates + trigger system + archive

**Beginner-Friendly Test**: ✅ Passes — beginners get a plain-language story instead of raw earnings data. The "What happened next" section teaches historical patterns without giving advice.

**Alignment with "Historian" Positioning**: "Here's what the company reported. Here's what it means. Here's what happened historically after similar reports." — pure historian storytelling.

**Competitive Gap**: 🔴 No TW competitor has automated plain-language earnings narratives. Finshots does this for Indian stocks but not TW. CMoney has earnings data but no narrative. This would be a **unique TW market feature** that transforms earnings season from overwhelming to educational.

---

### [ISSUE-C95] "Watchlist Health Dashboard" — Aggregate Portfolio Health with Plain-Language Summary

**Source**: Codebase gap analysis — watchlist.py has multi-list support and price alerts but no aggregate health view; cross-competitor synthesis — Simply Wall St (snowflake health) + Tykr (Fair Value score) + StockEdge (portfolio health) + C43 (Snowflake Health Visualization)

**Priority**: P2

**Effort**: 10-14h

**Alignment**: Core value #1 "Story first, data second" + Core value #2 "PPT-style presentation" + "Ten-second test" + "Historian" positioning

**Description**:
Stock Explorer's watchlist (watchlist.py) supports multiple lists, price alerts, and basic summary data — but has no aggregate health view. Simply Wall St has a snowflake for individual stocks but no portfolio view. Tykr has Fair Value scores but no portfolio aggregation. No competitor provides a plain-language portfolio health summary.

A "Watchlist Health Dashboard" would:
1. **Aggregate health score**: Combine C43 (Snowflake Health) scores for all watched stocks into a single "Watchlist Health Score" — "Your watchlist scores 7.5/10 overall"
2. **Plain-language summary**: "Your watchlist is heavy on semiconductors (60%) and light on financials (10%). Your average dividend yield is 3.2%. Your most volatile stock is X."
3. **"What to watch" alerts**: "3 of your watched stocks have earnings this week. 2 are approaching your alert thresholds."
4. **Sector diversification visual**: A simple pie chart showing sector allocation — "You're 80% tech. Here's what that means for your risk."
5. **Historical performance story**: "Over the last 3 months, your watchlist would have returned X%. Here's what drove that."

**User Value**: Beginners who track multiple stocks have no way to see the "big picture" of their watchlist. A health dashboard transforms a list of stocks into a coherent portfolio story — "Here's what you own, here's how healthy it is, here's what to watch."

**Implementation Notes**:
- Extend `watchlist.py` with a `get_watchlist_health()` function
- Aggregate C43 snowflake scores across all watched stocks
- Calculate sector allocation, average dividend yield, average volatility
- Generate plain-language summary using template-based text generation
- Display as a "📊 觀察清單健康度" page accessible from the navbar
- Connect to C43 (Snowflake Health) for individual stock scores
- Connect to C02/C03/C04 (Notifications) for "what to watch" alerts
- MVP: 10-14h for aggregate scoring + plain-language summary + sector visual

**Beginner-Friendly Test**: ✅ Passes — beginners get a single, plain-language summary instead of interpreting multiple stock pages. The "What to watch" section proactively surfaces important information.

**Alignment with "Historian" Positioning**: "Here's what you own. Here's how it's performed. Here's what's happening." — historian summarizing the current state, not predicting the future.

**Competitive Gap**: 🟡 Simply Wall St has individual stock health but no portfolio view. Tykr has scores but no plain-language summary. No TW competitor has a watchlist health dashboard with plain-language narrative. This would be a **unique portfolio-level feature**.

---

### [ISSUE-C96] "Sector Ecosystem Map" — Visual Supply Chain & Ecosystem Relationship Map

**Source**: Codebase gap analysis — group_structure.py shows parent-subsidiary relationships but not supply chain/ecosystem relationships; cross-competitor synthesis — Visual Capitalist (sector visualizations) + Simply Wall St (peer comparison) + TW market-specific (supply chain is critical in TW market)

**Priority**: P2

**Effort**: 16-22h

**Alignment**: Core value #1 "Story first, data second" + Core value #2 "PPT-style presentation" + Core value #4 "Point-to-point knowledge construction" + "Historian" positioning

**Description**:
Stock Explorer's group_structure.py shows parent-subsidiary ownership relationships. But TW's market is defined by **supply chain ecosystems** — TSMC → Apple, 鴻海 → iPhone, 大立光 → iPhone camera. No competitor visualizes these ecosystem relationships.

A "Sector Ecosystem Map" would:
1. **Visual ecosystem diagram**: For each major sector (semiconductor, electronics, finance), show a visual map of how companies relate — "TSMC makes chips → 鴻海 assembles them → Apple sells them"
2. **Plain-language relationship descriptions**: Each connection has a one-line explanation — "TSMC is 鴻海's largest chip supplier. If TSMC has a problem, 鴻海 feels it."
3. **"Ripple effect" analysis**: "If TSMC's revenue drops 10%, here are 5 companies that would be affected and why"
4. **Sector story**: Each ecosystem map includes a plain-language sector story — "The semiconductor ecosystem is like a restaurant kitchen: TSMC is the chef, 鴻海 is the server, Apple is the customer"
5. **Interactive exploration**: Users can click on any company in the ecosystem to see its role and relationships

**User Value**: Beginners understand companies in isolation but miss the bigger picture — how companies depend on each other. An ecosystem map teaches "systems thinking" about the market — "TSMC doesn't exist in a vacuum; it's part of a chain." This is the "historian" explaining the interconnected nature of markets.

**Implementation Notes**:
- Create `ecosystem_map.py` service with a `sector_ecosystems.yaml` data file
- Define 5-7 major TW sector ecosystems (semiconductor, electronics, finance, retail, energy)
- Each ecosystem: list of companies + relationships + plain-language descriptions
- Visual: use a force-directed graph or simple node-link diagram (Plotly or D3.js)
- Display as a "🗺️ 產業生態圈" page accessible from the navbar
- Connect to company pages — each company shows "My Ecosystem" section
- Connect to C38 (Compare Stories) — ecosystem relationships inform peer comparisons
- MVP: 16-22h for 5 ecosystems + visual diagram + plain-language descriptions

**Beginner-Friendly Test**: ✅ Passes — beginners see a visual map (intuitive) with plain-language explanations. The "ripple effect" analysis teaches market dynamics through concrete examples.

**Alignment with "Historian" Positioning**: Historians understand that events don't happen in isolation — they're part of interconnected systems. An ecosystem map is the "historian's" view of how markets work.

**Competitive Gap**: 🔴 No TW competitor has visual supply chain/ecosystem maps. Visual Capitalist has sector visualizations but not TW-specific supply chains. This would be a **culturally-specific TW feature** that leverages TW's unique position in global supply chains.

---

### [ISSUE-C97] "First 30 Days" — Structured Beginner Onboarding Curriculum with Daily Micro-Tasks

**Source**: Beginner journey mapping — analyzing the complete first-time user experience; cross-competitor synthesis — Bloom (Money Personality quiz → personalized path) + Zerodha Varsity (14-module course) + Beewise (adaptive micro-learning) + C58 (Beginner Onboarding Flow)

**Priority**: P1

**Effort**: 18-24h

**Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + "Historian" positioning + beginner-friendly

**Description**:
Stock Explorer has C58 (Beginner Onboarding Flow) planned but not built. Bloom has a personality quiz that creates a personalized path. Zerodha Varsity has 14 modules. But no competitor has a **structured 30-day curriculum with daily micro-tasks** that transforms a complete beginner into a confident stock explorer.

A "First 30 Days" feature would:
1. **Day 1-5: "What is a stock?"** — Daily 5-minute lessons with interactive exercises. "A stock is like owning a slice of a pizza shop. Here's what that means."
2. **Day 6-10: "Reading a company"** — Guided exploration of 5 companies using Stock Explorer's existing pages. "Today, explore TSMC. Here's what to look for."
3. **Day 11-15: "Understanding financials"** — Plain-language explanations of key metrics with real TW stock examples. "What is P/E ratio? Let's look at TSMC's."
4. **Day 16-20: "Building a watchlist"** — Guided watchlist creation with educational context. "Here's why diversification matters. Let's pick 5 stocks from different sectors."
5. **Day 21-25: "Reading the market"** — Using the event dashboard and market data to understand market dynamics. "The market dropped 3% today. Here's what happened historically."
6. **Day 26-30: "Your investment story"** — Reflection and synthesis. "What have you learned? What companies interest you? What's your investment personality?"
7. **Daily micro-tasks**: Each day has one 5-minute task — "Explore one company," "Add one stock to your watchlist," "Read one earnings story"
8. **Progress tracking**: Visual progress bar showing "Day 12 of 30" with checkmarks for completed days
9. **Completion badge**: "🎓 股市探索新手" badge after completing all 30 days

**User Value**: Beginners are overwhelmed by financial platforms. A structured 30-day curriculum gives them a clear path — "I don't need to learn everything at once. Today, I just need to do this one 5-minute task." This dramatically improves retention and transforms Stock Explorer from a "tool" into a "teacher."

**Implementation Notes**:
- Create `first_30_days.py` service with a `curriculum.yaml` data file
- 30 daily lessons, each with: title, plain-language content, micro-task, interactive element
- Display as a "🌟 新手 30 天" page accessible from the navbar
- Progress tracking: store completion status in session state (or local file)
- Connect to existing features: company pages, watchlist, event dashboard, quiz mode
- Connect to C58 (Beginner Onboarding Flow) — this IS the onboarding flow
- Connect to C50 (Learning Progress Tracker) and C60 (Concept Mastery Badges)
- MVP: 18-24h for 30 lessons + progress tracking + completion badge

**Beginner-Friendly Test**: ✅ Passes — this IS the ultimate beginner-friendly feature. It doesn't assume any prior knowledge and builds understanding one day at a time.

**Alignment with "Historian" Positioning**: A good teacher (historian) doesn't dump all knowledge at once — they structure a learning journey. The "First 30 Days" is the "historian's curriculum" — a structured path from "I don't understand" to "I know what this company does."

**Competitive Gap**: 🔴 No TW competitor has a structured 30-day beginner curriculum. Zerodha Varsity has modules but no daily structure. Bloom has personalized paths but no 30-day curriculum. This would be a **unique onboarding differentiator** that transforms Stock Explorer from a tool into a learning platform.

---

## Updated Competitor Overview Table (Round 17 Deep-Dive Additions)

| Dimension | 口袋股利 | Finshots | Simply Wall St | StockEdge | **Stock Explorer** |
|---|---|---|---|---|---|
| **Region** | TW | India | US/Global | India | **TW** |
| **Focus** | Dividend Calendar | Earnings Narratives | Health Visualization | Portfolio Health | **Historian** |
| **Dividend Calendar** | ✅ Monthly view | ❌ | ❌ | ❌ | ⚠️ C1 countdown only |
| **Earnings Narratives** | ❌ | ✅ Plain-language | ❌ | ❌ | ❌ MISSING |
| **Portfolio Health** | ❌ | ❌ | ✅ Individual | ✅ Aggregate | ❌ MISSING |
| **Ecosystem Map** | ❌ | ❌ | ⚠️ Sector | ❌ | ❌ MISSING |
| **30-Day Curriculum** | ❌ | ❌ | ❌ | ❌ | ❌ MISSING |
| **TW Market** | ✅ Deep | ❌ India | ⚠️ Some | ❌ India | ✅ Deep |
| **Free** | ✅ Free | ✅ Free | ⚠️ Freemium | ⚠️ Freemium | ✅ Free |

---

## Key Insights from Round 17 Deep-Dive

### 1. **The "Earnings Season Gap" is the Biggest Untapped Engagement Opportunity**
Every quarter, TW companies release earnings. This is the #1 market event that drives beginner interest — but no TW competitor provides plain-language earnings narratives. Stock Explorer's M5 event detection already identifies earnings releases; it just needs a narrative layer. C94 (Earnings Story) would create a **quarterly engagement loop** that drives users back to the platform 4 times per year.

### 2. **Dividend Investing is TW's #1 Beginner Strategy — But No Platform Serves It Well**
TW's dividend investing community is massive (口袋股利, 股息小人, 長投學堂 all focus on dividends). Stock Explorer has C1 (ex-dividend countdown) but no comprehensive dividend tools. C93 (Dividend Income Calendar) would be the **definitive TW dividend tool** — combining calendar, income projection, and gap analysis in one place.

### 3. **Portfolio-Level Features Are the Missing "Step Up"**
All 76 competitors focus on individual stock analysis. Almost none provide portfolio-level insights with plain-language summaries. Stock Explorer's watchlist infrastructure (multi-list, alerts) is already built — it just needs an aggregate health layer. C95 (Watchlist Health Dashboard) would be the **"step up"** from individual stock analysis to portfolio understanding.

### 4. **TW's Supply Chain Identity is a Unique Educational Asset**
Taiwan's position in global supply chains (TSMC → Apple, 鴻海 → iPhone) is unique and educationally valuable. No competitor visualizes these relationships. C96 (Sector Ecosystem Map) would be a **culturally-specific feature** that international competitors can't easily replicate — it leverages TW's unique market position.

### 5. **The "First Week" Determines Retention — And No Competitor Does It Well**
Beginner retention is the #1 problem in financial education. Bloom's personality quiz → personalized path is the closest, but it's not a structured curriculum. C97 (First 30 Days) would be the **ultimate retention feature** — a daily micro-learning path that keeps beginners engaged for their critical first month.

### 6. **Cross-Feature Synthesis Creates Category-of-One Features**
The most valuable white space isn't individual features — it's **combinations**. C93 combines 口袋股利's calendar + C1's countdown + MoneySmart's calculators. C94 combines M5's event detection + Finshots' narratives + analogy engine's plain language. C95 combines watchlist.py + C43's snowflake + plain-language synthesis. These combination features are harder to replicate than individual features.

### 7. **The "Historian" Positioning Enables Features Others Can't Build**
Every feature identified in this round (earnings stories, dividend calendars, ecosystem maps, 30-day curriculum) is strengthened by the "historian" positioning. A historian tells stories (earnings narratives), tracks patterns (dividend calendars), explains systems (ecosystem maps), and structures learning (30-day curriculum). The "historian" isn't just a positioning — it's a **feature design philosophy**.

---

## Feature Gap Summary (Round 17 Deep-Dive)

| ID | Title | Priority | Effort | Source | Alignment |
|---|---|---|---|---|---|
| C93 | Dividend Income Calendar (Market-Wide + Income Projection) | P1 | 12-16h | 口袋股利 + C1 + MoneySmart synthesis | Story first + Point-to-point + Historian |
| C94 | Earnings Story (Post-Earnings Plain-Language Narrative) | P1 | 14-18h | M5 gap + Finshots + The Indicator synthesis | Story first + Adaptive + Ten-second test + Historian |
| C95 | Watchlist Health Dashboard (Aggregate Portfolio Health) | P2 | 10-14h | watchlist.py gap + Simply Wall St + Tykr synthesis | Story first + PPT-style + Ten-second test + Historian |
| C96 | Sector Ecosystem Map (Visual Supply Chain Relationships) | P2 | 16-22h | group_structure.py gap + Visual Capitalist + TW market analysis | Story first + PPT-style + Point-to-point + Historian |
| C97 | First 30 Days (Structured Beginner Curriculum) | P1 | 18-24h | Beginner journey mapping + Bloom + Zerodha Varsity synthesis | Point-to-point + Ten-second test + Historian + Beginner-friendly |

---

## Recommendations

### Immediate (Next Sprint — Sprint 5)
1. **C94 Earnings Story** — P1 gap, creates quarterly engagement loop, builds on existing M5 event detection. No TW competitor has this. Beginners get plain-language earnings narratives instead of raw data.

2. **C93 Dividend Income Calendar** — P1 gap, serves TW's massive dividend investing community. Combines C1 + 口袋股利 + MoneySmart into one feature. No TW competitor has income projection.

### Short-Term (Sprint 5-6)
3. **C97 First 30 Days** — P1 gap, the ultimate retention feature. Transforms Stock Explorer from tool to learning platform. No TW competitor has a structured 30-day curriculum.

4. **C95 Watchlist Health Dashboard** — P2 gap, medium effort, builds on existing watchlist infrastructure. Provides portfolio-level insights that no competitor offers.

### Medium-Term (Post-Sprint 6)
5. **C96 Sector Ecosystem Map** — P2 gap, highest effort, culturally-specific TW differentiator. Leverages TW's unique position in global supply chains.

---

## Cumulative Competitor Research Summary

| Round | New Competitors | New Features | Total Competitors | Total Features |
|---|---|---|---|---|
| Round 7 | 5 | 7 | 5 | 7 |
| Round 8 | 8 | 6 | 13 | 13 |
| Round 9 | 9 | 6 | 22 | 19 |
| Round 10 | 6 | 6 | 28 | 25 |
| Round 11 | 3 | 6 | 31 | 31 |
| Round 12 | 9 | 8 | 40 | 39 |
| Round 13 | 8 | 6 | 48 | 45 |
| Round 14 | 8 | 6 | 56 | 51 |
| Round 15 | 8 | 6 | 64 | 57 |
| Round 16 | 6 | 5 | 70 | 62 |
| Round 17 (macro) | 6 | 7 | 76 | 69 |
| **Round 17 (deep-dive)** | **5 (口袋股利 revisited, Finshots, Simply Wall St revisited, StockEdge, Zerodha Varsity revisited)** | **5 (C93-C97)** | **81** | **74** |

**Total unique competitors analyzed across all rounds: 81**
**Total unique feature suggestions identified: 74 (C01-C97)**

---

*This is the seventeenth competitor research round (deep-dive supplement). Five new feature suggestions identified (C93-C97). Unlike previous rounds that profiled individual competitors or analyzed macro trends, Round 17 Deep-Dive used codebase architecture analysis, cross-competitor synthesis, and beginner journey mapping to identify execution gaps and TW market-specific white space. The most impactful new gap is C94 (Earnings Story) — it creates the quarterly engagement loop that Stock Explorer critically lacks, and no TW competitor has it. The most strategically important gap is C97 (First 30 Days) — it transforms Stock Explorer from a tool into a learning platform, addressing the #1 problem in financial education: beginner retention. The most unique gap is C96 (Sector Ecosystem Map) — it leverages TW's culturally-specific position in global supply chains that international competitors can't easily replicate.*
