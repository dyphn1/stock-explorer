"""
src/core/i18n.py
Minimal i18n module: reads YAML locale files, provides t() function.
"""
from __future__ import annotations

import yaml
import streamlit as st
from pathlib import Path

_LOCALE_DIR = Path(__file__).resolve().parent.parent / "locales"

_locale_cache: dict[str, dict] = {}


def _load_locale(lang: str) -> dict:
    """Load YAML file for the given language."""
    if lang not in _locale_cache:
        path = _LOCALE_DIR / f"{lang}.yaml"
        if not path.exists():
            # fallback to zh-TW
            path = _LOCALE_DIR / "zh-TW.yaml"
        with open(path, encoding="utf-8") as f:
            _locale_cache[lang] = yaml.safe_load(f) or {}
    return _locale_cache[lang]


def t(key: str, **kwargs) -> str:
    """
    Translation function.

    Usage:
        t("page.title")                    # "股識 Stock Explorer"
        t("metric.revenue_yoy", value=25)  # "營收年增率 {value}%"
        t("error.not_found", sid="9999")   # "找不到股票代號 9999"

    YAML structure uses dot-notation key, e.g.:
        page: { title: "股識 Stock Explorer" }
    key "page.title" → data["page"]["title"]

    If key not found, returns the key itself (no crash).
    """
    lang = st.session_state.get("lang", "zh-TW")
    data = _load_locale(lang)

    # Support nested key: "page.title" → data["page"]["title"]
    node = data
    for part in key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return key  # key not found → return key text

    text = str(node)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text


def get_available_locales() -> list[dict]:
    """Return list of available locales."""
    return [
        {"code": "zh-TW", "name": "繁體中文", "label": "🇹🇼 繁體中文"},
        {"code": "en", "name": "English", "label": "🇺🇸 English"},
    ]


def set_lang(lang: str):
    """Set language and clear cache to trigger re-translation."""
    st.session_state["lang"] = lang
    _locale_cache.clear()
