# Challenger Discussion — Round 8 Feature Priority Challenge

> **Date**: 2026-06-13
> **Author**: Challenger
> **Context**: Challenging the team's preliminary priority decision for Round 8 features (C36-C41).
> **Product Vision**: "Historian, not stock picker" — educational, beginner-focused.
> **Core Values**: (1) Story first, data second, (2) PPT-style presentation, (3) Adaptive and self-evolving, (4) Point-to-point knowledge construction, (5) Benchmark-oriented analysis.
> **Key Design Principle**: The ten-second test — a beginner must understand the core concept within 10 seconds.
> **Current State**: Sprint 0 complete, Sprint 1 starting (C28 Spike + LLM Architecture). 5-sprint roadmap approved.

---

## Table of Contents

1. [Pre-Challenge Observations](#pre-challenge-observations)
2. [Round 1: Feature Direction Challenge](#round-1-feature-direction-challenge)
3. [Round 2: Priority & Sprint Allocation Challenge](#round-2-priority--sprint-allocation-challenge)
4. [Round 3: Goal Alignment & Risk Assessment](#round-3-goal-alignment--risk-assessment)
5. [Verdict & Recommendations](#verdict--recommendations)

---

## Pre-Challenge Observations

Before diving into the three rounds, I want to note several structural observations that inform my challenge:

### What the team got right
- **C37 (Key Takeaways) as #1** is uncontroversial. All three roles rank it first or second. It directly addresses the ten-second test — our most critical design principle.
- **C38 (Compare Stories) at Sprint 5** is the right call. It's the most complex, least beginner-critical, and depends on LLM architecture decisions.
- **The developer's bundling insight** (C37+C39+C41 sharing infrastructure) is architecturally sound and should be taken seriously.

### Structural tensions I see
1. **The designer fundamentally disagrees with the architect on C36 vs C41 priority** — this isn't just a ranking difference, it reflects a philosophical split on whether visual storytelling (C36) or knowledge path-building (C41) better serves beginners.
2. **The designer's "beginner mode by default" recommendation directly contradicts the architect's toggle approach** — this is a design system decision, not just a priority question.
3. **The developer's V/E ranking puts C39 first**, while the PM consolidation puts C37 first. Both are defensible, but the reasoning differs.
4. **C38 at Sprint 5 may be too late** if it's the single most "historian-aligned" feature, as the architect notes.

---

## Round 1: Feature Direction Challenge

### 1.1 Do these 6 features truly align with the "historian" positioning?

**Assessment: Mostly yes, but with important caveats.**

| Feature | Historian Alignment | Analysis |
|---------|-------------------|----------|
| **C37** Key Takeaways | ✅ Strong | Synthesizes data into narrative understanding. A historian doesn't just show facts — they tell you what matters. |
| **C36** Revenue Tree | ✅ Strong | Shows *how money flows through a business* — this is business model storytelling, not just data display. |
| **C39** What Changed | ✅ Strong | Makes data feel alive. A historian explains *what happened recently* and *why it matters*. |
| **C41** Read Next | ✅ Strong | Creates learning paths between companies. A historian connects stories across time and entities. |
| **C38** Compare Stories | ✅ Strongest | This is the MOST historian-aligned feature — comparing narratives is what historians do. But it's also the hardest to execute. |
| **C40** Mode Toggle | ⚠️ Weak | This is a UX convenience feature, not a historian feature. It doesn't teach, narrate, or contextualize. It just hides/shows content. |

**Key concern**: C40 is the weakest historian feature. The designer's recommendation to replace it with "beginner mode by default" is actually more aligned with the historian positioning — it forces us to design every page as a clear narrative rather than relying on a toggle to clean up a cluttered expert view.

### 1.2 Are there better directions we're missing?

**Yes. Three gaps I see:**

**Gap 1: No "Why Should I Care?" feature.**
All 6 features are about presenting existing data better. None answer the fundamental beginner question: "Why should I care about this company?" The closest is C37 (Key Takeaways), but even that synthesizes *existing* data rather than providing *contextual motivation*. A true "historian" would explain why this company matters in the broader economic story.

**Gap 2: No temporal narrative feature in this batch.**
C28 (Story Timeline) is in Sprint 3, but none of the C36-C41 features add temporal narrative to the business card page. C39 (What Changed) is the closest, but it's a delta card, not a narrative. We're missing "the story so far" on the main page.

**Gap 3: No "common beginner mistakes" or "what experts know" feature.**
The designer's PPT-style approach is about simplification, but there's an educational opportunity in explicitly teaching beginners what to look for. None of these features include an educational overlay.

**However**, I recognize these gaps might be better addressed through content strategy (C31 Daily Story, C28 Story Timeline) rather than new features. I raise them to ensure we're not over-indexing on presentation features at the expense of educational depth.

### 1.3 How do competitors handle these? Why are we doing it this way?

From the competitor research context:
- **Key Takeaways (C37)**: No TW competitor has auto-generated key takeaways. This is a genuine differentiator. Most competitors show raw metrics with tooltips. Our approach of synthesizing 3-5 plain-language bullets is unique.
- **Revenue Tree (C36)**: Some competitors (e.g., Finviz) have sector maps, but none show customer-supplier hierarchies for TW stocks. Our manual curation approach is necessary because FinMind doesn't provide this data.
- **Compare Stories (C38)**: Competitors do metric comparison well (Yahoo Finance, Finviz). Narrative comparison is rare. This could be a differentiator but also a risk — if the narrative feels shallow, it's worse than no narrative.
- **Mode Toggle (C40)**: Most competitors don't have mode toggles. They either show everything (expert-oriented) or have separate beginner/advanced pages. Our toggle approach is more elegant but also more complex to maintain.

**My concern**: We're building features that competitors don't have, which is good for differentiation but risky for validation. We should be especially careful about C38 and C40 — if competitors don't do narrative comparison or mode toggles, it might be because the UX doesn't work, not because they haven't thought of it.

### 1.4 Challenge C37: Is rule-based synthesis good enough? Won't it feel generic?

**This is my strongest challenge in Round 1.**

The architect proposes a rule-based algorithm:
1. Always include the one-liner
2. Include the most "impressive" metric
3. Include a trend observation
4. Include a "did you know" fact
5. Cap at 5 bullets

The developer adds curated takeaways for top 20 stocks as a fallback.

**My concerns:**

1. **Rule-based synthesis WILL feel generic for non-top-20 stocks.** The architect acknowledges this (Risk: "Rule-based summaries feel generic/repetitive" — Medium severity). But the mitigation is "acceptable for P2" and "can be enhanced with LLM later." This is a cop-out. If the feature is our #1 priority and defines the ten-second test, "acceptable for P2" isn't good enough.

2. **The selection logic is naive.** "Highest absolute value among gross_margin, roe, revenue_yoy, dividend_yield" — this will produce bizarre results. A company with 80% revenue YoY (but tiny revenue) will get highlighted over a company with 55% gross margin (but massive scale). The algorithm doesn't account for industry context, company scale, or what's actually interesting.

3. **The designer's template-first approach is better but underexplored.** The designer recommends "template-based generation (rule-based, not LLM) for the top 20 stocks. Manual review before shipping." This is the right instinct, but it's listed as a risk mitigation, not the primary approach.

**My recommendation**: C37 should use **curated templates for top 20 stocks as the PRIMARY approach**, with rule-based generation as a fallback for stocks without templates. The 6.5h developer estimate includes 2.5h for "curated takeaways for top 20 stocks" — this should be the main deliverable, not an enhancement.

### 1.5 Challenge C40: Is a toggle the right approach vs "beginner by default"?

**The designer is right. The toggle is the wrong approach.**

Here's why:

1. **Zone violation.** The architect proposes putting the toggle in the navbar (Zone A). The designer correctly identifies this as a Zone A violation — "Zone A must NOT contain: search box, filters, or any interactive controls." The architect's own design system rules forbid this.

2. **Maintenance burden.** The architect acknowledges "every new feature must consider both modes" (Medium risk). For a small team, this is a significant ongoing cost. Every future feature will need two rendering paths, two test matrices, two design reviews.

3. **The toggle contradicts PPT style.** Expert mode showing "everything per page" violates the "one key point per page" principle. The designer notes: "Even in expert mode, maintain PPT style. Show more sections, but each section still has one key point." But this means expert mode isn't really "show everything" — it's "show more PPT-style sections." Which is just... the natural evolution of the product.

4. **"Beginner by default" achieves the same goal more elegantly.** If every page is designed for beginners first, with progressive drill-down for detail, we get the beginner experience without the toggle. Users who want more detail can click into sections. This is the existing design philosophy (progressive drill-down) extended consistently.

5. **The toggle is a crutch.** If we need a toggle to make the product usable for beginners, the product isn't designed well enough. The toggle should be unnecessary if we follow the ten-second test rigorously.

**My recommendation**: **Deprioritize C40 entirely.** Replace it with a design principle: "Every page must pass the ten-second test in its default state. Advanced detail is always one click away." This achieves the designer's "beginner mode by default" without the engineering cost of a toggle.

---

## Round 2: Priority & Sprint Allocation Challenge

### 2.1 Is the sprint allocation correct?

**The PM consolidation allocation:**

| Sprint | Features | Base Hours | With 50% Buffer |
|--------|----------|------------|-----------------|
| Sprint 2 | C37 + C39 | 12-17h | 18-25.5h |
| Sprint 3 | C41 + C36 | 14-21h | 21-31.5h |
| Sprint 4 | C40 | 10-15h | 15-22.5h |
| Sprint 5 | C38 | 10-14h | 15-21h |

**My assessment:**

**Sprint 2 (C37 + C39): Reasonable, but tight.**
- C37 (6.5h) + C39 (5.5h) = 12h base. With the developer's bundling insight (shared analogy_engine work), this could be ~10h.
- However, Sprint 2 already has D02 (7h) + C31 (11h) = 18h base. Adding C37 + C39 would make Sprint 2 = 30h base, which is way over the 15h base + buffer.
- **The PM consolidation doesn't account for existing Sprint 2 commitments.** This is a serious oversight.

**Wait — re-reading the handoff:** Sprint 2 has D02 (7h base, 10.5h buffered) + C31 (11h base, 16.5h buffered). That's already 18h base / 27h buffered. Adding C37 + C39 (12h base) would make it 30h base — far exceeding any reasonable sprint capacity.

**This means the PM consolidation's Sprint 2 allocation is only feasible if C37 + C39 are bundled into the existing Sprint 2 work**, which is what the developer's "Sprint 2a" suggestion implies. But the developer's Sprint 2a includes C37 + C39 + C41 = 18.5h, which is even larger.

**I think there's a fundamental sprint capacity problem here.** The existing roadmap already has:
- Sprint 2: D02 + C31 = 18h base
- Sprint 3: C28 = 20h base
- Sprint 4: C07 + C14 = 17h base
- Sprint 5: C29 = 10h base

Adding 40h of C36-C41 features across Sprint 2-5 means we need to either:
(a) Extend the roadmap to Sprint 6
(b) Reduce scope of existing features
(c) Accept that sprints will be overloaded

**None of these options are discussed in the PM consolidation.** This is a critical gap.

### 2.2 Should C39 really be bundled with C37 in Sprint 2, or deferred?

**C39 should NOT be bundled with C37 in Sprint 2. Here's why:**

1. **Sprint 2 is already overloaded.** D02 + C31 = 18h base. Adding C39 (5.5h) makes it 23.5h — before C37.

2. **C39 is the lowest-risk feature to defer.** It's a presentation-layer repackaging of existing data. It doesn't create new infrastructure. It can be added to the business card page in any sprint without blocking other work.

3. **C39's value is complementary to C37, not dependent on it.** The delta card doesn't need the key takeaways card to function. Deferring C39 to Sprint 3 doesn't lose any synergy.

4. **The developer's V/E ranking puts C39 first**, which suggests it's a quick win. But quick wins in an overloaded sprint don't help — they just add to the overload.

**My recommendation**: Defer C39 to Sprint 3. Sprint 2 should focus on C37 (the ten-second test gate) alongside D02 + C31. C39 can be added to the business card page in Sprint 3 when there's more capacity.

### 2.3 Should C36 data curation be a blocker or can we ship with fewer ships?

**We should ship with fewer stocks. Here's why:**

1. **The architect says "Start with top 10 stocks, not 20" in the risk summary.** This is the right call. The developer estimates 2-3h for data curation regardless of the number of stocks (the research time per stock decreases after the first few).

2. **Manual curation doesn't scale.** The architect acknowledges this (Medium risk). Starting with top 10 stocks (TSMC, 鴻海, 聯發科, 台達電, 富邦金, 台泥, 中鋼, 台塑, + 2 more) covers the most-seen companies. Beginners are most likely to search for these.

3. **The pie chart fallback already exists.** For non-curated stocks, the existing pie chart is shown. This is a graceful degradation that doesn't require engineering — just a tab that shows the pie chart when tree data is unavailable.

4. **Shipping with 10 stocks and expanding later is better than delaying the feature for 20 stocks.** The feature's value is in the visualization concept, not the coverage. Once the treemap works for 10 stocks, adding more is pure data entry.

**My recommendation**: Ship C36 with top 10 stocks. Reduce data curation from 4-5h to 2-3h. This brings C36's total to ~8-10h, making it more feasible for Sprint 3.

### 2.4 Is C38 at Sprint 5 too late?

**Yes, and this is my strongest challenge in Round 2.**

The architect says: *"C38 (Compare Stories) is the most aligned with the historian vision but also the most technically risky — deferring it is the right call."*

**I disagree.** Here's why:

1. **C38 is the purest expression of "historian, not stock picker."** Comparing two companies' stories — their business models, key events, revenue trajectories — is exactly what a historian does. It's not about picking stocks; it's about understanding business narratives in context.

2. **The designer's ten-second test concern is valid but solvable.** The designer notes C38 "likely fails the ten-second test for beginners" because "comparing two narratives requires holding two mental models simultaneously." But the designer also provides a mitigation: "Frame the entire comparison as ONE key point: 'These two companies have different business strategies.' The two columns serve that single point." This is exactly right.

3. **Phase 1 (structured comparison without LLM) is independently valuable.** The architect's Phase 1 approach — comparing structured data side-by-side (one-liner, revenue milestones, key events, business model) — doesn't require LLM. It's essentially two business cards side by side with a narrative frame. This is valuable even without sophisticated narrative generation.

4. **Deferring to Sprint 5 means it might never ship.** Sprint 5 is the last sprint in the approved roadmap. If any earlier sprint slips (which is likely, given the 50% buffer pattern), C38 gets cut. The most historian-aligned feature — the one that best expresses our product vision — would be the first to be sacrificed.

5. **C38 creates a natural "second visit" experience.** A beginner who visits one company, then compares it with a peer, is engaging in deeper learning. This is the "point-to-point knowledge construction" core value in action.

**My recommendation**: Move C38 to Sprint 3 (Phase 1, structured comparison only). This gives it two sprints of buffer before the roadmap ends. The 10-14h effort fits within Sprint 3's capacity if C28 is the primary feature and C38 is a secondary feature.

**Revised sprint allocation:**

| Sprint | Features | Base Hours | Notes |
|--------|------------|------------|-------|
| Sprint 2 | C37 + C39 + C41 | 18.5h | Quick wins bundle (developer's Sprint 2a) |
| Sprint 3 | C36 + C38 (Phase 1) | 18.5-22h | Revenue tree + structured comparison |
| Sprint 4 | C40 (or replacement) | 10h | Mode toggle OR beginner-by-default design pass |
| Sprint 5 | Buffer / C38 Phase 2 | 10-14h | LLM-enhanced comparison or overflow |

**Wait — this doesn't account for existing sprint commitments.** Let me redo this properly:

| Sprint | Existing | New | Total Base |
|--------|----------|-----|------------|
| Sprint 2 | D02 (7h) + C31 (11h) = 18h | C37 (6.5h) | 24.5h |
| Sprint 3 | C28 (20h) | C39 (5.5h) + C41 (6.5h) = 12h | 32h |
| Sprint 4 | C07 (12h) + C14 (5h) = 17h | C36 (10.5h) | 27.5h |
| Sprint 5 | C29 (10h) | C38 (11h) | 21h |

**This is still overloaded.** Every sprint exceeds the 15h base target. The reality is that the existing roadmap (73h across 5 sprints) plus the new features (40h) = 113h total, which is ~22.6h per sprint. This is simply too much for a single developer.

**The honest assessment**: We need to either cut scope or extend the roadmap. I'll address this in the verdict.

---

## Round 3: Goal Alignment & Risk Assessment

### 3.1 Does this set of features advance all 5 core values?

| Core Value | Features That Advance It | Assessment |
|------------|-------------------------|------------|
| **#1: Story first, data second** | C37 (synthesis), C36 (visual story), C39 (narrative delta), C38 (narrative comparison), C41 (story connections) | ✅ **Strong.** 5 of 6 features directly advance this value. |
| **#2: PPT-style presentation** | C37 (one card, 3-5 bullets), C36 (one visual, one message), C39 (max 2 deltas) | ✅ **Strong.** C37 and C36 are inherently PPT-style. |
| **#3: Adaptive and self-evolving** | C39 (delta detection), C40 (mode toggle) | ⚠️ **Weak.** Only C39 meaningfully advances this. C40 is a static toggle, not adaptive. |
| **#4: Point-to-point knowledge construction** | C41 (Read Next), C38 (Compare Stories) | ✅ **Moderate.** C41 is the strongest expression of this value. C38 supports it through comparison. |
| **#5: Benchmark-oriented analysis** | C38 (Compare Stories) | ⚠️ **Weak.** Only C38 directly supports benchmarking. The existing peer comparison page handles this, but none of the new features add benchmark-oriented analysis. |

**Key finding**: Core values #3 (Adaptive) and #5 (Benchmark) are underrepresented. This is a gap.

**For #3 (Adaptive)**: C39's delta detection is a start, but true adaptation would mean the product learns what each user cares about and adjusts the presentation. C40's toggle is manual adaptation, not self-evolution. We're missing a feature that adapts content based on user behavior or preferences.

**For #5 (Benchmark)**: The existing peer comparison page handles benchmarking, but none of the new features extend benchmark-oriented analysis. C38 (Compare Stories) is the closest, but it's narrative comparison, not benchmark comparison.

### 3.2 Are there contradictions between roles' recommendations?

**Yes, three significant contradictions:**

**Contradiction 1: C40 — Toggle vs. No Toggle**
- **Architect**: Build a toggle (10-15h, Sprint 4)
- **Designer**: Replace with "beginner mode by default" design philosophy (0h engineering cost)
- **Developer**: Implement toggle but notes "scope management" and "testing matrix" risks

These are fundamentally different approaches. The architect wants a technical solution; the designer wants a design philosophy change. The developer is caught in the middle, estimating the technical cost of the architect's approach while noting significant risks.

**Resolution needed**: This is a design system decision, not a feature decision. The team needs to decide: do we build a toggle or redesign the default experience? These are mutually exclusive at the implementation level.

**Contradiction 2: C36 vs. C41 Priority**
- **Designer**: C36 at #2, C41 tied at #3
- **Architect**: C41 at #3, C36 at #4 (lower risk, no data curation bottleneck)
- **Developer**: C41 at #3, C36 at #4 (lower cost)

The designer values C36's visual storytelling impact. The architect and developer value C41's lower risk. This isn't just a priority difference — it reflects different theories of what helps beginners most: visual understanding (designer) vs. knowledge path-building (architect/developer).

**Resolution needed**: Both are right. C36 is more impactful for visual learners; C41 is lower risk and supports knowledge construction. The decision should depend on Sprint 3 capacity, not abstract priority.

**Contradiction 3: C39 Sprint Placement**
- **PM consolidation**: C39 in Sprint 2
- **Designer**: C39 in Sprint 4
- **Developer**: C39 in Sprint 2a (bundled with C37 + C41)

The designer wants to defer C39 to Sprint 4, presumably to avoid overloading the business card page. The developer wants to bundle it with C37 + C41 for infrastructure efficiency. The PM puts it in Sprint 2.

**Resolution needed**: The developer's bundling argument is strongest from an efficiency perspective. But the designer's concern about overloading the business card page is valid — adding C37 + C39 + C41 to the same page simultaneously risks violating the ten-second test through sheer content volume.

### 3.3 What are the overlooked risks?

**Risk 1: Business Card Page Overload (HIGH)**
The PM consolidation puts C37, C39, C41, and C36 all on the business card page. That's 4 new sections/cards added to the existing page. Even if each individually passes the ten-second test, the combined page might fail because there's too much content. The designer warns about this: "One new card per page per sprint. Don't add C36 + C37 + C39 + C41 to the Business Card page simultaneously."

**This risk is not addressed in the PM consolidation.**

**Risk 2: Data Curation Bottleneck (MEDIUM)**
C36, C38, and C41 all require manual data curation. The developer estimates:
- C36: 2-3h data curation (top 8-10 stocks)
- C38: 2-3h milestone curation (top 10 stocks)
- C41: 2-3h relationship curation (top 20 stocks)

That's 6-9h of data curation work, which is non-engineering work that still requires domain expertise. If the developer is also doing the curation, this competes with engineering time. If someone else does it, there's a coordination cost.

**Risk 3: LLM Dependency Confusion (MEDIUM)**
C38 Phase 2 depends on the Sprint 1 LLM architecture decision. But the team is planning C38 for Sprint 5 without knowing if LLM will be available. The architect's Phase 1 approach (structured comparison without LLM) is the right mitigation, but the team should explicitly commit to Phase 1 for Sprint 5 and treat Phase 2 as a future enhancement.

**Risk 4: No Verification Plan (HIGH)**
The handoff mentions "verification gates: ten-second test after each sprint." But the PM consolidation doesn't include ten-second test time in any sprint estimate. Running the ten-second test requires:
- Preparing test materials (5-10 minutes per feature)
- Finding test participants (beginners)
- Running the test (10-15 minutes per participant)
- Analyzing results and iterating (1-2 hours per feature)

This is roughly 2-3h per feature for proper testing, or 12-18h across all 6 features. This time is not accounted for in any sprint.

**Risk 5: Sprint Capacity Overallocation (CRITICAL)**
As I showed in Round 2, adding 40h of new features to the existing 73h roadmap creates a 113h total, which is ~22.6h per sprint for 5 sprints. The existing sprint targets are 15-20h base. We're looking at a 15-50% overallocation across all sprints.

**This is the most critical risk because it threatens the entire roadmap.**

---

## Verdict & Recommendations

### Verdict: **REVISE**

The team's preliminary decision has the right individual feature priorities but fails at the sprint allocation level. The total scope (113h across 5 sprints) exceeds capacity, and several critical risks are unaddressed.

### Specific Revisions Required

#### Revision 1: Cut C40 (Mode Toggle) Entirely
**Replace with**: "Beginner mode by default" design principle. Every page must pass the ten-second test in its default state. Advanced detail is always one click away (progressive drill-down).

**Rationale**: Saves 10-15h of engineering cost. Avoids zone violation. Eliminates maintenance burden. Achieves the same goal through design discipline rather than a toggle.

**Impact**: Frees up Sprint 4 capacity. Reduces total new feature scope from 40h to ~30h.

#### Revision 2: Move C38 (Compare Stories) to Sprint 3
**From**: Sprint 5 (10-14h)
**To**: Sprint 3, Phase 1 only (structured comparison, 8-10h)

**Rationale**: C38 is the most historian-aligned feature. Deferring it to Sprint 5 risks it never shipping. Phase 1 (structured comparison without LLM) is independently valuable and doesn't depend on the LLM architecture decision.

**Impact**: Sprint 3 becomes heavier (C28 + C38 Phase 1 = 28-30h), but C38 Phase 1 is a natural complement to C28's story timeline.

#### Revision 3: Defer C39 to Sprint 3
**From**: Sprint 2 (5.5h)
**To**: Sprint 3 (5.5h)

**Rationale**: Sprint 2 is already overloaded with D02 + C31 + C37. C39 is a presentation-layer feature that can be added to the business card page in any sprint. Moving it to Sprint 3 reduces Sprint 2 overload and groups it with other business card page enhancements.

**Impact**: Sprint 2 becomes D02 + C31 + C37 = 24.5h base (still high but more manageable). Sprint 3 becomes C28 + C38 + C39 + C41 = 43h base (very high — see Revision 5).

#### Revision 4: Ship C36 with Top 10 Stocks Only
**From**: Top 20 stocks (4-5h data curation)
**To**: Top 10 stocks (2-3h data curation)

**Rationale**: Covers the most-seen companies. Reduces data curation bottleneck. The pie chart fallback already exists for non-curated stocks.

**Impact**: Reduces C36 from 10.5h to ~8-9h.

#### Revision 5: Extend Roadmap to Sprint 6 OR Reduce Existing Scope
**The math doesn't work with 5 sprints.** Here's the honest capacity analysis:

**Existing roadmap**: 73h base (with 50% buffer: 109h)
**New features (revised)**: ~28h base (C37 + C39 + C41 + C36 + C38 Phase 1, minus C40)
**Total**: ~101h base (with 50% buffer: ~152h)

**Per sprint (5 sprints)**: ~30h per sprint — far exceeding the 15-20h target.

**Options**:
- **Option A**: Extend to 6 sprints. ~25h per sprint (still high but more manageable with buffer).
- **Option B**: Cut existing features. Candidates: C07 (Custom Event Thresholds, 12h) or C29 (Explain Any Metric, 10h) could be deferred to a post-roadmap phase.
- **Option C**: Accept overload and plan for 2 developers (if available).

**My recommendation**: **Option B — Cut C07 from Sprint 4.** Custom Event Thresholds is a power-user feature that contradicts the "beginner by default" philosophy. It can be added post-roadmap. This saves 12h, bringing the total to ~89h base (~133h buffered), which is ~26.6h per sprint across 5 sprints — still high but closer to feasible.

### Revised Sprint Allocation

| Sprint | Features | Base Hours | With 50% Buffer | Core Value Focus |
|--------|----------|------------|-----------------|-----------------|
| **Sprint 0** | Design + Quick wins | 2.7h | 4h | #2 PPT |
| **Sprint 1** | C28 Spike + LLM | 5h | 7.5h | #1 Story |
| **Sprint 2** | D02 + C31 + C37 | 24.5h | 37h | #1 Story, #3 Adaptive |
| **Sprint 3** | C28 Full + C38 Phase 1 + C39 + C41 | 43h | 64.5h | #1 Story, #4 Knowledge |
| **Sprint 4** | C14 + C36 | 15.5h | 23h | #5 Benchmark, #1 Story |
| **Sprint 5** | C29 + Buffer | 10h | 15h | #4 Knowledge |
| **Total** | | **~101h** | **~151h** | |

**Note**: Sprint 3 is still heavily overloaded at 43h base. This could be mitigated by:
- Moving C39 to Sprint 4 (adding it to the business card page after C36)
- Moving C41 to Sprint 4 (it's a bottom-of-page section that can be added anytime)

### Final Priority Ranking (Revised)

| Rank | Feature | Sprint | Rationale |
|------|---------|--------|-----------|
| **1** | C37: Key Takeaways | Sprint 2 | Ten-second test gate. Non-negotiable. |
| **2** | C39: What Changed | Sprint 3 | Lowest cost, high value. Makes data feel alive. |
| **3** | C41: Read Next | Sprint 3 | Knowledge construction. Low cost. |
| **4** | C38: Compare Stories (Phase 1) | Sprint 3 | Most historian-aligned. Can't risk Sprint 5. |
| **5** | C36: Revenue Tree | Sprint 4 | Visual storytelling. Data curation bottleneck. |
| **—** | C40: Mode Toggle | **CUT** | Replace with "beginner by default" principle. |

### Key Risks After Revision

1. **Sprint 3 overload** (C28 + C38 + C39 + C41 = 43h base): Mitigated by C28 being the primary feature and others being smaller additions.
2. **Business card page overload** (C37 + C39 + C41 + C36 all on one page): Mitigated by the designer's "one new card per page per sprint" principle. C37 in Sprint 2, C39 + C41 in Sprint 3, C36 in Sprint 4.
3. **Data curation bottleneck** (C36 + C38 + C41): Mitigated by reducing C36 to top 10 stocks and using existing data sources for C38/C41.
4. **No ten-second test time in estimates**: Must add 2-3h per feature for verification. This is non-negotiable per the handoff agreement.

### Closing Statement

The team's preliminary decision demonstrates strong individual feature analysis but insufficient attention to system-level constraints. The total scope exceeds capacity, the sprint allocation doesn't account for existing commitments, and critical risks (business card page overload, data curation bottleneck, missing verification time) are unaddressed.

My revisions cut scope (C40), reduce data curation burden (C36 top 10 only), and reposition the most historian-aligned feature (C38) earlier in the roadmap. The result is a more realistic plan that still delivers on the product vision.

The "historian, not stock picker" positioning is best served by **C37 (Key Takeaways)** and **C38 (Compare Stories)** — one synthesizes a single company's story, the other connects two companies' stories. These two features should be the non-negotiable core of the roadmap. Everything else is secondary.

---

*Challenger Discussion completed. Verdict: REVISE. Recommendations provided above.*
