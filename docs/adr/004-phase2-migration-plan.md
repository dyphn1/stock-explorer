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
└── daily_story/
    └── plugin.py
```

**Key principle:** Each plugin directory contains ONLY `plugin.py`. The actual page rendering logic STAYS in `src/pages/*.py` — we do NOT move the page source files, we only create thin adapter wrappers. This is the same pattern as Phase 1.

---

## 3. Migration Order

### Wave 1: Simple Standalone Pages (client-only signature)
These use `(client)` → `client_only` adapter path. Highest confidence, lowest risk.

| Order | page_key | Signature | Reason |
|-------|----------|-----------|--------|
| 1 | `watchlist` | `(client)` | Simple, commonly used |
| 2 | `investment_memo` | `(client)` | Independent tool |
| 3 | `etf_section` | `(client)` | Browser page |
| 4 | `case_study` | `(client)` | Learning content |
| 5 | `financial_wellness` | `(client)` | Tool page |
| 6 | `comprehension_check` | `(client)` | Quiz page |
| 7 | `case_study_library` | `(client)` | Library browser |
| 8 | `stock_screener` | `(client)` | Screening tool |
| 9 | `sector_heatmap` | `(client)` | Visualization |
| 10 | `learn_first_gate` | `(client)` | Gate/tutorial |
| 11 | `first_visit_guide` | `(client)` | Onboarding |
| 12 | `daily_story` | `(client)` (wrapper) | See special handling above |

### Wave 2: Data-Only Stock Pages (data signature)
These use `(data)` → `data_only` adapter path. Need stock_id + data loading.

| Order | page_key | Signature | Reason |
|-------|----------|-----------|--------|
| 13 | `operation_checkup` | `(data)` | Simple analysis page |
| 14 | `financial_health` | `(data)` | Common analysis page |
| 15 | `group_structure` | `(data)` | Structure visualization |

### Wave 3: Full Stock Pages (data, client signature)
These use `(data, client)` → `data_client` adapter path. Most complex rendering.

| Order | page_key | Signature | Reason |
|-------|----------|-----------|--------|
| 16 | `business_card` | `(data, client)` | Highest traffic page — migrate early to validate |
| 17 | `peer_comparison` | `(data, client)` | Comparison tool |
| 18 | `story_timeline` | `(data, client)` | Timeline viz |
| 19 | `full_story_timeline` | `(data, client)` | Extended timeline |
| 20 | `revenue_tree` | `(data, client)` | Tree visualization |
| 21 | `compare_stories` | `(data, client)` | Story comparison |
| 22 | `moat_comparison` | `(data, client)` | Moat analysis |
| 23 | `debate_cards` | `(data, client)` | Debate cards |

**Rationale for ordering:**
- Wave 1 first: All standalone pages with `(client)` signature are mechanically identical to the 5 already-migrated Phase 1 pages. This builds confidence in the pattern.
- Wave 2 second: `(data)` stock pages are simpler than `(data, client)` — they don't need client for API calls during render.
- Wave 3 last: `(data, client)` pages are the most complex. `business_card` (#16) is first because it's the default/highest-traffic page and serves as the标杆 (benchmark).
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
from src.pages.watchlist_page import _render_watchlist_page

registered_plugin = LegacyPageAdapter(
    key="watchlist",
    icon="📋",
    category=PluginCategory.TOOL,
    render_fn=_render_watchlist_page,
    requires_stock_id=False,
    requires_data=False,
    order=10,
)
```

### 4B. Data-only stock page — e.g. `operation_checkup/plugin.py`

```python
"""
src/plugins/operation_checkup/plugin.py
Phase 2: LegacyPageAdapter for operation_checkup (stock data page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.operation_checkup import _render_operation_checkup

registered_plugin = LegacyPageAdapter(
    key="operation_checkup",
    icon="🔧",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_operation_checkup,
    requires_stock_id=True,
    requires_data=True,
    order=20,
)
```

### 4C. Full stock page — e.g. `business_card/plugin.py`

```python
"""
src/plugins/business_card/plugin.py
Phase 2: LegacyPageAdapter for business_card (stock data + client page).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.business_card._main import _render_business_card

registered_plugin = LegacyPageAdapter(
    key="business_card",
    icon="🏢",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_business_card,
    requires_stock_id=True,
    requires_data=True,
    order=10,
)
```

### 4D. Special case — `daily_story/plugin.py`

```python
"""
src/plugins/daily_story/plugin.py
Phase 2: LegacyPageAdapter for daily_story (wrapper for investor_story_feed).
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.investor_story_feed import render_investor_story_feed


def _render_daily_story_adapter(client):
    """Adapter: render_investor_story_feed expects (data, client) but data is unused."""
    render_investor_story_feed({}, client)


registered_plugin = LegacyPageAdapter(
    key="daily_story",
    icon="📰",
    category=PluginCategory.LEARN,
    render_fn=_render_daily_story_adapter,
    requires_stock_id=False,
    requires_data=False,
    order=70,
)
```

### 4E. Special case — `story_timeline/plugin.py`

Note: `story_timeline` maps to `render_company_timeline` (not `render_story_timeline_page`).

```python
"""
src/plugins/story_timeline/plugin.py
Phase 2: LegacyPageAdapter for story_timeline.
Note: render_fn is render_company_timeline from src/pages/company_timeline.py.
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.company_timeline import render_company_timeline

registered_plugin = LegacyPageAdapter(
    key="story_timeline",
    icon="📅",
    category=PluginCategory.ANALYSIS,
    render_fn=render_company_timeline,
    requires_stock_id=True,
    requires_data=True,
    order=60,
)
```

### 4F. Special case — `full_story_timeline/plugin.py`

Note: `full_story_timeline` maps to `render_story_timeline_page`.

```python
"""
src/plugins/full_story_timeline/plugin.py
Phase 2: LegacyPageAdapter for full_story_timeline.
"""

from src.core.plugin_protocol import PluginCategory
from src.core.plugin_registry import LegacyPageAdapter
from src.pages.story_timeline import render_story_timeline_page

registered_plugin = LegacyPageAdapter(
    key="full_story_timeline",
    icon="📆",
    category=PluginCategory.ANALYSIS,
    render_fn=render_story_timeline_page,
    requires_stock_id=True,
    requires_data=True,
    order=65,
)
```

---

## 5. Changes to router.py

### 5A. Phase 2 Strategy: Expand `_PHASE1_PLUGIN_KEYS` → `_ALL_PLUGIN_KEYS`

After all 23 new plugins are created, the `_PHASE1_PLUGIN_KEYS` set should be replaced with a comprehensive set that includes ALL plugin-managed pages. The router's `load_and_render_page()` function should be restructured:

**Current structure (Phase 1):**
```python
# Phase 1: Try plugin registry first for standalone pages
if page_key in _PHASE1_PLUGIN_KEYS:
    _render_navbar_minimal(page_key)
    with st.spinner(t("status.loading_page")):
        rendered = _render_via_plugin(page_key, client)
    ...
    return

# Legacy standalone pages (not yet migrated)
if page_key == "etf_section": ...
if page_key == "watchlist": ...
...

# Stock-dependent pages
...
if page_key == "business_card": ...
elif page_key == "operation_checkup": ...
...
```

**Target structure (Phase 2 complete):**
```python
def load_and_render_page(client: FinMindClient, stock_id: str):
    page_key = st.session_state.get("page_key", "business_card")

    # Try plugin registry for ALL pages
    registry = _get_registry()
    if registry.has(page_key):
        plugin = registry.get(page_key)
        
        # Standalone pages (no stock_id needed)
        if not plugin.metadata.requires_stock_id:
            _render_navbar_minimal(page_key)
            with st.spinner(t("status.loading_page")):
                ctx = PluginRenderContext(
                    page_key=page_key,
                    data=None,
                    client=client,
                    stock_id=None,
                    session_state=st.session_state,
                )
                plugin.render(ctx)
            return
        
        # Stock-dependent pages
        with st.spinner(t("status.loading_stock")):
            data = get_stock_data(client, stock_id)
        if data is None:
            st.error(t("error.not_found", sid=stock_id))
            return
        
        # M5 event detection
        _run_m5_event_detection(stock_id, data)
        
        # ETF redirect
        if _is_etf_check(stock_id, data["stock_name"], data["industry"]):
            _render_navbar(data, page_key)
            with st.spinner(t("status.loading_page")):
                etf_ctx = PluginRenderContext(
                    page_key="etf_detail",
                    data=data,
                    client=client,
                    stock_id=stock_id,
                    session_state=st.session_state,
                )
                registry.get("etf_detail").render(etf_ctx)
            return
        
        _render_navbar(data, page_key)
        with st.spinner(t("status.loading_page")):
            ctx = PluginRenderContext(
                page_key=page_key,
                data=data,
                client=client,
                stock_id=stock_id,
                session_state=st.session_state,
            )
            plugin.render(ctx)
        return

    # Fallback: page not found in registry (should not happen after full migration)
    logger.error("Page key '%s' not found in PluginRegistry.", page_key)
    st.error(t("error.page_not_found", page=page_key))
```

### 5B. Incremental Migration Approach (Recommended)

Rather than a big-bang change, migrate incrementally:

1. **For each standalone page:** Add its key to `_PHASE1_PLUGIN_KEYS` (or rename to `_PLUGIN_MANAGED_KEYS`). The existing `if page_key in _PHASE1_PLUGIN_KEYS` block handles it. Remove the corresponding `if page_key == "...":` block.

2. **For each stock-dependent page:** Add a check BEFORE the stock data loading section:
   ```python
   # After M5 event detection, before the if-elif chain:
   if page_key in _STOCK_PLUGIN_KEYS:
       _render_navbar(data, page_key)
       with st.spinner(t("status.loading_page")):
           rendered = _render_via_plugin(page_key, client, stock_id, data)
       if rendered:
           return
   ```
   Then remove the corresponding `elif page_key == "...":` branch.

3. **Final cleanup:** Once all pages are migrated, remove the if-elif chain entirely and restructure as shown in 5A.

### 5C. Import Changes

**Remove from router.py imports (after full migration):**
```python
# These imports become unnecessary:
from src.pages.business_card import _render_business_card
from src.pages.revenue_tree import _render_revenue_tree
from src.pages.compare_stories import _render_compare_stories_page
from src.pages.moat_comparison import _render_moat_comparison_page
from src.pages.operation_checkup import _render_operation_checkup
from src.pages.financial_health import _render_financial_health
from src.pages.peer_comparison import _render_peer_comparison
from src.pages.group_structure import _render_group_structure
from src.pages.etf_browser import _render_etf_browser
from src.pages.etf_detail import _render_etf_detail
from src.pages.watchlist_page import _render_watchlist_page
from src.pages.sector_heatmap import _render_sector_heatmap
from src.pages.investment_memo import _render_investment_memo
from src.pages.financial_wellness import _render_financial_wellness
from src.pages.comprehension_check import _render_comprehension_check
from src.pages.market_event_case_study import _render_market_event_case_study
from src.pages.stock_screener import _render_stock_screener
from src.pages.first_visit_guide import _render_first_visit_guide
from src.pages.learn_first_gate import _render_learn_first_gate
from src.pages.company_timeline import render_company_timeline
from src.pages.story_timeline import render_story_timeline_page
from src.pages.debate_cards import render_debate_cards_page
from src.pages.academy import _render_academy
from src.pages.case_study_library import _render_case_study_library
from src.pages.investor_story_feed import render_investor_story_feed
```

**Keep in router.py:**
- `get_stock_data` from `_router_base`
- `navigate_to` from `url_sync`
- `_render_adaptive_banner`, `_render_event_alerts` from `event_dashboard` (M5 features)
- `run_auto_detection` from `adaptive_engine`
- i18n functions
- `_is_etf_check`
- Plugin infrastructure imports

### 5D. PAGE_KEYS Handling

The `PAGE_KEYS` list in `router.py` is used for i18n label generation. After full migration, this should be derived from the registry:

```python
# Replace static PAGE_KEYS with dynamic registry lookup
def _get_page_keys():
    registry = _get_registry()
    return registry.all_keys
```

However, `PAGE_KEYS` is currently a module-level constant used by `_get_localized_page_labels()` and `_get_label_to_key_map()`. These are called at module level for the navbar. **Recommendation:** Keep `PAGE_KEYS` as-is during migration (it's harmless), and replace it in Phase 4 (cleanup).

---

## 6. Risk Assessment

### Risk 1: Signature Mismatch in LegacyPageAdapter
**Severity:** High | **Likelihood:** Medium

The `LegacyPageAdapter._validate_signature()` uses `inspect.signature()` to count positional parameters. If a render function has `*args`, `**kwargs`, or default parameters, the validation may misclassify it.

**Mitigation:**
- All 23 target functions have been verified to have clean signatures (see Section 1).
- The adapter validates at construction time (in `plugin.py`), so any mismatch is caught at import time — before the page is even rendered.
- For `daily_story`, we use a wrapper function to avoid the `(data, client)` vs `requires_data=False` conflict.

### Risk 2: Navbar Rendering Differences
**Severity:** Medium | **Likelihood:** Medium

Currently, standalone pages use `_render_navbar_minimal(page_key)` and stock pages use `_render_navbar(data, page_key)`. The router must correctly call the right navbar function for each page type.

**Mitigation:**
- The `plugin.metadata.requires_stock_id` flag determines which navbar to use.
- In the target architecture, the check `if not plugin.metadata.requires_stock_id` cleanly separates the two paths.

### Risk 3: M5 Event Detection & ETF Redirect
**Severity:** High | **Likelihood:** Low

The M5 event detection (`run_auto_detection`, `_render_adaptive_banner`, `_render_event_alerts`) and ETF redirect logic currently live in the stock-dependent section of `router.py`. This logic must continue to work for all stock-dependent plugins.

**Mitigation:**
- Keep M5 event detection and ETF redirect in `router.py` as middleware — they run BEFORE the plugin render call.
- This is the correct architectural position: cross-cutting concerns belong in the router, not in individual plugins.
- The ETF detail page (`_render_etf_detail`) should also be migrated to a plugin.

### Risk 4: session_state Access
**Severity:** Medium | **Likelihood:** Low

Some render functions may access `st.session_state` directly. The `PluginRenderContext` provides `session_state` as a field, but existing functions don't use it — they call `st.session_state` directly.

**Mitigation:**
- No change needed: existing render functions continue to use `st.session_state` directly. The `LegacyPageAdapter` doesn't intercept or modify session_state access.
- This is a known technical debt item for future refactoring (Phase 4+), not a blocking issue.

### Risk 5: Import Side Effects
**Severity:** Medium | **Likelihood:** Low

When `PluginRegistry.discover()` imports `plugin.py` modules, those modules import from `src/pages/*.py`. If any page module has side effects at import time (e.g., Streamlit calls), this could cause issues.

**Mitigation:**
- Phase 1 already validated this pattern with 5 pages — no import side effects were observed.
- All `src/pages/*.py` files use function-level Streamlit calls, not module-level.

### Risk 6: i18n Page Key Mismatch
**Severity:** Low | **Likelihood:** Low

The `PAGE_KEYS` list must match the keys used in locale files under `page:` section. If a plugin uses a key that doesn't have a locale entry, `t(f"page.{key}")` will return the key itself (fallback behavior).

**Mitigation:**
- All 28 page keys already exist in `PAGE_KEYS` and have locale entries (the app is already using them).
- No new keys are being introduced.

### Risk 7: Concurrent Migration Conflicts
**Severity:** Medium | **Likelihood:** Medium

If multiple developers migrate pages simultaneously, merge conflicts in `router.py` are likely.

**Mitigation:**
- Migrate sequentially in the order specified (Wave 1 → Wave 2 → Wave 3).
- Each wave can be a separate PR.
- The `_PHASE1_PLUGIN_KEYS` set (or incremental additions) provides a clear coordination mechanism.

---

## 7. Testing Strategy

### 7A. Unit Tests (per plugin)

For each new plugin, add a test in `tests/test_plugin_chassis.py` (or a new `test_plugins.py`):

```python
class TestPluginExists:
    """Verify each plugin is discoverable and has correct metadata."""
    
    @pytest.mark.parametrize("key,expected_category,expected_requires_stock", [
        ("business_card", "analysis", True),
        ("watchlist", "tool", False),
        # ... all 23 new plugins
    ])
    def test_plugin_registered(self, key, expected_category, expected_requires_stock):
        registry = _get_registry()
        assert registry.has(key), f"Plugin '{key}' not found in registry"
        plugin = registry.get(key)
        assert plugin.metadata.category == expected_category
        assert plugin.metadata.requires_stock_id == expected_requires_stock
```

### 7B. Adapter Signature Tests

For each plugin, verify the adapter correctly dispatches:

```python
class TestAdapterDispatch:
    """Verify LegacyPageAdapter correctly dispatches to render_fn."""
    
    def test_data_client_dispatch(self):
        """(data, client) signature: both args passed through."""
        calls = []
        def mock_render(data, client):
            calls.append((data, client))
        
        adapter = LegacyPageAdapter(
            key="test", icon="📊", category="analysis",
            render_fn=mock_render, requires_data=True,
        )
        data = {"stock_id": "2330"}
        client = MagicMock()
        ctx = PluginRenderContext(page_key="test", data=data, client=client, stock_id="2330")
        adapter.render(ctx)
        
        assert len(calls) == 1
        assert calls[0] == (data, client)
    
    def test_data_only_dispatch(self):
        """(data) signature: only data passed."""
        # Similar pattern...
    
    def test_client_only_dispatch(self):
        """(client) signature: only client passed."""
        # Similar pattern...
    
    def test_data_none_warning(self):
        """Adapter logs warning and skips render when data is None but required."""
        calls = []
        def mock_render(data, client):
            calls.append((data, client))
        
        adapter = LegacyPageAdapter(
            key="test", icon="📊", category="analysis",
            render_fn=mock_render, requires_data=True,
        )
        ctx = PluginRenderContext(page_key="test", data=None, client=MagicMock(), stock_id="2330")
        adapter.render(ctx)
        
        assert len(calls) == 0  # Should not render
```

### 7C. Integration Tests

After each wave, run the full test suite:

```bash
uv run python -m pytest tests/ -v
```

### 7D. Manual Verification Checklist

For each migrated page, verify:

- [ ] Page loads without errors in Streamlit
- [ ] Navigation bar renders correctly (minimal for standalone, full for stock pages)
- [ ] Page content renders identically to pre-migration
- [ ] Switching between pages works (navbar radio buttons)
- [ ] Browser back/forward buttons work (URL sync)
- [ ] For stock pages: M5 event detection still runs
- [ ] For stock pages: ETF redirect still works
- [ ] i18n labels display correctly

### 7E. Regression Test Script

Create a script that verifies all pages are registered:

```python
# tests/test_all_pages_registered.py
def test_all_pages_have_plugins():
    """Every page key in PAGE_KEYS must have a corresponding plugin."""
    from src.pages.router import PAGE_KEYS
    registry = _get_registry()
    
    missing = [key for key in PAGE_KEYS if not registry.has(key)]
    assert not missing, f"Pages missing from PluginRegistry: {missing}"
```

---

## 8. Implementation Checklist

### Wave 1: Standalone Pages (12 plugins)

- [ ] `watchlist/plugin.py`
- [ ] `investment_memo/plugin.py`
- [ ] `etf_section/plugin.py`
- [ ] `case_study/plugin.py`
- [ ] `financial_wellness/plugin.py`
- [ ] `comprehension_check/plugin.py`
- [ ] `case_study_library/plugin.py`
- [ ] `stock_screener/plugin.py`
- [ ] `sector_heatmap/plugin.py`
- [ ] `learn_first_gate/plugin.py`
- [ ] `first_visit_guide/plugin.py`
- [ ] `daily_story/plugin.py` (with wrapper)
- [ ] Update `router.py`: add Wave 1 keys to plugin set, remove legacy standalone blocks
- [ ] Run tests + manual verification

### Wave 2: Data-Only Stock Pages (3 plugins)

- [ ] `operation_checkup/plugin.py`
- [ ] `financial_health/plugin.py`
- [ ] `group_structure/plugin.py`
- [ ] Update `router.py`: add Wave 2 keys to plugin stock set, remove elif branches
- [ ] Run tests + manual verification

### Wave 3: Full Stock Pages (8 plugins)

- [ ] `business_card/plugin.py`
- [ ] `peer_comparison/plugin.py`
- [ ] `story_timeline/plugin.py`
- [ ] `full_story_timeline/plugin.py`
- [ ] `revenue_tree/plugin.py`
- [ ] `compare_stories/plugin.py`
- [ ] `moat_comparison/plugin.py`
- [ ] `debate_cards/plugin.py`
- [ ] Update `router.py`: add Wave 3 keys, remove all remaining elif branches
- [ ] Run tests + manual verification

### Phase 4: Cleanup

- [ ] Remove all page-specific imports from `router.py`
- [ ] Remove `_render_standalone_page_legacy()` function
- [ ] Remove `_PHASE1_PLUGIN_KEYS` / `_STOCK_PLUGIN_KEYS` sets (replace with direct `registry.has()` check)
- [ ] Refactor `load_and_render_page()` to the clean target structure (Section 5A)
- [ ] Update `url_sync.py` `VALID_PAGES` to use registry (or keep as-is for URL validation)
- [ ] Update `main.py` sidebar `nav_items` to use registry
- [ ] Add `test_all_pages_registered` regression test
- [ ] Full test suite + manual regression

---

## 9. Summary

| Metric | Value |
|--------|-------|
| Total pages to migrate | 23 (28 total − 5 Phase 1) |
| Stock-dependent pages | 11 |
| Standalone pages | 12 (incl. daily_story wrapper) |
| `(data, client)` signatures | 8 |
| `(data)` signatures | 3 |
| `(client)` signatures | 11 |
| `()` signatures | 0 (settings already done) |
| Special wrapper needed | 1 (daily_story) |
| Estimated waves | 3 |
| New plugin directories | 23 |
| Lines removed from router.py | ~120 (if-elif blocks) |
| Lines removed from router.py imports | ~23 |
