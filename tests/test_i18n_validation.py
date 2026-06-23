'''Translation key validation tests.
Ensures that all PAGE_KEYS have corresponding entries in locale files and vice versa.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

# Import PAGE_KEYS from the router module
from src.pages.router import PAGE_KEYS

# Path to locale files
LOCALES_DIR = Path(__file__).parents[1] / "locales"
EN_YAML = LOCALES_DIR / "en.yaml"
ZH_TW_YAML = LOCALES_DIR / "zh-TW.yaml"


def load_locale(filepath: Path) -> dict:
    """Load YAML locale file and return the 'page' section."""
    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("page", {})


def contains_cjk(text: str) -> bool:
    """Return True if string contains any CJK Unicode characters."""
    # CJK Unified Ideographs range
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def is_only_ascii_or_latin1(text: str) -> bool:
    """Return True if string contains only ASCII/Latin-1 characters (no CJK)."""
    # We'll consider it English if it doesn't contain CJK characters.
    # This is a simplification but sufficient for detecting accidental Chinese in en.yaml.
    return not contains_cjk(text)


def test_page_keys_match_locale_en():
    """Ensure every PAGE_KEY has an entry in en.yaml page section."""
    en_page = load_locale(EN_YAML)
    missing = [key for key in PAGE_KEYS if key not in en_page]
    assert not missing, f"Missing keys in en.yaml: {missing}"


def test_page_keys_match_locale_zh_tw():
    """Ensure every PAGE_KEY has an entry in zh-TW.yaml page section."""
    zh_tw_page = load_locale(ZH_TW_YAML)
    missing = [key for key in PAGE_KEYS if key not in zh_tw_page]
    assert not missing, f"Missing keys in zh-TW.yaml: {missing}"


def test_no_orphaned_keys_in_en():
    """Ensure en.yaml page section has no keys that are not in PAGE_KEYS."""
    en_page = load_locale(EN_YAML)
    extra = [key for key in en_page if key not in PAGE_KEYS]
    assert not extra, f"Orphaned keys in en.yaml: {extra}"


def test_no_orphaned_keys_in_zh_tw():
    """Ensure zh-TW.yaml page section has no keys that are not in PAGE_KEYS."""
    zh_tw_page = load_locale(ZH_TW_YAML)
    extra = [key for key in zh_tw_page if key not in PAGE_KEYS]
    assert not extra, f"Orphaned keys in zh-TW.yaml: {extra}"


def test_en_values_contain_no_cjk():
    """Ensure en.yaml page values contain only ASCII/Latin-1 characters (no CJK)."""
    en_page = load_locale(EN_YAML)
    bad_keys = []
    for key, value in en_page.items():
        if not isinstance(value, str):
            continue
        if contains_cjk(value):
            bad_keys.append((key, value))
    assert not bad_keys, f"en.yaml contains CJK characters in keys: {bad_keys}"


def test_zh_tw_values_contain_cjk():
    """Ensure zh-TW.yaml page values contain at least one CJK character."""
    zh_tw_page = load_locale(ZH_TW_YAML)
    bad_keys = []
    for key, value in zh_tw_page.items():
        if not isinstance(value, str):
            continue
        if not contains_cjk(value):
            bad_keys.append((key, value))
    assert not bad_keys, f"zh-TW.yaml values lack CJK characters: {bad_keys}"