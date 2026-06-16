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

# Curated historical scenarios for major Taiwan stocks
_HISTORICAL_SCENARIOS = {
    "2330": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月疫情恐慌低點（約 230 元）買入台積電，"
                "持有至今（2025 年）股價約 1,000+ 元，\n\n"
                "📈 **報酬率：約 330%**（不含股息）\n\n"
                "💡 這說明了「在恐慌中買入優質資產」的長期價值。"
            ),
        },
        {
            "title": "情境二：2022 年高點買入",
            "content": (
                "如果你在 2022 年 1 月高點（約 670 元）買入台積電，"
                "隨後面臨全球半導體庫存修正，股價一度跌至 370 元。\n\n"
                "📉 **短期跌幅：約 45%**\n\n"
                "💡 即使是好公司，追高買入也可能面臨大幅回檔。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入台積電，"
                "無論股價漲跌都持續買入，\n\n"
                "📊 **年化報酬率約 25-30%**\n\n"
                "💡 定期定額能有效平滑買入成本，適合長期投資者。"
            ),
        },
    ],
    "2317": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 60 元）買入鴻海，"
                "持有至今（2025 年）股價約 170 元，\n\n"
                "📈 **報酬率：約 180%**（含股息）\n\n"
                "💡 鴻海的轉型故事需要耐心，長期持有才能看到成果。"
            ),
        },
        {
            "title": "情境二：2017 年高點買入",
            "content": (
                "如果你在 2017 年高點（約 110 元）買入鴻海，"
                "隨後面臨蘋果手機銷售放緩，股價長期低迷。\n\n"
                "📉 **5 年報酬：約 0-20%**（含股息）\n\n"
                "💡 買在高點可能需要更長的時間才能回本。"
            ),
        },
        {
            "title": "情境三：AI 伺服器題材爆發",
            "content": (
                "如果你在 2023 年初（約 100 元）看好 AI 伺服器趨勢買入鴻海，"
                "至今股價約 170 元，\n\n"
                "📈 **報酬率：約 70%**\n\n"
                "💡 掌握產業趨勢，在題材發酵前布局能獲得超額報酬。"
            ),
        },
    ],
    "2454": [
        {
            "title": "情境一：2021 年高點買入",
            "content": (
                "如果你在 2021 年高點（約 1,100 元）買入聯發科，"
                "隨後面臨手機市場衰退與庫存修正。\n\n"
                "📉 **短期跌幅：約 40%**\n\n"
                "💡 即使是成長股，在估值過高時買入也有風險。"
            ),
        },
        {
            "title": "情境二：2023 年低點買入",
            "content": (
                "如果你在 2023 年低點（約 600 元）買入聯發科，"
                "受惠於手機市場復甦與 AI PC 題材，\n\n"
                "📈 **報酬率：約 50-80%**\n\n"
                "💡 在產業谷底買入優質公司，報酬可觀。"
            ),
        },
        {
            "title": "情境三：定期定額 3 年",
            "content": (
                "如果你從 2022 年起每月定期定額買入聯發科，\n\n"
                "📊 **年化報酬率約 15-20%**\n\n"
                "💡 定期定額在高波動的科技股上特別有效。"
            ),
        },
    ],
    "2308": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 100 元）買入台達電，"
                "持有至今（2025 年）股價約 380 元，\n\n"
                "📈 **報酬率：約 280%**（含股息）\n\n"
                "💡 台達電的長期成長性在電源管理領域無可取代。"
            ),
        },
        {
            "title": "情境二：AI 資料中心題材",
            "content": (
                "如果你在 2023 年初（約 250 元）看好 AI 資料中心電源需求買入台達電，\n\n"
                "📈 **報酬率：約 50%**\n\n"
                "💡 掌握 AI 基礎建設的供應鏈機會。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入台達電，\n\n"
                "📊 **年化報酬率約 25%**\n\n"
                "💡 穩健成長股適合定期定額長期投資。"
            ),
        },
    ],
    "2881": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 35 元）買入富邦金，"
                "持有至今（2025 年）股價約 80 元，\n\n"
                "📈 **報酬率：約 130%**（含股息）\n\n"
                "💡 金融股在低點買入，長期報酬相當可觀。"
            ),
        },
        {
            "title": "情境二：升息循環受惠",
            "content": (
                "如果你在 2022 年升息循環開始前（約 60 元）買入富邦金，"
                "受惠於利差擴大，\n\n"
                "📈 **報酬率：約 30-40%**\n\n"
                "💡 金融股在升息環境下通常表現較好。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入富邦金，\n\n"
                "📊 **年化報酬率約 15%**\n\n"
                "💡 金融股配息穩定，適合存股族。"
            ),
        },
    ],
    "2882": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 30 元）買入國泰金，"
                "持有至今（2025 年）股價約 60 元，\n\n"
                "📈 **報酬率：約 100%**（含股息）\n\n"
                "💡 壽險股在低利率環境反轉後表現亮眼。"
            ),
        },
        {
            "title": "情境二：IFRS 17 接軌挑戰",
            "content": (
                "如果你在 2023 年（約 40 元）買入國泰金，"
                "面臨 IFRS 17 會計準則接軌的不確定性，\n\n"
                "📊 **報酬率：約 30-50%**\n\n"
                "💡 政策變化可能帶來短期波動，但長期影響有限。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入國泰金，\n\n"
                "📊 **年化報酬率約 12%**\n\n"
                "💡 金融股適合長期持有，享受穩定配息。"
            ),
        },
    ],
    "1301": [
        {
            "title": "情境一：2021 年景氣高點買入",
            "content": (
                "如果你在 2021 年石化景氣高點（約 110 元）買入台塑，"
                "隨後面臨景氣反轉與中國產能過剩。\n\n"
                "📉 **跌幅：約 30-40%**\n\n"
                "💡 景氣循環股在高點買入風險極大。"
            ),
        },
        {
            "title": "情境二：2020 年低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 70 元）買入台塑，"
                "持有至今（2025 年）股價約 70-80 元，\n\n"
                "📊 **報酬：主要來自配息，資本增值有限**\n\n"
                "💡 傳統產業股的成長性有限，但配息穩定。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入台塑，\n\n"
                "📊 **年化報酬率約 5-8%**（主要來自股息）\n\n"
                "💡 景氣循環股適合在低點定期定額布局。"
            ),
        },
    ],
    "2002": [
        {
            "title": "情境一：2021 年鋼鐵景氣高點",
            "content": (
                "如果你在 2021 年鋼鐵景氣高點（約 40 元）買入中鋼，"
                "隨後面臨需求下滑與原物料價格回落。\n\n"
                "📉 **跌幅：約 25-35%**\n\n"
                "💡 鋼鐵股景氣循環明顯，追高風險大。"
            ),
        },
        {
            "title": "情境二：2020 年低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 18 元）買入中鋼，"
                "持有至今（2025 年）股價約 23 元，\n\n"
                "📊 **報酬：約 30%**（含股息）\n\n"
                "💡 在景氣谷底買入，等待下一輪循環。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入中鋼，\n\n"
                "📊 **年化報酬率約 5-8%**\n\n"
                "💡 鋼鐵股適合在景氣低點定期定額布局。"
            ),
        },
    ],
    "2382": [
        {
            "title": "情境一：2020 年疫情低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 55 元）買入廣達，"
                "持有至今（2025 年）股價約 270 元，\n\n"
                "📈 **報酬率：約 390%**（含股息）\n\n"
                "💡 AI 伺服器趨勢讓廣達從 NB 代工廠華麗轉身。"
            ),
        },
        {
            "title": "情境二：2023 年 AI 題材爆發前",
            "content": (
                "如果你在 2023 年初（約 80 元）看好 AI 伺服器趨勢買入廣達，\n\n"
                "📈 **報酬率：約 200%+**\n\n"
                "💡 掌握產業趨勢，在爆發前布局報酬驚人。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入廣達，\n\n"
                "📊 **年化報酬率約 30%**\n\n"
                "💡 轉型成功的公司，定期定額也能獲得超額報酬。"
            ),
        },
    ],
    "3045": [
        {
            "title": "情境一：2017 年高點買入",
            "content": (
                "如果你在 2017 年歷史高點（約 6,000 元）買入大立光，"
                "隨後面臨中國競爭對手崛起與手機市場飽和。\n\n"
                "📉 **跌幅：約 60-70%**\n\n"
                "💡 即使是護城河極深的公司，也可能面臨結構性挑戰。"
            ),
        },
        {
            "title": "情境二：2020 年低點買入",
            "content": (
                "如果你在 2020 年 3 月（約 3,000 元）買入大立光，"
                "持有至今（2025 年）股價約 2,400 元，\n\n"
                "📉 **跌幅：約 20%**\n\n"
                "💡 即使是低點買入，若產業結構惡化仍可能虧損。"
            ),
        },
        {
            "title": "情境三：定期定額 5 年",
            "content": (
                "如果你從 2020 年起每月定期定額買入大立光，\n\n"
                "📊 **年化報酬：約 -5% 至 0%**\n\n"
                "💡 定期定額無法避免結構性衰退的產業。"
            ),
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
                _scenario_card(scenario["title"], scenario["content"], "🔍")
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
