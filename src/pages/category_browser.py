"""
分類瀏覽頁 — M3
提供權值股列表、產業分類瀏覽、熱門列表三大區塊
"""

import streamlit as st
import pandas as pd
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to


def _render_category_browser(client: FinMindClient):
    """分類瀏覽主頁（M3）"""

    st.markdown("## 🔍 分類瀏覽")
    st.markdown("探索台股市場：權值股、產業分類、熱門標的")
    st.markdown("---")

    # 取得全部股票資訊（一次性載入，供三個區塊使用）
    with st.spinner("載入股票資料中…"):
        try:
            all_stock_info = client.get_stock_info()
        except Exception as e:
            st.error(f"無法取得股票資訊：{e}")
            return

    if all_stock_info is None or len(all_stock_info) == 0:
        st.warning("目前無股票資料可顯示。")
        return

    # 確保必要欄位存在
    required_cols = ["stock_id", "stock_name", "industry_category"]
    for col in required_cols:
        if col not in all_stock_info.columns:
            st.error(f"資料缺少必要欄位：{col}")
            return

    # ── Section A: 權值股列表 ──────────────────────────────
    _render_top_stocks_by_value(client, all_stock_info)

    st.markdown("---")

    # ── Section B: 產業分類瀏覽 ─────────────────────────────
    _render_industry_browser(all_stock_info)

    st.markdown("---")

    # ── Section C: 熱門列表 ─────────────────────────────────
    _render_hot_stocks_by_volume(client, all_stock_info)


# ════════════════════════════════════════════════════════════
# Section A: 權值股列表（依成交金額排序）
# ════════════════════════════════════════════════════════════

def _render_top_stocks_by_value(client: FinMindClient, all_stock_info: pd.DataFrame):
    """權值股列表：取最近一日成交金額最高的前 20 檔"""
    st.markdown("### 💰 權值股列表（依成交金額）")

    # 收集每檔股票的最新日成交金額
    stock_money = []
    # 只取前 200 檔避免 API 呼叫過多（依 stock_id 排序確保穩定）
    candidate_stocks = all_stock_info.sort_values("stock_id").head(200)

    progress = st.progress(0, text="正在取得成交金額…")
    total = len(candidate_stocks)

    for idx, (_, row) in enumerate(candidate_stocks.iterrows()):
        sid = row["stock_id"]
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                money = float(latest.get("Trading_money", 0) or 0)
                volume = int(latest.get("Trading_Volume", 0) or 0)
                close = float(latest.get("close", 0) or 0)
                stock_money.append({
                    "stock_id": sid,
                    "stock_name": row.get("stock_name", sid),
                    "industry": row.get("industry_category", "—"),
                    "trading_money": money,
                    "trading_volume": volume,
                    "close": close,
                })
        except Exception:
            pass

        if idx % 10 == 0:
            progress.progress(min((idx + 1) / total, 1.0), text=f"已處理 {idx + 1}/{total} 檔…")

    progress.empty()

    if not stock_money:
        st.info("暫無成交金額資料。")
        return

    df_value = pd.DataFrame(stock_money).sort_values("trading_money", ascending=False).head(20)
    df_value["排名"] = range(1, len(df_value) + 1)
    df_value["成交金額"] = df_value["trading_money"].apply(_format_money)
    df_value["收盤價"] = df_value["close"].apply(lambda x: f"{x:,.2f}")

    # 顯示表格 + 按鈕
    st.markdown("#### 前 20 大權值股")
    for _, row in df_value.iterrows():
        cols = st.columns([0.7, 1, 1.5, 1.8, 1.4, 1])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(row["industry"])
        cols[4].markdown(row["成交金額"])
        if cols[5].button("查看", key=f"val_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# Section B: 產業分類瀏覽
# ════════════════════════════════════════════════════════════

def _render_industry_browser(all_stock_info: pd.DataFrame):
    """產業分類瀏覽：左側產業列表，右側該產業個股"""
    st.markdown("### 🏭 產業分類瀏覽")

    # 取得所有唯一產業
    industries = (
        all_stock_info["industry_category"]
        .dropna()
        .unique()
    )
    # 過濾空字串
    industries = sorted([str(i).strip() for i in industries if str(i).strip()])

    if not industries:
        st.info("無產業分類資料。")
        return

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("#### 選擇產業")
        # 使用 radio 選擇產業
        selected_industry = st.radio(
            "產業",
            industries,
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown(f"#### {selected_industry} — 成分股")
        industry_stocks = all_stock_info[
            all_stock_info["industry_category"] == selected_industry
        ].sort_values("stock_id")

        if len(industry_stocks) == 0:
            st.info("此產業無股票資料。")
            return

        # 以卡片網格顯示
        cols_per_row = 3
        stock_list = industry_stocks.reset_index(drop=True)
        for i in range(0, len(stock_list), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx >= len(stock_list):
                    break
                row = stock_list.iloc[idx]
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
                                {row.get('stock_name', '')}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "查看名片",
                        key=f"ind_{row['stock_id']}",
                        use_container_width=True,
                    ):
                        navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# Section C: 熱門列表（依成交量排序）
# ════════════════════════════════════════════════════════════

def _render_hot_stocks_by_volume(client: FinMindClient, all_stock_info: pd.DataFrame):
    """熱門列表：取最近一日成交量最高的前 20 檔"""
    st.markdown("### 🔥 熱門列表（依成交量）")

    stock_volume = []
    candidate_stocks = all_stock_info.sort_values("stock_id").head(200)

    progress = st.progress(0, text="正在取得成交量…")
    total = len(candidate_stocks)

    for idx, (_, row) in enumerate(candidate_stocks.iterrows()):
        sid = row["stock_id"]
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                volume = int(latest.get("Trading_Volume", 0) or 0)
                money = float(latest.get("Trading_money", 0) or 0)
                close = float(latest.get("close", 0) or 0)
                stock_volume.append({
                    "stock_id": sid,
                    "stock_name": row.get("stock_name", sid),
                    "industry": row.get("industry_category", "—"),
                    "trading_volume": volume,
                    "trading_money": money,
                    "close": close,
                })
        except Exception:
            pass

        if idx % 10 == 0:
            progress.progress(min((idx + 1) / total, 1.0), text=f"已處理 {idx + 1}/{total} 檔…")

    progress.empty()

    if not stock_volume:
        st.info("暫無成交量資料。")
        return

    df_volume = pd.DataFrame(stock_volume).sort_values("trading_volume", ascending=False).head(20)
    df_volume["排名"] = range(1, len(df_volume) + 1)
    df_volume["成交量"] = df_volume["trading_volume"].apply(_format_volume)
    df_volume["收盤價"] = df_volume["close"].apply(lambda x: f"{x:,.2f}")

    st.markdown("#### 前 20 大熱門股")
    for _, row in df_volume.iterrows():
        cols = st.columns([0.7, 1, 1.5, 1.8, 1.4, 1])
        cols[0].markdown(f"**#{int(row['排名'])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(row["industry"])
        cols[4].markdown(row["成交量"])
        if cols[5].button("查看", key=f"vol_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# 輔助函式
# ════════════════════════════════════════════════════════════

def _format_money(value: float) -> str:
    """格式化成交金額：億 / 萬"""
    if value >= 1e8:
        return f"{value / 1e8:,.1f} 億"
    elif value >= 1e4:
        return f"{value / 1e4:,.0f} 萬"
    else:
        return f"{value:,.0f}"


def _format_volume(value: int) -> str:
    """格式化成交量：張 / 萬張"""
    if value >= 1e4:
        return f"{value / 1e4:,.1f} 萬張"
    else:
        return f"{value:,.0f} 張"
