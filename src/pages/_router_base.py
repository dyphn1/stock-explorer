"""
路由器共享工具函式
"""

import pandas as pd
from src.data.finmind_client import FinMindClient


def get_stock_data(client: FinMindClient, stock_id: str) -> dict:
    """載入一支股票的所有資料，回傳 dict"""
    stock_info = client.get_stock_info(stock_id)
    if len(stock_info) == 0:
        return None

    stock_name = stock_info.iloc[0]["stock_name"]
    industry = stock_info.iloc[0]["industry_category"]

    latest_price = client.get_latest_price(stock_id)
    latest_per_pbr = client.get_latest_per_pbr(stock_id)
    monthly_revenue = client.get_monthly_revenue(stock_id)
    daily_price = client.get_daily_price(stock_id)
    financial = client.get_financial_statement(stock_id)
    news = client.get_news(stock_id)
    institutional = client.get_institutional_investors(stock_id)
    balance_sheet = client.get_balance_sheet(stock_id)
    cash_flow = client.get_cash_flow(stock_id)
    dividend = client.get_dividend(stock_id)

    extra_metrics = _calc_extra_metrics(financial, balance_sheet, monthly_revenue)

    return {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "industry": industry,
        "latest_price": latest_price,
        "latest_per_pbr": latest_per_pbr,
        "monthly_revenue": monthly_revenue,
        "daily_price": daily_price,
        "financial": financial,
        "news": news,
        "institutional": institutional,
        "balance_sheet": balance_sheet,
        "cash_flow": cash_flow,
        "dividend": dividend,
        "extra_metrics": extra_metrics,
    }


def _calc_extra_metrics(financial_df, balance_sheet_df, monthly_revenue_df) -> dict:
    """計算額外的財務指標"""
    metrics = {}

    if financial_df is not None and len(financial_df) > 0:
        try:
            latest_date = financial_df["date"].max()
            latest = financial_df[financial_df["date"] == latest_date]

            revenue = _find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
            gross_profit = _find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
            operating_income = _find_financial_value(latest, ["營業利益", "營業利潤", "Operating Income", "operating_income"])
            net_income = _find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])

            if revenue and revenue > 0:
                if gross_profit:
                    metrics["gross_margin"] = round(gross_profit / revenue * 100, 1)
                if operating_income:
                    metrics["operating_margin"] = round(operating_income / revenue * 100, 1)
                if net_income:
                    metrics["net_margin"] = round(net_income / revenue * 100, 1)
        except Exception:
            pass

    if balance_sheet_df is not None and len(balance_sheet_df) > 0:
        try:
            latest_date = balance_sheet_df["date"].max()
            latest = balance_sheet_df[balance_sheet_df["date"] == latest_date]

            total_assets = _find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
            total_liabilities = _find_financial_value(latest, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])
            total_equity = _find_financial_value(latest, ["權益總計", "股東權益", "Total Equity", "total_equity"])

            if total_assets and total_assets > 0:
                if total_liabilities:
                    metrics["debt_ratio"] = round(total_liabilities / total_assets * 100, 1)
                if total_equity:
                    metrics["equity_ratio"] = round(total_equity / total_assets * 100, 1)
        except Exception:
            pass

    if monthly_revenue_df is not None and len(monthly_revenue_df) > 12:
        try:
            latest_rev = monthly_revenue_df.iloc[-1]["revenue"]
            last_year_rev = monthly_revenue_df.iloc[-13]["revenue"]
            if last_year_rev > 0:
                metrics["revenue_yoy"] = round((latest_rev - last_year_rev) / last_year_rev * 100, 1)
        except Exception:
            pass

    return metrics


def _find_financial_value(df, keywords: list) -> float:
    """從財務資料中根據關鍵字找值"""
    for _, row in df.iterrows():
        type_val = str(row.get("type", ""))
        for kw in keywords:
            if kw.lower() in type_val.lower():
                val = row.get("value")
                if pd.notna(val) and val != 0:
                    return float(val)
    return 0.0


def _section_title(title: str):
    import streamlit as st
    st.markdown(f"### 📊 {title}")


def _白话_card(label: str, value: str, analogy: str = ""):
    import streamlit as st
    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
        <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
        <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{analogy}</div>
    </div>
    """, unsafe_allow_html=True)


def _info_card(title: str, content: str, icon: str = "💡"):
    import streamlit as st
    st.markdown(f"""
    <div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
        <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.3rem;line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)
