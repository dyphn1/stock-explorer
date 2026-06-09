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
from src.pages._router_base import filter_by_timeline, _section_title, _白话_card, _info_card, _find_financial_value
from src.pages.timeline_controls import render_timeline_selector


def _render_financial_health(data: dict):
    """財務體質主頁"""
    stock_name = data["stock_name"]
    financial = data["financial"]
    balance_sheet = data["balance_sheet"]
    cash_flow = data["cash_flow"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]

    st.markdown(f"## 💪 財務體質 — {stock_name}")
    st.markdown(f"*賺多少？花多少？剩多少？*")
    st.markdown("---")

    # ── M3: 時間軸選擇器 ──────────────────────────────
    render_timeline_selector(key_prefix="fh_")
    st.markdown("---")

    # ── 1. 利潤漏斗 ──────────────────────────────────
    _section_title("利潤漏斗：錢從哪裡來、往哪裡去？")

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

            revenue = _find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
            gross_profit = _find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
            operating_income = _find_financial_value(latest, ["營業利益", "營業利潤", "Operating Income", "operating_income"])
            net_income = _find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])
        except Exception:
            pass

    if revenue > 0:
        fig = create_funnel_chart(revenue, gross_profit, operating_income, net_income,
                                  f"{stock_name} 利潤漏斗")
        st.plotly_chart(fig, use_container_width=True)

        # 漏斗白話解釋
        if gross_profit > 0 and net_income > 0:
            margin_pct = net_income / revenue * 100
            _info_card(
                "利潤漏斗解讀",
                f"每 {revenue/1e8:,.0f} 億元的營收，最終能賺進 {net_income/1e8:,.0f} 億元淨利。"
                f"中間的差距就是成本、費用和稅金。淨利率 {margin_pct:.1f}% 代表每 100 元營收，"
                f"最終能賺進 {margin_pct:.1f} 元。",
                "💰",
            )
    else:
        st.info("暫無損益表資料，無法生成利潤漏斗")

    st.markdown("---")

    # ── 2. 關鍵財務比率 ──────────────────────────────
    _section_title("關鍵財務比率：這家公司健不健康？")

    col1, col2, col3 = st.columns(3)

    with col1:
        gm = extra_metrics.get("gross_margin")
        if gm is not None:
            _白话_card("毛利率", f"{gm:.1f}%", get_gross_margin_analogy(gm))
        else:
            _白话_card("毛利率", "資料不足", "從損益表計算中")

        om = extra_metrics.get("operating_margin")
        if om is not None:
            _白话_card("營業利益率", f"{om:.1f}%",
                       f"每 100 元營收，扣掉成本和營業費用後賺 {om:.1f} 元")

        nm = extra_metrics.get("net_margin")
        if nm is not None:
            _白话_card("淨利率", f"{nm:.1f}%",
                       f"每 100 元營收，最終賺進 {nm:.1f} 元")

    with col2:
        # ROE
        industry = data.get("industry", "")
        filtered_financial_roe = filter_by_timeline(financial, date_col="date") if financial is not None and len(financial) > 0 else financial
        filtered_balance_roe = filter_by_timeline(balance_sheet, date_col="date") if balance_sheet is not None and len(balance_sheet) > 0 else balance_sheet
        roe_result = calc_roe_ttm(filtered_financial_roe, filtered_balance_roe)
        if roe_result is not None:
            roe = roe_result["roe"]
            method = roe_result["method"]
            label = "ROE（近4季）" if method == "TTM" else f"ROE（{method}）"
            analogy = get_roe_analogy(roe)
            if is_seasonal_industry(industry):
                if method != "TTM":
                    analogy = f"⚠ {method}數據，此產業具明顯季節性 — {analogy}"
                else:
                    analogy = f"⚠ 此產業具明顯季節性，ROE 波動大 — {analogy}"
            _白话_card(label, f"{roe:.1f}%", analogy)
        else:
            _白话_card("ROE", "資料不足", "股東權益報酬率")

        # 負債比
        debt = extra_metrics.get("debt_ratio")
        if debt is not None:
            _白话_card("負債比", f"{debt:.1f}%", get_debt_ratio_analogy(debt))
        else:
            _白话_card("負債比", "資料不足", "從資產負債表計算中")

        # 淨值比
        if latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            _白话_card("淨值比 (PBR)", f"{pbr:.2f}", get_pbr_analogy(pbr))

    with col3:
        # PER
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            _白话_card("本益比 (PER)", f"{per:.1f}", get_per_analogy(per))

        # 殖利率
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            _白话_card("殖利率", f"{dy:.2f}%", get_dividend_analogy(dy))

    st.markdown("---")

    # ── 3. 資產負債結構 ──────────────────────────────
    _section_title("資產負債結構：公司家底有多厚？")

    if balance_sheet is not None and len(balance_sheet) > 0:
        filtered_balance = filter_by_timeline(balance_sheet, date_col="date")
        try:
            latest_date = filtered_balance["date"].max()
            latest = filtered_balance[filtered_balance["date"] == latest_date]

            total_assets = _find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
            total_liabilities = _find_financial_value(latest, ["負債總計", "總負債", "Total Liabilities", "total_liabilities"])
            total_equity = _find_financial_value(latest, ["權益總計", "股東權益", "Total Equity", "total_equity"])

            if total_assets > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    _白话_card("總資產", f"{total_assets/1e8:,.0f} 億",
                               f"公司名下所有財產，相當於 {total_assets/1e8/1000:.1f} 個 1000 億")
                with col2:
                    _白话_card("總負債", f"{total_liabilities/1e8:,.0f} 億",
                               f"公司欠別人的錢，佔資產的 {total_liabilities/total_assets*100:.1f}%")
                with col3:
                    _白话_card("股東權益", f"{total_equity/1e8:,.0f} 億",
                               f"真正屬於股東的錢，資產扣除負債後的剩餘")

                # 財務體質評估
                debt_ratio = total_liabilities / total_assets * 100 if total_assets > 0 else 0
                if debt_ratio >= 70:
                    health = "⚠️ 負債比較高，要注意償債能力"
                    health_color = "#E74C3C"
                elif debt_ratio >= 50:
                    health = "📊 負債比適中，屬於正常範圍"
                    health_color = "#F39C12"
                elif debt_ratio >= 30:
                    health = "✅ 財務結構穩健，負債比偏低"
                    health_color = "#27AE60"
                else:
                    health = "✅ 幾乎不借錢，財務非常保守"
                    health_color = "#27AE60"

                st.markdown(f"""
                <div style="background:{health_color}15;border-radius:12px;padding:1.5rem;border-left:4px solid {health_color};margin:1rem 0;">
                    <div style="font-weight:600;color:#2C3E50;">🏥 財務體質評估</div>
                    <div style="font-size:1rem;color:#2C3E50;margin-top:0.5rem;">{health}</div>
                    <div style="font-size:0.85rem;color:#7F8C8D;margin-top:0.3rem;">
                        負債比 {debt_ratio:.1f}% — 每 100 元資產中，有 {debt_ratio:.0f} 元是借來的
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("資產負債表資料不完整")
        except Exception:
            st.info("無法解析資產負債表")
    else:
        st.info("暫無資產負債表資料")

    st.markdown("---")

    # ── 4. 現金流量 ──────────────────────────────────
    _section_title("現金流量：公司真的有在賺錢嗎？")

    if cash_flow is not None and len(cash_flow) > 0:
        filtered_cashflow = filter_by_timeline(cash_flow, date_col="date")
        try:
            latest_date = filtered_cashflow["date"].max()
            latest = filtered_cashflow[filtered_cashflow["date"] == latest_date]

            operating_cf = _find_financial_value(latest, ["營業活動", "經營活動", "Operating", "operating"])
            investing_cf = _find_financial_value(latest, ["投資活動", "Investing", "investing"])
            financing_cf = _find_financial_value(latest, ["籌資活動", "融資活動", "Financing", "financing"])

            col1, col2, col3 = st.columns(3)
            with col1:
                sign = "+" if operating_cf >= 0 else ""
                _白话_card("營業現金流", f"{sign}{operating_cf/1e8:,.0f} 億",
                           "本業賺進來的錢" if operating_cf >= 0 else "本業在燒錢")
            with col2:
                sign = "+" if investing_cf >= 0 else ""
                _白话_card("投資現金流", f"{sign}{investing_cf/1e8:,.0f} 億",
                           "賣掉資產或收到投資收益" if investing_cf >= 0 else "花錢投資擴廠或買設備")
            with col3:
                sign = "+" if financing_cf >= 0 else ""
                _白话_card("籌資現金流", f"{sign}{financing_cf/1e8:,.0f} 億",
                           "借錢或增資" if financing_cf >= 0 else "還錢或配息")

            # 現金流解讀
            if operating_cf > 0 and investing_cf < 0:
                _info_card("現金流解讀",
                           "營業現金流為正、投資現金流為負，代表公司本業賺錢，而且把賺到的錢拿去投資擴廠。"
                           "這通常是健康的成長型公司的特徵。", "💵")
            elif operating_cf > 0 and investing_cf > 0:
                _info_card("現金流解讀",
                           "營業和投資現金流都為正，代表公司本業賺錢，同時也在回收投資。"
                           "可能是成熟穩定的公司。", "💵")
            elif operating_cf < 0:
                _info_card("現金流解讀",
                           "營業現金流為負，代表本業目前還在燒錢。需要關注公司是否有足夠的資金支撐。", "⚠️")
        except Exception:
            st.info("無法解析現金流量表")
    else:
        st.info("暫無現金流量表資料")
