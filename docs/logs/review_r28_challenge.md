# Round 28 — Challenge Record (2026-06-18)

## Round 1: Gap Authenticity Challenge

- **Team proposal**: QA identified 4 new feature gaps (C123-C126) from competitor research:
  - C123: Revenue Geography Breakdown (P2, 8-12h)
  - C124: Moat Type Classification System (P2, 10-14h)
  - C125: Segment-Level Profitability View (P2, 6-10h)
  - C126: Competitor Moat Comparison View (P2, 10-14h)
  - All 4 are deferred to Sprint 14+. Sprint 13b focuses on C36 Revenue Tree + C46 Moat Analysis.

- **Challenge**:

  **1. C123 (Revenue Geography) — authentic gap, but premature.**
  Koyfin and Simply Wall St both show revenue geography. However, Stock Explorer's target users are *beginners* exploring *TW-listed* stocks. For most TW stocks, revenue geography data is either unavailable via FinMind or requires manual curation. The QA report itself says "if available" — this is a conditional feature, not a proven gap. Geography is valuable context for a few headline stocks (TSMC) but low-value for the majority of the 1,800+ TW stocks. Is this really more impactful than C42 (Stock Screener, P1) or C45 (Valuation Band, P2) which serve ALL companies?

  **2. C124 (Moat Type Classification) — strongest gap, but duplicates C46's Sprint 13b scope.**
  C46 Moat Analysis is planned for Sprint 13b. C124 adds moat type classification to... C46? If C124 is P2 and aligned with core value #4, why isn't it part of C46's Sprint 13b scope instead of deferred to Sprint 14? The architect's pre-work for C46 already suggests defining "5 moat dimensions." The designer's C46 spec already plans "5 dimensions: brand, network effects, switching costs, cost advantages, intangible assets." C124's content is essentially *baked into* C46's planned design. Splitting it into Sprint 14 suggests C46 will ship without the most educational dimension — exactly the "rating without the story" anti-pattern the historian positioning rejects.

  **3. C125 (Segment Profitability) — legitimate extension, but depends on C123.**
  Margin-per-segment is a natural extension of C36 Revenue Tree (Sprint 13b). Simply Wall St proves this is valued. However, without C123's geographic dimension being resolved first (data source uncertainty), C125 faces the same data availability problem. Also, segment-level margin data for TW stocks is scarcer than segment-level revenue data. The 6-10h estimate likely omits data sourcing effort.

  **4. C126 (Moat Comparison) — highest competitor alignment, but highest risk.**
  This is the only gap that directly serves core value #5 (Benchmark-oriented analysis). But it creates a dependency on C46's moat scoring model being stable. Shipping C46 in Sprint 13b and then adding comparison in Sprint 14 requires the C46 scoring rubric to be designed for comparison from day one. If the Sprint 13b team optimizes for single-company analysis, Sprint 14's comparison view will require rework.

  **5. Missing question: Are there things competitors DON'T have that we should build?**
  The competitor analysis is entirely US/EU-centric (Morningstar, Simply Wall St, Stockopedia, Koyfin). No TW competitor analysis for these specific features was done. 財報狗, CMoney, and TEJ likely have segment views or moat-adjacent features for TW stocks. The QA report mentions TEJ only in passing. Before claiming C124 is a "unique educational feature" and C125 is "world-class," the team should verify what 財報狗 and CMoney already show for TW stock segment breakdowns. White-space claims require TW-competitor validation, not just US-competitor absence.

  **6. Priority challenge: Is Sprint 13b (C36 + C46) correctly prioritized vs. other P1 items?**
  The regression check shows C42 (Stock Screener) is P1 and still fully relevant. C119 (Glossary-First Onboarding) is P1 and still fully relevant. Sprint 13b chooses C36 (revenue tree polish — a Sprint 12 feature being enhanced) and C46 (new moat analysis) over these P1 items. The implicit priority is: new feature creation > P1 backlog items. This needs explicit justification — is C36+C46 truly more valuable than a stock screener or onboarding flow for beginners?

## Round 2: Priority Challenge

- **Team response** (as represented in PM's consolidated report):
  - C36 🟢 READY — infrastructure exists (73-line page + service layer), Sprint 13b work is polish/enhancement.
  - C46 🟡 CONDITIONALLY READY — needs 2-3h pre-work for data model design before Sprint 13b Day 1.
  - D-079 (dual tooltip) should be fixed before adding more tooltips to C36 — 1-2h.
  - D-080 (health card border) can be fixed during Sprint 13b.
  - Sprint 13b execution order: C36 first, then C46, then D-080.

- **Re-challenge**:

  **1. C36 before C46 sequencing is correct, but the rationale is incomplete.**
  C36 first makes sense because the infrastructure exists and it's lower risk. However, C36's Sprint 13b scope (glossary tooltips, concentration warning, trend mini-chart) is *enhancement* of an already-shipped feature. C46 is *new* and higher risk. The sequencing should be: C36 Day 1-2 (quick wins, validate Sprint 13b velocity), then C46 Day 3+ (main effort). But the PM report doesn't specify a go/no-go gate between C36 and C46. If C36 takes longer than expected (e.g., the concentration warning requires new data logic), C46's timeline compresses. A Day 2 go/no-go gate for C46 should be explicit.

  **2. 2-3h pre-work for C46 is likely insufficient.**
  The architect recommends: (a) define moat data model (5 dimensions, scoring scale, data sources), (b) design moat.yaml schema, (c) scaffold moat_analyzer.py. This is 2-3h *if* the team already knows what moat dimensions to use. But the designer's spec lists 5 dimensions (brand, network effects, switching costs, cost advantages, intangible assets) while the QA's C124 suggests Morningstar's 5-type taxonomy. Are these the same 5? If the team spends 2-3h pre-work and then discovers the dimensions need to change after designer review, the pre-work estimate doubles. Recommend: 2-3h pre-work is the *minimum*. Budget 4-5h and include a 1h "dimension alignment" session between architect and designer before coding begins.

  **3. D-079 should be fixed BEFORE Sprint 13b, not during.**
  The PM report says "Fix D-079 before adding more tooltips to C36" — this is correct. But the Sprint 13b plan lists C36 polish (which includes adding glossary tooltips) as Day 1 work. If D-079 isn't fixed first, C36's new tooltips will be added to a broken dual-tooltip pattern, making D-079 harder to fix later (more tooltips to merge). D-079 must be a Sprint 13b Day 0 prerequisite, not a concurrent task.

  **4. D-080 (health card border) should be fixed during Sprint 13b, but it's coupled to C46.**
  The designer recommends a `_health_card()` component with dynamic border colors. C46 Moat Analysis plans a moat strength indicator that could use the same pattern. If D-080 is fixed independently (0.5-1h) and then C46 builds a separate moat strength card, there's duplication. Better: fix D-080 as part of C46's card component work, creating a reusable `_score_card(value, label, color_fn)` that serves both the story card health score and the moat strength indicator.

  **5. The Sprint 13b plan has no explicit content creation budget.**
  C36's "concentration warning" and "trend mini-chart" are data features (engineering). But C46's moat analysis requires: (a) moat.yaml with dimension definitions, (b) scoring criteria per dimension, (c) plain-language explanations per dimension per company. The handoff rules say "content creation must be budgeted at 40% of effort for education features." C46 is an education feature. If C46 is estimated at 26-38h total, ~10-15h should be content creation. The PM report doesn't mention this. Without content budgeting, C46 ships with hardcoded placeholder text.

## Round 3: Goal Alignment Challenge

- **Team response** (as represented in PM's consolidated report and sub-agent analyses):
  - C36 Revenue Tree: Already has `_historian_disclaimer("revenue_tree")` (falls back to "general"). Designer recommends adding a specific revenue tree disclaimer.
  - C46 Moat Analysis: Designer explicitly recommends `_historian_disclaimer("general")` at the bottom. Moat analysis is "inherently interpretive, so the disclaimer is important."
  - C46 design direction: "historian-evidential approach" — show evidence for moat claims, not just ratings.
  - All 4 new gaps (C123-C126) are claimed to align with core values #1, #4, and #5.

- **Confirmation**: ✅ **Aligned — with conditions**

- **Conditions**:

  **1. C46 Moat Analysis must NOT become a "stock picking" signal.**
  The product vision explicitly says: "Do not say buy or sell; only explain what has happened to the company over time." A moat rating (Wide/Narrow/None) is dangerously close to a buy signal — "wide moat = good company = buy" is the intuitive leap beginners will make. The historian framing must be: "This company has maintained a cost advantage for 15 years because..." not "This company has a WIDE moat (score: 85/100)." The evidence-first, narrative approach the designer recommends is correct. The scoring/rating should be secondary to the historical evidence narrative. **Condition: C46's primary content must be historical evidence (what happened, when, why), with the moat score as a summary — not the other way around.**

  **2. C124 (Moat Type Classification) must be integrated into C46, not deferred.**
  As challenged in Round 1, C124's content is already in C46's planned design. Deferring C124 to Sprint 14 means C46 ships without moat type classification — the most educational dimension. This contradicts core value #4 (point-to-point knowledge construction) and the ten-second test (a beginner seeing "Wide Moat" without understanding *what type* of moat fails the test). **Condition: C46 must include moat type classification (from C124) as part of its Sprint 13b scope. C124 should be closed/merged, not deferred.**

  **3. C126 (Moat Comparison) requires C46's scoring rubric to be comparison-ready from day one.**
  If C46's scoring model is designed for single-company analysis, adding comparison in Sprint 14 will require rework. **Condition: C46's moat scoring rubric must be designed with peer comparison in mind (normalized scores, comparable dimensions), even if the comparison UI ships in Sprint 14.**

  **4. C123 (Revenue Geography) needs a TW-competitor check before Sprint 14 commitment.**
  The "world-class" claim requires validation that no TW competitor (財報狗, CMoney, TEJ) already shows revenue geography for TW stocks. **Condition: Before Sprint 14 planning, QA must verify revenue geography availability for top 20 TW stocks via FinMind and check 財報狗/CMoney for existing geography features.**

  **5. Content creation must be explicitly budgeted for C46.**
  Per handoff rules: "Content creation must be budgeted at 40% of effort for education features." C46 requires moat dimension definitions, scoring criteria, and plain-language explanations. **Condition: C46's Sprint 13b estimate must explicitly separate engineering hours (service + page) from content hours (moat.yaml + scoring rubric + explanations). Content creation should begin in parallel with D-079 fix (pre-Sprint 13b).**

  **6. D-079 must be a Day 0 prerequisite, not concurrent.**
  **Condition: D-079 (dual tooltip merge) must be completed before any Sprint 13b tooltip work begins. No new tooltips until the dual pattern is resolved.**

- **Alignment Basis**: After 3 rounds, Sprint 13b's core direction (C36 + C46) is sound and aligns with the historian positioning. The key risks are: (a) C46 drifting toward stock-picking signals (mitigated by evidence-first design), (b) C124 being unnecessarily deferred when it's core to C46's educational value (mitigated by merging into C46), and (c) content creation being underestimated (mitigated by explicit 40% content budget). With these 6 conditions met, Sprint 13b delivers features that are genuinely historian-aligned, not just competitor-matching.
