"""
Story Timeline page (C28) — Full Company Story Timeline MVP.

Composes a scrollable timeline from detected events, case studies,
and company milestones, enriched with historian-style interpretations.

This page is accessible from the Business Card page via the "更多分析" expander.

i18n: all user-facing strings use t() function. The story_arc_detector
service returns i18n keys; this page resolves them via t().
"""

from __future__ import annotations

import streamlit as st

from src.core.i18n import t
from src.pages._router_base import _section_title, _summary_card, _info_card
from src.services.timeline_service import get_timeline, TimelineEntry
from src.services.story_arc_detector import detect_arcs, get_arc_legend, ArcLabel


# ── Severity → border color ───────────────────────────────

_SEVERITY_COLORS = {
    "high": "#E74C3C",
    "medium": "#E67E22",
    "low": "#27AE60",
}


def _severity_color(severity: str) -> str:
    return _SEVERITY_COLORS.get(severity, "#3498DB")


# ── Arc badge renderer ─────────────────────────────────────

def _render_arc_badge(arc: ArcLabel) -> None:
    """Render an arc label badge at a transition point."""
    emoji = arc.get("arc_emoji", "")
    arc_key = arc.get("arc_key", "")
    desc_key = arc.get("arc_description_key", "")
    count = arc.get("event_count", 0)
    bucket_start = arc.get("bucket_start", "")
    bucket_end = arc.get("bucket_end", "")

    # Resolve display text via i18n
    label = t(f"story_arc.{arc_key}") if arc_key else ""
    desc = t(desc_key) if desc_key else ""

    # Determine badge color based on arc type
    _arc_colors = {
        "growth": "#27AE60",
        "decline": "#E74C3C",
        "volatile": "#E67E22",
        "recovery": "#3498DB",
    }
    color = _arc_colors.get(arc_key, "#3498DB")

    badge_title = f"{emoji} {label}"
    badge_content = (
        f"{desc}\n\n"
        f"📅 {bucket_start} ～ {bucket_end}\n\n"
        f"📌 {t('story_arc.badge_events', count=count)}"
    )
    _info_card(
        title=badge_title,
        content=badge_content,
        icon="",
    )
    # Add a colored left border via markdown spacer
    st.markdown(
        f'<div style="border-left: 4px solid {color}; padding-left: 0.5em; margin: 0.5em 0;">'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_arc_legend() -> None:
    """Render arc legend section."""
    _section_title(t("story_arc.legend_title"))
    legend = get_arc_legend()
    cols = st.columns(4)
    for i, item in enumerate(legend):
        with cols[i]:
            label = t(item["label_key"])
            desc = t(item["desc_key"])
            emoji = item["emoji"]
            st.markdown(f"**{emoji} {label}**")
            st.caption(desc)


def _render_timeline_card(entry: TimelineEntry, index: int) -> None:
    """Render a single timeline entry as a styled card.

    Uses _summary_card with severity-based border color.
    """
    date = entry.get("date", t("status.data_missing"))
    icon = entry.get("icon", "📌")
    title = entry.get("title", "")
    summary = entry.get("summary", "")
    interpretation = entry.get("interpretation", "")
    severity = entry.get("severity", "low")
    source = entry.get("source", "")
    count = entry.get("count", 0)

    # Build card content
    content_parts = [f"**{title}**", ""]
    if summary:
        content_parts.append(summary)
        content_parts.append("")
    if interpretation:
        content_parts.append(f"💡 {interpretation}")
        content_parts.append("")
    if count and count > 1:
        content_parts.append(f"📌 {t('story_arc.badge_events', count=count)}")
        content_parts.append("")

    # Source badge — use i18n keys where available
    _source_map = {
        "detected": f"🔍 {t('scenario.source_detected')}",
        "case_study": f"📚 {t('scenario.source_case_study')}",
        "milestone": f"⭐ {t('scenario.source_milestone')}",
    }
    source_label = _source_map.get(source, "")
    if source_label:
        content_parts.append(f"*{source_label} · {date}*")

    content = "\n\n".join(content_parts)

    _summary_card(
        title=f"{icon} {date}",
        content=content,
        icon="",
        border_color=_severity_color(severity),
    )


# ── Main page renderer ─────────────────────────────────────

def render_story_timeline_page(data: dict, client) -> None:
    """C28 Story Timeline — full company story timeline page.

    Shows a scrollable horizontal timeline with event cards,
    color-coded by severity, enriched with interpretations.

    Args:
        data: Standard page data dict with stock_id, stock_name, etc.
        client: FinMindClient instance.
    """
    stock_id = data["stock_id"]
    stock_name = data.get("stock_name", "")

    # Page header
    display_name = f"{stock_name} ({stock_id})" if stock_name else stock_id
    _section_title(f"📅 {t('page.story_timeline')} — {display_name}")

    st.markdown(f"*{t('story_arc.section_subtitle')}*")
    st.markdown("")

    # ── Lookback selector ───────────────────────────────────
    col_sel, _ = st.columns([1, 3])
    with col_sel:
        lookback_options = {
            t("timeline.label_1y"): 365,
            t("timeline.label_3y"): 1095,
            t("timeline.label_5y"): 1825,
            t("timeline.label_all"): 3650,
        }
        selected_label = st.selectbox(
            t("scenario.time_range"),
            list(lookback_options.keys()),
            index=0,
            key=f"timeline_lookback_{stock_id}",
        )
    lookback_days = lookback_options.get(selected_label, 365)

    st.markdown("")

    # ── Fetch timeline ──────────────────────────────────────
    with st.spinner(t("status.loading")):
        try:
            entries = get_timeline(stock_id, lookback_days=lookback_days)
        except Exception as exc:
            st.error(f"{t('error.no_data')}: {exc}")
            return

    # ── Empty state ─────────────────────────────────────────
    if not entries:
        _info_card(
            title=t("scenario.no_timeline_data"),
            content=(
                f"{t('scenario.no_timeline_detail', range=selected_label, name=display_name)}\n\n"
                f"{t('scenario.no_timeline_sources')}\n\n"
                f"• **{t('scenario.no_timeline_auto')}**\n\n"
                f"• **{t('scenario.no_timeline_case')}**\n\n"
                f"• **{t('scenario.no_timeline_milestone')}**\n\n"
                f"💡 {t('scenario.no_timeline_tip')}"
            ),
            icon="📭",
        )
        return

    # ── Timeline stats ──────────────────────────────────────
    st.caption(t("scenario.timeline_count", count=len(entries), range=selected_label))
    st.markdown("---")

    # ── Arc detection ────────────────────────────────────────
    arcs = detect_arcs(entries)
    if arcs:
        _section_title(t("story_arc.section_title"))
        st.markdown(f"*{t('story_arc.section_subtitle')}*")
        st.markdown("")
        for arc in arcs:
            _render_arc_badge(arc)
        st.markdown("---")

    # ── Timeline display ────────────────────────────────────
    for idx, entry in enumerate(entries):
        _render_timeline_card(entry, idx)
        if idx < len(entries) - 1:
            st.markdown("")

    st.markdown("---")

    # ── Severity legend ─────────────────────────────────────
    _section_title(t("scenario.legend_title"))
    legend_cols = st.columns(3)
    with legend_cols[0]:
        _info_card(t("scenario.legend_major"), t("scenario.legend_major_desc"), "⚠️")
    with legend_cols[1]:
        _info_card(t("scenario.legend_important"), t("scenario.legend_important_desc"), "📌")
    with legend_cols[2]:
        _info_card(t("scenario.legend_reference"), t("scenario.legend_reference_desc"), "💡")

    # ── Arc legend ───────────────────────────────────────────
    if arcs:
        _render_arc_legend()
        st.markdown("---")

    # ── Historian disclaimer ────────────────────────────────
    st.markdown("---")
    st.caption(t("disclaimer.historical"))
