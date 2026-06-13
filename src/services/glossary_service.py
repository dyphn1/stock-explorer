"""
Glossary service — loads financial term definitions from YAML data file.

Provides get_glossary_term(), get_all_terms(), and search_terms() for use
in glossary tooltips and the beginner glossary page.
"""

from pathlib import Path

import yaml

_MODULE_DIR = Path(__file__).resolve().parent
_DATA_FILE = _MODULE_DIR.parent / "data" / "glossary.yaml"

_cache: dict | None = None


def _load_data() -> dict:
    """Load and cache the glossary YAML file."""
    global _cache
    if _cache is None:
        if not _DATA_FILE.exists():
            raw: dict = {}
        else:
            with open(_DATA_FILE, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
        _cache = raw
    return _cache


def get_glossary_term(term_key: str) -> dict | None:
    """Return the term dict for a given key, or None if not found.

    Returns:
        dict with keys: name, plain, example, analogy, category
    """
    data = _load_data()
    term = data.get(term_key)
    if term is None:
        return None
    return dict(term)


def get_all_terms() -> dict:
    """Return all glossary terms as a dict keyed by term key."""
    return dict(_load_data())


def search_terms(query: str) -> list[dict]:
    """Search glossary terms by key, name, or plain text (case-insensitive).

    Args:
        query: Search string to match against term keys, names, and plain text.

    Returns:
        List of term dicts that match the query, each with an added 'key' field.
    """
    data = _load_data()
    q = query.lower().strip()
    results: list[dict] = []
    for key, term in data.items():
        if not isinstance(term, dict):
            continue
        searchable = " ".join([
            str(key),
            str(term.get("name", "")),
            str(term.get("plain", "")),
        ])
        if q in searchable.lower():
            entry = dict(term)
            entry["key"] = key
            results.append(entry)
    return results
