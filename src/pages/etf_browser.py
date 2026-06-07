"""
ETF 瀏覽頁 — 熱門 ETF、ETF 分類、配息排行三大區塊
提供台灣 ETF 市場的快速瀏覽與篩選功能
"""

import streamlit as st
import pandas as pd
from src.data.finmind_client import FinMindClient


def _render_etf_browser(client: FinMindClient):
    """ETF 瀏覽主頁"""

    st.markdown("## 📊 ETF 瀏覽")
    st.markdown("探索台灣 ETF 市場：熱門排行、分類瀏覽、配息比較")
    st.markdown("---")

    # ── 白話解釋卡片 ──────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#EBF5FB,#EAF2F8);border-radius:14px;
                padding:1.4rem 1.6rem;border-left:5px solid #2E86C1;margin-bottom:1.2rem;">
        <div style="font-weight:700;font-size:1.1rem;color:#1B4F72;margin-bottom:0.4rem;">
            💡 什麼是 ETF？
        </div>
        <div style="font-size:0.92rem;color:#2C3E50;line-height:1.7;">
            ETF（指數股票型基金）就像一個「股票籃子」，一次買進就等於買進一籃子標的。<br>
            例如買入 <b>0050</b>，等於同時持有台灣市值最大的 50 間公司股票。<br>
            ETF 可以像股票一樣在交易所買賣，費用比基金低，適合新手分散投資。<br>
            <span style="color:#7F8C8D;font-size:0.85rem;">
                ⚠️ 注意：ETF 價格會隨市場波動，投資前請評估自身風險承受能力。
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 取得 ETF 股票清單 ──────────────────────────────────
    with st.spinner("載入 ETF 資料中…"):
        try:
            all_stock_info = client.get_stock_info()
        except Exception as e:
            st.error(f"無法取得股票資訊：{e}")
            return

    if all_stock_info is None or len(all_stock_info) == 0:
        st.warning("目前無股票資料可顯示。")
        return

    # 過濾 ETF（industry_category 包含 "ETF"，不分大小寫）
    etf_mask = all_stock_info["industry_category"].str.contains("ETF", case=False, na=False)
    etf_info = all_stock_info[etf_mask].copy()

    if len(etf_info) == 0:
        st.warning("找不到任何 ETF 資料。")
        return

    st.markdown(f"<div style='color:#7F8C8D;font-size:0.85rem;'>共找到 <b>{len(etf_info)}</b> 檔 ETF</div>",
                unsafe_allow_html=True)

    # ── 子頁面選擇 ──────────────────────────────────────────
    st.markdown("---")
    sub_view = st.radio(
        "選擇功能",
        ["🔥 熱門 ETF", "📂 ETF 分類", "💰 配息排行"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if sub_view == "🔥 熱門 ETF":
        _render_hot_etfs(client, etf_info)
    elif sub_view == "📂 ETF 分類":
        _render_etf_categories(client, etf_info)
    elif sub_view == "💰 配息排行":
        _render_dividend_ranking(client, etf_info)


# ════════════════════════════════════════════════════════════
# 子頁面 A: 熱門 ETF（依成交量排序）
# ════════════════════════════════════════════════════════════

def _render_hot_etfs(client: FinMindClient, etf_info: pd.DataFrame):
    """熱門 ETF：取最近一日成交量最高的前 20 檔"""
    st.markdown("### 🔥 熱門 ETF（依成交量）")

    etf_volume = []
    candidate_etfs = etf_info.sort_values("stock_id")

    progress = st.progress(0, text="正在取得成交量…")
    total = len(candidate_etfs)

    for idx, (_, row) in enumerate(candidate_etfs.iterrows()):
        sid = row["stock_id"]
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                volume = int(latest.get("Trading_Volume", 0) or 0)
                money = float(latest.get("Trading_money", 0) or 0)
                close = float(latest.get("close", 0) or 0)
                prev_close = float(daily.iloc[-2]["close"]) if len(daily) >= 2 else close
                change = close - prev_close
                change_pct = (change / prev_close * 100) if prev_close > 0 else 0.0
                etf_volume.append({
                    "stock_id": sid,
                    "stock_name": row.get("stock_name", sid),
                    "trading_volume": volume,
                    "trading_money": money,
                    "close": close,
                    "change": change,
                    "change_pct": change_pct,
                })
        except Exception:
            pass

        if idx % 10 == 0:
            progress.progress(min((idx + 1) / total, 1.0), text=f"已處理 {idx + 1}/{total} 檔…")

    progress.empty()

    if not etf_volume:
        st.info("暫無成交量資料。")
        return

    df_volume = pd.DataFrame(etf_volume).sort_values("trading_volume", ascending=False).head(20)
    df_volume["排名"] = range(1, len(df_volume) + 1)

    st.markdown("#### 前 20 大熱門 ETF")
    for _, row in df_volume.iterrows():
        change = row["change"]
        change_pct = row["change_pct"]
        sign = "+" if change >= 0 else ""
        color = "#E74C3C" if change >= 0 else "#27AE60"  # 紅漲綠跌（台股慣例）

        cols = st.columns([0.5, 0.8, 1.5, 1.2, 1.2, 0.8])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(f"{row['close']:,.2f}")
        cols[4].markdown(
            f"<span style='color:{color};font-weight:600;'>{sign}{change:,.2f} ({sign}{change_pct:.2f}%)</span>",
            unsafe_allow_html=True,
        )
        if cols[5].button("查看", key=f"hot_{row['stock_id']}", use_container_width=True):
            st.session_state["stock_id"] = row["stock_id"]
            st.session_state["page"] = "名片"
            st.rerun()


# ════════════════════════════════════════════════════════════
# 子頁面 B: ETF 分類
# ════════════════════════════════════════════════════════════

# 分類關鍵字（依 stock_name 匹配）
ETF_CATEGORY_KEYWORDS = {
    "市值型": ["50", "56", "6208", "台灣", "加權", "大盤"],
    "高股息型": ["股息", "高息", "高殖", "股利", "存股"],
    "債券型": ["債券", "債", "政府債", "公司債", "美債"],
    "主題型": ["電動車", "AI", "半導體", "5G", "ESG", "生技", "醫療"],
}


def _classify_etf(stock_name: str) -> str:
    """根據股票名稱關鍵字分類 ETF"""
    for category, keywords in ETF_CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in stock_name:
                return category
    return "其他"


def _render_etf_categories(client: FinMindClient, etf_info: pd.DataFrame):
    """ETF 分類：將 ETF 依類型分組，可展開查看"""
    st.markdown("### 📂 ETF 分類")

    # 分類所有 ETF
    etf_info = etf_info.copy()
    etf_info["etf_category"] = etf_info["stock_name"].apply(_classify_etf)

    # 取得每檔 ETF 的最新價格
    etf_with_price = []
    progress = st.progress(0, text="正在取得價格…")
    total = len(etf_info)

    for idx, (_, row) in enumerate(etf_info.iterrows()):
        sid = row["stock_id"]
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                close = float(latest.get("close", 0) or 0)
                prev_close = float(daily.iloc[-2]["close"]) if len(daily) >= 2 else close
                change = close - prev_close
                change_pct = (change / prev_close * 100) if prev_close > 0 else 0.0
            else:
                close = 0
                change = 0
                change_pct = 0.0
        except Exception:
            close = 0
            change = 0
            change_pct = 0.0

        etf_with_price.append({
            "stock_id": sid,
            "stock_name": row.get("stock_name", sid),
            "etf_category": row["etf_category"],
            "close": close,
            "change": change,
            "change_pct": change_pct,
        })

        if idx % 20 == 0:
            progress.progress(min((idx + 1) / total, 1.0), text=f"已處理 {idx + 1}/{total} 檔…")

    progress.empty()

    df_cat = pd.DataFrame(etf_with_price)
    if df_cat.empty:
        st.info("無 ETF 資料可分類。")
        return

    # 分類順序
    categories = ["市值型", "高股息型", "債券型", "主題型", "其他"]
    category_icons = {
        "市值型": "🏛️",
        "高股息型": "💵",
        "債券型": "📜",
        "主題型": "🎯",
        "其他": "📦",
    }
    category_descriptions = {
        "市值型": "追蹤大盤指數，一次買進台灣大型股",
        "高股息型": "聚焦高配息股票，適合存股領息",
        "債券型": "投資債券市場，波動相對較低",
        "主題型": "鎖定特定產業或趨勢主題",
        "其他": "不屬於以上分類的 ETF",
    }

    # 使用 st.expander 顯示各分類
    for cat in categories:
        cat_df = df_cat[df_cat["etf_category"] == cat].sort_values("stock_id")
        if cat_df.empty:
            continue

        icon = category_icons.get(cat, "📋")
        desc = category_descriptions.get(cat, "")
        count = len(cat_df)

        with st.expander(f"{icon} **{cat}**（{count} 檔）— {desc}", expanded=(cat == "市值型")):
            # 以卡片網格顯示
            cols_per_row = 2
            stock_list = cat_df.reset_index(drop=True)
            for i in range(0, len(stock_list), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx >= len(stock_list):
                        break
                    row = stock_list.iloc[idx]
                    change = row["change"]
                    change_pct = row["change_pct"]
                    sign = "+" if change >= 0 else ""
                    color = "#E74C3C" if change >= 0 else "#27AE60"

                    with cols[j]:
                        st.markdown(
                            f"""
                            <div style="background:#F8F9FA;border-radius:10px;
                                        padding:0.8rem;margin-bottom:0.5rem;
                                        border-left:3px solid #3498DB;">
                                <div style="font-size:0.8rem;color:#7F8C8D;">
                                    {row['stock_id']}
                                </div>
                                <div style="font-weight:600;color:#2C3E50;">
                                    {row['stock_name']}
                                </div>
                                <div style="font-size:0.9rem;color:#2C3E50;">
                                    {row['close']:,.2f}
                                    <span style="color:{color};font-size:0.8rem;margin-left:0.4rem;">
                                        {sign}{change:,.2f} ({sign}{change_pct:.2f}%)
                                    </span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            "查看名片",
                            key=f"cat_{row['stock_id']}",
                            use_container_width=True,
                        ):
                            st.session_state["stock_id"] = row["stock_id"]
                            st.session_state["page"] = "名片"
                            st.rerun()


# ════════════════════════════════════════════════════════════
# 子頁面 C: 配息排行（依殖利率排序）
# ════════════════════════════════════════════════════════════

def _render_dividend_ranking(client: FinMindClient, etf_info: pd.DataFrame):
    """配息排行：取最近年度股利換算殖利率，排序前 20 檔"""
    st.markdown("### 💰 配息排行（依殖利率）")

    etf_dividends = []
    candidate_etfs = etf_info.sort_values("stock_id")

    progress = st.progress(0, text="正在取得股利資料…")
    total = len(candidate_etfs)

    for idx, (_, row) in enumerate(candidate_etfs.iterrows()):
        sid = row["stock_id"]
        try:
            # 取得股利資料
            div_df = client.get_dividend(sid)
            # 取得最新價格
            daily = client.get_daily_price(sid)

            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                close = float(latest.get("close", 0) or 0)
                prev_close = float(daily.iloc[-2]["close"]) if len(daily) >= 2 else close
                change = close - prev_close
                change_pct = (change / prev_close * 100) if prev_close > 0 else 0.0
            else:
                close = 0
                change = 0
                change_pct = 0.0

            # 計算年度股利：取最近一年的現金股利加總
            annual_dividend = 0.0
            stock_name_d = row.get("stock_name", sid)
            if div_df is not None and len(div_df) > 0:
                # 嘗試從股利資料中擷取現金股利
                # FinMind taiwan_stock_dividend 欄位可能包含：
                # Cash_Dividend, Stock_Dividend, date 等
                if "Cash_Dividend" in div_df.columns:
                    # 取最近一年的資料
                    div_df = div_df.copy()
                    div_df["date"] = pd.to_datetime(div_df["date"], errors="coerce")
                    one_year_ago = pd.Timestamp.now() - pd.Timedelta(days=365)
                    recent = div_df[div_df["date"] >= one_year_ago]
                    if len(recent) > 0:
                        annual_dividend = float(recent["Cash_Dividend"].sum())
                    else:
                        # 若最近一年無資料，取最新一筆
                        annual_dividend = float(div_df.iloc[-1]["Cash_Dividend"])
                elif "dividend" in div_df.columns:
                    div_df = div_df.copy()
                    div_df["date"] = pd.to_datetime(div_df["date"], errors="coerce")
                    one_year_ago = pd.Timestamp.now() - pd.Timedelta(days=365)
                    recent = div_df[div_df["date"] >= one_year_ago]
                    if len(recent) > 0:
                        annual_dividend = float(recent["dividend"].sum())
                    else:
                        annual_dividend = float(div_df.iloc[-1]["dividend"])

            # 計算殖利率
            dividend_yield = (annual_dividend / close * 100) if close > 0 else 0.0

            etf_dividends.append({
                "stock_id": sid,
                "stock_name": stock_name_d,
                "close": close,
                "change": change,
                "change_pct": change_pct,
                "annual_dividend": annual_dividend,
                "dividend_yield": dividend_yield,
            })
        except Exception:
            pass

        if idx % 10 == 0:
            progress.progress(min((idx + 1) / total, 1.0), text=f"已處理 {idx + 1}/{total} 檔…")

    progress.empty()

    if not etf_dividends:
        st.info("暫無股利資料。")
        return

    df_div = pd.DataFrame(etf_dividends)
    # 只顯示有配息的 ETF，依殖利率排序
    df_div = df_div[df_div["dividend_yield"] > 0].sort_values("dividend_yield", ascending=False).head(20)

    if df_div.empty:
        st.info("目前無配息資料的 ETF。")
        return

    df_div["排名"] = range(1, len(df_div) + 1)

    st.markdown("#### 前 20 大配息 ETF")
    for _, row in df_div.iterrows():
        change = row["change"]
        change_pct = row["change_pct"]
        sign = "+" if change >= 0 else ""
        color = "#E74C3C" if change >= 0 else "#27AE60"

        cols = st.columns([0.5, 0.8, 1.3, 1, 1, 1, 0.8])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(f"{row['close']:,.2f}")
        cols[4].markdown(
            f"<span style='color:{color};font-size:0.85rem;'>{sign}{change_pct:.2f}%</span>",
            unsafe_allow_html=True,
        )
        cols[5].markdown(
            f"<span style='color:#8E44AD;font-weight:600;'>{row['dividend_yield']:.2f}%</span>",
            unsafe_allow_html=True,
        )
        if cols[6].button("查看", key=f"div_{row['stock_id']}", use_container_width=True):
            st.session_state["stock_id"] = row["stock_id"]
            st.session_state["page"] = "名片"
            st.rerun()

    # 白話補充
    st.markdown("""
    <div style="background:#FEF9E7;border-radius:10px;padding:0.8rem 1.2rem;
                border-left:4px solid #F1C40F;margin-top:0.8rem;">
        <div style="font-size:0.85rem;color:#7F8C8D;">
            💡 <b>殖利率小知識</b>：殖利率 = 年度股利 ÷ 股價 × 100%。
            殖利率越高代表每投入 1 元能領回的現金越多，但高殖利率不等於高報酬，
            仍需留意 ETF 的追蹤誤差、費用率及折溢價狀況。
        </div>
    </div>
    """, unsafe_allow_html=True)
