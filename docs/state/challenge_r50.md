# Challenge – Round 50 (Sprint 25 Planning)

**Date**: 2026-06-17
**Author**: Challenger (Round 50)
**Sprint**: Sprint 25 — Planning
**Context**: Sprint 24 ✅ C201 COMPLETE + design system cleanup done. 662 tests green. Planning Sprint 25 with candidates C206, C203, C209.

---

## Executive Verdict

**⚠️ CONDITIONAL** — The candidate set for Sprint 25 is individually feasible, but the Challenger identifies **4 systemic risks** that collectively make this sprint plan premature without explicit Daniel decisions:

1. **Two features are pending Daniel approval with no fallback** — C203 (scope) and C206 (scope). If Daniel doesn't respond, the sprint has no MUST features.
2. **The 92-issue design debt is being ignored again** — only 5 of 92 issues fixed across 7 rounds. The top 5 are trivial (1.5h total) and global.
3. **Layer 1-3 infrastructure problems are unaddressed** — API abuse, race conditions, and cache design are accumulating under new features.
4. **The 3 low-severity tech debt items from Sprint 23 are now 2 sprints old** — they should not cross into Sprint 25.

---

## Part 1: Round 49 Blocking Questions — Status Check

| # | Question (from challenge_r49 Q1-Q5) | Status | Evidence |
|---|--------------------------------------|--------|----------|
| Q1 | When will C201 implementation start? | ✅ RESOLVED | C201 implemented and committed (`ad5b46c`). 662 tests green. |
| Q2 | Resolve C201 open questions (TAIEX, volume, events) | ✅ RESOLVED | All 3 resolved in Round 49 discussion. Used avg change proxy, absolute volume, event type filtering. |
| Q3 | C203 data source — where does customer-supplier data come from? | ⚠️ PARTIALLY | Redefined as "Ecosystem Cards" using existing `group_structures.yaml`. But Daniel has NOT approved the redefined approach. Still listed as "pending_review". |
| Q4 | C209 redesign decision (A/B/C) | ✅ RESOLVED | Round 49 chose Option A: collapsible source section, 4-6h. Architect and Challenger both recommend this. |
| Q5 | C203 scope — is team prepared for 36-50h or should 12-15h v1 be target? | ⚠️ PARTIALLY | Redefined to 12-15h "ecosystem cards" v1. But Daniel hasn't approved. |

### Recommended Non-Blocking Questions (from R49)

| # | Question | Status | Evidence |
|---|----------|--------|----------|
| Q6 | Rename `validate_debate_text()` | ❌ NOT DONE | Still named `validate_debate_text()` after 2 sprints |
| Q7 | Move timeline strings to `timeline:` namespace | ❌ NOT DONE | Still in `scenario:` namespace after 2 sprints |
| Q8 | Remove dead `calculate_scenario` import | ❌ NOT DONE | Still present after 2 sprints |
| Q9 | Add C201 i18n keys during implementation | ✅ DONE | Keys were added as part of C201 implementation |

---

## Part 2: Cross-Examination of Sprint 25 Candidates

### 2.1 C203 — Company Ecosystem Cards v1 (12-15h, MUST, pending Daniel)

**Architect's Position**: Feasible with constraints. Reuse `_subsidiary_card()`. Expand `group_structures.yaml` from 5 to 10-15 companies.

**Designer's Position**: `_subsidiary_card()` is the correct primary component. No new component needed. Card-based approach is fully PPT-compliant.

**Challenger's Cross-Examination**:

**🔴 BLOCKING: Data source problem has NOT been solved — only renamed.**

The original C203 was killed because:
- FinMind's supply chain API is paid-only
- True customer-supplier data requires 2-4h per stock manual curation
- Network visualization was new territory

The redefined C203 claims to solve this by:
- Using existing `group_structures.yaml` (5 parent companies, ~20 subsidiaries)
- Adding "2-3 well-known customer-supplier pairs (e.g., Apple→TSMC, NVIDIA→TSMC)"
- Card layout instead of network graph

**The Challenger's problem**: `group_structures.yaml` has **parent-subsidiary** data, NOT customer-supplier data. These are fundamentally different relationships. The redefined feature is actually a "Group Structure Browser" — which already exists as `group_structure.py` (314 lines). 

**❓ Challenger Question 1**: Is C203 actually a new feature, or is it a rebrand of the existing group_structure.py page with slightly different cards? If the existing page already shows parent-subsidiary relationships, what exactly is new?

**❓ Challenger Question 2**: The architect says "add 2-3 well-known customer-supplier pairs." Where does this data come from? Annual reports? How is this different from the manual curation problem that killed the original C203? If we're only adding 2-3 pairs, the feature is 90% "show existing group data in new cards" — is that worth 12-15h?

**❓ Challenger Question 3**: The designer says "no new component needed" because `_subsidiary_card()` already exists. If no new component is needed and the data already exists, why is this 12-15h? The architect's own breakdown shows 4-6h for data expansion + 3-4h for service layer + 4-5h for page module = 13-18h. But if the data and components already exist, shouldn't this be closer to 6-8h?

**Risk Assessment**: 🟡 MEDIUM — The feature is feasible but the value proposition is unclear. It may be a marginal improvement over the existing group_structure.py page. The 12-15h estimate may be inflated by data curation that isn't clearly scoped.

---

### 2.2 C206 — Recurring Investment Education (6-8h, SHOULD, no architecture doc)

**Architect's Position**: Feasible. Pure content addition using existing academy infrastructure. Single DCA lesson recommended.

**Designer's Position**: Strong alignment with "historian, not stock picker" — it's educational, not advisory. Uses existing `_lesson_card()`, `_progress_dots()`, `_白话_card()`.

**Challenger's Cross-Examination**:

**🟡 CONCERN: "Investment education" vs "investment advice" boundary is thin.**

The designer correctly identifies the risk: "Must NOT include any calculator or 'try it' tool — that crosses into advisory." And "Chart in Card 2 must use hypothetical/fictional data only — NO real stock examples with real returns."

But the architect says: "Can use C200's 'What If' calculator as interactive example."

**❓ Challenger Question 4**: These two positions are contradictory. The designer says NO real stock examples and NO calculator. The architect says use the existing calculator. Which is it? If C206 uses the C200 calculator with real stock data, it becomes a "try it" tool — which the designer explicitly says crosses into advisory territory.

**❓ Challenger Question 5**: C206 has no architecture doc. It's been "pending Daniel" since Sprint 24 planning. It was listed as Sprint 24 Week 4 stretch and didn't happen. Now it's Sprint 25 SHOULD. How many sprints will it be carried forward before either building it or killing it?

**Risk Assessment**: 🟡 MEDIUM — The feature itself is low-risk (pure content), but the scope ambiguity between "education" and "advice" is a real regulatory concern. The existing `_historian_disclaimer()` pattern helps but doesn't eliminate the risk. **Recommendation**: Default to single DCA lesson with hypothetical data only. No calculator integration. No real stock examples. If Daniel wants more, that's a separate sprint.

---

### 2.3 C209 — Collapsible Source Transparency Section (4-6h, SHOULD, redesigned)

**Architect's Position**: Feasible. Additive change. New `_render_source_section()` in `_router_base.py`. Apply to 3-4 key pages.

**Designer's Position**: Strong fit. Progressive disclosure is a core UI pattern. Create `_source_section()` component. Apply to business_card, daily_market, event dashboard first.

**Challenger's Cross-Examination**:

**✅ C209 is the cleanest candidate.** It's additive, low-risk, well-scoped, and both architect and designer agree on the approach.

**🟡 CONCERN: 4-6h estimate may be optimistic for "modify multiple page files."**

The architect estimates:
- 1.5-2h for shared component
- 1-1.5h for per-page integration (3-4 pages)
- 0.5h for i18n keys
- 0.5-1h for data source metadata
- 0.5-1h for testing

**❓ Challenger Question 6**: The designer identifies 4 placement priorities (business_card, daily_market, event dashboard, all other pages). If "all other pages" means 8-10 additional pages, the 1-1.5h per-page estimate is unrealistic. Each page needs: understanding the data sources, formatting the source dict, testing the expander. For 12 pages total, this is closer to 4-5h for integration alone, making the total 7-9h.

**❓ Challenger Question 7**: The designer's spec for `_source_section()` takes a `list[dict]` parameter. But different pages have different data sources. Business card uses price + financial + news + group data. Daily market uses sector grid + batch summaries. Who creates the source dict for each page? Is this the implementer's responsibility (adding time) or does the service layer already track this (saving time)?

**Risk Assessment**: 🟢 LOW — The feature is sound. The estimate may be slightly optimistic but even at 7-9h it's the lowest-risk candidate. **Recommendation**: Cap at 3 pages for v1 (business_card, daily_market, event dashboard). Defer remaining pages to Sprint 26.

---

## Part 3: Layer 1-3 Problems — Should They Take Priority?

From `current_problems.md`:

### Layer 1: Data Flow & Architecture

| # | Problem | Severity | Sprint 25 Impact |
|---|---------|----------|-------------------|
| 1 | **API Abuse in `get_stock_info`** — fetches entire stock list per stock_id, 50 stocks = 50 API calls | 🔴 HIGH | C203 ecosystem cards will fetch price data for 10-15 companies. This directly triggers the API abuse problem. |
| 2 | **Daily cache invalidation** — cache key changes every day, TTL useless, old files never deleted | 🟡 MEDIUM | Affects all features equally. Not new in Sprint 25. |
| 3 | **No Chinese name search** — stock search only matches stock_id | 🟡 MEDIUM | Not directly related to Sprint 25 candidates. |

### Layer 2: Business Logic & UI/UX

| # | Problem | Severity | Sprint 25 Impact |
|---|---------|----------|-------------------|
| 4 | **DuplicateWidgetID crash** in event_dashboard | 🔴 CRITICAL | C209 will add components to event_dashboard. Risk of triggering this. |
| 5 | **ETF misclassification** in watchlist | 🟡 MEDIUM | Not directly related to Sprint 25. |
| 6 | **No rate limit warning** to users | 🟡 MEDIUM | C203's multi-stock fetching will trigger rate limits. |
| 7 | **ROE annualization** misleading for seasonal businesses | 🟡 MEDIUM | Not directly related to Sprint 25. |

### Layer 3: Concurrency & Robustness

| # | Problem | Severity | Sprint 25 Impact |
|---|---------|----------|-------------------|
| 8 | **YAML race conditions** in watchlist/events | 🔴 HIGH | C203 will add new YAML data. More YAML = more race condition surface. |
| 9 | **Fragile event detection** field access | 🟡 MEDIUM | Not directly related to Sprint 25. |
| 10 | **Silent timeline filter failure** | 🟡 MEDIUM | Not directly related to Sprint 25. |

**Challenger Assessment**:

**🔴 The API abuse problem (#1) is directly relevant to C203.** If ecosystem cards fetch price data for 10-15 companies using the current `get_stock_info` pattern, it will trigger FinMind rate limits. This should be addressed BEFORE C203 implementation.

**🔴 The YAML race condition (#8) is directly relevant to C203.** Expanding `group_structures.yaml` means more YAML read/write operations. Without file locking, concurrent access could corrupt the file.

**🟡 The DuplicateWidgetID crash (#4) is relevant to C209** if it modifies event_dashboard.py.

**❓ Challenger Question 8**: Should Sprint 25 Week 1 be dedicated to fixing the API abuse in `get_stock_info` and adding file locking to YAML operations BEFORE building new features that depend on these broken foundations?

---

## Part 4: Design System Debt — 92 Issues, Grade C+

### Current State

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 | 26 | 26 | 2 |
| Round 3 | 3 | 29 | 0 |
| Round 4 | 25 | 54 | 0 |
| Round 5 | 17 | 71 | 2 |
| Round 6 | 10 | 81 | 1 |
| Round 7 | 11 | 92 | 0 |
| **Total** | **92** | **92** | **5** |

**Fix rate: 5.4% over 7 rounds. At this rate, it will take 126 rounds (≈ 3 years) to fix all issues.**

### Designer's Verification of Top 5 Fixes

The designer's Round 50 analysis reveals important corrections to the Round 7 recommendations:

| Issue | Round 7 Status | Designer Verification | Actual Status |
|-------|---------------|----------------------|---------------|
| D-073 (`_info_card()` color) | 5 min fix needed | **Already fixed** in Sprint 24 cleanup | ✅ FIXED |
| D-071 (Set3 palette) | 30 min fix needed | **Already fixed** in Sprint 24 cleanup | ✅ FIXED |
| D-084 (`st.bar_chart`) | 30 min fix needed | **Already fixed** in Sprint 24 cleanup | ✅ FIXED |
| D-005 (emoji conflict) | 15 min fix needed | Still present but **low severity in practice** | ⚠️ LOW |
| D-074 (`#F8F9FA` bg) | 10 min fix needed | Partially present — `_白话_card()` uses `white` intentionally | ⚠️ DESIGN DECISION |

**Key finding**: 3 of the 5 "top priority" fixes were ALREADY done during Sprint 24's design system cleanup (commit `2fc60d3`). The Round 7 recommendations were not cross-referenced with the Sprint 24 changes.

**❓ Challenger Question 9**: The design review process is not tracking what's been fixed. Round 7 recommended fixes that were already applied. This means the 92-issue count may include already-fixed issues. **Recommendation**: Before Sprint 25, run a fresh design audit that verifies ALL 92 issues against current code. The actual open count may be significantly lower.

### Remaining Non-Palette Colors (from Designer)

The designer identified 8 remaining non-palette colors in shared components, all fixable in ~10 minutes total:

| Color | Location | Should Be |
|-------|----------|-----------|
| `#BDC3C7` | `chart_stock_health.py`, `_financial.py` | `#ECF0F1` |
| `#95A5A6` | `main.py` (search, welcome) | `#7F8C8D` |
| `#F9E79F`/`#7D6608` | `main.py` (disclaimer) | `#FEF9E7`/`#2C3E50` |
| `#EBF5FB` | `_router_base.py` (lesson_card) | `#F8F9FA` |
| `#E8F8F5` | `_router_base.py` (beginner_banner) | `#F8F9FA` |
| `#F0F7FF` | `_router_base.py` (so_what_box) | `#F8F9FA` |
| `#2980B9` | `_router_base.py` (so_what_box border) | `#3498DB` |
| `white` | `_router_base.py` (白话_card bg) | `#F8F9FA` or keep as design choice |

**These 8 fixes (10 minutes) would bring the grade from C+ to B-.**

---

## Part 5: Tech Debt Items — 2 Sprint Old

From `handoff.md`:

| Issue | Severity | Location | Age |
|-------|----------|----------|-----|
| `validate_debate_text()` naming counterintuitive | 🟢 Low | `debate_engine.py` | 2 sprints |
| Timeline strings in `scenario:` namespace | 🟢 Low | `locales/*.yaml` | 2 sprints |
| Dead import in `_historical_scenarios.py` | 🟢 Low | `business_card/_historical_scenarios.py` | 2 sprints |

**Challenger Assessment**: These are individually trivial (5-15 min each) but collectively represent a pattern: **tech debt is never addressed, only accumulated.** The Sprint 24 plan listed these as "if time permits" and they weren't done. Now they're carried into Sprint 25.

**❓ Challenger Question 10**: Should Sprint 25 have a "tech debt budget" — e.g., 2h per sprint specifically for addressing accumulated low-severity items? Without this, tech debt will continue compounding indefinitely.

---

## Part 6: Blocking Questions — MUST ANSWER Before Sprint 25

| # | Question | Owner | Blocker For | Deadline |
|---|----------|-------|-------------|----------|
| **Q1** | Does Daniel approve the "ecosystem cards" approach for C203? (10-15 companies, parent-subsidiary + limited customer-subsidiary, card-based) | Daniel | C203 (MUST feature) | Before Sprint 25 starts |
| **Q2** | What is C206's scope? Single DCA lesson or multiple? Hypothetical data only or real stock examples? Calculator integration or pure content? | Daniel | C206 (SHOULD feature) | Before Sprint 25 starts |
| **Q3** | Should the 8 remaining non-palette color fixes be applied before Sprint 25 development? (10 minutes, brings grade to B-) | PM | Design system debt | Sprint 25 Week 1 Day 1 |
| **Q4** | Should the API abuse fix in `get_stock_info` be a prerequisite for C203? (C203 fetches 10-15 stock prices) | Architect | C203 data layer | Before C203 implementation |
| **Q5** | Should the 3 Sprint 23 tech debt items be fixed in Sprint 25? (20 minutes total) | PM | Tech debt accumulation | Sprint 25 Week 1 |

### Non-Blocking but Recommended

| # | Question | Owner | Impact |
|---|----------|-------|--------|
| Q6 | Should `_白话_card()` background be standardized to `#F8F9FA` or is `white` intentional? | Daniel + Designer | Card consistency |
| Q7 | Should `_section_title()` auto-prefix be removed entirely? | PM + Designer | Emoji consistency |
| Q8 | Should C209 be capped at 3 pages for v1? | PM | Scope control |

---

## Part 7: Recommendations

### 7.1 Sprint 25 Pre-Conditions (MUST be done before feature development)

1. **Apply the 8 non-palette color fixes** (10 minutes). This is the highest-ROI design activity possible. Brings grade from C+ to B-.
2. **Fix the 3 Sprint 23 tech debt items** (20 minutes). `validate_debate_text()` → `contains_banned_words()`, move timeline strings, remove dead import.
3. **Run a fresh design audit** to verify which of the 92 issues are actually still open. The count may be 60-70, not 92.
4. **Fix API abuse in `get_stock_info`** before C203 implementation. This is a prerequisite, not optional.

### 7.2 Sprint 25 Composition — Revised

**If Daniel approves C203 scope:**

| Priority | Feature | Effort | Notes |
|----------|---------|--------|-------|
| MUST | Pre-sprint fixes (colors + tech debt + API fix) | 2-3h | Week 1 Day 1-2 |
| MUST | C203 Ecosystem Cards v1 | 12-15h | Cap at 8-10 companies, not 15-20 |
| SHOULD | C209 Collapsible Source (3 pages) | 4-6h | Cap at 3 pages for v1 |
| SHOULD | C206 Recurring Investment Ed | 6-8h | Single lesson, hypothetical data only |
| COULD | Remaining design fixes | 2-3h | If time permits |

**If Daniel does NOT approve C203:**

| Priority | Feature | Effort | Notes |
|----------|---------|--------|-------|
| MUST | Pre-sprint fixes | 2-3h | Same as above |
| MUST | C209 Collapsible Source (all pages) | 7-9h | Expand to all pages since no C203 |
| MUST | C206 Recurring Investment Ed | 6-8h | Elevate to MUST |
| SHOULD | API abuse fix | 2-3h | Still needed for general health |
| COULD | Remaining design fixes | 2-3h | If time permits |

### 7.3 Scope Control Recommendations

1. **C203**: Cap at 8 companies (existing 5 + 3 new). NOT 15-20. The 15-20 scope is what caused the original 36-50h estimate.
2. **C206**: Single lesson only. Hypothetical data only. No calculator. No real stock examples.
3. **C209**: 3 pages for v1 (business_card, daily_market, event_dashboard). Defer remaining pages.

---

## Part 8: Risk Assessment

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C203 triggers API rate limits (10-15 stock fetches) | 🔴 High | High | Fix `get_stock_info` API abuse BEFORE C203 |
| C203 YAML data corruption (concurrent access) | 🔴 High | Medium | Add file locking to YAML operations |
| C206 crosses into investment advice territory | 🟡 Medium | Medium | Hypothetical data only, no calculator, disclaimer |
| C209 estimate exceeds 6h (page count creep) | 🟡 Medium | Medium | Cap at 3 pages for v1 |
| Design system grade stays at C+ indefinitely | 🟡 Medium | High | Apply 8 color fixes (10 min) before Sprint 25 |

### Product Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C203 is actually just group_structure.py with new cards | 🟡 Medium | Medium | Clarify value proposition before building |
| C206 scope ambiguity leads to rework | 🟡 Medium | High | Default to single lesson, hypothetical data |
| Sprint 25 has no MUST features if Daniel doesn't respond | 🔴 High | Medium | Define fallback plan (C209 + C206 as MUST) |
| Tech debt accumulation becomes unmanageable | 🟡 Medium | High | Establish 2h/sprint tech debt budget |

### Process Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Design audit doesn't track what's already fixed | 🟡 Medium | High | Run fresh audit before Sprint 25 |
| Round 7 recommendations were applied to already-fixed issues | 🟡 Medium | High | Cross-reference before recommending |
| Daniel decisions remain pending across multiple sprints | 🟡 Medium | High | Set deadline: if no response by Sprint 25 Week 1, use defaults |

---

## Part 9: Summary

### What's Working
- C201 shipped cleanly in Sprint 24 with 662 tests green
- Design system cleanup fixed 30+ violations in shared components
- C209 is well-designed and low-risk
- Academy infrastructure (C206) is proven and ready for new content
- `_subsidiary_card()` exists and is ready for C203 reuse

### What's Broken
- API abuse in `get_stock_info` will be triggered by C203
- 92 design issues with 5.4% fix rate over 7 rounds
- 3 tech debt items now 2 sprints old
- C203 value proposition is unclear (may duplicate group_structure.py)
- C206 scope ambiguity between education and advice

### What Needs to Happen
1. Daniel must decide on C203 and C206 scope BEFORE Sprint 25
2. Apply 8 color fixes (10 min) and 3 tech debt fixes (20 min) in Week 1
3. Fix API abuse before C203 implementation
4. Run fresh design audit to get accurate issue count
5. Cap all features at conservative scope estimates

---

*Created: 2026-06-17 by Challenger*
*References: docs/state/handoff.md, docs/state/handoff_discuss_r49.md, docs/state/challenge_r49.md, docs/architecture/discuss_r49_architect.md, docs/architecture/discuss_r50_architect.md, docs/design/discuss_r50_designer.md, docs/state/current_problems.md, docs/state/pending_review.md*
*Verification: All 662 tests passing. Design system grade C+ (92 issues, 5 fixed). Sprint 24 C201 complete.*
