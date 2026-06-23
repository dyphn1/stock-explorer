"""
股識 Stock Explorer
Streamlit entry point — thin bootstrap.
Architecture: Controller → View → Model (MVC pattern).
"""

import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
from src.core.i18n import t
from src.controller.app_controller import AppController

st.set_page_config(
    page_title=t("app.title"),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

AppController().run()
