# ADR-004 Phase 2: Complete Migration Plan — Legacy Pages → Plugin Chassis

**Date:** 2026-06-18
**Status:** Approved (Ready for Implementation)
**Scope:** Migrate ALL remaining 28 pages from `router.py` if-elif branches to Plugin Chassis

---

## 1. Complete Page Inventory

Every page currently in `router.py`'s `load_and_render_page()` if-elif chain or standalone block:

### 1A. Stock-Dependent Pages (require stock_id + data)

| # | page_key | render_fn | Signature | Params | Category | Icon | Order |
|---|----------|-----------|-----------|--------|----------|------|-------|
| 1 | `business_card` | `_render_business_card` | `(data, client)` | 2 positional | `analysis` | 🏢 | 10 |
| 2 | `operation_checkup` | `_render_operation_checkup` | `(data)` | 1 positional | `analysis` | 🔧 | 20 |
| 3 | `financial_health` | `_render_financial_health` | `(data)` | 1 positional | `analysis` | 💪 | 30 |
| 4 | `peer_comparison` | `_render_peer_comparison` | `(data, client)` | 2 positional | `analysis` | 👥 | 40 |
| 5 | `group_structure` | `_render_group_structure` | `(data)` | 1 positional | `analysis` | 🏗️ | 50 |
| 6 | `story_timeline` | `render_company_timeline` | `(data, client)` | 2 positional | `analysis` | 📅 | 60 |
| 7 | `full_story_timeline` | `render_story_timeline_page` | `(data, client)` | 2 positional | `analysis` | 📆 | 65 |
| 8 | `revenue_tree` | `_render_revenue_tree` | `(data, client)` | 2 positional | `analysis` | 🌳 | 70 |
| 9 | `compare_stories` | `_render_compare_stories_page` | `(data, client)` | 2 positional | `analysis` | 📖 | 80 |
| 10 | `moat_comparison` | `_render_moat_comparison_page` | `(data, client)` | 2 positional | `analysis` | 🏰 | 90 |
| 11 | `debate_cards` | `render_debate_cards_page` | `(data, client)` | 2 positional | `analysis` | 🃏 | 100 |

### 1B. Standalone Pages (no stock_id, no data)

| # | page_key | render_fn | Signature | Params | Category | Icon | Order |
|---|----------|-----------|-----------|--------|----------|------|-------|
| 12 | `etf_section` | `_render_etf_browser` | `(client)` | 1 positional | `browse` | 🏷️ | 20 |
| 13 | `watchlist` | `_render_watchlist_page` | `(client)` | 1 positional | `tool` | 📋 | 10 |
| 14 | `sector_heatmap` | `_render_sector_heatmap` | `(client)` | 1 positional | `browse` | 🔥 | 30 |
| 15 | `investment_memo` | `_render_investment_memo` | `(client)` | 1 positional | `tool` | 📝 | 20 |
| 16 | `case_study` | `_render_market_event_case_study` | `(client)` | 1 positional | `learn` | 📚 | 10 |
| 17 | `financial_wellness` | `_render_financial_wellness` | `(client)` | 1 positional | `tool` | 💰 | 30 |
| 18 | `comprehension_check` | `_render_comprehension_check` | `(client)` | 1 positional | `learn` | ✅ | 20 |
| 19 | `academy` | `_render_academy` | `(client)` | 1 positional | `learn` | 🎓 | 30 |
| 20 | `case_study_library` | `_render_case_study_library` | `(client)` | 1 positional | `learn` | 📖 | 40 |
| 21 | `stock_screener` | `_render_stock_screener` | `(client)` | 1 positional | `tool` | 🔎 | 40 |
| 22 | `learn_first_gate` | `_render_learn_first_gate` | `(client)` | 1 positional | `learn` | 🚪 | 60 |
| 23 | `first_visit_guide` | `_render_first_visit_guide` | `(client)` | 1 positional | `learn` | 👋 | 50 |
| 24 | `daily_story` | `render_investor_story_feed` | `(data, client)` | 2 positional* | `learn` | 📰 | 70 |

> **\* `daily_story` special case:** The render fn `render_investor_story_feed` has signature `(data, client)`, but in `router.py` it's called as `render_investor_story_feed({}, client)` — an empty dict is passed as data. This means it technically uses the `(data, client)` adapter path but its `requires_data` should be `False` (the data is a dummy). The plugin should declare `requires_stock_id=False, requires_data=False` and the adapter will pass the `ctx.client` correctly — BUT the fn takes 2 params. **Resolution:** Use `LegacyPageAdapter` with `requires_data=False`; the adapter validates signature as `data_client` (2 params) but since `requires_data=False`, in `render()` it would check `ctx.data is not None` and skip calling. **Better resolution:** Wrap `render_investor_story_feed` in a lambda or adapter fn that only passes `client`, OR set `requires_data=True` in the adapter so the dummy `{}` data flows through. **Recommended fix:** In the plugin file, create a thin wrapper:
> ```python
> def _render_daily_story_adapter(client):
>     render_investor_story_feed({}, client)
> ```
> Then use the `(client)` → `client_only` path.

### 1C. Already Migrated (Phase 1)

| page_key | Category | Icon | Order |
|----------|----------|------|-------|
| `category_browser` | `browse` | 🗺️ | 10 |
| `settings` | `system` | ⚙️ | 30 |
| `event_dashboard` | `system` | 📊 | 10 |
| `notification_center` | `system` | 🔔 | 20 |
| `daily_market` | `browse` | 📈 | 40 |

---

## 2. Directory Structure

Each new plugin follows the established Phase 1 pattern — a single `plugin.py` per directory using `LegacyPageAdapter`:

```
src/plugins/
├── __init__.py                    # existing, empty
├── category_browser/              # Phase 1 ✅
│   └── plugin.py
├── settings/                      # Phase 1 ✅
│   └── plugin.py
├── event_dashboard/               # Phase 1 ✅
│   └── plugin.py
├── notification_center/           # Phase 1 ✅
│   └── plugin.py
├── daily_market/                  # Phase 1 ✅
│   └── plugin.py
│
├── # ── Phase 2 NEW ──────────────────
├── business_card/
│   └── plugin.py
├── operation_checkup/
│   └── plugin.py
├── financial_health/
│   └── plugin.py
├── peer_comparison/
│   └── plugin.py
├── group_structure/
│   └── plugin.py
├── story_timeline/
│   └── plugin.py
├── full_story_timeline/
│   └── plugin.py
├── revenue_tree/
│   └── plugin.py
├── compare_stories/
│   └── plugin.py
├── moat_comparison/
│   └── plugin.py
├── debate_cards/
│   └── plugin.py
├── etf_section/
│   └── plugin.py
├── watchlist/
│   └── plugin.py
├── sector_heatmap/
│   └── plugin.py
├── investment_memo/
│   └── plugin.py
├── case_study/
│   └── plugin.py
├── financial_wellness/
│   └── plugin.py
├── comprehension_check/
│   └── plugin.py
├── academy/
│   └── plugin.py
├── case_study_library/
│   └── plugin.py
├── stock_screener/
│   └── plugin.py
├── learn_first_gate/
│   └── plugin.py
├── first_visit_guide/
│   └── plugin.py
├── daily_story/
│   └── plugin.py
```

---

## 3. Migration Waves

### Wave 1: Standalone (client-only) pages — 13 pages

| # | page_key | Signature | Notes |
|---|----------|-----------|-------|
| 1 | `watchlist` | `(client)` | |
| 2 | `investment_memo` | `(client)` | |
| 3 | `financial_wellness` | `(client)` | |
| 4 | `stock_screener` | `(client)` | |
| 5 | `case_study` | `(client)` | |
| 6 | `comprehension_check` | `(client)` | |
| 7 | `academy` | `(client)` | |
| 8 | `case_study_library` | `(client)` | |
| 9 | `learn_first_gate` | `(client)` | |
| 10 | `first_visit_guide` | `(client)` | |
| 11 | `etf_section` | `(client)` | |
| 12 | `sector_heatmap` | `(client)` | |
| 13 | `daily_story` | `(client)` | Uses wrapper to adapt `(data, client)` fn |

### Wave 2: Stock pages (data only) — 5 pages

| # | page_key | Signature | Notes |
|---|----------|-----------|-------|
| 14 | `operation_checkup` | `(data)` | |
| 15 | `financial_health` | `(data)` | |
| 16 | `group_structure` | `(data)` | |

### Wave 3: Stock pages (data + client) — 6 pages

| # | page_key | Signature | Notes |
|---|----------|-----------|-------|
| 16 | `business_card` | `(data, client)` | Default/highest-traffic page, serves as the benchmark |
| 17 | `peer_comparison` | `(data, client)` | |
| 18 | `story_timeline` | `(data, client)` | |
| 19 | `full_story_timeline` | `(data, client)` | |
| 20 | `revenue_tree` | `(data, client)` | |
| 21 | `compare_stories` | `(data, client)` | |
| 22 | `moat_comparison` | `(data, client)` | |
| 23 | `debate_cards` | `(data, client)` | Debate cards |

**Rationale for ordering:**
- Wave 1 first: All standalone pages with `(client)` signature are mechanically identical to the 5 already-migrated Phase 1 pages. This builds confidence in the pattern.
- Wave 2 second: `(data)` stock pages are simpler than `(data, client)` — they don't need client for API calls during render.
- Wave 3 last: `(data, client)` pages are the most complex. `business_card` (#16) is first because it's the default/highest-traffic page and serves as the benchmark.
- `daily_story` is in Wave 1 despite having a `(data, client)` render fn because the dummy `{}` data pattern allows a clean `(client)` wrapper.

---

## 4. Plugin.py Template

### 4A. Standalone (client-only) page — e.g. `watchlist/plugin.py`

```python
"""
src/plugins/watchlist/plugin.py
Phase 2: LegacyPageAdapter for watchlist (standalone page, stock_id not needed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.legacy_renderers import _render_watchlist_page

plugin = LegacyPageAdapter(
    key="watchlist",
    icon="📋",
    category=PluginCategory.TOOL,
    requires_stock_id=False,
    requires_data=False,
    render_fn=_render_watchlist_page,
    order=10,
)
```

### 4B. Stock page (data only) — e.g. `operation_checkup/plugin.py`

```python
"""
src/plugins/operation_checkup/plugin.py
Phase 2: LegacyPageAdapter for operation_checkup (stock page, data only).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.legacy_renderers import _render_operation_checkup

plugin = LegacyPageAdapter(
    key="operation_checkup",
    icon="🔧",
    category=PluginCategory.ANALYSIS,
    requires_stock_id=True,
    requires_data=True,
    render_fn=_render_operation_checkup,
    order=20,
)
```

### 4C. Stock page (data + client) — e.g. `business_card/plugin.py`

```python
"""
src/plugins/business_card/plugin.py
Phase 2: LegacyPageAdapter for business_card (stock page, data + client).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.legacy_renderers import _render_business_card

plugin = LegacyPageAdapter(
    key="business_card",
    icon="🏢",
    category=PluginCategory.ANALYSIS,
    requires_stock_id=True,
    requires_data=True,
    render_fn=_render_business_card,
    order=10,
)
```

### 4D. Special case: `daily_story` with wrapper

```python
"""
src/plugins/daily_story/plugin.py
Phase 2: LegacyPageAdapter for daily_story (standalone, uses wrapper to adapt fn).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.legacy_renderers import render_investor_story_feed

def _render_daily_story_adapter(client):
    """Adapter: daily_story's render fn takes (data, client) but data is unused."""
    render_investor_story_feed({}, client)

plugin = LegacyPageAdapter(
    key="daily_story",
    icon="📰",
    category=PluginCategory.LEARN,
    requires_stock_id=False,
    requires_data=False,
    render_fn=_render_daily_story_adapter,
    order=70,
)
```

---

## 5. Migration Checklist

### Per-Page Checklist

For each page, the following must be completed:

- [ ] Create `src/plugins/<page_key>/plugin.py` using the appropriate template
- [ ] Move render logic from `src/pages/` to the plugin (or use `LegacyPageAdapter`)
- [ ] Update `router.py` to use `registry.get(page_key).render(ctx)` instead of if-elif
- [ ] Remove the if-elif branch from `router.py`
- [ ] Remove the import from `router.py`
- [ ] Remove the key from `PAGE_KEYS` list
- [ ] Run `pytest tests/ -x` to verify
- [ ] Run `bash scripts/verify.sh` to verify

### Global Checklist (after all pages migrated)

- [ ] Remove all if-elif branches from `router.py`
- [ ] Remove all page imports from `router.py`
- [ ] Remove `PAGE_KEYS` list from `router.py`
- [ ] Update `url_sync.py` `VALID_PAGES` to use `registry.all_keys`
- [ ] Update `main.py` sidebar nav_items to use `registry.get_by_category()`
- [ ] Run full test suite
- [ ] Run `bash scripts/verify.sh`

---

## 6. Rollback Plan

If any wave fails verification:

1. Revert `router.py` to use the original if-elif branch for the failing page
2. Keep the plugin file (it doesn't break anything if not registered)
3. Document the failure in `docs/state/current_problems.md`
4. Re-attempt in the next session

---

## 7. Related Documents

- [ADR-004: Plugin Chassis Architecture](./004-plugin-chassis.md)
- `src/core/plugin_protocol.py` — Plugin protocol definition
- `src/core/plugin_registry.py` — Plugin registry implementation
- `src/pages/router.py` — Router to be refactored
- `docs/state/current_problems.md` — Known issues log
