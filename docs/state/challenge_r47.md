# Challenge Log — Discussion Round 47

## Date: 2026-06-15
## Topic: Sprint 23 Feature Planning — C202, C199, C200

---

## Preliminary Team Decision (Pre-Challenge)

### Proposed Sprint 23 Sprint Plan

| Priority | Feature | Effort | Risk |
|----------|---------|--------|------|
| 1 | C202 Story Arc Timeline Labels | 9-14h | Low |
| 2 | C199 Bear vs Bull Debate Cards | 10-16h | Medium |
| 3 | C200 What If Calculator | 12-17h | Medium-High |
| **Total** | | **31-47h** | |

### Proposed Sprint 24
- C201 follow-ups (daily caching pipeline)
- C206 Recurring Investment Education (pending regulatory review)
- C203 Supply Chain Visual Map

### Key Conditions
1. C199: Four-safeguard advisor boundary pattern required before development
2. C200: FinMind API caching strategy must be validated in Week 1
3. Implementation order: C202 → C199 (parallel) → C200

---

## Round 1: Feature Direction Challenge

### Challenger Questions

**Q1: Does building all three features (C202 + C199 + C200) in a single sprint align with our "refuse to implement all features at once" development philosophy?**

The preliminary plan proposes building 3 features totaling 31-47h in one sprint. The product vision explicitly states: "Refuse to implement all features at once." Is this sprint overcommitting? Should we be more selective?

**Q2: C202's rule-based arc detection feels shallow. Are we building a feature that will make us look foolish when the "arcs" are obviously mechanical?**

The Architect admits the rule-based approach is "limited but useful" and detects arcs via simple heuristics like "3+ high severity events in 30 days → Crisis Phase." For a platform positioned as a "historian," how is this different from a basic event counter? Is the arc label adding real insight or just repackaging?

**Q3: C199's advisor boundary risk is critical. Have we quantified the actual risk? What happens when a news outlet screenshots our "Bull Case" cards without the disclaimer?**

The Designer identifies this as a P1 issue with four safeguards. But are four template-level safeguards enough? If the visual cards are screenshot-friendly but the disclaimer is at the bottom, the damage is done. Shouldn't we consider NOT building debate cards at all until we have a more robust framing mechanism?

**Q4: C200 is essentially C74 with interactivity. Why is this ranked COULD instead of MUST if the C74 foundation already exists?**

The Architect says C200 has "highest feasibility" and "best ROI per hour" due to existing C74 code. If it's the easiest and highest-value feature, why isn't it the lead feature for Sprint 23? The current sequencing puts C200 last.

### Team Responses

**A1: Sprint scope is not "all features at once" — it's a focused 3-feature set from a filtered backlog.**
The product vision's "refuse to implement all features at once" refers to not building everything from the 150+ feature backlog simultaneously. Sprint 23's 3 features were filtered from 8 candidates (C199-C206) through competitor research, feasibility analysis, and design review. This is disciplined prioritization, not scope creep. However, the Challenger raises a valid point — if capacity is constrained, a reduced scope of C202 + C199 service layer only (20h) is the recommended fallback.

**A2: C202's value is in the presentation layer, not the detection algorithm.**
The "historian" positioning isn't about having perfect narrative detection — it's about making company history accessible and structured. Even simple arc labels ("成長期 2020-2023") provide a scaffolding that helps beginners understand a company's trajectory. The key is: (a) confidence indicators show this is algorithmic, not expert-labeled, (b) minimum data thresholds prevent meaningless arcs for sparse data, (c) the arc descriptions reference actual events. It's not a basic event counter — it's a chapter-heading system for company history.

**A3: C199 advisor risk is real but manageable with the right safeguards.**
The four-safeguard pattern (prominent disclaimer, "自動產生" label, data-driven points only, banned word list) is the minimum. Additional measures: (a) disclaimer rendered WITHIN the debate card area, not below the fold, (b) asymmetric evidence display prevents false balance, (c) content review gate required before release. The risk of NOT building C199 is that we miss the strongest visual differentiator. The risk of building it is reputational if framing fails. Net assessment: proceed with safeguards, assign a "tone QA gate" as a sprint exit criterion.

**A4: C200 sequencing is about risk management, not value ranking.**
While C200 has the highest feasibility score, it also has the most external dependencies (FinMind API for arbitrary dates, caching strategy, edge cases around splits/dividends). The implementation sequencing (C202 first → C199 parallel → C200 last) follows the "de-risk the sprint" principle: quick win first, then parallel medium-risk, then highest-technical-risk last. Value ranking != implementation ordering. C200's value is acknowledged as high, but it benefits from the patterns established by C202 and C199.

### Round 1 Verdict
⚠️ **Issues raised** — Challenger requests revisions on scope justification, C202 quality bar, C199 safeguards, and C200 sequencing. Team responds with clarifications. Proceed to Round 2.

---

## Round 2: Priority Challenge

### Challenger Questions

**Q1: From a competitive positioning perspective, is C202 (Story Arc Labels) really a MUST priority over C199 (Bear vs Bull)?**

No TW competitor has either feature. But C199 (visual debate cards) has direct competitor validation from Simply Wall St, and it's more visually distinctive. C202's auto-detected arcs are novel but unproven. If we can only build one feature in Sprint 23, which creates more competitive differentiation?

**Q2: The Designer recommends C200 be deferred to Sprint 24 due to FOMO framing risk. The Developer puts it last in sequencing. The Architect ranks it #1 feasibility. Which is it?**

There's a clear contradiction: the Architect says C200 is the easiest but the Designer says it should be deferred. How does the PM resolve this? If two roles disagree on whether a feature should be in Sprint 23 at all, what's the decision framework?

**Q3: The total effort range (31-47h) is very wide. What's the actual sprint capacity, and does this plan fit?**

The sprint capacity hasn't been stated. If the team has 40h capacity, the realistic estimate (39h) barely fits with zero buffer. If any feature runs over, the sprint fails. Is this acceptable risk?

**Q4: Shouldn't we be discussing C207-C214 from the Round 10 competitor research before committing to Sprint 23?**

The Round 10 competitor research identified new gaps like C209 Analyst/Source Transparency Layer (P1) and C210 Video Explanation Library (P1). Are we prematurely committing to Sprint 23 without considering potentially higher-value features from the latest research?

### Team Responses

**A1: C202 as MUST is about vision alignment, not competitive differentiation.**
Both features are competitively differentiated, but C202 directly serves the core "historian" positioning — it transforms the timeline from a flat event list into a structured narrative. C199 serves "critical thinking" education but is closer to the advisor boundary. If Sprint 23 can only fit one feature, the answer is C202 — it's lower risk, lower controversy, and directly aligned with the #1 core value ("Story first, data second"). C199 is SHOULD because it's higher impact but higher risk.

**A2: C200 is IN Sprint 23 but sequenced last with a go/no-go gate.**
Resolving the contradiction: the Architect is right that C200's code feasibility is highest (existing C74 foundation). The Designer is right that the UX/framing risk is non-trivial (FOMO). The resolution is: C200 goes into Sprint 23 with a Week 1 go/no-go gate. If the FinMind API caching strategy works and the historian framing passes tone QA, proceed. If not, defer to Sprint 24. This is consistent with the "phased delivery" principle from the product vision.

**A3: Sprint capacity is estimated at 40h based on historical velocity.**
Sprints 16-21 have consistently delivered 20-40h of work. The Sprint 23 plan of 39h (realistic) fits within the upper bound of historical capacity. The 31h optimistic / 47h pessimistic range is normal variance. The fallback plan (C202 + C199 service layer only = ~20h) is the capacity-constrained path. The Challenger's concern is noted: if Sprint 22 (C201) runs long, Sprint 23 capacity may be reduced. Mitigation: C202 alone (9-14h) is a complete, shippable feature even in a reduced-capacity sprint.

**A4: C207-C214 will be evaluated in the next Discussion cycle (Round 48).**
C209 (Source Transparency) and C210 (Video Library) from Round 10 are acknowledged as high-potential but need full Architect/Dev/Designer analysis before they can be prioritized against C199-C206. The current Discussion cycle is specifically scoped to evaluate the 8 features from Round 46 competitor research (C199-C206). Mixing in C207-C214 without proper analysis would violate the "discussion before commitment" principle. They'll be the focus of Discussion Round 48.

### Round 2 Verdict
⚠️ **Tensions remain** — Challenger requests tighter conditions on C200, acknowledges C202 C199 prioritization logic, and accepts C207-C214 deferral to Round 48. Proceed to Round 3.

---

## Round 3: Goal Alignment Challenge

### Challenger Questions

**Q1: Does this triple-feature plan genuinely help beginners understand stocks better, or are we building features that make the platform more complex?**

The product vision's verification principle: "After each feature implementation, verify: does it genuinely help beginners understand better?" C202 adds arc labels to the timeline (helps structure understanding). C199 adds debate cards (teaches critical thinking). C200 adds a calculator (teaches time-in-market). All three serve the educational mission. But they also add UI complexity — new tabs, new sections, new interactive elements. Is there a risk of overwhelming beginners with features they didn't ask for?

**Q2: Are there contradictions between the roles' opinions that haven't been resolved?**

- Architect ranks C200 #1 feasibility but Designer wants it deferred
- Developer says C202 is lowest risk but Architect says C202 has "medium-high" feasibility (not "high")
- Designer says C199 has "highest UX impact" but Architect says C199 has "medium" competitive value

Are these contradictions or just different perspectives? Has the PM truly reconciled them?

**Q3: What are the specific go/no-go criteria for each feature?**

The plan mentions "content review gate" for C199 and "Week 1 go/no-go gate" for C200, but the specific criteria aren't defined. What exactly needs to be true for each feature to proceed? What's the kill switch?

### Team Responses

**A1: All three features serve the educational mission, but progressive disclosure prevents overwhelm.**
The key is HOW these features are presented:
- C202: Arc labels appear on the existing timeline page — no new navigation, no new tab. It enhances existing content without adding complexity.
- C199: New "觀點" tab on company pages — adds one tab, but it's opt-in (users must click to see it). Default view remains the business card.
- C200: New "試算" tab — also opt-in. The existing curated scenarios remain the default view; the calculator is an enhancement.

None of these features change the default user experience. They add depth for users who want it, following the "progressive drill-down" principle. The ten-second test is preserved: the business card page still gives you the company essence in 10 seconds.

**A2: The apparent contradictions are actually complementary perspectives resolving into a coherent plan.**
- C200: Architect (code feasibility HIGH) + Designer (UX risk MEDIUM) + Dev (technical risk MEDIUM-HIGH) = Proceed with go/no-go gate. Not a contradiction — different dimensions of the same risk profile.
- C202: Architect (medium-high feasibility) + Dev (low risk) = The Architect is being conservative about detection quality while the Dev is confident about implementation. Both agree it's the safest feature. The "medium-high" vs "low risk" difference is about outcome quality vs implementation difficulty — different axes.
- C199: Designer (highest UX impact) + Architect (medium competitive value) = The Designer is right that it's visually distinctive; the Architect is right that competitor validation is moderate (Simply Wall St has it but no TW competitor does). Both agree it's SHOULD priority with safeguards.

The PM has reconciled these into: C202 MUST (safest, highest vision alignment) → C199 SHOULD (highest impact, manageable risk) → C200 COULD (highest feasibility but highest technical/framing risk, go/no-go gate).

**A3: Go/no-go criteria defined:**

**C202 Go/No-Go Criteria:**
- ✅ GO if: Arc detection produces sensible labels for ≥3 test stocks (TSMC, 鴻海, 緯穎) with ≥8 quarters of data
- ❌ NO-GO if: Arc labels feel random or meaningless for well-known stocks → defer to Sprint 24 for algorithm refinement

**C199 Go/No-Go Criteria:**
- ✅ GO if: (a) Four-safeguard pattern is implemented, (b) Content review gate passes (arguments are factual, balanced, historian-toned), (c) Banned word list is enforced
- ❌ NO-GO if: Content review fails after 2 revision cycles → defer to Sprint 24

**C200 Go/No-Go Criteria (Week 1 gate):**
- ✅ GO if: (a) FinMind API caching works for arbitrary dates without rate limiting, (b) Historian framing passes tone QA (no FOMO language), (c) Edge cases (pre-IPO, non-trading days, delisted) are handled gracefully
- ❌ NO-GO if: FinMind API rate limits are hit during testing, or framing cannot be resolved → defer to Sprint 24

### Round 3 Verdict
✅ **ALIGNED** — All three rounds of challenges have been addressed. The team has a coherent, well-reasoned plan with clear go/no-go criteria. The Challenger confirms alignment with the following conditions:

---

## Final Challenger Verdict: ✅ ALIGNED

### Conditions (3)
1. **C199 Tone QA Gate**: Content review must pass before C199 ships. No exceptions. If arguments feel generic or advisor-adjacent after 2 revision cycles, defer to Sprint 24.
2. **C200 Week 1 Go/No-Go**: FinMind API caching must be validated in Week 1. If rate limits or framing issues cannot be resolved, defer C200 to Sprint 24 without impacting C202/C199.
3. **C207-C214 Evaluation**: Round 48 Discussion must evaluate C209 (Source Transparency) and C210 (Video Library) from Round 10 research before Sprint 24 planning.

### Sprint 23 Final Plan (Post-Challenge)

| Priority | Feature | Effort | Go/No-Go Gate |
|----------|---------|--------|----------------|
| MUST | C202 Story Arc Timeline Labels | 9-14h | Quality check on 3 test stocks |
| SHOULD | C199 Bear vs Bull Debate Cards | 10-16h | Tone QA gate (2 revision max) |
| COULD | C200 What If Calculator | 12-17h | Week 1 API + framing gate |
| **Total** | | **31-47h** | |

### Sprint 24 (Provisional)
- C200 (if deferred from Sprint 23)
- C201 follow-ups (daily caching pipeline)
- C206 Recurring Investment Education (pending regulatory review)
- C203 Supply Chain Visual Map
- C209 Source Transparency Layer (pending Round 48 evaluation)

---

*Challenger confirmation: 2026-06-15 — All concerns addressed. Plan is coherent, risks are managed, and go/no-go criteria are clear. Ready for Sprint 23 execution.*
