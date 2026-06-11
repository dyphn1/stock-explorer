# Stock Explorer — Challenger Discussion Round 10

> **Date**: 2026-06-16
> **Role**: Challenger
> **Purpose**: Challenge the team's preliminary decision (Direction A: C42 + C44) across 3 rounds
> **Context**: Sprint 2 complete (C37, C39, C45, C43 ✅). Sprint 3 next with C41 + C38 + C44 + R5 planned.

---

## Challenger Round 10 — 3-Round Challenge

### Round 1: Feature Direction

**Challenges:**

1. **Does C42 (Stock Screener) truly align with "historian, not stock picker" positioning?**
   The product vision explicitly states: "Do not say buy or sell; only explain what has happened to the company over time." A stock screener, even framed as "discovery," inherently implies selection — users filter stocks to find ones worth buying. The designer acknowledges this tension by prescribing framing language ("發現有趣的公司" not "篩選好股票"), but I challenge whether framing alone resolves the fundamental contradiction. 財報狗's screener exists because 財報狗 IS a stock-picking tool. We are not. Does building the #1 feature of a product we're NOT trying to become really serve our vision?

2. **Is C42 actually P1, or is it P1 for a competitor's product strategy?**
   The architect labels C42 as P1 because "財報狗's #1 feature is its stock screener." But our product is not 財報狗. Our P1 should be defined by our own vision gaps, not competitor feature parity. The product vision's M2 milestone asks: "Can answer 'What has this company been up to recently?'" — that's about depth of company understanding, not breadth of discovery. Is the P1 label driven by genuine user need or competitive FOMO?

3. **Are there better directions the team hasn't considered?**
   The three directions presented are all C42/C44/C46/C47 combinations. But C34 (Company Story Timeline) was identified in Round 7 as "the #1 thing competitors DON'T have" — a unique differentiator. C38 (Compare Stories) is in Sprint 3, which creates the data structures needed for C34. Why isn't "C38 → C34" (Story Timeline) being considered as a direction? C34 directly serves the historian positioning — it narrates what happened over time. It's the purest expression of the product vision. The team seems to have fixated on the Round 9 feature gap list (C42-C47) and forgotten that C34 exists as an option.

4. **How do competitors actually do screening, and why are we copying them?**
   The designer notes that 財報狗 has 100+ screening metrics, Stockopedia has StockRank-integrated results, and Simply Wall St has visual-first results. All of these are screening tools for investors making allocation decisions. Our "historian" positioning means we should help users understand companies they already have a connection to (buy their products, see their ads, work in their industry). A screener serves users who don't yet have a company in mind — that's a different user journey. The designer's own ten-second test for C42 says: "This tool helps me find interesting companies to learn about." But is that what beginners actually need, or is it what we think they need because competitors have it?

**Team Response (based on analysis files):**

- **Architect**: C42 is the P1 gap because "Stock Explorer requires users to know which stock to look up, which is a fundamental barrier for beginners." Without discovery, the product remains a reference tool, not an exploration tool. The in-memory filtering approach using existing FinMind data makes it technically feasible. C42 transforms the product from lookup to discovery, which is the single most important strategic gap.

- **Designer**: C42 is a new page (separate from business card), so it doesn't create page overload. The "discovery for learning" framing with preset cards ("穩定收息", "成長潛力", "便宜估值") and plain-language explanations differentiates it from 財報狗's screening-for-investing approach. The ten-second test for C42 is: "This tool helps me find interesting companies to learn about" — which aligns with "help users move from 'I don't understand' to 'I know what this company does.'"

- **Developer**: C42 (19-24h) is feasible for Sprint 4. It reuses existing `get_stock_info()` data and follows the `category_browser.py` pattern. The key risk is FinMind API rate limits at scale (1,800+ stocks), but the batch ThreadPoolExecutor pattern mitigates this.

- **On C34**: The pending_review.md notes C34 is scheduled for Sprint 5+ after C38 completes. It was not included in the Round 10 direction options because the focus was on Round 9's C42-C47 feature gaps. C34 remains on the roadmap but wasn't part of this round's scope.

**Resolution: PARTIALLY RESOLVED — requires revision**

The team makes a reasonable case that C42 serves a real user need (beginners don't know which stocks to look up) and that the "discovery for learning" framing differentiates it from competitor screeners. However, I'm not fully convinced that C42 should be P1 over C34 (Company Story Timeline). C34 is the "historian" feature par excellence — it narrates what happened over time, which IS the product vision. C42 is a discovery mechanism; C34 is the core value proposition.

That said, C34 depends on C38 (in Sprint 3), so it can't be built yet. C42 doesn't have the same dependency. This makes C42 the right Sprint 4 priority by process of elimination, but the team should explicitly acknowledge that C34 — not C42 — is the true P1 vision feature, and C42 is an enabler, not the destination.

**Revision required**: The team should explicitly state that C42 is a P1 *enabler* feature (gets users to companies) while C34 remains the P1 *vision* feature (delivers the historian narrative). The sprint plan should include C34 in Sprint 5 alongside or instead of C46.

---

### Round 2: Priority

**Challenges:**

1. **Is Sprint 3's plan (C41 + C38 + C44 + R5) realistic given the developer's estimates?**
   The developer estimates C44 at 17-24h, but the Sprint 3 plan allocates only 10-14h. The developer explicitly states: "BARELY for Sprint 3" and recommends reducing C44 to MVP scope (3 risk dimensions, top 20 stocks only) to fit. Meanwhile, C41 (6.5h) + C38 (8-10h) + C44-MVP (12-14h) + R5 (4-6h) = 30.5-36.5h. This fits within ~40h capacity, but with almost no buffer. If any single estimate slips, Sprint 3 is over. Is the team comfortable with a sprint that has <10h buffer?

2. **Is the priority of C42 over C46 correct?**
   The team's plan defers C46 to Sprint 5 because Sprint 4 can't fit both C42 and C46. But let's examine this: C42 is 19-24h of primarily technical work (new page, filtering engine, API integration), while C46 is 20-28h of which 3-4h is manual research/writing. C46 is the more unique feature (no TW competitor has moat analysis) and aligns more directly with "historian" positioning (explain competitive advantages historically). C42, while strategically important, is technically riskier (FinMind rate limits, 1,800-stock performance). If we're choosing based on vision alignment and competitive differentiation, C46 > C42. The team chose C42 based on "P1 gap" labeling, but I challenge that labeling (see Round 1).

3. **Is Sprint 4 the right time to build C42?**
   C42 depends on R3 (batch API calls) being verified. The developer says: "Must verify R3 status before starting C42." If R3 wasn't done in Sprint 2, C42 will be "unusably slow." The team has no confirmation that R3 is complete. Building C42 in Sprint 4 without verifying R3 first is building on an unverified foundation. Shouldn't R3 verification (or R3 itself at 3-5h) be a Sprint 3 prerequisite?

4. **Sprint 4 capacity: the developer says it's over capacity. Does the team agree?**
   The developer's analysis shows Sprint 4 (C36 + C42 + C46) at 47-62h vs ~40h capacity — "significantly over capacity." The architect's plan shows Sprint 4 with only C36 + C42 = ~27-34h, which fits. But this means C46 is deferred to Sprint 5, and the developer's Sprint 5 plan (C47 Phase 1 + C46 = 42h) is also tight. The team is essentially playing Tetris with features and hoping nothing slips. What's the contingency if Sprint 3's C44-MVP slips by even 3-4h?

**Team Response (based on analysis files):**

- **Architect**: Sprint 3 (C42 in architect's plan, but the handoff says C44 is in Sprint 3) — there's a discrepancy here. The architect's sprint plan shows C42 in Sprint 3 and C44 in Sprint 4, but the developer's context says "C44 is already in Sprint 3" per the handoff. The architect recommends C42 in Sprint 3 (16-24h) and C44 in Sprint 4 (10-14h), which is the reverse of what the developer is planning.

- **Developer**: Sprint 3 is "tight but feasible" IF C44 is scoped to MVP. Sprint 4 is confirmed over capacity with C46 included. Recommendation: defer C46 to Sprint 5. R1 (financial_metrics extraction, 2.5-4h) should be done before C44 as it's a P0 blocker.

- **Designer**: C42 should be Sprint 4 priority, not C46. "If Sprint 4 has capacity issues, cut C46 before C42." This aligns with the developer's recommendation.

**Resolution: REQUIRES REVISION**

There's a critical contradiction between the architect's sprint plan and the developer's understanding:
- **Architect**: Sprint 3 = C42, Sprint 4 = C44
- **Developer**: Sprint 3 = C44, Sprint 4 = C42

The handoff says Sprint 3 = C41 + C38 + C44 + R5, which matches the developer's understanding. The architect's plan appears to be outdated or based on a different handoff. This contradiction must be resolved before Sprint 3 begins.

Additionally, the team needs to:
1. Confirm R3 status before Sprint 4 (C42 dependency)
2. Do R1 before or alongside C44 in Sprint 3 (P0 blocker)
3. Accept that Sprint 3 has minimal buffer (<10h) and define what gets cut if estimates slip

**Revision required**: Resolve the Sprint 3/4 contradiction between architect and developer plans. The handoff (C44 in Sprint 3, C42 in Sprint 4) should be the canonical plan. Add R1 as a Sprint 3 prerequisite. Define Sprint 3 contingency: if C44-MVP exceeds 14h, cut to 2 risk dimensions instead of 3.

---

### Round 3: Goal Alignment

**Challenges:**

1. **Does Direction A help achieve the M2 milestone?**
   The product vision's M2 milestone is: "Four deep-dive sections — Can answer 'What has this company been up to recently?'" Direction A (C42 + C44) adds a screener (discovery) and risk analysis (one aspect of "what could go wrong"). But M2 is about depth of company understanding, not breadth of discovery. C44 partially serves M2 (risk is part of "Financial Condition" deep-dive), but C42 doesn't serve M2 at all — it serves M3 ("Users can independently explore across dimensions"). The team is building M3 features before M2 is complete. Is the M2 milestone actually done? The business card page has 13 sections, but are the four deep-dive sections from the product vision (Operations Health, Financial Condition, Peer Comparison, Conglomerate Structure) all implemented?

2. **Are there contradictions between the roles' opinions?**
   Yes — I've identified several:
   - **Sprint planning contradiction**: Architect says C42 in Sprint 3; developer says C44 in Sprint 3 (handoff confirms developer is correct).
   - **C44 scope contradiction**: Architect estimates C44 at 10-14h; developer estimates 17-24h. The 10-14h figure assumes MVP scope that the architect doesn't explicitly acknowledge.
   - **C46 priority contradiction**: The architect's original plan includes C46 in Sprint 4; the developer says Sprint 4 can't fit C46; the designer agrees C46 should be cut before C42. The team's "Direction A" defers C46, but the architect's sprint plan doesn't clearly show this.
   - **R1 urgency contradiction**: Developer says R1 is a "P0 blocker" for C44; architect says C44 "benefits from R1 but doesn't strictly depend on it." These are fundamentally different risk assessments.

3. **Are there overlooked risks?**
   - **R1 not being done**: If R1 (financial_metrics extraction) is not completed before C44, the developer warns C44 will add a "5th copy of the same gross_margin/debt_ratio/ROE logic." This is architecture debt compounding. The team treats R1 as optional ("benefits from but doesn't depend on"). This is a significant risk.
   - **C42 FinMind rate limits**: The developer rates this as HIGH risk. Screening 1,800+ stocks with multiple metrics could hit FinMind's rate limits, making the screener unusable. The architect's in-memory filtering approach helps but doesn't eliminate the risk if `get_stock_info()` itself requires API calls per stock.
   - **Business card page overload**: The designer clearly states the business card page has 13 sections and adding C44 as a 14th requires progressive disclosure. But the architect's plan doesn't mention progressive disclosure for C44 — it just says "add a section to business card page." If C44 is built without the collapsible/expander pattern, the page becomes a scrolling wall that violates the ten-second test.
   - **C44 tone risk**: The developer notes that risk analysis must feel educational, not like a "sell signal," and rates this as MEDIUM risk. But for a "historian" product, getting the tone wrong on risk analysis could fundamentally undermine the product positioning. This should be HIGH risk, not MEDIUM.
   - **No user validation**: The team is making significant architectural decisions (C42 as P1, C44 scope, sprint priorities) without any user testing or validation. The ten-second test is a design principle, not a tested hypothesis. When was the last time a real beginner interacted with Stock Explorer?

**Team Response (based on analysis files):**

- **Architect**: R1 and R3 are beneficial but not strict dependencies. C42 can use in-memory filtering; C44 uses data already loaded by the router. The architect's sprint plan is more aggressive (C42 in Sprint 3) than the developer's, reflecting different risk tolerance.

- **Developer**: R1 is P0. R3 must be verified. C44 without R1 adds technical debt. Sprint 4 is over capacity with C46. C42 FinMind rate limits are a real concern that needs investigation before Sprint 4.

- **Designer**: Business card page needs progressive disclosure for C44 (collapsible/expander). The "above the fold" definition (C37 + C43 = ten-second test) must be formally approved before Sprint 4. New card types (warning card for C44) need to be added to the design system.

**Resolution: REQUIRES REVISION**

The contradictions between roles must be resolved:
1. **Sprint plan**: Confirm C44 in Sprint 3, C42 in Sprint 4 (per handoff and developer)
2. **R1**: Upgrade from "beneficial" to "mandatory before C44" — the developer's P0 assessment is correct
3. **C44 design**: Must use progressive disclosure (collapsible/expander), not a full card section
4. **C42**: Must verify R3 status before Sprint 4 begins
5. **Tone**: C44 tone risk should be elevated to HIGH — consider a tone review checkpoint before C44 ships

---

## Final Assessment

### Strengths of Direction A
- C42 addresses a real user need (discovery for beginners who don't know which stocks to look up)
- C44 is a genuine differentiator (no TW competitor has plain-language risk analysis with historical evidence)
- The "discover → understand" flow (C42 → business card → C44) is a natural user journey
- Both features use existing FinMind data (no new data sources needed)
- The combined effort (36-48h across Sprints 3-4) is manageable

### Weaknesses of Direction A
- C42's P1 labeling is driven by competitor parity (財報狗 has it) rather than vision alignment
- C34 (Company Story Timeline) — the true "historian" feature — is being deferred in favor of C42
- Sprint planning has architect/developer contradictions that must be resolved
- R1 (financial_metrics extraction) is underweighted as a dependency
- Business card page overload risk for C44 is not adequately addressed in the architect's plan
- No user validation data supporting any of these priorities

### Key Risks
1. **R1 not done before C44** → 5th copy of financial logic, compounding architecture debt
2. **C42 FinMind rate limits** → Screener unusable at scale
3. **C44 tone miscalibration** → Risk analysis feels like "sell signal" instead of education
4. **Sprint 3 overrun** → Minimal buffer (<10h) with C44-MVP at the edge of capacity
5. **Business card page bloat** → 14 sections without progressive disclosure violates ten-second test

---

## Final Verdict

### ❌ REVISED

Direction A (C42 + C44) is the **right general direction** but requires the following revisions before confirmation:

#### Required Revisions

1. **Resolve sprint plan contradiction**: Confirm the canonical sprint plan is:
   - Sprint 3: C41 + C38 + C44 (MVP: 3 risk dimensions, top 20 stocks) + R5 + R1
   - Sprint 4: C36 + C42 (verify R3 status first)
   - Sprint 5: C34 (Company Story Timeline) + C46 OR C47 Phase 1 (not both)

2. **Upgrade R1 to P0**: R1 (financial_metrics extraction, 2.5-4h) must be completed **before or alongside C44** in Sprint 3. Without it, C44 adds a 5th copy of duplicated financial logic. The architect's "benefits from but doesn't depend on" assessment is too optimistic.

3. **Add C34 to the roadmap explicitly**: C34 (Company Story Timeline) should be scheduled for Sprint 5 as the primary feature, with C46 or C47 Phase 1 as secondary. C34 is the purest expression of "historian" positioning and was identified as the #1 unique differentiator in Round 7. It should not be perpetually deferred.

4. **Mandate progressive disclosure for C44**: C44 must use `st.expander()` or equivalent collapsible pattern on the business card page. The architect's plan to "add a section to business card.py" without progressive disclosure will push the page to 14 sections and violate the ten-second test.

5. **Verify R3 before Sprint 4**: Before starting C42, verify that R3 (batch API calls) is complete. If not, do R3 (3-5h) as the first Sprint 4 task. C42 without R3 will be "unusably slow" per the developer.

6. **Define Sprint 3 contingency**: If C44-MVP exceeds 14h, reduce to 2 risk dimensions (financial health + revenue concentration) instead of 3. C41 is the next candidate for reduction if further cuts are needed.

7. **Elevate C44 tone risk to HIGH**: Add a tone review checkpoint before C44 ships. Risk analysis must use "過去發生" / "歷史證據" / "觀察指標" language — never "可能發生" / "預測" / "建議". Consider having a non-technical reviewer validate the tone.

#### What's Confirmed
- ✅ C42 (Stock Screener) is the right Sprint 4 feature (after C38 creates prerequisite data structures)
- ✅ C44 (Risk Analysis) is the right Sprint 3 P2 feature (unique differentiator, manageable scope)
- ✅ C46 should be deferred to Sprint 5 (Sprint 4 is over capacity)
- ✅ C47 should be phased (Phase 1 in Sprint 5, Phase 2 post-plan)
- ✅ Direction A is preferable to Direction B (defers P1 gap) and Direction C (too ambitious)

#### What Needs Daniel's Input
- C34 vs C46 priority for Sprint 5 (pending_review.md item 3)
- C47 Phase 1 scope: 5 lessons (12h) or 10 lessons (20h)? (pending_review.md item 1)
- Business card page "above the fold" definition approval (pending_review.md item 4)

---

*Summary: Direction A is sound in principle but has execution risks that need mitigation. The sprint plan contradiction between architect and developer must be resolved, R1 must be treated as mandatory, C44 must use progressive disclosure, and C34 should be explicitly scheduled for Sprint 5. With these revisions, Direction A can be confirmed.*

---

*Created: 2026-06-16*
*Role: Challenger*
*Review cycle: Round 10*
*Confidence level: High (based on cross-referencing all three role documents, pending_review.md, and product_vision.md)*
