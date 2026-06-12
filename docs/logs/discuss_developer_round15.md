# Developer Cost Estimates — Discussion Round 15

> **Date**: 2026-06-21
> **Author**: Developer
> **Cycle**: Discussion Round 15
> **Context**: Sprint 4 complete (L0: 65/65, L1: 8/8). Sprint 5 prerequisites (D-039/040/D-041) about to start. This analysis covers the next wave of candidate features for post-Sprint 5 planning.
> **References**: `docs/state/handoff.md`, `docs/state/review_report.md`, `docs/design/developer_estimates_r16.md`, `docs/logs/discuss_architect_round15.md`, `docs/status/issues.md`, `docs/status/tech_debt.md`

---

## 1. Current State Assessment

### Proven Velocity (Sprint 4 Benchmark)
Sprint 4 delivered 5 items (R3, C48, C38, C51, C53-1) plus 3 debt items (D25, D23, D37) in **~35-43h** (planned 43.5h). This is the most reliable estimate baseline we have.

| Metric | Sprint 4 Actual |
|--------|-----------------|
| Items delivered | 5 features + 3 debt |
| Total effort | 35-43h |
| Avg per item | ~5-6h (including debt) |
| Complex items (C38, C51) | 11-14h each |
| Simple items (R3, C53-1) | 1.5-2.5h each |
| L0 verification | 65/65 ✅ |
| L1 verification | 8 pass (10 pre-existing failures) |

### Key Architectural Constraints
1. **Content cap**: 100 items max across all features
2. **D-041 is a hard prerequisite** before Sprint 5 feature coding (prevents D-003 regression)
3. **Streamlit limitations**: No native timeline, no WebSocket, no partial refresh
4. **Service layer pattern**: data → service → presentation (strict separation)
5. **YAML persistence pattern**: Proven for watchlist; must be used for new stateful features
6. **_sections.py emerging monolith**: At 604 lines; D37 split must happen during Sprint 5

---

## 2. Implementation Cost Estimates

### 2.1 Sprint 5 Prerequisites (NOT STARTING — Hard Prerequisites)

| ID | Description | Base Estimate | Risk-Adjusted | Dependencies | Risk Level |
|----|-------------|---------------|---------------|--------------|------------|
| **D-039** | Standardized section header pattern (`_section_header()`) | 1.5h | 1.5-2h | None | Low |
| **D-040** | Standardized disclaimer component (`_historian_disclaimer()`) | 0.5h | 0.5h | None | Very Low |
| **D-041** | Sprint 5 card components (`_study_card()`, `_expert_card()`, `_scenario_card()`) | 1h | 1h | None | Low (but HIGH risk if skipped) |
| **D-037 fix** | Fix 白话 card background color | 0.3h | 0.3h | None | Very Low |
| **Total** | | **3.3h** | **3.3-3.8h** | | |

**Notes**:
- D-039, D-040, D-041 are **sequential** (no parallelism benefit — each is small enough to batch)
- D-039 currently NOT imported in `_sections.py` (designer's finding). Adding import + replacing 8 raw headers is mechanical but error-prone
- D-041 risk: If skipped, forecasted D-003 regression from A to B- (challenger's explicit warning)

### 2.2 Sprint 5 Features (Already Planned: C71 → C74 → C73)

| ID | Description | Base Estimate | Risk-Adjusted | Dependencies | Risk Level |
|----|-------------|---------------|---------------|--------------|------------|
| **C71** | Study Log — YAML-based learning journal | 10h | 8-12h | D-041 (`_study_card`) | Low |
| **C74** | Historical Scenarios — "What would have happened if..." | 13h | 10-16h | D-041 (`_scenario_card`), D-040 (disclaimer) | Medium |
| **C73** | Expert Analysis — Curated expert consensus (10 stocks) | 17h | 14-20h | D-041 (`_expert_card`), D-040 (disclaimer) | High |
| **D-038** | Move C41 API call from view to router layer | 1.5h | 1-2h | None | Low |
| **Total** | | **41.5h** | **36-50h** | | |

**Notes**:
- C73 is the highest-risk Sprint 5 item. Data source for expert consensus is uncertain (FinMind may not have analyst ratings). If data sourcing fails, could add 4-6h for mock data or alternative sourcing
- C74 and C81 data overlap: C74's `historical_scenarios.yaml` could serve as foundation for C81 later
- C74 MVP: static scenario results, not real-time calculations

### 2.3 New Features from Round 16 (C81-C85)

| ID | Title | Base Estimate | Risk-Adjusted | Content Items | Dependencies | Risk Level |
|----|-------|---------------|---------------|---------------|--------------|------------|
| **C83** | Investment Memo Template | 8h | 6-10h | 0 (templates only) | None | Low |
| **C85** | Financial Wellness Check | 10h | 8-12h | 1 (quiz flow) | None | Low-Medium |
| **C84** | Market Event Case Study | 12h | 10-14h | 5-10 (curated studies) | D-040 (disclaimer) | Medium |
| **C82** | Animated Data Story | 14h | 12-20h | 20-50 (depending on scope) | Plotly/JS animation framework | High |
| **C81** | Historical Decision Scenarios | 17h | 14-22h | 50-100 (5-10 scenarios × 10 stocks) | FinMind historical prices | High |
| **Total** | | **61h** | **50-78h** | | | |

#### C83: Investment Memo Template (LOWEST RISK — HIGHEST ROI)
- **Effort**: 8h (6-10h range)
- **Complexity**: Medium — templated form with 5-7 prompts, pre-fill from existing business card data
- **Content burden**: 0 items (templates are code, not content)
- **Files**: `src/pages/memo_page.py` (~150 lines), `src/data/memo_templates.yaml` (~50 lines), `src/services/memo_engine.py` (~80 lines)
- **Risks**: Low. C55 (Investment Diary) partially overlaps; this is the structured version. Pre-fill logic accesses existing services via proven patterns
- **Competitive validation**: 長投學堂 proves demand. Directly extends C55
- **Recommendation**: **First post-Sprint 5 feature.** Lowest effort, zero content burden, proven demand

#### C85: Financial Wellness Check (LOW-MEDIUM RISK)
- **Effort**: 10h (8-12h range)
- **Complexity**: Medium — 10-question quiz with scoring rubric + company recommendation matching
- **Content burden**: 1 item (the quiz flow itself)
- **Legal risk**: Must frame as self-awareness, NOT investment advice. Historian tone QA gate must approve all quiz result language
- **Files**: `src/pages/wellness_check.py` (~200 lines), `src/data/wellness_questions.yaml` (~100 lines), `src/services/wellness_engine.py` (~100 lines)
- **Risks**: Medium. Company recommendation matching logic is basic (filter by risk profile). If recommendation algorithm needs sophistication, +3-5h
- **Competitive validation**: Cleo/Plum/Bloom all proved demand for behavioral finance self-assessment
- **Strategic value**: Enables personalization layer for all other content features. "Historian of self" positioning
- **Recommendation**: Second in C81-C85 sequence. Enables future personalization features

#### C84: Market Event Case Study (MEDIUM RISK)
- **Effort**: 12h (10-14h range)
- **Complexity**: Medium — content-heavy. Code complexity is LOW; content writing is the bottleneck
- **Content burden**: 5-10 curated case studies. Each study: ~200-400 words of historical narrative + current market comparison
- **Files**: `src/data/market_case_studies.yaml` (~400 lines), `src/pages/case_study_page.py` (~200 lines), `src/services/case_engine.py` (~60 lines)
- **Risks**: Medium. "How does this relate to today?" comparison logic needs careful design. Content writing for 5-10 case studies could take 8-10h of PM/Designer time (NOT counted in developer estimate)
- **Competitive gap**: No TW competitor has interactive case studies
- **Recommendation**: Third in sequence. Requires parallel content creation workstream from PM/Designer

#### C82: Animated Data Story (HIGH RISK)
- **Effort**: 14h (12-20h range)
- **Complexity**: High — Streamlit + JavaScript animation is UNTESTED in this codebase
- **Content burden**: 20-50 items depending on scope (each scroll step = content)
- **Files**: `src/pages/data_story.py` (~250 lines), `src/templates/step_card.html`, `static/data_story.js` (NEW — first JS file in project), `chart.py` additions (~100 lines)
- **Risks**: HIGH
  - Streamlit + custom JS animation via `streamlit.components.v1` is unproven here
  - Could require custom component architecture (+6-8h if pure Streamlit approach fails)
  - Content volume grows quickly (each company = 5-10 scroll steps × historical data)
- **Mitigation**: Start with MVP (5 scroll steps, static fade-in images). Full animation as enhancement in separate sprint
- **Competitive gap**: Visual Capitalist proves demand. No TW competitor has animated data stories
- **Recommendation**: Fourth in sequence. MUST start as MVP spike to de-risk JS integration before committing to full build

#### C81: Historical Decision Scenario Explorer (HIGHEST RISK)
- **Effort**: 17h (14-22h range)
- **Complexity**: High — branching logic is NEW for Stock Explorer
- **Content burden**: 50-100 items (5-10 decision points × 10 stocks). This alone could exhaust 50-100% of the content cap
- **Files**: `src/pages/scenario_page.py` (~200 lines), `src/data/historical_scenarios.yaml` (~300 lines), `src/services/scenario_engine.py` (~100 lines)
- **Risks**: HIGH
  - Content creation is massive: 50-100 scenario definitions with branching outcomes
  - Branching logic UX is untested in Streamlit (selectbox navigation works, but multi-step branching is complex)
  - Content cap pressure: 50-100 items is the entire content budget
- **Overlap with C74**: C81 could reuse C74's `historical_scenarios.yaml` data foundation, reducing both effort and content burden to ~30 items
- **Recommendation**: Last in sequence. Build AFTER C74 (shares data) and after C82 MVP de-risks JS/animation patterns

### 2.4 Previously Planned Features (C63, C64 — from Round 14)

| ID | Title | Round 14 Estimate | Revised Estimate | Dependencies | Risk Level |
|----|-------|-------------------|------------------|--------------|------------|
| **C63** | Audio Market Story (weekly) | 18-24h | 18-24h | D28 (audio service layer — NOT built) | High |
| **C64** | Community Q&A | 26-38h | 26-38h | D22 (persistence layer), D29 (community service layer) | High |

#### C63: Audio Market Story (Weekly)
- **Effort**: 18-24h (unchanged from Round 14)
- **Complexity**: High — audio generation requires either TTS API integration or pre-recorded audio file management
- **Content burden**: 52 weekly episodes/year. **WEEKLY ONLY** (challenger ruling: not daily)
- **Blocker dependency**: D28 (audio service layer) is not yet estimated or started
- **Files needed**: `src/services/audio_service.py` (~150 lines), `src/data/audio_scripts.yaml` (~100 lines), `src/pages/audio_story.py` (~200 lines), audio file storage system (S3 or local)
- **Risks**: High — audio infrastructure is entirely new to the codebase. TTS API cost/quality tradeoffs unknown. Audio file hosting (local vs cloud) adds infrastructure complexity
- **Content bottleneck**: Writing 52 audio scripts requires a dedicated content pipeline. Each script: 3-minute narrative (~400-500 words). Total: 20,000-26,000 words/year
- **Recommendation**: Defer to Sprint 8+ (per Round 14 challenger ruling). The content pipeline and D28 infrastructure need to be proven first. The 18-24h code estimate DOES NOT include content creation

#### C64: Community Q&A
- **Effort**: 26-38h (unchanged from Round 14)
- **Complexity**: Highest — this is essentially a forum/chat system. Requires: user-generated content, moderation, threading, voting, notifications
- **Content burden**: Potentially unlimited (user-generated). The 100-item content cap does NOT apply to UGC
- **Blocker dependencies**: D22 (persistence layer, P0), D29 (community service layer)
- **Files needed**: `src/services/community_service.py` (~300 lines), `src/services/persistence.py` (~100 lines), `src/pages/community_qa.py` (~300 lines), `src/data/community_threads.yaml` (grows over time), moderation tools
- **Risks**: Highest of all candidate features
  - User-generated content requires moderation infrastructure (spam, accuracy, tone)
  - Persistence layer (D22) is the critical blocker — YAML pattern works for single user but community content needs either SQLite or a backend service
  - Community features invite regulatory risk (financial advice from users)
  - Thread navigation, voting, and reputation systems add significant complexity
  - If multi-user is required, YAML persistence insufficient — SQLite migration adds 4-6h
- **Recommendation**: Sprint 8+ (per Round 14). D22 persistence layer must be proven before C64 starts. D29 community service layer adds 2-3h. Consider starting with a heavily MVP'd version: read-only curated Q&A (no user posting) to validate the UI before building full community infrastructure

### 2.5 Architecture Debt (D-042/043/D-044)

| ID | Description | Base Estimate | Risk-Adjusted | Dependencies | Risk Level |
|----|-------------|---------------|---------------|--------------|------------|
| **D-042** | Health mini-card non-standard styling → `_mini_score_card()` | 0.5h | 0.5h | None | Very Low |
| **D-043** | Dividend table inline HTML → `st.dataframe` | 1.5h | 1-2h | None | Low |
| **D-044** | C41 Read Next header not using `_section_title()` | 0.3h | 0.3h | D-039 first | Very Low |
| **Total** | | **2.3h** | **1.8-2.8h** | | |

**Notes**:
- D-042 and D-043 can be done **anytime** (no dependencies, pure cleanup)
- D-044 is blocked on D-039 (sequential dependency)
- D-043 has upside: `st.dataframe` provides sorting and filtering "for free" — UX improvement beyond debt cleanup

---

## 3. Risk Analysis Summary

### Critical Risks (Could Impact Estimates By >20%)

| Risk | Affected Items | Impact | Likelihood | Mitigation |
|------|---------------|--------|------------|------------|
| **C73 Expert Analysis data source** | C73 | If FinMind lacks analyst data, +4-6h for data sourcing/mock data | Medium | Spike FinMind API first; fallback to mock data + `_historian_disclaimer()` |
| **C82 JS animation integration** | C82 | Custom JS component could add +6-8h | High | Start with MVP (static fade-in), defer full animation |
| **C63 audio infrastructure** | C63 | TTS API cost/quality unknown; file hosting adds complexity | High | D28 spike first; defer to Sprint 8+ |
| **C64 persistence architecture** | C64 | YAML insufficient for multi-user; SQLite migration +4-6h | Medium-High | D22 P0 first; MVP as read-only curated Q&A |
| **C81 content cap exhaustion** | C81 | 50-100 items could exhaust entire content budget | High | Build after C74 (shares data); scope to 20 items max |

### Medium Risks (Could Impact Estimates By 10-20%)

| Risk | Affected Items | Impact | Likelihood | Mitigation |
|------|---------------|--------|------------|------------|
| **C74 scenario data quality** | C74, C81 | Some stocks may have incomplete historical data | Medium | Graceful degradation (+1-2h) |
| **C85 legal positioning** | C85 | "Wellness check" could drift into financial advice framing | Medium | Historian tone QA gate must approve all quiz language |
| **C63 content pipeline** | C63 | 52 scripts/year is unsustainable without dedicated content process | High | Start with 12 scripts (quarterly) before committing to 52 |
| **Context switching** | All | Developer doing code + designer doing content in parallel creates sync overhead | Medium | 0.5-1h buffer per feature for PM/Designer coordination |

### Low Risks (Minimal Impact)

| Risk | Affected Items | Mitigation |
|------|---------------|------------|
| D-039 section header edge cases | D-039 | Test each replacement visually |
| D-043 dataframe migration | D-043 | Option to keep HTML with fixed border color if dataframe approach is complex |
| C83 overlap with C55 (Diary) | C83 | Position as "structured diary" — complementary, not duplicate |

---

## 4. Sequencing Recommendations

### Parallel vs Sequential Analysis

#### Sprint 5 Prerequisites (Must Be Sequential)
```
D-037 fix (0.3h) → D-039 (1.5h) → D-040 (0.5h) → D-041 (1h) → Sprint 5 features begin
```
Total: **~3.3-3.8h**. These MUST complete before Sprint 5 feature coding begins. D-044 also waits for D-039.

#### Sprint 5 Features (Sequential with Internal Parallelism)
```
C71 (Study Log) — can start immediately after D-41
C74 (Historical Scenarios) — depends on D-41 + D-40
C73 (Expert Analysis) — depends on D-41 + D-40 + should follow C74 for learning
D-038 fix — can run in parallel with any Sprint 5 feature (no dependencies)
```
**C71 → C74 → C73** is the recommended sequence (matches Round 16 review). D-038 can be done anytime.

#### Post-Sprint 5 (Sprint 6+): Parallel Two-Track Approach

**Track A — Content-Light Features (RECOMMENDED PRIMARY):**
```
Sprint 6: C83 (Investment Memo, 8h) → C85 (Wellness Check, 10h)
Sprint 7: C84 (Case Studies, 12h) [with parallel content creation]
Sprint 8: C63 (Audio Story, 18-24h) [D28 spike first]
```

**Track B — Architecture Debt + De-risk Spikes (Parallel):**
```
Sprint 6: D-042 (0.5h) + D-043 (1.5h) + D-044 (0.3h)  [batch, ~2.3h total]
Sprint 7: C82 MVP spike (5-6h to de-risk JS animation)
Sprint 8: D28 audio spike (3-4h) before C63 build
```

**Track C — Complex Features (Deferred):**
```
Sprint 9+: C81 (17h) — after C74 data proven, C82 animation de-risked
Sprint 9+: C64 (26-38h) — after D22 + D29 infrastructure proven
Sprint 10+: C63 full build — if audio infrastructure and content pipeline ready
```

### What Can Be Parallelized

| Parallel Opportunity | Items | Constraint |
|---------------------|-------|------------|
| Debt cleanup during Sprint 5 | D-038 fix alongside C71/C74/C73 | No dependency conflicts |
| Design system updates alongside coding | Mini Score Card spec, Story Card spec | Designer capacity |
| Content creation alongside coding | C84 case study writing, C63 script templates | PM/Designer capacity |
| D-042/D-043/D-044 batch | All three debt items | D-044 waits for D-039 |
| C82 MVP spike alongside C83 | Spike vs feature | Different files, no conflict |

### What MUST Be Sequential

| Sequence | Reason |
|----------|--------|
| D-041 → C71/C74/C73 | Card components needed before feature coding |
| D-039 → D-044 | `_section_title()` must exist before use |
| D-039 → C73/C74 sections | `_section_title()` should be used in new Sprint 5 sections |
| C74 → C81 | C81 shares C74's `historical_scenarios.yaml` data |
| D22 → C64 | Persistence layer is a hard blocker |
| C82 MVP → C82 full | De-risk JS before committing to full build |

---

## 5. Total Effort Estimates by Sprint

### Sprint 5 (Current — Prerequisites + Features)

| Category | Items | Low Estimate | High Estimate |
|----------|-------|-------------|---------------|
| Prerequisites | D-037, D-039, D-040, D-041 | 3.3h | 3.8h |
| Features | C71, C74, C73 | 40h | 50h |
| Alongside debt | D-038 | 1.5h | 2h |
| **Sprint 5 Total** | | **44.8h** | **55.8h** |

**Likely outcome**: 44.8h (within 1.1 dev-weeks at ~40h/week). Matches existing Sprint 5 plan.

### Sprint 6 (Post-Sprint 5 Primary)

| Category | Items | Low Estimate | High Estimate |
|----------|-------|-------------|---------------|
| New features | C83, C85 | 18h | 22h |
| Debt cleanup | D-042, D-043, D-044 | 2.3h | 2.8h |
| L0/L1 verification | Per feature | 2h | 3h |
| **Sprint 6 Total** | | **22.3h** | **27.8h** |

**Notes**: Lowest-effort sprint. Good opportunity to build momentum after Sprint 5's complexity. C83 and C85 are both standalone pages that don't touch `_sections.py` — no coupling risk.

### Sprint 7 (Medium Complexity)

| Category | Items | Low Estimate | High Estimate |
|----------|-------|-------------|---------------|
| New features | C84 (Case Studies) | 12h | 14h |
| C82 MVP spike | JS animation de-risk | 5h | 8h |
| L0/L1 verification | Per feature | 2h | 3h |
| **Sprint 7 Total** | | **19h** | **25h** |

**Notes**: C84 requires parallel content creation (5-10 case studies). C82 MVP spike determines whether full animation Sprint is viable.

### Sprint 8 (Infrastructure Heavy)

| Category | Items | Low Estimate | High Estimate |
|----------|-------|-------------|---------------|
| D28 spike | Audio service layer | 3h | 4h |
| C63 feature | Audio Market Story | 18h | 24h |
| L0/L1 verification | Per feature | 2h | 3h |
| **Sprint 8 Total** | | **23h** | **31h** |

**Notes**: C63 is the highest-risk Sprint 8 item. The D28 spike must succeed first. If audio infrastructure proves unfeasible, this slot can be filled with C81 or C45 (Valuation Band Enhancement) as fallback.

### Sprint 9+ (Complex Features)

| Category | Items | Low Estimate | High Estimate |
|----------|-------|-------------|---------------|
| C81 | Historical Decision Scenarios | 14h | 22h |
| C64 | Community Q&A | 26h | 38h |
| L0/L1 verification | Per feature | 3h | 5h |
| **Sprint 9+ Total** | | **43h** | **65h** |

**Notes**: These are the two most complex features. C81 should follow C74 (data sharing). C64 should follow D22 + D29 (infrastructure). Both may need to be split across multiple sprints.

### Grand Summary

| Sprint | Items | Low Estimate | High Estimate | Confidence |
|--------|-------|-------------|---------------|------------|
| Sprint 5 | C71, C74, C73 + prereqs | 44.8h | 55.8h | High (±15%) |
| Sprint 6 | C83, C85 + debt cleanup | 22.3h | 27.8h | High (±10%) |
| Sprint 7 | C84 + C82 spike | 19h | 25h | Medium (±20%) |
| Sprint 8 | C63 + D28 spike | 23h | 31h | Medium (±25%) |
| Sprint 9+ | C81, C64 | 43h | 65h | Low (±30%) |
| **Grand Total** | | **152.1h** | **205.4h** | Medium (±20%) |

---

## 6. Developer Recommendation

### Primary Recommendation: "Quick Wins + Infrastructure Spikes"

I recommend the team adopt a **two-track approach** for post-Sprint 5 development:

**Track A: Deliver Value Quickly (Sprints 6-7)**
1. **C83 (Investment Memo Template)** — Sprint 6, first item. 8h effort, standalone page, extends C55 directly, zero content burden, zero dependencies. Highest ROI per hour invested.
2. **C85 (Financial Wellness Check)** — Sprint 6, second item. 10h effort, standalone page, enables future personalization pipeline, only 1 content item.
3. **C84 (Market Event Case Studies)** — Sprint 7. 12h code effort + content creation. Unique "historian" differentiator. No TW competitor has this.

**Track B: De-Risk Complex Features (Spikes, Sprints 7-8)**
4. **C82 MVP spike** — Sprint 7, 5-8h. Determine if Streamlit can handle animated data stories before committing to 14-20h full build.
5. **D28 audio spike** — Sprint 8, 3-4h. Determine if audio infrastructure is feasible before committing to C63's 18-24h build.

### Defer To Sprint 9+ (After Infrastructure Proven)
- **C64 (Community Q&A)**: Wait for D22 persistence + D29 community service layer. Start with read-only curated Q&A MVP to validate UI
- **C81 (Historical Decision Scenarios)**: Wait for C74 to prove scenario data patterns. Share C74's `historical_scenarios.yaml`. Scope to 20 items max to protect content cap.
- **C63 (Audio)**: Only build if D28 spike succeeds AND content pipeline for 52 scripts is sustainable (start with 12/quarter)

### Why This Order?

1. **C83 and C85 are forced wins**: No dependencies, minimal risk, standalone pages, zero conflict with existing code. They demonstrate progress while building reusable page infrastructure.

2. **De-risk before committing**: C82 (JS animation) and C63 (audio) both have unproven infrastructure. Spikes in Sprint 7-8 protect against 20-40h investments in unfeasible directions.

3. **C84 before C63/C64**: Case studies are content-heavy but code-light. Building them teaches the team the content pipeline process before committing to audio (52 scripts/year) or community (unlimited UGC).

4. **D-042/043/044 batch in Sprint 6**: 2.3h of pure cleanup with no dependencies. Quick win that maintains design grade.

5. **Content cap discipline**: C83 adds 0, C85 adds 1, C84 adds 5-10 = 6-11 items through Sprint 7. This leaves 89-94 items for C82, C81, C63, C64 (content-heavy features that need careful budgeting).

### Key Conditions for Challenger Review

1. **D-041 before Sprint 5 feature coding** ✅ (already mandated)
2. **Content cap budget must be tracked** — PM should maintain a content item ledger. Each feature's content items must be counted before implementation begins
3. **D22 persistence layer is P0 for any multi-user feature** — C64 cannot start without D22 proven
4. **Spikes before full builds for C82 and C63** — Don't commit full estimates until spike results are in
5. **Historian tone QA gate for C85 and C84** — both features risk drifting into advice territory; all output language must pass QA gate before shipping

---

*Created: 2026-06-21*
*Developer estimates for Discussion Round 15 cycle.*
*Sprint 4 complete (L0: 65/65, L1: 8/8). Sprint 5 prerequisites (D-039/040/D-041) about to start.*
*Next cycle: Sprint 5 execution (prerequisites first, then C71 → C74 → C73).*
