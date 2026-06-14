## 2026-06-15 Developer Estimate — Discussion Round 46

### Feature Estimates

#### C199: Bear vs Bull Visual Debate Cards
- **Validated Effort**: 10-14h (original: 8-12h) — **revised up**
- **Implementation Approach**:
  - New service: `src/services/debate_engine.py` — pure Python, generates bear/bull argument dicts from financial data (valuation metrics, revenue trend, institutional flow, news sentiment). Reuses `financial_metrics.py` for per/pbr/debt inputs and `risk_analyzer.py` risk classifications.
  - New page component or section: `src/pages/business_card/_sections/_debate.py` — renders side-by-side cards using existing `_summary_card()` / `_info_card()` helpers from `_router_base.py`. Uses columns layout (`st.columns(2)`) with emoji headers (🐻/🐂), 3 bullet arguments each, and key stat callouts.
  - Data layer: For the first release, use template-based arguments keyed on metric thresholds (PER > 25 → bull argument about growth premium; PER < 12 → bull argument about value). This aligns with the "all explanations are template-based" constraint.
  - Wire into `business_card/_sections.py` as a new collapsible section ("多空辯論").
- **Technical Risks**:
  - Content quality is the main risk: generating balanced, factual arguments from thresholds is harder than it looks. Each argument needs historian tone (past facts only, no prediction). Expect 2-3 rounds of content tuning.
  - business_card.py is already 447 lines; adding a section here contributes to the D24 architectural limit concern. Must use the `_sections/` sub-directory pattern.
  - The feature is P2 but has high visual impact — stakeholders may expect more polish than the estimate allows.
- **Dependencies**: None on Sprint 21 features. Can be developed independently. Reuses existing UI components and financial_metrics.py.

---

#### C200: "What If I Had Invested?" Historical Scenario Calculator
- **Validated Effort**: 12-16h (original: 10-14h) — **revised up**
- **Implementation Approach**:
  - The business logic already partially exists: `src/pages/business_card/_historical_scenarios.py` (320 lines) contains hardcoded scenario cards for major stocks. `src/data/yaml/historical_scenarios.yaml` has curated scenarios for 2330, 2317, 2454, 2308.
  - **Upgrade path**: Instead of just displaying pre-written scenarios, add interactive calculation:
    - New service: `src/services/scenario_calculator.py` — pure Python, takes (stock_id, invest_date, amount) → fetches historical price via FinMind client → computes return, CAGR, and comparison to定期定額.
    - Modify `_historical_scenarios.py` to add an interactive input section (date picker, amount slider) at the top, then show curated scenarios below.
    - Reuse `chart.py` `create_price_chart()` for the visual, with a vertical line at the buy date.
  - Add historian disclaimer: "歷史績效不代表未來結果" (already a pattern in the codebase via `_historian_disclaimer()`).
- **Technical Risks**:
  - **API dependency**: Requires fetching historical daily price for an arbitrary date range. FinMind API rate limits may be hit if users experiment with many dates. Need caching (`st.cache_data`).
  - **Date edge cases**: Handling stock splits, dividend adjustments, and non-trading dates adds complexity. The existing `chart.py` price chart already handles some of this, but buy-date price lookup needs careful handling.
  - **Content scope**: Pre-written scenarios cover only ~8 stocks. Interactive mode needs to handle ALL stocks gracefully, with fallback messages for insufficient history.
- **Dependencies**: Builds on existing `_historical_scenarios.py` (C74). Reuses chart.py. No dependency on Sprint 21 features.

---

#### C201: "Daily Market Story" 3-Minute Morning Briefing Card
- **Validated Effort**: 14-18h (original: 12-16h) — **revised up** (P1 priority)
- **Implementation Approach**:
  - The investor story feed (`src/pages/investor_story_feed.py`, C116) already exists with `story_feed.py` service that generates stories from watchlist events + market data.
  - **Upgrade path**: Create a new, condensed briefing card component:
    - New service: `src/services/morning_briefing.py` — extends `story_feed.py` to select top-3 most relevant stories, add a 3-minute read time estimate, and compose a structured briefing dict.
    - New page component: `src/pages/business_card/_sections/_morning_briefing.py` — a compact card layout with 3 story highlights, each with: icon, one-line summary, "why it matters" sentence. Estimated read time header: "⏱️ 3 分鐘讀完".
    - Wire to appear at the top of the homepage (router.py conditional) for beginner mode.
  - Needs `market_data.py` for sector performance context and `adaptive_engine.py` for event detection.
- **Technical Risks**:
  - **Blank state**: What shows when there are no significant events today? Need a fallback "market is quiet" card with rotating financial education content. This adds ~2h for fallback content creation.
  - **Data freshness**: Market data from FinMind may be T-1. The briefing should date-stamp clearly: "昨日市場重點".
  - **Performance**: The briefing card runs on page load. If event detection is slow (>1s), it blocks the entire page. Must ensure `get_all_recent_events()` is cached or pre-computed.
  - **P1 scope creep**: This is the highest-risk feature in the set because it requires curation quality, not just code. The difference between "useful briefing" and "noise" is content, not architecture.
- **Dependencies**: Reuses `story_feed.py` (C116), `market_data.py`, `adaptive_engine.py`. No dependency on C170/C188. Benefits from D-127 (performance debt) if completed first.

---

#### C202: "Story Arc" Timeline Labels — Auto-Detected Narrative Arcs
- **Validated Effort**: 10-14h (original: 8-10h) — **revised up**
- **Implementation Approach**:
  - `src/services/timeline_service.py` (299 lines) already composes timeline entries from events, case studies, and milestones. It has `date`, `type`, `severity`, `title`, `summary`, `interpretation` fields — but no narrative arc labels.
  - **Upgrade path**:
    - New service: `src/services/story_arc_detector.py` — analyzes a sequence of TimelineEntry objects and detects arcs: "recovery arc" (negative events followed by positive), "growth arc" (consistent positive), "declarc" (consistent negative), "volatility arc" (mixed). Pure Python, no Streamlit.
    - Classify arcs by simple heuristics: count positive/negative/medium severity events in a sliding window of 6 months. If all positive → "成長期", all negative → "調整期", mixed → "震盪期".
    - Output: `(arc_label, arc_emoji)` — e.g., ("成長期", "📈"), ("調整期", "📉"), ("震盪期", "🔄").
    - Modify `story_timeline.py` to display arc labels as colored badges between timeline sections.
  - Arc label templates in `src/data/yaml/story_arcs.yaml` for content.
- **Technical Risks**:
  - **Heuristic quality**: Simple threshold-based arc detection will produce noisy results for stocks with sparse events. Need minimum event count threshold (≥3 events in 6 months) before showing any arc label.
  - **Content quality**: Arc labels need to feel insightful, not mechanical. Expect tuning iterations.
  - **Performance**: Timeline is already YAML-local (no API calls). Arc detection is pure computation — negligible overhead.
- **Dependencies**: Reuses `timeline_service.py`. No dependency on Sprint 21 features.

---

#### C203: "Supply Chain Impact" Visual Map
- **Validated Effort**: 18-24h (original: 14-18h) — **revised up significantly**
- **Implementation Approach**:
  - `src/data/group_structures.yaml` already has parent-subsidiary data with `holding`, `revenue_contrib`, `business`, `relation` fields — but only for ~5 major groups.
  - **New work**:
    - New page: `src/pages/supply_chain_map.py` — dedicated page for supply chain visualization.
    - New service: `src/services/supply_chain_service.py` — loads `group_structures.yaml`, enriches with FinMind price data for overlay (stock price change of key suppliers).
    - Visualization: Use Plotly `create_funnel_chart()` (exists in chart.py) as a starting point, but a supply chain map needs a network-style layout. Options:
      - **Option A (simpler)**: Use a radial/treemap approach with `create_revenue_treemap()` (exists) to show parent → subsidiaries with size = revenue_contrib, color = YoY change. ~4h for adaptation.
      - **Option B (better UX)**: Use Plotly annotations + shapes to draw a directed graph. ~8h for custom layout logic.
    - Option A recommended for MVP; Option B as stretch goal.
  - Enrich `group_structures.yaml` with customer relationships (not just subsidiaries). This is a significant data entry task.
- **Technical Risks**:
  - **Data sparsity**: Only ~5 groups have detailed data. Expanding to 15-20 groups requires manual research (2-4h of data entry per group). This is a content blocker, not a code blocker.
  - **Visualization complexity**: Network diagrams in Plotly are notoriously finicky. The treemap fallback is safer but less impressive.
  - **TW market specific**: True supply chain data (customer-supplier relationships) is not fully available via FinMind API. Relies on manual YAML curation.
  - **Scope creep risk**: Highest-effort feature in the set. The 18-24h estimate assumes Option A and existing data. Full supply chain mapping with event propagation could be 40h+.
- **Dependencies**: Reuses `chart.py`, `financial_metrics.py`. No dependency on Sprint 21. Data entry is the real bottleneck.

---

#### C204: "Confidence Indicator" on AI Explanations — Emoji-Based
- **Validated Effort**: 4-6h (original: 4-6h) — **confirmed**
- **Implementation Approach**:
  - The `ExplanationResponse` dataclass in `src/services/llm/base.py` already has a `confidence: float = 1.0` field. The template-based provider (`template_provider.py`) always returns `confidence=1.0` since templates are deterministic.
  - **Implementation**:
    - Modify `ExplanationResponse` serialization to include an emoji confidence indicator:
      - `confidence >= 0.8` → "🟢 高度信心" (high: metric has clear threshold, value is current)
      - `confidence >= 0.5` → "🟡 中度信心" (medium: estimate or involves comparison)
      - `confidence < 0.5` → "🟠 參考性質" (low: sparse data or extrapolation)
    - In `template_provider.py`, set confidence based on template match quality: exact metric match → 0.9, fallback/generic → 0.5, missing data handled → 0.3.
    - Update all pages that render explanations to show the confidence emoji. Affected files: `business_card/_sections/_detail.py`, `financial_health.py`, `peer_comparison.py` (any place `_info_card()` or `_summary_card()` is used for explanations).
    - New helper in `_router_base.py`: `_confidence_badge(confidence: float) -> str` — returns emoji + text.
- **Technical Risks**:
  - **Trivial implementation** (2h) vs. **meaningful implementation** (6h): The easy path is just adding emoji constants and displaying them. The meaningful path requires each explanation source to calculate its own confidence metric. Recommend the meaningful path.
  - **Consistency**: Every explanation rendering site must be updated. Missing one means inconsistent UX. Need to audit all explanation display locations.
  - **No LLM yet**: Since all explanations are template-based, "confidence" is synthetic. Must be clearly communicated as "data completeness" not "AI certainty."
- **Dependencies**: Reuses `llm/base.py` ExplanationResponse. No dependency on Sprint 21 features. **Best done as a quick win early in the sprint.**

---

#### C205: "Read Time" Indicator on All Content
- **Validated Effort**: 3-5h (original: 2-4h) — **revised up slightly**
- **Implementation Approach**:
  - New helper in `_router_base.py`: `_read_time(text: str) -> str` — estimates read time based on Chinese character count. Average Chinese reading speed: ~400-500 characters/minute. Formula: `max(1, ceil(char_count / 450))` → returns "X 分鐘閱讀".
  - Apply to all content sections: business_card sub-sections, timeline entries, scenario cards, glossary entries.
  - **Systematic approach**: Instead of adding `_read_time()` to every page individually, create a wrapper `_section_title_with_read_time(title: str, content: str)` that renders the title + read time badge.
  - Add to the following sections: `_summary.py`, `_financial.py`, `_health.py`, `_story.py`, `_moat.py`, `_detail.py`, `_historical_pattern.py` in `business_card/_sections/`.
- **Technical Risks**:
  - **Trivial feature, distributed cost**: The calculation is 5 lines of code. The cost is touching 8-10 files to add the indicator consistently.
  - **Streamlit re-render**: Read time is computed on each render. For dynamic content, this is fine. For static YAML content, could be pre-computed — but not worth the complexity.
  - **Visual clutter**: Adding read time to EVERY section may add noise. Recommend only showing it for sections with >50 characters of content.
- **Dependencies**: None. Pure UI addition. **Best done as a quick win paired with C204.**

---

#### C206: "Recurring Investment" Concept Education
- **Validated Effort**: 8-12h (original: 6-8h) — **revised up**
- **Implementation Approach**:
  - New lesson content in `src/data/yaml/dca_lessons.yaml` — structured lesson explaining Dollar-Cost Averaging (定期定額) with:
    - Plain-language definition ("每個月固定金額買進，不猜高低點")
    - Historical example using existing data (e.g., "每月買 2330 一萬元，過去 5 年...").
    - Comparison: lump sum vs. DCA visualization using `chart.py`.
    - Disclaimer: "此為概念教學，非投資建議".
  - New service: `src/services/dca_education.py` — pure Python, computes DCA scenarios from historical price data. Reuses `financial_metrics.py` functions.
  - New page: `src/pages/recurring_investment_edu.py` — educational page with interactive sliders (monthly amount, duration, stock selection). Or integrate as a component in the existing `financial_wellness.py` page.
  - Pre-compute DCA results for 5 major stocks and store in YAML for instant display. Interactive recalculation for other stocks.
- **Technical Risks**:
  - **Regulatory sensitivity**: DCA education is close to investment advice. Every screen needs clear "教育用途" disclaimers. Legal review may be needed. **This is the highest non-technical risk in the feature set.**
  - **Data requirements**: Need reliable historical price data for 5+ years. FinMind provides this, but rate limiting is a concern for interactive recalculation.
  - **Scope**: Interactive DCA calculator with chart is 8h. Adding comparison visualization (lump sum vs. DCA bar chart) adds 2-4h.
- **Dependencies**: Reuses `chart.py`, `financial_metrics.py`. Conceptually related to C200 (Historical Scenarios) — they share the "historical what-if" pattern but C206 is educational-only. No dependency on Sprint 21.

---

### Recommended Implementation Order

Considering effort vs. impact, dependencies on Sprint 21 (C170, C188), and the quick-win vs. long-term-investment tradeoff:

**Quick Wins (do first — build momentum, low risk):**

1. **C204: Confidence Indicator** (4-6h) — Minimal code, high perceived quality. Improves trust in all existing AI explanations. Sets the pattern for transparent AI communication.
2. **C205: Read Time Indicator** (3-5h) — Pairs naturally with C204. Both touch `_router_base.py` and section files. Together they take 7-11h and improve every page instantly.

**Sprint 22 — Mid-Effort, High Value:**

3. **C202: Story Arc Timeline Labels** (10-14h) — Uniquely differentiated feature (no competitor has auto-detected arcs). Builds on existing `timeline_service.py`. The heuristic approach is low-risk.
4. **C199: Bear vs Bull Debate Cards** (10-14h) — High visual impact, reusable card pattern. Uses existing financial data. Good "wow factor" for demos.
5. **C200: Historical Scenario Calculator** (12-16h) — Builds on existing `_historical_scenarios.py`. Interactive element drives engagement. FinMind caching is the main technical concern.

**Sprint 23 — High Effort, Strategic:**

6. **C206: Recurring Investment Education** (8-12h) — Important for beginner-friendly positioning. Regulatory sensitivity requires careful review.
7. **C201: Daily Market Morning Briefing** (14-18h) — P1 priority but high content curation cost. Needs fallback content strategy. Reuses existing `story_feed.py` infrastructure.

**Sprint 24 — Capstone:**

8. **C203: Supply Chain Visual Map** (18-24h) — Highest effort, highest uncertainty. Data entry is the real bottleneck. Best done when data for 10+ groups is ready. Consider phasing: treemap MVP first, network visualization later.

### Key Dependencies & Sequencing Notes

- **C170 (Tappable Glossary, Sprint 21)** and **C188 (Why Did This Stock Move?, Sprint 21)** are prerequisites for none of the new features. They can proceed in parallel.
- **D-125/D-126/D-127 (Tech Debt, Sprint 21)**: D-127 (performance caching) would benefit C201 (morning briefing) and C200 (scenario calculator). Recommend completing D-127 before those features.
- **C204 + C205** can be started immediately — no dependencies, no Sprint 21 blockers. **Recommend starting these in Sprint 21 as stretch goals.**

### Total Effort for Top 3 Recommended Features

| Feature | Effort | Priority |
|---------|--------|----------|
| C204: Confidence Indicator | 4-6h | Quick Win |
| C205: Read Time Indicator | 3-5h | Quick Win |
| C202: Story Arc Timeline Labels | 10-14h | Mid-Effort, High Value |

**Total: 17-25h** for the top 3 quick-to-mid wins.

If replacing C202 with the next highest-value feature:

| Feature | Effort | Priority |
|---------|--------|----------|
| C204: Confidence Indicator | 4-6h | Quick Win |
| C205: Read Time Indicator | 3-5h | Quick Win |
| C199: Bear vs Bull Debate Cards | 10-14h | Mid-Effort, Visual Impact |

**Total: 17-25h** (same range).

---

### Risk Summary

| Risk | Features Affected | Mitigation |
|------|-------------------|------------|
| Content quality / historian tone tuning | C199, C201, C202, C206 | Pre-write YAML content templates; 2h content review per feature |
| FinMind API rate limits | C200, C201, C203, C206 | `st.cache_data` with TTL; pre-compute for top 20 stocks |
| Regulatory sensitivity (investment advice) | C200, C206 | Mandatory "教育用途，非投資建議" disclaimers on every screen |
| Data sparsity | C203 | Start with treemap (existing data), defer network graph |
| Scope creep | C201, C203 | Strict MVP definition; "3 stories, 3 minutes" for C201; treemap-only for C203 |
| C188 completion blocking | None of C199-C206 | Confirmed: no hard dependencies on Sprint 21 features |
