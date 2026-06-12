"""
ETF 瀏覽頁 — 熱門 ETF、ETF 分類、配息排行三大區塊
提供台灣 ETF 市場的快速瀏覽與篩選功能
"""

import streamlit as st
import pandas as pd
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.pages._router_base import _info_card, _summary_card, _count_label


def _cached_get_stock_info(client: FinMindClient):
    """Cache the full stock info table so it's only fetched once across sub-views."""
    return client.get_stock_info()


def _get_all_etf_prices(client: FinMindClient, etf_ids_tuple):
    """Fetch daily prices for all ETFs once; returns a DataFrame keyed by stock_id."""
    ids = list(etf_ids_tuple)
    rows = []
    for sid in ids:
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                close = float(latest.get("close", 0) or 0)
                volume = int(latest.get("Trading_Volume", 0) or 0)
                money = float(latest.get("Trading_money", 0) or 0)
                prev_close = float(daily.iloc[-2]["close"]) if len(daily) >= 2 else close
                change = close - prev_close
                change_pct = (change / prev_close * 100) if prev_close > 0 else 0.0
                rows.append({
                    "stock_id": sid,
                    "close": close,
                    "trading_volume": volume,
                    "trading_money": money,
                    "change": change,
                    "change_pct": change_pct,
                })
        except Exception:
            rows.append({
                "stock_id": sid,
                "close": 0,
                "trading_volume": 0,
                "trading_money": 0,
                "change": 0,
                "change_pct": 0.0,
            })
    return pd.DataFrame(rows).set_index("stock_id")


def _render_etf_browser(client: FinMindClient):
    """ETF 瀏覽主頁"""

    st.markdown("## 📊 ETF 瀏覽")
    st.markdown("探索台灣 ETF 市場：熱門排行、分類瀏覽、配息比較")
    st.markdown("---")

    # ── 白話解釋卡片 ──────────────────────────────────────
    _info_card("💡 什麼是 ETF？", "ETF（指數股票型基金）就像一個「股票籃子」，一次買進就等於買進一籃子標的。\n例如買入 0050，等於同時持有台灣市值最大的 50 間公司股票。\nETF 可以像股票一樣在交易所買賣，費用比基金低，適合新手分散投資。\n\n⚠️ 注意：ETF 價格會隨市場波動，投資前請評估自身風險承受能力。", "💡")

    # ── 取得 ETF 股票清單（cached） ──────────────────────────
    with st.spinner("載入 ETF 資料中…"):
        try:
            all_stock_info = _cached_get_stock_info(client)
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

    _count_label(len(etf_info), "檔 ETF")

    # ── 預取所有 ETF 價格（一次的迭代，全部 cache）────────────
    etf_ids = tuple(sorted(etf_info["stock_id"].tolist()))
    with st.spinner("正在取得 ETF 價格（首次載入需時較長，之後切換頁籤將加速）…"):
        price_df = _get_all_etf_prices(client, etf_ids)

    # ── 子頁面選擇 ──────────────────────────────────────────
    st.markdown("---")
    sub_view = st.radio(
        "選擇功能",
        ["🔥 熱門 ETF", "📂 ETF 分類", "💰 配息排行"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if sub_view == "🔥 熱門 ETF":
        _render_hot_etfs(etf_info, price_df)
    elif sub_view == "📂 ETF 分類":
        _render_etf_categories(etf_info, price_df)
    elif sub_view == "💰 配息排行":
        _render_dividend_ranking(client, etf_info, price_df)


# ════════════════════════════════════════════════════════════
# 子頁面 A: 熱門 ETF（依成交量排序）
# ════════════════════════════════════════════════════════════

def _render_hot_etfs(etf_info: pd.DataFrame, price_df: pd.DataFrame):
    """熱門 ETF：取最近一日成交量最高的前 20 檔"""
    st.markdown("### 🔥 熱門 ETF（依成交量）")

    # Build candidates from cached price data
    records = []
    for _, row in etf_info.sort_values("stock_id").iterrows():
        sid = row["stock_id"]
        if sid in price_df.index:
            p = price_df.loc[sid]
            records.append({
                "stock_id": sid,
                "stock_name": row.get("stock_name", sid),
                "trading_volume": int(p.get("trading_volume", 0) or 0),
                "trading_money": float(p.get("trading_money", 0) or 0),
                "close": float(p.get("close", 0) or 0),
                "change": float(p.get("change", 0) or 0),
                "change_pct": float(p.get("change_pct", 0) or 0),
            })

    if not records:
        st.info("暫無成交量資料。")
        return

    df_volume = pd.DataFrame(records).sort_values("trading_volume", ascending=False).head(20)
    df_volume["排名"] = range(1, len(df_volume) + 1)

    st.markdown("#### 前 20 大熱門 ETF")
    for _, row in df_volume.iterrows():
        change = row["change"]
        change_pct = row["change_pct"]
        sign = "+" if change >= 0 else ""
        color = "#E74C3C" if change >= 0 else "#27AE60"  # 紅漲綠跌（台股慣例）

        cols = st.columns([0.6, 1, 2, 1.4, 1.4, 1])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(f"{row['close']:,.2f}")
        cols[4].markdown(
            f"<span style='color:{color};font-weight:600;'>{sign}{change:,.2f} ({sign}{change_pct:.2f}%)</span>",
            unsafe_allow_html=True,
        )
        if cols[5].button("查看", key=f"hot_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# 子頁面 B: ETF 分類
# ════════════════════════════════════════════════════════════

# 分類關鍵字（依 stock_name 匹配）
# 優先順序：先匹配精確/高置信度關鍵字，再匹配通用關鍵字
ETF_CATEGORY_KEYWORDS = {
    "高股息型": [
        # 精確匹配
        "元大高股息", "國泰永續", "國泰高股息", "元大臺灣高息",
        "富邦高股息", "復華高股息", "凱基優選", "FT臺灣",
        "群益精選", "永豐優息存股", "統一MIT",
        # 一般關鍵字
        "股息", "高息", "高殖", "股利", "存股", "優息",
    ],
    "債券型": [
        # 精確匹配
        "國泰美債", "富邦美債", "元大美債", "永豐美債",
        "群益美債", "復華美債", "中信美債", "統一美債",
        # 一般關鍵字
        "債券", "債", "政府債", "公司債", "美債", "投資等級",
    ],
    "主題型": [
        # 精確匹配
        "元大全球AI", "國泰AI", "富邦NASDAQ", "元大未來關鍵科技",
        "新光車電", "中信電池", "群益半導體", "富邦半導體",
        "元大生技", "國泰基因", "富邦基因",
        # 一般關鍵字
        "電動車", "AI", "半導體", "5G", "ESG", "生技", "醫療",
        "網安", "資安", "太空", "元宇宙", "電競", "遊戲",
    ],
    "市值型": [
        # 精確匹配（高置信度）
        "元大台灣50", "富邦台50", "元大台股", "大盤", "加權",
        # 一般關鍵字
        "50", "56", "6208", "台灣",
    ],
}


def _classify_etf(stock_name: str) -> str:
    """根據股票名稱關鍵字分類 ETF"""
    for category, keywords in ETF_CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in stock_name:
                return category
    return "其他"


def _render_etf_categories(etf_info: pd.DataFrame, price_df: pd.DataFrame):
    """ETF 分類：將 ETF 依類型分組，可展開查看"""
    st.markdown("### 📂 ETF 分類")

    # 分類所有 ETF
    etf_info = etf_info.copy()
    etf_info["etf_category"] = etf_info["stock_name"].apply(_classify_etf)

    # 取得每檔 ETF 的最新價格（from cached price_df）
    etf_with_price = []
    for _, row in etf_info.iterrows():
        sid = row["stock_id"]
        if sid in price_df.index:
            p = price_df.loc[sid]
            close = float(p.get("close", 0) or 0)
            change = float(p.get("change", 0) or 0)
            change_pct = float(p.get("change_pct", 0) or 0)
        else:
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
                        _info_card(f"{row['stock_name']} ({row['stock_id']})", f"價格：{row['close']:,.2f}  漲跌：{sign}{change:,.2f} ({sign}{change_pct:.2f}%)", "📊")
                        if st.button(
                            "查看名片",
                            key=f"cat_{row['stock_id']}",
                            use_container_width=True,
                        ):
                            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# 子頁面 C: 配息排行（依殖利率排序）
# ════════════════════════════════════════════════════════════

def _render_dividend_ranking(client: FinMindClient, etf_info: pd.DataFrame, price_df: pd.DataFrame):
    """配息排行：取最近年度股利換算殖利率，排序前 20 檔"""
    st.markdown("### 💰 配息排行（依殖利率）")
    st.caption("⏳ 配息排行需取得股利資料，首次載入可能較慢，請耐心等候…")

    etf_dividends = []
    candidate_etfs = etf_info.sort_values("stock_id")

    progress = st.progress(0, text="正在取得股利資料…")
    total = len(candidate_etfs)

    for idx, (_, row) in enumerate(candidate_etfs.iterrows()):
        sid = row["stock_id"]
        try:
            # 取得股利資料（still needed — no shared cache for dividends)
            div_df = client.get_dividend(sid)

            # 取得最新價格（from cached price_df — avoids redundant fetches）
            if sid in price_df.index:
                p = price_df.loc[sid]
                close = float(p.get("close", 0) or 0)
                change = float(p.get("change", 0) or 0)
                change_pct = float(p.get("change_pct", 0) or 0)
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

        cols = st.columns([0.6, 1, 1.5, 1, 1, 1.2, 1])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(f"{row['close']:,.2f}")
        cols[4].markdown(
            f"<span style='color:{color};font-size:0.85rem;'>{sign}{change_pct:.2f}%</span>",
            unsafe_allow_html=True,
        )
        cols[5].markdown(
            f"<span style='color:#3498DB;font-weight:600;'>{row['dividend_yield']:.2f}%</span>",
            unsafe_allow_html=True,
        )
        if cols[6].button("查看", key=f"div_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])

    # 白話補充
    _info_card("殖利率小知識", "殖利率 = 年度股利 ÷ 股價 × 100%。\n殖利率越高代表每投入 1 元能領回的現金越多，但高殖利率不等於高報酬，仍需留意 ETF 的追蹤誤差、費用率及折溢價狀況。", "💡")
