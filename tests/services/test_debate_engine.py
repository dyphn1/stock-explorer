"""
Unit tests for debate_engine.py (C199).

Tests cover:
- generate_debate with sample data (all bull, all bear, mixed)
- Edge cases: missing peer data, empty metrics, neutral
- get_debate_summary verdict logic
- Banned word filtering
- No Streamlit imports in service layer
- i18n keys returned (not hardcoded text)

All tests use mock data — no Streamlit, no API calls.
"""
import pytest
from src.services.debate_engine import (
    generate_debate,
    get_debate_summary,
    contains_banned_words,
    _calc_strength,
    _METRICS,
)


# ── Helpers ──────────────────────────────────────────────────

def _sample_extra_metrics(**overrides) -> dict:
    """Build a sample extra_metrics dict (without peer data)."""
    base = {
        "roe": 15.0,
        "revenue_yoy": 8.0,
        "gross_margin": 30.0,
        "operating_margin": 12.0,
        "net_margin": 8.0,
        "debt_ratio": 30.0,
        "current_ratio": 150.0,
        "dividend_yield": 4.0,
    }
    base.update(overrides)
    return base


def _sample_peer_metrics(**overrides) -> dict:
    """Build a sample peer_metrics dict."""
    base = {
        "roe": 10.0,
        "revenue_yoy": 5.0,
        "gross_margin": 25.0,
        "operating_margin": 10.0,
        "net_margin": 6.0,
        "debt_ratio": 40.0,
        "current_ratio": 120.0,
        "dividend_yield": 3.0,
    }
    base.update(overrides)
    return base


def _empty_data() -> dict:
    return {"stock_id": "2330", "stock_name": "TSMC"}


# ── _calc_strength() tests ───────────────────────────────────

class TestCalcStrength:
    def test_identical_values_returns_zero(self):
        assert _calc_strength(10.0, 10.0) == 0.0

    def test_higher_value_returns_positive(self):
        # |15 - 10| / max(10, 1) * 0.5 = 5/10 * 0.5 = 0.25
        assert _calc_strength(15.0, 10.0) == pytest.approx(0.25)

    def test_lower_value_returns_positive(self):
        # |5 - 10| / max(10, 1) * 0.5 = 5/10 * 0.5 = 0.25
        assert _calc_strength(5.0, 10.0) == pytest.approx(0.25)

    def test_large_difference_capped_at_one(self):
        # |100 - 10| / max(10, 1) * 0.5 = 90/10 * 0.5 = 4.5 → capped at 1.0
        assert _calc_strength(100.0, 10.0) == 1.0

    def test_zero_peer_avg_returns_modest_strength(self):
        # peer_avg == 0 → returns 0.3
        assert _calc_strength(5.0, 0.0) == 0.3

    def test_symmetric(self):
        """Strength is symmetric — same difference gives same result."""
        assert _calc_strength(15.0, 10.0) == _calc_strength(5.0, 10.0)


# ── generate_debate() tests ──────────────────────────────────

class TestGenerateDebate:
    def test_empty_metrics_returns_empty(self):
        result = generate_debate(_empty_data(), {})
        assert result == []

    def test_no_peer_metrics_returns_empty(self):
        """If peer_metrics is None/empty, no points can be generated."""
        extra = _sample_extra_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=None)
        assert result == []

    def test_empty_peer_metrics_returns_empty(self):
        extra = _sample_extra_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics={})
        assert result == []

    def test_all_bull_metrics(self):
        """All metrics above peer_avg → all bull points."""
        extra = _sample_extra_metrics()  # all values > peer defaults
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        bull_points = [p for p in result if p["side"] == "bull"]
        bear_points = [p for p in result if p["side"] == "bear"]
        assert len(bull_points) >= 1
        assert len(bear_points) == 0

    def test_all_bear_metrics(self):
        """All metrics below peer_avg → all bear points."""
        extra = _sample_extra_metrics(
            roe=5.0,
            revenue_yoy=2.0,
            gross_margin=20.0,
            operating_margin=5.0,
            net_margin=3.0,
            debt_ratio=50.0,  # higher debt → bear (lower_is_bullish)
            current_ratio=100.0,
            dividend_yield=2.0,
        )
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        bull_points = [p for p in result if p["side"] == "bull"]
        bear_points = [p for p in result if p["side"] == "bear"]
        assert len(bear_points) >= 1
        assert len(bull_points) == 0

    def test_mixed_metrics_produce_both_sides(self):
        """Some metrics above, some below → both sides represented."""
        extra = _sample_extra_metrics(
            roe=5.0,  # bear
            revenue_yoy=8.0,  # bull
        )
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        sides = {p["side"] for p in result}
        assert "bull" in sides
        assert "bear" in sides

    def test_missing_peer_data_skips_metric(self):
        """Metrics without peer data are skipped."""
        extra = {"roe": 15.0}
        peer = {}  # no roe in peer
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert result == []

    def test_equal_values_skipped(self):
        """Metric exactly equal to peer_avg → strength 0.05 threshold filters it."""
        # value == peer_avg → rel_diff = 0 → strength = 0.0 → < 0.05 → skipped
        extra = {"roe": 10.0}
        peer = {"roe": 10.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert result == []

    def test_max_six_per_side_enforced(self):
        """No more than 6 points per side (hardcoded limit)."""
        extra = _sample_extra_metrics()
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        bull_count = sum(1 for p in result if p["side"] == "bull")
        bear_count = sum(1 for p in result if p["side"] == "bear")
        assert bull_count <= 6
        assert bear_count <= 6

    def test_debate_point_has_required_fields(self):
        """Each DebatePoint must have all required fields."""
        extra = _sample_extra_metrics()
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        for point in result:
            assert "side" in point
            assert "metric" in point
            assert "value" in point
            assert "peer_avg" in point
            assert "argument_key" in point
            assert "icon" in point
            assert "strength" in point
            assert point["side"] in ("bull", "bear")
            assert 0.0 <= point["strength"] <= 1.0

    def test_argument_key_format(self):
        """Argument keys must follow debate.{metric}_{side} pattern."""
        extra = _sample_extra_metrics()
        peer = _sample_peer_metrics()
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        for point in result:
            key = point["argument_key"]
            assert key.startswith("debate.")
            assert key.endswith(("_bull", "_bear"))

    def test_debt_ratio_inverted_direction(self):
        """Lower debt_ratio is bullish, higher is bearish."""
        # Lower debt → bull
        extra = {"debt_ratio": 20.0}
        peer = {"debt_ratio": 40.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert len(result) >= 1
        assert result[0]["side"] == "bull"

        # Higher debt → bear
        extra = {"debt_ratio": 50.0}
        peer = {"debt_ratio": 40.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert len(result) >= 1
        assert result[0]["side"] == "bear"

    def test_current_ratio_higher_is_bullish(self):
        """Higher current_ratio is bullish (higher_is_bullish direction)."""
        # Higher current_ratio → bull
        extra = {"current_ratio": 200.0}
        peer = {"current_ratio": 120.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert len(result) >= 1
        assert result[0]["side"] == "bull"

        # Lower current_ratio → bear
        extra = {"current_ratio": 80.0}
        peer = {"current_ratio": 120.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert len(result) >= 1
        assert result[0]["side"] == "bear"

    def test_metrics_list_complete(self):
        """All 8 required metrics should be in _METRICS."""
        metric_names = [m["key"] for m in _METRICS]
        expected = [
            "roe", "revenue_yoy", "gross_margin", "operating_margin",
            "net_margin", "debt_ratio", "current_ratio", "dividend_yield",
        ]
        for name in expected:
            assert name in metric_names, f"Missing metric: {name}"

    def test_metrics_have_required_fields(self):
        """Each metric config must have key, direction, bull_key, bear_key, icons."""
        for m in _METRICS:
            assert "key" in m
            assert "direction" in m
            assert "bull_key" in m
            assert "bear_key" in m
            assert "icon_bull" in m
            assert "bear_icon" in m
            assert m["direction"] in ("higher_is_bullish", "lower_is_bullish")

    def test_no_streamlit_import(self):
        """Service layer must NOT import streamlit."""
        import src.services.debate_engine as mod
        import inspect
        source = inspect.getsource(mod)
        assert "import streamlit" not in source
        assert "from streamlit" not in source

    def test_peer_metrics_as_separate_dict(self):
        """peer_metrics is a separate dict parameter, not embedded in extra_metrics."""
        extra = {"roe": 15.0}
        peer = {"roe": 10.0}
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        assert len(result) >= 1
        assert result[0]["side"] == "bull"

    def test_points_not_sorted_by_strength(self):
        """Points are returned in _METRICS order, not sorted by strength."""
        # Only provide two metrics so we can check their order
        # roe: very high strength (|100-10|/10 * 0.5 = 4.5 → 1.0)
        # revenue_yoy: moderate strength (|20-5|/5 * 0.5 = 1.5 → 1.0)
        extra = {
            "roe": 100.0,
            "revenue_yoy": 20.0,
        }
        peer = {
            "roe": 10.0,
            "revenue_yoy": 5.0,
        }
        result = generate_debate(_empty_data(), extra, peer_metrics=peer)
        # Points should be in _METRICS order: roe first, then revenue_yoy
        assert len(result) == 2
        assert result[0]["metric"] == "roe"
        assert result[1]["metric"] == "revenue_yoy"


# ── get_debate_summary() tests ───────────────────────────────

class TestGetDebateSummary:
    def test_empty_points(self):
        summary = get_debate_summary([])
        assert summary["bull_count"] == 0
        assert summary["bear_count"] == 0
        assert summary["bull_strength"] == 0.0
        assert summary["bear_strength"] == 0.0
        assert summary["verdict_key"] == "debate.neutral"

    def test_bull_strong(self):
        points = [
            {"side": "bull", "metric": "roe", "strength": 0.8, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bull", "metric": "revenue_yoy", "strength": 0.6, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bear", "metric": "debt_ratio", "strength": 0.2, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
        ]
        summary = get_debate_summary(points)
        assert summary["verdict_key"] == "debate.bull_strong"
        assert summary["bull_count"] == 2
        assert summary["bear_count"] == 1

    def test_bear_strong(self):
        points = [
            {"side": "bear", "metric": "roe", "strength": 0.9, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bear", "metric": "revenue_yoy", "strength": 0.7, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bull", "metric": "debt_ratio", "strength": 0.1, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
        ]
        summary = get_debate_summary(points)
        assert summary["verdict_key"] == "debate.bear_strong"
        assert summary["bull_count"] == 1
        assert summary["bear_count"] == 2

    def test_neutral_when_close(self):
        points = [
            {"side": "bull", "metric": "roe", "strength": 0.5, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bear", "metric": "debt_ratio", "strength": 0.5, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
        ]
        summary = get_debate_summary(points)
        assert summary["verdict_key"] == "debate.neutral"

    def test_strength_values_summed(self):
        points = [
            {"side": "bull", "metric": "a", "strength": 0.3, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bull", "metric": "b", "strength": 0.4, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
            {"side": "bear", "metric": "c", "strength": 0.5, "value": 0.0, "peer_avg": 0.0, "argument_key": "", "icon": ""},
        ]
        summary = get_debate_summary(points)
        assert summary["bull_strength"] == 0.7
        assert summary["bear_strength"] == 0.5


# ── contains_banned_words() tests ─────────────────────────────

class TestContainsBannedWords:
    def test_clean_text_returns_true(self):
        """contains_banned_words returns False when text is clean (no banned words)."""
        # Note: contains_banned_words returns _check_banned(text), which returns
        # True if banned words ARE found. So clean text → False.
        assert contains_banned_words("ROE 15% above industry average 10%") is False

    def test_banned_chinese_buy_word(self):
        """Text with banned Chinese word '買進' returns True (banned detected)."""
        assert contains_banned_words("建議買進此股票") is True

    def test_banned_chinese_sell_word(self):
        """Text with banned Chinese word '賣出' returns True (banned detected)."""
        assert contains_banned_words("建議賣出持股") is True

    def test_banned_english_buy_word(self):
        """Text with banned English word 'buy' returns True (banned detected)."""
        assert contains_banned_words("You should buy this stock") is True

    def test_banned_english_sell_word(self):
        """Text with banned English word 'sell' returns True (banned detected)."""
        assert contains_banned_words("You should sell this stock") is True

    def test_banned_word_strong_buy(self):
        """Text with banned phrase 'strong buy' returns True (banned detected)."""
        assert contains_banned_words("Analysts give a strong buy rating") is True

    def test_banned_word_target_price(self):
        """Text with banned phrase 'target price' returns True (banned detected)."""
        assert contains_banned_words("The target price is $100") is True

    def test_empty_text_not_banned(self):
        """Empty text has no banned words → returns False."""
        assert contains_banned_words("") is False

    def test_banned_word_推薦(self):
        """Text with banned Chinese word '推薦' returns True (banned detected)."""
        assert contains_banned_words("推薦買入") is True

    def test_banned_word_建議(self):
        """Text with banned Chinese word '建議' returns True (banned detected)."""
        assert contains_banned_words("建議投資") is True
