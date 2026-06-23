import streamlit as st


def section_title(title: str):
    if not title:
        return
    first_char = title[0]
    code = ord(first_char)
    if code >= 0x2300 or (first_char.isalpha() and first_char.isascii()):
        st.markdown(f"### {title}")
    else:
        st.markdown(f"### 📊 {title}")


def divider():
    st.markdown("---")
