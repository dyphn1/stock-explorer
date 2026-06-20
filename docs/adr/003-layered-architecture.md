# ADR-003: Adopt Strict Layered Architecture

## Status
Accepted

## Date
2026-06-07

## Background

Initial development used a "code-first" approach, resulting in code that mixed data access, business logic, and UI rendering, making it difficult to maintain and test.

## Decision

Adopt a **strict four-layer architecture**, with clear responsibilities and prohibitions for each layer.

## Architecture Definition

```
Presentation Layer (src/pages/)
    ↕ depends only on
Routing Layer (src/pages/router.py)
    ↕ depends only on
Business Logic Layer (src/services/)
    ↕ depends only on
Data Layer (src/data/)
```

## Layer Responsibilities

### Data Layer (`src/data/`)
- **Responsibility**: FinMind API encapsulation, cache management
- **Returns**: pandas DataFrame or dict
- **Prohibited**: import streamlit, include business logic

### Business Logic Layer (`src/services/`)
- **Responsibility**: Calculate indicators, generate charts, plain-language translation
- **Returns**: Calculation results or chart objects
- **Prohibited**: import streamlit, direct API calls, side effects

### Routing Layer (`src/pages/router.py`)
- **Responsibility**: Manage session_state, select View, coordinate data loading
- **Prohibited**: Directly generate UI components

### Presentation Layer (`src/pages/*.py`)
- **Responsibility**: Pure rendering, receive data dict, generate Streamlit UI
- **Prohibited**: Direct API calls, direct cache read/write, complex calculations

## Rationale

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Modifying one layer does not affect others
3. **AI Agent friendly**: Clear boundaries tell AI where each file belongs

## Consequences

- ✅ Code has clear ownership
- ✅ Each layer can be tested independently
- ⚠️ Slower initial development speed (must follow layering)
- ⚠️ Strict enforcement required, otherwise easy to regress
