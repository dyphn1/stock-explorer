"""
Backward-compat re-export: url_sync has moved to src/controller/url_sync.py.
"""

from src.controller.url_sync import (  # noqa: F401
    VALID_PAGES, _PAGE_KEY_TO_NAME, _PAGE_NAME_TO_KEY, DEFAULT_PAGE,
    _resolve_page, sync_url_to_session, _sync_session_to_url, navigate_to,
)
