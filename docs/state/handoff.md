# Handoff – Development

## Summary
- **Topic**: Development (🔧)
- **Date**: 2026-06-12
- **Participants**: Product Manager, Developer
- **Theme**: C01 Ex-Dividend Countdown + Foundation Fixes (DR-01, D-059, gradients)

## Completed Items
| Issue ID | Description | Owner | Result |
|----------|-------------|-------|--------|
| ISSUE-C01 | Ex-dividend countdown + badge | Developer | ✅ Done — Commit `9cbdc73`. Countdown card ("⏳ 距離除息日還剩 N 天") added to business_card.py. History table upgraded to HTML with green "即將除息" / blue "已除息" badges. |
| DR-01 | Color system violations | Developer | ✅ Done — Commit `9cbdc73`. All `#F39C12` (orange) replaced with `#3498DB` across all files. Zero violations remaining. |
| D-059 | Orange border in `_info_card()` | Developer | ✅ Done — Commit `9cbdc73`. `_info_card()` border changed from `#F39C12` to `#3498DB`. |
| Gradient elimination | `linear-gradient` in 6 files | Developer | ✅ Done — Commit `9cbdc73`. All 7 gradient instances replaced with flat `#EBF5FB`. |
| ISSUE-D01 | M5 Event Detection Verification | Architect + Developer | ✅ Done (prior cycle) |
| ISSUE-D04 | M5 Pipeline Integration | Developer | ✅ Done (prior cycle) |
| ISSUE-D05 | DR-03 + C01 Financial Health Redesign | Developer | ✅ Done (prior cycle) |

## Key Findings
- **C16 "Did You Know?" already implemented**: `company_facts.py` service + `company_facts.yaml` (70 facts for 7 stocks) + UI in `business_card.py` lines 142-157. No work needed.
- **C01 fully complete**: Both the dividend story (D05) and countdown+badge (this cycle) are done. ISSUE-C01 can be marked ✅.
- **DR-01 fully complete**: All `#F39C12` and `linear-gradient` eliminated from `src/`. Design system compliance achieved.
- **L0**: 55/55 ✅ | **L1**: 15/15 ✅ (3 pre-existing event baseline failures)

## Pending Items
| Issue ID | Description | Owner | Next Steps |
|----------|-------------|-------|------------|
| ISSUE-C31 | Daily Financial Challenge | Dev | 7-10h, approved by Challenger Round 5 |
| ISSUE-C02 | Notification / Push System | Dev + Architect | Needs D02 background worker architecture |
| ISSUE-D02 | Background Worker Architecture | Architect | Blocker for C02 |
| ISSUE-C07 | Customizable Event Thresholds | Dev | Now unblocked — M5 verified ✅. ~10-14h |
| ISSUE-C04 | Market Thermometer | Dev | ~12-16h |
| ISSUE-C06 | Auto-Generate PPT | Dev | Depends on all pages at B+ |
| ISSUE-C14 | Health Score (Badge or Radar) | Dev | Needs Daniel decision on scope |
| ISSUE-DR-04 | Component inconsistency (inline HTML) | Dev | 2h |
| ISSUE-DR-05 | Responsive column layouts | Dev | 1.5h |

## Decisions Made
- **C01 fully complete**: Ex-dividend countdown + badge implemented. ISSUE-C01 status → ✅ Done.
- **C16 already done**: Was implemented in a prior cycle. No separate work needed.
- **DR-01 fully resolved**: All color violations fixed. Design system compliance is now enforced.
- **Next priority**: C31 Daily Financial Challenge (7-10h) — Challenger Round 5 "best new feature"
- **D02 (Background Worker)** remains blocker for C02 (Notifications)

## Next Cycle Handoff
Next theme: 💡 Discussion → read `docs/status/handoff_discuss.md`
Next dev cycle should tackle: C31 Daily Financial Challenge (7-10h)
# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡)
- **Date**: 2026-06-12
- **Participants**: Product Manager, System Architect, Developer, Design Reviewer, Challenger (timed out — PM synthesized)
- **Theme**: Feature Direction + Roadmap Round 6

## Idea Proposals
| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C01 | Ex-Dividend Countdown + Badge | Dev | Approved — 3-4h, finish partial work |
| C31 | Daily Financial Challenge | Dev | Approved — 7-10h, Challenger Round 5 "best new feature" |
| C16 | "Did You Know?" Company Facts | Dev | Approved — 4-5h, cheapest "Story first" feature |
| C07 | Customizable Event Thresholds | Dev + Architect | Deferred — 12-16h, too large for this cycle |
| C14 | Health Score (Badge or Radar) | Dev | Needs Daniel decision — Badge 4-6h or Radar 14-20h |
| C19 | Structured Learning Path | Dev | Deferred — 16-22h, needs C31 data first |
| C23 | "Why Now" Narrative Card | Dev | Deferred — 8-12h, content-heavy |
| C02 | Email Notifications | Dev | Blocked by D02 background worker |
| C04/C32 | Market Thermometer/Mood | Dev | Deferred — lower priority than engagement |
| C06 | PPT Generation | Dev | Phase 3 — 18-24h, needs all pages at B+ |

## Decisions Made
1. **Foundation fixes first** — D-059 (orange border fix, 5min) + chart.py color constants (30min) + gradient elimination (1h) = 1.5h total. These 3 fixes resolve ~15 of 71 design issues and raise every page by one partial grade.
2. **C01 is Sprint 1** — Ex-dividend countdown completes a partially-built feature. Uses existing dividend data pipeline. 3-4h.
3. **C16 is Sprint 2** — "Did You Know?" company facts. Cheapest "Story first" feature at 4-5h. Pure content, no API changes. Directly counters StockStory/Stockopedia AI threat with curated human-verified facts.
4. **C31 is Sprint 3** — Daily Financial Challenge. Challenger Round 5 approved as "best new feature." 7-10h. Key retention mechanism identified across all Round 5 competitors.
5. **C07 deferred to next cycle** — 12-16h is too large for current budget. It's a force multiplier but needs dedicated sprint.
6. **C14 scope decision needed from Daniel** — Badge (4-6h) vs Radar (14-20h). Design Reviewer recommends Badge given C- design grade.
7. **Analysis paralysis warning** — 5 review rounds produced 114 documented items but only ~4h actual implementation. This cycle prioritizes BUILDING over DOCUMENTING.

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| D-059 | Fix `_info_card()` orange border → `#3498DB` in `_router_base.py` | Dev | Next dev cycle |
| D-053-58 | Fix chart.py color constants (batch) | Dev | Next dev cycle |
| D-046+ | Eliminate gradients across 6 files | Dev | Next dev cycle |
| C01 | Ex-dividend countdown + badge on business_card.py | Dev | Next dev cycle |
| C16 | "Did You Know?" company facts (20-30 facts, top 10 stocks) | Dev | Next dev cycle |
| C31 | Daily Financial Challenge (20+ templates, streak tracking) | Dev | Next dev cycle |
| C14-scope | Daniel to decide: Badge (4-6h) or Radar (14-20h) | Daniel | Pending |

## Team Opinions Summary

### Architect (nemotron-120b)
- **Recommended order**: C01 → C31 → C16 → C07
- **Highest ROI**: C07 (force multiplier for all event-dependent features)
- **Key insight**: C07 transforms event detection from demo to real tool. Every event-dependent feature benefits.
- **Competitive threat**: StockStory and Stockopedia AI both have sophisticated event/alert systems; hardcoded thresholds make Stock Explorer feel rigid.
- **Build vs. defer**: C02 blocked by D02, C06 too expensive, C19 needs C31 data first, AI Q&A (C17) defer post-MVP

### Design Reviewer (gemma-31b)
- **Recommended order**: Foundation fixes (1.5h) → C14 Badge → C01 → C23
- **Key insight**: The gap between A- (Event Dashboard) and D (Category Browser/Group Structure) is almost entirely about shared component usage, color compliance, and PPT-style discipline
- **C14 recommendation**: Build simple Badge (4-6h), NOT Radar Chart (14-20h). Badge communicates in <1 second, radar requires 15-30s to interpret.
- **Pattern to replicate**: Event Dashboard's badge system, expandable detail, empty state handling, progressive disclosure
- **Anti-pattern**: Event Dashboard uses `linear-gradient` (D-035 violation) — copy structure but fix styling

### Developer (owl-alpha)
- **Recommended order**: C01 + C16 (Sprint 1, ~8h) → C14 + C32 (Sprint 2, ~12h) → C31 + C23 (Sprint 3, ~15h)
- **ROI ranking**: C16 (⭐⭐⭐⭐⭐) > C01 (⭐⭐⭐⭐⭐) > C14 (⭐⭐⭐⭐) > C32 (⭐⭐⭐⭐) > C31 (⭐⭐⭐) > C23 (⭐⭐⭐) > C07 (⭐⭐)
- **Key insight**: C01 + C16 for 15h budget = lowest risk, both touch business_card.py, both use existing data
- **Technical risks**: C06 (kaleido + Chinese fonts), C07 (cascading changes in adaptive_engine.py), C02 (blocked by D02)
- **Optimal sequence**: C01 → C16 → C14 → C32 → C31 → C23 → D02 → C07 → C19

## Final PM Decision (Post-Team-Synthesis)

| Order | Item | Hours | Core Value | Risk |
|-------|------|-------|------------|------|
| 1 | Foundation fixes (D-059, chart colors, gradients) | 1.5h | #2 PPT-style | Trivial |
| 2 | C01: Ex-dividend countdown + badge | 3-4h | Data completeness | Low |
| 3 | C16: "Did You Know?" company facts | 4-5h | #1 Story first | Low |
| 4 | C31: Daily Financial Challenge | 7-10h | #1 Story first, engagement | Medium |
| **Total** | | **15.5-20.5h** | | |

**Rationale**: This plan delivers foundation fixes (raising all pages), completes a partial feature (C01), adds the cheapest "Story first" feature (C16), and builds the Challenger-approved retention mechanism (C31). All features use existing data pipelines with zero new API calls. The plan avoids analysis paralysis by focusing on BUILDING over DOCUMENTING.

## Pending Daniel's Decision
See `docs/status/pending_review.md` for items requiring human input:
- #7: C14 Health Score scope — Badge (4-6h) or Full Radar (14-20h)?
- #8: Revised roadmap approval (this 4-item plan, 15.5-20.5h)
- #9: Category Browser + Group Structure structural redesign — include now or defer?

## Next Cycle Handoff
Next theme: 🔧 Development → read `docs/status/handoff_dev.md`
Next dev cycle should tackle: Foundation fixes → C01 → C16 → C31
# Handoff – Review

## Summary
- **Topic**: Review (🔍)
- **Date**: 2026-06-10
- **Participants**: Product Manager, Architect, Design Reviewer, QA Engineer, Developer, Challenger

## Competitor Research Findings
| Platform | Feature Gap | Suggested Improvement |
|----------|-------------|-----------------------|
| Yahoo Finance | Watchlist + notifications | C02 (notifications) |
| TradingView | Advanced charts | Improve chart interactivity |
| StatementDog | Plain-language explanations | Already matched |
| CMoney | AI stock picking | Differentiation — stay "historian" |
| WantGoo | PPT export | C06 (auto-generate PPT) |
| Simply Wall St | Visual stock education | Improve visual storytelling |
| Finviz | Screeners + heatmap | New feature opportunity |

## Decisions Made
- **DR-03 (Financial Health) promoted to P0** — worst-graded core page
- **TD-B01 (Rate Limit Visibility) promoted to P0** — silently swallowing errors
- **C06 (PPT Generation) moved to Phase 2/3** — fix pages first
- **C03 (Multi-Watchlist) confirmed Done** — reconciled status
- **Next Sprint priority**: D01 (4h) + TD-E01 (3h) + DR-03 (1.5h)

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| D01 | M5 Event Detection Verification | QA Engineer | Next dev cycle |
| D02 | Background Worker Architecture | Architect | Next dev cycle |
| TD-E01 | Event detection unit tests | Developer | Next dev cycle |
| DR-03 | Financial Health text reduction | Developer | Next dev cycle |
| DR-01 | Color system violations (6 files) | Developer | After DR-03 |

## Next Cycle Handoff
Next theme: 🔧 Development (pm-dev)
Read this file + issues.md + tech_debt.md to restore context.
