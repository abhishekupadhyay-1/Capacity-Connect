"""
app.py — Capacity Connect main entry point.
Clean, modern corporate layout with top horizontal dock navigation:
- /dashboard
- /employees
- /appraisal
- /feedback
- /suggestions
- /reports
- /chatbot_page
"""

import streamlit as st
import os
import sys

# ── Ensure project root is on the Python path ─────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules.ui_theme import apply_theme, render_top_dock
from pages.dashboard import show_dashboard
from pages.employees import show_employees
from pages.appraisal import show_appraisal
from pages.feedback import show_feedback
from pages.suggestions import show_suggestions
from pages.reports import show_reports
from pages.chatbot_page import show_chatbot

# ── Set overall page configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="Capacity Connect",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme Mode Management (Light / Dark) ──────────────────────────────────────
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
st.session_state["_dock_rendered"] = False

# ── Inject cohesive aesthetic CSS matching active theme mode ─────────────────
apply_theme(theme_mode=st.session_state.theme_mode)

# ── Theme Toggle Button via Streamlit (Anchored seamlessly in top dock) ──────
is_dark = st.session_state.theme_mode == "dark"
toggle_icon = "☀️" if is_dark else "🌙"
toggle_label = f"{toggle_icon} {'Light' if is_dark else 'Dark'}"
if st.button(toggle_label, key="theme_toggle_btn", help="Toggle between Light and Dark mode"):
    st.session_state.theme_mode = "light" if is_dark else "dark"
    st.rerun()

# ── Explicit Programmatic Page Router ─────────────────────────────────────────
def route_page(page: str):
    """
    Page router supporting session_state and direct programmatic page dispatch.
    Ensures explicit routing branches for all pages in Capacity Connect.
    """
    if page == "Dashboard":
        from pages.dashboard import show_dashboard
        show_dashboard()
    elif page == "Employees":
        from pages.employees import show_employees
        show_employees()
    elif page == "Add Appraisal":
        from pages.appraisal import show_appraisal
        show_appraisal()
    elif page == "Add Feedback":
        from pages.feedback import show_feedback
        show_feedback()
    elif page == "Suggestions":
        from pages.suggestions import show_suggestions
        show_suggestions()
    elif page == "Reports":
        from pages.reports import show_reports
        show_reports()
    elif page in ("Chatbot", "Assistant") or page == "Chatbot":
        from pages.chatbot_page import show_chatbot
        show_chatbot()


# ── Define native Streamlit URL endpoints with clean Material icons ──────────
pages = [
    st.Page(show_dashboard,   title="Dashboard",      icon=":material/dashboard:",   url_path="dashboard",    default=True),
    st.Page(show_employees,   title="Employees",      icon=":material/group:",       url_path="employees"),
    st.Page(show_appraisal,   title="Add Appraisal",  icon=":material/rate_review:", url_path="appraisal"),
    st.Page(show_feedback,    title="Add Feedback",   icon=":material/comment:",     url_path="feedback"),
    st.Page(show_suggestions, title="Suggestions",    icon=":material/lightbulb:",   url_path="suggestions"),
    st.Page(show_reports,     title="Reports",        icon=":material/analytics:",   url_path="reports"),
    st.Page(show_chatbot,     title="Assistant",      icon=":material/smart_toy:",   url_path="chatbot_page"),
]

# ── Setup navigation router with top horizontal dock ─────────────────────────
pg = st.navigation(pages, position="hidden")
active_path = getattr(pg, "url_path", None) or "dashboard"
render_top_dock(active_page=active_path)
pg.run()

