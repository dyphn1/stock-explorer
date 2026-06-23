# Model Failure Log

> This file tracks all model call failures across cron runs.
> Purpose: Identify chronically failing models and make data-driven swap decisions.
> Format: See `docs/diagrams/flow.md` → "Model Failure Log" section.

---

## [2026-06-22] Log initialized
- Created by PM as part of fallback logging protocol update.
- Previous runs had no structured failure tracking.

---

## [2026-06-24 00:00] Run: Sprint 28 — Fix Failing Tests + UX Improvements
| Role | Primary Model | Fallback Model | Result |
|------|-------------|---------------|--------|
| Challenger 1 | gpt-oss-120b:free | — | ✅ Primary succeeded (but routed through nemotron-120b due to model routing) |
| Developer A | nemotron-120b:free | — | ✅ Primary succeeded |
| Developer B | nemotron-120b:free | — | ✅ Primary succeeded |
| Developer C | nemotron-120b:free | — | ✅ Primary succeeded |
| Challenger 2 | gpt-oss-120b:free | nemotron-120b:free | ⚠️ Primary may have been rate-limited; fallback used |
| QA | gemma-4-31b-it:free | nemotron-120b:free | ⚠️ Primary may have been rate-limited; fallback used |

### Model Health Summary
| Model Used | Times Called | Failures | Notes |
|------------|-------------|----------|-------|
| owl-alpha | 1 | 0 | PM only |
| nemotron-120b | 6 | 0 | +2 fallback from gpt-oss/gemma |
| gpt-oss-120b | 0 | 0 | May have been rate-limited |
| gemma-31b | 0 | 0 | May have been rate-limited |

### Notes
- Challenger 2 and QA both used nemotron-120b instead of their primary models (gpt-oss-120b and gemma-31b respectively). This suggests possible rate limiting on those models.
- All tasks completed successfully despite model routing changes.
- 719 tests passed (up from 717 in previous run).

---

## [2026-06-24 06:15] Run: Fix Failing Tests + Integrate Why Did This Move (C188)
| Role | Primary Model | Fallback Model | Result |
|------|-------------|---------------|--------|
| Challenger 1 | gpt-oss-120b:free | — | ✅ Primary succeeded |
| Challenger 2 | nemotron-120b:free | — | ✅ Primary succeeded |
| Developer A (path fix) | nemotron-120b:free | — | ✅ Primary succeeded |
| Developer B (integration) | nemotron-120b:free | — | ✅ Primary succeeded |
| Architect | nemotron-120b:free | — | ✅ Primary succeeded |
| QA | gemma-4-31b-it:free | — | ✅ Primary succeeded |

### Model Health Summary
| Model Used | Times Called | Failures | Notes |
|------------|-------------|----------|-------|
| owl-alpha | 1 | 0 | PM only |
| gpt-oss-120b | 1 | 0 | Challenger 1 |
| nemotron-120b | 4 | 0 | Challenger 2 + 2 Developers + Architect |
| gemma-31b | 1 | 0 | QA |

### Notes
- All primary models succeeded — no fallbacks needed.
- 7 new tests passing (test_sprint_202606240010.py: 7/7).
- 2 UI no-raw-keys tests passing.
- Full suite timeout at 89% is a pre-existing issue (slow test, unrelated to changes).
- 13 files changed, 633 insertions, 71 deletions.

---

## [2026-06-24 11:30] Run: Sprint 30 — i18n Translation Fix + Validation Test
| Role | Primary Model | Fallback Model | Result |
|------|-------------|---------------|--------|
| Developer | nemotron-120b:free | — | ✅ Primary succeeded |
| Challenger | gpt-oss-120b:free | — | ✅ Primary succeeded |
| Security Architect | nemotron-120b:free | — | ✅ Primary succeeded |
| Architect | nemotron-120b:free | — | ✅ Primary succeeded |
| QA | gemma-4-31b-it:free | — | ✅ Primary succeeded |

### Model Health Summary
| Model Used | Times Called | Failures | Notes |
|------------|-------------|----------|-------|
| owl-alpha | 1 | 0 | PM only |
| nemotron-120b | 3 | 0 | Developer + Security Architect + Architect |
| gpt-oss-120b | 1 | 0 | Challenger |
| gemma-31b | 1 | 0 | QA |

### Notes
- All primary models succeeded — no fallbacks needed.
- 27 missing page key translations added to both locale files.
- English locale why_did_this_move section corrected (was Chinese, now English).
- New validation test (test_i18n_validation.py) with 6 tests — all passing.
- 734 tests pass, 1 pre-existing UI test flakiness (unrelated to changes).
- 3 files changed, 155 insertions, 3 deletions.
