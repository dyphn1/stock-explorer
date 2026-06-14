# Handoff – Discussion Round 46

## Summary
- **Topic**: 💡 Discussion (Round 46 — 2026-06-15)
- **Date**: 2026-06-15
- **Participants**: Product Manager, System Architect, Design Reviewer, Developer, Challenger
- **Sprint Status**: Sprint 20 ✅ → Sprint 21 in progress (C170 + C188 + D-125/126/127)
- **Challenger Verdict**: ✅ ALIGNED — 3 conditions (regulatory review gate, C201 performance budget, C201 content preparation)

---

## Idea Proposals

| Idea ID | Description | Source | Priority | Status |
|---------|-------------|--------|----------|--------|
| C199 | Bear vs Bull Visual Debate Cards | Competitor R46 (Simply Wall St) | P2 | Sprint 23 (SHOULD) |
| C200 | What If I Had Invested? Historical Calculator | Competitor R46 (Magnify.money, StockStory) | P2 | Sprint 23 (COULD) — C74 enhancement |
| C201 | Daily Market Story / 今日市場動態 | Competitor R46 (Finimize, Robinhood) — ELEVATED from C196 | **P1** | Sprint 22 MVP |
| C202 | Story Arc Timeline Labels | Competitor R46 (StockStory) | P2 | Sprint 23 (MUST) |
| C203 | Supply Chain Impact Visual Map | Competitor R46 (Spiking) | P2 | Sprint 24+ (deferred) |
| C204 | Confidence Indicator on AI Explanations | Competitor R46 (Spiking) | P2 | Sprint 21 stretch / Sprint 22 Day 1 |
| C205 | Read Time Indicator on All Content | Competitor R46 (Finimize, Robinhood) | P2 | Sprint 21 stretch / Sprint 22 Day 1 |
| C206 | Recurring Investment Concept Education | Competitor R46 (Robinhood) | P2 | Sprint 24+ (pending regulatory review) |

---

## Decisions Made

### Sprint 21 (Current — Extended)
- **Core**: C170 (Tappable Glossary) + C188 (Why Did This Stock Move?) + D-125/126/127
- **Stretch Goals**: C204 (Confidence Indicator, 4-6h) + C205 (Read Time, 3-5h)
  - If Sprint 21 core finishes early → start immediately
  - If not → move to Sprint 22 Day 1 (before C201)

### Sprint 22
- **C201 "今日市場動態" (Daily Market Story)** — P1 for growth
  - MVP scope: Template-based, on-demand generation, retrospective framing ("yesterday's news")
  - Renamed from "Daily Market Story" to "今日市場動態" to avoid naming collision with C202
  - Kill switch: If 7-day retention doesn't improve by Sprint 23 review, deprioritize
  - Daily caching pipeline deferred to Sprint 23

### Sprint 23 (MoSCoW Priority)
1. **C202 Story Arc Timeline Labels** (MUST, 10-14h) — Highest vision alignment
2. **C199 Bear vs Bull Debate Cards** (SHOULD, 10-14h)
3. **C200 What If Calculator** (COULD, 12-16h) — C74 enhancement, moves to Sprint 24 if capacity constrained

### Sprint 24+
- C206 Recurring Investment Education (pending regulatory review)
- C203 Supply Chain Visual Map (18-24h, data entry bottleneck)

### Feature Boundaries (Resolved Contradictions)
- C204 confidence indicators NOT applied to C201 bullets (template content ≠ analytical explanations)
- C205 read time NOT double-applied to C201 card (already has built-in read time)
- C201 and C202 have distinct naming: market-level daily briefing vs company-level historical narrative

---

## 3 Conditions (Must Be Met Before Sprint 22)

| Condition | Owner | Deadline |
|-----------|-------|----------|
| Regulatory review gate: Compliance review of C201 + C200 + C206 aggregate impression | PM + External advisor | Before Sprint 22 kickoff |
| C201 performance budget: 2-second timeout + cache strategy + mobile viewport test | Developer + Designer | During Sprint 22 development |
| C201 content preparation: 14-day template library + 10 fallback educational snippets | PM + Content | Before Sprint 22 content freeze |

---

## Action Items

| Item ID | Description | Owner | Sprint |
|---------|-------------|-------|--------|
| A46-01 | Add C204+C205 as Sprint 21 stretch goals in issues.md | PM | Sprint 21 |
| A46-02 | Rename C201 to "今日市場動態" in issues.md | PM | Sprint 21 |
| A46-03 | Note C200 = "C74 interactive upgrade" in issues.md | PM | Sprint 21 |
| A46-04 | Schedule regulatory review gate | PM | Before Sprint 22 |
| A46-05 | Prepare C201 14-day template library | PM + Content | Before Sprint 22 |
| A46-06 | Conduct mobile viewport test for C201 homepage placement | Designer | Sprint 22 dev |
| A46-07 | Implement C201 2-second timeout + cache strategy | Developer | Sprint 22 dev |

---

## Role Opinions Summary

### Architect
- **Top pick**: C201 (P1, highest retention impact) → C200 (proven engagement) → C204+C205 (quick wins)
- **Key concern**: Template-based explanations limit C201 narrative quality; phased delivery recommended
- **Not recommended near-term**: C199 (content heavy), C202 (needs real LLM), C203 (data bottleneck), C206 (low priority)

### Designer
- **Top pick**: C201 (P1, highest UX impact) → C204 (highest ROI, 4-6h) → C199 (visual differentiator)
- **Key concern**: Advisor boundary risk on C199/C200/C206; mobile responsiveness for C199/C203
- **Design risks**: D-003 regression (inline HTML), content quality, scope creep

### Developer
- **Top pick**: C204+C205 (quick wins, 7-11h, no deps) → C202 (low risk, high differentiation) → C199
- **Key concern**: C201 content curation cost outweighs code cost; C203 data entry is real bottleneck
- **Validated efforts**: All original estimates revised up by 2-4h except C204 (confirmed)

### Challenger
- **Round 1**: C201 historian alignment risk → resolved with retrospective framing; feature overlap resolved; P1 justified with phased delivery
- **Round 2**: C204+C205 moved to Sprint 21 stretch; C202 > C199 priority; Sprint 23 MoSCoW established
- **Round 3**: Dual-axis framework (vision vs growth); feature boundaries clarified; regulatory review gate added

---

## Next Cycle Handoff

**Next cycle**: 🔧 Development Round 47 — Sprint 21 execution (C170 + C188 + D-125/126/127 + C204/C205 stretch)
**Reference**: `docs/state/handoff.md` Development section for Sprint 21 plan

---

*Created: 2026-06-15 by PM*
*Source: docs/architecture/discuss_r46_architect.md, docs/design/discuss_r46_designer.md, docs/status/discuss_r46_developer.md, docs/state/challenge_r46.md*
