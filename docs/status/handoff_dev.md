# Handoff – Development

## Summary
- **Topic**: Development (🔧) — Sprint 21
- **Date**: 2026-06-15
- **Participants**: Product Manager, Architect, Developer (4 parallel sub-agents)
- **Sprint Status**: Sprint 21 ✅ COMPLETE (D-125 + D-126 + D-127 + C170 + C188 + C204 + C205 shipped)

## Completed Items
| Issue ID | Description | Owner | Result |
|----------|-------------|-------|--------|
| D-125 | chart_stock.py split into domain submodules | Architect | ✅ 3 submodules + re-export shim (db1bc13) |
| D-126 | INDUSTRY_BENCHMARKS dedup → shared benchmarks service | Developer | ✅ benchmarks.py + YAML + dedup all 3 files (9cda6df) |
| D-127 | _summary.py split into hero + secondary modules | Developer | ✅ _summary_hero.py (282 lines) + _summary.py (89 lines) (93280a4) |
| C170 | Tappable Glossary — inline metric definitions | Developer | ✅ 7 files, +242/-8 lines. Glossary tooltips + beginner mode + chart annotations (858e0ff) |
| C188 | Why Did This Move? — inline movement explanation | Developer | ✅ 6 files, +483 lines. New explainer service + section + templates (746e318) |
| C204 | Confidence Indicator — emoji badges on explanations | Developer | ✅ template_provider confidence scoring + _confidence_badge helper + 8 files updated (07ec00a) |
| C205 | Read Time Indicator — X min read on sections | Developer | ✅ _read_time + _section_title_with_read_time + 8 files updated (07ec00a) |

## Implementation Details

### D-125: chart_stock.py Split
- **Before**: `chart_stock.py` — 818 lines (god module)
- **After**: Re-export shim (~50 lines) + 3 domain submodules:
  - `chart_stock_financial.py` (~330 lines) — shared theme, revenue, price, institutional charts
  - `chart_stock_health.py` (~140 lines) — health snowflake, radar
  - `chart_stock_valuation.py` (~190 lines) — valuation band, PER/PB
- All existing imports verified working
- L0: 131 passed (baseline), L1: 20 pre-existing failures (FinMind env)

### D-126: INDUSTRY_BENCHMARKS Dedup
- Created `src/services/benchmarks.py` (164 lines) with:
  - `get_industry_benchmarks()` — loads 28 industries from YAML with caching
  - `fetch_benchmark_health_scores()` — extracted shared function replacing ~100 lines of duplicated logic
- Removed hardcoded dicts from `_summary.py`, `_health.py`, `peer_comparison.py`
- L0: 133 passed, L1: 20 pre-existing failures

### D-127: _summary.py Split
- **Before**: `_summary.py` — 464 lines
- **After**: `_summary_hero.py` (282 lines) + `_summary.py` (89 lines)
- `_render_story_card()` and `_render_header()` moved to hero module
- Re-export pattern maintains backward compatibility
- L0: 133 passed, L1: 20 pre-existing failures

### C170: Tappable Glossary
- Enhanced `_glossary_tooltip()` with beginner mode support
- New helpers: `_glossary_label()`, `_glossary_annotated_metric()`, `_glossary_help_text()`
- `resolve_term_key()` in service layer — handles metric names, English keys, dimension names
- Wired into: `_summary_hero.py`, `_health.py`, `_financial.py`, chart annotations
- Beginner mode: prominent "💡 什麼是{name}？" labels with blue borders
- Chart annotations: passive `<sub>` HTML in chart titles (service layer stays Streamlit-free)
- L0: 133 passed, L1: 20 pre-existing failures

### C188: Why Did This Move?
- New service: `stock_movement_explainer.py` (~150 lines, Streamlit-free)
  - `explain_movement()` — calculates % change, cross-references events, builds narrative
  - Uses `get_interpretation()` from event_interpretation_service.py
  - Returns structured dict: {direction, magnitude, change_pct, reason, detail, key_concept, events_used, narrative}
- New section: `_why_moved.py` (~100 lines) — "🔍 為什麼這檔股票會動？" card
- Templates: `config/movement_explanation_templates.yaml` — up/down/sideways, 6 reason categories
- Wired into `_main.py` after story card, before health snowflake
- L0: 135 passed (+4 from new files), L1: 20 pre-existing failures

### C204 + C205: Confidence + Read Time
- `template_provider.py` — confidence scoring: exact match 0.9, fallback 0.5, missing data 0.3
- New helpers: `_confidence_badge()`, `_read_time()`, `_section_title_with_read_time()`
- Applied to 8 section files: _summary_hero, _summary, _health, _financial, _why_moved, _story
- Confidence footnote: "信心指標反映資料完整度，非AI預測確定性"
- Read time: subtle gray pill style, only for sections >50 chars
- L0: 135 passed, L1: 20 pre-existing failures

## Verification Results
| Date | Gate 1 (Import) | Gate 2 (Render) | Gate 3 (Smoke) | Notes |
|------|-----------------|-----------------|----------------|-------|
| 2026-06-15 | ✅ 135/135 (L0) | ✅ 0/20 (L1 pre-existing FinMind) | — | Sprint 21 complete: D-125/126/127 + C170 + C188 + C204 + C205 |

## Pending Items
| Issue ID | Description | Owner | Next Steps |
|----------|-------------|-------|------------|
| C201 | 今日市場動態 (Daily Market Story) | Developer | Sprint 22 — P1, needs regulatory review gate |
| C202 | Story Arc Timeline Labels | Developer | Sprint 23 MUST |
| C199 | Bear vs Bull Debate Cards | Developer | Sprint 23 SHOULD |
| C200 | What If I Had Invested? Calculator | Developer | Sprint 23 COULD |

## Decisions Made
- D-125 re-export shim pattern chosen over import updates — zero changes needed in consuming files
- D-126 benchmarks.py as dedicated service (not _router_base constant) — cleaner separation of concerns
- C170 chart annotations are passive HTML in service layer — interactive tooltips wired in page layer
- C188 uses lazy import of adaptive_engine to avoid circular dependencies
- C204 confidence is synthetic (data completeness) — footnote added to every badge
- C205 read time only for sections >50 chars — avoids visual clutter on short sections

## Next Cycle Handoff
Next theme: 🔧 Development Round 47 — Sprint 22 (C201 今日市場動態 MVP)
Reference: `docs/state/handoff_discuss_r46.md` Sprint 22 section.
3 conditions must be met before Sprint 22:
1. Regulatory review gate
2. C201 performance budget (2s timeout + cache + mobile viewport)
3. C201 content prep (14-day template library + 10 fallback snippets)

---
*Last updated: 2026-06-15*
