## 2026-06-14 Developer Estimates — Sprint 19 Planning

> **Developer**: Developer Agent (openrouter/owl-alpha)
> **Date**: 2026-06-14
> **Scope**: Sprint 19 — C147 (Historical Event Pattern) + C152 (Multi-Factor Event Narratives) + C140 (Historical Case Study Library)
> **Context**: Sprint 18 ✅ COMPLETE. 44 service modules, 249 tests passing. Architecture 🟢 HEALTHY. Design Grade A (5th consecutive).
> **Baseline**: Sprint 18 actual was 27.6h against 24-32h estimate (on target). Use Sprint 18 actuals to calibrate Sprint 19.

---

### C147 — Historical Event Pattern

- **Feasibility Spike: 2h (2h is sufficient, barely)**
  - The spike validates one specific question: can `case_studies.yaml` event-type tags map cleanly to `adaptive_engine.py` event types (`revenue_surge`, `price_abnormal`, `news_major`, `news_medium`, `dividend_change`, `institutional_shift`)?
  - Existing `case_studies.yaml` has 5 scenarios with `related_stocks` but NO event-type field. The spike must determine whether to: (a) add an `event_types` field to each case study, or (b) create a separate `historical_patterns.yaml` mapping event types → patterns.
  - 2h is enough to load the YAML, write a quick mapping prototype, and validate that 3+ event types can be matched. It is NOT enough to build the full service.
  - **Risk**: If the spike reveals that case studies don't map to event types (most are market-wide, not event-specific), C147 needs a different data source. This would push it to Sprint 20.

- **Service Layer: 6-8h (new services: `historical_pattern_service.py`)**
  - `historical_pattern_service.py` (~120 lines): Loads `historical_patterns.yaml` (new file), provides `get_patterns_for_event(event_type, severity, magnitude) -> list[HistoricalPattern]`. Follows the exact pattern as `glossary_service.py` (YAML load + filter + cache).
  - `HistoricalPattern` dataclass: `pattern_title`, `historical_precedents: list[str]`, `outcome_range: str`, `sample_size: int`, `lessons: list[str]`, `disclaimer: str`.
  - Integration into `timeline_service.py`: Add Step 1.5 after event detection — for each detected event, look up historical patterns and attach to `TimelineEntry` as optional `historical_pattern` field. ~20 lines added to timeline_service.py.
  - **Reuses**: `adaptive_engine.py` event types (no changes), `ExplanationResponse` protocol (no changes), `market_event_service.py` `get_events_for_stock()` (no changes).

- **Page Layer: 4-5h (modified pages: `event_dashboard.py`, `story_timeline.py`)**
  - `event_dashboard.py`: Add "📜 歷史上的類似事件" section below event cards when `historical_pattern` data exists. Uses existing `_scenario_card()` and `_historian_disclaimer()` helpers from `_historical_scenarios.py`. ~40 lines added.
  - `story_timeline.py`: Add historical pattern badge to timeline entries that have pattern data. ~15 lines added.
  - No new page needed. No new shared components needed.
  - **Reuses**: `_scenario_card()`, `_historian_disclaimer()`, `_severity_badge()` — all existing.

- **Content: 3-4h (new YAML: `historical_patterns.yaml`)**
  - New file: `src/data/historical_patterns.yaml` with 4-6 patterns for the most common event types.
  - Each pattern: 3-5 historical precedents, outcome range text, sample size, lessons, disclaimer.
  - Writing historically accurate, tone-compliant content in zh-TW is the bulk of this effort.
  - Tone QA: All pattern text must pass blocklist. The `outcome_range` field is highest risk (must use past tense, range language).

- **Testing: 2-3h**
  - `tests/services/test_historical_pattern_service.py`: ~25 tests covering event type lookup, severity filtering, empty results, malformed YAML, cache behavior.
  - `tests/test_tone_qa.py`: Verify YAML content is scanned (currently only scans .py files — need to add YAML scanning or add a separate test).
  - L0/L1 verification.

- **Total: 17-22h** (spike 2h + service 6-8h + page 4-5h + content 3-4h + testing 2-3h)

- **Technical Risks:**
  1. **🔴 Data model risk**: `case_studies.yaml` has no event-type field. The feasibility spike must validate the mapping approach. If mapping fails, need a new YAML file (+2h content).
  2. **🟡 Content quality risk**: Historical patterns must be factually accurate and tone-compliant. Poor patterns mislead users. Mitigation: Start with 4 well-researched patterns for `revenue_surge`, `price_abnormal`, `news_major`, `news_medium`.
  3. **🟡 Tone compliance risk**: Outcome range text ("3 of 5 cases showed...") must not sound predictive. The tone blocklist scanner currently only scans .py files — YAML content loaded at runtime is NOT scanned. Need to add YAML scanning to `test_tone_qa.py` or create a separate YAML tone check (+0.5h).
  4. **🟢 False precision risk**: Small sample sizes (3-5 cases) with prominent disclaimers mitigate this.

- **Reusable Infrastructure:**
  - `adaptive_engine.py` event detection (no changes needed)
  - `market_event_service.py` `get_events_for_stock()` (no changes needed)
  - `timeline_service.py` compose-and-enrich pipeline (minimal extension)
  - `_scenario_card()`, `_historian_disclaimer()` helpers (no changes needed)
  - `glossary_service.py` pattern (YAML load + filter + cache)
  - `tests/test_tone_qa.py` (extend to scan YAML)

---

### C152 — Multi-Factor Event Narratives

- **Design Spike: 4-6h (recommended, not 2h)**
  - C152 is the most architecturally complex feature in Sprint 19. The design spike must validate:
    1. Event correlation logic: How to group events by stock_id within a sliding window (30 days). What threshold triggers narrative generation (2+ events of different types? 3+?).
    2. Template coverage: With 6 event types, the combination space is 2^6 - 6 - 1 = 57 possible multi-factor combinations. The spike must identify the 5-8 most common combinations that cover ~80% of real cases.
    3. Protocol design: Whether `NarrativeProvider` should be a new protocol or extend `ExplanationProvider`. Recommendation: New protocol because input is fundamentally different (multiple events vs. single metric).
    4. Integration point: Whether narratives are injected into `timeline_service.py` as synthetic entries or rendered as a separate section.
  - 4-6h is realistic for a thorough design spike. 2h would only cover a superficial review.

- **Service Layer: 8-10h (new services: `narrative_engine.py`)**
  - `narrative_engine.py` (~180 lines): New `NarrativeProvider` protocol + `NarrativeResponse` dataclass + `TemplateNarrativeProvider` implementation.
  - `NarrativeResponse`: `headline`, `body`, `factors: list[str]`, `historical_parallel: Optional[HistoricalPattern]`, `confidence: float`, `disclaimer: str`.
  - Event correlation logic: Group events by stock_id within 30-day sliding window. Trigger on 2+ different event types. ~40 lines of logic.
  - Integration with C147: `TemplateNarrativeProvider` can incorporate `HistoricalPattern` objects as narrative elements (soft dependency — graceful degradation if C147 deferred).
  - **Reuses**: `adaptive_engine.py` event types, `events.yaml` event log, `ExplanationProvider` pattern (protocol-based design), `event_interpretation_service.py` template loading pattern.

- **Page Layer: 4-5h (modified pages: `event_dashboard.py`, `story_timeline.py`)**
  - `event_dashboard.py`: Add "📖 事件敘事" section that renders `NarrativeResponse` as a synthesized narrative card. Uses existing `_白话_card()` with `label="事件敘事"`. ~30 lines added.
  - `story_timeline.py`: Inject narrative entries as synthetic timeline entries with a distinct icon (📖). ~15 lines added.
  - No new page needed.
  - **Reuses**: `_白话_card()`, `_section_title()`, severity badge helpers.

- **Content: 3-4h (new YAML: `narrative_templates.yaml`)**
  - New file: `src/data/narrative_templates.yaml` mapping event-type tuples → narrative templates.
  - Start with 5-8 combinations: `{revenue_surge + price_up}`, `{revenue_surge + news_major}`, `{price_abnormal + news_major}`, `{revenue_surge + institutional_shift}`, `{price_abnormal + institutional_shift}`.
  - Each template: `headline` (slot-filled), `body` (slot-filled), `disclaimer`.
  - All templates must pass tone blocklist. Multi-factor narratives have the HIGHEST advice-risk because synthesizing directional signals sounds like investment advice.

- **Testing: 3-4h**
  - `tests/services/test_narrative_engine.py`: ~30 tests covering event correlation logic, template matching, empty results, single-event fallback, multi-event synthesis, confidence scoring.
  - Tone QA for all narrative templates (manual review + automated scanning).
  - L0/L1 verification.

- **Total: 22-29h** (spike 4-6h + service 8-10h + page 4-5h + content 3-4h + testing 3-4h)

- **Technical Risks:**
  1. **🔴 Architectural complexity risk**: This is the most complex feature. The design spike could reveal fundamental blockers (e.g., event correlation produces too many false positives). If the spike fails, fall back to showing individual event cards with C147 historical patterns only.
  2. **🔴 Tone compliance risk**: Multi-factor narratives are the highest advice-risk content in the product. Synthesizing "revenue up + price up" into a narrative can easily sound like "this is a buy signal." Requires manual QA review in addition to automated scanning. All templates must use factual past-tense framing.
  3. **🟡 Template coverage risk**: 5-8 templates cover ~80% of cases, but the remaining 20% may produce awkward fallback text. Mitigation: A well-written generic fallback template for uncovered combinations.
  4. **🟡 Dependency on C147**: C152's `historical_parallel` field links to C147's `HistoricalPattern`. If C147 is deferred, C152 still functions but with reduced narrative depth. This is a soft dependency — acceptable.
  5. **🟢 Protocol design risk**: New `NarrativeProvider` protocol follows the same pattern as `ExplanationProvider`. Low risk given existing precedent.

- **Reusable Infrastructure:**
  - `adaptive_engine.py` event detection (no changes needed)
  - `events.yaml` event log (no changes needed)
  - `ExplanationProvider` protocol pattern (for design reference, not reuse)
  - `event_interpretation_service.py` template loading pattern
  - `_白话_card()`, `_section_title()` helpers
  - C147's `HistoricalPattern` dataclass (soft dependency)

---

### C140 — Historical Case Study Library

- **Service Layer: 3-4h (new services: `case_study_library.py`)**
  - `case_study_library.py` (~80 lines): Loads `case_studies.yaml`, provides `search_case_studies(query, category, tags) -> list[CaseStudy]` and `get_case_study_by_id(id) -> CaseStudy` and `get_case_studies_for_stock(stock_id) -> list[CaseStudy]`.
  - Follows the exact pattern as `glossary_service.py` (YAML load + filter + cache). Very low risk.
  - Minor: Add `category`, `tags`, `read_time_minutes` fields to the existing `CaseStudy` dataclass (if one exists) or create a new one.
  - **Reuses**: `market_event_service.py` already loads `case_studies.yaml` — can extend or duplicate the loading logic. `glossary_service.py` pattern.

- **Page Layer: 5-7h (new page: `case_study_library.py`)**
  - New page: `src/pages/case_study_library.py` (~200 lines). Searchable grid of case study cards with category filters, tag chips, and detail view.
  - Follows the `academy.py` page pattern (standalone page, no stock_id required).
  - Search: Simple keyword matching on title/summary (sufficient for <50 items, no full-text search needed).
  - Filter: Category dropdown + tag chips.
  - Detail view: Expandable card or separate page section showing full case study content.
  - Router registration: Add to standalone pages in `router.py` (~3 lines).
  - Cross-linking: Each case study's `related_stocks` field links to stock pages via `navigate_to()`.
  - **Reuses**: `academy.py` page pattern, `_section_title()`, `_info_card()`, `_scenario_card()`, `_historian_disclaimer()`, `navigate_to()`.

- **Content: 6-10h (YAML schema extension + 10-15 new case studies)**
  - **Schema extension**: Add `category`, `tags`, `read_time_minutes` fields to existing `case_studies.yaml`. Backward-compatible (new fields optional). ~0.5h.
  - **Existing content migration**: Add category/tags to existing 5 case studies. ~1h.
  - **New content creation**: 10-15 new case studies for a meaningful library. This is 40% of the total effort.
    - Each case study: title, date, summary, what_happened (5-8 bullet points), key_metrics (3-5 metrics with analogies), lessons (3-4 lessons), related_stocks (2-3 stocks with impact).
    - Estimated 0.5-1h per case study for research + writing + tone compliance.
    - Total: 5-10h for 10-15 case studies.
  - **Tone QA**: All case study content must pass blocklist. The `lessons` field is highest risk.

- **Testing: 2-3h**
  - `tests/services/test_case_study_library.py`: ~20 tests covering search by query, filter by category, filter by tags, get by ID, get for stock, empty results, malformed YAML.
  - Tone QA for all new YAML content.
  - L0/L1 verification.

- **Total: 16-24h** (service 3-4h + page 5-7h + content 6-10h + testing 2-3h)

- **Technical Risks:**
  1. **🔴 Content creation bottleneck**: 40% of the effort is writing 10-15 quality case studies. This is a designer/PM task, not a developer task. If content isn't ready, the feature ships with only the existing 5 scenarios — still functional but thin.
  2. **🟡 YAML schema evolution**: Adding `category`/`tags` fields is backward-compatible, but the existing 5 case studies need migration. Low risk.
  3. **🟢 Search quality**: Simple keyword matching is sufficient for <50 items. No full-text search infrastructure needed.
  4. **🟢 Page pattern risk**: Very low — follows `academy.py` pattern exactly.

- **Reusable Infrastructure:**
  - `case_studies.yaml` (existing 5 scenarios)
  - `market_event_service.py` YAML loading pattern
  - `glossary_service.py` search/filter pattern
  - `academy.py` page pattern (standalone page, search, filter)
  - `_section_title()`, `_info_card()`, `_scenario_card()`, `_historian_disclaimer()` helpers
  - `navigate_to()` for cross-linking

---

### Sprint 19 Total Estimate

- **Combined: 55-75h** (C147: 17-22h + C152: 22-29h + C140: 16-24h)
- **Realistic target: 58-68h** (assuming C147 spike succeeds, C152 spike succeeds, content creation is shared with PM/designer)

#### Parallelization Opportunities:

| Track | Features | Effort | Dependencies |
|-------|----------|--------|--------------|
| **Track A (Dev)** | C147 service + page | 12-16h | C147 spike (Day 1) |
| **Track B (Dev)** | C152 service + page | 16-20h | C152 spike (Day 1-2) |
| **Track C (Dev)** | C140 service + page | 8-11h | None (independent) |
| **Track D (Content)** | C140 content (10-15 case studies) | 6-10h | None (can start immediately) |
| **Track E (Content)** | C147 patterns YAML (4-6 patterns) | 3-4h | C147 spike |
| **Track F (Content)** | C152 narrative templates (5-8 templates) | 3-4h | C152 spike |

- **C140 (Track C + D) can start immediately** — no spike needed, no dependencies on C147/C152.
- **C147 (Track A + E) starts after 2h spike on Day 1** — soft dependency on C140 only if sharing `case_studies.yaml` schema.
- **C152 (Track B + F) starts after 4-6h design spike on Day 1-2** — soft dependency on C147 for `historical_parallel` field.
- **Content tracks (D, E, F) can run in parallel with dev tracks** — content creation is independent of code implementation.

#### Critical Path:

1. **Day 1**: C147 feasibility spike (2h) + C152 design spike (4-6h, can run in parallel if two devs). C140 service+page dev can start immediately.
2. **Day 2-3**: C147 service implementation + C140 page implementation. C152 service implementation starts after spike.
3. **Day 4-5**: C147 page integration + C152 page integration. Content creation (case studies, patterns, templates) ongoing in parallel.
4. **Day 6-7**: Testing for all three features. Tone QA for all new YAML content. L0/L1 verification.

**If single developer**: Sequential execution is required. Order: C140 (easiest, builds content foundation) → C147 (moderate, spike first) → C152 (hardest, design spike first). Total: 55-75h over 7-9 days.

**If two developers**: Dev1 does C140 + C147 (24-33h), Dev2 does C152 (22-29h). Content creation shared with PM/designer. Total calendar time: 5-7 days.

#### Risk Adjustment:

| Risk | Probability | Impact | Adjustment |
|------|------------|--------|------------|
| C147 spike reveals data model mismatch | 25% | +3-4h (new YAML file) | Already accounted in range |
| C152 spike reveals architectural blockers | 20% | +5-8h (redesign) or defer to Sprint 20 | If deferred, Sprint 19 total drops to 33-46h |
| Content creation bottleneck (C140) | 40% | Feature ships with 5 case studies only | Not a blocker — still functional |
| Tone QA failures in new YAML content | 30% | +1-2h (rewrite) | Already accounted in content estimates |
| Tone QA doesn't scan YAML files | 100% (known gap) | +0.5h (add YAML scanning) | Should be a prerequisite before content creation |

**Recommended risk buffer**: +3-5h for unknowns (tone QA YAML scanning, content iteration, integration edge cases).

#### Final Recommendation:

**Sprint 19 budget: 58-73h** (including risk buffer).

This is higher than the handoff's 34-42h estimate because:
1. The handoff estimate was a rough PM estimate before detailed technical analysis.
2. C152's design spike (4-6h) was not explicitly budgeted in the handoff.
3. Content creation for C140 (6-10h) is now more precisely estimated.
4. Tone QA YAML scanning gap (+0.5h) and risk buffer (+3-5h) added.

**If the sprint budget is capped at 42h**, defer C152 to Sprint 20 and implement C147 + C140 only (33-46h). This is the "Pattern-First" direction recommended by the Architect.

**If the sprint budget is 55-75h**, implement all three features with the parallelization plan above.

---

*Created: 2026-06-14*
*Reviewer: Developer Agent (openrouter/owl-alpha)*
*Next: Sprint 19 execution planning*
