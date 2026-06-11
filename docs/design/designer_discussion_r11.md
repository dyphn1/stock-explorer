# Design Review — Discussion Round 11

> **Author**: Design Reviewer
> **Date**: 2026-06-17
> **Context**: Round 11 review — evaluating 7 new competitor-inspired features (C48-C54) for UX impact, design direction, and fit with the PPT-style design system. Sprint 2 is complete (C37, C39, C43, C45). Sprint 3 is in progress. The business card page now has 13 sections and is at A- grade.
> **Current Design Grade**: A- (upgraded from B+ in Round 10)

---

## Table of Contents

1. [UX Impact Assessment](#ux-impact-assessment)
2. [Design Direction for C48 (Company Story Card)](#design-direction-for-c48-company-story-card)
3. [Design Direction for C49 (Daily Market Pulse)](#design-direction-for-c49-daily-market-pulse)
4. [Design Direction for C50 (Learning Progress Tracker)](#design-direction-for-c50-learning-progress-tracker)
5. [Design Direction for C51 (Sector Heatmap)](#design-direction-for-c51-sector-heatmap)
6. [Design Direction for C52 (Quiz Mode)](#design-direction-for-c52-quiz-mode)
7. [Design Direction for C53 (Social Sharing)](#design-direction-for-c53-social-sharing)
8. [Design Direction for C54 (Video/Audio Explanation)](#design-direction-for-c54-videoaudio-explanation)
9. [Design Risks & Cross-Cutting Concerns](#design-risks--cross-cutting-concerns)
10. [Proposed Design Directions](#proposed-design-directions)
11. [Recommendation](#recommendation)

---

## UX Impact Assessment

### Current Business Card Page State (Post-Sprint 2)

The business card page now has 13 sections:

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

**That is 13 sections on a single page.** The Round 10 discussion already flagged that C44 and C46 cannot be added as full sections without progressive disclosure. The same logic applies to ALL 7 new features.

### Overload Risk Matrix for C48-C54

| Feature | Proposed Placement | Overload Risk | PPT-Style Risk | Recommendation |
|---------|-------------------|---------------|----------------|----------------|
| **C48** (Story Card) | Business Card page | 🟡 MEDIUM — replaces/enhances C37 | 🟢 LOW — card-based, visual | Merge with C37 or replace it |
| **C49** (Market Pulse) | **New page** (sidebar nav) | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |
| **C50** (Progress Tracker) | **New page** (sidebar nav) | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |
| **C51** (Sector Heatmap) | **New page** (sidebar nav) | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |
| **C52** (Quiz Mode) | **New page** or within C47 Academy | 🟢 LOW — separate page | 🟢 LOW — no impact on business card | Safe to implement as-is |
| **C53** (Social Sharing) | Business Card page (share button) | 🟡 MEDIUM — adds UI element | 🟡 MEDIUM — new interaction pattern | Needs careful placement |
| **C54** (Video/Audio) | Business Card page or Lesson page | 🟡 MEDIUM — adds media player | 🟡 MEDIUM — new media type | Needs progressive disclosure |

### Key Finding: Only C48 and C53 Touch the Business Card Page

Of the 7 new features, only **C48 (Company Story Card)** and **C53 (Social Sharing)** would modify the business card page itself. The other 5 (C49, C50, C51, C52, C54) are new pages or additions to separate pages. This is good news for page overload.

However, C48 is essentially a **superset of C37 (Key Takeaways)** — both are "summary cards" that tell the company's story. The design decision is whether to replace C37 with C48 or merge them.

---

## Design Direction for C48 (Company Story Card)

### 1. UX Impact on Business Card Page

**Risk: 🟡 MEDIUM** — C48 is a "30-second visual summary" that overlaps significantly with C37 (Key Takeaways). Both serve the same purpose: give the user a quick understanding of the company.

**Key question**: Is C48 a replacement for C37, or an enhancement?

**Analysis**:
- C37 (Key Takeaways) = text-based summary (3-5 bullets, ≤ 200 chars). Implemented in Sprint 2.
- C48 (Story Card) = **visual** summary with charts, icons, and narrative flow. Proposed for Round 11.

The competitor research shows:
- **Stake** uses a card-stack approach: swipeable cards with key facts
- **StockEdge** uses a "Company Story" section with visual timeline
- **Finimize** uses a "Why It Matters" narrative summary

**Recommendation**: C48 should **replace and enhance C37**, not be added alongside it. The current C37 is text-heavy. C48 would be a visual-first evolution of the same concept. Adding both would be redundant and push the page to 14 sections.

### 2. Design Consistency with PPT-Style Principle

**Placement**: Same as C37 — FIRST content element on the business card page, below the header. This is the "slide title."

**Card design** (evolved from C37):
- **Visual layout**: Not just text bullets. Use a **visual story card** with:
  - Company one-liner (large, bold)
  - 3 key visual metrics (icon + number + label, horizontal layout)
  - 1 mini chart (revenue trend sparkline or snowflake mini)
  - "Story" narrative (≤ 80 chars)
- **Card style**: Orange/amber hero card (the style C37 was supposed to have but doesn't — see D-016). Border `#F39C12`, background `#FFF8F0`.
- **Icon**: `📖` (open book) — signals "story" not just "summary."
- **Character limits**: Total card text ≤ 150 Chinese characters. Visual elements (charts, metrics) don't count toward this limit.

**PPT-style compliance**: The story card IS the "one key point" of the page. Everything else is supporting detail. This is perfectly aligned with PPT-style.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Stake** | Card-stack with swipeable key facts | 3 visual metric blocks + 1 mini chart in a single card |
| **StockEdge** | Company Story with visual timeline | Revenue sparkline + 3 key events as a timeline strip |
| **Finimize** | "Why It Matters" narrative | Plain-language story (≤ 80 chars) with analogy |

**Key differentiator**: No competitor combines a visual story card with the Snowflake health visualization. The combination of C48 (story) + C43 (snowflake) would be unique: "Here's the story → Here's the health score → Here's what changed → Here are the details."

### 4. Mobile Responsiveness Considerations

- **Visual metrics**: 3 metrics in a row on desktop → stack vertically on mobile
- **Mini chart**: Full-width on mobile, may need simplified labels
- **Card padding**: Increase on mobile for readability
- **Avoid**: Horizontal scrolling within the card

### 5. Ten-Second Test Implications

**C48 IS the ten-second test answer.** The user should be able to:
1. Read the one-liner (3 seconds)
2. Glance at 3 key metrics (3 seconds)
3. Read the story narrative (4 seconds)
4. Understand: "This company does X, its key strength is Y, and the trend is Z"

**If the user sees a wall of text, the test fails.** Visual-first is non-negotiable.

### Design Spec Summary

```markdown
Section: 📖 公司故事 (replaces C37 Key Takeaways)
├── Visual Story Card (orange/amber hero card)
│   ├── One-liner (large, bold, ≤ 40 chars)
│   ├── 3 Visual Metrics (icon + number + label)
│   │   ├── 💰 營收: 2.89兆元 (+15%)
│   │   ├── 📈 ROE: 25% (每100元賺25元)
│   │   └── 🏷️ 本益比: 18x (歷史中間)
│   ├── Mini revenue sparkline (6-month trend)
│   └── Story narrative (≤ 80 chars, plain language)
└── Timestamp: "🕐 更新於 YYYY-MM-DD"
```

---

## Design Direction for C49 (Daily Market Pulse)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C49 is a new top-level page accessible from the sidebar. It does not touch the business card page.

**Strategic impact**: HIGH — This creates a **daily engagement loop**. Finimize's newsletter and StockEdge's daily analysis prove that daily content drives retention. Stock Explorer currently has no reason for users to return daily. C49 changes that.

**Key question**: What is the entry point?
- Option A: New sidebar entry `📰 市場日報` (Market Daily)
- Option B: Homepage widget (requires a homepage — currently Stock Explorer opens to search)
- Option C: Both (widget on homepage + full page in sidebar)

**Recommendation**: Option A for now (sidebar entry). A homepage (Option B) is a larger UX discussion that affects the entire product architecture.

### 2. Design Consistency with PPT-Style Principle

**Page structure** (PPT-style: one key point per "slide"):
```
Slide 1: "今日市場概況" (hero text, date, ≤ 40 chars summary)
Slide 2: Market indices (3-4 key indices with direction arrows)
Slide 3: Top movers (5 gainers + 5 losers, card-based)
Slide 4: Sector performance (mini heatmap or bar chart)
Slide 5: Key events today (earnings, economic data, news)
```

**Card design**: Use existing card types:
- Index cards: Standard info card (blue border) with `📊` icon
- Mover cards: Standard card with direction color (green ↑ / red ↓)
- Event cards: Tip card (orange border) with `📅` icon

**Content tone** (historian positioning): Factual, not predictive. "Today, the TAIEX rose 1.2% driven by semiconductor earnings" not "The market will continue to rise."

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Finimize** | Daily newsletter (text-first) | Visual-first with cards and charts |
| **StockEdge** | Daily analysis (PDF + app) | In-app daily page with interactive elements |
| **Moomoo** | Market summary with AI commentary | Plain-language summary with analogy engine |

**Key differentiator**: No competitor combines daily market data with plain-language explanations. Every market move should have a "why" in plain language. "TAIEX rose 1.2% → 因為台積電財報優於預期，帶動半導體類股上漲."

### 4. Mobile Responsiveness Considerations

- **Market indices**: 2x2 grid on desktop → 2x2 grid on mobile (same layout)
- **Top movers**: Single-column stack on mobile
- **Sector performance**: Horizontal scroll on mobile (if too many sectors)
- **Key events**: Single-column, full-width cards on mobile

### 5. Ten-Second Test Implications

**The daily pulse page IS a ten-second test for the product's daily value.** A user should be able to:
1. Read the hero summary (3 seconds)
2. Glance at market indices (3 seconds)
3. Understand: "Today's market moved because of X" (4 seconds)

**If the user sees a wall of numbers without context, the test fails.**

### Design Spec Summary

```markdown
Page: 📰 市場日報
├── Hero: "2026年6月17日 — 台股上漲1.2%，半導體領漲" (≤ 60 chars)
├── Market Indices (4 cards, 2x2 grid)
│   ├── 加權指數 23,456 ↑1.2%
│   ├── 櫃買指數 234.5 ↑0.8%
│   ├── 費半指數 5,678 ↑2.1%
│   └── 道瓊指數 42,123 ↓0.3%
├── Top Movers (card-based, 5 gainers + 5 losers)
│   └── Per card: name, price, change%, one-line reason
├── Sector Performance (horizontal bar chart or mini heatmap)
└── Key Events (3-5 event cards with plain-language explanation)
```

---

## Design Direction for C50 (Learning Progress Tracker)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C50 is a new top-level page or a section within the C47 Education Academy page. It does not touch the business card page.

**Strategic impact**: HIGH — Khan Academy's mastery system proves that progress tracking dramatically increases learning engagement. Users who see their progress are more likely to continue learning. This is the "gamification" layer that makes C47 sticky.

**Key question**: Is C50 a standalone page or part of C47?

**Recommendation**: Part of C47 Education Academy. The progress tracker is a natural companion to the lesson system. Users see lessons → complete lessons → track progress. Separating them would create a disjointed experience.

### 2. Design Consistency with PPT-Style Principle

**Page structure** (within C47 Academy page):
```
Section: 📊 學習進度
├── Overall progress bar: "已完成 3/15 堂課 (20%)"
├── Concept mastery grid (per concept: name, status, score)
│   ├── ✅ 營收 — 已掌握
│   ├── ✅ 獲利 — 已掌握
│   ├── 🔄 ROE — 學習中
│   ├── ⬜ P/E — 未開始
│   └── ⬜ 股利 — 未開始
└── Achievement badges (optional, Phase 2)
    ├── 🎓 第一堂課 (complete first lesson)
    ├── 📚 五堂課達人 (complete 5 lessons)
    └── 🏆 投資新手 (complete all beginner lessons)
```

**Card design**: Standard info card (blue border) with `📊` icon. Each concept is a row in the grid, not a separate card. This keeps the layout compact.

**Progress visualization**: Use Streamlit's `st.progress()` for the overall bar. Per-concept status uses emoji indicators (✅🔄⬜) — color-blind accessible, works on all screens.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Khan Academy** | Mastery system (3 levels: started → familiar → mastered) | 3-level system: 未開始 → 學習中 → 已掌握 |
| **Zerodha** | Module completion tracking | Per-lesson completion with quiz score |
| **Finimize** | Streak tracking (daily engagement) | Optional: daily learning streak (Phase 2) |

**Key differentiator**: Khan Academy's mastery system is for general education. Stock Explorer's progress tracker is tied to **real stock data**. When you "master" ROE, you've not only read the lesson — you've seen how ROE applies to 台積電, 鴻海, and 聯詠. This connection between concept and real data is unique.

### 4. Mobile Responsiveness Considerations

- **Progress bar**: Full-width on mobile
- **Concept grid**: Single-column list on mobile (each concept = one row)
- **Achievement badges**: 3-column grid on desktop → 2-column on mobile
- **Avoid**: Dense tables with many columns

### 5. Ten-Second Test Implications

**The progress tracker is NOT part of the ten-second test.** It's a "return visit" feature — users see it when they come back to the academy.

**However**: The progress visualization should be immediately understandable. A user should glance at the progress bar and know "I'm 20% done" without reading any text.

### Design Spec Summary

```markdown
Section: 📊 學習進度 (within C47 Academy page)
├── Overall: st.progress(0.2) + "已完成 3/15 堂課 (20%)"
├── Concept Grid (single-column list)
│   ├── ✅ 營收 — 已掌握 (quiz score: 100%)
│   ├── ✅ 獲利 — 已掌握 (quiz score: 80%)
│   ├── 🔄 ROE — 學習中
│   ├── ⬜ P/E — 未開始
│   └── ⬜ 股利 — 未開始
└── Achievements (Phase 2, optional)
    └── Badge grid with earned/unearned states
```

---

## Design Direction for C51 (Sector Heatmap)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C51 is a new top-level page accessible from the sidebar. It does not touch the business card page.

**Strategic impact**: MEDIUM-HIGH — Sector heatmaps are a standard feature in financial platforms (StockEdge, Moomoo). They provide a visual overview of market performance by sector, which helps beginners understand "what's happening in the market" without reading numbers. This complements C49 (Daily Market Pulse) — C49 is text-based daily summary, C51 is visual sector overview.

**Key question**: Is C51 a standalone page or part of C49?

**Recommendation**: Standalone page. C49 is a daily narrative ("today the market did X"), C51 is a visual tool ("see how all sectors perform"). They serve different purposes. C51 can be linked from C49 ("查看類股熱力圖 →").

### 2. Design Consistency with PPT-Style Principle

**Page structure** (PPT-style: one key point per "slide"):
```
Slide 1: "類股表現一覽" (hero text, ≤ 40 chars)
Slide 2: Sector heatmap (the main visual, 60%+ of page area)
Slide 3: Top performing sectors (3 cards)
Slide 4: Worst performing sectors (3 cards)
```

**Heatmap design**:
- **Layout**: Grid-based heatmap (not a geographic map). Each sector = one cell.
- **Color**: Green (positive) to Red (negative), with intensity proportional to change %.
- **Labels**: Sector name + change % in each cell.
- **Size**: Cell size proportional to market cap (larger sector = larger cell).
- **Interactivity**: Click a sector → navigate to sector detail page or filtered stock list.

**Color compliance**: The green/red color coding is already approved for direction indication (not buy/sell). Heatmap cells use the same color logic.

**Card design**: Top/worst sector cards use standard info card style (blue border) with `📈` / `📉` icons.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **StockEdge** | Sector heatmap with color-coded cells | Same grid-based approach, but with plain-language sector names |
| **Moomoo** | Sector performance with AI commentary | Add plain-language explanation for top movers |
| **TradingView** | Sector treemap | Grid heatmap is simpler and more readable for beginners |

**Key differentiator**: StockEdge and Moomoo show sector performance but don't explain WHY in plain language. Stock Explorer should add a one-line explanation for the top 3 movers: "半導體類股上漲3.2% → 因為台積電財報優於預期."

### 4. Mobile Responsiveness Considerations

- **Heatmap grid**: 4-column on desktop → 3-column on mobile → 2-column on small mobile
- **Cell labels**: Abbreviate sector names on small screens (e.g., "半導體" instead="半導體類股")
- **Top/bottom sectors**: Single-column stack on mobile
- **Avoid**: Horizontal scrolling. The heatmap should fit within the viewport.

### 5. Ten-Second Test Implications

**The heatmap IS a visual ten-second test for market overview.** A user should be able to:
1. Glance at the heatmap (5 seconds)
2. Identify: "Green sectors are up, red sectors are down" (3 seconds)
3. Understand: "Today, semiconductors are leading" (2 seconds)

**If the user can't identify the market trend in 10 seconds, the heatmap fails.**

### Design Spec Summary

```markdown
Page: 🗺️ 類股熱力圖
├── Hero: "類股表現一覽 — 2026年6月17日" (≤ 40 chars)
├── Sector Heatmap (main visual, 60%+ of page)
│   ├── Grid layout (4-col desktop, 3-col tablet, 2-col mobile)
│   ├── Each cell: sector name + change % + color intensity
│   └── Click → sector detail or filtered stock list
├── Top 3 Sectors (card-based)
│   └── Per card: sector name, change%, one-line reason
├── Bottom 3 Sectors (card-based)
│   └── Per card: sector name, change%, one-line reason
└── Link to C49 Daily Market Pulse
```

---

## Design Direction for C52 (Quiz Mode)

### 1. UX Impact on Business Card Page

**Risk: 🟢 NONE** — C52 is a new page or a section within C47 Education Academy. It does not touch the business card page.

**Strategic impact**: HIGH — Khan Academy's exercises and Zerodha's quizzes prove that interactive assessment is the missing piece in financial education. Reading a lesson is passive; taking a quiz is active. Quizzes also provide the "mastery signal" for C50 (Progress Tracker).

**Key question**: Is C52 standalone or part of C47?

**Recommendation**: Integrated into C47 Academy. Each lesson ends with a quiz (as specified in the C47 design). A separate "Quiz Mode" page can be a practice test that aggregates questions from all completed lessons.

### 2. Design Consistency with PPT-Style Principle

**Quiz interaction** (within lesson page):
```
Lesson: 什麼是營收？
├── Concept explanation (analogy + plain language)
├── Real TW stock example
├── Key takeaway
└── Quiz: "以下哪個是營收？"
    ├── A. 公司賺到的錢 ← ✅ Correct
    ├── B. 公司花掉的錢
    ├── C. 公司的資產
    └── D. 公司的負債
    [提交答案] → Show result + explanation
```

**Quiz card design**: Standard info card (blue border) with `❓` icon. Use `st.radio()` for multiple choice (native Streamlit, mobile-friendly).

**Result feedback**:
- ✅ Correct: Green success card (`#27AE60` border, `#EAFAF1` background) with `🎉` icon
- ❌ Incorrect: Orange tip card (`#F39C12` border, `#FFF8F0` background) with explanation of why the answer is wrong

**Quiz Mode page** (aggregated practice):
- 10 random questions from completed lessons
- Score at the end
- "Review wrong answers" option
- Progress saved to C50 tracker

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Khan Academy** | Exercise with instant feedback + hints | Same pattern, but with TW stock examples |
| **Zerodha** | Module-end quiz with score | Per-lesson quiz with mastery tracking |
| **Finimize** | Daily quiz (engagement loop) | Optional: daily quiz question (Phase 2) |

**Key differentiator**: Khan Academy's quizzes are generic. Stock Explorer's quizzes use **real TW stock data**. "台積電2024年營收是多少？" is more engaging than "Company X's revenue is $Y because..."

### 4. Mobile Responsiveness Considerations

- **Quiz options**: Full-width radio buttons on mobile (easy to tap)
- **Submit button**: Full-width, ≥ 44px height
- **Result feedback**: Full-width card below the question
- **Avoid**: Side-by-side layout for quiz options

### 5. Ten-Second Test Implications

**Quizzes are NOT part of the ten-second test.** They're an active engagement feature for users who are already in learning mode.

**However**: The quiz should be immediately understandable. A user should see the question and know what to do without instructions.

### Design Spec Summary

```markdown
Section: ❓ 隨堂測驗 (within C47 Academy, at end of each lesson)
├── Quiz Card (blue border, ❓ icon)
│   ├── Question (≤ 80 chars)
│   ├── 4 options (st.radio, full-width)
│   └── Submit button (full-width)
├── Result Feedback
│   ├── ✅ Correct: Green success card + explanation
│   └── ❌ Incorrect: Orange tip card + correct answer + explanation
└── Navigation: "下一堂課" / "重新測驗"
```

---

## Design Direction for C53 (Social Sharing)

### 1. UX Impact on Business Card Page

**Risk: 🟡 MEDIUM** — C53 adds a share button to the business card page. This is a UI element, not a full section, so the overload risk is low. However, it introduces a new interaction pattern (generating a shareable image/card) that needs careful placement.

**Strategic impact**: MEDIUM — TradingView's Ideas feed and Plotch.ai's shareable cards prove that social sharing drives organic growth. Users share interesting analyses with friends, which brings new users to the platform. This is a **growth feature**, not a core UX feature.

**Key question**: What is shared?
- Option A: A shareable image of the company's key metrics (like TradingView's chart screenshots)
- Option B: A link back to the Stock Explorer page (simple URL sharing)
- Option C: A generated "analysis card" image with key facts (like Plotch.ai)

**Recommendation**: Option C — a generated "analysis card" image. This is the most visually engaging and shareable format. The card would include: company name, one-liner, 3 key metrics, snowflake mini-chart, and "via 股識 Stock Explorer" branding.

### 2. Design Consistency with PPT-Style Principle

**Placement**: Business card page, TOP-RIGHT corner of the header area (next to the company name/price). This is consistent with social sharing patterns on TradingView and Twitter/X.

**Share button design**:
- **Icon**: `📤` (share icon) — universally understood
- **Style**: Small, secondary button (not primary CTA). Use Streamlit's `st.button()` with `use_container_width=False`.
- **Label**: `分享` (2 chars, minimal)

**Shareable card design** (generated image):
- **Format**: 1200x630px (Twitter/X card ratio)
- **Content**: Company name + one-liner + 3 key metrics + mini snowflake + branding
- **Style**: Match the PPT-style design system (same colors, same card style)
- **Branding**: "via 股識 Stock Explorer" at bottom-right

**Interaction flow**:
1. User clicks `分享` button
2. System generates a shareable card image (using Pillow or Plotly)
3. User sees a preview modal with download/share options
4. User can download the image or copy a link

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **TradingView** | Chart screenshot sharing | Company card image sharing (not just charts) |
| **Plotch.ai** | Shareable analysis cards | Same concept, but with TW stock data |
| **Stake** | Social feed with shared analysis | No feed needed — just the share button |

**Key differentiator**: TradingView shares charts. Stock Explorer would share **company stories** — a visual card that tells the company's story in one glance. This is more beginner-friendly than a chart screenshot.

### 4. Mobile Responsiveness Considerations

- **Share button**: ≥ 44px touch target on mobile
- **Preview modal**: Full-width on mobile, scrollable
- **Download button**: Full-width on mobile
- **Avoid**: Small text in the shareable image that's unreadable on mobile

### 5. Ten-Second Test Implications

**Social sharing is NOT part of the ten-second test.** It's a secondary action for users who want to share what they've learned.

**However**: The shareable card itself IS a ten-second test for the company's story. If someone sees the shared image and can't understand the company in 10 seconds, the card design has failed.

### Design Spec Summary

```markdown
UI Element: 📤 分享 button (top-right of business card header)
├── Button: Small, secondary, "📤 分享"
├── On click: Generate shareable card image
│   ├── Size: 1200x630px
│   ├── Content: company name + one-liner + 3 metrics + mini snowflake
│   ├── Branding: "via 股識 Stock Explorer"
│   └── Style: PPT-style design system colors
└── Preview modal: Image preview + download button + copy link
```

---

## Design Direction for C54 (Video/Audio Explanation)

### 1. UX Impact on Business Card Page

**Risk: 🟡 MEDIUM** — C54 adds a media player to the business card page or lesson page. This is a new media type that needs careful placement to avoid page overload.

**Strategic impact**: MEDIUM — Khan Academy's video lessons are the gold standard for financial education. However, video/audio content is expensive to produce and maintain. For a small team, this is a long-term feature.

**Key question**: Where does video/audio live?
- Option A: On the business card page (e.g., "Watch a 2-minute video about this company")
- Option B: On the C47 Academy lesson pages (e.g., "Listen to the audio explanation")
- Option C: Both

**Recommendation**: Option B — on the C47 Academy lesson pages. Video/audio is a natural companion to lessons, not to the business card page. The business card page is for data and analysis; the academy is for education.

### 2. Design Consistency with PPT-Style Principle

**Placement**: Within C47 Academy lesson pages, BELOW the text explanation but ABOVE the quiz. The flow: read the lesson → watch/listen to the video/audio → take the quiz.

**Media player design**:
- **Video**: Use Streamlit's `st.video()` (supports YouTube embeds or direct video files)
- **Audio**: Use Streamlit's `st.audio()` (supports audio files)
- **Wrapper**: Standard info card (blue border) with `🎬` (video) or `🎧` (audio) icon
- **Duration**: Display prominently — "🎬 2分鐘影片" or "🎧 3分鐘音訊"

**Content guidelines**:
- Video: 2-3 minutes max, covers one concept, uses real TW stock examples
- Audio: 3-5 minutes max, podcast-style explanation
- Both: Use the same analogy engine for consistency

**Fallback**: If video/audio is not available for a lesson, show a text-only version. Never show a broken media player.

### 3. Competitor Design Patterns to Follow

| Competitor | Pattern | Stock Explorer Adaptation |
|------------|---------|--------------------------|
| **Khan Academy** | Video lessons with subtitles | Short videos (2-3 min) with TW stock examples |
| **Sensical** | Audio explanations (podcast-style) | Audio versions of lessons for on-the-go learning |
| **Investopedia** | Video + text combined | Video above text, or text above video (user's choice) |

**Key differentiator**: Khan Academy's videos are generic. Stock Explorer's videos would use **real TW stock data** and the analogy engine. "Here's how ROE works → Let me show you 台積電's actual ROE → See how it translates to real money."

### 4. Mobile Responsiveness Considerations

- **Video player**: Full-width on mobile (Streamlit's `st.video()` is responsive)
- **Audio player**: Full-width on mobile (Streamlit's `st.audio()` is responsive)
- **Autoplay**: NEVER autoplay on mobile (data usage, user experience)
- **Subtitles**: Always provide text transcript below the video (accessibility + mobile)

### 5. Ten-Second Test Implications

**Video/audio is NOT part of the ten-second test.** It's a "deep engagement" feature for users who want to learn more.

**However**: The video/audio card should be immediately understandable. A user should see the `🎬` icon and duration and know "this is a 2-minute video about this concept."

### Design Spec Summary

```markdown
Section: 🎬 影音解釋 (within C47 Academy lesson page)
├── Media Card (blue border, 🎬 or 🎧 icon)
│   ├── Title: "用2分鐘了解營收的概念"
│   ├── Duration badge: "🎬 2分鐘"
│   ├── Media player (st.video() or st.audio())
│   │   └── Full-width, responsive, no autoplay
│   └── Text transcript (collapsible, below player)
└── Fallback: If no media available, show text-only explanation
```

---

## Design Risks & Cross-Cutting Concerns

### 1. Page Overload (P1 — Critical)

**Current state**: The business card page has 13 sections. Adding C48 (replacing C37) keeps it at 13. Adding C53 (share button) adds a UI element but not a section.

**Risk**: If the team adds C48 as a new section alongside C37 (instead of replacing), the page goes to 14 sections. This is unacceptable.

**Mitigation**:
- C48 **replaces** C37, not added alongside it
- C53 is a button, not a section
- All other features (C49-C54) are on separate pages

### 2. Design Inconsistency (P1 — Critical)

**Current state**: D-016 (C37 missing hero card style), D-020 (C39 missing color coding), D-021 (C43 missing plain-language) indicate a pattern of implementation not following design specs.

**Risk**: New features (C48-C54) will be implemented without following the design system, compounding the inconsistency.

**Mitigation**:
- Create `docs/design/design_system.md` BEFORE implementing any new features (this has been recommended since Round 9 but still hasn't been done)
- Define all card types, colors, and spacing in the design system
- Review each new feature against the design system before approving

### 3. Mobile Responsiveness (P1 — Important)

**Current state**: Multi-column layouts don't stack gracefully on mobile. Only basic padding/font-size adjustments exist.

**Risk**: New features (especially C51 heatmap, C49 daily pulse) may break on mobile.

**Mitigation**:
- Design all new features mobile-first
- Use Streamlit's native components (responsive by default)
- Test on 375px width before approving

### 4. Content Quality (P2 — Optimization)

**Current state**: C37 has curated templates for top 20 stocks. C43 has sophisticated scoring. But auto-generated content can feel generic.

**Risk**: C48 (Story Card), C49 (Daily Pulse), and C54 (Video/Audio) all require high-quality content. Auto-generated stories may feel robotic.

**Mitigation**:
- C48: Curated story templates for top 20 stocks, auto-generated for others
- C49: Rule-based daily summary with curated templates for major market events
- C54: Start with text-only lessons, add video/audio in Phase 2

### 5. Technical Feasibility (P2 — Optimization)

**Current state**: Streamlit has limitations for image generation (C53) and media playback (C54).

**Risk**:
- C53 (Social Sharing): Generating shareable images requires Pillow or Plotly. This is feasible but adds complexity.
- C54 (Video/Audio): Hosting video/audio files requires storage and bandwidth. This may be expensive for a small team.

**Mitigation**:
- C53: Use Plotly to generate chart images (already a dependency). Use Pillow for text overlay.
- C54: Start with text-only. Use YouTube embeds for video (free hosting). Use hosted audio files for audio.

---

## Proposed Design Directions

### Direction A: "Story First" — Prioritize C48 + C49 + C51

**Goal**: Make Stock Explorer the best **visual story platform** for TW stocks.

**Features to implement**:
1. **C48 (Company Story Card)** — Replace C37 with a visual story card. This is the single most impactful change.
2. **C49 (Daily Market Pulse)** — Create the daily engagement loop. This drives retention.
3. **C51 (Sector Heatmap)** — Provide visual market overview. This complements C49.

**Rationale**:
- C48 directly addresses the ten-second test (the core design principle)
- C49 creates a daily engagement loop (the #1 retention driver in competitor research)
- C51 provides visual market context (table stakes per competitor research)
- All three are **separate pages or replace existing sections** — no page overload risk
- Total effort: ~2-3 weeks for a small team

**Design focus**: Visual-first, card-based, plain-language. Every feature must pass the ten-second test.

**Grade projection**: A (if implemented well)

---

### Direction B: "Education First" — Prioritize C50 + C52 + C54

**Goal**: Make Stock Explorer the best **learning platform** for TW investors.

**Features to implement**:
1. **C50 (Learning Progress Tracker)** — Add progress tracking to C47 Academy. This makes learning sticky.
2. **C52 (Quiz Mode)** — Add interactive assessment to C47 Academy. This validates learning.
3. **C54 (Video/Audio Explanation)** — Add media to C47 Academy lessons. This improves engagement.

**Rationale**:
- C50 + C52 transform C47 from a "lesson library" to a "learning system"
- Khan Academy proves that progress tracking + quizzes = engagement
- C54 adds accessibility (audio for on-the-go learning, video for visual learners)
- All three are within the C47 Academy page — no business card page impact
- Total effort: ~2-3 weeks for a small team

**Design focus**: Interactive, gamified, accessible. Every feature must work on mobile.

**Grade projection**: A (if implemented well)

---

### Direction C: "Growth First" — Prioritize C53 + C49 + C51

**Goal**: Maximize **organic growth** through social sharing and daily engagement.

**Features to implement**:
1. **C53 (Social Sharing)** — Add share button to business card page. This drives organic growth.
2. **C49 (Daily Market Pulse)** — Create daily content. This drives daily visits.
3. **C51 (Sector Heatmap)** — Create visual content worth sharing. This drives social engagement.

**Rationale**:
- C53 enables viral growth (users share company cards with friends)
- C49 gives users a reason to come back daily
- C51 creates visually shareable content
- Together, these three create a growth engine: visit daily → see interesting content → share with friends → new users visit
- Total effort: ~2-3 weeks for a small team

**Design focus**: Shareable, visual, daily. Every feature must be "share-worthy."

**Grade projection**: A- (growth features don't directly improve core UX)

---

## Recommendation

### Recommended Direction: **Direction A ("Story First") + Selective Elements from B**

**Primary**: Implement C48 (Company Story Card) + C49 (Daily Market Pulse) + C51 (Sector Heatmap)

**Secondary**: Implement C52 (Quiz Mode) as part of the existing C47 Academy (5 pilot lessons with quiz)

**Defer**: C50 (Progress Tracker), C53 (Social Sharing), C54 (Video/Audio) to Sprint 5+

**Rationale**:

1. **C48 is the highest-impact feature** — It replaces C37 with a visual story card that directly addresses the ten-second test. The current C37 is text-heavy and uses the wrong card style (D-016). Replacing it with C48 fixes both issues.

2. **C49 is the highest-retention feature** — Daily engagement loops are the #1 driver of user retention in competitor research. Finimize's newsletter and StockEdge's daily analysis prove this. Without C49, Stock Explorer is a "one-visit" tool.

3. **C51 is table stakes** — Every major competitor has a sector heatmap. It's expected by users who are familiar with StockEdge or Moomoo. Without it, Stock Explorer feels incomplete.

4. **C52 (Quiz) is a natural companion to C47** — The 5 pilot lessons should include quiz questions. This is low-effort (add `st.radio()` to existing lessons) and high-impact (validates learning).

5. **C50, C53, C54 can wait** — These are "nice-to-have" features that don't address core UX gaps. Progress tracking is only valuable after users have completed multiple lessons. Social sharing is only valuable after there's something worth sharing. Video/audio is expensive to produce and maintain.

### Implementation Priority

| Sprint | Feature | Effort | Impact |
|--------|---------|--------|--------|
| Sprint 3 | C48 (Story Card, replaces C37) | 1 week | HIGH — ten-second test |
| Sprint 3 | C52 (Quiz for C47 lessons) | 3 days | MEDIUM — learning validation |
| Sprint 4 | C49 (Daily Market Pulse) | 1 week | HIGH — retention |
| Sprint 4 | C51 (Sector Heatmap) | 1 week | MEDIUM — table stakes |
| Sprint 5+ | C50 (Progress Tracker) | 3 days | LOW — depends on C47 adoption |
| Sprint 5+ | C53 (Social Sharing) | 1 week | MEDIUM — growth |
| Sprint 5+ | C54 (Video/Audio) | 2 weeks | LOW — expensive to produce |

### Design System Updates Needed

Before implementing any new features, the following design system updates are required:

1. **Create `docs/design/design_system.md`** — Document all card types, colors, spacing, and interaction patterns. This has been recommended since Round 9 and is still not done.

2. **Add new card types**:
   - Story card (orange/amber border, for C48)
   - Success card (green border, for quiz correct answers)
   - Share card (for C53 shareable image template)

3. **Define the "business card page architecture"**:
   - Above the fold: C48 (Story Card) + C43 (Snowflake) = ten-second test
   - Below the fold: metrics, charts, dividend, news
   - Tabs: C36 (Revenue Tree) + C46 (Moat)
   - Collapsible: C44 (Risk)

4. **Define the "daily content" design pattern** (for C49):
   - Hero summary (≤ 60 chars)
   - 4 index cards (2x2 grid)
   - Top movers (card-based)
   - Plain-language explanation for each data point

---

*Design Review completed. The key message: C48 replaces C37 (don't add alongside), C49 creates the daily engagement loop, C51 is table stakes. All three are safe (no page overload). C52 (Quiz) is a natural add-on to C47. Defer C50, C53, C54 to Sprint 5+. The design system must be created BEFORE implementing any new features to avoid compounding the inconsistency issues (D-016, D-020, D-021).*
