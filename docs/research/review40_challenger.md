# Review Round 40 — Challenger Report

> **Date**: 2026-06-14
> **Reviewer**: Challenger (Independent Stress Test)
> **Context**: Sprint 19 COMPLETE (5/6 items). Sprint 20 planned: C167 + C163 + C40 (30-42h).
> **Scope**: 3-round challenge of Review Round 40 findings and Sprint 20 plan.

---

## Round 1: Gap Authenticity Challenge

### 1.1 — Are C170-C175 really gaps or nice-to-haves?

**C170 (Tappable Glossary, P1, 6-10h)**: **AUTHENTIC GAP.** The QA report identifies that FinChat, StockStory, Finimize, and Stash all have tappable metric glossary as a core feature. D-113 (metric_explainer tests) was written in Sprint 19 but the feature is not yet implemented. This is a validated competitive gap — not a nice-to-have. The fact that 4/5 new competitors in Round 40 alone have this feature elevates it from P2 to P1. **Verdict: Real gap, should be addressed.**

**C171 (Valuation Band Chart, P2, 8-10h)**: **AUTHENTIC but not urgent.** StockStory and 財報狗 both have this. It's a standard feature in stock analysis platforms. However, it doesn't differentiate — it's expected. **Verdict: Real gap, but P2 is correct. Sprint 21 candidate.**

**C172 (Concept Comparison, P2, 10-14h)**: **NICE-TO-HAVE.** Magnify.money has this for US concepts, but no TW competitor does. This is a differentiator, not a gap. **Verdict: Not a gap — it's a future differentiator. Sprint 22+ candidate.**

**C173 (Visual Calculators, P2, 12-16h)**: **NICE-TO-HAVE.** Magnify.money and Investopedia have this, but it's an enhancement, not a gap. No TW competitor has it, which means it's white space, not a missing feature. **Verdict: Not a gap — it's a future differentiator. Sprint 22+ candidate.**

**C174 (Sector Storytelling, P2, 14-20h)**: **NICE-TO-HAVE.** Smallcase (India) proves the model, but no TW competitor has it. This is a potential differentiator, not a gap. **Verdict: Not a gap — it's a future differentiator. Sprint 21+ candidate.**

**C175 (Learn First Soft Gate, P1, 8-12h)**: **DUPLICATE of C163.** C175 is essentially the same feature as C163 (Learn First Gate). The QA report lists both as P1, but they're the same concept. **Verdict: Duplicate — C163 already covers this. No new gap.**

**Round 1 Verdict on C170-C175**: 1 authentic P1 gap (C170), 1 authentic P2 gap (C171), 2 nice-to-haves (C172, C173), 1 future differentiator (C174), 1 duplicate (C175 = C163). The QA report's claim of "6 new gaps" is overstated — there are 2 real gaps and 4 other items.

### 1.2 — Is C167 (AI Screener Explanations) authentic given we have a screener?

**The challenge**: The screener exists (C42, `stock_screener.py`, 272 lines). C167 adds plain-language explanations to screener results. This is NOT building infrastructure for a feature that doesn't exist — it's enhancing an existing feature with narrative context. The screener page already has filtering, presets, and a results grid. C167 adds the "why" behind the "what."

**Evidence**: The `stock_screener_service.py` already returns structured results via `format_screening_results()`. The `TemplateExplanationProvider` pattern is already proven by `delta_explanation_provider.py`. C167 composes these existing pieces. This is a 12-16h integration task, not a 12-16h build-from-scratch.

**Verdict: AUTHENTIC.** C167 is a real gap — the screener exists but lacks narrative context. This is a "last mile" feature that transforms a data tool into a learning tool. The infrastructure exists; C167 adds the historian layer.

### 1.3 — Do we need C163 (Learn First Gate) when C47 (Education Academy) already exists?

**The challenge**: C47 (Education Academy) is a full page with lessons, quizzes, and progress tracking (`academy.py`, 367 lines). C163 (Learn First Gate) is an onboarding gate that appears before users see stock data. These are DIFFERENT features serving DIFFERENT purposes:

- **C47 Academy**: A destination page users visit to learn. It's a library of structured lessons.
- **C163 Learn First Gate**: An onboarding flow that appears on FIRST visit. It's a gateway, not a destination.

**The distinction matters**: C47 is "go learn when you want." C163 is "learn before you explore." The QA report validates this distinction — Tastytrade's "Learn → Paper Trade → Live Trade" pipeline is a gate model, not a library model. Webull's "Learn first, trade later" is also a gate.

**However**: The existing `first_visit_guide.py` (C103, 47 lines) already provides a 2-card dismissible primer. C163 is a more comprehensive version with multi-step micro-lessons. The question is whether the additional complexity (3-5 micro-lessons vs. 2 cards) justifies the effort.

**Verdict: AUTHENTIC but with a caveat.** C163 is a real gap — no TW competitor has education-first onboarding. But C163 must be designed to REPLACE `first_visit_guide.py`, not coexist with it. Having both would be confusing. The design should consolidate: C163 absorbs C103's role and extends it.

### 1.4 — Is extracting INDUSTRY_BENCHMARKS to YAML (D-120) worth 1-2h for 23 entries?

**The challenge**: The dict is only 23 entries, identical across 3 files. Is extracting to YAML really worth the effort?

**Evidence**: All 3 dicts are byte-for-byte identical (verified above). The dict is 29 lines in each file. Adding a new industry requires editing 3 files. Missing one creates inconsistent benchmark behavior.

**Analysis**: The 1-2h estimate includes: (1) creating `industry_benchmarks.yaml`, (2) updating 3 consumers, (3) testing. For 23 entries, this is a straightforward YAML migration. The risk of NOT doing it: every future industry edit is a 3-file synchronization task. Given that the codebase has 15+ YAML files and the D6 (hardcoded data) pattern is well-established, this is a low-effort, high-consistency win.

**Counter-argument**: The dict is small and stable. How often do industries change? If the answer is "rarely," the YAML extraction is cosmetic.

**Verdict: WORTH DOING, but not at the expense of features.** D-120 is a 1-2h task that should be done on Day 1 of Sprint 20 as infrastructure cleanup. It's not a feature, but it prevents future bugs. The 23-entry size is irrelevant — what matters is the duplication pattern. However, it should NOT displace any Sprint 20 feature work. It's a "do while waiting for content" task.

### Round 1 Verdict

| Item | Challenge | Verdict |
|------|-----------|---------|
| C170-C175 | Are they real gaps? | ✅ C170 real, C171 real, C172-174 nice-to-haves, C175 duplicate |
| C167 | Building for non-existent feature? | ✅ Authentic — screener exists, needs narrative layer |
| C163 | Redundant with C47? | ✅ Authentic — gate ≠ library, but must REPLACE C103 |
| D-120 | Worth 1-2h for 23 entries? | ✅ Worth doing as Day 1 infrastructure, not feature work |

**Confirmed**: C167 is authentic, C163 is authentic (with C103 consolidation requirement), C170 is authentic.
**Challenged**: C175 is duplicate of C163. C172-C174 are nice-to-haves, not gaps.
**Needs revision**: C163 must absorb C103, not coexist. D-120 should be Day 1 infrastructure, not a feature.

---

## Round 2: Priority Challenge

### 2.1 — Is adding C170 (Tappable Glossary, 6-10h) as a 4th P1 item realistic?

**The math**: Sprint 20 budget is 30-42h for 3 features. Adding C170 (6-10h) as a 4th item pushes the total to 36-52h. The upper bound exceeds the budget by 10h.

**Current estimates**:
- C167: 12-16h
- C163: 10-14h
- C40: 8-12h
- C170: 6-10h
- **Total: 36-52h**

**Analysis**: The QA report recommends 38-54h (with different estimates). Both estimates exceed the 30-42h budget at the upper bound. This is a problem.

**However**: C170 (Tappable Glossary) has a natural integration point with C40 (Beginner/Expert Mode). The glossary is a core component of beginner mode — beginners need term definitions. If C40 and C170 are designed together, the combined effort may be less than the sum of parts.

**Revised estimate if integrated**:
- C167: 12-16h (standalone)
- C163: 10-14h (standalone)
- C40 + C170: 10-16h (integrated — C40's beginner mode includes glossary)
- **Total: 32-46h**

This is within the 30-42h budget at the midpoint (39h), with the upper bound only 4h over.

**Verdict: REALISTIC IF INTEGRATED.** Adding C170 as a standalone 4th item is NOT realistic (36-52h exceeds budget). But integrating C170 into C40 as a "beginner mode feature" is realistic. The glossary should not be a separate feature — it should be a component of C40.

### 2.2 — Should C170 displace C40 in Sprint 20?

**No.** C40 (Beginner/Expert Mode) is a broader feature that affects the entire application's information architecture. C170 (Tappable Glossary) is a component that serves beginner mode. Displacing C40 with C170 would be replacing a system with a component.

**The right approach**: C40 absorbs C170. Beginner mode includes the glossary. Expert mode hides it. This is how FinChat does it — the glossary is part of the beginner experience, not a separate feature.

**Verdict: NO displacement. C40 absorbs C170.**

### 2.3 — Is the C152 swap condition still valid?

**Background**: C152 (Multi-Factor Event Narratives) was deferred from Sprint 19. The swap condition states: "If Sprint 19 C152 spike quality is high, C152 replaces C40 in Sprint 20."

**The challenge**: The C152 spike was deferred — it was not completed in Sprint 19. The spike was supposed to produce 4 artifacts: (a) event correlation logic, (b) 3-5 tone-audited templates, (c) `NarrativeProvider` protocol design, (d) integration point identified. If the spike wasn't done, there are no artifacts to evaluate.

**Current state**: The C152 spike was deferred to "future sprint" per the Sprint 19 completion report. This means the swap condition cannot be evaluated — there's nothing to evaluate.

**Verdict: SWAP CONDITION IS VOID.** The C152 spike was deferred, not completed. There are no artifacts to assess. The swap condition should be removed from Sprint 20 planning. C152 should be planned for Sprint 21 based on a new spike, not carried over from Sprint 19.

### 2.4 — Are any of the 4 new debt items (D-117 through D-120) important enough for Sprint 20?

**D-117 (events.yaml survivorship bias)**: Content task, 2-3h. Not a code issue. **Verdict: Do alongside C167 if time permits. Not blocking.**

**D-118 (case_study_library.yaml missing severity)**: 0.5h. Trivial. **Verdict: Do on Day 1 as infrastructure cleanup. Not blocking.**

**D-119 (pattern_detector.py field redundancy)**: 0.25h. Cosmetic. **Verdict: No action needed. The redundancy is defensive.**

**D-120 (INDUSTRY_BENCHMARKS duplication)**: 1-2h. **Verdict: Do on Day 1 as infrastructure cleanup. Prevents future bugs.**

**Summary**: D-118 and D-120 should be done on Day 1 of Sprint 20 as infrastructure cleanup (1.5h total). D-117 is a content task that can be done alongside C167. D-119 needs no action.

### Round 2 Verdict

| Item | Challenge | Verdict |
|------|-----------|---------|
| C170 as 4th item | Realistic? | ⚠️ Only if integrated into C40, not standalone |
| C170 displaces C40? | Should it? | ❌ No — C40 absorbs C170 |
| C152 swap condition | Still valid? | ❌ VOID — spike was deferred, no artifacts to evaluate |
| D-117 through D-120 | Important for Sprint 20? | ⚠️ D-118 + D-120 = Day 1 cleanup (1.5h). D-117 = content task alongside C167. D-119 = no action. |

**Confirmed**: C170 integrated into C40 is realistic. D-118 + D-120 are quick Day 1 wins.
**Challenged**: C170 as standalone 4th item is NOT realistic. C152 swap condition is void.
**Needs revision**: Remove C152 swap condition from Sprint 20 plan. Integrate C170 into C40.

---

## Round 3: Goal Alignment Challenge

### 3.1 — Does adding an AI screener (C167) contradict the "historian" positioning?

**The concern**: Screeners are for finding stocks to buy, not for learning about companies. The "historian" positioning is about explaining what happened, not recommending what to buy.

**The counter-argument**: C167 doesn't add a screener — the screener already exists (C42). C167 adds plain-language explanations to screener results. This transforms a "stock picker" tool into a "learning tool." Instead of "here are 50 stocks with P/E < 15," it says "these stocks have low P/E ratios, which means the market is pricing them cheaply relative to earnings. Historically, this can mean..."

**The historian framing**: The discussion round already established that C167 uses historian tone with disclaimer: "篩選結果僅供學習參考，不構成投資建議." This is consistent with the positioning.

**However**: There's a risk that C167's explanations become implicit recommendations. "These stocks have high dividend yields because they return more cash to shareholders" can be read as "you should buy these stocks." The historian tone must be carefully maintained.

**Verdict: DOES NOT CONTRADICT, but requires careful tone management.** C167 is a bridge feature that brings historian-style narratives to a non-historian page. The key is ensuring explanations describe, not recommend. The disclaimer is necessary but not sufficient — the explanation text itself must maintain historian tone.

### 3.2 — Does C163 (Learn First Gate) create a barrier to entry that reduces engagement?

**The concern**: Gating content behind education creates friction. Users want to see stock data immediately, not complete a lesson first.

**The counter-argument**: The QA report explicitly addresses this — Tastytrade proves that education-first drives retention without reducing engagement. The key design principle is "soft gate" (educate, don't block). C163 should be a dismissible onboarding flow, not a mandatory gate.

**The evidence**: The existing `first_visit_guide.py` (C103) is already a soft gate — 2 cards with a dismiss button. C163 extends this to multi-step micro-lessons, but the dismiss option must remain.

**The risk**: If C163 is a HARD gate (must complete before seeing data), it will reduce engagement. If C163 is a SOFT gate (can dismiss, but encourages learning), it will increase retention.

**Verdict: DOES NOT CREATE BARRIER if designed as soft gate.** C163 must have a dismiss option. The gate should encourage, not require. The Tastytrade model proves this works.

### 3.3 — Is "beginner/expert mode" (C40) just a show/hide toggle dressed up as a feature?

**The concern**: C40 could be a simple "show more/less sections" toggle with no real value.

**The counter-argument**: C40 is more than show/hide. It's a complexity management system that affects:
1. Which sections are visible (beginner sees hero sections only)
2. How much detail is shown in each section (beginner sees summaries, expert sees full data)
3. Whether glossary tooltips are auto-shown (beginner sees glossary, expert doesn't)
4. Whether the onboarding gate appears (beginner sees C163, expert doesn't)

**The evidence**: The C105 toggle already exists in `_main.py` (line 208). C40 extends this to a full mode system with persistence, section-level control, and glossary integration. This is a meaningful enhancement, not a cosmetic change.

**However**: The design spec must define what "beginner view" and "expert view" mean for EACH section. Without this spec, C40 risks becoming a binary show/hide toggle. The design reviewer flagged this: "the mode concept needs careful scoping to avoid becoming a 'show/hide all' toggle."

**Verdict: NOT JUST A TOGGLE, but requires a per-section design spec.** C40 is a real feature IF each section has a defined beginner view and expert view. Without this spec, it risks being a binary toggle. The shared "beginner experience spec" (from the discussion round) must be written before C40 implementation.

### 3.4 — What are the top 3 risks for Sprint 20?

**Risk 1: Content creation bottleneck (HIGH probability, HIGH impact)**
Both C167 and C163 require content creation. C167 needs ~15-20 narrative templates for screener outcomes. C163 needs 3-5 educational cards for the onboarding gate. The discussion round's mitigation plan (PM writes C163 templates during Sprint 19, Designer writes C163 cards before Sprint 20 Day 3) is good but depends on PM/Designer availability. If content is not ready, features will use placeholders and quality will suffer.

**Mitigation**: Placeholder templates (3-5 instead of 15-20) with expansion in Sprint 21. This is already in the plan.

**Risk 2: C40/C163 integration complexity (MEDIUM probability, HIGH impact)**
C163 defines what "beginner" means through onboarding. C40 extends that into a persistent mode preference. If these are built independently, the definitions may conflict. The discussion round's mitigation (shared "beginner experience spec") is correct but the spec hasn't been written yet.

**Mitigation**: Write the shared spec BEFORE either feature is implemented. This is a prerequisite, not a parallel task.

**Risk 3: C167 tone drift (LOW probability, MEDIUM impact)**
C167's explanations could drift from historian tone ("this is what happened") to recommendation tone ("you should buy this"). This is a subtle risk that's hard to catch in code review. The disclaimer helps but doesn't prevent tone drift in the explanation text itself.

**Mitigation**: Tone QA audit of all C167 templates before release. Use the existing tone QA framework (from Sprint 19's tone QA work).

### Round 3 Verdict

| Item | Challenge | Verdict |
|------|-----------|---------|
| C167 vs historian positioning | Contradicts? | ✅ No — but requires careful tone management |
| C163 barrier to entry | Reduces engagement? | ✅ No — if designed as soft gate with dismiss option |
| C40 just a toggle? | Dressed up feature? | ⚠️ Not just a toggle, but needs per-section design spec |
| Top 3 risks | What are they? | 1) Content bottleneck, 2) C40/C163 integration, 3) C167 tone drift |

**Confirmed**: C167 doesn't contradict historian positioning. C163 doesn't create barriers if soft gate.
**Challenged**: C40 needs more than a toggle — it needs a per-section spec.
**Needs revision**: The shared "beginner experience spec" must be written before C163/C40 implementation.

---

## Final Verdict

### ✅ CONFIRMED with 5 conditions

The Sprint 20 plan (C167 + C163 + C40) is **confirmed** as the right scope, with the following conditions:

**Condition 1: Remove the C152 swap condition.**
The C152 spike was deferred from Sprint 19, not completed. There are no artifacts to evaluate. The swap condition is void. C152 should be planned for Sprint 21 based on a new spike.

**Condition 2: Integrate C170 (Tappable Glossary) into C40 (Beginner/Expert Mode).**
C170 should not be a standalone 4th feature. It should be a component of C40's beginner mode. This keeps the sprint within budget (32-46h with integration savings) and creates a cohesive beginner experience.

**Condition 3: Write the shared "beginner experience spec" before C163/C40 implementation.**
This spec must define what "beginner" means for both features: what content is shown, what the onboarding gate teaches, and how the mode toggle affects each section. This is a prerequisite, not a parallel task.

**Condition 4: C163 must REPLACE first_visit_guide.py, not coexist with it.**
Having both C163 and the existing C103 first visit guide would be confusing. C163 should absorb C103's role and extend it. The old `first_visit_guide.py` should be removed or refactored into C163.

**Condition 5: Do D-118 and D-120 as Day 1 infrastructure cleanup.**
D-118 (add severity field to case_study_library.yaml, 0.5h) and D-120 (extract INDUSTRY_BENCHMARKS to YAML, 1-2h) should be done on Day 1 before feature coding begins. Total: 1.5h. This prevents future bugs and keeps the codebase clean.

---

## Sprint 20 Final Plan (Post-Challenge)

### Features

| Priority | Feature | Effort | Notes |
|----------|---------|--------|-------|
| **P1** | **C167: AI Screener Explanations** | 12-16h | Add plain-language narratives to existing screener results. Uses existing `TemplateExplanationProvider` pattern. Historian tone with disclaimer. |
| **P1** | **C163: Learn First Gate** | 10-14h | Multi-step onboarding gate with micro-lessons. Soft gate (dismissible). Replaces `first_visit_guide.py`. Must complete shared "beginner experience spec" first. |
| **P2** | **C40: Beginner/Expert Mode** (includes C170 Tappable Glossary) | 10-16h | Extends C105 toggle with persistence, per-section control, and integrated glossary. Beginner mode includes auto-shown glossary tooltips. |

### Infrastructure (Day 1)

| Item | Effort | Notes |
|------|--------|-------|
| D-118: Add severity field to case_study_library.yaml | 0.5h | Quick consistency fix |
| D-120: Extract INDUSTRY_BENCHMARKS to YAML | 1-2h | Prevents 3-file synchronization bugs |
| Shared "beginner experience spec" | 1-2h | Prerequisite for C163/C40 |

### Total Effort

| Component | Low | High |
|-----------|-----|------|
| C167 | 12h | 16h |
| C163 | 10h | 14h |
| C40 + C170 (integrated) | 10h | 16h |
| Infrastructure (D-118 + D-120 + spec) | 2.5h | 4.5h |
| **Total** | **34.5h** | **50.5h** |

**Midpoint: 42.5h** — within the original 30-42h budget at the midpoint, with the upper bound 8.5h over. The integration savings from combining C40 + C170 (vs. standalone) bring the total within a manageable range.

### Removed Items

- **C152 swap condition**: Removed (spike was deferred, no artifacts to evaluate)
- **C170 as standalone feature**: Integrated into C40
- **C175**: Duplicate of C163, removed

### Deferred Items

- **C171 (Valuation Band Chart)**: Sprint 21
- **C172 (Concept Comparison)**: Sprint 22+
- **C173 (Visual Calculators)**: Sprint 22+
- **C174 (Sector Storytelling)**: Sprint 21+
- **C152 (Multi-Factor Event Narratives)**: Sprint 21 (new spike required)
- **D-117 (events.yaml negative events)**: Content task, do alongside C167 if time permits
- **D-119 (pattern_detector.py redundancy)**: No action needed

---

## Top 3 Risks

### 1. 🔴 Content Creation Bottleneck (HIGH Probability, HIGH Impact)
**What**: C167 needs ~15-20 narrative templates. C163 needs 3-5 educational cards. If PM/Designer content delivery is delayed, features will ship with placeholder content, reducing quality.
**Mitigation**: Placeholder templates (3-5 instead of 15-20) with expansion in Sprint 21. PM writes C167 templates during Sprint 19 remaining time. Designer writes C163 cards before Sprint 20 Day 3.
**Early warning**: If content is not ready by Day 3, reduce C167 scope to 3 preset explanations (value, growth, dividend) instead of free-form screening.

### 2. 🟡 C40/C163 Integration Complexity (MEDIUM Probability, HIGH Impact)
**What**: C163 defines "beginner" through onboarding content. C40 extends "beginner" into a persistent mode. If these definitions conflict, the user experience will be incoherent.
**Mitigation**: Write the shared "beginner experience spec" BEFORE either feature is implemented. This spec defines: (a) what "beginner" means, (b) what content is shown in each mode, (c) how C163's lessons map to C40's mode behavior.
**Early warning**: If the spec is not written by Day 2, pause C163/C40 development and write it first.

### 3. 🟡 C167 Tone Drift (LOW Probability, MEDIUM Impact)
**What**: C167's explanations could drift from historian tone ("this is what happened") to recommendation tone ("you should buy this"). This is subtle and hard to catch in code review.
**Mitigation**: Tone QA audit of all C167 templates before release. Use the existing tone QA framework. Every template must pass the "historian test": does it describe without recommending?
**Early warning**: If any template uses words like "應該," "建議," "買," "賣," it fails the historian test and must be rewritten.

---

## Summary

The Sprint 20 plan is **sound but needs refinement**. The core three features (C167, C163, C40) are the right priorities. The key changes from the challenge:

1. **Remove the C152 swap condition** (spike was deferred, not completed)
2. **Integrate C170 into C40** (don't add as standalone 4th feature)
3. **Write the shared "beginner experience spec"** before C163/C40 implementation
4. **C163 replaces first_visit_guide.py** (don't coexist)
5. **Do D-118 + D-120 on Day 1** as infrastructure cleanup

The sprint advances the "historian" positioning through C163 (teach before data) and C167 (narrative explanations). C40 enables both by providing a beginner mode that defaults to the historian experience. This is a cohesive sprint that builds the onboarding and explanation layers while preserving the historian core.

---

*Report generated: 2026-06-14*
*Reviewer: Challenger (Review Round 40)*
*Next: Development Round 41 — Sprint 20 execution*
