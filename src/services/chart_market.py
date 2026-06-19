"""
圖表生成器 — 市場/ETF 相關圖表
用 Plotly 生成市場與 ETF 相關的視覺化圖表
"""

from typing import Optional

import plotly.graph_objects as go
import pandas as pd

from src.core.i18n import t
from src.services.chart_stock import _get_chart_colors, _apply_theme_layout


def create_price_area_chart(df: pd.DataFrame, title: Optional[str] = None) -> go.Figure:
    """ETF 價格面積圖；單一期間 fallback 為單根長條圖"""
    if title is None:
        title = t("chart.market.price_area_title")
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.market.no_price_data"), x=0.5, y=0.5, showarrow=False)
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
            x=[t("chart.market.close_price")], y=[row["close"]],
            marker_color="#3498DB",
            hovertemplate=t("chart.market.close_price_hover") + "<extra></extra>",
        ))
        fig.update_layout(
            title=dict(text=f"{title}（{t('chart.market.single_period')}）", font=dict(size=18, color=theme["title"]), x=0.5),
            showlegend=False,
            margin=dict(t=60, b=60, l=60, r=20),
            height=400,
        )
        _apply_theme_layout(fig)
        fig.update_yaxes(title_text=t("chart.market.price"))
        fig.add_annotation(
            text=t("chart.market.single_period_note"),
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
        name=t("chart.market.close_price"),
        line=dict(color="#3498DB", width=2),
        fill="tozeroy",
        fillcolor="rgba(52, 152, 219, 0.1)",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=theme["title"]), x=0.5),
        xaxis_title=t("chart.market.date"),
        yaxis_title=t("chart.market.price"),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    _apply_theme_layout(fig)
    fig.update_xaxes(showgrid=True, gridcolor=theme["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=theme["grid"])

    return fig
