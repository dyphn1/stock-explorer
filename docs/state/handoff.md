# Handoff — Stock Explorer

## Summary
- **Topic**: 🔍 Sprint Review (Review PM — 2026-06-17)
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 22 (C201) ❌ NOT STARTED → Sprint 23 READY (with pre-conditions)

---

# 🔍 Review PM Report (2026-06-17)

## Sprint 22 (C201 今日市場動態) — VERDICT: NOT STARTED
- **Status**: Feature was planned and approved across Rounds 46-48 but **zero implementation** exists
- No source code, no commits, no verification logs for C201
- The i18n refactoring (commit 7bcbc00) consumed the development capacity allocated for Sprint 22
- **Recommendation**: Renumber C201 to Sprint 24 or restart as Sprint 22 with proper pre-conditions (regulatory review, performance budget, content prep)

## i18n Refactoring (Commit 7bcbc00) — VERDICT: NEEDS REMEDIATION

### Fixes Applied This Review
| Issue | Severity | Action |
|-------|----------|--------|
| `src/core/locales/` duplicate directory | 🔴 Critical | ✅ DELETED |
| `src/core/i18n.py.backup` leftover | 🟡 Low | ✅ DELETED |
| `t.spinner()` → `st.spinner()` in router.py:158 | 🐛 Bug | ✅ FIXED |
| `error.search_no_results` → `error.not_found` in main.py:311 | 🐛 Bug | ✅ FIXED |
| main.py truncated (311→322 lines, missing else branch) | 🔴 Critical | ✅ RESTORED from git |

### Remaining Issues (Non-blocking for Sprint 23)
| Issue | Severity | Location |
|-------|----------|----------|
| `story_arc_detector.py` returns Chinese text, not i18n keys | 🔴 Major | `src/services/story_arc_detector.py:30-47,185-188` |
| `story_timeline.py` renders Chinese directly, no `t()` calls | 🔴 Major | `src/pages/story_timeline.py` (entire file) |
| `_historical_scenarios.py` has ~280 lines of hardcoded Chinese | 🔴 Major | `src/pages/business_card/_historical_scenarios.py:10-291` |
| Sprint 23 keys (`story_arc.*`, `debate.*`, `scenario.*`) missing from locales | 🔴 Major | `locales/zh-TW.yaml`, `locales/en.yaml` |
| `_helpers.py` duplicates Chinese disclaimer text already in locales | 🟡 Medium | `src/pages/business_card/_helpers.py:115-119` |
| `story_arcs.yaml` has display strings (scope creep) + is dead code | 🟡 Medium | `src/data/yaml/story_arcs.yaml` |
| 8+ page files use hardcoded Chinese in `st.spinner()` instead of `t()` | 🟡 Medium | Multiple files |

### i18n Strategy Compliance Summary
- **Rule**: Services return keys, pages call `t()`
- **Reality**: `story_arc_detector.py` returns Chinese text directly; `story_timeline.py` never calls `t()`
- **Impact**: C202 (Story Arc Labels) cannot be properly i18n-wrapped until `story_arc_detector.py` is refactored
- **Recommendation**: Refactor `story_arc_detector.py` in Sprint 23 Week 1 before C202 development

## Test Health
- **458 passed** in 3.50s — all tests green
- No regressions from the fixes applied

---

# 🔧 Development Section — Sprint 23 Ready

## Sprint 23 Plan (Confirmed)
| Priority | Feature | Effort | Risk | Gate |
|----------|---------|--------|------|------|
| MUST | C202 Story Arc Labels | 11-18h | Low | i18n wrapping + 3-stock quality check |
| SHOULD | C199 Bear vs Bull Debate Cards | 14-22h | Medium | Tone QA gate (2 rev max) |
| COULD | C200 What If Calculator | 12-17h (+2-3h gate) | Medium-High | Week 1: API caching + data completeness + historian framing |
| **Total** | | **37-57h (+2-3h gate)** | | |

## Pre-Sprint 23 Actions (Updated)
1. ~~Delete `src/core/locales/` directory~~ ✅ DONE (this review)
2. Add Sprint 23 i18n keys to `locales/zh-TW.yaml` and `locales/en.yaml` — **STORY_ARC.* KEYS STILL NEEDED**
3. Refactor `story_arc_detector.py` to return keys instead of Chinese text — **REQUIRED before C202**
4. Design four-safeguard advisor boundary pattern for C199 (PM + Designer)

## Sprint 23 Readiness: ⚠️ CONDITIONAL
- **Blocker**: `story_arc_detector.py` must return keys (not Chinese) before C202 can be i18n-compliant
- **Blocker**: Sprint 23 locale keys (`story_arc.*`) must be added to both locale files
- **Non-blocker**: Other i18n compliance issues (story_timeline.py, _historical_scenarios.py) can be addressed during Sprint 23

## Next Cycle (Development)
🔧 Development Round 49: Sprint 23 execution — C202 i18n wrapping → C199 debate engine → C200 calculator (if gate passes).

---

# 💡 Discussion Section (Round 48 — 2026-06-17)

## Final Team Decision — Sprint 23 Feature Plan (Post-Challenge)

### i18n Conflict Resolution
- **Decision**: `locales/` (project root) is canonical. `src/core/locales/` deleted as dead code.
- **Reason**: `i18n.py` points to `locales/`, all existing `t()` calls use its schema. The new directory has an incompatible schema and is orphaned.
- **Action**: Add Sprint 23 keys (`story_arc.*`, `debate.*`, `scenario.*`) to both locale files.

### i18n Strategy Standardization
- **Decision**: Services return keys, pages call `t()`. Service-layer modules do NOT call `t()` directly.
- **Impact**: `story_arc_detector.py` refactored to return arc type keys (`growth`, `decline`, `volatile`, `recovery`) instead of Chinese text.

### story_arcs.yaml Scope
- **Decision**: Config only (thresholds, colors). Display strings moved to locale YAML files.

### C200 Deferral Criteria
- **Decision**: If C202 + C199 combined exceed 30h, C200 auto-deferred to Sprint 24.

## Key Decisions
1. C202 (Story Arc Labels) is Sprint 23 lead feature — service exists, needs i18n wrapping
2. C199 (Bear vs Bull) proceeds with four-safeguard pattern as pre-sprint dependency
3. C200 (What If Calculator) proceeds with Week 1 go/no-go gate (API caching + data completeness + historian framing)
4. All three features are rules-based (no LLM)
5. `locales/` is canonical — `src/core/locales/` deleted
6. Services return keys, pages call `t()` — standard i18n pattern
7. C200 deferral: C202 + C199 > 30h → auto-defer

## Conditions (Pre-Sprint 23)
1. C199 Four-Safeguard Pattern: PM + Designer must define before C199 development begins
2. C200 Week 1 Go/No-Go: FinMind API caching + data completeness + historian framing
3. C207-C214 Evaluation: Round 49 must evaluate C209 and C210 before Sprint 24 planning
4. ~~Locale Cleanup: Delete `src/core/locales/` before Sprint 23 Day 1~~ ✅ DONE (this review)
5. **NEW**: Refactor `story_arc_detector.py` to return keys before C202 development
6. **NEW**: Add `story_arc.*` keys to both locale files before C202 development

## Challenger Verdict
⚠️ CONDITIONAL ALIGNED — 5 blocking questions resolved, 4 recommendations accepted

## Documentation Created
- `docs/architecture/discuss_r48_architect.md`
- `docs/state/challenge_r48.md`
- `docs/state/handoff_discuss_r48.md`

---

# QA Verification (Review PM — 2026-06-17)
- Test suite: 458 passed in 3.50s
- Fixes applied: `src/core/locales/` deleted, `i18n.py.backup` cleaned, `t.spinner()` bug fixed, `error.not_found` key fixed, main.py truncation restored
- All tests green, no regressions
