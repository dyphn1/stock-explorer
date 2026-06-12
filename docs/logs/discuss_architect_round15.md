# 2026-06-20 Technical Analysis — Feature Directions for Post-Sprint 5

> **Author**: System Architect
> **Cycle**: Discussion Round 15
> **Context**: Sprint 4 complete (R3, C48, C38, C51, C53-1). Sprint 5 prerequisites (D-039, D-040, D-041) about to start. Looking beyond Sprint 5 to the next wave of development.
> **References**: docs/architecture/architecture.md, docs/architecture/technical_design.md, docs/research/competitor_research.md (Rounds 7-9 + R16), docs/status/tech_debt.md, docs/design/architect_review_r16.md

---

## Problem Description

Stock Explorer has completed 4 sprints with a solid foundation:
- **Completed**: Business Card page (14 sections), Operation Checkup, Financial Health, Peer Comparison, Group Structure, Category Browser, ETF Browser/Detail, Watchlist, Event Dashboard, Sector Heatmap, Company Story Card, Compare Stories, Social Sharing
- **Architecture debt resolved**: D16 (analogy_engine.py split), D24 (business_card.py sub-directory), D1/D2 (financial_metrics.py extraction), D20 (valuation band return value)
- **Active architecture debt**: 19 P2 items (D-042/043/044 newly identified), D37 (_sections.py emerging monolith at 604 lines), D3 (inline HTML duplication), D6 (hardcoded data in Python), D13 (no test infrastructure)

The product vision ("historian, not stock picker") is validated by competitor research but needs stronger execution. The content cap (100 items max) and mandatory historian tone QA gate constrain the pace of content-heavy features.

**The core question for this analysis**: What 2-3 feature directions should the team pursue after Sprint 5, given the current architecture state, competitor landscape, and product vision?

---

## Current Architecture Constraints

Before proposing directions, the architectural constraints that shape feasibility:

1. **Streamlit limitations**: No native timeline component (C34 spike needed for D27), no partial refresh (sidebar prices use cached session_state), no WebSocket/SSE. Any real-time or complex interaction requires workarounds.
2. **_sections.py emerging monolith**: At 604 lines with C71/C73/C74 adding ~210 lines in Sprint 5, it will reach ~810 lines. D37 split must happen during Sprint 5, not after.
3. **Service layer boundaries holding**: The split of analogy_engine.py into 4 modules (D16) created clean imports. New features should follow the pattern: data → service → presentation, with no cross-layer calls.
4. **Content YAML pattern established**: watchlist.yaml, events.yaml, company_facts.yaml prove the pattern. New content features should use YAML data + service layer loaders, not hardcoded Python dicts (anti-pattern D6).
5. **Risk analyzer at 567 lines**: Approaching god-module territory. New risk-related features (C73 Expert Analysis) should go in a separate module, not extend risk_analyzer.py.

---

## Option A: "Discovery & Health" — Stock Screener + Company Snowflake + Valuation Band

### Description
A trio of features that transform Stock Explorer from a "lookup a company you already know" tool into a "discover companies worth learning about" platform:

- **C42 (Stock Screener / Discovery Engine)**: Beginner-friendly screening presets ("穩定收息", "成長潛力", "便宜估值") + custom screening on key metrics. Effort: 16-24h.
- **C43 (Company Snowflake Health Visualization)**: 5-dimension radar chart (Profitability, Growth, Financial Health, Dividend, Valuation) with color-coded scores and plain-language explanations. Effort: 12-16h.
- **C45 (Valuation Band Chart)**: Current P/E vs 5-year historical range with percentile and plain-language interpretation. Effort: 8-10h.

### Technical Impact Analysis

**New modules required**:
- `src/services/screener.py` — Screening logic (filter stocks by metric thresholds, return ranked results)
- `src/pages/screener_page.py` — New standalone page (no stock_id required, like category_browser.py)
- `src/services/health_snowflake.py` — Radar chart generation + scoring algorithms (extends existing `health_scoring.py` from D16 split)
- `chart.py` additions — Valuation band chart (extends existing `create_valuation_band_chart()` with percentile calculation)

**Architecture alignment**:
- Clean layer separation: screener service → screener page → UI components
- Snowflake extends existing `health_scores.py` (D16 split module) — no god module risk
- Valuation band reuses `financial_metrics.py` EPS extraction (D17 resolved)
- All data from FinMind APIs already in use — no new API dependencies

**Content cap implications**: C42 adds 0 content items (algorithmic). C43/C45 add 0 content items (computed from data). Well within the 100-item cap.

**Dependencies**: C42 needs `market_data.py` (D25) for batch data loading. D25 is already planned as part of C51 (Sprint 4, already complete). C43 needs `financial_metrics.py` (D1 resolved). C45 needs `financial_metrics.py` (D1 resolved). **No blocker dependencies.**

### Pros
- **Highest competitive gap closure**: C42 is 財報狗's #1 feature (Round 9). C43 addresses Simply Wall St/Morningstar/Stockopedia visual health scores (Round 9). C45 is 財報狗's most popular chart.
- **Pure "historian" positioning**: Screener framed as "discover interesting companies" not "find stocks to buy." Snowflake explains "how healthy" not "whether to buy."
- **Technical feasibility highest**: All data available from existing FinMind client. No new API dependencies. Service layer patterns proven.
- **Zero content creation burden**: All three features are algorithmic — no manual curation needed for MVP.
- **Complements existing pages**: Screener → business card page. Snowflake + valuation band → enhance existing business card page. No new page infrastructure needed beyond screener.

### Cons
- **Screener UI complexity**: Multi-condition filtering requires careful UI design to avoid overwhelming beginners. D-040 (Beginner/Expert mode toggle, from Round 8) would be a natural fit.
- **Snowflake scoring algorithm design**: Scoring 5 dimensions fairly requires calibration. Risk of oversimplifying (just like competitors) vs. maintaining historian nuance.
- **Valuation band overlaps with existing**: `create_valuation_band_chart()` already exists. C45 must enhance it (add percentile, plain-language interpretation) rather than duplicate it.

### Effort Estimate
- C42 Stock Screener: 16-24h (new page + service + UI)
- C43 Company Snowflake: 12-16h (new service + business card integration)
- C45 Valuation Band Enhancement: 8-10h (enhance existing chart + new UI card)
- **Total: 36-50h** (approximately one sprint)

---

## Option B: "Narrative & Education" — Story Timeline + Financial Academy + Concept Explainer

### Description
A trio of features that deepen the "historian" narrative layer beyond the current business card:

- **C34 (Company Story Timeline)**: Chronological narrative weaving events, revenue milestones, and price movements into "Here's what happened to TSMC in the last 3 years, told as a story." Effort: 16-24h.
- **C47 Phase 1 (Financial Education Academy)**: 5 structured lessons ("What is revenue?", "What is ROE?", "What is P/E?", etc.) with real TW stock examples, quizzes, and completion certificates. Effort: 20-30h.
- **C56 (Explain This Metric)**: Interactive financial concept explainer — click any metric on any page → get a plain-language explanation with real TW stock examples. Effort: 12-16h.

### Technical Impact Analysis

**New modules required**:
- `src/services/story_composer.py` — Already planned (D26 unblocked by D16). Weaves event data + revenue data + analogy engine into narrative paragraphs. Timeline rendering logic.
- `src/pages/learning_academy.py` — New standalone page. Lesson navigation, quiz rendering, progress tracking.
- `src/data/lessons.yaml` — Structured lesson content (following established YAML pattern).
- `src/data/metric_explanations.yaml` — Per-metric plain-language explanations with examples.
- `src/services/llm/` — **D5 (no LLM integration layer)** becomes relevant here. Currently all explanations are template-based. Narrative features (especially C34) would benefit enormously from LLM-generated prose assembled from structured data. The architecture doc specifies "LLM (plain-language translation only) + templates."

**Architecture alignment**:
- Story composer imports from 7+ service modules (analogy_engine, key_takeaways, delta_engine, health_scoring, company_facts, chart, financial_metrics) — all stable after D16 split
- Learning academy follows the standalone page pattern (like category_browser.py)
- Metric explainer is a cross-cutting enhancement that touches ALL pages — requires a consistent injection point (sidebar tooltip? modal?)

**Content cap implications**: This is the highest-risk option for the content cap. C34 generates 1 narrative per company (~200 TW stocks = 200 items). C47 generates 5 lessons (5 items). C56 generates ~15 metric explanations (15 items). **Total: ~220 potential content items — exceeds the 100-item cap unless scoped carefully.**

**Mitigation**: C34 only for top 20 manually curated companies (not algorithmic). C47 only 5 lessons (Phase 1). C56 only 10 core metrics. **Capped total: 35 items.**

### Pros
- **Strongest "historian" differentiator**: C34 is the #1 feature competitors DON'T have (Round 7, Round 16). No TW competitor has narrative timeline. This is the purest expression of the product vision.
- **Validates product direction internationally**: Zerodha Varsity (Round 11) proves structured finance education demand. Investopedia Academy (Round 9) proves course-with-certificates model.
- **Creates compounding value**: Each lesson in C47 uses real TW stock examples → more reasons to visit more company pages. Each metric explanation in C56 makes the whole platform more beginner-friendly.
- **Deeper engagement loop**: C47 (study) → C34 (apply knowledge to a company's story) → C56 (explain a metric you just encountered) → back to business card page. This creates the "learning path" that Finimize's Academy model (Round 11) proves drives retention.

### Cons
- **Content creation bottleneck**: C34 requires curated narratives for even 20 companies. C47 requires writing 5 lessons. C56 requires writing 10 metric explanations. This is a **content sprint, not a code sprint** — the team needs capacity for both.
- **C34 D27 timeline UI risk**: Streamlit has no native timeline component. The D27 spike (4-6h) must be completed first. If the spike reveals Streamlit can't render timelines adequately, C34 may need a different tech approach (custom HTML/CSS, or defer).
- **Content cap pressure**: Even mitigated at 35 items, this direction consumes 35% of the content budget for 3 features.
- **LLM dependency (D5)**: C34's narrative quality depends on generating coherent paragraphs from structured data. Template-only approach (current) may produce robotic-sounding narratives. The LLM abstraction layer (D5, effort: 2-3h) should be addressed before C34 implementation for quality.

### Effort Estimate
- **D27 spike (prerequisite)**: 4-6h
- D5 LLM abstraction layer: 2-3h
- C34 Story Timeline: 16-24h (includes spike findings integration)
- C47 Phase 1 Education Academy: 20-30h (5 lessons, quizzes, certificates)
- C56 Explain This Metric: 12-16h
- **Total: 54-79h** (approximately 1.5-2 sprints, content creation included)

---

## Option C: "Competitive Moat" — Moat Analysis + Risk Analysis Enhancement + Financial Wellness Check

### Description
A trio of features that analyze companies from the angles competitors don't cover well:

- **C46 (Moat Analysis)**: Explain what the competitive advantage IS and how it has protected the company historically (technology, brand, cost, network, switching costs). Historical evidence, not future prediction. Effort: 12-16h.
- **C44 Enhancement ("What Could Go Wrong" — expanded)**: Expand C44's 3 risk dimensions to 5 (add volatility, cyclicality) with historical evidence of risks that materialized. Effort: 10-14h (enhancement, not new feature).
- **C85 (Financial Wellness Check)**: Behavioral finance self-assessment — "How do you feel about market drops?" with personalized learning recommendations based on risk tolerance profile. Effort: 8-12h.

### Technical Impact Analysis

**New modules required**:
- `src/services/moat_analyzer.py` — Moat assessment logic (moat type classification, strength scoring, historical evidence matching)
- `src/data/moat_analysis.yaml` — Curated moat data for top 20 stocks (following established YAML pattern)
- `src/pages/wellness_check.py` — Quiz-style standalone page with result rendering
- `risk_analyzer.py` expansion — **Must NOT add to existing 567-line module.** Create `risk_analyzer_extended.py` for new dimensions (volatility, cyclicality) to avoid god module recurrence.

**Architecture alignment**:
- Moat analyzer is a standalone service (pure functions, no Streamlit imports) — clean layer separation
- Moat data is YAML-backed (follows D6 remediation pattern)
- Wellness check follows standalone page pattern
- Risk analyzer extension must be a new module (D31 mitigation — monitor risk_analyzer.py growth beyond 700 lines)

**Content cap implications**: C46 adds 20 manually curated items (top 20 stocks). C44 enhancement adds 0 (algorithmic). C85 adds 1 self-assessment flow (1 item). **Total: 21 items.**

### Pros
- **Unique TW market differentiator**: No TW competitor has moat analysis (Round 9). Morningstar's moat rating is iconic but US-only. This fills a genuine white space.
- **Risk analysis depth**: Simply Wall St has risk analysis but without historical evidence. Morningstar has uncertainty ratings but not in plain language. Stock Explorer can do both — plus historical evidence of risks that materialized. True to "historian" positioning.
- **Behavioral finance angle (C85)**: Cleo (Round 16) proved demand for AI financial coach + self-assessment. C85 is the "historian of self" — not "what should I buy" but "how do I think about risk."
- **Moderate technical risk**: All three features use existing data pipelines and established service layer patterns.
- **Content cap friendly**: 21 items total, leaving 79 items for future features.

### Cons
- **C46 manual curation bottleneck**: Moat analysis requires human judgment about competitive advantages. Can't be fully automated from FinMind data. 20 stocks × research time could be 10-15h of content research alone.
- **C44 enhancement overlaps with existing**: C44 (Risk Analysis MVP) was just completed in Sprint 3. Expanding it so soon after delivery could feel premature — users need time to engage with the existing 3 dimensions first.
- **C85 positioning risk**: Financial wellness check could feel like it's drifting from "historian of companies" toward "financial advisor for self." The historian tone QA gate must scrutinize this carefully. C85 must help users understand their OWN relationship with risk, not advise them on investments.
- **Moat analysis subjectivity**: Different people interpret competitive advantages differently. The scoring must be grounded in historical evidence (as specified) to avoid opinion-driven analysis. This constrains the implementation approach.

### Effort Estimate
- C46 Moat Analysis: 12-16h (service + data + business card integration)
- C44 enhancement (2 more dimensions): 10-14h (new service module + expand existing UI)
- C85 Financial Wellness Check: 8-12h (standalone page + YAML quiz data)
- **Total: 30-42h** (approximately one sprint, plus ~10-15h content research for C46)

---

## Comparative Analysis

| Dimension | Option A (Discovery & Health) | Option B (Narrative & Education) | Option C (Competitive Moat) |
|---|---|---|---|
| **Total Effort** | 36-50h | 54-79h | 30-42h |
| **Content Items Added** | 0 | ~35 (mitigated) | ~21 |
| **New Service Modules** | 3 | 4 (incl. LLM layer) | 3 |
| **New Pages** | 1 (screener) | 2 (academy, wellness) | 1 (wellness) |
| **Blocker Dependencies** | None (D25 already done) | D27 spike + D5 LLM layer | None (risk_analyzer split needed) |
| **Technical Risk** | Low | High (D27 timeline UI, D5 LLM) | Medium (manual curation bottleneck) |
| **Vision Alignment** | Strong (discovery + health) | Strongest (historian narrative) | Strong (historian evidence) |
| **Competitive Gap** | Highest (3 proven gaps) | High (unique differentiator) | High (TW white space) |
| **Content Burden** | None | High (lessons + narratives) | Medium (moat research) |
| **Beginner Value** | Very high (synthesis + discovery) | Very high (education path) | Moderate (deeper analysis) |

---

## Recommendation

**I recommend Option A ("Discovery & Health") as the primary post-Sprint 5 direction, with C34 Story Timeline from Option B as a parallel spike/investment track.**

### Reasoning

**1. Technical feasibility is highest.** All data is available via existing FinMind APIs. No blocker dependencies. The architecture is proven: new standalone page (C42), service layer extensions (C43), chart enhancements (C45). No Streamlit UI unknowns (unlike C34's timeline risk).

**2. Competitive gap closure is most impactful per hour invested.** C42 closes the #1 feature gap from 財報狗 (Round 9). C43 addresses every international competitor's visual health score (Simply Wall St, Morningstar, Stockopedia). C45 enhances an already-implemented chart with context that beginners actually need. These are proven competitive gaps with proven demand.

**3. Zero content creation burden respects the 100-item cap.** The content budget is precious. Option A adds 0 content items, preserving capacity for future content-heavy features (C34, C47) when the team has capacity for a content sprint.

**4. Best serves beginners immediately.** C42 transforms the product from lookup to discovery — beginners don't need to know which company to search for. C43 gives instant "how healthy is this company?" answers. C45 gives instant "is this expensive or cheap?" context. All three reduce the beginner's cognitive load.

**5. The C34 story timeline should be investigated in parallel as a spike (D27, 4-6h).** Not as a full feature commitment — just the spike to determine if Streamlit can render timelines adequately. If the spike succeeds, C34 becomes the centerpiece of Sprint 6+. If it fails, the team can invest in the LLM layer (D5) before committing to narrative features.

### Suggested Sequence (Post-Sprint 5)

1. **Sprint 6 (Primary — Option A)**: C42 Stock Screener (20h) + C43 Company Snowflake (14h) + C45 Valuation Band Enhancement (9h) = **43h**
2. **Sprint 6 (Parallel — Spike)**: D27 C34 Timeline Spike (5h) to de-risk future narrative features
3. **Sprint 7 (Decision Point)**: If D27 spike succeeds → C34 Story Timeline. If D27 spike fails → Option C (C46 Moat Analysis) or Option B's C47 Education Academy

### Conditions for Challenger Review
1. **Must not exceed content cap**: Option A adds 0 items, preserving budget for future sprints ✅
2. **Must maintain historian tone**: Screener framed as discovery, not stock-picking. Snowflake framed as health assessment, not buy signal. Valuation band framed as historical context, not price prediction. ✅
3. **Must address D-042/043/044 in Sprint 5 prerequisites**: These P2 design items should be completed before adding new business card sections (C43, C45). ✅
4. **Must monitor _sections.py growth**: C43 business card integration will push _sections.py past 650 lines. D37 split must happen during Sprint 6, not deferred. ✅

---

*This analysis is based on Sprint 4 completion state (R3, C48, C38, C51, C53-1) and Sprint 5 planned features (C71, C73, C74). The recommended direction is the most technically feasible path that delivers the highest competitive gap closure per hour invested while respecting content cap and historian positioning constraints.*
