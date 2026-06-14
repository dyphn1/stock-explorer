"""
Glossary service — loads financial term definitions from YAML data file.

Provides get_glossary_term(), get_all_terms(), search_terms(), and
term-key resolution helpers for tappable glossary annotations (C170).
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


# ── C170: Term-key resolution mapping ──────────────────────────
# Maps display labels / metric names used in the UI to glossary.yaml keys.
# The service layer stays Streamlit-free; this is pure data.

_DISPLAY_TERM_MAP: dict[str, str] = {
    # Metric names from analogy engine + extra_metrics keys
    "ROE": "ROE",
    "毛利率": "毛利率",
    "本益比": "本益比",
    "PER": "本益比",
    "淨值比": "淨值比",
    "PBR": "淨值比",
    "殖利率": "殖利率",
    "dividend_yield": "殖利率",
    "營收年增率": "營收年增率",
    "revenue_yoy": "營收年增率",
    "負債比": "負債比",
    "debt_ratio": "負債比",
    "流動比": "流動比",
    "current_ratio": "流動比",
    "淨利率": "淨利率",
    "net_margin": "淨利率",
    "營業利益率": "營業利益率",
    "自由現金流": "自由現金流",
    "每股盈餘": "每股盈餘",
    "EPS": "每股盈餘",
    # Health dimension names → primary glossary term for that dimension
    "獲利能力": "ROE",
    "成長性": "營收年增率",
    "財務健康": "負債比",
    "股利品質": "殖利率",
    "估值合理性": "本益比",
}

# Chinese display name → glossary key (for labels shown to users)
_CH_DISPLAY_MAP: dict[str, str] = {
    "ROE（股東權益報酬率）": "ROE",
    "股東權益報酬率": "ROE",
    "本益比 (PER)": "本益比",
    "淨值比 (PBR)": "淨值比",
    "最近月營收": "營業收入",
    "月營收": "營業收入",
}


def resolve_term_key(label: str) -> str | None:
    """Resolve a UI display label to a glossary term key.

    Checks the display-term map first, then falls back to the Chinese
    display map, then finally tries the label itself as a direct key.

    Args:
        label: Any metric name, dimension name, or Chinese display string.

    Returns:
        A glossary.yaml key string, or None if no match found.
    """
    # Direct map lookup
    key = _DISPLAY_TERM_MAP.get(label)
    if key is not None:
        return key

    # Chinese display variants
    key = _CH_DISPLAY_MAP.get(label)
    if key is not None:
        return key

    # Fallback: try the label itself as a direct glossary key
    data = _load_data()
    if label in data:
        return label

    # Strip parenthetical English suffixes like " (PER)" and retry
    stripped = label.split(" (")[0].strip()
    if stripped in data:
        return stripped
    if stripped in _DISPLAY_TERM_MAP:
        return _DISPLAY_TERM_MAP[stripped]

    return None


def get_term_map() -> dict[str, str]:
    """Return a copy of the full display-term → glossary-key mapping."""
    return dict(_DISPLAY_TERM_MAP)
