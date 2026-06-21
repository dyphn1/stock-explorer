# Unified _plain_card() Component Specification

## Function Signature

```python
def _plain_card(
    title: str,
    content: str,
    icon: str = "📋",
    border_color: str = "#3498DB",
    bg_color: str = "#F8F9FA"
) -> None:
    """Render a unified card component.

    Args:
        title: Card title displayed with icon.
        content: Card body content.
        icon: Emoji or text icon to display before title (default: "📋").
        border_color: CSS color for left border (default: "#3498DB").
        bg_color: CSS background color for the card (default: "#F8F9FA").
    """
```

## HTML/CSS Template

The component renders the following HTML via `st.markdown` with `unsafe_allow_html=True`:

```html
<div style="
    background: {bg_color};
    border-radius: 12px;
    padding: 1.2rem;
    border-left: 4px solid {border_color};
    margin: 0.5rem 0;
">
    <div style="font-weight: 600; color: #2C3E50;">
        {icon} {title}
    </div>
    <div style="
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-top: 0.3rem;
        line-height: 1.6;
    ">
        {content}
    </div>
</div>
```

## Migration Guide

### Replacing `_info_card()`

**Before:**
```python
_info_card(title, content, icon="💡")
```

**After:**
```python
_plain_card(title, content, icon=icon, border_color="#3498DB", bg_color="#F8F9FA")
```

Since `_info_card` uses a fixed border color (`#3498DB`) and background color (`#F8F9FA`), you can also rely on the defaults of `_plain_card` and only specify the icon if it differs from the default `"📋"`:
```python
# If using the default icon "📋" is acceptable:
_plain_card(title, content)
# Or to keep the original icon "💡":
_plain_card(title, content, icon="💡")
```

### Replacing `_summary_card()`

**Before:**
```python
_summary_card(title, content, icon="📋", border_color="#E67E22")
```

**After:**
```python
_plain_card(title, content, icon=icon, border_color=border_color, bg_color="#FFF8F0")
```

Note that `_summary_card` uses a distinct background color (`#FFF8F0`). To preserve the exact appearance, pass the corresponding `bg_color`. If the default background color of `_plain_card` (`#F8F9FA`) is acceptable, you can omit it:
```python
_plain_card(title, content, icon=icon, border_color=border_color)
```

### General Migration Tips

1. **Parameter Order**: `_plain_card` expects `(title, content, icon, border_color, bg_color)` in that order.
2. **Default Values**: The defaults match `_info_card`’s styling except for the icon (which defaults to `"📋"` instead of `"💡"`). Adjust the icon argument as needed.
3. **Backward Compatibility**: By explicitly supplying the original `border_color` and `bg_color` values, you can achieve pixel‑perfect replacements of the existing cards.