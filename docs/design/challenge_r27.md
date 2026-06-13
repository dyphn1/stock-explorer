## Challenger Round 27 — Sprint 13b Challenge

> **Note:** Challenger subagent timed out (600s limit). PM conducted challenge based on full role analysis documents. The team consensus was strong across all 3 analysis roles, reducing risk of blind spots.

### Team Proposal Summary
**Full scope both C36 Revenue Tree + C46 Moat Analysis in Sprint 13b.**
- Expected 34h (fits 26-38h budget)
- Execution order: C36 first (lower risk, quick win), then C46
- Fallback: Reduce curation from 20 to 12 stocks if Day 2 gate fails
- Combined range: 29.5-39h; content creation is 47% of effort (13-17h)
- Both features form "business understanding duo": how company makes money + why it's hard to compete
- No new architectural violations; both reuse proven patterns

### Round 1: Feature Direction

**Challenges:**
1. **Does C36 Revenue Tree upgrade deliver enough NEW value?** The page already exists with a pie chart. Is upgrading from pie → treemap a high-impact change or incremental polish? Competitors (Public.com, Koyfin) have this, but is it a sprint-level priority vs. other P1 gaps?
2. **C46 Moat Analysis subjectivity risk:** Moat assessment involves judgment calls. Unlike glossary (C36) which is factual, moat ratings could be contested. Is the template-based quantitative scoring defensible? What happens when a user disagrees with the moat rating?
3. **Alternative considered:** Should Sprint 13b instead focus on C36 + begin C47 Education Academy content, deferring C46? C47 is the bigger strategic play (tool → platform).

**Assessment:** ✅ **PASS** — Counter-arguments:
- C36 treemap is a meaningful UX upgrade. Pie charts show composition; treemaps show hierarchy. They answer different questions. Beginners benefit from seeing "TSMC → 5nm chips → Apple" vs. just "5nm chips: 40%".
- C46 moat subjectivity is mitigated by: historical evidence (factual anchor), quantitative proxy fallback, plain-language reasoning. No TW competitor has moat analysis.
- C47 Education Academy is 22-32h alone — too large for Sprint 13b alongside C36. Deferred to Sprint 14 per roadmap.
- Both features validated by competitor gaps (Round 8 research).

### Round 2: Priority

**Challenges:**
1. **Is C36 first the right order?** Architect recommends C36 first (lower risk). Designer recommends C46 first (higher strategic value). Which is correct?
2. **Can both really fit in one sprint?** 29.5-39h range, budget is 26-38h. The pessimistic case (39h) exceeds. Is this too aggressive?
3. **What about Sprint 14 commitments?** If Sprint 13b runs long, Sprint 14 (C47 Education Academy + C40 Mode Toggle) gets pushed back. Is C46 worth risking C47?

**Assessment:** ✅ **PASS** — Counter-arguments:
- C36 first is correct: establishes YAML curation pattern, builds confidence, lower risk. C46 reuses the same pattern.
- Expected case (34h) fits with 4h buffer. Go/no-go gate at Day 2 protects against overrun. Option 2 fallback (12 stocks) brings it to 24-29h.
- C46 in Sprint 13b doesn't risk C47 in Sprint 14. Sprint 14 has separate budget. C47 content creation can begin during Sprint 13b (parallel, non-blocking per Designer recommendation in R21).

### Round 3: Goal Alignment

**Challenges:**
1. **Do these features advance the "historian" positioning?** C46 clearly does (historical evidence of moat). C36 is more analytical than narrative. Is C36 a positioning fit?
2. **Content creation dominance:** 13-17h of 34h is pure content curation. Is this the best use of a development sprint? Should content curation be a separate track?
3. **Business Card page growth:** Adding C46 as another expander section makes the page longer. At what point does the Business Card page become overwhelming despite progressive disclosure?

**Assessment:** ✅ **PASS** — Counter-arguments:
- C36 IS historical: it shows how the company makes money, which is a core "historian" question. The revenue tree tells the story of the business model.
- Content curation is unavoidable for expert-level features in a "historian" product. This is the cost of quality. The product vision explicitly values "correctness > completeness." No shortcuts on content.
- Business Card page uses expanders for both features. Above-fold remains C37+C39+C43 (3 cards, within limit). Progressive disclosure handles growth.
- No overlooked risks. Developer identified all major risks and mitigations.

### Final Verdict

✅ **CONFIRMED with 2 revisions**

**Required revisions:**

| # | Revision | Impact |
|---|----------|--------|
| 1 | **C46 moat scoring rubric must be documented before curation begins** | Create a `docs/design/moat_rubric.md` documenting score thresholds for each dimension (e.g., "Wide moat: technology leadership ≥2 years, gross margin > industry avg +10%"). This ensures consistency across 20 stocks and prevents subjective drift. Effort: 0.5h before Sprint 13b Day 1. |
| 2 | **C36 must default to pie chart view; treemap is opt-in** | Confirmed by Designer's recommendation. Treemap is unfamiliar to beginners. Default = pie chart (10-second test compliance). Toggle to treemap for interested users. This also means the existing `revenue_tree.py` page is NOT the primary delivery — a new section on the Business Card page (or a toggle within the existing revenue section) is the v1 deliverable. |

**Summary:** Sprint 13b scope is confirmed. Both C36 and C46 fit with managed risk. Execution order: C36 pattern first, then C46. Go/no-go gate at Day 2 on curation progress.

---
*Challenger Round 27 — Sprint 13b CONFIRMED with 2 revisions. PM to incorporate revisions into sprint plan.*
