# Handoff — Stock Explorer

> **Last Updated**: 2026-06-20

## Current State
- **Tests**: 699/699 pass
- **i18n (TD-02)**: Complete — zero hardcoded Chinese in `src/`
- **Code Quality**: Color system unified (TD-06), component consistency (TD-07), API caching (TD-03)

## Completed
- TD-01: Plugin Chassis — all 24 pages on PluginRegistry
- TD-02: i18n — all `src/` UI strings use `t()`
- TD-03: API caching — `get_stock_info` has LRU cache
- TD-04: business_card.py split into submodules
- TD-06: Color system unified across all `src/` files
- TD-07: Component consistency — no bare `st.metric()` calls
- BUG-001: dividend.* locale keys added
- UX-01: Chinese stock name search
- UX-05: ROE TTM fix
- UX-07: Watchlist toast feedback
- C170: Clickable Glossary
- C188: Why Did This Move?
- C204: Confidence Indicator
- C205: Reading Time Indicator
- D-125: chart_stock.py split

## Not Done (True P1 Backlog)
- **SB-01~03**: Sidebar core — NOT STARTED
- **SB-05~08**: Sidebar improvements — NOT STARTED
- **ADR-009**: Two-layer navigation — NOT STARTED
- **UX-02**: Page transition spinner — Open
- **UX-14**: Watchlist concurrent write (filelock) — Open
- **TD-05**: Test coverage improvement — NOT STARTED

## Next Steps
1. **SB-01~03 Sidebar core** — highest priority P1
2. **ADR-009 Two-layer navigation** — P1
3. **UX-02 Page spinner** — P1 quick win
4. **UX-14 Watchlist concurrency** — P2
5. **TD-05 Test coverage** — P1
