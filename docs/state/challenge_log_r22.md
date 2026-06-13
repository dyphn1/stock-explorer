# Challenge Log — Round 22

> **Date**: 2026-06-13
> **Challenger**: Challenger Role
> **Scope**: Round 22 Review Report — Sprint 9 post-implementation review + Sprint 10 plan
> **Context**: Sprint 9 (C98 + C101 + C103 Lite) complete. Sprint 10 planned: C34 + C105 + M5 remediation + D-061.

---

## Round 1: Gap Authenticity Challenge

### Challenger Questions:

**Q1: Are C107-C112 genuine gaps or feature creep?**

The competitor research identifies 6 new feature gaps (C107-C112) from 10 new competitors. Let me examine each:

- **C107 (Inline AI Explanations, P1, 12-16h)**: This is described as extending C98 with a frontend UX pattern. But C98 was *just* delivered in Sprint 9 as a template-only engine. C107 proposes adding AI-generated explanations — which requires the LLM abstraction layer (D5) that has been deferred since Sprint 1. The competitor research says "Spiking and Busyu both offer AI explanations" but those are AI-native platforms, not template-first. **This is premature**: we haven't even validated that users want more narrative from our template-based C98 before layering AI on top. C107 conflates two separate decisions: (a) inline "Why" card UX, and (b) AI-generated vs. template-generated content. These should be decoupled.

- **C108 (Insider Trading, P2, 10-14h)**: Spiking covers this for ASEAN markets. But Stock Explorer's TW market focus means we'd need TWSE insider holding data (internal人持有). This is a genuine data availability question, not just a feature gap. **Is the data even accessible via FinMind for TW stocks?** If not, this gap is theoretical.

- **C109 (Compare Timelines, P2, 14-18h)**: Cake has "Compare Stories" for ASEAN stocks. But C38 (Compare Stories) is already in the backlog. C109 is C38 + C34 combined. **This is a compound feature being presented as a gap.** It should be noted as "C38 prerequisite: C34 timeline" rather than a new gap.

- **C110 (Earnings Story, P1, 14-18h)**: Also labeled C94 from Round 17. This has been identified 5 rounds ago and never built. **At what point does a "gap" become a "deliberate omission"?** If earnings stories are P1, why weren't they in Sprint 9 alongside C98 (Event Interpretation)? The answer is probably scope management, but the research doesn't acknowledge this tension.

- **C111 (Badge System, P2, 8-12h)**: C60 (Concept Mastery Badges) from Round 12. Same as C110 — this is a resurrected gap, not a new one. The research says "no TW stock platform has badges" but **is gamification aligned with "historian, not stock picker"?** Badges incentivize engagement, not understanding. This could actually conflict with the core positioning.

- **C112 (Investment Diary, P2, 10-14h)**: C55 from Round 12. The "historian twist" (educational diary vs. trading diary) is clever, but **does Streamlit support persistent user data?** The research notes "stored in session state" — which means data is lost on browser close. A diary that disappears isn't a diary.

**Verdict on C107-C112**: 3 of 6 are resurrected gaps (C110/C94, C111/C60, C112/C55), not new. C109 is a compound of C38+C34. C107 is premature (requires D5). Only C108 might be genuinely new, but data availability is unverified. **The 6 "new gaps" overstate the new information content.**

**Q2: Does Tiger Brokers' competition change our priority?**

The research identifies Tiger Brokers as "the most direct competitive threat" due to TW market expansion, "Stock Stories," and "Tiger Academy." The recommended response: "C34 is MORE important than ever" and "Sprint 10 should prioritize C34 as the #1 feature."

**Challenge**: Tiger Brokers is a *trading platform* with education features. Stock Explorer is an *education platform* with no trading. Tiger's "Stock Stories" are short narratives for traders. Stock Explorer's C34 (Company Story Timeline) is a deep educational tool. **These are different products serving different needs.** The competitive threat is real but the response should be differentiation, not imitation. Prioritizing C34 because Tiger has "Stock Stories" conflates competitive awareness with competitive panic.

Moreover, Tiger's advantages (mobile app, social features, fractional shares) are *structural* — they can't be addressed by prioritizing C34. **The research doesn't explain how building a timeline feature counters Tiger's mobile app advantage.**

**Q3: Is M5 remediation still the right priority after 5+ sprints of "pre-existing" failures?**

The 10 L1 event-alert failures have been "pre-existing" since Sprint 7 (at least 5 sprints). The architect's root cause analysis identifies 4 causes, with the primary one being a try/except that silently swallows errors. The remediation estimate is 8-12h.

**Challenge**: If the root cause is truly just a try/except suppression (Cause 1), this should take 2-3h to fix, not 8-12h. The inflated estimate suggests the architect knows the try/except is a symptom, not the disease. **What are the other 3 causes actually costing in effort?** The research says Cause 4 (no events in test data) is "High" impact — but that's a test data problem, not a code problem. Are we fixing the code or the tests?

More fundamentally: **M5 is the adaptive event detection engine — the core of the product's "adaptive and self-evolving" value proposition.** If it's been broken for 5+ sprints, why is it only now being remediated? The answer (Sprint 10 plan) is fine, but the research should acknowledge that this is 5 sprints of a broken core feature, not just "pre-existing failures."

**Q4: Is C34 Option B (custom HTML/CSS) the right approach given the "no inline HTML" principle?**

The architect recommends Option B: custom HTML/CSS timeline with a reusable `_timeline_event()` helper in `_router_base.py`. The designer recommends a `_timeline_event_card()` component. Both agree on encapsulating the HTML.

**Challenge**: The architect's Option B explicitly notes "50-80 lines of inline HTML in page code (violates D3 pattern)" as a con, then recommends it anyway with the mitigation of a reusable helper. But **the reusable helper IS the inline HTML** — it just moves it from the page to `_router_base.py`. This doesn't eliminate inline HTML; it relocates it. The designer's `_timeline_event_card()` proposal is better because it suggests a card-based layout using existing design system components, not custom HTML/CSS.

**The real question**: Why is Option A (st.expander chain) dismissed as "underwhelming UX" when it's pure Streamlit, zero inline HTML, and follows the existing progressive disclosure pattern (C44 uses st.expander successfully)?** The "underwhelming" judgment is aesthetic, not functional. For a "historian" platform, a clean expander-based timeline may be more appropriate than a flashy CSS timeline.

### Team Response (Anticipated):

**On C107-C112**: The team would likely argue that resurrected gaps (C110, C111, C112) are validated by new competitor evidence, not just recycled. C107 is a genuine new insight from Spiking/Busyu. C108 needs data availability verification before scheduling.

**On Tiger Brokers**: The team would argue that competitive awareness should accelerate existing priorities, not change them. C34 was already planned; Tiger's "Stock Stories" just confirms the direction.

**On M5**: The team would argue that the root cause analysis is new (this sprint), and the 8-12h estimate includes test infrastructure (D-061) and test-mode event injection, not just the try/except fix.

**On C34 Option B**: The team would argue that a reusable helper in `_router_base.py` is architecturally sound — it encapsulates the HTML in one place, making it maintainable and testable. The helper approach follows the same pattern as `_info_card()` and `_白话_card()`.

### Round 1 Verdict: ⚠️ PARTIALLY VALIDATED

- C107-C112: **Overstated**. Only ~2-3 are genuinely new insights. C107 is premature without D5. C111 may conflict with historian positioning.
- Tiger Brokers: **Valid competitive threat but overstated urgency**. C34 priority is correct but not because of Tiger.
- M5: **Valid priority but under-analyzed delay**. 5 sprints of broken core feature needs acknowledgment, not just root cause.
- C34 Option B: **Questionable**. Option A (expander) may be more aligned with design principles. The "reusable helper" for Option B is just relocated inline HTML.

---

## Round 2: Priority Challenge

### Challenger Questions:

**Q1: Should Sprint 10 focus on C34 first, or M5 remediation first?**

The Sprint 10 plan lists: C34 (Company Story Timeline) + C105 (Simple/Detailed Toggle) + M5 remediation + D-061 (test infra). The architect's top 3 recommendations rank: (1) D-062 quiz engine extraction, (2) C34 timeline, (3) M5 + test infra. The competitor research says "C34 is MORE important than ever" and "M5 remediation should include C107 as a prerequisite."

**Challenge**: There are three different priority orderings from three different reviews:
- Architect: D-062 → C34 → M5
- Designer: (implicit) Fix inline HTML first → C34 components → C105
- QA/Competitor: C34 #1 → M5 + C107

**These don't agree.** The architect puts D-062 first (1-2h, low risk, high leverage). The competitor research puts C34 first (strategic urgency). The designer implies debt clearance before new features.

**The key question**: M5 is a broken core feature. C34 is a new feature. **Should we build new features on a broken foundation?** If M5's event detection is silently failing (try/except suppression), then C34's timeline — which depends on `adaptive_engine.get_events_for_stock()` — may also be unreliable. Building C34 before fixing M5 is like building a house on a cracked foundation.

**Q2: Is D-062 (quiz engine extraction) really the first task, or should it be deferred?**

The architect recommends D-062 as "first task of Sprint 10" (1-2h). The reasoning: "Before C105 adds more quiz-like features, extract a shared quiz_engine.py to prevent further duplication."

**Challenge**: C105 is a content depth toggle, not a quiz feature. C105 doesn't add quiz-like features — it shows/hides content sections. **The architect's justification for D-062 is based on a false premise.** The actual duplication is between C101 (comprehension quiz) and C85 (financial wellness quiz). If neither C105 nor C34 adds more quiz patterns, the duplication is static — it won't grow. D-062 is a nice-to-have refactoring, not a blocker.

**Moreover**: D-062 is 1-2h, but it requires refactoring two existing services (`comprehension_quiz_service.py` and `financial_wellness_service.py`) and their tests. With zero test coverage for these services (the architect notes "new services untested"), refactoring without tests is risky. **Shouldn't D-061 (test infrastructure) come before D-062 (refactoring untested code)?**

**Q3: Are we adding too many new features (C107-C112) when Sprint 10 isn't complete?**

The competitor research identifies 6 new feature gaps. The Sprint 10 plan already has 4 items (C34 + C105 + M5 + D-061). The architect estimates C34 at 14-18h, C105 at 10-14h, M5 at 8-12h, D-061 at 3-4h. Total: 35-48h.

**Challenge**: If Sprint 9 took ~37-51h (per the Round 21 plan), Sprint 10's 35-48h is already at capacity. **There is zero room for C107-C112.** The competitor research doesn't acknowledge this. It presents 6 new gaps without discussing sprint capacity or trade-offs. This is the classic "competitor research fallacy" — identifying every possible gap without prioritizing based on capacity.

**The real question**: Should C107 (Inline AI Explanations, 12-16h) replace C34 in Sprint 10? The competitor research implies yes ("M5 remediation should include C107 as a prerequisite"). But C107 requires D5 (LLM abstraction), which is deferred. **The research is recommending a feature that depends on a deferred prerequisite.**

### Team Response (Anticipated):

**On C34 vs M5 priority**: The team would likely argue that M5 remediation and C34 can proceed in parallel — M5 is a code fix while C34 is a new page. Different developers can work on each. The dependency (C34 uses M5 data) is real but manageable since C34 can use mock/test data during development.

**On D-062 timing**: The team would argue that D-062 is a quick win (1-2h) that can be done on Day 1 before any other work starts. It's not blocking anything, but it's low-risk and prevents future pain. The test coverage concern is valid but D-062 is a pure refactoring — the external behavior doesn't change.

**On capacity**: The team would argue that C107-C112 are for future sprints (11+), not Sprint 10. The competitor research is directional, not a Sprint 10 scope change.

### Round 2 Verdict: ⚠️ PRIORITY CONFLICTS IDENTIFIED

- C34 vs M5: **M5 should come first** (or at minimum, M5 fix before C34 integration). Building timeline on broken event detection is risky.
- D-062: **Justification is weak** (C105 doesn't add quiz features). D-062 should be deferred to Sprint 11 unless there's a genuine near-term need.
- Capacity: **C107-C112 are not Sprint 10 scope**. The research should explicitly state this to avoid scope creep.
- D-061 before D-062: **Test infrastructure should precede refactoring of untested code.**

---

## Round 3: Goal Alignment Challenge

### Challenger Questions:

**Q1: Does the overall Sprint 10 direction align with "historian, not stock picker"?**

Sprint 10 plan: C34 (Company Story Timeline) + C105 (Simple/Detailed Toggle) + M5 remediation + D-061 (test infra).

**Assessment**:
- C34 (Timeline): ✅ Strong alignment. A company story timeline is the essence of "historian" — showing what happened over time without predicting the future.
- C105 (Toggle): ✅ Strong alignment. Beginner-first positioning demands complexity adaptation. The toggle serves beginners (simple mode) and advanced users (detailed mode).
- M5 remediation: ✅ Strong alignment. "Adaptive and self-evolving" (core value #3) requires working event detection.
- D-061 (Test infra): ✅ Indirect alignment. Quality infrastructure supports all features.

**However**: The competitor research's suggested additions (C107-C112) include some misaligned items:
- C111 (Badge System): ⚠️ Gamification may conflict with "historian" positioning. Badges incentivize engagement metrics, not understanding. "Historian" is about depth, not streaks.
- C108 (Insider Trading): ⚠️ Insider trading data can easily slip into "smart money is buying = you should buy" territory. The research claims it would be "historian positioned" but the line is thin.
- C112 (Investment Diary): ⚠️ Even with a "historian twist," a diary feature risks becoming "what I think about this stock" rather than "what I learned about this company."

**Q2: Are we maintaining beginner-first positioning with C34 (timeline) and C105 (toggle)?**

**C34 (Timeline)**: The architect's Option B (custom HTML/CSS timeline) is visually compelling but may be too complex for beginners. A timeline with 20+ events, color-coded severity, and drill-down interpretations could overwhelm a novice. **Has anyone tested whether beginners understand timeline visualizations?** The designer's recommendation (card-based layout, max 5-7 events, "載入更多" button) is more beginner-friendly than the architect's full timeline.

**C105 (Toggle)**: Defaulting to "simple" mode is correct. But the architect notes "which pages get the toggle? Business card page is the obvious first target (15+ sections)." **15+ sections on a single page is the opposite of beginner-first.** The toggle is a band-aid for page overload (D-005). The real fix is reducing content per page, not adding a toggle to manage it.

**Q3: Is the design grade A still justified given 5 new P2 issues?**

The designer recommends "Maintain A" with the condition that D-062/D-064/D-065 are fixed in Sprint 10. The designer notes:
- C103 Lite is "exemplary" (zero inline HTML)
- C101 is "well-structured" (80% shared components)
- C98 is "architecturally sound" (minor inline HTML)
- Net inline HTML: Sprint 8 removed 150+ lines, Sprint 9 added ~20 lines

**Challenge**: The design grade A was assigned in Round 21 because Sprint 8 "closed the inline HTML enforcement gap." Sprint 9 reopened it with 3 new inline HTML instances. The designer calls these "minor and structural, not visual" — but **the whole point of the A- downgrade in Round 20 was that inline HTML enforcement was the metric.** You can't downgrade for inline HTML in Round 20, then ignore new inline HTML in Round 22 and keep the A.

**The counter-argument**: The *trend* is still positive (150 removed vs. 20 added). The new instances are in new pages, not regressions of previously-clean pages. And the designer's condition ("fix in Sprint 10") is reasonable.

**My assessment**: The A is borderline. The condition should be stricter: **"Maintain A only if D-062, D-064, D-065, and D-066 are all fixed in Sprint 10. If any remain open, downgrade to A-."** D-066 (adaptive banner inline HTML) is pre-existing and explicitly listed for Sprint 10 — it should be included in the condition.

### Team Response (Anticipated):

**On historian alignment**: The team would argue that C107-C112 are future-sprint considerations, not Sprint 10 scope. Sprint 10's 4 items are all strongly aligned. The badge system (C111) can be designed to reward learning milestones (e.g., "Understood ROE") rather than engagement metrics.

**On beginner-first**: The team would argue that C105's toggle *is* the solution to page overload — it lets beginners see a simple view while preserving advanced content. The alternative (removing content) sacrifices depth for advanced users.

**On design grade**: The team would argue that 3 new instances in 35 lines vs. 150+ lines removed is a net positive. The A is justified by the overall trajectory, not any single sprint.

### Round 3 Verdict: ⚠️ CONDITIONALLY ALIGNED

- Sprint 10 core (C34 + C105 + M5 + D-061): ✅ Strong alignment with "historian, not stock picker"
- C107-C112 additions: ⚠️ Some misaligned items (C111 badges, C108 insider data). Need historian-positioning review before implementation.
- Beginner-first: ⚠️ C105 toggle is a band-aid for page overload. C34 timeline needs beginner testing.
- Design grade A: ⚠️ Borderline. Condition should include D-066 (pre-existing) alongside D-062/D-064/D-065.

---

## Final Challenger Decision

### ⚠️ REVISED — Sprint 10 plan is sound but needs 4 revisions

### Required Revisions:

1. **M5 remediation before C34 integration**: M5's event detection must be fixed (at minimum, the try/except suppression in Cause 1) before C34's timeline integrates with live M5 data. C34 can be *developed* in parallel using test data, but *integration* should wait for M5 fix. This is a sequencing constraint, not a priority change.

2. **D-061 (test infrastructure) before D-062 (quiz engine refactoring)**: Refactoring untested code without test coverage is risky. D-061's conftest.py and service tests should be in place before D-062 refactors `comprehension_quiz_service.py` and `financial_wellness_service.py`. Estimated resequencing: D-061 first (3-4h), then D-062 (1-2h), then C34/C105/M5.

3. **C107-C112 are explicitly NOT Sprint 10 scope**: The competitor research should include a clear statement that C107-C112 are directional inputs for Sprint 11+ planning, not Sprint 10 scope additions. C107 specifically requires D5 (LLM abstraction) as a prerequisite and should not be implicitly bundled with M5 remediation.

4. **Design grade A condition strengthened**: The "Maintain A" condition should include all 4 inline HTML items (D-062, D-064, D-065, and pre-existing D-066). If any remain unfixed after Sprint 10, the grade drops to A-. This closes the loophole where pre-existing issues are excluded from the condition.

### Approved Sprint 10 Scope:

| Order | Item | Hours | Type | Dependency |
|-------|------|-------|------|------------|
| 1 | D-061: Test infrastructure (conftest.py, pytest config, service tests) | 3-4h | Debt | None |
| 2 | D-062: Quiz engine extraction | 1-2h | Debt | D-061 (test coverage first) |
| 3 | D-063: Remove unused import (first_visit_guide.py) | <0.1h | Debt | None |
| 4 | M5 remediation: Fix try/except suppression + test-mode event injection | 8-12h | Debt | D-061 (test infra) |
| 5 | C34: Company Story Timeline (Option B with reusable helper) | 14-18h | Feature | M5 fix (for live data integration) |
| 6 | C105: Simple/Detailed Toggle (business card page only) | 10-14h | Feature | None |
| 7 | D-064 + D-065 + D-066: Fix inline HTML (quiz result cards, key concept, disclaimer, adaptive banner) | 1-2h | Debt | None |
| **TOTAL** | | **37-52h** | | |

### Notes on Approved Scope:

- **C34 approach**: Option B (custom HTML/CSS with reusable `_timeline_event()` helper) is approved, but the helper should follow the design system's card patterns as closely as possible. The designer's recommendation of `_timeline_event_card()` using `_summary_card()` as a base is preferred over raw CSS.
- **C105 scope**: Business card page only. Defer other pages to Sprint 11. Default to "simple" mode.
- **M5 remediation**: Focus on Cause 1 (try/except suppression) and Cause 4 (test-mode event injection). Causes 2 and 3 are lower priority and can be addressed in Sprint 11.
- **D-065 (session state)**: Document all session state keys in a comment block in `main.py`. Defer the session state manager (D28) to Sprint 11.
- **C107-C112**: To be evaluated for Sprint 11+ during the next review cycle. C107 requires D5 (LLM abstraction) as a prerequisite. C111 (badges) needs historian-positioning review.

---

*Challenger Round 22 — 2026-06-13*
*Next challenge: Round 23 (after Sprint 10)*
