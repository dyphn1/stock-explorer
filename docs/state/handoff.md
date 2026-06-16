# Handoff — Stock Explorer

## Summary
- **Topic**: 💡 Discussion (Round 47 — 2026-06-15)
- **Date**: 2026-06-15
- **Sprint Status**: Sprint 16a ✅ → 16b ✅ → 17 ✅ → 18 ✅ → 19 ✅ → 20 ✅ → 21 ✅ COMPLETE → Sprint 22 (C201) in progress

---

# 🔧 Development Section (Round 47 — 2026-06-15)
**Sprint 22: C201 (今日市場動態)** — IN PROGRESS

## C201 今日市場動態
- Sprint 22 MVP: Template-based, on-demand generation, retrospective framing (\"yesterday's news\")
- 3 pre-sprint conditions: regulatory review gate, 2s performance budget, 14-day template library
- Kill switch: If 7-day retention doesn't improve by Sprint 23 review, deprioritize

## Next Cycle (Development)
🔧 Development Round 48: Sprint 23 — C202 (Story Arc Labels) + C199 (Bear vs Bull Debate Cards) + C200 (What If Calculator). See Sprint 23 plan in docs/state/handoff_discuss_r47.md.

---

# 💡 Discussion Section (Round 47 — 2026-06-15)

## Final Team Decision — Sprint 23 Feature Plan (Post-Challenge)

| Sprint | Features | Hours |
|--------|----------|-------|
| Sprint 23 | C202 (MUST) + C199 (SHOULD) + C200 (COULD) | 31-47h |
| Sprint 24 | C200 (if deferred) + C201 follow-ups + C206 + C203 + C209 (pending eval) | TBD |

## Key Decisions
1. C202 (Story Arc Labels) is Sprint 23 lead feature — lowest risk, highest vision alignment
2. C199 (Bear vs Bull) proceeds with four-safeguard advisor boundary pattern and Tone QA gate
3. C200 (What If Calculator) proceeds with Week 1 go/no-go gate (API caching + historian framing)
4. C200 extends existing C74 `_historical_scenarios.py` (320 lines) — not greenfield
5. C207-C214 from Round 10 research deferred to Round 48 Discussion evaluation
6. All three features are independent of Sprint 21/22 work
7. Rule-based arc detection (not LLM) for C202 — YAML-configurable thresholds

## Conditions (Pre-Sprint 23)
1. C199 Tone QA Gate: Content review must pass before C199 ships (2 revision max)
2. C200 Week 1 Go/No-Go: FinMind API caching + historian framing validation
3. C207-C214 Evaluation: Round 48 must evaluate C209 and C210 before Sprint 24 planning

## Documentation Created
- `docs/architecture/discuss_r47_architect.md`
- `docs/design/discuss_r47_designer.md`
- `docs/status/discuss_r47_developer.md`
- `docs/state/challenge_r47.md` (3-round challenge, 3 conditions)
- `docs/state/handoff_discuss_r47.md` (full discussion record)

## Challenger Verdict
✅ ALIGNED — 3 conditions → All resolved

---

# QA Verification (Cron Run)
- Test suite: 458 passed
- Design compliance: Found zone separation violation in business_card/_sections/_summary_hero.py (watchlist buttons in navbar). Matches D-001 in current_problems.md.
- Previously fixed issue D-007 (heavy text) remains fixed.
- Tone blocklist violations fixed in recent QA commit.