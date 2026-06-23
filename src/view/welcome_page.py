import streamlit as st
from src.core.i18n import t


def render_welcome_page():
    st.markdown(f"""
    <div style="text-align:center;padding:2rem;">
        <h1 style="font-size:1.5rem;">📊 {t("main.home.title")}</h1>
        <p style="color:#7F8C8D;margin-top:0.5rem;">{t("main.home.lead1")}</p>
        <p style="color:#5A6B7D;margin-top:0.5rem;font-style:italic;">{t("main.home.quick_hint")}</p>
    </div>
    """, unsafe_allow_html=True)
