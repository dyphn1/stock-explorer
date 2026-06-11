# 2026-06-19 Challenger Log — Round 14 Discussion

> **Author**: Challenger
> **Date**: 2026-06-19
> **Context**: Round 14 — challenging the team's preliminary decision on Sprint 4 feature directions (C48, C51, C38, C53-1, D16, R3). Three-round challenge process to stress-test the "Sprint 4 Execution" direction.

---

### Team Preliminary Decision

The PM consolidated all three roles into a "Sprint 4 Execution" direction with 6 items:

**Direction A: C48 Company Story Card** — Hero card at top of company pages. 30-second visual summary with one-liner, 3 notable metrics with analogies, rotating "Did You Know?" fact. New `story_composer.py` service + `_story_card()` component. 10-14h. Requires D16 + D24 (D24 ✅). Competitive urgency: 🔴 HIGH — Atom Finance, Dhan, Toss, Stake all have this.

**Direction B: C51 Sector Heatmap** — First market-level feature. Plotly treemap with green/red performance colors. Click-through to sector detail with plain-language narratives. New `market_data.py` service (resolves D25) + `sector_classification.yaml`. 12-16h. Requires R3 (Batch API). Competitive validation: 🟡 HIGH — StockEdge, Moomoo, 永豐金證券 all have heatmaps but lack narrative layer.

**Direction C: C38 Compare Stories Phase 1** — New "故事比較" tab on peer comparison page. Side-by-side narrative cards + comparison bullets + closing analogy. New `narrative_comparator.py` service + `comparison_templates.yaml`. 10-12h. Soft dependency on D16. Competitive gap: 🔴 No TW competitor has narrative comparison.

**Direction D: C53-1 Social Sharing URL** — Quick win. URL parameter handling + copy link button. 2-3h. No dependencies. Table stakes — every competitor has sharing.

**Direction E: D16 Split analogy_engine.py** — Extract 850-line god module into 4 focused modules. 2-3h. Unblocks C48. Critical path item.

**Direction F: R3 Batch API minimal** — ThreadPoolExecutor for category_browser.py. 1-2h. Unblocks C51. Resolves P1 bottleneck + D7.

**Recommended Sequence**: D16 → R3 → C38 → C51 → C48 → C53-1
**Total Sprint 4 effort**: 37-50h (most likely 43.5h)

**Key constraints**:
- Stack: Python + Streamlit + Plotly + FinMind API. No LLM in production.
- business_card.py extracted (D24 ✅). D16 must complete before C48.
- All content in YAML files, not Python.
- All features must pass "explain, don't predict" test.
- L0 + L1 verification required before every commit.

---

### Round 1: Feature Direction Challenge

#### Challenges

**1.1 — Does C48 (Company Story Card) truly differentiate, or is it "C37 but bigger"?**

C37 (Key Takeaways) already shows 3-5 bullet points of synthesized information at the top of the business card page. C48 adds a hero card with one-liner, 3 metrics, and a fact — also at the top. The Designer flags this as DR-041 (P1 risk): "Both are summary cards; C37 already shows key takeaways above the fold."

The key question: **Does the user need TWO summary cards?** C48's positioning is "narrative identity" while C37's is "analytical summary." But from a user's perspective, both answer "what should I know about this company?" The risk is redundancy — two hero cards competing for attention.

**Counter-argument**: C48 is the "30-second story" (who is this company?) while C37 is the "key facts" (what are the most important numbers?). They serve different cognitive purposes: identity vs. analysis. The positioning is defensible IF the visual distinction is clear (C48 = amber hero, C37 = orange summary).

**1.2 — Does C51 (Sector Heatmap) align with "historian" positioning, or does it veer into market commentary?**

The product vision says "Focus on the company itself, not short-term price movement." A sector heatmap is inherently about short-term price movement — "which sectors are up/down today." The Architect flags this as D34 (new data flow pattern) and the Developer flags market-level tone drift risk (T4).

The key question: **Can a sector heatmap be built in "historian" language?** The Architect's recommendation is to add plain-language narratives explaining WHY sectors moved (past tense, factual). But the heatmap visualization itself is inherently present-focused. The competitor research shows StockEdge and Moomoo both have heatmaps, but they're purely visual — no narrative layer.

**Counter-argument**: C51 can be historian-aligned if it focuses on "what happened to this sector" (past tense narratives) rather than "which sectors are hot" (present-focused). The sector detail page should say "本週半導體上漲3.2%，主要因為AI晶片需求持續強勁" not "半導體板塊大漲，建議關注."

**1.3 — Is C38 (Compare Stories) Phase 1 actually valuable without LLM?**

The Developer's own assessment: "May feel like 'reading two business cards side by side' rather than true narrative comparison." The Phase 1 approach is structured data only — two companies' metrics and analogies side-by-side with comparison bullets. No true narrative generation.

The key question: **Is "side-by-side business cards" actually a new feature, or just a layout change?** Users can already open two browser tabs and compare. The value of C38 Phase 1 is the comparison bullets and closing analogy — but these are template-generated, not truly narrative.

**Counter-argument**: No TW competitor has narrative comparison at all. Even side-by-side cards with comparison bullets are a differentiator. Phase 2 (true narrative comparison) can be added later with LLM. Phase 1 establishes the UI pattern and template infrastructure.

**1.4 — Is the Sprint 4 sequence optimal?**

The recommended sequence is D16 → R3 → C38 → C51 → C48 → C53-1. But the Architect recommends prioritizing C48 over C51: "C48 has the highest competitive urgency (Atom Finance is doing it now) and lowest technical risk after D16."

The key question: **Should C48 come before C51?** The current sequence puts C38 before C51 before C48. But C48 only depends on D16 (which is first), while C51 depends on R3 (which is second). If D16 completes first, C48 could start before C51.

**Counter-argument**: The current sequence is fine because C38 and C51 can be parallelized after R3. C48 is sequenced last because it's the most complex view integration (hero card at top of business card page). The sequence is: unblockers first (D16, R3), then parallel work (C38, C51), then C48 (which benefits from all previous work being done).

#### Team Response

**Architect's response**: The Architect recommends prioritizing C48 over C51 due to competitive urgency. Atom Finance is doing exactly this now. The Architect's proposed sequence: D16 → R3 → C48 → C51 → C38 → C53-1. On the C48/C37 redundancy concern, the Architect notes that C48 is a "narrative identity" card (who is this company?) while C37 is "analytical summary" (what are the key facts). The Architect recommends clear visual distinction: C48 = amber hero card (6px border), C37 = orange summary card (4px border). On C51 historian alignment, the Architect recommends past-tense narratives and factual language. On C38 Phase 1 value, the Architect acknowledges the limitation but notes that no TW competitor has narrative comparison at all.

**Designer's response**: The Designer's DR-041 (C48/C37 redundancy) is a P1 risk that must be resolved. The Designer's recommendation: C48 goes ABOVE C37 (first on page). C48 = narrative identity (one-liner + 3 metrics + fact). C37 = analytical summary (3-5 bullets). If redundancy is detected in testing, merge fact elements. The Designer also flags DR-042 (C38 recommendation perception) as the most critical design risk — the side-by-side comparison MUST NOT be perceived as "which stock to buy." On C51, the Designer recommends the treemap visualization with 6-level green/red color scale and past-tense sector narratives.

**Developer's response**: The Developer's sequence (D16 → R3 → C38 → C51 → C48 → C53-1) is based on dependency analysis, not value prioritization. The Developer agrees that C48 could be prioritized over C51 if the team wants to ship the highest-urgency feature first. On C38 Phase 1 value, the Developer notes that the comparison bullets and closing analogy are the real value — the side-by-side cards are just the presentation layer. On C48/C37 redundancy, the Developer notes that C48 adds new data (metric selection algorithm, rotating facts) that C37 doesn't have.

**Synthesis**: The Architect and Designer agree that C48 should be prioritized over C51. The Developer's sequence is dependency-optimal but not value-optimal. The C48/C37 redundancy concern is acknowledged — clear visual distinction and positioning is required. C51's historian alignment requires careful tone management. C38 Phase 1 is valuable as a differentiator even without LLM.

#### Resolution

**PARTIALLY RESOLVED**. The challenge identifies three issues:

1. **C48/C37 redundancy (DR-041)**: Acknowledged by all roles. Resolution: C48 goes above C37. Clear visual distinction (amber 6px vs. orange 4px). Different cognitive purpose (identity vs. analysis). Monitor for redundancy in testing.

2. **C51 historian alignment**: Resolution: Past-tense narratives only. Sector detail pages must use factual language. D23 tone guidelines must be written before C51 implementation.

3. **Sequence adjustment**: The Architect recommends C48 before C51. The Developer's sequence is dependency-optimal. Resolution: Keep the current sequence (D16 → R3 → C38 → C51 → C48 → C53-1) but allow C48 to start as soon as D16 completes, even if C38/C51 are in progress. This is a parallelization opportunity, not a sequence change.

---

### Round 2: Priority Challenge

#### Challenges

**2.1 — Should C48 really be last in the sequence when it has the highest competitive urgency?**

The Architect states: "C48 has the highest competitive urgency (Atom Finance is doing it now) and lowest technical risk after D16." But the recommended sequence puts C48 fifth (after D16, R3, C38, C51). If C48 only depends on D16, why isn't it second?

The current sequence means C48 starts after C38 and C51 are complete. At 10-12h each, that's 22-28h of work before C48 starts. If the team works sequentially, C48 doesn't start until 22-28h into the sprint.

**The "competitive urgency" argument**: If Atom Finance is doing this now, every week of delay is a week where Stock Explorer looks less differentiated. C48 should be the FIRST feature after unblockers (D16 + R3).

**The counter-argument**: C38 and C51 can be developed in parallel with C48 if resources allow. The sequence is not strictly linear — C38 and C51 are independent of C48. The "fifth" position is just the commit order, not the development order.

**2.2 — Is C51 (Sector Heatmap) the right market-level feature to build first?**

C51 is Stock Explorer's first market-level feature. It introduces a new architectural pattern (market-level data flow via `market_data.py`). The Developer notes this is "architecturally significant" and "establishes the pattern for C49 and future market features."

The key question: **Is a sector heatmap the right FIRST market-level feature for a "historian" product?** Alternatives:
- C49 (Daily Market Pulse) — automated market summary with plain-language explanations
- C61 (Sector Rotation Visualizer) — shows how sectors have rotated over time (more historian-aligned)
- C64 (Daily Market Quiz) — gamified daily engagement

C61 (Sector Rotation) is more historian-aligned (shows how sectors have changed over time) and creates a daily engagement loop. C51 (Heatmap) is more present-focused ("which sectors are hot now").

**Counter-argument**: C51 is the lowest-effort market-level feature (12-16h vs. C49 at 10-14h + content creation, C61 at 10-16h + more complex visualization). It's the right first step because it establishes the `market_data.py` pattern with the least risk. C61 can build on C51's foundation.

**2.3 — Is C53-1 (Social Sharing URL) worth doing in Sprint 4?**

C53-1 is a 2-3h quick win. It adds URL parameter handling and a copy link button. The Developer notes: "URL sharing without image/summary is low-value" and "Acceptable for MVP."

The key question: **Is 2-3h better spent on C53-1, or on accelerating C48 content creation?** C48's content creation (story templates for 5-6 company archetypes) is 2-3h that could be done in parallel with D16/R3. C53-1 is purely a presentation-layer change with no content creation.

**Counter-argument**: C53-1 is a true quick win — 2-3h, no dependencies, no content creation. It can be done in parallel with any other work. It also enables future features (notification deep links, external app integration). The opportunity cost is near zero.

**2.4 — Should C64 (Daily Market Quiz) be considered for Sprint 5?**

The Architect identifies a gap: "Daily engagement loop — Kabu.com and Toss Securities prove that daily gamified engagement drives retention. It's low effort (8-12h) and creates a daily engagement loop that Stock Explorer currently lacks."

The key question: **Should C64 be added to Sprint 5, replacing or supplementing existing features?** Sprint 5 is already heavy (C58 + C62 + C60 + C55 + C56 = 42-68h). Adding C64 (8-12h) would make it 50-80h.

**Counter-argument**: C64 is a P2 feature. It should be evaluated after Sprint 4 ships. The current Sprint 5 plan is already approved by the Challenger (Round 13). Adding C64 should be a separate discussion.

#### Team Response

**Architect's response**: The Architect's original recommendation was to prioritize C48 over C51. The Architect agrees that C48 should start as soon as D16 completes, even if C38/C51 are in progress. On C51 as the first market-level feature, the Architect acknowledges that C61 (Sector Rotation) is more historian-aligned but notes that C51 is the lowest-risk first step. The Architect recommends C51 now, C61 in Sprint 6. On C64, the Architect recommends evaluating it for Sprint 5 after Sprint 4 ships.

**Designer's response**: The Designer's framework places C48 as the hero card (first on page) and C51 as a new page (separate from company pages). The Designer agrees that C48 should be prioritized. On C51, the Designer's treemap design is complete and ready for implementation. On C64, the Designer has no position — it's outside the current design scope.

**Developer's response**: The Developer agrees that C48 can start in parallel with C38/C51 after D16 completes. The Developer's sequence is dependency-optimal, not value-optimal. On C51 as the first market-level feature, the Developer notes that `market_data.py` is architecturally significant regardless of which market feature is built first. On C53-1, the Developer confirms it's a true quick win with near-zero opportunity cost. On C64, the Developer recommends evaluating it after Sprint 4.

**Synthesis**: All roles agree that C48 should be prioritized (start as soon as D16 completes). C51 is the right first market-level feature (lowest risk, establishes pattern). C53-1 is a true quick win. C64 should be evaluated after Sprint 4.

#### Resolution

**RESOLVED — with revision required**. The priority order is confirmed with one revision:

1. **C48 starts in parallel with C38/C51 after D16 completes**: Don't wait for C38/C51 to finish before starting C48. The sequence is: D16 → (R3 + C48 start) → C38/C51/C48 in parallel → C53-1.

2. **C51 is the right first market-level feature**: Lowest risk, establishes `market_data.py` pattern. C61 can build on this foundation.

3. **C53-1 stays in Sprint 4**: True quick win, near-zero opportunity cost.

4. **C64 deferred to Sprint 5 evaluation**: After Sprint 4 ships, evaluate whether C64 should replace or supplement existing Sprint 5 features.

---

### Round 3: Goal Alignment Challenge

#### Challenges

**3.1 — Does this proposal help achieve M2/M3 milestones?**

M2: "Four deep-dive sections — Can answer 'What has this company been up to recently?'"
M3: "Timeline & categorization — Users can independently explore across dimensions."

**M2 analysis**:
- C48 (Story Card): Serves M2 by providing a 30-second company understanding. The "what has this company been up to" question is partially answered by the one-liner and metrics.
- C38 (Compare Stories): Serves M2 by enabling comparison of two companies' stories.
- C51 (Sector Heatmap): Does NOT directly serve M2 — it's a market-level feature, not company-level.
- C53-1 (Social Sharing): Does NOT serve M2 — it's distribution, not content.
- D16 (Split): Does NOT serve M2 — it's technical debt.
- R3 (Batch API): Does NOT serve M2 — it's performance infrastructure.

**Verdict**: Only C48 and C38 directly serve M2. C51 is M3-aligned. The rest are infrastructure.

**M3 analysis**:
- C51 (Sector Heatmap): Directly serves M3 — "categorization" and "explore across dimensions."
- C38 (Compare Stories): Serves M3 by enabling cross-company exploration.
- C48 (Story Card): Partially serves M3 — the "Did You Know?" facts add cross-dimensional context.

**Verdict**: The Sprint 4 features are more M3-aligned than M2-aligned. This is acceptable if M2 is on track (C44 Risk Analysis, C38 Compare Stories both serve M2).

**3.2 — Are there contradictions between the roles' opinions?**

**Contradiction 1: C48 priority vs. sequence**
- Architect: C48 should be prioritized over C51 (competitive urgency)
- Developer: C48 is sequenced last (dependency-optimal)
- Resolution: C48 starts in parallel with C38/C51 after D16 completes. Both are correct — the sequence is commit order, not development order.

**Contradiction 2: C51 historian alignment**
- Architect: C51 can be historian-aligned with past-tense narratives
- Developer: Market-level tone drift is a medium risk (T4)
- Designer: C51 is a separate page, not company-level, so historian alignment is less critical
- Resolution: D23 tone guidelines must be written before C51. All market-level text must use past-tense, factual language.

**Contradiction 3: C38 Phase 1 value**
- Architect: "No TW competitor has narrative comparison" — high value
- Developer: "May feel like reading two business cards side by side" — limited value
- Designer: Side-by-side cards with comparison bullets are a differentiator
- Resolution: C38 Phase 1 is valuable as a differentiator AND as infrastructure for Phase 2. The comparison bullets and closing analogy are the real value.

**3.3 — Are there overlooked risks?**

**Risk 1: C48/C37 redundancy is still unresolved**
The Designer's DR-041 is P1. The mitigation is "clear visual distinction" and "different cognitive purpose." But this is untested. If users see two summary cards and don't understand the difference, the page feels cluttered.

**Mitigation**: Add a "設計說明" tooltip to each card explaining its purpose. C48: "這是公司的故事 — 30秒認識這家公司." C37: "這是重點摘要 — 用數據看懂這家公司."

**Risk 2: C51 FinMind sector data gap**
The Developer flags this as T2 (medium probability, high impact). If FinMind doesn't provide clean sector classification, `sector_classification.yaml` becomes a manual curation burden.

**Mitigation**: Validate FinMind sector codes in the first 1h of C51. If data quality is poor, fall back to `category_browser.py` industry classification (already exists).

**Risk 3: Sprint 4 total effort (37-50h) is heavy**
At 37-50h, Sprint 4 is the heaviest sprint yet. The previous sprints were 24-29h (Sprint 3) and 24-33h (Sprint 4 planned). The team is nearly doubling the sprint load.

**Mitigation**: The parallelization of C48 with C38/C51 helps. C53-1 (2-3h) is a quick win that can be done in any spare time. If the sprint is at risk of overrun, C53-1 can be deferred to Sprint 5 (it's P2).

**Risk 4: C38 mobile layout**
The Developer flags T3: "Two-column layout breaks PPT-style on mobile." The Designer's mockup shows a 2-column layout that won't work on 320px screens.

**Mitigation**: Design mobile fallback first (single-column stacked layout). Test with 320px viewport before implementing desktop version.

**3.4 — Does the proposal create a coherent product experience?**

The Sprint 4 features add:
- A hero story card on every company page (C48)
- A new sector heatmap page (C51)
- A new comparison tab on peer comparison (C38)
- Shareable URLs (C53-1)

**The coherence question**: Does a user who starts in Sprint 4 experience a coherent product? Or do they experience a grab bag of features?

**Analysis**: The features are coherent IF the narrative thread is clear:
1. **C48** = "Here's the company's story" (identity)
2. **C38** = "Here's how two companies' stories differ" (comparison)
3. **C51** = "Here's how the company's sector is doing" (context)
4. **C53-1** = "Share what you've learned" (distribution)

This is a coherent "story-first" narrative: identity → comparison → context → distribution. The features build on each other logically.

#### Team Response

**Architect's response**: The Architect agrees that the features form a coherent "story-first" narrative. On M2/M3 alignment, the Architect notes that M2 is on track (C44 + C38 serve M2) and M3 features (C51) can be built in parallel. On the C48/C37 redundancy, the Architect recommends A/B testing the two cards in Sprint 5. On total effort, the Architect notes that 37-50h is achievable with parallelization.

**Designer's response**: The Designer's card type library (_story_card, _compare_card, _sector_tile) provides visual coherence across all Sprint 4 features. On mobile, the Designer recommends designing the mobile fallback for C38 first. On C48/C37 redundancy, the Designer's DR-041 remains P1 — the team must monitor this in testing.

**Developer's response**: The Developer confirms that the parallelization of C48 with C38/C51 is feasible. On total effort, the Developer notes that 37-50h is the full pipeline — if the team needs to cut scope, C53-1 is the easiest to defer. On FinMind sector data, the Developer recommends a 1h spike at the start of C51 to validate data availability.

**Synthesis**: All roles agree that the Sprint 4 features are coherent. The "story-first" narrative (identity → comparison → context → distribution) is sound. The main risks are C48/C37 redundancy (P1), C51 data validation (medium), and total effort (manageable with parallelization).

#### Resolution

**RESOLVED — with conditions**. The challenge identifies genuine risks but the overall direction is sound. The key conditions:

1. **C48 starts in parallel with C38/C51 after D16 completes**: Don't wait for C38/C51 to finish.

2. **D23 tone guidelines before C51**: Write market-level tone guidelines before implementing C51. All market-level text must use past-tense, factual language.

3. **C51 data validation spike**: 1h spike at the start of C51 to validate FinMind sector data availability. Fall back to `category_browser.py` industry classification if needed.

4. **C38 mobile fallback first**: Design and test mobile fallback (single-column stacked layout) before implementing desktop version.

5. **C48/C37 redundancy monitoring**: Add design tooltips to both cards. Monitor for redundancy in testing. Merge if needed in Sprint 5.

6. **Scope deferral plan**: If Sprint 4 is at risk of overrun, C53-1 (2-3h) is the first item to defer to Sprint 5.

---

### Final Decision

✅ **CONFIRMED — with 6 conditions**

The team's Round 14 "Sprint 4 Execution" direction is confirmed, with the following plan:

**Sprint 4 Sequence**:
```
D16 (2-3h) → Split analogy_engine.py [UNBLOCKS C48]
  │
  ├─→ R3 (1-2h) → Batch API minimal [UNBLOCKS C51]
  │     │
  │     ├─→ C38 (10-12h) → Compare Stories Phase 1
  │     │     │
  │     │     └─→ C51 (12-16h) → Sector Heatmap
  │     │
  │     └─→ C48 (10-14h) → Company Story Card [STARTS AFTER D16]
  │
  └─→ C53-1 (2-3h) → Social Sharing URL [ANY TIME]
```

**Total Sprint 4 effort**: 37-50h (most likely 43.5h)
**Parallelization**: C48 starts after D16 (in parallel with C38/C51)

**Conditions**:
1. C48 starts in parallel with C38/C51 after D16 completes
2. D23 tone guidelines written before C51 implementation
3. C51 data validation spike (1h) at start of implementation
4. C38 mobile fallback designed and tested before desktop version
5. C48/C37 redundancy monitored in testing; merge if needed in Sprint 5
6. C53-1 is first item to defer if sprint is at risk

**Key risks accepted**:
1. **C48/C37 redundancy (DR-041)**: Mitigated by visual distinction and positioning. Monitor in testing.
2. **C51 data quality**: Mitigated by 1h validation spike. Fallback plan exists.
3. **Total effort (37-50h)**: Mitigated by parallelization. C53-1 is deferrable.
4. **C38 mobile layout**: Mitigated by mobile-first fallback design.
5. **Market-level tone drift**: Mitigated by D23 tone guidelines.

**Challenger's note**: The Round 14 proposal is strategically sound. The "story-first" narrative (identity → comparison → context → distribution) is coherent and aligns with the historian positioning. The main operational risk is the sprint load (37-50h is heavy) — the team must parallelize effectively and be ready to defer C53-1 if needed. The C48/C37 redundancy is a design risk that must be monitored in testing. Overall, this is the right set of features for Sprint 4.

---

*Challenger Round 14 challenge completed. 3 rounds conducted. Decision confirmed with 6 conditions.*
