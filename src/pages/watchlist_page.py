"""
關注列表頁 — 顯示使用者關注的股票與 ETF
提供摘要卡片、價格列表、警示狀態與移除功能
支援多個命名清單
"""

import streamlit as st
from src.core.i18n import t
from src.data.finmind_client import FinMindClient
from src.pages.url_sync import navigate_to
from src.services.watchlist import (
    load_watchlist,
    remove_from_watchlist,
    get_watchlist_summary,
    update_alerts,
    create_list,
    delete_list,
    rename_list,
    list_names,
)
from src.pages._router_base import _白话_card, _info_card

def _render_watchlist_page(client: FinMindClient):
    """關注列表主頁"""
    st.markdown(f"## 📋 {t('watchlist.title')}")
    st.markdown(t("watchlist.subtitle"))
    st.markdown("---\n")

    # --- List Management Section ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### {t('watchlist.list_selection')}")
    with col2:
        if st.button(t("watchlist.new_list_btn"), key="btn_new_list", use_container_width=True):
            st.session_state["show_new_list_popup"] = True

    # Popup for creating new list
    if st.session_state.get("show_new_list_popup", False):
        with st.popover(t("watchlist.new_list_popover"), use_container_width=True):
            with st.form("new_list_form"):
                new_list_name = st.text_input(t("watchlist.list_name_input"), placeholder=t("watchlist.list_name_placeholder"))
                submitted = st.form_submit_button(t("watchlist.create_list_btn"))
                if submitted and new_list_name:
                    if create_list(new_list_name):
                        st.success(t("watchlist.list_created", name=new_list_name))
                        st.session_state["show_new_list_popup"] = False
                        st.rerun()
                    else:
                        st.error(t("watchlist.list_create_failed"))
                elif submitted:
                    st.error(t("watchlist.list_name_required"))

    # Get list of list names
    list_name_options = list_names()
    # Ensure there's always at least one list (預設清單)
    if not list_name_options:
        # If no lists exist, create default list
        create_list(t("watchlist.default_list_name"))
        list_name_options = [t("watchlist.default_list_name")]

    # Let user select a list to view/edit
    selected_list = st.selectbox(
        t("watchlist.select_list_label"),
        options=list_name_options,
        index=0 if list_name_options else 0,
        key="selected_watchlist",
    )

    st.markdown("---\n")

    # If no lists (should not happen because we ensured at least one)
    if not selected_list:
        st.warning(t("watchlist.no_lists"))
        return

    # Load watchlist for selected list
    entries = load_watchlist(selected_list)
    total = len(entries)
    stocks_count = sum(1 for e in entries if e.get("type") == "stock")
    etfs_count = sum(1 for e in entries if e.get("type") == "etf")

    # ── Summary Cards ──────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        _白话_card(t("watchlist.total_label"), str(total), t("watchlist.total_help"))
    with col2:
        _白话_card(t("watchlist.stocks_label"), str(stocks_count), t("watchlist.stocks_help"))
    with col3:
        _白话_card(t("watchlist.etfs_label"), str(etfs_count), t("watchlist.etfs_help"))

    st.markdown("---\n")

    # ── Empty State ────────────────────────────────────────────
    if total == 0:
        _info_card(
            t("watchlist.empty_title"),
            t("watchlist.empty_message"),
            "📌",
        )
        # Still show list management buttons for the empty list
        # We'll show rename/delete buttons below
        pass
    else:
        # ── Fetch Latest Prices ────────────────────────────────────
        with st.spinner(t("watchlist.loading_prices")):
            try:
                summary = get_watchlist_summary(client, selected_list)
            except Exception as e:
                st.error(t("watchlist.price_error", error=e))
                summary = []

        if not summary:
            st.warning(t("watchlist.price_unavailable"))
            # Still show list management
        else:
            # ── Watchlist Table ────────────────────────────────────────
            st.markdown(f"### 📈 {t('watchlist.price_overview')}")

            for item in summary:
                stock_id = item["stock_id"]
                name = item["name"]
                etf_type = item.get("type", "stock")
                latest_price = item.get("latest_price")
                change = item.get("change")
                alert_above = item.get("alert_above")
                alert_below = item.get("alert_below")
                alert_triggered = item.get("alert_triggered", False)

                # Type badge
                if etf_type == "etf":
                    badge = f'<span style="background:#27AE60;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-right:0.4rem;">{t("watchlist.type_etf_badge")}</span>'
                else:
                    badge = '<span style="background:#3498DB;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-right:0.4rem;">{t("watchlist.type_stock_badge")}</span>'

                # Price and change formatting
                if latest_price is not None:
                    price_str = f"{latest_price:,.2f}"
                    if change is not None:
                        sign = "+" if change >= 0 else ""
                        # 台股慣例：紅漲綠跌
                        color = "#E74C3C" if change >= 0 else "#27AE60"
                        change_str = f'<span style="color:{color};font-weight:600;">{sign}{change:,.2f}</span>'
                    else:
                        change_str = '<span style="color:#7F8C8D;">—</span>'
                else:
                    price_str = "—"
                    change_str = '<span style="color:#7F8C8D;">—</span>'

                # Alert info
                alert_parts = []
                if alert_above is not None:
                    alert_parts.append(t("watchlist.alert_above", price=f"{alert_above:,.2f}"))
                if alert_below is not None:
                    alert_parts.append(t("watchlist.alert_below", price=f"{alert_below:,.2f}"))

                # Alert triggered indicator
                if alert_triggered:
                    alert_badge = f'<span style="background:#E74C3C;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-left:0.4rem;">{t("watchlist.alert_triggered")}</span>'
                else:
                    alert_badge = ""

                # Card-style row
                alert_str = t("watchlist.alert_separator").join(alert_parts) if alert_parts else t("watchlist.alert_unset")
                alert_triggered_str = f" {t('watchlist.alert_triggered')}" if alert_triggered else ""
                if change is not None:
                    change_sign = "+" if change >= 0 else ""
                    change_display = f"{change_sign}{change:,.2f}"
                else:
                    change_display = "—"
                _info_card(
                    f"{name} ({stock_id}){alert_triggered_str}",
                    t("watchlist.card_content", price=price_str, change=change_display, alert=alert_str),
                    "📈" if etf_type != "etf" else "🏷️",
                )

                # Action buttons row
                col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
                with col1:
                    if st.button(t("watchlist.btn_view_card"), key=f"wl_card_{stock_id}_{selected_list}", use_container_width=True):
                        navigate_to(page="名片", stock_id=stock_id)
                with col2:
                    if st.button(t("watchlist.btn_remove"), key=f"wl_remove_{stock_id}_{selected_list}", use_container_width=True):
                        if remove_from_watchlist(stock_id, selected_list):
                            st.toast(t("watchlist.removed_toast"))
                            st.rerun()
                        else:
                            st.error(t("watchlist.remove_failed"))
                with col3:
                    with st.popover(t("watchlist.set_alert"), key=f"wl_alert_{stock_id}_{selected_list}"):
                        st.markdown(f"**{name}** ({stock_id})")
                        st.markdown("---\n")

                        # Show current alert values
                        current_above = alert_above if alert_above is not None else 0.0
                        current_below = alert_below if alert_below is not None else 0.0

                        new_above = st.number_input(
                            t("watchlist.alert_upper_label"),
                            min_value=0.0,
                            value=current_above,
                            step=0.5,
                            key=f"wl_above_{stock_id}_{selected_list}",
                        )
                        new_below = st.number_input(
                            t("watchlist.alert_lower_label"),
                            min_value=0.0,
                            value=current_below,
                            step=0.5,
                            key=f"wl_below_{stock_id}_{selected_list}",
                        )

                        save_col, clear_col = st.columns(2)
                        with save_col:
                            if st.button(
                                t("watchlist.btn_save"), key=f"wl_save_alert_{stock_id}_{selected_list}", use_container_width=True
                            ):
                                above_val = new_above if new_above > 0 else None
                                below_val = new_below if new_below > 0 else None
                                if update_alerts(stock_id, above_val, below_val, selected_list):
                                    st.success(t("watchlist.alert_saved"))
                                    st.rerun()
                                else:
                                    st.error(t("watchlist.alert_save_failed"))
                        with clear_col:
                            if st.button(
                                t("watchlist.btn_clear_alert"), key=f"wl_clear_alert_{stock_id}_{selected_list}", use_container_width=True
                            ):
                                if update_alerts(stock_id, None, None, selected_list):
                                    st.success(t("watchlist.alert_cleared"))
                                    st.rerun()
                                else:
                                    st.error(t("watchlist.alert_clear_failed"))

    # ── List Management (rename/delete) for the selected list ────────
    st.markdown("---\n")
    st.markdown(f"### {t('watchlist.list_management')}")
    mgmt_col1, mgmt_col2, mgmt_col3 = st.columns([2, 1, 1])
    with mgmt_col1:
        st.markdown(f"**{t('watchlist.current_list')}** {selected_list}")
    with mgmt_col2:
        # Rename button
        with st.popover(t("watchlist.btn_rename"), use_container_width=True):
            with st.form(f"rename_form_{selected_list}"):
                new_name = st.text_input(
                    t("watchlist.new_list_name_input"), placeholder=t("watchlist.new_list_name_placeholder"), key=f"rename_input_{selected_list}"
                )
                submitted = st.form_submit_button(t("watchlist.btn_confirm_rename"))
                if submitted and new_name:
                    if rename_list(selected_list, new_name):
                        st.success(t("watchlist.renamed_success", name=new_name))
                        st.rerun()
                    else:
                        st.error(t("watchlist.rename_failed"))
                elif submitted:
                    st.error(t("watchlist.new_name_required"))
    with mgmt_col3:
        # Delete button
        if st.button(t("watchlist.btn_delete_list"), key=f"delete_list_{selected_list}", use_container_width=True):
            # Prevent deleting the last list
            if len(list_names()) <= 1:
                st.error(t("watchlist.cannot_delete_last"))
            else:
                if delete_list(selected_list):
                    st.success(t("watchlist.deleted_success", name=selected_list))
                    st.rerun()
                else:
                    st.error(t("watchlist.delete_failed"))

    # ── Footer hint ────────────────────────────────────────────
    st.markdown("---\n")
    _info_card(
        t("watchlist.footer_title"),
        t("watchlist.footer_message"),
        "💡",
    )