"""
分類瀏覽頁 — M3
提供權值股列表、產業分類瀏覽、熱門列表三大區塊
"""

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.core.i18n import t


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

    st.markdown(f"## 🔍 {t('category_browser.title')}")
    st.markdown(t("category_browser.subtitle"))
    st.markdown("---")

    # 取得全部股票資訊（一次性載入，供三個區塊使用）
    with st.spinner(t("category_browser.loading_stocks")):
        try:
            all_stock_info = client.get_stock_info()
        except Exception as e:
            st.error(f"{t('category_browser.fetch_error')}: {e}")
            return

    if all_stock_info is None or len(all_stock_info) == 0:
        st.warning(t("category_browser.no_data"))
        return

    # 確保必要欄位存在
    required_cols = ["stock_id", "stock_name", "industry_category"]
    for col in required_cols:
        if col not in all_stock_info.columns:
            st.error(f"{t('category_browser.missing_col')}: {col}")
            return

    # 取得候選股票列表（前 200 檔）
    candidate_stocks = all_stock_info.sort_values("stock_id").head(200)
    candidate_ids = tuple(candidate_stocks["stock_id"].tolist())

    # ── 批量取得日收盤價（平行 API 呼叫，取代 N+1 逐一查詢）──
    with st.spinner(t("category_browser.loading_prices")):
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
    st.markdown(f"### 💰 {t('category_browser.top_stocks_title')}")

    if not price_map:
        st.info(t("category_browser.no_value_data"))
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
    df_value[t("category_browser.col_rank")] = range(1, len(df_value) + 1)
    df_value[t("category_browser.col_money")] = df_value["trading_money"].apply(_format_money)
    df_value[t("category_browser.col_close")] = df_value["close"].apply(lambda x: f"{x:,.2f}")

    # 顯示表格 + 按鈕
    st.markdown(f"#### {t('category_browser.top_20')}")
    for _, row in df_value.iterrows():
        cols = st.columns([0.7, 1, 1.5, 1.8, 1.4, 1])
        cols[0].markdown(f"**#{int(row[t('category_browser.col_rank')])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(row["industry"])
        cols[4].markdown(row[t("category_browser.col_money")])
        if cols[5].button(t("category_browser.btn_view"), key=f"val_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# Section B: 產業分類瀏覽
# ════════════════════════════════════════════════════════════

def _render_industry_browser(all_stock_info: pd.DataFrame):
    """產業分類瀏覽：左側產業列表，右側該產業個股"""
    st.markdown(f"### 🏭 {t('category_browser.industry_browser_title')}")

    # 取得所有唯一產業
    industries = (
        all_stock_info["industry_category"]
        .dropna()
        .unique()
    )
    # 過濾空字串
    industries = sorted([str(i).strip() for i in industries if str(i).strip()])

    if not industries:
        st.info(t("category_browser.no_industry_data"))
        return

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown(f"#### {t('category_browser.select_industry')}")
        # 使用 radio 選擇產業
        selected_industry = st.radio(
            t("stock.industry"),
            industries,
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown(f"#### {selected_industry} — {t('category_browser.components')}")
        industry_stocks = all_stock_info[
            all_stock_info["industry_category"] == selected_industry
        ].sort_values("stock_id")

        if len(industry_stocks) == 0:
            st.info(t("category_browser.no_industry_stocks"))
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
                        t("category_browser.btn_view_card"),
                        key=f"ind_{row['stock_id']}",
                        use_container_width=True,
                    ):
                        navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# Section C: 熱門列表（依成交量排序）
# ════════════════════════════════════════════════════════════

def _render_hot_stocks_by_volume(price_map: dict, info_map: dict):
    """熱門列表：取最近一日成交量最高的前 20 檔"""
    st.markdown(f"### 🔥 {t('category_browser.hot_stocks_title')}")

    if not price_map:
        st.info(t("category_browser.no_volume_data"))
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
    df_volume[t("category_browser.col_rank")] = range(1, len(df_volume) + 1)
    df_volume[t("category_browser.col_volume")] = df_volume["trading_volume"].apply(_format_volume)
    df_volume[t("category_browser.col_close")] = df_volume["close"].apply(lambda x: f"{x:,.2f}")

    st.markdown(f"#### {t('category_browser.top_20_hot')}")
    for _, row in df_volume.iterrows():
        cols = st.columns([0.7, 1, 1.5, 1.8, 1.4, 1])
        cols[0].markdown(f"**#{int(row[t('category_browser.col_rank')])}**")
        cols[1].markdown(f"`{row['stock_id']}`")
        cols[2].markdown(row["stock_name"])
        cols[3].markdown(row["industry"])
        cols[4].markdown(row[t("category_browser.col_volume")])
        if cols[5].button(t("category_browser.btn_view"), key=f"vol_{row['stock_id']}", use_container_width=True):
            navigate_to(page="名片", stock_id=row["stock_id"])


# ════════════════════════════════════════════════════════════
# 輔助函式
# ════════════════════════════════════════════════════════════

def _format_money(value: float) -> str:
    """格式化成交金額：億 / 萬"""
    if value >= 1e8:
        return f"{value / 1e8:,.1f} {t('unit.hundred_million')}"
    elif value >= 1e4:
        return f"{value / 1e4:,.0f} {t('unit.ten_thousand')}"
    else:
        return f"{value:,.0f}"


def _format_volume(value: int) -> str:
    """格式化成交量：張 / 萬張"""
    if value >= 1e4:
        return f"{value / 1e4:,.1f} {t('unit.thousand_shares')}"
    else:
        return f"{value:,.0f} {t('unit.shares')}"
