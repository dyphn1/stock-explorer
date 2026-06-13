"""
圖表生成器 — 市場/ETF 相關圖表
用 Plotly 生成市場與 ETF 相關的視覺化圖表
"""

import plotly.graph_objects as go
import pandas as pd

from src.services.chart_stock import _get_chart_colors, _apply_theme_layout


def create_price_area_chart(df: pd.DataFrame, title: str = "收盤價走勢") -> go.Figure:
    """ETF 價格面積圖；單一期間 fallback 為單根長條圖"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無價格資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # ── 單一期間 fallback：單根長條圖 ──────────────────────
    if len(df) < 2:
        row = df.iloc[0]
        theme = _get_chart_colors()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["收盤價"], y=[row["close"]],
            marker_color="#3498DB",
            hovertemplate="收盤價: %{y:,.2f}<extra></extra>",
        ))
        fig.update_layout(
            title=dict(text=f"{title}（僅單一期間）", font=dict(size=18, color=theme["title"]), x=0.5),
            showlegend=False,
            margin=dict(t=60, b=60, l=60, r=20),
            height=400,
        )
        _apply_theme_layout(fig)
        fig.update_yaxes(title_text="價格")
        fig.add_annotation(
            text="只有1期的資料，改用長條圖顯示",
            xref="paper", yref="paper", x=0.5, y=-0.25,
            showarrow=False, font=dict(size=13, color=theme["muted"]),
        )
        return fig

    # ── 正常：折線 + 面積 ──────────────────────────────────
    theme = _get_chart_colors()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["close"],
        mode="lines",
        name="收盤價",
        line=dict(color="#3498DB", width=2),
        fill="tozeroy",
        fillcolor="rgba(52, 152, 219, 0.1)",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=theme["title"]), x=0.5),
        xaxis_title="日期",
        yaxis_title="價格",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    _apply_theme_layout(fig)
    fig.update_xaxes(showgrid=True, gridcolor=theme["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=theme["grid"])

    return fig
