# 2026-06-15 Developer Estimate — Discussion Round 47

## C202: "Story Arc" Timeline Labels — Auto-Detected Narrative Arcs

### Implementation Breakdown

| Layer | Work Items | Hours |
|-------|-----------|-------|
| **Service Layer** | New `src/services/story_arc_detector.py` — `ArcLabel` TypedDict, sliding-window heuristic (6-month window, ≥3 events minimum), (`arc_label`, `arc_emoji`, `arc_description`) output. Pure Python, no Streamlit. | 3-4h |
| **YAML Content** | New `src/data/yaml/story_arcs.yaml` — arc label templates: `成長期📈`, `調整期📉`, `震盪期🔄`, `復甦期🌱`. Each with description templates and minimum event thresholds. | 1-2h |
| **Page/UI** | Modify `src/pages/story_timeline.py` — add arc badge rendering between timeline sections. Insert colored `st.badge()` or inline markdown badge at arc transition points. Add arc legend below timeline stats. | 2-3h |
| **Testing** | L0 unit tests for `story_arc_detector.py`: empty entries, single event, all-positive arc, all-negative arc, mixed arc, recovery arc (neg→pos), boundary conditions (exactly 3 events, exactly 6-month window). Mock `TimelineEntry` lists. | 2-3h |
| **Edge Cases** | Sparse events (<3 in window → no label shown), stocks with no events, stocks with only milestones (no severity), arc transitions within same month, future-dated entries. | 1-2h |

### Technical Risks

1. **Heuristic noise**: Simple threshold-based detection will produce noisy labels for stocks with sparse events. Mitigation: enforce minimum event count (≥3 events in 6 months) before showing any arc label. This is the single most important quality gate.
2. **Arc transition detection**: Determining *where* one arc ends and another begins is ambiguous with overlapping windows. Mitigation: use non-overlapping 6-month buckets (Jan-Jun, Jul-Dec) for cleaner transitions, accepting lower temporal precision.
3. **Content quality**: Arc labels can feel mechanical ("成長期") without context. Mitigation: include a one-line `arc_description` template that references the dominant event type (e.g., "過去6個月營收連續成長，市場評價偏向正面").
4. **Performance**: Negligible — all computation is over YAML-local timeline entries (already loaded). No API calls.
5. **UI clutter**: Adding badges between every timeline entry could be visually noisy. Mitigation: only show arc labels at transition points (where the arc classification changes between consecutive buckets), not on every entry.

### Dependencies

- **Hard**: `src/services/timeline_service.py` (TimelineEntry type, `get_timeline()`)
- **Hard**: `src/pages/story_timeline.py` (page renderer)
- **Soft**: `src/data/yaml/story_arcs.yaml` (content templates — can be created in parallel)
- **None on Sprint 21/22 features**: Fully independent

### Estimate: 9-14 hours

**Confidence**: Medium-High. The service layer is straightforward pure-Python. The main uncertainty is UI integration — the timeline page currently renders entries in a flat loop, and inserting arc labels between entries requires restructuring the render loop to detect arc transitions. The original 10-14h estimate is validated; we narrow the lower bound to 9h because the service logic is simpler than initially expected (sliding window over pre-sorted entries).

---

## C199: "Bear vs Bull" Visual Debate Cards

### Implementation Breakdown

| Layer | Work Items | Hours |
|-------|-----------|-------|
| **Service Layer** | New `src/services/debate_engine.py` — `generate_debate(stock_id, data) -> DebateResult`. Produces 3 bear arguments + 3 bull arguments from financial metrics (PER, PBR, revenue YoY, debt ratio, institutional flow, dividend yield). Template-based with metric-threshold keying. Pure Python, no Streamlit. | 3-4h |
| **YAML Content** | New `src/data/yaml/debate_templates.yaml` — argument templates keyed on metric thresholds. E.g., PER > 25 → bull: "市場願意給予高估值，反映成長預期"; bear: "本益比偏高，若成長不如預期，回檔風險較大". Templates must maintain historian tone (past facts only). | 2-3h |
| **Page/UI** | New `src/pages/business_card/_sections/_debate.py` — `_render_debate(data, client)` function. Side-by-side `st.columns(2)` with 🐻/🐂 emoji headers, 3 bullet arguments each, key stat callouts. Wire into `business_card/_sections.py` as re-export and into `_main.py` rendering pipeline. | 2-3h |
| **Testing** | L0 unit tests for `debate_engine.py`: test each threshold branch (high/medium/low PER, positive/negative revenue YoY, high/low debt), test with missing data (some metrics None), test that arguments are balanced (neither side is empty), test historian tone (no future-tense predictions). | 2-3h |
| **Edge Cases** | All metrics missing → graceful fallback ("目前數據不足以產生多空分析"), only bear or only bull arguments available → show available side with "另一方暫無明確論點" placeholder, extreme values (PER > 100 or negative), ETF stocks (no PER/PBR). | 1-2h |

### Technical Risks

1. **Content quality (HIGH RISK)**: This is the #1 risk. Template-based arguments can feel generic or preachy. Each argument must be factual, specific to the stock's actual metrics, and maintain historian tone. Expect 2-3 rounds of content tuning after initial implementation. Mitigation: invest 2-3h upfront in high-quality YAML templates with metric-specific values interpolated (not generic statements).
2. **Balanced arguments**: Ensuring both sides have equally compelling arguments is hard. A stock with PER=8 and debt_ratio=20% will have strong bull arguments but weak bear arguments. Mitigation: include "even the bull side acknowledges..." nuance templates for edge cases.
3. **business_card.py size**: The `_main.py` orchestrator is already 321 lines with 15+ section imports. Adding another section import is fine (the re-export pattern handles this), but the rendering pipeline in `_main.py` needs a new `_render_debate()` call in the correct position. Low risk due to the established pattern.
4. **Visual polish**: Stakeholders may expect animated cards or interactive elements. The MVP uses static side-by-side cards. If stakeholders want more, scope creep could add 4-6h.

### Dependencies

- **Hard**: `src/services/financial_metrics.py` (PER, PBR, debt_ratio, revenue_yoy from `extra_metrics` dict)
- **Hard**: `src/services/risk_analyzer.py` (risk classifications for bear arguments)
- **Hard**: `src/pages/business_card/_sections.py` (re-export pattern)
- **Hard**: `src/pages/business_card/_main.py` (rendering pipeline integration)
- **Soft**: `src/data/yaml/debate_templates.yaml` (content templates)
- **None on Sprint 21/22 features**: Fully independent

### Estimate: 10-16 hours

**Confidence**: Medium. The service layer and UI are straightforward. The main variance is content quality — the YAML templates need careful writing to avoid generic/fluffy arguments. The original 10-14h estimate is validated but we extend the upper bound to 16h to account for content tuning iterations, which are the dominant cost.

---

## C200: "What If I Had Invested?" Historical Scenario Calculator

### Implementation Breakdown

| Layer | Work Items | Hours |
|-------|-----------|-------|
| **Service Layer** | New `src/services/scenario_calculator.py` — `calculate_scenario(stock_id, invest_date, amount, client) -> ScenarioResult`. Fetches historical daily price via `client.get_daily_price()` with date range, computes: shares bought (integer shares, fractional if price allows), current value, total return %, CAGR, dividend-adjusted return (using `dividend_analyzer.py`), comparison to 定期定額 (DCA) over same period. Pure Python, no Streamlit. | 4-5h |
| **Page/UI** | Modify `src/pages/business_card/_historical_scenarios.py` — add interactive input section at top: date picker (`st.date_input`), amount slider (`st.slider` 1000-100000 TWD), "計算" button. Below: show computed scenario card + existing curated scenarios. Add vertical buy-date line to price chart using `chart.py` `create_price_chart()` with Plotly `add_vline`. | 3-4h |
| **Caching** | Implement `st.cache_data` wrapper for the scenario calculation to avoid repeated FinMind API calls for same (stock_id, date, amount) inputs. TTL = 1 hour. Handle cache invalidation when user changes inputs. | 1-2h |
| **Testing** | L0 unit tests for `scenario_calculator.py`: mock FinMind client returning known price series, test return calculation accuracy, test CAGR formula, test edge cases (invest_date = today, invest_date before IPO, non-trading date, zero dividend), test with split-adjusted prices. | 2-3h |
| **Edge Cases** | Invest date on non-trading day (weekend/holiday) → use next trading day, invest date before stock IPO → error message, insufficient price history (< 30 days) → "歷史資料不足", amount too small to buy even 1 share → "投資金額不足以購買", stock delisted → handle gracefully, dividend data missing → show return without dividend adjustment. | 2-3h |

### Technical Risks

1. **FinMind API rate limits (HIGH RISK)**: This feature requires fetching historical daily price for arbitrary date ranges on user interaction. Unlike other features that load data once on page load, this could trigger API calls on every button click. Mitigation: aggressive `st.cache_data` caching with TTL=1h, pre-compute for top 20 stocks at module load, show loading spinner during fetch. If rate limit hit, show friendly message: "目前查詢人數較多，請稍後再試".
2. **Date/price lookup accuracy**: Finding the exact closing price for an arbitrary date requires careful handling. FinMind's `taiwan_stock_daily` returns trading days only. If user picks a weekend, we need to find the next trading day. The existing `chart.py` `create_price_chart()` already handles date filtering, but buy-date price lookup needs a dedicated helper.
3. **Stock splits and dividend adjustments**: Raw FinMind prices are not split-adjusted. For accurate long-term returns, we need split-adjusted prices or explicit split handling. Mitigation: for MVP, use raw prices with a disclaimer: "以上計算未考慮除權息調整，實際報酬可能略有差異". For v2, integrate `dividend_analyzer.py` for adjusted returns.
4. **Scope creep**: The line between "scenario calculator" and "full backtesting engine" is blurry. Users may want to compare multiple dates, add sell dates, or see drawdown analysis. Strict MVP: one buy date, one amount, hold to today.
5. **Existing code integration**: `_historical_scenarios.py` is 320 lines with hardcoded scenarios. Adding interactive mode at the top requires careful restructuring to avoid breaking the existing curated scenario display. The `_section_header` with `collapsed=True` pattern should be reused.

### Dependencies

- **Hard**: `src/data/finmind_client.py` (`get_daily_price()` with date range)
- **Hard**: `src/services/chart.py` (`create_price_chart()` with vline annotation)
- **Hard**: `src/pages/business_card/_historical_scenarios.py` (existing page to extend)
- **Hard**: `src/services/dividend_analyzer.py` (for dividend-adjusted returns — soft dependency, can be v2)
- **Soft**: `src/pages/business_card/_helpers.py` (`_scenario_card`, `_historian_disclaimer` — existing helpers)
- **None on Sprint 21/22 features**: Fully independent

### Estimate: 12-17 hours

**Confidence**: Medium. The core calculation logic is straightforward (4-5h). The main uncertainty is around FinMind API integration for arbitrary date ranges — this hasn't been done before in the codebase (existing code uses fixed lookback periods). The caching layer adds 1-2h. Edge cases around non-trading dates, splits, and delisted stocks add 2-3h. The original 12-16h estimate is validated; we extend to 17h upper bound for the caching + edge case handling.

---

## Recommended Implementation Order

### Sprint 23 Sequence (3 features, ~31-47h total)

**Phase 1 — Foundation First (Week 1):**

1. **C202: Story Arc Timeline Labels** (9-14h)
   - **Why first**: Lowest risk, pure service-layer feature with minimal UI changes. Builds on the well-understood `timeline_service.py`. Completes quickly and provides a "quick win" to start the sprint with momentum. No API dependencies.
   - **Deliverable**: `story_arc_detector.py` service + modified `story_timeline.py` with arc badges.

**Phase 2 — Parallel Track (Week 1-2):**

2. **C199: Bear vs Bull Debate Cards** (10-16h)
   - **Why second**: Can start in parallel with C202's UI phase. The service layer (`debate_engine.py`) is independent. Content template writing (YAML) can begin while C202 is being tested. High visual impact — good for stakeholder demos.
   - **Deliverable**: `debate_engine.py` service + `_debate.py` section + YAML templates.
   - **⚠️ Content review gate**: After initial implementation, schedule a 1-2h content review pass to tune argument quality. This is not optional — bad debate content is worse than no debate content.

3. **C200: What If Calculator** (12-17h)
   - **Why third**: Highest technical risk (API integration, caching, edge cases). Benefits from C202 and C199 being underway first. The FinMind API caching pattern established here will be reusable for future interactive features.
   - **Deliverable**: `scenario_calculator.py` service + modified `_historical_scenarios.py` with interactive mode.
   - **⚠️ API testing gate**: Must test with live FinMind API early in development to validate caching strategy and rate limit handling. Don't wait until the end.

### Sequencing Notes

- **C202 and C199 can be developed in parallel** after C202 service layer is done (first 3-4h). They touch completely different files.
- **C200 should not start until C202 is complete** to avoid context-switching between three features. Ideally start C200 in Week 2.
- **All three features are independent of Sprint 21 (C170, C188) and Sprint 22 (C201)**. No blocking dependencies.
- **If Sprint 23 capacity is limited**, C202 alone (9-14h) is the highest-value single feature. C199+C200 can defer to Sprint 24.

### Alternative: Reduced Scope Sprint

If the sprint capacity is ~20h instead of ~40h, recommend:
- **C202** (9-14h) + **C199 service layer only** (6-8h, skip UI integration)
- This delivers the story arc feature complete and leaves the debate engine service ready for UI wiring in the next sprint.

---

## Total Sprint 23 Estimate

| Feature | Low Estimate | High Estimate | Priority | Risk Level |
|---------|-------------|---------------|----------|------------|
| C202: Story Arc Timeline Labels | 9h | 14h | P2 MUST | Low |
| C199: Bear vs Bull Debate Cards | 10h | 16h | P2 SHOULD | Medium |
| C200: What If Calculator | 12h | 17h | P2 COULD | Medium-High |
| **Total** | **31h** | **47h** | | |

### Risk-Adjusted Recommendation

- **Optimistic** (31h): All features complete with minimal content tuning. Assumes heuristic arc detection works well on first try, debate templates need only 1 revision, and FinMind API caching works cleanly.
- **Realistic** (39h): 1 round of content tuning for C199, minor arc detection threshold adjustments for C202, and 1-2 edge case fixes for C200 API integration.
- **Pessimistic** (47h): 2-3 rounds of debate content revision, arc detection needs significant threshold tuning, and C200 requires additional caching/rate-limit work.

### Key Cross-Cutting Risks

| Risk | Features Affected | Mitigation |
|------|-------------------|------------|
| Content quality / historian tone | C199, C202 | Pre-write YAML templates; schedule content review gate |
| FinMind API rate limits | C200 | `st.cache_data` with TTL; pre-compute for top 20 stocks |
| Scope creep | C200 | Strict MVP: one buy date, one amount, hold to today |
| Heuristic quality | C202 | Minimum event threshold (≥3 in 6 months); non-overlapping windows |
| Stakeholder expectations | C199 | Set expectation: template-based arguments, not AI-generated debate |
