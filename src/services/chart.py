"""
圖表生成器
用 Plotly 生成所有視覺化圖表

此模組為 re-export shim，實際功能拆分至：
- chart_stock.py：個股相關圖表（營收、股價、法人、估值等）
- chart_market.py：市場/ETF 相關圖表
"""

from src.services.chart_stock import (
    _get_chart_colors,
    _apply_theme_layout,
    create_revenue_pie_chart,
    create_revenue_trend_chart,
    create_revenue_treemap,
    create_price_chart,
    create_funnel_chart,
    create_comparison_radar,
    create_institutional_chart,
    create_health_snowflake,
    create_valuation_band_chart,
)

from src.services.chart_market import (
    create_price_area_chart,
)

__all__ = [
    # Shared utilities
    "_get_chart_colors",
    "_apply_theme_layout",
    # Stock charts
    "create_revenue_pie_chart",
    "create_revenue_trend_chart",
    "create_revenue_treemap",
    "create_price_chart",
    "create_funnel_chart",
    "create_comparison_radar",
    "create_institutional_chart",
    "create_health_snowflake",
    "create_valuation_band_chart",
    # Market/ETF charts
    "create_price_area_chart",
]
