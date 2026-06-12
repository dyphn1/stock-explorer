"""
分類瀏覽頁 — M3
提供權值股列表、產業分類瀏覽、熱門列表三大區塊
"""

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to


@st.cache_data(ttl=300)
def _fetch_latest_daily_prices(client: FinMindClient, stock_ids: tuple) -> dict:
    """批量取得多檔股票的最新日收盤價（平行 API 呼叫）。

    Args:
        client: FinMindClient 實例
        stock_ids: stock_id tuple（可 hash，供 cache 使用）

    Returns:
        dict: {stock_id: {"trading_money": float, "trading_volume": int, "close": float}}
              若取得失敗則該 stock_id 不會出現在 dict 中。
    """
    results: dict = {}

    def _fetch_one(sid: str):
        try:
            daily = client.get_daily_price(sid)
            if daily is not None and len(daily) > 0:
                latest = daily.iloc[-1]
                return sid, {
                    "trading_money": float(latest.get("Trading_money", 0) or 0),
                    "trading_volume": int(latest.get("Trading_Volume", 0) or 0),
                    "close": float(latest.get("close", 0) or 0),
                }
        except Exception:
            pass
        return sid, None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_one, sid): sid for sid in stock_ids}
        for future in as_completed(futures):
            sid, data = future.result()
            if data is not None:
                results[sid] = data

    return results


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

    # 取得候選股票列表（前 200 檔）
    candidate_stocks = all_stock_info.sort_values("stock_id").head(200)
    candidate_ids = tuple(candidate_stocks["stock_id"].tolist())

    # ── 批量取得日收盤價（平行 API 呼叫，取代 N+1 逐一查詢）──
    with st.spinner("正在取得行情資料…"):
        price_map = _fetch_latest_daily_prices(client, candidate_ids)

    # 建立 stock_id → name / industry 對照表
    info_map = {
        row["stock_id"]: {
            "stock_name": row.get("stock_name", row["stock_id"]),
            "industry": row.get("industry_category", "—"),
        }
        for _, row in candidate_stocks.iterrows()
    }

    # ── Section A: 權值股列表 ──────────────────────────────
    _render_top_stocks_by_value(price_map, info_map)

    st.markdown("---")

    # ── Section B: 產業分類瀏覽 ─────────────────────────────
    _render_industry_browser(all_stock_info)

    st.markdown("---")

    # ── Section C: 熱門列表 ─────────────────────────────────
    _render_hot_stocks_by_volume(price_map, info_map)


# ════════════════════════════════════════════════════════════
# Section A: 權值股列表（依成交金額排序）
# ════════════════════════════════════════════════════════════

def _render_top_stocks_by_value(price_map: dict, info_map: dict):
    """權值股列表：取最近一日成交金額最高的前 20 檔"""
    st.markdown("### 💰 權值股列表（依成交金額）")

    if not price_map:
        st.info("暫無成交金額資料。")
        return

    stock_money = []
    for sid, price_data in price_map.items():
        info = info_map.get(sid, {})
        stock_money.append({
            "stock_id": sid,
            "stock_name": info.get("stock_name", sid),
            "industry": info.get("industry", "—"),
            "trading_money": price_data["trading_money"],
            "trading_volume": price_data["trading_volume"],
            "close": price_data["close"],
        })

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

def _render_hot_stocks_by_volume(price_map: dict, info_map: dict):
    """熱門列表：取最近一日成交量最高的前 20 檔"""
    st.markdown("### 🔥 熱門列表（依成交量）")

    if not price_map:
        st.info("暫無成交量資料。")
        return

    stock_volume = []
    for sid, price_data in price_map.items():
        info = info_map.get(sid, {})
        stock_volume.append({
            "stock_id": sid,
            "stock_name": info.get("stock_name", sid),
            "industry": info.get("industry", "—"),
            "trading_volume": price_data["trading_volume"],
            "trading_money": price_data["trading_money"],
            "close": price_data["close"],
        })

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
