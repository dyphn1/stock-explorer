# Design Review — Round 13 Discussion

## 2026-06-19 Design Review — Round 13 Discussion

> **Author**: Design Reviewer  
> **Date**: 2026-06-19  
> **Context**: 💡 Discussion theme cycle — evaluating new Round 12 features (C55-C62) for design direction, analyzing unaddressed competitor UX patterns, and proposing design approaches for upcoming sprints.  
> **Current Design Grade**: A (upgraded from A- in Round 12)

---

## Table of Contents

1. [Current Design State Summary](#current-design-state-summary)
2. [Design Gap Analysis vs. Competitor Patterns](#design-gap-analysis-vs-competitor-patterns)
3. [Design Direction A: Interactive Metric Explorer](#design-direction-a-interactive-metric-explainer)
4. [Design Direction B: Guided Onboarding Journey](#design-direction-b-guided-onboarding-journey)
5. [Design Direction C: Reflective Learning Loop](#design-direction-c-reflective-learning-loop)
6. [Cross-Cutting Design System Recommendations](#cross-cutting-design-system-recommendations)
7. [Recommendation](#recommendation)

---

## Current Design State Summary

### Where We Are

Stock Explorer's design has progressed from **B+ → A- → A** across the last three review cycles. The core visual foundation is now solid:

| Component | Status | Grade |
|-----------|--------|-------|
| **Visual Health Score (C43 Snowflake)** | ✅ Implemented — 5-dimension radar chart with color-coded scores, reference lines, health summary | A |
| **Synthesis Layer (C37 Key Takeaways)** | ✅ Implemented — orange hero card, curated top-20 templates, 3-bullet cap | A |
| **Delta Tracking (C39 What Changed)** | ✅ Implemented — 2-delta cap, directional color coding, dual-channel encoding | A |
| **Valuation Context (C45 Band Chart)** | ✅ Implemented — 5-year PER percentile band with graceful fallback | A |
| **Recommendations (C41 Read Next)** | ✅ Implemented — peer stocks + fun facts on business card | A |
| **Page Layout Flow** | ✅ Summary → Delta → Health → Metrics → Details | A |
| **Hero Card Visual Distinction** | ✅ `_summary_card()` with orange/amber styling for C37 | A |

### Remaining Issues

| ID | Issue | Severity | Status |
|----|-------|----------|--------|
| D-021 | C43 hover/dimension cards lack underlying metric values | P1 | ⚠️ Partial |
| D-024 | `_info_card` background `#FFF8F0` should be `#F8F9FA` | P1 | ❌ Open |
| D-025 | C39 missing empty state when no deltas exceed threshold | P2 | ❌ Open |
| D-003 | Inconsistent card styling (group_structure, watchlist, etf_detail) | P2 | ❌ Open |
| D-006 | Mobile responsiveness gaps | P2 | ❌ Open |

### Sprint 3 Remaining Work

Three items remain before Sprint 4:

1. **C44 (Risk Analysis MVP)** — 12-14h — 3 risk dimensions (customer concentration, financial health, event-based)
2. **C38 (Compare Stories P1)** — 10-12h — structured side-by-side comparison
3. **D16 (Split analogy_engine.py)** — 2-3h — prerequisite for C48

### Sprint 5 Approved Features (Round 12 Decisions)

| ID | Feature | Effort | Design Notes |
|----|---------|--------|-------------|
| **C58** | Beginner Onboarding Flow | 14-22h | P1 prerequisite for education features |
| **C62** | Pre-Investment Checklist | 8-14h | "Historian" differentiator, amber checklist card |
| **C56** | Explain This Metric | 12-18h | Interactive metric explanations with mini-charts |
| **C60** | Concept Mastery Badges | 8-14h | Gamification, session-only MVP |

### Sprint 6-7 Approved Features

| ID | Feature | Effort | Design Notes |
|----|---------|--------|-------------|
| **C57** | Compare Concepts | 10-14h | Side-by-side metric comparison |
| **C55** | Investment Diary | 10-16h | Personal reflection journal |
| **C61** | Sector Rotation Visualizer | 10-16h | Extends C51 with time dimension |
| **C59** | AI Q&A Chatbot | 18-28h | Natural language interface |

---

## Design Gap Analysis vs. Competitor Patterns

### Competitor UX Patterns We've Addressed

| Competitor Pattern | Our Response | Status |
|-------------------|-------------|--------|
| Simply Wall St — Visual health score | C43 Snowflake radar chart | ✅ Done |
| Morningstar — Star rating / Moat | C43 5-dimension scoring + planned C46 | ✅ Partial |
| Public.com / Seeking Alpha — Key takeaways | C37 Key Takeaways hero card | ✅ Done |
| Koyfin — Recent changes | C39 Delta card | ✅ Done |
| 財報狗 — P/E band / Valuation context | C45 Valuation band chart | ✅ Done |
| 財報狗 — Stock screener | C42 (deferred) | ❌ Not started |
| Robinhood — Recommendations | C41 Read Next | ✅ Done |

### Competitor UX Patterns We Have NOT Addressed

These are the **critical unaddressed gaps** — competitor patterns that have no implementation plan and represent the biggest opportunities for differentiation:

#### 🔴 Gap 1: Interactive Metric Explanations (Magnify.money + 永豐金證券 + Robinhood)

**The pattern**: Magnify.money generates AI visual explanations for any financial concept. 永豐金證券's Financial Statement Visualizer lets users tap on any line item for a plain-language explanation. Robinhood has metric tooltips on every stock page. **All three** provide contextual, on-demand explanations — not static glossaries, but interactive, in-context learning.

**Our gap**: Stock Explorer shows metrics with analogies in dedicated sections, but there is no "explain this" interaction model. A user seeing "ROE: 25%" on the key metrics card has no way to tap/click for an explanation. C56 (Explain This Metric) is approved for Sprint 5 but the **design direction hasn't been specified**. This is the single highest-ROI unaddressed pattern — it directly addresses the ten-second test by making every data point a learning opportunity.

**Why it matters for Round 13**: The business card page goes from "shows metrics" to "teaches metrics." This is the difference between a reference tool and an education tool.

#### 🔴 Gap 2: Structured Onboarding (玉山證券 Beginner Village)

**The pattern**: 玉山證券's "Beginner Village" is a 7-step guided tutorial covering: what is a stock, how to read a chart, what is P/E, what is a dividend, how to place an order, how to manage risk, how to build a portfolio. It's the **most structured beginner experience** among TW brokers.

**Our gap**: Stock Explorer has no onboarding. Users land on the homepage and must figure out what to do. C58 is approved for Sprint 5 but the **design framework hasn't been established**. Without onboarding, beginners bounce before discovering Stock Explorer's value. This is the #1 UX gap for new user retention.

**Why it matters for Round 13**: Before we add more educational features (C56, C62, C57), we need users to actually **arrive at them**. Onboarding is the prerequisite for the entire education feature set.

#### 🟡 Gap 3: Reflection & Journaling (元大證券 Investment Diary + Tastytrade Trade Journal)

**The pattern**: 元大證券 lets users keep an investment diary for journaling about stocks. Tastytrade provides a built-in trade journal for recording rationale, outcomes, and lessons learned. Both turn passive reading into **active reflection**.

**Our gap**: Stock Explorer has no mechanism for users to record their own thoughts. Users read about companies but never create personal annotations. C55 (Investment Diary) is approved for Sprint 6, making it the **lowest-priority education feature**. However, the "historian of self" positioning is uniquely aligned with our product vision — users become historians of their own investment journey.

**Why it matters for Round 13**: This is a white space that no TW competitor has addressed properly. It transforms Stock Explorer from a lookup tool into a personal learning platform.

#### 🟡 Gap 4: Pre-Trade Educational Scaffolding (永豐金證券 Investment Checklist)

**The pattern**: 永豐金證券's "Investment Checklist" is a pre-trade educational tool — before buying a stock, users complete a checklist of key metrics to check. It teaches users **what to look for**, not **what to do**.

**Our gap**: Stock Explorer shows company data but provides no analytical scaffolding. Users see metrics but don't know which ones matter or in what order to consider them. C62 (Pre-Investment Checklist) is approved for Sprint 5.

**Why it matters for Round 13**: This is the purest expression of the "historian" positioning — "Here's what you should understand before making a decision" — and it has direct synergy with C56 (Explain This Metric). Together, they form a complete "understand → analyze → decide" learning pipeline.

#### 🟢 Gap 5: Gamified Learning (Robinhood Learn→Earn + Khan Academy Badges)

**The pattern**: Robinhood rewards users with stock for completing educational modules. Khan Academy has achievement badges. Both use gamification to create a **positive feedback loop** for learning.

**Our gap**: Stock Explorer has no recognition system for learning milestones. C60 (Concept Mastery Badges) is approved for Sprint 5 as a session-only MVP.

**Why it matters for Round 13**: Gamification is important for engagement but secondary to the core education experience. It should be designed to reinforce the learning paths established by onboarding (C58) and interactive explanations (C56).

---

## Design Direction A: Interactive Metric Explainer

### Description

Transform every metric on the business card page from a **static data point** into an **interactive learning moment**. Each metric gets an "❓" button that opens a visual explanation with a mini-chart, analogy, and "Why this matters" context — directly applying the Magnify.money / 永豐金證券 / Robinhood pattern to Stock Explorer's PPT-style, plain-language foundation.

### UX Approach

**Core Interaction Model — "Tap to Learn"**:

1. **Trigger**: Place a subtle "❓" icon button next to every metric label on the key metrics card section (關鍵數字三連卡). The icon is small (12px) and uses the neutral gray (`#7F8C8D`) to avoid visual clutter, but becomes blue (`#3498DB`) on hover to signal interactivity.

2. **Response**: Clicking the icon opens an **expandable card** (using `st.expander` with custom styling) positioned inline below the metric row. The expansion is smooth (CSS transition) to maintain the PPT-style flow.

3. **Card content structure** (PPT-style: visual first, text supports):
   - **Top: Mini-chart** — A sparkline or small bar chart (Plotly, ~120px tall) showing the metric's historical trend over 3 years. This gives visual context immediately.
   - **Middle: Plain-language explanation** — "ROE 25% 意思是每 100 元股東資金，公司賺 25 元" — using existing analogy engine. Max 40 Chinese characters.
   - **Bottom: "Why this matters"** — One line explaining when this metric is important and what to watch for. Example: "ROE 越高代表公司用錢效率越好，但要注意是否靠舉債撐高。"

4. **Priority metrics** (Sprint 5 MVP — 10 metrics):
   - ROE (股東權益報酬率) — Most important profitability metric
   - P/E (本益比) — Most referenced valuation metric
   - P/B (股價淨值比) — Complements P/E
   - Gross Margin (毛利率) — Core business quality
   - Revenue Growth (營收成長率) — Growth trajectory
   - Dividend Yield (殖利率) — Income investor focus
   - Debt Ratio (負債比率) — Financial health indicator
   - EPS (每股盈餘) — Basic earnings measure
   - Free Cash Flow (自由現金流) — Cash generation quality
   - Institutional Ownership (法人持股比例) — Market confidence signal

5. **State management**: Remember which explanations the user has opened (session state). Within a single session, previously opened explanations show a faint "👁 已讀" indicator next to the ❓ — subtle gamification that reinforces C60 badges.

**Content Architecture**:
- New file: `src/data/metric_explanations.yaml` — structured content with metric_name, chart_type, explanation_template, why_matters, analogy_key
- Uses existing `analogy_engine.py` for consistent plain-language generation
- Chart data sourced from existing FinMind integration — no new API calls needed

**Visual Design**:
- Expandable card uses a **light blue background** (`#EBF5FB`) to distinguish from the neutral info card background (`#F8F9FA`)
- Border-left: 3px solid `#3498DB` (blue, matching primary color)
- Mini-chart uses the existing color system — blue line for the metric, gray reference line for industry average
- Total height when expanded: ~200px (chart 120px + text 80px) — fits within card-based layout without breaking page flow

### Competitor Reference

| Competitor | What They Do | How We Adapt |
|-----------|-------------|-------------|
| **Magnify.money** | AI-generated custom visuals for every question | We use template-based explanations with real TW stock data — more reliable, less expensive, better localized |
| **永豐金證券** | Tap any financial statement line item | We apply this to all metrics on the business card — not just financial statements, but every key metric |
| **Robinhood** | Metric tooltips on every stock page | We go deeper than tooltips (which are limited to text) — we add mini-charts and "why this matters" context |

### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ One concept per explanation (one metric at a time), chart leads text, ≤ 40 chars per explanation |
| **Ten-second test** | ✅ User sees the mini-chart + one-line analogy and understands the metric in ≤ 10 seconds |
| **Zone A/B/C** | ✅ Explanation opens inline within Zone C, no zone violations |
| **Plain-language** | ✅ Uses existing analogy engine — no arbitrary jargon |
| **Color system** | ✅ Light blue background (`#EBF5FB`) is a tint of primary blue (`#3498DB`) — no new colors |
| **Component consistency** | ✅ New `_explain_card()` component in `_router_base.py`, follows same card pattern |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Content creation bottleneck** — 10 metrics × (explanation + chart config + "why this matters") = ~15h content work | High | Start content creation in Sprint 4 as parallel workstream (per Round 12 decision). Reuse analogy engine where possible. |
| **Page length increase** — Expandable cards add height when opened | Medium | Only one explanation open at a time (auto-close others). Expander pattern familiar to users. |
| **Information overload** — ❓ next to every metric could feel cluttered | Low | Use neutral gray by default, blue on hover. Small icon size (12px). Progressive disclosure — users who don't need explanations aren't affected. |
| **Stale content** — Static explanations don't adapt to current values | Medium | Explanation templates use f-string interpolation for current values. Chart shows actual historical data. |

---

## Design Direction B: Guided Onboarding Journey

### Description

A 5-step first-time user onboarding flow that introduces Stock Explorer's core features and guides beginners to their first "aha moment" — understanding a company they know. Modeled on 玉山證券's "Beginner Village" but adapted for our **stock analysis** (not stock trading) positioning. This directly addresses the #1 UX complaint: "I don't know where to start."

### UX Approach

**Onboarding Philosophy — "First Company First"**:

Unlike 玉山證券's abstract "what is a stock" approach (7 conceptual steps), Stock Explorer's onboarding should follow the **"First Company First"** principle: get users to their first company page as quickly as possible, then teach features in context.

**The 5-Step Flow**:

| Step | Title | Content | Interaction |
|------|-------|---------|-------------|
| 1 | 👋 歡迎來到股識 | "我們不是報明牌，而是帶你認識公司。讓我們從一間你熟悉的公司開始。" | Welcome card with "開始探索" button |
| 2 | 🔍 搜尋公司 | "試著搜尋一間你聽過的公司 — 台積電、鴻海、或星巴克" | Pre-highlights the search box in Zone B sidebar. Auto-suggests TSMC (2330) as the default example. |
| 3 | 📋 認識名片 | "這是公司的『名片』。橘色卡片是重點摘要 — 10 秒內說出這家公司在做什麼？" | Navigates to TSMC business card page. Highlights C37 (orange hero card). Uses tooltip overlay pointing to the card. |
| 4 | 📊 健康檢查 | "這個雷達圖跟你說公司健不健康。綠色代表好，紅色代表要注意。" | Highlights C43 (snowflake chart). Tooltip explains the 5 dimensions briefly. |
| 5 | 💡 自己試試看 | "現在換你試試看！三間適合新手的公司：台積電、鴻海、富邦媒" | End card with 3 clickable company buttons. Offers "📖 新手指南 PDF" download option. |

**Technical Implementation**:

- **Detection**: Session state flag `onboarding_completed` (defaults to `False`)
- **Trigger**: On first page load, if `onboarding_completed == False`, show a full-screen modal overlay with Step 1
- **Progressive highlight**: Each step uses a semi-transparent overlay (`position: fixed`, `z-index: 999`) that darkens the page except for the highlighted element
- **Navigation**: Steps 3-4 navigate to the actual TSMC business card page — users experience the **real product**, not a simulation
- **Completion**: After Step 5, `onboarding_completed = True`. A small "❓" in Zone A (navbar) allows replaying the tour
- **Skip**: Every step has a "跳過" button — never force onboarding

**Beginner-Friendly Company Selection**:

The 3 recommended companies in Step 5 are chosen based on:
1. **台積電 (2330)** — Most well-known TW company, excellent for showing technology sector analysis
2. **鴻海 (2317)** — Household name, different business model (manufacturing vs. semiconductor)
3. **富邦媒 (8454)** — Consumer-facing business beginners can intuitively understand (momo購物網)

This gives beginners exposure to **3 different business models** and **3 different sectors**, demonstrating Stock Explorer's range.

### Competitor Reference

| Competitor | What They Do | How We Adapt |
|-----------|-------------|-------------|
| **玉山證券 "Beginner Village"** | 7-step conceptual onboarding (what is a stock, how to read a chart, etc.) | We compress to 5 contextual steps — users learn by DOING, not reading tutorials. Every step happens in the real product. |
| **Robinhood "First Stock"** | Step-by-step tutorial for buying your first stock | We replace "buying" with "understanding" — aligns with historian positioning. No trading context. |
| **eToro "Virtual Portfolio"** | Practice with virtual money | We use real companies — no simulation needed. Real data is more engaging than fake portfolios. |

### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ Onboarding IS a presentation — 5 slides, one key point per slide, minimal text (≤ 100 chars per step) |
| **Ten-second test** | ✅ Each step's content can be understood in ≤ 10 seconds. "認識公司 → 看名片 → 查健康" is the core loop. |
| **Zone A/B/C** | ✅ Onboarding overlays respect zone boundaries. Step 2 highlights Zone B, Steps 3-4 highlight Zone C content. |
| **Plain-language** | ✅ No jargon in onboarding. "健康檢查" not "財務分析". "名片" not "公司資訊頁". |
| **Color system** | ✅ Overlay uses semi-transparent dark background (`rgba(0,0,0,0.5)`). Highlight uses primary blue (`#3498DB`). CTA button uses existing button styling. |
| **Component consistency** | ✅ New `_onboarding_overlay()` component in `_router_base.py` for tooltip-style guidance. |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Streamlit limitations** — Tooltips and overlays may be difficult to implement with pure Streamlit | Medium | Use HTML/CSS overlays via `st.markdown(unsafe_allow_html=True)`. Pre-built positioning for each step. Accept imperfect positioning over abandonment. |
| **Step 3-4 navigation disruption** — Navigating to TSMC page during onboarding disrupts the flow | Medium | Show steps 1-2 on ANY page. For step 3, ask user to search for TSMC first. After search, show the remaining steps as overlays. |
| **Onboarding fatigue** — Users skip through without reading | Low | Keep each step ≤ 30 seconds. Only 5 steps total. "跳過" button always available. |
| **Replay complexity** — "Replay onboarding" from navbar requires re-implementing Step 3-4 navigation | Medium | Replay shows a condensed 3-step version skippable to each feature. No product navigation replay. |

---

## Design Direction C: Reflective Learning Loop

### Description

A three-part reflection system combining **Investment Diary (C55)**, **Pre-Investment Checklist (C62)**, and **Concept Mastery Badges (C60)** into a cohesive "Reflective Learning Loop" — users read → reflect → check → earn. This transforms Stock Explorer from a passive lookup tool into an active learning platform. Inspired by 元大證券's Investment Diary and Tastytrade's Trade Journal, but reimagined for the "historian of self" positioning.

### UX Approach

**The Loop: Read → Reflect → Check → Earn**

```
[Read Company Page] → [Reflect: Write Diary Entry] → [Check: Complete Pre-Investment Checklist] → [Earn: Badge Unlocked]
```

**Component 1: Investment Diary (C55) — "認識自己"**

- **Placement**: Bottom of the business card page, **after C41 (Read Next)** and before the disclaimer. This is the LAST content section — users have absorbed all company information before reflecting.
- **Card type**: New `_diary_card()` — green border (`#27AE60`), light green background (`#F0FFF4`), `📝` icon. Green signals "personal/growth" — distinct from blue (info) and amber (summary) and red (warning).
- **Interaction**:
  - Text area for free-form notes ("你覺得這家公司在做什麼？有什麼問題想問？")
  - Save button persists to session state (or local JSON file in Sprint 6 MVP)
  - Previously saved entries shown below in a collapsed "查看先前的筆記" section
  - Connection to events: If the user saved a note > 30 days ago, show a banner: "你 30 天前寫了這張筆記 — 營收成長了 15%，你有猜到嗎？"
- **Design constraint**: Max 500 characters per entry (prevents wall-of-text). PPT-style discipline applies.

**Component 2: Pre-Investment Checklist (C62) — "準備好再做決定"**

- **Placement**: Business card page, **between C43 (Snowflake) and 關鍵數字三連卡**. This positions the checklist AFTER the health visualization (which teaches what's important) but BEFORE the detailed metrics (which the checklist teaches you to use).
- **Card type**: New `_checklist_card()` — amber border (`#F39C12`), light amber background (`#FFF8F0`), `📋` icon. Same color family as the hero card (C37) to create visual connection between "what to understand" and "what to check."
- **Content** (5 items — matching the 5 snowflake dimensions):
  1. "我了解這家公司靠什麼賺錢" → links to 一句話定位 section
  2. "我有看過健康檢查的五個面向" → links to C43 Snowflake
  3. "我知道估值是貴還是便宜" → links to C45 Valuation Band
  4. "我有留意主要風險" → links to C44 Risk Analysis
  5. "我有跟同業比較過" → links to Peer Comparison page
- **Interaction**: Each item is a checkbox. Clicking the item scrolls to the relevant section. Progress saved in session state.
- **Completion message**: "你完成了 5/5 檢查項目！你已經了解這家公司了。" — This triggers a C60 badge.

**Component 3: Concept Mastery Badges (C60) — "學習看得見"**

- **Placement**: New top-level page ("🏆 學習成就") accessible from the sidebar. NOT on the business card page — badges are a meta-layer, not a company-specific feature.
- **Card type**: New `_badge_card()` — blue border (`#3498DB`), gradient background (light blue to white), badge emoji icons.
- **Badge definitions** (MVP — 6 badges):
  - 📚 **新手上路** — Complete onboarding (C58)
  - 🔍 **第一次探索** — View first company page
  - 📝 **觀察家** — Write 3 diary entries (C55)
  - 📋 **分析師** — Complete 5 checklists (C62)
  - 🌐 **跨產業視野** — View companies from 3 different sectors
  - 🎯 **十秒挑戰** — Complete checklist for the same company where you wrote a diary entry (CROSS-FEATURE badge)
- **Session-only**: Badges tracked in session state. No persistence (avoids D22 persistence layer dependency).

**Visual Design Across All Three**:

| Component | Border | Background | Icon | Color Meaning |
|-----------|--------|------------|------|---------------|
| Diary (C55) | `#27AE60` (green) | `#F0FFF4` | 📝 | Growth, personal |
| Checklist (C62) | `#F39C12` (amber) | `#FFF8F0` | 📋 | Attention, preparation |
| Badges (C60) | `#3498DB` (blue) | `#EBF5FB` | 🏆 | Achievement, completion |

### Competitor Reference

| Competitor | What They Do | How We Adapt |
|-----------|-------------|-------------|
| **元大證券 "Investment Diary"** | Journaling about stocks, personal notes | We go beyond passive notes — we connect diary entries to actual outcomes and create a feedback loop |
| **Tastytrade "Trade Journal"** | Record rationale, outcome, lessons learned | We don't have trades (historian positioning) — we record understanding, not transactions. "What do I think about this company?" not "Why did I buy this stock?" |
| **永豐金證券 "Investment Checklist"** | Pre-trade checklist before buying | We reframe as educational scaffolding — "Here's what you should understand" not "Here's what you should do." No buy/sell framing. |
| **Robinhood "Learn → Earn"** | Stock rewards for completing education | We use badges instead of financial rewards — aligns with historian positioning. No monetary incentives. |

### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| **PPT-style** | ✅ Each component has ONE purpose: Diary = reflect, Checklist = analyze, Badges = achieve. One key point per card. |
| **Ten-second test** | ✅ Checklist items are ≤ 20 chars each. Badge names are ≤ 4 chars. Instant comprehension. |
| **Zone A/B/C** | ✅ Diary and Checklist are in Zone C (business card page). Badges are a separate page (also Zone C). No zone violations. |
| **Plain-language** | ✅ "投資前檢查清單" → uses task-focused, action-oriented language. No financial jargon in UI labels. |
| **Color system** | ✅ Green (growth/personal), amber (attention/preparation), blue (achievement) — all from the existing palette. No new colors. |
| **Component consistency** | ✅ Three new `_diary_card()`, `_checklist_card()`, `_badge_card()` components in `_router_base.py`, following the same card pattern. |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Session-only data loss** — Users lose diary entries and badge progress on page refresh | High | Acceptable for MVP (C60 is explicitly session-only). D22 (persistence layer) is the long-term solution. Clear disclaimer: "目前筆記僅在此瀏覽階段保存". |
| **Content-filling pressure** — Getting users to actually write diary entries is hard | Medium | Lower friction: provide sentence starters ("我覺得這家公司...") instead of blank text area. Suggest prompts based on the company. |
| **Checklist credibility** — Users check boxes without actually understanding | Low | This is a learning tool, not a certification. The items link to relevant sections, encouraging actual review. Design intent is scaffolding, not gatekeeping. |
| **Feature interaction complexity** — Three interlinked features (C55+C62+C60) create complex state management | Medium | Implement independently first (C60 badges are simplest). Add cross-feature triggers (diary + checklist → badge) only in later sprint. |

---

## Cross-Cutting Design System Recommendations

### 1. New Card Type Library

The upcoming features require **three new card types** that should be added to `_router_base.py` in Sprint 5:

```python
def _explain_card(title: str, content: str, icon: str = "❓") -> str:
    """Light blue expandable card for metric explanations (C56)."""
    # border-left: 3px solid #3498DB, background: #EBF5FB

def _diary_card(title: str, content: str, icon: str = "📝") -> str:
    """Green card for personal diary entries (C55)."""
    # border-left: 4px solid #27AE60, background: #F0FFF4

def _checklist_card(title: str, content: str, icon: str = "📋") -> str:
    """Amber card for pre-investment checklist (C62)."""
    # border-left: 4px solid #F39C12, background: #FFF8F0

def _badge_card(title: str, content: str, icon: str = "🏆") -> str:
    """Blue gradient card for achievement badges (C60)."""
    # border-left: 4px solid #3498DB, background: linear-gradient(135deg, #EBF5FB, #FFFFFF)
```

### 2. Content File Architecture

New data files needed for Sprint 5-6 features:

| File | Purpose | Features |
|------|---------|----------|
| `src/data/metric_explanations.yaml` | Metric → explanation + chart config + analogy | C56 |
| `src/data/concept_pairs.yaml` | Concept pair → comparison + examples | C57 |
| `src/data/checklist_items.yaml` | Checklist items → labels + section links | C62 |
| `src/data/badges.yaml` | Badge definitions → criteria + icons | C60 |

### 3. Business Card Page Growth Management

With C44 (Risk Analysis) and C56 (Explain This Metric) both adding to the business card page, the page is approaching **15+ sections**. The design system must enforce:

- **Expandable sections** for anything below the fold (C44 Risk Analysis, C56 Metric Explanations)
- **"Above the fold" definition**: C37 + C39 + C43 should be visible without scrolling on 1080p (≤ 800px height)
- **D24 (sub-directory extraction)**: business_card.py must be split before adding C56 to prevent > 600 lines

---

## Recommendation

### Primary Recommendation: Adopt All Three Directions as a Unified "Education Core"

The three directions — **Interactive Metric Explainer (A)**, **Guided Onboarding Journey (B)**, and **Reflective Learning Loop (C)** — are not independent features. They form a **cohesive education pipeline**:

```
[Onboarding: C58] → [Interactive Explanations: C56] → [Checklist: C62] → [Diary: C55] → [Badges: C60]
     ↓                      ↓                            ↓                  ↓                ↓
"First company"      "Understand metrics"         "Analyze properly"   "Reflect"        "Achieve"
```

This is the **"Foundation + Education Core"** direction approved in Round 12, now with concrete design specifications.

### Sprint 5 Design Priority

| Priority | Feature | Design Deliverable | Effort |
|----------|---------|-------------------|--------|
| **1** | C58 Onboarding | 5-step flow design, overlay component, beginner company selection | 14-22h |
| **2** | C56 Explain Metric | `_explain_card()` component, `metric_explanations.yaml` structure, 10 metric templates | 12-18h |
| **3** | C62 Checklist | `_checklist_card()` component, `checklist_items.yaml`, section linking | 8-14h |
| **4** | C60 Badges | `_badge_card()` component, `badges.yaml`, session tracking | 8-14h |

### Design Grade Projection

If all three directions are implemented as specified, the design grade can reach **A+** in Round 14:

- **A+ criteria**: All P1 issues resolved, education features have cohesive design system, onboarding drives beginner retention, interactive explanations make every data point a learning opportunity, reflection tools create unique "historian of self" positioning.
- **Current blockers to A+**: D-021 (partial), D-024 (open), D-025 (open) — all fixable in Sprint 4.

### Key Design Risks to Monitor

1. **Content creation bottleneck** — C56 requires 10 metric explanations + chart configs. Must start Sprint 4.
2. **Business card page length** — C44 + C56 additions push page toward 15+ sections. Expandable design is critical.
3. **Session state scalability** — C55 + C60 + C62 all use session state. D22 (persistence) will be needed by Sprint 7.
4. **Streamlit overlay limitations** — C58 onboarding may require creative HTML/CSS workarounds.

---

*Design Review completed. Three directions proposed: Interactive Metric Explainer (Magnify.money model), Guided Onboarding Journey (玉山證券 model), and Reflective Learning Loop (元大證券 + Tastytrade model). All three align with PPT-style design system, ten-second test principle, and "historian" positioning. Next review: After Sprint 5 feature implementation.*
