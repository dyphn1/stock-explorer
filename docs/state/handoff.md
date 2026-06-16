# Handoff — Stock Explorer

## Summary
- **Topic**: 💡 Discussion (Round 48 — 2026-06-17)
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 22 (C201) in progress → Sprint 23 planned

---

# 🔧 Development Section (Round 48 — 2026-06-17)
**Sprint 23: C202 + C199 + C200** — PLANNED

## Sprint 23 Plan
| Priority | Feature | Effort | Risk | Gate |
|----------|---------|--------|------|------|
| MUST | C202 Story Arc Labels | 11-18h | Low | i18n wrapping + 3-stock quality check |
| SHOULD | C199 Bear vs Bull Debate Cards | 14-22h | Medium | Tone QA gate (2 rev max) |
| COULD | C200 What If Calculator | 12-17h (+2-3h gate) | Medium-High | Week 1: API caching + data completeness + historian framing |
| **Total** | | **37-57h (+2-3h gate)** | | |

## Pre-Sprint 23 Actions (Before Day 1)
1. Delete `src/core/locales/` directory (dead code, incompatible schema)
2. Add Sprint 23 i18n keys to `locales/zh-TW.yaml` and `locales/en.yaml`
3. Refactor `story_arc_detector.py` to return keys instead of Chinese text
4. Design four-safeguard advisor boundary pattern for C199 (PM + Designer)

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
4. Locale Cleanup: Delete `src/core/locales/` before Sprint 23 Day 1

## Documentation Created
- `docs/architecture/discuss_r48_architect.md`
- `docs/state/challenge_r48.md`
- `docs/state/handoff_discuss_r48.md`

## Challenger Verdict
⚠️ CONDITIONAL ALIGNED — 5 blocking questions resolved, 4 recommendations accepted

---

# QA Verification (Cron Run)
- Test suite: 458 passed
- i18n tests: All passing (test_i18n.py, test_story_arc_detector.py)
- Design compliance: D-001 (zone separation) still open in business_card/_sections/_summary_hero.py
