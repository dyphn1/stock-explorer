"""
圖表生成器 — 健康/雷達相關圖表
用 Plotly 生成公司健康狀況雷達圖等視覺化圖表
"""

import plotly.graph_objects as go
from src.core.i18n import t
from src.services.chart_stock_financial import _get_chart_colors, _apply_theme_layout


def create_health_snowflake(
    stock_name: str,
    health_scores: dict,
    metric_values: dict | None = None,
    benchmark_scores: dict | None = None,
    benchmark_label: str = "",
) -> go.Figure:
    """
    公司健康狀況雷達圖（雪花圖）
    health_scores: {"獲利能力": 85, "成長性": 72, "財務健康": 90, "股利品質": 65, "估值合理性": 55}
    所有分數應為 0-100。
    metric_values: optional dict mapping dimension names to lists of metric labels,
        e.g. {"獲利能力": ["ROE 25.3%", "毛利率 66.2%"], ...}
    benchmark_scores: optional dict mapping dimension names to benchmark scores (0-100).
        When provided, renders a dashed ghost overlay on the radar chart.
    benchmark_label: label for the benchmark line in legend (default: "同業平均").
    """
    if not health_scores:
        fig = go.Figure()
        fig.add_annotation(text=t("chart.health.no_data"), x=0.5, y=0.5, showarrow=False)
        _apply_theme_layout(fig)
        return fig

    categories = list(health_scores.keys())
    values = [health_scores[c] for c in categories]

    # 根據各維度分數決定顏色
    def _score_color(score: float) -> str:
        if score >= 70:
            return "#27AE60"
        elif score >= 40:
            return "#3498DB"
        else:
            return "#E74C3C"

    # 整體平均分數決定主色
    avg_score = sum(values) / len(values) if values else 0
    main_color = _score_color(avg_score)

    # 每個維度的分數標籤（含顏色標記）
    r_with_labels = [f"{v:.0f}" for v in values]

    fig = go.Figure()

    # ── Benchmark overlay (ghost line) ──────────────────────
    # Rendered first so it appears behind the company scores.
    if benchmark_scores:
        bench_values = []
        bench_categories = []
        for c in categories:
            if c in benchmark_scores and benchmark_scores[c] is not None:
                bench_values.append(benchmark_scores[c])
                bench_categories.append(c)
            else:
                # Skip dimensions where benchmark data is missing
                pass

        if bench_values:
            # Close the polygon
            bv_closed = bench_values + [bench_values[0]]
            bc_closed = bench_categories + [bench_categories[0]]
            label = benchmark_label or t("comparison.industry_avg")

            fig.add_trace(go.Scatterpolar(
                r=bv_closed,
                theta=bc_closed,
                fill="none",
                line=dict(color="#ECF0F1", width=2, dash="dash"),
                name=label,
                text=[
                    t("chart.health.benchmark_tooltip", label=label, category=c, score=v)
                    for c, v in zip(bench_categories, bench_values)
                ],
                hovertemplate="%{text}<extra></extra>",
            ))

    # Outer line (actual scores per dimension)
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Close the polygon
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(52, 152, 219, 0.15)",
        line=dict(color=main_color, width=2.5),
        name=t("chart.health.current_score"),
        text=(
            (
                t("chart.health.score_tooltip", category=c, score=v)
                + ("<br>" + "<br>".join(f"  • {m}" for m in metric_values[c]) if metric_values and c in metric_values and metric_values[c] else "")
            )
            for c, v in zip(categories, values)
        ),
        hovertemplate="%{text}<extra></extra>",
    ))

    # Reference line: pass line 40
    fig.add_trace(go.Scatterpolar(
        r=[40] * (len(categories) + 1),
        theta=categories + [categories[0]],
        line=dict(color="#3498DB", width=1, dash="dot"),
        name=t("chart.health.pass_line"),
        hoverinfo="skip",
    ))

    # Reference line: good line 70
    fig.add_trace(go.Scatterpolar(
        r=[70] * (len(categories) + 1),
        theta=categories + [categories[0]],
        line=dict(color="#27AE60", width=1, dash="dot"),
        name=t("chart.health.good_line"),
        hoverinfo="skip",
    ))

    theme = _get_chart_colors()

    fig.update_layout(
        title=dict(
            text=t("chart.health.title", stock_name=stock_name)
                 + " <sub style='font-size:0.7rem;color:#7F8C8D;'>💡 點擊各維度分數旁圖示查看名詞解釋</sub>",
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
