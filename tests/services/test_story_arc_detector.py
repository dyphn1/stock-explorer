"""
Unit tests for story_arc_detector.py (C202).

Tests cover:
- Empty entries
- Single event
- All-positive arc (growth)
- All-negative arc (decline)
- Mixed/volatile arc (volatile)
- Recovery arc (recovery — neg→pos transition)
- Sparse events (< min_events → no label shown)
- Boundary conditions (exactly min_events, exactly 6-month window)
- Stocks with no events
- get_arc_legend()

All tests use mock TimelineEntry lists — no Streamlit, no API calls.

i18n: the service returns arc type keys ("growth", "decline", etc.)
and description keys ("story_arc.growth_description", etc.).
Display text resolution (t()) is the page layer's responsibility.
"""
import pytest
from src.services.story_arc_detector import (
    detect_arcs,
    get_arc_legend,
    _bucket_key,
    _bucket_label,
    _score_bucket,
    _classify_bucket,
    ARC_GROWTH,
    ARC_DECLINE,
    ARC_VOLATILE,
    ARC_RECOVERY,
)


# ── Helpers ──────────────────────────────────────────────────

def _entry(date: str, severity: str = "low", etype: str = "revenue_surge") -> dict:
    """Build a minimal TimelineEntry dict."""
    return {
        "date": date,
        "type": etype,
        "severity": severity,
        "title": "Test event",
        "summary": "",
        "icon": "📌",
        "source": "detected",
    }


def _make_entries(specs: list[tuple[str, str, str]]) -> list[dict]:
    """Build a list of TimelineEntry dicts from (date, severity, type) tuples."""
    return [_entry(d, s, t) for d, s, t in specs]


# ── Arc key constants tests ──────────────────────────────────

class TestArcKeyConstants:
    def test_arc_keys_are_english(self):
        """Arc constants must be English i18n keys, not Chinese text."""
        assert ARC_GROWTH == "growth"
        assert ARC_DECLINE == "decline"
        assert ARC_VOLATILE == "volatile"
        assert ARC_RECOVERY == "recovery"

    def test_arc_keys_not_chinese(self):
        """Arc constants must NOT contain Chinese characters."""
        for key in (ARC_GROWTH, ARC_DECLINE, ARC_VOLATILE, ARC_RECOVERY):
            assert all(ord(c) < 0x4E00 for c in key), f"Key '{key}' contains CJK characters"


# ── _bucket_key() tests ─────────────────────────────────────

class TestBucketKey:
    def test_january_goes_to_h1(self):
        assert _bucket_key("2024-01-15") == "2024-01"

    def test_june_goes_to_h1(self):
        assert _bucket_key("2024-06-30") == "2024-01"

    def test_july_goes_to_h2(self):
        assert _bucket_key("2024-07-01") == "2024-07"

    def test_december_goes_to_h2(self):
        assert _bucket_key("2024-12-31") == "2024-07"

    def test_invalid_date_returns_empty(self):
        assert _bucket_key("not-a-date") == ""

    def test_empty_string_returns_empty(self):
        assert _bucket_key("") == ""


# ── _bucket_label() tests ────────────────────────────────────

class TestBucketLabel:
    def test_h1_label(self):
        assert _bucket_label("2024-01") == "2024 上半年"

    def test_h2_label(self):
        assert _bucket_label("2024-07") == "2024 下半年"

    def test_empty_returns_empty(self):
        assert _bucket_label("") == ""


# ── _score_bucket() tests ───────────────────────────────────

class TestScoreBucket:
    def test_all_high_severity(self):
        entries = [_entry("2024-01-01", "high") for _ in range(3)]
        assert _score_bucket(entries) == 9.0

    def test_mixed_severity(self):
        entries = [
            _entry("2024-01-01", "high"),
            _entry("2024-01-02", "medium"),
            _entry("2024-01-03", "high"),
        ]
        assert _score_bucket(entries) == 8.0

    def test_price_abnormal_flips_sign(self):
        entries = [_entry("2024-01-01", "high", "price_abnormal") for _ in range(3)]
        assert _score_bucket(entries) == -9.0

    def test_empty_entries(self):
        assert _score_bucket([]) == 0.0


# ── _classify_bucket() tests ────────────────────────────────

class TestClassifyBucket:
    def test_growth_high_score(self):
        assert _classify_bucket(5.0, 3) == ARC_GROWTH

    def test_decline_low_score(self):
        assert _classify_bucket(-5.0, 3) == ARC_DECLINE

    def test_volatile_mixed_score(self):
        assert _classify_bucket(0.0, 3) == ARC_VOLATILE
        assert _classify_bucket(-1.0, 3) == ARC_VOLATILE

    def test_recovery_mild_positive(self):
        assert _classify_bucket(1.0, 3) == ARC_RECOVERY
        assert _classify_bucket(3.0, 3) == ARC_RECOVERY

    def test_insufficient_events_returns_empty(self):
        assert _classify_bucket(5.0, 2) == ""
        assert _classify_bucket(0.0, 0) == ""
        assert _classify_bucket(-5.0, 1) == ""

    def test_boundary_exactly_3_events(self):
        assert _classify_bucket(4.0, 3) != ""
        assert _classify_bucket(-4.0, 3) != ""


# ── detect_arcs() tests ─────────────────────────────────────

class TestDetectArcs:
    def test_empty_entries(self):
        assert detect_arcs([]) == []

    def test_single_event_no_arc(self):
        entries = [_entry("2024-03-01", "high")]
        assert detect_arcs(entries) == []

    def test_sparse_events_no_signal(self):
        """Less than min_events events across 2 buckets → no arcs."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-08-15", "high"),
        ]
        assert detect_arcs(entries) == []

    def test_all_positive_growth_arc(self):
        """All high-severity events in one bucket → growth key."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
            _entry("2024-03-15", "high"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        assert arcs[0]["arc_key"] == ARC_GROWTH
        assert arcs[0]["arc_emoji"] == "📈"
        assert arcs[0]["event_count"] == 3

    def test_all_negative_decline_arc(self):
        """Price-abnormal high-severity events → decline key."""
        entries = [
            _entry("2024-01-15", "high", "price_abnormal"),
            _entry("2024-02-15", "medium", "price_abnormal"),
            _entry("2024-03-15", "high", "price_abnormal"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        assert arcs[0]["arc_key"] == ARC_DECLINE
        assert arcs[0]["arc_emoji"] == "📉"

    def test_transition_decline_to_growth(self):
        """Decline bucket followed by growth bucket → 2 arcs (one per transition)."""
        # Bucket 2024-H1: negative events (decline)
        decline_entries = [
            _entry("2024-01-15", "high", "price_abnormal"),
            _entry("2024-02-15", "high", "price_abnormal"),
            _entry("2024-03-15", "high", "price_abnormal"),
        ]
        # Bucket 2025-H1: positive events (growth)
        growth_entries = [
            _entry("2025-01-15", "high"),
            _entry("2025-02-15", "high"),
            _entry("2025-03-15", "high"),
        ]
        entries = decline_entries + growth_entries
        arcs = detect_arcs(entries)
        # Should detect 2 transition arcs: decline first, then growth
        assert len(arcs) >= 2
        arc_keys = [a["arc_key"] for a in arcs]
        assert ARC_DECLINE in arc_keys
        assert ARC_GROWTH in arc_keys

    def test_same_label_no_extra_transition(self):
        """Two consecutive buckets with same label → only first transition shown."""
        # Both buckets growth
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
            _entry("2024-03-15", "high"),
            _entry("2024-07-15", "high"),
            _entry("2024-08-15", "high"),
            _entry("2024-09-15", "high"),
        ]
        arcs = detect_arcs(entries)
        # First bucket starts growth, second bucket continues growth → only 1 arc
        arc_keys = [a["arc_key"] for a in arcs]
        assert arc_keys.count(ARC_GROWTH) == 1

    def test_arc_fields_complete(self):
        """Verify all expected fields in ArcLabel output."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
            _entry("2024-03-15", "high"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        arc = arcs[0]
        assert "arc_key" in arc
        assert "arc_emoji" in arc
        assert "arc_description_key" in arc
        assert "bucket_start" in arc
        assert "bucket_end" in arc
        assert "event_count" in arc
        assert "score" in arc
        assert arc["bucket_start"].startswith("2024-01")
        assert arc["bucket_end"].startswith("2024-06")

    def test_arc_description_key_format(self):
        """Description keys must follow story_arc.*_description pattern."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
            _entry("2024-03-15", "high"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        desc_key = arcs[0]["arc_description_key"]
        assert desc_key.startswith("story_arc.")
        assert desc_key.endswith("_description")

    def test_arc_key_not_chinese(self):
        """Arc keys returned by detect_arcs must NOT contain Chinese."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
            _entry("2024-03-15", "high"),
        ]
        arcs = detect_arcs(entries)
        for arc in arcs:
            key = arc["arc_key"]
            assert all(ord(c) < 0x4E00 for c in key), f"arc_key '{key}' contains CJK"

    def test_recovery_arc_mild_positive(self):
        """Mildly positive score → recovery key."""
        # 3 low-severity events → score = 3 → recovery (1 <= score < 4)
        entries = [
            _entry("2024-01-15", "low"),
            _entry("2024-02-15", "low"),
            _entry("2024-03-15", "low"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        assert arcs[0]["arc_key"] == ARC_RECOVERY

    def test_volatile_bucket(self):
        """Score near zero → volatile key."""
        # 1 pos low + 2 neg low = 1 - 2 = -1 → volatile
        entries = [
            _entry("2024-01-15", "low"),
            _entry("2024-02-15", "low", "price_abnormal"),
            _entry("2024-03-15", "low", "price_abnormal"),
        ]
        arcs = detect_arcs(entries)
        assert len(arcs) >= 1
        assert arcs[0]["arc_key"] == ARC_VOLATILE

    def test_custom_min_events(self):
        """Test with custom min_events threshold."""
        entries = [
            _entry("2024-01-15", "high"),
            _entry("2024-02-15", "high"),
        ]
        # Default min_events=3 → no arcs with 2 events
        assert detect_arcs(entries) == []
        # With min_events=2 → should detect
        arcs = detect_arcs(entries, min_events=2)
        assert len(arcs) >= 1

    def test_bucket_boundaries_jan_jun(self):
        """Verify Jan-Jun forms one bucket."""
        entries = [
            _entry("2024-01-01", "high"),
            _entry("2024-03-15", "high"),
            _entry("2024-06-30", "high"),
        ]
        arcs = detect_arcs(entries)
        if arcs:
            assert arcs[0]["bucket_start"] == "2024-01-01"

    def test_bucket_boundaries_jul_dec(self):
        """Verify Jul-Dec forms one bucket."""
        entries = [
            _entry("2024-07-01", "high"),
            _entry("2024-09-15", "high"),
            _entry("2024-12-31", "high"),
        ]
        arcs = detect_arcs(entries)
        if arcs:
            assert arcs[0]["bucket_start"] == "2024-07-01"

    def test_all_four_arc_types_produce_correct_keys(self):
        """Each arc type maps to the correct i18n key."""
        test_cases = [
            # (entries_spec, expected_key)
            ([("2024-01-15", "high", "revenue_surge"),
              ("2024-02-15", "high", "revenue_surge"),
              ("2024-03-15", "high", "revenue_surge")], ARC_GROWTH),
            ([("2024-01-15", "high", "price_abnormal"),
              ("2024-02-15", "high", "price_abnormal"),
              ("2024-03-15", "high", "price_abnormal")], ARC_DECLINE),
            ([("2024-01-15", "low", "revenue_surge"),
              ("2024-02-15", "low", "price_abnormal"),
              ("2024-03-15", "low", "price_abnormal")], ARC_VOLATILE),
            ([("2024-01-15", "low", "revenue_surge"),
              ("2024-02-15", "low", "revenue_surge"),
              ("2024-03-15", "low", "revenue_surge")], ARC_RECOVERY),
        ]
        for spec, expected_key in test_cases:
            entries = _make_entries(spec)
            arcs = detect_arcs(entries)
            assert len(arcs) >= 1, f"Expected arc for {expected_key}, got none"
            assert arcs[0]["arc_key"] == expected_key, (
                f"Expected {expected_key}, got {arcs[0]['arc_key']}"
            )


# ── get_arc_legend() tests ──────────────────────────────────

class TestGetArcLegend:
    def test_returns_four_items(self):
        legend = get_arc_legend()
        assert len(legend) == 4

    def test_each_item_has_required_fields(self):
        legend = get_arc_legend()
        for item in legend:
            assert "key" in item
            assert "emoji" in item
            assert "label_key" in item
            assert "desc_key" in item

    def test_contains_all_arc_types(self):
        legend = get_arc_legend()
        keys = {item["key"] for item in legend}
        assert ARC_GROWTH in keys
        assert ARC_DECLINE in keys
        assert ARC_VOLATILE in keys
        assert ARC_RECOVERY in keys

    def test_label_keys_follow_pattern(self):
        """All label keys must follow story_arc.* pattern."""
        legend = get_arc_legend()
        for item in legend:
            assert item["label_key"].startswith("story_arc.")
            assert not item["label_key"].endswith("_description")

    def test_desc_keys_follow_pattern(self):
        """All description keys must follow story_arc.*_description pattern."""
        legend = get_arc_legend()
        for item in legend:
            assert item["desc_key"].startswith("story_arc.")
            assert item["desc_key"].endswith("_description")

    def test_no_chinese_in_keys(self):
        """Legend keys must NOT contain Chinese characters."""
        legend = get_arc_legend()
        for item in legend:
            for field in ("key", "label_key", "desc_key"):
                val = item[field]
                assert all(ord(c) < 0x4E00 for c in val), (
                    f"Legend item '{field}' = '{val}' contains CJK"
                )
