## 2026-06-14 Design Review — Round 33 Discussion: Post-Sprint 15 Feature Directions

> **Author**: Design Reviewer
> **Context**: Sprint 15 planned (D6 YAML migration → chart.py split → CI check → C101 Comprehension Check Quiz). Evaluating 2-3 feature directions for the development cycle AFTER Sprint 15.
> **Scope**: UX impact evaluation and design direction for next-cycle features, referencing design system (docs/design/design_system.md), competitor research (docs/research/competitor_research.md), issue tracker (docs/state/issues.md), and product vision (docs/domain/product_vision.md).

---

## Current Design State Assessment

### What's Shipping in Sprint 15
- **D6 YAML migration**: Infrastructure, no UX impact
- **chart.py split**: Architecture cleanup, no direct UX impact
- **CI check**: Quality infrastructure, no UX impact
- **C101 Comprehension Check Quiz**: First interactive assessment feature — extends the education mission with active recall

### Design System Maturity
The design system is well-established after 30+ rounds of iteration. Core Zone A/B/C architecture is stable. PPT-style principles (one key point per page, charts > text, 200-char limit) are consistently enforced. The Event Dashboard (A-) sets the quality benchmark. Business Card page carries 15+ sections (D-005 "super page" risk remains open but managed).

### Key Design Debt Entering Next Cycle
1. **D-005**: Business Card page overload (15+ sections) — needs consolidation, not more sections
2. **D-003**: Card styling consistency (partially fixed, potential regressions with new pages)
3. **D-006**: Mobile responsiveness gaps (longstanding)
4. **ISSUE-DR-01**: 13+ non-palette colors may have regressed during Sprint 14 additions
5. **ISSUE-DR-06**: Financial Health page still worst-graded core page (C+)

---

## Feature Direction Evaluations

After reviewing competitor research rounds 1-11, issue tracker (47 issues, 14 P0/P1 gaps), and product vision alignment, I've selected **3 feature directions** for post-Sprint 15 development. These are ordered by UX impact × "historian" alignment ÷ implementation cost.

---

### Feature Direction 1: C28 — Company Story Timeline (Narrative Thread)

**Summary**: Add a "Company Story" tab weaves events, revenue milestones, and price movements into a chronological narrative with plain-language explanations. "Here's what happened to TSMC in the last 3 years, told as a story."

#### UX Impact: **HIGH**

- **Beginner Experience**: This is THE most impactful feature for beginners because it transforms disconnected data into a coherent narrative. The product vision explicitly calls out "Lack of narrative: Piles of data withoutcontext" as pain point #4. When a beginner opens TSMC's page and sees a story — "TSMC started making chips for Apple in 2010, then NVIDIA needed AI chips in 2023, and that's why revenue grew 40%" — they remember it. Data is forgettable; stories are not.

- **Ten-Second Test**: A well-designed story timeline passes the ten-second test perfectly. A beginner glancing at the "Turning Points" section should immediately understand the 2-3 most important moments in the company's recent history. "TSMC's big moment: When AI exploded in 2023, everyone needed their chips."

- **PPT-Style Alignment**: One story, told chronologically, with visual turning points. This IS PPT-style — each "turning point" is one slide in the story. Charts show the data that matters (revenue at each milestone), text provides ≤ 200 chars of narrative context per point.

- **Design System Alignment**: ✅ Zone A (navbar adds "📖 故事" tab), ✅ Zone B (sidebar unchanged), ✅ Zone C (story content area). Uses existing card components (info cards for turning points, tip cards for "why this mattered"). Color system unchanged.

#### Competitive Reference

- **StockStory** (Singapore, 2025): AI-generated narratives for TW stocks with "Turning Points" timeline — direct overlap with our "historian" positioning
- **Stockopedia AI** (2025 relaunch): "AI Stock Story" + "TW Market Education Hub" in Traditional Chinese
- **Public.com**: Story cards that connect companies to current events
- **Seeking Alpha**: "Story" tab per stock + narrative summaries
- **Stocksera**: "Compare Stories" side-by-side mode
- **Key Insight**: AI-generated company narratives are becoming table stakes internationally. Stock Explorer must own this space with our unique angle: explain what happened, don't predict what will happen.

#### Design Direction & Recommendations

**Placement: New Zone A tab "📖 故事"** — This is a top-level navigation item alongside Business Card, Operational Checkup, etc. The story is fundamental enough to warrant first-level access.

**Page Structure** (PPT Story Format):
```
Zone A: Navbar
  Tabs: [Business Card] [Operational Checkup] [Financial Health] [📖 故事] [Peer Comparison] ...

Zone C: Story Content Area
  1. Hero Card: "📖 {Company}的故事" + one-line narrative summary (≤ 50 chars)
     Example: "從晶圓代工到AI帝國：台積電如何成為全球最重要的科技公司"

  2. Turning Points Timeline (visual Gantt-style):
     ├── 📌 2020: 開始量產5nm晶片 → 營收成長25%
     ├── 📌 2022: 美國亞利桑那州建廠 → 地緣政治風險管理
     ├── 📌 2023: AI需求爆發 → NVIDIA訂單增長300%
     └── 📌 2024: 3nm量產 → 蘋果全面採用
     Each point: icon + date + event label + impact metric

  3. "故事更新" Card (last 90 days):
     Auto-generated from M5 event detection engine
     "最近90天內，台積電發生了3件重要事件..."
     Max 3 events, plain-language, ≤ 100 chars each

  4. "為什麼重要" Explanation Card:
     Connects story to current business state
     "這些事件告訴我們：台積電的成功來自技術領先 + 大客戶信任"

  5. "📖 接著看" (optional, see Feature Direction 3):
     Cross-link to related company stories
```

**Design Constraints**:
- Maximum 8 turning points per company (PPT-style: don't overload)
- Timeline chart horizontally scrollable (follows existing Gantt chart pattern from design system Section 3.4)
- Each turning point card: ≤ 100 chars total (event + impact)
- Chart proportion: Timeline chart occupies > 60% of page area
- Use existing card components: `_info_card()`, `_render_tip_card()`
- Color system: Turning point markers use `#3498DB` (blue, clickable), `#F39C12` for "highlight" moments (orange, important), `#27AE60` for positive outcomes

**Integration with Existing Systems**:
- Reuses M5 event detection data (already captures events with timestamps)
- Reuses `analogy_engine.py` for plain-language metric explanations at each turning point
- Reuses existing chart patterns (Gantt chart code from timeline_controls.py)
- Optional: Extend events.yaml schema (ISSUE-NEW-G18) with `narrative_category` field

**Exclusion: Do NOT build "Compare Stories" yet.** C38 is valuable but complex. Start with single-company narrative, validate with users, then add comparison mode.

#### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| Historian, not stock picker | ✅ Perfect — explains what happened, never predicts |
| PPT-style | ✅ One story, visual timeline, minimal text |
| Ten-second test | ✅ Hero card + 3 turning points = instant understanding |
| Beginner-friendly | ✅ Plain-language narrative, no jargon |
| Zone A/B/C | ✅ Tab in Zone A, content in Zone C, no zone mixing |

---

### Feature Direction 2: C29 — AI-Powered "Explain Any Metric" Inline Explanations

**Summary**: Add an "Explain" button (ℹ️ icon) next to every financial metric across all pages. Clicking opens a contextual plain-language explanation: what the metric means, how to interpret the current value, industry benchmark, and a real-world analogy.

#### UX Impact: **HIGH**

- **Beginner Experience**: This is the single most impactful incremental improvement for beginners because it addresses the #1 pain point: "Information overload but insufficient understanding" (product vision pain point #1). Currently, a beginner sees "ROE: 28.5%" and has to either know what it means or go search elsewhere. An inline explanation eliminates this friction entirely. The design system **requires** "All professional terms must have plain-language translations" — this feature fulfills that requirement systemically.

- **Ten-Second Test**: A beginner who doesn't know what "ROE" means can click the ℹ️ icon and understand within 10 seconds. "ROE measures how efficiently a company uses shareholder money. TSMC's 28.5% means: for every $100 of shareholder equity, TSMC generates $28.50 profit. This is excellent — the semiconductor industry average is ~15%."

- **PPT-Style Alignment**: This doesn't add visual content to pages — it adds depth on demand. The base page remains clean (one key point per page). Explanations are progressive disclosure: available but not imposed. This aligns perfectly with "progressive drill-down" in the product vision.

- **Design System Alignment**: ℹ️ icons use `#3498DB` (blue = clickable follows design system Section 3.1). Explanation tooltips/modals use existing card styling. No zone violations.

#### Competitive Reference

- **Stockopedia AI** (2025): "AI Explain" lets users highlight any metric and get a plain-language explanation with context
- **Finimize**: "Ask Finimize" AI Q&A answers natural language questions
- **Investopedia**: 10,000+ term financial dictionary (reference standard)
- **Koyfin**: Metric descriptions + dashboard narratives
- **Simply Wall St**: Short descriptions instead of jargon
- **Key Insight**: AI-powered metric explanations are becoming standard. Stockopedia AI launching "TW Market Education Hub" makes this urgent — if a competitor launches this with TW coverage first, Stock Explorer loses educational differentiation.

#### Design Direction & Recommendations

**Implementation: Two-Phase Approach**

**Phase 1 — Template-Based (12-18h, for post-Sprint 15)**:
```
ℹ️ icon next to every metric → click → popover card with:
  - What is it? (≤ 40 chars, plain-language definition)
  - What does {value} mean? (≤ 60 chars, contextual interpretation)
  - Industry benchmark: "Industry avg: X%" (where available)
  - Analogy: "Think of it like..." (≤ 40 chars, from analogy_engine.py)
```

**Phase 2 — LLM-Enhanced (post-MVP, ISSUE-C17 integration)**:
```
Same UX, but powered by LLM for:
  - More natural language variations
  - Cross-metric explanations ("Why is ROE high but debt also high?")
  - Personalized to user's knowledge level (from C40 Beginner/Expert preference)
```

**Phase 1 Technical Design**:
```python
# New service: src/services/metric_explainer.py
# - Load explanation templates from src/data/metric_explanations.yaml
# - Each metric has: definition_template, interpretation_template, analogy_key
# - Integration: Add ℹ️ icon next to every metric rendering call in all pages

# YAML structure:
# roe:
#   definition: "ROE（股東權益報酬率）衡量公司用股東的錢賺了多少利潤"
#   interpretation: "ROE {value}% 代表每100元股東資金，公司賺了{value}元"
#   analogy_key: "roE_analogy"
#   benchmark: "半導體業平均約15%"
```

**Coverage**: ISSUE-NEW-G20 flags that `analogy_engine.py` covers 8 metrics but Financial Health page uses 15+ additional. C29 Phase 1 requires extending to 30+ metrics. Prioritize:
1. Business Card page metrics (ROE, P/E, P/B, gross margin, revenue) — highest visibility
2. Financial Health page metrics (debt ratio, current ratio, net margin) — worst-graded page, highest ROI
3. All remaining metrics — comprehensive coverage

**Design Constraints**:
- ℹ️ icon: Use `#3498DB` blue, 16px, positioned immediately after metric label
- Popover card: Use existing `_render_tip_card()` styling — consistent with design system
- Popover position: Below the metric, max width 300px
- Popover dismiss: Click outside or ESC key (accessibility)
- Text limits per field: definition ≤ 40 chars, interpretation ≤ 60 chars, analogy ≤ 40 chars (maintains PPT-style brevity)
- No more than 2 sentences per field (design system Section 5.2)

**Design Patterns to Adopt**:
- Investopedia's inline definition hover (encyclopedia UX, proven)
- Stockopedia AI's contextual explanations (industry benchmark + plain-language)
- Simply Wall St's icon/tooltip pattern (consistent, discoverable)

**Design Patterns to AVOID**:
- ❌ Full-screen modal (too heavy, breaks PPT flow)
- ❌ Inline expansion (pushes content down, causes layout shift)
- ❌ Glossary page navigation (too slow, breaks reading flow)
- ❌ LLM-only explanations without template fallback (hallucination risk, cost)

#### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| Historian, not stock picker | ✅ Explains what metrics mean, not what to do |
| PPT-style | ✅ Base page stays clean, depth on demand |
| Ten-second test | ✅ Beginner understands metric in 10s after click |
| Beginner-friendly | ✅ Fulfills "plain-language translations" requirement |
| Progressive drill-down | ✅ Perfect progressive disclosure pattern |
| Zone A/B/C | ✅ No zone changes, inline enhancement |

---

### Feature Direction 3: C41 — "Read Next" Company Recommendation Engine

**Summary**: Add a "📖 接著看" section at the bottom of the Business Card page with 2-3 recommended companies based on industry relationships, parent-subsidiary connections, and customer-supplier mappings.

#### UX Impact: **MEDIUM-HIGH**

- **Beginner Experience**: This solves a fundamental discovery problem. Currently, a beginner who finishes learning about TSMC has no guided path to the next company. "Read Next" creates a learning journey: "After TSMC, learn about its biggest customer (Apple/TSM), its main competitor (UMC/聯華電子), or its parent structure (if applicable)." This transforms Stock Explorer from a single-company lookup tool into a connected knowledge graph — directly supporting "Point-to-point knowledge construction" (Core Value #4).

- **Ten-Second Test**: A beginner sees "📖 接著看" and immediately knows where to go next. "想了解台積電最大的客戶？→ 蘋果 AAPL" — three seconds to understand the recommendation and its relevance.

- **PPT-Style Alignment**: The recommendation section is a single card with 3 items. Each item: company name + relationship label + one-line reason. This is PPT-style: one key action (what to explore next), presented visually with minimal text.

- **Design System Alignment**: ✅ Placed at bottom of Zone C content, uses existing card components. No zone mixing. Blue `#3498DB` for clickable company names.

#### Competitive Reference

- **The Motley Fool**: "Related Stocks" section at bottom of analysis articles
- **Seeking Alpha**: "You May Also Like" recommendations
- **Zerodha Varsity**: Module-to-module navigation (concept-based, not company-based)
- **Sharesies** (NZ): "Discover" section with related companies
- **Key Insight**: No TW competitor has relationship-based recommendations. 財報狗, GoodInfo, and Yahoo Finance all require users to know what to search for. Stock Explorer's group structure data (parent-subsidiary relationships with ownership %) is a UNIQUE asset that no competitor has access to — this feature leverages that moat.

#### Design Direction & Recommendations

**Placement: Bottom of Business Card page, Zone C**
```
📖 接著看 — 了解完{Company}之後，你可能還想知道：
┌─────────────────┬──────────────────┬────────────────────┐
│ 🏭 主要客戶      │ 🏁 最大競爭對手   │ 🏢 同集團其他公司    │
│ 蘋果 (AAPL)     │ 聯華電子 (2303)   │ 世界先進 (5347)     │
│ 台積電25%營收    │ 晶圓代工市佔第二   │ 台積電持股 31.4%    │
│ 來源來自蘋果     │ 技術落後2年       │ 專注成熟製程        │
│ [查看故事 →]     │ [查看故事 →]      │ [查看故事 →]        │
└─────────────────┴──────────────────┴────────────────────┘
```

**Recommendation Categories** (priority order):
1. **Same peer group** (industry #2 player) — from existing peer_comparison.py data
2. **Parent-subsidiary** — from existing group_structure.py data (unique advantage)
3. **Customer-supplier** — from manual curation for top 20 stocks (high value, limited coverage)

**Design Constraints**:
- Maximum 3 recommendations (PPT-style: don't overwhelm)
- Each recommendation: company name + stock ID + relationship type + one-line reason (≤ 30 chars)
- "查看故事 →" button: blue `#3498DB`, sets `session_state["stock_id"]` + `st.rerun()`
- If data unavailable for a category, show only available categories (graceful degradation)
- Section title: "📖 接著看" — consistent with C28 Story narrative theme

**Integration with Existing Services**:
- Reuses `peer_comparison.py` for peer group data
- Reuses `group_structure.py` for parent-subsidiary data
- New: `src/services/recommendation_engine.py` for customer-supplier mappings

**Content Strategy**:
- **Phase A** (post-Sprint 15): Peer group + parent-subsidiary only (data already exists, 2-3h)
- **Phase B** (follow-up): Customer-supplier for top 20 stocks (manual curation, 3-4h)
- **Phase C** (future): Algorithmic recommendations based on user browsing history (requires user tracking, post-MVP)

#### Alignment with Design System

| Principle | Alignment |
|-----------|-----------|
| Historian, not stock picker | ✅ Recommends "learn about", not "buy" |
| PPT-style | ✅ One section, 3 items, minimal text |
| Ten-second test | ✅ Instant understanding of what to explore next |
| Beginner-friendly | ✅ Guided discovery, no need to know what to search |
| Point-to-point | ✅ Core Value #4 — connects companies through relationships |
| Progressive drill-down | ✅ Natural next step in learning journey |

---

## Feature Directions Evaluated But NOT Recommended

### C47 Education Academy — DEFERRED to Sprint 7+
- **Reasoning**: Architecturally significant (introduces second navigation paradigm). Should not be rushed into post-Sprint 15 cycle. Build C28 Story Timeline first — it's the narrative foundation that the Academy curriculum would teach THROUGH. Academy without rich company content = empty curriculum shell.
- **Prerequisite**: C28 Story Timeline + C29 Explain Any Metric must be live before Academy adds value.

### C43 Company Snowflake Health Visualization — DEFERRED pending Daniel decision
- **Reasoning**: ISSUE-C14/D06 still awaiting Daniel's scope decision (4-6h badge vs 14-20h radar). Pushing to next cycle gives time for decision.
- **If approved**: Should integrate with C28 Story Timeline (health score changes at each turning point = powerful narrative device)

### C02 Notifications — NOT a UX design priority
- **Reasoning**: All competitor research confirms this is P0 for retention, but it's infrastructure/backend work. The UX design for notifications is trivial (badge + item list). No design direction needed — build when D02 background worker architecture is resolved.

---

## Design Patterns to Adopt (From Competitor Research)

### ✅ Adopt: Zerodha Varsity's Module Progress Pattern
- Left-side progress indicator for narrative/learning content
- Stock Explorer adaptation: Timeline progress in C28, quiz progress in C101
- Exception to Zone B rule (established in Round 15, still valid)

### ✅ Adopt: Simply Wall St's Visual-First Approach
- Every metric gets a visual (gauge, chart, or icon), not just a number
- Stock Explorer adaptation: C29 ℹ️ icons make metrics explainer-friendly
- Aligns with PPT-style "charts > text" principle

### ✅ Adopt: Finimize's Explanation Depth Model
- 3 layers: headline (5 sec) → summary (30 sec) → deep dive (3 min)
- Stock Explorer adaptation: C29 follows this exactly (label → tooltip → quiz)
- Differentiator: Finimize uses AI, Stock Explorer uses verified FinMind data + templates

### ❌ Avoid: Yahoo Finance's Dense Information Model
- Wall of numbers, no visual hierarchy, ad-heavy
- This is the ANTI-PATTERN for Stock Explorer's PPT-style positioning

### ❌ Avoid: TipRanks' Score-Centric Black-Box
- Smart Score (0-10) with no plain-language explanation
- Stock Explorer differentiator: every score must be explainable ("why is ROE 28.5% good?")

### ❌ Avoid: TradingView's Feature Overload
- 100+ indicators, community features, Pine Script, social feed
- Stock Explorer discipline: one key point per page, refuse to add features that violate PPT-style

---

## Priority Order for Post-Sprint 15 Development

| Order | Feature | Est. Effort | UX Impact | Core Value | Risk |
|-------|---------|-------------|-----------|------------|------|
| 1 | **C28 Story Timeline** | 20-30h | HIGH | #1 Story first | Medium — spike-first recommended (3h to validate data pipeline) |
| 2 | **C29 Explain Any Metric** | 12-18h | HIGH | #4 Point-to-point | Low — template-based, no LLM dependency |
| 3 | **C41 Read Next** | 6-8h | MEDIUM-HIGH | #4 Point-to-point | Low — reuses existing data |

**Total effort**: 38-56h base + 50% buffer = 57-84h (~2 sprints at historical velocity)

**Recommended Sprint Plan**:
- **Sprint 16a**: C29 Phase 1 (ℹ️ icons + templates for 10 key metrics on Business Card + Financial Health pages)
- **Sprint 16b**: C41 Phase A (peer + parent-subsidiary recommendations)
- **Sprint 17**: C28 (Company Story Timeline with Turning Points + Story Updates)
- **Sprint 18**: C29 Phase 2 (30+ metric coverage across all pages) + C41 Phase B (customer-supplier)

---

## Design Risk Assessment

### Risk 1: Business Card Page Overload (D-005)
- **Threat**: C41 adds a 16th section to the Business Card page. C29 adds ℹ️ icons to every metric.
- **Mitigation**: C41 Read Next goes at the BOTTOM of the page (after all existing sections). C29 ℹ️ icons are non-intrusive (tiny blue icons, content on click). RECOMMEND: Before Sprint 16, audit the Business Card page and collapse low-value sections into expandable containers.

### Risk 2: Inconsistency Across Pages
- **Threat**: C29 must add ℹ️ icons consistently across ALL 9 pages.
- **Mitigation**: Create a shared `_render_metric_with_explain()` component in `chart.py` or `components.py`. All pages must use this component, not inline HTML. Add to pre-development checklist.

### Risk 3: C28 Narrative Quality
- **Threat**: Auto-generated narratives may be bland or repetitive.
- **Mitigation**: Spike-first approach. Build a prototype with TSMC data only, evaluate narrative quality with real users before committing 20h. Use manual curation for top 10 stocks (ensure quality), template-based for rest (acceptable quality floor).

### Risk 4: C41 Recommendation Staleness
- **Threat**: Static recommendations become outdated (e.g., customer relationships change).
- **Mitigation**: Label all recommendations with data source and date. "資料來源: 2024年年報" sets user expectations. Phase B (customer-supplier) should include annual refresh cycle.

---

## Verification Gates

Following Challenger Round 7's requirement for verification gates after each sprint:

### After Sprint 16a (C29 Phase 1):
- [ ] Ten-second test: 5 beginners, each shown "ROE: 28.5%" with ℹ️ icon. All 5 must correctly explain ROE after clicking.
- [ ] Design audit: All ℹ️ icons use `#3498DB`, all popovers use `_render_tip_card()` styling.
- [ ] No color system violations introduced (scan for non-palette colors).

### After Sprint 16b (C41 Phase A):
- [ ] Every stock with peer data shows at least 1 recommendation.
- [ ] Clicking "查看故事 →" navigates correctly (session_state + st.rerun).
- [ ] Graceful degradation: stocks with no peer data show 0 recommendations (no error, no blank space).

### After Sprint 17 (C28):
- [ ] TSMC story timeline has 5-8 turning points with correct data.
- [ ] "故事更新" card correctly reflects last 90 days of M5 events.
- [ ] Horizontal timeline scrolls correctly without clipping content.
- [ ] Beginner can state TSMC's "big moment" within 10 seconds of viewing the story tab.

---

## Summary

The post-Sprint 15 development cycle should focus on **three narrative and educational features** that transform Stock Explorer from a data display tool into a guided learning platform:

1. **C28 Story Timeline** — The "historian" promise fully realized. Companies have stories, not just metrics. Competitors are converging on AI narratives; Stock Explorer must own this space with historical accuracy.

2. **C29 Explain Any Metric** — The "beginner-friendly" promise fulfilled systemically. Every metric everywhere has a one-click explanation. Closes the biggest gap between our design system ("plain-language translations required") and our implementation.

3. **C41 Read Next** — The "point-to-point knowledge construction" promise connected. Learning about one company naturally leads to discovering related companies through real business relationships.

Together, these three features create a **learning flywheel**: Explain (C29) → Understand the company → See its story (C28) → Discover related companies (C41) → Explain their metrics (C29) → Compare their stories (C38, future) → ...

This flywheel is Stock Explorer's unique competitive advantage. No competitor combines all three.

---

*This design discussion was prepared by the Design Reviewer for Round 33 planning. All recommendations align with the PPT-style design system (docs/design/design_system.md), the "historian, not stock picker" product positioning (docs/domain/product_vision.md), and reinforce the 18+ consecutive A/A design quality standard. Competitive references verified against 11 rounds of competitor research covering 45+ competitors across TW and international markets.*
