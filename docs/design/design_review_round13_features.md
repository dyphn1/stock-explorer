# Design Review: Round 13 New Features (C63-C68)

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: Evaluating 6 new features from Round 13 competitor research for UX impact, design consistency, beginner-friendliness, and design direction.
> **Current Design Grade**: A (0 P0, 7 P1, 10 P2)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Evaluation Framework](#evaluation-framework)
3. [C63: Sector Stories](#c63-sector-stories)
4. [C64: Daily Market Quiz](#c64-daily-market-quiz)
5. [C65: Company Filing Explorer](#c65-company-filing-explorer)
6. [C66: Risk Profile Quiz](#c66-risk-profile-quiz)
7. [C67: Community Sentiment](#c67-community-sentiment)
8. [C68: Weekly Market Digest](#c68-weekly-market-digest)
9. [Comparative Matrix](#comparative-matrix)
10. [New Design Issues](#new-design-issues)
11. [Recommendations Summary](#recommendations-summary)

---

## Executive Summary

All 6 Round 13 features align strongly with Stock Explorer's "historian" positioning and PPT-style design philosophy. Each feature was validated by 2-3 Asian market competitors, confirming genuine market demand. The evaluation identifies **2 features as immediate wins** (C66, C64), **2 as high-value medium-term additions** (C63, C68), **1 as a strategic differentiator** (C65), and **1 as requiring careful privacy-by-design** (C67).

**Key risk**: C67 (Community Sentiment) could undermine the "historian" positioning if social proof overshadows factual analysis. Must be designed as supplementary data, never as a recommendation signal.

**Key opportunity**: C65 (Company Filing Explorer) has **zero TW competitors** offering this — it is the single most powerful "historian" differentiator available.

---

## Evaluation Framework

Each feature is evaluated across 5 dimensions:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **UX Impact** | 25% | Engagement lift, retention impact, daily/weekly habit formation |
| **Design Consistency** | 25% | PPT-style adherence, Zone A/B/C compliance, color system, card component reuse |
| **Beginner-Friendliness** | 20% | Ten-second test pass, plain-language alignment, cognitive load |
| **Design Risk** | 15% | Page overload potential, positioning dilution, technical complexity |
| **Strategic Value** | 15% | Competitive differentiation, "historian" alignment, discovery mechanism value |

**Grading scale**: A+ / A / A- / B+ / B / B- / C+ / C / C- / D / F

---

## C63: Sector Stories

### Feature Summary
**Thematic stock collections with plain-language sector explanations**. Curated collections of stocks by industry/theme (semiconductors, electronics, finance, etc.), each with a "Sector Story Card" — what the sector does, why it matters, key performance drivers. 10-14h effort.

**Competitor Inspiration**: Toss Securities ("Investment Themes"), Minkabu ("Favorites Ranking")

### UX Impact: **A**

- **High discovery value**: This directly addresses D-007 (No Discovery Mechanism — the C+ graded gap in the current design review). Beginners currently land on the homepage with no guided path to stocks they'd care about.
- **Emotional connection**: "I use iPhone → let me learn about semiconductors" bridges the life-to-investment gap in a way that raw screeners (C42) cannot.
- **Low daily engagement, high session value**: Unlike a quiz or digest, Sector Stories is a "return when curious" feature — high utility during onboarding, lower recurring engagement.
- **Complements C42 (Stock Screener) vs. replaces it**: C42 is metric-driven (filter by P/E, ROE). C63 is narrative-driven (explore by life context). Both are needed; C63 better matches beginner mental models.

**Estimated UX Impact**: Resolves D-007 from C+ to B+ when combined with existing features.

### Design Consistency: **A-**

**Strengths:**
- Card-based layout naturally fits PPT-style "one key point per page" — one sector story = one collection page.
- Reuses existing `_info_card()` and `_summary_card()` patterns for sector-level data (sector performance, key metrics).
- Fits the existing Zone B sidebar as a navigation item ("產業故事") or as a new Zone C page type.
- Color system alignment: sector performance charts can use existing green/red for up/down, blue for clickable stocks.

**Concerns:**
- **New card type needed**: `_sector_story_card()` — similar to C48's Company Story Card but at sector level. Must be consistent with emerging card system (D-003 risk).
- **Grid layout challenge**: Showing 3-5 representative stocks per sector could violate PPT-style if done as a dense table. Must use individual stacked cards, not a table. This is a **D-010/Watchlist anti-pattern** risk.
- **Page length**: 10 sectors × (story + 3-5 stocks) could become a long scroll. Needs a card-grid landing page with individual sector pages behind clicks.

**Design Direction:**
```
Landing Page (Zone C):
┌─────────────────────────────────────────────┐
│  📊 產業故事 Sector Stories            │
│  "從生活中發現投資機會"                        │
├─────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ 半導體   │ │ 金融業   │ │ 電子業   │       │
│  │ 🔵      │ │ 🟢      │ │ 🔴      │       │
│  │ 3分鐘閱讀│ │ 3分鐘閱讀│ │ 3分鐘閱讀│       │
│  └─────────┘ └─────────┘ └─────────┘       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ 生技業   │ │ 零售業   │ │ 綠能     │       │
│  └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────────────────────────────┘

Sector Page (Zone C, after click):
┌─────────────────────────────────────────────┐
│  📊 半導體產業故事                             │
│  "台灣心臟：從晶片到你的手機"                   │
│                                              │
│  [Sector Story Card: 2-3 sentences]          │
│  [Performance Chart: sector vs index]        │
│                                              │
│  ── 代表個股 ──                               │
│  [Stock Card 1: TSMC — 一分鐘說明]            │
│  [Stock Card 2: 聯發科 — 一分鐘說明]          │
│  [Stock Card 3: 日月光 — 一分鐘說明]            │
└─────────────────────────────────────────────┘
```

### Beginner-Friendliness: **A+**

- **Ten-second test**: "Stock Explorer按產業分類股票，用故事解釋每個產業" — passes easily.
- **Natural mental model**: Beginners think in life contexts ("I use phones"), not financial metrics ("P/E < 15"). Sector Stories meets them where they are.
- **Plain-language-first**: Sector descriptions must follow the same analogy_engine patterns as existing company explanations.
- **Low cognitive load**: Browse → click → read story → click stock → learn. No decisions, no filters, no numbers upfront.

### Design Risk: **B+**

- **Medium risk**: The grid-of-cards landing page could feel like a traditional portal if not carefully designed. Must maintain generous whitespace (PPT-style).
- **Mitigation**: Limit to 6 sectors visible at once. Use large cards with icons, not dense lists.
- **Dependency**: Must wait for D-003 (card standardization) or at least define `_sector_story_card()` consistently. Without this, another inline HTML card variant enters the codebase.

### Strategic Value: **A**

- **Discovery mechanism**: Fills the #1 UX gap (D-007) with a beginner-appropriate approach.
- **Historian alignment**: Sector stories are "what happened to this industry" — pure historian positioning.
- **Competitor validation**: Toss Securities (Korea's fastest-growing broker) uses this exact pattern.

---

## C64: Daily Market Quiz

### Feature Summary
**Gamified daily engagement with streak counter**. One question per day about market knowledge, stock facts, or financial concepts. Immediate plain-language feedback. Streak counter for consecutive days. 8-12h effort.

**Competitor Inspiration**: Kabu.com ("Kabu Quiz" + leaderboard), Toss Securities ("Stock Quiz" + rewards)

### UX Impact: **A+**

- **Highest engagement potential**: Daily features drive retention better than any other pattern. Kabu.com's quiz is their #1 engagement driver.
- **Habit formation**: Streak counter creates variable-ratio reinforcement — the same mechanic behind Duolingo's growth.
- **Complements C52 (Quiz Mode)**: C52 is a 20-question comprehensive quiz (assessment). C64 is one question per day (engagement). Together they form a complete learning loop.
- **Low-friction entry**: 30-second time limit means zero commitment barrier.

**Estimated UX Impact**: Transforms Stock Explorer from "visit when researching" to "visit every day" — the strongest possible shift in user behavior.

### Design Consistency: **B+**

**Strengths:**
- Single-question format is inherently PPT-style: one key point per session.
- Streak counter fits neatly into Zone A (navbar) as a small badge, or Zone B (sidebar) as a gamification element.
- Can reuse existing card components for question display.

**Concerns:**
- **New UI pattern**: Quiz interaction (multiple choice → feedback) doesn't exist in current Stock Explorer. This is the first "game" element. Must feel like a natural extension of the learning experience, not a minigame bolted on.
- **Zone placement debate**: Where does the quiz live? Options:
  - **Zone A badge**: "🔥 7-day streak" → click to open Zone C quiz area
  - **Zone B widget**: Streak counter + "每日挑戰" button in sidebar
  - **Homepage takeover**: Full quiz as the first thing users see on the landing page
  - **Recommendation**: Zone B sidebar widget with expand in Zone C. Avoid Zone A (no interactive controls in navbar per design system).
- **Color system challenge**: Quiz feedback (correct/incorrect) wants green/red but the existing color system restricts red/green to price direction. Solution: Use blue for correct ("✅ 答對了！") and amber for incorrect ("🤔 再想想"), avoiding red/green confusion.

**Design Direction:**
```
Zone B Sidebar Addition:
┌──────────────────┐
│ 🔥 每日挑戰       │
│ 連續 7 天 ✓      │
│ [今日挑戰 →]      │
└──────────────────┘

Zone C Quiz Modal:
┌─────────────────────────────────────┐
│  📚 每日市場挑戰           Day 7    │
│                                      │
│  「本益比(P/E Ratio)是什麼？」        │
│                                      │
│  A. 公司賺錢能力的指標               │
│  B. 股票便宜還是貴的指標             │
│  C. 公司還債能力的指標               │
│  D. 公司成長速度的指標               │
│                                      │
│  [提交答案]                           │
│                                      │
│  ── 答後 ──                           │
│  ✅ A: 公司賺錢能力的指標            │
│  「本益比是...（白話文解釋）」        │
│  連續 8 天 🔥 明天再來！              │
└─────────────────────────────────────┘
```

### Beginner-Friendliness: **A+**

- **Ten-second test**: "每天一題，輕鬆學投資" — trivial.
- **Scaffolded learning**: Each question teaches one concept. No prerequisite knowledge for easy questions.
- **Immediate feedback**: Plain-language explanation after each answer reinforces learning (not just "correct/wrong").
- **Streak anxiety risk**: Some users may feel pressured. Mitigation: Make the streak visible but not punitive. "連續 7 天" not "已經 7 天沒中斷了".

### Design Risk: **B+**

- **Medium-low risk**: The primary risk is scope creep (adding leaderboards, points, badges beyond C60). Keep it minimal: one question, one explanation, one streak counter.
- **Content generation**: 365 questions/year is a content burden. Mitigation: Source from existing analogy_engine content, start with 50 questions, rotate.
- **Mobile concern**: Quiz interaction on mobile must be tap-friendly (large buttons, not small radio buttons).

### Strategic Value: **A**

- **Engagement loop**: The #1 missing piece in Stock Explorer's UX. Currently no reason to return daily.
- **Competitor validation**: Both Kabu.com (Japan) and Toss Securities (Korea) prove this drives engagement in Asian markets.
- **Education mechanism**: Each quiz is micro-learning. Over a year, users learn 365 financial concepts.

---

## C65: Company Filing Explorer

### Feature Summary
**AI-parsed annual reports in plain language**. Users can click on any section of a company's annual report (年報) and get a plain-language summary. Similar to Atom Finance's "Interactive Documents" but focused on TW market filings. 16-24h effort (highest-effort feature).

**Competitor Inspiration**: Atom Finance ("Interactive Documents"), Upside AI ("AI Earnings Analysis")

### UX Impact: **A**

- **Powerful differentiation**: No TW competitor offers this. Atom Finance is US-only. This is a "10x feature" that could define Stock Explorer.
- **Moderate engagement frequency**: Users visit annual reports 1-4 times per year per company, not daily. But the depth of each session is very high.
- **Trust building**: "Here's what the company said, and here's what it means" builds enormous trust with beginners who can't parse 200-page annual reports.
- **Historian positioning reinforcement**: This is the purest "historian" feature — translating historical documents into accessible narratives.

**Estimated UX Impact**: High per-session impact, low frequency. Transforms annual reports from "intimidating" to "accessible."

### Design Consistency: **A-**

**Strengths:**
- Section-by-section parsing naturally maps to PPT-style progressive disclosure: one section = one expandable card.
- Link to existing stock analysis pages fits the "hub and spoke" navigation model already in place.
- Highlighting key metrics connects to existing C43 (Snowflake) dimension data.

**Concerns:**
- **Highest UI complexity**: This is the most complex feature proposed in Round 13. Requires:
  - Document outline sidebar (Zone B sub-nav?)
  - Section content area (Zone C main)
  - Expandable plain-language overlay for each section
  - Key metric highlights inline
  - Back-to-stock-card navigation
- **Zone layout challenge**: The document outline wants to live in Zone B, but Zone B is global navigation. Options:
  - **Option A**: Replace Zone B content when in "Filing Explorer" mode (contextual sidebar)
  - **Option B**: Use Zone C left column for outline, right column for content
  - **Recommendation**: Option A — filing explorer is a dedicated mode where Zone B becomes the document's table of contents. This is how Atom Finance handles it.
- **New card type**: `_filing_section_card()` — expandable card with original text + plain-language toggle.

**Design Direction:**
```
Zone A:
┌─────────────────────────────────────────────────────┐
│  2330 台積電 │ 半導體 │ 105.0 (+1.5)                  │
│  **▎公開說明書** │ 業務概況 │ 財務報表 │ 公司治理 │      │
├────────────┬────────────────────────────────────────┤
│ Zone B     │ Zone C                                  │
│ (File TOC) │                                         │
│ 📋 目錄    │  📄 第3節：業務概況                      │
│            │                                         │
│ ▸ 公司簡介  │  [Original filing text excerpt]          │
│ ▸ 業務概況  │                                         │
│ ▸ 財務報表  │  [🗣️ 白話文解釋]                         │
│   ├ 綜合損益 │  「台積電主要做晶圓代工，也就是...」     │
│   ├ 資產負債 │                                         │
│   └ 現金流量 │  [📊 關鍵指標]                           │
│ ▸ 公司治理  │  營收：2.2兆 (+15%)                      │
│ ▸ 風險因素  │  毛利率：53%                              │
└────────────┴─────────────────────────────────────────┘
```

### Beginner-Friendliness: **A**

- **Ten-second test**: "看不懂年報？Stock Explorer幫你翻譯成白話文" — clear and compelling.
- **Progressive complexity**: Beginners read the plain-language explanation. Advanced users can toggle to the original filing text.
- **Contextual education**: Learning about a company by reading its own words, with translations, is the most natural educational approach.
- **Reading burden concern**: Annual reports are long. Must have a "Key Highlights" summary at the top (similar to C37 Key Takeaways).

### Design Risk: **B-**

- **Highest technical risk**: 16-24h effort means significant engineering. AI parsing of TW annual reports (often PDF, Traditional Chinese) is non-trivial.
- **Content accuracy risk**: AI-parsed explanations could misrepresent filing content. This would violate the "Correctness > Clarity" design principle. Must include a disclaimer: "此為AI協助整理，請以原始文件為準."
- **Dependency risk**: Should not block C66/C64/C63. Can run as a separate stream.

### Strategic Value: **A+**

- **Zero TW competition**: This is the strongest differentiator in the entire Round 13 research.
- **Pure historian positioning**: "Here's what the company said, translated into plain language" — the historian ideal.
- **Atom Finance validation**: Atom Finance is considered best-in-class for this feature, and they only support US SEC filings. TW market is wide open.

---

## C66: Risk Profile Quiz

### Feature Summary
**8-10 question risk assessment during onboarding**. Covers time horizon, risk tolerance, financial goals, investment experience. Results displayed as a simple profile ("Conservative Growth" / "Balanced Explorer"). Drives personalized content recommendations. 6-10h effort (lowest-effort feature).

**Competitor Inspiration**: Smart FOLIO ("Risk Profile Quiz"), Syfe ("Risk Assessment"), Toss Securities (implied)

### UX Impact: **A-**

- **Onboarding enhancement**: Directly enhances C58 (Beginner Onboarding), which is the P1 prerequisite feature in Sprint 5.
- **Personalization**: Results driving content recommendations creates a tailored experience from day one.
- **One-time value**: Users take the quiz once (retakeable). Not a recurring engagement driver, but significantly improves the first-session experience.
- **Emotional value**: "This quiz told me I'm a 'Balanced Explorer'" creates identity and ownership.

**Estimated UX Impact**: Enhances C58 from a basic onboarding flow to a personalized onboarding experience. Reduces bounce rate in first session.

### Design Consistency: **A**

- **Natural card progression**: Each question is a card → next card → next card → result card. This is "one key point per page" personified (one question per screen).
- **Fits existing Zone C**: Can be a dedicated onboarding page that appears before the main app.
- **Result card reuses patterns**: Risk profile result is just a special `_summary_card()` with a unique icon.
- **Color system friendly**: Risk profiles can use the existing categorical colors (Conservative = 🟢, Balanced = 🔵, Aggressive = 🟡).

**Design Direction:**
```
Onboarding Flow:

[Question 1/8] Zone C:
┌─────────────────────────────────────────┐
│  📊 投資風險評測                          │
│  ─────────────────────                   │
│  問題 1 / 8                               │
│                                          │
│  「你預計什麼時候會用到投資的錢？」         │
│                                          │
│  ○ 1年以內                               │
│  ○ 1-3年                                │
│  ○ 3-5年                                │
│  ○ 5年以上                               │
│                                          │
│  [下一題 →]                               │
└─────────────────────────────────────────┘

[Results] Zone C:
┌─────────────────────────────────────────┐
│  🎯 你的投資屬性                          │
│  ─────────────────────                   │
│                                          │
│  「穩健探索者」Balanced Explorer          │
│                                          │
│  你希望穩定成長，願意承擔適度風險...       │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ 📊 為你推薦：                     │   │
│  │ • 金融股 (穩定配息)              │   │
│  │ • ETF (分散風險)                 │   │
│  │ • 大型藍籌股                     │   │
│  └──────────────────────────────────┘   │
│                                          │
│  [開始探索 Stock Explorer] [重新評測]     │
└─────────────────────────────────────────┘
```

### Beginner-Friendliness: **A+**

- **Ten-second test**: "一個小測驗，幫你了解自己適合什麼投資" — perfect clarity.
- **No financial knowledge required**: Questions use life scenarios, not financial jargon.
- **Reassuring**: Beginners fear risk. Making it a quiz makes risk tangible and personal rather than abstract.
- **Action-oriented result**: "Based on your profile, here's what to explore" turns assessment into action.

### Design Risk: **A-**

- **Lowest risk of all 6 features**: Simple question→answer→result pattern. No complex UI.
- **One design concern**: Must NOT result in investment advice. "Based on your profile, you might find X interesting" is ok. "Based on your profile, you should buy X" violates historian positioning. All recommendation language must be discovery-oriented, not advisory.

### Strategic Value: **A-**

- **Low effort, high value**: 6-10h is the cheapest of all Round 13 features. Returns: onboarding personalization + competitor parity.
- **C58 prerequisite**: Enhances the most important P1 onboarding feature.
- **Competitor parity**: Every major platform (Smart FOLIO, Syfe, Toss) has this. Not having it is a gap.

---

## C67: Community Sentiment

### Feature Summary
**Social proof indicator showing what other users think about a stock**. "X% of users who viewed this stock added it to their watchlist." Optional emoji reactions. "Most viewed stocks this week" leaderboard. 12-16h effort.

**Competitor Inspiration**: Minkabu ("Minkabu Rating"), eToro ("Social Sentiment"), Toss Securities ("Social Feed")

### UX Impact: **B+**

- **Discovery value**: "Lots of people are looking at this stock" is a valid discovery signal for beginners.
- **Social proof**: Reduces the isolation beginners feel. "Other people are also curious about TSMC" is reassuring.
- **Emoji reactions**: Quick, lightweight engagement. Users can react without writing.
- **Moderate engagement**: Only meaningful when viewing a stock page. Doesn't drive standalone sessions.

**Estimated UX Impact**: Supplementary feature. Enhances existing pages, doesn't create new engagement loops.

### Design Consistency: **B**

**Strengths:**
- Sentiment indicators are small widgets, not page-dominating features. Can be embedded in existing Zone C card layouts.

**Concerns:**
- **UI complexity**: Emoji reaction systems, percentage bars, and leaderboards are new UI patterns. Risk of feeling like a different product (similar to D-10 watchlist risk).
- **Zone placement**: Where does sentiment live?
  - **In stock card**: Small "% added to watchlist" badge on each stock card (homepage, sector stories)
  - **On stock page**: Dedicated "社群看法" section on the business card page (D-005 page overload risk)
  - **Leaderboard**: Separate page or sidebar section
- **Color system conflict**: Sentiment data (positive/negative/neutral) wants red/green, but those are reserved for price direction. Must use blue/amber/gray for neutral-positive-negative.

**Design Direction:**
```
Stock Card Enhancement:
┌─────────────────────────────────┐
│  2330 台積電         105.0 (+1.5)│
│  半導體晶圓代工                    │
│  "台灣最大的晶片製造商"            │
│  👀 1,247人看過  ❤️ 342人收藏    │
│  [查看詳細 →]                     │
└─────────────────────────────────┘

Stock Page Section (Zone C):
┌─────────────────────────────────────┐
│  👀 社群看法                          │
│  ─────────────────────               │
│  本週 1,247 人瀏覽此股票              │
│  342 人加入觀察清單 (27%)            │
│                                      │
│  大家的反應：                         │
│  😊 好奇 (45%)  🤔 觀望 (30%)        │
│  😮 驚訝 (15%)  😴 無感 (10%)        │
└─────────────────────────────────────┘
```

### Beginner-Friendliness: **B+**

- **Ten-second test**: "看看其他人對這支股票的看法" — clear.
- **Social proof value**: Beginners benefit most from knowing what others think. Reduces decision paralysis.
- **Risk**: Could create herd-following behavior. "Everyone likes this stock, so I should too" contradicts the "education first, decisions are yours" positioning.

### Design Risk: **B-**

- **Highest positioning risk**: Stock Explorer is a "historian," not a social platform. Community sentiment could subtly shift the perceived purpose.
- **Mitigation**: Frame sentiment as historical data: "Here's how other users have interacted with this stock" not "Here's what other users think you should do."
- **Privacy concern**: Requires user tracking (even anonymous). Must be privacy-first aggregate data only.
- **Leaderboard risk**: "Most viewed stocks this week" could create a popularity contest. Include a historian-flavored frame: "本週最多人研究的股票 — 大家都在學什麼？"

### Strategic Value: **B+**

- **Social proof without full social features**: Lightweight social without building a social network. Good stepping stone.
- **Competitor validation**: Minkabu (30M+ monthly pageviews) proves the model works in Japan.
- **Not a historian differentiator**: This feature supports engagement but doesn't reinforce the core positioning.

---

## C68: Weekly Market Digest

### FeatureSummary
**Curated weekly market summary in plain language**. Published every Friday after market close. Covers major index movements, sector performance, notable stock stories. Written in Stock Explorer's "historian" voice. 8-12h effort.

**Competitor Inspiration**: Syfe ("Market Insights"), Smart FOLIO ("Market Commentary"), Upside AI ("Daily AI Briefing")

### UX Impact: **A-**

- **Recurring engagement**: Weekly is digestible for beginners (competitor insight: Syfe and Smart FOLIO chose weekly over daily deliberately).
- **Content marketing value**: Can be shared (C53 social sharing), emailed, or linked from push notifications.
- **Complements C49 (Daily Market Pulse)**: C49 provides daily raw updates. C68 provides weekly curated analysis. If C68 is approved, C49 scope can be reduced or deferred.
- **Low creation burden**: One curated piece per week vs. 365 daily quiz questions.

**Estimated UX Impact**: Gives users a reason to return weekly. Complements daily quiz (C64) as the "depth" layer to the quiz's "breadth" layer.

### Design Consistency: **A**

- **Perfect PPT-style fit**: One digest = one page. Each section answers one question (what happened to indices, what happened to sectors, what happened to notable stocks).
- **Natural content hierarchy**: Hero summary → index chart → sector grid → stock spotlights. Each layer is progressive disclosure.
- **Color system**: Index charts use existing green/red for up/down. Sector grid uses existing card colors.
- **Link to existing pages**: Each stock spotlight links to the company's business card page — seamless navigation.

**Design Direction:**
```
Zone C — Weekly Digest Page:

┌─────────────────────────────────────────────────┐
│  📰 每週市場週報                    6月第2週    │
│  "這週市場發生了什麼事"                           │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ 📊 本週重點一句話：                          │ │
│  │ 「半導體帶頭衝，金融股拖累大盤」              │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ── 大盤指數 ──                                  │
│  [Chart: TAIEX weekly performance]              │
│  加權指數：+1.2%｜櫃買指數：+2.8%                 │
│                                                  │
│  ── 產業表現 ──                                  │
│  [Sector Heatmap: top/bottom 5 sectors]          │
│  🟢 半導體 +4.5%  🟢 電子 +3.2%                 │
│  🔴 金融 -1.8%    🔴 紡織 -0.9%                 │
│                                                  │
│  ── 本週焦點股 ──                                 │
│  [Stock Spotlight 1: TSMC — 一分鐘白話文]        │
│  [Stock Spotlight 2: 富邦金 — 一分鐘白話文]      │
│  [Stock Spotlight 3: 聯發科 — 一分鐘白話文]       │
│                                                  │
│  ── 歷史上的這週 ──                               │
│  「過去5年的6月第2週，市場平均...」               │
│                                                  │
│  [📤 分享本週週報]  [👀 往期週報]                 │
└─────────────────────────────────────────────────┘
```

### Beginner-Friendliness: **A+**

- **Ten-second test**: "每週一次，用白話文告訴你市場發生什麼事" — clear value proposition.
- **Narrative format**: Written in Stock Explorer's "historian" voice — consistent with existing tone.
- **Links to deeper learning**: Each stock spotlight links to the full company analysis — the digest is an entry point, not a destination.
- **"本週重點一句話"**: The hero summary line is a PPT-style superpower — one sentence tells you everything.

### Design Risk: **A-**

- **Low design risk**: Layout reuses existing card and chart components. Section hierarchy is clear.
- **Content consistency risk**: Weekly publication requires consistent content pipeline. If a week is missed, the feature looks abandoned.
- **Compatibility with C49**: Must clarify relationship. Recommendation: C68 replaces C49 as the market commentary feature. C49 Daily Pulse is deferred. Rationale: Weekly is more digestible for beginners (competitor validation) and requires 1/7th the content production.

### Strategic Value: **A-**

- **Engagement loop**: Weekly reason to return. Complements daily quiz (C64).
- **Content marketing**: Shareable weekly content increases organic reach.
- **Historian positioning**: "Here's what happened this week in plain language" is the essence of the historian voice.
- **Recommendation authority**: Regularly explaining market events positions Stock Explorer as the go-to source.

---

## Comparative Matrix

| Dimension | C63 Sector Stories | C64 Daily Quiz | C65 Filing Explorer | C66 Risk Quiz | C67 Community Sentiment | C68 Weekly Digest |
|-----------|-------------------|----------------|--------------------|---------------|-----------------------|--------------------|
| **Priority** | P2 | P2 | P2 | P2 | P2 | P2 |
| **Effort** | 10-14h | 8-12h | 16-24h | 6-10h | 12-16h | 8-12h |
| **UX Impact** | A | A+ | A | A- | B+ | A- |
| **Design Consistency** | A- | B+ | A- | A | B | A |
| **Beginner-Friendliness** | A+ | A+ | A | A+ | B+ | A+ |
| **Design Risk** | B+ | B+ | B- | A- | B- | A- |
| **Strategic Value** | A | A | A+ | A- | B+ | A- |
| **Overall Grade** | **A-** | **A** | **A-** | **A-** | **B+** | **A-** |

### Ranking by Priority for Implementation

| Rank | Feature | Rationale |
|------|---------|-----------|
| 1 | **C66 Risk Quiz** | Lowest effort (6-10h), directly enhances C58 (P1 prerequisite), every competitor has it |
| 2 | **C64 Daily Quiz** | Highest engagement driver, extends C52, validated by 2 major competitors |
| 3 | **C68 Weekly Digest** | Replaces C49 (scope reduction), weekly > daily for beginners, strong historian positioning |
| 4 | **C63 Sector Stories** | Fills D-007 discovery gap, strong beginner appeal, medium effort |
| 5 | **C65 Filing Explorer** | Highest strategic value but highest effort. Defer to post-Sprint 3 |
| 6 | **C67 Community Sentiment** | Lowest historian alignment, privacy risks, positioning concerns |

---

## New Design Issues

### D-035: C64 Quiz UI Pattern Not in Design System

**Priority**: P1
**Effort**: 2-3h
**Source**: C64 Daily Market Quiz evaluation

**Problem**: The quiz feature introduces the first "interactive test" UI pattern to Stock Explorer. No existing design system guidance for quiz interactions (question display, answer selection, feedback display, streak indicator). If implemented ad-hoc, this will become another D-003-style card inconsistency.

**Proposed Resolution**: Before C64 development begins, create a lightweight design spec for quiz UI:
- Question card CSS (reuse `_info_card` base, add numbered indicator)
- Answer button styles (reuse existing `st.button` but add CSS for selected/unselected state)
- Feedback state (correct: blue banner; incorrect: amber banner — NOT green/red)
- Streak badge (Zone B widget, compact, uses amber color)

### D-036: C67 Sentiment Data Could Undermine Historian Positioning

**Priority**: P1
**Effort**: 1h (guideline writing)
**Source**: C67 Community Sentiment evaluation

**Problem**: Social proof signals ("342 people added this to watchlist") could create herd-following behavior that contradicts the "historian, not stock picker" positioning. If users interpret community sentiment as implicit advice, Stock Explorer risks becoming a social trading platform.

**Proposed Resolution**: Add a tone guideline to `docs/domain/design_system.md`:
- **Section IX: Community Data Guidelines**
  1. Always frame community actions as historical behavior: "X users did Y" never "X users recommend Y"
  2. Never place sentiment data alongside buy/sell-relevant metrics (P/E, health score)
  3. Include a persistent banner: "社群數據僅供參考，不構成投資建議"
  4. Emoji reactions must be framed as "reactions," not "ratings"

### D-037: C65 Document Layout Needs Zone B Context Switching

**Priority**: P2
**Effort**: 2-3h
**Source**: C65 Company Filing Explorer evaluation

**Problem**: The current design system specifies Zone B as global navigation (search, hot stocks, hot ETFs). C65 requires Zone B to become a document table of contents when in "Filing Explorer" mode. This is a contextual Zone B — not in the current design system.

**Proposed Resolution**: Define a "Contextual Sidebar" pattern:
- When a "document mode" feature is active, Zone B switches to document-specific navigation
- A "← 返回" button at the top of Zone B allows users to exit document mode
- Zone B retains its collapse/expand behavior in both modes
- This pattern could also serve future features (e.g., C47 Education Academy with chapter navigation)

### D-038: C63/C68 Both Need New Landing Pages — IA Implication

**Priority**: P2
**Effort**: 1-2h
**Source**: C63 Sector Stories + C68 Weekly Digest evaluation

**Problem**: C63 needs a "Sector Stories" landing page and C68 needs a "Weekly Digest" archive page. Neither fits into the existing Zone A tab structure (which is per-stock). Both are cross-stock informational features. This implies a need for a **non-stock home page** — something Stock Explorer currently lacks.

**Proposed Resolution**: Create a "Home" or "探索" tab in Zone A that provides:
- Sector Stories card grid (C63)
- Latest Weekly Digest (C68)
- Daily Quiz entry point (C64)
- Risk profile badge (C66)
- Community leaderboard (C67)

This is essentially D-026 (No Beginner Onboarding) + D-007 (No Discovery) addressed with a single non-stock landing zone.

---

## Recommendations Summary

### Immediate Design Concerns

1. **D-035 (P1)**: Create quiz UI pattern spec before C64 development — prevents D-003-style inconsistency
2. **D-036 (P1)**: Write community data tone guidelines before C67 development — protects historian positioning
3. **D-037 (P2)**: Define contextual sidebar pattern for C65 — prevents ad-hoc Zone B hacking
4. **D-038 (P2)**: Plan non-stock landing page (Home/探索 tab) — resolves D-007 and D-026 simultaneously

### Implementation Sequence

| Sprint | Feature | Prerequisite Design Work |
|--------|---------|------------------------|
| **Sprint 4** (current) | D-035 quiz UI spec (2-3h) | Before C64 development |
| **Sprint 5** | C66 Risk Quiz (6-10h) | D-036 tone guidelines (1h) |
| **Sprint 5** | C64 Daily Quiz (8-12h) | D-035 quiz spec complete |
| **Sprint 5** | D-036 community guidelines (1h) | Before C67 design starts |
| **Sprint 6** | C68 Weekly Digest (8-12h) | D-038 landing page plan (1-2h) |
| **Sprint 6** | C63 Sector Stories (10-14h) | D-038 landing page plan (1-2h) |
| **Sprint 6** | C67 Community Sentiment (12-16h) | D-036 guidelines mandatory |
| **Sprint 7+** | C65 Filing Explorer (16-24h) | D-037 contextual sidebar pattern (2-3h) |

### Design Grade Impact Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | All 6 features implemented with design specs; D-035 through D-038 resolved; landing page (D-038) transforms discovery experience |
| **Expected case** | A | C66, C64, C68 implemented cleanly; C63 and C65 deferred; D-035 and D-036 resolved |
| **Worst case** | A- | C64 or C67 implemented without design specs, creating new D-003-style inconsistencies that compound existing P1 issues |

### Key Design Risks to Monitor

1. **Card system scalability (D-003)**: 6 new features = ~3-4 new card types (`_sector_story_card`, `_quiz_card`, `_filing_section_card`, `_sentiment_badge`). Each must be added to the design system, not implemented inline.
2. **Page overload (D-005)**: C68 adds a new page type. C67 adds a section to existing pages. Combined with planned C44/C48/C56, Zone C is growing fast. D-032 (progressive disclosure) is more critical than ever.
3. **Color system compliance**: C64 quiz feedback (can't use green/red) and C67 sentiment (can't use green/red) both need careful color mapping. Verify all new features use only the approved 8-color system.
4. **Zone A expansion**: Non-stock landing page (D-038) means Zone A needs more than stock tabs. This is a structural change requiring careful IA design.
5. **Historian dilution**: C67 (Community Sentiment) is the weakest historian fit. Strongly recommend framing as "historical user behavior data" and including the disclaimer banner (D-036).

### Final Note: The Non-Stock Landing Page Opportunity

The most significant design insight from this evaluation is that **4 of 6 Round 13 features (C63, C64, C67, C68) need a non-stock landing surface**. Currently, Stock Explorer only surfaces content in the context of a specific stock. A "Home" or "探索" page — accessible as the first Zone A tab when no stock is selected — would:

- Serve as the Sector Stories gallery (C63)
- Host the Daily Quiz entry point (C64)
- Display the latest Weekly Digest (C68)
- Show Community Leaderboard (C67)
- Feature the Risk Profile result badge (C66)
- Replace the blank/novel experience of landing on Stock Explorer with no stock selected

This single piece of IA architecture (D-038) has the highest transformative potential of any design recommendation in this review. It converts Round 13's disparate features into a cohesive "daily learning experience" and directly addresses the two longest-standing UX gaps: D-007 (No Discovery) and D-026 (No Beginner Onboarding).

---

*Next design review: After Sprint 5 feature implementation. Update this file with implementation assessment for each feature as it ships.*
