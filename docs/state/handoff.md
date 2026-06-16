# Handoff — Stock Explorer

## Summary
- **Topic**: 🔍 Review PM Report — Sprint 23 Quality Review + Sprint 24 Readiness (2026-06-17)
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 23 ✅ COMPLETE (with fixes applied) | Sprint 24 ✅ READY TO START

---

# 🔍 Review PM Report (2026-06-17)

## Sprint 23 — Quality Review Results

All three features reviewed. 2 blocking issues found and fixed, 3 minor issues documented.

| Feature | Review Result | Issues Found | Fixes Applied |
|---------|--------------|--------------|---------------|
| C202 Story Arc Labels | ✅ PASS | Minor: `_bucket_label()` returns hardcoded Chinese (non-blocking) | None needed |
| C199 Bear vs Bull Debate | ⚠️ FIXED | (1) Hardcoded Chinese empty-state in `debate_cards.py:157-163` (2) Banned words filter defined but not called in generation flow | Replaced with `t("debate.no_data_detail")` + added key to both locales |
| C200 What If Calculator | ⚠️ FIXED | (1) 3 missing i18n keys: `invalid_date`, `invalid_range`, `amount_too_small` (2) `en.yaml:341` wrong text for `future_date` ("in the past" → "in the future") | Added all 3 keys to both locales + fixed English text |

## Critical Infrastructure Fix

**BLOCKER FIXED**: `router.py:50` had broken import `_is_etf_check` (function doesn't exist in watchlist.py). App was non-functional.
- **Fix**: Changed to `_is_etf as _is_etf_check` (correct function name)
- **Impact**: App can now start. This was introduced in commit 7bcbc00 (i18n refactoring).

## Missing Locale Keys — FIXED

Added missing i18n keys to both `locales/en.yaml` and `locales/zh-TW.yaml`:
- `sidebar.nav_label` — "Navigation" / "導覽"
- `page.learn_first_gate` — "Learn First Gate" / "學習優先門"
- `debate.no_data_detail` — empty-state detail message
- `scenario.invalid_date` — "Invalid date format..."
- `scenario.invalid_range` — "Invalid date range..."
- `scenario.amount_too_small` — "Investment amount is too small..."

## C201 (今日市場動態) Status — CLARIFIED

`investor_story_feed.py` is **C116** (每日故事 Feed), NOT C201. The `daily_story` page in router.py routes to C116 content. C201 (daily market dashboard with market-level narrative) is **NOT implemented** and remains a Sprint 24 candidate.

## Test Health
- **545 passed** in 3.33s — all tests green (unchanged after fixes)
- No regressions introduced

## Remaining Tech Debt (Non-blocking for Sprint 24)

| Issue | Severity | Location |
|-------|----------|----------|
| `_historical_scenarios.py` curated scenario content (hardcoded Chinese) | 🟡 Medium | `src/pages/business_card/_historical_scenarios.py:14-291` |
| `story_arc_detector.py:_bucket_label()` returns hardcoded Chinese | 🟢 Low | `src/services/story_arc_detector.py:82-87` |
| `debate_engine.py` banned words filter not called in generation flow | 🟢 Low | `src/services/debate_engine.py:55-59` (defined but not invoked) |
| `investor_story_feed.py` not i18n-wrapped (hardcoded Chinese) | 🟡 Medium | `src/pages/investor_story_feed.py` |
| Design system compliance: 92 issues across 7 rounds (grade C+) | 🟡 Medium | `docs/state/current_problems.md` |

---

# 🔧 Development Section — Sprint 24 Planning

## Sprint 24 Candidates

| Priority | Feature | Effort | Risk |
|----------|---------|--------|------|
| MUST | C201 今日市場動態 (daily market dashboard) | 15-22h | Medium |
| SHOULD | C203 Supply Chain Visual Map | 18-25h | High |
| SHOULD | C209 Source Transparency Layer | 10-15h | Medium |
| COULD | C206 Recurring Investment Education | 12-18h | Medium (regulatory) |
| COULD | i18n tech debt cleanup (spinner strings, scenario content) | 6-10h | Low |

## Pre-Sprint 24 Conditions — ALL RESOLVED ✅

| Condition | Status |
|-----------|--------|
| Fix broken `_is_etf_check` import | ✅ DONE (this review) |
| Add missing i18n keys | ✅ DONE (this review) |
| Fix `scenario.future_date` wrong English text | ✅ DONE (this review) |
| Replace hardcoded Chinese in `debate_cards.py` | ✅ DONE (this review) |
| Verify all tests pass | ✅ DONE (545/545) |

## Next Cycle (Development)
🔧 Development Round 50: Sprint 24 execution — C201 daily market dashboard → C203 supply chain map → C209 source transparency.

---

*Created: 2026-06-17 by Review PM*
*Commits: fix(router) broken import + fix(i18n) missing keys + fix(debate) hardcoded Chinese*
