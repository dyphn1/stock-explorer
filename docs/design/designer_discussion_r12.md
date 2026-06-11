# 2026-06-18 Design Review — Round 12 Discussion

> **Author**: Design Reviewer
> **Date**: 2026-06-18
> **Context**: Round 12 discussion — evaluating UX impact of 8 new feature proposals (C55-C62) from Round 12 competitor research, assessing design feasibility, and proposing design directions for team discussion.
> **Current Design Grade**: A (Round 12 review)
> **Design Principle**: "Ten-second test" — a beginner can restate the core concept within 10 seconds.
> **Design System**: PPT-style (one key point per page, images lead/text supports, minimal walls of text)

---

## Table of Contents

1. [UX Impact Analysis (C55-C62)](#ux-impact-analysis)
2. [Design Direction A: "Guided Learning Path"](#design-direction-a-guided-learning-path)
3. [Design Direction B: "Personal Learning Companion"](#design-direction-b-personal-learning-companion)
4. [Design Direction C: "Modular Education Layer"](#design-direction-c-modular-education-layer)
5. [Recommendation](#recommendation)
6. [UX Risks & Mitigations](#ux-risks--mitigations)
7. [Design System Impact](#design-system-impact)

---

## UX Impact Analysis

### C55: Investment Diary (投資日記) — Personal Reflection Journal

**Priority**: P2 | **Effort**: 10-14h

**UX Benefit**: ★★★★★ (Transformative)
- Transforms Stock Explorer from a **lookup tool** into a **personal learning platform**
- Creates emotional attachment — users return to see their own thoughts
- "Historian of self" positioning — unique among all TW competitors
- Encourages reflective learning, which is proven to improve retention

**Design Requirements**:
- **New page**: "📝 投資日記" accessible from sidebar — NOT on the business card page (avoids page overload)
- **Card on business card page**: A small "📝 我的筆記" expander at the bottom of each company page (before C41 Read Next) with a single text input and "儲存" button
- **Diary page layout**: Chronological list of entries, each showing: company name + ticker (linked), date, note text, and "當時 vs 現在" comparison (if data available)
- **Card type**: New `_diary_card()` — warm green border (`#27AE60`) with notebook icon (`📝`) to signal "personal" content
- **Empty state**: "還沒有寫任何筆記。瀏覽任何公司頁面，點擊「新增筆記」開始記錄你的投資想法。"

**Risks**:
- **Data persistence**: Session state only means notes are lost on refresh. This is a significant UX risk — users will lose their writing. Mitigation: Add local file export/import (JSON) as a minimum. Full persistence requires D22 (persistence layer) which is deferred.
- **Low discoverability**: If the diary entry point is buried at the bottom of the business card page, users won't find it. Mitigation: Add a prominent "📝" button in the sidebar when the user has 0 entries.
- **Content quality**: Users may write nothing meaningful. Mitigation: Provide prompts — "你為什麼對這家公司感興趣？" / "你覺得這家公司的風險是什麼？"

**PPT-Style Compliance**: ✅ The diary page follows PPT style — one entry per card, one key thought per entry. The inline note input on the business card page is a single text field, not a wall of text.

---

### C56: Explain This Metric (解釋這個指標) — Interactive Financial Concept Explainer

**Priority**: P1 | **Effort**: 12-16h

**UX Benefit**: ★★★★★ (Critical)
- Directly addresses the **ten-second test** — the #1 design principle
- Transforms every data point into a **learning opportunity**
- Multiple competitors prove demand (Magnify.money, Robinhood, 永豐金證券)
- Closes the gap between "seeing a number" and "understanding what it means"

**Design Requirements**:
- **Inline "❓" buttons**: Next to every metric on the business card page (ROE, P/E, P/B, gross margin, revenue growth, dividend yield, debt ratio, EPS, free cash flow, institutional ownership)
- **Interaction**: Clicking "❓" opens an `st.expander` below the metric with:
  - **One-line definition** (≤ 30 Chinese characters)
  - **Visual**: Mini Plotly chart showing the metric's historical trend (sparkline style, ≤ 100px height)
  - **Analogy**: Real-world comparison from the existing analogy engine
  - **"為什麼重要"**: One sentence explaining why this metric matters
  - **"注意什麼"**: One sentence on what to watch for
- **Total content per explanation**: ≤ 150 characters of text + 1 chart. This is critical for PPT-style compliance.
- **Card style**: Use the existing `_info_card()` (blue border) with `❓` icon — no new card type needed
- **Data source**: `src/data/metric_explanations.yaml` with pre-written templates for the 10 priority metrics

**Risks**:
- **Page bloat**: Adding 10 "❓" buttons and expanders to the business card page could significantly increase page length. Mitigation: Only show "❓" buttons for the top 5 most important metrics initially. Use progressive disclosure — the expander only loads content when clicked.
- **Content creation effort**: Writing 10 metric explanations with analogies, charts, and "why it matters" is a significant content creation task. Mitigation: Start with 5 metrics (ROE, P/E, P/B, gross margin, dividend yield) and expand in future sprints.
- **Mobile responsiveness**: Sparkline charts may be too small on mobile. Mitigation: Hide charts on mobile (< 768px), show only text explanation.

**PPT-Style Compliance**: ✅ Each explanation is one key point (the metric definition) with a visual supporting it. The expander pattern ensures the page stays clean until the user actively seeks more information.

---

### C57: Compare Concepts (概念比較) — Financial Concept Comparison Tool

**Priority**: P2 | **Effort**: 10-14h

**UX Benefit**: ★★★★☆ (High)
- Helps beginners understand that financial metrics are **tools, not answers**
- Unique educational differentiator — no TW competitor has this
- Magnify.money proves demand
- Addresses a common beginner confusion: "What's the difference between P/E and P/B?"

**Design Requirements**:
- **New page**: "📊 概念比較" accessible from sidebar — NOT on the business card page
- **Layout**: Two-column selector at top (dropdown A vs dropdown B), then side-by-side comparison below
- **Comparison content** (one dimension at a time, tab-switchable):
  - **定義**: One-line definition of each concept (≤ 25 chars each)
  - **公式**: Simple formula with plain-language variable names
  - **什麼時候用**: When to use each metric (one sentence each)
  - **實際範例**: Real TW stock example showing both metrics side-by-side
  - **哪個更適合這家公司?**: One-line analysis for the currently-viewed stock
- **Card style**: Use `st.columns(2)` with blue (`#3498DB`) for Concept A and green (`#27AE60`) for Concept B
- **Pre-written content**: 10 most common concept pairs (P/E vs P/B, ROE vs ROA, dividend yield vs payout ratio, etc.)

**Risks**:
- **PPT-style violation risk**: Side-by-side comparison is inherently data-dense. Mitigation: Use tabs to show one dimension at a time (定義 → 公式 → 什麼時候用 → 實際範例). Each tab shows ONE key point.
- **Content generation**: Writing 10 concept pair comparisons is a significant content effort. Mitigation: Start with 5 pairs, expand over time.
- **Relevance to current stock**: The "哪個更適合這家公司?" section requires context about what the user is currently viewing. This requires passing state between pages, which Streamlit makes challenging. Mitigation: Show a generic example instead of stock-specific analysis.

**PPT-Style Compliance**: ⚠️ Requires careful design. The tab-based approach (one dimension per tab) maintains PPT style. The two-column layout within each tab should be simple: one key point per column.

---

### C58: Beginner Onboarding Flow (新手引導) — Guided First Experience

**Priority**: P1 | **Effort**: 14-20h

**UX Benefit**: ★★★★★ (Critical)
- Addresses the **#1 UX complaint**: "I don't know where to start"
- Directly impacts **beginner retention** — without onboarding, users bounce before discovering value
- 玉山證券's "Beginner Village" and Robinhood's "First Stock" prove demand
- Makes ALL other features more effective by teaching users how to navigate

**Design Requirements**:
- **Trigger**: First-time user detection via session state flag `onboarding_complete`
- **Modal overlay**: 5-step guided tour with progress indicator (Step X of 5)
- **Step content** (one key point per step, ≤ 50 characters each):
  1. **歡迎來到股識！** — "我們幫你認識公司，而不是報明牌" + highlight the search bar
  2. **搜尋一家公司** — "輸入股票代號或公司名稱" + highlight the search input
  3. **閱讀公司名片** — "先看重點摘要，再深入了解" + highlight C37 Key Takeaways
  4. **探索事件儀表板** — "了解公司最近發生了什麼事" + highlight the event dashboard tab
  5. **加入觀察清單** — "追蹤你有興趣的公司" + highlight the watchlist button
- **Visual design**: Use a centered modal (max-width: 600px) with a large illustration/icon per step, one sentence of explanation, and a "下一步" button. Progress dots at the bottom.
- **Completion**: After step 5, show "🎉 完成引導！建議你從這三家公司開始探索：台積電、鴻海、富邦媒" with clickable links
- **Replay**: Add a "❓ 重新觀看引導" button in the sidebar
- **Skip option**: "跳過引導" link at the bottom of each step

**Risks**:
- **Streamlit limitations**: Streamlit doesn't natively support step-by-step UI highlighting (tooltips on specific elements). Mitigation: Use a modal with screenshots/illustrations of each UI area rather than actual element highlighting. This is less immersive but achievable within Streamlit.
- **One-time experience**: Users only see onboarding once. If they don't retain the information, it's wasted. Mitigation: Add contextual tooltips throughout the app that reinforce onboarding concepts (e.g., a small "💡" next to the search bar that says "輸入股票代號或公司名稱").
- **Mobile responsiveness**: Modal overlays on mobile can be problematic. Mitigation: Use a full-screen overlay on mobile instead of a centered modal.

**PPT-Style Compliance**: ✅ Perfect alignment — one key point per step, visual-first (illustration + one sentence), progressive disclosure (5 steps, one at a time).

---

### C59: AI Q&A Chatbot (問問股識) — Natural Language Stock Questions

**Priority**: P2 | **Effort**: 16-24h

**UX Benefit**: ★★★★☆ (High)
- Most **natural interface** for beginners — they ask questions in their own words
- 元大證券's chatbot and Finimize's "Ask Finimize" prove demand
- Complements the analogy engine — instead of pre-written explanations, users get answers to their specific questions
- High engagement potential — chat interfaces encourage exploration

**Design Requirements**:
- **New page**: "💬 問問股識" accessible from sidebar
- **Chat interface**: Message history with user questions (right-aligned, blue bubbles) and bot responses (left-aligned, gray bubbles)
- **Input**: Text input at the bottom with placeholder "問我任何關於股票的問題，例如：台積電最近表現如何？"
- **Suggested questions**: 3 clickable suggestion chips below the input (rotating based on context):
  - "這家公司最近發生了什麼事？"
  - "這家公司的獲利能力如何？"
  - "這家公司的主要風險是什麼？"
- **Response format**: Plain-language answer (≤ 100 characters) + optional mini-chart + "延伸閱讀" link to the relevant page section
- **Follow-up questions**: After each response, suggest 2-3 follow-up questions as clickable chips
- **Card style**: Chat bubbles use the existing color system (user: `#3498DB` blue, bot: `#F8F9FA` gray)
- **Pattern matching**: NOT a full LLM — use regex/pattern matching to map questions to pre-built response templates (revenue → show revenue chart, risk → show C44 analysis, dividend → show dividend data)

**Risks**:
- **Scope creep**: This is the highest-effort feature (16-24h) and could easily expand beyond scope. Mitigation: Strictly limit to pattern-matching with 10 pre-built question templates. No LLM integration in MVP.
- **Uncanny valley**: If the chatbot can't answer a question, the user feels let down. Mitigation: Always provide a helpful fallback — "我目前只能回答關於公司基本資料、財務數據、風險分析的問題。試試問：'這家公司最近發生了什麼事？'"
- **Historian positioning guardrail**: The chatbot must ONLY answer historical/factual questions, never predictive ones. "台積電會漲嗎？" → "我無法預測股價，但我可以告訴你台積電過去的表現..."
- **PPT-style compliance**: A chat interface is inherently NOT PPT-style (it's conversational, not visual-first). Mitigation: Each bot response should include a visual element (mini-chart, icon, or emoji) alongside the text.

**PPT-Style Compliance**: ⚠️ The chat interface itself is a departure from PPT style. However, each individual response can follow PPT principles (one key point + visual). The overall page layout should be clean: chat history in the center, suggestions at the bottom.

---

### C60: Concept Mastery Badges (學習成就) — Gamified Learning Achievement

**Priority**: P2 | **Effort**: 8-12h

**UX Benefit**: ★★★★☆ (High)
- Creates a **positive feedback loop** — learning → badges → sharing → more learning
- Robinhood's "Learn → Earn" and Khan Academy badges prove demand
- Drives **engagement and retention** — users return to earn more badges
- Connects to C53 (Social Sharing) — badges are shareable achievements

**Design Requirements**:
- **New page**: "🏆 學習成就" accessible from sidebar
- **Badge display**: Grid layout (3 columns on desktop, 2 on mobile) of badge cards
- **Badge card design**: Circular badge icon (emoji) + badge name + description + earned date
  - **Earned badges**: Full color, prominent display
  - **Unearned badges**: Grayed out with "如何獲得？" tooltip showing the criteria
- **Badge categories**:
  - 📚 **閱讀類**: "閱讀 5 家公司分析" (Reader), "閱讀 20 家公司分析" (Scholar)
  - 🧪 **測驗類**: "完成 10 道測驗" (Quiz Master) — requires C52
  - 🌐 **探索類**: "探索 3 個不同產業" (Sector Explorer), "探索 10 個不同產業" (Diversifier)
  - 📝 **筆記類**: "寫下 5 篇投資筆記" (Thinker) — requires C55
  - 🔍 **搜尋類**: "使用選股工具 5 次" (Screener) — requires C42
- **Progress tracking**: Session state counters for each badge criteria (companies viewed, quizzes completed, sectors explored, notes written, screener used)
- **New badge notification**: When a badge is earned, show a toast notification 🎉 with the badge name

**Risks**:
- **Session state only**: Badges are lost when the session ends. This is a significant UX risk — users will lose their achievements. Mitigation: Add local storage export/import. Full persistence requires D22.
- **Badge inflation**: Too many badges reduce the sense of achievement. Mitigation: Start with 5-8 badges, expand based on user feedback.
- **Motivation mismatch**: Not all users are motivated by gamification. Mitigation: Make badges opt-in — don't show notifications for users who haven't earned any badges yet.
- **PPT-style compliance**: A grid of badges is visual-first and follows PPT principles. Each badge card is one key point (the achievement).

**PPT-Style Compliance**: ✅ Badge grid is visual-first (emoji icons lead, text supports). Each badge is one key point. The page follows the "one key point per card" principle.

---

### C61: Sector Rotation Visualizer (產業輪動) — Market Momentum Map

**Priority**: P2 | **Effort**: 10-14h

**UX Benefit**: ★★★★☆ (High)
- Adds the **time dimension** to C51 (Sector Heatmap) — shows rotation, not just snapshot
- 永豐金證券 proves demand, but without plain-language explanations
- Helps beginners understand **market dynamics** — why some sectors are "hot"
- Aligns with "historian" positioning — explaining what's happening, not predicting

**Design Requirements**:
- **Extension of C51**: Add to the existing Sector Heatmap page as a new sub-tab ("產業輪動")
- **Chart type**: Animated bubble chart or multi-line chart showing sector momentum over time
  - X-axis: Time (1W / 1M / 3M selector)
  - Y-axis: Momentum score (normalized)
  - Bubble size: Sector market cap
  - Color: Green (positive momentum) → Red (negative momentum)
- **Plain-language explanation**: Below the chart, a dynamically generated summary:
  - "半導體產業過去 3 個月從悲觀轉為樂觀，主要受 AI 晶片需求復甦推動"
  - "金融產業動能持續下降，已連續 2 個月走弱"
- **"旋轉中" highlight**: Sectors that are changing direction (bearish→bullish or vice versa) get a special "🔄 旋轉中" badge
- **Company connection**: "如果你對這個產業感興趣，這裡是前 3 家公司：" with clickable links
- **Card style**: Use the existing `_info_card()` for the explanation section

**Risks**:
- **Complexity**: Sector rotation is a complex concept for beginners. The chart could be overwhelming. Mitigation: Add a "這是什麼？" expander at the top explaining sector rotation in ≤ 50 characters: "產業輪動是指資金在不同產業間流動，導致有些產業變熱、有些變冷。"
- **Data availability**: FinMind sector performance data may not have sufficient history for meaningful rotation analysis. Mitigation: Start with 1M view only, add 3M when data is available.
- **PPT-style compliance**: A bubble chart with many sectors could violate "one key point per page." Mitigation: Limit to top 8 sectors by market cap. Use the plain-language summary to distill the chart into ONE key point.

**PPT-Style Compliance**: ⚠️ Requires careful design. The chart should be the visual anchor, with the plain-language summary providing the "one key point" interpretation. The "旋轉中" badges help users focus on what matters.

---

### C62: Pre-Investment Checklist (投資前檢查清單) — Educational Scaffolding Tool

**Priority**: P2 | **Effort**: 8-12h

**UX Benefit**: ★★★★★ (Critical)
- Perfect **"historian" differentiator** — teaches users WHAT to look for, not WHAT to buy
- 永豐金證券 proves demand, but their checklist is pre-trade (broker context)
- Stock Explorer's version is **educational scaffolding** — teaches analysis methodology
- Low effort (8-12h) for high impact — teaches users how to think about stocks

**Design Requirements**:
- **Placement**: Bottom of the business card page, AFTER C41 (Read Next) and BEFORE the disclaimer. This is the "before you go" section — the last learning moment.
- **Card type**: New `_checklist_card()` — amber/orange border (`#F39C12`) with `📋` icon. Uses the same orange as C37 hero card to signal "important learning moment."
- **Checklist items** (5-7 items, each clickable to scroll to the relevant section):
  - ☐ 我了解這家公司是做什麼的 → scrolls to "一句話定位"
  - ☐ 我檢查了公司的獲利能力 → scrolls to ROE/P/E in key metrics
  - ☐ 我看了公司的負債情況 → scrolls to debt ratio
  - ☐ 我知道這家公司的主要風險 → scrolls to C44 Risk Analysis
  - ☐ 我跟同業做了比較 → scrolls to peer comparison tab
  - ☐ 我了解公司最近發生了什麼事 → scrolls to event dashboard tab
  - ☐ 我看了所屬產業的動態 → scrolls to C51 Sector Heatmap
- **Interaction**: Each item is a checkbox. Clicking the text scrolls to the relevant section (anchor links). Progress tracked in session state.
- **Progress indicator**: "完成了 3/7 項" at the top of the checklist
- **Completion message**: When all 7 items checked: "🎉 你已經完成了這家公司的基本分析！記得，這不是投資建議，而是你對這家公司的理解程度。"

**Risks**:
- **Anchor link reliability**: Streamlit's anchor scrolling is unreliable. Mitigation: Use `st.markdown(f'<a name="section"></a>')` markers and JavaScript-based scrolling. If this proves too fragile, remove the scroll-to-section feature and make items non-clickable checkboxes.
- **Checklist fatigue**: 7 items may feel like homework. Mitigation: Make it clear this is optional — "這份清單幫助你確認自己是否充分了解這家公司。不需要全部勾選才能繼續。"
- **Page length**: Adding another section to the already-long business card page. Mitigation: Make the checklist collapsible (default: collapsed). Only expand when the user clicks "📋 投資前檢查清單."

**PPT-Style Compliance**: ✅ The checklist is ONE key point ("Here's what you should understand before making a decision") presented as a visual checklist. The collapsible design keeps the page clean.

---

## Design Direction A: "Guided Learning Path"

**Philosophy**: Structure the 8 new features as a **progressive learning journey** — users start with onboarding, learn concepts through interactive tools, and track their progress with gamification.

**Features**: C58 → C56 → C57 → C62 → C60 → C55 → C61 → C59

**Design approach**:
1. **C58 Onboarding** is the entry point — teaches users how to navigate
2. **C56 Explain This Metric** is the core learning tool — every metric becomes a lesson
3. **C57 Compare Concepts** deepens understanding — metrics as tools
4. **C62 Pre-Investment Checklist** is the capstone — synthesizes everything
5. **C60 Badges** provide motivation throughout
6. **C55 Diary** is the reflection layer — personal learning archive
7. **C61 Sector Rotation** extends learning to market level
8. **C59 Chatbot** is the natural language interface — ties everything together

**Pros**:
- Clear user journey from beginner to competent
- Each feature builds on the previous one
- Onboarding (C58) ensures users discover all features
- Badges (C60) provide motivation throughout the journey
- Aligns with "point-to-point knowledge construction" core value

**Cons**:
- Requires implementing C58 first (14-20h) before other features can shine
- The "journey" metaphor may feel prescriptive — users may not want to follow a linear path
- High total effort (88-124h for all 8 features)
- Some features (C59 Chatbot, C61 Sector Rotation) don't fit neatly into the journey metaphor

---

## Design Direction B: "Personal Learning Companion"

**Philosophy**: Focus on features that create a **personal, reflective learning experience** — the diary, badges, and checklist form a "learning companion" that grows with the user.

**Features**: C55 → C60 → C62 → C56 → C58 → C57 → C59 → C61

**Design approach**:
1. **C55 Investment Diary** is the centerpiece — the user's personal learning archive
2. **C60 Badges** recognize learning milestones — motivates continued use
3. **C62 Checklist** ensures thorough analysis — quality over quantity
4. **C56 Explain This Metric** provides just-in-time learning — when the user needs it
5. **C58 Onboarding** introduces the companion concept — "Stock Explorer learns with you"
6. **C57 Compare Concepts** deepens understanding — for users who want more
7. **C59 Chatbot** is the conversational interface — "Ask your learning companion"
8. **C61 Sector Rotation** is the market context — "What's happening in the market"

**Pros**:
- Creates emotional attachment through personal content (diary)
- Badges provide recognition and motivation
- Checklist ensures learning quality
- "Companion" metaphor is beginner-friendly and aligns with "historian" positioning
- Lower initial effort — C55 + C60 + C62 = 26-38h for the core experience

**Cons**:
- Diary without persistence (session state only) risks user frustration
- Without onboarding (C58), users may not discover the diary and badges
- Less structured than Direction A — users may not know what to do next
- Chatbot (C59) feels tacked on rather than integrated

---

## Design Direction C: "Modular Education Layer"

**Philosophy**: Implement features as **independent modules** that can be used in any order — users pick what they need, when they need it.

**Features**: C56 → C62 → C58 → C55 → C60 → C57 → C61 → C59

**Design approach**:
1. **C56 Explain This Metric** is the highest-impact, most universally useful feature — implement first
2. **C62 Checklist** is the lowest-effort, highest-impact feature — implement second
3. **C58 Onboarding** ensures discoverability of all modules
4. **C55 Diary** is the personal layer — optional but valuable
5. **C60 Badges** are the engagement layer — optional but motivating
6. **C57 Compare Concepts** is the deep-dive module — for advanced beginners
7. **C61 Sector Rotation** is the market-level module — for context
8. **C59 Chatbot** is the interface layer — the ultimate module that ties everything together

**Pros**:
- Each feature stands alone — no dependencies between features
- Users can engage with any feature without completing others
- Flexible implementation order based on effort/priority
- C56 + C62 can be implemented quickly (20-28h) for immediate impact
- Easy to defer features without breaking the overall design

**Cons**:
- Less cohesive user experience — features may feel disconnected
- Without a unifying metaphor, the product may feel like a collection of tools
- Onboarding (C58) is less effective if it introduces features that don't feel related
- Badges (C60) need other features to track — less meaningful as a standalone

---

## Recommendation

**Adopt Direction A ("Guided Learning Path") with modifications from Direction C.**

**Rationale**:

1. **Start with C56 + C62** (from Direction C's modular approach) — these two features deliver the highest immediate UX impact for beginners:
   - C56 (Explain This Metric) directly addresses the ten-second test
   - C62 (Pre-Investment Checklist) teaches analysis methodology
   - Combined effort: 20-28h — achievable in one sprint

2. **Then implement C58 Onboarding** — this is the P1 feature that ensures users discover C56 and C62:
   - Without onboarding, beginners won't find the "❓" buttons or the checklist
   - Effort: 14-20h — but it multiplies the value of ALL other features

3. **Then add C55 + C60** (from Direction B's companion approach) — these create the personal learning experience:
   - C55 (Diary) + C60 (Badges) = 18-26h
   - Together, they transform Stock Explorer from a tool into a platform

4. **Defer C57 + C59 + C61** to later sprints — these are valuable but not critical for the beginner experience:
   - C57 (Compare Concepts) requires significant content creation
   - C59 (Chatbot) is the highest-effort feature (16-24h) with the most risk
   - C61 (Sector Rotation) depends on C51 being implemented first

**Recommended Sprint Sequence**:

| Sprint | Features | Effort | Rationale |
|--------|----------|--------|-----------|
| Sprint 5 | C56 + C62 | 20-28h | Highest immediate UX impact |
| Sprint 6 | C58 | 14-20h | Ensures discoverability |
| Sprint 7 | C55 + C60 | 18-26h | Personal learning experience |
| Sprint 8+ | C57 + C59 + C61 | 34-50h | Advanced features |

**Key Design Principles for Implementation**:
1. **PPT-style compliance**: Every feature must follow "one key point per page/card" — no exceptions
2. **Ten-second test**: Every feature must help beginners understand faster, not add cognitive load
3. **Progressive disclosure**: Use expanders, tabs, and collapsible sections to keep pages clean
4. **Session state awareness**: All features must gracefully handle session state loss (notes, badges, checklist progress)
5. **Mobile-first consideration**: Every feature must work on mobile (Streamlit's responsive limitations acknowledged)

---

## UX Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Business card page overload** — Adding C55 (diary input), C56 (metric explanations), C62 (checklist) to the already 14-section business card page | 🔴 High | Use expanders for all new sections. C56 "❓" buttons only show content on click. C62 checklist defaults to collapsed. C55 diary input is a single text field, not a full editor. |
| **Session state loss** — C55 diary entries, C60 badges, C62 checklist progress all lost on refresh | 🔴 High | Add export/import (JSON) for diary entries and badge progress. Show a warning: "你的筆記和成就僅保存在目前瀏覽階段，關閉瀏覽器後將遺失。" Consider local file storage as a bridge to D22 persistence layer. |
| **Onboarding fatigue** — 5-step onboarding may feel like homework before users see value | 🟡 Medium | Keep each step to ONE sentence + ONE illustration. Total onboarding time ≤ 60 seconds. Always offer "跳過" option. Show a compelling company (TSMC) at the end as immediate reward. |
| **Chatbot disappointment** — C59 can't answer most questions, leading to frustration | 🟡 Medium | Strictly limit to 10 pre-built question patterns. Always provide helpful fallback. Set expectations: "我只能回答關於公司基本資料、財務數據、風險分析的問題。" |
| **Badge inflation** — Too many badges reduce sense of achievement | 🟢 Low | Start with 5 badges. Only add more based on user feedback. Make unearned badges grayed out with clear criteria. |
| **Mobile responsiveness** — C57 two-column comparison, C61 bubble chart, C59 chat interface may not work on mobile | 🟡 Medium | Use CSS media queries to stack columns vertically on mobile. Hide complex charts on mobile, show text-only alternatives. Test on 375px width (iPhone SE). |
| **Content creation bottleneck** — C56 (10 metric explanations), C57 (10 concept pairs), C62 (7 checklist items with anchor links) require significant content writing | 🟡 Medium | Start with 5 metrics (C56), 5 concept pairs (C57). Use the existing analogy engine for content generation where possible. Prioritize TW stock examples. |
| **Anchor link unreliability** — C62 checklist items scroll to sections using anchor links, which Streamlit handles poorly | 🟢 Low | If anchor links prove unreliable, make checklist items non-clickable checkboxes. The educational value is in the checklist content, not the navigation. |
| **C61 depends on C51** — Sector Rotation Visualizer extends the Sector Heatmap, which is planned for Sprint 4 | 🟡 Medium | Plan C61 for Sprint 5+ (after C51 is complete). Don't start C61 until C51 is stable. |
| **C60 depends on C52** — Quiz Mode badges require C52 (Quiz Mode), which is planned for Sprint 5 | 🟢 Low | Design C60 badge criteria to work without C52 initially (companies viewed, sectors explored, notes written). Add quiz badges when C52 is implemented. |

---

## Design System Impact

### New Card Types Required

| Card Type | Use Case | Border | Background | Icon |
|-----------|----------|--------|------------|------|
| `_summary_card()` | C37 Key Takeaways (exists) | `#F39C12` (orange) | `#FFF8F0` (warm white) | `📋` |
| `_warning_card()` | C44 Risk Analysis (exists) | `#E74C3C` (red) | `#FDEDEC` (light red) | `⚠️` |
| `_tip_card()` | C41 Read Next (new) | `#F39C12` (orange) | `#FFF8F0` (warm white) | `📖` |
| `_diary_card()` | C55 Investment Diary (new) | `#27AE60` (green) | `#F0FFF4` (light green) | `📝` |
| `_checklist_card()` | C62 Pre-Investment Checklist (new) | `#F39C12` (orange) | `#FFF8F0` (warm white) | `📋` |
| `_badge_card()` | C60 Concept Mastery Badges (new) | `#3498DB` (blue) | `#F8F9FA` (neutral) | `🏆` |

### New Page Layouts Required

| Page | Navigation | Layout |
|------|------------|--------|
| 📝 投資日記 | Sidebar | Chronological card list |
| 📊 概念比較 | Sidebar | Two-column comparison with tabs |
| 💬 問問股識 | Sidebar | Chat interface with bubbles |
| 🏆 學習成就 | Sidebar | Badge grid (3 col desktop, 2 col mobile) |
| 產業輪動 | C51 sub-tab | Bubble chart + plain-language summary |

### Design System Documentation Updates Needed

1. **Add new card types** to `docs/domain/design_system.md`
2. **Add chat interface guidelines** (bubble colors, message alignment, suggestion chips)
3. **Add badge grid guidelines** (size, spacing, earned vs unearned states)
4. **Add onboarding modal guidelines** (step count, progress indicator, skip option)
5. **Add expandable checklist guidelines** (checkbox styling, progress indicator, completion message)

---

## Summary

### Top 3 Design Priorities for Round 12 Features

1. **C56 (Explain This Metric)** — P1, directly addresses ten-second test, transforms every data point into a learning opportunity. Start with 5 metrics, expand to 10.

2. **C62 (Pre-Investment Checklist)** — P2, lowest effort (8-12h) for highest educational impact. Teaches users HOW to analyze, not WHAT to buy. Perfect "historian" differentiator.

3. **C58 (Beginner Onboarding Flow)** — P1, critical for beginner retention. Without onboarding, users bounce before discovering C56 and C62. Keep it ≤ 60 seconds total.

### Design Grade Impact

Implementing C56 + C62 + C58 with proper PPT-style design could push the design grade from **A to A+** — the first A+ in Stock Explorer's history. The key is maintaining strict PPT-style compliance (one key point per card/section) while adding these interactive features through progressive disclosure (expanders, tabs, collapsible sections).

---

*Design Review completed. Recommendations aligned with PPT-style design system, ten-second test principle, and "beginner education" mission. Next steps: Team discussion to select design direction and approve Sprint 5 feature scope.*
