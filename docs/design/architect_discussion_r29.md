## 2026-06-13 Technical Analysis — Sprint 14 Feature Candidates

### Current Architecture State

**Architecture Health: 🟢 HEALTHY**
- 32 service modules (`src/services/`), 6 data modules (`src/data/`), 39 page modules (`src/pages/`)
- 0 god modules — no single file exceeds reasonable responsibility scope
- 100% Streamlit-free in service/data layers — all `st.*` calls confined to View layer
- 4-layer architecture (Data → Service → Router → View) consistently enforced
- C36 Revenue Tree V2 complete: `revenue_tree.py` page + `create_revenue_treemap()` in chart service
- C46 Moat Analysis complete: `moat_analyzer.py` service + `_moat.py` section + `moat_data.yaml` (20 TW stocks with 5-dimension scoring + moat type classification from C124)
- C105 Mode Toggle **already implemented** in `_main.py` (line 199-208): `simple_mode` toggle with session_state, `_render_simple_overview()` for beginner mode, full sections hidden behind `if not simple_mode` gate

**Key Architectural Patterns Established:**
- Section-based rendering: Business card uses `_sections.py` sub-modules dispatched from `_main.py`
- Progressive disclosure: Secondary sections in `st.expander()` containers, only shown in detailed mode
- YAML-curated data: `moat_data.yaml` (20 stocks), `glossary.yaml` (99 terms), `company_facts.yaml` — all loaded via service layer
- Session state for UI mode: `st.session_state["simple_mode"]` pattern already proven

---

### Feature Feasibility Analysis

#### C47 Education Academy (Structured Learning Path)
- **Feasibility: 🟡 MEDIUM** — Architecturally straightforward but content-heavy
- **Effort:** 20-30h (40% content creation = 8-12h for lesson writing, 12-18h engineering)
- **Architecture Fit:**
  - New page: `src/pages/education_academy.py` (View layer) — follows existing page pattern
  - New service: `src/services/learning_path.py` (Service layer) — progress tracking, lesson sequencing
  - New data: `src/data/lessons.yaml` (Data layer) — lesson content, prerequisites, stock examples
  - New router entry: Add `"教育學院"` to navbar in `router.py`
  - Progress tracking via `session_state` (existing pattern) or file-based persistence
- **Risks:**
  - **Content creation is 40% of effort** — 10-15 structured lessons with TW stock examples, analogies, and quizzes. This is the bottleneck, not the code.
  - **Scope creep risk:** "Structured learning path" can expand indefinitely. Must cap at 10-15 lessons for Sprint 14.
  - **Progress persistence:** `session_state` is ephemeral (lost on page switch). File-based persistence adds complexity. Recommendation: start with `session_state`-only, add file persistence in a later sprint.
  - **Card-count constraint:** Must respect 5 cards per page section. Lesson cards need compact design.
- **Dependencies:** None hard. Soft dependency on `glossary_service.py` (already built) for term definitions. Soft dependency on `quiz_engine.py` (already built) for lesson quizzes.
- **Verdict:** Feasible for Sprint 14 but should be scoped as **MVP** (5-8 lessons, not 15). Full academy can be phased.

#### C40 Mode Toggle (Simple/Detailed Content Depth)
- **Feasibility: 🟢 ALREADY BUILT** — C105 is the implementation of C40
- **Effort:** 0h (already complete in Sprint 13b)
- **Evidence:** `_main.py` lines 199-208 implement the toggle with `st.session_state["simple_mode"]`. The toggle controls rendering of `_render_simple_overview()` vs full sections. All detailed sections gated behind `if not simple_mode`.
- **Architecture Fit:** Perfect — toggle state in `session_state` (router/view layer), rendering logic in View layer, no service/data layer contamination.
- **Risks:** None. Feature is complete and working.
- **Remaining Work (if any):** 
  - The toggle currently only controls the business card page. If the intent is to propagate "simple mode" to ALL pages (peer comparison, financial health, etc.), that's additional work: ~4-6h to add `simple_mode` checks to other page render functions.
  - Currently defaults to `value=True` (simple mode). This is the right default for beginner positioning.
- **Verdict:** **Already complete.** If Sprint 14 scope includes propagating mode toggle to all pages, budget 4-6h. Otherwise, C40/C105 is done.

#### C123 Revenue Geography (Geographic Revenue Breakdown)
- **Feasibility: 🔴 LOW** — Data availability is the critical blocker
- **Effort:** 8-12h (if data is available)
- **Architecture Fit:**
  - New service: `src/services/revenue_geography.py` — geographic breakdown logic
  - New chart: `create_revenue_geo_chart()` in `chart.py` — choropleth or bar chart
  - New section: Add to `revenue_tree.py` or business card revenue section
  - Data source: **FinMind does NOT have geographic revenue breakdown for TW stocks** (confirmed — no `get_geographic_revenue()` method in `finmind_client.py`, no matching API endpoint)
- **Risks:**
  - **🔴 CRITICAL: No FinMind data source.** TW companies are not required to disclose geographic revenue breakdown in standardized format. Some large caps (TSMC, Foxconn) disclose in annual reports but not in machine-readable format.
  - **Manual curation required:** Would need to create `revenue_geography.yaml` with manually researched data for top 20 stocks. High maintenance burden.
  - **Content creation:** Each geography entry needs plain-language explanation ("65% of TSMC's customers are American companies like Apple and NVIDIA").
  - **Staleness:** Geographic revenue shifts annually; manual data would be outdated quickly.
- **Dependencies:** C36 Revenue Tree (complete) — natural extension but not blocked by it.
- **Verdict:** **DEFER.** Data availability makes this infeasible for Sprint 14. Requires either (a) a new data source API, or (b) significant manual curation effort that doesn't fit Sprint 14's capacity. Revisit when FinMind adds geographic revenue data or when manual curation budget is available.

#### C125 Segment Profitability (Business Segment Margin View)
- **Feasibility: 🟡 MEDIUM** — Data partially available, requires content curation
- **Effort:** 6-10h (engineering) + 4-6h (content curation for segment margin data)
- **Architecture Fit:**
  - Extend `src/services/revenue_analyzer.py` — add `analyze_segment_margin()` function
  - Extend `chart.py` — add margin overlay to existing treemap/sunburst (color-coded segments)
  - Extend `revenue_tree.py` — add "segment margin" tab or toggle
  - New data: `src/data/segment_margins.yaml` — manually curated segment margin data
- **Risks:**
  - **🟡 Data availability:** FinMind's financial statements have segment-level data for SOME companies (via `get_financial_statement()` line items), but it's inconsistent across TW stocks. Large conglomerates (TSMC, Hon Hai) have segment reporting; smaller companies don't.
  - **Content curation:** Need to research and document segment margins for ~20 stocks. This is 40% of the effort (consistent with the 40% content budget rule).
  - **Maintenance:** Segment margins change quarterly; manual YAML needs updates.
  - **Card-count constraint:** Adding margin overlay to existing treemap doesn't add cards, so this is fine.
- **Dependencies:** C36 Revenue Tree (complete) — extends it naturally. C123 (Revenue Geography) is NOT a dependency; segment profitability is about business segments, not geographic segments.
- **Verdict:** **Conditionally feasible** for Sprint 14. Key condition: limit to top 10-15 stocks with available segment data. Don't try to cover all 20 moat_data stocks. Engineering is straightforward (extend existing treemap with color-coded margin overlay).

#### C126 Moat Comparison (Side-by-Side Moat Comparison)
- **Feasibility: 🟢 HIGH** — C46 is complete with comparison-ready data for 20 stocks
- **Effort:** 10-14h
- **Architecture Fit:**
  - New page or tab: Add `"🏰 護城河比較"` tab to existing `peer_comparison.py` (View layer)
  - Reuse `moat_analyzer.py` service — `get_moat_summary()` already returns structured data (moat_type, moat_score, dimensions, evidence)
  - New chart: `create_moat_comparison_chart()` in `chart.py` — radar chart or side-by-side bar chart
  - Data: `moat_data.yaml` already has 20 stocks with scores — **comparison-ready from day one** (this was a Sprint 13b condition per Challenge Log)
- **Risks:**
  - **Low risk.** All data exists. Service layer exists. Just need View-layer rendering.
  - **Content creation:** Need plain-language comparison explanations ("台積電的護城河比聯電寬，因為..."). Budget ~4h for 10-15 comparison pairs.
  - **Card-count:** Side-by-side comparison of 3-5 peers fits within 5-card limit if using compact cards.
  - **Peer selection logic:** Need to determine which peers to show. Can reuse `INDUSTRY_BENCHMARKS` from `peer_comparison.py`.
- **Dependencies:** ✅ C46 complete (Sprint 13b). ✅ `moat_data.yaml` has 20 stocks. ✅ `peer_comparison.py` has industry benchmark mapping.
- **Verdict:** **Highly feasible** for Sprint 14. This is the lowest-risk, highest-value Sprint 14 candidate. All infrastructure is built; it's a View-layer addition.

---

### Proposed Directions

#### Option A: "Education Foundation" Sprint
**Scope:** C47 Education Academy (MVP: 5-8 lessons) + C126 Moat Comparison
- **Pros:**
  - C126 is low-risk, high-value — all data exists, just needs View-layer rendering
  - C47 MVP establishes the education infrastructure (lesson YAML format, progress tracking pattern) for future expansion
  - Combined effort: ~30-40h (C47 MVP: 15-20h + C126: 10-14h + integration: 5h)
  - Aligns with "40% content budget" — C47 lessons are content-first by design
  - Strengthens the "historian + education" positioning that differentiates from all TW competitors
- **Cons:**
  - C47 MVP is still content-heavy (5-8 lessons with TW stock examples, analogies)
  - No geographic/segment revenue features (C123/C125 deferred)
  - Education Academy without C40 mode toggle propagation is incomplete (but C105 already works on business card)
- **Effort:** 30-40h total
- **Risk Level:** Low-Medium (content creation is the main risk)

#### Option B: "Analysis Depth" Sprint
**Scope:** C125 Segment Profitability + C126 Moat Comparison + C40 Mode Toggle Propagation (4-6h)
- **Pros:**
  - All three features are engineering-light, data-ready
  - C125 + C126 together create a powerful "deep analysis" suite: "Here's how the business works (segments) + how strong it is (moat) + how it compares (moat comparison)"
  - C40 propagation completes the mode toggle vision across all pages
  - Combined effort: ~24-30h (C125: 10-16h + C126: 10-14h + C40 propagation: 4-6h)
  - No content-heavy features — all data exists or can be derived
- **Cons:**
  - C125 segment margin data is only available for ~10-15 of the 20 moat stocks
  - No education feature (C47 deferred) — misses the "education-first" positioning opportunity
  - C123 (geographic revenue) remains deferred with no timeline
- **Effort:** 24-30h total
- **Risk Level:** Low (all engineering, minimal content creation)

#### Option C: "Quick Wins + Infrastructure" Sprint
**Scope:** C126 Moat Comparison + C40 Mode Toggle Propagation + C47 Education Academy (Spike: 3-5 lesson prototype)
- **Pros:**
  - C126 delivers immediate user-facing value (comparison is a top competitor gap)
  - C40 propagation completes existing feature
  - C47 spike validates the lesson YAML format and progress tracking pattern without committing to full 15-lesson content creation
  - Most balanced: delivers features + infrastructure for future sprints
  - Combined effort: ~25-32h (C126: 10-14h + C40 propagation: 4-6h + C47 spike: 10-12h)
- **Cons:**
  - C47 spike doesn't deliver a complete feature — may feel incomplete
  - C125 segment profitability deferred (but was always medium feasibility)
  - Requires careful scope management on C47 spike to avoid creeping into full academy
- **Effort:** 25-32h total
- **Risk Level:** Low (all well-understood technical challenges)

---

### Technical Risks and Dependencies Summary

| Risk | Severity | Affected Features | Mitigation |
|------|----------|-------------------|------------|
| No FinMind geographic revenue API | 🔴 High | C123 | Defer. Manual curation not justified for Sprint 14. |
| Segment margin data inconsistent across TW stocks | 🟡 Medium | C125 | Limit to top 10-15 stocks with available data. Use `st.info()` for stocks without data. |
| C47 content creation bottleneck (40% rule) | 🟡 Medium | C47 | Cap at 5-8 lessons MVP. Use existing analogy_engine patterns. |
| C40 mode toggle only on business card | 🟢 Low | C40 | Propagation to other pages is 4-6h of straightforward work. |
| moat_data.yaml coverage (20 stocks) | 🟢 Low | C126 | 20 stocks is sufficient for comparison. More can be added incrementally. |
| Session state loss on page navigation | 🟢 Low | C47, C40 | Acceptable for MVP. File-based persistence can be added later. |

### Recommendation

**Recommend Option C: "Quick Wins + Infrastructure"** with the following Sprint 14 scope:

1. **C126 Moat Comparison** (10-14h) — **INCLUDE.** All infrastructure exists. Lowest risk, highest value. Directly supports "benchmark-oriented analysis" core value. Extends C46 which was just completed.

2. **C40 Mode Toggle Propagation** (4-6h) — **INCLUDE.** Completes the C105 implementation across all pages. Small effort, high polish impact.

3. **C47 Education Academy — Spike/Prototype** (10-12h) — **INCLUDE as MVP.** Build 3-5 lesson prototype with:
   - `src/data/lessons.yaml` with lesson schema (title, difficulty, stock_example, content, quiz_questions)
   - `src/services/learning_path.py` with progress tracking
   - `src/pages/education_academy.py` with lesson viewer
   - Validates the architecture before committing to full 15-lesson content creation

**Defer to Sprint 15+:**
- **C123 Revenue Geography** — Blocked by data availability. Revisit when FinMind adds geographic revenue API or when manual curation budget is available.
- **C125 Segment Profitability** — Feasible but lower priority than education features. Pair with C123 in a future "Revenue Deep Dive" sprint.
- **C47 Full Academy** — After spike validates architecture in Sprint 14.

**Total Sprint 14 Effort: 24-32h** — within normal sprint capacity (50h max), leaving buffer for bug fixes and debt items.

**Rationale:** This direction delivers immediate user value (C126), completes existing work (C40), and establishes education infrastructure (C47 spike) without over-committing on content creation. It balances the "historian + education" positioning with technical pragmatism. The deferred features (C123, C125) are deferred for data availability reasons, not technical complexity reasons — they can be picked up when data sourcing is resolved.
