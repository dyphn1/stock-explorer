# Design Review — Round 8 Feature Proposals (C36-C41)

> **Author**: Design Reviewer
> **Date**: 2026-06-13
> **Context**: Evaluating 6 new feature proposals from Round 8 competitor research against the Stock Explorer design system, PPT-style principles, and "beginner education" mission.
> **Current Design Grade**: B (improved from C+ in Sprint 0)

---

## Evaluation Framework

Each feature is evaluated across 5 dimensions:

1. **Design System Alignment** — Zone A/B/C layout compliance, PPT style, ten-second test
2. **Beginner UX Impact** — How much this helps (or hinders) a first-time user
3. **Visual Design Recommendations** — Where it goes, how it looks, component choices
4. **Design Risks** — Clutter, complexity, PPT style violations
5. **Priority Recommendation** — From a pure design perspective

---

## C36: Visual Revenue Tree (Hierarchical Revenue Breakdown)

### 1. Design System Alignment: ⭐⭐⭐⭐ (4/5)

- **Zone fit**: Natural extension of the Business Card page (Zone C). Replaces or supplements the existing revenue pie chart.
- **PPT style**: A treemap or sunburst chart is inherently PPT-friendly — one visual, one key message ("here's how money flows through this business"). Charts >60% of the page area is easily met.
- **Ten-second test**: A well-designed treemap passes the ten-second test — the largest segment is immediately visible, and the hierarchy tells a story at a glance.
- **Zone compliance**: No zone violations. The chart stays in Zone C. No interactive controls needed beyond the existing time range selector.

### 2. Beginner UX Impact: High Positive

Beginners struggle with pie charts that show percentages without context. A revenue tree that shows "TSMC → 5nm chips (40%) → Apple (25%)" tells a *story* — it connects the company to real-world customers they recognize. This is the "historian" positioning in visual form.

### 3. Visual Design Recommendations

- **Placement**: Add as a second tab ("收入樹狀圖") next to the existing pie chart on the Business Card page. Default to the pie chart; let users discover the tree.
- **Chart type**: Use a **treemap** (not sunburst). Treemaps use space more efficiently, labels are easier to read, and the rectangular format fits the card-based layout better than circular sunburst charts.
- **Color**: Use the existing color system. Primary segments in `#3498DB` (blue), with sub-segments in lighter tints. Avoid introducing new colors. Use `#27AE60` (green) only if showing growth direction.
- **Labels**: Each rectangle must show the segment name + percentage. If the rectangle is too small, show only the name with a tooltip for the percentage.
- **Card wrapper**: Use the standard info card (blue border, `#F8F9FA` background) with a plain-language explanation below: e.g., "台積電最主要的收入來自5奈米晶片，佔總營收40%。最大客戶是蘋果，佔25%。"

### 4. Design Risks

- **Risk 1: Over-complexity for small companies**. Some companies have 10+ revenue segments. A treemap with 15 tiny rectangles fails the ten-second test. **Mitigation**: Cap at top 5 segments, group the rest as "其他".
- **Risk 2: Data availability**. Manual curation for top 20 stocks means the feature won't work for all stocks initially. **Mitigation**: Show a graceful fallback — "此公司的收入結構資料仍在整理中" with the pie chart as the default view.
- **Risk 3: Chart density**. If the treemap has too many levels (company → segment → customer), it becomes a wall of rectangles. **Mitigation**: Maximum 2 levels of hierarchy. No drilling down.

### 5. Priority Recommendation: **HIGH** (2nd of 6)

Strong alignment with "story first" and PPT style. The treemap is a natural, low-interaction way to tell the revenue story. Low design risk, high beginner impact.

---

## C37: Key Takeaways Summary Card (3-5 Synthesized Bullet Points)

### 1. Design System Alignment: ⭐⭐⭐⭐⭐ (5/5)

- **Zone fit**: Top of the Business Card page (Zone C), above all other content. This is the *first thing* a user sees.
- **PPT style**: This IS the PPT style — one card, 3-5 bullets, the entire story in 10 seconds. Text limit: 200 chars total across all bullets is achievable.
- **Ten-second test**: This feature *is* the ten-second test. If the key takeaways card works, the page passes. If it doesn't, the page fails regardless of other content.
- **Zone compliance**: No zone violations. Pure content in Zone C.

### 2. Beginner UX Impact: Very High Positive

This is the single highest-impact feature for beginners. The current Business Card page shows 15+ metrics with no synthesis. A beginner sees numbers but doesn't know what matters. The key takeaways card answers: "What are the 3 things I should remember about this company?"

### 3. Visual Design Recommendations

- **Placement**: First element on the Business Card page, below the company name/price (Zone A) but above all charts and metrics.
- **Card design**: Use a **tip card** (orange border `#F39C12`, background `#FFF8F0`) to visually distinguish it from data cards. This signals "this is a summary, not raw data."
- **Icon**: Use `📋` as the card icon.
- **Typography**: Each bullet as a separate line with `① ② ③` numbering. Each bullet ≤ 40 characters. Total card text ≤ 200 characters.
- **Example**:
  ```
  📋 重點摘要
  ① 台積電是全球90%先進晶片的製造商
  ② 毛利率55%，每賣100元賺55元
  ③ 過去3年營收穩定成長，資本支出很高
  ```
- **Plain-language**: Each bullet must be understandable without financial knowledge. No jargon without explanation.

### 4. Design Risks

- **Risk 1: Auto-generation quality**. If the bullets are generic or inaccurate, the card loses trust. **Mitigation**: Start with template-based generation (rule-based, not LLM) for the top 20 stocks. Manual review before shipping.
- **Risk 2: Taking up too much vertical space**. 5 bullets + card padding could push charts below the fold. **Mitigation**: Maximum 3 bullets for the initial release. Compact padding (0.8rem instead of 1.2rem).
- **Risk 3: Stale content**. If the takeaways don't update when data changes, they become misleading. **Mitigation**: Regenerate on each data refresh. Add a small "updated" timestamp in secondary text color.

### 5. Priority Recommendation: **CRITICAL** (1st of 6)

This is the highest-priority feature from a design perspective. It directly addresses the ten-second test, which is a core design principle. It has the highest ROI: 6-8h effort for a feature that defines the entire page experience. The competitor research notes that no TW competitor has auto-generated key takeaways — this is a differentiator.

---

## C38: Compare Stories Side-by-Side (Narrative Comparison)

### 1. Design System Alignment: ⭐⭐⭐ (3/5)

- **Zone fit**: New tab on the Peer Comparison page (Zone C). Fits within existing navigation.
- **PPT style**: **Tension with PPT style**. PPT style says "one key point per page." A side-by-side comparison inherently shows two points of information. The risk is cognitive overload — beginners comparing two companies' stories simultaneously may not know where to look.
- **Ten-second test**: Likely **fails** the ten-second test for beginners. Comparing two narratives requires holding two mental models simultaneously, which is an expert-level cognitive task.
- **Zone compliance**: No zone violations, but the comparison view needs careful layout to avoid clutter.

### 2. Beginner UX Impact: Mixed

For beginners, comparing two companies' stories is valuable *in concept* but challenging *in execution*. A beginner who just learned about TSMC may not have the context to compare it with UMC. This feature is more valuable for intermediate users who already understand both companies.

### 3. Visual Design Recommendations

- **Placement**: Add as a "故事比較" tab on the Peer Comparison page, *after* the existing metric comparison tab. Default to metric comparison; let users discover narrative comparison.
- **Layout**: Two-column layout (50/50 split). Left column: Company A. Right column: Company B. Each column shows: key events timeline, revenue milestones, and a 2-sentence business model summary.
- **Color coding**: Use `#3498DB` (blue) for Company A, `#27AE60` (green) for Company B. Consistent with the color system.
- **Text limit**: Each column ≤ 100 characters of narrative text. Total ≤ 200 characters (PPT style compliance).
- **Visual separator**: A vertical divider (`border-left: 1px solid #E0E0E0`) between columns.
- **Highlight differences**: Use bold text or a subtle background tint to highlight where the two stories diverge. E.g., "TSMC focuses on **advanced** nodes" vs "UMC focuses on **mature** nodes."

### 4. Design Risks

- **Risk 1: PPT style violation**. Two narratives on one page = two key points. **Mitigation**: Frame the entire comparison as ONE key point: "These two companies have different business strategies." The two columns serve that single point.
- **Risk 2: Clutter**. Two timelines + two revenue models + two summaries = visual chaos. **Mitigation**: Show only ONE dimension at a time. Add a sub-toggle: "商業模式" / "關鍵事件" / "收入里程碑". Default to "商業模式" (simplest).
- **Risk 3: Beginner confusion**. Beginners may not know *why* they're comparing. **Mitigation**: Add a one-line explanation at the top: "比較兩家公司的商業模式，了解它們的策略差異。"

### 5. Priority Recommendation: **MEDIUM** (4th of 6)

Valuable feature but not beginner-critical. The PPT style tension and ten-second test concerns make this a "nice to have" for the current roadmap. Recommend deferring to a later sprint after the beginner experience is solid.

---

## C39: What Changed Recently Delta Card (Recent Metric Changes)

### 1. Design System Alignment: ⭐⭐⭐⭐ (4/5)

- **Zone fit**: Business Card page (Zone C), positioned below the key takeaways card (if C37 is implemented) and above the detailed metrics.
- **PPT style**: A delta card can be PPT-style if it shows only the most significant change. "One key point: here's what changed." However, showing multiple deltas risks becoming a data dump.
- **Ten-second test**: Passes if limited to 1-2 changes. Fails if showing 5+ deltas with percentages.
- **Zone compliance**: No zone violations.

### 2. Beginner UX Impact: High Positive

Beginners don't know what to look for in historical charts. A delta card that says "最近3個月營收成長15%，是過去一年最快的增速" tells the beginner exactly what matters. It makes the data feel alive and relevant — a key part of the "historian" positioning.

### 3. Visual Design Recommendations

- **Placement**: Business Card page, below C37 (Key Takeaways) and above the revenue chart.
- **Card design**: Use the standard info card (blue border) with a `🔄` icon.
- **Content**: Show **maximum 2 deltas** — the two most significant changes. Each delta: metric name + direction arrow + percentage + plain-language explanation.
- **Color coding**: Use `#27AE60` (green) with ↑ arrow for positive changes, `#E74C3C` (red) with ↓ arrow for negative changes. This is one of the approved uses of red/green (direction indication).
- **Example**:
  ```
  🔄 最近有什麼變化
  📈 營收成長15% — 過去3個月增速是一年來最快
  📉 毛利率下降3% — 因為晶片價格競爭加劇
  ```
- **Threshold**: Only show deltas > 10% change. Small fluctuations are noise, not signal.

### 4. Design Risks

- **Risk 1: Too many deltas**. If 5 metrics changed >10%, the card becomes a list. **Mitigation**: Hard cap at 2 deltas. Pick the two with the largest absolute change.
- **Risk 2: Negative-only deltas**. If all significant changes are negative, the card becomes a "bad news" card that discourages beginners. **Mitigation**: If all deltas are negative, add context: "短期波動是正常的，長期趨勢才是重點。" (Short-term fluctuations are normal; long-term trends matter.)
- **Risk 3: Stale "recent" data**. If the data is 2 months old, "最近" feels misleading. **Mitigation**: Add a timestamp: "資料更新：2026-06-10". If data is >60 days old, hide the card entirely.

### 5. Priority Recommendation: **HIGH** (3rd of 6)

Strong beginner impact, good PPT style alignment, low design risk. The delta card makes data feel alive and teaches beginners what to watch. Natural companion to C37 (Key Takeaways).

---

## C40: Beginner/Expert Mode Toggle (Complexity Toggle)

### 1. Design System Alignment: ⭐⭐ (2/5)

- **Zone fit**: **Zone violation risk**. The proposal puts the toggle in the navbar (Zone A). Zone A "must NOT contain: search box, filters, or any interactive controls." A mode toggle is an interactive control.
- **PPT style**: The toggle itself doesn't affect PPT style — it controls which PPT-style pages are shown. However, the *concept* of an expert mode contradicts the "one key point per page" principle. Expert mode would show more data per page, which is anti-PPT.
- **Ten-second test**: Beginner mode *improves* the ten-second test by reducing clutter. Expert mode *worsens* it by showing everything.
- **Zone compliance**: **Needs redesign** to comply with zone rules.

### 2. Beginner UX Impact: High Positive (for Beginner Mode), Neutral (for Expert Mode)

Beginner mode is excellent — it hides advanced metrics and shows only the essentials. This directly serves the "beginner education" mission. Expert mode is neutral — it doesn't help beginners, but it doesn't hurt them either (they won't toggle it).

### 3. Visual Design Recommendations

- **Placement**: **NOT in Zone A (navbar)**. Move to Zone B (sidebar) as a persistent toggle at the top of the sidebar, above the search box. This complies with the zone rules (Zone B is for navigation and controls).
- **Alternative placement**: If Zone B is too crowded, add it as a **floating button** in the bottom-right corner of Zone C (main content area). Use `position: fixed; bottom: 20px; right: 20px;` with a semi-transparent background.
- **Toggle design**: Use a simple toggle (not buttons). Label: "🌱 新手模式" (default ON) / "🔬 進階模式". Use `#27AE60` (green) for beginner mode, `#3498DB` (blue) for expert mode.
- **Beginner Mode behavior**:
  - Show only: one-liner, revenue pie chart, 3-4 key metrics, "Did You Know?" facts
  - Hide: institutional investor charts, detailed financial ratios, debt analysis, advanced peer comparison
  - Maximum 1 chart per section
- **Expert Mode behavior**: Current behavior (show everything).

### 4. Design Risks

- **Risk 1: Zone A violation**. The proposal explicitly says "navbar." This violates the design system. **Mitigation**: Move to Zone B or floating button.
- **Risk 2: Maintenance burden**. Two modes = two versions of every page to maintain. Every new feature must be evaluated for both modes. **Mitigation**: Implement as a simple `if beginner_mode: show_simplified()` wrapper, not as separate pages.
- **Risk 3: Beginner mode becomes "lite" mode**. If beginner mode hides too much, users feel they're getting an inferior product. **Mitigation**: Frame it as "focused view" not "simple mode." The key takeaways card (C37) should be visible in BOTH modes.
- **Risk 4: Toggle discovery**. Users won't know the toggle exists. **Mitigation**: Add a one-time tooltip on first visit: "🌱 目前為新手模式，只顯示最重要的資訊。"
- **Risk 5: Expert mode PPT violation**. Expert mode showing everything per page violates the "one key point per page" rule. **Mitigation**: Even in expert mode, maintain PPT style. Show more sections, but each section still has one key point.

### 5. Priority Recommendation: **MEDIUM-LOW** (5th of 6)

The concept is valuable, but the implementation complexity and zone violation risk are non-trivial. The toggle adds a maintenance burden that the small team may not sustain. **Alternative approach**: Instead of a toggle, *design all pages in beginner mode by default* and let users drill down for more detail. This achieves the same goal without a toggle. The "progressive drill-down" principle in the product vision already supports this.

---

## C41: Read Next Recommendations (Relationship-Based Discovery)

### 1. Design System Alignment: ⭐⭐⭐⭐ (4/5)

- **Zone fit**: Business Card page (Zone C), at the bottom as a "next steps" section. This is a natural position — after learning about a company, the user sees what to learn next.
- **PPT style**: A recommendation section is not a chart, but it's also not violating PPT style. It's a "next slide" prompt — "now that you've seen this, go here next." This is actually *more* PPT-like than most features (PPTs have "next slide" cues).
- **Ten-second test**: The recommendations themselves are simple enough (2-3 company names with one-line descriptions). Passes.
- **Zone compliance**: No zone violations. The recommendations are content, not navigation.

### 2. Beginner UX Impact: High Positive

Beginners don't know what to search for next. A "Read Next" section creates a learning path: "After TSMC, learn about Apple (its biggest customer)" or "After TSMC, learn about UMC (its main competitor)." This is the "point-to-point knowledge construction" core value in action.

### 3. Visual Design Recommendations

- **Placement**: Bottom of the Business Card page, after all charts and metrics. This is the "what's now?" position — the user has finished reading and is ready for the next thing.
- **Card design**: Use a **tip card** (orange border) with a `📖` icon to distinguish it from data cards. This signals "this is a suggestion, not data."
- **Content**: 2-3 recommendations maximum. Each recommendation: company name + ticker + one-line relationship description.
- **Example**:
  ```
  📖 接著看
  → 蘋果 (AAPL) — 台積電最大的客戶，佔營收25%
  → 聯華電子 (UMC) — 台積電的主要競爭對手
  → 輝達 (NVDA) — 台積電5奈米晶片的大客戶
  ```
- **Interaction**: Each recommendation is a clickable button (`st.button`) that navigates to that company's Business Card page. Use the existing sidebar navigation pattern (set `session_state["stock_id"]` + `st.rerun()`).
- **Color**: Use `#3498DB` (blue) for the clickable company names (blue = clickable, per color system rules).

### 4. Design Risks

- **Risk 1: Manual curation bottleneck**. The proposal says "manual curation for top 20 stocks." This means the feature only works for 20 stocks initially. **Mitigation**: For stocks without curated recommendations, use a fallback: same-industry recommendations from existing industry data. Show "同行業其他公司" as a generic fallback.
- **Risk 2: Circular recommendations**. If TSMC recommends Apple and Apple recommends TSMC, users go in circles. **Mitigation**: Track the last 3 visited stocks and exclude them from recommendations.
- **Risk 3: Too many recommendations**. If showing 5+ recommendations, the section becomes a list. **Mitigation**: Hard cap at 3. Prioritize: (1) customer-supplier relationship, (2) direct competitor, (3) same-industry #2 player.
- **Risk 4: Cluttering the bottom of the page**. If the Business Card page is already long, the recommendations may never be seen. **Mitigation**: This is actually fine — recommendations are a "bonus" feature. Users who scroll to the bottom are engaged and ready for the next step.

### 5. Priority Recommendation: **HIGH** (3rd of 6, tied with C39)

Strong beginner impact, good PPT style alignment, low design risk. The relationship-based approach is a unique differentiator — no competitor does this. The manual curation limitation is acceptable for an initial release.

---

## Overall Design Recommendation

### Priority Ranking (Design Perspective)

| Rank | Feature | Score | Rationale |
|------|---------|-------|-----------|
| **1** | **C37: Key Takeaways** | ⭐⭐⭐⭐⭐ | Directly addresses the ten-second test — the core design principle. Highest ROI (6-8h for a defining feature). No design risks. |
| **2** | **C36: Visual Revenue Tree** | ⭐⭐⭐⭐ | Strong "story first" alignment. Treemap is inherently PPT-friendly. Natural extension of existing pie chart. |
| **3** | **C39: What Changed Recently** | ⭐⭐⭐⭐ | Makes data feel alive. Teaches beginners what to watch. Natural companion to C37. |
| **3** | **C41: Read Next** | ⭐⭐⭐⭐ | Unique differentiator. Creates learning paths. Low design risk. |
| **5** | **C38: Compare Stories** | ⭐⭐⭐ | Valuable but PPT-style tension. Better suited for intermediate users. Defer. |
| **6** | **C40: Mode Toggle** | ⭐⭐ | Zone violation risk. Maintenance burden. Better alternative: design everything in beginner mode by default. |

### Recommended Sprint Allocation

**Sprint 2 (alongside D02 + C31)**:
- **C37: Key Takeaways** (6-8h) — Must-have. Defines the page experience.

**Sprint 3 (alongside C28 full)**:
- **C36: Visual Revenue Tree** (10-14h) — High impact, natural extension of Business Card.
- **C41: Read Next** (6-8h) — Low effort, high differentiation.

**Sprint 4 (alongside C07 + C14)**:
- **C39: What Changed Recently** (8-10h) — Complements C37 nicely.

**Deferred**:
- **C38: Compare Stories** — Revisit after beginner experience is solid.
- **C40: Mode Toggle** — Replace with "beginner mode by default" design philosophy.

### Design Principles for Implementation

1. **C37 first, always**. The key takeaways card defines the page. Every other feature on the Business Card page should be designed around it.
2. **Beginner mode by default**. Instead of a toggle (C40), design ALL pages to show the beginner view first. Let users drill down for more detail. This achieves C40's goal without the zone violation and maintenance burden.
3. **One new card per page per sprint**. Don't add C36 + C37 + C39 + C41 to the Business Card page simultaneously. Add them one at a time, test the ten-second test after each addition.
4. **Template-first, LLM-later**. All auto-generated content (C37, C39) should start with rule-based templates. LLM can improve quality later, but templates ensure correctness and PPT style compliance.
5. **The "10-second test" gate**. After implementing each feature, run the ten-second test: show the page to someone unfamiliar with the stock. If they can't summarize the core concept in 10 seconds, the feature needs redesign.

### The "Beginner Education" Mission — Top 3 Features

The three features that best serve the beginner education mission are:

1. **C37: Key Takeaways** — Tells beginners what matters
2. **C36: Visual Revenue Tree** — Shows beginners how the business works
3. **C41: Read Next** — Guides beginners to the next learning step

These three features form a complete beginner experience: **understand the summary** (C37) → **explore the business model** (C36) → **discover related companies** (C41). This is the "point-to-point knowledge construction" core value in action.

---

*Design Review completed. Recommendations aligned with PPT-style design system, ten-second test principle, and "beginner education" mission.*
