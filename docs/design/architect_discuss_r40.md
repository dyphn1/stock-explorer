# Architect Discussion Analysis — Round 40

## Current Architecture Assessment

### Codebase State (Sprint 19, 5/6 complete)

**Scale**: ~44 service modules (40 top-level + 3 LLM sub-modules + `__init__.py`), 0 god modules, 91% under 300 lines, 98% Streamlit-free in service layer.

**Quality Gates**: L0: 124/124 passing, Tests: 249+ passing.

**Key Infrastructure**:
- **ExplanationProvider protocol** (`src/services/llm/base.py`) — Clean Protocol + dataclass design. `TemplateExplanationProvider` is the current implementation. Factory pattern in `factory.py` ready for future LLM swap.
- **TemplateExplanationProvider** (`src/services/llm/template_provider.py`, 131 lines) — 9 metric templates with increase/decrease/neutral directions. Used by `metric_explainer.py` and `delta_explanation_provider.py`.
- **analogy_engine.py** (193 lines) — Now clean after D16 split. Contains only analogy functions (one-liners, revenue/PER/dividend/ROE/gross margin/volume/institutional analogies). Health scoring moved to `health_scoring.py` (269 lines), key takeaways to `key_takeaways.py`, deltas to `delta_engine.py` (183 lines).
- **compose-and-enrich pipeline** (`src/services/timeline_service.py`, 299 lines) — Merges events + case studies + milestones into enriched `TimelineEntry` dicts. Used by story timeline page and `story_feed.py`.
- **YAML-backed data services** — 25+ YAML files under `src/data/yaml/` and `src/data/`. Pattern established: data in YAML, loading/parsing in Python. Examples: `industry_benchmarks.yaml`, `key_takeaways.yaml`, `one_liners.yaml`, `group_structures.yaml`, `moat_data.yaml`, `glossary.yaml`, `historical_scenarios.yaml`, `expert_analysis.yaml`.
- **BatchAPI** (`src/data/batch_api.py`, 230 lines) — Eliminates N+1 query patterns. Used by `stock_screener_service.py` and `story_feed.py`.
- **market_data.py** (283 lines) — Sector-level data aggregation. Abstracts market-wide access for sector heatmap and story feed.
- **financial_metrics.py** (188 lines) — Shared financial calculations (extracted via R1). All financial metric consumers import from one place.
- **business_card sub-directory** — Extracted via D24 into `_sections/` with 8 section modules: `_summary`, `_financial`, `_health`, `_story`, `_detail`, `_historical_pattern`, `_moat`, `_expert_analysis`. Main orchestrator `_main.py` (312 lines) imports from sections.

### Architecture Debt Status
- **Resolved**: D1, D2, D17, D20, D16 (financial metrics duplication, EPS triplication, valuation double-computation, analogy_engine god module split)
- **Open (critical)**: D24 (business_card.py — now extracted, resolved)
- **Open (medium)**: D3 (inline HTML), D5 (LLM abstraction — partially done), D6 (hardcoded data — partially migrated), D12 (routing/UI mix), D19 (inline HTML in business_card)
- **Open (low/performance)**: D7/D8 (sequential API calls — BatchAPI exists but not all pages use it), D9/D10 (YAML re-read)

### What Already Exists (Sprint 19 context)
Many candidate features for Sprint 20 are **already partially or fully built**:
- **C37** (Key Takeaways) — ✅ Built. `key_takeaways.py` service + `_render_takeaways` in `_summary.py`.
- **C39** (What Changed Delta Card) — ✅ Built. `delta_engine.py` + `delta_explanation_provider.py` + `_render_deltas` in `_story.py`.
- **C41** (Read Next Recommendations) — ✅ Built. `_render_read_next` in `_story.py`.
- **C36** (Visual Revenue Tree) — ✅ Built. `create_revenue_treemap()` in `chart.py` + `revenue_tree.py` page.
- **C40** (Beginner/Expert Mode) — ⚠️ Partial. `settings_service.py` exists with threshold helpers, but no complexity toggle UI.
- **C163** (Learn First Gate) — ⚠️ Partial. `lesson_service.py` (207 lines) + `academy.py` page (367 lines) exist, but no "gate" that blocks data access before education.
- **C152** (Multi-Factor Event Narratives) — ⚠️ Partial. `event_interpretation_service.py` (123 lines) + `pattern_detector.py` (91 lines) + `adaptive_engine.py` (622 lines) exist. Spike done per task description.
- **C167** (AI Screener Explanations) — ⚠️ Partial. `stock_screener_service.py` (232 lines) + `stock_screener.py` page exist, but no plain-language outcome narratives.

---

## Proposed Sprint 20 Directions

### Direction A: "Narrative Intelligence Layer" — Complete the Story Engine

**Features included**: C167 (AI Screener Explanations) + C152 (Multi-Factor Event Narratives)

**Technical approach**:
- **C167**: Add a new `screener_explanation_provider.py` service that implements the `ExplanationProvider` protocol. It composes with `TemplateExplanationProvider` (already used by `delta_explanation_provider.py` via the same pattern) to generate plain-language narratives for screener results. The `stock_screener_service.py` already returns structured results via `format_screening_results()` — the explanation provider wraps these with historian-tone narratives. New YAML file: `src/data/yaml/screener_narratives.yaml` for narrative templates per screening dimension (value, growth, dividend).
- **C152**: Extend `event_interpretation_service.py` (currently single-event) to a new `multi_factor_narrative.py` service that composes events from `adaptive_engine.py` + patterns from `pattern_detector.py` + analogies from `analogy_engine.py` into a single unified narrative. Uses the compose-and-enrich pattern from `timeline_service.py`. The spike already validated the approach — this is implementation.

**Pros**:
- Both features leverage the existing `ExplanationProvider` protocol — clean extension point, no architectural changes needed.
- C167 reuses `stock_screener_service.py` (already built) + `TemplateExplanationProvider` (already used by delta explanations). Minimal new code.
- C152's spike is done — implementation risk is low. The compose-and-enrich pattern from `timeline_service.py` is a proven template.
- Both align with the "historian" positioning and "story first" core value.
- Competitor gap: No TW platform has narrative screener explanations (財報狗 has screening but no narratives). Stocksera has AI narratives but not for screening.

**Cons**:
- C152 depends on `adaptive_engine.py` (622 lines) which is the largest remaining service module. If it needs changes, the module is unwieldy.
- C167's narrative quality depends on template coverage — for a first release, template-based is correct, but may feel generic for edge cases.
- Both features add to the `llm/` package's conceptual surface area without actually adding LLM — the naming may confuse future contributors.

**Dependencies**:
- C167: `stock_screener_service.py` ✅, `TemplateExplanationProvider` ✅, `ExplanationProvider` protocol ✅
- C152: `event_interpretation_service.py` ✅, `adaptive_engine.py` ✅, `pattern_detector.py` ✅, `analogy_engine.py` ✅, `timeline_service.py` pattern ✅

**Risks**:
- **Medium**: C152 scope creep — "multi-factor" could expand beyond sprint scope. Mitigate: strict limit to 3 factors (events + patterns + financial metrics) for Sprint 20.
- **Low**: C167 template coverage — start with 3 screening presets (value, growth, dividend) rather than free-form screening.

**Effort estimate**: C167: 14-18h, C152: 16-20h. Total: 30-38h.

---

### Direction B: "Progressive Disclosure System" — Onboarding & Complexity Management

**Features included**: C163 (Learn First Gate) + C40 (Beginner/Expert Mode Toggle)

**Technical approach**:
- **C40**: Add a new `complexity_service.py` that manages a session_state complexity level (`"beginner"` / `"expert"`). Create a `ComplexityProvider` protocol (similar pattern to `ExplanationProvider`) that sections can query to determine what to render. The `_main.py` orchestrator passes complexity level to each section renderer. Sections already accept `data` dict — adding a `complexity` parameter is a clean extension. Beginner mode hides: detailed financial ratios, debt analysis, institutional investor charts, expert analysis tab. Shows: one-liner, revenue pie, 3-4 key metrics, "Did You Know" facts.
- **C163**: Add a new `onboarding_gate.py` service that checks `session_state["_onboarding_complete"]` before rendering data pages. The gate renders a 3-step interactive walkthrough using existing `lesson_service.py` content. On completion, sets the session_state flag and redirects to the requested stock page. The `lesson_service.py` already loads lesson content from YAML — the gate reuses this with a new `onboarding_lessons.yaml` file.

**Pros**:
- C40 leverages the existing section-based architecture — each section already has a render function. Adding complexity gating is a per-section `if complexity == "beginner": show_simplified()` pattern.
- C163 reuses `lesson_service.py` (207 lines, already built) + academy content infrastructure. The gate is a thin wrapper.
- Both features address the "ten-second test" and "progressive drill-down" design principles directly.
- Competitor gap: No TW platform has a complexity toggle (per Round 8 research). Investopedia has concept-first approach but no interactive gate.
- Low architectural risk — both are additive, neither modifies existing service internals.

**Cons**:
- C40 requires touching every section renderer in `business_card/_sections/` — 8 files need complexity checks. This is mechanical but tedious.
- C163's gate could frustrate returning users who want quick data access. Need a "skip" option and session persistence.
- C40's beginner mode definition is subjective — requires PM/design sign-off on what to hide/show.
- Neither feature generates direct revenue or retention value — they're enablers for user satisfaction.

**Dependencies**:
- C40: `settings_service.py` ✅ (threshold pattern), `_main.py` orchestrator ✅, all section renderers ✅
- C163: `lesson_service.py` ✅, `academy.py` page ✅, session_state infrastructure ✅

**Risks**:
- **Medium**: C40 scope creep — every section needs a "simplified" version. Mitigate: start with 3 sections (summary, financial, health) in Sprint 20, remaining in Sprint 21.
- **Low**: C163 gate friction — returning users annoyed by forced onboarding. Mitigate: session_state persistence + prominent skip button.

**Effort estimate**: C40: 10-14h, C163: 8-12h. Total: 18-26h.

---

### Direction C: "Visual Discovery & Education" — Revenue Tree Enhancement + Glossary Integration

**Features included**: C36 (Visual Revenue Tree — enhancement) + C37 (Key Takeaways — enhancement) + C163 (Learn First Gate — glossary component)

**Technical approach**:
- **C36 enhancement**: The revenue tree already exists as `create_revenue_treemap()` in `chart.py` and `revenue_tree.py` page. Sprint 20 enhancement adds: (1) hierarchical customer-supplier relationships (TSMC → Apple/NVIDIA/AMD) via new `src/data/yaml/revenue_tree_hierarchy.yaml`, (2) interactive drill-down using Plotly's treemap click events, (3) comparison mode showing two companies' revenue trees side-by-side.
- **C37 enhancement**: The key takeaways card already exists. Sprint 20 enhancement adds: (1) dynamic takeaways based on what changed recently (linking to `delta_engine.py`), (2) "why this matter" implication sentences using `TemplateExplanationProvider`, (3) curated takeaways expanded from 20 to 50 stocks via `key_takeaways.yaml`.
- **C163 glossary component**: Add a new `glossary_tooltip.py` service that wraps metric displays with hover-triggered glossary definitions from `glossary.yaml` (already exists). Uses `metric_explainer.py` (86 lines, already built) for the explanation content.

**Pros**:
- All three sub-features enhance existing code rather than building from scratch — low risk.
- C36's hierarchy data is a unique competitive asset (no TW competitor has customer-supplier revenue trees).
- C37's dynamic takeaways + implications directly address the "ten-second test".
- C163's glossary tooltips are reusable across all pages — write once, use everywhere.
- Leverages existing infrastructure: `chart.py`, `delta_engine.py`, `TemplateExplanationProvider`, `glossary.yaml`, `metric_explainer.py`.

**Cons**:
- C36's hierarchical data requires manual curation — doesn't scale beyond top 20-30 stocks. Acceptable for P2.
- C37's "dynamic takeaways" may overlap with C39 (deltas) — need clear positioning: takeaways = "what matters most", deltas = "what changed recently".
- C163 glossary tooltips require Streamlit popover/metric wrapper changes across multiple pages — mechanical work.
- This direction is less architecturally ambitious — it's incremental improvement, not new capability.

**Dependencies**:
- C36: `chart.py` treemap ✅, `revenue_analyzer.py` ✅, `known_revenue.yaml` ✅
- C37: `key_takeaways.py` ✅, `delta_engine.py` ✅, `TemplateExplanationProvider` ✅
- C163: `glossary_service.py` ✅, `metric_explainer.py` ✅, `glossary.yaml` ✅

**Risks**:
- **Low**: All sub-features are enhancements to existing code. Risk is primarily scope management.
- **Medium**: C36 comparison mode could become a feature creep trap. Mitigate: defer comparison mode to Sprint 21.

**Effort estimate**: C36 enhancement: 10-14h, C37 enhancement: 6-8h, C163 glossary: 8-12h. Total: 24-34h.

---

## Recommendation

### Priority Order: **Direction A → Direction B → Direction C**

**Reasoning**:

1. **Direction A first** because:
   - C167 and C152 are the highest-value features with the strongest competitive differentiation. No TW platform has narrative screener explanations or multi-factor event narratives.
   - Both leverage the `ExplanationProvider` protocol — the cleanest architectural extension point in the codebase. This is exactly what the protocol was designed for.
   - C152's spike is already done — the research risk is retired. Implementation is straightforward.
   - C167 reuses the screener infrastructure (already built) + the template composition pattern (already proven by `delta_explanation_provider.py`).
   - These features directly enable the "historian" positioning at scale — not just for individual stocks (C37, C39) but for screening and event analysis.

2. **Direction B second** because:
   - C40 and C163 are foundational UX improvements that make all other features more accessible.
   - They're lower risk than Direction A but provide less competitive differentiation.
   - C40's section-by-section complexity gating is mechanical work that's easy to parallelize across developers.
   - C163's gate reuses the academy infrastructure — it's a thin wrapper, not a new system.
   - These should be built after Direction A to avoid blocking the higher-value narrative features.

3. **Direction C third** because:
   - All three sub-features are enhancements to existing code — they're incremental, not transformative.
   - C36's revenue tree already exists — the enhancement is nice-to-have, not critical.
   - C37's key takeaways already exist — dynamic takeaways are an improvement, not a gap.
   - C163's glossary tooltips are a polish item that can be deferred.
   - If Sprint 20 capacity allows, these are good "filler" features that improve quality without architectural risk.

### Sprint 20 Capacity Planning

Assuming a standard sprint capacity of ~40-50 developer-hours:
- **Direction A only**: 30-38h — fits comfortably, leaves room for bug fixes and debt reduction.
- **Direction A + B**: 48-64h — tight but achievable if C152 spike quality is high and C40 is scoped to 3 sections.
- **Direction A + B + C**: 72-98h — exceeds single-sprint capacity. Direction C should be deferred to Sprint 21.

**Recommended Sprint 20 scope**: Direction A (C167 + C152) + Direction B scoped to C163 only (defer C40 to Sprint 21). Total: 38-50h.

---

## Technical Risks & Mitigations

### Risk 1: C152 Multi-Factor Narrative Complexity
- **Risk**: Composing events + patterns + financial metrics into a single narrative could produce incoherent output if the factors conflict (e.g., positive revenue trend + negative event).
- **Mitigation**: Define a clear narrative priority: financial metrics as context, events as the story driver, patterns as historical perspective. Use the compose-and-enrich pattern from `timeline_service.py` which already handles multi-source merging.

### Risk 2: C167 Screener Performance at Scale
- **Risk**: Screening 1,800 stocks with narrative generation could be slow if not properly batched.
- **Mitigation**: `stock_screener_service.py` already uses `BatchAPI`. The explanation provider operates on the filtered result set (typically 10-50 stocks), not the full universe. Pre-compute screening metrics for the 200 most-traded stocks.

### Risk 3: ExplanationProvider Protocol Extensibility
- **Risk**: Adding `ScreenerExplanationProvider` and potentially `MultiFactorNarrativeProvider` to the same protocol could dilute the protocol's coherence.
- **Mitigation**: Keep the `ExplanationProvider` protocol simple (it already is — just `explain()` and `is_available()`). Each provider implementation is independent. The protocol is a duck-typed contract, not a shared implementation.

### Risk 4: Session State Proliferation (C163 + C40)
- **Risk**: Adding `_onboarding_complete`, `complexity_level`, and related session_state keys adds to the already-growing session state surface.
- **Mitigation**: Consolidate into a single `session_state["_user_prefs"]` dict with keys for onboarding, complexity, and future preferences. This is a D28 (session state audit) item that should be addressed before C163.

### Risk 5: YAML Data Maintenance Burden
- **Risk**: Adding `screener_narratives.yaml`, `revenue_tree_hierarchy.yaml`, and `onboarding_lessons.yaml` adds to the YAML maintenance surface.
- **Mitigation**: All three follow the existing YAML-backed data pattern. The loading/caching pattern from `market_event_service.py` (module-level cache with file-level loading) should be extracted into a shared `yaml_loader.py` utility if more than 2 new YAML services are added.

### Risk 6: business_card Section Interface Consistency
- **Risk**: Adding complexity parameters to section renderers changes the implicit interface contract. All sections currently accept `data` dict and `stock_id` — adding `complexity` is a breaking change to the calling convention.
- **Mitigation**: Use `**kwargs` pattern in section renderers for forward compatibility. The `_main.py` orchestrator passes complexity via `**kwargs`, and sections that don't use it simply ignore it. This is consistent with how `_router_base.py` helpers handle optional parameters.

---

*Created: 2026-06-14*
*Maintainer: System Architect*
*Next review: After Sprint 20 kickoff*
