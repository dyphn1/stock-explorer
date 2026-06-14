## 2026-06-15 Technical Analysis — Discussion Round 45

### Proposed Feature Directions

---

#### Direction 1: C170 Tappable Glossary — Inline Metric Definitions with Contextual Judgment Callouts (Combined C170 + C194)

- **Description**: Every financial metric on the business card page gets a tappable glossary tooltip. But beyond just defining the term (C170), each tooltip includes a **judgment callout** (C194) — explaining *why* this particular value is labeled "good" or "bad." For example, tapping on "ROE 28%" shows: "ROE (Return on Equity) = how much profit a company generates from shareholder money. 28% is considered **strong** — the semiconductor industry average is ~15%, so TSMC is nearly double." This combines the oldest P2 gap (C33 → C170, elevated in Round 40) with the most under-explored competitor gap (C194 — no competitor explains the reasoning behind good/bad labels). The feature also extends to the event narratives (C152) — when a multi-factor narrative mentions "毛利率下降," the term is tappable for inline definition.

- **Technical Approach**:
  - **Data layer**: Create `src/data/glossary.yaml` with 50+ metric entries. Each entry has: `term_zh`, `term_en`, `definition_plain`, `formula`, `benchmark_industry`, `good_threshold`, `bad_threshold`, `judgment_template`. The `judgment_template` is a string template like `"{value}% is considered **{label}** — the {industry} average is ~{benchmark}%, so {company} is {comparison}."` This is pure YAML data, no LLM needed.
  - **Service layer**: New `src/services/glossary_service.py` — loads YAML, provides `get_definition(metric_key) -> dict`, `get_judgment(metric_key, value, industry) -> str`. Pure functions, no state. Imports `financial_metrics.py` for benchmark data (after D-120 extraction).
  - **Presentation layer**: In `business_card.py`, wrap every metric display with a Streamlit `st.expander` or `st.popover` (Streamlit 1.40+ supports `st.popover`). Each metric shows a ℹ️ icon. Clicking it opens the glossary definition + judgment callout. For C152 event narratives, use `st.tooltip` on metric keywords within the narrative text.
  - **D-120 prerequisite**: The judgment callout needs `INDUSTRY_BENCHMARKS` data. D-120 extracts this to YAML + shared service. C170/C194 depends on D-120 being complete.

- **Pros**:
  - Highest-ROI educational feature: transforms every data point into a learning opportunity without requiring the user to navigate away
  - Directly addresses the "ten-second test" — a beginner can restate what a metric means within 10 seconds of tapping
  - C194 (judgment callout) is a **unique differentiator** — no competitor explains *why* something is labeled good/bad (validated by Round 12 research: Inderes, Morningstar, Gurufocus all label but don't explain reasoning)
  - Pure data + template approach — zero LLM dependency, zero hallucination risk
  - YAML-driven content is maintainable by non-developers
  - Enables C152 — multi-factor narratives become more useful when terms are inline-defined

- **Cons**:
  - 50+ glossary entries require significant content creation effort (the YAML file is the bottleneck, not the code)
  - `st.popover` availability depends on Streamlit version (need 1.40+); fallback to `st.expander` if not available
  - Judgment templates may feel repetitive for metrics with similar patterns (all percentage-based metrics use similar templates)
  - D-120 dependency means this can't start until benchmark extraction is complete
  - `business_card.py` is already 561 lines (D24/D30 debt) — adding inline glossary wrappers to every metric will grow it further. The D24 extraction (business_card/ sub-directory) should happen before or alongside this feature.

- **Effort**: 12-18 hours
  - D-120 prerequisite: 1.5-2.5h (benchmark extraction, already planned for Sprint 21)
  - `glossary.yaml` content creation: 4-6h (50+ entries with definitions, benchmarks, judgment templates)
  - `glossary_service.py`: 1-2h (YAML loader + judgment function)
  - `business_card.py` integration: 3-4h (wrap 15+ metrics with popover/expander)
  - C152 narrative integration: 1-2h (tooltip on metric keywords in event narratives)
  - Testing + edge cases: 1-2h

- **Architectural Impact**:
  - **Data layer**: New `src/data/glossary.yaml` (additive, no changes to existing data)
  - **Service layer**: New `src/services/glossary_service.py` (additive)
  - **Presentation layer**: `business_card.py` modified (grows from 561 → ~620 lines; D24 extraction recommended first)
  - **No changes to**: routing layer, data layer (FinMind client), chart.py
  - **Dependency**: D-120 (benchmark extraction) must be complete first

- **Vision Alignment**:
  - ✅ Core value #1 "Story first, data second" — every metric gets a plain-language story
  - ✅ Core value #4 "Point-to-point knowledge construction" — inline definitions build knowledge at the point of encounter
  - ✅ "Ten-second test" — a beginner can understand any metric within 10 seconds of tapping
  - ✅ "Historian" positioning — explains what happened (this metric is high/low because...), doesn't predict

---

#### Direction 2: C152 Multi-Factor Event Narratives — "One Story, All Factors Combined"

- **Description**: Currently, Stock Explorer shows events as isolated data points (e.g., "Revenue dropped 5% in March" and "Gross margin declined 2% in March" as two separate items). C152 synthesizes multiple factors into a single coherent narrative: "In March, TSMC's revenue dropped 5% **because** seasonal chip demand weakened, **and** gross margin declined 2% **because** factory utilization fell to 75%. **However**, this was partially offset by a 3% increase in advanced chip orders from NVIDIA." This is the "historian" positioning in action — telling the full story of what happened, not just listing disconnected facts. The feature directly counters StockStory and Stockopedia AI's narrative capabilities (Round 12-13 research) and is the most strategically important feature for defending the "historian" positioning.

- **Technical Approach**:
  - **Data layer**: Uses existing `adaptive_engine.py` event data + `financial_metrics.py` delta calculations + `analogy_engine.py` analogy templates. No new data sources needed.
  - **Service layer**: New `src/services/narrative_engine.py` — the core synthesis engine. Takes a time window (default: 1 quarter), gathers all events + metric deltas within that window, groups them by time proximity, and generates a multi-factor narrative using templates. The template system has 5 pre-written narrative patterns:
    1. **"Headline + supporting factors"** — one primary event + 2-3 contributing factors
    2. **"Offsetting factors"** — positive + negative factors that partially cancel out
    3. **"Causal chain"** — A caused B which caused C
    4. **"Sector-driven"** — sector-level event affecting the company
    5. **"Mixed signals"** — contradictory indicators requiring judgment
  - **Presentation layer**: New "📖 事件故事" section in `business_card.py` below the existing event dashboard. Shows 1-3 multi-factor narratives per quarter. Each narrative is a plain-language paragraph with inline metric references (tappable via C170 glossary).
  - **D-16 prerequisite**: `analogy_engine.py` provides analogy templates for narrative text. D16 (split analogy_engine.py) should be done first to isolate the analogy functions from the god module.
  - **D-120 prerequisite**: Benchmark context for narratives (e.g., "毛利率下降2%，但仍在產業平均之上").

- **Pros**:
  - **Strategic differentiator** — no TW competitor synthesizes multiple factors into coherent narratives. StockStory and Stockopedia AI do this for US stocks; Stock Explorer can do it for TW stocks with better localization
  - Directly embodies "historian" positioning — tells the full story, not just disconnected facts
  - Template-based approach is safe (no hallucination risk) and maintainable
  - Natural extension of existing `adaptive_engine.py` + `analogy_engine.py` infrastructure
  - C170 glossary integration makes narratives self-contained (readers can tap any metric for definition)
  - High competitive moat — narrative quality improves over time as templates are refined

- **Cons**:
  - Template-based narratives may feel formulaic — only 5 patterns means limited variety
  - Requires D-16 (analogy_engine.py split) and D-120 (benchmark extraction) as prerequisites — 2 dependencies
  - Narrative quality depends heavily on the quality of the 5 templates — poor templates = poor narratives
  - Risk of "narrative overload" — if every quarter generates 3 narratives, the page becomes text-heavy. Need strict quality threshold (only generate narratives when factors are genuinely related)
  - `business_card.py` is already 561 lines — adding narrative section pushes it toward 650+ lines. D24 extraction is strongly recommended first.
  - The "causal chain" pattern is the hardest to implement correctly — causal inference from correlation is risky for the "historian" positioning

- **Effort**: 16-22 hours
  - D-16 prerequisite: 2-3h (analogy_engine.py split, already planned for Sprint 21)
  - D-120 prerequisite: 1.5-2.5h (benchmark extraction, already planned for Sprint 21)
  - `narrative_engine.py` service: 6-8h (event grouping, factor synthesis, 5 template patterns)
  - Template content creation: 3-4h (5 narrative patterns × multiple industry variants)
  - `business_card.py` integration: 2-3h (narrative section + C170 inline tooltips)
  - Testing + edge cases: 2-3h

- **Architectural Impact**:
  - **Service layer**: New `src/services/narrative_engine.py` (additive). Imports from `adaptive_engine.py`, `analogy_engine.py` (after D16 split), `financial_metrics.py`, `glossary_service.py` (after C170)
  - **Presentation layer**: `business_card.py` modified (adds narrative section, ~60-80 lines). D24 extraction strongly recommended.
  - **Data layer**: No new data sources. Uses existing events.yaml + FinMind data.
  - **No changes to**: routing layer, data layer, chart.py
  - **Dependency chain**: D-120 → D-16 → C170 → C152 (linear dependency)

- **Vision Alignment**:
  - ✅ Core value #1 "Story first, data second" — the entire feature IS a story
  - ✅ Core value #3 "Adaptive and self-evolving" — narratives update as new events/metrics arrive
  - ✅ Core value #5 "Benchmark-oriented analysis" — narratives include industry context
  - ✅ "Historian" positioning — explains what happened and why, doesn't predict
  - ✅ "Ten-second test" — a beginner can read a 3-sentence narrative and understand what happened

---

#### Direction 3: C188 "Why Did This Stock Move?" — Inline AI Explanations + C196 Daily Market Story (Combined for Retention)

- **Description**: Two features combined into a retention-focused direction. **C188** adds an inline "Why did this move?" button next to every price change on the business card page — clicking it generates a plain-language explanation of what drove the price move (e.g., "TSMC dropped 3% today because the semiconductor sector weakened after Micron's earnings miss, which raised concerns about chip demand. TSMC's revenue is 30% from memory chip customers, so it's affected by Micron's results."). **C196** is a daily 3-minute market narrative — a "Today's Market Story" section on the homepage that synthesizes the day's market action into a single plain-language paragraph (e.g., "Today the TWSE fell 1.2%. The semiconductor sector led the decline (-2.5%) after TSMC reported weaker-than-expected guidance. But the financial sector gained 0.8% as banks benefited from rising interest rates. 3 stocks hit new highs: 富邦媒, 祥碩, 保瑞."). Together, these create a **daily engagement loop** — users return every day to read the market story, then dive into individual stock explanations. This directly addresses the #1 competitor gap identified in Round 11: "Daily Engagement Loops Drive Retention" (Finimize, TradingView, StockEdge, Moomoo all have daily engagement mechanisms; Stock Explorer has none).

- **Technical Approach**:
  - **C188 (Why Did This Move?)**:
    - **Data layer**: Uses existing `adaptive_engine.py` events + `news_summarizer.py` news + FinMind price data. No new data sources.
    - **Service layer**: Extend existing `news_summarizer.py` with a `explain_price_move(stock_id, date, price_change) -> str` function. The function: (1) fetches events within ±3 days of the price move, (2) fetches news within the same window, (3) matches the price direction to the most relevant event/news, (4) generates a plain-language explanation using templates. Template patterns: "X happened → which affects this company because Y → leading to Z% price move."
    - **Presentation layer**: Add a "❓" button next to daily/weekly/monthly price change displays in `business_card.py`. Clicking it shows the explanation in an expander below the price display.
    - **No LLM needed** — pure template-based approach with event/news data filling in the blanks.

  - **C196 (Daily Market Story)**:
    - **Data layer**: Uses FinMind TWSE index data + sector performance data (requires new `market_data.py` service — D25 debt item). This is the main infrastructure dependency.
    - **Service layer**: New `src/services/daily_story_engine.py` — fetches today's TWSE data, sector performance, top movers, and generates a 3-paragraph narrative using templates. Template structure: (1) market overview (TWSE change + primary driver), (2) sector highlights (top 2 gaining + top 2 losing sectors with reasons), (3) notable stocks (3-5 stocks with interesting stories).
    - **Presentation layer**: New "📰 今日市場故事" section on the homepage (`_main.py` or `homepage.py`). Shows the daily narrative with a "Read More" link that expands to show sector details and top movers.
    - **Scheduling**: The daily story is generated on first page load each day (cached in session_state with date key). No cron job needed — lazy generation is sufficient for the current scale.

- **Pros**:
  - **Addresses the #1 retention gap** — Stock Explorer has no daily engagement mechanism. Every competitor analyzed in Round 11 has one (Finimize newsletter, TradingView Ideas feed, StockEdge daily analysis, Moomoo social feed)
  - **C188 is low-risk, high-ROI** — pure template-based explanation using existing event/news data. No LLM, no hallucination risk
  - **C196 creates a daily habit** — users return every day to read the market story, increasing DAU/MAU
  - **Combined, they form a retention funnel**: Daily story → click on interesting stock → read "Why did this move?" → explore the company → return tomorrow
  - **C188 directly counters StockStory and Stockopedia AI** — both offer "why did this move?" explanations for US stocks; Stock Explorer can do it for TW stocks with better data depth
  - **Template-based approach is safe and maintainable** — no LLM dependency

- **Cons**:
  - **C196 requires D25 (market_data.py)** — sector performance data is not currently available in the architecture. This is a new data flow (market-wide → aggregate → visualize) that doesn't fit the current single-stock pattern. D25 is estimated at 4-6h additional infrastructure work.
  - **C188 quality depends on event/news coverage** — if no event is found within ±3 days of a price move, the explanation is weak ("No significant event found — price may have moved due to market sentiment"). This happens for ~30% of price moves.
  - **C196 requires daily data freshness** — FinMind data updates daily, but the market story is only as good as the data. If FinMind data is delayed, the story will be stale.
  - **Homepage real estate** — adding a daily story section to the homepage competes with existing content for space. The homepage is already dense.
  - **C196 is the highest-ROI retention feature** (per Round 12 research: Finimize, Acorns prove demand) but also the most architecturally complex due to D25 dependency.

- **Effort**: 18-26 hours
  - C188 (Why Did This Move?):
    - `news_summarizer.py` extension: 3-4h (explain_price_move function + templates)
    - `business_card.py` integration: 1-2h (❓ button + expander)
    - Template content: 2-3h (5 explanation patterns)
    - Subtotal: 6-9h
  - C196 (Daily Market Story):
    - D25 prerequisite (market_data.py): 4-6h (sector performance data service)
    - `daily_story_engine.py`: 3-4h (data fetching + narrative generation)
    - Homepage integration: 2-3h (new section + layout)
    - Template content: 2-3h (daily story templates)
    - Subtotal: 11-16h
  - Combined testing: 1-2h

- **Architectural Impact**:
  - **Service layer**: New `src/services/daily_story_engine.py` (C196). Extended `news_summarizer.py` (C188). New `src/services/market_data.py` (D25, C196 prerequisite).
  - **Presentation layer**: Homepage modified (C196 section). `business_card.py` modified (C188 button). Both are additive additions to existing files.
  - **Data layer**: No new FinMind endpoints needed. Sector performance data may require a new FinMind API call or aggregation from existing stock-level data.
  - **No changes to**: routing layer, analogy_engine.py, financial_metrics.py
  - **New data flow**: Market-wide → aggregate → visualize (D25). This is architecturally distinct from the current single-stock flow and needs a clear abstraction.

- **Vision Alignment**:
  - ✅ Core value #1 "Story first, data second" — daily market story IS a story
  - ✅ Core value #3 "Adaptive and self-evolving" — daily story updates every day with fresh data
  - ✅ "Ten-second test" — a beginner can read the 3-paragraph daily story in 30 seconds and understand what happened
  - ✅ "Historian" positioning — explains what happened today, doesn't predict tomorrow
  - ✅ Retention — creates a daily engagement loop (the #1 missing UX feature per Round 11 research)

---

### Recommendation

**Primary Recommendation: Direction 1 (C170 + C194 Tappable Glossary with Judgment Callouts) as the lead feature for Sprint 21, with Direction 2 (C152 Multi-Factor Event Narratives) as the centerpiece.**

**Justification**:

1. **C170 + C194 is the highest-ROI, lowest-risk feature**. At 12-18h, it delivers the most educational value per hour invested. It directly addresses the "ten-second test" — the product vision's core verification principle. The C194 judgment callout component is a **unique differentiator** that no competitor offers (validated across 12 rounds of competitor research). The YAML-driven content approach means non-developers can contribute glossary entries, making the feature scalable beyond the development team.

2. **C152 is the strategic centerpiece** but should follow C170, not precede it. The dependency chain is clear: D-120 → D-16 → C170 → C152. C152's multi-factor narratives are significantly more valuable when inline glossary definitions (C170) are available — readers can tap any metric in a narrative for instant understanding. Building C152 before C170 would produce narratives that reference undefined terms, reducing their educational value.

3. **Direction 3 (C188 + C196) should be deferred to Sprint 22**. While the daily engagement loop is critically important for retention (the #1 gap per Round 11), the D25 infrastructure dependency (market_data.py for sector performance) adds 4-6h of prerequisite work that doesn't fit cleanly into Sprint 21's capacity. C188 alone (6-9h) is a good candidate for Sprint 21 if capacity allows after C170 + C152. C196 should be the opening feature of Sprint 22, paired with D25 infrastructure work.

4. **Sprint 21 recommended plan**:
   - **Day 1**: D-120 (benchmark extraction, 1.5-2.5h) + D-16 (analogy_engine.py split, 2-3h) — infrastructure prerequisites
   - **Week 1**: C170 + C194 (Tappable Glossary with Judgment Callouts, 12-18h) — lead feature
   - **Week 2**: C152 (Multi-Factor Event Narratives, 16-20h) — centerpiece feature
   - **Stretch**: C188 (Why Did This Move?, 6-9h) — if capacity allows
   - **Total**: 31.5-43.5h (fits within proven 30-42h sprint capacity)

5. **Architectural health note**: `business_card.py` will grow from 561 to ~680 lines with these additions. The D24 extraction (business_card/ sub-directory) should be done as part of D-16 (they're both refactoring tasks). This is a 2-3h investment that prevents the file from becoming unmaintainable.

**Competitor defense**: This plan directly counters the two most threatening competitor trends:
- **StockStory and Stockopedia AI** (Round 12-13): C152's multi-factor narratives match their narrative capabilities, but with TW-localized data and C194's unique judgment callouts
- **元大證券 AI Chatbot** (Round 12): C170's inline glossary provides a similar "explain this metric" experience, but embedded in the analysis flow rather than in a separate chatbot interface
- **Finimize daily engagement** (Round 11): Deferred to Sprint 22 (C196), but C188 provides a lighter-weight engagement mechanism for Sprint 21
