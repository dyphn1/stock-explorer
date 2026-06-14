## 2026-06-14 Technical Analysis — Sprint 19 Planning

### Problem Description

Sprint 19 must advance Stock Explorer's "historian, not a stock picker" positioning by adding narrative depth to the existing metric-centric views. Three P1 features are under discussion:

1. **C147 — Historical Event Pattern**: When a significant event is detected, show what historically followed similar events (range of outcomes, past tense, strict historian framing).
2. **C152 — Multi-Factor Event Narratives**: Combine multiple simultaneous event factors (e.g., revenue surge + news + institutional shift) into a single coherent narrative instead of showing disconnected event cards.
3. **C140 — Historical Case Study Library**: A browseable, searchable collection of curated historical case studies (e.g., "2008 Financial Crisis", "2021 Shipping Boom") that users can explore independently of any specific stock.

The challenge is to scope these features within the existing layered architecture (Data → Service → Router → Presentation), respecting the Streamlit-free service layer constraint, the ExplanationProvider protocol pattern, and the tone blocklist CI gate — while managing the interdependencies between all three features.

---

### Feature Feasibility Analysis

#### C147 — Historical Event Pattern

- **Feasibility: MEDIUM-HIGH** — The core infrastructure exists. `adaptive_engine.py` already detects events (revenue surge, price abnormal, news). `case_studies.yaml` already contains 5 richly structured historical scenarios with `related_stocks`, `key_metrics`, `lessons`, and `what_happened`. The `ExplanationProvider` protocol + `ExplanationResponse` can carry pattern data. The main gap is a service that bridges "current detected event type" → "historical patterns for similar events."

- **Data requirements:**
  - **Existing**: `case_studies.yaml` (5 scenarios, each with `related_stocks[]` linking to stock_ids), `adaptive_engine` event types (`revenue_surge`, `price_abnormal`, `news_major`, `news_medium`), `events.yaml` (detected events log).
  - **New/expanded**: A new `historical_patterns.yaml` (or extension to `case_studies.yaml`) that maps event types → historical precedents with structured outcome ranges. For example, `revenue_surge > 50%` → "In 3 of 5 historical cases, revenue continued growing for 2+ quarters; in 2 cases, it reverted within 1 quarter." This is primarily content creation (YAML), not API-dependent.
  - **FinMind dependency**: None for the pattern lookup itself (all local YAML). FinMind data is only needed to *trigger* the pattern display (already done by adaptive_engine).

- **Technical approach:**
  1. New service: `src/services/historical_pattern_service.py` — Pure Python, loads `historical_patterns.yaml`, provides `get_patterns_for_event(event_type, severity, magnitude) -> list[HistoricalPattern]`.
  2. New `HistoricalPattern` dataclass (or TypedDict) with fields: `pattern_title`, `historical_precedents: list[str]`, `outcome_range: str`, `sample_size: int`, `lessons: list[str]`.
  3. Presentation: A new section on the event dashboard (or a new tab on business card) that shows "📜 歷史上的類似事件" cards when an active event is detected. Uses existing `_scenario_card()` and `_historian_disclaimer()` helpers.
  4. Integration point: `timeline_service.py` Step 1 already fetches detected events from `adaptive_engine`. C147 adds a Step 1.5: for each detected event, look up historical patterns and attach them to the `TimelineEntry` as an optional `historical_pattern` field.
  5. Tone QA: All pattern text must pass the existing blocklist scanner. The `outcome_range` field must use past tense and range language ("3 of 5 cases showed...") not prediction language ("this will likely...").

- **Risks:**
  - **Content quality risk (HIGH)**: The value depends entirely on the quality and historical accuracy of the YAML content. Poorly researched patterns could mislead users. Mitigation: Start with 3-5 well-researched patterns for the most common event types (revenue_surge, price_abnormal, news_major).
  - **False precision risk (MEDIUM)**: Showing "3 of 5 cases" implies statistical rigor that may not exist. Mitigation: Use broad ranges, small sample sizes, and prominent disclaimers. The Challenger condition (strict historical framing) is the right guardrail.
  - **Scope creep risk (MEDIUM)**: The 2h feasibility spike is essential. The spike should validate that `case_studies.yaml` structure can be repurposed for event-type→pattern mapping without a full schema redesign.
  - **Tone compliance risk (LOW)**: The existing tone blocklist CI gate (`tests/test_tone_qa.py`) will catch violations. All new YAML content must be scanned.

#### C152 — Multi-Factor Event Narratives

- **Feasibility: MEDIUM** — This is the most architecturally complex of the three features. The current architecture treats events as independent items (each detected event is a separate card in the timeline). C152 requires correlating multiple events across types and time windows, then generating a unified narrative. The `ExplanationProvider` protocol is designed for single-metric explanations, not multi-factor synthesis.

- **Data requirements:**
  - **Existing**: `adaptive_engine` event detection (multiple types per stock), `events.yaml` (event log with dates, types, severities), `DeltaExplanationProvider` (already handles per-metric implications).
  - **New**: A narrative template system that maps event-factor combinations → narrative templates. For example: `{revenue_surge + price_up}` → "營收與股價同步上揚，顯示市場對公司基本面改善的認可。" This is YAML-based content, not API-dependent.
  - **FinMind dependency**: None for narrative generation. FinMind data is consumed upstream by the detection layer.

- **Technical approach:**
  1. New service: `src/services/narrative_engine.py` — Pure Python, implements a new `NarrativeProvider` protocol (separate from `ExplanationProvider`). Takes a list of `DetectedEvent` objects within a time window (e.g., 30 days) and produces a `NarrativeResponse` with fields: `headline`, `body`, `factors: list[str]`, `historical_parallel` (optional link to C147 pattern), `confidence` (based on number of corroborating factors).
  2. Event correlation logic: Group events by stock_id within a sliding window (default 30 days). If 2+ events of different types occur, trigger narrative generation.
  3. Template matching: A YAML file (`narrative_templates.yaml`) maps sorted event-type tuples → narrative templates with slot filling for stock_name, dates, magnitudes.
  4. Integration: The `timeline_service.py` pipeline can call `NarrativeEngine.synthesize()` after Step 1 (event fetching) and inject a synthetic "narrative" entry into the timeline. Alternatively, a new page/section renders narratives separately.
  5. Protocol design: `NarrativeProvider` is a new protocol (not extending `ExplanationProvider`) because the input is fundamentally different (multiple events vs. single metric). This follows the existing pattern of protocol-based design with composition.

- **Risks:**
  - **Architectural complexity risk (HIGH)**: This is the most complex feature. The design spike is essential. The narrative quality depends on template coverage — with N event types, the combination space is 2^N - N - 1. Starting with the 3-4 most common combinations (revenue+price, revenue+news, price+institutional) covers ~80% of real cases.
  - **Tone risk (HIGH)**: Multi-factor narratives are more likely to sound like investment advice because they synthesize directional signals. The tone blocklist must be extended to catch synthesis-level advisory phrases. All templates must be reviewed by QA before merge.
  - **Dependency on C147 (MEDIUM)**: C152's `historical_parallel` field naturally links to C147's pattern data. If C147 is deferred, C152 can still function but with reduced narrative depth.
  - **Design spike required (per handoff)**: The 16-20h estimate assumes a successful design spike. If the spike reveals fundamental architectural blockers, this could balloon to 25+h.

#### C140 — Historical Case Study Library

- **Feasibility: HIGH** — This is the most straightforward feature architecturally. The data already exists (`case_studies.yaml` has 5 complete scenarios). The presentation pattern (browseable card grid with search/filter) is well-established in the codebase (see `academy.py`, `event_dashboard.py`). The primary effort is content creation (40% of the 16-22h estimate).

- **Data requirements:**
  - **Existing**: `case_studies.yaml` — 5 richly structured scenarios with `title`, `date`, `summary`, `what_happened`, `key_metrics`, `lessons`, `related_stocks`, `severity`.
  - **New/expanded**: The existing YAML schema needs minor additions for library browsing: `category` (e.g., "金融危機", "科技泡沫", "產業循環", "地緣政治"), `tags: list[str]`, `cover_image` (optional), `read_time_minutes: int`. 10-15 additional case studies for a meaningful library.
  - **FinMind dependency**: None. All content is curated YAML.

- **Technical approach:**
  1. New service: `src/services/case_study_library.py` — Pure Python, loads `case_studies.yaml`, provides `search_case_studies(query, category, tags) -> list[CaseStudy]` and `get_case_study_by_id(id) -> CaseStudy`. Follows the same pattern as `glossary_service.py` (YAML load + filter).
  2. New page: `src/pages/case_study_library.py` — Searchable grid of case study cards with category filters, tag chips, and detail view. Follows the `academy.py` page pattern.
  3. Router registration: Add to standalone pages (no stock_id required), same as `category_browser.py` and `academy.py`.
  4. Cross-linking: Each case study's `related_stocks` field links to stock pages. Each stock's business card can link to relevant case studies (via `case_study_service.get_case_stocks(stock_id)`).
  5. Tone QA: All case study content passes through the existing blocklist scanner. The `lessons` field is the highest-risk content and should be reviewed manually.

- **Risks:**
  - **Content creation bottleneck (HIGH)**: 40% of the effort is writing 10-15 quality case studies. This is a designer/PM task, not a developer task. If content isn't ready, the feature ships with only the existing 5 scenarios — still functional but thin.
  - **YAML schema evolution (LOW)**: Adding `category`/`tags` fields to the existing schema is backward-compatible (new fields are optional). Existing 5 scenarios can be migrated incrementally.
  - **Search quality (LOW)**: Simple keyword matching on title/summary is sufficient for <50 items. No need for full-text search infrastructure.

---

### Proposed Directions

#### Direction A: "Pattern-First" — C147 + C140 Combined, C152 Deferred

- **Description**: Implement C147 (Historical Event Pattern) and C140 (Case Study Library) as a unified feature. C140 provides the content library; C147 uses that content to show relevant historical patterns when events are detected. C152 (Multi-Factor Narratives) is deferred to Sprint 20.
  - C140's `case_study_library.py` service is built first, extending `case_studies.yaml` with category/tags.
  - C147's `historical_pattern_service.py` is built as a thin layer on top of the case study library, mapping event types → case studies.
  - The presentation layer adds a "📜 歷史上的類似事件" section to the event dashboard and business card page.
  - C152's design spike is deferred; the event correlation logic is noted as future work.

- **Pros:**
  - C140 and C147 share the same data source (`case_studies.yaml`), reducing content creation overhead.
  - C147's feasibility spike (2h) validates the event-type→case-study mapping before committing.
  - Lower architectural risk: no new protocol (`NarrativeProvider`) needed.
  - Fits within Sprint 19 budget: C147 (14-18h) + C140 (16-22h) = 30-40h, but with shared content and infrastructure, effective cost is ~28-35h.
  - Delivers immediate user value: users can browse case studies AND see historical patterns on stock pages.

- **Cons:**
  - Defers C152, which is the most impactful narrative feature (P1).
  - Without C152, the event dashboard still shows disconnected event cards (no synthesis).
  - The "historical pattern" in C147 is limited to what case studies exist — if no matching case study exists, the section is empty.

- **Effort: 28-35h** (C147: 14-18h + C140: 10-14h dev + 4-6h content creation for 5 new case studies)

#### Direction B: "Narrative Core" — C152 Design Spike + C147, C140 Content Prep

- **Description**: Prioritize the C152 design spike (4-6h) in the first sprint week. If the spike succeeds, implement C152's `narrative_engine.py` + `narrative_templates.yaml` as the core narrative infrastructure. Simultaneously implement C147 as a supporting feature (historical patterns enrich C152 narratives). C140 is limited to content preparation (writing 5-10 new case studies) without the browseable library page.
  - Week 1: C152 design spike (4-6h) + C147 feasibility spike (2h, can run in parallel with spike analysis).
  - Week 2: C152 implementation (12-14h) + C147 implementation (10-12h, reusing C152's narrative infrastructure).
  - C140 content: 4-6h of content creation (separate from dev track).

- **Pros:**
  - C152 is the most differentiating feature — no competitor has multi-factor narrative synthesis.
  - C147 and C152 share infrastructure: C152's `NarrativeProvider` can incorporate C147's historical patterns as a narrative element.
  - If the C152 spike fails, the team can fall back to Direction A with only 4-6h invested.
  - Positions Sprint 20 for C140 full implementation + C152 enhancements.

- **Cons:**
  - Highest risk: C152's design spike could reveal blockers that invalidate the approach.
  - C140 library page is deferred — users can't browse case studies independently.
  - Tight timeline: 4-6h spike + 12-14h C152 + 10-12h C147 = 26-32h dev + 4-6h content = 30-38h. Leaves little buffer.
  - If the spike fails and Direction A is chosen mid-sprint, there's context-switching cost.

- **Effort: 30-38h** (C152 spike: 4-6h + C152 impl: 12-14h + C147: 10-12h + C140 content: 4-6h)

#### Direction C: "Content Foundation" — C140 Full + C147 Spike, C152 Deferred

- **Description**: Use Sprint 19 to build the content and data foundation for all three features. Implement C140 fully (library page + 10-15 new case studies). Run the C147 feasibility spike and, if successful, implement a minimal version (3 event-type patterns). Defer C152 entirely to Sprint 20.
  - C140 is the primary deliverable: full library page with search, filter, detail view.
  - C147 feasibility spike (2h) → if greenlit, implement with 3 patterns for the most common event types.
  - C152: Design doc only (no implementation), positioning it as Sprint 20's primary feature.
  - Content creation is the main effort: 8-10h for 10-15 new case studies.

- **Pros:**
  - Lowest risk: C140 is the most feasible feature; C147 spike is low-cost.
  - Builds the content foundation that C147 and C152 both need.
  - C140 delivers standalone user value (browseable library) even without C147/C152.
  - Sprint 20 can focus entirely on C152 with a rich content library already in place.
  - Most predictable timeline: C140 (16-22h) + C147 spike+impl (2h + 8-10h) = 26-34h.

- **Cons:**
  - No narrative features ship in Sprint 19 — only the content library.
  - C147 minimal version may feel incomplete (only 3 patterns).
  - Defers both C147 (full) and C152, the two P1 narrative features, by another sprint.
  - May feel like a "content sprint" rather than a "feature sprint" to stakeholders.

- **Effort: 26-34h** (C140: 12-16h dev + 8-10h content + C147 spike: 2h + C147 impl: 8-10h, but with 3 patterns only)

---

### Recommendation

**Direction A ("Pattern-First")** is the recommended approach for Sprint 19, with the following rationale:

1. **Balances delivery and risk**: Ships two features (C140 + C147) with shared infrastructure, while deferring the riskiest feature (C152) to Sprint 20. The C147 feasibility spike (2h) is a prerequisite regardless of direction.

2. **Content synergy**: C140 and C147 both consume `case_studies.yaml`. Building the library service first means C147's pattern matcher can query the same data source. This is more efficient than building separate data pipelines.

3. **User value**: Users get both a browseable case study library (C140) AND contextual historical patterns when viewing stock events (C147). This is a coherent user experience: "I can explore history on my own, AND the app shows me relevant history when it matters."

4. **Architectural soundness**: No new protocols needed. C147's `historical_pattern_service.py` follows the same YAML-load-and-filter pattern as `glossary_service.py`. C140's `case_study_library.py` follows the `academy.py` page pattern. Both are low-risk, high-confidence implementations.

5. **Sprint 20 positioning**: With C140's content library and C147's pattern infrastructure in place, C152 (Multi-Factor Narratives) in Sprint 20 can focus on the novel synthesis logic rather than content creation. The `NarrativeProvider` protocol can compose with the existing `CaseStudyLibrary` service for historical parallels.

6. **Fits the budget**: 28-35h fits within the 34-42h Sprint 19 budget from the handoff, with buffer for the C147 feasibility spike and content creation.

**Critical success factor**: The C147 feasibility spike must validate that event-type→case-study mapping is meaningful. If the spike reveals that case studies don't map cleanly to event types (e.g., most case studies are market-wide, not event-type-specific), then Direction C should be used instead, and C147 should be re-scoped for Sprint 20 with a dedicated `historical_patterns.yaml`.

---

### Dependencies & Risks

**Cross-feature dependencies:**

| Dependency | Type | Impact |
|---|---|---|
| C140 → C147 | Data dependency (soft) | C147 can use `case_studies.yaml` directly without C140's library service, but C140's enriched schema (category/tags) makes pattern matching more precise. |
| C147 → C152 | Data dependency (soft) | C152 can incorporate C147's `HistoricalPattern` objects as narrative elements. If C147 is deferred, C152 narratives lack historical depth but still function. |
| C140 → C152 | Data dependency (soft) | C152 can link narratives to case studies via `related_stocks`. If C140 is deferred, C152 can still use `case_studies.yaml` directly. |
| C147 → Tone QA | Hard requirement | All pattern text must pass `tests/test_tone_qa.py`. The blocklist must be validated against range-of-outcomes language before C147 content is written. |
| C152 → Tone QA | Hard requirement | Multi-factor narratives have the highest advice-risk. Requires manual QA review in addition to automated scanning. |

**Technical risks (ranked by severity):**

1. **C152 architectural complexity** (HIGH): The `NarrativeProvider` protocol, event correlation logic, and template matching system are all new. The design spike is essential. If the spike reveals that event correlation produces too many false positives (e.g., unrelated events within the same window), the approach needs rethinking.

2. **Content quality at scale** (HIGH): All three features depend on YAML content quality. `case_studies.yaml` has 5 scenarios; C140 needs 15+, C147 needs event-type mappings, C152 needs narrative templates. Content creation is 30-40% of the total effort and is on the critical path.

3. **Tone compliance across languages** (MEDIUM): The tone blocklist is enforced via AST scanning of Python files, but YAML content is loaded at runtime and may not be scanned. Need to verify that `tests/test_tone_qa.py` also scans YAML files under `src/data/`, or add a separate YAML tone check.

4. **`market_event_service` import failure** (LOW): `timeline_service.py` imports `from src.services.market_event_service import get_events_for_stock` but this module doesn't exist in the codebase. The import is wrapped in try/except, so it fails gracefully, but it means case studies are never actually loaded into the timeline. C147 and C140 should NOT depend on this import path. Instead, they should load `case_studies.yaml` directly (following the `company_milestones.yaml` pattern).

5. **Service module count growth** (LOW): Adding 2-3 new service modules (pattern service, case study library, narrative engine) brings the total from 44 to 47-48. Still well within the "0 god modules" constraint. No action needed.

**Recommended risk mitigations:**
- Run the C147 feasibility spike on Day 1 of Sprint 19 (2h, as required by Challenger condition).
- Add YAML tone scanning to `tests/test_tone_qa.py` before writing new content.
- Fix the `market_event_service` import in `timeline_service.py` (or replace with direct YAML loading) as part of C140/C147 work.
- Pre-write 5 case studies during Sprint 18 wrap-up (content creation can happen in parallel with dev).
