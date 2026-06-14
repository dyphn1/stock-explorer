# 🔥 Three-Round Challenge — Round 38

> **Date**: 2026-06-14
> **Challenger**: Challenger Agent
> **PM**: Product Manager
> **Context**: Review Round 38 — Sprint 17 Post-Mortem + Sprint 18 Prerequisites

---

## Round 1: Gap Authenticity Challenge

### Challenger Questions

**Q1: C147 (Historical Event Pattern) — Is this really a gap?**
The feature requires a historical event store that doesn't exist. We compute deltas on-the-fly. Isn't this a "build infrastructure first" feature rather than a genuine user-facing gap? Shouldn't we validate that users actually want historical patterns before building the infrastructure?

**PM Response**: C147 is a genuine gap but the Challenger is right about the infrastructure risk. The feature as described (14-18h) assumes the event store exists. Since it doesn't, the actual effort is 14-18h + infrastructure. This is why the Developer recommends a 2h spike first. **Revision**: C147 should be scoped as "Sprint 19 with 2h spike prerequisite" rather than a straight implementation. The gap is authentic (Spiking proves demand) but the implementation path needs de-risking.

**Q2: C152 (Multi-Factor Event Narratives) — Isn't this just C134 + C139 combined?**
C134 already explains individual metric changes. C139 explains individual metrics. C152 combines them into one narrative. But do users actually want a single narrative, or do they prefer individual explanations they can consume at their own pace? Isn't C152 solving a problem users don't have?

**PM Response**: Valid challenge. The competitor research shows Public.com and Spiking both provide single-story narratives, which validates demand. However, the Challenger raises a good point about consumption mode. **Revision**: C152 should include a "progressive disclosure" design — show the single narrative summary first, with expandable individual explanations below. This preserves both consumption modes. The gap is authentic but the design needs this dual-mode approach.

**Q3: C149 ("So What?" Implication Box) — Isn't this just C143 with better styling?**
C143 already generates implication sentences. C149 puts them in a styled box. Is this a separate feature or just a design enhancement to C143? Why is it in the pipeline as a separate item?

**PM Response**: The Challenger is partially right. C143 generates the content; C149 provides the visual treatment. However, they serve different purposes: C143 replaces delta card explanations (content change), while C149 adds a new visual element after metric sections (presentation change). **Revision**: C149 should be re-scoped as "C143 visual enhancement" and bundled with C143 in Sprint 18, not deferred to Sprint 19. The content and visual treatment should ship together for maximum impact.

**Q4: C148 (Metric Judgment Transparency) — Do we need to explain why something is "good" or "bad"?**
Our historian positioning is "explain what happened, not whether it's good or bad." C148 seems to contradict this by labeling metrics as good/bad and then explaining why. Isn't this a positioning violation?

**PM Response**: Strong challenge. C148 as described does risk contradicting the historian positioning. However, the competitor research shows users want to know "is this number high or low?" — they just want it framed factually. **Revision**: C148 should be reframed as "Metric Context" — instead of "this is good because..." it should be "this is higher than the industry average of X" or "this is in the top 25% historically." Factual context, not judgment. This aligns with the historian positioning.

### Round 1 Verdict
- ✅ C147 confirmed authentic (with spike prerequisite)
- ✅ C152 confirmed authentic (with progressive disclosure design)
- ✅ C149 confirmed authentic (but should bundle with C143, not defer)
- ✅ C148 confirmed authentic (but reframe as "Metric Context" not "Judgment")
- ✅ C150, C151, C153 confirmed authentic as-is

---

## Round 2: Priority Challenge

### Challenger Questions

**Q1: Sprint 18 has 23-28.5h of work. The hidden template audit adds 1.5h. D-074 and D-103 add 1.75h. Total: 26-31.5h. Is this too much for one sprint?**

**PM Response**: The total is at the upper bound of the PM's 22-31h range. However, the Challenger is right that this is tight. **Revision**: If the sprint is at capacity, Tone QA Automation (2.5h) can be deferred to Sprint 19. The critical path is D-074 → D-103 → D-097 → Template Audit → C139+C141 → C143. Tone QA automation is important but not blocking for C143 if the template audit is done manually first.

**Q2: C149 was moved from Sprint 19 to Sprint 18 (bundled with C143). Doesn't this make Sprint 18 even tighter?**

**PM Response**: C149 as a visual enhancement to C143 adds ~2-3h (the `_implication_box()` component + wiring into 3-4 locations). This is smaller than the original 10-14h estimate because the content already exists from C143. **Decision**: Include C149 in Sprint 18 as a stretch goal. If the sprint is on track after C143, add C149. If not, defer to Sprint 19.

**Q3: Should C147 (P1, 14-18h) displace C143 (P1, 7-9h) in priority? Both are P1.**

**PM Response**: No. C143 is a prerequisite for C149 and builds on C134 (Sprint 17). C147 requires a spike and new infrastructure. The right sequence is C143 (Sprint 18) → C147 spike (Sprint 19 start) → C147 implementation (Sprint 19). Both are P1 but C143 has lower risk and higher immediate user impact.

**Q4: The tone blocklist has 11 terms. Is this too aggressive? Will it block legitimate historian explanations?**

**PM Response**: The 11-term blocklist was expanded in Discussion Round 38 after the Challenger flagged advice-like language. The terms are: 建議, 應該, 買, 賣, 推薦, 進場, 出場, 值得關注, 需要密切關注, 值得持續追蹤, 表現優於預期. The Challenger is right that some of these could appear in legitimate historian contexts (e.g., "值得持續追蹤的趨勢" is factual, not advice). **Revision**: The blocklist should be context-aware. "值得關注" after a positive trend is advice-like. "值得持續追蹤的趨勢" as a factual observation is acceptable. The Tone QA test should check for sentence-level patterns, not just keyword matching.

### Round 2 Verdict
- ✅ Sprint 18 scope confirmed (Tone QA Automation deferrable if tight)
- ✅ C149 included as stretch goal
- ✅ C143 before C147 confirmed
- ✅ Tone blocklist needs context-aware implementation (not just keyword matching)

---

## Round 3: Goal Alignment Challenge

### Challenger Questions

**Q1: Sprint 18 is all about explanations (C139, C141, C143, D-097). The product vision says "Story first, data second." Are we building an explanation engine or a story engine? Is there a risk of becoming a "metric dictionary" instead of a "historian"?**

**PM Response**: This is the most important challenge of the round. The Challenger is right that there's a risk of over-indexing on metric-level explanations at the expense of narrative. However, the Sprint 18 features are building blocks: C139 explains individual metrics, C143 adds implication sentences that connect metrics to observations, and D-097 adds industry context. Together, these create the foundation for C152 (Multi-Factor Event Narratives) and C153 (Company Financial Story) in future sprints. **Mitigation**: The Sprint 18 features should be designed with narrative composition in mind. The `ExplanationResponse` protocol should support chaining (one explanation referencing another). This ensures Sprint 18 builds toward stories, not just isolated explanations.

**Q2: The tone blocklist approach — scanning for banned words — is crude. "表現優於預期" is banned, but "營收表現超出分析師預期" is the same meaning without the banned phrase. Can users game the blocklist? Can the blocklist be bypassed by rephrasing?**

**PM Response**: The Challenger is absolutely right. A keyword-based blocklist is trivially bypassed. "表現優於預期" → "表現比預期好" → "表現亮眼" — same meaning, no blocked words. **Revision**: The Tone QA approach needs to be:
1. **Keyword blocklist** as a first-pass filter (catches obvious violations)
2. **Pattern-based detection** for common advice structures ("建議...", "應該...", "可以考慮...")
3. **Human review gate** for all implication sentence templates (C143 content must be reviewed by a human before shipping)
4. **The blocklist is a safety net, not the primary quality gate**

This is a 3-layer approach: automated keyword check → pattern detection → human review.

**Q3: C147 (Historical Event Pattern) could be seen as predictive. "When this happened before, the stock went up 5%" — that's implicitly predictive. How do we keep this historian-aligned?**

**PM Response**: Critical concern. The framing must be strictly historical: "When revenue grew >20% in Q3 before (2019, 2021), the stock price changed by +5% and -2% in the following quarter." This is factual reporting of what happened, not "the stock will go up 5%." The key is:
- Always show the range of outcomes, not just the average
- Use past tense exclusively
- Include the sample size ("in 2 out of 3 cases...")
- Add a historian disclaimer: "歷史表現不代表未來走勢"

C147's tone QA must be even stricter than C143's.

### Round 3 Verdict
- ✅ Sprint 18 features are building blocks toward narrative (C152/C153), not isolated explanations
- ✅ Tone QA must be 3-layer (keyword + pattern + human review), not just keyword blocklist
- ✅ C147 must use strict historical framing with range-of-outcomes and historian disclaimer
- ✅ ExplanationResponse protocol should support chaining for future narrative composition

---

## Final Challenger Verdict

### ✅ CONFIRMED with 6 conditions:

1. **C147 requires a 2h feasibility spike** before committing to implementation (infrastructure risk)
2. **C149 bundles with C143** in Sprint 18 as a stretch goal (content + visual together)
3. **C148 reframes as "Metric Context"** (factual comparisons, not good/bad judgments)
4. **Tone QA is 3-layer**: keyword blocklist + pattern detection + human review gate for C143 content
5. **C147 uses strict historical framing**: range of outcomes, past tense, sample size, historian disclaimer
6. **Tone QA Automation (2.5h) is deferrable** to Sprint 19 if Sprint 18 is at capacity

### Sprint 18 Final Plan (Post-Challenge)

| Order | Task | Estimate | Notes |
|-------|------|----------|-------|
| 1 | D-074 filelock fix | 0.25h | Day 1 mandatory |
| 2 | D-103 DeltaExplanationProvider tests | 1.5h | Early sprint |
| 3 | D-097 Industry context threading | 1.5h | Protocol extension |
| 4 | Template audit + rewrite | 1.5h | Tone blocklist compliance |
| 5 | C139 + C141 Explain This Number + Source Badge | 10-13h | Core Sprint 18 deliverable |
| 6 | C143 + C149 Implication Sentence + "So What?" Box | 9-12h | Content + visual together |
| 7 | Tone QA Automation | 2.5h | Deferrable if at capacity |
| | **Total (with C149, without Tone QA)** | **24-29.5h** | |
| | **Total (with Tone QA)** | **26.5-32h** | Upper bound |

### Pipeline (Post-Challenge)

| Sprint | Features | Effort |
|--------|----------|--------|
| **Sprint 18** | C139 + C141 + C143 + C149 + D-097 + Tone QA | 24-32h |
| **Sprint 19** | C147 (with 2h spike) + C152 spike + C140 content | 34-42h |
| **Sprint 20** | C152 + C142 + C146 | 33-43h |

---

*Challenge completed: 2026-06-14*
*Challenger: ✅ CONFIRMED with 6 conditions*
*Next: 🔧 Development Round 39 (Sprint 18 execution)*
