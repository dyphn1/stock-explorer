# Design Review: Sprint 19 Features (C147, C152, C140)

> **Reviewer**: Design Reviewer
> **Date**: 2026-06-14
> **Scope**: C147 (Historical Event Pattern), C152 (Multi-Factor Event Narratives), C140 (Historical Case Study Library)
> **Sprint Budget**: 34-42h (C147: 14-18h + C152 spike + C140 content)

---

## 1. Product Vision Alignment

Stock Explorer's vision is **"Historian, not a stock picker"** — explain what happened, not what to buy. Three core design principles govern all features:

1. **PPT-style presentation**: one key point per page, images lead text supports
2. **Ten-second test**: a beginner can restate the core concept within 10 seconds
3. **Historian tone QA gate**: factual past-tense only, no investment advice words

All three Sprint 19 features are **strongly aligned** with this vision — they represent the deepest execution of the "historian" positioning to date. C147 and C152 directly operationalize the historian framing ("when this happened before, here's what followed"), while C140 creates the educational infrastructure that makes the historian positioning credible.

However, these three features also carry the **highest advice-perception risk** in the product's history. Historical pattern matching (C147) and multi-factor narratives (C152) can easily be interpreted as predictive signals. The design must be meticulously crafted to maintain the historian boundary.

---

## 2. Feature-by-Feature Evaluation

### 2.1 C147 — Historical Event Pattern ("When This Happened Before, Here's What Followed")

**UX Impact Score: 9/10** — This is the single most impactful feature planned for Sprint 19, and potentially the most impactful feature since the PPT-style redesign. It directly addresses the #1 beginner question: "What usually happens next?"

Currently, Stock Explorer shows events (revenue beat, institutional buying, product launch) but leaves users to draw their own conclusions. C147 closes the loop by showing historical precedents — transforming isolated data points into contextual knowledge.

#### Design Direction

| Aspect | Recommendation |
|--------|---------------|
| **Trigger** | Auto-detect when a significant event (M5-detected) has ≥3 historical precedents. Show a collapsible section below the event card — NOT a popover (too small for range-of-outcomes display). |
| **Layout** | Use `st.expander("📜 過去類似事件發生時，後續發展...")` placed directly below the triggering event card in the event dashboard. The expander pattern keeps the main page clean while making historical context one click away. |
| **Content structure** | Three-part layout inside the expander: (1) **Header**: "過去N次類似事件" with date range, (2) **Range chart**: Plotly bar/box chart showing the range of outcomes (min/max/median) at 1-month, 3-month, 6-month intervals, (3) **Outcome cards**: 2-3 individual historical cases as compact cards with date, event description, and outcome. |
| **Range-of-outcomes display** | CRITICAL: Must show the FULL range, not just the average. Use a bar chart with error bars or a box-and-whisker plot. Green bars for positive outcomes, red for negative, gray for neutral. The visual must communicate: "historical outcomes varied widely" — never imply a single expected outcome. |
| **Disclaimer** | Mandatory historian disclaimer at the top of the expander: `st.caption("⚠️ 歷史表現不代表未來結果。以下僅供參考，不構成任何投資建議。")` — rendered in `#7F8C8D` at 0.75rem. |
| **Component** | New `_historical_pattern_section()` helper in `_router_base.py`. Reuses `_section_title()` for the header. Uses Plotly for the range chart (transparent background, matching existing chart specs). |
| **Color usage** | Green `#27AE60` for positive historical outcomes, Red `#E74C3C` for negative, Blue `#3498DB` for the median line. No other colors. Follows existing color system rules. |
| **Empty state** | When <3 historical precedents exist, show `st.info("歷史資料不足，無法分析模式")` inside the expander. Never fabricate patterns from insufficient data. |

#### Competitor Reference

- **Quiver Quantitative** (Round 24): "When Congress bought X, Y happened" — Quiver's historical trade analysis shows the pattern of "when this type of trade occurred before, here's the average outcome." Stock Explorer should adopt the same pattern but with a WIDER range display (Quiver shows averages; we must show ranges to maintain historian positioning).
- **Spiking** (Round 22): "Why Stock Moved" AI explanations — Spiking shows historical correlations between events and price movements. Stock Explorer should go further by showing the RANGE of outcomes, not just the most common one.
- **Simply Wall St** (Round 9): "Future Growth Estimates" with confidence intervals — Simply Wall St shows analyst estimates as ranges (bull/base/bear). This visual pattern maps directly to our range-of-outcomes display.
- **Public.com** (Round 8): Story cards with historical context — Public.com embeds historical precedents within story cards. Stock Explorer's expander approach is more appropriate for our PPT-style (less dense, more focused).

#### UX Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Advice perception** — Users interpret historical patterns as predictions | 🔴 CRITICAL | Mandatory disclaimer + range-of-outcomes display (never single-point estimates) + past-tense framing throughout. Tone QA blocklist must cover "通常會," "往往會," "預期." |
| **Information overload** — Range charts + outcome cards + disclaimer = dense expander | 🟡 MEDIUM | Limit to 3 outcome cards max. Range chart must be simple (3 time horizons × outcome range). No individual stock charts inside the expander. |
| **False precision** — Showing exact percentages for historical outcomes implies predictive accuracy | 🟡 MEDIUM | Round percentages to whole numbers. Use "約X%" framing. Show confidence level: "基於N筆歷史資料" prominently. |
| **Small sample size** — 3-5 historical precedents is statistically weak | 🟡 MEDIUM | Require minimum 3 precedents to display. Show sample size prominently. When N<5, add "樣本數較少，參考價值有限" note. |
| **Survivorship bias** — Only showing companies that survived, not those that delisted | 🟢 LOW | Acknowledge in disclaimer: "以上資料僅包含目前仍上市的公司" |

#### Integration with Existing UI

- **Event Dashboard page**: C147 renders as an expander below existing event cards. No new page needed.
- **M5 event detection**: C147 is triggered by M5-detected events. The existing `market_event_service.py` provides the event data; a new `historical_pattern_service.py` provides the historical matching.
- **Shared components**: Reuses `_section_title()` for the expander header, `_info_card()` for individual outcome cards, and the existing Plotly chart infrastructure.
- **Tone QA**: All C147 content (event descriptions, outcome summaries, disclaimer) must pass the existing tone QA blocklist. Add new blocklist entries: "通常會," "往往會," "預期," "可能會上漲," "可能會下跌."
- **Zone compliance**: C147 content appears in Zone C (main content area) only. No navbar or sidebar changes.

#### Ten-Second Test

**PASS** — "過去3次營收優於預期後，股價在1個月內上漲5-15%，但也有下跌2%的情況" — a beginner can restate: "sometimes it went up, sometimes it went down." The range display reinforces the historian message: history shows possibilities, not predictions.

---

### 2.2 C152 — Multi-Factor Event Narratives (One Story, All Factors Combined)

**UX Impact Score: 8/10** — This is the natural evolution of C143 (Implication Sentence) and C149 (So What? Box). Where C143 added a single implication sentence to individual delta cards, C152 weaves multiple factors into a coherent narrative. This is the feature that transforms Stock Explorer from "data display with explanations" to "historian that tells stories."

However, C152 is also the **highest-risk feature** for advice perception. A narrative that combines multiple factors ("revenue up + institutional buying + new product launch") inherently sounds like a bullish thesis. The design must carefully maintain the historian boundary.

#### Design Direction

| Aspect | Recommendation |
|--------|---------------|
| **Trigger** | Auto-generate when ≥2 significant events (M5-detected, severity ≥ medium) occur within a 30-day window for the same stock. |
| **Layout** | New section at the TOP of the event dashboard page (below `_section_title()` but above individual event cards). Use a full-width card with a light gray background (`#F8F9FA`) and blue left border (`4px solid #3498DB`) — matching the existing info card pattern. |
| **Content structure** | Three-part card: (1) **Headline**: "📖 近期事件總覽" — one sentence summarizing the combined narrative, (2) **Factor bullets**: 2-4 bullet points, each linking to the detailed event card below, (3) **Historian framing sentence**: "以上事件同時發生，值得持續觀察其後續發展。" — factual, non-predictive. |
| **Narrative generation** | Template-based (NOT LLM) for Sprint 19. Use `TemplateExplanationProvider` with a new multi-factor template. The template combines event types into a coherent paragraph using historian-framed transitions: "同時," "此外," "值得注意的是." |
| **Component** | New `_narrative_card()` helper in `_router_base.py`. Renders as an info card variant with a special "narrative" mode. Reuses existing card HTML pattern. |
| **Progressive disclosure** | The narrative card is the SUMMARY. Users click individual factor bullets to scroll to the detailed event card. This follows the PPT-style principle: one key point per page, with drill-down available. |
| **Empty state** | When <2 co-occurring events, no narrative card appears. The event dashboard shows individual cards only. No placeholder or "not available" message needed. |

#### Competitor Reference

- **Public.com** (Round 8): "Story Cards" — Public.com combines multiple data points into a single narrative card at the top of each stock page. Stock Explorer's narrative card follows the same pattern but with stricter historian framing.
- **Spiking** (Round 22): "Why Stock Moved" — Spiking's AI combines multiple factors into a single explanation. Stock Explorer should be more conservative: show the factors AND the narrative, letting users draw their own conclusions.
- **Copilot Money** (Round 24): "Money Insights" — Copilot generates daily narrative summaries of financial changes. Stock Explorer's narrative card is analogous but event-triggered rather than time-triggered.
- **Stocksera** (Round 8): "Story" tab — Stocksera has a dedicated "Story" tab per stock. Stock Explorer's approach (narrative card within event dashboard) is more integrated and less siloed.
- **FinChat** (Round 20): AI-powered multi-factor analysis — FinChat combines fundamental, technical, and sentiment factors. Stock Explorer should focus on EVENT factors only (not technical/sentimental) to maintain the historian positioning.

#### UX Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Advice perception** — Multi-factor narrative sounds like a thesis | 🔴 CRITICAL | Mandatory historian framing sentence at the end. Template QA gate. Blocklist: "買入信號," "賣出信號," "看多," "看空," "利多," "利空." |
| **Narrative overload** — Multiple narrative cards on the same page | 🟡 MEDIUM | Limit to ONE narrative card per page (the most recent/relevant combination). If multiple combinations exist, show only the one with the most factors. |
| **Generic narratives** — Template-generated text feels hollow without stock-specific context | 🟡 MEDIUM | Thread industry context through `ExplanationRequest.context` (D-097 fix from Sprint 18). At minimum, include the company's industry in the narrative template. |
| **False causality** — Combining events implies they're related | 🟡 MEDIUM | Use "同時發生" (occurred simultaneously) framing, not "因為...所以..." (because...therefore...) framing. The narrative describes coincidence, not causation. |
| **Tone violation** — Narrative tone is harder to control than single-sentence tone | 🟡 MEDIUM | All narrative templates must pass tone QA BEFORE implementation. Pre-write all possible narrative combinations and audit each one. |

#### Integration with Existing UI

- **Event Dashboard page**: C152 renders as a new section at the top of the existing event dashboard. No new page needed.
- **M5 event detection**: C152 uses the same M5 event data as C147. The `market_event_service.py` provides event data; a new `narrative_service.py` handles multi-factor combination logic.
- **Shared components**: New `_narrative_card()` helper follows the same HTML pattern as `_info_card()`. Reuses `_section_title()` for the section header.
- **C143/C149 relationship**: C152 is the "macro" version of C143's "micro" implication sentences. Where C143 adds implication to a single delta card, C152 adds narrative across multiple cards. They complement each other: C152 at the top of the page, C143 on individual cards.
- **Tone QA**: All narrative templates must be pre-audited. Add new blocklist entries: "買入信號," "賣出信號," "看多," "看空," "利多," "利空," "強烈建議."
- **Zone compliance**: C152 content appears in Zone C only.

#### Ten-Second Test

**PASS** — "台積電最近同時發生：營收優於預期、外資買擴、新產品量產。以上事件同時發生，值得持續觀察其後續發展。" — a beginner can restate: "several good things happened at the same time, and we should watch what happens next." The historian framing ("observe what happens next") is key — it tells the user WHAT happened, not WHAT TO DO.

---

### 2.3 C140 — Historical Case Study Library

**UX Impact Score: 7/10** — This is the most strategically important feature for long-term positioning but has the lowest immediate UX impact. The Case Study Library is the infrastructure that makes the "historian" positioning credible: it's not just a tagline, it's a browsable collection of curated historical knowledge.

For Sprint 19, C140 is primarily a content creation task (6-8h of the 16-22h estimate). The UI is relatively simple; the value is in the curated content.

#### Design Direction

| Aspect | Recommendation |
|--------|---------------|
| **Page location** | New tab in Zone A navbar: "案例庫" (Case Library). This is a top-level navigation item, alongside existing tabs. Position it after "Event Dashboard" to maintain the logical flow: company data → events → historical cases. |
| **Page layout** | Zone C only. Two sections: (1) **Search/filter bar** at the top (industry dropdown + keyword search), (2) **Case card grid** below (2-column grid of case study cards). |
| **Case card design** | Compact card pattern: `background:#F8F9FA; border-radius:12px; padding:1rem; border-left:4px solid #3498DB;` — matching existing info card style. Each card shows: (1) case title (e.g., "2018年台積電蘋果訂單流失事件"), (2) industry tag + date range, (3) one-line summary (max 30 Chinese characters), (4) "閱讀更多 →" link to full case detail. |
| **Case detail page** | Clicking a case card navigates to a detail page (new route). Layout: (1) title + metadata, (2) "背景" section (what happened), (3) "發展" section (what followed), (4) "啟示" section (historian-framed lessons — NOT investment advice). Each section uses `_section_title()` and follows PPT-style text limits. |
| **Search/filter** | Industry dropdown (`st.selectbox`) + keyword search (`st.text_input`). Search is client-side filtering of pre-loaded YAML data — no API calls. |
| **Data source** | New `case_studies.yaml` (separate from existing `case_studies.yaml` if it exists — verify and extend). Schema: `title, industry, date_range, summary, background, development, lessons, related_stocks[], sources[]`. |
| **Content quality gate** | Every case study must pass: (1) tone QA blocklist, (2) historian framing review (past tense, factual), (3) source attribution (at least 2 sources per case), (4) "啟示" section must use "觀察" framing, not "建議" framing. |
| **Empty state** | When no cases match filter: `st.info("沒有找到符合條件的案例，請嘗試其他關鍵字或產業。")` |
| **Component** | New `_case_card()` helper in `_router_base.py`. Follows existing card HTML pattern. New `case_study_service.py` for data loading and filtering. |

#### Competitor Reference

- **Morningstar** (Round 9): "StockReport" — Morningstar's detailed analysis reports are the gold standard for structured case studies. Stock Explorer's case format (background → development → lessons) mirrors Morningstar's report structure but in a more concise, PPT-style format.
- **財報狗 (StatementDog)** (Round 9): Blog posts + analysis — 財報狗 has informal case studies in blog format. Stock Explorer's structured YAML approach is more systematic and searchable.
- **Investopedia** (Round 9): "Financial Dictionary" + Academy — Investopedia's encyclopedia model is the inspiration for a browsable, searchable knowledge base. Stock Explorer's case library is a domain-specific (TW stocks) version of Investopedia's concept-first approach.
- **Stockopedia** (Round 9): "StockReport" + "Stockopedia Academy" — Stockopedia combines structured reports with educational progression. Stock Explorer's case library should eventually link to a learning path (C142 Glossary Gate), but for Sprint 19, standalone cases are sufficient.
- **股感知識庫** (Round 11): Knowledge base — 股感 has a knowledge base but without structured progression or historian framing. Stock Explorer's structured YAML + tone QA approach is a clear differentiator.

#### UX Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Content quality** — Poorly written cases undermine credibility | 🔴 CRITICAL | Pre-write ALL cases before Sprint 19 development. Apply the 4-point quality gate (tone, framing, sources, "啟示" framing). Minimum 10 cases for launch. |
| **Advice perception** — "啟示" (lessons) section can easily become advice | 🔴 CRITICAL | "啟示" must be historian-framed: "從這個案例可以觀察到..." not "投資人可以學習到..." Tone QA blocklist applies to ALL case content. |
| **Content maintenance** — Cases become outdated | 🟡 MEDIUM | Include "last reviewed" date in metadata. Plan quarterly content reviews. Start with evergreen cases (multi-year patterns) rather than recent events. |
| **Discovery** — Users don't know the case library exists | 🟡 MEDIUM | Add a "📚 相關案例" link from event dashboard cards to relevant case studies. Cross-linking drives discovery. |
| **Scope creep** — 16-22h estimate includes content creation, which is unpredictable | 🟡 MEDIUM | Separate dev (8-10h for UI/service) from content (6-8h for 10 cases). If content isn't ready, ship the UI with 5 cases and add more in Sprint 20. |

#### Integration with Existing UI

- **New page**: C140 requires a new page (`case_library.py`) and a new route. Registered in the router with URL sync.
- **Navbar tab**: New "案例庫" tab in Zone A. Follows existing tab styling (bold for active, `st.button` for others).
- **Cross-linking**: Event dashboard cards (C147/C152) should link to relevant case studies. Add a "📚 相關案例" button to event cards that have matching cases.
- **Shared components**: Reuses `_section_title()`, `_info_card()` (as `_case_card()` variant), and existing Plotly chart infrastructure for any charts within case studies.
- **Tone QA**: All case study content must pass the existing tone QA blocklist. The `tests/test_tone_qa.py` scanner should be extended to scan `case_studies.yaml` in addition to `.py` files.
- **Zone compliance**: Search/filter in Zone C top, case grid in Zone C body. Navbar tab in Zone A. No sidebar changes.

#### Ten-Second Test

**PASS** — A case card shows: "2018年台積電蘋果訂單流失事件 — 當最大客戶訂單減少時，台積電的營收和股價如何變化？" — a beginner can restate: "this is a story about what happened when TSMC lost Apple's order." The case library is inherently narrative, which aligns perfectly with the historian positioning.

---

## 3. Cross-Feature Interaction Map

```
┌─────────────────────────────────────────────────────────────────┐
│  Zone A: Navbar                                                  │
│  [Business Card] [Events] [案例庫 ← NEW] [Peer Comparison] ...   │
├─────────────────────────────────────────────────────────────────┤
│  Zone C: Event Dashboard                                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [C152] 📖 近期事件總覽                                    │  │
│  │ 台積電最近同時發生：營收優於預期、外資買擴、新產品量產。  │  │
│  │ 以上事件同時發生，值得持續觀察其後續發展。                │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Event Card] 營收優於預期 +15%                             │  │
│  │ 💡 [C141 source badge]                                    │  │
│  │ [C143 implication sentence]                                │  │
│  │ [C149 So What? Box — if 2+ deltas active]                 │  │
│  │                                                           │  │
│  │ 📜 過去類似事件發生時，後續發展... [C147 expander]         │  │
│  │   ├─ Range chart: 1mo +5%~+15%, 3mo -2%~+20%           │  │
│  │   ├─ Outcome card 1: 2023/02 營收優於預期 → +8% (1mo)   │  │
│  │   ├─ Outcome card 2: 2022/08 營收優於預期 → +12% (1mo)  │  │
│  │   └─ Outcome card 3: 2021/11 營收優於預期 → -2% (1mo)   │  │
│  │   ⚠️ 歷史表現不代表未來結果                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Event Card] 外資買擴 500張                                │  │
│  │ 📚 相關案例 → [C140 case study link]                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Zone C: Case Library (NEW PAGE)                                 │
│  [Search: ________] [Industry: 半導體 ▼]                        │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │ 2018年台積電        │  │ 2020年聯發科        │                │
│  │ 蘋果訂單流失事件    │  │ 5G晶片需求爆發      │                │
│  │ 半導體 | 2018-2019  │  │ 半導體 | 2020-2021  │                │
│  │ 當最大客戶訂單減少  │  │ 當5G需求突然爆發    │                │
│  │ 時，台積電的...     │  │ 時，聯發科的...     │                │
│  │ 閱讀更多 →          │  │ 閱讀更多 →          │                │
│  └────────────────────┘  └────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

All three features form a cohesive narrative layer: C152 provides the "big picture" narrative across events, C147 provides the "historical precedent" context for individual events, and C140 provides the "deep dive" case studies for broader patterns. Together, they transform the event dashboard from a data list into a historian's workspace.

---

## 4. Priority & Sequencing Recommendation

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **P0** | C147 (Historical Event Pattern) | HUX impact (9/10). Directly addresses the #1 beginner question. Builds on existing M5 + event infrastructure. 2h feasibility spike required before committing. |
| **P1** | C140 (Case Study Library) | Strategic infrastructure for "historian" positioning. Content creation can start NOW (pre-write cases during C147 spike). UI is straightforward. |
| **P2** | C152 (Multi-Factor Narratives) | Highest UX impact (8/10) but also highest risk. Requires C143/C149 to be stable first. Recommend SPIKE only in Sprint 19, full implementation in Sprint 20. |

**Suggested Sprint 19 execution order**:
1. **C147 feasibility spike** (2h) — Validate historical data availability and pattern matching approach
2. **C140 content creation** (6-8h, parallel with spike) — Pre-write 10 case studies
3. **C147 implementation** (12-16h, post-spike) — Build the historical pattern section
4. **C140 UI implementation** (8-10h) — Build the case library page
5. **C152 spike** (2-4h) — Validate narrative generation approach, defer full implementation

**Total: 30-40h** (within the 34-42h budget, with C152 spike replacing full implementation)

---

## 5. Scope Adjustments Recommended

1. **Defer C152 full implementation to Sprint 20** — C152 is the highest-risk feature and depends on C143/C149 being stable (shipping in Sprint 18). A 2-4h spike in Sprint 19 validates the approach without committing to full implementation. Sprint 20 can deliver C152 with more mature tone QA infrastructure.

2. **Start C140 content creation NOW** — The 40% content rule applies: 6-8h of C140's 16-22h is content. Pre-writing 10 case studies during the C147 spike ensures the UI ships with substantive content. Target: 10 cases covering 5 industries (semiconductor, finance, retail, tech, energy).

3. **Expand tone QA blocklist for Sprint 19** — C147 and C152 introduce new advice-perception vectors. Add to blocklist: "通常會," "往往會," "預期," "可能會上漲," "可能會下跌," "買入信號," "賣出信號," "看多," "看空," "利多," "利空," "強烈建議." Update `tests/test_tone_qa.py` to scan `case_studies.yaml` and narrative templates.

4. **Require C147 feasibility spike before committing** — The 2h spike should validate: (a) historical data availability for pattern matching (minimum 3 precedents for at least 10 event types), (b) Plotly range chart rendering within Streamlit expanders, (c) performance of historical matching algorithm (<200ms). If any of these fail, reduce C147 scope to "top 5 event types only."

5. **Cross-link C140 with C147/C152** — Add "📚 相關案例" links from event cards to relevant case studies. This drives discovery of the case library and creates a cohesive narrative layer. Budget 1-2h for cross-linking logic.

---

## 6. Design Verdict

| Feature | Vision Alignment | Ten-Second Test | Historian Tone | Risk | Score |
|---------|-----------------|-----------------|---------------|------|-------|
| C147 | ✅ Strong | ✅ Pass | ⚠️ Needs expanded blocklist | High (advice perception) | **9/10** |
| C152 | ✅ Strong | ✅ Pass | ⚠️ Needs pre-audit | Very high (narrative = thesis) | **8/10** |
| C140 | ✅ Strong | ✅ Pass | ⚠️ Needs content gate | Medium (content quality) | **7/10** |

**Overall: APPROVE with conditions.**

- **C147**: Approved with prerequisite — 2h feasibility spike must validate data availability before full implementation. Expanded tone QA blocklist required.
- **C152**: Approved for SPIKE ONLY in Sprint 19. Full implementation deferred to Sprint 20. This reduces risk and allows C143/C149 to stabilize.
- **C140**: Approved with prerequisite — content creation must start immediately (10 cases pre-written before UI development begins). Ship with minimum 10 cases.

**Sprint 19 revised budget**: C147 (14-18h with spike) + C140 (16-22h with content) + C152 spike (2-4h) = **32-44h**. This is within the original 34-42h budget when accounting for C152 deferral.

---

## 7. Design Recommendations for Sprint 19

### Immediate Actions (Before Development)

1. **Expand tone QA blocklist** — Add 12 new entries for C147/C152 advice vectors. Update `tests/test_tone_qa.py` to scan YAML content files.
2. **Pre-write 10 case studies** — Start content creation NOW. Use the 4-point quality gate. Cover 5 industries.
3. **Run C147 feasibility spike** — Validate data availability, chart rendering, and performance.
4. **Design C152 spike plan** — Define the scope of the narrative generation spike (template design, tone pre-audit, cross-linking logic).

### Design Patterns to Reuse

| Existing Component | Sprint 19 Usage |
|-------------------|-----------------|
| `_section_title()` | C147 expander header, C152 narrative section, C140 page sections |
| `_explain_button()` | C147 outcome cards (💡 for detailed explanations) |
| `_so_what_box()` | C152 narrative card (extended for multi-factor) |
| `_info_card()` | C147 outcome cards, C140 case cards (as `_case_card()` variant) |
| `st.popover()` | C147 outcome card detail (if needed) |
| `st.expander()` | C147 historical pattern section |
| Plotly charts | C147 range-of-outcomes chart, C140 case detail charts |
| Tone QA scanner | Extended to scan C147/C152/C140 content |

### Design Patterns to Create

| New Component | Usage | Reuse of Existing |
|--------------|-------|------------------|
| `_historical_pattern_section()` | C147 expander with range chart + outcome cards | `_section_title()`, `_info_card()`, Plotly |
| `_narrative_card()` | C152 multi-factor narrative card | `_info_card()` HTML pattern |
| `_case_card()` | C140 case study grid cards | `_info_card()` HTML pattern |
| `_disclaimer_badge()` | C147/C152 historian disclaimer | New — `st.caption()` with warning styling |

### Color System Compliance

All three features use only the approved color palette:
- **Blue `#3498DB`**: Card borders, median lines, clickable elements
- **Green `#27AE60`**: Positive historical outcomes, "啟示" section headers
- **Red `#E74C3C`**: Negative historical outcomes, disclaimer icons
- **Light gray `#F8F9FA`**: Card backgrounds
- **Dark gray `#2C3E50`**: Primary text
- **Gray `#7F8C8D`**: Secondary text, disclaimers, captions

No new colors introduced. ✅

### Inline HTML Budget

Current: 11 instances (stable, CI enforced). Sprint 19 additions:
- `_historical_pattern_section()`: 1 new instance (card HTML)
- `_narrative_card()`: 1 new instance (card HTML)
- `_case_card()`: 1 new instance (card HTML)
- `_disclaimer_badge()`: 1 new instance (caption HTML)

**Projected total: 15 instances** — still within acceptable range. CI enforcement prevents uncontrolled growth.

---

## 8. Ten-Second Test Assessment

### C147 — Historical Event Pattern
**PASS ✅** — A beginner sees the expander "📜 過去類似事件發生時，後續發展..." and can immediately understand: "this will show me what happened before in similar situations." After opening: "sometimes the stock went up 5-15%, sometimes it went down 2%." The range display reinforces the historian message: history shows possibilities, not predictions.

**Key metric**: Can a beginner restate the core concept in 10 seconds? "過去類似情況下，股價有漲有跌，沒有一定。" — YES.

### C152 — Multi-Factor Event Narratives
**PASS ✅** — A beginner sees the narrative card at the top of the event dashboard and can immediately understand: "this is a summary of what's been happening recently." The historian framing sentence ("值得持續觀察其後續發展") tells the user what to do with this information: observe, not act.

**Key metric**: Can a beginner restate the core concept in 10 seconds? "最近有幾件重要的事同時發生，我們可以繼續觀察。" — YES.

### C140 — Historical Case Study Library
**PASS ✅** — A beginner sees the case library tab and can immediately understand: "this is a collection of stories about what happened to companies in the past." Each case card's one-line summary is inherently narrative: "當最大客戶訂單減少時，台積電的營收和股價如何變化？"

**Key metric**: Can a beginner restate the core concept in 10 seconds? "這是一個圖書館，裡面有很多公司過去發生過的故事。" — YES.

### Overall Ten-Second Test: PASS ✅

All three features pass the ten-second test individually and collectively. They reinforce the historian positioning by providing historical context (C147), narrative synthesis (C152), and curated knowledge (C140) — all without crossing into advisory territory.

---

## 9. Competitive Differentiation Summary

| Feature | Competitors Have | Stock Explorer's Differentiation |
|---------|-----------------|--------------------------------|
| C147 Historical Patterns | Quiver Quantitative (averages), Spiking (correlations) | Range-of-outcomes display (not averages), mandatory historian disclaimer, strict past-tense framing |
| C152 Multi-Factor Narratives | Public.com (story cards), Copilot Money (AI insights) | Template-based (not LLM) for tone control, historian framing sentence, event-triggered (not time-triggered) |
| C140 Case Study Library | Morningstar (reports), Investopedia (encyclopedia) | TW-market focus, structured YAML + tone QA, cross-linked with event dashboard, historian-framed "啟示" |

Stock Explorer's unique advantage is the **combination** of all three features with strict historian tone QA. No competitor combines historical pattern matching + multi-factor narratives + curated case studies under a unified "historian, not stock picker" positioning. This is the white space that Sprint 19 owns.

---

*Design Reviewer, Sprint 19 — 2026-06-14*
