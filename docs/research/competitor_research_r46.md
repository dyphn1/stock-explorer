# Stock Explorer Competitor Research Report — Round 46

> **Date**: 2026-06-15
> **Author**: QA Engineer (Round 46)
> **Purpose**: Deep-dive research on 8 key competitors (Robinhood, Finimize, Public.com, Spiking, StockStory, Magnify.money, Tickertape, Simply Wall St) to identify feature gaps, design patterns, and new opportunities not covered in Rounds 1-45.

---

## 1. Executive Summary

### Key Findings

1. **"Explainability" is the new baseline, not a differentiator.** All 8 competitors researched in this round provide some form of plain-language explanation — from Robinhood's simple metric tooltips to Spiking's AI-powered "Why did this move?" narratives. Stock Explorer's analogy engine remains ahead in depth, but the gap is narrowing. The competitive moat must shift from "we explain" to "we explain *better* and *in context*."

2. **Bite-sized daily education is the #1 retention pattern.** Finimize's entire product is built around a 5-minute daily lesson. Robinhood's recurring buys + education nuggets, Public.com's story cards, and StockStory's visual summaries all follow the same pattern: small, consumable, daily. Stock Explorer's Financial Education Academy (5 structured lessons) is a strong foundation but lacks a *daily* cadence. C186 (Daily 5-Min Finance Lesson) and C196 (Daily Market Story) are critical — this round confirms they should be P0, not P1.

3. **Social/community features are table stakes for engagement but dangerous for positioning.** Public.com's social investing, Tickertape's community screens, and Robinhood's social proof (e.g., "1.2M people own this") all drive engagement. However, Stock Explorer's "Historian, not a stock picker" positioning means social features must be *education-focused*, not *trade-focused*. The opportunity is "community learning" (sharing insights, not picks).

4. **Visual-first analysis is winning over data-dense tables.** Simply Wall St's snowflake, StockStory's visual stories, Magnify.money's calculators, and Tickertape's visual screening all prove that beginners prefer visuals over tables. Stock Explorer's PPT-style presentation is well-positioned, but the implementation needs more *interactive* visuals (not just static charts). The health score snowflake (C43) is already implemented — the next step is making it *trendable* (C197) and *comparable* (C191).

5. **AI-powered "Why?" explanations are becoming expected, not novel.** Spiking's entire value proposition is "Why did this stock move?" — AI-generated explanations for price movements. Stock Explorer's C188 (planned) addresses this, but the bar is rising: competitors are delivering these explanations *inline*, *in real-time*, and *with confidence indicators*. C188 must go beyond "what happened" to "why it matters for this company's story."

---

## 2. Competitor Profiles

### 2.1 Robinhood

**Positioning**: "Investing for everyone" — the gateway drug for beginner investors
**Target Users**: Young (18-35), first-time investors in the US market
**Revenue Model**: Payment for order flow, margin interest, Robinhood Gold ($5/mo)

**Key Features Stock Explorer Doesn't Have**:
- **Recurring Investments**: Auto-invest daily/weekly/monthly in any stock/ETF — this is a *behavioral* feature that builds investing habits. Stock Explorer is purely analytical; it has no action layer.
- **Fractional Shares Education**: Robinhood teaches fractional investing as a concept — "You can buy 0.01 shares of Amazon for $2." This is educational scaffolding for beginners who think they need $3,000+ to invest.
- **Push Notifications with Context**: Price alerts, earnings reminders, and news alerts — all with plain-language context. Not just "AAPL moved 5%" but "AAPL moved 5% after reporting earnings that beat expectations."
- **Clean Card-Based UI**: Every stock page is a single scrollable card with clear sections: Overview, News, Earnings, Financials. No tabs, no navigation — just scroll.
- **Options/Futures Education**: Even for advanced products, Robinhood provides bite-sized education before allowing access.

**UX/Design Patterns Worth Adopting**:
- **One-page stock view**: Robinhood's single-page design eliminates navigation complexity. Stock Explorer's multi-page approach (business card → health → financial → peers → structure) is powerful but can overwhelm. Consider a "Quick View" mode that shows everything on one scrollable page.
- **Micro-animations**: Subtle animations for price changes (green/red flash), loading states, and transitions. Stock Explorer's Streamlit-based UI is static — adding subtle motion would improve perceived responsiveness.
- **"X people own this" social proof**: Not about FOMO — about reducing the intimidation factor. "1.2M people own TSMC" makes beginners feel less alone.

**Feature Gaps → New Issues**:
- No recurring investment education (not a feature gap per se, but an educational gap — beginners don't know this exists)
- No push notification system (C02, long-standing gap)
- No fractional share concept education (could be part of Financial Education Academy)

---

### 2.2 Finimize

**Positioning**: "Finance in 5 minutes a day" — daily financial education for busy people
**Target Users**: Professionals (25-45) who want financial literacy without the time investment
**Revenue Model**: Freemium — free daily email, premium ($5/mo) for deeper analysis, community, and tools

**Key Features Stock Explorer Doesn't Have**:
- **Daily Email/Notification Cadence**: The core product is a daily 5-minute finance lesson delivered via email/app. This creates a *habit loop* — users open Finimize every morning. Stock Explorer has no daily touchpoint.
- **"Finimize Bytes"**: Ultra-short (30-second) explainers on single concepts — "What is inflation?" "Why did oil prices drop?" These are standalone educational units that don't require context.
- **Premium Community**: Paid members get access to a community of financially-literate professionals. The community is *education-focused*, not *trade-focused*.
- **"Explain Like I'm 5" Toggle**: Every article has a complexity slider — from "ELI5" to "Expert." This is similar to Stock Explorer's Beginner/Expert mode (C40, already implemented) but applied to *content*, not just UI.
- **Weekly Roundup + Monthly Deep Dive**: Structured content cadence — daily bytes, weekly summary, monthly deep dive.

**UX/Design Patterns Worth Adopting**:
- **Content cadence as a feature**: The daily/weekly/monthly rhythm creates anticipation and habit. Stock Explorer should adopt a similar cadence: daily market story (C196), weekly sector spotlight, monthly deep dive.
- **Complexity slider on content**: Not just a UI toggle, but a content-level toggle. The same concept explained at 3 different depths. This is different from C40 (UI toggle) — it's about *content adaptation*.
- **"Read time" indicator**: Every piece shows "3 min read" — sets expectations and reduces commitment anxiety.

**Feature Gaps → New Issues**:
- No daily content cadence (C186, C196 — planned but not yet built)
- No complexity-adapted content (different from UI toggle — the *same* concept at different depths)
- No email/notification touchpoint (C02 — long-standing gap)

---

### 2.3 Public.com

**Positioning**: "Social investing for everyone" — invest alongside friends and experts
**Target Users**: Socially-connected investors (20-40) who want community + education
**Revenue Model**: Tipping (users tip creators), payment for order flow, premium features

**Key Features Stock Explorer Doesn't Have**:
- **Story Cards**: Each stock has a visual "story card" — a single image with the company's key narrative, designed for sharing. This is similar to Stock Explorer's Company Story Card (C48, implemented) but optimized for *social sharing* (square format, bold text, branded).
- **Social Timeline**: A feed of what other investors are buying, holding, and discussing — with *context*. Not just "UserX bought AAPL" but "UserX bought AAPL because they believe in the iPhone cycle."
- **Creator Profiles**: Expert investors share their thesis and track record. Followers can see their portfolio allocation and reasoning.
- **"Why I Own This" Narratives**: Every holding has a written narrative — "I own TSMC because they manufacture 90% of the world's advanced chips." This is *exactly* Stock Explorer's "historian" positioning but applied to *portfolio holdings*.
- **Group Investing**: Pool money with friends to invest together — with shared research and discussion.

**UX/Design Patterns Worth Adopting**:
- **Story cards optimized for sharing**: Stock Explorer's C48 (Company Story Card) exists but isn't optimized for social sharing. Public.com's cards are designed to be screenshot-worthy — bold visuals, key stat, one-line narrative.
- **"Why I Own This" narrative pattern**: This is a *user-generated* version of Stock Explorer's analogy engine. Allowing users to write their own "why this company matters" narratives would be a unique social feature.
- **Social proof without FOMO**: Public.com shows "trending" stocks without price pressure — it's about *discovery*, not *urgency*.

**Feature Gaps → New Issues**:
- No social sharing-optimized story cards (C53 exists but isn't screenshot-optimized)
- No user-generated narratives ("Why I'm interested in this company")
- No community discussion layer (C64 — planned)

---

### 2.4 Spiking

**Positioning**: "AI-powered stock movement explanations" — why did this stock move?
**Target Users**: Active investors who want to understand price movements in real-time
**Revenue Model**: Freemium — free basic alerts, premium for AI explanations and early signals

**Key Features Stock Explorer Doesn't Have**:
- **Real-Time "Why Did This Move?" Engine**: Spiking's core feature — when a stock moves significantly, the AI generates a plain-language explanation: "TSMC moved +5% because Apple announced new iPhone orders, and TSMC is Apple's primary chip supplier." This is *exactly* what C188 aims to do, but Spiking does it in *real-time*.
- **Insider Trading Tracker**: Spiking tracks insider buying/selling and explains the significance: "The CEO bought $2M in shares — historically, this has preceded 15% gains over 90 days."
- **Supply Chain Mapping**: Spiking maps customer-supplier relationships: "TSMC's top customers: Apple (25%), NVIDIA (15%), AMD (10%)." When Apple moves, Spiking shows which suppliers are affected.
- **Unusual Activity Detection**: AI detects unusual options flow, volume spikes, and institutional activity — then explains what it means.
- **Multi-Market Coverage**: Spiking covers SG, MY, HK, US, AU, IN, TH, ID, VN, JP, KR markets — with the same AI explanation engine.

**UX/Design Patterns Worth Adopting**:
- **Inline "Why?" explanations**: Not a separate section — explanations appear *inline* with the data. When you see a price spike, the explanation is right there.
- **Confidence indicators**: Spiking shows how confident the AI is in its explanation — "High confidence: This move is driven by earnings" vs. "Low confidence: Multiple factors may be contributing."
- **Supply chain visualization**: A simple diagram showing "If Apple moves, here are the affected suppliers." This is a natural extension of Stock Explorer's group structure mapping.

**Feature Gaps → New Issues**:
- No real-time "Why did this move?" engine (C188 — planned, but Spiking sets the bar high)
- No supply chain mapping (C96 — Sector Ecosystem Map, planned)
- No insider trading context layer (C108 — planned)
- No confidence indicators on AI explanations (C157 — planned)

---

### 2.5 StockStory

**Positioning**: "Visual stock stories for beginners" — every stock has a story, told visually
**Target Users**: Beginner investors who want to understand companies through narratives, not spreadsheets
**Revenue Model**: Freemium — free basic stories, premium for detailed analysis

**Key Features Stock Explorer Doesn't Have**:
- **Visual Story Format**: Each stock is presented as a visual story — like a children's book for stocks. "Once upon a time, there was a company that made chips..." This is *exactly* Stock Explorer's positioning but executed as a *scrollable visual narrative*.
- **"Story Arcs"**: StockStory identifies narrative arcs in a company's history — "The Rise," "The Crisis," "The Recovery." These are visual timelines with illustrations.
- **Plain-Language Summaries**: Every metric is explained in one sentence: "P/E ratio of 25 means you're paying $25 for every $1 of earnings — that's like paying $25 for a $1 bill."
- **Comparison Stories**: "How is Apple's story different from Microsoft's?" — side-by-side narrative comparison, not just metric comparison.
- **"What Could Happen Next?"**: Forward-looking narrative scenarios — "If Apple's iPhone sales drop, here's what might happen to TSMC."

**UX/Design Patterns Worth Ading**:
- **Story arc visualization**: A visual timeline with narrative labels — "The Rise (2020-2021)," "The Chip Shortage (2021-2022)," "The AI Boom (2023-present)." Stock Explorer's event timeline (C28) has the data but lacks narrative arcs.
- **One-sentence metric explanations**: Stock Explorer's analogy engine does this, but StockStory's are *shorter* and *more visual* — one sentence + one icon.
- **Forward-looking narratives**: "What could happen next?" is different from "What will happen?" — it's educational speculation, not investment advice. This aligns with Stock Explorer's "historian" positioning.

**Feature Gaps → New Issues**:
- No story arc visualization (C28 — Story Timeline exists but lacks narrative arc labels)
- No forward-looking narrative scenarios (C115 — Scenario Explorer, planned)
- No visual story format (C48 — Story Card exists but isn't a full visual narrative)

---

### 2.6 Magnify.money

**Positioning**: "Visual financial calculators" — understand money through interactive visuals
**Target Users**: Beginners who want to understand financial concepts through hands-on interaction
**Revenue Model**: Free (ad-supported) + premium for advanced calculators

**Key Features Stock Explorer Doesn't Have**:
- **Interactive Financial Calculators**: Compound interest calculator, dividend reinvestment calculator, inflation calculator — all with real-time visual feedback. Move a slider, see the chart update instantly.
- **Concept Comparison Tools**: Side-by-side comparison of financial concepts — "What's the difference between P/E and P/B?" with visual examples.
- **"What If" Scenarios**: "What if you invested $100/month in TSMC for 10 years?" — interactive scenario modeling with historical data.
- **Visual Explanations**: Every concept is explained with an interactive visual — not just text. "Compound interest" shows a growing tree metaphor.
- **Personal Finance Integration**: Connects stock analysis to personal finance — "Based on your savings rate, here's how long it would take to buy 10 shares of TSMC."

**UX/Design Patterns Worth Adopting**:
- **Interactive calculators with real-time feedback**: Stock Explorer has static charts. Magnify.money's calculators let users *play* with the numbers. C173 (Visual Financial Calculators) is planned but should be prioritized higher.
- **Concept comparison as a format**: Not just comparing stocks, but comparing *concepts*. "ROE vs ROA" — side-by-side with visual examples. C172 (Concept Comparison Tool) exists but isn't visual enough.
- **"What If" scenario modeling**: This is educational, not advisory. "What if you had invested $1000 in TSMC 5 years ago?" — teaches historical perspective without recommending future action.

**Feature Gaps → New Issues**:
- No interactive financial calculators (C173 — planned, should be elevated to P1)
- No concept comparison visuals (C172 — planned)
- No "What If" scenario modeling (C115 — Scenario Explorer, planned)

---

### 2.7 Tickertape

**Positioning**: "Stock screening + community insights" — find stocks through smart filters and community wisdom
**Target Users**: Indian retail investors who want data-driven screening with social validation
**Revenue Model**: Freemium — free basic screening, premium for advanced filters and community features

**Key Features Stock Explorer Doesn't Have**:
- **Visual Stock Screener**: Tickertape's screener is entirely visual — no forms, no dropdowns. Users see a grid of stocks and can filter by dragging sliders on charts. This is radically different from traditional screeners.
- **Community Screens**: Users can save and share their screening strategies. "My Dividend Growth Screen" — other users can see the criteria, results, and discussion.
- **"Tickertape Score"**: A proprietary composite score (0-100) for each stock based on valuation, financial health, and momentum. Similar to Stock Explorer's health score but more comprehensive.
- **Visual Analysis**: Every stock page has visual-first analysis — snowflake charts, bubble charts, heat maps. Minimal tables.
- **"Price Alert" with Context**: Not just "AAPL hit $200" but "AAPL hit $200, which is above its 5-year average P/E of 28."

**UX/Design Patterns Worth Adopting**:
- **Visual screener UI**: Tickertape's screener is a *visual experience*, not a form. Stock Explorer's planned screener (C42) should adopt this approach — visual filters, not dropdown menus.
- **Community screens as social learning**: Users share screening strategies with explanations. "I screen for companies with ROE > 15% because..." — this is educational, not advisory.
- **Composite score with breakdown**: Tickertape's score is broken into sub-scores with visual indicators. Stock Explorer's health score (C43) should show *trend* (C197) and *component breakdown*.

**Feature Gaps → New Issues**:
- No visual stock screener (C42 — planned, should be visual-first)
- No community screen sharing (C177 — planned)
- No composite score trend (C197 — planned)

---

### 2.8 Simply Wall St

**Positioning**: "Make complex investing simple" — visual-first stock analysis through infographics
**Target Users**: Global retail investors who want to understand stocks through visuals, not spreadsheets
**Revenue Model**: Freemium — free basic analysis, premium for detailed reports and unlimited access

**Key Features Stock Explorer Doesn't Have**:
- **Snowflake Analysis (Proprietary)**: The iconic snowflake diagram showing 5 dimensions (value, future, past performance, financial health, dividends) with color-coded scores. Stock Explorer has a health score snowflake (C43, implemented) but Simply Wall St's is more *polished* and *animated*.
- **Infographic-Style Reports**: Each stock page reads like an infographic — one key visual per concept, minimal text, maximum visual impact. This is *very similar* to Stock Explorer's PPT-style approach.
- **Future Growth Visualization**: Analyst estimates presented as visual ranges with confidence intervals — "Analysts expect 15% growth, but the range is 5% to 25%."
- **"Bear vs Bull" Visual Debate**: Visual presentation of bull and bear arguments side-by-side — not as text, but as visual cards with icons and key stats.
- **Portfolio Snowflake**: Aggregate portfolio analysis showing diversification, risk concentration, and overall health — all in a single visual.

**UX/Design Patterns Worth Adopting**:
- **Animated snowflake**: Simply Wall St's snowflake *animates* when scores change — the segments grow/shrink. Stock Explorer's static snowflake could be enhanced with animation.
- **Infographic report format**: Simply Wall St's reports are designed to be *read in 60 seconds*. Each section is one visual + one sentence. Stock Explorer's PPT-style is close but could be more *concise*.
- **"Bear vs Bull" visual debate**: This is educational — showing both sides without recommending either. Perfect for Stock Explorer's "historian" positioning.
- **Future growth visualization**: Showing analyst estimates as a *range* (not a single number) teaches beginners that the future is uncertain.

**Feature Gaps → New Issues**:
- No animated snowflake (C43 — exists but static)
- No "Bear vs Bull" visual debate format
- No future growth range visualization
- No portfolio-level snowflake (C95 — Watchlist Health Dashboard, planned)

---

## 3. Feature Gap Analysis Table

| Feature | Robinhood | Finimize | Public.com | Spiking | StockStory | Magnify.money | Tickertape | Simply Wall St | Our Status |
|---------|-----------|----------|------------|---------|------------|---------------|------------|----------------|------------|
| **Daily content cadence** | ⚠️ News alerts | ✅ Core product | ⚠️ Social feed | ⚠️ Alerts | ❌ | ❌ | ❌ | ❌ | ❌ MISSING (C186/C196 planned) |
| **Push notifications** | ✅ Price + news | ✅ Email daily | ✅ Social alerts | ✅ Real-time | ❌ | ❌ | ✅ Price alerts | ❌ | ❌ MISSING (C02 planned) |
| **"Why did this move?" AI** | ⚠️ Basic news | ❌ | ⚠️ Social context | ✅ Core product | ⚠️ Narrative | ❌ | ⚠️ Alerts | ❌ | ⚠️ C188 planned |
| **Visual story format** | ⚠️ Card UI | ❌ | ✅ Story cards | ❌ | ✅ Core product | ❌ | ❌ | ✅ Infographic | ⚠️ C48 exists |
| **Interactive calculators** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Core product | ❌ | ❌ | ❌ MISSING (C173 planned) |
| **Visual stock screener** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Core product | ❌ | ❌ MISSING (C42 planned) |
| **Community/social** | ⚠️ Social proof | ✅ Premium | ✅ Core product | ❌ | ❌ | ❌ | ✅ Community screens | ❌ | ⚠️ C53/C64 planned |
| **Snowflake/health visual** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ Score | ✅ Core product | ✅ C43 implemented |
| **Beginner/Expert toggle** | ⚠️ Gold tier | ✅ Complexity slider | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ C40 implemented |
| **Supply chain mapping** | ❌ | ❌ | ❌ | ✅ Core product | ❌ | ❌ | ❌ | ❌ | ⚠️ C96 planned |
| **Insider trading context** | ⚠️ Basic | ❌ | ❌ | ✅ Core product | ❌ | ❌ | ❌ | ❌ | ⚠️ C108 planned |
| **"Bear vs Bull" debate** | ❌ | ❌ | ⚠️ Social | ❌ | ❌ | ❌ | ❌ | ✅ Visual | ❌ MISSING |
| **Future growth range** | ⚠️ Estimates | ❌ | ❌ | ❌ | ⚠️ "What could happen" | ❌ | ❌ | ✅ Visual range | ❌ MISSING |
| **Story arc timeline** | ❌ | ❌ | ❌ | ❌ | ✅ Core product | ❌ | ❌ | ❌ | ⚠️ C28 exists |
| **Concept comparison** | ❌ | ⚠️ Bytes | ❌ | ❌ | ❌ | ✅ Core product | ❌ | ❌ | ⚠️ C172 planned |
| **Confidence indicators** | ❌ | ❌ | ❌ | ✅ AI confidence | ❌ | ❌ | ❌ | ❌ | ⚠️ C157 planned |
| **Recurring investment edu** | ✅ Core feature | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ MISSING |
| **Fractional share edu** | ✅ Core feature | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ MISSING |

### Legend
- ✅ = Full implementation
- ⚠️ = Partial/planned
- ❌ = Not available

---

## 4. New Feature Suggestions

### [ISSUE-C199] "Bear vs Bull" Visual Debate Cards
- **Source**: Competitor research round 46 (Simply Wall St "Bear vs Bull" visual debate)
- **Priority**: P2
- **Effort**: 8-12h
- **Alignment**: Core value #1 "Story first, data second" + Core value #5 "Benchmark-oriented analysis" + "Historian" positioning
- **Description**: Simply Wall St presents bull and bear arguments side-by-side as visual cards — not as text, but as visual cards with icons and key stats. Stock Explorer's peer comparison shows metrics but doesn't frame them as *arguments*. A "Bull vs Bear" card on each stock page would show: "🟢 Bull case: TSMC has 90% market share in advanced chips" vs "🔴 Bear case: TSMC's capital spending is growing faster than revenue." This is educational, not advisory — it teaches beginners to think in terms of *arguments*, not just *data*.
- **Implementation**: Add a "📊 多角度分析" section to the business card page with 2-3 bull points and 2-3 bear points, each as a visual card with an icon, one-sentence argument, and supporting metric. Use existing analogy engine for plain-language framing.
- **Competitive Gap**: 🟡 Simply Wall St has this but no TW competitor does; aligns with "historian" positioning

---

### [ISSUE-C200] "What If I Had Invested?" Historical Scenario Calculator
- **Source**: Competitor research round 46 (Magnify.money "What If" scenarios, StockStory forward-looking narratives)
- **Priority**: P2
- **Effort**: 10-14h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Ten-second test"
- **Description**: Magnify.money and StockStory both offer "What if?" scenario modeling — "What if you had invested $1000 in TSMC 5 years ago?" This is *educational*, not advisory. It teaches historical perspective and compound growth without recommending future action. Stock Explorer has historical price data but no interactive scenario calculator. Beginners want to understand "what would have happened" — this is the "historian" perspective applied to personal finance.
- **Implementation**: Add an interactive calculator to the business card page: user inputs an amount ($1000, $5000, $10000) and a time period (1 year, 3 years, 5 years, 10 years). Show the result as a visual card: "If you had invested $1000 in TSMC 5 years ago, you would have $2,400 today — a 140% return." Include a plain-language explanation: "This means your money would have grown by 140%, which is like turning $100 into $240." Use historical price data from FinMind.
- **Competitive Gap**: 🟡 Magnify.money has calculators but not stock-specific scenarios; no TW competitor has this

---

### [ISSUE-C201] "Daily Market Story" — 3-Minute Morning Briefing
- **Source**: Competitor research round 46 (Finimize daily 5-min lesson, Robinhood morning briefing)
- **Priority**: P1 (ELEVATED from C196)
- **Effort**: 12-16h
- **Alignment**: Core value #1 "Story first, data second" + Core value #3 "Adaptive and self-evolving" + "Ten-second test"
- **Description**: Finimize's entire product is built around a 5-minute daily lesson. Robinhood sends morning briefings. Stock Explorer has no daily touchpoint — users must actively visit the app. A "Daily Market Story" would be a single card shown on the homepage: "Today's Big Story: TSMC rose 3% on Apple's AI announcement. Here's why this matters..." This creates a *habit loop* — users check Stock Explorer every morning. C196 was originally P1; this round confirms it should be P0 given the retention impact.
- **Implementation**: Add a "📰 今日市場故事" card to the homepage. Content: (1) biggest market mover of the day, (2) plain-language explanation of why it moved, (3) one "Did You Know?" fact about the company. Auto-generated from M5 event detection + analogy engine. Manual curation for top 20 stocks.
- **Competitive Gap**: 🔴 No TW competitor has daily market storytelling; Finimize proves the model internationally

---

### [ISSUE-C202] "Story Arc" Timeline Labels
- **Source**: Competitor research round 46 (StockStory "Story Arcs," Simply Wall St narrative sections)
- **Priority**: P2
- **Effort**: 8-10h
- **Alignment**: Core value #1 "Story first, data second" + "Historian" positioning
- **Description**: StockStory identifies narrative arcs in company history — "The Rise," "The Crisis," "The Recovery." Stock Explorer's event timeline (C28) has the data but lacks *narrative labels*. A timeline with "The Rise (2020-2021)" is more memorable than a list of events. This is the difference between a *chronology* and a *story*.
- **Implementation**: Add narrative arc labels to the existing event timeline. Use M5 event data to auto-detect arcs: (1) sustained revenue growth = "成長期," (2) revenue decline + layoffs = "挑戰期," (3) recovery + new products = "轉型期." Show as colored segments on the timeline with plain-language labels.
- **Competitive Gap**: 🔴 No competitor has auto-detected narrative arcs — unique differentiator

---

### [ISSUE-C203] "Supply Chain Impact" Visual Map
- **Source**: Competitor research round 46 (Spiking supply chain mapping, Simply Wall St ecosystem)
- **Priority**: P2
- **Effect**: 14-18h
- **Alignment**: Core value #1 "Story first, data second" + Core value #4 "Point-to-point knowledge construction" + "Historian" positioning
- **Description**: Spiking maps customer-supplier relationships: "When Apple moves, here are the affected suppliers." Stock Explorer's group structure mapping (point-to-point) covers parent-subsidiary relationships but not *customer-supplier* relationships. A "Supply Chain Impact" map would show: "TSMC's customers: Apple (25%), NVIDIA (15%), AMD (10%)" — and when Apple has a big move, show the potential impact on TSMC.
- **Implementation**: Add a "供應鏈關係" section to the business card page. For top 20 stocks, manually curate customer-supplier relationships. Show as a simple diagram: "Apple → TSMC (25% of revenue)" with a plain-language explanation: "If Apple sells more iPhones, TSMC makes more chips." Use M5 event detection to highlight when a customer/supplier has a significant event.
- **Competitive Gap**: 🟡 Spiking has this but no TW competitor does; extends Stock Explorer's group structure advantage

---

### [ISSUE-C204] "Confidence Indicator" on AI Explanations
- **Source**: Competitor research round 46 (Spiking AI confidence, Simply Wall St estimate ranges)
- **Priority**: P2
- **Effort**: 4-6h
- **Alignment**: Core value #1 "Story first, data second" + "Ten-second test" + "Historian" positioning
- **Description**: Spiking shows confidence levels on AI explanations — "High confidence" vs "Low confidence." Stock Explorer's analogy engine and planned C188 "Why Did This Move?" don't indicate confidence. Beginners don't know when to trust an explanation. A simple confidence indicator (🟢 High / 🟡 Medium / 🔴 Low) would teach beginners that *not all explanations are equally certain* — this is a critical financial literacy concept.
- **Implementation**: Add a confidence indicator to all AI-generated explanations. High confidence = based on clear data (e.g., "TSMC moved +5% on earnings beat"). Medium confidence = based on correlation (e.g., "TSMC moved +5% possibly due to Apple news"). Low confidence = multiple factors (e.g., "TSMC moved +5% — market conditions, sector rotation, and news may all be contributing"). Use a simple emoji-based indicator.
- **Competitive Gap**: 🟡 Spiking has AI confidence but no TW competitor does; teaches critical thinking

---

### [ISSUE-C205] "Read Time" Indicator on All Content
- **Source**: Competitor research round 46 (Finimize "3 min read," Robinhood bite-sized content)
- **Priority**: P2
- **Effort**: 2-4h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + "Ten-second test" + Beginner-friendly
- **Description**: Finimize shows "3 min read" on every article. This sets expectations and reduces commitment anxiety — beginners are more likely to start reading if they know it's only 3 minutes. Stock Explorer has no read time indicators. Some sections (e.g., Financial Education Academy lessons) could be 10+ minutes, which intimidates beginners.
- **Implementation**: Add a "⏱️ X min read" indicator to all sections and lessons. Calculate based on word count (avg 200 words/min reading speed). For PPT-style pages, estimate based on number of slides (30 seconds per slide). Show as a subtle indicator at the top of each section.
- **Competitive Gap**: 🟢 No TW competitor has read time indicators; low effort, high impact

---

### [ISSUE-C206] "Recurring Investment" Concept Education
- **Source**: Competitor research round 46 (Robinhood recurring investments, Finimize habit-building)
- **Priority**: P2
- **Effort**: 6-8h
- **Alignment**: Core value #4 "Point-to-point knowledge construction" + Beginner-friendly + "Historian" positioning
- **Description**: Robinhood teaches recurring investments as a concept — "Invest $50/week automatically." Stock Explorer is purely analytical with no action layer, but it can *educate* about the concept. Beginners don't know that recurring investments exist, how they work, or why they reduce risk (dollar-cost averaging). This is educational, not advisory.
- **Implementation**: Add a "💡 投資小知識" section to the Financial Education Academy (or as a standalone "Did You Know?" card) explaining: (1) What are recurring investments? (2) How does dollar-cost averaging work? (3) Historical example: "If you had invested $100/month in TSMC for 5 years..." Use the C200 "What If" calculator as an interactive example.
- **Competitive Gap**: 🟡 Robinhood teaches this but no TW competitor does; educational (not advisory)

---

## 5. Design Pattern Analysis

### 5.1 Patterns We're Missing

| Pattern | Description | Competitors Using It | Our Status |
|---------|-------------|---------------------|------------|
| **Daily cadence** | Content delivered on a daily rhythm (email, notification, homepage card) | Finimize, Robinhood | ❌ Missing |
| **Confidence indicators** | Showing how certain an AI/system is about its explanation | Spiking, Simply Wall St | ❌ Missing |
| **Story arc labels** | Narrative labels on timelines ("The Rise," "The Crisis") | StockStory | ❌ Missing |
| **"Bear vs Bull" debate** | Visual presentation of both sides of an argument | Simply Wall St | ❌ Missing |
| **"What If" scenarios** | Interactive historical scenario modeling | Magnify.money, StockStory | ❌ Missing |
| **Read time indicators** | "X min read" on all content | Finimize, Robinhood | ❌ Missing |
| **Social proof** | "X people own this" or "trending" without FOMO | Robinhood, Public.com, Tickertape | ❌ Missing |
| **Micro-animations** | Subtle animations for state changes, loading, transitions | Robinhood, Simply Wall St | ❌ Missing |
| **One-page stock view** | Everything on one scrollable page (no tabs) | Robinhood | ❌ Missing (we use multi-page) |
| **Visual screener** | Drag-and-drop visual filtering (not forms) | Tickertape | ❌ Missing |
| **Supply chain visualization** | Customer-supplier relationship diagrams | Spiking | ❌ Missing |
| **Forward-looking ranges** | Future estimates shown as ranges, not single numbers | Simply Wall St | ❌ Missing |

### 5.2 Patterns We Have (Competitive Advantages)

| Pattern | Our Implementation | Competitors |
|---------|-------------------|-------------|
| **PPT-style presentation** | Custom CSS, one key point per page | Simply Wall St (similar) |
| **Plain-language analogies** | Analogy engine for all metrics | StockStory (similar but shallower) |
| **Adaptive event detection** | M5 engine with false positive filtering | Spiking (similar but real-time) |
| **Benchmark-oriented comparison** | Always compare to industry #1 | Tickertape (compares to average) |
| **Point-to-point group structure** | Parent-subsidiary mapping with ownership % | Spiking (customer-supplier only) |
| **Ex-dividend countdown** | Real-time countdown + badge | ❌ No competitor has this |
| **"Did You Know?" facts** | 70 facts for 7 stocks, rotating tips | ❌ No competitor has this |
| **Health score snowflake** | Visual 5-dimension health score | Simply Wall St (similar) |
| **Financial Education Academy** | 5 structured lessons with YAML content | Finimize (daily, not structured) |
| **Learn First Gate** | 4-lesson onboarding before data | ❌ No competitor has this |

### 5.3 Design Principles to Strengthen

1. **"Show, don't tell"**: Magnify.money and Simply Wall St prove that interactive visuals > static text. Stock Explorer should add more interactive elements (calculators, sliders, scenario modeling).

2. **"Daily > Comprehensive"**: Finimize's success proves that a small daily touchpoint beats a comprehensive weekly report. Stock Explorer's comprehensive analysis is valuable, but without a daily hook, users forget to come back.

3. **"Confidence > Certainty"**: Spiking's confidence indicators teach beginners that financial analysis is probabilistic, not deterministic. Stock Explorer should embrace uncertainty rather than presenting single-point answers.

4. **"Narrative > Chronology"**: StockStory's story arcs prove that labeled narratives are more memorable than event lists. Stock Explorer's event timeline needs narrative structure.

5. **"Social Learning > Social Trading"**: Public.com and Tickertape show that social features drive engagement, but Stock Explorer must keep social features *education-focused*, not *trade-focused*.

---

## 6. Recommendations

### Immediate (Next Sprint — Sprint 21)

1. **C188 "Why Did This Move?" — Inline AI Explanations** (P1, 10-14h)
   - Already planned for Sprint 21. Spiking sets the bar: explanations must be *inline*, *real-time*, and include *confidence indicators* (C204).
   - **Action**: Ensure C188 includes confidence indicators (combine with C204).

2. **C170 "Tappable Glossary"** (P1, 6-10h)
   - Already planned for Sprint 21. Robinhood and Finimize prove that inline explanations are table stakes.
   - **Action**: Prioritize completion; this is foundational for all other explanation features.

3. **C205 "Read Time" Indicators** (P2, 2-4h)
   - Lowest effort, high impact. Finimize proves this reduces commitment anxiety.
   - **Action**: Add to all sections and lessons in Sprint 21 as a quick win.

### Short-Term (Sprint 22-23)

4. **C201 "Daily Market Story"** (P1, 12-16h) — ELEVATED from C196
   - This round confirms daily cadence is the #1 retention pattern. Finimize's entire product is built on this.
   - **Action**: Build as a homepage card with auto-generated content from M5 + analogy engine.

5. **C199 "Bear vs Bull" Visual Debate Cards** (P2, 8-12h)
   - Simply Wall St proves this format works. Aligns perfectly with "historian" positioning.
   - **Action**: Add to business card page as a new section.

6. **C202 "Story Arc" Timeline Labels** (P2, 8-10h)
   - StockStory proves narrative arcs are more memorable than event lists.
   - **Action**: Enhance existing C28 timeline with auto-detected arc labels.

7. **C204 "Confidence Indicator" on AI Explanations** (P2, 4-6h)
   - Spiking proves this builds trust and teaches critical thinking.
   - **Action**: Add to C188 explanations and all analogy engine outputs.

### Medium-Term (Sprint 24+)

8. **C200 "What If I Had Invested?" Calculator** (P2, 10-14h)
   - Magnify.money and StockStory prove demand for historical scenario modeling.
   - **Action**: Build as an interactive calculator on the business card page.

9. **C203 "Supply Chain Impact" Visual Map** (P2, 14-18h)
   - Spiking proves supply chain mapping is valuable for understanding stock movements.
   - **Action**: Extend existing group structure mapping with customer-supplier relationships.

10. **C206 "Recurring Investment" Concept Education** (P2, 6-8h)
    - Robinhood proves beginners need this concept explained.
    - **Action**: Add to Financial Education Academy as a new lesson.

11. **C186 "Daily 5-Min Finance Lesson"** (P1, 10-14h)
    - Finimize's core product. Stock Explorer needs a daily educational touchpoint.
    - **Action**: Build as a daily-updated lesson on the homepage, separate from C201 (which is market-focused; C186 is concept-focused).

---

## Appendix: Competitor URLs

| Competitor | URL | Focus |
|------------|-----|-------|
| Robinhood | https://robinhood.com | Beginner-friendly investing |
| Finimize | https://finimize.com | Daily 5-min finance lessons |
| Public.com | https://public.com | Social investing + story cards |
| Spiking | https://spiking.com | AI-powered stock movement explanations |
| StockStory | https://stockstory.org | Visual stock stories |
| Magnify.money | https://magnify.money | Visual financial calculators |
| Tickertape | https://tickertape.in | Stock screening + community |
| Simply Wall St | https://simplywall.st | Visual infographic analysis |

---

*This is the forty-sixth competitor research round. Seven new feature suggestions identified (C199-C205, C201 elevated from C196). The most impactful finding is that daily content cadence is the #1 retention pattern across competitors — C201 (Daily Market Story) should be elevated to P0. The most unique opportunity is C202 (Story Arc Timeline Labels) — no competitor has auto-detected narrative arcs, making it a true differentiator for the "historian" positioning.*
