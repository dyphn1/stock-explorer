# Architecture Review: Post-i18n Refactoring (Commit 7bcbc00)

> This document reviews the architecture alignment after the i18n refactoring commit (7bcbc00) and notes any observed deviations from the layered architecture defined in `docs/architecture/architecture.md`.

## Summary

The i18n refactoring successfully integrated the `t()` function across user-facing strings in the codebase, moving hardcoded strings to locale YAML files. The refactoring adhered to the layered architecture in the examined components (Story Arc Detector and Story Timeline page). However, some pre-existing architectural deviations were noted in other parts of the codebase.

## Layer Adherence in i18n Refactoring

### Story Arc Detector (`src/services/story_arc_detector.py`)
- **Layer**: Service Layer ✅
- **Compliance**:
  - No Streamlit imports.
  - No direct FinMind API calls; receives `TimelineEntry` objects from the timeline service.
  - Returns i18n keys (not display text), delegating localization to the presentation layer.
  - Pure functions with no side effects.

### Story Timeline Page (`src/pages/story_timeline.py`)
- **Layer**: Presentation Layer ✅
- **Compliance**:
  - Uses Streamlit for UI rendering.
  - Calls the service layer to obtain arc labels (i18n keys).
  - Resolves keys via `t()` function to obtain localized strings.
  - Does not perform business logic (e.g., scoring, classification); delegates to service layer.

### i18n Core (`src/core/i18n.py`)
- **Layer**: Cross-cutting utility (acceptable)
- **Compliance**:
  - Provides `t()` function for localization.
  - Does not import Streamlit (uses `streamlit as st` only for accessing `session_state`, which is acceptable as it is a presentation-state bridge).
  - Locale loading is cached and does not contain business logic.

## Observed Architectural Deviations (Pre-existing)

The following deviations were noted in the codebase and are **not** introduced by the i18n refactoring. They represent areas where the current implementation diverges from the prescribed layered architecture.

### 1. Service Layer Importing Streamlit
- **File**: `src/services/quiz_service.py`
- **Issue**: The service layer imports `streamlit` and uses it for UI components (e.g., `st.popover`). This violates the service layer responsibility of being free of UI concerns.
- **Impact**: Services become tightly coupled to the presentation layer, hindering reusability and testability.

### 2. Service Layer Directly Using FinMindClient
- **Files**: Multiple services (e.g., `src/services/stock_screener_service.py`, `src/services/batch_api.py`, etc.) instantiate and call `FinMindClient` directly.
- **Issue**: The service layer should not directly call the data layer (FinMind API). According to the architecture, data fetching should be uniformly handled by the router layer (`get_stock_data` in `_router_base.py`) or by standalone pages managing their own data loading.
- **Impact**: Duplicated data loading logic, inconsistent caching, and potential bypass of router-layer optimizations (e.g., parallel fetching, rate limit handling).

### 3. View Layer Using Caching Mechanisms
- **Files**: `src/pages/category_browser.py`, `src/pages/router.py` use `st.cache_data` or `st.cache_resource`.
- **Issue**: The architecture explicitly forbids using `st.cache_data` in the view layer due to cross-session sharing issues. Caching should be uniformly managed by the `FinMindClient` in the data layer.
- **Impact**: Cache inconsistency across user sessions, debugging complexity.

## Recommendations

1. **Refactor quiz_service.py**: Move UI-specific code (e.g., `st.popover`) to the presentation layer. The service should return data only.
2. **Centralize data fetching**: Ensure that all data fetching (except for standalone pages) goes through the router layer's `get_stock_data` function. Services should receive pre-fetched data as arguments.
3. **Remove view-layer caching**: Replace `st.cache_data`/`st.cache_resource` in view layers with reliance on the data layer's caching mechanism (`FinMindClient`).
4. **Update architecture documentation**: Consider refining the architecture document to clarify the responsibilities of standalone pages (which may manage their own data loading) and the role of `_router_base.py` as part of the routing layer.

## Conclusion

The i18n refactoring itself maintains architectural integrity in the components it touched. The observed deviations are pre-existing and should be addressed in future refactoring efforts to ensure strict adherence to the layered architecture, thereby improving maintainability, testability, and consistency.
