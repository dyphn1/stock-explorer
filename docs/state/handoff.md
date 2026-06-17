# Handoff — Stock Explorer

## Summary
- **Topic**: 🔍 Sprint Review + Sprint 26 Readiness Assessment
- **Date**: 2026-06-17
- **Sprint Status**: Sprint 25 ✅ COMPLETE → Sprint 26 ✅ READY TO START

---

# ✅ Sprint 22 — COMPLETE (Verified)

| Feature | Status | Tests |
|---------|--------|-------|
| C201 Daily Market Dashboard | ✅ Complete | 113/113 passing |

---

# ✅ Sprint 23 — COMPLETE (Verified)

| Feature | Status | Tests |
|---------|--------|-------|
| C199 Debate Cards | ✅ Complete | 39/39 passing |
| C200 What If Calculator | ✅ Complete | 40/40 passing |
| C202 Story Arc Labels | ✅ Complete | 43/43 passing |

---

# ✅ Sprint 25 — COMPLETE

## C206 Recurring Investment Education — LESSON CREATED

| Item | Status |
|------|--------|
| `lesson_06.yaml` — DCA lesson | ✅ Created (commit 1a0c426) |
| `academy_meta.yaml` — lesson_06 registered | ✅ Updated |
| Hypothetical data only (no real stocks) | ✅ Confirmed |
| No calculator, no stock_example blocks | ✅ Confirmed |
| 3 quiz questions with explanations | ✅ Included |
| All Traditional Chinese | ✅ Confirmed |

**Lesson content:**
- Title: "定期定額：懶人投資法"
- 6 sections: concept, hypothetical 6-month example (範例公司), benefits, caveats, when DCA works, summary
- 3 callout blocks (info, tip, warning)
- Quiz: Q1 timing risk, Q2 averaging down, Q3 long-term commitment

## C209 Integration — ALL 3 PAGES DONE

| Page | Status | Details |
|------|--------|---------|
| `daily_market.py` | ✅ Integrated | 4 sources, `_render_freshness()` removed |
| `business_card/_main.py` | ✅ Integrated | 5 grouped sources, placed after `_render_footer()` |
| `event_dashboard.py` | ✅ Integrated | 2 sources, dead code removed |

## Pre-Sprint Fixes — APPLIED
- `validate_debate_text()` → `contains_banned_words()` ✅
- `_TIMELINE_LABELS` → i18n `t()` ✅
- 8 non-palette color fixes ✅
- `_section_title()` emoji logic improvement ✅

## Test Health
- **658 passed** in 3.95s — all tests green
- No regressions from C206 or C209

## Commits
- `1a0c426` — `feat(c206): add DCA recurring investment lesson (lesson_06)`
- `964e90c` — `feat(c209): integrate _source_section into daily_market, business_card, event_dashboard`
- `8ed9a97` — `feat(c209): add _source_section component for source transparency`
- `9bcbf22` — `fix(pre-sprint): rename validate_debate_text, i18n timeline labels, color fixes, section title emoji`

---

# 📋 Sprint 26 — READY TO START (Reviewed)

## i18n Refactoring Review (Commit 7bcbc00)

### ✅ What's Good
- `src/core/i18n.py` — clean `t()` implementation with nested key support, fallback to key text (no crash)
- `src/services/story_arc_detector.py` — returns i18n keys, not display text; pure Python, no Streamlit imports
- `src/services/roe_calculator.py` — proper TTM method, no naive *4 multiplication; seasonal industry warnings
- `src/services/dividend_analyzer.py` — proper annualized projection with `is_estimated` flag
- Locale files at `locales/en.yaml` (582 lines, 439 keys) and `locales/zh-TW.yaml` (590 lines, 443 keys)
- Architecture doc at `docs/architecture/i18n_integration.md`

### ⚠️ Issues Found

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| I-01 | **4 validation keys missing in EN**: `validation.error.empty`, `validation.error.format`, `validation.error.not_digit`, `validation.error.not_four_digit` exist in zh-TW but not en | Medium | Add to en.yaml before Sprint 26 |
| I-02 | **event_dashboard.py partially i18n'd**: Hardcoded Chinese strings on lines 51-52, 56, 61, 100, 113, 127, 133-144, 162 | Medium | Add to Sprint 26 COULD backlog |
| I-03 | **Untracked files**: `docs/design/i18n_review_event_dashboard.md` and `docs/design/zone_separation_review.md` exist but are not committed | Low | Commit or .gitignore |
| I-04 | **quiz_service.py imports Streamlit** — pre-existing architectural deviation | Low | Defer to future refactoring |
| I-05 | **format_percent()** uses `t('unit.percent')` which returns `" %"` — leading space baked into locale value | Low | Fix locale value or strip in code |

### i18n Verdict: ✅ ACCEPTABLE with minor fixes needed
- Core i18n infrastructure is sound
- Missing EN keys (I-01) is a quick fix (5 min)
- event_dashboard partial i18n (I-02) is a known gap from the untracked review doc

---

## Sprint 26 — FINAL PLAN (Post-Review, Unchanged)

| Priority | Feature | Effort | Risk | Gate |
|----------|---------|--------|------|------|
| **MUST** | Top 5 design debt fixes (D-005 + D-074) | 25 min | None | Week 1 Day 1 |
| **MUST** | Fix I-01: Add 4 missing EN validation keys | 5 min | None | Week 1 Day 1 |
| **MUST** | Fix API abuse in `get_stock_info` | 3-4h | Low | Week 1 |
| **MUST** | Fix YAML race conditions | 2-3h | Low | Week 1 |
| **MUST** | Fix cache invalidation + cleanup | 2-3h | Low | Week 1 |
| **SHOULD** | C203 Company Ecosystem Cards v1 | 12-14h | Low-Med | Week 2, pending Daniel |
| **COULD** | I-02: Complete event_dashboard i18n | 1-2h | Low | Week 2 |
| **COULD** | D-075-D-083 batch color fix | 2-3h | Low | Week 2 |
| **DEFERRED** | D-126 Dark/Light Theme | 12-18h | High | Sprint 27 |
| **DEFERRED** | D-127 `_infocard()` | 6-9h | Medium | Sprint 27 |

## Total Effort: 22-30h (2-week sprint)

## Key Decisions
1. Infrastructure before features — API/YAML/cache fixes are MUST Week 1
2. C203 conditional on Daniel approval by Week 1 Day 1 (no more deferrals)
3. D-127 dropped — no consumer identified
4. D-126 deferred — requires color compliance first
5. 3 of 5 top design fixes already done (D-073, D-071, D-084 verified fixed)
6. I-01 (missing EN keys) added as MUST Week 1 Day 1 — 5 min fix

## Pre-Conditions for C203
- `group_structures.yaml`: 5 parent companies, ~18 subsidiaries ✅
- `_subsidiary_card()`: ✅ Reusable
- Missing: `ecosystem_service.py` + `ecosystem_cards.py`
- **Gate**: Daniel approval required by Week 1 Day 1; otherwise drop

---

# 📋 Sprint History (Compressed)

| Sprint | Features | Status |
|--------|----------|--------|
| Sprint 22 | C201 Daily Market Dashboard | ✅ Complete |
| Sprint 23 | C202 Story Arc Labels, C199 Debate Cards, C200 What If Calculator | ✅ Complete |
| Sprint 24 | Design System Cleanup | ✅ Complete |
| Sprint 25 | C209 Collapsible Source, C206 DCA Lesson, Pre-sprint fixes | ✅ Complete |
| Sprint 26 | Infrastructure fixes + C203 Ecosystem Cards | ✅ Ready to Start |

---

*Updated: 2026-06-17 by Review PM*
*658 tests green. Sprint 22/23 verified complete. i18n refactoring reviewed — 5 minor issues found, 1 added to Sprint 26 MUST.*
*Sprint 26 cleared for Week 1 execution.*
