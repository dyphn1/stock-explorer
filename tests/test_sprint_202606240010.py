import sys
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _load_yaml(path: Path) -> dict:
    """Load YAML file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_nested(d: dict, *keys):
    """Safely traverse nested dicts; returns None if any key is missing."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


class TestETFComparison:
    """Tests for the ETF comparison section."""

    def test_etf_comparison_locale_keys_exist(self):
        """Verify all etf.detail.comparison.* keys exist in both en.yaml and zh-TW.yaml."""
        en_path = PROJECT_ROOT / "locales" / "en.yaml"
        zh_tw_path = PROJECT_ROOT / "locales" / "zh-TW.yaml"
        en_data = _load_yaml(en_path)
        zh_tw_data = _load_yaml(zh_tw_path)
        
        expected_keys = [
            "title",
            "expense_ratio",
            "tracking_error",
            "dividend_yield",
            "current_etf",
            "note",
        ]
        
        for key in expected_keys:
            full_key = f"etf.detail.comparison.{key}"
            en_val = _get_nested(en_data, *full_key.split("."))
            zh_tw_val = _get_nested(zh_tw_data, *full_key.split("."))
            assert en_val is not None, f"Missing i18n key in en.yaml: {full_key}"
            assert zh_tw_val is not None, f"Missing i18n key in zh-TW.yaml: {full_key}"

    def test_etf_comparison_section_renders(self):
        """Mock the data dict and verify the comparison section renders without errors."""
        from src.pages.etf_detail import _render_etf_detail
        
        data = {
            "stock_id": "0050",
            "stock_name": "台灣50",
            "industry": "ETF",
            "latest_price": {"close": 100.0, "change": 1.0},
            "institutional": [],
            "dividend": [],
            "extra_metrics": {
                "expense_ratio": 0.09,
                "tracking_error": 0.05,
                "dividend_yield": 4.2,
            },
            "daily_price": [],
        }
        
        client = MagicMock()
        
        with patch("src.pages.etf_detail.st") as mock_st:
            mock_st.columns.side_effect = lambda x: [MagicMock() for _ in range(len(x) if isinstance(x, list) else x)]
            _render_etf_detail(data, client)
            # Basic check: no exception means render succeeded
            assert True


class TestWhyDidThisMove:
    """Tests for the Why Did This Move section."""

    def test_why_did_this_move_locale_keys_exist(self):
        """Verify all why_did_this_move.* keys exist in both en.yaml and zh-TW.yaml."""
        en_path = PROJECT_ROOT / "locales" / "en.yaml"
        zh_tw_path = PROJECT_ROOT / "locales" / "zh-TW.yaml"
        en_data = _load_yaml(en_path)
        zh_tw_data = _load_yaml(zh_tw_path)
        
        expected_keys = [
            "title",
            "institutional_buying",
            "institutional_selling",
            "price_surge",
            "price_drop",
            "check_news",
            "no_data",
        ]
        
        for key in expected_keys:
            full_key = f"why_did_this_move.{key}"
            en_val = _get_nested(en_data, *full_key.split("."))
            zh_tw_val = _get_nested(zh_tw_data, *full_key.split("."))
            assert en_val is not None, f"Missing i18n key in en.yaml: {full_key}"
            assert zh_tw_val is not None, f"Missing i18n key in zh-TW.yaml: {full_key}"

    def test_why_did_this_move_institutional_buying(self):
        """Mock data with net positive institutional buying, verify buying explanation."""
        from src.pages.business_card._sections._why_did_this_move import _render_why_did_this_move
        
        data = {
            "latest_price": {"change": 0.0},
            "institutional": {
                "buy": [100, 200],
                "sell": [50, 30],
            },
        }
        
        client = MagicMock()
        
        with patch("src.pages.business_card._sections._why_did_this_move.st") as mock_st:
            with patch("src.pages.business_card._sections._why_did_this_move._plain_card") as mock_plain_card:
                _render_why_did_this_move(data, client)
                mock_plain_card.assert_called_once()
                # Check that the explanation contains the buying phrase
                args, _ = mock_plain_card.call_args
                explanation = args[1]
                from src.core.i18n import t
                assert t("why_did_this_move.institutional_buying") in explanation

    def test_why_did_this_move_institutional_selling(self):
        """Mock data with net negative institutional selling, verify selling explanation."""
        from src.pages.business_card._sections._why_did_this_move import _render_why_did_this_move
        
        data = {
            "latest_price": {"change": 0.0},
            "institutional": {
                "buy": [50, 30],
                "sell": [100, 200],
            },
        }
        
        client = MagicMock()
        
        with patch("src.pages.business_card._sections._why_did_this_move.st") as mock_st:
            with patch("src.pages.business_card._sections._why_did_this_move._plain_card") as mock_plain_card:
                _render_why_did_this_move(data, client)
                mock_plain_card.assert_called_once()
                args, _ = mock_plain_card.call_args
                explanation = args[1]
                from src.core.i18n import t
                assert t("why_did_this_move.institutional_selling") in explanation

    def test_why_did_this_move_no_data(self):
        """Mock data with no institutional data, verify fallback message."""
        from src.pages.business_card._sections._why_did_this_move import _render_why_did_this_move
        
        data = {
            "latest_price": {"change": 0.0},
            "institutional": None,
        }
        
        client = MagicMock()
        
        with patch("src.pages.business_card._sections._why_did_this_move.st") as mock_st:
            with patch("src.pages.business_card._sections._why_did_this_move._plain_card") as mock_plain_card:
                _render_why_did_this_move(data, client)
                mock_plain_card.assert_called_once()
                args, _ = mock_plain_card.call_args
                explanation = args[1]
                from src.core.i18n import t
                assert explanation == t("why_did_this_move.no_data")


class TestGeneral:
    """General tests for the new sections."""

    def test_no_raw_keys_in_new_sections(self):
        """Verify no raw i18n key patterns in the new code."""
        sprint_files = [
            PROJECT_ROOT / "src" / "pages" / "etf_detail.py",
            PROJECT_ROOT / "src" / "pages" / "business_card" / "_sections" / "_why_did_this_move.py",
        ]
        
        raw_key_patterns = [
            "etf.detail.comparison.",
            "why_did_this_move.",
        ]
        
        for file_path in sprint_files:
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for pattern in raw_key_patterns:
                    if pattern in line:
                        # Simple check: if the pattern is not inside a t() call
                        if "t(" not in line and "t('" not in line:
                            # Allow false positives for now; in practice, we'd do a more thorough check
                            # For this test, we'll just note that we found a pattern and fail if it's likely raw.
                            # We'll check if the pattern is inside a string that is not a translation call.
                            # We'll skip lines where the pattern is inside a comment or a docstring.
                            # We'll also skip if the line contains a translation call for a different key.
                            # Given time, we'll just fail if we see the pattern and no t( or t(' on the line.
                            # This is a heuristic.
                            raise AssertionError(
                                f"Raw i18n key pattern '{pattern}' found in {file_path}:{i}\\n{line}"
                            )