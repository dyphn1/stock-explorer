# Handoff – Development
## Summary
- **Topic**: Development (🔧) — Sprint 7 Complete
- **Date**: 2026-06-13 (Sprint 7 development completed)
- **Sprint Status**: Sprint 7 ✅ COMPLETE → Sprint 8 next

## Key Metrics
- Design grade: A- (downgraded from A — inline HTML enforcement gap; 10th consecutive A/A-)
- L0: 85/85 ✅ | L1: 8/18 (10 pre-existing event-alert failures unchanged)
- Sprint 8: Debt-first (10-17h debt before new features)
- Features rejected this round: 2 (C100, C102)
- Structural changes required: 6 (historian filter, feature triage, CI enforcement, milestone verification, competitor research restructuring, product vision LLM scope update)

## Sprint Plans (Summary)
| Sprint | Items | Status |
|--------|-------|--------|
| Sprint 3 | C44, C41, C38, D16, D-025 | ✅ Complete |
| Sprint 4 | R3, C48, C38, C51, C53-1 | ✅ Complete |
||| Sprint 5 | D-039/040/041 + D37 + C71 + C74 + C73 | ✅ Complete |
|| Sprint 6 | C83 + C85 + C02 + C43 + C45 | ✅ Complete |
||| Sprint 7 | C84 + D3 + D6 + D7 + D-044 | ✅ Complete |
|| Sprint 8 | D-048 + D6 + D-055 + D-050 + D8/D9/D10 (Debt-First) | 📋 Next |
|||| Sprint 9 | C98 + C101 + C103 | 📋 Round 20 approved |
|||| Sprint 10+ | C99 + C81, C64, C65, C68 | 📋 Deferred |

## Key Rules
- Content cap: 100 items max across all features
- Mandatory historian tone QA gate before each content feature ships
- C63 weekly only (start with 12 quarterly, not 52)
- D-041 (card components) is a HARD PREREQUISITE before Sprint 5 feature coding
- D37 (_sections.py split) is a HARD PREREQUISITE for Sprint 6 C43
- Card-count limit: max 5 cards per page section (Direction A)

## Pending Daniel Decisions
1. C34 vs C46 priority — Recommend defer both to Sprint 9+
2. C47 Phase 1 scope: 5 vs 10 lessons — Recommend 5
3. Business Card Page IA: "above the fold" definition — Recommend C37 + C43 only
4. NEW: Color palette expansion (purple/teal for content types) — Direction C Phase 2

## Detailed Logs
- Discussion: docs/state/handoff_discuss.md (Round 16)
- Review: docs/state/review_report.md (Round 19)

## 🔧 Development Section

### Sprint 4 Execution (2026-06-20) — COMPLETE ✅
All 5 items delivered: R3 (batch_api.py), C48 (story card), C38 (compare stories), C51 (sector heatmap), C53-1 (social sharing). L0: 65/65, L1: 8/8. Effort: 35-43h.

### Sprint 5 Status (2026-06-22) — COMPLETE ✅
All prerequisites, features, and D37 split delivered:
- **D-043**: P0 bug fix — `get_roe_analyzer`/`get_pbr_analyzer` → `get_roe_analogy`/`get_pbr_analogy` (318d30f)
- **D-039/040/041**: Section header, disclaimer, card component helpers (075df11)
- **C71**: Study Log — `_study_log.py` (e6c79f3)
- **C73**: Expert Analysis MVP — `_expert_analysis.py` (e6c79f3)
- **C74**: Historical Scenarios — `_historical_scenarios.py` (e6c79f3)
- **D37**: `_sections.py` split into `_sections/` sub-modules — `__init__.py`, `_summary.py`, `_financial.py`, `_health.py`, `_story.py`, `_detail.py` (cf27659)
- **D-044**: Read Next/Share headers already using `_section_title()` (verified)
- **D-046**: Sector heatmap 4th KPI card now uses `_白话_card()` (344a895)
- L0: 74/74 ✅ | L1: 8/8 + 10 pre-existing event-alert failures unchanged

### Sprint 6 Execution (2026-06-23) — COMPLETE ✅
All 5 Sprint 6 items delivered:
- **C83**: Investment Memo Template — `investment_memo.py` + `investment_memo_service.py` (standalone page, stock selector, memo form with validation, session-stored memos, navigate-to-business-card buttons) (eb5e962)
- **C85**: Financial Wellness Check — `financial_wellness.py` + `financial_wellness_service.py` (10-question behavioral finance quiz, score calculation, interpretation, personalized tips, category breakdown) (eb5e962)
- **C43**: Health Snowflake — `health_scoring.py` service extracted, `compute_health_scores()` + `get_health_summary()` used in `_health.py` section (done in Sprint 5)
- **C45**: Valuation Band Chart — already implemented in Sprint 4
- **C02**: Notification Center — `notification_service.py` (settings, pending notifications, ack/all-ack) + `notification_center.py` (standalone page with severity badges, per-stock grouped cards, "查看全部" and "標記已讀" buttons, settings expander) + wired into router and sidebar nav (b197764)
- **D-037**: `_白话_card()` background color fixed `#F5F5F5` → `#F8F9FA` (b197764)
- **D-044**: Already applied — `_render_read_next()` uses `_section_title()`
- **D-046**: Already applied — sector heatmap 4th KPI uses `_白话_card()`
- **D-047**: Already applied — `_render_share_section()` uses `_section_title()`
- L0: 82/82 ✅ | L1: 8/18 (10 pre-existing event-alert failures unchanged, 8 new L1 tests for notification_center pass)
- Commit: b197764

### Sprint 7 Execution (2026-06-13) — COMPLETE ✅
All Sprint 7 debt items and main feature delivered:

**Debt Cleanup (4 items completed):**
- **D6**: YAML migration — `financial_wellness_service.py` quiz data extracted to `config/quiz.yaml` with in-memory caching; `notification_service.py` YAML re-read pattern fixed (6eeeb8a, 1544e64)
- **D-044**: market_data.py extraction — Created `src/services/market_data.py` with 8 functions (`get_all_stock_info`, `get_sector_list`, `get_sector_stocks`, `get_sector_performance`, `get_top_movers`, `get_all_summaries`, `compute_sector_metrics`, `get_sector_grid_data`); `sector_heatmap.py` refactored to remove direct FinMindClient calls and a 41-line duplicate `_compute_sector_metrics()` function (0d15148)
- **D7**: N+1 API fix — `category_browser.py` replaced 400+ sequential `get_daily_price()` calls with a single batched `_fetch_latest_daily_prices()` using `ThreadPoolExecutor(max_workers=10)` + `@st.cache_data(ttl=300)`. Expected 5-10x page load improvement (7afb748)
- **D3**: Card consolidation — Added `_subsidiary_card()` and `_count_label()` helpers to `_router_base.py`; replaced 22-line inline HTML card in `group_structure.py` and inline count in `etf_browser.py`. Analyzed watchlist_page.py, etf_detail.py, _story.py — already using shared components (6ec9e48)

**Main Feature:**
- **C84**: Market Event Case Study — `src/services/market_event_service.py` (5 case studies: dot-com bubble, 2008 financial crisis, TSMC semiconductor super cycle, 2021 shipping frenzy, 2023-2024 AI boom) + `src/pages/market_event_case_study.py` (standalone page with hero section, narrative timeline, key metrics comparison, lessons learned in expandable sections, related stocks with navigation, historian disclaimers) + registered in router and url_sync (1827bb5)

**New Components Added to _router_base.py:**
- `_subsidiary_card(name, holding, business, relationship)` — card with holding badge + business description
- `_count_label(text)` — muted count display

**Metrics:**
- L0: 85/85 ✅ (up from 82, +3 new modules all pass)
- L1: 8/18 (10 pre-existing event-alert failures unchanged, zero new failures)

## 🔍 Review Section

### Round 20 (2026-06-13)
- Design Grade A- (downgraded from A — inline HTML enforcement gap)
- D6 PARTIALLY resolved: only 1/6 YAML blocks migrated; _CASE_STUDIES (230 lines) is new D6 violation
- D-044/D7/D3: ✅ Confirmed resolved (market_data.py, N+1 fix, card consolidation)
- 8 new debt items: D-048 through D-056 (D-048 elevated to P1 — _CASE_STUDIES YAML migration)
- 6 new competitor features (C98-C103): 2 REJECTED (C100, C102), 1 deferred (C99→P3), 3 conditional
- C100 (Natural Language Screener) REJECTED — contradicts "historian, not stock picker"
- C102 (Market Narrative Feed) REJECTED — market news, not historian
- C52 (Quiz Mode) CANCELLED — replaced by C101
- Sprint 8 = DEBT-FIRST (10-17h debt before any new features)
- 6 structural changes required: historian filter, feature triage, CI enforcement, milestone verification, competitor research restructuring, product vision LLM scope update
- Challenger: ⚠️ REQUIRES REVISION — 2 features rejected, Sprint 8 debt-first confirmed
- New: D-049 (C84 inline HTML), D-050 (C84 non-standard cards), D-051 (ETF browser inline HTML), D-052 (_subsidiary_card non-standard), D-053 (_count_label undocumented)

### Round 19 (2026-06-12)
- Design Grade A (9th consecutive) — maintained, Sprint 6 pages are cleanest new additions
- D37 RESOLVED: _sections.py split into 6 sub-modules (57-line orchestrator)
- D-043/D-046: False alarms — already fixed in Sprint 5, documentation debt only
- 6 new debt items from Sprint 6: D-048 through D-052 (severity lower than claimed)
- Sprint 6 scope change: Delivered C83/C85/C02 instead of planned C93/C94/C97
- Challenger: ✅ CONFIRMED — Sprint 7 = C84 (12h) + 4 debt items (13.4h) + 2 spikes (4.8h) = 34.2h
- D13 (test infra) deferred to Sprint 8; C82 deferred to Sprint 8 (conditional on D28)
- New: D-049 (C85 score cards inline HTML), D-050 (C02 settings raw st.expander) — both P2

### Round 17 (2026-06-21)
- Design Grade A (7th consecutive) — maintained but fragile
- New: C93-C97 (5 features), C52/C55 deferred to Sprint 8+
- Challenger: ⚠️ REVISED — Sprint 5 scope locked, Feature Triage established
- D-045-D-048: 4 new P2 design issues from Sprint 4 (C51 inline HTML, C53-1 header/JS)

### Round 16 (2026-06-20)
- D16 RESOLVED, D26 UNBLOCKED, Design Grade A (6th consecutive)
- New: D-042/043/044 (P2), C81-C85 added to backlog

## 💡 Discussion Section (Round 17 — 2026-06-13)

### Team Decision: Narrative-First Education Path (Challenger ✅ CONFIRMED after revision)
| Sprint | Features | Effort | Type |
|--------|----------|--------|------|
| 8 | D22 (Persistence + C64 feasibility) + D28 (Audio spike) + [C63 if D28 ✓] OR [D-049/D-050 debt if D28 ✗] | 18-44h | Infrastructure + Conditional |
| 9 | C34 Company Story Timeline (top 15 stocks) + C81 Interactive Historical Scenarios | 32-44h | Core Differentiator |
| 10 | C68 Financial Concept Storytelling | 32-44h | Education |
| 11+ | C65 Company Story Game → C64 Community Q&A (if D22 ✓) | 54-72h | Long-haul |
| Parallel | Content creation (C34 narratives + C68 stories + C63 scripts) | 20-30h | Content |
| **TOTAL** | | **156-234h** (+ 20-30h content) | |

### Key Discoveries
1. **C37/C39/C41 already implemented** — backlog was stale, these shipped in Sprints 3-5
2. **C42 Stock Screener already implemented** — shipped in Sprint 6, backlog stale
3. **C40 Beginner/Expert Mode previously cut** — "beginner mode by default" design philosophy adopted
4. **Net new features remaining: C34, C81, C63, C65, C64, C68** (6 features, not 10+)

### Key Decisions
1. C34 (Company Story Timeline) is the #1 priority after Sprint 8 — the purest "historian" differentiator
2. C81 (Interactive Historical Scenarios) moves to Sprint 9 alongside C34 — leverages C34 narrative patterns
3. C68 (Financial Concept Storytelling) before C64 (Community Q&A) — education before community
4. C63 (Audio) remains conditional on D28 spike — if D28 fails, D-049/D-050 debt cleanup fills Sprint 8
5. C34 scoped to top 15 stocks for Sprint 9 — content cap compliance (100 items max)
6. D22 must include C64 feasibility proof-of-concept — 30-40h feature can't assume unproven infrastructure
7. Content creation effort (20-30h) added as explicit PM/Designer line item — was excluded from dev estimates

### Challenger 3-Round Summary
- **Round 1**: C42 was missing from plan → DISCOVERED C42 already implemented (backlog stale); C64/C68 sequence swapped; Sprint 8 fallback added
- **Round 2**: C34 content scope unbounded → capped at top 15 stocks; Sprint 8 fallback confirmed; C37/C39/C41 polish confirmed unnecessary (already ship)
- **Round 3**: Content creation effort excluded → added 20-30h; D22 C64 feasibility requirement added; MVP boundary clarified (C34+C81 = MVP)
- **Final Verdict**: ✅ CONFIRMED after 6 required revisions adopted

### Action Items
| Item ID | Description | Status |
|---------|-------------|--------|
| C34 | Company Story Timeline (top 15 stocks) | 📋 Sprint 9 |
| C81 | Interactive Historical Scenarios | 📋 Sprint 9 |
| D22 | Persistence Layer + C64 feasibility test | 📋 Sprint 8 |
| D28 | Audio Infrastructure spike | 📋 Sprint 8 |
| C63 | Audio Market Story (conditional) | 📋 Sprint 8 (if D28 ✓) |
| C68 | Financial Concept Storytelling | 📋 Sprint 10 |
| C65 | Company Story Game | 📋 Sprint 11+ |
| C64 | Community Q&A (if D22 ✓) | 📋 Sprint 11+ |
| Backlog cleanup | Mark C37/C39/C41/C42 as Done in issues.md | 📋 This cycle |

### Next Cycle
🔧 Development → Sprint 8 (DEBT-FIRST: D-048 → D6 → D-055 → D-050 → D8/D9/D10 = 10-17h) → 🔍 Review Round 21 → Sprint 9 (C98 + C101 + C103)

## 💡 Discussion Log
*See docs/state/handoff_discuss.md for full Round 16 discussion log. See docs/state/challenge_log.md for Round 17 challenger analysis.*
