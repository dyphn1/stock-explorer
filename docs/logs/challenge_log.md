# Challenge Log — Review Round 7 (2026-06-12)

> **Theme**: 🔍 Review
> **Participants**: PM, Architect, Design Reviewer, QA Engineer, Challenger
> **Date**: 2026-06-12

---

## Review Report Summary

### Competitor Research (QA)
- **3 new feature suggestions**: C33 (Glossary), C34 (Company Story Timeline), C35 (Market Mood)
- **Key finding**: Notifications (C02) remains the most critical P0 gap — all competitors have it
- **Unique differentiator confirmed**: Company Story Timeline (C34) — no competitor has narrative timeline

### Technical Debt (Architect)
- **19 previous items**: All still open (zero resolved since Round 6)
- **3 new items**: NEW-G15 (bare FinMindClient cache split), NEW-G16 (ETF detection logic bug — **HIGH**), NEW-G17 (revenue_analyzer dead code)
- **Critical finding**: `detect_company_type()` inverts empty-industry logic — stocks with missing industry classified as ETF

### Design Compliance (Designer)
- **DR-01 fully confirmed resolved**: No more `#F39C12` or `linear-gradient` in src/
- **business_card.py confirmed at 462 lines**: All sections render
- **13+ non-palette color instances** remain across 6 files
- **12 component consistency issues** remain
- **Overall grade: C+** (upgraded from C)

---

## Challenger Round 1: Gap Authenticity Challenge

**Challenger questions**:
1. Are C33 (Glossary) and C34 (Story Timeline) really gaps? Or are they nice-to-haves?
2. C35 (Market Mood) — is this aligned with "historian" positioning or does it drift toward trading?
3. NEW-G16 (ETF detection bug) — how long has this been broken? What's the real-world impact?

**Team responses**:
1. **C33 (Glossary)**: The design system explicitly requires "All professional terms must have plain-language translations." This is a **design system compliance issue**, not a nice-to-have. Without systematic glossary, each page invents its own explanations inconsistently. **Verdict: CONFIRMED as gap.**
2. **C34 (Story Timeline)**: This is the #1 thing competitors DON'T have. Our event dashboard (A- graded) has all the data but no narrative thread. The "historian" positioning demands storytelling. **Verdict: CONFIRMED as gap.**
3. **C35 (Market Mood)**: Risk of drifting toward trading. However, framed as "understanding market conditions" (not "buy/sell signal"), it aligns with historian positioning. **Verdict: CONDITIONAL — must be educational, not trading-oriented.**
4. **NEW-G16 (ETF bug)**: The bug exists since `detect_company_type()` was written. Real-world impact: any stock with empty `industry_category` (e.g., newly listed stocks, some ETFs) gets wrong analysis framework. **Verdict: CONFIRMED as P1 bug, not just tech debt.**

---

## Challenger Round 2: Priority Challenge

**Challenger questions**:
1. Should NEW-G16 (ETF bug) be fixed before any new features?
2. C02 (Notifications) has been P0 for 7 rounds but never built. Is it really P0 or should we accept the "pull on next visit" model?
3. With 19 tech debt items and 0 resolved, should the next sprint be a "cleanup sprint" instead of feature work?

**Team responses**:
1. **NEW-G16**: Yes, this is a **data correctness bug**. A stock with missing industry showing the ETF framework is wrong. Should be fixed in the next dev cycle, before C07 (which depends on correct company type detection). **Verdict: Promote to P0 bug fix.**
2. **C02**: The "pull on next visit" model is already partially implemented — the event dashboard shows events on page load. True push notifications (email/Line) require D02 (background worker). The P0 gap is **push notifications specifically**, not event visibility. **Verdict: Keep C02 as P0 but clarify scope — D02 first, then email phase.**
3. **Cleanup sprint**: 7 rounds of 0% tech debt velocity is a serious problem. However, the approved roadmap (Discussion Round 6) has Sprint 1 starting with DR-04 → DR-5 → C07. Recommend **adding NEW-G16 fix to Sprint 1** and dedicating 2h of Sprint 1 to quick tech debt wins (A01, G01, G02, G10, G11, G12 — total ~40min). **Verdict: Add tech debt quick wins to Sprint 1, not a separate cleanup sprint.**

---

## Challenger Round 3: Goal Alignment Challenge

**Challenger questions**:
1. Does the review output align with the product vision's "Iterative cycle over waterfall" principle?
2. Are we building features that pass the "ten-second test"?
3. What are the risks of continuing to defer tech debt?

**Team responses**:
1. **Iterative cycle**: The review identified that 7 rounds produced extensive documentation but 0 tech debt resolution. This is **analysis paralysis** — the team is documenting problems instead of fixing them. The review recommends concrete actions for the next sprint. **Verdict: Alignment improved if recommendations are acted upon.**
2. **Ten-second test**: C34 (Story Timeline) is the strongest ten-second test feature — "Here's what happened to TSMC" is immediately understandable. C33 (Glossary) supports the ten-second test by making terms understandable. C35 (Market Mood) risks failing the ten-second test if too complex. **Verdict: C33 and C34 align, C35 needs careful UX design.**
3. **Tech debt risks**: The ETF detection bug (NEW-G16) is a **correctness issue** that will cause wrong analysis for affected stocks. The N+1 query pattern (C01) will cause performance degradation as the user base grows. The YAML storage (D01) will cause data loss in multi-user scenarios. **Verdict: Tech debt is not just cleanup — some items are correctness and reliability risks.**

---

## Challenger Verdict: ✅ CONFIRMED

**The review report is approved with the following additions**:
1. NEW-G16 (ETF detection bug) promoted to P0 — fix in Sprint 1
2. Add 40min of tech debt quick wins to Sprint 1 (A01, G01, G02, G10, G11, G12)
3. C35 (Market Mood) must be framed as educational, not trading-oriented
4. C34 (Company Story Timeline) is the highest-priority new feature for "historian" alignment

---

*Challenge completed: 2026-06-12. 3 rounds conducted. Review approved with modifications.*

---

# Challenge Log — Review Round 8 (2026-06-13)

> **Theme**: 🔍 Review
> **Participants**: PM, Architect, Design Reviewer, QA Engineer, Challenger
> **Date**: 2026-06-13

---

## Review Report Summary

### Competitor Research (QA)
- **8 new competitors**: Public.com, Seeking Alpha, Koyfin, Finary, Sharesies, Stocksera, Motley Fool, NerdWallet
- **6 new feature suggestions**: C36 (Revenue Tree), C37 (Key Takeaways), C38 (Compare Stories), C39 (What Changed), C39 (Beginner/Expert Mode), C41 (Read Next)
- **Key insight**: Narrative features becoming table stakes internationally; synthesis > data trend confirmed

### Technical Debt (Architect)
- **6 items fixed** since Round 6: G01, G02, G10, G11, G12, G14
- **3 new items**: G15 (st.bar_chart), G16/G06 (bare FinMindClient dup), G17 (KNOWN_COMPANY_REVENUE)
- **14 active + 1 deferred**, ~14 hours remaining

### Design Compliance (Designer)
- **Old palette fully cleaned**: F39C12, 2E86C1, 1B4F72, 8E44AD, 2ECC71, 4A90D9 all gone
- **0 linear-gradient instances** remain
- **11 new issues**: 8 non-palette colors (#5D6D7E, #F8F9FA, #FEF9E7, etc.), 1 component consistency, 1 emoji conflict, 1 Set3 palette
- **Overall grade: C+** (unchanged)

---

## Challenger Round 1: Gap Authenticity Challenge

**Challenger questions**:
1. Are C36 (Revenue Tree) and C37 (Key Takeaways) really gaps? Or do we already have similar features?
2. C38 (Compare Stories) — is this just peer comparison with a different name?
3. With 6 tech debt items now fixed, is the "zero velocity" problem solved?

**Team responses**:
1. **C36 (Revenue Tree)**: We have a pie chart showing revenue breakdown by segment. C36 is a HIERARCHICAL tree showing how money flows (TSMC → 5nm → Apple/NVIDIA). This is fundamentally different from a pie chart. Public.com and Koyfin both have this. **Verdict: CONFIRMED as gap.**
2. **C37 (Key Takeaways)**: We have event dashboard (A-) but no synthesized summary. A beginner looking at the business card page sees 7 sections but no "here are the 3 things you should remember." Seeking Alpha's Key Takeaways prove this pattern works. **Verdict: CONFIRMED as gap.**
3. **C38 (Compare Stories)**: Different from peer comparison. Peer comparison shows metrics side-by-side. Compare Stories would show "TSMC's story vs Intel's story" — narrative comparison, not metric comparison. **Verdict: CONFIRMED as distinct from peer comparison.**
4. **Tech debt velocity**: 6 items fixed is meaningful progress. But 14 items remain and the team hasn't done a dedicated cleanup sprint. **Verdict: Improving but not solved.**

---

## Challenger Round 2: Priority Challenge

**Challenger questions**:
1. Should design quick wins (D-073, D-071, D-084) be done before any new features?
2. C02 (Notifications) has been P0 for 8 rounds. Is it time to accept "pull on next visit" as sufficient?
3. With C34 (Story Timeline) requiring a spike first, should we prioritize C37 (Key Takeaways) instead since it's lower effort?

**Team responses**:
1. **Design quick wins**: D-073 (5 min, global impact) and D-071 (30 min, all pie charts) should absolutely be done before new features. They're 35 minutes total and affect every page. **Verdict: Add to Sprint 0.**
2. **C02 (Notifications)**: The "pull on next visit" model IS partially implemented — events show on page load. True push (email/Line) requires D02 (background worker). The P0 gap is specifically PUSH notifications. **Verdict: Keep C02 as P0 but clarify — D02 investigation first, then email phase.**
3. **C37 vs C34 priority**: C37 (6-8h) is lower effort and delivers immediate value. C34 (16-24h + 3h spike) is higher risk. **Verdict: C37 before C34. C34 spike in Sprint 1, full implementation in Sprint 2.**

---

## Challenger Round 3: Goal Alignment Challenge

**Challenger questions**:
1. Does the 6-new-feature pipeline align with "Iterative cycle over waterfall"?
2. Will C36-C41 pass the "ten-second test"?
3. What's the risk of continuing to add features while design grade is C+?

**Team responses**:
1. **Iterative cycle**: Adding 6 features at once would be waterfall. The recommended approach is: Sprint 0 (design fixes) → Sprint 1 (C37 + C28 spike) → Sprint 2 (C34 full + C36). One feature per sprint, verify, then next. **Verdict: Alignment IF sprint plan is followed.**
2. **Ten-second test**: C37 (Key Takeaways) is the strongest — "Here are 3 things to remember about TSMC" is immediately testable. C36 (Revenue Tree) is also strong — visual hierarchy is intuitive. C38 (Compare Stories) is weakest — comparing narratives is abstract. **Verdict: C37 and C36 pass, C38 needs UX validation.**
3. **Design grade risk**: Adding features on a C+ foundation means each new feature inherits design inconsistencies. Sprint 0 design fixes are a prerequisite. **Verdict: Sprint 0 must complete before feature work begins.**

---

## Challenger Verdict: ✅ CONFIRMED

**The review report is approved with the following additions**:
1. D-073 and D-071 must be in Sprint 0 (35 min total, global impact)
2. C37 (Key Takeaways) prioritized over C34 (Story Timeline) — lower effort, immediate value
3. C34 spike (3h) in Sprint 1, full implementation in Sprint 2
4. Sprint 0 design prerequisite must be completed before any new feature work
5. C02 scope clarified: D02 investigation → email phase → Line phase

---

*Challenge completed: 2026-06-13. 3 rounds conducted. Review approved with modifications.*
