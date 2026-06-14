# Handoff — Stock Explorer

## Summary
- **Topic**: 💡 Discussion (Round 47 — 2026-06-15)
- **Date**: 2026-06-15
- **Sprint Status**: Sprint 16a ✅ → 16b ✅ → 17 ✅ → 18 ✅ → 19 ✅ → 20 ✅ → 21 ✅ COMPLETE → Sprint 22 (C201) in progress

---

# 🔧 Development Section (Round 47 — 2026-06-15)
**Sprint 22: C201 (今日市場動態)** — IN PROGRESS

## C201 今日市場動態
- Sprint 22 MVP: Template-based, on-demand generation, retrospective framing ("yesterday's news")
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

# 🔧 Development Section (Round 47 — 2026-06-15) [Sprint 21 COMPLETE]
**Sprint 21: D-125 + D-126 + D-127 + C170 + C188 + C204 + C205** — ✅ COMPLETE (commits db1bc13, 9cda6df, 93280a4, 858e0ff, 746e318, 07ec00a)

## D-125 chart_stock.py Split
- 818-line god module → 3 domain submodules + re-export shim
- `chart_stock_financial.py` (~330), `chart_stock_health.py` (~140), `chart_stock_valuation.py` (~190)

## D-126 INDUSTRY_BENCHMARKS Dedup
- Created `benchmarks.py` (164 lines) with `get_industry_benchmarks()` + `fetch_benchmark_health_scores()`
- Removed hardcoded dicts from 3 files (_summary, _health, peer_comparison)

## D-127 _summary.py Split
- 464 lines → `_summary_hero.py` (282) + `_summary.py` (89)
- Re-export pattern maintains backward compatibility

## C170 Tappable Glossary
- Enhanced `_glossary_tooltip()` with beginner mode support
- New helpers: `_glossary_label()`, `_glossary_annotated_metric()`, `_glossary_help_text()`
- `resolve_term_key()` in service layer — handles metric names, English keys, dimension names
- Wired into 4 section files + chart annotations

## C188 Why Did This Move?
- New `stock_movement_explainer.py` (~150 lines, Streamlit-free)
- New `_why_moved.py` section (~100 lines)
- `config/movement_explanation_templates.yaml` — 6 reason categories, historian-toned

## C204 + C205 Stretch Goals
- Confidence badges (🟢🟡🟠) on all explanation displays
- Read time indicators ("X 分鐘閱讀") on content sections >50 chars
- 8 section files updated

## Verification
- L0: 135 passed (2 pre-existing quiz_service.py failures)
- L1: 20 failures (all pre-existing FinMind not installed)

## Next Cycle
🔧 Development Round 47: Sprint 22 — C201 (今日市場動態) + 3 pre-sprint conditions (regulatory review, performance budget, content prep). See Sprint 22 plan in handoff_discuss_r46.md.

---

# 💡 Discussion Section (Round 46 — 2026-06-15)

## Final Team Decision — Feature Roadmap (Post-Challenge)

| Sprint | Features | Hours |
|--------|----------|-------|
| Sprint 21 | C170 + C188 + D-125/126/127 + C204/C205 stretch | 27.5-40.5h + 7-11h |
| Sprint 22 | C201 (今日市場動態, P1 MVP) | 12-16h |
| Sprint 23 | C202 → C199 → C200 (MoSCoW) | 32-44h |
| Sprint 24+ | C206 + C203 | 26-36h |

## Key Decisions
1. C201 renamed to "今日市場動態" (avoid naming collision with C202)
2. C201 reframed as retrospective "yesterday's news" (not advice)
3. C204+C205 moved to Sprint 21 stretch goals (from Sprint 22)
4. Sprint 23 MoSCoW: C202 MUST → C199 SHOULD → C200 COULD
5. C200 acknowledged as C74 enhancement (not new feature)
6. Feature boundaries: C204 NOT on C201, C205 NOT double-applied to C201
7. Regulatory review gate added before Sprint 22

## Conditions (Pre-Sprint 22)
1. Regulatory review of C201+C200+C206 aggregate impression
2. C201 performance budget: 2s timeout + cache + mobile viewport test
3. C201 content: 14-day template library + 10 fallback snippets

## Documentation Created
- `docs/architecture/discuss_r46_architect.md`
- `docs/design/discuss_r46_designer.md`
- `docs/status/discuss_r46_developer.md`
- `docs/state/challenge_r46.md` (3-round challenge, 3 conditions)
- `docs/state/handoff_discuss_r46.md` (full discussion record)

## Challenger Verdict
✅ ALIGNED — 3 conditions → All resolved

---

# 💡 Discussion Section (Round 45 — 2026-06-15)

## Final Team Decision — Revised Roadmap (Post-Challenge)

| Sprint | Features | Hours |
|--------|----------|-------|
| Pre-21 | D-120 (benchmark extraction) | 1.5-2.5h |
| Sprint 21 | C170 + C188 + D-125/126/127 | 27.5-40.5h |
| Sprint 21 stretch | C194 | 8-12h |
| Sprint 22 | C152 + C194 | 24-32h |
| Sprint 23 | C196 + C175 | 26-34h |
| Sprint 24 | C184 | 18-24h |

## Key Changes from Preliminary Plan
1. C188 moved to Sprint 21 core (fewer prerequisites than C194)
2. C194 moved to Sprint 22 (pairs with C152 narratives)
3. Tech debt D-125/D-126/D-127 added to Sprint 21
4. C196 deferred to Sprint 23 (D25 prerequisite)
5. C184 is Sprint 24 capstone

## Documentation Created
- `docs/architecture/discuss_r45_architect.md`
- `docs/design/discuss_r45_designer.md`
- `docs/status/discuss_r45_developer.md`
- `docs/state/challenge_r45.md` (3-round challenge, 7 conditions)
- `docs/state/handoff_discuss_r45.md` (full discussion record)

## Challenger Verdict
⚠️ Contradictions found → 7 conditions → All resolved in final decision

---

*Previous rounds R1-R44 compressed — see git log for details. Key archives: docs/state/handoff_discuss_r45.md, docs/state/challenge_r45.md, docs/architecture/discuss_r45_architect.md*
