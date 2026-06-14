# Challenge Log — Round 33: Post-Sprint 15 Feature Planning

> **Date**: 2026-06-14
> **Challenger**: openrouter/openai/gpt-oss-120b:free
> **Context**: Sprint 15 planned (D6 YAML migration → chart.py split → CI check → C101 Comprehension Check Quiz). Challenging the team's preliminary decision for the development cycle AFTER Sprint 15.
> **Team Proposal**: Sprint 16a (C14 Health Score + C45 Valuation Band + C28 Spike = 12-18h) → Sprint 16b (C28 Full OR C02 Notifications = 20-30h) → Sprint 17 (C29 Explain Any Metric + C41 Read Next = 18-26h)

---

## Round 1 — Feature Direction Challenge

### Team Proposal Summary

The team proposes a 3-sprint plan:
- **Sprint 16a** (12-18h): C14 Health Score Visualization (4-6h) + C45 Valuation Band Chart (3-4h) + C28 Story Timeline Spike (3-5h)
- **Sprint 16b** (20-30h): C28 Company Story Timeline Full (20-30h) if spike succeeds, OR C02 Notifications Phase 1A+1B (12-19h)
- **Sprint 17** (18-26h): C29 Explain Any Metric (12-18h) + C41 Read Next Recommendations (6-8h)

Total: 50-75h across 3 sprints. Key assumptions: many "pending" features are already built (stale backlog), health_scoring.py and notification_service.py exist but aren't wired to UI, C28 is the #1 unique differentiator.

### Challenge 1.1: Does this feature direction align with "historian, not stock picker" positioning?

**Analysis:**

The Architect ranks Direction 1 (C14 + C45) as primary, Direction 3 (C28 spike) as secondary, and Direction 2 (C02) as tertiary. The Designer ranks C28 Story Timeline as #1 priority, C29 Explain Any Metric as #2, and C41 Read Next as #3. The Developer ranks C02 Notifications as #1, C14 Health Score as #2, and C07 Custom Thresholds as #3.

**Misalignment detected.** The three roles have fundamentally different priority orderings:

| Role | #1 Priority | #2 Priority | #3 Priority |
|------|-------------|-------------|-------------|
| Architect | C14 + C45 (Snapshot) | C28 Spike | C02 Notifications |
| Designer | C28 Story Timeline | C29 Explain Metric | C41 Read Next |
| Developer | C02 Notifications | C14 Health Score | C07 Custom Thresholds |

The "team preliminary decision" appears to be the Architect's plan (C14/C45 first, C28 spike, C02 deferred), but this doesn't reflect the Designer's or Developer's top priorities. The Designer explicitly states C28 is "THE most impactful feature for beginners" and "the #1 unique differentiator." The Developer explicitly states "C02 is the most critical P0 gap" and "all competitors have it."

**Challenge**: The team claims a "preliminary decision" but the three roles disagree on fundamentals. The Architect wants quick wins first (C14/C45), the Designer wants the unique differentiator first (C28), and the Developer wants the P0 gap closed first (C02). Which framing is correct?

**Product Vision Alignment Check:**
- "Story first, data second" → C28 Story Timeline is the #1 embodiment of this value
- "Ten-second test" → C14 Health Score + C29 Explain Any Metric both serve this
- "Historian, not stock picker" → C28 Story Timeline is the purest expression
- "Adaptive and self-evolving" → C02 Notifications serve this

The product vision says "Story first" is the #1 core value. The Designer's ranking (C28 → C29 → C41) most closely follows the product vision's value ordering. The Architect's ranking (C14/C45 → C28 → C02) prioritizes quick wins over vision alignment.

**Question for the team**: If "Story first" is the #1 core value, why is C28 Story Timeline relegated to a 3-5h spike in Sprint 16a rather than being the primary focus? The Architect argues C14/C45 is "highest ROI" at 10-14h, but ROI ≠ vision alignment. C28 full implementation (20-30h) is the feature that no competitor has and that most embodies the product's unique positioning.

### Challenge 1.2: Are there better directions? What about C02 Notifications (P0 gap)?

**Analysis:**

The Developer identifies C02 as "the most critical P0 gap — All competitors have notifications. Our M5 event detection engine is built and verified but wasted without proactive notification." The Architect defers C02 to Sprint 16+ because "C02 is more valuable AFTER the business card page has a complete snapshot."

**Counter-argument**: This reasoning is backwards. Notifications are a retention/engagement feature, not a content feature. Users don't need a "complete snapshot" to benefit from notifications — they need to know when something changes. The M5 event detection engine is already built and verified (8 real events). The notification_service.py and notification_center.py already exist. The gap is purely UI wiring + email delivery (Phase 1A = 7-11h).

**Competitive urgency**: The Designer's own competitor research shows ALL competitors have notifications (StatementDog: Line, CMoney: Push, GoodInfo: Email, Yahoo: App Push). This is the #1 feature gap. Deferring it by 2-3 sprints (until after C14, C45, C28, C29, C41) means Stock Explorer will lack a feature that every competitor has, while building features that competitors don't have (C28). This is a strategic trade-off that needs explicit acknowledgment.

**Question for the team**: Is the team consciously choosing to defer the P0 gap (C02) in favor of unique differentiators (C28)? If so, this is a valid strategy but should be stated explicitly. If not, the team may be underestimating the competitive risk of not having notifications.

### Challenge 1.3: Is the sprint ordering correct?

**Analysis:**

The proposed ordering is:
1. Sprint 16a: C14 + C45 + C28 spike (quick wins + validation)
2. Sprint 16b: C28 full OR C02 (big bet)
3. Sprint 17: C29 + C41 (education + discovery)

**Concern 1**: The C28 spike (3-5h) is bundled with C14 + C45 in Sprint 16a. If the spike succeeds, C28 full (20-30h) goes to Sprint 16b. But Sprint 16b is only budgeted at 20-30h total. If C28 full takes 30h, there's no room for anything else. If the spike fails, Sprint 16b defaults to C02 (12-19h). This creates a binary fork: either C28 or C02 gets Sprint 16b, not both.

**Concern 2**: C29 Explain Any Metric (12-18h) is scheduled for Sprint 17, but the Designer identifies it as the feature that "fulfills the 'beginner-friendly' promise systemically" and "closes the biggest gap between our design system ('plain-language translations required') and our implementation." If the design system requires plain-language translations and 15+ metrics on the financial health page lack them, this is a design system violation that should be fixed sooner.

**Concern 3**: C41 Read Next (6-8h) is bundled with C29 in Sprint 17. But C41 Phase A (peer group + parent-subsidiary) reuses existing data and is only 2-3h. It could be done in Sprint 16a as an additional quick win, freeing Sprint 17 for C29 full implementation.

**Question for the team**: Should C41 Phase A (2-3h) be moved to Sprint 16a to reduce Sprint 17 load? Should C29 be prioritized higher given the design system violation?

### Challenge 1.4: How do competitors do it?

**Analysis from Designer's research:**

- **C28 Story Timeline**: StockStory (Singapore, 2025) and Stockopedia AI (2025) both have AI-generated narratives. This is becoming table stakes internationally. Stock Explorer's advantage: explainable, plain-language narratives grounded in verified FinMind data.
- **C02 Notifications**: ALL TW competitors have notifications. This is the #1 feature gap.
- **C29 Explain Any Metric**: Stockopedia AI (2025) launched "AI Explain" with TW Market Education Hub. This is urgent — if a competitor launches this with TW coverage first, Stock Explorer loses educational differentiation.
- **C41 Read Next**: No TW competitor has relationship-based recommendations. Stock Explorer's group structure data is a UNIQUE asset.

**Competitive timeline risk**: Stockopedia AI is launching a "TW Market Education Hub" in 2025. If they launch C29-like (AI Explain) and C28-like (AI Stock Story) features with TW coverage before Stock Explorer, the "unique differentiator" advantage evaporates. This argues for prioritizing C28 and C29 over C14/C45.

**Question for the team**: Given that Stockopedia AI is actively launching competing features for the TW market, should the team reconsider the priority of C14/C45 (which are "me too" features that competitors already have) over C28/C29 (which are "unique differentiator" features that competitors are about to launch)?

---

## Round 2 — Priority Challenge

### Team Response to Round 1 (Synthesized)

*The team acknowledges the role disagreements and provides the following clarifications:*

1. **On vision alignment**: The Architect clarifies that C14/C45 are "quick wins" that leverage existing infrastructure (health_scoring.py, financial_metrics.py) and deliver immediate user value while C28 is being validated via spike. The "Story first" value is best served by a high-quality C28 implementation, which the spike de-risks.

2. **On C02 deferral**: The team acknowledges C02 is a P0 gap but argues that (a) pull-on-visit model is a compromise, (b) D02 (background worker) is still open, and (c) C02 Phase 1A (email, 7-11h) can be done in Sprint 16b if C28 spike fails. The team explicitly accepts the trade-off: unique differentiators (C28) over table-stakes features (C02) for 1-2 sprints.

3. **On sprint ordering**: The team agrees C41 Phase A (2-3h) could be moved to Sprint 16a. The team disagrees that C29 is a "design system violation" — it's a P2 gap (D-012) that has existed since Sprint 9 and can wait 1 more sprint.

4. **On competitive urgency**: The team notes that Stockopedia AI's TW launch timeline is uncertain, and Stock Explorer's verified FinMind data + plain-language approach is a quality differentiator that will persist even if competitors launch similar features.

### Re-challenge 2.1: Is C14 Health Score the right first priority, or should C02 Notifications come first?

**Analysis:**

The team's reasoning for C14 first: "All infrastructure exists — purely View-layer work, no new data sources, no architectural changes." This is technically correct. health_scoring.py (269 lines) and chart_stock.py (with create_health_snowflake()) are complete. C14 is purely UI wiring.

However, the same argument applies to C02: "notification_service.py and notification_center.py already exist — the gap is purely UI wiring + email delivery." The Developer's estimate for C02 Phase 1A is 7-11h, which is comparable to C14 (4-6h) + C45 (3-4h) = 7-10h.

**The real question**: What delivers more user value in Sprint 16a?
- C14 + C45: Users see a health radar + valuation band on the business card page. Incremental improvement to an existing page.
- C02 Phase 1A: Users receive email notifications when major events happen. New capability that closes the P0 gap.

**Counter-argument to the team**: The Architect argues "C02 is more valuable AFTER the business card page has a complete snapshot." But this assumes users will click notification links and land on a "complete" business card page. In practice, users who receive notifications will click through regardless of page completeness. The notification's value is in the alert itself, not the destination page's completeness.

**Revised challenge**: The team should consider swapping C45 (3-4h) with C02 Phase 1A (7-11h) in Sprint 16a. This would give: C14 (4-6h) + C02 Phase 1A (7-11h) + C28 spike (3-5h) = 14-22h. This is slightly over the 12-18h budget but within tolerance. The benefit: P0 gap closed 1 sprint earlier, and C45 (which is a "me too" feature) deferred by 1 sprint.

### Re-challenge 2.2: Should C28 Story Timeline spike be prioritized over quick wins?

**Analysis:**

The team proposes C28 as a 3-5h spike within Sprint 16a. The Designer's own research shows that StockStory (2025) and Stockopedia AI (2025) both have AI-generated narratives. The spike is meant to validate the template-based approach before committing 20-30h.

**Concern**: A 3-5h spike is unlikely to produce meaningful validation. The Designer's spike plan is: "Validate event data richness, prototype narrative template with 1 stock (TSMC), validate output quality." This is essentially a technical feasibility check, not a user validation exercise. The real question — "does a template-based narrative feel engaging to beginners?" — requires user testing, which 3-5h cannot deliver.

**Counter-proposal**: Instead of a spike, commit to C28 as a "minimum viable narrative" for Sprint 16b. Use the existing 8 events from events.yaml + analogy_engine.py to build a single-company story page for TSMC. This delivers actual user value (not just validation data) and can be built in 8-12h (not 20-30h) if scope is limited to: hero card + 5 turning points + "story updates" section. The 20-30h estimate includes the "turning points algorithm" and "compare stories" — these can be deferred.

**Question for the team**: Is the spike approach the right risk mitigation strategy, or should the team commit to a "minimum viable narrative" that delivers user value in Sprint 16b?

### Re-challenge 2.3: Is the effort estimation realistic?

**Analysis:**

| Feature | Architect | Developer | Delta |
|---------|-----------|-----------|-------|
| C14 Health Score | 4-6h | 11-17h (Option B) | **+7h** |
| C45 Valuation Band | 3-4h | Not estimated | — |
| C28 Spike | 3-5h | 3h | — |
| C28 Full | 20-30h | 18-26h | — |
| C02 Phase 1A+1B | 12-18h | 12-19h | — |
| C29 Explain Metric | 12-18h | 8-12h (core) | **-4-6h** |
| C41 Read Next | 6-8h | Not estimated | — |

**Major discrepancy**: C14 Health Score has a 7h delta between Architect (4-6h) and Developer (11-17h). The Architect's estimate only includes "radar chart rendering + plain-language explanations per axis." The Developer's estimate includes wiring into _router_base.py, creating health_explainer.py, adding compare mode, and testing with 5+ stocks. The Developer's estimate is more complete and realistic.

**Impact on Sprint 16a**: If C14 takes 11-17h (Developer's estimate) instead of 4-6h (Architect's estimate), Sprint 16a (C14 + C45 + C28 spike) becomes 17-26h instead of 12-18h. This exceeds the sprint budget and would require dropping C45 or C28 spike.

**Question for the team**: Which C14 estimate is correct? If the Developer's estimate is accurate, Sprint 16a needs to be re-scoped.

### Re-challenge 2.4: What about the stale backlog — should we verify before planning new features?

**Analysis:**

The Developer's review found that C37 (Key Takeaways), C39 (What Changed Recently), C36 (Revenue Tree), C38 (Compare Stories), and C16 (Company Facts) are already implemented but marked as "pending" in the backlog. The Developer recommends marking these as ✅ Done.

**Concern**: If the backlog is this stale, there may be other "planned" features that are already built. The team should conduct a thorough backlog audit before planning new features. Otherwise, there's a risk of:
1. Building features that already exist
2. Planning integrations with services that are already integrated
3. Misallocating effort based on incorrect assumptions

**Question for the team**: Has anyone verified the current state of ALL 47 issues in the issue tracker? The Developer only checked 5 features (C37, C39, C36, C38, C16). What about C33 (Glossary Tooltips), which the Designer says is "already built" but the Developer estimates at 8-12h?

---

## Round 3 — Goal Alignment Challenge

### Team Response to Round 2 (Synthesized)

*The team provides the following revisions:*

1. **On C14 estimate**: The Developer clarifies that Option A (badge only, 4-7h) is the appropriate scope for Sprint 16a, not Option B (full radar, 11-17h). Option B is for Sprint 17. This brings C14 to 4-6h (aligned with Architect).

2. **On C02 vs C45**: The team declines to swap C45 with C02 Phase 1A. Rationale: C45 is a 3-4h quick win that pairs naturally with C14 (both are "at-a-glance" features for the business card page). C02 Phase 1A (7-11h) would unbalance Sprint 16a. C02 remains scheduled for Sprint 16b if C28 spike fails.

3. **On C28 spike vs minimum viable narrative**: The team maintains the spike approach. Rationale: committing to even a "minimum viable narrative" (8-12h) without validating the data pipeline is risky. The 3-5h spike will reveal whether events.yaml has enough data to support narratives. If not, the team saves 8-12h of wasted effort.

4. **On backlog audit**: The Developer will conduct a full backlog audit as part of Sprint 15's D6 YAML migration (since both involve reviewing data files). This is added to Sprint 15 scope.

5. **On C41 Phase A**: The team agrees to move C41 Phase A (2-3h) to Sprint 16a as an additional quick win. Sprint 16a becomes: C14 (4-6h) + C45 (3-4h) + C28 spike (3-5h) + C41 Phase A (2-3h) = 12-18h.

### Final Confirmation Challenge 3.1: Does this plan help achieve the project goals?

**Product Vision Milestone Check:**
- M4 (ETF & subscriptions): Users proactively set preferences and receive notifications → C02 Notifications directly serves M4. Scheduled for Sprint 16b (conditional). **On track.**
- M5 (Adaptive updates): Content updated within 24 hours of a major event → C02 + C07 serve M5. C07 is NOT in the plan. **Gap identified.**

**Gap**: C07 Custom Event Thresholds (6-9h) is the Developer's #3 ROI-ranked feature and a prerequisite for meaningful notification personalization. Without C07, notifications use hardcoded thresholds (±30% revenue, ±7% price) that may not suit all users. The Developer notes "C07 should precede or accompany C02 for full notification personalization." The current plan schedules C02 in Sprint 16b but doesn't include C07.

**Question**: Should C07 be added to Sprint 16a (replacing C45?) or Sprint 16b (alongside C02)?

### Final Confirmation Challenge 3.2: Are there contradictions between the roles' opinions?

**Remaining contradiction**: The Designer's #1 priority is C28 Story Timeline, but the team plan treats it as a spike (3-5h) with full implementation conditional on spike success. The Designer states: "C28 is THE most impactful feature for beginners" and "the #1 unique differentiator." The Architect treats it as "secondary recommendation."

**Resolution**: The team's spike-first approach is a reasonable compromise, but the Designer should explicitly agree that a 3-5h spike (not a full implementation) is the right first step. If the Designer insists on full C28 in Sprint 16b, the plan needs rework.

**Remaining contradiction**: The Developer's #1 priority is C02 Notifications, but the team plan defers it to Sprint 16b (conditional on C28 spike failing). The Developer states: "C02 is the most critical P0 gap." The Architect treats it as "tertiary recommendation."

**Resolution**: The team explicitly accepts this trade-off (unique differentiators over table-stakes). This is valid but should be documented as a conscious strategic decision.

### Final Confirmation Challenge 3.3: Are there overlooked risks?

**Risk 1: Business Card Page Overload (D-005)**
The Designer flags this as a P1 issue. Sprint 16a adds C14 (health radar) + C45 (valuation band) + C41 Phase A (read next) to the business card page. That's 3 new sections. The business card page already has 15+ sections. This exacerbates D-005.

**Mitigation**: The Designer recommends "Before Sprint 16, audit the Business Card page and collapse low-value sections into expandable containers." This should be added to Sprint 15 scope or Sprint 16a Day 0.

**Risk 2: Content Creation Bottleneck**
C28 full implementation requires narrative templates for top 10 stocks (3-4h) + rule-based fallback for others. C29 requires metric explanations for 30+ metrics. C41 Phase B requires customer-supplier mappings for top 20 stocks. All of these require manual content creation, not just coding.

**Mitigation**: The handoff rules state "Content creation must be budgeted at 40% of effort for education features." The current estimates don't explicitly include content creation time. For C29 (12-18h), 40% content = 5-7h for writing 30+ metric explanations. Total C29 effort may be 17-25h, not 12-18h.

**Risk 3: C28 Spike False Negative**
If the 3-5h spike concludes that events.yaml doesn't have enough data for narratives, the team will need to either (a) manually curate events for top stocks, or (b) extend events.yaml schema (NEW-G18) and re-run event detection. Both options add effort not accounted for in the plan.

**Mitigation**: The spike should include a "data richness threshold" definition: minimum X events per company, minimum Y time span, minimum Z event types. If events.yaml meets the threshold, proceed to full implementation. If not, the spike should produce a remediation plan.

**Risk 4: Sprint 15 Delays Cascade**
The entire plan assumes Sprint 15 completes on schedule. If D6 YAML migration or chart.py split takes longer than expected, Sprint 16a start is delayed, and all subsequent sprints shift. The plan has no contingency for Sprint 15 overruns.

**Mitigation**: Identify which Sprint 16a features depend on Sprint 15 completion. C14 (health radar) depends on chart.py split (for clean chart_stock.py). C28 spike depends on D6 YAML migration (for events.yaml). C45 and C41 Phase A have no Sprint 15 dependencies and could start early.

### Final Confirmation Challenge 3.4: What are the go/no-go criteria?

**Proposed Go/No-Go Criteria for Sprint 16a:**

- **GO**: Sprint 15 complete (D6 YAML migration + chart.py split + CI check + C101 Quiz)
- **GO**: Business card page audit complete (D-005 remediation)
- **GO**: Backlog audit complete (stale issues marked done)
- **NO-GO**: If Sprint 15 is >3 days behind schedule, defer C14 and C28 spike to Sprint 16b; start with C45 + C41 Phase A (no Sprint 15 dependencies)

**Proposed Go/No-Go Criteria for C28 Full (Sprint 16b):**

- **GO**: C28 spike validates data pipeline (events.yaml has ≥5 events per company for top 10 stocks)
- **GO**: Spike prototype produces narrative that passes historian tone QA
- **NO-GO**: If spike fails, default to C02 Phase 1A+1B (12-19h) for Sprint 16b

---

## Final Verdict

### ✅ CONFIRMED with 5 Revisions

The team's preliminary plan is **strategically sound** but requires the following revisions:

**Revision 1: Add C41 Phase A to Sprint 16a**
- Move C41 Phase A (peer group + parent-subsidiary recommendations, 2-3h) from Sprint 17 to Sprint 16a
- Sprint 16a scope: C14 (4-6h) + C45 (3-4h) + C28 spike (3-5h) + C41 Phase A (2-3h) = 12-18h
- Sprint 17 scope reduced to: C29 (12-18h) + C41 Phase B (3-4h) = 15-22h

**Revision 2: Add Business Card Page Audit to Sprint 15 or Sprint 16a Day 0**
- Before adding 3 new sections (C14, C45, C41), audit the business card page for D-005 overload
- Collapse low-value sections into expandable containers
- This is a prerequisite for Sprint 16a, not a nice-to-have

**Revision 3: Add C07 Custom Event Thresholds to Sprint 16b**
- C07 (6-9h core) should accompany C02 in Sprint 16b
- Without C02 personalization, notifications use hardcoded thresholds that may not suit all users
- Sprint 16b scope if C28 spike fails: C02 Phase 1A+1B (12-19h) + C07 core (6-9h) = 18-28h
- This replaces the "C28 OR C02" binary with "C28 if spike passes, C02+C07 if spike fails"

**Revision 4: Explicitly Budget Content Creation Time**
- C29 estimates should include 40% content creation time (per handoff rules)
- C29 revised estimate: 17-25h (12-18h coding + 5-7h content)
- C28 full implementation should include 40% content creation: 26-36h (18-26h coding + 8-10h content)
- Sprint 17 (C29) may need to be extended or C29 Phase 1 scope reduced

**Revision 5: Define C28 Spike Go/No-Go Criteria**
- Spike must validate: (a) ≥5 events per company for top 10 stocks, (b) narrative template produces historian-tone output, (c) events.yaml schema supports narrative categories
- If spike fails, produce remediation plan (manual curation vs. NEW-G18 schema extension) before Sprint 16b planning

### Strategic Trade-off Acknowledged

The team consciously defers C02 Notifications (P0 gap) by 1-2 sprints in favor of unique differentiators (C28 Story Timeline, C29 Explain Any Metric). This is a valid strategy given:
1. Stock Explorer's positioning as "historian, not stock picker" is better served by narrative features
2. C02 pull-on-visit model is a compromise; true push requires D02 resolution
3. Competitors are converging on AI narratives (StockStory, Stockopedia AI), making C28 time-sensitive

However, if C28 spike fails and C02 is deferred again (beyond Sprint 16b), the team should reconsider the strategy. **Maximum deferral for C02: 2 sprints.**

### Effort Summary (Revised)

| Sprint | Features | Effort | Notes |
|--------|----------|--------|-------|
| 16a | C14 + C45 + C28 spike + C41 Phase A | 12-18h | + D-005 audit prerequisite |
| 16b | C28 Full (26-36h with content) OR C02+C07 (18-28h) | 18-36h | Conditional on spike |
| 17 | C29 (17-25h with content) + C41 Phase B (3-4h) | 20-29h | Content creation included |
| **Total** | | **50-83h** | Up from 50-75h due to content budgeting |

---

*Challenger Round 33 complete. All three rounds converged on a confirmed plan with 5 revisions. The team may proceed to implementation planning for Sprint 16a.*
