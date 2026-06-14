"""
圖表生成器 — 個股相關圖表（re-export shim）

此模組為 re-export shim，實際功能拆分至：
- chart_stock_financial.py：營收、股價、法人、雷達等財務圖表
- chart_stock_health.py：公司健康狀況雷達圖（雪花圖）
- chart_stock_valuation.py：估值區間圖
"""

from src.services.chart_stock_financial import (
    _get_chart_colors,
    _apply_theme_layout,
    create_revenue_pie_chart,
    create_revenue_trend_chart,
    create_revenue_treemap,
    create_price_chart,
    create_funnel_chart,
    create_comparison_radar,
    create_institutional_chart,
)

from src.services.chart_stock_health import (
    create_health_snowflake,
)

from src.services.chart_stock_valuation import (
    create_valuation_band_chart,
)

__all__ = [
    # Shared utilities
    "_get_chart_colors",
    "_apply_theme_layout",
    # Financial charts
    "create_revenue_pie_chart",
    "create_revenue_trend_chart",
    "create_revenue_treemap",
    "create_price_chart",
    "create_funnel_chart",
    "create_comparison_radar",
    "create_institutional_chart",
    # Health charts
    "create_health_snowflake",
    # Valuation charts
    "create_valuation_band_chart",
]
