from collections.abc import Callable

import streamlit as st


class PageShell:
    def __init__(self, title: str, subtitle: str = ""):
        self._title = title
        self._subtitle = subtitle

    def __enter__(self):
        if self._title:
            st.markdown(f"## {self._title}")
        if self._subtitle:
            st.markdown(f"*{self._subtitle}*")
        st.markdown("---")
        self._container = st.container()
        self._container.__enter__()
        return self

    def __exit__(self, *args):
        self._container.__exit__(*args)

    @staticmethod
    def divider():
        st.markdown("---")

    @staticmethod
    def section(title: str):
        first_char = title[0]
        code = ord(first_char)
        if code >= 0x2300 or (first_char.isalpha() and first_char.isascii()):
            st.markdown(f"### {title}")
        else:
            st.markdown(f"### 📊 {title}")

    @staticmethod
    def columns(count: int, *, vertical_alignment: str = "top"):
        return st.columns(count, vertical_alignment=vertical_alignment)

    @staticmethod
    def info(message: str):
        st.info(message)

    @staticmethod
    def warning(message: str):
        st.warning(message)

    @staticmethod
    def error(message: str):
        st.error(message)

    @staticmethod
    def spinner(text: str):
        return st.spinner(text)

    @staticmethod
    def plotly_chart(fig, **kwargs):
        st.plotly_chart(fig, use_container_width=True, **kwargs)

    @staticmethod
    def metric_card(title: str, value: str = "", description: str = "", icon: str = "", color: str = "#3498DB"):
        if value:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1.2rem;border:1px solid #E1E4E8;border-left:4px solid {color};margin:0.5rem 0;">
                <div style="font-size:0.85rem;color:#7F8C8D;">{title}</div>
                <div style="font-size:1.6rem;font-weight:700;color:#2C3E50;">{value}</div>
                {f'<div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{description}</div>' if description else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid {color};margin:0.5rem 0;">
                <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
                <div style="font-size:0.9rem;color:#7F8C8D;margin-top:0.3rem;line-height:1.6;">{description}</div>
            </div>
            """, unsafe_allow_html=True)
