"""
Company Facts service — loads fun/educational facts from YAML data file.

Provides get_company_facts() and get_random_fact() for use in the
business card page's "Did You Know?" section.
"""

import random
from pathlib import Path

import yaml

import sys

# Resolve project root relative to this module for reliable imports
_MODULE_DIR = Path(__file__).resolve().parent
_DATA_FILE = _MODULE_DIR.parent / "data" / "company_facts.yaml"

_cache: dict[str, list[str]] | None = None


def _load_data() -> dict[str, list[str]]:
    """Load and cache the company facts YAML file."""
    global _cache
    if _cache is None:
        if not _DATA_FILE.exists():
            raw: dict[str, list[str]] = {}
        else:
            with open(_DATA_FILE, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
        _cache = raw
    return _cache


def get_company_facts(stock_id: str) -> list[str]:
    """Return the list of facts for a given stock_id, or empty list if none."""
    data = _load_data()
    return data.get(stock_id, [])


def get_random_fact(stock_id: str) -> str | None:
    """Return a random fact for a given stock_id, or None if no facts exist."""
    facts = get_company_facts(stock_id)
    if not facts:
        return None
    return random.choice(facts)
