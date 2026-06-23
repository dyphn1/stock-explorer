import streamlit as st


def loading_spinner(text: str = "Loading..."):
    return st.spinner(text)


def error_banner(message: str):
    st.error(message)


def warning_banner(message: str):
    st.warning(message)


def info_banner(message: str):
    st.info(message)


def empty_state(message: str, icon: str = "📭"):
    st.info(f"{icon} {message}")
