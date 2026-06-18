"""
財務體質頁 — M2 第二頁
目標：用生活化比喻理解財務數據
"""

import streamlit as st
import pandas as pd
from src.services.chart import create_funnel_chart
from src.services.analogy_engine import (
    get_gross_margin_analogy,
    get_roe_analogy,
    get_debt_ratio_analogy,
    get_per_analogy,
    get_pbr_analogy,
    get_dividend_analogy,
)
from src.services.roe_calculator import calc_roe_ttm, is_seasonal_industry
from src.services.dividend_analyzer import extract_dividend_summary
from src.pages._router_base import filter_by_timeline, _section_title, _白话_card, _info_card
from src.services.financial_metrics import find_financial_value
from src.pages.timeline_controls import render_timeline_selector
from src.core.i18n import t, format_amount, format_percent


def _render_financial_health(data: dict):
    """財務體質主頁"""
    stock_name = data["stock_name"]
    financial = data["financial"]
    balance_sheet = data["balance_sheet"]
    cash_flow = data["cash_flow"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    dividend = data.get("dividend")

    st.markdown(f"## 💪 {t('page.financial_health')} — {stock_name}")
    st.markdown(f"*{t('financial.health.subtitle')}*")
    st.markdown("---")

    # ── M3: 時間軸選擇器 ──────────────────────────────
    render_timeline_selector(key_prefix="fh_")
    st.markdown("---")

    # ── 1. 利潤漏斗 ──────────────────────────────────
    _section_title(t("financial.health.profit_funnel"))

    # 從損益表提取數據
    revenue = 0
    gross_profit = 0
    operating_income = 0
    net_income = 0

    if financial is not None and len(financial) > 0:
        filtered_financial = filter_by_timeline(financial, date_col="date")
        try:
            latest_date = filtered_financial["date"].max()
            latest = filtered_financial[filtered_financial["date"] == latest_date]

            revenue = find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
            gross_profit = find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
            operating_income = find_financial_value(latest, ["營業利益", "營業利潤", "Operating Income", "operating_income"])
            net_income = find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])
        except Exception:
            pass

    if revenue > 0:
        fig = create_funnel_chart(revenue, gross_profit, operating_income, net_income,
                                  f"{stock_name} {t('financial.health.profit_funnel')}")
        st.plotly_chart(fig, use_container_width=True)

        # 漏斗白話解釋
        if gross_profit > 0 and net_income > 0:
            margin_pct = net_income / revenue * 100
            _info_card(t("metric.net_margin"), t("financial.health.net_margin_explain", margin_pct=f"{margin_pct:.1f}"), "💰")
    else:
        st.info(t("financial.health.no_financial_data"))

    st.markdown("---")

    # ── 2. 關鍵財務比率 ──────────────────────────────
    _section_title(t("financial.health.key_ratios"))

    col1, col2, col3 = st.columns(3)

    with col1:
        gm = extra_metrics.get("gross_margin")
        if gm is not None:
            _白话_card(t("metric.gross_margin"), f"{gm:.1f}%", get_gross_margin_analogy(gm))
        else:
            _白话_card(t("metric.gross_margin"), t("financial.health.data_insufficient"), t("financial.health.calculating_from"))

        om = extra_metrics.get("operating_margin")
        if om is not None:
            _白话_card(t("metric.operating_margin"), f"{om:.1f}%",
                       t("financial.health.operating_margin_explain", om=f"{om:.1f}"))

        nm = extra_metrics.get("net_margin")
        if nm is not None:
            _白话_card(t("metric.net_margin"), f"{nm:.1f}%",
                       t("financial.health.net_margin_explain2", nm=f"{nm:.1f}"))

    with col2:
        # ROE
        industry = data.get("industry", "")
        filtered_financial_roe = filter_by_timeline(financial, date_col="date") if financial is not None and len(financial) > 0 else financial
        filtered_balance_roe = filter_by_timeline(balance_sheet, date_col="date") if balance_sheet is not None and len(balance_sheet) > 0 else balance_sheet
        roe_result = calc_roe_ttm(filtered_financial_roe, filtered_balance_roe)
        if roe_result is not None:
            roe = roe_result["roe"]
            method = roe_result["method"]
            label = t("financial.health.roe_ttm") if method == "TTM" else t("financial.health.roe_method", method=method)
            analogy = get_roe_analogy(roe)
            if is_seasonal_industry(industry):
                if method != "TTM":
                    analogy = t("financial.health.seasonal_warning", method=method) + " — " + analogy
                else:
                    analogy = t("financial.health.seasonal_warning2") + " — " + analogy
            _白话_card(label, f"{roe:.1f}%", analogy)
        else:
            _白话_card(t("metric.roe"), t("financial.health.data_insufficient"), t("financial.health.roe_desc"))

        # 負債比
        debt = extra_metrics.get("debt_ratio")
        if debt is not None:
            _白话_card(t("metric.debt_ratio"), f"{debt:.1f}%", get_debt_ratio_analogy(debt))
        else:
            _白话_card(t("metric.debt_ratio"), t("financial.health.data_insufficient"), t("financial.health.calculating_from_bs"))

        # 淨值比
        if latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            _白话_card(t("financial.health.pbr_label"), f"{pbr:.2f}", get_pbr_analogy(pbr))

    with col3:
        # PER
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            _白话_card(t("financial.health.per_label"), f"{per:.1f}", get_per_analogy(per))

        # 殖利率
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            _白话_card(t("metric.dividend_yield"), f"{dy:.2f}%", get_dividend_analogy(dy))

    st.markdown("---")

    # ── 3. 資產負債結構 ──────────────────────────────
    _section_title(t("financial.health.balance_structure"))

    if balance_sheet is not None and len(balance_sheet) > 0:
        filtered_balance = filter_by_timeline(balance_sheet, date_col="date")
        try:
            latest_date = filtered_balance["date"].max()
            latest = filtered_balance[filtered_balance["date"] == latest_date]

            total_assets = find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
            total_liabilities = find_financial_value(latest, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])
            total_equity = find_financial_value(latest, ["權益總計", "股東權益", "Total Equity", "total_equity"])

            if total_assets > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    _白话_card(t("metric.total_assets"), f"{total_assets/1e8:,.0f} {t('unit.hundred_million')}",
                               t("financial.health.assets_explain", assets=f"{total_assets/1e8/1000:.1f}"))
                with col2:
                    _白话_card(t("metric.total_liabilities"), f"{total_liabilities/1e8:,.0f} {t('unit.hundred_million')}",
                               t("financial.health.liabilities_explain", pct=f"{total_liabilities/total_assets*100:.1f}"))
                with col3:
                    _白话_card(t("metric.total_equity"), f"{total_equity/1e8:,.0f} {t('unit.hundred_million')}",
                               t("financial.health.equity_explain"))

                # 財務體質評估
                debt_ratio = total_liabilities / total_assets * 100 if total_assets > 0 else 0
                if debt_ratio >= 70:
                    health = t("financial.health.debt_high")
                elif debt_ratio >= 50:
                    health = t("financial.health.debt_medium")
                elif debt_ratio >= 30:
                    health = t("financial.health.debt_low")
                else:
                    health = t("financial.health.debt_very_low")

                _info_card(t("financial.health.health_assessment"), f"{health}\n\n{t('metric.debt_ratio')} {debt_ratio:.1f}%", "🏥")
            else:
                st.info(t("financial.health.balance_incomplete"))
        except Exception:
            st.info(t("financial.health.balance_parse_error"))
    else:
        st.info(t("financial.health.no_balance_data"))

    st.markdown("---")

    # ── 4. 現金流量 ──────────────────────────────────
    _section_title(t("financial.health.cash_flow"))

    if cash_flow is not None and len(cash_flow) > 0:
        filtered_cashflow = filter_by_timeline(cash_flow, date_col="date")
        try:
            latest_date = filtered_cashflow["date"].max()
            latest = filtered_cashflow[filtered_cashflow["date"] == latest_date]

            operating_cf = find_financial_value(latest, ["營業活動", "經營活動", "Operating", "operating"])
            investing_cf = find_financial_value(latest, ["投資活動", "Investing", "investing"])
            financing_cf = find_financial_value(latest, ["籌資活動", "融資活動", "Financing", "financing"])

            col1, col2, col3 = st.columns(3)
            with col1:
                sign = "+" if operating_cf >= 0 else ""
                _白话_card(t("metric.operating_cash_flow"), f"{sign}{operating_cf/1e8:,.0f} {t('unit.hundred_million')}",
                           t("financial.health.operating_cf_pos") if operating_cf >= 0 else t("financial.health.operating_cf_neg"))
            with col2:
                sign = "+" if investing_cf >= 0 else ""
                _白话_card(t("metric.investing_cash_flow"), f"{sign}{investing_cf/1e8:,.0f} {t('unit.hundred_million')}",
                           t("financial.health.investing_cf_pos") if investing_cf >= 0 else t("financial.health.investing_cf_neg"))
            with col3:
                sign = "+" if financing_cf >= 0 else ""
                _白话_card(t("metric.financing_cash_flow"), f"{sign}{financing_cf/1e8:,.0f} {t('unit.hundred_million')}",
                           t("financial.health.financing_cf_pos") if financing_cf >= 0 else t("financial.health.financing_cf_neg"))

            # 現金流解讀
            if operating_cf > 0 and investing_cf < 0:
                _info_card(t("financial.health.cash_flow_reading"), t("financial.health.cash_flow_growth"), "💵")
            elif operating_cf > 0 and investing_cf > 0:
                _info_card(t("financial.health.cash_flow_reading"), t("financial.health.cash_flow_mature"), "💵")
            elif operating_cf < 0:
                _info_card(t("financial.health.cash_flow_reading"), t("financial.health.cash_flow_warning"), "⚠️")
        except Exception:
            st.info(t("financial.health.cashflow_parse_error"))
    else:
        st.info(t("financial.health.no_cashflow_data"))

    st.markdown("---")

    # ── 5. 股利指標 ──────────────────────────────────
    _section_title(t("financial.health.dividend_section"))

    current_price = None
    if latest_per_pbr and latest_per_pbr.get("price"):
        current_price = latest_per_pbr["price"]

    div_summary = extract_dividend_summary(dividend, current_price=current_price)

    if div_summary["has_data"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            latest_div = div_summary["latest_cash_div"]
            _白话_card(t("financial.health.latest_dividend"), f"{latest_div} {t('unit.yuan')}" if latest_div else "—",
                       t("financial.health.cash_dividend_per_share"))
        with col2:
            est_annual = div_summary["estimated_annual"]
            annual_str = f"{est_annual} {t('unit.yuan')}" if est_annual else "—"
            est_label = t("financial.health.estimated_annual") if div_summary.get("is_estimated") else t("financial.health.annual_dividend")
            hint = t("financial.health.estimated_hint") if div_summary.get("is_estimated") else t("financial.health.actual_hint")
            _白话_card(est_label, annual_str, hint)
        with col3:
            est_yield = div_summary["estimated_yield"]
            yield_label = t("financial.health.estimated_yield") if div_summary.get("is_estimated") else t("metric.dividend_yield")
            _白话_card(yield_label, f"{est_yield}%" if est_yield else "—",
                       t("financial.health.yield_calc"))

        freq_label = {
            "quarterly": t("dividend.frequency_quarterly"),
            "annual": t("dividend.frequency_annual"),
            "irregular": t("dividend.frequency_irregular"),
        }.get(div_summary["frequency"], "—")
        _info_card(t("financial.health.dividend_frequency"), f"{freq_label} — {div_summary['plain_summary']}", "🎁")
    else:
        _info_card(t("dividend.summary"), div_summary["plain_summary"], "🎁")
