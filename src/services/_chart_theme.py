"""
Chart theme utilities — shared color/layout helpers for all chart modules.
"""

import plotly.graph_objects as go


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

def get_chart_colors() -> dict:
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


def apply_theme_layout(fig: go.Figure) -> go.Figure:
    """Apply theme-aware layout defaults to a Plotly figure.

    Sets transparent backgrounds (so Streamlit theme is inherited),
    and applies theme-aware font / grid / axis colors that work in
    both light and dark mode.
    """
    colors = get_chart_colors()

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
    annotations = fig.layout.annotations
    if annotations:
        for ann in annotations:
            if ann.font and ann.font.color is None:
                ann.font.color = colors["muted"]

    return fig
