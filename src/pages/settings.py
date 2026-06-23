import streamlit as st

from src.core.i18n import t
from src.view.pages.base_page import PageShell
from src.view.components.section import section_title, divider

_DEFAULT_PRICE_THRESHOLD = 5.0
_DEFAULT_VOLUME_THRESHOLD = 2.0
_DEFAULT_REVENUE_THRESHOLD = 10.0

_KEY_PRICE = "settings_price_threshold"
_KEY_VOLUME = "settings_volume_threshold"
_KEY_REVENUE = "settings_revenue_threshold"


def _init_defaults():
    if _KEY_PRICE not in st.session_state:
        st.session_state[_KEY_PRICE] = _DEFAULT_PRICE_THRESHOLD
    if _KEY_VOLUME not in st.session_state:
        st.session_state[_KEY_VOLUME] = _DEFAULT_VOLUME_THRESHOLD
    if _KEY_REVENUE not in st.session_state:
        st.session_state[_KEY_REVENUE] = _DEFAULT_REVENUE_THRESHOLD


def _reset_defaults():
    st.session_state[_KEY_PRICE] = _DEFAULT_PRICE_THRESHOLD
    st.session_state[_KEY_VOLUME] = _DEFAULT_VOLUME_THRESHOLD
    st.session_state[_KEY_REVENUE] = _DEFAULT_REVENUE_THRESHOLD


def _value_label_pricerange(value: float) -> str:
    if value < 3:
        return f"🔴 {value:.1f}% {t('settings.price.sensitive')}"
    elif value < 7:
        return f"🟡 {value:.1f}% {t('settings.price.moderate')}"
    else:
        return f"🟢 {value:.1f}% {t('settings.price.relaxed')}"


def _value_label_volume(value: float) -> str:
    if value < 1.5:
        return f"🔢 {value:.1f}x {t('settings.volume.sensitive')}"
    elif value < 3.0:
        return f"🔢 {value:.1f}x {t('settings.volume.moderate')}"
    else:
        return f"🔢 {value:.1f}x {t('settings.volume.relaxed')}"


def render_settings_page():
    _init_defaults()

    with PageShell(t("settings.title")):
        section_title(t("settings.risk_section"))
        PageShell.info(t("settings.risk_description"))
        divider()

        st.markdown(f"### 📈 {t('settings.price.heading')}")
        PageShell.info(t("settings.price.description"))

        price_threshold = st.slider(
            t("settings.price.slider_label"),
            min_value=0.0, max_value=20.0,
            value=st.session_state[_KEY_PRICE],
            step=0.5, help=t("settings.price.help_text"),
            key=f"{_KEY_PRICE}_slider",
        )
        st.session_state[_KEY_PRICE] = price_threshold

        if price_threshold < 0:
            PageShell.error(t("settings.price.error_negative"))
            st.session_state[_KEY_PRICE] = 0.0
        elif price_threshold == 0:
            PageShell.warning(t("settings.price.warn_zero"))

        st.caption(_value_label_pricerange(price_threshold))

        st.markdown(
            f"<div style='background-color:#F8F9FA; border-radius:8px; padding:12px 16px; "
            f"font-size:14px;'>"
            f"✅ <b>{t('settings.price.current_threshold', value=price_threshold)}</b> &nbsp;│&nbsp; "
            f"{t('settings.price.trigger_when', value=price_threshold)}"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        st.markdown(f"### 📊 {t('settings.volume.heading')}")
        PageShell.info(t("settings.volume.description"))

        volume_threshold = st.slider(
            t("settings.volume.slider_label"),
            min_value=1.0, max_value=5.0,
            value=st.session_state[_KEY_VOLUME],
            step=0.1, help=t("settings.volume.help_text"),
            key=f"{_KEY_VOLUME}_slider",
        )
        st.session_state[_KEY_VOLUME] = volume_threshold

        if volume_threshold < 1.0:
            PageShell.error(t("settings.volume.error_below_one"))
            st.session_state[_KEY_VOLUME] = 1.0

        st.caption(_value_label_volume(volume_threshold))
        st.caption(t("settings.volume.de_scoped"))
        st.markdown("")

        st.markdown(f"### 💰 {t('settings.revenue.heading')}")
        PageShell.info(t("settings.revenue.description"))

        revenue_threshold = st.slider(
            t("settings.revenue.slider_label"),
            min_value=0.0, max_value=50.0,
            value=st.session_state[_KEY_REVENUE],
            step=1.0, help=t("settings.revenue.help_text"),
            key=f"{_KEY_REVENUE}_slider",
        )
        st.session_state[_KEY_REVENUE] = revenue_threshold

        if revenue_threshold < 0:
            PageShell.error(t("settings.revenue.error_negative"))
            st.session_state[_KEY_REVENUE] = 0.0
        elif revenue_threshold == 0:
            PageShell.warning(t("settings.revenue.warn_zero"))

        if revenue_threshold < 5:
            st.caption(t("settings.revenue.caption_very_sensitive"))
        elif revenue_threshold < 15:
            st.caption(t("settings.revenue.caption_moderate"))
        else:
            st.caption(t("settings.revenue.caption_relaxed"))

        st.markdown(
            f"<div style='background-color:#F8F9FA; border-radius:8px; padding:12px 16px; "
            f"font-size:14px;'>"
            f"✅ <b>{t('settings.revenue.current_threshold', value=revenue_threshold)}</b> &nbsp;│&nbsp; "
            f"{t('settings.revenue.trigger_when', value=revenue_threshold)}"
            f"</div>",
            unsafe_allow_html=True,
        )

        divider()

        if st.button(t("settings.reset_btn"), use_container_width=False):
            _reset_defaults()
            st.rerun()

        st.markdown("")
        PageShell.info(t("settings.info_box"))
