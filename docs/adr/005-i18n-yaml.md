# ADR-005: i18n Using Single YAML File per Locale

## Status
Accepted

## Date
2026-06-14

## Background

The project currently has 3,146 hardcoded Chinese strings scattered across 93 Python files. An internationalization (i18n) mechanism needs to be established.

## Decision

Use **single YAML file per locale** to manage translated strings.

## Architecture

```
src/core/i18n.py          # i18n core module (single entry point)
locales/
├── zh-TW.yaml            # Traditional Chinese (default)
└── en.yaml               # English
```

**No folder categorization** (e.g., `locales/zh-TW/ui.yaml`) — single file per locale is the simplest approach. Split only if it exceeds 500 lines in the future.

## Naming Convention

```
<module>.<submodule>.<component>.<purpose>
```

Examples:
- `pages.business_card.title` — Business card page title
- `pages.router.nav_label` — Navigation label
- `errors.no_data` — No data error

## Usage

```python
from src.core.i18n import t

# Basic usage
st.markdown(t("pages.business_card.title"))

# With parameters
st.markdown(t("pages.stock.price", price=100))
```

## Alternatives

| Option | Reason for Rejection |
|--------|---------------------|
| Python dict | Cannot be separated from code, hard to maintain |
| JSON | No comment support, poor readability |
| Database | Over-engineered for MVP stage |
| Multiple files per locale | Increases lookup cost |

## Consequences

- ✅ Simple and easy to maintain
- ✅ Language switchable
- ⚠️ Need to replace 3,146 hardcoded strings one by one
- ⚠️ Team discipline required: all new UI strings must use `t()`
