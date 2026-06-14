"""Business card section: summary sections (takeaways, one-liner, news).

Hero functions (_render_story_card, _render_header) moved to _summary_hero.py
to keep file sizes under the 500-line threshold. Re-exported here for backward
compatibility.
"""
import streamlit as st
from src.services.analogy_engine import get_one_liner
from src.services.key_takeaways import generate_key_takeaways
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.pages._router_base import _info_card, _summary_card, _confidence_badge

# ── Re-export hero functions from _summary_hero for backward compatibility ──
from src.pages.business_card._sections._summary_hero import (
    _render_story_card,
    _render_header,
)


def _render_takeaways(data: dict, client) -> None:
    """C37 Key Takeaways section."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]

    # 📋 重點摘要 (C37: Key Takeaways)
    takeaways = generate_key_takeaways(
        stock_id=stock_id,
        stock_name=stock_name,
        industry=industry,
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        monthly_revenue=monthly_revenue,
        financial_df=financial,
    )
    if takeaways:
        takeaways_text = "\\n\\n".join(f"• {t}" for t in takeaways)
        _summary_card("重點摘要", takeaways_text, "📋")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · 信心指標反映資料完整度，非AI預測確定性")


def _render_one_liner(data: dict, client) -> None:
    """One-liner + rotating company facts tip card."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    # 一句話定位
    one_liner = get_one_liner(stock_id, stock_name, industry)
    _info_card("一句話定位", one_liner, "💡")
    # C204: confidence badge
    st.caption(f"{_confidence_badge(0.9)} · 信心指標反映資料完整度，非AI預測確定性")

    # 💡 你知道嗎？ Company facts tip card
    facts = get_company_facts(stock_id)
    if facts:
        # Rotate facts on each rerun using session_state
        fact_key = f"_fact_idx_{stock_id}"
        if fact_key not in st.session_state:
            st.session_state[fact_key] = 0
        idx = st.session_state[fact_key] % len(facts)
        st.session_state[fact_key] = (idx + 1) % len(facts)
        current_fact = facts[idx]
        _info_card("你知道嗎？", current_fact, "💡")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · 信心指標反映資料完整度，非AI預測確定性")


def _render_news(data: dict, client) -> None:
    """Recent news with impact level badges."""
    news = data["news"]
    stock_name = data["stock_name"]

    # 近期動態（白話摘要版）
    st.markdown("### 📊 近期動態")
    if len(news) > 0:
        for i in range(min(3, len(news))):
            news_item = news.iloc[i]
            title = news_item['title']
            source = news_item.get('source', '未知')
            date_str = str(news_item.get('date', ''))[:10]
            impact = get_news_impact_level(title)
            summary = summarize_news(title, stock_name)

            impact_class = {"high": "🔴 重大", "medium": "🟡 注意", "low": "🟢 參考"}[impact]

            _info_card(f"{impact_class} {title}\n\n{summary}\n\n📡 {source} ｜ {date_str}", "", "📰")
    else:
        st.info("近期無重大新聞")
