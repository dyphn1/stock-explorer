# Design Review — Discussion Round 46 (2026-06-15)

> **Reviewer**: Design Reviewer
> **Sprint**: Discussion Cycle Round 46
> **Current Design Grade**: A (stable since Round 44)
> **Theme**: Future Feature UX Evaluation — 8 new competitor-sourced features (C199-C206)

---

## Feature Evaluations

### C199: "Bear vs Bull" Visual Debate Cards

- **UX Impact**: **High**
- **Design Compliance**: ⚠️ (with conditions)
- **Design Direction**:
  - Two side-by-side cards (left = 🐻 Bear / right = 🐂 Bull) in Zone C main area
  - Each card: icon header + 3 key stats with plain-language interpretation + one-line conclusion
  - Bear card uses `#E74C3C` (red) left border; Bull card uses `#27AE60` (green) left border — consistent with color system
  - Cards use existing `_info_card()` pattern: `#F8F9FA` background, `border-radius:12px`, `padding:1.2rem`
  - Each card text ≤ 80 chars; combined ≤ 160 chars — within 200-char page limit
  - Footer: "這不是投資建議，只是整理兩種觀點" (historian positioning disclaimer)
  - **Ten-second test**: "有人看好這家公司，也有人看壞 — 這是雙方的論點" ✅
- **Risks**:
  - Could be misinterpreted as investment advice — must include prominent historian disclaimer
  - Risk of false balance (presenting both sides as equally valid when data may favor one) — should weight by evidence quality
  - Side-by-side layout may not render well on mobile (Streamlit columns collapse) — needs responsive fallback to stacked cards
  - Must NOT appear on Business Card page (too opinionated for first impression) — best placed on Peer Comparison or a new "觀點" tab

---

### C200: "What If I Had Invested?" Historical Scenario Calculator

- **UX Impact**: **High**
- **Design Compliance**: ⚠️ (interactive element in Zone C)
- **Design Direction**:
  - Single interactive card in Zone C with date picker + investment amount input (top of content area, clearly separated from data per Zone C rules)
  - Result displayed as large number: "如果在 2020-01-01 投入 10,000 元，現在價值 **28,500 元**" — uses `font-size:1.6rem; font-weight:700` per typography spec
  - Below result: one-line plain-language explanation in green italic (`#27AE60; font-style:italic`)
  - Chart: simple line chart showing growth over time (Plotly, transparent background, >60% of card area)
  - Disclaimer: "歷史報酬不代表未來表現，這只是讓你了解這家公司過去的表現"
  - Color: gain in `#27AE60` (green), loss in `#E74C3C` (red)
  - **Ten-second test**: "如果當初投資一萬塊，現在會變多少？" ✅
- **Risks**:
  - Interactive controls in Zone C must be at the TOP, separated from data display — cannot mix controls with chart
  - Could encourage recency bias (users pick recent dates that show best returns) — should default to "5 years ago" or "IPO date"
  - Must NOT include dividend reinvestment (too complex for beginner) — clearly label "不含股息"
  - Streamlit date_input + number_input need unique keys following `{function}_{stock_id}` convention

---

### C201: "Daily Market Story" 3-Minute Morning Briefing Card (P1 — ELEVATED)

- **UX Impact**: **Very High** (P1 priority — highest UX impact)
- **Design Compliance**: ✅ (fully aligned)
- **Design Direction**:
  - Homepage card (appears before stock search) — "📰 今日市場故事" header
  - 3-5 bullet points, each ≤ 40 chars, total text ≤ 180 chars
  - Each bullet: emoji + plain-language statement + one key metric
  - Example: "📈 台積電昨日漲 2%，因為 AI 晶片需求超乎預期"
  - Read time indicator: "⏱ 閱讀時間 2 分鐘" (ties to C205)
  - Card uses `#FEF9E7` (warning yellow) background to distinguish from data cards — this is informational, not analytical
  - Auto-generated daily; cached per day; shows "今天" / "昨天" date label
  - **Ten-second test**: "今天市場發生了什麼事？三分鐘看完" ✅
- **Risks**:
  - Requires daily content generation pipeline — if content is stale or generic, it damages credibility
  - Must NOT include buy/sell language — pure historian framing ("發生了什麼" not "該買什麼")
  - P1 effort (12-16h) is significant — should be phased: v1 = curated template, v2 = AI-generated
  - Must handle weekends/holidays gracefully ("今天休市，來看看最近的大事")
  - This is the #1 retention feature — if done poorly, it becomes noise; must maintain quality bar

---

### C202: "Story Arc" Timeline Labels — Auto-Detected Narrative Arcs

- **UX Impact**: **Medium-High**
- **Design Compliance**: ✅ (historian positioning — core identity)
- **Design Direction**:
  - Integrated into existing Event Dashboard / Story Timeline page
  - Auto-detected narrative arcs displayed as colored labels on timeline: "📈 成長期", "⚠️ 挑戰期", "🔄 轉型期", "📉 衰退期"
  - Labels use existing color system: growth = `#27AE60` (green), challenge = `#F39C12` (orange/warning), transformation = `#3498DB` (blue), decline = `#E74C3C` (red)
  - Each label: icon + 2-word name + one-line plain-language explanation on hover/expand
  - Max 3-4 arcs per company (keep it simple) — each arc spans a time range on the timeline
  - Arc detection: based on revenue trend + event density + margin changes (algorithm in service layer, not UI)
  - **Ten-second test**: "這家公司經歷了哪些階段？" ✅
- **Risks**:
  - Auto-detection accuracy — if arcs are wrong, it undermines trust. Must include confidence indicator (ties to C204)
  - Overlapping arcs could confuse beginners — must have clear visual separation
  - "Story arc" is a literary term — must always show plain-language translation: "故事階段"
  - Timeline labels must not clutter the chart — max 4 labels, positioned above/below timeline bar

---

### C203: "Supply Chain Impact" Visual Map

- **UX Impact**: **Medium** (high value for specific stocks, niche for others)
- **Design Compliance**: ⚠️ (complex visualization, high effort)
- **Design Direction**:
  - Node-and-link diagram in Zone C: company center node + customer/supplier nodes radiating outward
  - Company node: large circle with name + industry tag
  - Customer nodes: `#27AE60` (green) — "誰買了這家公司的產品"
  - Supplier nodes: `#3498DB` (blue) — "這家公司的原料來自哪裡"
  - Event propagation: when a key event affects a supplier/customer, show ripple animation (subtle, not distracting)
  - Max 8-10 nodes (keep readable) — prioritize top customers/suppliers by revenue %
  - Plain-language labels on each node: "蘋果 — 佔營收 25%" not just "AAPL"
  - **Ten-second test**: "這家公司的上下游關係" ✅
- **Risks**:
  - Highest effort (14-18h) — may not justify UX impact for all stocks
  - Node-and-link diagrams are hard to render in Streamlit (no native support) — requires Plotly or HTML/SVG injection (D-003 risk)
  - Data availability: supply chain data is incomplete for many TW stocks — must handle "資料不足" gracefully
  - Could overwhelm beginners if too many nodes — should default to "top 5" with "顯示更多" option
  - Best as a tab on Group Structure page, not a standalone page

---

### C204: "Confidence Indicator" on AI Explanations — Emoji-Based

- **UX Impact**: **High** (trust + transparency, low effort)
- **Design Compliance**: ✅ (fully aligned)
- **Design Direction**:
  - Small emoji indicator appended to every AI-generated explanation:
    - 🟢 "高信心" — data is strong, conclusion is well-supported
    - 🟡 "中信心" — data is partial, conclusion is reasonable but uncertain
    - 🔴 "低信心" — data is limited, conclusion is speculative
  - Position: inline after explanation text, same line, `font-size:0.85rem`
  - Tooltip/hover: one-line plain-language explanation of why this confidence level
  - Example: "台積電的毛利率穩定在 55%，代表它有很強的定價能力 🟢" — "數據來自 10 季財報，結論可靠"
  - Color: use emoji colors (inherent) — no additional color system usage needed
  - **Ten-second test**: "這個分析的可信度有多高？看顏色就知道" ✅
- **Risks**:
  - Emoji rendering may be inconsistent across browsers/OS — test on Safari, Chrome, mobile
  - Must NOT appear on non-AI content (raw data, charts) — only on generated explanations
  - Confidence algorithm must be simple and defensible — if users question the confidence levels, trust erodes
  - Lowest effort (4-6h) — should be bundled with another feature, not standalone sprint

---

### C205: "Read Time" Indicator on All Content

- **UX Impact**: **Medium** (reduces commitment anxiety, improves scannability)
- **Design Compliance**: ✅ (fully aligned)
- **Design Direction**:
  - Small text label at top-right of each content section: "⏱ 閱讀 1 分鐘"
  - `font-size:0.75rem; color:#7F8C8D` — subtle, non-intrusive
  - Calculation: word count / 200 words per minute (TW Chinese reading speed)
  - Applied to: all card content, all page sections, all educational modules
  - Total page read time shown in page header: "本頁閱讀時間：3 分鐘"
  - **Ten-second test**: "這個頁面要花多少時間看完？" ✅
- **Risks**:
  - Must NOT clutter the UI — keep it subtle and secondary
  - Read time estimates may be inaccurate for non-native readers — add 20% buffer
  - Trivial to implement (2-4h) — should be bundled with C201 or C204, not standalone
  - Must update dynamically if content changes (e.g., user selects different time range)

---

### C206: "Recurring Investment" Concept Education

- **UX Impact**: **Medium-High** (financial literacy, beginner-friendly)
- **Design Compliance**: ✅ (educational, not advisory)
- **Design Direction**:
  - Educational card/section: "📚 什麼是定期定額？" — concept explanation, not tool
  - Content: 3-part card series (one key point per card, PPT-style):
    - Card 1: "定期定額 = 每個月固定買，不管漲跌" (definition)
    - Card 2: "長期來說，這樣可以平滑買入成本" (benefit, with simple chart)
    - Card 3: "這不是投資建議，只是讓你了解這個概念" (historian disclaimer)
  - Simple chart: line showing "每月投入 3000 元" over 12 months with varying prices
  - Plain-language throughout: "定期定額" always paired with "固定時間投入固定金額"
  - **Ten-second test**: "什麼是定期定額？每月固定買，長期平滑成本" ✅
- **Risks**:
  - Must be clearly educational — NO calculator, NO "try it" tool (that crosses into advisory)
  - Could be seen as promoting a specific strategy — must include "這只是眾多策略之一" disclaimer
  - Best placed in a new "投資概念" section or ETF Zone, not on individual stock pages
  - Must NOT include specific stock examples with real returns (too close to advisory)

---

## Top Recommendations

### 1. C201: "Daily Market Story" 3-Minute Morning Briefing Card (P1)
**Rationale**: Highest UX impact + P1 priority + directly addresses retention. The issues file notes "daily cadence is #1 retention pattern" from Finimize and Robinhood research. This is the single most impactful feature for transforming Stock Explorer from a lookup tool into a daily habit. Design compliance is excellent — it's a simple card with plain-language content, perfectly aligned with PPT-style and ten-second test.

### 2. C204: "Confidence Indicator" on AI Explanations (P2, 4-6h)
**Rationale**: Highest ROI (4-6h for high UX impact) + unique transparency feature + teaches critical thinking. No TW competitor has this. It directly supports the historian positioning by teaching beginners to evaluate data quality. It's also a trust-building feature — users will trust AI explanations more when they know the confidence level. Bundles naturally with any AI-generated content.

### 3. C199: "Bear vs Bull" Visual Debate Cards (P2, 8-12h)
**Rationale**: Strong UX impact + unique differentiator + aligns with "benchmark-oriented analysis" core value. No TW competitor has visual debate format. Teaches beginners that investing involves weighing multiple perspectives — a critical financial literacy skill. The side-by-side card format is a natural extension of the existing card system.

**Honorable Mention**: C205 (Read Time, 2-4h) should be implemented as a companion to C201 — they're naturally bundled and together create a "respect the user's time" design pattern.

---

## Design Direction for Top Picks

### C201: Daily Market Story — Detailed Design Spec

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  Zone A: Stock Explorer | 股識                    │
├──────────┬──────────────────────────────────────┤
│          │  📰 今日市場故事                        │
│  Zone B  │  ⏱ 閱讀時間 2 分鐘                      │
│  Sidebar │                                      │
│          │  • 📈 台積電漲 2%，AI 晶片需求超乎預期    │
│          │  • 📉 聯電跌 1%，成熟製程價格競爭加劇     │
│          │  • 💡 半導體類股整體上漲 1.5%            │
│          │  • 🌐 美股那斯達克昨收漲 0.8%            │
│          │                                      │
│          │  ── 分隔線 ──                          │
│          │                                      │
│          │  [搜尋股票...]                          │
└──────────┴──────────────────────────────────────┘
```

**Content Rules**:
- Exactly 4 bullets (not 3, not 5 — 4 is scannable in 10 seconds)
- Each bullet: emoji + company/event + metric + plain-language cause
- Total text: ≤ 180 chars (including emojis)
- Source: M5 event detection engine + analogy engine for plain-language
- Fallback: if no significant events, show "今天市場相對平靜，來看看最近的大事" + 3 recent events from past week

**Technical Notes**:
- Cache key: `daily_story_{date}` in session_state
- Regenerate at 08:00 TW time daily
- Weekend: show "今天休市" + weekly summary
- Error state: hide card entirely (never show broken content)

---

### C204: Confidence Indicator — Detailed Design Spec

**Visual Design**:
```
┌─────────────────────────────────────────────────┐
│  台積電的毛利率穩定在 55%，代表它有很強的定價能力 🟢  │
│  ↳ 資料來自 10 季財報，結論可靠（tooltip）          │
├─────────────────────────────────────────────────┤
│  台積電可能受惠於 AI 趨勢，但競爭正在加劇 🟡          │
│  ↳ 資料有限，這是合理推測但非確定結論（tooltip）      │
├─────────────────────────────────────────────────┤
│  台積電明年營收可能成長 20%，但有不確定性 🔴          │
│  ↳ 這是推測性結論，請參考更多資料（tooltip）          │
└─────────────────────────────────────────────────┘
```

**Confidence Algorithm** (service layer, not UI):
- 🟢 High: ≥ 8 quarters of consistent data, clear trend, no conflicting signals
- 🟡 Medium: 4-7 quarters of data, some trend, minor conflicting signals
- 🔴 Low: < 4 quarters, speculative, or significant conflicting signals

**Integration Points**:
- Every `_白话_card()` call should include optional `confidence` parameter
- Every `_summary_card()` call should include optional `confidence` parameter
- New helper: `_confidence_badge(level)` returns emoji + tooltip HTML
- Must be backward-compatible: existing cards without confidence show no badge

---

### C199: Bear vs Bull Debate Cards — Detailed Design Spec

**Layout**:
```
┌──────────────────────┬──────────────────────┐
│  🐻 看空觀點           │  🐂 看多觀點           │
│  ──────────────────  │  ──────────────────  │
│                      │                      │
│  ⚠️ 毛利率從 56%     │  ✅ 營收連續 5 季     │
│  下降到 52%          │  成長超過 15%         │
│                      │                      │
│  📉 資本支出持續      │  📈 AI 晶片需求      │
│  高漲，壓縮自由現金流  │  推動先進製程營收     │
│                      │                      │
│  💡 競爭加劇可能      │  💡 技術領先優勢      │
│  影響定價能力        │  難以被超越           │
│                      │                      │
│  border-left: 4px    │  border-left: 4px    │
│  solid #E74C3C       │  solid #27AE60       │
└──────────────────────┴──────────────────────┘
│  這不是投資建議，只是整理兩種觀點。請自行判斷。  │
└─────────────────────────────────────────────────┘
```

**Content Rules**:
- Each card: exactly 3 points (icon + metric + plain-language interpretation)
- Each point: ≤ 50 chars; total per card ≤ 140 chars
- Points must be DATA-DRIVEN (from actual metrics), not opinion
- Bear points: focus on risks, declining metrics, competitive threats
- Bull points: focus on strengths, growth metrics, market opportunities
- Source: analogy engine generates both perspectives from same data
- Disclaimer: always present, historian positioning

**Placement**: New "觀點" tab on company pages (after Peer Comparison), NOT on Business Card page

---

## Summary Table

| Feature | UX Impact | Design Fit | Effort | Priority | Recommendation |
|---------|-----------|------------|--------|----------|----------------|
| C199 Bear vs Bull | High | ⚠️ | 8-12h | P2 | ✅ Top 3 |
| C200 What If Calculator | High | ⚠️ | 10-14h | P2 | 🔶 Phase 2 |
| C201 Daily Market Story | **Very High** | ✅ | 12-16h | **P1** | ✅ **#1 Pick** |
| C202 Story Arc Labels | Medium-High | ✅ | 8-10h | P2 | 🔶 Phase 2 |
| C203 Supply Chain Map | Medium | ⚠️ | 14-18h | P2 | ❌ Defer |
| C204 Confidence Indicator | **High** | ✅ | **4-6h** | P2 | ✅ **#2 Pick** |
| C205 Read Time | Medium | ✅ | **2-4h** | P2 | ✅ Bundle w/ C201 |
| C206 Recurring Investment Ed | Medium-High | ✅ | 6-8h | P2 | 🔶 Phase 2 |

---

## Design Risks Summary

1. **Advisor Boundary Risk** (C199, C200, C206): All features that discuss investment outcomes must include prominent historian disclaimers. The line between "education" and "advice" is thin.

2. **Mobile Responsiveness** (C199, C203): Side-by-side card layouts and node diagrams may break on mobile. All features must have stacked fallback layouts.

3. **Content Quality Risk** (C201, C202): Auto-generated content must meet quality bar. Stale or generic content damages credibility more than no content.

4. **D-003 Regression Risk** (C200, C203): Interactive controls and custom visualizations may tempt inline HTML. All UI must use shared components from `_router_base.py`.

5. **Scope Creep** (C206): Educational content must stay educational. Any feature drift toward "tools" or "calculators" crosses into advisory territory.

---

*Design Review completed: 2026-06-15*
*Next review: Round 47 (after Sprint 21 completion)*
