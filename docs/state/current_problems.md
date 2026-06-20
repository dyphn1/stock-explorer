# Current Problems — Stock Explorer

> **Last Updated**: 2026-06-20
> **Maintainer**: PM Agent

## P1 — High Priority

### SB-01~03: Sidebar Core — NOT STARTED
- **Type**: Feature / Architecture
- **Reported**: 2026-06-20
- **Description**: Sidebar with inline data, multiple watchlists, market overview — not implemented
- **Affected**: `src/pages/`, `src/core/`
- **Status**: Open

### ADR-009: Two-Layer Navigation — NOT STARTED
- **Type**: Architecture
- **Reported**: 2026-06-20
- **Description**: Activity Bar + FAB navigation architecture — not implemented
- **Affected**: `src/pages/router.py`, `src/main.py`
- **Status**: Open

### UX-02: Page Transition Spinner
- **Type**: UX / Visual Feedback
- **Reported**: 2026-06-18
- **Description**: No loading indicator when switching pages
- **Affected**: `src/pages/router.py`
- **Status**: Open

### TD-05: Test Coverage Improvement
- **Type**: Tech Debt / Quality
- **Reported**: 2026-06-20
- **Description**: 699 tests pass but coverage is insufficient — need more edge case and integration tests
- **Affected**: `tests/`
- **Status**: Open

## P2 — Medium Priority

### UX-14: Watchlist Concurrent Write
- **Type**: Bug / Data Integrity
- **Reported**: 2026-06-18
- **Description**: Multiple sessions writing watchlist.yaml simultaneously may corrupt file
- **Affected**: `src/services/watchlist.py`
- **Status**: Open
- **Solution**: Add filelock for concurrent write control
