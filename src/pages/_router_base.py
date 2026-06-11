"""
路由器共享工具函式
"""

import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from src.data.finmind_client import FinMindClient, FinMindRateLimitError
from src.services.financial_metrics import calc_extra_metrics, find_financial_value


def get_stock_data(client: FinMindClient, stock_id: str) -> dict:
    """載入一支股票的所有資料，回傳 dict。gate check sequential，其餘資料平行載入。"""
    stock_info = client.get_stock_info(stock_id)
    if len(stock_info) == 0:
        return None

    stock_name = stock_info.iloc[0]["stock_name"]
    industry = stock_info.iloc[0]["industry_category"]

    data = {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "industry": industry,
    }

    # ── 定義每個 fetch task：(name, lambda) ──
    tasks = [
        ("latest_price",         lambda: client.get_latest_price(stock_id)),
        ("latest_per_pbr",       lambda: client.get_latest_per_pbr(stock_id)),
        ("monthly_revenue",      lambda: client.get_monthly_revenue(stock_id)),
        ("daily_price",          lambda: client.get_daily_price(stock_id)),
        ("financial",            lambda: client.get_financial_statement(stock_id)),
        ("news",                 lambda: client.get_news(stock_id)),
        ("institutional",        lambda: client.get_institutional_investors(stock_id)),
        ("balance_sheet",        lambda: client.get_balance_sheet(stock_id)),
        ("cash_flow",            lambda: client.get_cash_flow(stock_id)),
        ("dividend",             lambda: client.get_dividend(stock_id)),
    ]

    def _fetch(name, fn):
        try:
            return name, fn()
        except FinMindRateLimitError:
            # Set session state flag so UI can show a warning
            st.session_state["_rate_limited"] = True
            return name, None
        except Exception:
            return name, None

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_fetch, name, fn): name for name, fn in tasks}
        for future in as_completed(futures):
            name, result = future.result()
            data[name] = result

    data["extra_metrics"] = calc_extra_metrics(
        data["financial"], data["balance_sheet"], data["monthly_revenue"]
    )

    if st.session_state.get("_rate_limited"):
        st.warning("⚠️ API 速率限制已達上限，部分資料可能無法載入。請稍後再試。")
        st.session_state["_rate_limited"] = False  # reset after showing

    return data


def _section_title(title: str):
    if not title:
        st.markdown(f"### 📊 {title}")
        return

    first_char = title[0]
    code = ord(first_char)
    if ( (0x1F300 <= code <= 0x1F5FF) or
         (0x1F600 <= code <= 0x1F64F) or
         (0x1F680 <= code <= 0x1F6FF) or
         (0x1F900 <= code <= 0x1F9FF) or
         (0x1FA70 <= code <= 0x1FAFF) or
         (0x2600 <= code <= 0x26FF) or
         (0x2700 <= code <= 0x27BF) or
         (0x1F1E6 <= code <= 0x1F1FF) ):
        st.markdown(f"### {title}")
    else:
        st.markdown(f"### 📊 {title}")


def _白话_card(label: str, value: str, analogy: str = ""):
    st.markdown(f"""
    <div style="background:#F5F5F5;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
        <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
        <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{analogy}</div>
    </div>
    """, unsafe_allow_html=True)

def _summary_card(title: str, content: str, icon: str = "📋"):
    st.markdown(f"""
    <div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
        <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)



def _info_card(title: str, content: str, icon: str = "💡"):
    st.markdown(f"""
    <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
        <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
        <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── M3: Timeline helpers ──────────────────────────────────

_TIMELINE_OPTIONS = {
    "1Y": 365,
    "3Y": 365 * 3,
    "5Y": 365 * 5,
    "ALL": None,
}

_TIMELINE_LABELS = {
    "1Y": "1 年",
    "3Y": "3 年",
    "5Y": "5 年",
    "ALL": "全部",
}


def filter_by_timeline(
    df: pd.DataFrame, date_col: str = "date", timeline_key: str = "timeline_range"
) -> pd.DataFrame:
    """
    根據 session_state[timeline_key] 過濾 dataframe。

    Args:
        df: 要過濾的 dataframe，必須包含 date_col 欄位。
        date_col: 日期欄位名稱，預設為 'date'。
        timeline_key: session_state 中的時間軸 key，預設為 'timeline_range'。

    Returns:
        過濾後的 dataframe。過濾失敗或結果為空時回傳原始 df 並顯示提示。
    """
    if df is None or len(df) == 0:
        return df

    selected = st.session_state.get(timeline_key, "3Y")

    if selected == "ALL":
        return df

    days = _TIMELINE_OPTIONS.get(selected)
    if days is None:
        return df

    try:
        dates = pd.to_datetime(df[date_col])
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
        mask = dates >= cutoff
        filtered_df = df[mask].reset_index(drop=True)
    except (ValueError, TypeError, KeyError) as e:
        st.warning(f"⚠️ 時間軸過濾失敗（{e}），已顯示全部資料")
        return df
    except Exception as e:
        st.warning(f"⚠️ 時間軸過濾異常，已顯示全部資料")
        return df

    # Filtered result is empty — fall back to full data with info
    if len(filtered_df) == 0:
        st.info("📌 此時間範圍內無資料，已切換至全部資料")
        return df

    return filtered_df
