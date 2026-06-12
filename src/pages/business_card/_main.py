"""Business card main orchestrator."""
import streamlit as st
import pandas as pd
from datetime import datetime, date

from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_pbr_analogy,
)
from src.services.key_takeaways import generate_key_takeaways
from src.services.delta_engine import compute_recent_deltas
from src.services.health_scoring import compute_health_scores, get_health_summary
from src.services.risk_analyzer import assess_risk
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.services.watchlist import (
    is_in_watchlist,
    is_in_any_list,
    get_lists_for_stock,
    add_to_watchlist,
    remove_from_all_lists,
    remove_from_watchlist,
    create_list,
    list_names,
)
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.url_sync import navigate_to

from src.pages.business_card._sections import (
    _render_header,
    _render_story_card,
    _render_takeaways,
    _render_deltas,
    _render_health,
    _render_risk,
    _render_one_liner,
    _render_key_metrics,
    _render_dividend,
    _render_revenue_breakdown,
    _render_revenue_trend,
    _render_valuation,
    _render_compare_stories,
    _render_news,
    _render_read_next,
    _render_share_section,
    _render_footer,
)


def _render_business_card(data: dict, client):
    """公司名片主頁（M1）— orchestrator"""
    # ── Data extraction ──
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]
    news = data["news"]
    extra_metrics = data["extra_metrics"]

    # ── Section dispatch ──
    _render_header(data, client)
    _render_story_card(data, client)
    _render_takeaways(data, client)
    _render_deltas(data, client)
    _render_health(data, client)
    _render_risk(data, client)
    _render_one_liner(data, client)
    _render_key_metrics(data, client)
    _render_dividend(data, client)
    _render_revenue_breakdown(data, client)
    _render_revenue_trend(data, client)
    _render_valuation(data, client)
    _render_compare_stories(data, client)
    _render_news(data, client)
    _render_read_next(data, client)
    _render_share_section(data, client)
    _render_footer(data, client)
