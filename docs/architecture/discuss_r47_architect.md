# 2026-06-15 Technical Analysis — Discussion Round 47

> **Author**: System Architect
> **Context**: Sprint 21 ✅ COMPLETE. Sprint 22 (C201 今日市場動態) starting. This is a DISCUSSION cycle evaluating Sprint 23 feature candidates (C199, C200, C202) from Round 46 competitor research.
> **Architecture Health**: B+ (47 service modules, 0 god modules, L0: 135 passed, L1: 20 pre-existing FinMind failures)
> **Key Constraint**: LLM integration layer (D5) is RESOLVED — template-based explanations via ExplanationProvider protocol. All service layers are Streamlit-free (100% pure Python).

---

## Feature Direction 1: C202 "Story Arc" Timeline Labels — Auto-Detected Narrative Arcs

**Description**: Automatically detect narrative "arcs" on the company event timeline — grouping sequential events into story phases like "Expansion Phase," "Crisis & Recovery," "Profit Surge." Labels appear as colored phase banners on the timeline between events.

- **Feasibility**: 🟡 **MEDIUM-HIGH** (rule-based feasible; LLM-based not viable)
- **Dependencies**:
  - `timeline_service.py` (299 lines) — provides `get_timeline()` pipeline merging events + milestones + case studies
  - `adaptive_engine.py` (622 lines) — provides `get_events_for_stock()` with event types and severity
  - `events.yaml` (232 lines of recent events) — data source for event stream
  - `event_interpretation_service.py` (123 lines) — existing interpretation templates
  - No new data sources needed
- **Risks**:
  - **Detection quality is the core risk**: "Narrative arc" detection via rules is possible but shallow. The rule-based approach would look for patterns like: 3+ "high" severity events within 30 days → "Crisis Phase"; consecutive "revenue_surge" events → "Growth Phase"; "news_major" + "price_abnormal" co-occurrence → "Market Overreaction." These heuristics are simplistic and may produce false arcs.
  - **Round 46 correctly identified this as deferred** — the original objection was "LLM-based narrative detection is not viable." But with rule-based detection, it IS viable, just limited. The question is whether "limited but useful" meets the quality bar.
  - **Edge case**: Stocks with sparse events (e.g., only 1-2 events in a year) would produce no arcs. Need graceful degradation — show nothing rather than pretending.
  - **Phase boundary ambiguity**: When does a "Growth Phase" end and a "Stabilization Phase" begin? Rule-based thresholds will be arbitrary. Need empirical tuning against 2-3 well-known stocks.
  - **No LLM creativity**: All arc labels and descriptions come from templates. This is consistent with the architect's "template-only" decision but limits narrative richness.
- **Architecture Fit**:
  - **Clean 4-layer fit**: New `story_arc_detector.py` service (pure functions: `detect_arcs(events) → list[ArcPhase]`) consumes `get_timeline()` output, produces arc metadata.
  - Output consumed by `story_timeline.py` (169 lines) or `company_timeline.py` (121 lines) — both already render timeline cards. Arc labels would be rendered as banners between events.
  - **Service layer is Streamlit-free**: The arc detection logic is pure Python. Only the rendering layer (page files) would use Streamlit for display.
  - **Zero new API calls or data sources**: All input data already exists in `events.yaml` + `adaptive_engine.py` output.
  - **Pattern follows existing conventions**: `adaptive_engine.py` already has severity scoring and false-positive filtering. `story_arc_detector.py` would follow the same pattern: pure functions, YAML-configurable thresholds, no external dependencies.
- **Effort**: 10-14h
  - Service (`story_arc_detector.py`): 4-5h (rule engine + phase templates)
  - Phase label templates (YAML): 2-3h (need ~15-20 phase types with TW Chinese labels)
  - Page integration (`story_timeline.py`): 2-3h (rendering arc banners between events)
  - Edge case handling + testing: 2-3h (sparse events, boundary conditions, tuning thresholds)
- **Competitive Value**: **Medium-High**. No TW competitor auto-detects narrative arcs on timelines. Zerodha Varsity has narrative-first design but not auto-detected arcs. TipRanks groups events by theme but not by temporal arc. This could be a unique "historian" differentiator — the timeline doesn't just show events, it tells the **chapters** of the company's story. Aligns with Core Value #1 "Story first, data second."
- **Round 46 → Round 47 delta**: Round 46 deferred this feature pending "real LLM implementation." **Round 47 revises this**: rule-based arc detection is feasible NOW and delivers 80% of the value. The "intelligent narrative" enhancement (LLM-generated arc summaries) remains a future Sprint 24+ enhancement. Recommend **proceeding with rule-based v1**.

---

## Feature Direction 2: C199 "Bear vs Bull" Visual Debate Cards

**Description**: Side-by-side cards presenting bull and bear arguments for a stock, with icons and key stats. Example: "🐂 Bull Case: AI chip demand growing 30% YoY, TSMC leads advanced nodes" vs "🐻 Bear Case: Geopolitical risk, capex cycle peak, valuation at 25x P/E."

- **Feasibility**: 🟡 **MEDIUM** (data exists but synthesis is content-heavy)
- **Dependencies**:
  - `risk_analyzer.py` (567 lines) — provides bear case inputs: debt risk, margin risk, concentration risk, event risk
  - `financial_metrics.py` — provides current metric values (ROE, P/E, debt ratio, etc.)
  - `adaptive_engine.py` — provides recent events (high-severity events feed bear case)
  - **No existing bull case generator**: The bull case needs revenue growth, market position, competitive advantages — data that exists in `company_facts.py` and `revenue_analyzer.py` but isn't synthesized into a bull argument.
  - No new data sources needed, but significant template content is required.
- **Risks**:
  - **Bull case construction is the hardest part**: Bear case data is comprehensive (risk_analyzer.py is 567 lines of risk signals). But bull case requires synthesizing positive signals — revenue growth trajectory, market share, competitive moat — into a coherent narrative. The `moat_analyzer.py` and `analogy_engine.py` provide some inputs but not a complete bull case.
  - **Balance risk**: Bull/bear cards must be genuinely balanced, not subtly biased. If the bull case always sounds stronger (because positive data is more abundant), users may perceive hidden endorsement. Needs careful template design to ensure both cases are equally substantive.
  - **Content volume**: Each stock needs 3-5 bull points and 3-5 bear points. With 20+ TW stocks in the system, this is 60-100 curated argument templates OR a very sophisticated rule-based generator. Template approach is feasible for v1 scoped to top 10 stocks.
  - **Tone risk**: "Bull case" stock arguments can be interpreted as investment advice. The historian positioning requires framing as "here are the arguments people make" not "here's why you should buy." Needs historian disclaimers.
  - **Round 46 agreed with deferral**: "Recommend deferring to Sprint 23+ when narrative infrastructure is mature." The C188 "Why Did This Move?" feature improves narrative quality. If C188 lands well in Sprint 21, C199 becomes more feasible for Sprint 23.
- **Architecture Fit**:
  - New `debate_card_service.py` (pure functions: `generate_bull_case(stock_id)`, `generate_bear_case(stock_id)`).
  - New `_debate_cards.py` section file in `business_card/_sections/`.
  - Uses existing `risk_analyzer.py` (bear), `financial_metrics.py` (both), `moat_analyzer.py` (bull), `revenue_analyzer.py` (bull).
  - Clean 4-layer fit, but the `debate_card_service.py` module would be one of the more complex pure-Python modules (~300-400 lines of rule-based synthesis logic).
- **Effort**: 12-16h
  - Bear case service (synthesizing risk_analyzer.py outputs): 3-4h
  - Bull case service (synthesizing revenue + moat data): 5-6h (**this is the hard part**)
  - Template/argument pool (10 stocks × 4-5 arguments each): 3-4h
  - Page integration + visual card design: 2-3h
  - Tone QA + historian positioning: 1-2h
- **Competitive Value**: **Medium**. TipRanks has analyst bull/bear arguments. StockEdge has "Edge Score" with explanations. But no TW competitor has visual debate cards side-by-side. The "debate" format is engaging and educational — it teaches beginners that every stock has both positive and negative arguments. Aligns with Core Value #1 "Story first, data second" — the bull/bear is essentially two competing stories.
- **Round 46 → Round 47 delta**: Round 46 recommended deferral. **Round 47 conditionally agrees** — only pursue C199 in Sprint 23 IF: (1) C188 "Why Did This Move?" lands well in Sprint 21 and its narrative patterns can be reused, AND (2) scope is limited to top 10 TW stocks with template-curated arguments. Otherwise, defer to Sprint 24.

---

## Feature Direction 3: C200 "What If I Had Invested?" Historical Scenario Calculator

**Description**: Interactive calculator where users pick a past date and investment amount. System shows what would have happened — price appreciation + dividends received. "If you invested $10,000 in TSMC on 2020-03-15, your shares would be worth $X today plus $Y in dividends."

- **Feasibility**: ✅ **HIGH** (easiest of the three candidates)
- **Dependencies**:
  - `_historical_scenarios.py` (320 lines) — **already exists** as C74 implementation with curated scenarios for major TW stocks
  - `chart_stock.py` — provides historical price data via FinMind
  - `dividend_analyzer.py` (201 lines) — provides dividend history and yield calculations
  - `finmind_client.py` — underlying data source for price + dividend DataFrames
  - No new data sources needed
  - No LLM layer needed — pure calculation + template explanation
- **Risks**:
  - **C74 overlap is the key consideration**: `_historical_scenarios.py` already implements historical scenario analysis — but as curated, pre-written scenarios (e.g., "If you invested in TSMC in March 2020..."). C200 would make this interactive and generalized — any date, any amount, any stock with sufficient data. This is a **significant enhancement**, not greenfield. Need to decide: extend `_historical_scenarios.py` or create new `scenario_calculator.py` service.
  - **Scope creep**: v1 should be price appreciation + simple dividend accumulation. Inflation-adjusted returns, benchmark comparison, and dividend reinvestion are natural follow-ups that must be deferred.
  - **Date boundary issues**: Users may pick dates before IPO, dates with missing FinMind data, or future dates. Need robust edge case handling with clear error messages in both Chinese and English.
  - **Tone risk**: Showing large historical returns (e.g., "your $10,000 would be worth $43,000 today") is inherently sensational. The historian positioning requires: (a) prominent disclaimer, (b) contextualization ("TSMC happened to perform exceptionally; many stocks from 2020 are worth less today"), (c) never show percentage returns without time period context.
  - **Session state management**: Interactive recalculation on every date/amount change needs careful Streamlit session state to avoid redundant FinMind API calls.
- **Architecture Fit**:
  - **Excellent fit** — follows the exact same pattern as the existing `_historical_scenarios.py` but generalized.
  - New `scenario_calculator.py` service module: pure functions `calculate_return(stock_id, start_date, amount) → ScenarioResult`.
  - Extends existing `_historical_scenarios.py` rather than replacing it — curated scenarios remain as "Featured Scenarios" while the calculator provides "Custom Scenarios."
  - Uses existing `chart_stock.py` for price data, `dividend_analyzer.py` for dividend data, `company_facts.py` for company name.
  - Clean 4-layer: Data (FinMind) → Service (scenario_calculator) → Page (enhanced _historical_scenarios.py) → Presentation (Streamlit date_input + number_input).
- **Effort**: 10-12h
  - `scenario_calculator.py` service: 3-4h (pure calculation logic, edge cases)
  - Enhance existing `_historical_scenarios.py` with interactive mode: 3-4h
  - Tone QA + historian disclaimers + contextualization: 2-3h
  - Testing + edge case handling: 1-2h
  - Note: This is **less than the original 12-16h estimate** from Round 46 because `_historical_scenarios.py` (320 lines) already exists as C74 foundation. We're building on top of it, not starting from scratch.
- **Competitive Value**: **High**. Magnify.money has this and it's one of their most shared features. StockStory's "What If" calculator is proven engagement driver. This feature directly teaches the most important investing lesson — time in the market — without being advisory. It's also inherently shareable ("See what $10,000 in TSMC would be worth"), which drives organic growth.
- **Round 46 → Round 47 delta**: Round 46 ranked this as Priority 2 after C201. **Round 47 agrees with high priority** but notes the existing C74 codebase significantly de-risks the implementation.

---

## Features NOT Recommended for Sprint 23

None of these are outright rejected — C199 is conditionally recommended. The remaining P2 features from Round 46 (C203 Supply Chain, C206 Recurring Investment, C207-C214 from Round 10) continue to be deferred per their original analysis.

---

## Recommendation

### Priority Order for Sprint 23

| Priority | Feature | Effort | Rationale |
|----------|---------|--------|-----------|
| **1** | **C200 What If I Had Invested** | 10-12h | ✅ Highest feasibility. ✅ Existing C74 codebase de-risks implementation. ✅ Proven engagement driver (Magnify.money, StockStory). ✅ No content curation bottleneck. ✅ Pure calculation — template explanations sufficient. Best ROI per hour invested. |
| **2** | **C202 Story Arc Timeline Labels** | 10-14h | 🟡 Medium-high feasibility with rule-based detection. ✅ No new data sources. ✅ Clean architecture fit. ✅ Unique "historian" differentiator — no TW competitor does this. ⚠️ Detection quality limited by rule-based approach, but "limited but useful" is acceptable for v1. |
| **3** | **C199 Bear vs Bull Debate Cards** | 12-16h | 🟡 Conditional — only if C188 lands well and narrative patterns can be reused. ⚠️ Bull case synthesis is content-heavy. ❌ Highest effort, highest content risk. **Recommend deferring to Sprint 24** unless C188 proves the narrative infrastructure is mature enough. |

### Suggested Sprint 23 Sequence

1. **Week 1**: C200 (What If I Had Invested) — lead feature, cleanest implementation path
2. **Week 2**: C202 (Story Arc Timeline Labels) — builds on C200's momentum, both are "historian storytelling" features
3. **Stretch/Week 3**: C199 (Bear vs Bull) — only if C188 review shows strong narrative infrastructure; otherwise begin C207 (Contextual Education Nuggets) or C208 (Prerequisite Chains) from Round 10

### Key Architectural Considerations

1. **C74 is the foundation for C200**: The existing `_historical_scenarios.py` (320 lines with curated TSMC/鴻海/緯穎 scenarios) means C200 is an enhancement, not greenfield. The `scenario_calculator.py` service module should be designed to coexist with (not replace) the curated scenarios. Curated scenarios serve as "Featured" examples; the calculator serves as "Explore Yourself."

2. **Template-based explanations are sufficient for all three features**: C200 needs calculation result templates ("Your $X would be worth $Y"). C202 needs phase label templates ("Growth Phase," "Crisis & Recovery"). C199 needs bull/bear argument templates. None require LLM generation. This is architecturally consistent with the D5 resolution.

3. **C202's rule-based arc detection should be YAML-configurable**: The phase detection rules (e.g., "3+ high severity events in 30 days → Crisis Phase") should be in a YAML config file, not hardcoded. This follows the `events.yaml` pattern and allows tuning without code changes. The `story_arc_detector.py` service should be ~200-250 lines with ~100 lines of YAML config.

4. **C199 should NOT be attempted if C188 review is negative**: The bear case is well-supported by `risk_analyzer.py`. The bull case requires synthesizing revenue growth, market position, and competitive advantages — data that exists but synthesis logic that doesn't. If C188's narrative patterns (developed in Sprint 21) prove robust and reusable, C199 becomes feasible. If C188 needs iteration, pushing C199 to Sprint 24 is the right call.

5. **All three features are presentation-heavy**: Monitor `_router_base.py` and `business_card/_sections/` growth. The existing `_historical_scenarios.py` is already 320 lines (page-level). Converting it to an interactive calculator + keeping curated scenarios may push it to 450+ lines. If so, extract the calculator UI into a separate `_scenario_calculator_ui.py` to keep files under 400 lines (D-127 pattern).

6. **FinMind dependency remains the #1 reliability risk**: All three features depend on FinMind data (prices, dividends, events). The 20 pre-existing L1 FinMind failures are acceptable for Sprint 23 features since C200/C202 degrade gracefully (missing data → "data unavailable" message). But if L1 failures increase, C200's "any date, any stock" promise will be tested.

---

*Created: 2026-06-15*
*Maintainer: System Architect*
*Next review: Sprint 23 kickoff*
