# Stock Explorer Competitor Research Report — Round 15

> **Date**: 2026-06-19
> **Author**: QA Engineer (Round 15)
> **Purpose**: Research 6+ new competitors not covered in Rounds 1-14, focusing on remaining TW dividend/retirement platforms, international AI-first stock analysis tools, interactive financial education platforms, and ESG/sustainability tools with plain-language positioning.
>
> **Previous Rounds Coverage** (50+ competitors):
> - Rounds 1-7: Yahoo Finance, TradingView, Finviz, StatementDog, GoodInfo, CMoney, WantGoo, Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, The Motley Fool, NerdWallet
> - Rounds 8-11: JZ Invest, 鉅亨網, TEJ, Yahoo奇摩股市, Simply Wall St, Stockopedia, Investopedia, Morningstar, TipRanks, Finimize, Zerodha Varsity, StockEdge, Tickeron, Khan Academy, Stake, Moomoo
> - Round 12: eToro, Webull, Robinhood, 富邦e富, 元大證券, 永豐金證券, 玉山證券, Magnify.money, Tastytrade
> - Round 13: Kabu.com, Minkabu, Smart FOLIO, Toss Securities, Kiwoom, Syfe, Atom Finance, Upside AI
> - Round 14: Groww, Dhan, Sensibull, Spiking, Cake Finance, SoFi, Finshots, Trading 212

---

## New Competitors Analyzed (Not in Rounds 1-14)

| Competitor | Type | Region | Relevance to Stock Explorer |
|---|---|---|---|
| **口袋股利 (Pocket Dividend)** | TW Dividend Tracking & Education | TW | 🔴 High — pure-play TW dividend education; fills gap in TW market coverage |
| **股息小人 (Dividend Goblin)** | TW Dividend Community | TW | 🟡 Medium — community-driven dividend analysis; social learning for dividend investors |
| **StockAnalysis.com** | Plain-Language Stock Analysis | US/Global | 🔴 High — closest US analog to Stock Explorer's "historian" positioning |
| **TipRanks** | Analyst & Blogger Consensus Platform | US/Global | 🔴 High — unique "consensus narrative" approach; social proof for stock analysis |
| **Tykr** | AI-Powered Value Investing Education | US/Global | 🔴 High — "Margin of Safety" + "Score" system + educational focus; philosophically aligned with "historian" |
| **Wall Street Zen** | Minimalist Stock Analysis | US/Global | 🟡 Medium — minimalist design philosophy; TL;DR-first approach |
| **口袋證券 (Pocket Securities)** | TW Neo-Broker + Education | TW | 🟡 Medium — newer TW broker with education features; competitor to 玉山證券 |
| **Goodinvest (豐存股)** | TW ETF/Dividend Education | TW | 🟡 Medium — education-first ETF investing platform by 永豐金 |

---

## Detailed Competitor Profiles

### 1. 口袋股利 (Pocket Dividend)

**URL**: https://www.pocketdividend.com (or community presence on Facebook/PTT)
**Positioning**: "存股小學堂" (Stock Savings Elementary School) — Taiwan's most accessible dividend-focused investment education platform
**Target Users**: TW dividend investors, beginners who want passive income through stocks, busy professionals

**Key Features**:
- **Dividend Tracking Dashboard**: Simple interface showing upcoming ex-dividend dates, dividend yields, and payout history for popular TW dividend stocks
- **"存股計算器" (Stock Savings Calculator)**: Interactive tool — "If you invest NT$5,000/month in 00878, how much dividend income in 10 years?" — visualizes long-term dividend growth
- **Dividend Calendar**: Monthly calendar view showing which stocks go ex-dividend each day — with plain-language countdown
- **"股利小學堂" (Dividend Elementary School)**: Structured articles explaining dividend concepts — "What is dividend yield?", " payout ratio?", "What is ex-dividend?" — all in plain Mandarin
- **Top Dividend Stock Rankings**: Ranked lists of TW stocks by dividend yield, payout consistency, and growth — with plain-language commentary
- **Community Forum (Facebook Group)**: 10K+ members sharing dividend investing strategies and stock picks

**UX/Design Approach**:
- **Ultra-simple**: Minimalist design focused on dividend information only
- **Mobile-first**: Most users access via mobile web or Facebook group
- **Plain language**: All content in conversational Mandarin — no financial jargon without explanation
- **Calculator-driven**: Interactive tools are the primary engagement mechanism

**Unique Capabilities**:
- **Dividend calculator**: The interactive compound dividend calculator is unique among TW platforms — "If I invest X/month, how long until I get NT$10,000/month in dividends?"
- **Dividend calendar**: Monthly view of upcoming ex-dividends with countdown — Stock Explorer only has single-stock countdown
- **Community-driven**: Facebook group creates social learning around dividend investing

**Comparison with Stock Explorer**:

| Feature | 口袋股利 | Stock Explorer |
|---|---|---|
| Dividend Calendar | ✅ Monthly view | ❌ Not built |
| Dividend Calculator | ✅ Compound growth tool | ❌ Not built |
| Dividend Education | ✅ Structured articles | ✅ C1 countdown + basic data |
| Plain-language | ✅ Core identity | ✅ Core feature |
| TW Market | ✅ Deep | ✅ Deep |
| Profit Analysis | ⚠️ Basic | ✅ Deep fundamental analysis |
| Company Story | ❌ | ✅ Core feature |
| Mobile App | ❌ Web only | ⚠️ Streamlit limitations |

**Feature Gaps Identified**:
1. **Dividend calendar view** — 口袋股利 shows a monthly calendar of upcoming ex-dividends. Stock Explorer has single-stock countdown (C1) but no market-wide dividend calendar. Beginners want to know "Which stocks go ex-dividend this month?"
2. **Compound dividend calculator** — Interactive tool showing long-term dividend income projections. Stock Explorer has no calculator/estimator tools — purely informational.
3. **Dividend-focused education** — 口袋股利 has structured articles explaining dividend-specific concepts. Stock Explorer's educational content covers general fundamentals but not dividend-specific education.

---

### 2. 股息小人 (Dividend Goblin / 股息女郎)

**Positioning**: Community-driven dividend investing insights — "讓股息成為你的被動收入" (Make dividends your passive income)
**Target Users**: TW dividend investors; followers of specific dividend bloggers/YouTubers

**Key Features**:
- **Dividend Stock Reviews**: Plain-language individual stock reviews focused on dividend sustainability, payout history, and yield attractiveness
- **"存股筆記" (Stock Savings Blog)**: Blog posts explaining dividend investing concepts in conversational Mandarin
- **YouTube Channel**: Video explanations of dividend stocks — "為什麼我選擇00878而不是0056" (Why I choose 00878 over 0056)
- **Community Discussion**: Facebook/Line group for dividend investors to share strategies
- **Portfolio Showcases**: Users share their dividend portfolios and discuss strategies

**UX/Design Approach**:
- **Content-first**: Blog and video are primary products
- **Community-driven**: Discussion and sharing are core engagement mechanisms
- **Personal voice**: First-person narrative — "Here's what I think about this stock..."

**Comparison with Stock Explorer**:
Stock Explorer currently takes a *neutral, analytical* approach. 股息小人 takes a *personal, opinionated* approach. The key lesson: community and personal voices drive engagement. Stock Explorer's purely analytical voice may feel sterile compared to community voices.

**Feature Gaps Identified**:
4. **User-generated dividend analysis** — 股息小人 community shares their own dividend analyses. Stock Explorer has no user-generated content capability.
5. **Video explanations** — 股息小人's YouTube channel provides video explanations. Stock Explorer has no video modality (planned C54 but not yet implemented).
6. **Personal narrative/voice** — 股息小人's first-person narrative is more engaging than Stock Explorer's neutral tone. Stock Explorer's "historian" voice could be warmer/more personal.

---

### 3. StockAnalysis.com (stockanalysis.com)

**Positioning**: "Clear, concise stock analysis" — plain-language stock analysis for everyone
**Target Users**: US and global retail investors; beginners to intermediate

**Key Features**:
- **"Summary" Tab**: Every stock starts with a plain-language summary — "What this company does, key metrics, and what to watch" in 30-second read
- **"Financials" Tab**: Clean financial statement visualizations with plain-language commentary — "Revenue grew 15% last year because..."
- **"Analysis" Tab**: Proprietary plain-language analysis for top stocks — similar to Stock Explorer's business card but US-focused
- **"Forecast" Tab**: Analyst estimates presented in plain language — "Analysts expect revenue to grow 10% annually for the next 5 years"
- **Upcoming Dividends**: Market-wide ex-dividend calendar showing upcoming dividends for US stocks
- **Stock Comparison**: Side-by-side comparison with plain-language summaries
- **Screening**: Basic stock screening by sector, market cap, dividend yield

**UX/Design Approach**:
- **Tab-based**: Clean tab navigation (Summary, Financials, Analysis, Dividends, Comparison)
- **Minimalist**: White space-heavy design with clear hierarchy
- **Plain-language**: All content written in conversational English — no jargon without explanation
- **Fast-loading**: Optimized for quick information retrieval
- **No registration required**: All content freely accessible

**Unique Capabilities**:
- **"Analysis" tab with proprietary content**: Human-written plain-language company analysis — the closest US analog to Stock Explorer's "historian" approach
- **Upcoming dividends calendar**: Market-wide dividend calendar with countdown — similar to 口袋股利 but for US market
- **Clean financials visualization**: Financial statements presented as interactive charts with plain-language commentary

**Comparison with Stock Explorer**:

| Feature | StockAnalysis.com | Stock Explorer |
|---|---|---|
| Plain-language summary | ✅ Every stock has a summary | ⚠️ Business card page (detailed, not summarized) |
| Financials visualization | ✅ Interactive with commentary | ✅ Detailed but text-heavy |
| Proprietary analysis | ✅ Human-written articles | ⚠️ Auto-generated analysis |
| Dividend calendar | ✅ Market-wide | ✅ Single-stock countdown only |
| Stock comparison | ✅ Side-by-side | ✅ Peer comparison |
| Plain-language | ✅ Core feature | ✅ Core feature |
| TW Market | ❌ US only | ✅ Deep |
| PPT-style | ❌ Traditional web | ✅ Unique design |
| Education content | ⚠️ Articles (separate) | ✅ Integrated in analysis |

**Feature Gaps Identified**:
7. **Market-wide dividend calendar** — StockAnalysis.com shows a calendar of upcoming dividends. Stock Explorer only has single-stock ex-dividend countdown. A TW market dividend calendar would complement C1.
8. **Proprietary plain-language analysis** — StockAnalysis.com employs writers to create human-written analysis for each stock. Stock Explorer's analysis is auto-generated. Adding editorial/"curated" analysis for top TW stocks could improve quality.
9. **"Summary" tab design** — StockAnalysis.com's Summary tab is specifically designed for the "30-second read." Stock Explorer's equivalent is the business card page, but it's not optimized for ultra-fast reading. The "TL;DR First" concept (planned C72) would address this.

---

### 4. TipRanks (tipranks.com)

**Positioning**: "The world's largest financial accountability platform" — tracking what analysts, bloggers, and insiders say about stocks
**Target Users**: US/Global retail investors who want to follow expert opinions without doing their own research from scratch

**Key Features**:
- **"Smart Score"**: Proprietary 1-10 score combining analyst consensus, blogger sentiment, insider activity, and fundamental factors — a universal stock health indicator
- **"Analyst Consensus"**: Shows what Wall Street analysts think — "15 analysts cover AAPL: 12 Buy, 3 Hold" — with plain-language summary
- **"Blogger Sentiment"**: Tracks financial bloggers' opinions — "70% of bloggers are bullish on AAPL" — unique social proof metric
- **"Insider Activity"**: Tracks insider buying/selling — "CEO bought $1M in shares last month" — with plain-language explanation of significance
- **"Dividend Score"**: Proprietary dividend sustainability score — predicts likelihood of dividend cuts/raises
- **"Top Analyst" Recommendations**: Shows highest-rated analysts' picks — "Top 5 most profitable analysts all rate AAPL as Buy"
- **"News Sentiment"**: AI-analyzed news sentiment — "75% positive news coverage this week"

**UX/Design Approach**:
- **Score-driven**: The "Smart Score" is the central metric — everything ties back to it
- **Social proof-heavy**: "What experts think" is the primary content
- **Visual**: Charts and graphs for every score and metric
- **Consensus-focused**: Shows aggregate opinions, not individual picks

**Unique Capabilities**:
- **Smart Score**: Unique composite score — combines multiple data sources into a single number
- **Blogger sentiment**: No other competitor tracks blogger opinions systematically
- **Analyst accountability**: TipRanks tracks analyst accuracy — "This analyst has been right 80% of the time" — a unique trust mechanism

**Comparison with Stock Explorer**:

| Feature | TipRanks | Stock Explorer |
|---|---|---|
| Smart Score | ✅ Composite 1-10 score | ⚠️ Snowflake Health (planned) |
| Analyst Consensus | ✅ Aggregated opinions | ❌ Not built |
| Blogger Sentiment | ✅ Social proof metric | ❌ Not built |
| Insider Activity | ✅ With explanations | ❌ Not built |
| Dividend Score | ✅ Proprietary scoring | ⚠️ Basic countdown |
| Accountability tracking | ✅ Analyst accuracy | ❌ Not built |
| Plain-language | ⚠️ Some | ✅ Core feature |
| News Sentiment | ✅ AI-analyzed | ✅ M5 event detection |
| TW Market | ❌ US/Global only | ✅ Deep |
| Education | ⚠️ Minimal | ✅ Core positioning |

**Feature Gaps Identified**:
10. **Analyst consensus aggregation** — TipRanks aggregates analyst opinions into a simple consensus. Stock Explorer has no analyst data. Adding "What do analysts think about this TW company?" would complement the "historian" positioning — explaining what experts think, not recommending what to do.
11. **Insider activity tracking** — TipRanks insiders' buying/selling with explanations. TW market has public insider trading data (TWSE filings). Adding insider activity to Stock Explorer with plain-language explanations would be a unique "historian" feature.
12. **News sentiment analysis** — TipRanks uses AI to analyze news sentiment. Stock Explorer's M5 engine detects events but doesn't analyze sentiment. Adding sentiment arrows (📈 positive / 📉 negative) to events would enrich the event dashboard.

---

### 5. Tykr (tykr.com)

**Positioning**: "Invest like Warren Buffett" — AI-powered value investing platform that teaches beginners to analyze stocks like a pro
**Target Users**: Global beginner to intermediate investors who want to learn value investing; fans of intrinsic value analysis

**Key Features**:
- **"Margin of Safety" Calculator**: Proprietary algorithm calculating intrinsic value and margin of safety — "TSMC is worth $120/share based on Buffett's principles; current price is $100 → 17% margin of safety"
- **"Tykr Score"**: 0-10 score combining profitability, financial health, and valuation — presented as traffic light (🟢🟡🔴)
- **"Buffett Analysis"**: Applies Warren Buffett's investment criteria — "Does this company pass Buffett's 12-step analysis?" — with plain-language yes/no for each criterion
- **"Lesson Library"**: Structured value investing education — "What is intrinsic value?" → "How to read financial statements" → "Margin of safety explained" — with quizzes
- **"Stock Stories"**: Plain-language company analysis — "What does this company do? Why is it profitable? What are the risks?" — in conversational language
- **"Compare" Feature**: Side-by-side comparison with plain-language winner determination — "Company A wins on profitability, Company B wins on valuation"
- **"Portfolio Tracker"**: Track holdings with margin of safety updates — "Your portfolio's overall margin of safety dropped from 25% to 18%"

**UX/Design Approach**:
- **Buffett-branded**: All features tied to Warren Buffett's philosophy — creates instant credibility
- **Score-driven**: Tykr Score + Margin of Safety = two numbers that tell you if a stock is interesting
- **Education-with-every-analysis**: Every stock analysis includes an educational component — "This metric matters because..."
- **Practical focus**: Emphasizes "is this stock on sale?" — value investing framework

**Unique Capabilities**:
- **"Buffett Analysis" framework**: Applies Buffett's 12-step criteria systematically — unique structured value investing approach
- **Margin of safety + Tykr Score**: Two proprietary scores give a quick stock "snapshot" — similar to our planned snowflake health
- **Education integrated into analysis**: Every analysis teaches something — "This company has a P/E of 15, which means..." — Stock Explorer's core philosophy but automated

**Comparison with Stock Explorer**:

| Feature | Tykr | Stock Explorer |
|---|---|---|
| Margin of Safety | ✅ Proprietary calculator | ❌ Not built |
| Value Investing Framework | ✅ Buffett's 12 criteria | ❌ Not built |
| Education + Analysis | ✅ Integrated | ✅ Core value |
| Health Score | ✅ Tykr Score (0-10) | ✅ Snowflake (planned) |
| Plain-language | ✅ Conversational | ✅ Core feature |
| Stock Stories | ✅ 30-second reads | ✅ Business card page |
| Portfolio Tracking | ✅ With MoS updates | ❌ Not built |
| TW Market | ❌ Global mix | ✅ Deep |
| PPT-style | ❌ Traditional web | ✅ Unique design |
| Active learning | ⚠️ Library only | ✅ Planned interactive tools |

**Feature Gaps Identified**:
13. **Margin of Safety calculator** — Tykr's margin of safety calculation is a unique "value lens" — showing how much "discount" a stock is trading at. Stock Explorer has C45 (Valuation Band Chart) which shows historical P/E range, but no intrinsic value calculation. A "valuation estimate" feature would complement C45.
14. **Structured investment framework** — Tykr applies Buffett's 12 criteria systematically. Stock Explorer has no structured analytical framework — analysis is descriptive, not criteria-based. A "Here's what makes this company strong/weak" checklist (similar to C62 Pre-Investment Checklist but company-specific) would add analytical rigor.
15. **Investment philosophy branding** — Tykr brands itself as "the Warren Buffett way." Stock Explorer's "historian" positioning is clever but abstract. Tying analysis to a specific investment philosophy (value, growth, dividend) could make the positioning more concrete for beginners.

---

### 6. Wall Street Zen (wallstreetzen.com)

**Positioning**: "Zen-like simplicity in stock analysis" — minimalist stock research that gets to the point
**Target Users**: US retail investors who want quick, no-fluff stock overviews; information overload sufferers

**Key Features**:
- **One-Page Stock Overview**: Every stock fits on ONE scrollable page — key metrics, valuation, dividend, growth, all visible without clicking
- **"Zen Score"**: Single composite score (0-100) with three sub-scores: Fundamentals, Valuation, Growth
- **"What to Know" Summary**: 3-sentence plain-language summary — "Company X does Y. It's profitable because Z. Watch out for risk A."
- **Minimalist UI**: Absolutely minimal design — no sidebar, no tabs, no clutter — just the essentials
- **"Is it overvalued?"**: Simple over/under-valued indicator with one-sentence explanation — "Overvalued by 20% because P/E is 30 while fair value is 25"
- **Plain-Language Financials**: Financial statement highlights in conversational language — "Made $10B last year, kept $2B as profit, paid $1B in dividends"

**UX/Design Approach**:
- **Extreme simplicity**: The primary design principle is "less is more"
- **One-page everything**: No drilling down — everything visible on one page
- **Score-driven**: The Zen Score is the focal point
- **Gentle, calm tone**: Writing style is meditative and reassuring — "Here's what you need to know. No rush."

**Unique Capabilities**:
- **True one-page design**: Unlike competitors who claim "simple" but have 10 tabs, Wall Street Zen genuinely fits everything on one scrollable page
- **"Zen-like" calm**: The tone is deliberately calming — counteracts the anxiety of financial data
- **Score + summary only**: No "deep dives" — only the essentials with an explanation

**Comparison with Stock Explorer**:

| Feature | Wall Street Zen | Stock Explorer |
|---|---|---|
| One-page overview | ✅ True single page | ⚠️ Multiple pages/sections |
| Composite score | ✅ Zen Score (0-100) | ✅ Snowflake (planned) |
| 3-sentence summary | ✅ "What to Know" | ❌ Not built |
| Minimalist design | ✅ Extreme minimalism | ✅ PPT-style (but detailed) |
| Plain-language | ✅ Calm, gentle tone | ✅ Core feature |
| TW Market | ❌ US only | ✅ Deep |
| Depth of analysis | ⚠️ Summary only | ✅ Detailed analysis |
| Education | ⚠️ Minimal | ✅ Core positioning |

**Feature Gaps Identified**:
16. **One-page overview mode** — Wall Street Zen's one-page design is the ultimate "progressive depth" implementation — everything visible at once, no drilling down. Stock Explorer's multi-section design requires scrolling through many sections. A "single-page summary" mode (or the planned C72 TL;DR First) would address this.
17. **Calm, gentle tone** — Wall Street Zen's "Zen-like" calm writing style specifically counteracts financial anxiety. Stock Explorer's tone is educational and warm but not explicitly calming. Adopting a more deliberately calming tone for anxious beginners could improve the UX.
18. **"Is it overvalued?" simple indicator** — Wall Street Zen has a single over/under-valued flag with one-sentence explanation. Stock Explorer's C45 (Valuation Band Chart) is more complex. A simple "overvalued/fair/undervalued" flag on the summary card would complement the detailed chart.

---

### 7. 口袋證券 (Pocket Securities)

**Positioning**: "Young people's first securities account" — TW neo-broker targeting Gen Z
**Target Users**: TW investors aged 18-30 opening their first brokerage account; mobile-native beginners

**Key Features**:
- **"口袋學堂" (Pocket Academy)**: Bite-sized investing lessons specifically for beginners — "What is a stock?" in 2 minutes, "How to read K-line" in 3 minutes
- **"AI Stock Picker"**: AI recommends stocks based on user's risk profile and interests — "You like gaming → here are gaming stocks to learn about" (educational framing, not investment advice)
- **Fractional Shares**: Buy NT$100 of any TW stock — lowers barrier to entry
- **Social Features**: "Pocket Wall" where users share what they're learning — social education, not signal-following
- **"Stock Card"**: Visual one-card stock overview — similar to our concept but simpler, mobile-optimized
- **"First Trade" Guided Flow**: Step-by-step onboarding for the first trade — education before transaction

**UX/Design Approach**:
- **Mobile-first native app**: Smartphone-first UX — swipe, tap, done
- **Gen Z aesthetic**: Bright colors, emoji, casual language
- **Gamified learning**: Points for completing lessons, badges for milestones
- **Community-as-education**: Social features focused on learning, not showing off

**Comparison with Stock Explorer**:
口袋證券 is the closest TW competitor to Stock Explorer's target audience (young beginners). Both platforms prioritize education before trading. However, 口袋證券 is a broker (must sell trades), while Stock Explorer is pure education. The "Stock Card" concept is directly analogous to our business card page.

**Feature Gaps Identified**:
19. **Mobile-first UX** — 口袋證券's native app is significantly more accessible than Stock Explorer's Streamlit web app. This is an architecture limitation, not a feature gap, but it's the #1 competitive disadvantage.
20. **Gamified learning** — 口袋證券 has points, badges, and milestones. Stock Explorer's planned C60 (Concept Mastery Badges) and C71 (Learning Streak) share this concept but aren't built yet.
21. **"First Trade" guided onboarding** — 口袋證券's onboarding flow teaches before transacting. Stock Explorer's planned C58 (Beginner Onboarding) should follow the same pattern: teach before exploring.

---

### 8. Goodinvest / 豐存股

**Positioning**: "ETF investing made simple" — 永豐金's education-first ETF platform for beginner investors
**Target Users**: TW beginners who want to start with ETFs before individual stocks; 永豐金 brokerage customers

**Key Features**:
- **"ETF Academy"**: Structured courses on ETF investing — "What is an ETF?" → "How to choose ETFs" → "Portfolio construction with ETFs"
- **"ETF Compare"**: Side-by-side ETF comparison with plain-language summaries — "00878 has higher yield but 0056 has longer track record"
- **"ETF Screener"**: Filter ETFs by yield, expense ratio, track record, issuer — plain-language results
- **"Investment Simulator"**: ETF-focused simulator — "If you invested NT$3,000/month in 0050 for 10 years..."
- **"Expert Column"**: Weekly ETF analysis from 永豐金 research team — plain-language market commentary
- **"Beginner Checklist"**: Pre-first-trade checklist — "Do you have an emergency fund? Do you understand the risks?"

**Comparison with Stock Explorer**:
ETF-focused vs. Stock Explorer's individual stock focus. However, the education philosophy is identical: teach beginners before they invest. The "ETF Academy" is a more structured version of our planned C47 (Financial Education Academy).

**Feature Gaps Identified**:
22. **ETF-focused education** — Goodinvest's ETF Academy is specifically designed for ETF beginners. Stock Explorer focuses on individual stocks. An "ETF Basics" education module could complement the stock analysis for beginners who want to start with ETFs.
23. **Investment simulator** — Goodinvest's ETF simulator is similar to Groww's Vola game. Stock Explorer has no simulation capability (planned C69 Paper Trading Simulator).

---

## Updated Competitor Overview Table (Round 15 Additions)

| Dimension | 口袋股利 | StockAnalysis.com | TipRanks | Tykr | Wall Street Zen | 口袋證券 | Goodinvest | **Stock Explorer** |
|---|---|---|---|---|---|---|---|---|
| **Region** | TW | US/Global | US/Global | US/Global | US | TW | TW | **TW** |
| **Focus** | Dividends | Company Analysis | Expert Consensus | Value Investing | Minimalism | Gen Z Broker | ETFs | **Historian** |
| **Composite Score** | ❌ | ❌ | ✅ Smart Score | ✅ Tykr Score | ✅ Zen Score | ❌ | ❌ | ✅ Snowflake |
| **Insider Data** | ❌ | ❌ | ✅ Tracked | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Sentiment** | ❌ | ❌ | ✅ Blogger/News | ❌ | ❌ | ❌ | ❌ | ⚠️ M5 events |
| **Education** | ✅ Articles | ⚠️ Articles | ❌ | ✅ Library | ❌ | ✅ Academy | ✅ Academy | **✅ Core** |
| **Calculator** | ✅ Dividend | ❌ | ❌ | ✅ MoS calc | ❌ | ❌ | ✅ Simulator | ❌ |
| **Dividend** | ✅ Calendar | ✅ Calendar | ✅ Dividend Score | ❌ | ❌ | ❌ | ❌ | ✅ Countdown |
| **Mobile** | ⚠️ Web | ✅ Responsive | ✅ Responsive | ✅ Responsive | ✅ Responsive | ✅ Native | ✅ Native | ⚠️ Streamlit |

---

## New Feature Ideas from Round 15

### [ISSUE-C75] "Dividend Calendar" — Market-Wide Upcoming Ex-Dividend View

**Source Competitor**: 口袋股利 (monthly dividend calendar), StockAnalysis.com (Upcoming Dividends), TipRanks (dividend tracking)
**Priority**: P2
**Effort**: 8-12h
**Alignment**: Core value #4 "Point-to-point knowledge construction" + Beginner-friendly + Benchmark-oriented analysis

**Description**: A calendar page showing all upcoming ex-dividend dates for TW stocks in a monthly view. Users can see at a glance which stocks go ex-dividend this week/month. Each entry shows stock name, dividend amount, yield, and days until ex-dividend. This complements C1 (single-stock countdown) with a market-wide view.

**User Value**: Dividend investors need to plan around ex-dividend dates. A calendar view helps beginners discover dividend stocks they didn't know about and plan their investment timing. "15 stocks go ex-dividend next week — here they are."

**Implementation Notes**:
- Add a "📅 股利日曆" page accessible from the navbar
- Monthly calendar view with stock entries on ex-dividend dates
- Color-coded by dividend yield (green = high yield, yellow = moderate, red = low)
- Click on a date → see list of stocks going ex-dividend that day
- Data sourced from FinMind dividend calendar API
- Show countdown badge on each entry (similar to C1)

**Competitive Gap**: 🔴 No TW competitor has a comprehensive dividend calendar with countdown. 口袋股利 proves demand. This would be a unique discovery mechanism for dividend-focused beginners.

---

### [ISSUE-C76] "Insider Activity Tracker" — Plain-Language Insider Trading Monitor

**Source Competitor**: TipRanks (insider activity tracking), Dhan (Super Investors), Spiking (Expert Tracking)
**Priority**: P2
**Effort**: 12-16h
**Alignment**: Core value #1 "Story first, data second" + Historian positioning + Benchmark-oriented analysis

**Description**: A feature tracking insider buying/selling for TW stocks with plain-language explanations. "The Chairman bought 100,000 shares at NT$500 — this is significant because insiders usually buy when they believe the stock is undervalued." This is not investment advice — it's the "historian" explaining what insiders did and what it might mean.

**User Value**: Beginners hear "insider buying" but don't understand the significance. An insider activity tracker with plain-language explanations transforms raw filing data into educational content. "Here's what insiders did, and here's why it might matter."

**Implementation Notes**:
- Use TWSE public insider trading filings (already available from FinMind)
- Show top 10 insider transactions for each stock with plain-language significance rating
- Significance = transaction size relative to average trade + position of buyer/seller (CEO vs. board member)
- Color coding: 🟢 Large buy, 🟡 Small buy/sell, 🔴 Large sell
- Add "What is insider trading?" educational blurb
- Frame as educational: "This is what insiders did — draw your own conclusions"

**Competitive Gap**: 🔴 No TW competitor offers plain-language insider activity explanations. TipRanks proves demand internationally. This is a unique "historian" differentiator — explaining what insiders did and why it might matter.

---

### [ISSUE-C77] "Valuation Verdict" — Simple Over/Fair/Under-Valued Flag

**Source Competitor**: Wall Street Zen ("Is it overvalued?" flag), Tykr (Margin of Safety %), Simply Wall St (Snowflake valuation dimension)
**Priority**: P2
**Effort**: 6-10h
**Alignment**: Core value #1 "Story first, data second" + "Ten-second test" + Benchmark-oriented analysis

**Description**: A simple, prominent "valuation flag" on each company's summary — 🟢 "Undervalued by ~15%", 🟡 "Fairly valued", or 🔴 "Overvalued by ~20%" — with a one-sentence explanation. This complements the detailed C45 (Valuation Band Chart) with a simple verdict that beginners can understand instantly.

**User Value**: Beginners look at a stock and want to know "Is this cheap or expensive?" — the Valuation Band Chart shows the range, but beginners still have to interpret it. A simple flag gives the answer instantly. "Overvalued by ~20% because the current P/E of 30 is above the 5-year average of 25."

**Implementation Notes**:
- Calculate valuation verdict from C45 data (current P/E vs 5-year average P/E)
- Simple algorithm: < -20% → 🟢 Undervalued, -20% to +20% → 🟡 Fair, > +20% → 🔴 Overvalued
- Display as a prominent badge/card at the top of the business card page
- One-sentence explanation generated from template: "[Undervalued/Overvalued] by ~X% because the current P/E of Y is [above/below] the 5-year average of Z"
- Conservative framing: "This is one way to look at valuation — not a recommendation"

**Competitive Gap**: 🟡 Wall Street Zen has this concept but only for US stocks. No TW competitor offers a simple valuation verdict with plain-language explanation. This directly addresses the "ten-second test."

---

### [ISSUE-C78] "Analyst Consensus" — Aggregated Expert Opinions in Plain Language

**Source Competitor**: TipRanks (analyst consensus), StockAnalysis.com (Forecast tab), Simply Wall St (Future Growth Estimates)
**Priority**: P2
**Effort**: 10-14h
**Alignment**: Core value #1 "Story first, data second" + Benchmark-oriented analysis + Historian positioning

**Description**: A feature aggregating analyst opinions about TW companies into a plain-language consensus. "Most analysts are positive about TSMC because of AI chip demand. However, some are concerned about capex spending." This is NOT a recommendation — it's the "historian" reporting what experts think.

**User Value**: Beginners want to know "What do experts think?" but analyst reports are in English and use jargon. An analyst consensus feature translates expert opinions into accessible Mandarin with plain-language summaries.

**Implementation Notes**:
- Use TW brokerage research reports (published publicly by TWSE)
- Aggregate into: optimistic / neutral / bearish sentiment
- Show top 3 reasons for each sentiment (extracted from report summaries)
- Plain-language framing: "Here's what analysts are saying about this stock"
- Include disclaimer: "This is analyst opinion, not fact. Make your own decisions."
- Start with top 20 TW stocks by analyst coverage

**Competitive Gap**: 🔴 No TW competitor aggregates analyst consensus into plain-language summaries. TipRanks does this for US stocks. This would be a unique "historian" differentiator.

---

### [ISSUE-C79] "Compound Return Calculator" — Interactive Investment Estimator

**Source Competitor**: 口袋股利 (dividend calculator), Goodinvest (simulator), Groww (Vola game with projections)
**Priority**: P2
**Effort**: 8-12h
**Alignment**: Core value #4 "Point-to-point knowledge construction" + Active learning + Beginner-friendly

**Description**: An interactive calculator where users input an investment amount, time horizon, and expected return — and see the projected outcome. "Invest NT$5,000/month in TSMC for 20 years at 8% annual return → NT$2,945,000." Not a prediction — an educational tool for understanding compound growth.

**User Value**: Beginners struggle to understand compound returns. Reading "8% annual return" is abstract. Seeing "NT$5,000/month becomes NT$3M in 20 years" makes it real. This is a transformative "aha moment" for financial literacy.

**Implementation Notes**:
- Add a "🧮 複利計算器" page accessible from the navbar
- Inputs: monthly investment amount, time horizon (years), expected annual return
- Outputs: total invested, final value, growth multiple
- Show a chart of growth over time (compound curve)
- Include a "What is compound interest?" explainer
- Optional: let users select a stock and use its historical return as the default
- Disclaimer: "This is a projection based on your assumptions, not a guarantee"

**Competitive Gap**: 🟡 口袋股利 has a dividend calculator but not a general compound return calculator. Stock Explorer having this tool would be a unique educational feature.

---

### [ISSUE-C80] "News Sentiment Indicator" — Event Dashboard Sentiment Analysis

**Source Competitor**: TipRanks (news sentiment), Spiking (Social Sentiment Dashboard), 元大證券 (Market Pulse)
**Priority**: P2
**Effort**: 10-14h
**Alignment**: Core value #3 "Adaptive and self-evolving" + Benchmark-oriented analysis + Story first

**Description**: Add sentiment indicators to M5's event dashboard — each event gets a sentiment arrow (📈 Positive / ⚪ Neutral / 📉 Negative) with a one-word reason. "TSMC reports Q3 earnings" → 📈 Positive (earnings beat). "CEO sells shares" → 📉 Negative (insider selling). This adds an emotional/sentiment layer to the factual event data.

**User Value**: Beginners see events in the dashboard but don't know "Is this good or bad?" Sentiment indicators provide immediate context without requiring analysis. "This event is positive because..." teaches beginners to interpret financial events.

**Implementation Notes**:
- Use keyword matching on event titles to determine sentiment
- Maintain a sentiment dictionary: "earnings beat" → 📈, "revenue miss" → 📉, "dividend announced" → 📈, etc.
- Display as a colored arrow next to each event in the dashboard
- Add a "Why this sentiment?" tooltip with one-sentence explanation
- Keep it simple: only 3 levels (positive/neutral/negative)
- This is educational, not predictive — "This event is generally seen as positive/negative"

**Competitive Gap**: 🟡 TipRanks has news sentiment but only for US stocks. No TW competitor adds sentiment to event data. This would enrich M5's event dashboard with an educational layer.

---

## Key Insights from Round 15

### 1. **TW Dividend Education is a Distinct Niche**
口袋股利 and 股息小人 represent a TW-specific niche: dividend-focused education. Stock Explorer covers dividends (C1 countdown) but not as a primary focus. The dividend calendar (C75) and compound return calculator (C79) would serve this audience without compromising the "historian" positioning.

### 2. **"Consensus" is a Powerful Education Format**
TipRanks (analyst consensus), Dhan (Super Investors), and Spiking (social sentiment) all use "what experts think" as educational content. Stock Explorer's purely company-focused analysis misses this social dimension. C76 (Insider Activity) and C78 (Analyst Consensus) would add the "expert perspective" layer.

### 3. **Simplicity is a Feature, Not a Limitation**
Wall Street Zen proves that extreme simplicity (one page, one score, 3 sentences) is a viable product philosophy. Stock Explorer's detailed analysis is valuable, but the "TL;DR First" concept (planned C72) and C77 (Valuation Verdict) would make the depth more accessible.

### 4. **Calculators Drive "Aha Moments"**
口袋股利's dividend calculator, Goodinvest's simulator, and Tykr's Margin of Safety calculator all create transformative learning moments. Stock Explorer is purely informational — users read but don't calculate. C79 (Compound Return Calculator) would add an interactive learning dimension.

### 5. **Sentiment is the Missing Layer in Event Data**
Stock Explorer's M5 engine detects events but doesn't interpret them. TipRanks, Spiking, and 元大證券 all add sentiment to events. C80 (News Sentiment Indicator) would transform M5 from a factual detector into an educational interpreter.

### 6. **TW Neo-Brokers are Catching Up on Education**
口袋證券 (Pocket Securities) and Goodinvest (豐存股) show that TW brokers are investing heavily in education features. Stock Explorer's advantage is depth and "historian" positioning, but the gap is narrowing. Mobile-first UX is the biggest competitive disadvantage.

### 7. **Value Investing Frameworks are Underrepresented**
Tykr's "Buffett Analysis" framework shows that structured investment criteria can be educational. Stock Explorer's analysis is descriptive ("here's what the company does") but not criteria-based ("here's how this company scores on key dimensions"). C77 (Valuation Verdict) and the existing C62 (Pre-Investment Checklist) partially address this.

### 8. **The "Calm Tone" Differentiator**
Wall Street Zen's deliberately calm, anxiety-reducing tone is unique among financial platforms. Stock Explorer's "historian" positioning could adopt a similar calming voice — "Here's what happened, explained calmly" — to differentiate from anxiety-inducing financial news.

---

## Feature Gap Summary (Round 15)

| ID | Title | Priority | Effort | Source Competitor | Alignment |
|---|---|---|---|---|---|
| C75 | "Dividend Calendar" — Market-Wide Upcoming Ex-Dividend View | P2 | 8-12h | 口袋股利, StockAnalysis.com | Point-to-point + Beginner-friendly |
| C76 | "Insider Activity Tracker" — Plain-Language Insider Trading Monitor | P2 | 12-16h | TipRanks, Dhan, Spiking | Story first + Historian |
| C77 | "Valuation Verdict" — Simple Over/Fair/Under-Valued Flag | P2 | 6-10h | Wall Street Zen, Tykr, Simply Wall St | Story first + Ten-second test |
| C78 | "Analyst Consensus" — Aggregated Expert Opinions in Plain Language | P2 | 10-14h | TipRanks, StockAnalysis.com | Benchmark + Historian |
| C79 | "Compound Return Calculator" — Interactive Investment Estimator | P2 | 8-12h | 口袋股利, Goodinvest, Groww | Point-to-point + Active learning |
| C80 | "News Sentiment Indicator" — Event Dashboard Sentiment Analysis | P2 | 10-14h | TipRanks, Spiking, 元大證券 | Adaptive + Story first |

---

## Recommendations

### Immediate (Next Sprint)
1. **C77 Valuation Verdict** — Lowest effort (6-10h), highest UX impact. Wall Street Zen and Tykr prove demand. Directly addresses the "ten-second test" — beginners get an instant answer to "is this cheap or expensive?"
2. **C79 Compound Return Calculator** — Low effort (8-12h), creates transformative "aha moments." 口袋股利 and Goodinvest prove demand. Adds interactive learning to Stock Explorer's informational approach.

### Short-Term (Sprint 2-3)
3. **C75 Dividend Calendar** — Medium effort (8-12h), unique TW market feature. 口袋股利 proves demand. Complements C1 (single-stock countdown) with market-wide view.
4. **C80 News Sentiment Indicator** — Medium effort (10-14h), enriches M5 event dashboard. TipRanks and Spiking prove demand. Transforms factual events into educational interpretations.
5. **C78 Analyst Consensus** — Medium effort (10-14h), unique "historian" differentiator. TipRanks proves demand. No TW competitor offers plain-language analyst consensus.

### Medium-Term (Post-Sprint 3)
6. **C76 Insider Activity Tracker** — Medium effort (12-16h), unique "historian" differentiator. TipRanks and Dhan prove demand. Leverages TWSE public data that no competitor uses for education.

---

*This is the fifteenth competitor research round. Six new feature suggestions identified (C75-C80). The most impactful new gap is C77 (Valuation Verdict) — it directly addresses the "ten-second test" design principle with the lowest effort (6-10h). The most strategically important gap is C80 (News Sentiment Indicator) — it enriches M5's event dashboard with an educational layer, transforming Stock Explorer from a factual detector into an educational interpreter. The most unique gap is C76 (Insider Activity Tracker) — no TW competitor offers plain-language insider trading explanations, and TWSE public data makes this feasible.*

---

## Cumulative Competitor Research Summary

| Round | New Competitors | New Features | Total Competitors | Total Features |
|---|---|---|---|---|
| Round 7 | 5 (StatementDog, GoodInfo, CMoney, WantGoo, Simply Wall St) | 7 (C33-C35 + earlier) | 5 | 7 |
| Round 8 | 8 (Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, Motley Fool, NerdWallet) | 6 (C36-C41) | 13 | 13 |
| Round 9 | 9 (財報狗, JZ Invest, 鉅亨網, TEJ, Yahoo奇摩股市, Simply Wall St, Stockopedia, Investopedia, Morningstar) | 6 (C42-C47) | 22 | 19 |
| Round 10 | 6 (TipRanks, Finimize, Zerodha, StockEdge, Tickeron, Khan Academy) | 6 (C48-C53) | 28 | 25 |
| Round 11 | 3 (Stake, Moomoo, + reviews) | 6 (C54-C62 incl. reorg) | 31 | 31 |
| Round 12 | 9 (eToro, Webull, Robinhood, 富邦e富, 元大證券, 永豐金證券, 玉山證券, Magnify.money, Tastytrade) | 8 (C55-C62) | 40 | 39 |
| Round 13 | 8 (Kabu.com, Minkabu, Smart FOLIO, Toss Securities, Kiwoom, Syfe, Atom Finance, Upside AI) | 6 (C63-C68) | 48 | 45 |
| Round 14 | 8 (Groww, Dhan, Sensibull, Spiking, Cake Finance, SoFi, Finshots, Trading 212) | 6 (C69-C74) | 56 | 51 |
| **Round 15** | **8 (口袋股利, 股息小人, StockAnalysis.com, TipRanks, Tykr, Wall Street Zen, 口袋證券, Goodinvest)** | **6 (C75-C80)** | **64** | **57** |

**Total unique competitors analyzed across all rounds: 64**
**Total unique feature suggestions identified: 57 (C01-C80, with some declassified/merged)**
