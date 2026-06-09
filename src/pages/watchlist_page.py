"""
關注列表頁 — 顯示使用者關注的股票與 ETF
提供摘要卡片、價格列表、警示狀態與移除功能
支援多個命名清單
"""

import streamlit as st
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

def _render_watchlist_page(client: FinMindClient):
    """關注列表主頁"""
    st.markdown("## 📋 我的關注")
    st.markdown("管理您關注的股票與 ETF，掌握最新價格與警示狀態")
    st.markdown("---\n")

    # --- List Management Section ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 清單選擇")
    with col2:
        if st.button("➕ 新增清單", key="btn_new_list", use_container_width=True):
            st.session_state["show_new_list_popup"] = True

    # Popup for creating new list
    if st.session_state.get("show_new_list_popup", False):
        with st.popover("新增清單", use_container_width=True):
            with st.form("new_list_form"):
                new_list_name = st.text_input("清單名稱", placeholder="請輸入清單名稱")
                submitted = st.form_submit_button("建立清單")
                if submitted and new_list_name:
                    if create_list(new_list_name):
                        st.success(f"已建立清單：{new_list_name}")
                        st.session_state["show_new_list_popup"] = False
                        st.rerun()
                    else:
                        st.error("清單名稱已存在或建立失敗")
                elif submitted:
                    st.error("請輸入清單名稱")

    # Get list of list names
    list_name_options = list_names()
    # Ensure there's always at least one list (預設清單)
    if not list_name_options:
        # If no lists exist, create default list
        create_list("預設清單")
        list_name_options = ["預設清單"]

    # Let user select a list to view/edit
    selected_list = st.selectbox(
        "選擇要檢視的清單",
        options=list_name_options,
        index=0 if list_name_options else 0,
        key="selected_watchlist",
    )

    st.markdown("---\n")

    # If no lists (should not happen because we ensured at least one)
    if not selected_list:
        st.warning("目前沒有任何清單")
        return

    # Load watchlist for selected list
    entries = load_watchlist(selected_list)
    total = len(entries)
    stocks_count = sum(1 for e in entries if e.get("type") == "stock")
    etfs_count = sum(1 for e in entries if e.get("type") == "etf")

    # ── Summary Cards ──────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""\
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #3498DB;">
                <div style="font-size:2rem;font-weight:700;color:#2C3E50;">{total}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">關注總數</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""\
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #E74C3C;">
                <div style="font-size:2rem;font-weight:700;color:#2C3E50;">{stocks_count}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">個股</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""\
            <div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;text-align:center;border-left:4px solid #27AE60;">
                <div style="font-size:2rem;font-weight:700;color:#2C3E50;">{etfs_count}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;">ETF</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---\n")

    # ── Empty State ────────────────────────────────────────────
    if total == 0:
        st.markdown(
            """\
            <div style="background:linear-gradient(135deg,#EBF5FB,#EAF2F8);border-radius:14px;
                        padding:2rem 1.6rem;border-left:5px solid #2E86C1;text-align:center;margin-top:1rem;">
                <div style="font-size:1.3rem;font-weight:700;color:#1B4F72;margin-bottom:0.8rem;">
                    📌 尚未加入任何關注標的
                </div>
                <div style="font-size:0.92rem;color:#2C3E50;line-height:1.7;">
                    您可以透過以下方式將股票或 ETF 加入關注：<br><br>
                    1️⃣ 前往 <b>🔍 分類瀏覽</b> 找到有興趣的股票<br>
                    2️⃣ 前往 <b>📊 ETF 瀏覽</b> 探索各類 ETF<br>
                    3️⃣ 在個股名片頁點擊「加入關注」按鈕<br><br>
                    加入後即可在此查看最新價格與設定警示價格 🔔
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Still show list management buttons for the empty list
        # We'll show rename/delete buttons below
        pass
    else:
        # ── Fetch Latest Prices ────────────────────────────────────
        with st.spinner("載入最新價格…"):
            try:
                summary = get_watchlist_summary(client, selected_list)
            except Exception as e:
                st.error(f"無法取得價格資料：{e}")
                summary = []

        if not summary:
            st.warning("無法取得價格資料，請稍後再試。")
            # Still show list management
        else:
            # ── Watchlist Table ────────────────────────────────────────
            st.markdown("### 📈 價格概覽")

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
                    badge = '<span style="background:#27AE60;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-right:0.4rem;">ETF</span>'
                else:
                    badge = '<span style="background:#3498DB;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-right:0.4rem;">股票</span>'

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
                    alert_parts.append(f"🔺 高於 {alert_above:,.2f}")
                if alert_below is not None:
                    alert_parts.append(f"🔻 低於 {alert_below:,.2f}")
                alert_str = " ｜ ".join(alert_parts) if alert_parts else "未設定"

                # Alert triggered indicator
                if alert_triggered:
                    alert_badge = '<span style="background:#E74C3C;color:white;padding:0.15rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-left:0.4rem;">⚠️ 已觸發</span>'
                else:
                    alert_badge = ""

                # Card-style row
                st.markdown(
                    f"""\
                    <div style="background:#F8F9FA;border-radius:10px;padding:1rem 1.2rem;
                                margin-bottom:0.5rem;border-left:4px solid #3498DB;">
                        <div style="display:flex;align-items:center;justify-content:space-between;">
                            <div style="flex:3;">
                                {badge}
                                <span style="font-weight:600;color:#2C3E50;font-size:1rem;">{name}</span>
                                <span style="color:#7F8C8D;font-size:0.8rem;margin-left:0.4rem;">{stock_id}</span>
                                {alert_badge}
                            </div>
                            <div style="flex:1;text-align:right;">
                                <span style="font-size:1.1rem;font-weight:700;color:#2C3E50;">{price_str}</span>
                            </div>
                            <div style="flex:1;text-align:right;">
                                {change_str}
                            </div>
                            <div style="flex:2;text-align:right;">
                                <span style="font-size:0.8rem;color:#7F8C8D;">{alert_str}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Action buttons row
                col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
                with col1:
                    if st.button("查看名片", key=f"wl_card_{stock_id}_{selected_list}", use_container_width=True):
                        navigate_to(page="名片", stock_id=stock_id)
                with col2:
                    if st.button("移除", key=f"wl_remove_{stock_id}_{selected_list}", use_container_width=True):
                        if remove_from_watchlist(stock_id, selected_list):
                            st.toast("🗑️ 已移除關注")
                            st.rerun()
                        else:
                            st.error("移除失敗")
                with col3:
                    with st.popover("🔔 設定提醒", key=f"wl_alert_{stock_id}_{selected_list}"):
                        st.markdown(f"**{name}** ({stock_id})")
                        st.markdown("---\n")

                        # Show current alert values
                        current_above = alert_above if alert_above is not None else 0.0
                        current_below = alert_below if alert_below is not None else 0.0

                        new_above = st.number_input(
                            "上限價格（高於此價提醒）",
                            min_value=0.0,
                            value=current_above,
                            step=0.5,
                            key=f"wl_above_{stock_id}_{selected_list}",
                        )
                        new_below = st.number_input(
                            "下限價格（低於此價提醒）",
                            min_value=0.0,
                            value=current_below,
                            step=0.5,
                            key=f"wl_below_{stock_id}_{selected_list}",
                        )

                        save_col, clear_col = st.columns(2)
                        with save_col:
                            if st.button(
                                "儲存", key=f"wl_save_alert_{stock_id}_{selected_list}", use_container_width=True
                            ):
                                above_val = new_above if new_above > 0 else None
                                below_val = new_below if new_below > 0 else None
                                if update_alerts(stock_id, above_val, below_val, selected_list):
                                    st.success("提醒已儲存")
                                    st.rerun()
                                else:
                                    st.error("儲存失敗")
                        with clear_col:
                            if st.button(
                                "清除提醒", key=f"wl_clear_alert_{stock_id}_{selected_list}", use_container_width=True
                            ):
                                if update_alerts(stock_id, None, None, selected_list):
                                    st.success("提醒已清除")
                                    st.rerun()
                                else:
                                    st.error("清除失敗")

    # ── List Management (rename/delete) for the selected list ────────
    st.markdown("---\n")
    st.markdown("### 清單管理")
    mgmt_col1, mgmt_col2, mgmt_col3 = st.columns([2, 1, 1])
    with mgmt_col1:
        st.markdown(f"**目前清單：** {selected_list}")
    with mgmt_col2:
        # Rename button
        with st.popover("✏️ 重命名", use_container_width=True):
            with st.form(f"rename_form_{selected_list}"):
                new_name = st.text_input(
                    "新清單名稱", placeholder="請輸入新清單名稱", key=f"rename_input_{selected_list}"
                )
                submitted = st.form_submit_button("確認重命名")
                if submitted and new_name:
                    if rename_list(selected_list, new_name):
                        st.success(f"已重命名為：{new_name}")
                        st.rerun()
                    else:
                        st.error("重命名失敗：名稱可能已存在或操作失敗")
                elif submitted:
                    st.error("請輸入新清單名稱")
    with mgmt_col3:
        # Delete button
        if st.button("🗑️ 刪除清單", key=f"delete_list_{selected_list}", use_container_width=True):
            # Prevent deleting the last list
            if len(list_names()) <= 1:
                st.error("無法刪除最後一個清單")
            else:
                if delete_list(selected_list):
                    st.success(f"已刪除清單：{selected_list}")
                    st.rerun()
                else:
                    st.error("刪除失敗")

    # ── Footer hint ────────────────────────────────────────────
    st.markdown("---\n")
    st.markdown(
        """\
        <div style="background:#FEF9E7;border-radius:10px;padding:0.8rem 1.2rem;
                    border-left:4px solid #F1C40F;">
            <div style="font-size:0.85rem;color:#7F8C8D;">
                💡 <b>提示</b>：在個股名片頁可以設定警示價格，當股價觸及警示價格時，
                此頁面會顯示 <span style="background:#E74C3C;color:white;padding:0.1rem 0.4rem;border-radius:3px;font-size:0.75rem;">⚠️ 已觸發</span> 標記。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )