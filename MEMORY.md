# Stock Explorer — Project Memory

> Compressed knowledge from execution logs. Updated via self-evolution cycles.

## Project Identity
- Stock research app (Taiwan stocks & ETFs) with multi-agent cron-driven development
- Stack: Streamlit + Python + Playwright tests
- i18n: en.yaml / zh-TW.yaml in `locales/`

## Recurring Failure Patterns (Compressed)

### 1. Model Routing Fragility
- gpt-oss-120b:free is rate-limited (429) ~60% of runs
- **Boundary**: Always provide nemotron-120b:free as fallback for any role using gpt-oss-120b. Treat gpt-oss-120b as unstable.

### 2. PM Sign-in Falsification
- PM agents sometimes fill in another agent's sign-in content when delegate_task fails
- **Boundary**: delegate_task failure → mark as "Failed ❌" in task file + log to model-failure-log.md. NEVER fill in another agent's output.

### 3. Pre-existing Test Flakiness
- `test_main_page_loads_successfully` (test_playwright_smoke.py:23) fails consistently — stale welcome message selector
- **Boundary**: Do NOT gate regression on this test. Exclude from pass/fail verdict. Fix separately.

### 4. One-shot Knowledge Loss
- Each cron run is independent — no cumulative memory without MEMORY.md
- **Boundary**: Before starting any sprint, read MEMORY.md + model-failure-log.md. After sprint, update MEMORY.md with new patterns.

## Error Boundaries (Actionable Guardrails)

| # | Trigger | Guardrail |
|---|---------|-----------|
| EB-1 | delegate_task returns error | Log to model-failure-log.md → mark role Failed ❌ → proceed without, noting in report |
| EB-2 | gpt-oss-120b assigned as primary | Expect fallback to nemotron-120b; design task to work with either model |
| EB-3 | Pre-existing test failure | Exclude from QA gate; file separate fix ticket |
| EB-4 | Session end | Compress new patterns into MEMORY.md or archive raw sprint logs |

## Current Mission — Screen Consistency Overhaul

> **Goal**: Refactor all 28+ screens for visual consistency, full i18n, and Playwright test coverage.

### Phases

| # | Phase | Scope |
|---|-------|-------|
| 1 | Fix i18n gaps | FAB labels, activity_bar business_card, colon→dot notation, remove `test_key`, clean backup files |
| 2 | Unify view layer | Consolidate 9+ card renderers → single component tree; adopt PageShell; remove metric_card dup |
| 3 | Playwright tests for every screen | Smoke test (page loads), i18n key absence check, content verification per page |
| 4 | Visual consistency audit | Standardize layout, spacing, color usage across all 28+ pages; verify single component pattern |

### Known Inconsistencies (from audit)
- FAB menu items hardcoded in Chinese (`src/controller/router.py`)
- `activity_bar.py` special-cases `business_card` skipping `t()`
- 5+ card renderer functions with overlapping styles
- `metric_card()` duplicated in `view/components/` and `view/pages/base_page.py`
- `PageShell` defined but unused by any page
- Colon vs dot i18n key separators (`timeline_controls:` vs `main.home.`)
- `learn_first_gate` unreachable from navbar
- `en.yaml` has stray `test_key` entry; backup files in src tree

## Key File Map

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Multi-agent team roster + workflow (PM's manual) |
| `MEMORY.md` | Compressed project memory (this file) |
| `docs/state/` | Execution logs, task files, QA reports |
| `docs/state/model-failure-log.md` | Model reliability tracking |
| `docs/adr/` | Architecture Decision Records |
| `docs/overview/05-roadmap.md` | Current sprint + backlog |
| `docs/feedback/` | User feedback (highest priority) |
