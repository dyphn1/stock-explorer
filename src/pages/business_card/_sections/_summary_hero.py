"""Business card section: hero components (story card, header).

Moved from _summary.py to keep file sizes under the 500-line threshold.
"""
import streamlit as st
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
from src.services.health_scoring import compute_health_scores
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
from src.pages._router_base import _白话_card, _info_card, _summary_card, _explain_button, _glossary_tooltip, _confidence_badge, _section_title_with_read_time
from src.services import glossary_service
from src.core.i18n import t
from src.services.benchmarks import (
    get_industry_benchmarks,
    fetch_benchmark_health_scores,
)



def _render_story_card(data: dict, client) -> None:
    """C48 Company Story Card — 30-second visual summary.

    A PPT-style hero card at the top of the business card page showing:
    - Company name + industry
    - One-liner description
    - 3 key metric highlights (bold numbers with plain-language)
    - Health score indicator
    - Rotating "Did You Know?" fact
    """
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]

    # ── One-liner ──
    one_liner = get_one_liner(stock_id, stock_name, industry)

    # ── Pick top 3 most notable metrics ──
    metrics = []

    # Revenue (monthly)
    if len(monthly_revenue) > 0:
        rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
        yoy = extra_metrics.get("revenue_yoy")
        yoy_analogy = get_yoy_analogy(yoy) if yoy is not None else ""
        metrics.append((t("summary_hero.revenue"), f"{rev:,.0f} 億", get_revenue_analogy(rev, industry) + (f" ｜ {yoy_analogy}" if yoy_analogy else "")))

    # PER
    if latest_per_pbr and latest_per_pbr.get("PER") is not None:
        per = latest_per_pbr["PER"]
        metrics.append((t("summary_hero.per"), f"{per:.1f}", get_per_analogy(per)))

    # Gross margin
    if extra_metrics.get("gross_margin") is not None:
        gm = extra_metrics["gross_margin"]
        metrics.append((t("summary_hero.gross_margin"), f"{gm:.1f}%", get_gross_margin_analogy(gm)))

    # Dividend yield
    if latest_per_pbr and latest_per_pbr.get("dividend_yield") is not None:
        dy = latest_per_pbr["dividend_yield"]
        metrics.append((t("summary_hero.dividend_yield"), f"{dy:.2f}%", get_dividend_analogy(dy)))

    # ROE
    if extra_metrics.get("roe") is not None:
        roe = extra_metrics["roe"]
        metrics.append((t("summary_hero.roe"), f"{roe:.1f}%", get_roe_analogy(roe)))

    # PBR
    if latest_per_pbr and latest_per_pbr.get("PBR") is not None:
        pbr = latest_per_pbr["PBR"]
        metrics.append((t("summary_hero.pbr"), f"{pbr:.2f}", get_pbr_analogy(pbr)))

    # Take top 3
    top_metrics = metrics[:3]

    # ── Health score indicator ──
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=data["financial"],
        monthly_revenue=monthly_revenue,
    )
    overall_health = None
    health_label = "—"
    if health_scores:
        overall_health = sum(health_scores.values()) / len(health_scores)
        if overall_health >= 70:
            health_label = t("summary_hero.health_good")
        elif overall_health >= 40:
            health_label = t("summary_hero.health_fair")
        else:
            health_label = t("summary_hero.health_poor")

    # ── Did You Know? fact ──
    facts = get_company_facts(stock_id)
    fact_text = ""
    if facts:
        fact_key = f"_story_fact_idx_{stock_id}"
        if fact_key not in st.session_state:
            st.session_state[fact_key] = 0
        idx = st.session_state[fact_key] % len(facts)
        st.session_state[fact_key] = (idx + 1) % len(facts)
        fact_text = facts[idx]

    # ── Build the story card using shared components ──
    # Company name + industry header
    st.markdown(f"### {stock_name} `{stock_id}`")
    st.markdown(f"*{industry}*")

    # One-liner
    _info_card(t("business_card.summary_hero.one_liner_title"), one_liner, "💡")
    # C204: confidence badge for the one-liner explanation
    st.caption(f"{_confidence_badge(0.9)} · {t('summary_hero.confidence_note')}")

    # Key metrics row — use _白话_card for each + 💡 explain button + glossary tooltip
    # C170: beginner mode → more prominent glossary indicators
    _is_beginner = st.session_state.get("simple_mode", False) or st.session_state.get("user_experience_level", "beginner") == "beginner"
    if top_metrics:
        cols = st.columns(len(top_metrics))
        for col, (label, value, analogy) in zip(cols, top_metrics):
            with col:
                _白话_card(label, value, analogy)
                _explain_button(
                    metric_name=label,
                    metric_value=value,
                    key_prefix=f"story_{stock_id}",
                    source_label="📊 FinMind" if "revenue" in label else t("summary_hero.system_estimate"),
                )
                # C170: Glossary tooltip — resolve display label to glossary key
                _gkey = glossary_service.resolve_term_key(label.split(" (")[0].strip())
                if _gkey:
                    _glossary_tooltip(_gkey, glossary_service, beginner=_is_beginner)

    # Health score
    if overall_health is not None:
        if overall_health >= 70:
            health_border = "#27AE60"
        elif overall_health >= 40:
            health_border = "#E67E22"
        else:
            health_border = "#E74C3C"
        _summary_card("整體健康度", f"{overall_health:.0f}/100 {health_label}", "🏥", border_color=health_border)
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t('summary_hero.confidence_note')}")

    # ── C14: vs 同業 comparison ──
    if health_scores:
        industry_for_benchmark = data.get("industry", "")
        stock_id_for_benchmark = data.get("stock_id", "")
        if industry_for_benchmark and industry_for_benchmark in get_industry_benchmarks():
            bench_id, bench_name = get_industry_benchmarks()[industry_for_benchmark]
            if bench_id != stock_id_for_benchmark:
                bench_scores = fetch_benchmark_health_scores(
                    client, industry_for_benchmark, stock_id_for_benchmark
                )
                if bench_scores:
                    bench_overall = sum(bench_scores.values()) / len(bench_scores)
                    diff = overall_health - bench_overall
                    if abs(diff) < 2:
                        vs_emoji = "➡️"
                        vs_text = t("summary_hero.vs_unchanged", name=bench_name)
                    elif diff > 0:
                        vs_emoji = "⬆️"
                        vs_text = t("summary_hero.vs_above", name=bench_name, diff=abs(diff))
                    else:
                        vs_emoji = "⬇️"
                        vs_text = t("summary_hero.vs_below", name=bench_name, diff=abs(diff))

                    vs_content = t("summary_hero.vs_content", health=overall_health, bench_name=bench_name, bench_overall=bench_overall) + f"\n\n{vs_emoji} {vs_text}"
                    _info_card(t("business_card.summary_hero.vs_industry_title"), vs_content, "🏭")
                    # C204: confidence badge
                    st.caption(f"{_confidence_badge(0.9)} · {t('summary_hero.confidence_note')}")

    # Did You Know?
    if fact_text:
        _info_card(t("business_card.summary_hero.did_you_know_title"), fact_text, "🤔")
        # C204: confidence badge
        st.caption(f"{_confidence_badge(0.9)} · {t('summary_hero.confidence_note')}")


def _render_header(data: dict, client) -> None:
    """Watchlist header with stock name, price, watchlist buttons."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"**{stock_name}** `{stock_id}` ｜ {industry}")
    with col2:
        if latest_price:
            price = latest_price["close"]
            change = latest_price["change"]
            sign = "+" if change >= 0 else ""
            st.markdown(f"**{price:,.0f}** `{sign}{change:,.0f}`")
    with col3:
        # Watchlist buttons
        watchlist_lists = get_lists_for_stock(stock_id)
        if watchlist_lists:
            # Stock is in at least one list
            st.markdown(t("summary_hero.in_lists", lists=", ".join(watchlist_lists)))
            if st.button(t("business_card.watchlist.remove_all"), key=f"unwatch_{stock_id}", use_container_width=True):
                if remove_from_all_lists(stock_id):
                    st.toast(t("business_card.watchlist.removed"))
                else:
                    st.error(t("business_card.watchlist.remove_failed"))
                st.rerun()
        else:
            # Stock is not in any list
            if st.button(t("business_card.watchlist.add_to"), key=f"watch_{stock_id}", use_container_width=True):
                # Show popup to select list
                st.session_state[f"show_watchlist_popup_{stock_id}"] = True
                st.rerun()

    # Popup for adding to watchlist
    if st.session_state.get(f"show_watchlist_popup_{stock_id}", False):
        with st.popover(t("summary_hero.select_list"), use_container_width=True):
            # Get existing list names
            existing_lists = list_names()
            tab1, tab2 = st.tabs([t("summary_hero.select_existing_list"), t("summary_hero.create_new_list")])
            target_list = None

            with tab1:
                if existing_lists:
                    selected = st.selectbox(
                        t("summary_hero.choose_list"),
                        options=existing_lists,
                        key=f"select_existing_{stock_id}",
                    )
                    if selected:
                        target_list = selected
                else:
                    st.info(t("business_card.watchlist.name_required"))

            with tab2:
                new_name = st.text_input(
                    t("summary_hero.new_list_name"),
                    placeholder=t("summary_hero.new_list_placeholder"),
                    key=f"new_name_{stock_id}",
                )
                if st.button(t("business_card.watchlist.create_button"), key=f"create_btn_{stock_id}"):
                    if new_name:
                        if create_list(new_name):
                            st.success(t("summary_hero.list_created", name=new_name))
                            target_list = new_name
                        else:
                            st.error(t("business_card.watchlist.create_failed"))
                    else:
                        st.error(t("business_card.watchlist.name_required"))

            # Add stock button
            if st.button(t("business_card.watchlist.add_button"), key=f"add_stock_btn_{stock_id}", type="primary"):
                if target_list:
                    success = add_to_watchlist(
                        stock_id=stock_id,
                        name=stock_name,
                        alert_above=None,
                        alert_below=None,
                        industry_category=industry,
                        list_name=target_list,
                    )
                    if success:
                        st.session_state[f"show_watchlist_popup_{stock_id}"] = False
                        st.toast(ft("summary_hero.added_to_list", name=target_list))
                        st.rerun()
                    else:
                        st.error(t("business_card.watchlist.add_failed"))
                else:
                    st.error(t("business_card.watchlist.select_required"))

    st.markdown("---")
