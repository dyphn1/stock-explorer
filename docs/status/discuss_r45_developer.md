## 2026-06-15 Developer Estimate — Discussion Round 45

### Codebase Context

**Architecture**: Streamlit app, Python backend. Services are pure Python (no Streamlit imports); pages are Streamlit UI. Shared UI components in `_router_base.py`. LLM abstraction via `ExplanationProvider` protocol with `TemplateExplanationProvider` as fallback. Data from FinMind API + YAML config files.

**Key existing services**: `metric_explainer.py`, `glossary_service.py`, `event_interpretation_service.py`, `adaptive_engine.py` (event detection + recording), `story_feed.py`, `news_summarizer.py`, `analogy_engine.py`, `delta_engine.py`, `screener_explanation_provider.py`, `metric_education.py`, `key_takeaways.py`

**Key existing pages**: `stock_screener.py`, `business_card/_main.py`, `event_dashboard.py`, `investor_story_feed.py`, `learn_first_gate.py`

**Sprint 20 complete**: C167 (AI Screener Explanations) + C163 (Learn First Gate) + C40 (Beginner/Expert Mode) shipped.

---

### Feature Cost Estimates

#### C170: Tappable Glossary — Inline Metric Definitions on Click/Hover
- **Validated Estimate**: 6-10h ✅ **Confirmed**
- **Main Risk**: Low. The `glossary_service.py` already exists with `get_glossary_term()`, `get_all_terms()`, `search_terms()`. The `_glossary_tooltip()` function already exists in `_router_base.py` (L269-290) using `st.popover`. The YAML data file (`glossary.yaml`) is in place. This feature is primarily about wiring the existing tooltip into metric display labels across business card sections.
- **Files Changed**:
  - `src/pages/business_card/_sections/_story.py` — add glossary tooltips to metric labels
  - `src/pages/business_card/_sections/_health.py` — add to health score labels
  - `src/pages/business_card/_sections/_financial.py` — add to key metric labels
  - `src/pages/business_card/_sections/_summary.py` — add to summary metrics
  - `src/pages/_router_base.py` — potentially enhance `_glossary_tooltip()` if needed
  - `src/data/glossary.yaml` — may need additional term entries
- **Complexity**: **Low**

---

#### C194: Explain Why Good/Bad — Metric Judgment Callout
- **Validated Estimate**: 6-10h → **Revised to 8-12h**
- **Main Risk**: Medium. Requires defining "good/bad" thresholds per metric and generating judgment explanations. The `metric_education.py` already has `is_higher_better` per metric and threshold-based scoring in `health_scoring.py`, but there's no existing "why is this good/bad" narrative generator. Need to build a new service that takes a metric value, compares against thresholds, and produces a historian-tone explanation of the judgment rationale. The threshold logic must handle industry-relative judgments (e.g., 40% gross margin is good for retail but mediocre for software).
- **Files Changed**:
  - `src/services/metric_explainer.py` — extend with `get_judgment_explanation()` function (or new `judgment_explainer.py` service)
  - `src/services/llm/template_provider.py` — add judgment templates
  - `src/pages/business_card/_sections/_health.py` — add judgment callouts to health scores
  - `src/pages/business_card/_sections/_financial.py` — add to key metrics
  - `src/pages/_router_base.py` — add `_judgment_badge()` shared component
  - `src/data/industry_benchmarks.yaml` — may need threshold data
- **Complexity**: **Medium**

---

#### C152: Multi-Factor Event Narratives — One Story, All Factors Combined
- **Validated Estimate**: 16-20h ✅ **Confirmed**
- **Main Risk**: High. This is the most complex feature in the set. Requires synthesizing multiple event types (revenue, news, price, institutional) into a single coherent narrative. The `event_interpretation_service.py` handles single events; `story_feed.py` collects events but doesn't synthesize them into one narrative. Need a new synthesis engine that: (1) collects all events for a stock in a time window, (2) identifies causal relationships or thematic connections, (3) generates a unified historian-tone narrative. The adaptive engine's `detect_company_type()` and `get_adaptive_framework()` provide framing context. The main risk is narrative coherence — combining 3-5 events into one readable story without it feeling like a bullet list.
- **Files Changed**:
  - `src/services/story_feed.py` — extend `generate_daily_stories()` or add `synthesize_multi_factor_narrative()`
  - `src/services/event_interpretation_service.py` — extend with multi-event synthesis
  - `src/services/adaptive_engine.py` — may need new correlation detection between event types
  - `src/pages/business_card/_sections/_story.py` — add narrative section to story card
  - `src/pages/event_dashboard.py` — add combined narrative view
  - `config/event_interpretation_templates.yaml` — add multi-event narrative templates
- **Complexity**: **High**

---

#### C188: Why Did This Stock Move? — Inline AI Explanation for Single-Stock Events
- **Validated Estimate**: 10-14h ✅ **Confirmed**
- **Main Risk**: Medium. The `event_interpretation_service.py` already provides `get_interpretation()` and `get_drilldown_interpretation()` for individual events. The `adaptive_engine.py` already detects revenue, news, and price events. The main work is: (1) adding a prominent inline explanation section to the business card (not just the event dashboard), (2) correlating price movements with detected events, (3) generating a "this stock moved because..." narrative. The `delta_engine.py` already computes price/revenue deltas. Risk is primarily UI integration — making the explanation feel native to the business card flow.
- **Files Changed**:
  - `src/services/event_interpretation_service.py` — extend with price-movement correlation
  - `src/pages/business_card/_sections/_story.py` — add "Why did this move?" section
  - `src/pages/business_card/_main.py` — add new section dispatch
  - `src/pages/business_card/_sections/__init__.py` — export new render function
  - `config/event_interpretation_templates.yaml` — add price-movement templates
- **Complexity**: **Medium**

---

#### C196: Daily Market Story — 3-Minute Daily Market Narrative for Retention
- **Validated Estimate**: 10-14h → **Revised to 12-16h**
- **Main Risk**: Medium-High. The `story_feed.py` and `investor_story_feed.py` (C116) already provide a daily story feed, but C196 is specifically a single cohesive 3-minute narrative (not a list of stories). This requires: (1) a new narrative composition service that weaves top events, sector movements, and education into one flowing story, (2) a dedicated page or hero section, (3) scheduling/notification integration for daily delivery. The `notification_service.py` exists but may need daily scheduling. The `generate_education_story()` in `story_feed.py` provides the education component. Main risk is creating a compelling single narrative vs. a list — requires careful template design and possibly LLM integration for coherence.
- **Files Changed**:
  - `src/services/story_feed.py` — add `compose_daily_market_story()` function
  - `src/pages/investor_story_feed.py` — add hero narrative section (or new page)
  - `src/services/notification_service.py` — add daily story notification trigger
  - `src/pages/_router_base.py` — add daily story card component
  - `config/event_interpretation_templates.yaml` — add daily narrative templates
  - `src/data/news_templates.yaml` — may need daily story templates
- **Complexity**: **Medium-High**

---

#### C175: NL-First Screening — Search-Box-First Natural Language Stock Screening UI
- **Validated Estimate**: 12-16h → **Revised to 14-18h**
- **Main Risk**: High. The `stock_screener.py` has preset-based and custom filter modes but no natural language input. This requires: (1) a new NL parsing service that converts plain Chinese/English queries ("高殖利率的半導體股") into structured filter parameters, (2) integration with `stock_screener_service.py`'s `apply_preset_filter()` and `apply_custom_filter()`, (3) a new search-box-first UI mode in `stock_screener.py`. The parsing can start template-based (keyword matching) but needs to handle compound queries. Risk: NL parsing accuracy for financial queries in Chinese — edge cases like "本益比不到15的成長股" require combining multiple filters. The `ScreenerExplanationProvider` can generate explanations for NL-origin filters.
- **Files Changed**:
  - `src/services/stock_screener_service.py` — add `parse_nl_query()` function (or new `nl_screener_service.py`)
  - `src/pages/stock_screener.py` — add NL search box mode (replaces or supplements current mode selector)
  - `src/services/screener_explanation_provider.py` — extend to explain NL-parsed filters
  - `src/data/screener_templates.yaml` — add NL keyword-to-filter mappings
  - `src/pages/_router_base.py` — add NL search input component
- **Complexity**: **High**

---

#### C184: Natural Language Q&A — Ask Questions About Any Stock in Plain Language
- **Validated Estimate**: 16-20h → **Revised to 18-24h**
- **Main Risk**: Very High. This is the highest-risk feature. Requires: (1) a new Q&A service that takes free-text questions about a stock, (2) retrieves relevant data from the stock's context (already loaded via `get_stock_data()`), (3) generates accurate historian-tone answers. The LLM abstraction layer (`ExplanationProvider` protocol, `TemplateExplanationProvider`) provides the foundation, but Q&A requires more than template filling — it needs question understanding, data retrieval, and answer synthesis. Starting with template-based Q&A (common questions only) is recommended, with LLM integration as a future phase. Risk: answer accuracy and hallucination prevention. Must maintain historian positioning (no investment advice). The `metric_explainer.py`, `key_takeaways.py`, and `event_interpretation_service.py` provide source material for answers.
- **Files Changed**:
  - New `src/services/qa_service.py` — Q&A engine (new file)
  - `src/services/llm/base.py` — may extend `ExplanationRequest` for Q&A context
  - `src/pages/business_card/_main.py` — add Q&A input section
  - `src/pages/business_card/_sections/__init__.py` — export new render function
  - `config/` — add Q&A template YAML
  - `src/pages/_router_base.py` — add Q&A UI components
- **Complexity**: **High**

---

### Recommended Priority Order

**Rationale**: Prioritize features that build on existing infrastructure, deliver user value quickly, and create foundations for more complex features. Group by dependency chains.

| Priority | Feature | Rationale |
|----------|---------|-----------|
| 1 | **C170 Tappable Glossary** (6-10h) | Lowest complexity, existing infrastructure (`glossary_service.py`, `_glossary_tooltip()`), immediate UX improvement. Good Sprint 21 starter. |
| 2 | **C188 Why Did This Stock Move?** (10-14h) | Builds on existing `event_interpretation_service.py` and `adaptive_engine.py`. Medium risk, high user value. Natural companion to C170. |
| 3 | **C194 Explain Why Good/Bad** (8-12h) | Extends `metric_explainer.py` with judgment rationale. Medium complexity. Complements C170 (glossary + judgment = complete metric understanding). |
| 4 | **C152 Multi-Factor Event Narratives** (16-20h) | High complexity but builds on C188's event correlation work. Should follow C188 to reuse event-to-narrative infrastructure. |
| 5 | **C196 Daily Market Story** (12-16h) | Builds on `story_feed.py` (C116). Benefits from C152's narrative synthesis work. Medium-high complexity. |
| 6 | **C175 NL-First Screening** (14-18h) | High complexity, new parsing layer. Benefits from `ScreenerExplanationProvider` (C167). Best done after simpler features stabilize. |
| 7 | **C184 Natural Language Q&A** (18-24h) | Highest risk and complexity. Should come last — benefits from all previous explanation/judgment/narrative infrastructure. Consider phased delivery (template-based first, LLM later). |

**Suggested Sprint Grouping**:
- **Sprint 21**: C170 + C188 (16-24h total) — quick wins on existing infrastructure
- **Sprint 22**: C194 + C152 (24-32h total) — judgment + narrative synthesis
- **Sprint 23**: C196 + C175 (26-34h total) — daily story + NL screening
- **Sprint 24**: C184 (18-24h) — Q&A as capstone feature

**Total estimated effort**: 104-138 hours across 7 features.
