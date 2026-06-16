"""Tests for dividend_analyzer and roe_calculator services."""
from __future__ import annotations

import pandas as pd
import pytest

from src.services.dividend_analyzer import (
    extract_dividend_summary,
    _classify_frequency,
    _estimate_annual_proper,
    _empty_result,
)
from src.services.roe_calculator import calc_roe_ttm, is_seasonal_industry


# ── dividend_analyzer tests ──────────────────────────────────────────────

class TestClassifyFrequency:
    def test_annual_single_payment_per_year(self):
        df = pd.DataFrame({
            "year": ["113年", "112年", "111年"],
            "CashEarningsDistribution": [10.0, 9.0, 8.0],
        })
        assert _classify_frequency(df) == "annual"

    def test_quarterly_four_payments_per_year(self):
        df = pd.DataFrame({
            "year": ["113年", "113年", "113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0],
        })
        assert _classify_frequency(df) == "quarterly"

    def test_quarterly_three_payments_per_year(self):
        df = pd.DataFrame({
            "year": ["113年", "113年", "113年",
                     "112年", "112年", "112年"],
            "CashEarningsDistribution": [3.0, 3.0, 3.0, 2.0, 2.0, 2.0],
        })
        assert _classify_frequency(df) == "quarterly"

    def test_irregular(self):
        df = pd.DataFrame({
            "year": ["113年", "111年", "109年"],
            "CashEarningsDistribution": [5.0, 3.0, 2.0],
        })
        assert _classify_frequency(df) == "irregular"

    def test_empty(self):
        df = pd.DataFrame({"year": [], "CashEarningsDistribution": []})
        assert _classify_frequency(df) == "none"

    def test_no_year_column(self):
        df = pd.DataFrame({"CashEarningsDistribution": [1.0, 2.0]})
        assert _classify_frequency(df) == "irregular"


class TestEstimateAnnualProper:
    def test_annual_frequency_returns_latest_year(self):
        df = pd.DataFrame({
            "year": ["113年", "112年", "111年"],
            "CashEarningsDistribution": [10.0, 9.0, 8.0],
        })
        val, is_est = _estimate_annual_proper(df, "annual")
        assert val == 10.0
        assert is_est is False

    def test_quarterly_frequency_complete_year(self):
        """4 payments in latest year → sum them, not estimated."""
        df = pd.DataFrame({
            "year": ["113年", "113年", "113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0],
        })
        val, is_est = _estimate_annual_proper(df, "quarterly")
        assert val == 10.0  # 2.5 * 4
        assert is_est is False

    def test_quarterly_frequency_partial_year_uses_prior(self):
        """Only 2 payments in latest year → use prior year, mark estimated."""
        df = pd.DataFrame({
            "year": ["113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [2.5, 2.5, 2.0, 2.0, 2.0, 2.0],
        })
        val, is_est = _estimate_annual_proper(df, "quarterly")
        assert val == 8.0  # prior year: 2.0 * 4
        assert is_est is True

    def test_quarterly_three_payments_complete(self):
        """3 payments in latest year → sum them, mark estimated (not 4)."""
        df = pd.DataFrame({
            "year": ["113年", "113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0],
        })
        val, is_est = _estimate_annual_proper(df, "quarterly")
        assert val == 9.0  # 3.0 * 3
        assert is_est is True  # < 4 payments → estimated

    def test_empty_returns_none(self):
        df = pd.DataFrame({"year": [], "CashEarningsDistribution": []})
        val, is_est = _estimate_annual_proper(df, "annual")
        assert val is None
        assert is_est is False


class TestExtractDividendSummary:
    def test_none_input(self):
        result = extract_dividend_summary(None, current_price=100.0)
        assert result["has_data"] is False
        assert result["is_estimated"] is False

    def test_empty_dataframe(self):
        result = extract_dividend_summary(pd.DataFrame(), current_price=100.0)
        assert result["has_data"] is False

    def test_no_cash_dividend_column(self):
        df = pd.DataFrame({"year": ["113年"], "StockEarningsDistribution": [1.0]})
        result = extract_dividend_summary(df, current_price=100.0)
        assert result["has_data"] is False

    def test_all_zero_dividends(self):
        df = pd.DataFrame({
            "date": ["2024-03-15"],
            "year": ["113年"],
            "CashEarningsDistribution": [0.0],
            "StockEarningsDistribution": [0],
            "CashExDividendTradingDate": [""],
            "CashDividendPaymentDate": [""],
        })
        result = extract_dividend_summary(df, current_price=100.0)
        assert result["has_data"] is False

    def test_annual_company_basic(self):
        df = pd.DataFrame({
            "date": ["2024-03-15", "2023-03-15", "2022-03-15"],
            "year": ["113年", "112年", "111年"],
            "CashEarningsDistribution": [10.0, 9.5, 9.0],
            "StockEarningsDistribution": [0, 0, 0],
            "CashExDividendTradingDate": ["", "", ""],
            "CashDividendPaymentDate": ["2024-07-15", "2023-07-15", "2022-07-15"],
        })
        result = extract_dividend_summary(df, current_price=500.0)
        assert result["has_data"] is True
        assert result["estimated_annual"] == 10.0
        assert result["is_estimated"] is False
        assert result["estimated_yield"] == 2.0
        assert result["frequency"] == "annual"
        assert len(result["yearly_dividends"]) == 3

    def test_historical_yields_populated(self):
        df = pd.DataFrame({
            "date": ["2024-03-15", "2023-03-15", "2022-03-15"],
            "year": ["113年", "112年", "111年"],
            "CashEarningsDistribution": [10.0, 9.5, 9.0],
            "StockEarningsDistribution": [0, 0, 0],
            "CashExDividendTradingDate": ["", "", ""],
            "CashDividendPaymentDate": ["2024-07-15", "2023-07-15", "2022-07-15"],
        })
        result = extract_dividend_summary(df, current_price=500.0)
        assert len(result["historical_yields"]) == 3
        assert result["historical_yields"][0]["year"] == "113年"
        assert result["historical_yields"][0]["total_dividend"] == 10.0
        assert result["historical_yields"][0]["yield"] == 2.0

    def test_historical_yields_empty_without_price(self):
        df = pd.DataFrame({
            "date": ["2024-03-15"],
            "year": ["113年"],
            "CashEarningsDistribution": [10.0],
            "StockEarningsDistribution": [0],
            "CashExDividendTradingDate": [""],
            "CashDividendPaymentDate": ["2024-07-15"],
        })
        result = extract_dividend_summary(df, current_price=None)
        assert result["historical_yields"] == []

    def test_estimated_flag_for_quarterly_partial(self):
        """Quarterly company with incomplete current year → is_estimated=True."""
        df = pd.DataFrame({
            "date": ["2024-09-15", "2024-06-15",
                     "2023-12-15", "2023-09-15", "2023-06-15", "2023-03-15"],
            "year": ["113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [2.5, 2.5,
                                         2.3, 2.3, 2.3, 2.3],
            "StockEarningsDistribution": [0, 0, 0, 0, 0, 0],
            "CashExDividendTradingDate": ["", "", "", "", "", ""],
            "CashDividendPaymentDate": ["2024-10-15", "2024-07-15",
                                         "2024-01-15", "2023-10-15", "2023-07-15", "2023-04-15"],
        })
        result = extract_dividend_summary(df, current_price=200.0)
        assert result["has_data"] is True
        assert result["is_estimated"] is True  # Only 2 payments in current year

    def test_yearly_dividends_structure(self):
        df = pd.DataFrame({
            "date": ["2024-03-15"],
            "year": ["113年"],
            "CashEarningsDistribution": [10.0],
            "StockEarningsDistribution": [0.5],
            "CashExDividendTradingDate": ["2024-06-15"],
            "CashDividendPaymentDate": ["2024-07-15"],
        })
        result = extract_dividend_summary(df, current_price=500.0)
        div = result["yearly_dividends"][0]
        assert div["year"] == "113年"
        assert div["cash_div"] == 10.0
        assert div["stock_div"] == 0.5
        assert div["ex_date"] == "2024-06-15"
        assert div["pay_date"] == "2024-07-15"

    def test_plain_summary_contains_estimated_label_for_estimated(self):
        df = pd.DataFrame({
            "date": ["2024-09-15", "2024-06-15",
                     "2023-12-15", "2023-09-15", "2023-06-15", "2023-03-15"],
            "year": ["113年", "113年",
                     "112年", "112年", "112年", "112年"],
            "CashEarningsDistribution": [2.5, 2.5,
                                         2.3, 2.3, 2.3, 2.3],
            "StockEarningsDistribution": [0, 0, 0, 0, 0, 0],
            "CashExDividendTradingDate": ["", "", "", "", "", ""],
            "CashDividendPaymentDate": ["2024-10-15", "2024-07-15",
                                         "2024-01-15", "2023-10-15", "2023-07-15", "2023-04-15"],
        })
        result = extract_dividend_summary(df, current_price=200.0)
        assert "預估" in result["plain_summary"]


# ── roe_calculator tests ─────────────────────────────────────────────────

class TestIsSeasonalIndustry:
    def test_semiconductor(self):
        assert is_seasonal_industry("半導體業") is True

    def test_retail(self):
        assert is_seasonal_industry("零售") is True

    def test_tourism(self):
        assert is_seasonal_industry("觀光餐旅") is True

    def test_non_seasonal(self):
        assert is_seasonal_industry("金融業") is False

    def test_empty(self):
        assert is_seasonal_industry("") is False


class TestCalcRoeTtm:
    def _make_financial_df(self, net_incomes: list[float]) -> pd.DataFrame:
        """Create a financial DataFrame with quarterly net income data."""
        rows = []
        for i, ni in enumerate(net_incomes):
            rows.append({
                "type": "淨利",
                "value": ni,
                "date": f"2024-Q{4-i}",
            })
        return pd.DataFrame(rows)

    def _make_balance_sheet(self, equities: list[tuple[str, float]]) -> pd.DataFrame:
        """Create a balance sheet DataFrame."""
        rows = []
        for date, eq in equities:
            rows.append({
                "type": "權益總計",
                "value": eq,
                "date": date,
            })
        return pd.DataFrame(rows)

    def test_basic_ttm_roe(self):
        fin = self._make_financial_df([100, 110, 120, 130])
        bs = self._make_balance_sheet([("2024-Q4", 1000), ("2024-Q1", 900)])
        result = calc_roe_ttm(fin, bs)
        assert result is not None
        assert result["method"] == "TTM"
        assert result["quarters_used"] == 4
        # TTM NI = 100+110+120+130 = 460, avg equity = (1000+900)/2 = 950
        # ROE = 460/950*100 = 48.4
        assert result["roe"] == pytest.approx(48.4, abs=0.1)
        assert result["is_seasonal"] is False
        assert result["warning"] is None

    def test_seasonal_industry_adds_warning(self):
        fin = self._make_financial_df([100, 110, 120, 130])
        bs = self._make_balance_sheet([("2024-Q4", 1000), ("2024-Q1", 900)])
        result = calc_roe_ttm(fin, bs, industry="半導體業")
        assert result is not None
        assert result["is_seasonal"] is True
        assert result["warning"] is not None
        assert "季節性" in result["warning"]

    def test_partial_quarters_method_label(self):
        fin = self._make_financial_df([100, 110])
        bs = self._make_balance_sheet([("2024-Q2", 1000), ("2024-Q1", 900)])
        result = calc_roe_ttm(fin, bs)
        assert result is not None
        assert result["method"] == "2季累計"
        assert result["quarters_used"] == 2

    def test_single_quarter_method_label(self):
        fin = self._make_financial_df([100])
        bs = self._make_balance_sheet([("2024-Q1", 1000)])
        result = calc_roe_ttm(fin, bs)
        assert result is not None
        assert result["method"] == "單季"

    def test_insufficient_data_returns_none(self):
        fin = pd.DataFrame(columns=["type", "value", "date"])
        bs = self._make_balance_sheet([("2024-Q1", 1000)])
        result = calc_roe_ttm(fin, bs)
        assert result is None

    def test_no_equity_returns_none(self):
        fin = self._make_financial_df([100, 110])
        bs = pd.DataFrame({
            "type": ["現金", "現金"],
            "value": [50, 60],
            "date": ["2024-Q2", "2024-Q1"],
        })
        result = calc_roe_ttm(fin, bs)
        assert result is None

    def test_seasonal_partial_quarters_warning(self):
        fin = self._make_financial_df([100, 110])
        bs = self._make_balance_sheet([("2024-Q2", 1000), ("2024-Q1", 900)])
        result = calc_roe_ttm(fin, bs, industry="零售")
        assert result is not None
        assert result["is_seasonal"] is True
        assert "季節性" in result["warning"]
        assert "2季" in result["warning"]


# ── peer_comparison ROE fix tests ──────────────────────────────────────

class TestPeerComparisonRoeFix:
    """Verify that _get_benchmark_data uses calc_roe_ttm (not naive *4)."""

    def test_benchmark_roe_uses_ttm_not_naive_quadruple(self):
        """When only 1 quarter of net income is available, benchmark ROE must
        NOT be 4x the single-quarter value (the old bug).  calc_roe_ttm
        reports method='單季' and uses the raw quarter sum (no *4)."""
        import ast, inspect
        from src.pages import peer_comparison as pc

        source = inspect.getsource(pc._get_benchmark_data)
        # The old bug was: net_income * 4 / total_equity * 100
        assert "* 4" not in source, (
            "_get_benchmark_data still contains naive '* 4' ROE annualization"
        )
        assert "net_income * 4" not in source, (
            "_get_benchmark_data still contains 'net_income * 4' pattern"
        )

    def test_benchmark_roe_delegates_to_calc_roe_ttm(self):
        """_get_benchmark_data should call calc_roe_ttm for ROE."""
        import inspect
        from src.pages import peer_comparison as pc

        source = inspect.getsource(pc._get_benchmark_data)
        assert "calc_roe_ttm" in source, (
            "_get_benchmark_data does not call calc_roe_ttm"
        )

    def test_benchmark_roe_ttm_integration(self):
        """End-to-end: pass financial + balance sheet data and verify ROE
        matches the TTM calculation (not naive *4)."""
        import pandas as pd
        from unittest.mock import MagicMock, patch
        from src.pages.peer_comparison import _get_benchmark_data

        # Build mock client
        mock_client = MagicMock()
        mock_client.get_stock_info.return_value = pd.DataFrame([{
            "stock_name": "TestBench",
            "industry_category": "半導體業",
        }])
        mock_client.get_latest_per_pbr.return_value = pd.DataFrame()
        mock_client.get_monthly_revenue.return_value = pd.DataFrame()

        # Financial: 4 quarters of net income
        mock_client.get_financial_statement.return_value = pd.DataFrame([
            {"type": "淨利", "value": 100, "date": "2024-Q4"},
            {"type": "淨利", "value": 110, "date": "2024-Q3"},
            {"type": "淨利", "value": 120, "date": "2024-Q2"},
            {"type": "淨利", "value": 130, "date": "2024-Q1"},
        ])
        # Balance sheet: beginning and ending equity
        mock_client.get_balance_sheet.return_value = pd.DataFrame([
            {"type": "權益總計", "value": 1000, "date": "2024-Q4"},
            {"type": "權益總計", "value": 900, "date": "2024-Q1"},
        ])

        result = _get_benchmark_data(mock_client, "9999")
        assert result is not None
        roe = result["extra_metrics"].get("roe")
        assert roe is not None, "ROE should be calculated"

        # TTM NI = 100+110+120+130 = 460, avg equity = (1000+900)/2 = 950
        # ROE = 460/950*100 ≈ 48.4
        # Old buggy method: 100*4/1000*100 = 40.0 (wrong!)
        assert roe == pytest.approx(48.4, abs=0.1), (
            f"ROE should be ~48.4 (TTM), got {roe}"
        )

    def test_benchmark_roe_single_quarter_not_quadrupled(self):
        """With only 1 quarter, ROE should NOT be *4."""
        import pandas as pd
        from unittest.mock import MagicMock
        from src.pages.peer_comparison import _get_benchmark_data

        mock_client = MagicMock()
        mock_client.get_stock_info.return_value = pd.DataFrame([{
            "stock_name": "TestBench",
            "industry_category": "半導體業",
        }])
        mock_client.get_latest_per_pbr.return_value = pd.DataFrame()
        mock_client.get_monthly_revenue.return_value = pd.DataFrame()

        # Only 1 quarter of net income
        mock_client.get_financial_statement.return_value = pd.DataFrame([
            {"type": "淨利", "value": 50, "date": "2024-Q1"},
        ])
        mock_client.get_balance_sheet.return_value = pd.DataFrame([
            {"type": "權益總計", "value": 1000, "date": "2024-Q1"},
        ])

        result = _get_benchmark_data(mock_client, "9999")
        assert result is not None
        roe = result["extra_metrics"].get("roe")
        assert roe is not None

        # TTM with 1 quarter: 50/1000*100 = 5.0
        # Old buggy method: 50*4/1000*100 = 20.0 (wrong!)
        assert roe == pytest.approx(5.0, abs=0.1), (
            f"Single-quarter ROE should be ~5.0 (not *4), got {roe}"
        )
