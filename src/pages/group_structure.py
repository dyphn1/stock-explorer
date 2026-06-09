"""
集團架構頁 — M2 第四頁
目標：認識集團內部的關係（點對點）
第一階段：顯示持股 > 50% 或營收貢獻 > 10% 的子公司
"""

import streamlit as st
import pandas as pd

from src.pages._router_base import _section_title, _info_card


# 已知集團架構資料（公開資訊，來自各公司年報）
# 第一階段只處理持股 > 50% 或營收貢獻 > 10% 的子公司
KNOWN_GROUP_STRUCTURES = {
    "2330": {  # 台積電
        "parent_name": "台積電",
        "parent_desc": "全球最大晶圓代工廠",
        "subsidiaries": [
            {
                "name": "台積電（中國）",
                "holding": 100,
                "revenue_contrib": 10,
                "business": "位於中國南京的晶圓廠，主要生產 16/28 奈米成熟製程",
                "relation": "全資子公司，服務中國客戶",
            },
            {
                "name": "台積電（美國）",
                "holding": 100,
                "revenue_contrib": 0,
                "business": "位於美國亞利桑那州的晶圓廠，正在建設中",
                "relation": "全資子公司，服務美國客戶",
            },
            {
                "name": "世界先進",
                "holding": 28,
                "revenue_contrib": 5,
                "business": "八吋晶圓代工，專注於特殊製程",
                "relation": "重要轉投資，提供差異化產能",
            },
            {
                "name": "SSMC",
                "holding": 39,
                "revenue_contrib": 3,
                "business": "新加坡晶圓代工廠，與恩智浦合資",
                "relation": "合資公司，服務車用和物聯網市場",
            },
        ],
    },
    "2317": {  # 鴻海
        "parent_name": "鴻海",
        "parent_desc": "全球最大電子代工帝國",
        "subsidiaries": [
            {
                "name": "工業富聯（FII）",
                "holding": 84,
                "revenue_contrib": 40,
                "business": "中國A股上市，專注於雲端伺服器和工業互聯網",
                "relation": "主要子公司，承接雲端伺服器訂單",
            },
            {
                "name": "鴻騰精密",
                "holding": 72,
                "revenue_contrib": 15,
                "business": "連接器和線纜組件，用於手機和汽車",
                "relation": "重要子公司，供應內部和外部客戶",
            },
            {
                "name": "夏普（Sharp）",
                "holding": 56,
                "revenue_contrib": 20,
                "business": "日本消費電子品牌，電視和家電",
                "relation": "策略收購，擴展品牌業務",
            },
            {
                "name": "樺漢科技",
                "holding": 45,
                "revenue_contrib": 5,
                "business": "工業電腦和嵌入式系統",
                "relation": "轉投資，佈局工業物聯網",
            },
        ],
    },
    "2881": {  # 富邦金
        "parent_name": "富邦金控",
        "parent_desc": "台灣最大的金融控股集團之一",
        "subsidiaries": [
            {
                "name": "富邦人壽",
                "holding": 100,
                "revenue_contrib": 45,
                "business": "人壽保險業務，保費收入為主",
                "relation": "全資子公司，金控主要獲利來源",
            },
            {
                "name": "台北富邦銀行",
                "holding": 100,
                "revenue_contrib": 30,
                "business": "商業銀行存放款、信用卡業務",
                "relation": "全資子公司，金控核心業務",
            },
            {
                "name": "富邦證券",
                "holding": 100,
                "revenue_contrib": 15,
                "business": "證券經紀、承銷業務",
                "relation": "全資子公司，證券業務平台",
            },
            {
                "name": "富邦產險",
                "holding": 100,
                "revenue_contrib": 8,
                "business": "產物保險，車險和火險",
                "relation": "全資子公司，產險業務",
            },
        ],
    },
    "1301": {  # 台塑
        "parent_name": "台塑",
        "parent_desc": "台灣最大的塑膠集團",
        "subsidiaries": [
            {
                "name": "南亞塑膠",
                "holding": 37,
                "revenue_contrib": 25,
                "business": "塑膠二次加工和電子材料",
                "relation": "關係企業，塑膠加工和電子材料",
            },
            {
                "name": "台塑石化",
                "holding": 29,
                "revenue_contrib": 35,
                "business": "煉油和石化原料生產",
                "relation": "關係企業，上游煉油事業",
            },
            {
                "name": "台化",
                "holding": 36,
                "revenue_contrib": 20,
                "business": "紡織纖維和塑膠原料",
                "relation": "關係企業，紡織和石化原料",
            },
        ],
    },
    "1101": {  # 台泥
        "parent_name": "台泥",
        "parent_desc": "台灣最老牌的水泥廠",
        "subsidiaries": [
            {
                "name": "台泥國際",
                "holding": 57,
                "revenue_contrib": 30,
                "business": "中國水泥市場，廣東和廣西地區",
                "relation": "重要子公司，擴展中國市場",
            },
            {
                "name": "和平電廠",
                "holding": 100,
                "revenue_contrib": 15,
                "business": "花蓮和平發電廠，燃煤發電",
                "relation": "全資子公司，能源事業",
            },
            {
                "name": "達和環保",
                "holding": 100,
                "revenue_contrib": 8,
                "business": "廢棄物處理和環保服務",
                "relation": "全資子公司，環保事業",
            },
        ],
    },
}


def _render_group_structure(data: dict):
    """集團架構主頁"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    st.markdown(f"## 🏢 集團架構 — {stock_name}")
    st.markdown(f"*這家公司旗下有哪些成員？*")
    st.markdown("---")

    # 檢查是否有集團資料
    if stock_id not in KNOWN_GROUP_STRUCTURES:
        st.info(f"📊 {stock_name} 的集團架構資料尚未建立。")
        _info_card("關於集團架構",
                   "這個頁面顯示集團內部的母子關係。第一階段只處理持股 > 50% 或營收貢獻 > 10% 的子公司。"
                   "目前支援的公司：台積電（2330）、鴻海（2317）、富邦金（2881）、台塑（1301）、台泥（1101）。",
                   "💡")
        return

    group = KNOWN_GROUP_STRUCTURES[stock_id]
    parent_name = group["parent_name"]
    subsidiaries = group["subsidiaries"]

    # ── 1. 集團總覽 ──────────────────────────────────
    _section_title("集團總覽")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);border-radius:16px;padding:2rem;margin:1rem 0;">
        <div style="font-size:1.5rem;font-weight:700;color:#2C3E50;">{parent_name}</div>
        <div style="font-size:1rem;color:#5D6D7E;margin-top:0.5rem;">{group['parent_desc']}</div>
        <div style="font-size:0.9rem;color:#7F8C8D;margin-top:1rem;">
            旗下主要成員：{len(subsidiaries)} 家
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 2. 母公司 ────────────────────────────────────
    _section_title("母公司")

    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-size:1.2rem;font-weight:700;color:#2C3E50;">🏢 {parent_name}</div>
        <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;">{group['parent_desc']}</div>
        <div style="font-size:0.85rem;color:#7F8C8D;margin-top:0.5rem;">股票代號：{stock_id} ｜ 產業：{industry}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 3. 子公司列表（點對點）────────────────────────
    _section_title("旗下成員（點對點關係）")

    for sub in subsidiaries:
        holding = sub["holding"]
        revenue = sub["revenue_contrib"]

        # 持股比例標籤
        if holding >= 51:
            hold_label = "🔴 控股子公司"
            hold_color = "#E74C3C"
        elif holding >= 20:
            hold_label = "🟡 重要轉投資"
            hold_color = "#F39C12"
        else:
            hold_label = "🟢 一般投資"
            hold_color = "#27AE60"

        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.5rem;border:1px solid #ECF0F1;margin:0.8rem 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:1.1rem;font-weight:700;color:#2C3E50;">{sub['name']}</span>
                    <span style="background:{hold_color}15;color:{hold_color};padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;font-weight:600;margin-left:0.5rem;">
                        {hold_label}
                    </span>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:0.85rem;color:#7F8C8D;">持股 {holding}%</span>
                    <span style="font-size:0.85rem;color:#7F8C8D;margin-left:1rem;">營收貢獻 ~{revenue}%</span>
                </div>
            </div>
            <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.8rem;line-height:1.6;">
                <strong>在做什麼：</strong>{sub['business']}
            </div>
            <div style="font-size:0.85rem;color:#27AE60;margin-top:0.5rem;line-height:1.5;">
                <strong>跟母公司的關係：</strong>{sub['relation']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 4. 集團關係圖（簡易版）────────────────────────
    _section_title("集團關係圖")

    # 用長條圖顯示持股比例
    sub_names = [s["name"] for s in subsidiaries]
    holdings = [s["holding"] for s in subsidiaries]
    revenues = [s["revenue_contrib"] for s in subsidiaries]

    chart_data = pd.DataFrame({
        "公司": sub_names,
        "持股比例 (%)": holdings,
        "營收貢獻 (%)": revenues,
    })

    st.bar_chart(chart_data.set_index("公司"), use_container_width=True)

    _info_card("關係圖解讀",
               "上圖顯示母公司對各子公司的持股比例和營收貢獻。持股比例越高，代表母公司對該子公司的控制力越強。"
               "營收貢獻越高，代表該子公司對集團整體收入的重要性越大。",
               "📊")

    st.markdown("---")

    # ── 5. 集團策略解讀 ──────────────────────────────
    _section_title("集團策略解讀")

    # 根據資料自動生成策略解讀
    strategy_parts = []

    controlled = [s for s in subsidiaries if s["holding"] >= 51]
    invested = [s for s in subsidiaries if 20 <= s["holding"] < 51]
    minor = [s for s in subsidiaries if s["holding"] < 20]

    if controlled:
        names = "、".join([s["name"] for s in controlled])
        strategy_parts.append(f"**核心控制**：{names} — 母公司直接掌控經營方向")

    if invested:
        names = "、".join([s["name"] for s in invested])
        strategy_parts.append(f"**策略投資**：{names} — 透過持股影響力佈局相關事業")

    if minor:
        names = "、".join([s["name"] for s in minor])
        strategy_parts.append(f"**財務投資**：{names} — 持股比例較低，可能是財務性投資")

    # 營收集中度
    total_rev = sum(s["revenue_contrib"] for s in subsidiaries)
    if total_rev > 80:
        strategy_parts.append("**營收集中度高**：少數子公司貢獻大部分營收，集團策略明確")
    elif total_rev > 50:
        strategy_parts.append("**營收分散適中**：多家子公司都有貢獻，風險分散")
    else:
        strategy_parts.append("**營收分散**：子公司營收貢獻較低，母公司本業佔比較高")

    for part in strategy_parts:
        st.markdown(f"- {part}")

    _info_card("策略解讀",
               f"{parent_name} 的集團架構反映了它的經營策略。"
               "控股子公司代表核心事業，策略投資代表佈局方向，財務投資代表資金運用。"
               "建議關注集團內部的協同效應：子公司之間是否有上下游關係？",
               "🎯")
