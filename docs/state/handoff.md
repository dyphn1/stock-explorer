# Handoff — Stock Explorer

## Summary
- **Topic**: 💡 Sprint 25 Planning — Round 50 Discussion Complete
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 24 ✅ COMPLETE → Sprint 25 📋 PLANNING

---

# 🚀 Sprint 24 — COMPLETE ✅

## Sprint 24 Deliverables

| Priority | Feature | Effort | Risk | Status |
|----------|---------|--------|------|--------|
| DONE | C201 今日市場動態 (daily market dashboard) | 6-8h | Low | ✅ COMPLETE |
| DONE | Design system color compliance (Round 7 fixes) | 2-3h | Low | ✅ COMPLETE |
| DEFERRED | C206 Recurring Investment Education | 6-8h | Low | → Sprint 25 |

## C201 Daily Market Dashboard — COMPLETE ✅

**Architecture design**: `docs/architecture/c201_daily_market.md` (714 lines)
**Page key**: `daily_market`
**Commit**: `ad5b46c` — feat(c201): Daily Market Dashboard implementation + i18n keys + tests

**Files created/modified**:
- NEW: `src/pages/daily_market.py` (300 lines)
- NEW: `tests/test_daily_market.py` (591 lines)
- MODIFY: `src/pages/router.py` (import + route already present)
- MODIFY: `locales/en.yaml` + `locales/zh-TW.yaml` (~50 new keys)
- MODIFY: `src/pages/url_sync.py` (already had "今日市場動態" in VALID_PAGES)

**Test coverage**: 662 tests pass (up from 545)

## Design System Cleanup — COMPLETE ✅

**Commit**: `2fc60d3` — fix(design-system): fix color violations across shared components and chart services

**Files changed**: 4 files, 14 insertions, 22 deletions

| File | Fixes |
|------|-------|
| `src/pages/_router_base.py` | `_summary_card()` border, `_section_title()` emoji detection, `_mini_score_card()` amber, `_白话_card()` background, `_subsidiary_card()` text, `_glossary_annotated_metric()` text |
| `src/services/chart_stock_financial.py` | Pie chart Set3 palette → explicit colors, treemap colors |
| `src/services/chart_stock_health.py` | `_score_color()` medium tier, pass-line color |
| `src/services/_chart_theme.py` | Stale color comments |

**Issues fixed**: D-005, D-059, D-063-D-083 (30+ design system violations)

# 📋 Sprint 25 Plan (2026-06-17)

## Sprint 25 Candidates

| Priority | Feature | Effort | Risk | Status |
|----------|---------|--------|------|--------|
| MUST | Pre-sprint fixes (colors + tech debt + API abuse) | 3-4h | Low | ⏳ Week 1 Day 1-2 |
| MUST | C209 Collapsible Source Transparency (3 pages) | 4-6h | Low | ⏳ Pending |
| SHOULD | C203 Company Ecosystem Cards v1 (8 companies) | 10-12h | Medium | ⏳ Pending Daniel |
| SHOULD | C206 Recurring Investment Education (1 lesson) | 6-8h | Low | ⏳ Pending Daniel |
| **Total** | | **23-30h** | | |

## Pre-Sprint Fixes (Week 1 Day 1-2) — MUST

| Fix | Effort | Impact |
|-----|--------|--------|
| 8 non-palette color fixes in `_router_base.py` | 10 min | Global — all pages |
| Rename `validate_debate_text()` → `contains_banned_words()` | 5 min | Code clarity |
| Move timeline strings from `scenario:` to `timeline:` namespace | 15 min | i18n consistency |
| Remove dead `calculate_scenario` import | 5 min | Dead code cleanup |
| Fix API abuse in `get_stock_info` | 1-2h | Prevents rate limits for C203 |

## C209 Collapsible Source Transparency — MUST

**Scope**: 3 pages for v1 (business_card, daily_market, event_dashboard)
**New component**: `_source_section()` in `_router_base.py`
**Pattern**: `st.expander("📡 資料來源", expanded=False)` — collapsed by default
**Effort**: 4-6h

## C203 Company Ecosystem Cards v1 — SHOULD (Pending Daniel)

**Scope**: 8 companies (existing 5 + 3 new), parent-subsidiary + 2-3 customer-supplier pairs
**Reuse**: `_subsidiary_card()` — no new component needed
**New files**: `ecosystem_service.py` + `ecosystem_cards.py`
**Effort**: 10-12h
**Gate**: Daniel approval required

## C206 Recurring Investment Education — SHOULD (Pending Daniel)

**Scope**: Single DCA lesson, hypothetical data only, NO calculator, NO real stock examples
**Reuse**: `_lesson_card()` + `_progress_dots()` + `_existing academy infrastructure`
**Effort**: 6-8h
**Gate**: Daniel scope confirmation; default to single lesson if no response

## Fallback Plan (if Daniel doesn't approve C203)
- C209 expands to all pages (7-9h) → MUST
- C206 elevates to MUST (6-8h)

---

# 🚀 Sprint 23 — COMPLETE ✅

## Sprint 23 — COMPLETE ✅

### Shipped Features

| Feature | Files | Tests | Status |
|---------|-------|-------|--------|
| C202 Story Arc Labels | `story_arc_detector.py` (228 lines) | 327 lines | ✅ Complete |
| C199 Bear vs Bull Debate Cards | `debate_engine.py` (196 lines), `debate_cards.py` (201 lines) | 388 lines | ✅ Complete |
| C200 What If Calculator | `scenario_calculator.py` (374 lines) | 484 lines | ✅ Complete |

### i18n Cleanup — COMPLETE ✅

| File | Issue | Fix |
|------|-------|-----|
| `story_arc_detector.py` | `_bucket_label()` returned hardcoded Chinese | Now returns i18n keys |
| `_historical_scenarios.py` | All scenario content hardcoded Chinese | Moved to locale files, uses `t()` |
| `investor_story_feed.py` | All display strings hardcoded Chinese | Wrapped with `t()` calls |
| `debate_engine.py` | Banned words filter defined but never called | Integrated into `debate_cards.py` rendering |
| `src/core/locales/` | Dead code directory with incompatible schema | Deleted entirely |
| `story_arcs.yaml` | Display strings in config file | Moved to locale YAML files |

### Commits

| Commit | Description |
|--------|-------------|
| `2fc60d3` | fix(design-system): fix color violations across shared components and chart services |
| `ad5b46c` | feat(c201): Daily Market Dashboard implementation + i18n keys + tests |
| `2d1f96b` | feat(discussion): Round 49 Sprint 24 planning — C201 ready, C203/C209 redefined |
| `cfb342f` | fix(debate): integrate banned words filter into debate card rendering |
| `d27f58d` | refactor(i18n): clean up hardcoded Chinese in service and page layers |
| `6cd766f` | fix(review): Sprint 23 quality review fixes — broken import, missing i18n keys, hardcoded Chinese |
| `f29c511` | feat(sprint23): C199 debate engine + C200 scenario calculator + test fixes |
| `d55452d` | refactor(i18n): Sprint 23 story_arc keys + detector i18n refactoring |
| `cfded35` | feat(discussion): Round 48 Sprint 23 planning - i18n conflict resolution + challenge |
| `7bcbc00` | feat(i18n): complete i18n integration across all pages and services |

## Test Health
- **662 passed** in 3.81s — all tests green
- No regressions introduced

## Remaining Tech Debt (Non-blocking)

| Issue | Severity | Location |
|-------|----------|----------|
| Design system compliance: 50+ issues remaining (grade C+) | 🟡 Medium | `docs/state/current_problems.md` |
| `validate_debate_text()` naming counterintuitive | 🟢 Low | `src/services/debate_engine.py` |
| Timeline strings in `scenario:` namespace | 🟢 Low | `locales/*.yaml` |
| Dead import in `_historical_scenarios.py` | 🟢 Low | `src/pages/business_card/_historical_scenarios.py` |

---

# 📋 Development Section — Sprint 25

## Next Steps

1. **Pre-sprint fixes (Week 1 Day 1-2)** — 8 color fixes + 3 tech debt + API abuse fix
2. **C209 Collapsible Source** — Create `_source_section()`, integrate into 3 pages
3. **C203 Ecosystem Cards** — If Daniel approves, expand data + create service + page
4. **C206 Education Lesson** — Single DCA lesson in academy
5. **Fresh design audit** — Verify actual open issue count

## Pre-Conditions — ALL RESOLVED ✅

| Condition | Status |
|-----------|--------|
| Fix broken `_is_etf_check` import | ✅ DONE (Sprint 23 review) |
| Add missing i18n keys | ✅ DONE (Sprint 23 review) |
| Fix `scenario.future_date` wrong English text | ✅ DONE (Sprint 23 review) |
| Replace hardcoded Chinese in `debate_cards.py` | ✅ DONE (Sprint 23 review) |
| Verify all tests pass | ✅ DONE (662/662) |
| i18n tech debt cleanup | ✅ DONE (Round 48) |
| Delete `src/core/locales/` | ✅ DONE (Round 48) |
| Refactor `story_arc_detector.py` to return keys | ✅ DONE (Round 48) |
| Implement four-safeguard pattern for C199 | ✅ DONE (Round 48) |
| Validate FinMind API data completeness | ✅ DONE (Round 48) |
| Resolve C201 open questions (TAIEX, volume, events) | ✅ DONE (Round 49) |
| C203/C209 evaluation and redesign | ✅ DONE (Round 49) |
| C201 implementation | ✅ DONE (Sprint 24) |
| Design system color compliance (shared components) | ✅ DONE (Sprint 24) |

---

*Created: 2026-06-17 by PM — Sprint 25 Round 50*
*Sprint 23: 3 features shipped, 998 lines of code, 1199 lines of tests, 662 total tests green*
*Sprint 24: C201 shipped (300 lines + 591 test lines), design system cleanup (4 files, 30+ violations fixed)*
*Sprint 25: Planning complete — C209 MUST, C203/C206 SHOULD (pending Daniel), pre-sprint fixes MUST*
