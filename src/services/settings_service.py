"""Settings service — threshold access helper."""
_DEFAULTS = {
    "price_threshold": 5.0,
    "revenue_threshold": 10.0,
}


def get_threshold(settings, key: str) -> float:
    """Get threshold from settings dict/session_state, falling back to default."""
    if settings is None:
        return _DEFAULTS.get(key, 0.0)
    try:
        val = settings.get(key, _DEFAULTS.get(key, 0.0))
    except (AttributeError, TypeError):
        val = _DEFAULTS.get(key, 0.0)
    return float(val)
