# ADR-004: Plugin Chassis Architecture

## Status
Planned → **Approved (Pending Implementation)**

## Date
2026-06-14 → **Updated: 2026-06-18**

---

## Background

`src/pages/router.py` is currently **355 lines** with **33 if-elif branches**. Adding a page requires modifying **3 places**:

1. Add an `import` statement
2. Add the key to the `PAGE_KEYS` list
3. Add an if-elif branch in `load_and_render_page()`

This severely violates the **Open-Closed Principle**: open for extension, but not closed for modification.

Additionally, the current architecture has the following problems:
- All page functions are concentrated in `src/pages/`, making it hard to distinguish between "pages that require stock data" and "standalone pages"
- Navigation rendering logic (`_render_navbar`, `_render_navbar_minimal`) is coupled with routing logic
- Cannot dynamically enable/disable pages (feature flag)
- Easy to miss a modification when adding a new page, causing runtime errors

---

## Decision

Design each page as an independent **Plugin** following a unified protocol, with the core framework automatically scanning, registering, and routing.

**Core principle: Adding a page = adding a plugin directory, zero modifications to routing logic.**

---

## Target Architecture

```
src/
├── core/                           # Core framework layer
│   ├── i18n.py                     # i18n module (existing)
│   ├── plugin_protocol.py          # Plugin interface definition (new)
│   └── plugin_registry.py          # Plugin registry (new)
│
├── plugins/                        # Plugin directory (new, replaces routing function of pages/)
│   ├── __init__.py                 # Package marker
│   ├── business_card/              # Business card
│   │   ├── plugin.py               # BusinessCardPlugin(BasePlugin)
│   │   └── ...                     # Original rendering logic (migrated from pages/)
│   ├── operation_checkup/          # Operation checkup
│   │   └── plugin.py
│   ├── financial_health/           # Financial health
│   │   └── plugin.py
│   ├── category_browser/           # Category browser (standalone page, no stock_id needed)
│   │   └── plugin.py
│   └── ...                         # Other pages
│
├── pages/                          # View layer (gradually migrating)
│   ├── router.py                   # Page router (refactored to use PluginRegistry)
│   ├── _router_base.py             # Shared utilities (kept)
│   ├── url_sync.py                 # URL ↔ session sync (kept)
│   └── *.py                        # Original page files (removed after migration)
│
├── services/                       # Business logic layer (unchanged)
└── data/                           # Data layer (unchanged)
```

---

## Plugin Protocol Design

### PluginMetadata

```python
@dataclass(frozen=True)
class PluginMetadata:
    key: str                    # Unique identifier (maps to i18n key: page.<key>)
    icon: str                   # Icon (emoji)
    requires_stock_id: bool     # Whether stock_id is required
    requires_data: bool         # Whether pre-loaded data dict is required
    category: str               # Category: analysis | browse | tool | learn | system
    order: int                  # Sort weight (smaller = earlier)
    enabled: bool               # Whether enabled (feature flag)
```

### PluginRenderContext

```python
@dataclass
class PluginRenderContext:
    page_key: str
    data: dict | None           # Pre-loaded stock data
    client: FinMindClient
    stock_id: str | None
```

### BasePlugin (Abstract Base Class)

```python
class BasePlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata: ...

    @abstractmethod
    def render(self, ctx: PluginRenderContext) -> None: ...

    def can_render(self, ctx: PluginRenderContext) -> bool:
        """Default implementation: check if stock_id / data requirements are met"""
        ...
```

### Category Constants

| Category | Description | Example Pages |
|----------|-------------|---------------|
| `analysis` | Stock analysis | Business card, operation checkup, financial health, peer comparison |
| `browse` | Browsing | Category browser, ETF section, sector heatmap |
| `tool` | Tools | Stock screener, investment memo, financial wellness check |
| `learn` | Learning | Academy, case studies, comprehension quiz |
| `system` | System | Settings, notification center, event dashboard |

---

## PluginRegistry Design

### Auto-Discovery Strategy

```
PluginRegistry.discover()
    → Traverse all subdirectories under src/plugins/
    → Find plugin.py in each subdirectory
    → Import module, find all BasePlugin subclasses
    → Instantiate and register to _plugins: dict[str, BasePlugin]
```

### Core API

```python
registry = PluginRegistry()
registry.discover()                          # Auto-scan, returns count of newly registered
registry.get("business_card")                # Find plugin by key
registry.has("business_card")                # Check if exists
registry.all_keys                            # List of all registered keys
registry.all_plugins                         # All plugins (sorted by category + order)
registry.get_by_category("analysis")         # Get by category
```

### LegacyPageAdapter (Backward Compatibility)

During the migration transition period, existing `_render_*` functions can be wrapped as Plugins without immediate refactoring:

```python
adapter = LegacyPageAdapter(
    key="business_card",
    icon="🏢",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_business_card,
    order=10,
)
registry.register(adapter)
```

---

## Refactored router.py

Pseudo-code for the refactored `load_and_render_page()`:

```python
def load_and_render_page(client: FinMindClient, stock_id: str):
    page_key = st.session_state.get("page_key", "business_card")

    # Find plugin from registry
    plugin = registry.get(page_key)

    # Build render context
    ctx = PluginRenderContext(
        page_key=page_key,
        data=None,
        client=client,
        stock_id=stock_id,
    )

    # Standalone pages (no stock_id needed): render directly
    if not plugin.metadata.requires_stock_id:
        _render_navbar_minimal(page_key)
        plugin.render(ctx)
        return

    # Pages requiring stock_id: load data
    with st.spinner(t("status.loading_stock")):
        data = get_stock_data(client, stock_id)
    if data is None:
        st.error(t("error.not_found", sid=stock_id))
        return

    # M5 event detection (unchanged)
    _run_event_detection(stock_id, data)

    # ETF redirect to ETF detail page (unchanged)
    if _is_etf(stock_id, data):
        _render_navbar(data, page_key)
        registry.get("etf_detail").render(ctx)
        return

    # Render navbar + page
    _render_navbar(data, page_key)
    ctx.data = data
    plugin.render(ctx)
```

---

## Migration Plan

### Phase 0: Foundation Skeleton (TD-01a) ✅ Current
**Goal**: Build Plugin Protocol and Registry skeleton, migrate no pages.

- [x] Create `src/core/plugin_protocol.py`
- [x] Create `src/core/plugin_registry.py`
- [x] Create `src/plugins/__init__.py`
- [ ] Update `docs/adr/004-plugin-chassis.md` (this document)

**Risk**: None. Does not affect existing functionality.

### Phase 1: Backward Compatibility Layer (TD-01b)
**Goal**: Wrap existing pages as Plugins using `LegacyPageAdapter`, verify Registry functionality.

Migration order (low risk first):
1. `category_browser` — standalone page, no stock_id needed
2. `settings` — system page, no data dependency
3. `event_dashboard` — standalone page
4. `notification_center` — standalone page
5. `daily_market` — standalone page

**Verification criteria**:
- All 5 pages registered via `LegacyPageAdapter`, navigation and rendering work correctly
- Original `router.py` if-elif branches can be replaced by registry lookups

### Phase 2: Core Analysis Page Migration (TD-01c)
**Goal**: Migrate core stock analysis pages to `src/plugins/` directory.

Migration order (by usage frequency):
1. `business_card` — highest frequency, serves as the benchmark
2. `operation_checkup`
3. `financial_health`
4. `peer_comparison`
5. `group_structure`
6. `story_timeline`
7. `full_story_timeline`
8. `revenue_tree`
9. `compare_stories`
10. `moat_comparison`
11. `debate_cards`

**Migration steps for each page**:
1. Create `src/plugins/<name>/plugin.py`
2. Inherit `BasePlugin`, define `metadata`
3. Move original `_render_*` function logic into `render()` method
4. Update `router.py` to use `registry.get(name).render(ctx)`
5. Run tests to verify

### Phase 3: Browse/Tool/Learn Page Migration (TD-01d)
**Goal**: Migrate remaining pages.

Migration order:
1. `etf_section` / `etf_browser`
2. `watchlist`
3. `investment_memo`
4. `financial_wellness`
5. `stock_screener`
6. `case_study` / `market_event_case_study`
7. `comprehension_check`
8. `academy`
9. `case_study_library`
10. `first_visit_guide`
11. `learn_first_gate`
12. `daily_story` / `investor_story_feed`
13. `sector_heatmap`

### Phase 4: Cleanup (TD-01e)
**Goal**: Remove old code, complete refactoring.

- [ ] Remove all if-elif branches from `router.py`
- [ ] Remove all imports from `router.py` (replaced by registry auto-discovery)
- [ ] Remove `PAGE_KEYS` list (replaced by `registry.all_keys`)
- [ ] Remove migrated `.py` files from `src/pages/`
- [ ] Update `url_sync.py` `VALID_PAGES` (replaced by dynamic registry lookup)
- [ ] Update `main.py` sidebar nav_items (replaced by `registry.get_by_category()`)
- [ ] Full test suite

---

## Page Categories and Ordering

| Key | Category | Order | requires_stock_id | requires_data | Icon |
|-----|----------|-------|-------------------|---------------|------|
| business_card | analysis | 10 | ✅ | ✅ | 🏢 |
| operation_checkup | analysis | 20 | ✅ | ✅ | 🔧 |
| financial_health | analysis | 30 | ✅ | ✅ | 💪 |
| peer_comparison | analysis | 40 | ✅ | ✅ | 👥 |
| group_structure | analysis | 50 | ✅ | ✅ | 🏗️ |
| story_timeline | analysis | 60 | ✅ | ✅ | 📅 |
| full_story_timeline | analysis | 65 | ✅ | ✅ | 📆 |
| revenue_tree | analysis | 70 | ✅ | ✅ | 🌳 |
| compare_stories | analysis | 80 | ✅ | ✅ | 📖 |
| moat_comparison | analysis | 90 | ✅ | ✅ | 🏰 |
| debate_cards | analysis | 100 | ✅ | ✅ | 🃏 |
| category_browser | browse | 10 | ❌ | ❌ | 🗺️ |
| etf_section | browse | 20 | ❌ | ❌ | 🏷️ |
| sector_heatmap | browse | 30 | ❌ | ❌ | 🔥 |
| daily_market | browse | 40 | ❌ | ❌ | 📈 |
| watchlist | tool | 10 | ❌ | ❌ | 📋 |
| investment_memo | tool | 20 | ❌ | ❌ | 📝 |
| financial_wellness | tool | 30 | ❌ | ❌ | 💰 |
| stock_screener | tool | 40 | ❌ | ❌ | 🔎 |
| case_study | learn | 10 | ❌ | ❌ | 📚 |
| comprehension_check | learn | 20 | ❌ | ❌ | ✅ |
| academy | learn | 30 | ❌ | ❌ | 🎓 |
| case_study_library | learn | 40 | ❌ | ❌ | 📖 |
| first_visit_guide | learn | 50 | ❌ | ❌ | 👋 |
| learn_first_gate | learn | 60 | ❌ | ❌ | 🚪 |
| daily_story | learn | 70 | ❌ | ❌ | 📰 |
| event_dashboard | system | 10 | ❌ | ❌ | 📊 |
| notification_center | system | 20 | ❌ | ❌ | 🔔 |
| settings | system | 30 | ❌ | ❌ | ⚙️ |

---

## Rationale

1. **Open-Closed Principle**: Adding functionality doesn't require modifying existing code, just adding a plugin directory
2. **Independent development**: Each plugin can be developed/tested independently, reducing coupling
3. **Dynamic enable/disable**: Feature flags via `metadata.enabled`
4. **Progressive migration**: `LegacyPageAdapter` allows gradual migration, reducing risk
5. **Type safety**: `PluginProtocol` + `BasePlugin` provides static and runtime double checking
6. **Auto-discovery**: No manual registration needed, reducing risk of omissions

## Consequences

### Positive
- ✅ Adding/removing features = adding/removing plugin directory, zero routing logic changes
- ✅ Independent development/testing of individual features
- ✅ Dynamic feature enable/disable (via `enabled` property)
- ✅ Centralized page metadata management (icon, order, category)
- ✅ Navigation auto-generated from registry, eliminating risk of `PAGE_KEYS` and routing getting out of sync

### Risks and Mitigation
- ⚠️ **One-time refactoring cost**: Mitigation: 5-phase progressive migration, each phase independently verifiable
- ⚠️ **Team needs to understand plugin concept**: Mitigation: Provide clear documentation and `LegacyPageAdapter` examples
- ⚠️ **Streamlit session_state coupled with Plugin lifecycle**: Mitigation: `PluginRenderContext` encapsulates all state, plugins don't access session_state directly
- ⚠️ **Auto-scan may import unwanted modules**: Mitigation: Only scan `src/plugins/` directory, each plugin must have `plugin.py`

---

## Related Files

- `src/core/plugin_protocol.py` — Plugin Protocol definition
- `src/core/plugin_registry.py` — Plugin Registry implementation
- `src/plugins/__init__.py` — Plugin directory marker
- `src/pages/router.py` — Router to be refactored
- `docs/overview/02-architecture.md` — System architecture document
- `docs/overview/06-development-guide.md` — Development guide
