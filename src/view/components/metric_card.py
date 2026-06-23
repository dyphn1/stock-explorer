import streamlit as st


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
