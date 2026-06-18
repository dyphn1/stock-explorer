"""
集團架構頁 — M2 第四頁
目標：認識集團內部的關係（點對點）
第一階段：顯示持股 > 50% 或營收貢獻 > 10% 的子公司
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.pages._router_base import _section_title, _info_card, _summary_card, _白话_card, _subsidiary_card
from src.services.chart import _apply_theme_layout
from src.core.i18n import t


# 已知集團架構資料（公開資訊，來自各公司年報）
# 第一階段只處理持股 > 50% 或營收貢獻 > 10% 的子公司
KNOWN_GROUP_STRUCTURES = {
    "2330": {  # 台積電
        "parent_name": "台積電",
        "parent_desc": t("group.structure.tsmc.desc"),
        "subsidiaries": [
            {
                "name": t("group.structure.tsmc.sub.china.name"),
                "holding": 100,
                "revenue_contrib": 10,
                "business": t("group.structure.tsmc.sub.china.business"),
                "relation": t("group.structure.tsmc.sub.china.relation"),
            },
            {
                "name": t("group.structure.tsmc.sub.usa.name"),
                "holding": 100,
                "revenue_contrib": 0,
                "business": t("group.structure.tsmc.sub.usa.business"),
                "relation": t("group.structure.tsmc.sub.usa.relation"),
            },
            {
                "name": t("group.structure.tsmc.sub.vis.name"),
                "holding": 28,
                "revenue_contrib": 5,
                "business": t("group.structure.tsmc.sub.vis.business"),
                "relation": t("group.structure.tsmc.sub.vis.relation"),
            },
            {
                "name": t("group.structure.tsmc.sub.ssmc.name"),
                "holding": 39,
                "revenue_contrib": 3,
                "business": t("group.structure.tsmc.sub.ssmc.business"),
                "relation": t("group.structure.tsmc.sub.ssmc.relation"),
            },
        ],
    },
    "2317": {  # 鴻海
        "parent_name": "鴻海",
        "parent_desc": t("group.structure.foxconn.desc"),
        "subsidiaries": [
            {
                "name": t("group.structure.foxconn.sub.fii.name"),
                "holding": 84,
                "revenue_contrib": 40,
                "business": t("group.structure.foxconn.sub.fii.business"),
                "relation": t("group.structure.foxconn.sub.fii.relation"),
            },
            {
                "name": t("group.structure.foxconn.sub.fhg.name"),
                "holding": 72,
                "revenue_contrib": 15,
                "business": t("group.structure.foxconn.sub.fhg.business"),
                "relation": t("group.structure.foxconn.sub.fhg.relation"),
            },
            {
                "name": t("group.structure.foxconn.sub.sharp.name"),
                "holding": 56,
                "revenue_contrib": 20,
                "business": t("group.structure.foxconn.sub.sharp.business"),
                "relation": t("group.structure.foxconn.sub.sharp.relation"),
            },
            {
                "name": t("group.structure.foxconn.sub.enspire.name"),
                "holding": 45,
                "revenue_contrib": 5,
                "business": t("group.structure.foxconn.sub.enspire.business"),
                "relation": t("group.structure.foxconn.sub.enspire.relation"),
            },
        ],
    },
    "2881": {  # 富邦金
        "parent_name": t("group.structure.fubon.parent"),
        "parent_desc": t("group.structure.fubon.desc"),
        "subsidiaries": [
            {
                "name": t("group.structure.fubon.sub.life.name"),
                "holding": 100,
                "revenue_contrib": 45,
                "business": t("group.structure.fubon.sub.life.business"),
                "relation": t("group.structure.fubon.sub.life.relation"),
            },
            {
                "name": t("group.structure.fubon.sub.bank.name"),
                "holding": 100,
                "revenue_contrib": 30,
                "business": t("group.structure.fubon.sub.bank.business"),
                "relation": t("group.structure.fubon.sub.bank.relation"),
            },
            {
                "name": t("group.structure.fubon.sub.securities.name"),
                "holding": 100,
                "revenue_contrib": 15,
                "business": t("group.structure.fubon.sub.securities.business"),
                "relation": t("group.structure.fubon.sub.securities.relation"),
            },
            {
                "name": t("group.structure.fubon.sub.property.name"),
                "holding": 100,
                "revenue_contrib": 8,
                "business": t("group.structure.fubon.sub.property.business"),
                "relation": t("group.structure.fubon.sub.property.relation"),
            },
        ],
    },
    "1301": {  # 台塑
        "parent_name": t("group.structure.fp.parent"),
        "parent_desc": t("group.structure.fp.desc"),
        "subsidiaries": [
            {
                "name": t("group.structure.fp.sub.nanya.name"),
                "holding": 37,
                "revenue_contrib": 25,
                "business": t("group.structure.fp.sub.nanya.business"),
                "relation": t("group.structure.fp.sub.nanya.relation"),
            },
            {
                "name": t("group.structure.fp.sub.fpcc.name"),
                "holding": 29,
                "revenue_contrib": 35,
                "business": t("group.structure.fp.sub.fpcc.business"),
                "relation": t("group.structure.fp.sub.fpcc.relation"),
            },
            {
                "name": t("group.structure.fp.sub.fcfc.name"),
                "holding": 36,
                "revenue_contrib": 20,
                "business": t("group.structure.fp.sub.fcfc.business"),
                "relation": t("group.structure.fp.sub.fcfc.relation"),
            },
        ],
    },
    "1101": {  # 台泥
        "parent_name": t("group.structure.tcc.parent"),
        "parent_desc": t("group.structure.tcc.desc"),
        "subsidiaries": [
            {
                "name": t("group.structure.tcc.sub.intl.name"),
                "holding": 57,
                "revenue_contrib": 30,
                "business": t("group.structure.tcc.sub.intl.business"),
                "relation": t("group.structure.tcc.sub.intl.relation"),
            },
            {
                "name": t("group.structure.tcc.sub.power.name"),
                "holding": 100,
                "revenue_contrib": 15,
                "business": t("group.structure.tcc.sub.power.business"),
                "relation": t("group.structure.tcc.sub.power.relation"),
            },
            {
                "name": t("group.structure.tcc.sub.dahe.name"),
                "holding": 100,
                "revenue_contrib": 8,
                "business": t("group.structure.tcc.sub.dahe.business"),
                "relation": t("group.structure.tcc.sub.dahe.relation"),
            },
        ],
    },
}


def _render_group_structure(data: dict):
    """集團架構主頁"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    st.markdown(f"## 🏢 {t('page.group_structure')} — {stock_name}")
    st.markdown(f"*{t('group.structure.subtitle')}*")
    st.markdown("---")

    # 檢查是否有集團資料
    if stock_id not in KNOWN_GROUP_STRUCTURES:
        st.info(t("group.structure.no_data", name=stock_name))
        _info_card(t("group.structure.about_title"),
                   t("group.structure.about_content"),
                   "💡")
        return

    group = KNOWN_GROUP_STRUCTURES[stock_id]
    parent_name = group["parent_name"]
    subsidiaries = group["subsidiaries"]

    # ── 1. 集團總覽 ──────────────────────────────────
    _section_title(t("group.structure.overview"))

    _summary_card(f"{parent_name} — {group['parent_desc']}", t("group.structure.member_count", count=len(subsidiaries)), "🏢")

    st.markdown("---")

    # ── 2. 母公司 ────────────────────────────────────
    _section_title(t("group.structure.parent"))

    _info_card(f"🏢 {parent_name}", f"{group['parent_desc']}\n\n{t('stock.code')}：{stock_id} ｜ {t('stock.industry')}：{industry}", "🏢")

    st.markdown("---")

    # ── 3. 子公司列表（點對點）────────────────────────
    _section_title(t("group.structure.members"))

    for sub in subsidiaries:
        holding = sub["holding"]
        revenue = sub["revenue_contrib"]

        # 持股比例標籤
        if holding >= 51:
            hold_label = t("group.structure.controlled")
            hold_color = "#E74C3C"
        elif holding >= 20:
            hold_label = t("group.structure.major_investment")
            hold_color = "#3498DB"
        else:
            hold_label = t("group.structure.general_investment")
            hold_color = "#27AE60"

        _subsidiary_card(
            name=sub['name'],
            hold_label=hold_label,
            hold_color=hold_color,
            holding=holding,
            revenue=revenue,
            business=sub['business'],
            relation=sub['relation'],
        )

    st.markdown("---")

    # ── 4. 集團關係圖（簡易版）────────────────────────
    _section_title(t("group.structure.chart_title"))

    # 用長條圖顯示持股比例
    sub_names = [s["name"] for s in subsidiaries]
    holdings = [s["holding"] for s in subsidiaries]
    revenues = [s["revenue_contrib"] for s in subsidiaries]

    chart_data = pd.DataFrame({
        t("group.structure.chart_company"): sub_names,
        t("group.structure.chart_holding"): holdings,
        t("group.structure.chart_revenue"): revenues,
    })

    # Plotly grouped bar chart (replaces st.bar_chart for design consistency)
    fig = px.bar(
        chart_data,
        x=t("group.structure.chart_company"),
        y=[t("group.structure.chart_holding"), t("group.structure.chart_revenue")],
        barmode="group",
        color_discrete_map={t("group.structure.chart_holding"): "#3498DB", t("group.structure.chart_revenue"): "#27AE60"},
    )
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

    _info_card(t("group.structure.chart_reading"),
               t("group.structure.chart_reading_content"),
               "📊")

    st.markdown("---")

    # ── 5. 集團策略解讀 ──────────────────────────────
    _section_title(t("group.structure.strategy"))

    # 根據資料自動生成策略解讀
    strategy_parts = []

    controlled = [s for s in subsidiaries if s["holding"] >= 51]
    invested = [s for s in subsidiaries if 20 <= s["holding"] < 51]
    minor = [s for s in subsidiaries if s["holding"] < 20]

    if controlled:
        names = "、".join([s["name"] for s in controlled])
        strategy_parts.append(t("group.structure.core_control", names=names))

    if invested:
        names = "、".join([s["name"] for s in invested])
        strategy_parts.append(t("group.structure.strategic_investment", names=names))

    if minor:
        names = "、".join([s["name"] for s in minor])
        strategy_parts.append(t("group.structure.financial_investment", names=names))

    # 營收集中度
    total_rev = sum(s["revenue_contrib"] for s in subsidiaries)
    if total_rev > 80:
        strategy_parts.append(t("group.structure.revenue_concentrated"))
    elif total_rev > 50:
        strategy_parts.append(t("group.structure.revenue_balanced"))
    else:
        strategy_parts.append(t("group.structure.revenue_dispersed"))

    for part in strategy_parts:
        st.markdown(f"- {part}")

    _info_card(t("group.structure.strategy_reading"),
               t("group.structure.strategy_reading_content", parent=parent_name),
               "🎯")
