# 2026-06-16 Challenge — Round 21 Discussion

## Challenger Briefing

Sprint 11 is complete. The Architect, Designer, and Developer have submitted their analyses for Round 21, covering Sprint 12 planning and post-Sprint 12 directions. Preliminary team consensus is:

**Sprint 12**: QA (3-8h) + Info Hierarchy (8-14h) + C40 Mode Toggle (10-18h, scope-reduced) + User Feedback (2-4h) = 24-38h (Team) / 24-44h (Developer upper bound)

**Post-Sprint 12 consensus**: C33 Glossary → C46 Moat + C36 Revenue Tree → C47 Education Academy

**Key disagreements**: Architect ranks C02+C33 (infrastructure) first post-Sprint 12; Designer ranks C48 (Story Card) first; Developer agrees with Architect's C33/C46/C36 trio but flags C02 P0 gap. Designer recommends C40 be deferred. Developer's estimate exceeds budget by 6h at the upper bound.

---

### Round 1: Feature Direction Challenge

**Team proposal summary**: Sprint 12 ships QA for C37/C39/C43/C45, implements 3-tier progressive disclosure Info Hierarchy on the Business Card page, adds a scope-reduced C40 Beginner/Expert mode toggle (conditional rendering only, no text simplification), and adds a 👍/👎 user feedback mechanism. Post-Sprint 12, the team converges on C33 → C36/C46 → C47 as the feature pipeline.

**Challenge questions**:

1. **C02 Notifications is P0 per the issues backlog, yet it is not in Sprint 12 and is explicitly deprioritized post-Sprint 12.** The product vision is "historian, not stock picker" — but retention is a prerequisite for mission fulfillment. If users never come back, the historian mission dies silently. C02 infrastructure (notification_service.py, M5 event detection) already exists. The remaining work is wiring. Why is a P0 competitive gap feature — one that ALL 14+ competitors have — being ranked behind C33 Glossary (P2), which is a content task with ongoing maintenance burden?

2. **C40 Beginner/Expert Mode was originally CUT in Sprint 1 planning and replaced with "beginner mode by default" as a design principle.** The Designer correctly notes that the Info Hierarchy achieves 80% of C40's UX benefit at far lower complexity. The Developer flags C40 at 10-18h with 🔴 High risk, cross-section coupling, and D24 dependency. The Designer explicitly recommends C40 be DEFERRED. What has changed since Sprint 1 to justify reinstating a previously-cut feature that now risks consuming 30-40% of Sprint 12 capacity with the highest risk profile in the sprint?

3. **The Designer identifies C48 Story Card and C56 Explain This Metric as Tier 1 UX priorities — both ranked higher by UX impact than C36/C47 — yet neither appears in the team's post-Sprint 12 top 3.** C56 is explicitly called out as "design system unfinished business" because the design system REQUIRES plain-language translations for all professional terms. Why is the team deprioritizing a design system requirement in favor of C36 Revenue Tree, which has data availability risk and is limited to top stocks?

4. **Both the Developer's estimate (24-44h) and Architect's estimate (26-42h) exceed the 38h budget at the upper bound.** The Designer identifies multiple risks (D24 coupling, C40 scope creep, C40's Zone A placement conflict) that could push actual hours higher. Is the team being honest about Sprint 12 capacity, or is this aspirational planning that will result in C40 slipping to Sprint 13 anyway? If C40 is likely to slip regardless, should it be moved to Sprint 13 now rather than discovered mid-sprint?

**Verdict: Need revision.** Three of the four challenges point to the same structural issue: C40 is the riskiest item in Sprint 12, was previously cut, is recommended for deferral by the Designer, and threatens the budget. The post-Sprint 12 pipeline also ignores the Designer's C48 and C56 recommendations without adequate justification. The team should commit to a Sprint 12 that can succeed without C40, and move C40 to Sprint 13 where it can be properly gated on Info Hierarchy completion.

---

### Round 2: Priority Challenge

**Challenge questions on priorities**:

1. **The Architect's post-Sprint 12 ranking (C02+C33 → C36+C46 → C47) and Designer's ranking (C48 → C56 → C42 → C46) have ZERO overlap in the top 3 positions.** This is not a minor sequencing disagreement — it is a fundamental split on what drives product value. Architect sees infrastructure as foundational; Designer sees engagement features as critical for the ten-second test. The team consensus of "C33 → C36/C46 → C47" appears to be an Architect-Developer compromise that ignores the Designer's UX-first arguments entirely. Has the Designer's perspective been genuinely incorporated, or simply overruled by vote count?

2. **The Developer identifies C33 Glossary as "highest ROI per hour" for post-Sprint 12, but flags maintenance burden risk (50-100 terms, ~1h/sprint ongoing, UI integration surface area underestimated by 2-4h).** The Architect rates C33+C02 at 12-20h. Meanwhile, C48 Story Card (8-12h) delivers a single, self-contained UX improvement with no maintenance burden. Which actually has higher total cost of ownership and better effort-to-impact ratio?

3. **The Developer's scope lock for Info Hierarchy (Tier 1: Header+Takeaways+One-liner+Key Metrics) and the Designer's recommended section order (above-fold: C37+C39+C43) are not identical.** The Developer's Tier 1 doesn't include C39 (What Changed), while the Designer's above-fold includes it as the second element. This disagreement must be resolved before Sprint 12 code begins to avoid implementation rework. Which is correct?

4. **The Developer flags C02 Notifications as having hidden architecture risk: D02 (background worker investigation) is still 📋 Todo.** Streamlit is request-response only. True push notifications require external cron or APScheduler. Yet the Architect proposes C02 as Sprint 13 Direction B at 14-18h "in-app only." Is 14-18h realistic when the underlying architecture hasn't been investigated? What happens when the team discovers in Sprint 13 that email delivery requires solving D02 first, and the 14-18h estimate balloons?

5. **The Developer flags a compounding maintenance cost the team hasn't acknowledged: "every future feature must now tag 'beginner' or 'expert' at design time — adds overhead to every sprint going forward."** If C40 ships in Sprint 12, this is a permanent tax on feature velocity for Sprint 13+. Is the team explicitly accepting this tradeoff, or is it an invisible cost that will slow future sprints?

**Verdict: Need revision.** The post-Sprint 12 priority split between Architect (infrastructure-first) and Designer (engagement-first) is unresolved. The Info Hierarchy section ordering disagreement must be resolved before implementation. C02's architecture dependency on D02 needs investigation before it's committed to a sprint.

---

### Round 3: Goal Alignment Challenge

**Challenge questions on alignment with the historian mission**:

1. **Sprint 12 ships zero new understanding-critical features for the user.** QA improves quality of existing features. Info Hierarchy improves layout. C40 improves content management. User Feedback gathers signal. None of these directly advance the "story first" mission or help users understand companies better. The product vision states: "Help users move from 'I don't understand' to 'I know what this company does.'" Is the team comfortable that an entire sprint cycle (Sprint 12) will ship no features that directly advance this mission, while two sprints of feature development (Sprints 9-11) are followed by a sprint of polish and infrastructure?

2. **The product vision's primary verification principle is the "ten-second test."** The Designer identifies C48 Story Card as the feature that makes it — a 30-second visual summary at the top of every company page. C48 (8-12h) directly targets the ten-second test. The team's post-Sprint 12 sequence (C33 → C36/C46 → C47) ranks C46 Moat (14-20h) and C36 Revenue Tree (12-18h) before C48. These features deepen understanding but don't improve the initial ten-second hook. C48 is the design team's #1 priority; it's ranked #4 by the team's implicit sequence. Is this sequence optimal for maximizing the ten-second test pass rate among the target user (beginner investors)?

3. **The Business Card page has 18+ sections, violating the product vision's PPT-style "one key point per page" principle.** Both Designer and Developer agree that C36 Revenue Tree should move to its own tab and C38 Compare Stories to Peer Comparison. This has not been done. Is the team building C40 Mode Toggle and Info Hierarchy on top of a page architecture they already agree needs fundamental restructuring? Should Business Card page consolidation (moving C36/C38 off the page) happen BEFORE both Info Hierarchy and C40, making both of those features simpler to implement?

4. **The product vision states: "Willing to sacrifice completeness for clarity."** The Sprint 1 "beginner by default" philosophy was designed to avoid complexity. Yet C40 Mode Toggle exists entirely to manage completeness (letting users choose how much to see). If beginners need mode toggles to avoid being overwhelmed, the default experience isn't beginner-friendly enough. Does C40 represent a retreat from the simplicity-first philosophy? The Designer's recommendation to defer C40 precisely because Info Hierarchy achieves 80% of the benefit is consistent with "sacrifice completeness for clarity." The team's inclusion of C40 contradicts it.

5. **The product vision defines the mission as understanding companies, not tracking prices.** C46 Moat Analysis and C36 Revenue Tree both advance this mission deeply — they explain how money flows and why competitive advantage exists. These are excellent historian features. But the Developer notes C46 requires manual moat scoring for top-20 stocks (content bottleneck) and C36 requires manual revenue hierarchy curation (data bottleneck). If both content-stream and code-stream are needed simultaneously in Sprint 13, is the team resourced for parallel content creation and feature development? The Architect's Sprint 13 plan (C36+C46+C02+C33 at 38-54h) is extremely aggressive — 54h exceeds a 2-week sprint budget. Does the team have a realistic Plan B if content creation lags?

**Final Verdict: ✅ CONFIRMED (with 4 revisions)**

The Sprint 12 plan is directionally sound — QA, Info Hierarchy improvement, and user feedback collection are appropriate activities after 11 sprints of feature delivery. The post-Sprint 12 historian features (C46, C36) are well-chosen. However, four structural issues require revision before the plan is actionable.

---

### Required Revisions

1. **C40 Mode Toggle must be deferred to Sprint 13.** Justification: (a) Originally cut in Sprint 1 with "beginner by default" as the replacement philosophy. (b) Designer explicitly recommends deferral — Info Hierarchy achieves 80% of benefit. (c) Developer flags 🔴 High risk with cross-section coupling, D24 dependency, and permanent per-feature maintenance tax. (d) Both Developer (44h) and Architect (42h) upper-bound estimates exceed the 38h Sprint 12 budget, with C40 being the variable that tips the sprint over. Sprint 12 should ship QA + Info Hierarchy + User Feedback = 13-26h, a healthy scope that can be completed with margin. C40 moves to Sprint 13, gated on Info Hierarchy completion.

2. **The post-Sprint 12 sequence must incorporate C48 Story Card as Sprint 13 priority alongside C33.** Justification: (a) Designer identifies C48 as #1 UX impact priority. (b) The product vision's ten-second test is the primary verification principle — C48 directly targets it. (c) The Architect's and Developer's post-Sprint 12 sequence ignores the Designer's top recommendation without adequate counter-argument. Recommended Sprint 13 sequence: C33 Glossary (8-14h) + C48 Story Card (8-12h) = 16-26h as Sprint 13a, followed by C36+C46 = 26-38h as Sprint 13b. This gives the Designer her #1 priority while preserving the Architect's infrastructure-first sequencing.

3. **Business Card page content reduction must happen before or concurrent with Info Hierarchy.** Justification: (a) Both Designer and Developer agree C36 Revenue Tree should move to its own tab and C38 to Peer Comparison. (b) Adding Info Hierarchy's 3-tier structure to the current 18-section page is more complex than doing so after reducing to ~10 sections. (c) The "one key point per page" principle is violated by the current page regardless of hierarchy design. The team should relocate C36 and C38 off the Business Card page as part of the Info Hierarchy work (estimated 2-4h additional), not defer it to an unspecified future sprint.

4. **D02 (background worker architecture investigation) must be completed before or concurrent with Sprint 12, not deferred.** Justification: (a) C02 is a P0 competitive gap — all 14+ competitors have it. (b) The Developer has flagged that Streamlit is request-response only and true notifications require external cron/APScheduler. (c) Committing C02 to Sprint 13 without resolving D02 means the Sprint 13 plan contains a hidden blocker that will likely cause C02 to slip again. The team should allocate 2-4h in Sprint 12 (during the lighter sprint created by Revision 1's removal of C40) to investigate D02 and produce a technical spike that informs Sprint 13's C02 scope. This is a low-risk investment that prevents a high-risk surprise in Sprint 13.

---

*Challenger: OWL | Date: 2026-06-16 | Round 21 | Three rounds completed → CONFIRMED with 4 revisions*
