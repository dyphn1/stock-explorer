# Developer Discussion Analysis — Round 40

## Implementation Cost Estimates

### C167: AI Screener Explanations

- **Files to create**:
  - `src/services/screener_explanation_service.py` — Generates plain-language narratives for screener outcomes (why a stock matched, what the filter means in context)
  - `src/services/screener_narrative_templates.py` — Tiered templates for each preset (dividend/growth/value) and custom filter combinations
- **Files to modify**:
  - `src/pages/stock_screener.py` — Add explanation section to `_render_results()` and `_render_beginner_mode()` / `_render_advanced_mode()`
  - `src/services/stock_screener_service.py` — Add `enrich_with_narrative()` helper or extend `format_screening_results()` with narrative fields
- **Reusable infrastructure**:
  - `analogy_engine.py` — `get_per_analogy()`, `get_dividend_analogy()`, `get_yoy_analogy()` for metric-level explanations
  - `TemplateExplanationProvider` / `ExplanationProvider` protocol — Can wrap screener-specific templates behind the same protocol
  - `stock_screener_service.py` — `apply_preset_filter()` and `apply_custom_filter()` already classify stocks; we add narrative layer on top
  - `_info_card()` / `_summary_card()` from `_router_base.py` — For rendering explanation cards
- **New infrastructure needed**:
  - Screener-specific narrative templates (different from delta/metric explanations — these explain *why a stock matched a filter*, not *what changed*)
  - A `ScreenerExplanationProvider` implementing `ExplanationProvider` protocol, or a simpler standalone function
- **Estimate**: 12-16 hours
  - **Why**: The screener page and service already exist and are well-structured. The main work is: (1) designing ~15-20 narrative templates for filter outcomes, (2) wiring them into the results rendering, (3) adding a "Why this stock matched" popover per result card. The `ExplanationProvider` protocol can be reused but screener explanations are conceptually different (filter-match vs metric-value), so a new provider is cleaner. The existing `_render_results()` card grid needs a small expansion to show a 1-line narrative under each stock's key metric. Testing: ~3-4 hours for the new service + page integration tests.
- **Risks**:
  - **Medium**: Narrative quality depends on having enough contextual data per stock. For stocks that match a filter but lack detailed metrics (e.g., missing revenue_yoy), the narrative must degrade gracefully.
  - **Low**: The screener already limits to 20 results, so performance of generating 20 narratives is negligible.
  - **Low**: Templates are pure Python string formatting — no LLM dependency risk.
- **Prerequisites**: None. Can be developed independently.

---

### C152: Multi-Factor Event Narratives

- **Files to create**:
  - `src/services/multi_factor_narrative_service.py` — Combines multiple detected events into a single coherent story
  - `src/data/yaml/multi_factor_templates.yaml` — Templates for common multi-event patterns (e.g., "revenue surge + price jump", "dividend cut + institutional sell-off")
- **Files to modify**:
  - `src/services/adaptive_engine.py` — Add `get_multi_factor_summary()` or extend existing event detection to flag multi-event clusters
  - `src/pages/event_dashboard.py` — Add narrative summary section to event dashboard
  - `src/pages/business_card/_sections/_story.py` — Potentially add multi-factor narrative to the business card's delta section
- **Reusable infrastructure**:
  - `adaptive_engine.py` — Already detects individual events; we cluster them by time window (e.g., same week)
  - `delta_engine.py` / `DeltaExplanationProvider` — Individual event explanations exist; we compose them
  - `timeline_service.py` — Compose-and-enrich pipeline pattern can be extended for multi-factor narratives
  - `market_event_service.py` — YAML-backed event data
  - `_so_what_box()` from `_router_base.py` — Already synthesizes multiple deltas; similar pattern for multi-event
- **New infrastructure needed**:
  - Multi-factor template engine (different from single-event templates — needs to weave 2-3 events into one story)
  - Event clustering logic (group events within N-day window)
- **Estimate**: 14-18 hours
  - **Why**: The spike is done, so the core event detection exists. The main work is: (1) event clustering logic (~3h), (2) designing ~10-15 multi-factor narrative templates in YAML (~4h), (3) the composition service that picks the right template based on event combination (~4h), (4) integrating into the event dashboard and/or business card (~3h), (5) testing edge cases — overlapping events, conflicting signals, missing data (~2-4h). The compose-and-enrich pattern from `timeline_service.py` is a good reference but multi-factor narratives are more complex because they need to resolve conflicting signals (e.g., revenue up but price down).
- **Risks**:
  - **High**: Multi-factor narrative quality is hard to get right. A template for "revenue surge + price drop" needs to acknowledge the contradiction, not just list both. This requires careful template writing and tone checking against the historian blocklist.
  - **Medium**: Event clustering depends on event detection reliability. If `adaptive_engine` produces false positives, the multi-factor narrative will be nonsensical. Need a confidence threshold.
  - **Low**: YAML templates are easy to iterate on without code changes.
- **Prerequisites**: Relies on `adaptive_engine` event detection being stable (it is — M5 is complete). No hard dependency on other Sprint 20 features.

---

### C163: Learn First Gate

- **Files to create**:
  - `src/pages/learn_first_gate.py` — New page: educational onboarding gate shown before data access
  - `src/services/onboarding_service.py` — Tracks onboarding completion state, manages gate logic
  - `config/onboarding_steps.yaml` — Onboarding content (3-5 educational cards)
- **Files to modify**:
  - `src/pages/router.py` — Add gate check before rendering stock pages; add "學習入口" page
  - `src/pages/_router_base.py` — Potentially add shared onboarding card components
  - `src/pages/first_visit_guide.py` — C103 Lite already exists as a 2-card primer; C163 is a superset/evolution
- **Reusable infrastructure**:
  - `first_visit_guide.py` (C103 Lite) — Already has a 2-card dismissible primer pattern; C163 extends this to a multi-step gate
  - `lesson_service.py` — YAML-backed lesson loading pattern can be reused for onboarding content
  - `academy.py` — Progress tracking pattern (`academy_progress` in session_state) can be adapted
  - `_summary_card()` / `_白话_card()` from `_router_base.py` — For rendering onboarding cards
  - `settings_service.py` — Session state management pattern
- **New infrastructure needed**:
  - Gate logic: check if user has completed onboarding before showing stock data
  - Onboarding completion persistence (session_state is sufficient for v1; no DB needed)
- **Estimate**: 10-14 hours
  - **Why**: The C103 Lite first visit guide already exists as a 2-card primer. C163 is a more comprehensive version: (1) gate logic that intercepts first-time users (~2h), (2) 3-5 educational cards with progressive disclosure (~3h), (3) completion tracking in session_state (~1h), (4) content writing for onboarding cards in YAML (~2h), (5) integration with router to show gate before stock pages (~2h), (6) testing the gate flow — dismiss, complete, skip, revisit (~2-4h). The main complexity is the gate integration with the router — need to ensure it doesn't break existing navigation or the C103 flow.
- **Risks**:
  - **Medium**: Gate placement in the router is tricky. The router has many page branches; the gate needs to show for stock pages but not for standalone pages (settings, academy, etc.). Need a clear definition of "data pages" vs "non-data pages".
  - **Low**: Content creation (writing the educational cards) is a design/PM concern, not a dev risk.
  - **Medium**: If C103 (first visit guide) and C163 (learn first gate) overlap, we need to decide whether to merge them or keep them separate. Merging is cleaner but requires coordination with the designer.
- **Prerequisites**: Should coordinate with C40 (Beginner/Expert Mode) since both affect the onboarding/experience tier. C163 is a prerequisite for C40's "beginner" definition.

---

### C37: Key Takeaways Summary Card

- **Files to create**: None (already exists)
- **Files to modify**: None (already exists)
- **Reusable infrastructure**:
  - `key_takeaways.py` — **Already fully implemented** with curated takeaways for 20 stocks and auto-generation for others
  - `_render_takeaways()` in `_summary.py` — Already renders takeaways as `_summary_card("重點摘要", ...)` on the business card page
  - `generate_key_takeaways()` — Returns 3 bullet points from curated data or auto-generated from metrics
- **New infrastructure needed**: None
- **Estimate**: 0 hours (already complete)
  - **Why**: C37 is already implemented and rendering on the business card page (`_render_takeaways()` at line 221 of `_main.py`). The feature shows 3-5 bullet points (currently returns max 3 from `generate_key_takeaways()[:3]`) at the top of the stock page. Curated content exists for 20 top stocks; auto-generation covers the rest using毛利率, 營收年增率, PER, 殖利率, ROE, 負債比.
- **Risks**: None — this is done.
- **Prerequisites**: None.

**Note**: If the PM's intent is to *enhance* C37 (e.g., expand curated coverage from 20 to 50 stocks, or increase from 3 to 5 bullets), that would be 2-4 hours of content work in `key_takeaways.py`.

---

### C40: Beginner/Expert Mode Toggle

- **Files to create**:
  - `src/services/complexity_service.py` — Manages complexity level per user, determines which sections/metrics to show
- **Files to modify**:
  - `src/pages/business_card/_main.py` — The `simple_mode_toggle` (C105) already exists at line 208! C40 is an evolution/rebranding of this toggle
  - `src/pages/business_card/_sections/*.py` — Add complexity-aware rendering to each section (show simplified vs detailed versions)
  - `src/pages/settings.py` — Add default complexity level setting
  - `src/services/settings_service.py` — Add complexity threshold helpers
- **Reusable infrastructure**:
  - `simple_mode_toggle` in `_main.py` (C105) — **Already exists** as `st.toggle("簡易模式", value=True)`. C40 renames/rebrands this to "新手模式/專家模式"
  - `_render_simple_overview()` in `_main.py` — Already renders a simplified view when `simple_mode=True`
  - `analogy_engine.py` — Analogy functions already provide beginner-friendly explanations
  - `glossary_service.py` — Can provide glossary tooltips for expert mode
  - `settings_service.py` — Session state management for persisting the toggle
- **New infrastructure needed**:
  - Complexity level definitions (what's shown in beginner vs expert mode for each section)
  - Per-section complexity-aware rendering (some sections need beginner/expert variants)
- **Estimate**: 8-12 hours
  - **Why**: The toggle itself already exists (C105). C40 is about: (1) rebranding the toggle from "簡易模式" to "新手/專家模式" (~1h), (2) defining what each mode shows for ALL sections, not just the business card overview (~3h), (3) adding complexity-aware rendering to sections that currently only have one version (health, risk, valuation, revenue) (~4h), (4) persisting the setting in settings page (~1h), (5) testing both modes across all sections (~1-3h). The `_render_simple_overview()` already handles the simple case for the business card, but other pages (financial health, peer comparison, etc.) don't have simple/expert variants yet.
- **Risks**:
  - **Medium**: Defining "beginner" vs "expert" for every section is a design decision that affects many files. Each section needs a clear spec of what to hide/show.
  - **Low**: The toggle infrastructure is already in place; this is an extension, not a new feature.
  - **Medium**: If beginner mode hides too much, users might not discover important features. Need a "peek" mechanism (e.g., "專家模式還有更多..." hint).
- **Prerequisites**: C163 (Learn First Gate) should be coordinated with C40 since both define the beginner experience. C163 sets the initial complexity level; C40 lets users change it.

---

### C36: Visual Revenue Tree

- **Files to create**: None (already exists)
- **Files to modify**: None (already exists)
- **Reusable infrastructure**:
  - `revenue_tree.py` — **Already fully implemented** as a standalone page with pie chart, treemap toggle, revenue concentration warning, trend sparkline, and per-source analogies
  - `revenue_analyzer.py` — `analyze_revenue_breakdown()` with known revenue data for 8 companies + generic fallback
  - `chart.py` — `create_revenue_pie_chart()`, `create_revenue_treemap()`, `create_revenue_trend_chart()`
  - `analogy_engine.py` — `get_revenue_analogy()`, `get_yoy_analogy()`
  - `_白话_card()`, `_info_card()` from `_router_base.py`
- **New infrastructure needed**: None
- **Estimate**: 0 hours (already complete)
  - **Why**: C36 is already implemented as a standalone page (`營收結構樹`) accessible from the business card's "更多分析" expander. It shows revenue breakdown with pie/treemap toggle, concentration warnings, trend sparklines, and plain-language analogies. The revenue tree is also embedded inline in the business card's detailed mode expander.
- **Risks**: None — this is done.
- **Prerequisites**: None.

**Note**: If the PM wants to expand revenue tree coverage (more companies in `KNOWN_COMPANY_REVENUE`), that's 1-2 hours per company for research + data entry.

---

### C39: What Changed Recently Delta Card

- **Files to create**: None (already exists)
- **Files to modify**: None (already exists)
- **Reusable infrastructure**:
  - `delta_engine.py` — **Already fully implemented** with `compute_recent_deltas()` and `explain_delta_full()`
  - `delta_explanation_provider.py` — Tiered explanation templates for revenue, price, and YoY changes
  - `_render_deltas()` in `_story.py` — Already renders delta cards on the business card page
  - `_so_what_box()` in `_router_base.py` — Already synthesizes multiple deltas into a "So What?" implication
  - `_explain_button()` in `_router_base.py` — Already provides popover explanations for each delta
- **New infrastructure needed**: None
- **Estimate**: 0 hours (already complete)
  - **Why**: C39 is already implemented and rendering as "最近有什麼變化" on the business card page. It shows revenue MoM, price 30-day, and YoY changes with tiered explanations, implication sentences (C143), and "So What?" synthesis (C149). The delta card is above-fold on the business card.
- **Risks**: None — this is done.
- **Prerequisites**: None.

---

### C41: Read Next Recommendations

- **Files to create**: None (already exists)
- **Files to modify**: None (already exists)
- **Reusable infrastructure**:
  - `_render_read_next()` in `_story.py` — **Already fully implemented** with peer stock recommendations from the same industry
  - `company_facts.py` — `get_company_facts()` for curated "you might be curious" facts
  - `compare_stories.py` — `generate_compare_stories()` for narrative peer comparisons
  - `_info_card()` from `_router_base.py` — For rendering recommendation cards
  - `navigate_to()` from `url_sync.py` — For "查看名片" navigation buttons
- **New infrastructure needed**: None
- **Estimate**: 0 hours (already complete)
  - **Why**: C41 is already implemented as "推薦閱讀" on the business card page. It shows up to 5 peer stocks from the same industry with navigation buttons, plus 2 curated "你知道嗎？" facts from `company_facts.yaml`. It also has a "完整故事時間軸" navigation button (C28).
- **Risks**: None — this is done.
- **Prerequisites**: None.

---

## Recommended Sprint 20 Scope

Based on the analysis above, **C37, C36, C39, and C41 are already complete**. The remaining candidate features are C167, C152, C163, and C40. Here's the recommended scope within a 30-42h budget:

| Priority | Feature | Estimate | Running Total |
|----------|---------|----------|---------------|
| 1 | C167: AI Screener Explanations | 12-16h | 12-16h |
| 2 | C40: Beginner/Expert Mode Toggle | 8-12h | 20-28h |
| 3 | C163: Learn First Gate | 10-14h | 30-42h |
| — | C152: Multi-Factor Event Narratives | 14-18h | 44-60h (overflow) |

**Recommended scope: C167 + C40 + C163 = 30-42h**

**Rationale**:
- **C167** is the highest-value P1 feature. The screener exists but lacks narrative context. Adding explanations transforms it from a filter tool into a learning tool. Well-scoped, clear requirements, reusable infrastructure.
- **C40** is a natural evolution of the existing C105 simple mode toggle. The toggle already exists; C40 extends it to a proper beginner/expert mode system. High user value, moderate effort.
- **C163** is important for onboarding but slightly less critical than C167. It builds on the C103 first visit guide pattern. Coordinates well with C40.
- **C152** is the riskiest P1 feature due to multi-factor narrative complexity. The spike is done, but the template design is non-trivial. Recommend deferring to Sprint 21 unless the team has bandwidth.

**Alternative scope (if C152 spike gives high confidence)**:
| Priority | Feature | Estimate | Running Total |
|----------|---------|----------|---------------|
| 1 | C167: AI Screener Explanations | 12-16h | 12-16h |
| 2 | C152: Multi-Factor Event Narratives | 14-18h | 26-34h |
| 3 | C40: Beginner/Expert Mode Toggle (lite) | 6-8h | 32-42h |

This alternative drops C163 and does a lite version of C40 (just the toggle rename + settings persistence, without per-section complexity variants).

---

## Dependency Graph

```
C167 (AI Screener Explanations)
  ├── Depends on: stock_screener_service.py (exists)
  ├── Depends on: analogy_engine.py (exists)
  └── No blockers → Can start immediately

C40 (Beginner/Expert Mode Toggle)
  ├── Depends on: simple_mode_toggle / C105 (exists)
  ├── Coordinates with: C163 (both define beginner experience)
  └── No hard blockers → Can start immediately

C163 (Learn First Gate)
  ├── Depends on: first_visit_guide.py / C103 (exists)
  ├── Depends on: lesson_service.py pattern (exists)
  ├── Coordinates with: C40 (C163 sets initial level, C40 changes it)
  └── No hard blockers → Can start immediately

C152 (Multi-Factor Event Narratives)
  ├── Depends on: adaptive_engine.py (exists, M5 complete)
  ├── Depends on: delta_engine.py (exists)
  ├── Depends on: timeline_service.py pattern (exists)
  └── No hard blockers → Can start immediately

Already Complete (no work needed):
  ├── C37: Key Takeaways Summary Card (key_takeaways.py)
  ├── C36: Visual Revenue Tree (revenue_tree.py)
  ├── C39: What Changed Recently Delta Card (delta_engine.py)
  └── C41: Read Next Recommendations (_render_read_next)
```

**Key coordination points**:
- C163 and C40 should be designed together since they both affect the beginner experience
- C167 and C152 both create narratives but for different contexts (screener vs events) — no shared code, but consistent tone guidelines
- All features are independently implementable; no hard technical dependencies between them

---

## Technical Risks Summary

### High Risk
1. **C152: Multi-factor narrative quality** — Combining 2-3 events into a coherent story requires careful template design. Conflicting signals (revenue up + price down) need nuanced language that passes the historian tone blocklist. Risk of producing nonsensical or tone-violating narratives. **Mitigation**: Start with 5-8 common multi-event patterns, test extensively, expand iteratively.

### Medium Risk
2. **C163: Gate placement in router** — The router has 20+ page branches. The gate needs to intercept stock data pages without blocking standalone pages (settings, academy, etc.). Risk of breaking existing navigation. **Mitigation**: Define a clear `DATA_PAGES` set in the router; gate only applies to those pages.
3. **C40: Per-section complexity definitions** — Each of the 10+ business card sections needs a beginner/expert variant. Risk of inconsistent experience or missing variants. **Mitigation**: Create a complexity spec document before coding; start with 3-4 key sections.
4. **C167: Graceful degradation for sparse data** — Screener results may have stocks with missing metrics. Narratives must handle `None` values without breaking. **Mitigation**: Template design includes fallback paths for each metric.

### Low Risk
5. **C167: Performance** — Generating 20 narratives is pure Python string formatting; negligible overhead.
6. **C163: Content creation** — Writing onboarding card content is a PM/design task, not a dev risk.
7. **C40: Toggle persistence** — Already solved by C105's session_state pattern; just needs renaming.
8. **All features: Test coverage** — The project has 249+ passing tests and L0: 124/124. New services should follow the same pattern (pure Python services are easily testable). Budget 20-25% of each feature's time for tests.

### Codebase Health Notes
- The codebase is in excellent shape: 44 service modules, 0 god modules, 91% under 300 lines
- The compose-and-enrich pipeline pattern (timeline_service.py) is a good reference for C152
- The ExplanationProvider protocol (D5) is well-designed and should be reused for C167
- The `_router_base.py` card components (_info_card, _summary_card, _白话_card) provide consistent UI across all features
- The YAML-backed data pattern (events.yaml, case_studies_library.yaml, glossary.yaml) should be used for C152 templates and C163 onboarding content
