"""
股識 Stock Explorer — C116: 每日故事 Feed
Personalized Daily Narrative Feed with AI Context.
Shows daily market stories and company narratives relevant to the
user's watchlist and browsing history.
"""

import streamlit as st
import logging

from src.core.i18n import t
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
            return t("investor_story.why_matters_event_stock", stock_id=stock_id, title=title)
        return t("investor_story.why_matters_event", title=title)
    elif story_type == TYPE_SECTOR:
        return t("investor_story.why_matters_sector")
    elif story_type == TYPE_EDUCATION:
        return t("investor_story.why_matters_education")
    return t("investor_story.why_matters_default")


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
    st.markdown(f"## 📰 {t('investor_story.page_title')}")
    st.markdown(f"*{t('investor_story.page_subtitle')}*")
    st.markdown("---")

    # ── Gather watchlist symbols ────────────────────────────
    from src.services.watchlist import load_watchlist
    try:
        watchlist_entries = load_watchlist(t("investor_story.default_watchlist"))
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
            t("investor_story.no_stories_title"),
            t("investor_story.no_stories_detail"),
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
        title=f"{t('investor_story.hero_prefix')}{hero.get('title', t('investor_story.hero_default'))}",
        content=hero_content,
        icon="🔥",
    )

    # "為何重要" for hero
    st.caption(f"**{t('investor_story.why_matters_label')}** {_why_matters(hero)}")
    st.markdown("")

    # Hero stock link button
    hero_stock = hero.get("stock_id")
    if hero_stock:
        if st.button(t("investor_story.view_card", stock_id=hero_stock), key="hero_view_btn"):
            navigate_to(page=t("investor_story.card_page"), stock_id=hero_stock)

    st.markdown("---")

    # Remaining stories
    remaining = all_stories[1:]
    if remaining:
        _section_title(t("investor_story.more_stories"))

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
            st.caption(f"**{t('investor_story.why_matters_label')}** {_why_matters(story)}")

            # Stock link button
            linked_stock = story.get("stock_id")
            if linked_stock:
                if st.button(
                    t("investor_story.view_card", stock_id=linked_stock),
                    key=f"story_view_{idx}_{linked_stock}",
                ):
                    navigate_to(page=t("investor_story.card_page"), stock_id=linked_stock)

            st.markdown("")

    st.markdown("---")

    # ── Historian disclaimer ────────────────────────────────
    st.caption(t("investor_story.disclaimer"))
