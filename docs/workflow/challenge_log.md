# Challenge Log — Review Round 9

> **Date**: 2026-06-14
> **Challenger**: Challenger Role
> **Context**: Round 9 Review — Challenging the PM's consolidated review report covering 6 new features (C42-C47), 5 architecture debt items (R1-R5), 15 design issues (D-001 to D-015), and the revised sprint plan (5 sprints, 163-235h total).

---

## Round 1: Gap Authenticity

### Challenger Questions

#### CQ 1.1: Are C42 (Screener) and C43 (Snowflake) *really* P1 — or is this competitor FOMO?

The PM labels C42 and C43 as P1 because "every major competitor has them." But Stock Explorer's positioning is **"historian, not a stock picker."** A stock screener (C42) is fundamentally a *discovery/filtering* tool — it answers "which stocks meet my criteria?" That's a stock-picker question. The PM tries to reframe it as "discover interesting companies," but the UI described (filter by ROE > 15%, dividend yield > 4%) is functionally identical to screening for investment candidates. 

**Challenge**: Is C42 aligned with our positioning, or are we copying 財報狗 because they're the market leader? If our target user is a beginner who doesn't know where to start, wouldn't a curated "learning path" (C47) or "Read Next" (C41) be more aligned than a screener that requires understanding what ROE > 15% means?

Similarly, C43 (Snowflake) is labeled P1 because Simply Wall St and Morningstar have visual health scores. But those scores are *ratings* — they tell you "this is a 4-star stock" or "this snowflake is mostly green." That's a stock-picker signal. Our "historian" positioning says we should *explain*, not *rate*. The PM's own design review says the snowflake should have "plain-language explanations for each dimension" — but if you're explaining, you're not rating. **Is C43 a health *explanation* or a health *score*?** These are different things.

**Specific question**: If we strip away the rating/scoring aspect, what's left of C43 that's different from the existing "Operation Health Check" page?

#### CQ 1.2: C44 (Risk Analysis) — historian gold or scope trap?

The PM positions C44 as a "unique differentiator" because no TW competitor has plain-language risk analysis. But the description says each risk includes "(1) what the risk is, (2) historical evidence, (3) current indicators to watch." Item (3) — "current indicators to watch" — is predictive. It's telling users what to look for in the future. That's not "historian" behavior; that's advisory.

**Challenge**: Can we honestly build C44 without crossing into "stock picker" territory? The line between "here's what happened before" (historian) and "here's what to watch" (advisory) is thin. Has the team defined where that line is?

#### CQ 1.3: C46 (Moat Analysis) — unique differentiator or manual curation nightmare?

C46 is labeled P2 with 17-26h effort. The implementation plan says "manual curation for top 20 stocks, template-based for others." But Morningstar's moat rating covers *thousands* of stocks with a dedicated research team. We're proposing to cover 20 stocks manually and use templates for the rest.

**Challenge**: What does the "template-based for others" moat analysis look like? If the template says "this company has a [type] moat because [generic reason]," it's worthless. Moat analysis is inherently qualitative and company-specific. Either we invest in real research (way more than 17-26h) or we produce generic filler. Which is it?

#### CQ 1.4: C47 (Education Academy) — endgame or fantasy?

C47 is 32-46h in the developer estimates — nearly a full sprint by itself. The PM calls it the "long-term differentiator" and "endgame." But:
- It requires writing 10-15 structured lessons (content creation, not just coding)
- It requires quiz interactivity, progress tracking, mobile-responsive layout
- The developer notes "content creation is 40% of the effort"

**Challenge**: Is it honest to put a 32-46h feature in Sprint 5 with a "buffer" label? The PM's own handoff says "Daniel to confirm scope." If C47 is truly the "endgame," shouldn't it be a separate project phase, not squeezed into Sprint 5 alongside a buffer?

#### CQ 1.5: Architecture debt — is R2 really P1 "alongside Sprint 2"?

R2 (move UI helpers to ui_components.py) is 1-1.5h and labeled P1. But it's purely a code hygiene change — it doesn't affect any user-facing behavior. Meanwhile, R5 (migrate hardcoded data to YAML) is 4-6h and labeled P2 for Sprint 3.

**Challenge**: R5 directly enables C36 (Visual Revenue Tree), C41 (Read Next), and C46 (Moat Analysis) because all of them need curated data. If R5 slips to Sprint 3, those features in Sprint 3-4 are building on a foundation that's still using hardcoded Python dicts. Shouldn't R5 be P0 alongside R1?

#### CQ 1.6: D-001 and D-002 as P0 — correct or inflated?

D-001 (no visual health score) and D-002 (no synthesis layer) are labeled P0 because they "violate core design principles" (ten-second test, story first). But:
- The ten-second test says "a beginner can restate the core concept within ten seconds" — that's about *comprehension*, not about having a visual score
- The existing one-liner, "Did You Know?" facts, and analogy engine already provide synthesis at a textual level
- Simply Wall St's snowflake is beautiful, but does it actually help beginners *understand* the company, or does it just give them a quick visual shortcut that replaces understanding?

**Challenge**: Is the ten-second test best served by a visual score (which gives an *answer*) or by better narrative structure (which builds *understanding*)? If it's the latter, then D-001 and D-002 should be about improving the narrative flow, not adding visual ratings. The current P0 framing assumes the solution (visual score) rather than diagnosing the real problem.

#### CQ 1.7: What are competitors NOT building that we SHOULD?

The competitor analysis is entirely focused on "what do they have that we don't?" But the most valuable question is the inverse: **what are competitors NOT building that we could?**

- No competitor combines narrative timeline (C34) with relationship-based recommendations (C41) — this is our unique "historian" path
- No competitor has a "Company Story" tab that weaves events, revenue, and price into a narrative — C34 from Round 7 is still not approved
- No competitor has point-to-point group structure with ownership percentages — we already have this

**Challenge**: Why is C34 (Company Story Timeline) — identified in Round 7 as the "#1 thing competitors DON'T have" — not in the sprint plan at all? It's been 2 rounds since identification. If it's truly our unique differentiator, why are we prioritizing competitor-copying features (C42, C43) over it?

### Team Responses (PM synthesis)

**To CQ 1.1**: C42 is reframed as "discovery" not "screening" — the historian angle is "learn about companies that match your curiosity" not "find stocks to buy." The beginner-friendly presets ("穩定收息", "成長潛力") are educational entry points, not investment filters. C43 is a health *explanation* visualized — each dimension has a plain-language description, not just a score. It differs from Operation Health Check by being a synthesized *overview* rather than a detailed *deep-dive*.

**To CQ 1.2**: C44's "indicators to watch" will be strictly historical — "here's what happened when X occurred in the past" not "watch for X in the future." The line is: we explain historical patterns, we don't make predictions. The implementation will use past event data only.

**To CQ 1.3**: C46 will start with top 10 stocks (not 20) with genuinely curated analysis. Template-based fallback will be a one-liner moat summary, not a full analysis. The 17-26h estimate includes research time for the top 10.

**To CQ 1.4**: C47 will be split: Phase 1 (10 lessons, 20h) in Sprint 5, Phase 2 (remaining lessons + progress tracking) as a separate post-plan item. Daniel to confirm.

**To CQ 1.5**: R5 is moved to P1 — will be done alongside R1 in Pre-Sprint 2. This ensures C36, C41, and C46 build on YAML data.

**To CQ 1.6**: D-001 and D-002 remain P0 because the ten-second test requires *instant comprehension*. Text-based synthesis (one-liner, Did You Know) requires reading and cognitive processing. A visual score provides instant pattern recognition. Both are needed — text for depth, visual for immediacy.

**To CQ 1.7**: C34 (Company Story Timeline) is deferred but not forgotten. It requires C38 (Compare Stories) data structures as a prerequisite. C38 is in Sprint 3, so C34 would naturally follow in Sprint 4-5 as an extension. The team acknowledges this should be explicitly tracked.

---

## Round 2: Priority

### Challenger Questions

#### CQ 2.1: Sprint 2 is overloaded — C37 + C39 + C45 + C43 = 49.5h

Sprint 2 contains 4 features totaling 49.5h (midpoint) in a 60h sprint. That's 82.5% utilization before accounting for:
- R2 (1.5h) and R4 (2h) that are also "alongside Sprint 2"
- D-003 (card standardization, 2-3h) and D-004 (design_system.md, 2-3h)
- Code review, testing, bug fixes, context switching

**Challenge**: The realistic Sprint 2 load is 49.5 + 1.5 + 2 + 2.5 + 2.5 = **58h** — leaving only 2h of buffer. If any single feature runs over (C43 has "radar normalization" risk, C45 has "date parsing" risk), the sprint slips. Shouldn't C43 (the riskiest Sprint 2 feature) move to Sprint 3?

#### CQ 2.2: C43 (Snowflake) in Sprint 2 is premature

C43 requires:
- R1 (shared financial metrics) as a prerequisite — correct
- Radar chart normalization — the existing `create_comparison_radar()` passes *raw values*, not normalized scores
- Defining a "health score" formula across 5 dimensions
- Industry benchmarking for scoring

**Challenge**: C43 is essentially building a proprietary scoring algorithm. This is research work, not just implementation work. Simply Wall St's snowflake took years to develop. We're allocating 17-24h. Is it honest to say we can build a meaningful health visualization in Sprint 2, or will we produce a pretty chart with arbitrary scores?

#### CQ 2.3: C42 (Screener) in Sprint 4 — too late or correctly placed?

The PM puts C42 in Sprint 4, after R3 (batch API) is done. But C42 is labeled P1 and "transforms the product." Meanwhile, C36 (Visual Revenue Tree, P2) is also in Sprint 4, and C46 (Moat Analysis, P2) makes Sprint 4 the heaviest sprint at 58.5h.

**Challenge**: If C42 truly "transforms the product from lookup to discovery," shouldn't it be in Sprint 3? The answer is: beginners can't *use* Stock Explorer effectively if they don't know which stock to search for. Every feature after C42 (C44, C45, C46, C47) is only useful if users can find companies to apply them to. C42 should be the gateway.

Conversely, if C42 is correctly in Sprint 4, then C46 (Moat Analysis) should move to Sprint 5 — Sprint 4 at 58.5h is already over capacity.

#### CQ 2.4: The 163-235h total — what's being underestimated?

The PM's total is 163-235h (midpoint 199h). But looking at the developer's estimates:
- C38 was revised from 8-10h to 10-12h (+2h)
- C39 was revised from 5.5h to 6-8h (+1.5h)
- C36 was confirmed at 8-10h (top of range)
- C47 content creation is 40% of effort — is that included in the 32-46h?

**Challenge**: The PM uses midpoint estimates for the sprint plan, but the *high* estimates are 235h. At the high end, Sprint 2 would be 49.5h → ~55h, Sprint 3 would be 41.5h → ~48h, Sprint 4 would be 58.5h → ~67h (over capacity!), Sprint 5 would be 60h → ~68h (also over!). **The plan only works if every feature comes in at the low-to-mid estimate.** What's the contingency if estimates run high?

#### CQ 2.5: Should any features be cut or deferred?

Looking at the full feature set:
- C36 (Visual Revenue Tree) — P2, 8-10h, extends existing pie chart
- C44 (Risk Analysis) — P2, 15-22h, unique but risky (predictive drift)
- C46 (Moat Analysis) — P2, 17-26h, manual curation bottleneck
- C47 (Education Academy) — P2, 32-46h, content creation heavy

**Challenge**: If we need to cut one feature to make the plan realistic, which one? C46 is the weakest value proposition — it requires manual research, the template fallback is generic, and it's the least "historian" feature (moat analysis is inherently forward-looking). C47 is the most strategically important but also the most effort. Should C46 be cut and its sprint time reallocated to C47 Phase 1?

### Team Responses (PM synthesis)

**To CQ 2.1**: Sprint 2 is tight but manageable. R2 and R4 are Pre-Sprint 2 items (moved there alongside R1 and R3). D-003 and D-004 are designer tasks that run in parallel with developer work — they don't consume sprint capacity. The real Sprint 2 developer load is 49.5h in 60h, leaving 10.5h buffer. This is acceptable.

**To CQ 2.2**: C43 will use a simple, transparent scoring formula (e.g., percentile rank within industry for each dimension). No proprietary algorithm — just "this company's ROE is in the top 20% of its industry." The plain-language explanation makes the score educational, not authoritative. Sprint 2 is correct because C37 + C43 together address both P0 design issues (D-001 and D-002).

**To CQ 2.3**: C42 stays in Sprint 4 because it depends on R3 (batch API) which is Pre-Sprint 2. The screener needs fast data loading to be usable — without R3, filtering 1,800 stocks would take minutes. C46 moves from Sprint 4 to Sprint 5 (swapping with C47 Phase 1). Revised Sprint 4: C36 + C42 = 37h. Revised Sprint 5: C46 + C47 Phase 1 + buffer = 58h.

**To CQ 2.4**: The team acknowledges the plan is optimistic at the high end. Contingency: if any sprint runs over, the buffer in Sprint 5 (now reduced) absorbs the overflow. If multiple sprints run over, C47 Phase 2 is deferred. The 199h midpoint is the realistic target; 235h is the worst case requiring scope reduction.

**To CQ 2.5**: C46 is deferred to Sprint 5 (per CQ 2.3 resolution). No features are cut, but C47 is explicitly split into Phase 1 (Sprint 5) and Phase 2 (post-plan). C46 is the lowest-priority P2 feature and would be the first to be cut if the plan slips.

---

## Round 3: Goal Alignment

### Challenger Questions

#### CQ 3.1: Does the plan align with "historian, not a stock picker"?

The product vision says: "Do not say buy or sell; only explain what has happened to the company over time." Let's audit the 6 new features:

| Feature | Historian-aligned? | Concern |
|---------|-------------------|---------|
| C42 Screener | ⚠️ Borderline | Filters imply "good" vs "bad" companies |
| C43 Snowflake | ⚠️ Borderline | Scores imply "healthy" vs "unhealthy" |
| C44 Risk Analysis | ✅ Aligned | Historical risks, factual |
| C45 Valuation Band | ⚠️ Borderline | "Expensive vs cheap" is valuation language |
| C46 Moat Analysis | ❌ Misaligned | Moat durability is forward-looking |
| C47 Academy | ✅ Aligned | Pure education |

**Challenge**: 4 of 6 new features have "borderline" or "misaligned" ratings. The PM's plan is gradually turning Stock Explorer into a stock analysis platform (like Simply Wall St or Morningstar) rather than a "historian" platform. At what point does adding enough "analysis" features change the product's fundamental positioning?

#### CQ 3.2: Does the plan support the "ten-second test"?

The ten-second test says: "a beginner can restate the core concept within ten seconds." The plan addresses this with:
- C37 (Key Takeaways) — 3 bullet points, ≤ 200 characters total ✅
- C43 (Snowflake) — visual pattern recognition ✅

But the plan also adds:
- C44 (Risk Analysis) — 3-5 risks with evidence and indicators
- C45 (Valuation Band) — chart + interpretation
- C46 (Moat Analysis) — type + strength + evidence + explanation
- C42 (Screener) — filter UI + results list

**Challenge**: Each of these features adds *more information* to process. The ten-second test is about *reducing* cognitive load to a single core concept. Are we testing the ten-second test, or are we adding features and hoping the summary card (C37) compensates for the increased complexity? The business card page will eventually have: header, one-liner, Did You Know, C37, C43, C39, existing metrics, C45, C36, C44, C46, C41, news, disclaimer. That's 12+ sections. **How does a beginner find the "core concept" in that wall of information?**

#### CQ 3.3: Are there contradictions between features?

Several potential contradictions:

1. **C37 (Key Takeaways) vs C43 (Snowflake)**: Both claim to be the "ten-second answer." C37 says "here are 3 bullet points." C43 says "here's a visual score." Which one does the user look at first? If both are at the top of the page, they compete for attention. If one is above the other, the lower one is de facto less important.

2. **C39 (What Changed) vs Event Dashboard**: C39 shows "stock-specific recent changes" on the business card page. The Event Dashboard shows "portfolio-wide historical events." The PM acknowledges overlap but positions them as complementary. But a user seeing a "毛利率下降3%" delta on the business card and then seeing the same event on the Event Dashboard will wonder why the same information is shown twice.

3. **C42 (Screener) vs C41 (Read Next)**: C42 lets users filter stocks by criteria. C41 recommends related stocks. Both are discovery mechanisms. C42 is active (user-driven), C41 is passive (system-driven). Having both is fine, but they need to be positioned differently — otherwise users will use C42 and ignore C41.

**Challenge**: Has the team mapped the *user journey* through these features? Not just "what does each feature do" but "how does a beginner move from landing on the site to understanding a company"? Without a user journey map, features risk being a disconnected collection rather than a coherent experience.

#### CQ 3.4: What are the biggest risks to this plan?

**Risk 1: Feature creep on the business card page.** The business card page is becoming a dumping ground for every feature. Without a clear information architecture (what's above the fold, what's below, what's expandable), the page will become overwhelming — the exact problem the "historian" positioning is supposed to solve.

**Risk 2: C43 scoring model credibility.** If the snowflake scores are perceived as arbitrary or misleading, they'll undermine trust. Simply Wall St's snowflake is backed by proprietary research. Ours will be based on simple percentile rankings. Users may question "why is this dimension green?"

**Risk 3: C42 screener performance.** If R3 (batch API) doesn't achieve sufficient speedup, the screener will be unusable. 1,800 stocks with multiple filter criteria needs sub-second response times. The current category browser takes 30-60 seconds for 200 stocks.

**Risk 4: C47 content quality.** If the 10-15 lessons are generic or shallow, the academy will feel like a checkbox feature rather than a real educational resource. Content quality requires domain expertise and editorial review, not just YAML schema design.

**Risk 5: Mobile experience ignored.** Every competitor has a native mobile app. Stock Explorer is Streamlit-based with known mobile limitations. The plan doesn't address mobile at all. As features multiply, the mobile experience will degrade further.

**Challenge**: Which of these risks is the team most prepared to mitigate? Which ones are being ignored?

### Team Responses (PM synthesis)

**To CQ 3.1**: The team acknowledges the tension. The resolution: C43 will be explicitly framed as "health explanation" not "health score" — the visualization shows *what the metrics are*, not *whether they're good*. C45 will use "估值區間" (valuation range) language, not "expensive/cheap" language. C46 is the weakest historian fit and is deferred to Sprint 5 (lowest priority). C42 will use "探索" (explore) framing throughout — the screener is a "company discovery tool," not a "stock screening tool."

**To CQ 3.2**: The team agrees the business card page needs an information architecture overhaul. The plan: C37 and C43 are the "above the fold" ten-second answer. Everything else is below the fold or in tabs. The "beginner mode" concept (C40, not yet approved) would hide advanced sections by default. The team commits to a "one key point per page" audit before each sprint — if a new feature doesn't have a clear "one key point," it goes in a tab or below the fold.

**To CQ 3.3**: The team will create a user journey map in the next cycle. For now: C37 is the primary ten-second answer (text), C43 is the visual complement. They're designed to be complementary — C37 for "what to remember," C43 for "how to visualize." C39 and the Event Dashboard are differentiated by scope (single stock vs. portfolio) and time frame (recent changes vs. historical events). C42 and C41 are differentiated by user intent (active search vs. passive discovery).

**To CQ 3.4**: 
- Risk 1 (page overload): Mitigated by the "one key point per page" audit and tab-based organization
- Risk 2 (scoring credibility): Mitigated by transparent scoring methodology — show the formula, not just the result
- Risk 3 (screener performance): Mitigated by R3 being a hard prerequisite; if R3 doesn't achieve 5x speedup, C42 is deferred
- Risk 4 (content quality): Mitigated by starting with 5 pilot lessons (not 10) and getting Daniel's review before scaling
- Risk 5 (mobile): Acknowledged as a known limitation; no mitigation in this plan. Mobile redesign is a post-plan initiative.

---

## Final Verdict

### ❌ REQUIRES REVISION

The plan is strategically sound but has significant execution risks that need to be addressed before development begins. The core issues are:

1. **Business card page overload** — 12+ sections without clear information architecture
2. **Sprint 4 was over capacity** — now resolved by moving C46 to Sprint 5
3. **Historian positioning drift** — 4 of 6 new features are borderline misaligned; needs explicit framing
4. **C47 scope ambiguity** — needs Phase 1/Phase 2 split confirmed by Daniel
5. **No user journey map** — features risk being a disconnected collection

---

## Recommended Changes

### Required Before Sprint 2

1. **Move R5 to Pre-Sprint 2** (alongside R1) — ensures C36, C41, C46 build on YAML data
2. **Split C47 into Phase 1 (5 lessons, 12h) and Phase 2 (remaining, +20h)** — Phase 2 is post-plan
3. **Move C46 from Sprint 4 to Sprint 5** — Sprint 4 was at 58.5h (over capacity)
4. **Define the business card page information architecture** — what's above the fold (C37 + C43), what's below, what's in tabs
5. **Create a user journey map** — even a simple one showing "beginner's first 5 minutes"

### Required During Sprint 2

6. **C43 scoring transparency** — show the formula, not just the score; frame as "health explanation" not "health rating"
7. **C42 framing audit** — ensure all screener UI uses "探索" language, not investment language
8. **"One key point per page" audit** — before adding any new section, verify it has a single clear message

### Revised Sprint Allocation

| Sprint | Items | Hours (midpoint) | Capacity |
|--------|-------|-----------------|----------|
| Pre-Sprint 2 | R1 + R3 + R2 + R4 + R5 | 16h | ~30h |
| Sprint 2 | C37 + C39 + C45 + C43 | 49.5h | ~60h |
| Sprint 3 | C41 + C38 + C44 | 36.5h | ~60h |
| Sprint 4 | C36 + C42 | 37h | ~60h |
| Sprint 5 | C47 Phase 1 + C46 + buffer | 52h | ~60h |

**Revised Grand Total**: 16h (debt) + 49.5 + 36.5 + 37 + 52 = **191h** (midpoint, down from 199h due to C47 Phase 2 deferral)

### Open Questions for Daniel

1. **C47 Phase 1 scope**: 5 lessons (12h) or 10 lessons (20h)?
2. **C42 priority vs C46**: If Sprint 4 slips, which gets cut — screener or moat?
3. **C34 (Company Story Timeline)**: When does this unique differentiator get scheduled?

---

*Challenge conducted by Challenger Role, Round 9 Review Cycle*
*Date: 2026-06-14*
