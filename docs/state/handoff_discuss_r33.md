# Handoff – Discussion (Round 33)

## Summary
- **Topic**: Discussion (💡) — Post-Sprint 15 Feature Planning: Health Score, Story Timeline, Explain Any Metric, Read Next, Notifications
- **Date**: 2026-06-14 (Round 33 Discussion completed)
- **Sprint Status**: Sprint 14 ✅ COMPLETE → Sprint 15 Planned → Sprint 16+ Confirmed
- **Participants**: Product Manager, System Architect, Developer, Designer, Challenger

## Key Discovery: Backlog Is Stale
The Developer's codebase review revealed that multiple features marked "📋 Todo" are already implemented:
- **C37 (Key Takeaways)** — `key_takeaways.py` + `key_takeaways.yaml` exist and are wired into `_sections/_summary.py` ✅ Already Done
- **C39 (What Changed Recently)** — `delta_engine.py` exists and is wired into `_sections/_story.py` ✅ Already Done
- **C36 (Revenue Tree)** — `revenue_tree.py` page exists with treemap visualization ✅ Already Done
- **C38 (Compare Stories)** — Both `compare_stories.py` service and page exist ✅ Already Done
- **C16 (Did You Know?)** — `company_facts.py` with 70 facts for 7 stocks, already wired ✅ Already Done

**Action**: Full backlog audit added to Sprint 15 scope.

## Team Proposals

### Architect Recommendation
- **Primary**: C14 Health Score + C45 Valuation Band "Company Snapshot" (10-14h, 🟢 HIGH feasibility)
- **Secondary**: C28 Story Timeline Spike (3-5h) → Full if spike succeeds
- **Tertiary**: C02 Notifications deferred to Sprint 16b+

### Designer Recommendation
- **#1**: C28 Company Story Timeline (20-30h) — "The #1 thing competitors DON'T have"
- **#2**: C29 Explain Any Metric (12-18h) — Fulfills "plain-language translations" design system requirement
- **#3**: C41 Read Next (6-8h) — Relationship-based discovery, leverages unique group structure data

### Developer Recommendation
- **P0**: C02 Notifications Phase 1A+1B (12-19h) — All competitors have it, M5 engine wasted without it
- **P1**: C28 Story Timeline (21-29h with spike) — Unique differentiator
- **P1**: C14 Health Score (11-17h Option B) — Scoring logic already built
- **P1**: C07 Custom Thresholds (6-9h) — Force multiplier for C02

## Challenger Verdict: ✅ CONFIRMED with 5 Revisions

### Revisions Required

| # | Revision | Impact |
|---|----------|--------|
| 1 | **Add C41 Phase A (2-3h) to Sprint 16a** | Reduces Sprint 17 load |
| 2 | **Add Business Card Page audit (D-005 remediation) as Sprint 16a prerequisite** | Prevents page overload |
| 3 | **Add C07 Custom Event Thresholds (6-9h) to Sprint 16b alongside C02** | Enables notification personalization |
| 4 | **Budget 40% content creation time for C28/C29** | Revised totals: 50-83h vs. 50-75h |
| 5 | **Define explicit C28 spike go/no-go criteria before Sprint 16b planning** | Risk mitigation |

### Round Summaries
- **Round 1 (Feature Direction)**: ✅ Passed — Role disagreements acknowledged (Architect: quick wins first, Designer: unique differentiator first, Developer: P0 gap first). Team consciously chooses unique differentiators over table-stakes for 1-2 sprints.
- **Round 2 (Priority)**: ✅ Passed — C14 estimate discrepancy resolved (Option A badge for Sprint 16a, Option B full radar for Sprint 17). C41 Phase A moved to Sprint 16a. Backlog audit added to Sprint 15.
- **Round 3 (Goal Alignment)**: ✅ Passed — C07 added to Sprint 16b. Content creation budgeted. D-005 audit added as prerequisite. C28 spike go/no-go criteria defined.

## Final Sprint 16+ Plan (Post-Challenger)

### Sprint 16a — Quick Wins + Validation (12-18h)
| Order | Item | Hours | Notes |
|-------|------|-------|-------|
| 0 | D-005 Business Card Page Audit | 1-2h | Prerequisite — collapse low-value sections |
| 0 | Backlog Audit | 1-2h | Mark stale issues as Done |
| 1 | C14 Health Score Badge (Option A) | 4-6h | Wire existing health_scoring.py to business card |
| 2 | C45 Valuation Band Chart | 3-4h | P/E vs 5-year historical range |
| 3 | C28 Story Timeline Spike | 3-5h | Validate events.yaml data richness |
| 4 | C41 Read Next Phase A | 2-3h | Peer group + parent-subsidiary only |
| **Total** | | **14-24h** | Including prerequisites |

### Sprint 16b — Big Bet (18-36h, conditional)
**If C28 spike passes:**
| Order | Item | Hours |
|-------|------|-------|
| 1 | C28 Company Story Timeline Full | 26-36h (incl. 40% content) |

**If C28 spike fails:**
| Order | Item | Hours |
|-------|------|-------|
| 1 | C02 Notifications Phase 1A+1B | 12-19h |
| 2 | C07 Custom Event Thresholds | 6-9h |

### Sprint 17 — Education + Discovery (20-29h)
| Order | Item | Hours |
|-------|------|-------|
| 1 | C29 Explain Any Metric | 17-25h (incl. 40% content) |
| 2 | C41 Read Next Phase B | 3-4h |
| 3 | C14 Health Score Full Radar (Option B) | 4-6h (coding only, content in C29) |

### Strategic Trade-off Acknowledged
The team consciously defers C02 Notifications (P0 gap) by 1-2 sprints in favor of unique differentiators (C28 Story Timeline, C29 Explain Any Metric). This is valid because:
1. Stock Explorer's "historian" positioning is better served by narrative features
2. C02 pull-on-visit model is a compromise; true push requires D02 resolution
3. Competitors are converging on AI narratives (StockStory 2025, Stockopedia AI 2025), making C28 time-sensitive

**Maximum deferral for C02: 2 sprints** (must ship by Sprint 17 end).

## Idea Proposals

| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C14 | Company Health Score — 5-axis visual radar | Architect | Accepted (Sprint 16a badge → Sprint 17 full) |
| C45 | Valuation Band Chart — P/E vs 5-year range | Architect | Accepted (Sprint 16a) |
| C28 | Company Story Timeline — narrative turning points | Designer | Accepted (Sprint 16a spike → 16b full) |
| C29 | Explain Any Metric — ℹ️ icons for 30+ metrics | Designer | Accepted (Sprint 17) |
| C41 | Read Next Recommendations — relationship-based | Designer | Accepted (Sprint 16a Phase A → 17 Phase B) |
| C02 | Notifications System — email + pull-on-visit | Developer | Accepted (Sprint 16b if C28 spike fails) |
| C07 | Custom Event Thresholds — parameterize detection | Developer | Accepted (Sprint 16b if C28 spike fails) |

## Decisions Made
1. **Backlog audit is P0** — Sprint 15 will include a full audit of all 47 issues to identify stale entries
2. **C14 Health Score uses phased approach** — Option A (badge, 4-6h) for Sprint 16a, Option B (full radar, 11-17h) for Sprint 17
3. **C28 Story Timeline uses spike-first de-risking** — 3-5h spike validates events.yaml data richness before committing 26-36h
4. **C02 Notifications deferred conditionally** — Only if C28 spike succeeds; otherwise C02+C07 ships in Sprint 16b
5. **Content creation budgeted at 40%** — Per handoff rules, education features (C28, C29) include content creation time
6. **D-005 remediation is prerequisite** — Business card page audit before adding 3 new sections

## Action Items

| Item ID | Description | Owner | Due |
|---------|-------------|-------|-----|
| A1 | Conduct full backlog audit (mark stale issues Done) | Developer | Sprint 15 |
| A2 | Audit business card page for D-005 overload | Designer | Sprint 15/16a Day 0 |
| A3 | C14 Health Score Badge — wire to business card | Developer | Sprint 16a |
| A4 | C45 Valuation Band Chart | Developer | Sprint 16a |
| A5 | C28 Story Timeline Spike — validate events data | Developer + Designer | Sprint 16a |
| A6 | C41 Read Next Phase A — peer + parent-subsidiary | Developer | Sprint 16a |
| A7 | C28 Full OR C02+C07 (conditional on spike) | Developer | Sprint 16b |
| A8 | C29 Explain Any Metric — ℹ️ icons + templates | Developer + Designer | Sprint 17 |
| A9 | C41 Phase B — customer-supplier mappings | Developer | Sprint 17 |
| A10 | C14 Health Score Full Radar (Option B) | Developer | Sprint 17 |

## Next Cycle
✅ Discussion Round 33 Complete → 🔧 Development Round 34 (Sprint 15: D6 YAML → chart.py split → CI check → C101) → 🔧 Development Round 35 (Sprint 16a: C14 + C45 + C28 spike + C41) → 🔍 Review Round 34

## Analysis Files
- **Architect analysis**: docs/design/architect_discussion_r33.md
- **Designer analysis**: docs/design/designer_discussion_r33.md
- **Developer estimate**: docs/design/developer_discussion_r33.md
- **Challenge log**: docs/design/challenge_r33.md
