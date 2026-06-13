"""
設定頁 — C07 自訂事件閾值骨架
風險閾值設定：價格變動、成交量放大、營收變化
完整自訂 UI 將於 Sprint 17 實作
"""

import streamlit as st

# ── Default threshold constants ──
_DEFAULT_PRICE_THRESHOLD = 5.0       # percent
_DEFAULT_VOLUME_THRESHOLD = 2.0      # x average
_DEFAULT_REVENUE_THRESHOLD = 10.0    # percent

# Session state keys
_KEY_PRICE = "settings_price_threshold"
_KEY_VOLUME = "settings_volume_threshold"
_KEY_REVENUE = "settings_revenue_threshold"


def _init_defaults() -> None:
    """Initialise threshold values in session_state if not already present."""
    if _KEY_PRICE not in st.session_state:
        st.session_state[_KEY_PRICE] = _DEFAULT_PRICE_THRESHOLD
    if _KEY_VOLUME not in st.session_state:
        st.session_state[_KEY_VOLUME] = _DEFAULT_VOLUME_THRESHOLD
    if _KEY_REVENUE not in st.session_state:
        st.session_state[_KEY_REVENUE] = _DEFAULT_REVENUE_THRESHOLD


def _reset_defaults() -> None:
    """Reset all thresholds back to their default values."""
    st.session_state[_KEY_PRICE] = _DEFAULT_PRICE_THRESHOLD
    st.session_state[_KEY_VOLUME] = _DEFAULT_VOLUME_THRESHOLD
    st.session_state[_KEY_REVENUE] = _DEFAULT_REVENUE_THRESHOLD


def _value_label_pricerange(value: float) -> str:
    """Return a human-readable label for the price threshold slider."""
    if value < 3:
        return f"🔴 {value:.1f}% （敏感）"
    elif value < 7:
        return f"🟡 {value:.1f}% （適中）"
    else:
        return f"🟢 {value:.1f}% （寬鬆）"


def _value_label_volume(value: float) -> str:
    """Return a human-readable label for the volume threshold slider."""
    if value < 1.5:
        return f"🔢 {value:.1f}x （敏感）"
    elif value < 3.0:
        return f"🔢 {value:.1f}x （適中）"
    else:
        return f"🔢 {value:.1f}x （寬鬆）"


def render_settings_page() -> None:
    """Render the Settings page — C07 skeleton."""
    st.title("⚙️ 設定")

    # Ensure defaults are in session_state
    _init_defaults()

    # ── Risk Threshold Section ──
    st.markdown("## 風險閾值設定")
    st.markdown(
        "調整以下閾值來控制事件偵測的敏感度。"
        "較低的閾值會觸發較多提醒，較高的閾值僅在重大變化時提醒。"
    )

    st.markdown("---")

    # ── Price change threshold ──
    st.markdown("### 📈 股價變動閾值")
    st.markdown("當股價單日漲跌幅超過此百分比時，觸發事件提醒。")

    price_threshold = st.slider(
        "股價變動閾值（%）",
        min_value=0.0,
        max_value=20.0,
        value=st.session_state[_KEY_PRICE],
        step=0.5,
        help="預設值 5%。偵測到單日漲跌幅超過此值時，會標記為異常事件。",
        key=f"{_KEY_PRICE}_slider",
    )
    st.session_state[_KEY_PRICE] = price_threshold

    # Validation: negative is impossible via slider (min=0) but guard explicitly
    if price_threshold < 0:
        st.error("❌ 閾值不可為負數，請調整為 0 以上的值。")
        price_threshold = 0.0
        st.session_state[_KEY_PRICE] = 0.0
    elif price_threshold == 0:
        st.warning("⚠️ 設為 0% 將觸發所有價格變動事件。")

    st.caption(_value_label_pricerange(price_threshold))
    st.markdown("")

    # ── Volume spike threshold ──
    st.markdown("### 📊 成交量放大閾值")
    st.markdown("當成交量超過過去 20 日均量的此倍數時，觸發事件提醒。")

    volume_threshold = st.slider(
        "成交量放大閾值（倍數）",
        min_value=1.0,
        max_value=5.0,
        value=st.session_state[_KEY_VOLUME],
        step=0.1,
        help="預設值 2x。成交量超過 20 日均量此倍數時，會標記為異常事件。",
        key=f"{_KEY_VOLUME}_slider",
    )
    st.session_state[_KEY_VOLUME] = volume_threshold

    if volume_threshold < 1.0:
        st.error("❌ 閾值不可低於 1.0 倍（即為平均量本身）。")
        volume_threshold = 1.0
        st.session_state[_KEY_VOLUME] = 1.0

    st.caption(_value_label_volume(volume_threshold))
    st.markdown("")

    # ── Revenue change threshold ──
    st.markdown("### 💰 營收變化閾值")
    st.markdown("當營收月增率或年增率超過此百分比時，觸發事件提醒。")

    revenue_threshold = st.slider(
        "營收變化閾值（%）",
        min_value=0.0,
        max_value=50.0,
        value=st.session_state[_KEY_REVENUE],
        step=1.0,
        help="預設值 10%。營收變化超過此值時，會標記為異常事件。",
        key=f"{_KEY_REVENUE}_slider",
    )
    st.session_state[_KEY_REVENUE] = revenue_threshold

    if revenue_threshold < 0:
        st.error("❌ 閾值不可為負數。")
        revenue_threshold = 0.0
        st.session_state[_KEY_REVENUE] = 0.0
    elif revenue_threshold == 0:
        st.warning("⚠️ 設為 0% 將觸發所有營收變動事件。")

    if revenue_threshold < 5:
        st.caption("🔴 非常敏感 — 幾乎每次營收公告都會觸發")
    elif revenue_threshold < 15:
        st.caption("🟡 適中 — 只在明顯變化時觸發")
    else:
        st.caption("🟢 寬鬆 — 僅在劇烈變化時觸發")

    st.markdown("---")

    # ── Reset button ──
    if st.button("🔄 重設為預設值", use_container_width=False):
        _reset_defaults()
        st.rerun()

    st.markdown("")

    # ── Info box: coming soon ──
    st.info("🚧 更多自訂選項即將推出（Sprint 17）：產業別閾值、法人動向敏感度、訊息通知頻率等。")
