# 2026-06-15 Technical Analysis — Discussion Round 46

> **Author**: System Architect
> **Context**: Sprint 20 COMPLETE. Sprint 21 planned: C170 + C188 + D-125/126/127. This is a DISCUSSION cycle evaluating future feature directions from Round 46 competitor research (C199-C206).
> **Architecture Health**: B+ (47 service modules, 0 god modules, L0/L1 passing, 319+ tests)
> **Key Constraint**: LLM integration layer (D5) is RESOLVED — `src/services/llm/` package exists with base.py, template_provider.py, factory.py. All explanations are template-based via the ExplanationProvider protocol.

---

## Feature Direction 1: C205 "Read Time" Indicator + C204 "Confidence Indicator" Bundle

**Description**: A bundled "content metadata" feature pair. C205 adds "X min read" estimates to every section and lesson (2-4h). C204 adds emoji-based 🟢🟡🔴 confidence indicators on all AI/template explanations (4-6h). Together they form a "content trust & effort" layer.

- **Feasibility**: ✅ **HIGH**
- **Dependencies**: None for C205 (pure presentation). C204 requires a confidence scoring strategy — but since all explanations are template-based (not LLM-generated), confidence can be derived from data freshness and source reliability, not model uncertainty.
- **Risks**:
  - C204's value is limited when explanations are template-based rather than LLM-generated. The confidence indicator would reflect "data confidence" (how recent is the data? how many data points?) rather than "AI confidence" (how sure is the model?). This is actually MORE honest but less flashy.
  - C205's read-time estimation is heuristic-based (word count / reading speed). Chinese text read-time estimation is less standardized than English. Need to calibrate for mixed Chinese/English financial content.
  - Risk of "metadata overload" — adding indicators to every section could create visual clutter. Needs careful design.
- **Architecture Fit**:
  - C205: Pure presentation layer. Add a `_read_time(text)` helper in `_router_base.py` or `ui_components.py`. Wrap section headers. Minimal service layer impact.
  - C204: Requires a small `confidence_service.py` (pure functions: `score_data_freshness()`, `score_source_reliability()`) and a `_confidence_badge(level)` UI component. Fits cleanly into the 4-layer architecture.
  - Both features are presentation-layer only — zero new API calls, zero new data sources.
- **Effort**: 6-10h total (C205: 2-4h + C204: 4-6h). Can be done sequentially or in parallel by two developers.
- **Competitive Value**: Low-to-medium. Finimize and Robinhood both have these. They're "table stakes" for modern financial apps but not differentiators. However, they reduce commitment anxiety (C205) and teach critical thinking (C204) — both align with the "historian" positioning.

---

## Feature Direction 2: C200 "What If I Had Invested?" Historical Scenario Calculator

**Description**: An interactive tool where users pick a past date and investment amount, and the system shows what would have happened — "If you invested $10,000 in TSMC on 2020-03-15, it would be worth $X today." Educational, not advisory.

- **Feasibility**: ✅ **HIGH**
- **Dependencies**:
  - Historical price data: Already available via FinMind client (`get_stock_price()`).
  - Dividend data: Already available via `dividend_analyzer.py`.
  - No LLM layer needed — pure calculation + template explanation.
  - No new data sources required.
- **Risks**:
  - **Scope creep**: The feature could expand to include dividend reinvestment, inflation adjustment, comparison with benchmarks, etc. Must be scoped to "simple price appreciation + dividend" for v1.
  - **Tone risk**: Showing large historical returns could be interpreted as "stocks always go up." Needs careful framing — "past performance ≠ future results" disclaimer and contextualization (e.g., "TSMC happened to do well, but many stocks from 2020 are worth less today").
  - **Date boundary issues**: Users might pick dates before the stock was listed, or dates with missing data. Need robust error handling.
  - **Streamlit interactivity**: The "what if" interaction pattern (date picker + amount input → dynamic recalculation) is straightforward in Streamlit but needs careful session state management to avoid recomputation on every keystroke.
- **Architecture Fit**:
  - New `scenario_calculator.py` service module (pure functions: `calculate_return(stock_id, start_date, amount)`, `format_scenario_result()`).
  - New page or section in `business_card/_sections/` — a `_scenario.py` section file.
  - Uses existing `chart_stock.py` for optional visualization (price line with entry point marker).
  - Clean 4-layer fit: Data (FinMind) → Service (scenario_calculator) → Page (_scenario.py) → Presentation (Streamlit widgets).
- **Effort**: 10-14h (service: 3-4h, page/UI: 4-5h, tone QA + edge cases: 2-3h, testing: 1-2h).
- **Competitive Value**: Medium-high. Magnify.money and StockStory both have this. It's a proven engagement driver and directly educational — teaches beginners about time in the market without being advisory.

---

## Feature Direction 3: C201 "Daily Market Story" 3-Minute Morning Briefing Card

**Description**: A P1-elevated feature (from C196) that shows a "daily market story" card on the homepage — a 3-minute briefing covering what happened in the market today, told as a narrative with plain-language explanations.

- **Feasibility**: 🟡 **MEDIUM** (architecturally feasible, but content pipeline is the bottleneck)
- **Dependencies**:
  - `market_data.py` (exists since Round 46 review) — provides market-wide data.
  - `story_feed.py` (exists, 283 lines) — provides story feed infrastructure.
  - `src/services/llm/` package (exists) — but all explanations are template-based. The "daily story" needs narrative generation, which is the hardest part.
  - **D25 (market_data.py)** is already resolved per the Round 46 review.
  - **No new API data sources** — FinMind provides market-level data.
- **Risks**:
  - **Content generation is the bottleneck**: The feature's value depends on the quality of the daily narrative. With template-based explanations (no LLM), the stories will be formulaic: "Today the TAIEX rose/fell X% driven by Y sector." This is useful but not compelling. The P1 elevation assumes narrative quality that templates alone may not deliver.
  - **Daily cadence requirement**: Unlike all other features (which are on-demand), this feature implies a daily update. This requires either: (a) real-time data fetching on page load (slow), (b) pre-computed daily stories cached in YAML (requires a cron/batch job), or (c) static "today's story" that updates when the user refreshes. Option (b) is best but adds operational complexity.
  - **Homepage real estate**: The homepage (`main.py` or `home_page.py`) needs a prominent card. Current homepage layout may need restructuring.
  - **Tone risk**: Market-level narratives can easily sound like investment advice ("tech stocks rallied today" → implies you should buy tech). The 3-layer tone QA must be enforced.
- **Architecture Fit**:
  - New `daily_briefing.py` service module — fetches market data, selects top movers, generates narrative from templates.
  - New `_daily_briefing.py` section file for homepage integration.
  - Uses existing `market_data.py` for data, `story_feed.py` patterns for narrative structure.
  - If daily caching is needed: new `src/data/daily_briefings/` YAML files + a scheduled job (cron or GitHub Action).
  - 4-layer fit is clean, but the "daily cadence" requirement introduces an operational dimension that the current architecture doesn't have.
- **Effort**: 12-16h (service + narrative templates: 5-6h, homepage integration: 2-3h, daily caching pipeline: 3-4h, tone QA: 2-3h).
- **Competitive Value**: **HIGH** — this is the #1 retention pattern identified in competitor research. Finimize's daily briefing is their core product. Robinhood's daily market card drives daily opens. No TW competitor has a daily narrative briefing. This could be Stock Explorer's killer retention feature.

---

## Features NOT Recommended for Near-Term

### C199 "Bear vs Bull" Visual Debate Cards (8-12h, P2)
- **Feasibility**: 🟡 Medium. Requires curated bull/bear arguments per stock. The data exists (events, metrics, risks) but synthesizing balanced arguments is content-heavy. The `risk_analyzer.py` and `adaptive_engine.py` provide half the inputs (bear case), but the bull case needs manual curation or a new `bull_case_generator.py`. **Recommend deferring to Sprint 23+** when narrative infrastructure (C152/C188) is mature.

### C202 "Story Arc" Timeline Labels (8-10h, P2)
- **Feasibility**: 🟡 Medium. "Auto-detected narrative arcs" implies either: (a) rule-based pattern matching on events (feasible but limited), or (b) LLM-based narrative detection (not viable with template-only explanations). Option (a) is possible with `timeline_service.py` + `events.yaml` but the detection quality will be low. **Recommend deferring** until the LLM layer has a real implementation beyond templates.

### C203 "Supply Chain Impact" Visual Map (14-18h, P2)
- **Feasibility**: 🟡 Medium. The highest-effort P2 feature. `group_structure.py` has some relationship data, but comprehensive customer-supplier data doesn't exist in the system. Would require either manual curation (100+ stocks × multiple relationships) or a new data source. The visualization (network graph) is also new — no existing network diagram component. **Recommend deferring to Sprint 24+** as a capstone feature.

### C206 "Recurring Investment" Concept Education (6-8h, P2)
- **Feasibility**: ✅ High, but low priority. Pure educational content — a new section or lesson about dollar-cost averaging. No new data sources, no new services. Could be added to `metric_education.py` or as a new lesson in `lesson_service.py`. **Recommend bundling with C170 (Tappable Glossary) in Sprint 21** as a stretch goal, or deferring to Sprint 22.

---

## Recommendation

### Priority Order for Sprint 22+

| Priority | Feature | Effort | Rationale |
|----------|---------|--------|-----------|
| **1** | **C201 Daily Market Story** | 12-16h | P1, elevated from C196. #1 retention pattern. No TW competitor has this. Architecturally feasible with existing `market_data.py` + `story_feed.py`. The content pipeline (daily caching) is the main risk but can start with on-demand generation. |
| **2** | **C200 What If I Had Invested** | 10-14h | High engagement, proven demand (Magnify.money, StockStory). Pure calculation — no content curation bottleneck. Clean architecture fit. Good companion to C201 (both are "personal" features). |
| **3** | **C204 + C205 Metadata Bundle** | 6-10h | Low effort, table-stakes features. Can be done as filler work or by a second developer in parallel with C201/C200. Reduces commitment anxiety (C205) and teaches critical thinking (C204). |

### Sprint 21 Impact

**None of these features should be added to Sprint 21.** Sprint 21 is already planned with C170 + C188 + D-125/126/127. The features above are for **Sprint 22+** planning.

### Suggested Sprint 22 Sequence

1. **Day 1**: D-125 (chart_stock.py split) + D-126 (INDUSTRY_BENCHMARKS dedup) — carry over from Sprint 21 if not done
2. **Week 1**: C201 (Daily Market Story) — lead feature, highest retention impact
3. **Week 2**: C200 (What If I Had Invested) — engagement feature
4. **Parallel/Stretch**: C204 + C205 (Metadata Bundle) — low effort, can be done alongside C200

### Key Architectural Considerations

1. **Template-based explanations limit narrative quality**: C201's "Daily Market Story" will only be as good as its templates. The `src/services/llm/` package exists but uses `TemplateExplanationProvider`. If the team wants truly dynamic daily narratives, the LLM layer needs a real implementation (not just templates). **Recommend treating C201 as a stepping stone** — ship with templates in Sprint 22, enhance with real LLM in Sprint 24+.

2. **Daily cadence is a new operational pattern**: C201 is the first feature that implies daily content updates. The current architecture has no caching/cron infrastructure for this. **Recommend starting with on-demand generation** (user opens homepage → fetch today's data → generate story) and adding a daily cache later if performance requires it.

3. **All three recommended features are presentation-heavy**: C201, C200, and C204/C205 all add UI elements to existing pages. This continues the pattern of presentation-layer growth. **Monitor `_router_base.py` and `business_card/_sections/` file sizes** — D-127 (_summary.py at 464 lines) may need attention if C200 adds a new section file.

4. **No new data sources needed**: All three recommended features use existing FinMind data. This is a key architectural advantage — the data layer is mature and doesn't need expansion for these features.

---

*Created: 2026-06-15*
*Maintainer: System Architect*
*Next review: Sprint 22 kickoff*
