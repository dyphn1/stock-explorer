# Handoff — Stock Explorer

## Summary
- **Topic**: 🚀 Sprint 24 Execution — C201 Daily Market Dashboard Implementation
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 24 🏗️ IN PROGRESS — C201 implementation ready to start

---

# 🚀 Sprint 24 Plan (2026-06-17)

## Sprint 24 Candidates

| Priority | Feature | Effort | Risk | Status |
|----------|---------|--------|------|--------|
| MUST | C201 今日市場動態 (daily market dashboard) | 6-8h | Low | 🏗️ Ready to implement |
| STRETCH | C206 Recurring Investment Education | 6-8h | Low | ⏳ Week 4 stretch |
| DONE | C202 Story Arc Labels | 11-18h | Low | ✅ COMPLETE |
| DONE | C199 Bear vs Bull Debate Cards | 14-22h | Medium | ✅ COMPLETE |
| DONE | C200 What If Calculator | 12-17h | Medium-High | ✅ COMPLETE |
| DONE | i18n tech debt cleanup | 6-10h | Low | ✅ COMPLETE |

## C201 Daily Market Dashboard — Ready for Implementation

**Architecture design**: `docs/architecture/c201_daily_market.md` (714 lines)
**Page key**: `daily_market`

**Resolved design changes** (from Round 49):
- Remove TAIEX placeholder — use avg change % as primary metric
- Simplify volume to absolute total (億元), no 5-day comparison
- Post-filter events by market-relevant types only (earnings, dividend, institutional, market_news)

**Sections**:
1. Market overview summary — plain-language paragraph (template-based)
2. Market sentiment indicator — advance/decline ratio + volume
3. Sector performance strip — top movers with explanations
4. Top gainers/losers — Top 5 with context
5. Key events summary — market-level events from M5 engine (filtered)
6. Data freshness indicator

**Data sources**: All free FinMind APIs via existing `market_data` service layer (~2-3 unique API calls)

**Files to create/modify**:
- NEW: `src/pages/daily_market.py`
- MODIFY: `src/pages/router.py` (add route), `locales/en.yaml` + `locales/zh-TW.yaml` (~40 new keys)
- MODIFY: `src/pages/url_sync.py` (add to VALID_PAGES)

**Estimated effort**: 6-8 hours

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
| `f29c511` | feat(sprint23): C199 debate engine + C200 scenario calculator + test fixes |
| `d55452d` | refactor(i18n): Sprint 23 story_arc keys + detector i18n refactoring |
| `cfded35` | feat(discussion): Round 48 Sprint 23 planning - i18n conflict resolution + challenge |
| `7bcbc00` | feat(i18n): complete i18n integration across all pages and services |
| `d27f58d` | refactor(i18n): clean up hardcoded Chinese in service and page layers |
| `cfb342f` | fix(debate): integrate banned words filter into debate card rendering |

## Test Health
- **545 passed** in 3.65s — all tests green
- No regressions introduced

## Remaining Tech Debt (Non-blocking)

| Issue | Severity | Location |
|-------|----------|----------|
| Design system compliance: 83 issues across 7 rounds (grade C+) | 🟡 Medium | `docs/state/current_problems.md` |
| `validate_debate_text()` naming counterintuitive | 🟢 Low | `src/services/debate_engine.py` |
| Timeline strings in `scenario:` namespace | 🟢 Low | `locales/*.yaml` |
| Dead import in `_historical_scenarios.py` | 🟢 Low | `src/pages/business_card/_historical_scenarios.py` |

---

# 📋 Development Section — Sprint 24 Execution

## Next Steps (Development Round 52)

1. **Implement C201 daily_market.py** — Follow the architecture design doc with Round 49 resolutions
2. **Add router entry** — Add 'daily_market' to PAGE_KEYS and load_and_render_page
3. **Add i18n keys** — ~40 keys under `daily_market:` section in both locale files
4. **QA verification** — Test with real FinMind data
5. **Design review** — Verify PPT-style compliance

## Pre-Conditions — ALL RESOLVED ✅

| Condition | Status |
|-----------|--------|
| Fix broken `_is_etf_check` import | ✅ DONE (Sprint 23 review) |
| Add missing i18n keys | ✅ DONE (Sprint 23 review) |
| Fix `scenario.future_date` wrong English text | ✅ DONE (Sprint 23 review) |
| Replace hardcoded Chinese in `debate_cards.py` | ✅ DONE (Sprint 23 review) |
| Verify all tests pass | ✅ DONE (545/545) |
| i18n tech debt cleanup | ✅ DONE (this session) |
| Delete `src/core/locales/` | ✅ DONE (Round 48) |
| Refactor `story_arc_detector.py` to return keys | ✅ DONE (Round 48) |
| Implement four-safeguard pattern for C199 | ✅ DONE (Round 48) |
| Validate FinMind API data completeness | ✅ DONE (Round 48) |
| Resolve C201 open questions (TAIEX, volume, events) | ✅ DONE (Round 49) |
| C203/C209 evaluation and redesign | ✅ DONE (Round 49) |

---

*Created: 2026-06-17 by PM — Round 49 Discussion Complete*
*Sprint 23: 3 features shipped, 998 lines of code, 1199 lines of tests, 545 total tests green*
*Sprint 24: C201 ready for implementation*
