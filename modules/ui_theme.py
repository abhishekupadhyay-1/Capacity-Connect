"""
modules/ui_theme.py — Production-grade Light & Dark corporate theme for Capacity Connect.
Architectural typography (Outfit + Plus Jakarta Sans), auto-hide top horizontal dock,
native Streamlit theme toggling, and clean visual tokens.
Zero gradients, zero glow effects, zero emoji clutter.
"""

import streamlit as st
import pandas as pd

NAV_ITEMS = [
    ("Dashboard", "dashboard"),
    ("Employees", "employees"),
    ("Add Appraisal", "appraisal"),
    ("Add Feedback", "feedback"),
    ("Suggestions", "suggestions"),
    ("Reports", "reports"),
    ("Assistant", "chatbot_page"),
]


def apply_theme(theme_mode: str = "light"):
    """
    Injects cohesive, high-precision corporate styling for either Light or Dark mode.
    Guarantees Material Symbols are never broken into raw ligature text like '_arrow_left'.
    """
    is_dark = (theme_mode or "").strip().lower() == "dark"

    # Semantic token palettes
    if is_dark:
        bg_app        = "#0a0d14"
        bg_card       = "#111622"
        bg_subtle     = "#1a2233"
        border_subtle = "#222c3f"
        border_strong = "#32415d"
        text_main     = "#f8fafc"
        text_muted    = "#94a3b8"
        text_subtle   = "#64748b"
        accent_bg     = "#2563eb"
        accent_text   = "#ffffff"
        accent_hover  = "#1d4ed8"
        btn_sec_bg    = "#111622"
        btn_sec_text  = "#f8fafc"
        btn_sec_border= "#28354d"
        btn_sec_hover = "#1a2334"
        btn_dis_bg    = "#111622"
        btn_dis_text  = "#475569"
        btn_dis_border= "#1e293b"
        dock_bg       = "#111622"
        dock_border   = "#222c3f"
        grid_dot      = "rgba(255, 255, 255, 0.08)"
        badge_top_bg  = "#064e3b"
        badge_top_txt = "#a7f3d0"
        badge_top_brd = "#059669"
        badge_mid_bg  = "#78350f"
        badge_mid_txt = "#fde68a"
        badge_mid_brd = "#d97706"
        badge_low_bg  = "#7f1d1d"
        badge_low_txt = "#fca5a5"
        badge_low_brd = "#dc2626"
        badge_na_bg   = "#1e293b"
        badge_na_txt  = "#94a3b8"
        badge_na_brd  = "#334155"
        chat_user_bg  = "#1a2233"
        chat_bot_bg   = "#111622"
    else:
        bg_app        = "#f8fafc"
        bg_card       = "#ffffff"
        bg_subtle     = "#f1f5f9"
        border_subtle = "#e2e8f0"
        border_strong = "#cbd5e1"
        text_main     = "#0f172a"
        text_muted    = "#525866"
        text_subtle   = "#868c98"
        accent_bg     = "#0f172a"
        accent_text   = "#ffffff"
        accent_hover  = "#1e293b"
        btn_sec_bg    = "#ffffff"
        btn_sec_text  = "#0f172a"
        btn_sec_border= "#cbd5e1"
        btn_sec_hover = "#f1f5f9"
        btn_dis_bg    = "#f1f5f9"
        btn_dis_text  = "#94a3b8"
        btn_dis_border= "#e2e8f0"
        dock_bg       = "#ffffff"
        dock_border   = "#e2e8f0"
        grid_dot      = "rgba(100, 116, 139, 0.12)"
        badge_top_bg  = "#ecfdf3"
        badge_top_txt = "#027a48"
        badge_top_brd = "#abefc6"
        badge_mid_bg  = "#fffaeb"
        badge_mid_txt = "#b54708"
        badge_mid_brd = "#fedf89"
        badge_low_bg  = "#fef3f2"
        badge_low_txt = "#b42318"
        badge_low_brd = "#fecdca"
        badge_na_bg   = "#f8f9fa"
        badge_na_txt  = "#475467"
        badge_na_brd  = "#eaecf0"
        chat_user_bg  = "#f0f2f5"
        chat_bot_bg   = "#ffffff"

    st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

    <style>
    /* ── Design Tokens ────────────────────────────────────────────────────────── */
    :root {{
        --font-display: 'Outfit', sans-serif;
        --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        --bg-app: {bg_app};
        --bg-card: {bg_card};
        --bg-subtle: {bg_subtle};
        --border-subtle: {border_subtle};
        --border-strong: {border_strong};
        --text-main: {text_main};
        --text-muted: {text_muted};
        --text-subtle: {text_subtle};
        --accent-bg: {accent_bg};
        --accent-text: {accent_text};
        --accent-hover: {accent_hover};
        --btn-sec-bg: {btn_sec_bg};
        --btn-sec-text: {btn_sec_text};
        --btn-sec-border: {btn_sec_border};
        --btn-sec-hover: {btn_sec_hover};
        --btn-dis-bg: {btn_dis_bg};
        --btn-dis-text: {btn_dis_text};
        --btn-dis-border: {btn_dis_border};
        --dock-bg: {dock_bg};
        --dock-border: {dock_border};
    }}

    /* ── Typography & Safe Icon Protection ───────────────────────────────────── */
    body, p, div, span, label, input, button, select, textarea {{
        font-family: var(--font-body);
    }}

    /* Protect Streamlit Material icons from losing font-family */
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"] span,
    .material-symbols-rounded,
    .material-symbols-outlined {{
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-feature-settings: 'liga' 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        display: inline-block !important;
        line-height: 1 !important;
    }}

    /* ── Base App Container ──────────────────────────────────────────────────── */
    .stApp {{ 
        background-color: var(--bg-app) !important; 
        background-image: radial-gradient({grid_dot} 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: var(--text-main) !important; 
    }}

    /* ── Animations ──────────────────────────────────────────────────────────── */
    @keyframes ccFadeInUp {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ── TOP HORIZONTAL NAVIGATION DOCK ────────────────────────────────────────── */
    #cc-top-dock {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        height: 58px !important;
        background-color: var(--dock-bg) !important;
        border-bottom: 1px solid var(--dock-border) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        z-index: 2147483647 !important;
        display: flex !important;
        align-items: center !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: none !important;
        pointer-events: auto !important;
    }}

    div:has(> #cc-top-dock),
    div:has(> * > #cc-top-dock),
    div:has(> * > * > #cc-top-dock),
    [data-testid="stElementContainer"]:has(#cc-top-dock),
    .element-container:has(#cc-top-dock) {{
        contain: none !important;
        transform: none !important;
        filter: none !important;
        will-change: auto !important;
        position: static !important;
        overflow: visible !important;
    }}

    .cc-dock-container {{
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        box-sizing: border-box;
    }}

    .cc-dock-brand {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        text-decoration: none !important;
        flex-shrink: 0;
    }}

    .cc-brand-title {{
        font-family: var(--font-display) !important;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-main);
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}

    .cc-brand-tag {{
        font-family: var(--font-display) !important;
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--text-muted);
        background: var(--bg-subtle);
        border: 1px solid var(--border-subtle);
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .cc-dock-nav {{
        display: flex;
        align-items: center;
        gap: 5px;
        overflow-x: auto;
        padding: 2px 0;
        margin-right: 120px; /* Space reserved for theme toggle button */
        -webkit-overflow-scrolling: touch;
    }}

    .cc-dock-nav::-webkit-scrollbar {{
        display: none;
    }}

    .cc-dock-item {{
        display: inline-flex;
        align-items: center;
        padding: 6px 13px;
        font-size: 0.82rem;
        font-weight: 600;
        font-family: var(--font-display) !important;
        letter-spacing: 0.01em;
        color: var(--text-muted) !important;
        text-decoration: none !important;
        border-radius: 6px;
        transition: all 0.15s ease;
        white-space: nowrap;
    }}

    .cc-dock-item:hover {{
        background-color: var(--bg-subtle);
        color: var(--text-main) !important;
    }}

    .cc-dock-item.active {{
        background-color: var(--accent-bg) !important;
        color: var(--accent-text) !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    }}

    /* ── Streamlit Theme Toggle Button (Integrated into top dock) ───────────── */
    .st-key-theme_toggle_btn,
    div[data-testid="stButton"].st-key-theme_toggle_btn {{
        position: fixed !important;
        top: 11px !important;
        right: 24px !important;
        z-index: 10000000 !important;
        width: auto !important;
        margin: 0 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: none !important;
    }}

    .st-key-theme_toggle_btn > button,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button {{
        height: 36px !important;
        padding: 0 14px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        font-family: var(--font-display) !important;
        border-radius: 6px !important;
        background-color: var(--bg-subtle) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border-strong) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.15s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        cursor: pointer !important;
    }}
    .st-key-theme_toggle_btn > button *,
    .st-key-theme_toggle_btn > button p,
    .st-key-theme_toggle_btn > button span,
    .st-key-theme_toggle_btn > button div,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button *,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button p,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button span,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button div {{
        color: var(--text-main) !important;
    }}

    .st-key-theme_toggle_btn > button:hover,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button:hover {{
        background-color: var(--border-strong) !important;
        border-color: var(--text-subtle) !important;
        color: var(--text-main) !important;
        transform: translateY(-1px) !important;
    }}
    .st-key-theme_toggle_btn > button:hover *,
    div[data-testid="stButton"].st-key-theme_toggle_btn > button:hover * {{
        color: var(--text-main) !important;
    }}

    /* ── Hide sidebar completely so dock is sole nav ─────────────────────────── */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}
    section[data-testid="stSidebar"] {{
        width: 0 !important;
        min-width: 0 !important;
    }}

    /* ── Main content breathing room ─────────────────────────────────────────── */
    .main .block-container,
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer {{
        padding-top: 5.2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px;
        margin: 0 auto;
    }}

    /* ── Header control ── */
    header[data-testid="stHeader"] {{
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }}

    /* ── Page Header ─────────────────────────────────────────────────────────── */
    .page-header {{
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        padding: 20px 24px;
        border-radius: 8px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        animation: ccFadeInUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    .page-header-title {{
        font-family: var(--font-display) !important;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text-main);
        letter-spacing: -0.02em;
    }}
    .page-header-sub {{
        font-size: 0.83rem;
        color: var(--text-muted);
        margin-top: 4px;
        font-weight: 400;
    }}

    /* ── Metric / KPI Cards ──────────────────────────────────────────────────── */
    .kpi-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        animation: ccFadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    .kpi-card:hover {{
        border-color: var(--border-strong);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    .kpi-value {{
        font-family: var(--font-display) !important;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-main);
        line-height: 1.05;
        letter-spacing: -0.02em;
    }}
    .kpi-label {{
        font-family: var(--font-display) !important;
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 8px;
        font-weight: 600;
    }}

    [data-testid="metric-container"] {{
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: var(--font-display) !important;
        color: var(--text-main) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: var(--font-display) !important;
        color: var(--text-muted) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* ── BASE BUTTON RESET & SECONDARY BUTTONS ─────────────────────────────────── */
    .stButton > button,
    button[kind="secondary"],
    button[data-testid="stBaseButton-secondary"] {{
        background-color: var(--btn-sec-bg) !important;
        color: var(--btn-sec-text) !important;
        border: 1px solid var(--btn-sec-border) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        font-family: var(--font-display) !important;
        letter-spacing: 0.01em !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }}
    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    button[kind="secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span,
    button[kind="secondary"] div,
    button[data-testid="stBaseButton-secondary"] *,
    button[data-testid="stBaseButton-secondary"] p,
    button[data-testid="stBaseButton-secondary"] span,
    button[data-testid="stBaseButton-secondary"] div {{
        color: var(--btn-sec-text) !important;
    }}
    .stButton > button:hover:not(:disabled),
    button[kind="secondary"]:hover:not(:disabled),
    button[data-testid="stBaseButton-secondary"]:hover:not(:disabled) {{
        background-color: var(--btn-sec-hover) !important;
        border-color: var(--border-strong) !important;
        color: var(--btn-sec-text) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
    }}
    .stButton > button:hover:not(:disabled) *,
    button[kind="secondary"]:hover:not(:disabled) * {{
        color: var(--btn-sec-text) !important;
    }}

    /* ── PRIMARY ACTION BUTTONS (Submit, Send, Download, Primary Actions) ──────── */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"],
    button[kind="primary"],
    button[data-testid="stBaseButton-primary"],
    [data-testid="stFormSubmitButton"] > button,
    .stDownloadButton > button {{
        background-color: var(--accent-bg) !important;
        color: var(--accent-text) !important;
        border: 1px solid var(--accent-bg) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        font-family: var(--font-display) !important;
        letter-spacing: 0.01em !important;
        padding: 0.5rem 1.4rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }}
    .stButton > button[kind="primary"] *,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    .stButton > button[kind="primary"] div,
    .stButton > button[data-testid="stBaseButton-primary"] *,
    .stButton > button[data-testid="stBaseButton-primary"] p,
    .stButton > button[data-testid="stBaseButton-primary"] span,
    .stButton > button[data-testid="stBaseButton-primary"] div,
    button[kind="primary"] *,
    button[kind="primary"] p,
    button[kind="primary"] span,
    button[kind="primary"] div,
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-primary"] span,
    button[data-testid="stBaseButton-primary"] div,
    [data-testid="stFormSubmitButton"] > button *,
    [data-testid="stFormSubmitButton"] > button p,
    [data-testid="stFormSubmitButton"] > button span,
    [data-testid="stFormSubmitButton"] > button div,
    .stDownloadButton > button *,
    .stDownloadButton > button p,
    .stDownloadButton > button span,
    .stDownloadButton > button div {{
        color: var(--accent-text) !important;
    }}
    .stButton > button[kind="primary"]:hover:not(:disabled),
    button[kind="primary"]:hover:not(:disabled),
    button[data-testid="stBaseButton-primary"]:hover:not(:disabled),
    [data-testid="stFormSubmitButton"] > button:hover:not(:disabled),
    .stDownloadButton > button:hover:not(:disabled) {{
        background-color: var(--accent-hover) !important;
        border-color: var(--accent-hover) !important;
        color: var(--accent-text) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12) !important;
    }}
    .stButton > button[kind="primary"]:hover:not(:disabled) *,
    button[kind="primary"]:hover:not(:disabled) *,
    [data-testid="stFormSubmitButton"] > button:hover:not(:disabled) *,
    .stDownloadButton > button:hover:not(:disabled) * {{
        color: var(--accent-text) !important;
    }}

    /* ── DISABLED BUTTON STATES ───────────────────────────────────────────────── */
    .stButton > button:disabled,
    button:disabled,
    button[disabled] {{
        background-color: var(--btn-dis-bg) !important;
        color: var(--btn-dis-text) !important;
        border-color: var(--btn-dis-border) !important;
        opacity: 0.7 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    .stButton > button:disabled *,
    .stButton > button:disabled p,
    .stButton > button:disabled span,
    button:disabled *,
    button:disabled p,
    button:disabled span {{
        color: var(--btn-dis-text) !important;
    }}

    /* ── Form Inputs, Selects, Textareas & Datepicker ───────────────────────── */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stDateInput input,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stDateInput"] input,
    div[data-baseweb="textarea"],
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"],
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"] input {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-strong) !important;
        color: var(--text-main) !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        font-size: 0.88rem !important;
        font-family: var(--font-body) !important;
    }}

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus,
    .stDateInput input:focus,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {{
        border-color: var(--accent-bg) !important;
        box-shadow: 0 0 0 1px var(--accent-bg) !important;
    }}

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {{
        color: var(--text-subtle) !important;
        opacity: 1 !important;
    }}

    [data-testid="stDateInput"] svg,
    div[data-baseweb="input"] svg {{
        fill: var(--text-muted) !important;
        color: var(--text-muted) !important;
    }}

    /* ── Selectbox & Dropdown Popovers ───────────────────────────────────────── */
    .stSelectbox > div > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {{
        background-color: var(--bg-card) !important;
        border-color: var(--border-strong) !important;
        border-radius: 6px !important;
    }}
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{
        color: var(--text-main) !important;
        font-family: var(--font-body) !important;
    }}
    div[data-baseweb="select"] svg {{
        fill: var(--text-muted) !important;
        color: var(--text-muted) !important;
    }}
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] span {{
        background-color: var(--bg-card) !important;
        color: var(--text-main) !important;
    }}
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {{
        background-color: var(--bg-subtle) !important;
        color: var(--text-main) !important;
    }}

    /* ── Datepicker Calendar Popover ────────────────────────────────────────── */
    div[data-baseweb="calendar"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-main) !important;
    }}
    div[data-baseweb="calendar"] *,
    div[data-baseweb="calendar"] div,
    div[data-baseweb="calendar"] span,
    div[data-baseweb="calendar"] button {{
        color: var(--text-main) !important;
    }}
    div[data-baseweb="calendar"] [aria-selected="true"],
    div[data-baseweb="calendar"] [aria-selected="true"] * {{
        background-color: var(--accent-bg) !important;
        color: var(--accent-text) !important;
    }}
    div[data-baseweb="calendar"] svg {{
        fill: var(--text-main) !important;
        color: var(--text-main) !important;
    }}

    /* ── Radio Buttons ───────────────────────────────────────────────────────── */
    .stRadio div[role="radiogroup"] label,
    .stRadio div[role="radiogroup"] label p,
    .stRadio div[role="radiogroup"] label span {{
        color: var(--text-main) !important;
        font-size: 0.88rem !important;
    }}

    /* ── Streamlit Slider Styling (Clean numbers & contrast) ──────────────────── */
    .stSlider {{
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }}

    /* Active slider track */
    div[data-testid="stSlider"] [data-baseweb="slider"] {{
        background: transparent !important;
    }}

    /* Slider Thumb (the circular draggable handle) */
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: #2563eb !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25) !important;
    }}

    /* Floating Score Value Label above Thumb (e.g. "75") */
    div[data-testid="stThumbValue"],
    [data-testid="stThumbValue"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 4px !important;
        padding: 3px 8px !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        font-family: var(--font-display) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
        min-width: 24px !important;
        text-align: center !important;
    }}
    div[data-testid="stThumbValue"] *,
    [data-testid="stThumbValue"] * {{
        color: var(--text-main) !important;
        font-weight: 700 !important;
    }}

    /* Min and Max tick labels (0 and 100) */
    div[data-testid="stTickBarMin"],
    div[data-testid="stTickBarMax"],
    [data-testid="stTickBarMin"],
    [data-testid="stTickBarMax"],
    div[data-testid="stSliderTickBar"] div {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        font-family: var(--font-display) !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}

    /* ── Universal Corporate Data Table ─────────────────────────────────────── */
    .cc-table-container {{
        width: 100%;
        overflow-x: auto;
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        background-color: var(--bg-card);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        margin: 8px 0 16px 0;
    }}
    .cc-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
        font-family: var(--font-body);
        color: var(--text-main);
        text-align: left;
    }}
    .cc-table th {{
        background-color: var(--bg-subtle);
        color: var(--text-muted);
        font-family: var(--font-display);
        font-weight: 700;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 10px 14px;
        border-bottom: 1px solid var(--border-subtle);
        white-space: nowrap;
    }}
    .cc-table td {{
        padding: 11px 14px;
        border-bottom: 1px solid var(--border-subtle);
        color: var(--text-main);
        vertical-align: middle;
    }}
    .cc-table tr:last-child td {{
        border-bottom: none;
    }}
    .cc-table tr:hover td {{
        background-color: var(--bg-subtle);
    }}

    /* ── DataFrames ─────────────────────────────────────────────────────────── */
    .stDataFrame,
    [data-testid="stDataFrame"],
    [data-testid="stDataFrameGlideDataGrid"] {{
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
        background-color: var(--bg-card) !important;
    }}

    /* ── Headings ────────────────────────────────────────────────────────────── */
    h1, h2, h3 {{
        font-family: var(--font-display) !important;
        color: var(--text-main) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}
    h4, h5, h6 {{
        font-family: var(--font-display) !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }}
    p, span, label {{
        color: var(--text-main);
    }}
    .text-muted, [data-testid="stCaptionContainer"] p {{
        color: var(--text-muted) !important;
    }}

    /* ── Expanders ───────────────────────────────────────────────────────────── */
    details > summary {{
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 6px !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
    }}
    details[open] > summary {{
        border-bottom: 1px solid var(--border-subtle) !important;
        border-radius: 6px 6px 0 0 !important;
    }}
    details > div {{
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
        color: var(--text-main) !important;
    }}

    /* ── Tabs ────────────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--bg-subtle) !important;
        border-radius: 6px;
        padding: 3px;
        gap: 3px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 5px;
        color: var(--text-muted) !important;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 6px 14px;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--bg-card) !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}

    /* ── Semantic Status Badges ──────────────────────────────────────────────── */
    .badge-top {{
        background: {badge_top_bg};
        color: {badge_top_txt};
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        font-family: var(--font-display) !important;
        letter-spacing: 0.02em;
        border: 1px solid {badge_top_brd};
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .badge-mid {{
        background: {badge_mid_bg};
        color: {badge_mid_txt};
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        font-family: var(--font-display) !important;
        letter-spacing: 0.02em;
        border: 1px solid {badge_mid_brd};
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .badge-low {{
        background: {badge_low_bg};
        color: {badge_low_txt};
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        font-family: var(--font-display) !important;
        letter-spacing: 0.02em;
        border: 1px solid {badge_low_brd};
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .badge-na {{
        background: {badge_na_bg};
        color: {badge_na_txt};
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        font-family: var(--font-display) !important;
        letter-spacing: 0.02em;
        border: 1px solid {badge_na_brd};
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}

    /* ── Chat Messages ───────────────────────────────────────────────────────── */
    .chat-user {{
        background: {chat_user_bg};
        border: 1px solid var(--border-subtle);
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        color: var(--text-main);
        animation: ccFadeInUp 0.25s ease both;
    }}
    .chat-bot {{
        background: {chat_bot_bg};
        border: 1px solid var(--border-subtle);
        padding: 14px 18px;
        border-radius: 8px;
        margin: 8px 0;
        color: var(--text-main);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        animation: ccFadeInUp 0.25s ease both;
    }}

    /* ── Avatars ─────────────────────────────────────────────────────────────── */
    .avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: var(--font-display) !important;
        font-weight: 700;
        font-size: 0.82rem;
        background: var(--bg-subtle);
        color: var(--text-main);
        border: 1px solid var(--border-subtle);
    }}

    /* Hide default footer and menu */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


def render_top_dock(active_page: str = "dashboard"):
    """
    Renders the modern top horizontal navigation dock with automatic
    hide-on-scroll-down and show-on-scroll-up behavior.
    """
    st.session_state["_dock_rendered"] = True
    norm_active = (active_page or "dashboard").strip().lower()

    mapping = {
        "dashboard": "dashboard",
        "employees": "employees",
        "add appraisal": "appraisal",
        "appraisal": "appraisal",
        "add feedback": "feedback",
        "feedback": "feedback",
        "suggestions": "suggestions",
        "reports": "reports",
        "assistant": "chatbot_page",
        "chatbot_page": "chatbot_page",
        "chatbot": "chatbot_page",
    }
    cur_key = mapping.get(norm_active, norm_active)

    links_html = []
    for label, url_path in NAV_ITEMS:
        is_active = (cur_key == url_path)
        cls = "cc-dock-item active" if is_active else "cc-dock-item"
        links_html.append(f'<a href="/{url_path}" class="{cls}" target="_self">{label}</a>')

    dock_html = (
        '<div id="cc-top-dock">'
        '  <div class="cc-dock-container">'
        '    <a href="/dashboard" class="cc-dock-brand" target="_self">'
        '      <span class="cc-brand-title">Capacity Connect</span>'
        '      <span class="cc-brand-tag">HR Portal</span>'
        '    </a>'
        '    <nav class="cc-dock-nav">'
        + "".join(links_html) +
        '    </nav>'
        '  </div>'
        '</div>'
    )

    st.markdown(dock_html, unsafe_allow_html=True)
    st.components.v1.html(
        """
        <script>
        (function() {
            try {
                const doc = window.parent.document;
                function pinElements() {
                    const dock = doc.getElementById('cc-top-dock');
                    if (dock && dock.parentElement !== doc.body) {
                        doc.body.prepend(dock);
                    }
                    const toggle = doc.querySelector('.st-key-theme_toggle_btn');
                    if (toggle && toggle.parentElement !== doc.body) {
                        doc.body.appendChild(toggle);
                    }
                }
                pinElements();
                setTimeout(pinElements, 80);
                setTimeout(pinElements, 300);
            } catch(e) {}
        })();
        </script>
        """,
        height=0,
    )


def get_plotly_layout(theme_mode: str = "light") -> dict:
    """Returns dynamic Plotly layout dictionary matching current theme."""
    is_dark = (theme_mode or "").strip().lower() == "dark"
    if is_dark:
        return dict(
            paper_bgcolor="#111622",
            plot_bgcolor="#111622",
            font=dict(color="#94a3b8", family="Plus Jakarta Sans, Outfit, sans-serif", size=12),
            margin=dict(l=10, r=10, t=32, b=10),
            xaxis=dict(gridcolor="#222c3f", zerolinecolor="#222c3f"),
            yaxis=dict(gridcolor="#222c3f", zerolinecolor="#222c3f"),
        )
    return dict(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#525866", family="Plus Jakarta Sans, Outfit, sans-serif", size=12),
        margin=dict(l=10, r=10, t=32, b=10),
        xaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#f1f5f9"),
        yaxis=dict(gridcolor="#f1f5f9", zerolinecolor="#f1f5f9"),
    )


def render_html_table(df, columns: list = None, column_labels: dict = None, height: int = None):
    """
    Renders a responsive, pixel-perfect corporate HTML table that seamlessly
    adapts to both Light and Dark mode using semantic CSS tokens.
    """
    if df is None or len(df) == 0:
        st.info("No records to display.")
        return

    cols = columns if columns is not None else list(df.columns)
    labels = column_labels or {}

    headers_html = "".join(f"<th>{labels.get(c, c)}</th>" for c in cols)
    
    rows_html = []
    for _, row in df.iterrows():
        cells = []
        for c in cols:
            val = row.get(c, "—")
            if pd.isna(val):
                cell_content = "—"
            else:
                sval = str(val).strip()
                c_lower = str(c).lower()
                if c_lower in ("category", "classification", "top category", "performance category", "performance_category"):
                    if sval == "Top Notch":
                        cell_content = '<span class="badge-top">Top Notch</span>'
                    elif sval == "Mediocre":
                        cell_content = '<span class="badge-mid">Mediocre</span>'
                    elif sval == "Below Average":
                        cell_content = '<span class="badge-low">Below Average</span>'
                    elif sval == "Not Appraised":
                        cell_content = '<span class="badge-na">Not Appraised</span>'
                    else:
                        cell_content = sval
                elif c_lower in ("nature", "feedback nature", "feedback_type", "type") and sval in ("Positive", "Improvement Needed", "General"):
                    if sval == "Positive":
                        cell_content = '<span class="badge-top">Positive</span>'
                    elif sval == "Improvement Needed":
                        cell_content = '<span class="badge-low">Improvement Needed</span>'
                    elif sval == "General":
                        cell_content = '<span class="badge-na">General</span>'
                    else:
                        cell_content = sval
                else:
                    cell_content = sval
            cells.append(f"<td>{cell_content}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    scroll_style = f"max-height:{height}px; overflow-y:auto;" if height else ""
    html = f"""
    <div class="cc-table-container" style="{scroll_style}">
      <table class="cc-table">
        <thead>
          <tr>{headers_html}</tr>
        </thead>
        <tbody>
          {''.join(rows_html)}
        </tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_header():
    """No-op fallback for backwards compatibility."""
    pass


def render_sidebar_footer():
    """No-op fallback for backwards compatibility."""
    pass
