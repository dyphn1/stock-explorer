# Known Issues & Reminders — Stock Explorer

> **Last Updated**: 2026-06-20
> **Maintainer**: PM Agent
> **Audience**: All roles

---

## Model Selection Rules

**Never use `openrouter/owl-alpha` for tasks requiring many API calls.**

| Role | Model | Reason |
|------|-------|--------|
| **PM** | `openrouter/owl-alpha` | Flow control only, few API calls |
| **Developer** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | 3-5x faster, good for file operations |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Same as above |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | Testing/verification, speed first |

**Lesson**: owl-alpha averages ~30s per API call, nemotron ~5-10s. Tasks with 15-20 calls will exceed 600s timeout on owl-alpha.

---

## Cron Environment Constraints

| Constraint | Description | Solution |
|------------|-------------|----------|
| `memory` unavailable | Cron has no memory tool | Write persistent info to `docs/state/handoff.md` |
| `execute_code` blocked | Background review blocks it | Use `terminal` or delegate to sub-agent |
| `read_file` wrong default path | Reads from `~/.hermes/` not project | **Always use absolute paths** |
| terminal wrong default dir | Commands target wrong directory | Prefix with `cd /Users/daniel.chang/Desktop/GitHub/stock-explorer &&` |
| sub-agent 600s timeout | Too many files or slow API | Max 2 files per batch; if timeout, reduce scope and re-dispatch |

---

## PM Rules

1. PM does NOT write code or modify files — delegate to Developer only
2. Do NOT use `execute_code` — blocked by background review
3. Do NOT use `terminal` for Python scripts — use `read_file` directly
4. After reading handoff + current_problems, dispatch sub-agents immediately
5. Use `git diff --stat` for gate check — don't trust sub-agent's word alone
6. If sub-agent times out — reduce scope and re-dispatch, don't take over

---

## Developer Rules

- **Locale key naming**: `page_block_function_description`, e.g., `etf_browser_filter_label`
- **Do NOT migrate**: docstrings, comments, stock IDs, ticker symbols, proper nouns, already-English UI labels
- **Test after migration**: `python3 -m pytest tests/ -x -q`
- **f-string escaping**: `"{{"` and `"}}"` in f-strings need care

---

## Architect Rules

- **Layered architecture** (never violate): Data → Service → Router → Presentation
- **No reverse dependencies**: Presentation must NOT import Service internals
- **Plugin Chassis**: All pages use `PluginRegistry` — new pages must follow
- **i18n**: `locales/en.yaml`, `locales/zh-TW.yaml` — all UI strings via `t('key')`

---

## Security Rules

- **LLM safety**: Translate only, never infer — no investment advice
- **No hardcoded secrets**
- **Input validation**: All user inputs must be validated
- **File lock**: watchlist.yaml concurrent writes need filelock

---

## Design Rules

- Use design system color tokens only — no hardcoded hex
- Use `_白话_card()` — not `st.metric()` or raw HTML
- All UI changes: HTML prototype → Daniel review → implementation → Design Reviewer verification
