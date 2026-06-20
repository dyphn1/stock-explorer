# ADR-010: i18n Phase 2 Migration Plan

> **Status**: Draft | **Date**: 2026-06-21

## Context
TD-02 i18n Phase 1 is complete (~300 strings, 5 major pages). Phase 2 must migrate remaining files with Chinese UI strings to use `t()` calls.

## Uncommitted Changes Assessment
- `src/services/adaptive_engine.py` — ✅ Good, uses proper locale keys
- `src/services/news_summarizer.py` — ✅ Good, uses proper locale keys
- `src/services/revenue_analyzer.py` — ⚠️ Needs fix: uses Chinese strings as locale keys instead of proper english keys
- `locales/en.yaml`, `locales/zh-TW.yaml` — ✅ New keys added for news_summarizer and adaptive_engine

## Phase 2 Priority Order

### Immediate Fix (before any batching)
1. **Fix `revenue_analyzer.py`** — Critical bug: uses Chinese strings as locale keys (lines 121-135). Replace with proper English keys, add missing keys to locale YAML. This must be done first to prevent compounding errors.

### Batch 1: Complete Service Layer (max ~300 strings)
2. Migrate remaining `src/services/` files with Chinese strings (excluding already-migrated adaptive_engine.py, news_summarizer.py, and the now-fixed revenue_analyzer.py)

### Batch 2: Plugin Layer (max ~300 strings)
3. Migrate plugin files in `src/plugins/` with Chinese strings (priority: most-used plugins first)

### Batch 3: Page Layer (max ~300 strings)
4. Migrate remaining page files in `src/pages/` with Chinese strings

### Batch 4: Utilities + Core (remaining)
5. Migrate `src/utils/` and remaining `src/core/` files

## Rules
- Do NOT migrate: docstrings, comments, stock IDs, ticker symbols, proper nouns, already-English UI labels
- Locale key naming: `module_submodule_description` (e.g., `revenue_analyzer_auto_describe_segment`)
- Each batch must pass tests before moving to next
- Max ~300 strings per batch to ensure thorough review
- Dynamic strings (f-strings with Chinese) need special handling — use `t()` with placeholders
- Create detection script for remaining hardcoded Chinese strings post-migration
