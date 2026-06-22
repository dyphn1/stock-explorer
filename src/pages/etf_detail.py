"""
ETF 詳情頁 — M1 MVP
目標：使用者在 10 秒內知道這檔 ETF 的投資定位與特色
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.finmind_client import FinMindClient
from src.core.i18n import t
from src.pages._router_base import _section_title, _白话_card, _info_card, filter_by_timeline
from src.services.chart import create_price_area_chart, _get_chart_colors


def _get_etf_one_liner(stock_name: str) -> str:
    """根據 ETF 名稱關鍵字產生一句話定位"""
    name = stock_name.lower()
    if "50" in name or "台灣50" in name:
        return t("etf.detail.one_liner_50")
    if "高股息" in name or "股息" in name:
        return t("etf.detail.one_liner_dividend")
    if "債券" in name or "債" in name:
        return t("etf.detail.one_liner_bond")
    if "esg" in name or "永續" in name:
        return t("etf.detail.one_liner_esg")
    return t("etf.detail.one_liner_default")


def _get_etf_knowledge(stock_name: str) -> str:
    """根據 ETF 類型回傳對應的 ETF 小知識"""
    name = stock_name.lower()
    if "50" in name or "台灣50" in name:
        return t("etf.detail.knowledge_50")
    if "高股息" in name or "股息" in name:
        return t("etf.detail.knowledge_dividend")
    if "債券" in name or "債" in name:
        return t("etf.detail.knowledge_bond")
    if "esg" in name or "永續" in name:
        return t("etf.detail.knowledge_esg")
    return t("etf.detail.knowledge_default")


def _get_dividend_frequency_analogy(dividend_df: pd.DataFrame) -> str:
    """根據配息資料推估配息頻率並給出白話說明"""
    if dividend_df is None or len(dividend_df) == 0:
        return ""

    try:
        years = dividend_df["year"].nunique() if "year" in dividend_df.columns else 0
        total = len(dividend_df)

        if years == 0:
            return ""

        avg_per_year = total / years if years > 0 else 0

        if avg_per_year >= 4:
            return t("etf.detail.dividend_frequency_quarterly")
        elif avg_per_year >= 2:
            return t("etf.detail.dividend_frequency_semi")
        elif avg_per_year >= 1:
            return t("etf.detail.dividend_frequency_annual")
        else:
            return t("etf.detail.dividend_frequency_irregular")
    except Exception:
        return ""


def _render_etf_detail(data: dict, client: FinMindClient):
    """ETF 詳情主頁（M1）"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    daily_price = data["daily_price"]
    institutional = data["institutional"]
    dividend = data["dividend"]
    extra_metrics = data.get("extra_metrics", {})

    # ── Header ──────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{stock_name}** `{stock_id}` ｜ {industry}")
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            sign = "+" if change >= 0 else ""
            st.markdown(f"**{price:,.2f}** `{sign}{change:,.2f}`")

    st.markdown("---")

    # ── ETF Specific Metrics ────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        _info_card(
            t("etf.detail.metric.expense_ratio"),
            (lambda v: f"{v}%" if isinstance(v, (int, float)) else v)(extra_metrics.get("expense_ratio", "N/A")),
            icon="📉",
        )
    with col2:
        _info_card(
            t("etf.detail.metric.tracking_error"),
            (lambda v: f"{v}%" if isinstance(v, (int, float)) else v)(extra_metrics.get("tracking_error", "N/A")),
            icon="🎯",
        )
    with col3:
        _info_card(
            t("etf.detail.metric.dividend_yield"),
            (lambda v: f"{v}%" if isinstance(v, (int, float)) else v)(extra_metrics.get("dividend_yield", "N/A")),
            icon="💰",
        )
    st.caption(t("etf.detail.metric.sample_data_note"))

    _section_title(t("etf.detail.comparison.title"))

    # Get current ETF metrics
    current_id = data["stock_id"]
    exp_ratio = extra_metrics.get("expense_ratio", "N/A")
    track_err = extra_metrics.get("tracking_error", "N/A")
    div_yield = extra_metrics.get("dividend_yield", "N/A")

    # Format as percentage if numeric
    def fmt_metric(v):
        if isinstance(v, (int, float)):
            return f"{v}%"
        return v

    # Current ETF row (highlighted by bolding the ETF ID)
    current_data = {
        "ETF": f"**{current_id}**" if current_id else current_id,
        "Expense Ratio": fmt_metric(exp_ratio),
        "Tracking Error": fmt_metric(track_err),
        "Dividend Yield": fmt_metric(div_yield),
    }

    # Sample data for popular ETFs
    popular = [
        {"id": "0050", "expense_ratio": 0.09, "tracking_error": 0.05, "dividend_yield": 4.2},
        {"id": "0056", "expense_ratio": 0.09, "tracking_error": 0.03, "dividend_yield": 5.0},
        {"id": "00878", "expense_ratio": 0.15, "tracking_error": 0.07, "dividend_yield": 3.8},
        {"id": "00919", "expense_ratio": 0.10, "tracking_error": 0.04, "dividend_yield": 4.5},
    ]

    popular_data = []
    for etf in popular:
        popular_data.append({
            "ETF": etf["id"],
            "Expense Ratio": fmt_metric(etf["expense_ratio"]),
            "Tracking Error": fmt_metric(etf["tracking_error"]),
            "Dividend Yield": fmt_metric(etf["dividend_yield"]),
        })

    # Combine: current ETF first, then popular
    all_data = [current_data] + popular_data
    df = pd.DataFrame(all_data)

    # Build markdown table
    headers = ["ETF", "Expense Ratio", "Tracking Error", "Dividend Yield"]
    rows = []
    # Current ETF row
    rows.append([
        f"**{current_id}**" if current_id else current_id,
        fmt_metric(exp_ratio),
        fmt_metric(track_err),
        fmt_metric(div_yield),
    ])
    # Popular ETFs rows
    for etf in popular:
        rows.append([
            etf["id"],
            fmt_metric(etf["expense_ratio"]),
            fmt_metric(etf["tracking_error"]),
            fmt_metric(etf["dividend_yield"]),
        ])
    
    # Create markdown table
    md = "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in rows:
        md += "| " + " | ".join(row) + " |\n"
    
    st.markdown(md)

    st.caption(t("etf.detail.comparison.note"))
    st.markdown("---")

    # ── 一句話定位 ──────────────────────────────────────────
    one_liner = _get_etf_one_liner(stock_name)
    _info_card(f"💡 {one_liner}", "", "💡")

    # ── 績效走勢 ────────────────────────────────────────────
    _section_title(t("etf.detail.section_performance"))
    if daily_price is not None and len(daily_price) > 0:
        try:
            df_price = daily_price.copy()
            df_price["date"] = pd.to_datetime(df_price["date"])
            # 取最近 1 年
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=365)
            df_price = df_price[df_price["date"] >= cutoff].reset_index(drop=True)

            if len(df_price) > 0:
                fig = create_price_area_chart(
                    df_price, title=t("etf.detail.chart_price_title", stock_name=stock_name)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(t("etf.detail.no_price_data_1y"))
        except Exception:
            st.info(t("etf.detail.price_data_processing"))
    else:
        st.info(t("etf.detail.no_price_data"))

    st.markdown("---")

    # ── 配息資訊 ────────────────────────────────────────────
    _section_title(t("etf.detail.section_dividend"))
    if dividend is not None and len(dividend) > 0:
        try:
            freq_analogy = _get_dividend_frequency_analogy(dividend)
            if freq_analogy:
                _info_card(t("etf.detail.dividend_explanation_title"), freq_analogy, icon="📅")

            # 顯示最近 5 筆配息
            display_cols = []
            col_mapping = {}
            for col in dividend.columns:
                if col in ("date", "stock_id", "year"):
                    display_cols.append(col)
                    col_mapping[col] = col
                elif "CashEarningsDistribution" in col:
                    display_cols.append(col)
                    col_mapping[col] = t("etf.detail.col_cash_dividend")
                elif "CashExDividendTradingDate" in col:
                    display_cols.append(col)
                    col_mapping[col] = t("etf.detail.col_ex_dividend_date")
                elif "StockEarningsDistribution" in col:
                    display_cols.append(col)
                    col_mapping[col] = t("etf.detail.col_stock_dividend")
                elif "ExRightDividendTradingDate" in col:
                    display_cols.append(col)
                    col_mapping[col] = t("etf.detail.col_ex_right_date")

            if not display_cols:
                display_cols = list(dividend.columns[:6])

            recent = dividend.head(5)[display_cols].copy()
            recent = recent.rename(columns=col_mapping)

            # 格式化數值
            for col in recent.columns:
                if t("etf.detail.col_cash_dividend") in str(col):
                    recent[col] = recent[col].apply(
                        lambda x: f"{x:.2f}" if pd.notna(x) else "-"
                    )

            st.dataframe(recent, use_container_width=True, hide_index=True)

            # 白話說明
            _info_card(t("etf.detail.dividend_explanation_title"), t("etf.detail.dividend_explanation_content"), "💡")
        except Exception:
            st.info(t("etf.detail.dividend_data_processing"))
    else:
        st.info(t("etf.detail.no_dividend_data"))

    st.markdown("---")

    # ── 法人動向 ────────────────────────────────────────────
    _section_title(t("etf.detail.section_institutional"))
    if institutional is not None and len(institutional) > 0:
        try:
            df_inst = institutional.copy()
            df_inst["date"] = pd.to_datetime(df_inst["date"])
            # 取最近 30 天
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
            df_inst = df_inst[df_inst["date"] >= cutoff].reset_index(drop=True)

            if len(df_inst) > 0:
                # 計算三大法人買賣超
                buy_col = None
                sell_col = None
                for col in df_inst.columns:
                    col_lower = col.lower()
                    if "buy" in col_lower or "買進" in col:
                        buy_col = col
                    elif "sell" in col_lower or "賣出" in col:
                        sell_col = col

                if buy_col and sell_col:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_inst["date"],
                        y=df_inst[buy_col],
                        name=t("etf.detail.buy_label"),
                        marker_color="#27AE60",
                    ))
                    fig.add_trace(go.Bar(
                        x=df_inst["date"],
                        y=-df_inst[sell_col],
                        name=t("etf.detail.sell_label"),
                        marker_color="#E74C3C",
                    ))
                    _tc = _get_chart_colors()
                    fig.update_layout(
                        title=t("etf.detail.chart_institutional_title", stock_name=stock_name),
                        xaxis_title=t("etf.detail.chart_date"),
                        yaxis_title=t("etf.detail.chart_shares"),
                        barmode="relative",
                        height=350,
                        margin=dict(l=40, r=40, t=60, b=40),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    )
                    fig.update_xaxes(showgrid=True, gridcolor=_tc["grid"])
                    fig.update_yaxes(showgrid=True, gridcolor=_tc["grid"])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # 若找不到買/賣欄位，直接顯示表格
                    st.dataframe(df_inst.tail(10), use_container_width=True, hide_index=True)

                # 白話說明
                _info_card(t("etf.detail.institutional_explanation_title"), t("etf.detail.institutional_explanation_content"), "💡")
            else:
                st.info(t("etf.detail.no_institutional_data_30d"))
        except Exception:
            st.info(t("etf.detail.institutional_data_processing"))
    else:
        st.info(t("etf.detail.no_institutional_data"))

    st.markdown("---")

    # ── 費用說明 ────────────────────────────────────────────
    _section_title(t("etf.detail.section_fees"))
    col1, col2 = st.columns(2)

    with col1:
        _白话_card(
            label=t("etf.detail.fee_management_label"),
            value=t("etf.detail.fee_management_value"),
            analogy=t("etf.detail.fee_management_analogy"),
        )

    with col2:
        _白话_card(
            label=t("etf.detail.fee_custody_label"),
            value=t("etf.detail.fee_custody_value"),
            analogy=t("etf.detail.fee_custody_analogy"),
        )

    _info_card(
        title=t("etf.detail.fee_reminder_title"),
        content=t("etf.detail.fee_reminder_content"),
        icon="💰",
    )

    st.markdown("---")

    # ── ETF 小知識 ──────────────────────────────────────────
    _section_title(t("etf.detail.section_knowledge"))
    knowledge = _get_etf_knowledge(stock_name)
    _info_card(
        title=t("etf.detail.knowledge_title", stock_name=stock_name),
        content=knowledge,
        icon="🎓",
    )

    # 免責聲明
    _info_card(t("etf.detail.disclaimer"), t("etf.detail.disclaimer_content"), "⚠️")
