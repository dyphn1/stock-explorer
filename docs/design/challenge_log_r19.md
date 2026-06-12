## 2026-06-13 Challenge Log — Round 19 Discussion

### Team Preliminary Decision

The team proposes a 5-sprint post-Sprint 10 plan organized around three directions:

- **Direction A (Discovery & Screening)** — HIGHEST priority: C42 Stock Screener (P1, 16-24h), C51 Sector Heatmap (P2, 8-12h), C49 Daily Market Pulse (P2, 10-14h). Total: 34-50h. Blocker: R3 batch API.
- **Direction B (Deep Education)** — HIGH priority: C58 Beginner Onboarding (P1, 14-20h), C47 Education Academy (P2, 20-30h), C56 Explain This Metric (P1, 12-16h), C52 Quiz Mode (P2, 10-14h). Total: 56-80h.
- **Direction C (Smart Narrative)** — MEDIUM priority, deferred: C98 Event Interpretation (P1, 14-18h), C86 AI Narrative Agent (P2, 20-30h), C100 Natural Language Screener (P1, 18-24h), C68 Concept Storytelling (P1, 12-16h). Total: 64-88h.

**Recommended Sprint Plan:**
- Sprint 11: D16 + D24 + R3 + C53 + C51 (22-32h)
- Sprint 12: R5 + C42 + C56 + C62 (37-52h)
- Sprint 13: C58 + C48 + C68 + C84 (44-62h)
- Sprint 14: C50 + C60 + C52 + C104 + C66 (32-48h)
- Sprint 15+: D5 (LLM layer) → C86, C100, C59, etc.

---

### Round 1: Feature Direction Challenge

#### Challenge 1.1: C58 Onboarding Is Deferred Despite Being "Retention-Critical"

The Designer explicitly ranks C58 (Beginner Onboarding Flow) as **#1 UX impact** across the entire backlog, stating: *"Without onboarding, beginners bounce before discovering any other feature. Every other feature's value is gated by this."* Yet the PM plan defers C58 to Sprint 13 — two full sprints after Sprint 10 completes. This is a direct contradiction.

If onboarding truly gates all other features' value, then building C42 (Screener), C51 (Heatmap), and C56 (Explain This Metric) before C58 means those features will be discovered and used by users who have no context for what they're looking at. The team is building advanced tools for users who haven't been onboarded.

**Specific challenge**: Why is C58 not in Sprint 11 or 12? The Developer estimates C58 at 16-22h and notes it's blocked by D24 (business_card extraction) — but D24 is already planned for Sprint 11. Once D24 completes in Sprint 11, C58 is unblocked. There is no technical reason to defer it to Sprint 13.

#### Challenge 1.2: C43 Snowflake Health Visualization Is Missing From All Sprint Plans

The Designer ranks C43 (Company Snowflake Health Visualization) as **#2 UX impact** — the feature that makes the "ten-second test" visual. The Designer states: *"This is the FIRST thing a user sees"* on the business card page. Yet C43 appears in **none** of the sprint plans from any role. It's not in Sprint 11, 12, 13, 14, or 15+.

This is a significant omission. If the product's core promise is that a beginner can understand a company in 10 seconds, the Snowflake visualization is the single most important feature to deliver on that promise. The team is planning 5 sprints of features without addressing the #2 UX priority.

**Specific challenge**: Where is C43 in the sprint plan? If it's not included, what is the rationale for deprioritizing the feature that directly delivers on the "ten-second test" design principle?

#### Challenge 1.3: C44 and C45 Are Already Built — Why Does the Designer Treat Them as Future Work?

The Developer explicitly notes that C44 (Risk Analysis) and C45 (Valuation Band Chart) are **already implemented** (C44 in Sprint 3 as risk_analyzer.py, C45 in Sprint 2). Yet the Designer ranks C45 as "#5 — Highest ROI" and C44 as "#9 — Historian Differentiator" in the future backlog. This suggests either:
1. The Designer was unaware these features exist, or
2. The existing implementations don't meet the design vision and need redesign

**Specific challenge**: Are C44 and C45 already implemented in a form that satisfies the design requirements? If not, should the sprint plan include redesign work? If yes, the Designer's priority rankings are misleading.

#### Challenge 1.4: Direction A Prioritization vs. Product Positioning

The Architect prioritizes Direction A (Discovery & Screening) as HIGHEST, arguing that C42 (Stock Screener) addresses the #1 competitive gap. However, the product's core positioning is *"historian, not stock picker"* and *"education-first."* A stock screener is fundamentally a **discovery/selection tool** — it helps users find stocks to invest in. This is closer to "stock picker" territory than "historian."

The Designer's top priorities (C58 Onboarding, C43 Snowflake, C56 Explain This Metric) are all **education-first** features that align with the "historian" positioning. The Architect's prioritization may be optimizing for competitive parity (matching 財報狗's screener) rather than product differentiation.

**Specific challenge**: Is the team building a stock discovery tool (Direction A) or an education platform (Direction B)? The current plan prioritizes the former while the product vision emphasizes the latter. How does C42's "stable dividends" preset align with "historian, not stock picker"?

#### Team Response

The team should:
1. **Move C58 to Sprint 12** at the latest — it's unblocked after D24 in Sprint 11 and is the Designer's #1 retention-critical feature
2. **Add C43 to Sprint 12 or 13** — it directly delivers on the ten-second test and should not be absent from a 5-sprint plan
3. **Clarify C44/C45 status** — if already built, remove from future backlog; if needing redesign, add to sprint plan explicitly
4. **Reconcile Direction A priority with product positioning** — either reframe C42 as an educational discovery tool (not investment selection) or acknowledge the tension and adjust priorities

---

### Round 2: Priority Challenge

#### Challenge 2.1: Sprint 12 Is Dangerously Overloaded

The PM's Sprint 12 plan includes R5 + C42 + C56 + C62 at 37-52h. The Developer's version is similar at 37-52h. However, the Developer's own recommendation states: *"Total sprint capacity: 30-50h (assuming 1 developer, part-time). Don't overload sprints."* Sprint 12's upper bound (52h) exceeds even the generous capacity estimate.

C42 alone is 18-26h (Developer's adjusted estimate). C56 is 10-14h. R5 is 3-4h. C62 is 6-8h. That's 37-52h with **zero buffer** for code review, testing, bug fixes, or the inevitable scope discovery that comes with a first-of-its-kind feature like C42.

**Specific challenge**: What is the contingency plan if C42 exceeds its 26h estimate? The Developer notes *"財報狗 took years to build theirs"* and *"Start with top 200 stocks only"* — suggesting the scope is already being managed down. If C42 is scoped down to top 200 stocks, does it still deliver the intended value? If not, should it be split into two sprints?

#### Challenge 2.2: Sprint 13 Is Even Worse — 44-62h

The PM's Sprint 13 (C58 + C48 + C68 + C84) at 44-62h is the heaviest sprint in the plan. The Developer's version is identical. This sprint is described as "content-creation heavy" — but the estimates appear to be **code-only estimates** that don't account for content creation.

The Architect notes that C47's content creation is *"~60-70% of the effort."* If the same ratio applies to C68 (Concept Storytelling) and C58 (Onboarding), then the real effort for Sprint 13 could be **80-100h** when content creation is included.

**Specific challenge**: Are the Sprint 13 estimates realistic when content creation is factored in? The team should either: (a) separate content creation into a parallel track with dedicated resources, or (b) reduce the sprint to 2 features with content creation included in the estimates.

#### Challenge 2.3: R3 Is a Hard Prerequisite But Has No Fallback Plan

All three roles identify R3 (Batch API calls) as a **hard prerequisite** for C42 (Stock Screener). The Architect states: *"Without R3, this entire direction is blocked."* The Developer states: *"C42 will be unusably slow without batch fetching."*

Yet R3 is estimated at only 1-2h in Sprint 11. If R3 takes longer than expected, or if the batch API approach doesn't work with the data provider's API limits, the entire Sprint 12 plan collapses. There is no fallback plan, no alternative approach, and no risk mitigation beyond "do R3 first."

**Specific challenge**: What is the Plan B if R3 cannot be completed in Sprint 11? Should the team pre-define a degraded-mode C42 (e.g., screening only top 50 stocks sequentially) that works without R3? Or should Sprint 12 be restructured to be independent of R3's success?

#### Challenge 2.4: D16 and D24 Are Scheduled Together in Sprint 11 — Is This Wise?

Sprint 11 includes both D16 (split analogy_engine.py, 850 lines, 6 responsibilities) and D24 (extract business_card.py, 561 lines) alongside R3, C53, and C51. That's **two major refactoring efforts** plus a new feature (C51) plus a quick win (C53) in one sprint.

D16 and D24 are both high-risk refactoring tasks that touch core modules. If either refactor introduces regressions, the other refactor becomes harder to test and debug. The Developer's own dependency graph shows D16 and D24 as parallel prerequisites for multiple downstream features.

**Specific challenge**: Should D16 and D24 be split across Sprint 11 and Sprint 12 to reduce risk? Or does the team need both completed before any feature work can safely proceed? If the latter, Sprint 11 should be reframed as a "debt sprint" with minimal feature work.

#### Team Response

The team should:
1. **Reduce Sprint 12 to 3 features max** — defer C62 to Sprint 13 to create buffer for C42's uncertainty
2. **Restructure Sprint 13** — either reduce to 2 features or explicitly budget for content creation (double the content-heavy estimates)
3. **Define a R3 fallback** — pre-specify a degraded C42 mode that works without batch API, ensuring Sprint 12 isn't blocked
4. **Consider a "debt-first" Sprint 11** — if D16 and D24 are truly critical-path, reduce Sprint 11 feature work to only C53 (quick win) and defer C51 to Sprint 12

---

### Round 3: Goal Alignment Challenge

#### Challenge 3.1: The Plan Optimizes for Competitive Parity, Not Differentiation

The Architect's primary argument for Direction A (C42 Screener) is that it addresses the *"#1 gap across all 9 rounds of competitor research."* But the product's stated differentiation is being a **"historian, not stock picker"** — the opposite of a stock screener.

Looking at the Designer's "Competitor Patterns to Avoid" table, the team explicitly rejects: black-box scoring, AI stock picking, social trading, buy/sell signals, and dense data tables. Yet C42 with its "stable dividends" and "cheap valuation" presets is functionally a **stock selection tool** — it tells users which stocks match investment criteria.

Meanwhile, the features that truly differentiate Stock Explorer — C44 Risk Analysis (no TW competitor has it), C46 Moat Analysis (unique TW differentiator), C58 Onboarding (retention-critical) — are deferred to later sprints or missing entirely.

**Specific challenge**: Is the team building a differentiated product or catching up to 財報狗? If the answer is "both," what is the ratio? The current plan is approximately 70% competitive parity (C42, C51, C49) and 30% differentiation (C58, C56, C68). Should this ratio be inverted?

#### Challenge 3.2: The "Ten-Second Test" Is Not Enforced by the Sprint Plan

The "ten-second test" is a core design principle: *"A beginner should be able to understand a company within 10 seconds of landing on its page."* The Designer identifies C43 (Snowflake) and C48 (Story Card) as the primary enablers of this test.

Yet the sprint plan:
- C43 (Snowflake): **Not in any sprint**
- C48 (Story Card): Sprint 13
- C56 (Explain This Metric): Sprint 12
- C58 (Onboarding): Sprint 13

This means that for Sprints 11-12 (approximately 4-6 weeks of development), the product will have **no features that directly enforce the ten-second test**. Users arriving at the business card page will see the same data-dense layout that currently exists.

**Specific challenge**: If the ten-second test is a core design principle, why are its primary enablers (C43, C48) deferred past features that don't address it (C42, C51, C53)? Should the ten-second test features be the highest priority until they ship?

#### Challenge 3.3: Three Roles, Three Different Priorities — No Clear Resolution

The three roles have fundamentally different priority orderings:

| Priority | Architect | Designer | Developer |
|----------|-----------|----------|-----------|
| 1st | C42 Screener | C58 Onboarding | D16 + D24 (debt) |
| 2nd | C58 Onboarding | C43 Snowflake | C51 Heatmap |
| 3rd | C56 Explain | C56 Explain | C42 Screener |

The Architect and Designer disagree on whether C42 or C58 is the top priority. The Developer focuses on debt remediation first. The PM consolidation attempts to split the difference but ends up satisfying none of the roles fully — C42 is prioritized (Architect happy) but C58 is deferred (Designer unhappy), and debt is addressed (Developer happy) but C43 is ignored (Designer unhappy).

**Specific challenge**: Has the team established a clear decision-making framework for resolving priority conflicts? If the product vision is "education-first," shouldn't the Designer's UX-driven priorities take precedence over the Architect's competitive-gap analysis?

#### Challenge 3.4: Content Creation Bottleneck Is Systematically Underestimated

The Architect notes that content creation is *"the real bottleneck for education features."* The Developer notes that content-heavy features should budget *"30-50% of effort for content, not code."* Yet the sprint plan treats content creation as invisible:

- C58 (Onboarding): 14-20h estimate, but requires writing 5 screens of tutorial content
- C47 (Academy): 20-30h estimate, but requires 10-15 lessons in TW Chinese
- C68 (Storytelling): 12-16h estimate, but is "mostly writing, minimal code"
- C56 (Explain): 12-16h estimate, but requires 30-50 metric explanations

If content creation is 40% of effort on average, the real cost of Direction B is **78-112h**, not 56-80h. This is a significant planning gap.

**Specific challenge**: Should the team create a separate content creation track that runs in parallel with development? Or should the sprint estimates be updated to include content creation, which would reduce the number of features per sprint?

#### Team Response

The team should:
1. **Clarify the product identity question** — Is Stock Explorer a stock discovery tool or an education platform? The answer should drive priority decisions. If education-first, Direction B should be higher priority than Direction A.
2. **Enforce the ten-second test as a gating criterion** — No sprint should ship without at least one feature that directly improves the ten-second test. C43 and C48 should be in Sprints 11-12.
3. **Establish a priority resolution framework** — When roles disagree, the decision should be driven by: (a) product vision alignment, (b) user retention impact, (c) technical risk. By this framework, C58 (retention-critical, vision-aligned, medium risk) should outrank C42 (competitive parity, vision-neutral, high risk).
4. **Budget for content creation explicitly** — Add a content creation line item to each sprint that includes content-heavy features. Reduce feature count per sprint accordingly.

---

### Final Verdict

❌ **REJECTED — Requires Revision**

The team's preliminary decision has significant structural problems that must be addressed before the plan can be approved:

**Critical Issues:**
1. **C58 (Onboarding) is deferred to Sprint 13** despite being the Designer's #1 retention-critical feature and the gating feature for all other features. This is the single biggest flaw in the plan.
2. **C43 (Snowflake) is absent from all sprint plans** despite being the #2 UX priority and the primary enabler of the "ten-second test" — a core design principle.
3. **Sprint 12 (37-52h) and Sprint 13 (44-62h) are overloaded** and don't account for content creation effort, code review, testing, or risk buffer.
4. **The plan optimizes for competitive parity over differentiation**, contradicting the "historian, not stock picker" positioning.
5. **No fallback plan exists for R3** — if the batch API approach fails, Sprint 12 collapses entirely.
6. **Content creation is systematically underestimated** across all education features, creating a planning gap of 20-30%.

**Required Revisions Before Approval:**
1. Move C58 to Sprint 12 (unblocked after D24 in Sprint 11)
2. Add C43 to Sprint 12 or 13
3. Reduce Sprint 12 to 3 features maximum; defer C62
4. Restructure Sprint 13 to account for content creation (reduce to 2 features or double content estimates)
5. Define a R3 fallback plan for C42
6. Clarify C44/C45 status — remove from future backlog if already implemented
7. Establish a priority resolution framework for future disagreements

**What the plan gets right:**
- D16 and D24 are correctly identified as Sprint 11 priorities
- The 3-direction framework (Discovery, Education, Narrative) is sound
- The LLM layer (D5) is correctly deferred to Sprint 15+
- Community features (C64, C67, C89) are correctly identified as infeasible in Streamlit
- The Developer's sprint-by-sprint breakdown is detailed and well-reasoned

The plan is a solid foundation but needs the above revisions to be actionable and aligned with the product vision.
