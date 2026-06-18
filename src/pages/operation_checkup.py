"""
營運健檢頁 — M2 第一頁
目標：理解這家公司的商業模式
"""

import streamlit as st
import pandas as pd
from src.services.chart import create_revenue_trend_chart, create_price_chart, create_institutional_chart
from src.services.analogy_engine import get_yoy_analogy, get_revenue_analogy, get_volume_analogy, get_institutional_analogy
from src.pages._router_base import filter_by_timeline, _section_title, _白话_card, _info_card
from src.pages.timeline_controls import render_timeline_selector
from src.core.i18n import t


def _render_operation_checkup(data: dict):
    """營運健檢主頁"""
    stock_name = data["stock_name"]
    industry = data["industry"]
    monthly_revenue = data["monthly_revenue"]
    daily_price = data["daily_price"]
    institutional = data["institutional"]
    extra_metrics = data["extra_metrics"]
    latest_price = data["latest_price"]

    st.markdown(f"## 🏥 {t('operation_checkup.title')} — {stock_name}")
    st.markdown(f"*{t('operation_checkup.subtitle')}*")
    st.markdown("---")

    # ── M3: 時間軸選擇器 ──────────────────────────────
    render_timeline_selector(key_prefix="oc_")
    st.markdown("---")

    # ── 1. 營收趨勢 ──────────────────────────────────
    _section_title(t("operation_checkup.revenue_trend_section"))

    if len(monthly_revenue) > 0:
        filtered_revenue = filter_by_timeline(monthly_revenue, date_col="date")
        fig = create_revenue_trend_chart(filtered_revenue, f"{stock_name} {t('operation_checkup.monthly_revenue_trend')}")
        st.plotly_chart(fig, use_container_width=True)

        # 營收白話解讀
        latest_rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
        yoy = extra_metrics.get("revenue_yoy")
        cols = st.columns(2)
        with cols[0]:
            _白话_card(
                t("operation_checkup.latest_monthly_revenue"),
                f"{latest_rev:,.0f} {t('unit.hundred_million')}",
                get_revenue_analogy(latest_rev, industry),
            )
        with cols[1]:
            if yoy is not None:
                _白话_card(
                    t("operation_checkup.revenue_yoy"),
                    f"{yoy:+.1f}%",
                    get_yoy_analogy(yoy),
                )
            else:
                _白话_card(t("operation_checkup.revenue_yoy"), t("operation_checkup.data_insufficient"), t("operation_checkup.need_13_months"))

        # 營收趨勢白話解讀
        if yoy is not None:
            if yoy >= 20:
                trend_msg = t("operation_checkup.trend_strong", stock_name=stock_name)
            elif yoy >= 5:
                trend_msg = t("operation_checkup.trend_stable", stock_name=stock_name)
            elif yoy >= -5:
                trend_msg = t("operation_checkup.trend_flat", stock_name=stock_name)
            else:
                trend_msg = t("operation_checkup.trend_decline", stock_name=stock_name)
            _info_card(t("operation_checkup.trend_interpret"), trend_msg, "📈")
    else:
        st.info(t("status.no_revenue_data"))

    st.markdown("---")

    # ── 2. 股價走勢 ──────────────────────────────────
    _section_title(t("operation_checkup.price_trend_section"))

    if daily_price is not None and len(daily_price) > 0:
        filtered_price = filter_by_timeline(daily_price, date_col="date")
        fig = create_price_chart(filtered_price, f"{stock_name} {t('operation_checkup.price_trend')}")
        st.plotly_chart(fig, use_container_width=True)

        if latest_price:
            vol = latest_price.get("volume", 0)
            cols = st.columns(2)
            with cols[0]:
                _白话_card(
                    t("operation_checkup.latest_close"),
                    f"{latest_price['close']:,.0f} {t('unit.yuan')}",
                    f"{t('operation_checkup.open')} {latest_price['open']:,.0f}｜{t('operation_checkup.high')} {latest_price['high']:,.0f}｜{t('operation_checkup.low')} {latest_price['low']:,.0f}",
                )
            with cols[1]:
                _白话_card(
                    t("operation_checkup.volume"),
                    f"{vol/1000:.0f} {t('unit.thousand_shares')}",
                    get_volume_analogy(vol),
                )
    else:
        st.info(t("status.no_price_data"))

    st.markdown("---")

    # ── 3. 法人動向 ──────────────────────────────────
    _section_title(t("operation_checkup.institutional_section"))

    if institutional is not None and len(institutional) > 0:
        filtered_institutional = filter_by_timeline(institutional, date_col="date")
        fig = create_institutional_chart(filtered_institutional, f"{stock_name} {t('operation_checkup.institutional_net')}")
        st.plotly_chart(fig, use_container_width=True)

        # 近期法人動向總結
        recent = filtered_institutional.tail(5)
        net_buy_total = (recent["buy"] - recent["sell"]).sum()
        _白话_card(
            t("operation_checkup.net_5d"),
            f"{net_buy_total/1000:+.0f} {t('unit.thousand_shares')}",
            get_institutional_analogy(net_buy_total),
        )

        if net_buy_total > 10000:
            _info_card(t("operation_checkup.institutional_interpret"), t("operation_checkup.inst_strong_buy"), "🏦")
        elif net_buy_total > 0:
            _info_card(t("operation_checkup.institutional_interpret"), t("operation_checkup.inst_mild_buy"), "🏦")
        elif net_buy_total > -10000:
            _info_card(t("operation_checkup.institutional_interpret"), t("operation_checkup.inst_mild_sell"), "🏦")
        else:
            _info_card(t("operation_checkup.institutional_interpret"), t("operation_checkup.inst_strong_sell"), "🏦")
    else:
        st.info(t("status.no_institutional_data"))

    st.markdown("---")

    # ── 4. 營運摘要 ──────────────────────────────────
    summary_parts = []
    if yoy is not None:
        if yoy >= 20:
            summary_parts.append(f"📈 {t('operation_checkup.summary_fast_growth')}")
        elif yoy >= 5:
            summary_parts.append(f"📊 {t('operation_checkup.summary_stable_growth')}")
        elif yoy >= -5:
            summary_parts.append(f"📊 {t('operation_checkup.summary_flat')}")
        else:
            summary_parts.append(f"📉 {t('operation_checkup.summary_decline')}")

    if latest_price:
        vol = latest_price.get("volume", 0)
        if vol >= 50000:
            summary_parts.append(f"🔥 {t('operation_checkup.summary_hot')}")
        elif vol <= 1000:
            summary_parts.append(f"💤 {t('operation_checkup.summary_cold')}")

    if institutional is not None and len(institutional) > 0:
        recent = institutional.tail(5)
        net = (recent["buy"] - recent["sell"]).sum()
        if net > 10000:
            summary_parts.append(f"🏦 {t('operation_checkup.summary_inst_buy')}")
        elif net < -10000:
            summary_parts.append(f"🏦 {t('operation_checkup.summary_inst_sell')}")

    if not summary_parts:
        summary_parts.append(f"📊 {t('operation_checkup.summary_observing')}")

    _info_card(t("operation_checkup.summary_title"), "\n".join(summary_parts), "🩺")
