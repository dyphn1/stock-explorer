"""
圖表生成器
用 Plotly 生成所有視覺化圖表
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def create_revenue_pie_chart(revenue_items: list, title: str = "營收來源") -> go.Figure:
    """
    營收來源圓餅圖
    revenue_items: [{"name": "手機晶片", "value": 40.0, "description": "..."}]
    """
    if not revenue_items:
        fig = go.Figure()
        fig.add_annotation(text="暫無營收組成資料", x=0.5, y=0.5, showarrow=False)
        return fig

    labels = [item["name"] for item in revenue_items]
    values = [item["value"] for item in revenue_items]
    descriptions = [item.get("description", "") for item in revenue_items]

    # 自定義顏色
    colors = px.colors.qualitative.Set3[:len(labels)]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>" +
                      "佔比: %{percent}<br>" +
                      "金額: %{value:,.0f} 千元<br>" +
                      "<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=20), x=0.5),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        margin=dict(t=60, b=60, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_revenue_trend_chart(df: pd.DataFrame, title: str = "月營收趨勢") -> go.Figure:
    """月營收趨勢圖（含年增率）"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無營收資料", x=0.5, y=0.5, showarrow=False)
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
        subplot_titles=("月營收", "年增率 (%)"),
        row_heights=[0.7, 0.3]
    )

    # 營收柱狀圖
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["revenue"] / 1e8,  # 轉為億
            name="月營收",
            marker_color="#4A90D9",
            hovertemplate="%{x|%Y/%m}<br>營收: %{y:,.1f} 億<extra></extra>"
        ),
        row=1, col=1
    )

    # 年增率折線圖
    yoy_data = df.dropna(subset=["yoy"])
    if len(yoy_data) > 0:
        colors = ["#2ECC71" if v >= 0 else "#E74C3C" for v in yoy_data["yoy"]]
        fig.add_trace(
            go.Bar(
                x=yoy_data["date"],
                y=yoy_data["yoy"],
                name="年增率",
                marker_color=colors,
                hovertemplate="%{x|%Y/%m}<br>年增率: %{y:.1f}%<extra></extra>"
            ),
            row=2, col=1
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=18), x=0.5),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
    )

    fig.update_yaxes(title_text="億元", row=1, col=1)
    fig.update_yaxes(title_text="%", row=2, col=1)

    return fig


def create_price_chart(df: pd.DataFrame, title: str = "股價走勢") -> go.Figure:
    """股價走勢圖（K 線 + 成交量）"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無股價資料", x=0.5, y=0.5, showarrow=False)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

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
            name="K線",
            increasing_line_color="#E74C3C",
            decreasing_line_color="#2ECC71",
        ),
        row=1, col=1
    )

    # 成交量
    colors = ["#E74C3C" if c >= o else "#2ECC71"
              for c, o in zip(df["close"], df["open"])]
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["Trading_Volume"] / 1e3,  # 轉為張
            name="成交量",
            marker_color=colors,
            opacity=0.6,
        ),
        row=2, col=1
    )

    fig.update_layout(
        title=dict(text=title, font=dict(size=18), x=0.5),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        xaxis_rangeslider_visible=False,
    )

    fig.update_yaxes(title_text="價格", row=1, col=1)
    fig.update_yaxes(title_text="張數(千)", row=2, col=1)

    return fig


def create_funnel_chart(revenue: float, gross_profit: float,
                        operating_income: float, net_income: float,
                        title: str = "利潤漏斗") -> go.Figure:
    """
    利潤漏斗圖
    營收 → 毛利 → 營業利益 → 淨利
    """
    stages = ["營收", "毛利", "營業利益", "淨利"]
    values = [revenue, gross_profit, operating_income, net_income]

    # 過濾掉 0 或負值
    valid = [(s, v) for s, v in zip(stages, values) if v > 0]
    if not valid:
        fig = go.Figure()
        fig.add_annotation(text="暫無財務資料", x=0.5, y=0.5, showarrow=False)
        return fig

    stages, values = zip(*valid)

    fig = go.Figure(go.Funnel(
        y=stages,
        x=[v / 1e8 for v in values],  # 轉為億
        textinfo="value+percent initial",
        texttemplate="%{x:,.1f} 億<br>%{percentInitial}",
        marker=dict(
            color=["#3498DB", "#2ECC71", "#F39C12", "#E74C3C"],
            line=dict(width=2, color="#fff")
        ),
        connector=dict(line=dict(color="#BDC3C7", width=2)),
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=18), x=0.5),
        margin=dict(t=60, b=40, l=100, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
    )

    return fig


def create_comparison_radar(metrics: dict, target_name: str,
                            benchmark_name: str) -> go.Figure:
    """
    同業比較雷達圖
    metrics: {"營收": [80, 100], "毛利率": [66, 35], "ROE": [25, 15], ...}
    """
    if not metrics:
        fig = go.Figure()
        fig.add_annotation(text="暫無比較資料", x=0.5, y=0.5, showarrow=False)
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

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(target_values), max(benchmark_values)) * 1.1])
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        margin=dict(t=40, b=60, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
    )

    return fig


def create_institutional_chart(df: pd.DataFrame, title: str = "三大法人買賣超") -> go.Figure:
    """三大法人買賣超圖"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無法人資料", x=0.5, y=0.5, showarrow=False)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # 計算每日買賣超
    df["net_buy"] = df["buy"] - df["sell"]

    fig = go.Figure()
    colors = ["#2ECC71" if v >= 0 else "#E74C3C" for v in df["net_buy"]]

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["net_buy"] / 1e3,  # 轉為張
        marker_color=colors,
        hovertemplate="%{x|%Y/%m/%d}<br>買賣超: %{y:,.0f} 張<extra></extra>"
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="#7F8C8D")

    fig.update_layout(
        title=dict(text=title, font=dict(size=16), x=0.5),
        showlegend=False,
        margin=dict(t=50, b=40, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
    )

    fig.update_yaxes(title_text="張數(千)")

    return fig
