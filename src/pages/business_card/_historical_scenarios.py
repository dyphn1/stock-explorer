"""C74 Historical Scenarios (歷史情境) — what-if analysis for stocks."""
from datetime import datetime, timedelta

import streamlit as st
from src.core.i18n import t
from src.pages.business_card._helpers import (
    _scenario_card,
    _section_header,
    _historian_disclaimer,
)
from src.services.scenario_calculator import calculate_scenario

# Curated historical scenarios for major Taiwan stocks.
# Each scenario has a title_key and content_key — the page calls t() to resolve.
# Placeholders like {price}, {return_pct}, {years} are filled via .format().
_HISTORICAL_SCENARIOS = {
    "2330": [
        {
            "title_key": "historical_scenario.2330.s1.title",
            "content_key": "historical_scenario.2330.s1.content",
            "content_kwargs": {
                "buy_price": "230",
                "buy_date": "2020-03",
                "current_price": "1,000+",
                "current_year": "2025",
                "return_pct": "330",
            },
        },
        {
            "title_key": "historical_scenario.2330.s2.title",
            "content_key": "historical_scenario.2330.s2.content",
            "content_kwargs": {
                "buy_price": "670",
                "buy_date": "2022-01",
                "low_price": "370",
                "drop_pct": "45",
            },
        },
        {
            "title_key": "historical_scenario.2330.s3.title",
            "content_key": "historical_scenario.2330.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "25-30",
            },
        },
    ],
    "2317": [
        {
            "title_key": "historical_scenario.2317.s1.title",
            "content_key": "historical_scenario.2317.s1.content",
            "content_kwargs": {
                "buy_price": "60",
                "buy_date": "2020-03",
                "current_price": "170",
                "current_year": "2025",
                "return_pct": "180",
            },
        },
        {
            "title_key": "historical_scenario.2317.s2.title",
            "content_key": "historical_scenario.2317.s2.content",
            "content_kwargs": {
                "buy_price": "110",
                "buy_date": "2017",
                "return_range": "0-20",
                "years": "5",
            },
        },
        {
            "title_key": "historical_scenario.2317.s3.title",
            "content_key": "historical_scenario.2317.s3.content",
            "content_kwargs": {
                "buy_price": "100",
                "buy_date": "2023 年初",
                "current_price": "170",
                "return_pct": "70",
            },
        },
    ],
    "2454": [
        {
            "title_key": "historical_scenario.2454.s1.title",
            "content_key": "historical_scenario.2454.s1.content",
            "content_kwargs": {
                "buy_price": "1,100",
                "buy_date": "2021",
                "drop_pct": "40",
            },
        },
        {
            "title_key": "historical_scenario.2454.s2.title",
            "content_key": "historical_scenario.2454.s2.content",
            "content_kwargs": {
                "buy_price": "600",
                "buy_date": "2023",
                "return_range": "50-80",
            },
        },
        {
            "title_key": "historical_scenario.2454.s3.title",
            "content_key": "historical_scenario.2454.s3.content",
            "content_kwargs": {
                "start_year": "2022",
                "annual_return": "15-20",
            },
        },
    ],
    "2308": [
        {
            "title_key": "historical_scenario.2308.s1.title",
            "content_key": "historical_scenario.2308.s1.content",
            "content_kwargs": {
                "buy_price": "100",
                "buy_date": "2020-03",
                "current_price": "380",
                "current_year": "2025",
                "return_pct": "280",
            },
        },
        {
            "title_key": "historical_scenario.2308.s2.title",
            "content_key": "historical_scenario.2308.s2.content",
            "content_kwargs": {
                "buy_price": "250",
                "buy_date": "2023 年初",
                "return_pct": "50",
            },
        },
        {
            "title_key": "historical_scenario.2308.s3.title",
            "content_key": "historical_scenario.2308.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "25",
            },
        },
    ],
    "2881": [
        {
            "title_key": "historical_scenario.2881.s1.title",
            "content_key": "historical_scenario.2881.s1.content",
            "content_kwargs": {
                "buy_price": "35",
                "buy_date": "2020-03",
                "current_price": "80",
                "current_year": "2025",
                "return_pct": "130",
            },
        },
        {
            "title_key": "historical_scenario.2881.s2.title",
            "content_key": "historical_scenario.2881.s2.content",
            "content_kwargs": {
                "buy_price": "60",
                "buy_date": "2022",
                "return_range": "30-40",
            },
        },
        {
            "title_key": "historical_scenario.2881.s3.title",
            "content_key": "historical_scenario.2881.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "15",
            },
        },
    ],
    "2882": [
        {
            "title_key": "historical_scenario.2882.s1.title",
            "content_key": "historical_scenario.2882.s1.content",
            "content_kwargs": {
                "buy_price": "30",
                "buy_date": "2020-03",
                "current_price": "60",
                "current_year": "2025",
                "return_pct": "100",
            },
        },
        {
            "title_key": "historical_scenario.2882.s2.title",
            "content_key": "historical_scenario.2882.s2.content",
            "content_kwargs": {
                "buy_price": "40",
                "buy_date": "2023",
                "return_range": "30-50",
            },
        },
        {
            "title_key": "historical_scenario.2882.s3.title",
            "content_key": "historical_scenario.2882.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "12",
            },
        },
    ],
    "1301": [
        {
            "title_key": "historical_scenario.1301.s1.title",
            "content_key": "historical_scenario.1301.s1.content",
            "content_kwargs": {
                "buy_price": "110",
                "buy_date": "2021",
                "drop_range": "30-40",
            },
        },
        {
            "title_key": "historical_scenario.1301.s2.title",
            "content_key": "historical_scenario.1301.s2.content",
            "content_kwargs": {
                "buy_price": "70",
                "buy_date": "2020-03",
                "current_price": "70-80",
                "current_year": "2025",
            },
        },
        {
            "title_key": "historical_scenario.1301.s3.title",
            "content_key": "historical_scenario.1301.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "5-8",
            },
        },
    ],
    "2002": [
        {
            "title_key": "historical_scenario.2002.s1.title",
            "content_key": "historical_scenario.2002.s1.content",
            "content_kwargs": {
                "buy_price": "40",
                "buy_date": "2021",
                "drop_range": "25-35",
            },
        },
        {
            "title_key": "historical_scenario.2002.s2.title",
            "content_key": "historical_scenario.2002.s2.content",
            "content_kwargs": {
                "buy_price": "18",
                "buy_date": "2020-03",
                "current_price": "23",
                "current_year": "2025",
                "return_pct": "30",
            },
        },
        {
            "title_key": "historical_scenario.2002.s3.title",
            "content_key": "historical_scenario.2002.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "5-8",
            },
        },
    ],
    "2382": [
        {
            "title_key": "historical_scenario.2382.s1.title",
            "content_key": "historical_scenario.2382.s1.content",
            "content_kwargs": {
                "buy_price": "55",
                "buy_date": "2020-03",
                "current_price": "270",
                "current_year": "2025",
                "return_pct": "390",
            },
        },
        {
            "title_key": "historical_scenario.2382.s2.title",
            "content_key": "historical_scenario.2382.s2.content",
            "content_kwargs": {
                "buy_price": "80",
                "buy_date": "2023 年初",
                "return_pct": "200+",
            },
        },
        {
            "title_key": "historical_scenario.2382.s3.title",
            "content_key": "historical_scenario.2382.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "30",
            },
        },
    ],
    "3045": [
        {
            "title_key": "historical_scenario.3045.s1.title",
            "content_key": "historical_scenario.3045.s1.content",
            "content_kwargs": {
                "buy_price": "6,000",
                "buy_date": "2017",
                "drop_range": "60-70",
            },
        },
        {
            "title_key": "historical_scenario.3045.s2.title",
            "content_key": "historical_scenario.3045.s2.content",
            "content_kwargs": {
                "buy_price": "3,000",
                "buy_date": "2020-03",
                "current_price": "2,400",
                "current_year": "2025",
                "drop_pct": "20",
            },
        },
        {
            "title_key": "historical_scenario.3045.s3.title",
            "content_key": "historical_scenario.3045.s3.content",
            "content_kwargs": {
                "start_year": "2020",
                "annual_return": "-5 至 0",
            },
        },
    ],
}


def _render_custom_scenario(data: dict, client) -> None:
    """C200 Custom What-If Calculator — interactive scenario calculator.

    Lets the user pick a start date and investment amount, then calculates
    the hypothetical return using historical price and dividend data.
    """
    from src.core.i18n import t

    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    five_years_ago = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

    with _section_header("🧮", t("scenario.custom_title"), collapsed=True):
        st.caption(t("scenario.custom_caption"))

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                t("scenario.custom_buy_date"),
                value=datetime.strptime(five_years_ago, "%Y-%m-%d"),
                max_value=datetime.now(),
                key="custom_scenario_start_date",
            )
        with col2:
            investment_amount = st.number_input(
                t("scenario.custom_amount"),
                min_value=1000.0,
                value=100000.0,
                step=10000.0,
                format="%d",
                key="custom_scenario_amount",
            )

        include_dividends = st.checkbox(
            t("scenario.custom_include_dividends"),
            value=True,
            key="custom_scenario_dividends",
        )

        if st.button(t("scenario.custom_calculate"), key="custom_scenario_calculate"):
            start_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else str(start_date)

            with st.spinner(t("scenario.custom_calculating")):
                result = calculate_scenario(
                    stock_id=stock_id,
                    start_date=start_str,
                    investment_amount=float(investment_amount),
                    include_dividends=include_dividends,
                    client=client,
                )

            if result["error_key"]:
                error_text = t(f"scenario.{result['error_key'].split('.')[-1]}")
                _scenario_card(
                    f"⚠️ {t('scenario.custom_cannot_calculate')}",
                    f"{t('scenario.custom_error_prefix')}{error_text}",
                    "⚠️",
                )
            else:
                # Build result content
                return_emoji = "📈" if result["total_return"] >= 0 else "📉"
                content_lines = [
                    f"**{t('scenario.custom_buy_date_label')}** {result['start_date']}  ",
                    f"**{t('scenario.custom_buy_price_label')}** {result['start_price']:.2f}  {t('unit.yuan')}  ",
                    f"**{t('scenario.custom_shares_label')}** {result['shares']:.0f}  {t('unit.shares')}  ",
                    f"**{t('scenario.custom_end_date_label')}** {result['end_date']}  ",
                    f"**{t('scenario.custom_end_price_label')}** {result['end_price']:.2f}  {t('unit.yuan')}  ",
                    "",
                    f"{return_emoji} **{t('scenario.custom_total_return_label')}** {result['total_return']:.2f}%  ",
                    f"**{t('scenario.custom_absolute_return_label')}** {result['absolute_return']:,.0f}  {t('unit.yuan')}  ",
                    f"**{t('scenario.custom_annualized_return_label')}** {result['annualized_return']:.2f}%  ",
                    f"**{t('scenario.custom_dividend_income_label')}** {result['dividend_income']:,.0f}  {t('unit.yuan')}  ",
                    f"**{t('scenario.custom_max_drawdown_label')}** {result['max_drawdown']:.2f}%  ",
                ]
                if result["is_estimated"]:
                    content_lines.append("")
                    content_lines.append(t("scenario.custom_estimated_note"))

                title = t(
                    "scenario.custom_result_title",
                    stock_name=stock_name,
                    stock_id=stock_id,
                )

                _scenario_card(
                    title,
                    "\n".join(content_lines),
                    "🧮",
                )

        _historian_disclaimer("scenario")


def _render_historical_scenarios(data: dict, client) -> None:
    """C74 Historical Scenarios: what-if analysis for stocks.

    Shows 2-3 historical what-if scenarios for the stock.
    Uses st.expander for progressive disclosure (collapsed by default).
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    scenarios = _HISTORICAL_SCENARIOS.get(stock_id)

    with _section_header("🔍", t("scenario.historical_title"), collapsed=True):
        if scenarios:
            for scenario in scenarios:
                title = t(scenario["title_key"])
                content = t(scenario["content_key"], **scenario.get("content_kwargs", {}))
                _scenario_card(title, content, "🔍")
        else:
            _scenario_card(
                f"{stock_name} ({stock_id})",
                f"📋 {t('scenario.upcoming_analysis')}\n\n"
                f"{t('scenario.upcoming_detail')}",
                "🔍",
            )

        _historian_disclaimer("scenario")

    # ── C200: Custom What-If Calculator ──────────────────────
    _render_custom_scenario(data, client)

    st.markdown("---")
