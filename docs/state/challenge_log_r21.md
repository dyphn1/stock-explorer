# Challenge Log — Review Round 21

## Team Preliminary Decision Under Challenge

**Review Round 21 Consolidated Findings:**
- Design Grade: A (upgraded from A-)
- 3 new features: C104 (P2, 8-12h), C105 (P2, 10-14h), C106 (P2, 16-22h)
- 5 new debt items: D-057 (HIGH), D-058 (Medium), D-059 (Medium), D-060 (Medium), D-061 (Medium)
- Sprint 9 plan: D-057 (Day 1) + C103 Lite + C101 + C98 = 37-51h
- Sprint 10 plan: C34 + C105 + C106 + M5 remediation + D-061 + D6 = 56-80h

---

## Round 1: Gap Authenticity Challenge

### Challenger Questions

**Q1.1 — C104 and C101 overlap: Are these really two separate features?**

The QA Engineer's own analysis states: "C104 is the **implementation specification** for C101. C101 defined the feature concept; C104 defines the specific UX pattern (Finimize-style embedded quiz cards)." If C104 is the implementation of C101, they should not be separate backlog items. Having both creates confusion about what to build and risks double-counting effort. **Should the team merge C104 into C101 and treat the Finimize-style embedded quiz card pattern as the accepted C101 design?**

**Q1.2 — C105 (Simple/Detailed Toggle): Is this the most strategically valuable feature in the entire backlog?**

The competitor analysis shows that NO TW competitor offers a complexity toggle. Finimize's ELI5 mode and Stash's 8th-grade writing level both solve the same problem Stock Explorer faces. The D-032 progressive disclosure gap has been open since Sprint 13. C105 directly addresses it with a simpler mechanism than progressive disclosure. **Should C105 be elevated to P1 and prioritized for Sprint 9, potentially replacing C103 Lite?**

**Q1.3 — C106 (First 7 Days): Is this too large for any single sprint?**

At 16-22h, C106 is the largest single feature proposed. Combined with C34 (16-24h) and M5 remediation (8-12h), Sprint 10 would have 40-58h of work before adding C105, D-061, and D6. **Should C106 be split into smaller deliverables (e.g., C106a: Days 1-3, C106b: Days 4-7) to reduce sprint risk?**

### Team Responses

**Response to Q1.1**: The team agrees C104 and C101 describe the same feature at different specificity levels. C101 was the concept (approved Round 20); C104 is the implementation spec (Finimize model, this round). The team merges C104 into C101. The C101 effort estimate already includes the embedded quiz card pattern (8-12h covers both the quiz engine and the per-section card rendering).

**Response to Q1.2**: The team acknowledges C105's strategic value but maintains P2 for now. C105 requires wrapping every section in a conditional, which is a significant refactoring of the business card page. The team recommends Sprint 10 for C105, after C98/C101/C103 prove the education-layer concept. If C105 were added to Sprint 3, the total would exceed 51h. The team does NOT replace C103 Lite with C105 — C103 Lite is a quick win (8-11.5h) that can be built in the first part of the sprint while the C98 spike runs.

**Response to Q1.3**: The team agrees C106 is large but notes that it's a content-heavy feature (7 micro-lessons with TW stock examples) rather than a complex engineering challenge. The 16-22h estimate includes content creation (writing 7 lessons with analogies and examples). The team does NOT split C106 — splitting a curriculum into partial deliverables creates a worse user experience (Days 1-3 without Days 4-7 is incomplete). C106 stays as a single Sprint 10 feature.

### Round 1 Verdict

**⚠️ PARTIALLY REVISED** — C104 should be merged into C101 (they're the same feature). C105's strategic value is acknowledged but Sprint 10 timing is correct. C106 should not be split (content coherence).

---

## Round 2: Priority Challenge

### Challenger Questions

**Q2.1 — D-057 (LLM abstraction): Is the 2-3h estimate realistic?**

Creating an LLM abstraction layer involves: (1) defining a protocol/ABC, (2) refactoring existing template engines as fallback, (3) creating an LLM provider adapter, (4) testing the integration. This is 3-4h of work, not 2-3h. **If D-057 takes 3-4h and is a Day 1 prerequisite, does this push C98 development later in the sprint, increasing the risk of C98 not being completed?**

**Q2.2 — D-061 (test infrastructure): When does "deferrable" become "blocker"?**

D-13 (test infrastructure) has been deferred since Round 14. It's now been 7 sprints. With 22 service modules and 33 page modules, the regression surface is growing every sprint. **Should D-061 be elevated to a hard Sprint 10 commitment (not "deferrable")? What is the concrete trigger for making test infrastructure a blocker?**

**Q2.3 — Sprint 10 scope: Is 56-80h realistic for a single sprint?**

The Sprint 10 plan includes C34 (16-24h) + C105 (10-14h) + C106 (16-22h) + M5 remediation (8-12h) + D-061 (3-4h) + D6 (3-4h) = 56-80h. Even at the lower bound (56h), this is more than a typical 2-week sprint (50h). **Should the team cut one feature from Sprint 10, or accept the upper-bound risk?**

### Team Responses

**Response to Q2.1**: The team revises D-057 to 3-4h. This is absorbed into the Sprint 9 plan by starting D-057 on Day 1 while the C98 spike runs in parallel (the spike is a 2h research task, not a coding task). The revised Sprint 9 total becomes 37-51h (with D-057 at 3-4h instead of 2-3h), which still fits within the developer's 44.5-51.5h estimate.

**Response to Q2.2**: The team commits D-061 as a **hard Sprint 10 commitment**, not deferrable. The trigger is: 22 service modules with zero test coverage. If Sprint 10 doesn't include D-061, it will be escalated to a blocker for Sprint 11.

**Response to Q2.3**: The team acknowledges the Sprint 10 scope is aggressive. The plan is: C34 + C105 + M5 remediation as the core (34-48h), with C106 + D-061 + D6 as stretch goals. If the sprint is on track at midpoint, all items proceed. If behind, C106 is the first cut (deferred to Sprint 11).

### Round 2 Verdict

**⚠️ REVISED** — D-057 estimate revised to 3-4h. D-061 is a hard Sprint 10 commitment. Sprint 10 scope is aggressive with C106 as the explicit cut candidate.

---

## Round 3: Goal Alignment Challenge

### Challenger Questions

**Q3.1 — Does the Sprint 9 plan advance "story first, data second"?**

The product vision's Core Value #1 is "Story first, data second." Sprint 9 delivers: C98 (event interpretations — narrative layer on events), C101 (quiz — comprehension verification), C103 Lite (onboarding — first impression). C98 directly advances "story first" by converting raw event data into narrative interpretations. C101 and C103 support the story-first approach by ensuring users understand and retain the narratives. **Does the team believe this combination advances the story-first vision more than C34 (Company Story Timeline) would?**

**Q3.2 — Does the design grade upgrade to A align with the product vision's "ten-second test"?**

The product vision requires: "Every explanation must pass the ten-second test: a beginner can restate the core concept within ten seconds." The design grade upgrade to A is based on closing the inline HTML gap, not on verifying the ten-second test. **Has the team verified that the current business card page passes the ten-second test? If not, should the design grade be A- until the ten-second test is verified?**

**Q3.3 — Is the competitor research process still aligned with the product vision?**

The competitor research has analyzed 90 competitors and identified 106 feature gaps. But the product vision explicitly states: "Just because competitors have it doesn't mean we should too." The research process identifies gaps but doesn't always filter through the "historian" lens. **Is the team confident that the 106 identified features all pass the "historian filter"? Or are there features in the backlog that should be rejected?**

### Team Responses

**Response to Q3.1**: The team maintains that C98 is a prerequisite for C34. You can't build a coherent company story timeline (C34) without first having event interpretation (C98). C98 converts raw events into narratives; C34 weaves those narratives into a chronological story. The Sprint 9 → Sprint 10 progression (C98 → C34) is the correct sequence for advancing "story first."

**Response to Q3.2**: The team acknowledges that the ten-second test hasn't been formally verified with users. However, the design grade is based on design system quality and consistency, not on user testing. The ten-second test is a product vision principle that should be verified through user research (M1 milestone), not through design review. The team maintains the A grade for design system quality while noting that ten-second test validation is a separate activity.

**Response to Q3.3**: The team reviews the 106 features and confirms that C100 (Natural Language Screener) and C102 (Market Narrative Feed) were already rejected for contradicting historian positioning. The remaining 104 features have been filtered through the historian lens. The team notes that C86 (AI Narrative Agent) and C88 (Market Narrative Feed — different from C102) should be reviewed for historian alignment. No bulk rejections are needed.

### Round 3 Verdict

**✅ CONFIRMED** — The Sprint 9 plan correctly sequences C98 before C34. The design grade A is justified for design system quality (ten-second test validation is a separate activity). The competitor research filtering is adequate with 2 explicit rejections.

---

## Required Revisions (Summary)

The challenger required the following specific revisions before confirming:

1. **Merge C104 into C101** — They are the same feature at different specificity levels. C101 effort (8-12h) already covers the embedded quiz card pattern.

2. **D-057 estimate revised to 3-4h** — Creating a protocol ABC + template fallback + LLM provider adapter + testing is 3-4h, not 2-3h.

3. **D-061 scheduled as hard Sprint 10 commitment** — No longer deferrable. 22 service modules with zero test coverage is the trigger.

4. **Sprint 10 scope: C106 is explicit cut candidate** — If the sprint is behind at midpoint, C106 is deferred to Sprint 11.

---

## Final Verdict

✅ **CONFIRMED** — The Review Round 21 findings are confirmed after 3 rounds of challenge with 4 required revisions adopted:

1. ✅ C104 merged into C101 (same feature)
2. ✅ D-057 estimate revised to 3-4h
3. ✅ D-061 is a hard Sprint 10 commitment
4. ✅ C106 is the explicit Sprint 10 cut candidate

**Sprint 9 plan (revised)**:
- **D-057** (LLM abstraction): 3-4h, Day 1 prerequisite
- **C103 Lite** (First Visit Guide): 8-11.5h, 1st in implementation order
- **C101** (Comprehension Check, includes C104): 8-12h, 2nd in implementation order
- **C98** (Event Interpretation Engine): 2h spike + 16-23.5h dev, 3rd
- **Total**: 37-51h

**Sprint 10 plan (revised)**:
- **C34** (Company Story Timeline): 16-24h
- **C105** (Simple/Detailed Toggle): 10-14h
- **M5 remediation** (fix 10 L1 event-alert failures): 8-12h
- **D-061** (test infrastructure): 3-4h — **hard commitment**
- **D6** (remaining YAML migrations): 3-4h
- **C106** (First 7 Days): 16-22h — **cut candidate if behind**
- **Total**: 56-80h (core: 34-48h, stretch: 22-32h)

**Design Grade**: A (upgraded from A-)

**Strategic note from challenger**: The education-first onboarding system (C103 + C101 + C106) is Stock Explorer's most defensible competitive moat. No TW competitor offers structured onboarding. The team should consider making this the primary narrative for Sprint 9-10, with C98 as the enabling infrastructure. The "historian" positioning is validated by the competitor analysis — the industry is moving toward social trading and guru-following (eToro), which makes Stock Explorer's "explain what happened" approach more differentiated, not less.

---

*Challenger: 🔥 Challenger (gpt-oss-120b) | Rounds: 3 | Revisions: 4 | Verdict: ✅ CONFIRMED with revisions*
