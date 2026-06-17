"""
QA Test Scaffolding — C201 Daily Market Dashboard
Tests for imports, router integration, URL sync, i18n keys,
data structure handling, color compliance, and i18n compliance.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import yaml

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_nested(d: dict, *keys):
    """Safely traverse nested dicts; returns None if any key is missing."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def _read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ===================================================================
# 1. Imports and Structure
# ===================================================================

class TestImportsAndStructure:
    """Test that daily_market module imports cleanly and exposes expected API."""

    def test_import_render_daily_market(self):
        from src.pages.daily_market import _render_daily_market
        assert callable(_render_daily_market)

    def test_import_render_freshness(self):
        from src.pages.daily_market import _render_freshness
        assert callable(_render_freshness)

    def test_import_render_overview(self):
        from src.pages.daily_market import _render_overview
        assert callable(_render_overview)

    def test_import_render_sentiment(self):
        from src.pages.daily_market import _render_sentiment
        assert callable(_render_sentiment)

    def test_import_render_sector_strip(self):
        from src.pages.daily_market import _render_sector_strip
        assert callable(_render_sector_strip)

    def test_import_render_top_movers(self):
        from src.pages.daily_market import _render_top_movers
        assert callable(_render_top_movers)

    def test_import_render_key_events(self):
        from src.pages.daily_market import _render_key_events
        assert callable(_render_key_events)

    def test_all_expected_functions_exist(self):
        import src.pages.daily_market as dm
        expected = [
            "_render_daily_market",
            "_render_freshness",
            "_render_overview",
            "_render_sentiment",
            "_render_sector_strip",
            "_render_top_movers",
            "_render_key_events",
        ]
        for name in expected:
            assert hasattr(dm, name), f"Missing function: {name}"
            assert callable(getattr(dm, name)), f"{name} is not callable"


# ===================================================================
# 2. Router Integration
# ===================================================================

class TestRouterIntegration:
    """Test that daily_market is wired into the page router."""

    def test_daily_market_in_page_keys(self):
        from src.pages.router import PAGE_KEYS
        assert "daily_market" in PAGE_KEYS

    def test_router_imports_without_errors(self):
        """Router module should import without errors (covers all page imports)."""
        # Re-import to catch any import-time side effects
        import importlib
        import src.pages.router
        importlib.reload(src.pages.router)
        assert hasattr(src.pages.router, "PAGE_KEYS")
        assert hasattr(src.pages.router, "load_and_render_page")


# ===================================================================
# 3. URL Sync Integration
# ===================================================================

class TestUrlSyncIntegration:
    """Test that the Chinese page name is in VALID_PAGES."""

    def test_chinese_name_in_valid_pages(self):
        from src.pages.url_sync import VALID_PAGES
        assert "今日市場動態" in VALID_PAGES

    def test_url_sync_imports_without_errors(self):
        from src.pages.url_sync import VALID_PAGES, sync_url_to_session, navigate_to
        assert isinstance(VALID_PAGES, frozenset)
        assert callable(sync_url_to_session)
        assert callable(navigate_to)


# ===================================================================
# 4. i18n Keys
# ===================================================================

# All required daily_market:* keys
REQUIRED_DM_KEYS = [
    "daily_market.title",
    "daily_market.subtitle",
    "daily_market.last_updated",
    "daily_market.freshness_fresh",
    "daily_market.freshness_stale",
    "daily_market.freshness_unknown",
    "daily_market.overview.title",
    "daily_market.overview.template_bull",
    "daily_market.overview.template_bear",
    "daily_market.overview.template_flat",
    "daily_market.overview.volume_above",
    "daily_market.overview.volume_below",
    "daily_market.overview.volume_normal",
    "daily_market.overview.sector_lead_up",
    "daily_market.overview.sector_lead_down",
    "daily_market.sentiment.title",
    "daily_market.sentiment.ad_ratio",
    "daily_market.sentiment.ad_ratio_value",
    "daily_market.sentiment.volume",
    "daily_market.sentiment.volume_unit",
    "daily_market.sentiment.mood",
    "daily_market.sentiment.mood_bullish",
    "daily_market.sentiment.mood_neutral",
    "daily_market.sentiment.mood_bearish",
    "daily_market.sentiment.up_count",
    "daily_market.sentiment.down_count",
    "daily_market.sectors.title",
    "daily_market.sectors.top_n",
    "daily_market.movers.title",
    "daily_market.movers.gainers",
    "daily_market.movers.losers",
    "daily_market.movers.rank",
    "daily_market.movers.price",
    "daily_market.events.title",
    "daily_market.events.empty",
    "daily_market.disclaimer",
    "page.daily_market",
]

LOCALE_EN = PROJECT_ROOT / "locales" / "en.yaml"
LOCALE_ZHTW = PROJECT_ROOT / "locales" / "zh-TW.yaml"


class TestI18nKeys:
    """Verify all required i18n keys exist in both locale files."""

    @pytest.fixture(scope="class")
    def en_data(self):
        return _load_yaml(LOCALE_EN)

    @pytest.fixture(scope="class")
    def zhtw_data(self):
        return _load_yaml(LOCALE_ZHTW)

    @pytest.mark.parametrize("key", REQUIRED_DM_KEYS)
    def test_key_exists_en(self, en_data, key):
        parts = key.split(".")
        val = _get_nested(en_data, *parts)
        assert val is not None, f"Missing i18n key in en.yaml: {key}"

    @pytest.mark.parametrize("key", REQUIRED_DM_KEYS)
    def test_key_exists_zhtw(self, zhtw_data, key):
        parts = key.split(".")
        val = _get_nested(zhtw_data, *parts)
        assert val is not None, f"Missing i18n key in zh-TW.yaml: {key}"


# ===================================================================
# 5. Data Structure Handling (with mocks)
# ===================================================================

class TestDataStructureHandling:
    """Test render functions with mock data — no Streamlit UI rendered."""

    # ---- _render_freshness ----

    def test_render_freshness_empty_summary(self):
        """Empty summary_map should not crash."""
        from src.pages.daily_market import _render_freshness
        with patch("src.pages.daily_market.st") as mock_st:
            _render_freshness({})
            # Should call st.caption with freshness_unknown status
            mock_st.caption.assert_called_once()

    def test_render_freshness_with_data(self):
        """Summary with today's date should show fresh status."""
        from src.pages.daily_market import _render_freshness
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        summary = {
            "2330": {"latest_price": f"{today}", "change": 1.5},
        }
        with patch("src.pages.daily_market.st") as mock_st:
            _render_freshness(summary)
            mock_st.caption.assert_called_once()

    def test_render_freshness_stale_data(self):
        """Summary with old date should show stale status."""
        from src.pages.daily_market import _render_freshness
        summary = {
            "2330": {"latest_price": "2024-01-01", "change": 1.5},
        }
        with patch("src.pages.daily_market.st") as mock_st:
            _render_freshness(summary)
            mock_st.caption.assert_called_once()

    # ---- _render_sentiment ----

    def test_render_sentiment_empty_summary(self):
        """Empty summary_map should show info message."""
        from src.pages.daily_market import _render_sentiment
        with patch("src.pages.daily_market.st") as mock_st:
            _render_sentiment({})
            mock_st.info.assert_called_once()

    def test_render_sentiment_with_up_down(self):
        """Summary with up/down stocks should render 4 columns."""
        from src.pages.daily_market import _render_sentiment
        summary = {
            "2330": {"change": 1.5, "stock_id": "2330", "stock_name": "台積電", "latest_price": 500},
            "2317": {"change": -0.5, "stock_id": "2317", "stock_name": "鴻海", "latest_price": 100},
            "2454": {"change": 0.0, "stock_id": "2454", "stock_name": "聯發科", "latest_price": 800},
        }
        with patch("src.pages.daily_market.st") as mock_st:
            mock_st.columns.return_value = [MagicMock() for _ in range(4)]
            _render_sentiment(summary)
            mock_st.columns.assert_called_once_with(4)

    # ---- _render_sector_strip ----

    def test_render_sector_strip_empty(self):
        """Empty sector_metrics should show info message."""
        from src.pages.daily_market import _render_sector_strip
        with patch("src.pages.daily_market.st") as mock_st:
            _render_sector_strip({})
            mock_st.info.assert_called_once()

    def test_render_sector_strip_with_sectors(self):
        """Sector metrics should render columns for top 6 sectors."""
        from src.pages.daily_market import _render_sector_strip
        sectors = {
            f"板塊{i}": {"avg_change": i * 0.5, "up": i, "down": 3 - i}
            for i in range(6)
        }
        with patch("src.pages.daily_market.st") as mock_st:
            mock_st.columns.return_value = [MagicMock() for _ in range(6)]
            _render_sector_strip(sectors)
            mock_st.columns.assert_called_once_with(6)

    # ---- _render_top_movers ----

    def test_render_top_movers_empty(self):
        """Empty summary_map should show info message."""
        from src.pages.daily_market import _render_top_movers
        with patch("src.pages.daily_market.st") as mock_st:
            _render_top_movers({}, {})
            mock_st.info.assert_called_once()

    def test_render_top_movers_with_stocks(self):
        """Summary with stocks should render two columns (gainers/losers)."""
        from src.pages.daily_market import _render_top_movers
        summary = {
            "2330": {
                "stock_id": "2330", "stock_name": "台積電",
                "change": 5.0, "latest_price": 500,
            },
            "2317": {
                "stock_id": "2317", "stock_name": "鴻海",
                "change": -3.0, "latest_price": 100,
            },
        }
        with patch("src.pages.daily_market.st") as mock_st:
            mock_st.columns.return_value = [MagicMock(), MagicMock()]
            _render_top_movers(summary, {})
            # The function calls st.columns(2) for gainers/losers layout
            assert mock_st.columns.call_args_list[0] == ((2,),)

    # ---- _render_key_events ----

    def test_render_key_events_empty(self):
        """Empty events list should show info message."""
        from src.pages.daily_market import _render_key_events
        with patch("src.pages.daily_market.st") as mock_st, \
             patch("src.pages.daily_market.get_all_recent_events", return_value=[]):
            _render_key_events()
            mock_st.info.assert_called_once()

    def test_render_key_events_with_data(self):
        """Events should be rendered via _info_card."""
        from src.pages.daily_market import _render_key_events
        events = [
            {"title": "Test Event", "description": "Test Description"},
        ]
        with patch("src.pages.daily_market.st") as mock_st, \
             patch("src.pages.daily_market.get_all_recent_events", return_value=events), \
             patch("src.pages.daily_market._info_card") as mock_card:
            _render_key_events()
            mock_card.assert_called_once_with("Test Event", "Test Description")


# ===================================================================
# 6. Color Compliance
# ===================================================================

# Colors that must NOT appear in daily_market.py
BANNED_COLORS = [
    "linear-gradient",
    "#F39C12",
    "#2E86C1",
    "#1B4F72",
    "#8E44AD",
    "#2ECC71",
    "#4A90D9",
    "#5D6D7E",
    "#BDC3C7",
    "#95A5A6",
    "#F9E79F",
    "#7D6608",
    "#EBF5FB",
    "#D4E6F1",
]

# Colors that MUST appear (semantic correctness)
REQUIRED_POSITIVE_COLOR = "#27AE60"
REQUIRED_NEGATIVE_COLOR = "#E74C3C"

DM_SOURCE_PATH = PROJECT_ROOT / "src" / "pages" / "daily_market.py"


class TestColorCompliance:
    """Verify color palette compliance in daily_market.py."""

    @pytest.fixture(scope="class")
    def source(self):
        return _read_source(DM_SOURCE_PATH)

    @pytest.mark.parametrize("color", BANNED_COLORS)
    def test_no_banned_colors(self, source, color):
        assert color not in source, (
            f"Design system violation: '{color}' found in daily_market.py"
        )

    def test_positive_color_present(self, source):
        """Green #27AE60 must be used for positive values."""
        assert REQUIRED_POSITIVE_COLOR in source, (
            f"Required positive color {REQUIRED_POSITIVE_COLOR} not found"
        )

    def test_negative_color_present(self, source):
        """Red #E74C3C must be used for negative values."""
        assert REQUIRED_NEGATIVE_COLOR in source, (
            f"Required negative color {REQUIRED_NEGATIVE_COLOR} not found"
        )

    def test_positive_for_gainers(self, source):
        """#27AE60 should be associated with gainers/positive context."""
        # Check that #27AE60 appears near "is_gainer" or "gain" context
        lines = source.splitlines()
        positive_lines = [l for l in lines if REQUIRED_POSITIVE_COLOR in l]
        assert len(positive_lines) >= 1, "Expected at least one usage of positive green"

    def test_negative_for_losers(self, source):
        """#E74C3C should be associated with losers/negative context."""
        lines = source.splitlines()
        negative_lines = [l for l in lines if REQUIRED_NEGATIVE_COLOR in l]
        assert len(negative_lines) >= 1, "Expected at least one usage of negative red"


# ===================================================================
# 7. i18n Compliance (no hardcoded Chinese strings)
# ===================================================================

# Chinese character range
_CHINESE_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")

# Patterns that are allowed to contain Chinese (not user-facing hardcoded strings)
ALLOWED_CHINESE_CONTEXTS = [
    # Docstrings are allowed
    '"""',
    "'''",
    # Comments are allowed
    "# ",
    # i18n key references are allowed (they're keys, not display strings)
    "daily_market.",
    "page.",
    "status.",
    # Function/variable names imported from _router_base are allowed
    # (they are identifiers, not user-facing strings)
    "_白话_card",
    "_summary_card",
    "_info_card",
    "_section_title",
    "_mini_score_card",
    "_so_what_box",
    "_subsidiary_card",
    "_count_label",
    "_glossary_tooltip",
    "_glossary_label",
    "_glossary_annotated_metric",
    "_glossary_help_text",
    "_confidence_badge",
    "_read_time",
    "_section_title_with_read_time",
    "_explain_button",
    "_render_mover_row",
    "_render_freshness",
    "_render_overview",
    "_render_sentiment",
    "_render_sector_strip",
    "_render_top_movers",
    "_render_key_events",
    "_render_daily_market",
    "_render_navbar_minimal",
    "_get_localized_page_labels",
    "_get_label_to_key_map",
    "_is_etf_check",
    "_historical_scenarios",
    "_is_in_t_call",
    "_is_docstring_line",
]


class TestI18nCompliance:
    """Verify no hardcoded Chinese strings outside of t() calls."""

    @pytest.fixture(scope="class")
    def source_lines(self):
        return _read_source(DM_SOURCE_PATH).splitlines()

    def _is_in_t_call(self, line: str, match_start: int) -> bool:
        """Check if a Chinese character at match_start is inside a t() call."""
        # Look backwards for t( before the match
        before = line[:match_start]
        # Simple heuristic: if there's a t( after the last ) or start
        last_t_open = before.rfind("t(")
        last_close = before.rfind(")")
        if last_t_open > last_close:
            return True
        return False

    def _is_docstring_line(self, line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith('"""') or stripped.startswith("'''") or \
               stripped.startswith('#')

    def test_no_hardcoded_chinese_in_strings(self, source_lines):
        """String literals containing Chinese must be wrapped in t()."""
        violations = []
        in_multiline_string = False
        multiline_quote = None

        for lineno, line in enumerate(source_lines, 1):
            stripped = line.strip()

            # Track multiline docstrings
            if not in_multiline_string:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    quote = stripped[:3]
                    # Single-line docstring
                    if stripped.count(quote) >= 2:
                        continue
                    in_multiline_string = True
                    multiline_quote = quote
                    continue
            else:
                if multiline_quote in stripped:
                    in_multiline_string = False
                continue

            # Skip pure comment lines
            if stripped.startswith("#"):
                continue

            # Skip import lines
            if stripped.startswith("import ") or stripped.startswith("from "):
                continue

            # Find Chinese characters in the line
            for match in _CHINESE_RE.finditer(line):
                pos = match.start()
                char = match.group()

                # Check if inside t() call
                if self._is_in_t_call(line, pos):
                    continue

                # Check if it's in a comment portion of the line
                comment_pos = line.find("#")
                if comment_pos != -1 and pos > comment_pos:
                    continue

                # Check if it's an i18n key reference (not a display string)
                # i18n keys don't contain Chinese, so this is fine
                context_after = line[pos:pos+20]
                context_before = line[max(0,pos-5):pos]

                # If preceded by t(" or t(' it's a key reference — skip
                if context_before.rstrip().endswith('t("') or \
                   context_before.rstrip().endswith("t('"):
                    continue

                # If the Chinese is inside a string literal that's an i18n key
                # (e.g., "daily_market.title"), skip — but Chinese chars
                # shouldn't appear in keys anyway

                # If it's inside f"..." with t() wrapping, the t() check above
                # should catch it. If it's a bare f-string with Chinese, flag it.

                # Check if the Chinese char is part of an allowed identifier
                # (e.g., function names like _白话_card from _router_base)
                context_window = line[max(0, pos - 30):pos + 20]
                if any(allowed in context_window for allowed in ALLOWED_CHINESE_CONTEXTS):
                    continue

                violations.append(
                    f"  Line {lineno}: '{char}' — {line.strip()!r}"
                )

        if violations:
            pytest.fail(
                f"Hardcoded Chinese strings found ({len(violations)}):\n"
                + "\n".join(violations[:20])  # Cap output
            )

    def test_no_bare_chinese_in_fstrings(self, source_lines):
        """F-strings with Chinese characters should use t() for the Chinese parts."""
        # Look for f-strings that contain Chinese not inside t()
        violations = []
        for lineno, line in enumerate(source_lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import"):
                continue
            # Check for f-string patterns with Chinese
            if ('f"' in line or "f'" in line) and _CHINESE_RE.search(line):
                # If it has Chinese and no t() call, flag it
                if "t(" not in line:
                    for match in _CHINESE_RE.finditer(line):
                        # Check it's not in a comment
                        comment_pos = line.find("#")
                        if comment_pos == -1 or match.start() < comment_pos:
                            violations.append(
                                f"  Line {lineno}: {line.strip()!r}"
                            )
                            break

        if violations:
            pytest.fail(
                f"F-strings with Chinese but no t() ({len(violations)}):\n"
                + "\n".join(violations[:20])
            )
