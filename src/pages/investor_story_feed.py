"""
股識 Stock Explorer — C116: 每日故事 Feed
Personalized Daily Narrative Feed with AI Context.
Shows daily market stories and company narratives relevant to the
user's watchlist and browsing history.
"""

import streamlit as st
import logging

from src.pages.url_sync import navigate_to
from src.pages._router_base import _summary_card, _info_card, _section_title
from src.services.story_feed import (
    generate_daily_stories,
    generate_education_story,
    TYPE_EVENT,
    TYPE_SECTOR,
    TYPE_EDUCATION,
)

logger = logging.getLogger(__name__)

# ── Type emoji mapping ─────────────────────────────────────
TYPE_EMOJI = {
    TYPE_EVENT: "📅",
    TYPE_SECTOR: "📊",
    TYPE_EDUCATION: "📚",
}

# ── "Why this matters" explanations ────────────────────────
def _why_matters(story: dict) -> str:
    """Generate a one-line plain-language 'why this matters' explanation."""
    story_type = story.get("type", "")
    stock_id = story.get("story_id") or story.get("stock_id") or ""
    title = story.get("title", "")

    if story_type == TYPE_EVENT:
        if stock_id:
            return f"你關注的 {stock_id} 發生了「{title}」，可能影響持股決策。"
        return f"市場發生「{title}」，值得留意整體影響。"
    elif story_type == TYPE_SECTOR:
        return "產業走勢會連動到你的持股表現，了解大局有助於判斷個股。"
    elif story_type == TYPE_EDUCATION:
        return "搞懂這個指標，未來看財報時你會更有感。"
    return "每個故事都是理解市場的一步。"


# ── Page renderer ──────────────────────────────────────────

def render_investor_story_feed(data: dict, client):
    """
    每日故事 Feed 主頁面。

    Layout:
        1. Hero card: today's top story (highest severity / most recent)
        2. Story list: remaining stories as info cards with date badge + emoji
        3. "為何重要" section: one-liner per story
        4. Historian disclaimer at bottom
    """
    st.markdown("## 📰 每日故事 Feed")
    st.markdown("*根據你的關注清單，每天為你整理最值得知道的市場故事*")
    st.markdown("---")

    # ── Gather watchlist symbols ────────────────────────────
    from src.services.watchlist import load_watchlist
    try:
        watchlist_entries = load_watchlist("預設清單")
        watchlist_symbols = [e.get("stock_id", "") for e in watchlist_entries if e.get("stock_id")]
    except Exception as exc:
        logger.debug("story feed: failed to load watchlist: %s", exc)
        watchlist_symbols = []

    # ── Fetch stories ───────────────────────────────────────
    stories = []
    education_story = {}
    try:
        stories = generate_daily_stories(client, watchlist_symbols, max_stories=5)
    except Exception as exc:
        logger.warning("story_feed page: generate_daily_stories failed: %s", exc)

    try:
        education_story = generate_education_story(client)
    except Exception as exc:
        logger.warning("story_feed page: generate_education_story failed: %s", exc)

    # Append education story if we have room
    all_stories = list(stories)
    if education_story and education_story.get("title"):
        all_stories.append(education_story)

    # ── Render ──────────────────────────────────────────────
    if not all_stories:
        _info_card(
            "今日無新故事 🌙",
            "目前沒有偵測到你的關注股票有重大事件。\n\n"
            "試著瀏覽幾支股票，或到「分類瀏覽」探索更多標的，"
            "事件會在你瀏覽時被自動偵測並收錄到故事 Feed 中。",
            icon="💡",
        )
        return

    # Hero card: first (most important) story
    hero = all_stories[0]
    hero_emoji = TYPE_EMOJI.get(hero.get("type", TYPE_EVENT), "📌")
    hero_date = hero.get("date", "")
    hero_analogy = hero.get("analogy", "")
    hero_summary = hero.get("summary", "")

    hero_content = f"**{hero_emoji} {hero_date}**  \n\n{hero_summary}"
    if hero_analogy:
        hero_content += f"\n\n> 💡 {hero_analogy}"

    _summary_card(
        title=f"今日焦點：{hero.get('title', '市場動態')}",
        content=hero_content,
        icon="🔥",
    )

    # "為何重要" for hero
    st.caption(f"**為何重要：** {_why_matters(hero)}")
    st.markdown("")

    # Hero stock link button
    hero_stock = hero.get("stock_id")
    if hero_stock:
        if st.button(f"查看 {hero_stock} 名片", key="hero_view_btn"):
            navigate_to(page="名片", stock_id=hero_stock)

    st.markdown("---")

    # Remaining stories
    remaining = all_stories[1:]
    if remaining:
        _section_title("更多故事")

        for idx, story in enumerate(remaining):
            story_type = story.get("type", TYPE_EVENT)
            emoji = TYPE_EMOJI.get(story_type, "📌")
            date_badge = story.get("date", "")
            title = story.get("title", "")
            summary = story.get("summary", "")
            analogy = story.get("analogy", "")

            card_title = f"{emoji} [{date_badge}] {title}"
            card_content = summary
            if analogy:
                card_content += f"\n\n> 💡 {analogy}"

            _info_card(card_title, card_content, icon=emoji)

            # "Why this matters" one-liner
            st.caption(f"**為何重要：** {_why_matters(story)}")

            # Stock link button
            linked_stock = story.get("stock_id")
            if linked_stock:
                if st.button(
                    f"查看 {linked_stock} 名片",
                    key=f"story_view_{idx}_{linked_stock}",
                ):
                    navigate_to(page="名片", stock_id=linked_stock)

            st.markdown("")

    st.markdown("---")

    # ── Historian disclaimer ────────────────────────────────
    st.caption(
        "📜 *免責聲明：本頁面提供之故事及分析基於系統自動偵測之市場事件與公開數據，"
        "「歷史學家」敘事純屬教育用途，不構成任何投資建議。投資有風險，"
        "入市需謹慎，請依個人判斷做出投資決策。*"
    )
