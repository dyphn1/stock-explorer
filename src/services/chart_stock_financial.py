"""
圖表生成器 — 財務相關圖表
用 Plotly 生成營收、股價、法人等財務視覺化圖表
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

from src.core.i18n import t


# ── Theme-aware color scheme ─────────────────────────────
# Strategy: use colors that provide sufficient contrast in BOTH
# light and dark Streamlit themes.  Semi-transparent values let
# the background show through, creating natural adaptation.
#
# - Text / axis labels: #7F8C8D — readable on white AND dark bg
# - Grid lines: rgba(128,128,128,0.15) — subtle on both themes
# - Muted / annotation text: #7F8C8D — mid-gray, works both ways
# - Divider / connector: rgba(128,128,128,0.3) — subtle structural line
# - Trace border: rgba(255,255,255,0.8) — soft white blend

def _get_chart_colors() -> dict:
    """Return a dict of theme-aware colors for chart styling.

    These values are chosen to have adequate contrast in both
    Streamlit light mode (white-ish bg) and dark mode (dark bg).
    """
    return {
        "text": "#7F8C8D",                     # axis & label text
        "title": "#2C3E50",                    # chart titles — slightly darker
        "grid": "rgba(128,128,128,0.15)",      # grid lines
        "muted": "#7F8C8D",                    # muted / annotation text
        "divider": "rgba(128,128,128,0.3)",    # connector / structural lines
        "border": "rgba(255,255,255,0.8)",     # pie / funnel borders
    }


def _apply_theme_layout(fig: go.Figure) -> go.Figure:
    """Apply theme-aware layout defaults to a Plotly figure.

    Sets transparent backgrounds (so Streamlit theme is inherited),
    and applies theme-aware font / grid / axis colors that work in
    both light and dark mode.
    """
    colors = _get_chart_colors()

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=colors["text"]),
    )

    # Apply axis styling — subplots may have xaxis2/yaxis2 etc.
    fig.update_xaxes(
        tickfont=dict(color=colors["text"]),
        title_font=dict(color=colors["text"]),
        gridcolor=colors["grid"],
        zerolinecolor=colors["grid"],
        linecolor=colors["grid"],
    )
    fig.update_yaxes(
        tickfont=dict(color=colors["text"]),
        title_font=dict(color=colors["text"]),
        gridcolor=colors["grid"],
        zerolinecolor=colors["grid"],
        linecolor=colors["grid"],
    )

    # Make annotation text use muted color by default
    for ann in fig.layout.annotations or []:
        if ann.font and ann.font.color is None:
            ann.font.color = colors["muted"]

    return fig


def create_revenue_pie_chart(revenue_items: list, title: str = None) -> go.Figure:
    """
    營收來源圓餅圖
    revenue_items: [{"name": "手機晶片", "value": 40.0, "description": "..."}]
    """
    if title is None:
        title = t("chart.stock_financial.revenue_source")
    if not revenue_items:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_revenue_composition"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    labels = [item["name"] for item in revenue_items]
    values = [item["value"] for item in revenue_items]
    descriptions = [item.get("description", "") for item in revenue_items]

    theme = _get_chart_colors()

    # Design system colors — theme-aware, accessible palette
    colors = ['#3498DB', '#27AE60', '#E74C3C', '#2C3E50', '#7F8C8D', '#ECF0F1']
    # Cycle if more labels than colors
    colors = [colors[i % len(colors)] for i in range(len(labels))]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color=theme["border"], width=2)),
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>" +
                      t("chart.stock_financial.proportion") + ": %{percent}<br>" +
                      "<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=theme["title"]), x=0.5),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        margin=dict(t=60, b=60, l=20, r=20),
    )
    _apply_theme_layout(fig)

    return fig


def create_revenue_trend_chart(df: pd.DataFrame, title: str = None) -> go.Figure:
    """月營收趨勢圖（含年增率）"""
    if title is None:
        title = t("chart.stock_financial.revenue_trend")
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_revenue_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    # 計算年增率
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["yoy"] = df["revenue"].pct_change(periods=12) * 100

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(t("chart.stock_financial.monthly_revenue"), t("chart.stock_financial.yoy_rate") + " (%)"),
        row_heights=[0.7, 0.3]
    )

    # 營收柱狀圖
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["revenue"] / 1e8,  # 轉為億
            name=t("chart.stock_financial.monthly_revenue"),
            marker_color="#3498DB",
            hovertemplate="%{x|%Y/%m}<br>" + t("chart.stock_financial.revenue") + ": %{y:,.1f} " + t("chart.unit_hundred_million") + "<extra></extra>"
        ),
        row=1, col=1
    )

    # 年增率折線圖
    yoy_data = df.dropna(subset=["yoy"])
    if len(yoy_data) > 0:
        colors = ["#27AE60" if v >= 0 else "#E74C3C" for v in yoy_data["yoy"]]
        fig.add_trace(
            go.Bar(
                x=yoy_data["date"],
                y=yoy_data["yoy"],
                name=t("chart.stock_financial.yoy_rate"),
                marker_color=colors,
                hovertemplate="%{x|%Y/%m}<br>" + t("chart.stock_financial.yoy_rate") + ": %{y:.1f}%<extra></extra>"
            ),
            row=2, col=1
        )

    theme = _get_chart_colors()

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=theme["title"]), x=0.5),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=20),
        height=450,
    )
    _apply_theme_layout(fig)

    fig.update_yaxes(title_text=t("chart.unit_hundred_million"), row=1, col=1)
    fig.update_yaxes(title_text="%", row=2, col=1)

    return fig


def create_revenue_treemap(revenue_items: list, title: str = None) -> go.Figure:
    """
    Create a treemap visualization of revenue breakdown.

    Args:
        revenue_items: list of dicts with keys: name, value, description
        title: chart title

    Returns:
        plotly go.Figure
    """
    if title is None:
        title = t("chart.stock_financial.revenue_source")
    # Use a pleasant color palette
    colors = ["#3498DB", "#27AE60", "#E74C3C", "#2C3E50", "#7F8C8D", "#ECF0F1"]

    labels = [item["name"] for item in revenue_items]
    values = [item["value"] for item in revenue_items]
    descriptions = [item.get("description", "") for item in revenue_items]
    parents = [""] * len(labels)

    # Build custom hover text
    hover_texts = [f"{item['name']}: {item['value']:.0f}%<br>{item.get('description', '')}"
                   for item in revenue_items]

    color_list = colors[:len(labels)]

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo="label+value",
        hovertext=hover_texts,
        hovertemplate="%{hovertext}<extra></extra>",
        marker=dict(
            colors=color_list,
            line=dict(width=2, color="white"),
        ),
        textfont=dict(size=14, color="white"),
        textposition="middle center",
        pathbar=dict(visible=False),
    ))

    # Apply same theme-aware styling as other charts
    colors_theme = _get_chart_colors()
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=colors_theme["title"])),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(color=colors_theme["text"]),
    )

    return fig


def create_price_chart(df: pd.DataFrame, title: str = None) -> go.Figure:
    """股價走勢圖（K 線 + 成交量）；單日資料時以分組長條圖呈現 OHLC"""
    if title is None:
        title = t("chart.stock_financial.price_trend")
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_price_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # ── 單日 fallback：分組長條圖呈現 OHLC ─────────────────
    if len(df) < 2:
        row = df.iloc[0]
        ohlc_labels = [t("chart.stock_financial.open"), t("chart.stock_financial.high"), t("chart.stock_financial.low"), t("chart.stock_financial.close")]
        ohlc_values = [row["open"], row["max"], row["min"], row["close"]]
        ohlc_colors = ["#3498DB", "#27AE60", "#E74C3C", "#3498DB"]
        theme = _get_chart_colors()

        fig = go.Figure()
        for label, val, color in zip(ohlc_labels, ohlc_values, ohlc_colors):
            fig.add_trace(go.Bar(
                x=[label], y=[val],
                name=label,
                marker_color=color,
                hovertemplate=f"{label}: %{{y:,.2f}}<extra></extra>",
            ))

        fig.update_layout(
            title=dict(text=f"{title}（" + t("chart.stock_financial.single_day_only") + "）", font=dict(size=18, color=theme["title"]), x=0.5),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
            margin=dict(t=60, b=60, l=60, r=20),
            height=400,
            barmode="group",
        )
        _apply_theme_layout(fig)
        fig.update_yaxes(title_text=t("chart.stock_financial.price"))
        fig.add_annotation(
            text=t("chart.stock_financial.single_day_note"),
            xref="paper", yref="paper", x=0.5, y=-0.25,
            showarrow=False, font=dict(size=13, color=theme["muted"]),
        )
        return fig

    # ── 正常：K 線 + 成交量 ────────────────────────────────
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.75, 0.25]
    )

    # K 線圖
    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["max"],
            low=df["min"],
            close=df["close"],
            name=t("chart.stock_financial.candlestick"),
            increasing_line_color="#E74C3C",
            decreasing_line_color="#27AE60",
        ),
        row=1, col=1
    )

    # 成交量
    colors = ["#E74C3C" if c >= o else "#27AE60"
              for c, o in zip(df["close"], df["open"])]
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["Trading_Volume"] / 1e3,  # 轉為張
            name=t("chart.stock_financial.volume"),
            marker_color=colors,
            opacity=0.6,
        ),
        row=2, col=1
    )

    theme = _get_chart_colors()

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=theme["title"]), x=0.5),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=20),
        height=400,
        xaxis_rangeslider_visible=False,
    )
    _apply_theme_layout(fig)

    fig.update_yaxes(title_text=t("chart.stock_financial.price"), row=1, col=1)
    fig.update_yaxes(title_text=t("chart.stock_financial.thousand_shares"), row=2, col=1)

    return fig


def create_funnel_chart(revenue: float, gross_profit: float,
                        operating_income: float, net_income: float,
                        title: str = None) -> go.Figure:
    """
    利潤漏斗圖
    營收 → 毛利 → 營業利益 → 淨利
    """
    if title is None:
        title = t("chart.stock_financial.profit_funnel")
    stages = [t("chart.stock_financial.revenue_stage"), t("chart.stock_financial.gross_profit"), t("chart.stock_financial.operating_income"), t("chart.stock_financial.net_income")]
    values = [revenue, gross_profit, operating_income, net_income]

    # 過濾掉 0 或負值
    valid = [(s, v) for s, v in zip(stages, values) if v > 0]
    if not valid:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_financial_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    stages, values = zip(*valid)

    theme = _get_chart_colors()

    fig = go.Figure(go.Funnel(
        y=stages,
        x=[v / 1e8 for v in values],  # 轉為億
        textinfo="value+percent initial",
        texttemplate="%{x:,.1f} " + t("chart.unit_hundred_million") + "<br>%{percentInitial}",
        marker=dict(
            color=["#3498DB", "#27AE60", "#3498DB", "#E74C3C"],
            line=dict(width=2, color=theme["border"])
        ),
        connector=dict(line=dict(color=theme["divider"], width=2)),
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=theme["title"]), x=0.5),
        margin=dict(t=60, b=40, l=100, r=20),
        height=350,
    )
    _apply_theme_layout(fig)

    return fig


def create_comparison_radar(metrics: dict, target_name: str,
                            benchmark_name: str) -> go.Figure:
    """
    同業比較雷達圖
    metrics: {"營收": [80, 100], "毛利率": [66, 35], "ROE": [25, 15], ...}
    """
    if not metrics:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_comparison_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    categories = list(metrics.keys())

    fig = go.Figure()

    # 目標公司
    target_values = [metrics[c][0] for c in categories]
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill="toself",
        name=target_name,
        line=dict(color="#3498DB"),
        fillcolor="rgba(52, 152, 219, 0.3)",
    ))

    # 標竿公司
    benchmark_values = [metrics[c][1] for c in categories]
    fig.add_trace(go.Scatterpolar(
        r=benchmark_values,
        theta=categories,
        fill="toself",
        name=benchmark_name,
        line=dict(color="#E74C3C"),
        fillcolor="rgba(231, 76, 60, 0.2)",
    ))

    theme = _get_chart_colors()

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(target_values), max(benchmark_values)) * 1.1])
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        margin=dict(t=40, b=60, l=40, r=40),
        height=400,
    )
    _apply_theme_layout(fig)

    return fig


def create_institutional_chart(df: pd.DataFrame, title: str = None) -> go.Figure:
    """三大法人買賣超圖"""
    if title is None:
        title = t("chart.stock_financial.institutional_trading")
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.stock_financial.no_institutional_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # 計算每日買賣超
    df["net_buy"] = df["buy"] - df["sell"]

    fig = go.Figure()
    colors = ["#27AE60" if v >= 0 else "#E74C3C" for v in df["net_buy"]]

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["net_buy"] / 1e3,  # 轉為張
        marker_color=colors,
        hovertemplate="%{x|%Y/%m/%d}<br>" + t("chart.stock_financial.net_buy_sell") + ": %{y:,.0f} " + t("chart.stock_financial.shares") + "<extra></extra>"
    ))

    theme = _get_chart_colors()

    fig.add_hline(y=0, line_dash="dash", line_color=theme["divider"])

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=theme["title"]), x=0.5),
        showlegend=False,
        margin=dict(t=50, b=40, l=60, r=20),
        height=250,
    )
    _apply_theme_layout(fig)

    fig.update_yaxes(title_text=t("chart.stock_financial.thousand_shares"))

    return fig
