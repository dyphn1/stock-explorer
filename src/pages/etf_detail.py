"""
ETF 詳情頁 — M1 MVP
目標：使用者在 10 秒內知道這檔 ETF 的投資定位與特色
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.finmind_client import FinMindClient
from src.pages._router_base import _section_title, _白话_card, _info_card, filter_by_timeline


def _get_etf_one_liner(stock_name: str) -> str:
    """根據 ETF 名稱關鍵字產生一句話定位"""
    name = stock_name.lower()
    if "50" in name or "台灣50" in name:
        return "追蹤台灣前 50 大企業的指數型基金"
    if "高股息" in name or "股息" in name:
        return "專注於高股息股票的收益型基金"
    if "債券" in name or "債" in name:
        return "投資債券市場的固定收益型基金"
    if "esg" in name or "永續" in name:
        return "考慮環境、社會、治理的永續投資型基金"
    return "一籃子股票的分散投資工具"


def _get_etf_knowledge(stock_name: str) -> str:
    """根據 ETF 類型回傳對應的 ETF 小知識"""
    name = stock_name.lower()
    if "50" in name or "台灣50" in name:
        return (
            "ETF（指數股票型基金）就像「一籃子股票」的套餐，一次買進就等於持有前 50 大上市公司。"
            "不用選股、自動跟著大盤走，管理費也遠低於主動型基金，適合想參與台股大盤但不想個股研究的投資人。"
        )
    if "高股息" in name or "股息" in name:
        return (
            "高股息 ETF 專門挑選「現金股利大方」的公司，目標是讓投資人定期收到配息，"
            "就像收房租一樣有穩定現金流。適合需要定期收入（如退休族）或偏好領息而非賺價差的投資人。"
        )
    if "債券" in name or "債" in name:
        return (
            "債券 ETF 投資的是政府或企業發行的債券，性質類似「借錢給對方、對方按期付利息」。"
            "波動通常比股票小，報酬來源主要是配息而非價差，適合保守型投資人或在股市震盪時作為避風港。"
        )
    if "esg" in name or "永續" in name:
        return (
            "ESG ETF 在選股時除了看財務表現，還會評估企業的環保（E）、社會責任（S）與公司治理（G）。"
            "概念是「好公司不只賺錢，還要對世界好」，適合重視永續發展、不想投資高污染或爭議產業的投資人。"
        )
    return (
        "ETF（指數股票型基金）就像一籃子股票的套餐，一次買進就分散持有多檔標的。"
        "好處是不用自己選股、管理費低、透明度高，適合想參與市場但不想花時間研究個股的投資人。"
    )


def _get_dividend_frequency_analogy(dividend_df: pd.DataFrame) -> str:
    """根據配息資料推估配息頻率並給出白話說明"""
    if dividend_df is None or len(dividend_df) == 0:
        return ""

    try:
        years = dividend_df["year"].nunique() if "year" in dividend_df.columns else 0
        total = len(dividend_df)

        if years == 0:
            return ""

        avg_per_year = total / years if years > 0 else 0

        if avg_per_year >= 4:
            return "📅 配息頻率：季配（一年配 4 次）— 就像每季領一次零用錢"
        elif avg_per_year >= 2:
            return "📅 配息頻率：半年配（一年配 2 次）— 就像半年領一次分紅"
        elif avg_per_year >= 1:
            return "📅 配息頻率：年配（一年配 1 次）— 就像年底領一次年終"
        else:
            return "📅 配息頻率：不固定 — 視當年獲利情況決定"
    except Exception:
        return ""


def _render_etf_detail(data: dict, client: FinMindClient):
    """ETF 詳情主頁（M1）"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    daily_price = data["daily_price"]
    institutional = data["institutional"]
    dividend = data["dividend"]
    extra_metrics = data.get("extra_metrics", {})

    # ── Header ──────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{stock_name}** `{stock_id}` ｜ {industry}")
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            sign = "+" if change >= 0 else ""
            st.markdown(f"**{price:,.2f}** `{sign}{change:,.2f}`")

    st.markdown("---")

    # ── 一句話定位 ──────────────────────────────────────────
    one_liner = _get_etf_one_liner(stock_name)
    st.markdown(f"""
    <div style="font-size:1.3rem;font-weight:500;color:#2C3E50;text-align:center;padding:1.5rem 2rem;background:linear-gradient(135deg,#EBF5FB 0%,#D4E6F1 100%);border-radius:12px;margin:1rem 0;line-height:1.8;border-left:5px solid #3498DB;">
        💡 {one_liner}
    </div>
    """, unsafe_allow_html=True)

    # ── 績效走勢 ────────────────────────────────────────────
    _section_title("績效走勢")
    if daily_price is not None and len(daily_price) > 0:
        try:
            df_price = daily_price.copy()
            df_price["date"] = pd.to_datetime(df_price["date"])
            # 取最近 1 年
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=365)
            df_price = df_price[df_price["date"] >= cutoff].reset_index(drop=True)

            if len(df_price) > 0:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_price["date"],
                    y=df_price["close"],
                    mode="lines",
                    name="收盤價",
                    line=dict(color="#3498DB", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(52, 152, 219, 0.1)",
                ))
                fig.update_layout(
                    title=f"{stock_name} 近一年收盤價走勢",
                    xaxis_title="日期",
                    yaxis_title="價格",
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                )
                fig.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
                fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("近一年無價格資料")
        except Exception:
            st.info("價格資料處理中，暫時無法顯示圖表")
    else:
        st.info("暫無價格資料")

    st.markdown("---")

    # ── 配息資訊 ────────────────────────────────────────────
    _section_title("配息資訊")
    if dividend is not None and len(dividend) > 0:
        try:
            freq_analogy = _get_dividend_frequency_analogy(dividend)
            if freq_analogy:
                _info_card("配息頻率", freq_analogy, icon="📅")

            # 顯示最近 5 筆配息
            display_cols = []
            col_mapping = {}
            for col in dividend.columns:
                if col in ("date", "stock_id", "year"):
                    display_cols.append(col)
                    col_mapping[col] = col
                elif "CashEarningsDistribution" in col:
                    display_cols.append(col)
                    col_mapping[col] = "現金股利"
                elif "CashExDividendTradingDate" in col:
                    display_cols.append(col)
                    col_mapping[col] = "除息日"
                elif "StockEarningsDistribution" in col:
                    display_cols.append(col)
                    col_mapping[col] = "股票股利"
                elif "ExRightDividendTradingDate" in col:
                    display_cols.append(col)
                    col_mapping[col] = "除權日"

            if not display_cols:
                display_cols = list(dividend.columns[:6])

            recent = dividend.head(5)[display_cols].copy()
            recent = recent.rename(columns=col_mapping)

            # 格式化數值
            for col in recent.columns:
                if "股利" in str(col):
                    recent[col] = recent[col].apply(
                        lambda x: f"{x:.2f}" if pd.notna(x) else "-"
                    )

            st.dataframe(recent, use_container_width=True, hide_index=True)

            # 白話說明
            st.markdown("""
            <div style="background:#F8F9FA;border-radius:10px;padding:1rem;margin-top:0.5rem;font-size:0.85rem;color:#5D6D7E;">
                💡 <b>白話說明：</b>「現金股利」是公司直接發錢給你，就像房東每月匯房租到你戶頭。
                「除息日」是股價會扣除配息金額的日子，所以除息當天股價會「自然下跌」，不代表賠錢。
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.info("配息資料處理中")
    else:
        st.info("此 ETF 暫無配息資料（可能為不配息型或尚未開始配息）")

    st.markdown("---")

    # ── 法人動向 ────────────────────────────────────────────
    _section_title("法人動向")
    if institutional is not None and len(institutional) > 0:
        try:
            df_inst = institutional.copy()
            df_inst["date"] = pd.to_datetime(df_inst["date"])
            # 取最近 30 天
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
            df_inst = df_inst[df_inst["date"] >= cutoff].reset_index(drop=True)

            if len(df_inst) > 0:
                # 計算三大法人買賣超
                buy_col = None
                sell_col = None
                for col in df_inst.columns:
                    col_lower = col.lower()
                    if "buy" in col_lower or "買進" in col:
                        buy_col = col
                    elif "sell" in col_lower or "賣出" in col:
                        sell_col = col

                if buy_col and sell_col:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=df_inst["date"],
                        y=df_inst[buy_col],
                        name="買超",
                        marker_color="#27AE60",
                    ))
                    fig.add_trace(go.Bar(
                        x=df_inst["date"],
                        y=-df_inst[sell_col],
                        name="賣超",
                        marker_color="#E74C3C",
                    ))
                    fig.update_layout(
                        title=f"{stock_name} 近 30 日法人買賣超",
                        xaxis_title="日期",
                        yaxis_title="張數",
                        barmode="relative",
                        height=350,
                        margin=dict(l=40, r=40, t=60, b=40),
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    )
                    fig.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
                    fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # 若找不到買/賣欄位，直接顯示表格
                    st.dataframe(df_inst.tail(10), use_container_width=True, hide_index=True)

                # 白話說明
                st.markdown("""
                <div style="background:#F8F9FA;border-radius:10px;padding:1rem;margin-top:0.5rem;font-size:0.85rem;color:#5D6D7E;">
                    💡 <b>白話說明：</b>「法人」指的是外資、投信、自營商這些大資金玩家。
                    法人連續買超 = 大戶看好；法人連續賣超 = 大戶在撤退。散戶可以參考法人動向，但不要盲目跟單。
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("近 30 日無法人交易資料")
        except Exception:
            st.info("法人資料處理中")
    else:
        st.info("暫無法人交易資料")

    st.markdown("---")

    # ── 費用說明 ────────────────────────────────────────────
    _section_title("費用說明")
    col1, col2 = st.columns(2)

    with col1:
        _白话_card(
            label="📋 經理費（管理費）",
            value="約 0.3% / 年",
            analogy="每投資 10 萬元，一年付 300 元 — 就像請一位專業管家幫你管錢，一天不到 1 元",
        )

    with col2:
        _白话_card(
            label="📋 保管費",
            value="約 0.04% / 年",
            analogy="每投資 10 萬元，一年付 40 元 — 就像把錢存在銀行保險庫的保管費",
        )

    _info_card(
        title="💡 ETF 費用小提醒",
        content=(
            "ETF 的總費用（經理費 + 保管費 + 其他）通常比主動型基金低很多。"
            "以台股 ETF 為例，總費用率大約 0.3%~0.5%，而主動型基金可能 1.5% 以上。"
            "長期投資下來，省下來的費用會默默幫你多賺好幾年的複利！"
        ),
        icon="💰",
    )

    st.markdown("---")

    # ── ETF 小知識 ──────────────────────────────────────────
    _section_title("ETF 小知識")
    knowledge = _get_etf_knowledge(stock_name)
    _info_card(
        title=f"📚 {stock_name} 是什麼？",
        content=knowledge,
        icon="🎓",
    )

    # 免責聲明
    st.markdown("""
    <div style="background:#FEF9E7;border:1px solid #F9E79F;border-radius:8px;padding:1rem;font-size:0.85rem;color:#7D6608;margin-top:2rem;">
        ⚠️ 本工具僅供認識 ETF 使用，所有數據來自公開資訊觀測站與 FinMind。
        不構成任何投資建議。投資有風險，請自行評估。
    </div>
    """, unsafe_allow_html=True)
