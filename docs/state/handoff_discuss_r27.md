# Handoff – Discussion (Round 27)

## Summary
- **Topic**: Discussion (💡) — Sprint 13b Scope Validation (C46 Moat Analysis + C36 Revenue Tree)
- **Date**: 2026-06-18 (Round 27 Discussion completed)
- **Sprint Status**: Sprint 13a ✅ COMPLETE → Sprint 13b CONFIRMED

## Team Proposals

### Architect Recommendation
- **Option A (preferred):** C36 Revenue Tree V2 in Sprint 13b, C46 Moat Analysis in Sprint 13c
- Revenue Tree V2: 15-22h, lower risk (page already exists, proven data pattern)
- Moat Analysis: 19-28h, higher strategic value but riskier (new page, subjective content)
- Combined (Option C) exceeds sprint capacity at 29-41h
- Key insight: Revenue Tree page already exists with flat pie chart; upgrade path is clean YAML→treemap

### Designer Recommendation
- **C46 Moat Analysis first priority** (higher strategic value, no TW competitor has it)
- Placement: Below-fold expander on Business Card page
- Visual: 5 dimension mini-cards with green/yellow/red color coding
- C36 Revenue Tree: Pie chart default, treemap opt-in via toggle
- Combined effort: 20-26h fits one sprint

### Developer Estimate
- **C46 Moat Analysis: 17-22h** (Service: 4-5h, View: 4-5h, Data/curation: 8-10h, Integration: 1-2h)
- **C36 Revenue Tree: 12.5-17h** (Service: 3-4h, View: 3-4h, Data/curation: 5-7h, Integration: 1.5-2h)
- **Combined: 29.5-39h**, expected 34h fits 26-38h budget
- Primary risk: content creation (13-17h, 47% of total effort)
- Go/No-Go gate at Day 2 on curation progress

## Challenger Verdict: ✅ CONFIRMED (with 2 revisions)

### Revisions Required

| # | Revision | Impact |
|---|----------|--------|
| 1 | **C46 moat scoring rubric must be documented before curation** | Create `docs/design/moat_rubric.md` documenting score thresholds per dimension. Ensures consistency across 20 stocks. Effort: 0.5h pre-sprint. |
| 2 | **C36 must default to pie chart; treemap is opt-in** | Pie chart = default view (10-second test). Toggle to treemap for interested users. Business Card page integration preferred over standalone page. |

### Round Summaries
- **Round 1 (Feature Direction):** ✅ Passed — Both features align with historian positioning. Competitor gaps validated. C47 Education Academy deferred to Sprint 14 (too large for Sprint 13b).
- **Round 2 (Priority):** ✅ Passed — C36 first (pattern establishment), then C46. Go/no-go gate at Day 2. Sprint 14 C47 not at risk.
- **Round 3 (Goal Alignment):** ✅ Passed — Content creation cost is unavoidable for expert-level historian features. Progressive disclosure handles page growth. No overlooked risks.

## Final Sprint 13b Plan (Post-Challenger)

### Sprint 13b — Business Understanding Duo (29.5-38h expected)

| Item | Hours | Order | Notes |
|------|-------|-------|-------|
| C36 Revenue Tree V2 | 12.5-17h | 1st | Treemap toggle on Business Card, segment-level for all stocks via FinMind, hierarchical YAML for top 20 |
| C46 Moat Analysis | 17-22h | 2nd | 5-dimension expander on Business Card, manual curation top 20, template scoring for all |
| **TOTAL** | **29.5-39h** | | Expected 34h, fits 26-38h budget |

### Day 2 Go/No-Go Gate
- If < 12 stocks curated across both YAML files → activate Option 2 (reduce to 12 stocks total)
- Option 2 revised total: 24-29h (comfortable fit)

### Fallback (Option 2)
- C36: Segment-level only (no customer-level Level 3)
- C46: 12 stocks manual curation, template for remaining 8

## Key Risks
1. **Content creation overrun** (13-17h): Both features need manual curation. Start Day 1.
2. **Moat subjectivity**: Mitigated by scoring rubric (revision #1) and historical evidence anchor
3. **Treemap beginner confusion**: Mitigated by pie-chart-default toggle (revision #2)
4. **Business Card page length**: Both features below-fold in expanders, progressive disclosure handles growth

## Action Items

| Item ID | Description | Owner | Due |
|---------|-------------|-------|-----|
| R27-01 | Create `docs/design/moat_rubric.md` scoring rubric | Designer | Sprint 13b Day 1 |
| R27-02 | Begin C36 `revenue_tree_data.yaml` curation (20 stocks) | Dev | Sprint 13b Day 1 |
| R27-03 | Begin C46 `moat_data.yaml` curation (20 stocks) | Dev | Sprint 13b Day 1 |
| R27-04 | Build C36 service layer (`revenue_tree.py` service + treemap chart) | Dev | Sprint 13b Day 2-3 |
| R27-05 | Build C46 service layer (`moat_analyzer.py`) | Dev | Sprint 13b Day 3-4 |
| R27-06 | Day 2 Go/No-Go: check curation progress (≥12 stocks?) | PM | Sprint 13b Day 2 |
| R27-07 | Build C36 view (pie chart default + treemap toggle) | Dev | Sprint 13b Day 4-5 |
| R27-08 | Build C46 view (5-dimension expander on Business Card) | Dev | Sprint 13b Day 5-6 |
| R27-09 | Integration, tests, L0/L1 verification | Dev | Sprint 13b Day 6-7 |
| R27-10 | C47 Education Academy content creation begins (parallel) | Designer | Sprint 13b (non-blocking) |

## Next Cycle
✅ Sprint 13b planned (C36 + C46) → 🔧 Development Sprint 13b → Sprint 14 (C47 Education Academy + C40 Mode Toggle) or 🔍 Review Round 28

## Analysis Files
- **Architect analysis:** docs/design/architect_discussion_r27.md
- **Designer analysis:** docs/design/designer_discussion_r27.md
- **Developer estimate:** docs/design/developer_discussion_r27.md
- **Challenge log:** docs/design/challenge_r27.md
