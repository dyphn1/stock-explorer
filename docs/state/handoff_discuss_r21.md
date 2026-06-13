# Handoff – Discussion (Round 21)

## Summary
- **Topic**: Discussion (💡) — Sprint 12 Scope Validation + Post-Sprint 12 Roadmap
- **Date**: 2026-06-16 (Round 21 Discussion completed)
- **Sprint Status**: Sprint 11 ✅ COMPLETE → Sprint 12 revised → Sprint 13-14 updated

## Team Proposals

### Architect Recommendation
- Sprint 12: QA (6-10h) + Info Hierarchy (8-12h) + C40 Mode Toggle (10-16h) + User Feedback (2-4h) = 26-42h
- Post-Sprint 12: Direction B (C02+C33, 12-20h) → Direction A (C36+C46, 26-34h) → Direction C (C47, 22-32h)
- C47 should reuse existing services: analogy_engine, metric_education, quiz_engine, health_scoring

### Designer Recommendation
- Sprint 12: QA + Info Hierarchy + User Feedback. **Defer C40** — "beginner by default" + progressive disclosure achieves 80% of benefit
- Info Hierarchy above-fold = C37+C39+C43 only (720px budget = 3 cards)
- Post-Sprint 12: **C48 Story Card (8-12h) #1 priority** → C56 Explain This Metric → C42 Screener → C46 Moat

### Developer Estimate
- Sprint 12: 24-44h (midpoint 34h). Upper bound exceeds 38h budget
- Info Hierarchy + C40 = 18-32h combined block (coupling makes them effectively one item)
- C40 scope must be locked: conditional rendering only, no text simplification
- Top 3 post-Sprint 12: C33 Glossary (8-14h), C46 Moat (14-20h), C36 Revenue Tree (12-18h)
- Hidden complexity: C40 permanent maintenance tax, C02 blocked by D02 investigation

## Challenger Verdict: ✅ CONFIRMED (with 4 revisions)

### Round 1 — Feature Direction: ❌ Need Revision
- C02 Notifications (P0) deprioritized despite all competitors having it
- C40 was previously cut; Designer recommends deferral; Developer flags 🔴 High risk
- C48 Story Card and C56 Explain This Metric ignored in team consensus
- Sprint 12 upper bound exceeds 38h budget

### Round 2 — Priority: ❌ Need Revision
- Architect vs Designer post-Sprint 12 top-3 have ZERO overlap (unresolved split)
- Info Hierarchy section ordering disagreement (Developer's Tier 1 ≠ Designer's above-fold)
- C02's D02 architecture dependency uninvestigated
- C40 permanent per-feature maintenance tax on future sprints

### Round 3 — Goal Alignment: ✅ Passed
- Sprint 12 is directionally sound after C40 removal
- C46 Moat + C36 Revenue Tree are excellent historian features
- "Sacrifice completeness for clarity" principle supports C40 deferral

### 4 Required Revisions

| # | Revision | Impact |
|---|----------|--------|
| 1 | **Defer C40 Mode Toggle to Sprint 13** | Sprint 12 becomes 13-26h (healthy scope). C40 gated on Info Hierarchy completion. |
| 2 | **Add C48 Story Card to Sprint 13a** | Designer's #1 UX priority, directly targets ten-second test, 8-12h, alongside C33 Glossary |
| 3 | **Relocate C36/C38 off Business Card page** | Must happen before/during Info Hierarchy. Reduces page from 18→~10 sections. |
| 4 | **Investigate D02 (background worker) in Sprint 12** | C02 is P0 but has hidden architecture blocker. 2-4h spike during lighter Sprint 12. |

## Final Sprint Plans (Post-Challenger)

### Sprint 12 — Polish + Foundation (13-26h → well within budget)
| Item | Hours | Notes |
|------|-------|-------|
| C37/C39/C43/C45 QA | 3-8h | Historian tone gate + design compliance |
| Info Hierarchy (3-tier) | 8-14h | Above-fold = C37+C39+C43; relocate C36/C38 off page |
| User Feedback | 2-4h | Binary 👍/👎 + JSONL storage |
| D02 Architecture Spike | 2-4h | Background worker investigation for C02 |
| **TOTAL** | **15-30h** | Healthy scope with margin |

### Sprint 13a — Engagement + Infrastructure (16-26h)
| Item | Hours | Notes |
|------|-------|-------|
| C33 Glossary/Tooltips | 8-14h | 50-100 terms, ℹ️ icons on all pages |
| C48 Story Card | 8-12h | 30-second visual summary, ten-second test |
| **TOTAL** | **16-26h** | |

### Sprint 13b — Historian Deep Dive (26-38h)
| Item | Hours | Notes |
|------|-------|-------|
| C46 Moat Analysis | 14-20h | 5-dimension scoring, manual curation top-20 |
| C36 Revenue Tree | 12-18h | Plotly treemap, FinMind segment data |
| **TOTAL** | **26-38h** | |

### Sprint 14 — Education Platform (22-32h)
| Item | Hours | Notes |
|------|-------|-------|
| C47 Education Academy | 22-32h | 7 lessons, scaffold + content, reuse existing services |
| C40 Mode Toggle | 10-16h | Deferred from Sprint 12, gated on Info Hierarchy |
| **TOTAL** | **32-48h** | Split into 2a/2b if needed |

## Action Items

| Item ID | Description | Owner | Due |
|---------|-------------|-------|-----|
| R21-01 | C40 deferred to Sprint 13 — update Sprint 12 plan | PM | Sprint 12 Day 1 |
| R21-02 | C48 Story Card added to Sprint 13a sprint plan | PM | Sprint 13 planning |
| R21-03 | C36/C38 relocation off Business Card page | Dev + Designer | Sprint 12 (with Info Hierarchy) |
| R21-04 | D02 background worker spike (2-4h) | Architect | Sprint 12 |
| R21-05 | Info Hierarchy section order: above-fold = C37+C39+C43 | Designer + Dev | Sprint 12 Day 1 |
| R21-06 | C47 content creation starts (4 lessons parallel to Sprint 12-13) | Designer | Sprint 12 |

## Revised Total: ~89-122h across 4 sprints (was 76-106h across 3)

### Key Risks Identified
1. **C40 permanent maintenance tax**: Every future feature must tag beginner/expert — ongoing overhead
2. **C36/C46 content bottleneck**: 19-27h pure content creation — needs dedicated owner + timeline
3. **C02 architecture dependency**: D02 investigation must complete before Sprint 13 ambitions
4. **Sprint 13b aggressiveness**: 26-38h for C36+C46 simultaneously; if content lags, C36 is the cut candidate
5. **Business Card page at 18+ sections**: C36/C38 relocation is prerequisite, not optional

## Analysis Files
- **Architect analysis**: docs/design/architect_discussion_r21.md
- **Designer analysis**: docs/design/designer_discussion_r21.md
- **Developer analysis**: docs/design/developer_discussion_r21.md
- **Challenge log**: docs/design/challenge_r21.md

## Next Cycle
✅ Sprint 12 completed (Info Hierarchy + User Feedback + 8 debt items) → 🔍 Review Round 26 → Sprint 13a (C33 Glossary + C48 Story Card)
