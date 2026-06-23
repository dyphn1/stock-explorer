# ADR 011: ETF Page Architecture

## Status
Accepted

## Context
Stock Explorer currently renders ETF detail pages via a legacy rendering function (`_render_etf_detail` in `src/pages/etf_detail.py`) that is invoked directly from the router when an ETF is detected. This bypasses the PluginRegistry, causing scattered routing logic and making it difficult to maintain a consistent user experience across security types. User feedback indicates that ETFs should not have the same features as stocks, as ETFs have distinct characteristics such as expense ratios, tracking error, holdings diversification, and creation/redemption mechanisms.

The application follows a strict layered architecture (Data → Service → Router → Presentation) and uses a Plugin Chassis where all pages are registered as plugins. To align with this architecture and address the feedback, the ETF detail page should be implemented as a Plugin.

## Decision
Implement the ETF detail page as a Plugin under `src/plugins/etf_detail/` that adheres to the `BasePlugin` interface (or uses `LegacyPageAdapter` for migration). The plugin will be registered with the key `"etf_detail"` and included in the `_STOCK_PLUGIN_KEYS` set in `router.py`. The special `if _is_etf_check:` branch in `router.load_and_render_page` will be removed, allowing the PluginRegistry to handle routing uniformly.

The plugin will receive a data dictionary containing both standard fields (price, name, industry) and ETF‑specific fields (expense ratio, tracking error, AUM, holdings, sector allocation, etc.) and will render ETF‑focused sections while reusing shared UI components (price ticker, chart, watchlist, feedback, etc.) from the existing component library.

## Consequences

### Positive
- **Uniform Routing**: All pages, including ETF detail, follow the same plugin‑based routing path, reducing scattered conditional logic.
- **Reduced Duplication**: Shared UI components (price ticker, chart, watchlist, feedback) are reused, eliminating redundant `st.*` calls.
- **Consistent UX**: Navigation, layout, and interaction patterns remain identical across stocks and ETFs, lowering cognitive load.
- **Simplified Maintenance**: Updates to shared components (e.g., a new chart type) automatically propagate to the ETF page.
- **Independent Deployability**: The ETF plugin can be enabled/disabled via the plugin registry without affecting other pages.
- **Alignment with Plugin Chassis**: Reinforces the architectural goal that features are added/removed by registering/unregistering plugins.

### Negative
- **Data Requirements**: ETF‑specific fields (expense ratio, holdings, etc.) may not be fully supplied by the existing FinMind client. This may require extending the data layer or creating an auxiliary ETF service.
- **Performance Impact**: Fetching holdings data for many ETFs could be costly; mitigation includes caching and lazy‑loading heavy sections.
- **Initial Effort**: Migrating the existing rendering logic to a plugin requires careful refactoring to preserve functionality and i18n keys.

### Implementation Plan
1. Create `src/plugins/etf_detail/plugin.py` (and `__init__.py` if needed) implementing `BasePlugin` or extending `LegacyPageAdapter`.
2. Move and adapt the rendering logic from `src/pages/etf_detail.py` into the plugin’s `render` method, replacing direct `st.*` calls with shared UI primitives where appropriate.
3. Register the plugin in its `plugin.py` file.
4. Add `"etf_detail"` to `_STOCK_PLUGIN_KEYS` in `router.py`.
5. Remove the `_is_etf_check` conditional block from `router.load_and_render_page`.
6. Ensure the plugin declares `requires_stock_id=True` and `requires_data=True`.
7. Add or update i18n entries in `locales/zh-TW.yaml` and `locales/en.yaml` for keys under `etf.detail.*`.
8. Write unit tests for the plugin using mock data.
9. Run the full test suite to verify no regressions.

### Related ADRs
- ADR 001: Plugin Chassis Architecture (if exists)
- ADR 005: Layered Architecture (if exists)

### Acceptance Criteria
- The ETF detail page is rendered via the PluginRegistry.
- The page displays ETF‑specific sections (fund overview, expense structure, tracking metrics, holdings analysis, dividend/distribution, risk/volatility, liquidity, cost of ownership, etc.).
- Shared components (price ticker, chart, watchlist, feedback) are identical to those used on the stock business_card page.
- No conditional bypass for ETFs remains in the router.
- All UI strings are internationalized via `t()`.