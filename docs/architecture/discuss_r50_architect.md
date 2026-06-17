# 2026-06-17 Technical Analysis — Discussion Round 50

> **Author**: System Architect
> **Context**: Sprint 24 ✅ C201 COMPLETE + design system cleanup done. 662 tests green. Planning Sprint 25.
> **Architecture Health**: B+ (662 tests passing, all green. i18n cleanup complete. Design system grade C+.)
> **Key Constraint**: All data must come from free FinMind APIs. No paid APIs. Template-based narratives only (no LLM).

---

## 1. Sprint 25 Candidate Feasibility Assessment

### 1.1 C206 — Recurring Investment Education

**Status**: 🟡 FEASIBLE — But Needs Scope Definition

**Context from prior analysis**:
- `docs/research/competitor_research_r46.md`: Robinhood teaches recurring investments as a concept. Finimize's entire product is built around daily 5-minute finance lessons. C206 is listed as P2, 6-8h effort.
- `docs/state/pending_review.md`: C206 scope undefined — needs Daniel decision on what to cover.
- No architecture doc exists for C206.

**What C206 Would Require**:

| Component | Description | Hours |
|-----------|-------------|-------|
| Content creation | Write 1-2 lessons on DCA, compound interest, recurring investment concepts | 3-4 |
| Lesson YAML files | Create `lesson_06.yaml` (and optionally `lesson_07.yaml`) in `config/lessons/` | 1-2 |
| Academy integration | Add lessons to `academy_meta.yaml`, verify rendering in `academy.py` | 0.5 |
| i18n keys | Add ~20-30 new keys under `academy.lesson_06.*` namespace | 1 |
| Testing | Verify lesson rendering, quiz flow, progress tracking | 0.5-1 |
| **Total** | | **6-8.5** |

**Existing Infrastructure** (reduces risk):
- `src/pages/academy.py` (367 lines) — fully functional education academy with lesson rendering, quiz system, progress tracking
- `src/services/lesson_service.py` (207 lines) — lesson loading, caching, quiz checking, progress management
- 5 existing lessons (`lesson_01.yaml` through `lesson_05.yaml`) in `config/lessons/`
- `_info_card()` and `_白话_card()` components for rendering
- `_render_stock_example()` in `academy.py` already supports live data examples (line 40-79)

**Feasibility Verdict**:
- **Technical feasibility**: ✅ High. Pure content addition — no new services, no new APIs, no new components. Follows existing lesson pattern exactly.
- **Content feasibility**: ✅ High. Well-defined topic (DCA, compound interest). Can use C200's "What If" calculator as interactive example.
- **Alignment with historian positioning**: 🟡 Medium. Educational about investing concepts but doesn't directly tell company stories. However, it fills a clear gap — competitor research shows Robinhood/Finimize both cover this.
- **Regulatory risk**: 🟡 Low-Medium. Must include disclaimer: "Educational only, not investment advice." The existing `_historian_disclaimer()` pattern can be reused.

**Open Questions**:
1. **Scope**: Single lesson (DCA concept) or multiple lessons (DCA + compound interest + risk management)? Recommend: single lesson for Sprint 25, expand later.
2. **Interactive element**: Should the lesson include an interactive DCA calculator? The C200 "What If" calculator exists but is not a DCA simulator. A simple DCA visualization (bar chart showing accumulated shares over time) would add 2-3h but significantly improve learning.
3. **Placement**: Add to existing academy, or create a new "投資小知識" card on the daily_market page? Recommend: academy integration (simpler, follows existing pattern).

**Recommendation**: ✅ Include in Sprint 25 as SHOULD. Low risk, fills education gap, leverages existing infrastructure. But scope MUST be defined before implementation starts (pending Daniel decision).

---

### 1.2 C203 — Company Ecosystem Cards v1

**Status**: 🟡 FEASIBLE WITH CONSTRAINTS — Pending Daniel Approval

**Context from prior analysis**:
- `docs/architecture/discuss_r49_architect.md`: Originally 36-50h (supply chain network graph). Redefined as "ecosystem cards" v1 at 12-15h.
- `docs/state/pending_review.md`: Redefined from "Supply Chain Visual Map" to "Company Ecosystem Cards" — card-based layout for top 15-20 stocks using existing `group_structures.yaml` + manually curated data.
- `docs/research/competitor_research_r46.md`: Spiking maps customer-supplier relationships. Simply Wall St has ecosystem visualization.

**Data Source Analysis**:

| Source | Availability | Cost | Coverage |
|--------|-------------|------|----------|
| `group_structures.yaml` | ✅ Exists (112 lines) | Free | 5 parent companies, ~20 subsidiaries |
| `group_structure.py` (page) | ✅ Exists (314 lines) | Free | Already renders group structure |
| Customer-supplier relationships | ❌ Not in existing data | Manual curation | Needed for "ecosystem" |
| FinMind industry chain API | ❌ Paid-only | ❌ Violates constraint | Full TW market |

**What C203 Would Require (Redesigned: Ecosystem Cards v1)**:

| Component | Description | Hours |
|-----------|-------------|-------|
| Data expansion | Expand `group_structures.yaml` from 5 to 15-20 parent companies + add key customer/supplier relationships | 4-6 |
| Service layer | New `src/services/ecosystem_service.py` — loads ecosystem data, enriches with FinMind price data | 3-4 |
| Page module | New `src/pages/ecosystem_cards.py` — card grid layout with stock selector + detail view | 4-5 |
| i18n keys | ~30 new keys under `ecosystem.*` namespace | 1 |
| Testing | Verify card rendering, data loading, edge cases | 1-2 |
| **Total** | | **13-18** |

**Key Design Decisions Needed**:
1. **Data scope**: 15-20 parent companies is ambitious for manual curation. Recommend starting with 8-10 (the 5 existing + 3-5 more from TWSE top 20).
2. **Customer-supplier data**: This is the hardest part. Annual reports have this data but it's labor-intensive. Recommend: for v1, focus on PARENT-SUBSIDIARY relationships (which `group_structures.yaml` already has) and add 2-3 well-known customer-supplier pairs (e.g., Apple→TSMC, NVIDIA→TSMC) as examples. This keeps the feature honest — it's "ecosystem" not "supply chain."
3. **Card layout**: Use existing `_白话_card()` + `_info_card()` components. Each card shows: company name, relationship type (parent/subsidiary/customer/supplier), holding %, revenue contribution, stock price change.

**Feasibility Verdict**:
- **Technical feasibility**: 🟡 Medium. New service + new page, but follows existing patterns exactly. No new visualization types needed (cards only).
- **Data feasibility**: 🟡 Medium. Existing `group_structures.yaml` covers 5 parents. Expanding to 10-15 requires ~4-6h of research (annual reports, TWSE filings). Customer-supplier data is the bottleneck.
- **Alignment with historian positioning**: ✅ High. "Understanding a company's ecosystem" is core to the historian approach — "TSMC matters because NVIDIA/Apple/AMD depend on it."
- **Risk**: 🟡 Medium. Data curation effort is easy to underestimate. Scope creep is the main risk.

**Recommendation**: ✅ Include in Sprint 25 as MUST (if Daniel approves scope). The redefined "ecosystem cards" approach is significantly de-risked vs the original "supply chain map." But Daniel must confirm:
- (A) Approve 10-15 company scope for v1
- (B) Accept parent-subsidiary + limited customer-supplier (not full supply chain)
- (C) Approve 12-15h budget

---

### 1.3 C209 — Collapsible Source Transparency Section

**Status**: ✅ FEASIBLE — Clean Redesign, Low Effort

**Context from prior analysis**:
- `docs/architecture/discuss_r49_architect.md`: Redesigned from "inline citations on every metric" (15-20h) to "collapsible source section per page" (4-6h).
- `docs/state/challenge_r49.md`: Challenger recommends Option A (collapsible source section, 4-6h).
- `docs/state/pending_review.md`: C209 redesign decision pending.

**What C209 Would Require (Redesigned)**:

| Component | Description | Hours |
|-----------|-------------|-------|
| Shared component | New `_render_source_section()` in `_router_base.py` — collapsible section showing data sources | 1.5-2 |
| Per-page integration | Add `_render_source_section()` call to 3-4 key pages (business_card, financial_health, daily_market, group_structure) | 1-1.5 |
| i18n keys | ~15 new keys under `source.*` namespace | 0.5 |
| Data source metadata | Leverage existing `check_data_freshness()` + add source API endpoint info | 0.5-1 |
| Testing | Verify collapsible section renders, verify source info accuracy | 0.5-1 |
| **Total** | | **4-6** |

**Existing Infrastructure** (reduces risk):
- `check_data_freshness()` in `adaptive_engine.py` (line 502) — already computes data freshness per page
- `st.expander()` pattern already used in 15+ places across the codebase (see `_helpers.py` line 100-108, `_health.py` line 117, `_financial.py` line 130/215)
- `_section_title()` in `_router_base.py` — can be reused for the section header
- `_info_card()` — for rendering individual source entries

**Design Approach**:
```
┌─────────────────────────────────────────────────────┐
│  📋 資料來源 (點擊展開)                               │  ← st.expander, collapsed by default
│  ─────────────────────────────────────────────────  │
│  • 股價資料: FinMind taiwan_stock_daily (2026-06-17)│
│  • 財務數據: FinMind taiwan_stock_financial (Q1/2026)│
│  • 集團架構: 年報公開資訊 (2025年報)                  │
│  • 最後更新: 2026-06-17 14:30                       │
└─────────────────────────────────────────────────────┘
```

**Feasibility Verdict**:
- **Technical feasibility**: ✅ High. Additive change — new component in `_router_base.py`, add `st.expander()` to existing pages. No modifications to data layer or service layer.
- **Data feasibility**: ✅ High. All data sources are already known (FinMind API endpoints). Just need to display existing metadata.
- **UI feasibility**: ✅ High. `st.expander()` is a native Streamlit component — no custom CSS, no JavaScript. Collapsed by default = zero clutter.
- **Alignment with historian positioning**: 🟡 Medium. Not core to the historian mission, but adds credibility and transparency. Competitor research shows Spiking provides confidence indicators — this is the transparency equivalent.
- **Risk**: 🟢 Low. Purely additive. If it breaks, it doesn't break existing functionality.

**Recommendation**: ✅ Include in Sprint 25 as SHOULD. Low effort, clean design, no data layer changes. The collapsible approach delivers 80% of the transparency value with 20% of the original effort.

---

## 2. Recommended Sprint 25 Composition

### MUST (Core — Sprint cannot ship without these)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| **C203** Company Ecosystem Cards v1 | 12-15h | Highest value, pending Daniel approval. Aligns with historian positioning. Redesigned scope is de-risked. |
| **Top 5 Design System Fixes** (D-073, D-071, D-084, D-005, D-074) | 1-1.5h | Quick wins that improve global quality. D-073/D-074 affect all pages via shared components. |

**MUST Total**: 13-16.5h

### SHOULD (High value — include if time permits)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| **C209** Collapsible Source Transparency | 4-6h | Low effort, clean, additive. Challenger recommended. |
| **C206** Recurring Investment Education | 6-8h | Fills education gap. Leverages existing academy infrastructure. Needs scope definition. |

**SHOULD Total**: 10-14h

### COULD (Nice to have — defer to Sprint 26)

| Feature | Effort | Rationale |
|---------|--------|-----------|
| D-075 through D-083 (remaining Round 7 fixes) | 2-3h | Individual page fixes, lower priority than top 5 |
| Dark/Light Theme (D-126) | 8-12h | Pending Daniel decision. Large effort for non-core feature. |
| `_infocard` component (D-127) | 6-9h | Pending Daniel decision. New component, needs design. |

### Sprint 25 Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| Week 1 | C203 ecosystem cards implementation | `ecosystem_service.py` + `ecosystem_cards.py` created, data expanded to 10 companies |
| Week 2 | C203 testing + C209 implementation | Ecosystem cards tested, collapsible source section added to 3-4 pages |
| Week 3 | C206 implementation (if scope defined) | New academy lesson on DCA/recurring investment |
| Week 4 | Buffer + design system fixes | Top 5 fixes applied, regression testing |

---

## 3. Design System Fix Priority

### Top 5 Round 7 Fixes — Status Check

| # | Issue | File | Status | Effort | Impact |
|---|-------|------|--------|--------|--------|
| D-073 | `#5D6D7E` → `#7F8C8D` in `_info_card()` | `_router_base.py:150` | 🟡 STILL OPEN | 5 min | **GLOBAL** — affects ALL pages via shared component |
| D-071 | Replace Set3 palette in pie charts | `chart.py:96` | 🟡 STILL OPEN | 30 min | **GLOBAL** — affects all pie charts |
| D-084 | Replace `st.bar_chart` with Plotly | `group_structure.py:283` | 🟡 STILL OPEN | 30 min | Single page, architecture compliance |
| D-005 | Fix `_section_title()` emoji logic | `_router_base.py:129-130` | 🟡 STILL OPEN | 15 min | **GLOBAL** — affects all section titles |
| D-074 | Standardize `#F8F9FA` background | `_router_base.py:138` | 🟡 STILL OPEN | 10 min | **GLOBAL** — affects `_白话_card()` on all pages |

**All 5 top-priority fixes are still open.** None were addressed during Sprint 24 (which focused on C201 + color compliance fixes for D-005, D-059, D-063-D-083).

**Recommended Priority Order**:
1. **D-073** (5 min) — Single line change in `_router_base.py`. Fixes ALL pages. Highest ROI.
2. **D-005** (15 min) — Emoji logic fix. Affects all section titles. Prevents double-emoji issues.
3. **D-074** (10 min) — Background color standardization. Affects all `_白话_card()` instances.
4. **D-071** (30 min) — Chart palette. Affects all pie charts. Improves visual consistency.
5. **D-084** (30 min) — Architecture compliance. Single page but violates layer architecture.

**Total for top 5**: ~1.5 hours. These should be applied at the START of Sprint 25 (or even as a pre-sprint cleanup commit) since they're global fixes that affect all subsequent development.

### Remaining Round 7 Issues (D-075 through D-083)

11 additional issues remain from Round 7. These are page-specific and lower priority:
- D-075, D-076, D-077: `etf_detail.py` color violations (3 issues)
- D-078: `group_structure.py` text color
- D-079: `business_card.py` table border
- D-080: `timeline_controls.py` label color
- D-081, D-082, D-083: `main.py` disclaimer/nav/welcome text colors

These can be batched as a single "design system cleanup" task (2-3h) and done after the top 5.

---

## 4. Architecture Risks and Blockers

### 4.1 Blocking Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **C203 scope not approved by Daniel** | 🔴 High | Medium | Sprint 25 cannot commit to C203 without Daniel's explicit approval of the "ecosystem cards" approach. If not approved, C206 + C209 become MUST. |
| **C206 scope undefined** | 🟡 Medium | High | Without Daniel's decision on C206 content, the team risks building the wrong thing. Recommend: default to single DCA lesson if no response. |
| **C203 data curation underestimated** | 🟡 Medium | Medium | Expanding `group_structures.yaml` from 5 to 10-15 companies requires research. Mitigation: start with 8 companies (existing 5 + 3 more), not 15-20. |

### 4.2 Non-Blocking Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **Design system grade stagnation** | 🟡 Medium | Medium | 92 total issues, only 5 fixed in 7 rounds. The top 5 fixes are trivial (1.5h total) but haven't been prioritized. Risk: grade stays at C+ indefinitely. |
| **Tech debt accumulation** | 🟢 Low | Medium | 3 low-severity issues from Sprint 23 (naming, namespace, dead import) still open. Not blocking but compounding. |
| **FinMind API rate limits (C203)** | 🟢 Low | Low | Ecosystem cards will fetch price data for 10-15 companies. Existing `BatchAPI` + 24h cache should handle this. |
| **i18n key proliferation** | 🟢 Low | Low | C203 (~30 keys) + C209 (~15 keys) + C206 (~25 keys) = ~70 new keys. Manageable with namespacing. |

### 4.3 Architecture Health Assessment

**Overall Health: B+ (Stable, no new critical debt)**

Positive indicators:
- 662 tests passing, all green
- i18n cleanup complete (commit 7bcbc00)
- C201 implementation follows architecture conventions perfectly
- Design system color compliance fixed in shared components (commit 2fc60d3)
- No new `@st.cache_data` violations introduced

Concerns:
- Design system grade C+ (92 issues, only 5 fixed across 7 rounds)
- 3 low-severity naming/namespace issues from Sprint 23 still open
- `group_structure.py` still uses `st.bar_chart` (D-084) — architecture violation
- No new tech debt from Sprint 24 (C201 is clean)

---

## 5. Competitor Features Worth Considering

Based on `docs/research/competitor_research_r46.md`, the following features are relevant to Sprint 25 planning:

### Directly Relevant to Sprint 25 Candidates

| Competitor Feature | Our Candidate | Relevance |
|-------------------|---------------|-----------|
| **Robinhood** recurring investment education | C206 | Direct match — C206 fills this gap |
| **Spiking** supply chain mapping | C203 | Direct match — C203 is our simplified version |
| **Simply Wall St** "Bear vs Bull" visual debate | C199 (shipped) | Already implemented in Sprint 23 |
| **Magnify.money** interactive calculators | C200 (shipped) | Already implemented in Sprint 23 |

### Not Directly in Sprint 25 Scope (But Worth Tracking)

| Feature | Effort | Relevance | Recommendation |
|---------|--------|-----------|----------------|
| **C204** Confidence indicators on AI explanations | 4-6h | Spiking does this. Our analogy engine doesn't indicate confidence. | Sprint 26 candidate |
| **C205** "Read time" indicators | 2-4h | Finimize does this. Low effort, high impact. | Sprint 26 quick win |
| **C202** Story arc timeline labels | 8-10h | StockStory does this. Our C202 is already implemented. | ✅ Already shipped |
| **C186** Daily 5-min finance lesson | 10-14h | Finimize's core product. Different from C206 (which is about recurring investments). | Sprint 26+ |

### Key Insight from Competitor Research

The most impactful finding is that **daily content cadence is the #1 retention pattern** across competitors. C201 (Daily Market Dashboard) addresses this. C206 (Recurring Investment Education) reinforces it by adding a daily educational touchpoint. Together, they create a "daily habit" loop that competitor research shows is critical for beginner engagement.

---

## 6. Total Effort Estimate

### Sprint 25 Effort Summary

| Category | Feature | Effort | Priority |
|----------|---------|--------|----------|
| **MUST** | C203 Company Ecosystem Cards v1 | 12-15h | P1 |
| **MUST** | Top 5 Design System Fixes | 1-1.5h | P1 |
| **SHOULD** | C209 Collapsible Source Transparency | 4-6h | P2 |
| **SHOULD** | C206 Recurring Investment Education | 6-8h | P2 |
| **COULD** | Remaining Round 7 fixes (D-075 to D-083) | 2-3h | P3 |
| **COULD** | Dark/Light Theme (D-126) | 8-12h | P3 (pending Daniel) |
| **COULD** | `_infocard` component (D-127) | 6-9h | P3 (pending Daniel) |

### Scenarios

| Scenario | Features | Total Effort | Risk |
|----------|----------|-------------|------|
| **Conservative** | C203 + top 5 fixes | 13-16.5h | Low |
| **Recommended** | C203 + top 5 fixes + C209 + C206 | 23-30.5h | Medium |
| **Full** | All of above + remaining fixes | 25-33.5h | Medium-High |

**Recommended scenario**: The "Recommended" scenario (23-30.5h) is achievable in a 4-week sprint if:
- C203 scope is approved by Daniel in Week 0 (before sprint starts)
- C206 scope defaults to single DCA lesson if Daniel doesn't respond
- Top 5 fixes are applied in the first 2 days
- C209 is implemented in parallel with C203 testing

---

## 7. Summary

| Feature | Status | Ready? | Effort | Risk | Recommendation |
|---------|--------|--------|--------|------|----------------|
| **C203** Company Ecosystem Cards v1 | Redefined | ⚠️ Pending Daniel | 12-15h | Medium | **MUST** — if Daniel approves scope |
| **C206** Recurring Investment Education | Concept | ⚠️ Needs scope | 6-8h | Low | **SHOULD** — existing infra, low risk |
| **C209** Collapsible Source Transparency | Redesigned | ✅ Ready | 4-6h | Low | **SHOULD** — clean, additive, low effort |
| **Top 5 Design System Fixes** | Identified | ✅ Ready | 1-1.5h | Low | **MUST** — quick wins, global impact |

**Bottom line**: Sprint 25 has a solid candidate set. C203 is the highest-value feature but requires Daniel's scope approval before commitment. C209 and C206 are both low-risk, high-value features that can fill the sprint if C203 is not approved. The top 5 design system fixes are trivial (1.5h total) and should be applied immediately — they've been open for 4+ rounds.

**Critical path**: Daniel's decision on C203 scope → Sprint 25 planning finalization → Implementation.

---

*Created: 2026-06-17 by System Architect*
*References: docs/state/handoff.md, docs/architecture/discuss_r49_architect.md, docs/state/challenge_r49.md, docs/state/pending_review.md, docs/research/competitor_research_r46.md, docs/state/current_problems.md, docs/architecture/c201_daily_market.md*
*Verification: All 662 tests passing. Design system grade C+ (92 issues, 5 fixed). No new tech debt from Sprint 24.*
