"""
圖表生成器
用 Plotly 生成所有視覺化圖表
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


# ── Theme-aware color scheme ─────────────────────────────
# Strategy: use colors that provide sufficient contrast in BOTH
# light and dark Streamlit themes.  Semi-transparent values let
# the background show through, creating natural adaptation.
#
# - Text / axis labels: #555555 — readable on white AND dark bg
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


def create_revenue_pie_chart(revenue_items: list, title: str = "營收來源") -> go.Figure:
    """
    營收來源圓餅圖
    revenue_items: [{"name": "手機晶片", "value": 40.0, "description": "..."}]
    """
    if not revenue_items:
        fig = go.Figure()
        fig.add_annotation(text="暫無營收組成資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    labels = [item["name"] for item in revenue_items]
    values = [item["value"] for item in revenue_items]
    descriptions = [item.get("description", "") for item in revenue_items]

    theme = _get_chart_colors()

    # Design system colors — theme-aware, accessible palette
    colors = ['#3498DB', '#27AE60', '#2C3E50', '#7F8C8D', '#1ABC9C', '#9B59B6', '#E67E22', '#2980B9']
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
                      "佔比: %{percent}<br>" +
                      "金額: %{value:,.0f} 千元<br>" +
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


def create_revenue_trend_chart(df: pd.DataFrame, title: str = "月營收趨勢") -> go.Figure:
    """月營收趨勢圖（含年增率）"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無營收資料", x=0.5, y=0.5, showarrow=False)
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
        subplot_titles=("月營收", "年增率 (%)"),
        row_heights=[0.7, 0.3]
    )

    # 營收柱狀圖
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["revenue"] / 1e8,  # 轉為億
            name="月營收",
            marker_color="#3498DB",
            hovertemplate="%{x|%Y/%m}<br>營收: %{y:,.1f} 億<extra></extra>"
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
                name="年增率",
                marker_color=colors,
                hovertemplate="%{x|%Y/%m}<br>年增率: %{y:.1f}%<extra></extra>"
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

    fig.update_yaxes(title_text="億元", row=1, col=1)
    fig.update_yaxes(title_text="%", row=2, col=1)

    return fig


def create_price_chart(df: pd.DataFrame, title: str = "股價走勢") -> go.Figure:
    """股價走勢圖（K 線 + 成交量）；單日資料時以分組長條圖呈現 OHLC"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無股價資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # ── 單日 fallback：分組長條圖呈現 OHLC ─────────────────
    if len(df) < 2:
        row = df.iloc[0]
        ohlc_labels = ["開盤", "最高", "最低", "收盤"]
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
            title=dict(text=f"{title}（僅單日資料）", font=dict(size=18, color=theme["title"]), x=0.5),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
            margin=dict(t=60, b=60, l=60, r=20),
            height=400,
            barmode="group",
        )
        _apply_theme_layout(fig)
        fig.update_yaxes(title_text="價格")
        fig.add_annotation(
            text="只有1天的資料，改用長條圖顯示",
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
            name="K線",
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
            name="成交量",
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
        _apply_theme_layout(fig)
        return fig

    stages, values = zip(*valid)

    theme = _get_chart_colors()

    fig = go.Figure(go.Funnel(
        y=stages,
        x=[v / 1e8 for v in values],  # 轉為億
        textinfo="value+percent initial",
        texttemplate="%{x:,.1f} 億<br>%{percentInitial}",
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
        fig.add_annotation(text="暫無比較資料", x=0.5, y=0.5, showarrow=False)
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


def create_institutional_chart(df: pd.DataFrame, title: str = "三大法人買賣超") -> go.Figure:
    """三大法人買賣超圖"""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無法人資料", x=0.5, y=0.5, showarrow=False)
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
        hovertemplate="%{x|%Y/%m/%d}<br>買賣超: %{y:,.0f} 張<extra></extra>"
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

    fig.update_yaxes(title_text="張數(千)")

    return fig


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


def create_health_snowflake(stock_name: str, health_scores: dict) -> go.Figure:
    """
    公司健康狀況雷達圖（雪花圖）
    health_scores: {"獲利能力": 85, "成長性": 72, "財務健康": 90, "股利品質": 65, "估值合理性": 55}
    所有分數應為 0-100。
    """
    if not health_scores:
        fig = go.Figure()
        fig.add_annotation(text="暫無健康評分資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    categories = list(health_scores.keys())
    values = [health_scores[c] for c in categories]

    # 根據各維度分數決定顏色
    def _score_color(score: float) -> str:
        if score >= 70:
            return "#27AE60"
        elif score >= 40:
            return "#F39C12"
        else:
            return "#E74C3C"

    # 整體平均分數決定主色
    avg_score = sum(values) / len(values) if values else 0
    main_color = _score_color(avg_score)

    # 每個維度的分數標籤（含顏色標記）
    r_with_labels = [f"{v:.0f}" for v in values]

    fig = go.Figure()

    # 外框線（各維度實際分數）
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # 閉合
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor=f"rgba(52, 152, 219, 0.15)",
        line=dict(color=main_color, width=2.5),
        name="目前評分",
        text=[f"{c}: {v:.0f}分" for c, v in zip(categories, values)],
        hovertemplate="%{text}<extra></extra>",
    ))

    # 參考線：及格線 40
    fig.add_trace(go.Scatterpolar(
        r=[40] * (len(categories) + 1),
        theta=categories + [categories[0]],
        line=dict(color="#F39C12", width=1, dash="dot"),
        name="及格線 (40)",
        hoverinfo="skip",
    ))

    # 參考線：良好線 70
    fig.add_trace(go.Scatterpolar(
        r=[70] * (len(categories) + 1),
        theta=categories + [categories[0]],
        line=dict(color="#27AE60", width=1, dash="dot"),
        name="良好線 (70)",
        hoverinfo="skip",
    ))

    theme = _get_chart_colors()

    fig.update_layout(
        title=dict(
            text=f"{stock_name} 公司健康狀況",
            font=dict(size=18, color=theme["title"]),
            x=0.5,
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 20, 40, 60, 80, 100],
                tickfont=dict(size=10, color=theme["text"]),
                gridcolor=theme["grid"],
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color=theme["title"]),
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        margin=dict(t=60, b=60, l=60, r=60),
        height=420,
    )
    _apply_theme_layout(fig)

    return fig


def create_valuation_band_chart(
    stock_id: str,
    stock_name: str,
    daily_price_df: pd.DataFrame,
    financial_df: pd.DataFrame,
    latest_per_pbr: dict,
) -> go.Figure:
    """
    估值區間圖（歷史 P/E 範圍）
    顯示當前 PER 在歷史百分位中的位置，含 25th-75th 百分位帶
    """
    theme = _get_chart_colors()

    # ── 基本資料驗證 ─────────────────────────────────────────
    if daily_price_df is None or len(daily_price_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無股價資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    if financial_df is None or len(financial_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="暫無財務資料，無法計算本益比", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    if not latest_per_pbr or not latest_per_pbr.get("PER"):
        fig = go.Figure()
        fig.add_annotation(text="目前無法取得本益比資料", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    try:
        # ── Step 1: 整理每日股價 ──────────────────────────────
        price_df = daily_price_df.copy()
        price_df["date"] = pd.to_datetime(price_df["date"])
        price_df = price_df.sort_values("date").reset_index(drop=True)

        # 只取最近 2 年
        cutoff_2y = pd.Timestamp.now() - pd.Timedelta(days=730)
        price_df = price_df[price_df["date"] >= cutoff_2y]

        if len(price_df) == 0:
            fig = go.Figure()
            fig.add_annotation(text="近兩年無股價資料", x=0.5, y=0.5, showarrow=False)
            _apply_theme_layout(fig)
            return fig

        # ── Step 2: 從財務資料提取季度 EPS ──────────────────
        fin = financial_df.copy()
        fin["date"] = pd.to_datetime(fin["date"])

        # 找出 EPS 列（type 欄位包含 eps 或 每股盈餘）
        eps_keywords = ["eps", "每股盈餘", "earnings per share"]
        eps_mask = fin["type"].str.lower().str.contains(
            "|".join(eps_keywords), case=False, na=False
        )
        eps_df = fin[eps_mask].copy()

        if len(eps_df) == 0:
            fig = go.Figure()
            fig.add_annotation(text="無法從財務資料中提取 EPS", x=0.5, y=0.5, showarrow=False)
            _apply_theme_layout(fig)
            return fig

        # 每個日期取一列（同一日期可能有多列，取 value 最大的）
        eps_df = eps_df.groupby("date", as_index=False)["value"].max()
        eps_df = eps_df.sort_values("date").reset_index(drop=True)

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
            return fig

        per_series = pd.Series(per_values, index=per_dates)

        # ── Step 4: 計算百分位帶 ─────────────────────────────
        p25 = float(per_series.quantile(0.25))
        p75 = float(per_series.quantile(0.75))
        current_per = float(latest_per_pbr["PER"])

        # ── Step 5: 繪圖 ─────────────────────────────────────
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

        fig.update_layout(
            title=dict(
                text=f"{stock_name} 估值區間（歷史 P/E 範圍）",
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

        return fig

    except Exception:
        fig = go.Figure()
        fig.add_annotation(text="估值區間圖計算失敗", x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig
