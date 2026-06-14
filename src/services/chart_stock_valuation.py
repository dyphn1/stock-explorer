"""
圖表生成器 — 估值相關圖表
用 Plotly 生成估值區間圖等視覺化圖表
"""

import plotly.graph_objects as go
import pandas as pd
from src.services.financial_metrics import extract_quarterly_eps
from src.services.chart_stock_financial import _get_chart_colors, _apply_theme_layout


def create_valuation_band_chart(
    stock_id: str,
    stock_name: str,
    daily_price_df: pd.DataFrame,
    financial_df: pd.DataFrame,
    latest_per_pbr: dict,
) -> tuple:
    """
    估值區間圖（歷史 P/E 範圍）
    顯示當前 PER 在歷史百分位中的位置，含 25th-75th 百分位帶
    Returns: (fig, interpretation_dict)
    """
    theme = _get_chart_colors()

    # ── 基本資料驗證 ─────────────────────────────────────────
    if daily_price_df is None or len(daily_price_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無股價資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig, {}

    if financial_df is None or len(financial_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無財務資料，無法計算本益比", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig, {}

    if not latest_per_pbr or not latest_per_pbr.get("PER"):
        fig = go.Figure()
        fig.add_annotation(text="目前無法取得本益比資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig, {}

    try:
        # ── Step 1: 整理每日股價 ──────────────────────────────
        price_df = daily_price_df.copy()
        price_df["date"] = pd.to_datetime(price_df["date"])
        price_df = price_df.sort_values("date").reset_index(drop=True)

        # 只取最近 5 年
        cutoff_5y = pd.Timestamp.now() - pd.Timedelta(days=1825)
        price_df = price_df[price_df["date"] >= cutoff_5y]

        # Fallback: if less than 2 years of data available, use whatever is available
        if len(price_df) == 0:
            price_df = daily_price_df.copy()
            price_df["date"] = pd.to_datetime(price_df["date"])
            price_df = price_df.sort_values("date").reset_index(drop=True)
            if len(price_df) == 0:
                fig = go.Figure()
                fig.add_annotation(text="近五年無股價資料", x=0.5, y=0.5, showarrow=False)
                _apply_theme_layout(fig)
                return fig, {}
            note = "（資料不足 5 年，顯示全部可用資料）"
        else:
            # Check if we have at least 2 years of data in the 5-year window
            date_range = price_df["date"].max() - price_df["date"].min()
            if date_range.days < 730:
                note = "（資料不足 5 年，顯示全部可用資料）"
            else:
                note = ""

        # ── Step 2: 從財務資料提取季度 EPS ──────────────────
        eps_df = extract_quarterly_eps(financial_df)

        if eps_df is None:
            fig = go.Figure()
            fig.add_annotation(text="無法從財務資料中提取 EPS", x=0.5, y=0.5, showarrow=False)
            _apply_theme_layout(fig)
            return fig, {}

        # ── Step 3: 計算 TTM EPS（近四季加總） ─────────────
        # 對每個股價日期，找到當時可用的最近 4 季 EPS 加總
        quarterly_dates = eps_df["date"].values
        quarterly_eps = eps_df["value"].values

        per_dates = []
        per_values = []

        for _, row in price_df.iterrows():
            current_date = row["date"]
            current_price = row["close"]

            # 找到當前日期前（含）的所有季度 EPS
            available = eps_df[eps_df["date"] <= current_date]

            if len(available) < 1:
                continue

            # 取最近最多 4 季
            ttm_eps = available.tail(4)["value"].sum()

            if ttm_eps <= 0:
                continue

            per = current_price / ttm_eps
            per_dates.append(current_date)
            per_values.append(per)

        if len(per_values) == 0:
            fig = go.Figure()
            fig.add_annotation(text="EPS 為負或零，無法計算本益比", x=0.5, y=0.5, showarrow=False)
            _apply_theme_layout(fig)
            return fig, {}

        per_series = pd.Series(per_values, index=per_dates)

        # ── Step 4: 計算百分位帶 ─────────────────────────────
        p25 = float(per_series.quantile(0.25))
        p75 = float(per_series.quantile(0.75))
        current_per = float(latest_per_pbr["PER"])

        # ── Step 5: 估值解讀 ─────────────────────────────────
        if current_per < p25:
            valuation_text = "📉 目前估值偏低，比過去 75% 的時候都便宜"
        elif current_per > p75:
            valuation_text = "📈 目前估值偏高，比過去 75% 的時候都貴"
        else:
            valuation_text = "📊 目前估值在中間範圍"

        interpretation = {
            "p25": p25,
            "p75": p75,
            "current_per": current_per,
            "valuation_text": valuation_text,
        }

        # ── Step 6: 繪圖 ─────────────────────────────────────
        fig = go.Figure()

        # 百分位帶（25th-75th）
        fig.add_trace(go.Scatter(
            x=per_series.index.tolist() + per_series.index.tolist()[::-1],
            y=[p75] * len(per_series) + [p25] * len(per_series),
            fill="toself",
            fillcolor="rgba(52, 152, 219, 0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="25th-75th 百分位",
            hoverinfo="skip",
        ))

        # 歷史 PER 折線
        fig.add_trace(go.Scatter(
            x=per_series.index,
            y=per_series.values,
            mode="lines",
            name="歷史 PER",
            line=dict(color="#3498DB", width=2),
            hovertemplate="日期: %{x|%Y/%m/%d}<br>PER: %{y:.1f}<extra></extra>",
        ))

        # 當前 PER 水平線
        fig.add_hline(
            y=current_per,
            line_dash="dash",
            line_color="#E74C3C",
            line_width=2,
            annotation_text=f"目前 PER: {current_per:.1f}",
            annotation_position="top right",
            annotation_font=dict(color="#E74C3C", size=13),
        )

        # 25th / 75th 百分位標註線
        fig.add_hline(y=p25, line_dash="dot", line_color=theme["divider"], line_width=1)
        fig.add_hline(y=p75, line_dash="dot", line_color=theme["divider"], line_width=1)

        title_text = f"{stock_name} 估值區間（歷史 P/E 範圍）"
        if note:
            title_text += f" {note}"
        title_text += " <sub style='font-size:0.7rem;color:#7F8C8D;'>💡 PER = 本益比</sub>"

        fig.update_layout(
            title=dict(
                text=title_text,
                font=dict(size=18, color=theme["title"]),
                x=0.5,
            ),
            xaxis_title="日期",
            yaxis_title="本益比 (PER)",
            height=420,
            margin=dict(t=60, b=40, l=60, r=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        )
        _apply_theme_layout(fig)

        return fig, interpretation

    except Exception:
        fig = go.Figure()
        fig.add_annotation(text="估值區間圖計算失敗", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig, {}
