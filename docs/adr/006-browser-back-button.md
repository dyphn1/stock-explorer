# ADR-006: Browser Back Button Support

## Status
Accepted

## Date
2026-06-12

## Background

When users click the browser back button, the page does not correctly return to the previous page — instead, the application closes directly. This is because Streamlit's `st.session_state` is not synchronized with the browser URL.

## Decision

Use bidirectional synchronization between `st.query_params` and `st.session_state` to implement browser back button support.

## Implementation

```python
# URL → session (on page load)
def sync_url_to_session():
    params = st.query_params
    if "page" in params:
        st.session_state["page"] = params["page"]
    if "stock_id" in params:
        st.session_state["stock_id"] = params["stock_id"]

# session → URL (on navigation)
def navigate_to(page: str, stock_id: str = None):
    st.session_state["page"] = page
    if stock_id:
        st.session_state["stock_id"] = stock_id
    st.query_params["page"] = page
    if stock_id:
        st.query_params["stock_id"] = stock_id
    st.rerun()
```

## Rationale

1. **User expectations**: The browser back button should work correctly
2. **Shareability**: URL contains page state, links can be shared
3. **Simplicity**: No additional routing package needed

## Consequences

- ✅ Browser back/forward buttons work correctly
- ✅ Specific pages can be shared via URL
- ⚠️ Every navigation operation must update both session and query_params simultaneously
