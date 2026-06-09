# Stock Explorer Competitor Research Report

**Date:** 2026-06-09
**Author:** QA Engineer (Hermes)
**Purpose:** Analyze Taiwanese stock information competitors and identify market gaps and feature ideas

---

## Table of Contents

1. [Competitor Overview Table](#1-competitor-overview-table)
2. [In-Depth Analysis of Each Competitor](#2-in-depth-analysis-of-each-competitor)
3. [Detailed Comparison with Stock Explorer](#3-detailed-comparison-with-stock-explorer)
4. [Feature Gap Analysis](#4-feature-gap-analysis)
5. [New Feature Ideas (Source: Competitor Research)](#5-new-feature-ideas-source-competitor-research)
6. [Recommendations](#6-recommendations)

---

## 1. Competitor Overview Table

| Dimension | StatementDog | GoodInfo | CMoney | WantGoo | FinMind | **Stock Explorer** |
|------|--------|----------|--------|--------|---------|-------------------|
| **Positioning** | Financial Report Analysis Expert | All-in-One TW Stock Portal | Investment Decision Platform | Stock Community + Data | API + Data Platform | Beginner Education-Oriented |
| **Target Users** | Mid-Career Investors | All Investors | Heavy Investors | Mid/Short-Term Traders | Developers/Quants | **Beginner Investors** |
| **UI Style** | Data-Dense Tables | Traditional Portal | App Style | Forum + Minimal Charts | API Docs + Charts | **PPT Style** |
| **Plain-Language Explanation** | Partial (improving in v2) | None | Yes (Key Summaries) | None | None (raw API data) | **Core Feature** |
| **Chart Types** | Candlestick + Financial Charts | Candlestick + Technical Indicators | Diverse Charts | Basic Candlestick | Build Your Own | **Plotly Interactive Charts** |
| **Category Browsing** | ✅ Industry Categories | ✅ Industry Categories | ✅ Theme Categories | ✅ Watchlist Categories | ✅ API Query | ✅ Three Major Categories |
| **ETF Section** | ✅ Yes | ✅ Yes | ✅ Complete | ✅ Basic | ✅ API | ✅ Dedicated Page |
| **Event Detection** | ⚠️ Fundamental Alerts | ⚠️ Price Alerts | ✅ Full Alerts | ⚠️ Sporadic News | ❌ | ✅ Adaptive Engine |
| **Peer Comparison** | ✅ Complete | ⚠️ Basic | ✅ Complete | ❌ | ❌ | ✅ Benchmark-Oriented |
| **Group Structure** | ⚠️ Simplified Subsidiaries | ❌ | ⚠️ Partial | ❌ | ❌ | ✅ Point-to-Point |
| **Pricing Model** | Free + Paid Membership | Free (Ad-Supported) | Free + Subscription | Free + VIP | Free Tier + Paid | **Free & Open Source** |
| **Mobile** | ✅ RWD Website | ✅ RWD Website | ✅ Native App | ✅ RWD + App | ❌ API Only | ⚠️ Streamlit Limitations |
| **Educational** | ⚠️ Medium | ❌ Low | ⚠️ Medium | ❌ Low | ❌ None | **Core: Education-Oriented** |

---

## 2. In-Depth Analysis of Each Competitor

### 2.1 StatementDog (statementdog.com)

**Basic Information**
- One of the largest financial report analysis platforms in Taiwan, operating for over 10 years
- Focuses on "understandable financial report analysis"
- Good mobile website support (RWD)

**Core Features**
- **Financial Report Analysis:** Visual interpretation of income statements, balance sheets, and cash flow statements
- **Dividend Yield Analysis:** Historical dividend yield ranges, estimated dividends
- **US Stock Support:** Approximately 500+ US companies
- **Map Feature:** Geographic distribution of company revenue worldwide
- **Debt Analysis:** Debt ratios, interest coverage ratio, and other debt indicators
- **Line Notify Alerts:** Configurable fundamental event notifications

**Target Users**
- Mid-to-long-term investors (dividend investors, value investors)
- Ages 30-50, with some investment experience but no financial reporting expertise
- Want to understand company fundamentals without looking at raw numbers

**UI Style**
- Information-dense but more designed than traditional portals
- Plain-language explanations below each indicator (greatly improved in recent v2)
- Has a "one-sentence summary" feature, but deep tables remain the primary browsing method
- Text reports as the main focus, charts as supplementary

**Pricing Model**
- Basic features free (some data delayed)
- Paid membership (monthly): real-time data, complete financial report history, full US stock features

**Key Differences from Stock Explorer**
- ✅ StatementDog's plain-language explanations are improving, which is its core development direction
- ❌ Lacks the PPT-style one-key-point-at-a-time presentation approach
- ❌ No "adaptive analysis framework" — does not adjust analysis perspectives based on company type
- ❌ Group structure breakdown is not deep enough
- ✅ Has Line Notify alert system (Stock Explorer currently has no push notification capability)
- ✅ US stock support (Stock Explorer is Taiwan stocks only)

---

### 2.2 GoodInfo.tw

**Basic Information**
- A long-standing Taiwanese stock information website, traditional interface but complete features
- Free, ad-supported revenue model
- Similar to early Yahoo奇摩股市

**Core Features**
- **Real-Time Quotes & Candlestick Charts:** Basic technical analysis charts
- **Three Major Institutional Investors:** Foreign investment, investment trust, and proprietary trader activity
- **Monthly Revenue, Quarterly Reports:** Raw data table presentation
- **Ex-Dividend Announcements:** Ex-dividend/ex-rights schedules and cash dividend information
- **Industry Category Browsing:** Industry categories for all TW listed/OTC companies
- **Margin Trading:** Credit transaction data

**Target Users**
- All levels of investors (from beginners to experienced)
- Mid-to-older-aged investors accustomed to traditional portal operation patterns
- Users who need to quickly look up raw data

**UI Style**
- Traditional portal style, information-dense tables
- Conservative blue/gray color scheme, minimal visual design
- Text and tables as the main focus, charts limited to basic candlesticks
- Deep navigation paths, requiring multiple clicks to reach target pages
- Mobile version uses RWD adaptation

**Pricing Model**
- Completely free (ad-supported)

**Key Differences from Stock Explorer**
- ❌ GoodInfo is a "data provider" not a "data interpreter"
- ❌ Completely lacks plain-language explanations
- ❌ Monotonous chart types, only basic candlestick and bar charts
- ✅ Provides very complete raw financial report data
- ✅ Complete ex-dividend information (Stock Explorer does not yet have this feature)
- ❓ GoodInfo's users are "data seekers," Stock Explorer's users are "data learners" — fundamentally different

---

### 2.3 CMoney

**Basic Information**
- One of the largest investment analysis platforms in Taiwan, with a powerful app ecosystem
- In addition to its own platform, also provides investment analysis content for multiple brokerages
- A one-stop platform offering stock screening tools, news, and research reports

**Core Features**
- **Stock Screening Tools (Flagship Feature):** Multi-condition filtering (technical, fundamental, chip analysis)
- **AI Stock Picking:** AI model-recommended buy/sell targets
- **Research Reports:** Integration of institutional and analyst reports
- **News Alerts:** Real-time TW stock news push notifications
- **Portfolio Management:** Performance tracking of watchlist combinations
- **Video Tutorials:** Investment education videos

**Target Users**
- Heavy investors (watch the market daily, trade frequently)
- Investors who need to use stock screening tools to filter targets
- Users who want a one-stop investment decision platform
- Some beginner users (using video tutorial features)

**UI Style**
- Strong app-oriented style (primary usage scenario is mobile)
- Dark theme, app bottom navigation as the main pattern
- Card-style content presentation, quick swipe browsing
- Homepage has many data cards (market index, holdings, news)

**Pricing Model**
- Basic features free
- Advanced features require paid subscription (number of screening conditions, AI stock picking quota)
- Brokerage subscription model (using CMoney content through brokerage apps)

**Key Differences from Stock Explorer**
- ❌ CMoney is "stock-picking oriented," Stock Explorer is "understanding oriented"
- ❌ CMoney directly calls buy/sell, Stock Explorer positions itself as a "historian, not a stock critic"
- ✅ CMoney's stock screening tools are very powerful (Stock Explorer doesn't have this feature, but the direction is different)
- ✅ CMoney has an app, more mature mobile experience
- ✅ News alerts and push notification features are comprehensive
- ❌ Lacks plain-language explanations and educational framework

---

### 2.4 WantGoo (wantgoo.com)

**Basic Information**
- A well-known Taiwanese stock community + data platform
- Has a large amount of user-generated content (UGC)
- Recent global stock market map is its differentiating highlight

**Core Features**
- **Global Stock Market Map:** Heat map showing global market gains/losses (product differentiation highlight)
- **Market Thermometer:** Presents market overheating/cooling in a "feels-like temperature" format
- **Financial Data:** Basic financial reports, revenue data
- **Stock Analyzer:** Quickly generates stock analysis reports (downloadable as PPT)
- **User Forums:** User discussion areas
- **Ranking Feature:** Ranks TW companies by various indicators (dividend yield, growth rate, etc.)

**Target Users**
- Mid-to-short-term traders
- Investors who enjoy forums and community interaction
- Users who need to quickly obtain ranking/filtering results

**UI Style**
- Clean, modern design
- Heavy use of infographic-style presentation
- Global stock market map visualization is outstanding
- Charts as the main focus, text as supplementary

**Pricing Model**
- Free (ad-supported revenue)
- VIP membership removes ads + additional features

**Key Differences from Stock Explorer**
- ✅ **Global Stock Market Map:** The approach of visualizing global market temperature is worth learning from
- ✅ **Market Thermometer:** Uses a simple "feels-like" concept to let beginners intuitively understand market conditions
- ✅ **[New Feature Idea] Stock Analysis PPT Download:** Users can download stock analysis presentations (but quality is average)
- ❌ WantGoo focuses on short-term trading, Stock Explorer focuses on long-term understanding
- ❌ No plain-language explanation framework

---

### 2.5 FinMind (finmindtrade.com)

**Basic Information**
- One of the largest financial data API providers in Taiwan
- Open-source datasets + paid API tier
- The underlying data provider used by Stock Explorer

**Core Features**
- **API Services:** Python SDK, REST API
- **50+ TW Stock Datasets:** Stock prices, financial reports, chip data, ETFs, etc.
- **Dashboard (Paid):** Built-in simple dashboard (relatively basic features)
- **Data Lab:** Online SQL queries (paid feature)
- **Data Marketplace:** Custom datasets

**Target Users**
- Developers (building their own stock analysis applications)
- Quantitative traders (strategy development)
- Data scientists (financial data research)
- **Not** general investors

**UI Style**
- Developer-oriented technical documentation style
- Dashboard is only a secondary feature, simple UI
- Centered around API documentation and code examples

**Pricing Model**
- Free tier (limited API calls + partial datasets)
- Paid tier (more API calls, complete datasets)

**Key Differences from Stock Explorer**
- 🔄 **Complementary relationship, not a competitor:** FinMind is Stock Explorer's data provider
- ❌ FinMind's Dashboard features are extremely weak, with no indicator explanation capability
- ❌ Completely lacks education-oriented design
- ✅ FinMind is a competitor but also has room for collaboration

---

### 2.6 Other Notable Competitors

#### 2.6.1 Yahoo奇摩股市 (tw.stock.yahoo.com)

**Basic Information**
- The largest free stock information portal in Taiwan
- Highest market share, but lacks deep analysis

**Core Features**
- Real-time quotes, candlesticks, news
- Watchlist
- Basic financial report data
- Forums (mixed reviews)

**Differences from Stock Explorer**
- Information-dense but explanation-poor
- Complete watchlist features but lacks educational elements

#### 2.6.2 Anue (anue.cnyes.com)

**Core Features**
- News-oriented, large volume of real-time news
- TW, HK, US, and CN stock markets
- Economic data calendar
- Video programs

**Differences**
- Professional news website, not an analysis platform

#### 2.6.3 TEJ (Taiwan Economic Journal)

**Positioning**
- Professional financial database (similar to a Taiwanese version of Bloomberg)
- Annual subscription, high price
- Targets professional institutions and researchers

**Differences**
- Completely different audience, no direct competition with Stock Explorer

#### 2.6.4 JZ Invest (Investment Assistant App)

**Positioning**
- Mobile quantitative investment app
- Very comprehensive notification system
- Alert-first driven usage

**Differences**
- Alert-first vs education-first

---

## 3. Detailed Comparison with Stock Explorer

### 3.1 Positioning Comparison Chart

```
Education ←──────────────────────────────→ Professional

Stock Explorer    StatementDog     GoodInfo     CMoney     WantGoo
     ●                ●               ●            ●          ●
     Beginner         Mid-level       All          Heavy      Mid/Short-Term
     Understanding    Analysis        Data Portal  Stock-     Trading
     Oriented         Oriented                     Picking    Oriented
                                                  Oriented
```

### 3.2 Stock Explorer's Unique Features (What Competitors Can't Do)

| Unique Feature | Description | Competitive Gap Level |
|---------|------|------------|
| **PPT-Style One Point at a Time** | One concept per slide, images as primary, text as supplementary | 🟡 Medium (WantGoo has similar infographics, but not PPT structure) |
| **Plain-Language Explanation Engine** | 12+ everyday analogies (e.g., gross margin → how much profit per $100 sold) | 🟡 Medium (StatementDog is improving) |
| **Adaptive Analysis Framework** | Recommends different analysis perspectives based on company type (group/single/ETF) | 🔴 High (no competitor does this) |
| **Benchmark-Oriented Peer Comparison** | Automatically compares against industry #1, explains gap reasons | 🔴 High (most competitors just display numbers side by side) |
| **Point-to-Point Group Structure** | Parent company → subsidiaries, with business descriptions and ratios | 🔴 High (only StatementDog has basic functionality) |
| **Event Detection Engine** | Revenue changes ±30%, news, stock price ±7% auto-detection | 🟡 Medium (CMoney's notification system is more complete) |
| **Educational System Architecture** | Product positioning is "understand a company" → no buy/sell calls | 🔴 High (all competitors ultimately aim for "stock picking") |
| **Adaptive Content** | Major events trigger content updates | 🟡 Medium (mostly manual) |
| **Ten-Second Test** | Beginner-friendly comprehension threshold requirement | 🔴 High (industry standard is different) |
| **Open Source Transparency** | All code publicly available on GitHub | 🟡 Low (CMoney has an open API tier) |

### 3.3 Features Competitors Have That Stock Explorer Doesn't Yet

| Missing Feature | Competitor Reference | Priority |
|---------|---------|-------|
| **Push Notifications (Line/App)** | StatementDog (Line Notify), CMoney (App Push), JZ Invest | 🔴 High |
| **Ex-Dividend Calendar** | GoodInfo (complete ex-dividend schedule) | 🔴 High |
| **AI Stock Picking/Recommendations** | CMoney (AI stock picking), WantGoo (ranking tools) | 🟡 Medium (different direction) |
| **Global/International Markets** | WantGoo (global map), GoodInfo (international indices) | 🟢 Low (Phase 1 focuses on TW stocks) |
| **Portfolio Performance Tracking** | CMoney (holdings tracking, realized/unrealized P&L) | 🟡 Medium |
| **Video Tutorials** | CMoney (investment courses) | 🟡 Medium |
| **Quantitative Backtesting** | JZ Invest, StatementDog (partial) | 🟢 Low (different direction) |
| **Stock Analysis PPT Download** | WantGoo (auto-generated analysis presentations) | 🟡 Medium |
| **Market Thermometer/Fear Index** | WantGoo (feels-like temperature), CMoney (market sentiment indicators) | 🟡 Medium |
| **Multiple Watchlists** | Yahoo Finance, StatementDog (multiple watchlists + Line push) | 🟡 Medium |
| **Real-Time Updates (WebSocket)** | StatementDog, CMoney (real-time prices) | 🟡 Medium (Streamlit limitations, requires architecture changes) |
| **Forums/Community Features** | WantGoo, GoodInfo (message boards) | 🟢 Low (education positioning doesn't need it) |

---

## 4. Feature Gap Analysis

### 4.1 P0 Gaps (Core Experience Gaps, Missing These Negatively Impacts Users)

#### Gap 1: Ex-Dividend Information
- **Current State:** Stock Explorer has no ex-dividend information at all
- **Competitor Reference:** GoodInfo has complete ex-dividend schedules; StatementDog has dividend yield analysis
- **User Scenario:** "I want to know when TSMC pays dividends and how much?" — Stock Explorer currently cannot answer this
- **Data Feasibility:** FinMind has a "TaiwanStockDividend" API (need to confirm if free tier includes it)

#### Gap 2: Push Notification System
- **Current State:** Stock Explorer has an event detection engine, but cannot "push" events out
- **Competitor Reference:** StatementDog has Line Notify; CMoney has App Push
- **User Scenario:** "I want to know immediately when TSMC revenue drops 30%" — requires actively opening the app to see
- **Implementation Suggestion:** Start with email notifications (low cost), then add Line Notify (requires Bot account)

#### Gap 3: Multiple Watchlists
- **Current State:** Only one "My Watchlist"
- **Competitor Reference:** Yahoo Finance (multiple watchlists); StatementDog (multiple lists + Line push)
- **User Scenario:** I want to separately track "dividend stocks," "watchlist," and "high dividend yield" categories
- **Implementation Suggestion:** Add a `lists` structure to watchlist.yaml

### 4.2 P1 Gaps (Important but Non-Critical Gaps)

#### Gap 4: Market Temperature/Sentiment Indicators
- **Current State:** No macroeconomic or market sentiment indicators
- **Competitor Reference:** WantGoo "Market Thermometer"
- **User Scenario:** Beginners want to know "is the market hot or cold right now?"
- **Data Feasibility:** FinMind has "TaiwanStockInstitutionalInvestorsBuySell" which can calculate institutional investor trends

#### Gap 5: Portfolio P&L Tracking
- **Current State:** Watchlist only has price alerts, no position P&L management
- **Competitor Reference:** CMoney (complete portfolio management)
- **User Scenario:** I want to know the current overall return rate of my "dividend portfolio"
- **Implementation Suggestion:** Add "quantity held" and "cost basis" fields to watchlist

#### Gap 6: Stock Analysis Report Download
- **Current State:** Cannot download the current analysis page
- **Competitor Reference:** WantGoo (one-click PPT generation)
- **User Scenario:** Want to share a company analysis with friends
- **Implementation Suggestion:** Use python-pptx to auto-generate PPT (foundation already exists)

### 4.3 P2 Gaps (Nice-to-Have Feature Gaps)

#### Gap 7: US Stocks/International Markets
- **Current State:** Only supports TW stocks
- **Competitor Reference:** StatementDog (500+ US stocks); GoodInfo (international indices)
- **Suggestion:** Consider after M5, FinMind already has US stock data

#### Gap 8: Quantitative Indicators/Stock Screening Conditions
- **Current State:** No technical indicators (e.g., moving averages, RSI, Bollinger Bands, etc.)
- **Competitor Reference:** CMoney (complete technical indicators + screening)
- **Suggestion:** Teaching-oriented vs stock-picking-oriented direction choice — recommend maintaining education positioning for now

---

## 5. New Feature Ideas

> **Tag: Source: Competitor Research**

### 🔴 High Priority New Features

#### Idea A: Ex-Dividend Calendar (from GoodInfo + StatementDog)
```
Description: Add a "Dividend Information" section to the business card page
  - Ex-dividend/ex-rights schedule for the past 5 years (ex-dividend date, ex-rights date)
  - Historical dividends (cash dividends, stock dividends)
  - Plain-language explanation: "Over the past 5 years, TSMC paid approximately $2.75 per quarter"
  - Estimated dividend yield (calculated at current stock price)
Data: FinMind TaiwanStockDividend
Page: business_card.py (new section)
Competitive Gap: 🔴 Severely Missing
```

#### Idea B: Push Notification System (from StatementDog Line Notify)
```
Description: After setting notification conditions, proactively notify users
  Phase 1: Email notifications (low cost)
    - Revenue changes ±30%
    - Stock price changes ±7%
    - Event detection engine already has the data, just need to add a sending layer
  
  Phase 2: Line Notify (requires Bot account)
    - Paid feature or premium membership exclusive
    - StatementDog's successful model: Line Notify is their highest converting paid feature
Technology: Background worker + SMTP (Phase 1)
Competitive Gap: 🔴 Severely Missing — all competitors have notification capabilities
```

#### Idea C: Multiple Watchlist Lists (from Yahoo Finance)
```
Description: Allow users to create multiple watchlists
  Structure example:
    - "Dividend List" (stable dividend-paying stocks)
    - "Watchlist" (want to buy but haven't yet)
    - "High Dividend Yield"
  
  Files to modify:
    - watchlist.yaml structure refactor (list_name, stocks[])
    - watchlist_page.py (multi-tab pages)
    - Business card page add "which list to join" selector
Competitive Gap: 🔴 P0 Gap
```

### 🟡 Medium Priority New Features

#### Idea D: Market Thermometer (from WantGoo)
```
Description: Add a "Market Temperature" indicator to the homepage
  Calculation method:
    - Three major institutional investors buy/sell (5-day average)
    - Market trading volume (hot vs cold)
    - Ratio of limit-up/limit-down stocks
  Presentation: Feels-like temperature (🔥Hot/😊Normal/🥶Cold) + plain-language explanation
  Page: New section on homepage or event dashboard
Competitive Gap: 🟡 P1 Gap
```

#### Idea E: Portfolio P&L Management (from CMoney)
```
Description: Watchlist evolution — add position management
  New features:
    - Cost per share
    - Quantity held
    - Unrealized P&L (real-time)
    - Realized P&L (historical trades)
    - Total portfolio return rate
  Page: Evolve existing watchlist_page.py
Competitive Gap: 🟡 P1 Gap
```

#### Idea F: Stock Analysis PPT Auto-Generation (from WantGoo, extending Stock Explorer's PPT style)
```
Description: One-click download of current analysis results as a PPT presentation
  Leverage existing PPT-style CSS, use python-pptx to generate actual PPT
  Includes:
    - Company business card
    - Operations health check highlights
    - Financial health summary
    - Peer comparison radar chart
  Technology: python-pptx + data from each page
  Page: Add "Download PPT" button on each page
Competitive Gap: 🟡 P1 Gap
  Differentiation: Stock Explorer's PPT style is more refined and more educational than WantGoo's
```

#### Idea G: User-Defined Event Thresholds (extending from Event Detection Engine)
```
Description: Let users customize event detection thresholds
  Current: Fixed (revenue ±30%, stock price ±7%)
  Evolution:
    - User-adjustable sensitivity
    - New event types (institutional investors buying/selling for N consecutive days, revenue declining for N consecutive months)
  Page: Settings page (new page)
Competitive Gap: 🟡 Differentiating Feature
```

### 🟢 Low Priority/Future Consideration

#### Idea H: Video Tutorials (from CMoney)
```
Description: Embed 30-second plain-language explanation videos below each indicator
  High production cost, recommend manual production after M5
  Example: What is "P/E Ratio"? 30-second animated explanation
```

#### Idea I: US Stock Support (from StatementDog)
```
Description: Extended support for US stocks (AAPL, MSFT, GOOG...)
  FinMind supports US stock data
  Target users: Those already familiar with TW stock analysis framework, wanting to extend to US stocks
  Timeline: After M5
```

#### Idea J: Global Market Map (from WantGoo, differentiated extension)
```
Description: Simplified map showing global market status
  TW stocks as primary, others as supplementary:
    - US (Dow Jones, NASDAQ, S&P 500)
    - Europe (Germany DAX, UK FTSE)
    - Japan (Nikkei 225)
    - China (Shanghai Composite, Shenzhen Composite)
  Presentation: 🟢Up 🔴Down ↔️Flat + disproportionate visualization
  Page: Homepage section or standalone page
  Differentiation: WantGoo's map leans toward "trading heat," Stock Explorer leans toward "fundamental understanding"
```

---

## 6. Recommendations

### 6.1 Strategic Positioning Recommendations

**Stock Explorer's best positioning is not to "replace" competitors, but to serve as an "education bridge"**

```
Assumed User Journey:
1. Beginners first use "Stock Explorer" to understand a company's essence
2. After starting to invest, they naturally flow to GoodInfo / StatementDog when they need data tools
3. After becoming experienced investors, they move to the next level

→ Stock Explorer's KPI should not be DAU/retention rate
→ It should be "what did users learn" and "did they successfully build investment awareness"
```

**Recommendation: Do not directly compete with competitors on the following features**
- ❌ Real-time quote speed (vs GoodInfo)
- ❌ Stock screening tools (vs CMoney)
- ❌ Community features (vs WantGoo)
- ❌ Technical analysis depth (vs StatementDog)

**Recommendation: Fully develop the following differentiators**
- ✅ Plain-language explanation quality (vs all competitors)
- ✅ PPT-style educational experience (vs all competitors)
- ✅ Adaptive analysis framework (vs all competitors)
- ✅ Event detection and notifications (achievable in the near term)
- ✅ Open source trust image (vs commercial competitors)

### 6.2 Feature Development Roadmap Recommendations

**Phase 1 (M5 Wrap-Up + Ex-Dividend)**
1. ✅ Add ex-dividend information to business card page (Idea A)
2. ✅ Push notification system email version (Idea B)
3. ✅ Multiple watchlist lists (Idea C)

**Phase 2 (Market + Export)**
4. 🔄 Market thermometer (Idea D)
5. 🔄 Portfolio P&L management (Idea E)
6. 🔄 PPT auto-generation (Idea F)

**Phase 3 (Personalization + International)**
7. 📋 Custom event thresholds (Idea G)
8. 📋 Video tutorials (Idea H)
9. 📋 US stock support (Idea I)
10. 📋 Global market map (Idea J)

### 6.3 Moat Recommendations

**Moats that Stock Explorer can build:**

1. **Educational Content Accumulation:** The plain-language explanation engine's analogy library, template library — difficult for competitors to quickly replicate
2. **User Cognitive Pathway:** A "company understanding process" built over 3 years of usage experience — competitors cannot easily poach users' mental frameworks
3. **Open Source Trust Endorsement:** "My analysis logic is completely transparent" — commercial competitors cannot achieve this
4. **Adaptive Framework Data:** As more companies are added, analysis framework recommendations become increasingly accurate — data network effects

### 6.4 Decisions Requiring Daniel's Confirmation

1. **Push Notifications:** Email (low cost, low reach) vs Line Notify (requires Bot account, high reach)?
2. **Direction Choice:** Whether to add any "stock screening" features, insisting on pure education positioning?
3. **Internationalization:** Whether to support US stocks? This would affect the business card page and comparison logic
4. **Video Content:** Self-produced vs embedding existing YouTube resources vs abandoning

---

## Appendix: Competitor Pricing Model Comparison

| Platform | Free Tier | Paid Plans | Estimated ARPU | Business Model |
|------|----------|---------|----------|---------|
| StatementDog | Delayed real-time data, limited features | Monthly membership (~$300-500 NTD/month) | Medium | Subscription |
| GoodInfo | Completely free | None | Low (Ads) | Advertising |
| CMoney | Basic features | Monthly/annual (~$500-2000+ NTD/month) | Medium-High | Subscription + B2B Licensing |
| WantGoo | Completely free | VIP ad removal (low price) | Low | Advertising + VIP |
| FinMind | Limited API calls | Monthly (~$1000-5000+ NTD/month) | Medium | SaaS API |
| **Stock Explorer** | Completely free & open source | None | Zero | **Open Source/Free** |

---

## Conclusion

Stock Explorer's core differentiators — **education-oriented + PPT style + plain-language explanations + adaptive framework** — are unique and valuable in the current TW stock platform market.

The three biggest gaps that must be filled:
1. **Ex-Dividend Information** (GoodInfo has it, the most common question from beginners)
2. **Push Notifications** (StatementDog and CMoney both have it, key to retention)
3. **Multiple Watchlist Lists** (basic feature gap)

All of the above new feature **ideas come from competitor research**, with implementation priority based on gap analysis ranking.

---

*Research Date: 2026-06-09 | Next Update: 2026-06-12 (three-cycle rotation)*
