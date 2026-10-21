"""
pages/dashboard.py — Main dashboard for Capacity Connect.
Clean, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from modules.performance import (
    get_dashboard_stats,
    classify_performance,
    CATEGORY_TOP_NOTCH, CATEGORY_MEDIOCRE,
    CATEGORY_BELOW_AVERAGE, CATEGORY_NOT_APPRAISED,
    CATEGORY_COLORS,
)
from modules.data_manager import get_all_departments, get_all_designations
from modules.ui_theme import get_plotly_layout, render_html_table

# ── Fallback Plotly theme ─────────────────────────────────────────────────────
_PLOTLY = get_plotly_layout("light")


def _kpi(col, value, label):
    """Render a clean, flat KPI card without emojis or gradients."""
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def show_dashboard():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("dashboard")

    cur_theme = st.session_state.get("theme_mode", "light")
    chart_layout = get_plotly_layout(cur_theme)
    is_dark = cur_theme == "dark"
    # ── Page Header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Executive Performance Dashboard</div>
      <div class="page-header-sub">Workforce appraisal benchmarks, department distributions, and ratings overview</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Load Data (Cached) ────────────────────────────────────────────────────
    with st.spinner("Loading metrics..."):
        stats    = get_dashboard_stats()
        enriched = stats["enriched_df"]

    # ── KPI Summary Row ───────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    _kpi(k1, stats["total_employees"],    "Total Employees")
    _kpi(k2, f"{stats['avg_score']:.1f}", "Average Score")
    _kpi(k3, stats["top_notch"],          "Top Notch")
    _kpi(k4, stats["mediocre"],           "Mediocre")
    _kpi(k5, stats["below_average"],      "Below Average")
    _kpi(k6, stats["not_appraised"],      "Not Appraised")

    st.markdown(f"<div style='font-size:0.75rem; color:var(--text-muted); text-align:right; margin-top:8px;'>"
                f"Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}</div>",
                unsafe_allow_html=True)
    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Charts Row 1 ──────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Performance Category Distribution")
        cat_data = stats["category_counts"]
        if cat_data:
            labels = list(cat_data.keys())
            values = list(cat_data.values())
            colors = [CATEGORY_COLORS.get(l, "#64748b") for l in labels]
            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.55,
                marker=dict(colors=colors, line=dict(color="#111622" if is_dark else "#ffffff", width=2)),
                textfont=dict(size=12, color="#f8fafc" if is_dark else "#0f172a"),
                hovertemplate="%{label}: <b>%{value}</b> (%{percent})<extra></extra>",
            ))
            fig.update_layout(
                **chart_layout, height=290,
                legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No appraisal data available yet.")

    with c2:
        st.markdown("#### Department Average Score")
        dept_stats = stats["dept_stats"]
        if not dept_stats.empty:
            sorted_d = dept_stats.sort_values("avg_score", ascending=True)
            dept_bar_color = "#38bdf8" if is_dark else "#0f172a"
            fig = px.bar(
                sorted_d, x="avg_score", y="department", orientation="h",
                color_discrete_sequence=[dept_bar_color],
                text="avg_score",
                labels={"avg_score": "Average Score", "department": ""},
                custom_data=["employee_count"],
            )
            fig.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside",
                textfont_color="#f8fafc" if is_dark else "#0f172a",
                hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<br>Headcount: %{customdata[0]}<extra></extra>",
            )
            fig.update_layout(
                **chart_layout, height=290,
            )
            fig.update_xaxes(range=[0, 108], title="")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Charts Row 2 ──────────────────────────────────────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Score Distribution")
        appraised = enriched.dropna(subset=["latest_score"])
        if not appraised.empty:
            fig = px.histogram(
                appraised, x="latest_score", nbins=12,
                color_discrete_sequence=["#3b82f6"],
                labels={"latest_score": "Score", "count": "Employees"},
            )
            fig.add_vline(x=50, line_dash="dot", line_color="#d97706",
                          annotation_text="50 (Mediocre)", annotation_font_color="#d97706",
                          annotation_position="top left")
            fig.add_vline(x=80, line_dash="dot", line_color="#059669",
                          annotation_text="80 (Top Notch)", annotation_font_color="#059669",
                          annotation_position="top left")
            fig.update_layout(**chart_layout, height=270)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c4:
        st.markdown("#### Top 10 High Achievers")
        appraised = enriched.dropna(subset=["latest_score"])
        if not appraised.empty:
            top10 = appraised.nlargest(10, "latest_score")[["name","latest_score","department"]].copy()
            achiever_bar_color = "#38bdf8" if is_dark else "#0f172a"
            fig = px.bar(
                top10.sort_values("latest_score"),
                x="latest_score", y="name", orientation="h",
                color_discrete_sequence=[achiever_bar_color],
                text="latest_score",
                labels={"latest_score": "Score", "name": ""},
                custom_data=["department"],
            )
            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside",
                textfont_color="#f8fafc" if is_dark else "#0f172a",
                hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<br>Dept: %{customdata[0]}<extra></extra>",
            )
            fig.update_layout(
                **chart_layout, height=270,
            )
            fig.update_xaxes(range=[0, 110])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Employee Directory ────────────────────────────────────────────────────
    st.markdown("#### Workforce Directory")

    f1, f2, f3, f4 = st.columns([2, 2, 2, 2])
    with f1:
        search = st.text_input("Search", placeholder="Search by name or ID...",
                               label_visibility="collapsed")
    with f2:
        dept_filter = st.selectbox("Department", ["All Departments"] + get_all_departments(),
                                   label_visibility="collapsed")
    with f3:
        desig_filter = st.selectbox("Designation", ["All Roles"] + get_all_designations(),
                                    label_visibility="collapsed")
    with f4:
        cat_filter = st.selectbox("Category",
            ["All Categories", CATEGORY_TOP_NOTCH, CATEGORY_MEDIOCRE,
             CATEGORY_BELOW_AVERAGE, CATEGORY_NOT_APPRAISED],
            label_visibility="collapsed")

    filtered = enriched.copy()
    if search:
        mask = (filtered["name"].str.contains(search, case=False, na=False)
                | filtered["employee_id"].str.contains(search, case=False, na=False))
        filtered = filtered[mask]
    if dept_filter  != "All Departments": filtered = filtered[filtered["department"]          == dept_filter]
    if desig_filter != "All Roles":       filtered = filtered[filtered["designation"]         == desig_filter]
    if cat_filter   != "All Categories":  filtered = filtered[filtered["performance_category"] == cat_filter]

    # Format table display
    disp = filtered[["employee_id","name","department","designation",
                     "latest_score","performance_category","latest_appraisal_date"]].copy()
    disp["latest_appraisal_date"] = disp["latest_appraisal_date"].apply(
        lambda x: x.strftime("%d %b %Y") if hasattr(x,"strftime") and pd.notna(x) else "—")
    disp["latest_score"] = disp["latest_score"].apply(
        lambda x: f"{x:.1f}" if pd.notna(x) else "—")
    disp.columns = ["Employee ID","Name","Department","Designation","Score","Category","Last Appraisal"]
    disp = disp.reset_index(drop=True)

    st.caption(f"Displaying {len(disp)} of {len(enriched)} employee records")
    render_html_table(disp, height=360)


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_dashboard()
