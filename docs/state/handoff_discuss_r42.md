# Handoff – Discussion Round 42 (2026-06-14)

## Summary
- **Topic**: Discussion (💡) — Sprint 21 Planning: C152 Multi-Factor Event Narratives + C170 Tappable Glossary + D-120 Benchmark Extraction
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger
- **Sprint Status**: Sprint 20 🔧 IN PROGRESS (C167 ✅ done, C163 + C40 pending) → Sprint 21 📋 PLANNED

---

## Key Discovery: All 3 Roles Converge on Option A (P1 Focus)

The Architect, Designer, and Developer independently recommended the same core Sprint 21 plan:

| Role | Primary Recommendation | Stretch Goal | Key Risk Flagged |
|------|----------------------|--------------|------------------|
| **Architect** | C152 (NarrativeExplanationProvider) + D-120 + D-16 | C170 Tappable Glossary | C152 scope creep, analogy_engine.py god module |
| **Designer** | C170 (highest impact/effort) + C152 (highest absolute impact) | C171 Valuation Band | D-003 regression, C152 advice-perception risk |
| **Developer** | D-120 + C170 + C152 = 27.5-38.5h | C171 Valuation Band | C152 scope creep (#1), C163/C40 carry-over |

---

## Idea Proposals

| Idea ID | Description | Proposed By | Status |
|---------|-------------|-------------|--------|
| DIR-1 | C152 Multi-Factor Event Narratives — "One Story, All Factors" | Architect + Developer + Designer | ✅ Sprint 21 centerpiece |
| DIR-2 | C170 Tappable Glossary — Inline metric definitions | Architect + Designer + Developer | ✅ Sprint 21, content starts NOW |
| DIR-3 | D-120 Benchmark Extraction — Pre-Sprint 21 prerequisite | Architect + Developer | ✅ Pre-Sprint 21 infrastructure |
| DIR-4 | C172 Concept Comparison — Stretch goal (replaces C171) | Challenger | ✅ Stretch (post-challenge revision) |

---

## Decisions Made

### Sprint 21 Final Plan (Post-Challenge)

| Order | Task | Estimate | Type |
|-------|------|----------|------|
| 0 | **D-120**: Benchmark extraction (pre-Sprint 21) | 1.5-2.5h | Infrastructure prerequisite |
| 1 | **C170**: Tappable Glossary | 8-12h | Feature (content creation starts NOW) |
| 2 | **C152**: Multi-Factor Event Narratives | 18-24h | Feature (max 8 templates, pre-audited) |
| 3 | **C172**: Concept Comparison Tool (stretch) | 12-16h | Feature (stretch) |
| | **Total (with D-120)** | **39.5-54.5h** | |
| | **Total (D-120 pre-req)** | **38-52h** | Fits 30-42h at lower bound |

### 8 Challenger Conditions (Binding)

1. **C152 template cap**: Maximum 8 multi-factor narrative templates. All 8 must be pre-written and tone-audited BEFORE coding begins. If templates aren't ready, scope reduces to 5 templates (12-15h).
2. **C170 before C152**: C170 must be completed before C152 implementation begins. C170 content creation (50-80 glossary entries) starts NOW as a parallel workstream during Sprint 20.
3. **D-120 as prerequisite**: D-120 must be completed as a pre-Sprint 21 infrastructure task, not consuming Sprint 21 feature capacity.
4. **Sprint 20 cut-line rule**: Before Sprint 21 begins, define explicit Sprint 20 exit criteria for C163 and C40. If either carries over, it displaces the lowest-priority Sprint 21 item (C172 stretch first, then C170). C152 is non-negotiable.
5. **C172 replaces C171 as stretch**: C172 (Concept Comparison) replaces C171 (Valuation Band Chart) as the stretch goal. C172 has higher educational value and better serves the historian positioning.
6. **Historian synthesis boundary document**: Before C152 implementation, write a document defining: past-tense only, "同時發生" framing (not "因為...所以..."), mandatory disclaimer, tone QA pre-audit requirement.
7. **Ten-second test audit**: Conduct a ten-second test audit of the event dashboard BEFORE C152 implementation. If users can't restate individual event explanations in 10 seconds, fix the foundation first.
8. **Sprint 21 success criteria**: Define minimum/target/stretch success criteria before development begins.

### Key Architectural Decisions

- **C152 extends ExplanationProvider protocol**: New `NarrativeExplanationProvider` composes existing providers (DeltaExplanationProvider, TemplateExplanationProvider, EventNarrativeProvider). Uses same `ExplanationRequest`/`ExplanationResponse` protocol.
- **C170 reuses _glossary_tooltip()**: The popover pattern from C139 is already production-ready in `_router_base.py`. C170 is primarily content creation + systematic application.
- **D-120 extracts to YAML**: `INDUSTRY_BENCHMARKS` dict triplicated across 3 files → `src/data/industry_benchmarks.yaml` + `health_scoring.get_benchmark_scores()` service.
- **C172 reuses C170 glossary data**: Concept Comparison Tool uses the same glossary YAML + service as C170.

### Competitor Intelligence (Round 9)

- **StockStory** (HIGH threat): AI-generated company narratives → C152 is the direct counter
- **Stockopedia AI** (HIGH threat): StockRank combines multiple factors → C152's multi-factor narrative is the historian-aligned response
- **財報狗**: Screener is #1 feature, P/E band chart is most popular → C171/C172 address this but deferred
- **Simply Wall St**: Visual synthesis (snowflake) → C152 provides equivalent for events
- **No TW competitor** combines narrative + plain-language + visual-first → "historian" positioning remains white space

---

## Action Items

| Item ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| R42-DISC1 | Write C170 glossary content (50-80 entries) — start NOW during Sprint 20 | PM + Designer | 🔴 Parallel with Sprint 20 |
| R42-DISC2 | Write C152 multi-factor narrative templates (8 max) — before Sprint 21 Day 1 | PM + Designer | 🔴 Before Sprint 21 |
| R42-DISC3 | Write "historian synthesis boundary" document | PM + Designer | 🔴 Before C152 coding |
| R42-DISC4 | Conduct ten-second test audit of event dashboard | Designer + QA | 🔴 Before C152 coding |
| R42-DEV1 | Complete D-120 (benchmark extraction) as pre-Sprint 21 task | Developer | 🔴 Pre-Sprint 21 |
| R42-DEV2 | Implement C170 Tappable Glossary | Developer | 🔴 Sprint 21 |
| R42-DEV3 | Implement C152 Multi-Factor Event Narratives | Developer | 🔴 Sprint 21 |
| R42-DEV4 | Implement C172 Concept Comparison (stretch) | Developer | 🟡 Sprint 21 stretch |
| R42-QA1 | Define Sprint 20 exit criteria for C163/C40 | QA + PM | 🔴 Before Sprint 21 |
| R42-QA2 | Define Sprint 21 success criteria (min/target/stretch) | QA + PM | 🔴 Before Sprint 21 |

---

## Feature Pipeline (Updated)

| Sprint | Features | Effort | Status |
|--------|----------|--------|--------|
| Sprint 20 | C167+C163+C40 (+ C152 swap condition) | 30-42h | 🔧 IN PROGRESS (1/3 done) |
| Sprint 21 | D-120(pre) + C170 + C152 + C172(stretch) | 38-52h (D-120 pre) | 📋 Planned |
| Sprint 22 | C171 + C174 spike + enhancements | TBD | 🔮 Future |

---

## Next Cycle
🔧 Development Round 43: Continue Sprint 20 with C163 Learn First Gate (10-14h), then C40 Beginner/Expert Mode Toggle (8-12h). D-120 benchmark extraction should be completed as pre-Sprint 21 infrastructure before Sprint 21 begins.
