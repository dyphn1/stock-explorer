# Challenge – Round 52 (Sprint 26 Planning)

**Date**: 2026-06-17
**Author**: Challenger (Round 52)
**Sprint**: Sprint 26 — Planning
**Context**: Sprint 25 ✅ COMPLETE (658 tests green). C206 DCA lesson shipped. C209 source section integrated. C203 deferred. Sprint 26 candidates: C203 Ecosystem Cards (10-12h), design debt top 5 (90 min), Dark/Light Theme D-126 (8-12h), _infocard D-127 (6-9h).

---

## Executive Verdict

**⚠️ CONDITIONAL** — Sprint 26 has a reasonable candidate set, but the Challenger identifies **3 structural problems** that must be resolved before committing:

1. **Infrastructure debt is now 3 sprints deep** — API abuse, cache invalidation, race conditions, and silent failures have been flagged since Sprint 23 and remain unaddressed. Sprint 26 adds features that depend on these broken foundations.
2. **C203 is still pending Daniel approval** — it was deferred from Sprint 25 with the same open questions. The default "defer to Sprint 26" has been consumed. This is now the last deferral.
3. **Design debt is 81 issues with a 3.7% fix rate** — the top 5 fixes (90 min total) are trivial and global, yet have been recommended for 3 consecutive rounds without action.

**Conditions for ALIGNED**:
- Fix API abuse in `get_stock_info` BEFORE C203 implementation (prerequisite, not optional)
- Apply the top 5 design debt fixes (90 min) in Sprint 26 Week 1 Day 1
- Daniel must approve C203 scope or it is dropped from Sprint 26 (no more deferrals)

---

## Part 1: Round 50/51 Blocking Questions — Status Check

| # | Question (from challenge_r50) | Status | Evidence |
|---|-------------------------------|--------|----------|
| Q1 | Does Daniel approve "ecosystem cards" for C203? | ⏳ STILL PENDING | Listed in `pending_review.md` as "⏳ Pending Daniel" — unchanged from Sprint 25 planning |
| Q2 | C206 scope (single lesson vs. multiple)? | ✅ RESOLVED | Sprint 25 shipped single DCA lesson with hypothetical data only (commit 1a0c426) |
| Q3 | Apply 8 non-palette color fixes before Sprint 25? | ❌ NOT DONE | Sprint 25 did fix 8 non-palette colors (per handoff.md line 64), but the Challenger cannot verify if these were the same 8 from Round 7 |
| Q4 | API abuse fix as prerequisite for C203? | ❌ NOT DONE | Sprint 25 did not address API abuse. C203 was deferred, so the prerequisite was not triggered |
| Q5 | Fix 3 Sprint 23 tech debt items in Sprint 25? | ⚠️ PARTIALLY | `validate_debate_text()` → `contains_banned_words()` was done (handoff.md line 62). Timeline i18n keys were added (line 63). Dead import status unclear. |

### Key Observation

Sprint 25 completed C206 and C209 but did NOT address the infrastructure prerequisites that the Challenger identified as blockers for C203. Now C203 is back as a Sprint 26 candidate with the same unaddressed prerequisites.

**❓ Challenger Question 1**: The API abuse in `get_stock_info` was identified as a prerequisite for C203 in Sprint 25. It was not fixed because C203 was deferred. Now C203 is proposed for Sprint 26. **Should Sprint 26 Week 1 be dedicated to infrastructure fixes (API abuse, cache invalidation, YAML race conditions) BEFORE any new feature work?**

---

## Part 2: Cross-Examination of Sprint 26 Candidates

### 2.1 C203 — Company Ecosystem Cards v1 (10-12h, pending Daniel)

**Context from Sprint 25**: Deferred by default. Pre-conditions exist (`group_structures.yaml` has 5 companies, `_subsidiary_card()` is reusable). Missing: `ecosystem_service.py` + `ecosystem_cards.py`.

**Challenger's Cross-Examination**:

**🔴 BLOCKING: The data source problem from Round 50 is STILL unsolved.**

From challenge_r50 (still valid):
- `group_structures.yaml` has **parent-subsidiary** data, NOT customer-supplier data
- The original C203 was killed because customer-supplier data requires paid APIs or manual curation
- The redefined C203 claims to use "2-3 well-known customer-supplier pairs" — but where does this data come from?

**❓ Challenger Question 2**: The handoff.md says "Pre-Conditions for C203: `group_structures.yaml`: 5 parent companies, ~20 subsidiaries ✅". But this is parent-subsidiary data. The Sprint 25 redesign added "customer-supplier pairs" as a scope item. **Where is the customer-supplier data source?** If it doesn't exist, C203 is just a reskin of the existing `group_structure.py` page — which is already 314 lines and functional.

**❓ Challenger Question 3**: C203 has been "pending Daniel" for 2 sprints. The Sprint 25 default was "defer to Sprint 26." Now we're in Sprint 26 planning with the same pending status. **What is the default if Daniel doesn't respond to Sprint 26 planning?** The Challenger recommends: **DROP C203 if no response by Sprint 26 Week 1 Day 1.** Three consecutive deferrals is not planning — it's avoidance.

**🔴 INFRASTRUCTURE CONFLICT**: C203 will fetch price data for 10-15 companies. The current `get_stock_info` fetches the ENTIRE stock list per stock_id (Layer 1, Problem 1). This means C203 will trigger 10-15 full-list API calls where 1 should suffice. **This will trigger FinMind rate limits.**

**Risk Assessment**: 🔴 HIGH — The feature has unresolved scope questions, an unclear data source, and depends on broken infrastructure. The 10-12h estimate may be optimistic if data curation is needed.

---

### 2.2 Design Debt Top 5 Fixes (90 min total, MUST)

From handoff.md:
| Issue | Effort | Impact |
|-------|--------|--------|
| D-005: Fix `_section_title()` emoji conflict | 15 min | Affects all pages |
| D-069+D-070: Fix chart.py theme colors | 115 min* | Affects all charts globally |
| D-071: Replace Set3 palette in pie charts | 30 min | Affects all pie charts |

*Note: handoff.md says 115 min for D-069+D-070, but the Challenger's Round 50 analysis found these were already partially addressed in Sprint 24 cleanup. The actual remaining effort may be lower.

**Challenger's Cross-Examination**:

**✅ These are the highest-ROI items in the entire sprint plan.** 90 minutes of work for global improvements to all pages and charts.

**🟡 CONCERN: These have been recommended for 3 consecutive rounds (R50, R51, R52) without action.** The Round 50 challenge identified that 3 of the 5 "top priority" fixes were already done in Sprint 24. The remaining 2 (D-005 emoji conflict, D-069+D-070 chart colors) are still open.

**❓ Challenger Question 4**: D-069+D-070 are listed at 115 min in handoff.md but the Round 50 designer verification found chart.py was already cleaned in Sprint 24. **What is the actual remaining effort?** If the chart colors were already fixed, this item should be 0 min, not 115 min.

**Risk Assessment**: 🟢 LOW — These are pure improvements with no feature risk. The only risk is that they continue to be deferred.

**Challenger Recommendation**: **MUST DO — Sprint 26 Week 1 Day 1.** These should be the first commits of the sprint. 90 min for global improvements is the best investment of Sprint 26 hours.

---

### 2.3 Dark/Light Theme D-126 (8-12h, pending Daniel)

**Context**: Listed in `pending_review.md` as "⏳ Pending Daniel — Sprint 26+ candidate." Design review identified missing dark/light theme implementation.

**Challenger's Cross-Examination**:

**🟡 CONCERN: Theme support is a large feature with infrastructure implications.**

Adding dark/light theme requires:
1. CSS variable system (design tokens) — the app currently has none (Layer 5 Round 5: D-062)
2. Every hardcoded color in the codebase must be replaced with CSS variables
3. Theme preference persistence (cookie, localStorage, or session state)
4. Testing across all pages for both themes

**❓ Challenger Question 5**: The design system has 81 issues, many of which are hardcoded colors that don't match the palette. **If we implement dark/light theme BEFORE fixing the color violations, we'll be theming a broken palette.** Should the color fixes (top 5, 90 min) be a prerequisite for D-126?

**❓ Challenger Question 6**: D-126 is estimated at 8-12h. But the app has 10+ page files with hardcoded colors. Replacing all of them with CSS variables, testing both themes, and handling edge cases (charts, gradients, custom HTML) is closer to 15-20h. **Is the 8-12h estimate realistic?**

**Risk Assessment**: 🟡 MEDIUM — The feature is desirable but the estimate is likely optimistic. It should not take priority over infrastructure fixes.

---

### 2.4 _infocard() Component D-127 (6-9h, pending Daniel)

**Context**: Listed in `pending_review.md` as "⏳ Pending Daniel — Sprint 26+ candidate." Proposal: Create `_infocard(icon, sparkline_data, label, value, analogy)` component.

**Challenger's Cross-Examination**:

**🟡 CONCERN: New component without clear consumer.**

The `_infocard()` component is described as "infographic-style visual cards." But:
- Which pages will use it?
- What data will populate the `sparkline_data` parameter?
- Is this a new component or a specialization of the existing `_白话_card()`?

**❓ Challenger Question 7**: The existing `_白话_card()` already handles the "visual card with label + value" pattern. What does `_infocard()` do that `_白话_card()` doesn't? If the answer is "sparkline data," should the sparkline be a parameter of `_白话_card()` rather than a new component?

**❓ Challenger Question 8**: D-127 has no architecture doc, no design doc, and no consumer identified. It's a component in search of a use case. **Should this be deferred until a specific page needs it, rather than building it speculatively?**

**Risk Assessment**: 🟡 MEDIUM — The component may be useful, but building it without a clear consumer risks creating dead code. The 6-9h may be wasted if no page adopts it.

---

## Part 3: Layer 1-3 Problems — The Elephant in the Room

From `current_problems.md`, these issues have been flagged since Sprint 23 (3 sprints ago):

### Critical Infrastructure Issues

| # | Problem | Severity | Sprint 26 Impact |
|---|---------|----------|-------------------|
| 1 | **API Abuse in `get_stock_info`** — fetches entire stock list per stock_id | 🔴 HIGH | C203 fetches 10-15 stocks → 10-15 full-list API calls → rate limit |
| 2 | **Daily cache invalidation** — cache key changes daily, TTL useless, old files never deleted | 🟡 MEDIUM | Affects all features. `.cache/` directory grows without bound |
| 3 | **YAML race conditions** — read-modify-write pattern with no file locking | 🔴 HIGH | C203 expands `group_structures.yaml` → more concurrent write surface |
| 4 | **Silent timeline filter failure** — returns ALL data on error, no user feedback | 🟡 MEDIUM | Affects all pages with timeline controls |
| 5 | **No rate limit warning** — API errors shown as "No data found" | 🟡 MEDIUM | C203 multi-stock fetching will trigger this |
| 6 | **DuplicateWidgetID crash** in event_dashboard | 🔴 CRITICAL | Any new component in event_dashboard risks triggering this |

### Challenger Assessment

**🔴 Sprint 26 cannot add C203 without fixing #1 (API abuse) and #3 (YAML race conditions) first.** These are not "nice to have" infrastructure improvements — they are prerequisites for the proposed feature.

**🟡 The cache invalidation (#2) and silent failure (#4) are not blockers for Sprint 26, but they are accumulating.** At some point, the `.cache/` directory will cause disk issues, and users will complain about broken timeline filters.

**❓ Challenger Question 9**: The Layer 1-3 problems have been documented for 3 sprints. They were flagged as "should be prioritized" in the original problem analysis. Yet 0 of the 6 critical/high issues have been addressed. **Is there a plan to address these, or will they be deferred indefinitely as new features are added on top of broken foundations?**

---

## Part 4: Design System Debt — 81 Issues, Grade C

### Current State (from Round 6)

| Round | New Issues | Total | Fixed |
|-------|-----------|-------|-------|
| Round 2 | 26 | 26 | 2 |
| Round 3 | 3 | 29 | 0 |
| Round 4 | 25 | 54 | 0 |
| Round 5 | 17 | 71 | 2 |
| Round 6 | 10 | 81 | 1 |
| **Total** | **81** | **81** | **5** |

**Fix rate: 6.2% over 6 rounds. At this rate, it will take 97 rounds (≈ 2.5 years) to fix all issues.**

### Sprint 25 Contribution

Sprint 25 fixed 8 non-palette color issues (handoff.md line 64). This is the first significant design debt reduction in 3 rounds. The Challenger commends this progress.

### Remaining High-Value Fixes

The top 5 fixes from handoff.md (D-005, D-069, D-070, D-071) total 90 min and affect all pages globally. These are the only items in Sprint 26 that provide universal improvement.

**❓ Challenger Question 10**: The design debt is accumulating faster than it's being fixed. New features (C203, D-126, D-127) will add new code with new design violations. **Should Sprint 26 allocate 20% of capacity (≈5h) to design debt reduction, or will we continue the pattern of adding features on top of a broken design system?**

---

## Part 5: Go/No-Go Criteria for Each Sprint 26 Feature

### C203 — Company Ecosystem Cards v1

| Gate | Criterion | Status |
|------|-----------|--------|
| **G1: Scope Approval** | Daniel approves the ecosystem cards approach | ⏳ PENDING — 2 sprints |
| **G2: Data Source** | Customer-supplier data source identified and curated | ❌ NOT MET — only parent-subsidiary data exists |
| **G3: API Fix** | `get_stock_info` API abuse fixed (prerequisite) | ❌ NOT MET — 3 sprints unaddressed |
| **G4: YAML Safety** | File locking added to YAML operations (prerequisite) | ❌ NOT MET — 3 sprints unaddressed |
| **G5: Test Coverage** | New `ecosystem_service.py` and `ecosystem_cards.py` have tests | ⏳ NOT STARTED |

**Verdict**: 🔴 **NO-GO** — 3 of 5 gates are not met, including 2 prerequisites. C203 should be **dropped from Sprint 26** unless G1, G3, and G4 are resolved before Sprint 26 Week 1 Day 3.

### Design Debt Top 5 Fixes

| Gate | Criterion | Status |
|------|-----------|--------|
| **G1: Verification** | Verify which of D-005, D-069, D-070, D-071 are still open | ⚠️ NEEDED — Round 50 found 3 of 5 were already done |
| **G2: Implementation** | Apply remaining fixes | ✅ READY — 90 min estimated |
| **G3: Test Pass** | 658 tests still green after fixes | ⏳ NOT STARTED |

**Verdict**: 🟢 **GO** — This is the lowest-risk, highest-ROI item in Sprint 26. Should be the first work of the sprint.

### Dark/Light Theme D-126

| Gate | Criterion | Status |
|------|-----------|--------|
| **G1: Scope Approval** | Daniel approves theme implementation | ⏳ PENDING |
| **G2: Color Fixes** | Design debt color violations fixed first | ❌ NOT MET — prerequisite |
| **G3: CSS Variable System** | Design tokens defined (`:root { --color-primary: #3498DB; }`) | ❌ NOT MET — D-062 still open |
| **G4: Consumer Adoption** | At least 3 pages updated to use CSS variables | ⏳ NOT STARTED |
| **G5: Dual Theme Test** | All pages tested in both light and dark modes | ⏳ NOT STARTED |

**Verdict**: 🟡 **CONDITIONAL GO** — Only if Daniel approves AND the top 5 design fixes are applied first. Without G2, theming will be applied to a broken palette. Estimate is likely 12-18h, not 8-12h.

### _infocard() Component D-127

| Gate | Criterion | Status |
|------|-----------|--------|
| **G1: Scope Approval** | Daniel approves component creation | ⏳ PENDING |
| **G2: Consumer Identified** | At least 1 page committed to using `_infocard()` | ❌ NOT MET — no consumer identified |
| **G3: Architecture Doc** | Component API documented | ❌ NOT MET — no doc |
| **G4: Design Compliance** | Component uses design system colors | ⏳ NOT STARTED |
| **G5: Test Coverage** | Component has unit tests | ⏳ NOT STARTED |

**Verdict**: 🔴 **NO-GO** — No consumer, no architecture doc, no design review. This is speculative development. Defer to Sprint 27+ when a specific page needs it.

---

## Part 6: Recommended Sprint 26 Composition

### Option A: Infrastructure-First (RECOMMENDED)

| Priority | Feature | Effort | Notes |
|----------|---------|--------|-------|
| MUST | Top 5 design debt fixes | 90 min | Week 1 Day 1 — verify and apply |
| MUST | Fix API abuse in `get_stock_info` | 3-4h | Week 1 — prerequisite for any multi-stock feature |
| MUST | Fix YAML race conditions (file locking) | 2-3h | Week 1 — prerequisite for any YAML-based feature |
| SHOULD | Fix cache invalidation + cleanup | 2-3h | Week 1 — affects all features |
| SHOULD | C203 Ecosystem Cards v1 | 10-12h | Week 2 — ONLY if Daniel approves scope |
| COULD | Dark/Light Theme D-126 | 12-18h | Week 2-3 — ONLY if Daniel approves |

**Total**: 30-38h (within a 2-week sprint with buffer)

### Option B: Feature-First (Current Plan)

| Priority | Feature | Effort | Notes |
|----------|---------|--------|-------|
| MUST | C203 Ecosystem Cards v1 | 10-12h | Depends on broken infrastructure |
| MUST | Top 5 design debt fixes | 90 min | |
| SHOULD | Dark/Light Theme D-126 | 8-12h | |
| SHOULD | _infocard() D-127 | 6-9h | No consumer identified |

**Total**: 26-33h

**Challenger Assessment**: Option B puts features before infrastructure. C203 will trigger rate limits on Day 1. The YAML race condition will worsen. This is technical debt compounding, not reduction.

---

## Part 7: Blocking Questions — MUST ANSWER Before Sprint 26

| # | Question | Owner | Blocker For | Deadline |
|---|----------|-------|-------------|----------|
| **Q1** | Does Daniel approve C203 ecosystem cards scope? (If no response, DROP from Sprint 26 — no more deferrals) | Daniel | C203 | Sprint 26 Week 1 Day 1 |
| **Q2** | Does Daniel approve Dark/Light Theme D-126? | Daniel | D-126 | Sprint 26 Week 1 Day 1 |
| **Q3** | Does Daniel approve _infocard() D-127? (Challenger recommends NO — no consumer identified) | Daniel | D-127 | Sprint 26 Week 1 Day 1 |
| **Q4** | Should Sprint 26 Week 1 be dedicated to infrastructure fixes (API abuse, YAML locking, cache) before feature work? | PM + Architect | All features | Sprint 26 planning |
| **Q5** | Where does customer-supplier data for C203 come from? | Architect | C203 data layer | Before C203 implementation |

### Non-Blocking but Recommended

| # | Question | Owner | Impact |
|---|----------|-------|--------|
| Q6 | Should the 3 Sprint 23 tech debt items be fixed in Sprint 26? (20 min total) | PM | Tech debt accumulation |
| Q7 | Should `_section_title()` auto-prefix be removed entirely? (D-005) | PM + Designer | Emoji consistency |
| Q8 | Should a "tech debt budget" be established (2h/sprint)? | PM | Long-term code health |

---

## Part 8: Risk Assessment

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C203 triggers API rate limits (10-15 stock fetches with broken `get_stock_info`) | 🔴 High | **CERTAIN** | Fix API abuse BEFORE C203 — no exceptions |
| C203 YAML data corruption (concurrent access to expanded `group_structures.yaml`) | 🔴 High | Medium | Add file locking to YAML operations |
| D-126 theme breaks existing UI (hardcoded colors don't respond to CSS variables) | 🟡 Medium | High | Fix color violations BEFORE theme implementation |
| D-127 _infocard() becomes dead code (no consumer adopts it) | 🟡 Medium | High | Defer until a page needs it |
| Cache directory grows without bound during Sprint 26 | 🟢 Low | High | Fix cache invalidation in Week 1 |

### Product Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| C203 is just group_structure.py with new cards (no new value) | 🟡 Medium | Medium | Clarify value proposition before building |
| Sprint 26 has no MUST features if Daniel doesn't respond | 🔴 High | Medium | Default: infrastructure fixes become MUST |
| Design debt continues accumulating (81 → 90+ issues) | 🟡 Medium | High | Allocate 20% capacity to design debt reduction |

### Process Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Daniel decisions remain pending for 3rd sprint | 🟡 Medium | High | Set hard deadline: no response = DROP |
| Infrastructure fixes are deferred again | 🔴 High | High | Make infrastructure fixes MUST, not SHOULD |
| Sprint 26 becomes "Sprint 25B" — same deferrals, same pending items | 🟡 Medium | Medium | Take decisive action on C203 (build or kill) |

---

## Part 9: Summary

### What's Working
- Sprint 25 shipped cleanly: C206 lesson + C209 source section + 8 color fixes
- 658 tests green — strong test infrastructure
- Design system grade improved from D+ to C
- Top 5 design fixes are well-defined and scoped (90 min)
- `_subsidiary_card()` exists and is reusable for C203

### What's Broken
- API abuse in `get_stock_info` — 3 sprints unaddressed, will be triggered by C203
- YAML race conditions — 3 sprints unaddressed, will worsen with C203
- Cache invalidation — daily cache miss, unbounded `.cache/` growth
- 81 design issues with 6.2% fix rate
- C203 scope still pending after 2 sprints
- D-127 _infocard() has no consumer

### What Needs to Happen
1. **Daniel must decide on C203, D-126, D-127 by Sprint 26 Week 1 Day 1** — no more deferrals
2. **Sprint 26 Week 1 = Infrastructure Week** — API fix, YAML locking, cache fix, design debt top 5
3. **C203 only if prerequisites met** — API fix + YAML locking + Daniel approval
4. **D-127 should be dropped** — no consumer, no architecture doc, speculative
5. **Establish 2h/sprint tech debt budget** — prevent indefinite accumulation

---

## Final Verdict: ⚠️ CONDITIONAL

**Sprint 26 is CONDITIONALLY aligned.** The plan is acceptable IF:

1. ✅ **Infrastructure fixes are MUST, not SHOULD** — API abuse, YAML locking, and cache invalidation must be Week 1 priorities
2. ✅ **C203 is dropped if Daniel doesn't respond by Week 1 Day 1** — three deferrals is the limit
3. ✅ **Top 5 design fixes are applied in Week 1 Day 1** — 90 min, global impact, no reason to defer
4. ✅ **D-127 _infocard() is dropped from Sprint 26** — no consumer, no architecture doc
5. ❌ **D-126 Dark/Light Theme is deferred to Sprint 27** — unless Daniel explicitly approves AND color fixes are done first

**If these conditions are met, Sprint 26 becomes:**
- Week 1: Infrastructure + design debt (API fix, YAML locking, cache fix, top 5 fixes)
- Week 2: C203 (if approved) or additional infrastructure work

**If these conditions are NOT met, Sprint 26 is BLOCKED** — adding features on broken foundations will compound technical debt and increase system fragility.

---

*Created: 2026-06-17 by Challenger*
*References: docs/state/handoff.md, docs/state/current_problems.md, docs/state/pending_review.md, docs/state/challenge_r50.md*
*Verification: 658 tests passing. Design system grade C (81 issues, 5 fixed). Sprint 25 C206+C209 complete.*
